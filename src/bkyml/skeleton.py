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

def ns_hasattr(ns, attr):
    return hasattr(ns, attr) and getattr(ns, attr) != None

def parse_env_pairs(env_pairs):
    pairs = [ pair.split('=', 1) for pair in env_pairs ]
    env_vars = {}
    for pair in pairs:
        if len(pair) == 2 and pair[0] != '':
            env_vars[pair[0]] = pair[1]
    return env_vars

def comment(ns):
    lines = "\n# ".join(' '.join(ns.str).splitlines())
    return f"# {lines}"

def steps(ns):
    return "steps:"

def env(ns):
    env_vars = parse_env_pairs(ns.env_pairs)
    if len(env_vars) == 0:
        return None
    else:
        return yaml.dump({ 'env': env_vars })

def command(ns):
    step = {}

    # label
    if ns_hasattr(ns, 'label'):
        step['label'] = ns.label

    # command
    assert ns_hasattr(ns, 'command')
    command = sum(ns.command, [])
    if len(command) == 1:
        command = command[0]
    step['command'] = command

    if ns_hasattr(ns, 'branches'):
        step['branches'] = ' '.join(ns.branches)

    if ns_hasattr(ns, 'env'):
        env_vars = parse_env_pairs(ns.env)
        if len(env_vars) > 0:
            step['env'] = env_vars

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
        metavar="STRING")
    parser_comment.set_defaults(func=comment)
    parser_steps = subparsers.add_parser('steps')
    parser_steps.set_defaults(func=steps)

    parser_env = subparsers.add_parser('env')
    parser_env.add_argument(
        'env_pairs',
        help="set env vars via a=b",
        nargs='+'
    )
    parser_env.set_defaults(func=env)

    parser_command = subparsers.add_parser('command')
    parser_command.add_argument(
        '--command',
        help="The shell command/s to run during this step.",
        nargs='+',
        action='append',
        type=str,
        metavar="STRING",
        required=True)
    parser_command.add_argument(
        '--label',
        help="The label that will be displayed in the pipeline visualisation in Buildkite. Supports emoji.",
        type=str,
        metavar="STRING")
    parser_command.add_argument(
        '--branches',
        help="The branch pattern defining which branches will include this step in their builds.",
        type=str,
        nargs='*',
        metavar="STRING"
    )
    parser_command.add_argument(
        '--env',
        help="A map of environment variables for this step. Set via a=b.",
        type=str,
        nargs='*',
        metavar="ENV_PAIR"
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
    return parser.parse_args(args)


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
