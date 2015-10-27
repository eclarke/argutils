import textwrap

META_KEY = "__meta__"
DESC_KEY = "__desc__"
EXCLUDE_FLAG = "__exclude__"

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


def format_comment(text, width=72, quote="# "):
    """Line-wraps and pads text to write as a comment.

    :param text: the text to format
    :param width: number of characters to wrap text to
    :param quote: the string to prefix each line (include a space!)
    """

    if not text: 
        return ""
    lines = textwrap.wrap(text, width=width)
    lines = [quote + line.strip() for line in lines if line.strip()]
    return "\n".join(lines) + "\n"
