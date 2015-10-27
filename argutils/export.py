"""Functions to export argument lists as config files or ArgumentParsers."""

from argutils import format_comment

from argutils import (
    META_KEY, DESC_KEY, EXCLUDE_FLAG
)

def to_config(header, argsdict):
    """Create an INI-style config file from a given dictionary of arguments.

    :param argsdict: a dictionary of arguments as provided by `read_serialized`
    :returns: a string representation of the config file, which can be written to a file
    """ 

    CFG_LINE_STR = "{key} = {value}\n"
    CFG_SECTION_STR = "[{header}]\n"

    # The string that will hold the final config file contents
    out = ""

    if META_KEY in argsdict:
        section_desc = argsdict[META_KEY].get(DESC_KEY, "")
        out += format_comment(section_desc, quote="## ")    

    out += CFG_SECTION_STR.format(header=header)

    for argname, argvals in argsdict.iteritems():
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

