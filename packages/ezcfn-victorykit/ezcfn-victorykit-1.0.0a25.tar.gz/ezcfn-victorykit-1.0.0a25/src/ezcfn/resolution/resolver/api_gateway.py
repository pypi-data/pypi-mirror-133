#!/usr/bin/env python3


class RestApiResolver(object):
    """AWS::ApiGateway::RestApi Resolver

    applies to 'BodyS3Location' property
    """

    @staticmethod
    def resolve( node, path, context ):
        """a
        """

        node[ 'Properties' ][ 'BodyS3Location' ] = {
            'Bucket': context[ 's3' ][ 'bucket' ],
            'Key': path
        }

        return node

    @staticmethod
    def uri( node ):
        """a
        """

        if 'BodyS3Location' in node[ 'Properties' ].keys():

            if isinstance( node[ 'Properties' ][ 'BodyS3Location' ], str ):

                return node[ 'Properties' ][ 'BodyS3Location' ]

        return None