.. argutils documentation master file, created by
   sphinx-quickstart on Mon Oct 26 20:54:34 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

argutils - functions for creating matched config files and argument parsers
===========================================================================

`argutils` provides a set of functions for quickly building command-line programs with matching config files. In particular, instead of separately building an ArgumentParser and ConfigParser, `argutils` lets the user build an interface from a JSON or YAML file, and then uses that to build both an argument parser and matching config file.

Here's a working example. We have a toy program that takes three arguments: a message to print, the number of times to print it, and where to print it. We have two files, an argument spec file we'll call `example_spec.yml`, and our program, `example.py`.

In `example_spec.yml`:

.. literalinclude:: example_spec.yml
  :language: YAML

In `example.py`:

.. literalinclude:: example.py

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

Release |release|

Contents:

.. toctree::
   :maxdepth: 1

   argutils

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

