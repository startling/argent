# Argent.
Argent is a new argument parser for command-line programs in Python.

## Rationale
Turns out Python already has objects that can take arbitrary arguments, supply defaults, and do things with them: they're called functions. Argent syntax is just decorated functions. For help messages, Argent uses some introspective magic on these functions and then analyzes your docstrings for more information. And you already detail your arguments meticulously in your docstrings, right?

## Features

* Easy syntax; no cascades of text, as in argparse. Use the Python function syntax you already know and love.
* Cleverness founded in introspective magic; on the other hand, it's only a little more magic than docutils. No black magic metaclass hacking here.
* So long as you format your docstrings how Argent expects you too, you'll get beautiful detailed help messages.

## Examples
This is about the simplest you can do:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argent import Parser

@Parser.from_function
def simplest():
    "Prints hello when you call it."
    print "hello!"

simplest.command_line()
```

This program's help message (run `python simplest.py --help`) is:

```
usage: simplest.py [--h] 

Prints hello when you call it.

optional flags:
   --h, --help   Display this help message and exit.
```


[Here's](https://github.com/startling/argent/blob/master/examples/subcommands.py) a more featureful example, and there are more over at [this other page](https://github.com/startling/argent/blob/master/examples.markdown).

## Todo:
* Flags that can take arguments -- like `--flag argument`.
* Type checking; for now you have to assume everything will come in as strings.
* Colorized help output?
* Clean up the codebase, as always.
* More documentation.

