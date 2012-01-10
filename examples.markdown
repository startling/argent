# Examples
This is a pretty huge list of examples. You can download and test them out from the [`examples` directory)(https://github.com/startling/argent/tree/master/examples), too.

## Positional Arguments
You can have positional arguments.

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argent import Parser

@Parser.from_function
def positional(something):
    ""Prints whatever you want.
    
    something: the argument that will be printed.
    ""
    print something

positional.command_line()
```

```
usage: positional.py [--h] something 

Prints whatever you want.

optional flags:
   --h, --help   Display this help message and exit.                               

necessary arguments:
   something     the argument that will be printed.
```

Arguments with defaults.

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argent import Parser

@Parser.from_function
def default_positional(something="hello"):
    ""Prints whatever you damn well please.
    
    something: the argument that will be printed; defaults to "hello".
    ""
    print something

default_positional.command_line()"
```

Argent made `something` an optional argument now, since you specified a default.

```
usage: defaults.py [--h] [something] 

Prints whatever you damn well please.

optional flags:
   --h, --help   Display this help message and exit.                               

optional arguments:
   something     the argument that will be printed; defaults to "hello".
```

And any mixture of the two.

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argent import Parser
import string

@Parser.from_function
def alphabet(first, second="b", third="c"):
    ""Prints the first three letters of the alphabet, if you can decipher its secrets...
    
    first: A cryptic glyph whose nature is not yet known.
    second: A powerful symbol with many names; to the ancients, "bet".
    third: A relatively recent invention, though still many lifetimes old.
    ""
    print first
    print second
    print third
    
    n = lambda x: string.letters.index(x)

    if n(first) + 1 == n(second) and n(second) + 1 == n(third):
        print "Only twenty-three more to go."

alphabet.command_line()
```

```
usage: mixed.py [--h] first [second] [third] 

Prints the first three letters of the alphabet, if you can decipher its secrets...

optional flags:
   --h, --help   Display this help message and exit.                               

necessary arguments:
   first         A cryptic glyph whose nature is not yet known.                    

optional arguments:
   second        A powerful symbol with many names; to the ancients, "bet".        
   third         A relatively recent invention, though still many lifetimes old.
```

## Boolean Flags
You can have boolean flags, too. Note the synonyms.

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argent import Parser

@Parser.from_function
# underscores indicate flags; from the command line, these are "--a" and "--b".
def xor(__a, __b):
    ""A boolean xor operation.
    
    --a, --i1: The first input.
    --b, --i2: The second input.
    ""
    print __a ^ __b

xor.command_line()
```

```
usage: boolean.py [--h] [--a] [--b] 

A boolean xor operation.

optional flags:
   --h, --help   Display this help message and exit.                               
   --a, --i1     The first input.                                                  
   --b, --i2     The second input. 
```

## Subcommands
You can have arbitrary amounts of arbitrarily-nested subcommands.

```python
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
    ""4081 quad 2-input AND gate.

    a: The first input.
    b: The second input.
    ""
    return a and b

@logical_operations.subparse
def OR(a, b):
    ""4071 quad 2-input OR gate.

    a: The first input.
    b: The second input.
    ""
    return a or b

@logical_operations.subparse
def NAND(a, b):
    ""4093 quad 2-input NAND (with Schmiit triggers!)

    a: The first input.
    b: The second input.
    ""
    return not a and b

logical_operations.command_line()
```

```
usage: subcommands.py [--h] 

Emulate some sea-moss logic ICs.

optional flags:
   --h, --help   Display this help message and exit.                               

Subcommands:
   AND           4081 quad 2-input AND gate.                                       
   OR            4071 quad 2-input OR gate.                                        
   NAND          4093 quad 2-input NAND (with Schmiit triggers!)
```

Each of the subparsers have help messages, too.

```
usage: subcommands.py AND [--h] a b 

4081 quad 2-input AND gate.

optional flags:
   --h, --help   Display this help message and exit.                               

necessary arguments:
   a             The first input.                                                  
   b             The second input.
```

etc. etc. etc.
