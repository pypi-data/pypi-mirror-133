from setuptools import setup

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "readme.md").read_text()
setup(name="Pandaspretty",
version="1.0.0",
url = 'https://github.com/ayushkumarsingh2422005/PandasPretty',
description="Powerful package to prettify DataFrame into table.",
long_description=long_description,
long_description_content_type='text/markdown',
author="Ayush Kumar Singh",
packages=["Pandaspretty"],
install_requires=['pandas'])