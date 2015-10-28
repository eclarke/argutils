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
    d['arg1'] = OrderedDict([
        ('default', 'default_value'),
        (DESC_KEY, 'Argument description/help')
    ])
    d['arg2'] = OrderedDict([
        ('default', 1),
        ('type', 'int'),
        (DESC_KEY, 'Second argument description')
    ])
    d['hidden'] = OrderedDict([
        ('default', 1),
        (EXCLUDE_FLAG, True),
        ('type', 'int'),
        (DESC_KEY, 'This arg does not appear in the config file')
    ])
    d['output'] = OrderedDict([
        ('default', 'stdout'),
        (DESC_KEY, 'Testing other filetypes/options'),
        ('type', 'File-w'),
        ('argtype', 'arg')
    ])
    d['flag'] = OrderedDict([
        ('argtype',  'flag'),
        (DESC_KEY, 'This is a flag')
    ])
    d['choices'] = OrderedDict([
        ('default', 1),
        ('choices', "1, 2, 3"),
        ('type', 'int')
    ])

    return d