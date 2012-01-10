# -*- coding: utf-8 -*-

from sys import argv
from argent.help import HelpFormatter
from argent.arguments import arguments_from_function, help_arg
from itertools import chain


def nothing(*args, **kwargs):
    """A function that does nothing. This is used because it's nice for
    Parser objects to always have a function as their obj.function attribute.
    """
    pass


class Parser(object):
    """A parser for command-line flags and arguments."""
    def __init__(self, function=nothing, help=HelpFormatter):
        # a dictionary of subparsers;
        # the keys are their names, the values are the actual objects.
        self.subparsers = {}
        # this is the function that will get all of the arguments passed
        # to the parser.
        self.function = function
        # presumably, a parser created this way is _not_ a subparser.
        self.parent = None
        # and these are the flags that it can take
        self.flags = []
        # this is the formatter that the parser will use for its help:
        self.help = help(self)

    @classmethod
    def from_function(cls, fn, **kwargs):
        """Create a parser from a function. This could also be a decorator."""
        parser = cls(fn, **kwargs)
        # figure out the parser's name.
        parser.name = fn.__name__
        # the description is the first line of the docstring...
        if fn.__doc__:
            parser.description = fn.__doc__.split("\n")[0]
        else:
            parser.description = ""
        # get the arguments the function expects
        args = arguments_from_function(fn)
        # flags are the ones that start with an underscore:
        parser.flags = [a for a in args if a.flag]
        # arguments are the ones that don't.
        parser.args = [a for a in args if not a.flag]
        # determine which arguments are necessary and which aren't.
        parser.necessary_args = [a for a in parser.args if a.necessary]
        parser.optional_args = [a for a in parser.args if not a.necessary]
        # return the parser...
        return parser

    def subparse(self, fn):
        """A decorator that creates a new subparser in self.subparsers
        from the decorated function.
        """
        # create a parser from this function
        # with its parent's help formatter class
        subparser = Parser.from_function(fn, help=type(self.help))
        # set the subparser's `parent` attribute to this parser.
        subparser.parent = self
        # add it to the `subparsers` dictionary.
        self.subparsers[subparser.name] = subparser
        # add this parser's help to it.
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
        # a dash ("-").
        flags = [a for a in arguments if a.startswith("-")]
        # strip the flags from the arguments list:
        arguments = [a for a in arguments if not a.startswith("-")]
        # check that there aren't any flags here that aren't
        # defined in self.flags; i.e., check that the given flags
        # is a subset of the possible flags.
        if not set(chain(
                    *[f.synonym_names for f in self.flags])) >= set(flags):
            raise NameError("Illegal flags.")
        elif help_arg.is_in(flags):
            self.help()
        # raise an error if there are more arguments given than what
        # the function expects.
        elif not len(self.args) >= len(arguments):
            raise NameError("Illegal arguments")
        # raise an error if there are fewer arguments than are necessary.
        elif len(arguments) < len(self.necessary_args):
            raise NameError("Not enough arguments.")
        else:
            # create a dictionary of used flags here, to be passed as kwargs.
            flag_dict = dict(((f.underscored, f.is_in(flags)) for f
                in self.flags if f != help_arg))
            # create a dictionary of possible args to used args here.
            # NOTE: since zip wants lists to be of equal length, it'll throw
            # out invalid arguments. We need to check before then!
            arg_dict = dict(
                    ((a.underscored, b) for a, b in zip(self.args, arguments)))
            # call the function with a combined dictionary of args and flags.
            return self.function(**dict(arg_dict.items() + flag_dict.items()))

    def command_line(self):
        """Get arguments from `sys.argv` and parse them."""
        # since the first argument is the name of the file, ignore it.
        arguments = argv[1:]
        return self.parse(arguments)
