"Logic to set up the module."
import setuptools # type: ignore

setuptools.setup(
    install_requires=[
		"precommit-diffcheck==1.1",
		"six==1.12.0",
		"unidiff==0.5.5",
	],
	extras_require={
		"develop": [
			"mypy",
			"nose2",
			"pylint",
		]
	},
)
