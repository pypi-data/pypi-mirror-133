import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

VERSION = "v0.1.1"
DESCRIPTION = "Retrieve local, global, external ipaddress."

#This call to setup() does all the work
setup(
    name ="LOLLOL",
    version = VERSION,
    description = DESCRIPTION,
    long_description = README,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ABIRHOSSAIN10",
    author="ABIR HOSSAIN",
    author_email = "abirhossain200019@gmail.com",
    license = "MIT",
    keywords=['python'],
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ],
    packages = find_packages(),
    include_package_data = True,
    install_requires = ['mechanize', 'requests'],
)
