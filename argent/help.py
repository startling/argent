#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv


def format_list(string, list):
    """Given a string and a list, return the string with each list item
    interpolated into as by %.

    >>> format_list("(%d) ", [1, 2, 3])
    "(1) (2) (3)"
    """
    total = ""
    for item in list:
        total += string % item
    return total


def parent_list(parser, string):
    """Given a parser and a string so far, recursively determine the parentage
    of the parser.
    """
    # if the parser doesn't have a parent.
    if not parser.parent:
        # and if it was called from the command line
        if argv[0]:
            # use the name it was called as from the command line.
            return "%s %s" % (argv[0], string)
        # otherwise, just use the parser's name attribute.
        else:
            return "%s %s" % (self.name, string)
    # if the parser does have a parent
    else:
        return parent_list(parser.parent, "%s %s" % (parser.name, string))


class HelpFormatter(object):
    "A class for formatting help messages, given an argent.Parser instance."
    def __init__(self, parser):
        self.parser = parser

    def usage(self):
        "Print a helpful message regarding the usage of this program."
        # determine the start of the usage string...
        usage = "usage: %s" % parent_list(self.parser, "")
        # list all of the flags, optional args, and necessary args.
        usage += format_list("[%s] ",
                [f.replace("_", "-") for f in self.parser.flags])
        usage += format_list("[%s] ", self.parser.optional_args)
        usage += format_list("%s ", self.parser.necessary_args)
        print(usage)

    def __call__(self):
        "Create and print a help message for `self.parser`."
        self.usage()
        print("")
        print(self.parser.function.__doc__)
