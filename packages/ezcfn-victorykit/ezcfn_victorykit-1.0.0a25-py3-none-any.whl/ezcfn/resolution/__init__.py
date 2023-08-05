#!/usr/bin/env python3
"""Utilities for resolving CloudFormation templates
"""
import logging
from . import tasks


def _get_default_logger():
    """get a standard logger

    :return: a logger instance
    :rtype: logging.Logger
    """

    logger = logging.getLogger( 'ezcfn' )
    logger.setLevel( logging.ERROR )

    ch = logging.StreamHandler()
    ch.setLevel( logging.ERROR )

    formatter = logging.Formatter( '%(asctime)s - %(name)s - %(levelname)s - %(message)s' )

    ch.setFormatter( formatter )

    logger.addHandler(ch)

    return logger



def resolve(
    path, 
    s3bucket,
    s3region,
    s3prefix = '', 
    flatten = False,
    intrinsic = False,
    outdir = 'ezcfn.out', 
    logger = None
):
    """resolve a local CloudFormation template

    :param path: path to root template file
    :type path: str

    :param s3bucket: name of an S3 bucket
    :type s3bucket: str

    :param s3bucket: region S3 bucket resides in
    :type s3bucket: str

    :param s3prefix: prefix to apply to S3 objects
    :type s3prefix: str, optional

    :param flatten: to preserve directory structure or not
    :type flatten: bool, optional

    :param intrinsic: inspect resource metadata
    :type flatten: bool, optional

    :param outdir: directory path to store resolved template tree under
    :type outdir: str, optional

    :param logger: logger instance
    :type logger: logging.Logger, optional

    :return: path to resolved CloudFormation root template
    :rtype: str
    """

    context = {
        'flatten': flatten,
        'intrinsic': intrinsic,
        'outdir': outdir,
        'logger': logger if logger != None else _get_default_logger(),
        's3': {
            'bucket': s3bucket,
            'region': s3region,
            'prefix': s3prefix
        }
    }

    return tasks._resolve_template( None, path, {}, context )[ 1 ]