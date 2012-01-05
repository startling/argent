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
        # a dictionary of subparsers; the keys are their names, the values are the actual objects:
        self.subparsers = defaultdict(Parser)
        # this is the function that will get all of the arguments passed to the parser.
        self.function = function

    def subparse(self, fn):
        """A decorator that creates a new subparser in self.subparsers from the function."""
        self.subparsers[fn.__name__].function = fn
    
    def parse(self, args):
        """Given some command-line arguments, do stuff with them."""
        pass
