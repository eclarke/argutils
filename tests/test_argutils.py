import os
import pytest
from collections import OrderedDict
import argutils
import argutils.read

def test_import_from_json(json_file, argsdict):
    """Should be able to produce an OrderedDict from a JSON file."""
    with open(json_file) as infile:
        result = argutils.read.from_json(infile.read())
        assert isinstance(result, OrderedDict)
        assert result == argsdict

def test_import_from_yaml(yaml_file, argsdict):
    """Should be able to produce an OrderedDict from a YAML file."""
    with open(yaml_file) as infile:
        result = argutils.read.from_yaml(infile.read())
        assert isinstance(result, OrderedDict)
        assert result == argsdict

def test_blank_comment():
    blank = ""
    assert argutils.format_comment(blank) == ""
    assert argutils.format_comment(None) == ""


    