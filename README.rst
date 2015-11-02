argutils - functions for creating matched config files and argument parsers
===========================================================================

.. image:: https://travis-ci.org/eclarke/argutils.svg?branch=v0.2.0
  :target: https://travis-ci.org/eclarke/argutils
.. image:: https://coveralls.io/repos/eclarke/argutils/badge.svg?branch=v0.2.0&service=github
  :target: https://coveralls.io/github/eclarke/argutils?branch=master
.. image:: https://readthedocs.org/projects/argutils/badge/?version=latest
  :target: http://argutils.readthedocs.org/en/latest/?badge=latest
  :alt: Documentation Status
.. image:: https://badge.fury.io/py/argutils.svg
    :target: https://badge.fury.io/py/argutils

`argutils` provides a set of functions for quickly building command-line programs with matching config files. In particular, instead of separately building an ArgumentParser and ConfigParser, `argutils` lets the user build an interface from a JSON or YAML file, and then uses that to build both an argument parser and matching config file.

Installation
------------

.. code-block:: bash

  $ pip install argutils
  
Usage example
--------------

Let's say we have a toy program that takes three arguments: a message to print, the number of times to print it, and where to print it. We have two files, an argument spec file we'll call `example_spec.yml`, and our program, `example.py`.

In `example_spec.yml`:

.. code-block:: YAML

  _meta:
    help: > 
      A program that prints a message some number of times to an output
      file
  message:
    help: the message to print
    default: "Hello world!"
  times:
    help: how many times to print the message
    default: 3
    type: int
  output:
    help: where to write the file
    _exclude: True
    default: stdout
    type: File-w
  init:
    help: write a config file with default values
    _exclude: True
    argtype: flag

In `example.py`:

.. code-block:: Python

  try:
      import ConfigParser
  except ImportError:
      import configparser as ConfigParser
  import argutils
  from argutils import (read, export)

  SPEC_FILE = 'example_spec.yml'
  CONF_FILE = 'example.cfg'

  def main():
      # Used in the config file and argument parser's help
      prog_name = 'example.py'

      config = ConfigParser.SafeConfigParser()

      # Read the spec and build a parser from it
      argsdict = read.from_yaml(open(SPEC_FILE).read())
      parser = export.to_argparser(prog_name, argsdict)

      # If the config file exists and we can read it, use it to set the 
      # defaults
      if config.read(CONF_FILE):
          parser = argutils.set_parser_defaults(parser, config)

      args = parser.parse_args()

      if args.init:
          export.to_config_file(prog_name, argsdict, CONF_FILE)

      for _ in range(args.times):
          args.output.write(args.message + '\n')


  if __name__ == '__main__':
      main()

Let's see what we've got:

.. code-block:: bash

  $ python example.py --help
  usage: example.py [-h] [--message MESSAGE] [--times TIMES]
                       [--output OUTPUT] [--init]

  A program that prints a message some number of times to an output file

  optional arguments:
    -h, --help         show this help message and exit
    --message MESSAGE  the message to print
    --times TIMES      how many times to print the message
    --output OUTPUT    where to write the file
    --init             write a config file with default values

We can see that all the arguments we specified in the YAML file are here. Let's write a config file and check that out:

.. code-block:: bash

  $ python example.py --init
  $ cat example.cfg
  ## A program that prints a message some number of times to an output file
  [example.py]
  # the message to print
  message = Hello world!
  # how many times to print the message
  times = 3

Note that two arguments don't show up here: `output` and `init`. These were excluded using the `_exclude` flag in the YAML file. This is useful for arguments that shouldn't be set using a config file, including one-time arguments.

Let's test it:

.. code-block:: bash

  $ python example.py
  Hello world!
  Hello world!
  Hello world!
  $ python example.py --times 1
  Hello world!

We can specify the arguments either with command-line flags or by modifying the values in the config file. Values specified on the command line take precedence, followed by the config file values, and resorting to the spec file defaults if nothing else is given.
