#!/usr/bin/env python3
"""Child process facilities
"""
import subprocess


def spawn_pretty( cmd, stdout, stderr, cwd = None ):

    stdout( '[START] %s\n' % ' '.join( cmd ) )

    result = spawn( 
        cmd,
        stdout,
        stderr,
        cwd
    )

    stdout( '[END] %s\n' % ' '.join( cmd ) )

    return result


def spawn( cmd, stdout, stderr, cwd = None ):

    proc = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        cwd = cwd
    )

    iserr = False
    last_lines = []
    out_line = None

    while True:

        if len( last_lines ) == 5: last_lines.pop( 0 )

        if out_line != None and out_line != b'': last_lines.append( out_line.rstrip() )

        #read output
        out_line = proc.stdout.readline()

        #no more output
        if out_line == b'' and proc.poll() is not None: break

        #write output
        if out_line: stdout( str( out_line.decode() ) )

    if proc.returncode != 0:

        err_line = proc.stderr.readline()
        while err_line != b'':

            stderr( str( err_line.decode() ) )

            err_line = proc.stderr.readline()

            raise BaseException( ' '.join( cmd ) + ' returned non-zero status code: %d' % proc.returncode )

    #find the last non-empty line
    for line in reversed( last_lines ):

        if line != b'': return line.decode()

    return None
