"""Test export functions."""
import shlex
import sys
from collections import OrderedDict
import pytest
import argutils
from argutils import (read, export, FILE_W, FILE_R)
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

def test_to_config(argsdict, argsdict_cfg_str):
    """
    Comments should appear above the option, and the excluded options should 
    not appear.
    """
    cfg_string = export.to_config(cmd_name='Section', argsdict=argsdict)
    assert cfg_string == argsdict_cfg_str

def test_to_config_no_meta():
    """If no metadata section included, use the passed description."""
    argsdict = OrderedDict({'arg1': {'default': 1}})
    cfgstr = export.to_config("test", argsdict, desc="test description")
    assert cfgstr == """## test description
[test]
arg1 = 1
"""

def test_to_argparser(argsdict):
    """Valid argdict should behave as expected."""
    parser = export.to_argparser(cmd_name='Command', argsdict=argsdict)
    # Valid, expected input
    validargs = "--arg1 someval --arg2 5 --hidden 6 --flag --choices 2 /dev/null"
    args = parser.parse_args(shlex.split(validargs))
    assert parser.prog == "Command"
    assert args.arg1 == "someval"
    assert args.arg2 == 5
    assert args.hidden == 6
    assert args.flag
    assert args.choices == 2
    assert args.output.name == "/dev/null"

def test_to_argparser_bad_input(argsdict):
    parser = export.to_argparser(cmd_name='Command', argsdict=argsdict)
    # Invalid choice
    with pytest.raises(SystemExit):
        parser.parse_args(shlex.split("--choices 4 blah"))
    # Invalid type
    with pytest.raises(SystemExit):
        parser.parse_args(shlex.split("--arg2 string blah"))

def test_to_argparser_bad_argsdict():
    """
    Should raise an error if the choices aren't coercible to the given type.
    """
    argsdict = {'badchoices': {
        'choices': 'a, b',
        'type': 'int'}}
    with pytest.raises(ValueError):
        export.to_argparser("...", argsdict)

def test_nargs():
    """`nargs` should work as expected by ArgumentParser."""
    argsdict = {'nargs': {
        'type': 'int', 
        'nargs': '+'}}
    parser = export.to_argparser('...', argsdict)
    args = parser.parse_args(shlex.split("--nargs 1 2 3"))
    assert args.nargs == [1, 2, 3]

def test_bad_nargs():
    """
    `nargs` that don't match an int or one of the given options should be set 
    to None.
    """
    argsdict = {'nargs': {
        'nargs': 'b'}}
    parser = export.to_argparser('...', argsdict)
    with pytest.raises(SystemExit):
        parser.parse_args("--nargs 1 2 3")

def test_stdin_stdout():
    argsdict = {
        'arg1': {'default': 'stdin'},
        'arg2': {'default': 'stdout'}
    }
    parser = export.to_argparser('test', argsdict)
    args = parser.parse_args("")
    assert args.arg1 == sys.stdin
    assert args.arg2 == sys.stdout

def test_filetypes():
    argsdict = {
        'arg1': {'type': FILE_W},
        'arg2': {'type': FILE_R}
    }
    parser = export.to_argparser('test', argsdict)
    args = parser.parse_args(
        shlex.split("--arg1 /dev/null --arg2 {}".format(__file__))
    )
    assert args.arg1.mode == 'w'
    assert args.arg2.mode == 'r'

def test_bad_typestr():
    argsdict = {
        'arg1': {'type': 'notatype'}
    }
    with pytest.raises(ValueError):
        export.to_argparser('test', argsdict)

def test_unordered_warning(argsdict):
    """Passing unordered argsdicts to to_config should raise an error."""
    unordered_args = dict(argsdict)
    with pytest.raises(ValueError):
        export.to_config(cmd_name='Section', argsdict=unordered_args)

def test_set_parser_defaults(argsdict, tmpdir):
    # Build a config parser
    config = ConfigParser.SafeConfigParser()
    cfg_file = tmpdir.join("test.cfg")
    cfg_file.write(export.to_config('test', argsdict))
    config.read(str(cfg_file))

    # Modify config from the spec defaults
    config.set("test", "arg2", "3")

    # Build argparser
    parser = export.to_argparser('test', argsdict)
    parser = argutils.set_parser_defaults(parser, config)
    args = parser.parse_args(["test"])
    # Should reflect the modified default
    assert args.arg2 == 3

    # Should warn since it can't find the section
    parser = export.to_argparser('test2', argsdict)
    with pytest.warns(UserWarning):
        argutils.set_parser_defaults(parser, config)

def test_to_config_file(argsdict, tmpdir, argsdict_cfg_str):
    cfg_out = tmpdir.join("out.cfg")
    with pytest.raises(SystemExit):
        cfg_str = export.to_config_file("Section", argsdict, str(cfg_out))
    assert cfg_out.read() == argsdict_cfg_str

