import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="esllib",
	version="0.0.1",
	author="Tim Gremalm",
	author_email="tim@gremalm.se",
	description="ESL(Electronic Shelf Label) library for 433Mhz e-ink price tags",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/TimGremalm/python-esllib",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)