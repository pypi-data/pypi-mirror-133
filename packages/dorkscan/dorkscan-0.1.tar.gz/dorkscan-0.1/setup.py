from setuptools import setup, find_packages

with open("README.md") as fh:
    long_description = fh.read()

with open("requirements.txt") as fh:
    requirements = fh.readlines()

setup(
    name="dorkscan",
    version="0.1",
    description="An atypical search engine parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://gitlab.com/unkwn1/dorkscan",
    project_urls={
        "Issues": "https://gitlab.com/unkwn1/dorkscan/-/issues",
        "Source": "https://gitlab.com/unkwn1/dorkscan/-/tree/main",
        "DorkScanner": "https://github.com/balgogan/dorkscanner",
        "GitHub": "https://github.com/jessefogarty/",
    },
    author="unkwn1",
    author_email="unkwn1@tutanota.com",
    license="MIT",
    keywords="dorking, google dork, web parser, web scraping",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=requirements,
    packages=find_packages(),
)
