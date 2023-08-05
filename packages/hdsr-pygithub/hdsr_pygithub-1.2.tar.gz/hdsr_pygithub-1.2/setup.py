from os import path
from setuptools import find_packages
from setuptools import setup


# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

version = "1.2"

install_requires = [
    "pathlib",
    "typing",
    "PyGithub",
    "python-dateutil",
]

tests_require = [
    "pytest",
]

setup(
    name="hdsr_pygithub",
    packages=find_packages(include=["hdsr_pygithub", "hdsr_pygithub.*"]),
    version=version,
    license="MIT",
    description="An interface for interacting with hdsr github repos",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="Renier Kramer",
    author_email="renier.kramer@hdsr.nl",
    url="https://github.com/hdsr-mid/hdsr_pygithub",
    download_url=f"https://github.com/hdsr-mid/hdsr_pygithub/archive/v{version}.tar.gz",
    keywords=["interface", "interaction", "github", "files", "hdsr"],
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={"test": tests_require},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
