#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argent import Parser

@Parser.from_function
def logical_operations():
    "Emulate some sea-moss logic ICs."
    # call the help message up, if they're not using a subcommand.
    logical_operations.help()

@logical_operations.subparse
def AND(a, b):
    """4081 quad 2-input AND gate.

    a: The first input.
    b: The second input.
    """
    return a and b

@logical_operations.subparse
def OR(a, b):
    """4071 quad 2-input OR gate.

    a: The first input.
    b: The second input.
    """
    return a or b

@logical_operations.subparse
def NAND(a, b):
    """4093 quad 2-input NAND (with Schmiit triggers!)

    a: The first input.
    b: The second input.
    """
    return not a and b

logical_operations.command_line()
