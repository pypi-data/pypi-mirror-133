"Main entrypoint logic for cpplint hook."
import argparse
import logging
import os
import subprocess
import sys
import typing

import precommit_diffcheck
import unidiff

import cpplinthook.cpplint
import cpplinthook.formatters

def main() -> None:
	"Main entrypoint for the hook."
	parser = argparse.ArgumentParser()
	parser.add_argument("--fail",
		action="store_true", help="Force failure, useful to see logging.")
	parser.add_argument("--root",
		help="The root directory to use when calculating header guard names.")
	parser.add_argument("--header-guard-base",
		help="An additional base to add to header guards.")
	parser.add_argument("--verbose", action="store_true", help="Show verbose logging.")
	parser.add_argument("filenames", nargs="*", help="The file(s) to lint.")
	args = parser.parse_args()

	logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING)

	_configure_cpplint(args.root, args.header_guard_base)
	has_errors = _process(args.filenames)
	sys.exit(1 if has_errors or args.fail else 0)


def _configure_cpplint(root: str, base: str) -> None:
	"""Set up configuration for cpplint.

	Args:
		root: The root of the code repository for the purpose of calculating header guards.
	"""
	cpplinthook.cpplint.state().ResetErrorCounts() # type: ignore
	if base:
		cpplinthook.cpplint.state().SetHeaderGuardBase(base) # type: ignore
	if root:
		root = os.path.abspath(root)
		cpplinthook.cpplint.state().SetRoot(root) # type: ignore


def _process(filenames: typing.Iterable[str]) -> bool:
	"""Process the files in the current changeset.

	This will print information on the cpplint violations of the current
	changeset. That is, either the currently staged files or the last
	commit.

	Returns true if there are lint violations.

	Args:
		filenames: The filenames to consider, or all of them if an empty list.
	"""
	patchset = precommit_diffcheck.get_diff_or_content(filenames)

	error_count = 0
	for patch in patchset:
		output_formatter = cpplinthook.formatters.DiffFormatter(patch)
		# Remove 'b/' from git patch format
		if patch.target_file.startswith("b/"):
			target = patch.target_file[2:]
		elif patch.target_file == "/dev/null":
			continue
		cpplinthook.cpplint.ProcessFile(target, 0, output_formatter) # type: ignore
		error_count += output_formatter.error_count

	print("Total errors found: {}".format(error_count))
	return error_count > 0
