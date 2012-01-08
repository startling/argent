# -*- coding: utf-8 -*-

from sys import argv

def nothing(*args, **kwargs):
    """A function that does nothing. This is used because it's nice for `Parser` objects
    to always have a function as their obj.function attribute. 
    """
    pass

class Parser(object):
    """A parser for command-line flags and arguments."""
    def __init__(self, function=nothing, flags=[]):
        # a dictionary of subparsers; the keys are their names, the values are the actual objects.
        self.subparsers = {}
        # this is the function that will get all of the arguments passed to the parser.
        self.function = function
        # and these are the flags that it can take
        self.flags = flags

    @classmethod
    def from_function(cls, fn):
        """Create a parser from a function. This could also be a decorator."""
        parser = cls(fn)
        # figure out the parser's name.
        parser.name = fn.__name__
        # return it.
        return parser
    
    def subparse(self, flags=[]):
        """A decorator that creates a new subparser in self.subparsers from the function."""
        def add_subparser(fn):
            # create a parser from this function...
            subparser = Parser.from_function(fn)
            # give it the flags it should have.
            subparser.flags = flags
            # add it to the `subparsers` dictionary.
            self.subparsers[subparser.name] = subparser
            # return the Parser object for the subparser.
            return subparser
        return add_subparser
    
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
            # get flags from arguments -- flags are anything that starts with `-`.
            flags = [a for a in arguments if a.startswith("-")]
            # strip the flags from the arguments list:
            arguments = [a for a in arguments if not a.startswith("-")]
            # check that there aren't any flags here that aren't defined in self.flags:
            if not set(self.flags) >= set(flags):
                raise NameError("Illegal arguments.")
            # create a dictionary of used flags here, to be passed as kwargs.
            # (instead of the flag's actual name, use instead its name without dashes)
            flag_dict = dict(((f.replace("-", ""), True) for f in flags))
            # call the function with the arguments and flags.
            self.function(*arguments, **flag_dict)

    def command_line(self):
        """Get arguments from `sys.argv` and parse them."""
        # since the first argument is the name of the file, ignore it.
        arguments = argv[1:]
        self.parse(arguments)

