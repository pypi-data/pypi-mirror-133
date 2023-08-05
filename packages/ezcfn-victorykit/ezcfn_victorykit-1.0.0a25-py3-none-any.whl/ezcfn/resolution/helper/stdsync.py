#!/usr/bin/env python3
"""Thread-Safe Synchronized Output
"""
import time, threading, atexit


# stream instances
__ISTREAM = {}
# stream cache
__ICACHE = {}
# stream states
__ISTATE = {}

STATE_UNBLOCKED = 0
STATE_BLOCKED = 1



def _stdout_id( name ):

    return f'{name}.stdout'



def _stderr_id( name ):

    return f'{name}.stderr'



def _write( stream_id, data ):

    __ICACHE[ stream_id ].append( ( stream_id, data ) )

    # so that we don't have to spawn another thread
    if __ISTATE[ stream_id ] == STATE_BLOCKED: return

    threading.Thread(target=_handle, args=( stream_id, ) ).start()



def _handle( stream_id ):

    __ISTATE[ stream_id ] = STATE_BLOCKED

    chunk_index = 0
    while chunk_index < len( __ICACHE[ stream_id ] ):

        if __ICACHE[ stream_id ][ chunk_index ][ 0 ] == stream_id:

            stream_id, data = __ICACHE[ stream_id ].pop( chunk_index )

            for handler in __ISTREAM[ stream_id ]: handler.write( data )

    __ISTATE[ stream_id ] = STATE_UNBLOCKED

    return



async def _close( stream_id ):

    while __ISTATE[ stream_id ] == 1: time.sleep( 1 )

    __ISTREAM[ stream_id ].close()

    return



def _cleanup():

    handles = []

    while STATE_BLOCKED in __ISTATE.values():

        for stream_id, state in __ISTATE.items():

            if state == STATE_BLOCKED: continue

        time.sleep( 0.5 )

    return



def _append_handler( stream_id, handler ):

    if handler not in __ISTREAM[ stream_id ]:

        __ISTREAM[ stream_id ].append( handler )

        return True

    return False



def open( name, ouths, errhs = None ):
    """open a synchronized stream writer

    will return write callables for out.write and err.write.

    Each name is linked to a singleton stream.

    The module is oblivious to the backend of file-like objects. One can 
    therefore implement two streams with differing file object handlers 
    pointing to the same e.g. filesystem object. This will make the module not
    thread-safe.

    .. code-block:: yaml

        #this is not thread-safe
        fh1 = open( 'foo.txt', 'w' )
        stdsync.open( 'stream1', ( fh1, ) )
        fh2 = open( 'foo.txt', 'w' )
        stdsync.open( 'stream2', ( fh2, ) )

    :param name: name of stream
    :type name: str

    :param ouths: list of stdout handlers (file-objects)
    :type ouths: list

    :param errs: list of stderr handlers (file-objects)
    :type errs: list

    :returns: tuple of write callables
    :rtype: tuple
    """

    out_id = _stdout_id( name )
    err_id = _stderr_id( name )

    if out_id not in __ISTREAM.keys(): 

        __ISTREAM[ out_id ] = ouths
        __ISTATE[ out_id ]  = STATE_UNBLOCKED
        __ICACHE[ out_id ]  = []

    else:

        for handler in ouths: _append_handler( out_id, handler )

    out = lambda data: _write( out_id, data )

    err = None

    if errhs != None and err_id not in __ISTREAM.keys(): 

        __ISTREAM[ err_id ] = errhs
        __ISTATE[ err_id ]  = STATE_UNBLOCKED
        __ICACHE[ err_id ]  = []

    elif errhs != None:

        for handler in errhs: _append_handler( err_id, handler )

    if errhs != None: err = lambda data: _write( err_id, data )


    return out, err



atexit.register( _cleanup )