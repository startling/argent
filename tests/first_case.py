#!/usr/bin/env python
"""This is a test case for argent's argument parsing."""

from argent.parser import Parser

# create a parser.
@Parser.from_function
def parser():
    "A test parser using argent."
    # This is where things will go if there are no subcommands.
    return "Some stuff."

# Add a subparser for the subcommand `hello`.
# So, `python thisfile.py hello` runs this function.
@parser.subparse
# anything that starts with an underscore is a boolean flag;
# anything that doesn't is a positional argument.
# docstrings will be used for help messages.
def hello(__f, something="hello"):
    "Return `something` if '--f' flag is given; else 'goodbye'"
    if __f:
        return something
    else:
        return "goodbye"

if __name__ == "__main__":
    # Parse the arguments from the command line and run accordingly.
    parser.command_line()
