import os
import json
import pytest
from collections import OrderedDict
import argutils
import argutils.export
import argutils.read
from argutils import (
	META_KEY, DESC_KEY, EXCLUDE_FLAG,
)

@pytest.fixture
def testdata_fp():
	return os.path.join(os.path.dirname(__file__), "data")

@pytest.fixture
def json_file(testdata_fp):
	return os.path.join(testdata_fp, "test.json")

@pytest.fixture
def yaml_file(testdata_fp):
	return os.path.join(testdata_fp, "test.yaml")

@pytest.fixture
def argsdict():
	d = OrderedDict()
	d[META_KEY] = {DESC_KEY: "Section description"}
	d['arg1'] = {
		'default': 'default_value',
		DESC_KEY: 'Argument description/help'
	}
	d['arg2'] = {
		'default': int(1),
		DESC_KEY: 'Second argument description',
		'type': 'int'
	}
	d['arg3'] = {
		'default': int(1),
		DESC_KEY: 'Third argument description',
		'type': 'int',
		EXCLUDE_FLAG: True
	}
	return d


def test_import_from_json(json_file, argsdict):
	with open(json_file) as infile:
		s = infile.read()
		result = argutils.read.from_json(s)
		assert isinstance(result, OrderedDict)
		assert result == argsdict

def test_import_from_yaml(yaml_file, argsdict):
	with open(yaml_file) as infile:
		s = infile.read()
		result = argutils.read.from_yaml(s)
		assert isinstance(result, OrderedDict)
		assert result == argsdict


def test_to_config(argsdict):
	cfg_string = argutils.export.to_config(header='Section', argsdict=argsdict)
	assert cfg_string == """## Section description
[Section]
# Argument description/help
arg1 = default_value
# Second argument description
arg2 = 1
"""

def test_unordered_warning(argsdict):
	"""Passing unordered argument dictionaries should raise an error."""
	unordered_args = dict(argsdict)
	with pytest.warns(UserWarning):
		argutils.export.to_config(header='Section', argsdict=unordered_args)

def test_blank_comment():
	blank = ""
	assert argutils.format_comment(blank) == ""
	assert argutils.format_comment(None) == ""
	