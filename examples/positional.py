#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argent import Parser

@Parser.from_function
def positional(something):
    """Prints whatever you want.
    
    something: the argument that will be printed.
    """
    print something

positional.command_line()
