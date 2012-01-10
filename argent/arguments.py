# -*- coding: utf-8 -*-

from inspect import getargspec
import re

def arguments_from_function(fn):
    """Given a function, use introspective magic to make inferences about 
    its arguments.
    """
    arguments = [help_arg]
    args, _, _, defaults = getargspec(fn)
    # find the descriptions of flags and arguments from the docstring:
    # any string after the first that starts with a name + ":"
    # has description following it.
    descriptions = {}
    for m in re.finditer(r'^\s*(\w+?):\s?(.+?)\s*$', fn.__doc__, re.MULTILINE):
        descriptions[m.group(1)] = m.group(2)
    # if defaults is None, make it a zero-length tuple, rather than None.
    # this way we can get its length.
    if not defaults:
        defaults = ()
    # pad the defaults list with Nones in order to give it the same number
    # of items as args, so we can zip them.
    defaults = ([None] * (len(args) - len(defaults))) + list(defaults)
    # for each argument, make an Argument object out of it and append it.
    for arg, default in zip(args, defaults):
        arg_object = Argument(arg, default, descriptions.get(arg, ""))
        arguments.append(arg_object)
    return arguments

class Argument(object):
    "A class to handle arguments and their metadata."
    def __init__(self, name, default=None, description=""):
        # `self.name` is what we get but with no underscores and all dashes.
        self.name = name.replace("_", "-")
        # `self.underscored` is the opposite.
        self.underscored = name.replace("-", "_")
        # this is the default value; can be None if there isn't one.
        self.default = default
        # if the name starts with an underscore or dash, it's a flag,
        # and so the default should be False
        if self.name.startswith("-"):
            self.flag = True
            self.default = False
        else:
            self.flag = False
        # if default is None, it's necessary
        if default == None:
            self.necessary = True
        # if there is a default, it's not necessary.
        else:
            self.necessary = False
        # description is nothing for now.
        self.description = description
    
    def is_in(self, list):
        "Determine whether this argument or its variants are in a list."
        return self.name in list or self.underscored in list

help_arg = Argument("--h", None, "Display this help message and exit.")
