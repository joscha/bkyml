#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import argparse
import sys
import logging
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

from bkyml import __version__

__author__ = "Joscha Feth"
__copyright__ = "Joscha Feth"
__license__ = "mit"

_logger = logging.getLogger(__name__)

class MyYAML(YAML):
    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()

yaml = MyYAML()
yaml.default_flow_style = False

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
         raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

def ns_hasattr(ns, attr):
    return hasattr(ns, attr) and getattr(ns, attr) is not None

def tuples_to_dict(tuples):
    ret = {}
    for tuple in tuples:
        ret[tuple[0]] = tuple[1]
    return ret

def singlify(a_list):
    if len(a_list) == 1:
        return a_list[0]
    else:
        return a_list

def comment(ns):
    lines = "\n# ".join(' '.join(ns.str).splitlines())
    return f"# {lines}"

def steps(ns):
    return "steps:"

def env(ns):
    return yaml.dump({ 'env': tuples_to_dict(ns.var) })

def command(ns):
    step = {}

    # label
    if ns_hasattr(ns, 'label'):
        step['label'] = ns.label

    # command (required)
    assert ns_hasattr(ns, 'command')
    command = sum(ns.command, [])
    step['command'] = singlify(command)

    # branches
    if ns_hasattr(ns, 'branches'):
        step['branches'] = ' '.join(ns.branches)

    # env
    if ns_hasattr(ns, 'env'):
        step['env'] = tuples_to_dict(ns.env)

    # agents
    if ns_hasattr(ns, 'agents'):
        step['agents'] = tuples_to_dict(ns.agents)

    # artifact_paths
    if ns_hasattr(ns, 'artifact_paths'):
        artifact_paths = sum(ns.artifact_paths, [])
        step['artifact_paths'] = singlify(artifact_paths)

    # parallelism
    if ns_hasattr(ns, 'parallelism') and ns.parallelism > 1:
        step['parallelism'] = ns.parallelism

    # concurrency and concurrency_group
    if ns_hasattr(ns, 'concurrency') and ns_hasattr(ns, 'concurrency_group'):
        step['concurrency'] = ns.concurrency
        step['concurrency_group'] = ns.concurrency_group

    yaml.indent(sequence=4, offset=2)
    return yaml.dump([ step ])

def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Generate pipeline YAML for Buildkite")

    subparsers = parser.add_subparsers(title='subcommands',
                                       description='valid subcommands',
                                       help='additional help')
    parser_comment = subparsers.add_parser('comment')
    parser_comment.add_argument(
        dest="str",
        help="Comment",
        type=str,
        nargs='+',
        metavar="COMMENT")
    parser_comment.set_defaults(func=comment)
    parser_steps = subparsers.add_parser('steps')
    parser_steps.set_defaults(func=steps)

    parser_env = subparsers.add_parser('env')
    parser_env.add_argument(
        '--var',
        help="A map of environment variables for this pipeline.",
        type=str,
        nargs=2,
        action='append',
        metavar=('KEY', 'VALUE'),
        required=True
    )
    parser_env.set_defaults(func=env)

    parser_command = subparsers.add_parser('command')
    parser_command.add_argument(
        '--command',
        help="The shell command/s to run during this step.",
        nargs='+',
        action='append',
        type=str,
        metavar="COMMAND",
        required=True)
    parser_command.add_argument(
        '--label',
        help="The label that will be displayed in the pipeline visualisation in Buildkite. Supports emoji.",
        type=str,
        metavar="LABEL")
    parser_command.add_argument(
        '--branches',
        help="The branch pattern defining which branches will include this step in their builds.",
        type=str,
        nargs='+',
        metavar="BRANCH_PATTERN"
    )
    parser_command.add_argument(
        '--env',
        help="A map of environment variables for this step.",
        type=str,
        nargs=2,
        action='append',
        metavar=('KEY', 'VALUE')
    )
    parser_command.add_argument(
        '--agents',
        help="A map of meta-data keys to values to target specific agents for this step.",
        type=str,
        nargs=2,
        action='append',
        metavar=('KEY', 'VALUE')
    )
    parser_command.add_argument(
        '--artifact-paths',
        help="The glob path or paths where artifacts from this step will be uploaded.",
        nargs='+',
        action='append',
        type=str,
        metavar="GLOB_OR_PATH"
    )
    parser_command.add_argument(
        '--parallelism',
        help="The number of parallel jobs that will be created based on this step.",
        type=check_positive,
        metavar="POSITIVE_NUMBER"
    )
    parser_command.add_argument(
        '--concurrency',
        help="The maximum number of jobs created from this step that are allowed to run at the same time. Requires --concurrency-group.",
        type=check_positive,
        metavar="POSITIVE_NUMBER"
    )
    parser_command.add_argument(
        '--concurrency-group',
        help="A unique name for the concurrency group that you are creating with the concurrency attribute.",
        type=str,
        metavar="GROUP_NAME"
    )

    parser_command.set_defaults(func=command)

    parser.add_argument(
        '--version',
        action='version',
        version='bkyml {ver}'.format(ver=__version__))
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)

    parsed = parser.parse_args(args)
    if ns_hasattr(parsed, 'concurrency') and not ns_hasattr(parsed, 'concurrency_group'):
        parser.error("--concurrency requires --concurrency-group.")
    return parsed

def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")

def parse_main(args):
    args = parse_args(args)

    setup_logging(args.loglevel)
    if hasattr(args, 'func'):
        return args.func(args)
    else:
        return None

def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    ret = parse_main(args)
    _logger.debug("Calling function")
    if ret != None:
        print(ret)
    _logger.info("Script ends here")

def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
