from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 10):
    sys.exit("This version of DorkScan requires python >= 3.10")

with open("README.md") as fh:
    long_description = fh.read()

with open("requirements.txt") as fh:
    requirements = fh.readlines()

setup(
    name="dorkscan",
    version="0.1.1",
    description="Automate sending dorked queries to search engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://gitlab.com/unkwn1/dorkscan",
    project_urls={
        "Issues": "https://gitlab.com/unkwn1/dorkscan/-/issues",
        "Source": "https://gitlab.com/unkwn1/dorkscan/-/tree/main",
    },
    author="unkwn1",
    author_email="unkwn1@tutanota.com",
    license="MIT",
    keywords="dorking, google dork, web parser, web scraping",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=requirements,
    packages=find_packages(),
)
