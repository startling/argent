#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argent import Parser
import string

@Parser.from_function
def alphabet(first, second="b", third="c"):
    """Prints the first three letters of the alphabet, if you can decipher its secrets...
    
    first: A cryptic glyph whose nature is not yet known.
    second: A powerful symbol with many names; to the ancients, "bet".
    third: A relatively recent invention, though still many lifetimes old.
    """
    print first
    print second
    print third
    
    n = lambda x: string.letters.index(x)

    if n(first) + 1 == n(second) and n(second) + 1 == n(third):
        print "Only twenty-three more to go."

alphabet.command_line()
