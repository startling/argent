from distutils.core import setup
import argent

setup(
    name = "argent",
    version = argent.__version__,
    author = "startling",
    author_email = "tdixon51793@gmail.com",
    url = "https://github.com/startling/argent",
    keywords = ["command-line", "arguments", "flags", "argparse"]
    description = "Parse command-line arguments using introspective magic.",
    packages = ["argent"],
    install_requires = ["Clint"],
    classifiers = [
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta",]
)
