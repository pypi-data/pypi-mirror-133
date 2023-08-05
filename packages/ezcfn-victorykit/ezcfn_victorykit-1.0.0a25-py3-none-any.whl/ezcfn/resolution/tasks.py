#!/usr/bin/env python3
"""Tasks for concurrent CloudFormation template resolution
"""
import pathlib, urllib.parse, json, os, concurrent.futures, hashlib, copy
import cfn_tools
from .resolver import api_gateway, api_gateway_v2, cloudformation, _lambda
from .helper import logging, process, filesystem



FORMAT_YAML = 'yaml'
FORMAT_JSON = 'json'



def _get_basename_extension( path ):

    return os.path.splitext( path )[ 1 ]



def _parse_uri_query_string( query_string ):
    """parse a query string

    :param uri: RFC 2396 conformant URI
    :type uri: stri

    :return: scheme, path, and query segments of URI
    :rtype: (str,str,str)
    """

    fields = urllib.parse.parse_qsl( query_string )

    out = {}

    for field in fields:

        #match query arrays
        if field[ 0 ][-2:] == '[]':

            if field[ 0 ][ :-2 ] not in out.keys(): out[ field[ 0 ][ :-2 ] ] = []
            out[ field[ 0 ][ :-2 ] ].append( field[ 1 ] )
        else:

            out[ field[ 0 ] ] = field[ 1 ]

    return out



def _compile_uri_query_string( options ):
    """compile a URI query string from an option set

    :param options: a set of options
    :type options: dict

    :return: a URI query string
    :rtype: string
    """

    out = []

    for key, value in options.items():

        if key == 'ezcfn': continue

        if isinstance( value, int ) or isinstance( value, str ):

            out.append( f'{key}={value}' )

        if isinstance( value, bool ):

            out.append( f'{key}=%s' % { True: 'true', False: 'false' }[value] )

        if isinstance( value, list ):

            out + [ f'{key}[]={_value}' for _value in value ]

        if isinstance( value, dict ):

            out + [ f'{key}[{_key}]={_value}' for _key, _value in value.items() ]

    return '?' + '&'.join( out ) if len( out ) > 0 else ''



def _parse_uri( uri ):
    """parse segments of a URI string

    :param uri: RFC 2396 conformant URI
    :type uri: stri

    :return: scheme, path, and query segments of URI
    :rtype: (str,str,dict)
    """
    obj = urllib.parse.urlparse( uri )

    query = _parse_uri_query_string( obj.query )

    return obj.scheme, obj.path, query



def _map_tuples_to_dict( _tuple ):
    """map a tuple of tuples to a dictionary

    https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences

    :param tuple: input tuple
    :type tuple: tuple

    :return: a mapped dictionary
    :rtype: dict
    """

    return dict( _tuple )



def _load_yaml( path ):
    """Load a yaml file

    :param path: path to file
    :type path: str

    :return: a dictionary
    :rtype: dict
    """
    with open( path ) as fh:

        data = fh.read()

        return cfn_tools.load_yaml( data )



def _load_json( path ):
    """Load a json file

    :param path: path to file

    :return: a dictionary
    :rtype: dict
    """
    with open( path ) as fh:

        return json.load( fh )



def _dump_yaml( data, path ):
    """Dump dict to filesystem object

    :param data: data to dump into file
    :param type: str

    :param path: path to file
    :param type: str
    """
    
    with open( path, 'w' ) as fh:

        dump = cfn_tools.dump_yaml( data )

        fh.write( dump )



def _init_task_context( type, logical_id, path, context, uri ):
    """Get the initial task context

    path resolution can only be done within the task, since a template 
    resolver (acting as the task scheduler) is oblivious to the output of each 
    task.

    :param type: type of task
    :type type: string

    :param logical_id: the logical id of the CloudFormation stack template 
    resource object/block/node
    :type logical_id: string

    :param path: path for the stack template resolution
    :type: path: str

    :param context: global resolution context
    :type context: dict

    :param context: an unresolved URI string, for scheme compatibilty
    :type context: str

    :return: an initialized task context object
    :rtype: dict
    """

    abspath = path
    if path[ 0 ] != os.path.sep:
        abspath = os.path.abspath( os.path.join( context[ 'cwd' ], path ) )

    prefix = ''
    if 'prefix' in context[ 's3' ].keys() and context[ 's3' ][ 'prefix' ] != None:

        prefix = context[ 's3' ][ 'prefix' ].replace( '/', os.path.sep )

    outpath = None
    _relpath = os.path.relpath( abspath, context[ 'rootdir' ] )
    # if foreign object
    if not os.path.exists( abspath ):

        _relpath = abspath.lstrip( os.path.sep )

        outpath = os.path.join( context[ 'outdir' ], '__external__', prefix, _relpath )

        outpath = os.path.abspath( outpath )
    # if local object, but out of root directory context
    elif _relpath[ :2 ] == '..':

        outpath = os.path.join( context[ 'outdir' ], prefix, '__root__', abspath.lstrip( os.path.sep ) )

        outpath = os.path.abspath( outpath )
    else:

        outpath = os.path.join( context[ 'outdir' ], prefix, _relpath )

        outpath = os.path.abspath( outpath )

    pointer = '.'.join( ( context[ 'namespace' ], logical_id ) )

    stdout, stderr = logging.get_duplex_std_stream( f'{pointer}({type})')

    return {
        **dict(context),
        **{
            'task': {
                'type': type,
                'stdout': stdout,
                'stderr': stderr,
                'pointer': pointer,
                'hash': hashlib.sha256( pointer.encode() ).hexdigest()[:10],
                'uri': uri,
                'outpath': outpath,
                'abspath': abspath
            }
        }
    }



def _init_global_context( logical_id, path, context ):
    """Get the initial global context

    :param logical_id: the logical id of the CloudFormation stack template 
    resource object/block/node
    :type logical_id: string

    :param path: path for the stack template resolution
    :type: path: str

    :param context: global resolution context
    :type context: dict

    :return: an initialized global context
    :rtype: dict
    """

    #set non-existent defaults
    if 'outdir' not in context.keys():

        context[ 'outdir' ] = os.path.join( os.getcwd(), 'ezcfn.out' )
    if 'cachedir' not in context.keys():

        context[ 'cachedir' ] = os.path.join( os.getcwd(), '.ezcfn', 'cache' )
    if 'builddir' not in context.keys():

        context[ 'builddir' ] = os.path.join( os.getcwd(), '.ezcfn', 'build' )

    # make paths absolute
    if context['outdir'][ 0 ] != os.path.sep:

        relpath = os.path.join( os.getcwd(), context[ 'outdir' ] )
        context[ 'outdir' ] = os.path.abspath( relpath )
    if context[ 'cachedir' ][ 0 ] != os.path.sep:

        relpath = os.path.join( os.getcwd(), context[ 'cachedir' ] )
        context[ 'cachedir' ] = os.path.abspath( relpath )
    if context[ 'builddir' ][ 0 ] != os.path.sep:

        relpath = os.path.join( os.getcwd(), context[ 'builddir' ] )
        context[ 'builddir' ] = os.path.abspath( relpath )

    # set working directory
    if path[0] != os.path.sep:

        context[ 'cwd' ] = os.path.dirname( os.path.abspath( path ) )
    else:

        context[ 'cwd' ] = os.path.dirname( path )

    context[ 'namespace' ] = ''
    context[ 'rootdir' ] = context[ 'cwd' ]
    context[ 'tasks' ] = {}

    return context



def _get_annotation( node, resolver, intrinsic = False ):
    """Get ezcfn annotations of a resource node
    
    :param node: CloudFormation resource node/block/object
    :type node: dict

    :param resolver: a resolver instance
    :type resolver: object

    :param intrinsic: flag for evaluation intrinsic annotation
    :type: intrinsic: bool

    :return: annotation set consisting of task type, path, and task options
    :rtype: ( str, str, dict )
    """

    scheme = None
    path = None
    query = {}
    unresolved_uri = None

    if intrinsic:

        if 'Metadata' not in node.keys() or 'ezcfn' not in node[ 'Metadata' ].keys():

            return None, None, None, None

        scheme = node[ 'Metadata' ][ 'ezcfn' ][ 'Type' ] 

        path = node[ 'Metadata' ][ 'ezcfn' ][ 'Path' ]

        if 'Options' in node[ 'Metadata' ][ 'ezcfn' ].keys():
            query =  node[ 'Metadata' ][ 'ezcfn' ][ 'Options' ]

        query_string = _compile_uri_query_string( query )

        unresolved_uri = f'{scheme}:{path}{query_string}'

    else:
        unresolved_uri = resolver.uri( node )

        if unresolved_uri == None: return None, None

        scheme, path, query = _parse_uri( unresolved_uri )

    return scheme, path, query, unresolved_uri



def _get_resolver( logical_id, node, context ):
    """Retrieve a resolver and it's corresponding task

    #        'AWS::Lambda::Function': lambda.FunctionResolver,
    #        'AWS::Lambda::LayerVersion': lambda.LayerVersionResolver,
    #        'AWS::Serverless::Function': serverless.FunctionResolver,
    #        'AWS::AppSync::GraphQLSchema': resolver.AppSync_GraphQLSchema,
    #        'AWS::AppSync::Resolver': resolver.AppSync_Resolver,
    #        'AWS::Serverless::Api': resolver.Serverless_Api,
    #        'AWS::Include': resolver.Include,
    #        'AWS::ElasticBeanstalk::ApplicationVersion': resolver.ElasticBeanstalk_ApplicationVersion,
    #        'AWS::CloudFormation::Stack': resolver.Cloudformation_Stack,
    #        'AWS::Glue::Job': resolver.Glue_Job,
    #        'AWS::StepFunctions::StateMachine': resolver.StepFunctions_StateMachine,

    :param logical_id: logical id of a CloudFormation template resource
    :type logical_id: str

    :param node: fields node of a CloudFormation template resource
    :type node: dict

    :param context: resolution context
    :type context: dict

    :return: a resolver and it's corresponding task
    :rtype: ( typing.Callable, asyncio.Task ),
    """
    resource_type = node[ 'Type' ]

    resolvers = {
        'AWS::ApiGateway::RestApi': api_gateway.RestApiResolver,
        'AWS::ApiGatewayV2::Api': api_gateway_v2.ApiResolver,
        'AWS::CloudFormation::Stack': cloudformation.StackResolver,
        'AWS::Lambda::Function': _lambda.FunctionResolver,
        'AWS::Lambda::LayerVersion': _lambda.LayerVersionResolver
    }

    if resource_type not in resolvers.keys(): return None, None

    resolver = resolvers[ resource_type ]

    scheme, path, options, uri = _get_annotation( node, resolver, context[ 'intrinsic' ] )

    if scheme == None: return None, None

    task = {
        'template':      execute_template_task,
        'docker':        execute_docker_task,
        'file':          execute_file_task,
        'http':          execute_http_task,
        'https':         execute_http_task,
        'script':        execute_script_task,
        'pip':           execute_pip_task,
        'site-packages': execute_site_packages_task,
        'zip':           execute_zip_task,
    }[ scheme ]

    task_args = tuple([ 
        logical_id,
        path,
        _init_task_context( scheme, logical_id, path, context.copy(), uri ),
    ])

    return resolver.resolve, ( task, task_args, options )



def execute_template_task( logical_id, path, context, **options ):
    """Create a concurrent task for handling a CloudFormation template

    :param logical_id: logical id of CloudFormation template resource
    :type logical_id: str

    :param path: path to local object referencing resource
    :type path: str

    :param options:: options specific to task
    :type options: dict

    :param context: resolution context
    :type context: dict

    :return: logical Id, and path to resolved object
    :rtype: ( str, str )
    """
    return _resolve_template( logical_id, path, options, context )



def execute_file_task( logical_id, path, context, **options ):
    """Create a concurrent task for a local file copy

    :param logical_id: logical id of CloudFormation template resource
    :type logical_id: str

    :param path: path to local object referencing resource
    :type path: str

    :param options:: options specific to task
    :type options: dict

    :param context: resolution context
    :type context: dict

    :return: logical Id, and path to resolved object
    :rtype: ( str, str )
    """
    return _copy_file( logical_id, path, options, context )



def execute_zip_task( logical_id, path, context, **options ):
    """Create a concurrent task for zipping a file or directory

    :param logical_id: logical id of CloudFormation template resource
    :type logical_id: str

    :param path: path to local object referencing resource
    :type path: str

    :param options:: options specific to task
    :type options: dict

    :param context: resolution context
    :type context: dict

    :return: logical Id, and path to resolved object
    :rtype: ( str, str )
    """
    return _zip_file( logical_id, path, options, context )



def execute_docker_task( logical_id, path, context, **options ):
    """Create a concurrent task for a Docker build

    :param logical_id: logical id of CloudFormation template resource
    :type logical_id: str

    :param path: path to local object referencing resource
    :type path: str

    :param options:: options specific to task
    :type options: dict

    :param context: resolution context
    :type context: dict

    :Keyword Arguments:
        * *artifact-path* (str) --
          The (in container) path to the final build artifact, optional
        * *build-arg* (dict) --
          Set build-time variables, optional
        * *file* (str) --
          Name of the Dockerfile (Default is 'PATH/Dockerfile'), optional
        * *force-rm* (bool) --
          Always remove intermediate containers, optional
        * *no-cache* (bool) --
          Do not use cache when building the image, optional
        * *pull* (bool) --
          Always attempt to pull a newer version of the image, optional
        * *target* (str) --
          Set the target build stage to build, optional
        * *network* (str) --
          Set the networking mode for the RUN instructions during build 
          (default "default"), optional

    :return: logical Id, and path to resolved object
    :rtype: ( str, str )
    """

    options = {
        **{
            'artifact-path': '/ezcfn.zip',
            'build-arg': {},
            'file': '',
            'force-rm': False,
            'no-cache': False,
            'pull': False,
            'target': '',
            'network': ''
        },
        **options
    }

    return _execute_docker_build( logical_id, path, options, context )



def execute_http_task( logical_id, path, context, **options ):
    """Create a concurrent task for an HTTP GET operation

    :param logical_id: logical id of CloudFormation template resource
    :type logical_id: str

    :param path: path to local object referencing resource
    :type path: str

    :param options:: options specific to task
    :type options: dict

    :param context: resolution context
    :type context: dict

    :return: logical Id, and path to resolved object
    :rtype: ( str, str )
    """
    return _download_file( logical_id, path, options, context )



def execute_script_task( logical_id, path, context, **options ):
    """Create a concurrent task for local script execution

    :param logical_id: logical id of CloudFormation template resource
    :type logical_id: str

    :param path: path to local object referencing resource
    :type path: str

    :param options:: options specific to task
    :type options: dict

    :param context: resolution context
    :type context: dict

    :return: logical Id, and path to resolved object
    :rtype: ( str, str )
    """
    return _execute_script( logical_id, path, options, context )



def execute_site_packages_task( logical_id, path, context, **options ):
    """Create a concurrent task for Pypi builds

    :param logical_id: logical id of CloudFormation template resource
    :type logical_id: str

    :param path: path to local object referencing resource
    :type path: str

    :param options:: options specific to task
    :type options: dict

    :param context: resolution context
    :type context: dict

    :return: logical Id, and path to resolved object
    :rtype: ( str, str )
    """
    logical_id_hash = hashlib.sha256(logical_id.encode()).hexdigest()

    output_basename = ''.join( ( logical_id_hash, '.zip' ) )

    context[ 'node' ] = {}

    if context['flatten']:
        context[ 'node'][ 'outpath' ] = os.path.join(
            context['outdir'],
            output_basename
        )
    else:
        output_dirname = os.path.join( 
            context['outdir'],
            os.path.relpath( path , context[ 'cwd' ] ),
        )

        context[ 'node'][ 'outpath'] = os.path.join(
            output_dirname,
            output_basename
        )

    return _build_pipenv_site_packages( logical_id, path, options, context )



def execute_pip_task( logical_id, path, context, **options ):
    """Create a concurrent task for Pypi builds

    :param logical_id: logical id of CloudFormation template resource
    :type logical_id: str

    :param path: path to local object referencing resource
    :type path: str

    :param options:: options specific to task
    :type options: dict

    :param context: resolution context
    :type context: dict

    :return: logical Id, and path to resolved object
    :rtype: ( str, str )
    """
    return _build_pypi_package( logical_id, path, options, context )



def _execute_tasks( tasks ):
    """execute a set of tasks concurrently

    :param tasks: a list of task definitions ( callable)
    :type tasks: list

    :return: tasks execution results identified by logical ids of nodes
    :rtype: dict
    """

    futures = []
    results = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:

        for task in tasks:

            callable = task[ 0 ]
            args = task[ 1 ]
            kwargs = task[ 2 ] 

            futures.append( executor.submit( callable, *args, **kwargs ) )

        raw_results = tuple( future.result() for future in futures )

        results = _map_tuples_to_dict( raw_results )

    return results



def _get_tasks( nodes, context ):
    """schedule tasks for resources nodes

    if multiple tasks reference the same path and their options are equal the
    latest of these tasks is not being scheduled.

    :param nodes: a CloudFormation template ``Resources`` block/object
    :type tasks: dict
    
    :param context: global resolution context
    :param type: dict

    :return: a tuple of task definition sets (callable, args, and kwargs) 
    and callback map (logical ids of nodes mapped to callables)
    :rtype: ( tuple, dict )
    """

    tasks = []
    callbacks = {}

    for logical_id, node in nodes.items():

        resolver_func, task = _get_resolver( 
            logical_id,
            node,
            context.copy()
        )

        ##task scoped context
        #task_context = task[ 1 ][ 2 ]
        #task_type = task_context[ 'task' ][ 'type' ]
        #task_pointer = task_context[ 'task' ][ 'pointer' ]
        #task_abspath = task_context['task'][ 'abspath' ]
        #task_options = task[ 2 ]
        #
        ##skip a task if another with same options is already scheduled
        #if task_abspath in context[ 'tasks'].keys():
        #
        #    task_registration = context[ 'tasks' ][ task_abspath ]
        #
        #    if task_registration[ 'options' ] == task_options and\
        #       task_registration[ 'type' ] == task_type:
        #
        #        msg  = f'Skipping {task_pointer}, already handled by '
        #        msg += f'{task_registration["pointer"].}'
        #
        #        context[ 'logger' ].warning( 'Skipping' )
        #
        #        task_registration['hooks'].append
        #        continue

        #context[ 'tasks'][ task_context[ 'task' ][ 'abspath' ] ] = {
        #    'type': task_context['task'][ 'type' ],
        #    'options': task[ 2 ],
        #    'pointer': task_pointer,
        #    'hooks': []
        #}

        if resolver_func != None: callbacks[ logical_id ] = resolver_func
        if task != None: tasks.append( task )

    return tasks, callbacks



def _resolve_template( logical_id, path, options, context ):
    """Resolve a CloudFormation template

    If the ``logical_id`` is specified as ``None``, the callable is to be 
    considered the entrypoint of a CloudFormation stack tree traversal. This
    includes nested stacks, which will be resolved recursively.

    :param logical_id: logical id of CloudFormation template resource
    :type logical_id: str

    :param path: path to local object referencing resource
    :type path: str

    :param options:: options specific to task
    :type options: dict

    :param context: resolution context
    :type context: dict

    :return: logical Id, and path to resolved object
    :rtype: ( str, str )
    """
    data = None

    #is root stack - namespace is equivalent to stack nesting level
    if not logical_id:

        data = _load_yaml( path )

        context = _init_global_context( logical_id, path, context )

        context = _init_task_context( 'template', '', path, context, '' )
    else:

        data = _load_yaml( context[ 'task' ][ 'abspath' ] )

        context[ 'namespace' ] = '.'.join( (context[ 'namespace' ], logical_id) )

        #rewrite cwd to reflect nested stack path
        if path[0] != os.path.sep:

            _relpath = os.path.join( context[ 'cwd' ], os.path.dirname( path ) )
            context[ 'cwd' ] = os.path.abspath( _relpath )
        else:
            context[ 'cwd' ] = os.path.dirname( context[ 'task' ][ 'abspath' ] )

    stdout, stderr = ( context[ 'task' ][ 'stdout' ], context[ 'task' ][ 'stderr' ] )

    tasks, callbacks = _get_tasks( data[ 'Resources' ], context )

    task_results = _execute_tasks( tasks )

    _logical_id = None
    for _logical_id, callback in callbacks.items():

        #finally, resolving/rewriting the resource
        data[ 'Resources' ][ _logical_id ] = callback(
            data[ 'Resources'][ _logical_id ],
            os.path.relpath(task_results[ _logical_id ], context['outdir' ] ),
            context
        )

    if not logical_id:

        output_dirname = context['outdir']

        if 'prefix' in context[ 's3' ].keys() and context[ 's3' ][ 'prefix' ] != None:

            output_dirname = os.path.join(
                output_dirname,
                context[ 's3' ][ 'prefix' ].replace( '/', os.path.sep )
            )

        output_path = os.path.join( output_dirname, os.path.basename( path ) )

        output_path = os.path.abspath( output_path )
    else:

        filesystem.mkdir( os.path.dirname( context[ 'task' ][ 'outpath' ] ) )

        output_path = context[ 'task' ][ 'outpath' ]

    _dump_yaml( data, output_path )

    stdout( 'Resolved %d items\n' % ( len( task_results ) ) )

    return logical_id, output_path



def _copy_file( logical_id, path, options, context ):
    """Resolve a local file

    :param logical_id: logical id of CloudFormation template resource
    :type logical_id: str

    :param path: path to local object referencing resource
    :type path: str

    :param options:: options specific to task
    :type options: dict

    :param context: resolution context
    :type context: dict

    :return: logical Id, and path to resolved object
    :rtype: ( str, str )
    """
    outpath= 'copy_file.sample'

    return logical_id, outpath



def _zip_file( logical_id, path, options, context ):
    """Resolve a local file to a zip archive

    :param logical_id: logical id of CloudFormation template resource
    :type logical_id: str

    :param path: path to local object referencing resource
    :type path: str

    :param options:: options specific to task
    :type options: dict

    :param context: resolution context
    :type context: dict

    :return: logical Id, and path to resolved object
    :rtype: ( str, str )
    """
    stdout, stderr = ( context[ 'task' ][ 'stdout' ], context[ 'task' ][ 'stderr' ] )

    output_path = os.path.join( 
        context[ 'task'][ 'outpath' ],
        context[ 'task' ][ 'hash' ]
    )

    abspath = context[ 'task' ][ 'abspath' ]

    filesystem.mkdir( os.path.dirname( output_path ) )

    stdout( f'zip {abspath} -> {output_path}.zip\n' )

    filesystem.zipdir( output_path, context[ 'task' ][ 'abspath' ], None )

    return logical_id, output_path + '.zip'



def _execute_docker_build( logical_id, path, options, context ):
    """Resolve a Docker build execution

    assumes that the build execution stores a ZIP artifact under the root
    directory of the Docker image.

    :param logical_id: logical id of CloudFormation template resource
    :type logical_id: str

    :param path: path to local object referencing resource
    :type path: str

    :param options:: options specific to task
    :type options: dict

    :param context: resolution context
    :type context: dict

    :return: logical Id, and path to resolved object
    :rtype: ( str, str )
    """
    stdout, stderr = ( context[ 'task' ][ 'stdout' ], context[ 'task' ][ 'stderr' ] )

    tag = 'ezcfn-local:' + context[ 'task' ][ 'hash' ]

    process.spawn_pretty( 
        ( 'docker', 'build', '--tag', tag, context[ 'task' ][ 'abspath' ] ),
        stdout,
        stderr
    )

    container_id = process.spawn_pretty( 
        ( 'docker', 'create', tag ),
        stdout,
        stderr
    )

    file_extension = _get_basename_extension( options[ 'artifact-path' ] )

    output_basename = ''.join( ( context['task']['hash'], file_extension ) )

    output_path = os.path.join( context[ 'task'][ 'outpath' ], output_basename )

    filesystem.mkdir( os.path.dirname(output_path) )

    process.spawn_pretty( 
        ( 'docker', 'cp', f'{container_id}:{options["artifact-path"]}', output_path ),
        stdout,
        stderr
    )

    process.spawn_pretty( 
        ( 'docker', 'rm', container_id ),
        stdout,
        stderr
    )

    return logical_id, output_path



def _download_file( logical_id, path, options, context ):
    """Resolve an HTTP file

    :param logical_id: logical id of CloudFormation template resource
    :type logical_id: str

    :param path: path to local object referencing resource
    :type path: str

    :param options:: options specific to task
    :type options: dict

    :param context: resolution context
    :type context: dict

    :return: logical Id, and path to resolved object
    :rtype: ( str, str )
    """
    outpath= 'download_file.sample'

    return logical_id, outpath



def _execute_script( logical_id, path, options, context ):
    """Resolve a local script execution

    assumes that the last line is a path to the resolved object

    :param logical_id: logical id of CloudFormation template resource
    :type logical_id: str

    :param path: path to local object referencing resource
    :type path: str

    :param options:: options specific to task
    :type options: dict

    :param context: resolution context
    :type context: dict

    :return: logical Id, and path to resolved object
    :rtype: ( str, str )
    """
    outpath= 'execute_script.sample'

    return logical_id, outpath



def _build_pipenv_site_packages( logical_id, path, options, context ):
    """Resolve a pypi build execution

    assumes that a ZIP distribution can be build

    :param logical_id: logical id of CloudFormation template resource
    :type logical_id: str

    :param path: path to local object referencing resource
    :type path: str

    :param options:: options specific to task
    :type options: dict

    :param context: resolution context
    :type context: dict

    :return: logical Id, and path to resolved object
    :rtype: ( str, str )
    """
    stdout, stderr = ( context[ 'task' ][ 'stdout' ], context[ 'task' ][ 'stderr' ] )

    #filesystem.mkdir( os.path.join( context[ 'task'][ 'abspath' ], '.venv' ) )

    process.spawn_pretty( 
        ( 'python3', '-m', 'pipenv', 'install' ),
        stdout,
        stderr,
        context[ 'task' ][ 'abspath' ]
    )

    packages_dir = process.spawn_pretty( 
        ( 'python3', '-m', 'pipenv', 'run', 'python3', '-c', 'import site; print(site.getsitepackages()[0])' ),
        stdout,
        stderr,
        context[ 'task' ][ 'abspath' ]
    )

    #get a clean base path of venv directory
    base_path = ''
    for segment in packages_dir.split( os.path.sep ):

        if segment != 'lib': base_path = os.path.sep.join( ( base_path, segment ) )
        else:
            base_path = os.path.sep.join( ( base_path, segment ) )
            base_path = base_path[ 1: ]
            break

    #create an intermediate copy for lambda layer path requirements
    builddirname = os.path.join( context[ 'builddir' ], context[ 'task' ][ 'hash' ] )
    buildpath = os.path.join( builddirname, 'python', 'lib' )
    filesystem.mkdir( buildpath )

    stdout( f'cp {base_path} -> {buildpath}\n' )

    filesystem.cp( base_path, buildpath, True )

    output_path = os.path.join( 
        context[ 'task'][ 'outpath' ],
        context[ 'task' ][ 'hash' ]
    )

    filesystem.mkdir( os.path.dirname( output_path ) )

    stdout( f'zip {buildpath} -> {output_path}.zip\n' )

    filesystem.zipdir( output_path, buildpath, None )

    return logical_id, output_path + '.zip'



def _build_pypi_package( logical_id, path, options, context ):
    """Resolve a pypi build execution

    assumes that a ZIP distribution can be build

    :param logical_id: logical id of CloudFormation template resource
    :type logical_id: str

    :param path: path to local object referencing resource
    :type path: str

    :param options:: options specific to task
    :type options: dict

    :param context: resolution context
    :type context: dict

    :return: logical Id, and path to resolved object
    :rtype: ( str, str )
    """
    outpath= 'build_pypi_package.sample'

    return logical_id, outpath