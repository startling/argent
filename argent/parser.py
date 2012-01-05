# -*- coding: utf-8 -*-

from collections import defaultdict

def nothing(*args, **kwargs):
    """A function that does nothing. This is used because it's nice for `Parser` objects
    to always have a function as their obj.function attribute. 
    """
    pass

class Parser(object):
    """A parser for command-line flags and arguments."""
    def __init__(self, function=nothing):
        # a dictionary of subparsers; the keys are their names, the values are the actual objects.
        self.subparsers = defaultdict(Parser)
        # this is the function that will get all of the arguments passed to the parser.
        self.function = function

    def subparse(self, fn):
        """A decorator that creates a new subparser in self.subparsers from the function."""
        self.subparsers[fn.__name__].function = fn
    
    def first_subcommand(self, arguments):
        """Given a list of arguments, return the first argument that corresponds to a subcommand
        and its index in the list. If none of them do, return None.
        """
        for n, a in enumerate(arguments):
            if a in self.subparsers.keys():
                return a, n
        return None

    def parse(self, arguments):
        """Given some command-line arguments, decide what to do with them."""
        # get the first subcommand of the arguments, or None if there aren't any.
        subcommand = self.first_subcommand(arguments)
        # if there is a subcommand:
        if subcommand:
            (name, index) = subcommand
            # pass all of the subcommands after the subcommand name
            args_to_pass = arguments[index + 1:]
            # give them to the subparser, to parse
            self.subparsers[name].parse(args_to_pass)
        # otherwise, run self.function with the arguments
        else:
            self.function(*arguments)

