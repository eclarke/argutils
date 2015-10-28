"""Test export functions."""

def test_to_config(argsdict):
    cfg_string = argutils.export.to_config(cmd_name='Section', argsdict=argsdict)
    assert cfg_string == """## Section description
[Section]
# Argument description/help
arg1 = default_value
# Second argument description
arg2 = 1
"""

def test_to_argparser(argsdict):
    parser = argutils.export.to_argparser(cmd_name='Command', argsdict=argsdict)
    # Valid, expected input
    validargs = "--arg1 someval --arg2 5 --arg3 6"
    parsed_valid_args = parser.parse_args(shlex.split(validargs))
    assert parsed_valid_args.arg1 == "someval"
    assert parsed_valid_args.arg2 == 5

def test_unordered_warning(argsdict):
    """Passing unordered argument dictionaries should raise an error."""
    unordered_args = dict(argsdict)
    with pytest.warns(UserWarning):
        argutils.export.to_config(cmd_name='Section', argsdict=unordered_args)