from distutils.core import setup
import argent

setup(
    name = "argent",
    version = argent.__version__,
    author = "startling",
    author_email = "tdixon51793@gmail.com",
    description = "A module for parsing command-line arguments and flags; simpler than argparse.",
    packages = ["argent"],
    install_requires = ["Clint"],
)
