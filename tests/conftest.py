import os
from collections import OrderedDict
import pytest
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
        'default': 1,
        DESC_KEY: 'Second argument description',
        'type': 'int'
    }
    d['hidden'] = {
        'default': 1,
        DESC_KEY: 'This arg does not appear in the config file',
        'type': 'int',
        EXCLUDE_FLAG: True
    },
    d['output'] = {
        'default': 'stdout',
        DESC_KEY: 'Testing other filetypes/options',
        'type': 'File-w',
        
    }
    return d