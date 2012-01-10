#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argent import Parser

@Parser.from_function
def default_positional(something="hello"):
    """Prints whatever you damn well please.
    
    something: the argument that will be printed; defaults to "hello".
    """
    print something

default_positional.command_line()
