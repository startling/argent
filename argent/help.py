#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import basename
from sys import argv
from clint.textui import columns


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


def parent_list(parser, l):
    """Given a parser and a list so far, recursively determine the parentage
    of the parser.
    """
    # if the parser doesn't have a parent.
    if not parser.parent:
        # and if it was called from the command line
        if argv[0]:
            # use the name it was called as from the command line.
            l.insert(0, basename(argv[0]))
            return l
        # otherwise, just insert the parser's name attribute.
        else:
            l.insert(0, parser.name)
            return l
    # if the parser does have a parent...
    else:
        # insert this parser's name
        l.insert(0, parser.name)
        # and call this function on the parent.
        return parent_list(parser.parent, l)


def word_description(words_and_descriptions):
    """Given a list of two-tuples, the first item being a word and the second
    being a description of that word, return a neatly-formatted string with
    the words and descriptions in columns.
    """
    lines = []
    for word, description in words_and_descriptions:
        lines.append(columns([" ", 2], [word, 13], [description, 65]))
    return "\n".join(lines)


class HelpFormatter(object):
    "A class for formatting help messages, given an argent.Parser instance."
    def __init__(self, parser):
        self.parser = parser

    def usage(self):
        "Print a helpful message regarding the usage of this program."
        # determine the start of the usage string...
        usage = "usage: %s " % " ".join(parent_list(self.parser, []))
        # list all of the flags, optional args, and necessary args.
        usage += format_list("[%s] ",
                [f.name for f in self.parser.flags])
        usage += format_list("%s ",
                [f.name for f in self.parser.necessary_args])
        usage += format_list("[%s] ",
                [f.name for f in self.parser.optional_args])
        print(usage)

    def print_subcommands(self):
        print("Subcommands:")
        print word_description([(n, f.description) for n, f
            in self.parser.subparsers.items()])

    def print_flags(self):
        print("optional flags:")
        print word_description([(", ".join(f.synonym_names), f.description) for
            f in self.parser.flags])

    def print_optional(self):
        print("optional arguments:")
        print word_description(
                [(f.name, f.description) for f in self.parser.optional_args])

    def print_necessary(self):
        print("necessary arguments:")
        print word_description(
                [(f.name, f.description) for f in self.parser.necessary_args])

    def __call__(self):
        "Create and print a help message for `self.parser`."
        self.usage()
        print("")
        print(self.parser.description)
        # if there are any flags, list them.
        if self.parser.flags:
            print("")
            self.print_flags()
        # if there are any subparsers, list them.
        if self.parser.subparsers:
            print("")
            self.print_subcommands()
        # print necessary and optional arguments, if there are any.
        if self.parser.necessary_args:
            print("")
            self.print_necessary()
        if self.parser.optional_args:
            print("")
            self.print_optional()
