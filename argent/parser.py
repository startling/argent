# -*- coding: utf-8 -*-

from sys import argv
import inspect


def nothing(*args, **kwargs):
    """A function that does nothing. This is used because it's nice for
    Parser objects to always have a function as their obj.function attribute.
    """
    pass


class Parser(object):
    """A parser for command-line flags and arguments."""
    def __init__(self, function=nothing, flags=[]):
        # a dictionary of subparsers;
        # the keys are their names, the values are the actual objects.
        self.subparsers = {}
        # this is the function that will get all of the arguments passed
        # to the parser.
        self.function = function
        # and these are the flags that it can take
        self.flags = flags

    @classmethod
    def from_function(cls, fn):
        """Create a parser from a function. This could also be a decorator."""
        parser = cls(fn)
        # figure out the parser's name.
        parser.name = fn.__name__
        # get the arguments the function expects
        args, _, _, _ = inspect.getargspec(fn)
        # flags are the ones that start with an underscore:
        parser.flags = [a for a in args if a.startswith("_")]
        # arguments are the ones that don't.
        parser.args = [a for a in args if not a.startswith("_")]
        # return it.
        return parser

    def subparse(self, fn):
        """A decorator that creates a new subparser in self.subparsers
        from the decorated function.
        """
        # create a parser from this function...
        subparser = Parser.from_function(fn)
        # add it to the `subparsers` dictionary.
        self.subparsers[subparser.name] = subparser
        # return the Parser object for the subparser.
        return subparser

    def first_subcommand(self, arguments):
        """Given a list of arguments, return the first argument that
        corresponds to a subcommand and its index in the list. If none
        of them do, return None.
        """
        for n, a in enumerate(arguments):
            if a in self.subparsers.keys():
                return a, n
        return None

    def parse(self, arguments):
        """Given some command-line arguments, decide what to do with them."""
        # get the first subcommand of the arguments, or None.
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
            self.run(arguments)

    def run(self, arguments):
        """Given some command-line arguments, run this Parser's function
        on them. Note that this will __not__ call any subparsers.
        """
        # get flags from arguments -- flags are anything that starts with
        # a dash ("-"). Instead of the flag's actual name, use its name
        # with underscores rather than dashes.
        flags = [a.replace("-", "_") for a in arguments if a.startswith("-")]
        # strip the flags from the arguments list:
        arguments = [a for a in arguments if not a.startswith("-")]
        # check that there aren't any flags here that aren't
        # defined in self.flags; i.e., check that the given flags
        # is a subset of the possible flags.
        if not set(self.flags) >= set(flags):
            raise NameError("Illegal arguments.")
        # create a dictionary of used flags here, to be passed as kwargs.
        flag_dict = dict(((f, f in flags) for f in self.flags))
        # call the function with the arguments and flags.
        self.function(*arguments, **flag_dict)

    def command_line(self):
        """Get arguments from `sys.argv` and parse them."""
        # since the first argument is the name of the file, ignore it.
        arguments = argv[1:]
        self.parse(arguments)
