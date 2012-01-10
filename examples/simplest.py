#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argent import Parser

@Parser.from_function
def simplest():
    "Prints hello when you call it."
    print "hello!"

simplest.command_line()
