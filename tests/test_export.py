"""Test export functions."""
import shlex
import pytest
from argutils import (read, export)

def test_to_config(argsdict):
    cfg_string = export.to_config(cmd_name='Section', argsdict=argsdict)
    assert cfg_string == """## Section description
[Section]
# Argument description/help
arg1 = default_value
# Second argument description
arg2 = 1
# Testing other filetypes/options
output = stdout
# This is a flag
flag = 
choices = 1
"""

def test_to_argparser(argsdict):
    parser = export.to_argparser(cmd_name='Command', argsdict=argsdict)
    # Valid, expected input
    validargs = "--arg1 someval --arg2 5 --hidden 6 --flag --choices 2 blah"
    args = parser.parse_args(shlex.split(validargs))
    assert parser.prog == "Command"
    assert args.arg1 == "someval"
    assert args.arg2 == 5
    assert args.hidden == 6
    assert args.flag
    assert args.choices == 2
    assert args.output.name == "blah"

def test_to_argparser_bad_input(argsdict):
    parser = export.to_argparser(cmd_name='Command', argsdict=argsdict)
    # Invalid choice
    with pytest.raises(SystemExit):
        parser.parse_args(shlex.split("--choices 4 blah"))
    # Invalid type
    with pytest.raises(SystemExit):
        parser.parse_args(shlex.split("--arg2 string blah"))
    pass

def test_to_argparser_bad_argsdict():
    argsdict = {
        'badchoices': {
            'choices': 'a, b',
            'type': 'int'
        }
    }
    with pytest.raises(ValueError):
        export.to_argparser("...", argsdict)

def test_nargs():
    argsdict = {'nargs': {'type': 'int', 'nargs': '+'}}
    parser = export.to_argparser('...', argsdict)
    args = parser.parse_args(shlex.split("--nargs 1 2 3"))
    assert args.nargs == [1, 2, 3]

def test_bad_nargs():
    argsdict = {'nargs': {'nargs': 'b'}}
    parser = export.to_argparser('...', argsdict)
    with pytest.raises(SystemExit):
        parser.parse_args("--nargs 1 2 3")

def test_unordered_warning(argsdict):
    """Passing unordered argument dictionaries should raise an error."""
    unordered_args = dict(argsdict)
    with pytest.warns(UserWarning):
        export.to_config(cmd_name='Section', argsdict=unordered_args)