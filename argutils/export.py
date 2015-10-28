"""Functions to export argument lists as config files or ArgumentParsers."""
from collections import OrderedDict
import argparse
import sys
import six
import warnings


from argutils import (
    format_comment, META_KEY, DESC_KEY, EXCLUDE_FLAG, FILE_W, FILE_R
)

def to_config(cmd_name, argsdict, desc=None):
    """Create an INI-style config file from a given dictionary of arguments.

    :param cmd_name: name of the command (used in the config section header)
    :param argsdict: a dictionary of arguments, as provided by argutils.read.*
    :param desc: (optional) a description of the command, if one is not provided
    by the argsdict
    :returns: a string representation of the config file, which can be written 
    to a file
    """ 

    if not isinstance(argsdict, OrderedDict):
        warnings.warn(
            "Arguments dictionary is unordered: output order will be random."
        )

    CFG_LINE_STR = "{key} = {value}\n"
    CFG_SECTION_STR = "[{header}]\n"

    # The string that will hold the final config file contents
    out = ""

    # Use the description provided if it's missing from the argsdict
    if META_KEY in argsdict:
        section_desc = argsdict[META_KEY].get(DESC_KEY, desc)
    else:
        section_desc = desc

    out += format_comment(section_desc, quote="## ")
    out += CFG_SECTION_STR.format(header=cmd_name)

    for argname, argvals in six.iteritems(argsdict):
        # Skip the metadata section (since we handled already)
        if argname == META_KEY:
            continue

        if EXCLUDE_FLAG in argvals:
            continue

        description = format_comment(argvals.get(DESC_KEY, ""))
        default = argvals.get("default", "")
        line = CFG_LINE_STR.format(key=argname, value=default)
        out += description + line

    return out


def to_argparser(cmd_name, argsdict, desc=None):
    """Create an ArgumentParser from the given dictionary of arguments.

    :param cmd_name: name of the command
    :param argsdict: a dictionary of arguments, as provided by argutils.read.*
    :param desc: (optional) a description of the command, if one is not provided
    by argsdict.
    :returns: An ArgumentParser with the specified options and args
    """
    # If there's a metadata section, get the description from there, otherwise
    # use the default provided
    if META_KEY in argsdict:
        cmd_desc = argsdict[META_KEY].get(DESC_KEY, desc)
    else:
        cmd_desc = desc
    parser = argparse.ArgumentParser(prog=cmd_name, description=cmd_desc)

    for argname, argvals in argsdict.iteritems():
        if argname == META_KEY:
            continue
        parser = _add_argument(argname, argvals, parser) 

    return parser


def _add_argument(argname, argvals, parser):
    """Adds an argument to the parser from a given set of argument values.

    :param argname: the name of the argument
    :param argvals: the options for the argument. Currently implemented:
        - argtype: one of 'arg', 'opt', or 'flag' 
            (mandatory, optional, and takes no value, respectively)
        - action: passed directly to add_argument (unless argtype == flag)
        - prefix: the prefix used to call the option. If opttype == 

    """
    action = argvals.get('action', 'store')
    prefix = argvals.get('prefix', '--')
    _help = argvals.get(DESC_KEY, '')

    nargs = argvals.get('nargs', None)
    try:
        nargs = int(nargs)
    except ValueError:
        nargs = nargs if nargs in ['+', '?', '*', argparse.REMAINDER] else None

    # We only use a non-False default value for stdin/stdout options,
    # all other options pull the default values from the config file
    default = argvals.get('default')
    if default == 'stdin':
        default = sys.stdin
    elif default == 'stdout':
        default = sys.stdout
    else:
        default = False

    # What kind of values can the argument take? We generally just evaluate
    # the type provided as a string, except for FileTypes which we handle 
    # specially
    _type = _parse_type(argvals.get('type'), argname)

    # Choices should be a container. We'll just split on commas and coerce to
    # the same type as defined above
    choices = _parse_choices(argvals.get('choices', None), _type)

    # There are three types of options allowed:
    # 'arg': positional arguments, which are required,
    # 'opt': options, which are optional, and
    # 'flag': flags, which do not take values after them
    argtype = argvals.get('argtype', 'opt')
    if argtype == 'arg':
        prefix = ''

    # The final constructor operation is different depending on the situation.
    # Case 1: It's a flag option, in which case we omit most of the parameters
    if argtype == 'flag':
        parser.add_argument(
            prefix + argname,
            action='store_true',
            help=_help)
    # Case 2: It's a normal argument with a default value of stdin/stdout
    elif default:
        parser.add_argument(
            prefix + argname,
            action=action,
            nargs=nargs,
            choices=choices,
            default=default,
            type=_type,
            help=_help)
    # Case 3: It's a normal argument with no default specified. Passing None
    # as the default conflicts with specifying a type, so we need to omit it
    # from the constructor entirely instead.
    else:
        parser.add_argument(
            prefix + argname,
            action=action,
            nargs=nargs,
            choices=choices,
            type=_type,
            help=_help)
    return parser

def _parse_type(typestr, argname):
    """Parses the type from a string. 

    :param typestr: a string coercible to a type or argparse.FileType. If None 
    or an empty string, the default is `str`.
    :param argname: the argument name (used for error reporting)
    :returns: the actual type found (i.e. `int`, `str`, argparse.FileType('w'))
    """
    if typestr == FILE_R:
        return argparse.FileType('r')
    elif typestr == FILE_W:
        return argparse.FileType('w')
    elif typestr:
        try:
            return getattr(__builtins__, typestr)
        except AttributeError:
            raise ValueError(
                "Invalid type specified for `{}`: {}"
                .format(argname, typestr)
            )
    else:
        return str

def _parse_choices(choices_str, arg_type):
    """Parses the choices for an argument from a comma-separated string.

    :param choices_str: a comma-separated list of options
    :param arg_type: a type to coerce each choice to; will throw an exception
    if the coercion fails.
    :returns: a list of choices of the specified type
    """

    if not choices_str:
        return None
    else:
        choices = [c.strip() for c in choices_str.split(",")]
        try:
            choices = [arg_type(c) for c in choices]
            return choices
        except (ValueError, argparse.ArgumentTypeError) as err:
            warnings.warn("Could not coerce choice(s) to given type!")
            raise err

