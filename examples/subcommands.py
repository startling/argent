#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argent import Parser

@Parser.from_function
def logical_operations():
    "Emulate some sea-moss logic ICs."
    # call the help message up, if they're not using a subcommand.
    logical_operations.help()

@logical_operations.subparse
def AND(__a, __b):
    """4081 quad 2-input AND gate.

    --a: The first input.
    --b: The second input.
    """
    return __a and __b

@logical_operations.subparse
def OR(__a, __b):
    """4071 quad 2-input OR gate.

    --a: The first input.
    --b: The second input.
    """
    return __a or __b

@logical_operations.subparse
def NAND(__a, __b):
    """4093 quad 2-input NAND (with Schmiit triggers!)

    --a: The first input.
    --b: The second input.
    """
    return not __a and __b

logical_operations.command_line()
