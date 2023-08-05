#!/usr/bin/env python3


class ApiResolver(object):
    """AWS::ApiGatewayV2::Api Resolver

    Applies to 'BodyS3Location' property. Provide a URI string instead of a
    block to trigger the resolver.

    .. code-block:: yaml

        Resources:
            Foobar:
                Type: AWS::ApiGatewayV2::Api
                Properties: 
                  BodyS3Location: 'file:./sample.json'
    """

    @staticmethod
    def resolve( node, path, context ):
        """a
        """

        key = path

        node[ 'Properties' ][ 'BodyS3Location' ] = {
            'Bucket': context[ 's3' ][ 'bucket' ],
            'Key': key
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