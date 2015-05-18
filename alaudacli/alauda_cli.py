import sys
import copy

import cmd_parser
import cmd_processor
from exceptions import AlaudaServerError


def patch_argv(argv):
    args = copy.copy(argv)

    if not args:
        print 'Arguments cannot be empty.'
        sys.exit(1)

    if len(args) == 1:
        args.append('-h')
    elif len(args) == 2 and args[1] in ['service', 'compose']:
        args.append('-h')
    elif len(args) == 3:
        if args[1] == 'service' and args[2] in ['create', 'run', 'update', 'inspect', 'start', 'stop', 'rm']:
            args.append('-h')
        elif args[1] == 'compose' and args[2] in ['scale']:
            args.append('-h')

    return args[1:]


def main():
    try:
        argv = patch_argv(sys.argv)
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
    except AlaudaServerError as ex:
        print ex
        sys.exit(1)
    print '[alauda] OK'

if __name__ == '__main__':
    main()
