import pathlib

from setuptools import setup, find_packages

from tempfolderpy import __version__

VERSION = __version__
DESCRIPTION = 'For python, light-weight and cross-platform temporary folder manager'
# LONG_DESCRIPTION = 'A package inspired by django model system and implemented that system for mssql via using pyodbc'
HERE = pathlib.Path(__file__).parent

# The text of the README file
# TODO: Add a README.md
# README = (HERE / "README.md").read_text()

# Setting up
setup(
    name="tempfolderpy",
    version=VERSION,
    author="Mehmet Berkay Özbay",
    author_email="<berkayozbay64@gmail.com>",
    url="https://github.com/bilinenkisi/tempy",
    description=DESCRIPTION,
    # long_description=README,
    long_description_content_type="text/markdown",

    packages=find_packages(),
    install_requires=["filelock==3.4.2"],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'tempfolderpy', "TEMPFOLDERPY", "tempfolder-python", "tempfolder manager for python"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
