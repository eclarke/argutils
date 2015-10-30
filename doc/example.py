import ConfigParser
import argutils
from argutils import (read, export)

SPEC_FILE = 'example_spec.yml'
CONF_FILE = 'example.cfg'

def main():
    # Used in the config file and argument parser's help
    prog_name = 'example.py'

    config = ConfigParser.SafeConfigParser()

    # Read the spec and build a parser from it
    argsdict = read.from_yaml(open(SPEC_FILE).read())
    parser = export.to_argparser(prog_name, argsdict)

    # If the config file exists and we can read it, use it to set the 
    # defaults
    if config.read(CONF_FILE):
        parser = argutils.set_parser_defaults(parser, config)

    args = parser.parse_args()

    if args.init:
        export.to_config_file(prog_name, argsdict, CONF_FILE)

    for _ in range(args.times):
        args.output.write(args.message + '\n')


if __name__ == '__main__':
    main()
