import pytest
from collections import OrderedDict
import argutils
import argutils.export
from argutils import (
	META_KEY, DESC_KEY, EXCLUDE_FLAG,
)

@pytest.fixture
def argsdict():
	argsdict = OrderedDict({
		META_KEY: {
			DESC_KEY: 'Section description'
		},
		'arg1': {
			DESC_KEY: 'Argument description/help',
			'default': 'default_value',
			'type': 'str'
		}, 
		'arg2': {
			DESC_KEY: 'Second argument description',
			'default': 1,
			'type': int,
		},
		'arg3': {
			DESC_KEY: 'Hidden argument description',
			'default': 3,
			'type': int,
			EXCLUDE_FLAG: True
		}
	})
	return argsdict

def test_to_config(argsdict):
	cfg_string = argutils.export.to_config(header='Section', argsdict=argsdict)
	assert cfg_string == """## Section description
[Section]
# Argument description/help
arg1 = default_value
# Second argument description
arg2 = 1
"""