import textwrap

META_KEY = "__meta__"
DESC_KEY = "__desc__"
EXCLUDE_FLAG = "__exclude__"
FILE_W = "File-w"
FILE_R = "File-r"

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
