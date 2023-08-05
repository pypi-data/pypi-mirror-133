#!/usr/bin/env python3


class FunctionResolver(object):
    """AWS::Lambda::Function

    applies to 'Code' property
    """

    @staticmethod
    def resolve( node, path, context ):
        """a
        """

        node[ 'Properties' ][ 'Code' ] = {
            'S3Bucket': context[ 's3' ][ 'bucket' ],
            'S3Key': path
        }

        return node

    @staticmethod
    def uri( node ):
        """a
        """

        if 'Code' in node[ 'Properties' ].keys():

            if isinstance( node[ 'Properties' ][ 'Code' ], str ):

                return node[ 'Properties' ][ 'Code' ]

        return None



class LayerVersionResolver(object):
    """AWS::Lambda::LayerVersion

    applies to 'Content' property
    """

    @staticmethod
    def resolve( node, path, context ):
        """a
        """

        node[ 'Properties' ][ 'Content' ] = {
            'S3Bucket': context[ 's3' ][ 'bucket' ],
            'S3Key': path
        }

        return node

    @staticmethod
    def uri( node ):
        """a
        """

        if 'Content' in node[ 'Properties' ].keys():

            if isinstance( node[ 'Properties' ][ 'Content' ], str ):

                return node[ 'Properties' ][ 'Content' ]

        return None