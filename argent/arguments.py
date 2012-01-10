# -*- coding: utf-8 -*-

def arguments_from_function(fn):
    """Given a function, use introspective magic to make inferences about 
    its arguments.
    """
    arguments = []
    args, _, _, defaults = getargspec(fn)
    # getargspec annoyingly returns None if there are none,
    # so turn it into an empty tuple if it's None.
    if defaults == None:
        defaults = ()
    # for the arguments that don't have defaults, 
    # that is, all of args except the last `len(defaults)`,
    # make Argument objects and append them to `arguments`
    for arg in args[:len(defaults)]:
        arguments.append(Argument(arg))
    # for the last `len(defaults)`, make 
    for arg, default in zip(args[len(args)-len(defaults):], defaults):
        arguments.append(Argument(arg, default))
    return arguments

class Argument(object):
    "A class to handle arguments and their metadata."
    def __init__(self, name, default=None):
        # `self.name` is what we get but with no underscores and all dashes.
        self.name = name.replace("_", "-")
        # `self.underscored` is the opposite.
        self.underscored = name.replace("_", "-")
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
        self.description = ""
