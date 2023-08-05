#!/usr/bin/env python3
"""ezcfn - AWS CloudFormation Template Bootstrap

Copyright (C) 2021  Tiara Rodney (victoryk.it)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
import argparse, os


def main():

    parser = argparse.ArgumentParser( 'ezcfn', description=__doc__, formatter_class=argparse.RawTextHelpFormatter )

    sp = parser.add_subparsers( dest = 'command', required = True )

    resolve_parser = sp.add_parser( 'resolve' )

    resolve_parser.add_argument(
        'path',
        metavar='PATH',
        help = 'use paths relative to current working directory for path outputs',
        default = os.getcwd()
    )

    resolve_parser.add_argument(
        'pointer',
        metavar='POINTER',
        nargs='?',
        help = 'use paths relative to current working directory for path outputs',
        default='.',
    )

    resolve_parser.add_argument(
        '--s3-bucket',
        required=True,
        help = 'use paths relative to current working directory for path outputs',
    )

    resolve_parser.add_argument(
        '--s3-region',
        required=True,
        help = 'use paths relative to current working directory for path outputs',
    )

    resolve_parser.add_argument(
        '--s3-prefix',
        help = 'use paths relative to current working directory for path outputs',
    )
    
    resolve_parser.add_argument(
        '--flatten',
        action='store_true',
        help = 'use paths relative to current working directory for path outputs',
    )

    resolve_parser.add_argument(
        '--intrinsic',
        action='store_true',
        help = 'use paths relative to current working directory for path outputs',
    )
    
    resolve_parser.add_argument(
        '--outdir',
        help = 'use paths relative to current working directory for path outputs',
        default='ezcfn.out'
    )

    args = vars( parser.parse_args() )

    from . import resolution

    resolution.resolve(
        args['path'],
        args['s3_bucket'],
        args['s3_region'],
        args['s3_prefix'],
        args[ 'flatten' ],
        args[ 'intrinsic' ]
     )



if __name__ == '__main__':

    main()