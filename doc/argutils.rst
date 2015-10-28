:mod:`argutils` -- Link config files and ArgumentParsers
=========================================================

.. module:: argutils
    :synopsis: Utilities to build config files and ArgumentParsers from the same backing specification
.. moduleauthor: Erik Clarke <erikclarke@gmail.com>

--------------------

Example
--------

`argutils` is intended for situations when you have a command-line program that has arguments specified by ArgumentParser as well as a config file that users can edit. In order to keep the options in the config file in sync with the arguments given to the parser, `argutils` can create both from a spec file in JSON or YAML. 

Here is an example spec file in YAML:

.. code:: YAML

    __meta__:
      __desc__: Program description
    arg1:
      __desc__: Argument description/help
      default: default_value
    arg2:
      __desc__: Second argument description
      default: 1
      type: int
    arg3:
      __desc__: Third argument description
      default: 1
      type: int
      __exclude__: True

The fields in this file have the following meanings:
    - `__meta__`: A metadata section that holds the program description
    - `__desc__`: A field that provides descriptions or help text
    - `default`: The default value for this argument (optional)
    - `type`: A base type for the default (should be one of the python base types, or `File-w` or `File-r` for writeable or readable file handles, respectively)
    - `__exclude__`: A flag (the value following doesn't matter) that denotes that this argument should be excluded from the config file

Generating a config file
^^^^^^^^^^^^^^^^^^^^^^^^

We can generate a config file from this YAML file as follows::

    from argutils import (read, export)
    # Read our YAML file as a string or file handle, doesn't matter
    yaml_file = open('test.yaml').read()
    argsdict = read.from_yaml(yaml_file)
    with open('test.cfg', 'w') as config_file:
        config_file.write(export.to_config('My Program', argsdict))

Now we can take a look at our config file:

.. code:: INI 

    ## Section description
    [My Program]
    # Argument description/help
    arg1 = default_value
    # Second argument description
    arg2 = 1

Notice that `arg3` is omitted, as specified by the `__exclude__` flag. Also note that type information is not encoded in the config file, but it will be used in the argument parser.

Generating an ArgumentParser
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To-do

