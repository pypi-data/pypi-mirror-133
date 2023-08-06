"Custom formatter used to capture detail about failures."
import logging
import typing

import unidiff

import cpplinthook.cpplint

LOGGER = logging.getLogger(__name__)


class FileFormatter(cpplinthook.cpplint.OutputFormatter): # type: ignore
	"""Basic formatter for showing all failures in a file.

	Since we don't control the names from cpplint we just disable some warnings
	from pylint on the various weird names, parameters, etc.
	"""
	def __init__(self):
		self.error_count = 0
		self.has_shown_header = False

	def _Format(self, # pylint: disable=invalid-name, too-many-arguments
		filename: typing.Text,
		linenum: int,
		category:typing.Text,
		confidence: int,
		message: typing.Text):
		"Format a single error in a file."
		if not self.has_shown_header:
			print("{}:".format(filename))
			self.has_shown_header = True
		print("\t{filename}:{linenum}:  {message}  [{category}] [{confidence}]".format(
			category=category,
			confidence=confidence,
			filename=filename,
			linenum=linenum,
			message=message,
		))
		self.error_count += 1

	def FinishedFile(self, filename): # pylint: disable=invalid-name
		"Called when a file is entirely finished."

	def Finished(self): # pylint: disable=invalid-name, no-self-use
		"Called when finished. Not sure how it differs from FinishedFile."
		for category, count in \
			cpplinthook.cpplint.state().errors_by_category.items():
			print("Category '{}' errors found: {}".format(category, count))

class DiffFormatter(FileFormatter):
	"""A formatter for showing errors against a diff."""
	def __init__(self, patch: unidiff.PatchedFile):
		super().__init__()
		self.filename = patch.target_file[2:]
		self.has_failure_outside_diff = False
		self.added_lines: typing.Set[int] = set()
		for hunk in patch:
			# Include only added lines in our analysis
			for i, line in enumerate(hunk.target_lines()):
				if line.is_context:
					continue
				if line.is_added:
					self.added_lines.add(hunk.target_start + i)
		LOGGER.debug(
			"Only accepting failures in %s on lines: %s",
			self.filename, sorted(list(self.added_lines)))


	def _Format(self, # pylint: disable=invalid-name, too-many-arguments
		filename: typing.Text,
		linenum: int,
		category: typing.Text,
		confidence: int,
		message: typing.Text):
		"""Log message is they match against the patch."""
		assert filename == self.filename, "{} is not {}".format(filename, self.filename)
		# Always allow failures on some magical lines since these are hard-coded into cpplint
		if linenum in self.added_lines or linenum == 0:
			super()._Format(filename, linenum, category, confidence, message)
			self.error_count += 1
		else:
			self.has_failure_outside_diff = True
			LOGGER.debug("Found failure outside of diff on line %d: %s", linenum, message)

	def FinishedFile(self, filename):
		"""Message to show when a file is done being processed."""
		if self.has_failure_outside_diff:
			print("\tFailures outside your changes are present in this file. "
				"Run 'pre-commit run cpplint --files {}' to see them".format(filename))
