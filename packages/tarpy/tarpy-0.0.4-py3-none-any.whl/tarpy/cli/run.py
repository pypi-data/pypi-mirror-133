''' CLI Parser

Module of tarpy.
Usage:
    tarpy [ROOT] [TARGET] -m {'w', 'e'} [--exclude_file] [--compression]

'''

import argparse
from typing import Any
from tarpy.tarhandler import Tarpy
from tarpy.logger import LOGGER, CONSOLE_HANDLER

def cliparser() -> Any:
    ''' CLI Parser

    Function takes parameters like defined below and
    returns the args.
    '''
    parser = argparse.ArgumentParser(
            description = 'Different TAR Archive operations.',
            epilog = 'Python3 version.',
            )
    parser.add_argument(
            'ROOT',
            type=str,
            help='''
            The (starting) directory to archive respectively 
            the file to extract.
            If giving a Path, avoid relative paths and always
            try to give the absolute path to not force any
            side effects.
            '''
            )
    parser.add_argument(
            'TARGET',
            type=str,
            help='The path where archive will be written to.'
            )
    parser.add_argument(
            '-m',
            choices=['w', 'e'],
            help = 'Which Operation to run.'
            )

    parser.add_argument(
            '-ex-f',
            '--exclude-file',
            metavar='PATH',
            help='File with exclusions defined. Please try to specify the full path.'
            )

    parser.add_argument(
            '-c',
            '--compression',
            choices=['gz', 'bz2', 'xz'],
            help='''
            The compression method.
            gz  -   Gzip
            bz2 -   bzip2
            xz  -   lzma'''
            )

    parser.add_argument(
            '-v',
            '--verbose',
            help='See Messages.',
            action='store_true'
            )

    return parser.parse_args()

def cli() -> Any:
    ''' Core function of CLI
    '''
    args = cliparser()

    root = args.ROOT
    target = args.TARGET
    mode = args.m

    # Default Variables.
    exclude_file = args.exclude_file
    compression = args.compression

    if args.verbose:
        LOGGER.addHandler(CONSOLE_HANDLER)

    handler = Tarpy(
            mode,
            root = root,
            target = target,
            exclude_file = exclude_file,
            compression = compression,
            )
    LOGGER.info('Initialized Tarpy.')
    return handler()
