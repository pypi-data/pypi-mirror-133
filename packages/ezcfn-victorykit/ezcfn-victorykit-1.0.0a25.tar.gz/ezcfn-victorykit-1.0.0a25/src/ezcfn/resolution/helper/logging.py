#!/usr/bin/env python3
"""Logging facilities
"""
import sys, random
from . import stdsync


UNIQUE_TERM_COLORS = []


def _get_unique_ansi_color():
    """retrieve an ANSI color unique to runtime

    :return: unique ANSI color code
    :rtype: int
    """

    codes = [ 30, 31, 32, 33, 34, 35, 36, 37, 90, 91, 92, 93, 94, 95, 96, 97 ]

    choice = None
    tries = 0
    while tries < len( codes ):

        choice = random.randrange( len( codes ) - 1 )

        if codes[ choice ] in UNIQUE_TERM_COLORS:

            tries += 1

            continue

        break

    #if all colors exhausted, return last try
    UNIQUE_TERM_COLORS.append( codes[ choice ] )

    return codes[ choice ]



class TerminalWriter:
    """std-like file object
    """

    _ansi_color = None

    def __init__( self, prefix, obj, color = None ):

        self._prefix = prefix
        self._obj = obj

        if color: self._ansi_color = color

    def write( self, data ):

        prefix = ''
        suffix = ''

        if self._ansi_color != None:

            color_prefix = f'\u001b[{self._ansi_color}m'
            color_suffix = '\u001b[0m'

        self._obj.write( f'{color_prefix}{self._prefix}{data}{color_suffix}' )



def _write_duplex( data, fwrite = None, swrite = None ):
    """duplex-call write callables

    :param data: data to write
    :type data: str

    :param fwrite: first write callable
    :type fwrite: callable

    :param swrite: second write callable
    :type swrite: callable

    :rtype: None
    """

    if fwrite: fwrite( data )
    if swrite: swrite( data )



def get_duplex_std_stream( id, std = True, path = None ):
    """get write stream callables

    conditionally creates shell and filesystem object write streams

    :param std: flag for creating std callables
    :type std: bool, optional

    :param path: path to filesystem object
    :type path: str

    :returns: tuple of ``out`` and ``err`` write callables
    :rtype: tuple
    """

    shouths = []
    sherrhs = []
    fhouths = []
    fherrhs = []

    ansi_color = _get_unique_ansi_color()

    sout = None
    serr = None
    if std:
        shouths.append( TerminalWriter( f'{id}: ', sys.stdout, ansi_color ) )
        sherrhs.append( TerminalWriter( f'{id}: [ERROR] ', sys.stderr, ansi_color ) )
        sout, serr = stdsync.open( id, shouths, sherrhs )

    fout = None
    ferr = None
    if path:
        fhouths.append( open( f'{path}', 'w' ) )
        fherrhs.append( open( f'{path}.err', 'w' ) )
        fout, ferr = stdsync.open( id, fhouths, fherrhs )

    out = lambda data: _write_duplex( data, sout, fout )
    err = lambda data: _write_duplex( data, serr, ferr )

    return out, err