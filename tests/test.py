#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

class FirstCase(unittest.TestCase):
    def setUp(self):
        import first_case
        self.parser = first_case.parser
    
    def assertParser(self, args, expected):
        "Given a list of arguments, test that the Parser returns `expected`."
        self.assertEqual(self.parser.parse(args), expected)

    def test_base_command(self):
        "Test that parsing with no arguments returns 'Some stuff.'"
        self.assertParser([], "Some stuff.")
    
    def test_flag_error(self):
        "Test that giving the main command a flag raises an error."
        self.assertRaises(Exception, self.parser.parse, ["--n"])

    def test_arg_error(self):
        "Tes that giving the main command an argument raises an error."
        self.assertRaises(Exception, self.parser.parse, ["boo"])

    def test_subcommand(self):
        "Test that the `hello subcommand` works without any arguments."
        self.assertParser(["hello"], "goodbye")

    def test_boolean_flags(self):
        "Test that the hello subcommand works with the flag '--f'."
        self.assertParser(["hello", "--f"], "hello")

    def test_positional_arguments(self):
        "Test that the hello subcommand works when you give it an argument."
        self.assertParser(["hello", "--f", "vuiqqwibuqw"], "vuiqqwibuqw")

if __name__ == "__main__":
    unittest.main()
