#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argent import Parser

@Parser.from_function
# underscores indicate flags; from the command line, these are "--a" and "--b".
def xor(__a, __b):
    """A boolean xor operation.
    
    --a, --i1: The first input.
    --b, --i2: The second input.
    """
    print __a ^ __b

xor.command_line()
