#!/usr/bin/env python3
"""Logging facilities
"""
import pathlib, os, shutil


def mkdir( path ):

    return pathlib.Path( path ).mkdir( parents=True, exist_ok=True )


def zipdir( path, rootdir, basedir ):

    shutil.make_archive(
      path, 
      'zip',           # the archive format - or tar, bztar, gztar 
      root_dir=rootdir,   # root for archive - current working dir if None
      base_dir=basedir
    )


def cp( source, destination, overwrite = False ):

    if overwrite and os.path.exists(destination):
        
        shutil.rmtree(destination)

    shutil.copytree( source, destination ) 