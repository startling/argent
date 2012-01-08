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

    def parse(self, arguments):
        """Given some command-line arguments, decide what to do with them."""
        # if the first argument corresponds to a subparser....
        if len(arguments) > 0 and arguments[0] in self.subparsers.keys():
            subcommand = arguments[0]
            # pass all of the subcommands after the subcommand name
            args_to_pass = arguments[1:]
            # give them to the subparser, to parse
            return self.subparsers[subcommand].parse(args_to_pass)
        # otherwise, run self.function with the arguments
        else:
            return self.run(arguments)

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
            raise NameError("Illegal flags.")
        # raise an error if there are more arguments given than what
        # the function expects.
        elif not len(self.args) >= len(arguments):
            raise NameError("Illegal arguments")
        else:
            # create a dictionary of used flags here, to be passed as kwargs.
            flag_dict = dict(((f, f in flags) for f in self.flags))
            # create a dictionary of possible args to used args here.
            # NOTE: since zip wants lists to be of equal length, it'll throw
            # out invalid arguments. We need to check before then!
            arg_dict = dict(((a, b) for a, b in zip(self.args, arguments)))
            # call the function with a combined dictionary of args and flags.
            return self.function(**dict(arg_dict.items() + flag_dict.items()))

    def command_line(self):
        """Get arguments from `sys.argv` and parse them."""
        # since the first argument is the name of the file, ignore it.
        arguments = argv[1:]
        return self.parse(arguments)
