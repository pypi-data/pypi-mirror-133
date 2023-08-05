#!/usr/bin/env python3


class StackResolver(object):
    """AWS::CloudFormation::Stack Resolver

    applies to 'TemplateURL' property
    """

    @staticmethod
    def resolve( node, path, context ):
        """a
        """

        region = context[ 's3' ][ 'region' ]
        bucket = context[ 's3' ][ 'bucket' ]
        key = path

        url = f'https://s3-{region}.amazonaws.com/{bucket}/{key}'

        node[ 'Properties' ][ 'TemplateURL' ] = url

        return node

    @staticmethod
    def uri( node ):
        """a
        """

        if 'TemplateURL' in node[ 'Properties' ].keys():

            if isinstance( node[ 'Properties' ][ 'TemplateURL' ], str ):

                return node[ 'Properties' ][ 'TemplateURL' ]

        return None