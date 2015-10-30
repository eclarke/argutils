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

.. code-block:: YAML

    __meta__:
      __desc__: Section description
    arg1:
      default: default_value
      __desc__: Argument description/help
    arg2:
      default: 1
      type: int  
      __desc__: Second argument description
    hidden_arg:
      default: 1
      __exclude__: True 
      type: int
      __desc__: This arg does not appear in the config file
    output:
      default: stdout
      __desc__: Where to write the output
      type: File-w
      argtype: arg
    verbose:
      argtype: flag
      __desc__: This is a flag
      __exclude__: True
    choice_arg:
      default: 1
      choices: "1, 2, 3"
      type: int

The fields in this file have the following meanings:
    - `__meta__`: A metadata section that holds the program description
    - `__desc__`: A field that provides descriptions or help text
    - `argtype`: One of 'arg', 'opt', or 'flag', denoting required positional arguments, non-mandatory options, and flags (that take no value), respectively. Default: 'arg'
    - `default`: The default value for this argument (optional). If 'stdin' or 'stdout', the function converts this to  to `sys.stdin` or `sys.stdout`, respectively. 
    - `type`: A base type for the default (should be one of the Python builtin types, or `File-w` or `File-r` for writeable or readable file handles, respectively). Default: 'str'
    - `__exclude__`: A flag (the value following doesn't matter) that denotes that this argument should be excluded from the config file
    - `nargs`: Either an integer giving the number of arguments, or one of ['\*', '+', '?']. If not recognized, it is ignored. Default: None
    - `choices`: a comma-separated list of allowed values for the function. Each item will be coerced to the given `type`; an error is raised if this fails.


Getting started
^^^^^^^^^^^^^^^

Our first step is to read in the spec file. Currently JSON and YAML are supported::

  from argutils import (read, export)
  argsdict = read.from_yaml(open('test.yaml').read())
  # Alternatively:
  argsdict = read.from_json(open('test.json').read())

The only reason to use the read functions instead of the raw JSON or YAML parsers is that the read functions return an OrderedDict, so that the order of the arguments in the spec are maintained when exported to a config file.

We can build an ArgumentParser for these options like so::

  from argutils import (read, export)
  # Read in our YAML file
  yaml_file = open('test.yaml').read()
  argsdict = read.from_yaml(yaml_file)
  parser = export.to_argparser("My Program", argsdict)
  # You can use the parser as you normally would, i.e:
  args = parser.parse_args(sys.argv)

Next, we can generate a config file from this YAML file as follows::

    from argutils import (read, export)
    # Read our YAML file as a string or file handle, doesn't matter
    yaml_file = open('test.yaml').read()
    argsdict = read.from_yaml(yaml_file)
    with open('test.cfg', 'w') as config_file:
        config_file.write(export.to_config('My Program', argsdict))

Now we can take a look at our config file:

.. code-block:: INI 

  ## Section description
  [My Program]
  # Argument description/help
  arg1 = default_value
  # Second argument description
  arg2 = 1
  # Where to write the output
  output = stdout
  choice_arg = 1

Notice that the arguments that have the `__exclude__` flag are omitted from the config file.





