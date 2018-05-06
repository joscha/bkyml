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
        stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        return stream.getvalue()

yaml = MyYAML()
yaml.default_flow_style = False

retry_manual_allowed_default = True
retry_manual_permit_on_passed_default = False

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

def bool_or_string(value):
    if value.lower() == 'true':
        return True
    if value.lower() == 'false':
        return False
    return value

def int_or_star(value):
    if value == '*':
        return value
    else:
        try:
            return int(value)
        except ValueError:
            raise argparse.ArgumentTypeError("%s is an invalid value" % value)

def ns_hasattr(namespace, attr):
    return hasattr(namespace, attr) and getattr(namespace, attr) is not None

def tuples_to_dict(tuples):
    ret = {}
    for tpl in tuples:
        ret[tpl[0]] = tpl[1]
    return ret

def singlify(a_list):
    if len(a_list) == 1:
        return a_list[0]
    return a_list

class Comment:
    @staticmethod
    def install(action):
        parser = action.add_parser('comment')
        parser.add_argument(
            dest="str",
            help="Comment",
            type=str,
            nargs='+',
            metavar="COMMENT")
        parser.set_defaults(func=Comment.comment)

    @staticmethod
    def comment(namespace):
        lines = "\n# ".join(' '.join(namespace.str).splitlines())
        return f"# {lines}"

class Steps:
    @staticmethod
    def install(action):
        parser = action.add_parser('steps')
        parser.set_defaults(func=Steps.steps)

    @staticmethod
    def steps(namespace):
        return "steps:"

class Env:
    @staticmethod
    def install(action):
        parser = action.add_parser('env')
        parser.add_argument(
            '--var',
            help="A map of environment variables for this pipeline.",
            type=str,
            nargs=2,
            action='append',
            metavar=('KEY', 'VALUE'),
            required=True
        )
        parser.set_defaults(func=Env.env)

    @staticmethod
    def env(namespace):
        return yaml.dump({
            'env': tuples_to_dict(namespace.var),
        })

class Command:

    # pylint: disable=line-too-long
    @staticmethod
    def install(action):
        parser = action.add_parser('command')
        parser.add_argument(
            '--command',
            help="The shell command/s to run during this step.",
            nargs='+',
            action='append',
            type=str,
            metavar="COMMAND",
            required=True)
        parser.add_argument(
            '--label',
            help="The label that will be displayed in the pipeline visualisation in Buildkite. Supports emoji.",
            type=str,
            metavar="LABEL")
        parser.add_argument(
            '--branches',
            help="The branch pattern defining which branches will include this step in their builds.",
            type=str,
            nargs='+',
            metavar="BRANCH_PATTERN"
        )
        parser.add_argument(
            '--env',
            help="A map of environment variables for this step.",
            type=str,
            nargs=2,
            action='append',
            metavar=('KEY', 'VALUE')
        )
        parser.add_argument(
            '--agents',
            help="A map of meta-data keys to values to target specific agents for this step.",
            type=str,
            nargs=2,
            action='append',
            metavar=('KEY', 'VALUE')
        )
        parser.add_argument(
            '--artifact-paths',
            help="The glob path or paths where artifacts from this step will be uploaded.",
            nargs='+',
            action='append',
            type=str,
            metavar="GLOB_OR_PATH"
        )
        parser.add_argument(
            '--parallelism',
            help="The number of parallel jobs that will be created based on this step.",
            type=check_positive,
            metavar="POSITIVE_NUMBER"
        )
        parser.add_argument(
            '--concurrency',
            help="The maximum number of jobs created from this step that are allowed to run at the same time. Requires --concurrency-group.",
            type=check_positive,
            metavar="POSITIVE_INT"
        )
        parser.add_argument(
            '--concurrency-group',
            help="A unique name for the concurrency group that you are creating with the concurrency attribute.",
            type=str,
            metavar="GROUP_NAME"
        )
        parser.add_argument(
            '--timeout-in-minutes',
            help="The number of minutes a job created from this step is allowed to run. If the job does not finish within this limit, it will be automatically cancelled and the build will fail.",
            type=int,
            metavar="TIMEOUT"
        )
        parser.add_argument(
            '--skip',
            help="Whether to skip this step or not.",
            type=bool_or_string,
            metavar="BOOL_OR_STRING"
        )
        parser.add_argument(
            '--retry',
            help="The conditions for retrying this step.",
            choices=['automatic', 'manual']
        )
        parser.add_argument(
            '--retry-automatic-exit-status',
            help="The exit status number that will cause this job to retry.",
            type=int_or_star,
            metavar='INT_OR_STAR'
        )
        parser.add_argument(
            '--retry-automatic-limit',
            help="The number of times this job can be retried. The maximum value this can be set to is 10.",
            type=check_positive,
            metavar="POSITIVE_INT"
        )
        parser.add_argument(
            '--retry-automatic-tuple',
            help="The exit status number that will cause this job to retry and a limit to go with it.",
            type=int_or_star,
            nargs=2,
            action='append',
            metavar=('INT_OR_STAR', 'POSITIVE_INT')
        )
        parser.add_argument(
            '--retry-manual-allowed',
            help="This job can be retried manually.",
            dest="retry_manual_allowed",
            action='store_true'
        )
        parser.add_argument(
            '--no-retry-manual-allowed',
            help="This job can not be retried manually.",
            dest="retry_manual_allowed",
            action='store_false'
        )
        parser.set_defaults(retry_manual_allowed=retry_manual_allowed_default)
        parser.add_argument(
            '--retry-manual-reason',
            help="A string that will be displayed in a tooltip on the Retry button in Buildkite.",
            type=str,
            metavar='REASON'
        )
        parser.add_argument(
            '--retry-manual-permit-on-passed',
            help="This job can be retried after it has passed.",
            dest="retry_manual_permit_on_passed",
            action='store_true'
        )
        parser.add_argument(
            '--no-retry-manual-permit-on-passed',
            help="This job can not be retried after it has passed.",
            dest="retry_manual_permit_on_passed",
            action='store_false'
        )
        parser.set_defaults(retry_manual_permit_on_passed=retry_manual_permit_on_passed_default)

        parser.set_defaults(func=Command.command)

    @staticmethod
    def assert_post_parse(parsed, parser):
        if ns_hasattr(parsed, 'concurrency') and not ns_hasattr(parsed, 'concurrency_group'):
            parser.error("--concurrency requires --concurrency-group.")

        if not ns_hasattr(parsed, 'retry') or (ns_hasattr(parsed, 'retry') and parsed.retry != 'automatic'):
            if ns_hasattr(parsed, 'retry_automatic_exit_status'):
                parser.error('--retry-automatic-exit-status requires --retry automatic.')

            if ns_hasattr(parsed, 'retry_automatic_limit'):
                parser.error('--retry-automatic-limit requires --retry automatic.')

            if ns_hasattr(parsed, 'retry_automatic_tuple'):
                parser.error('--retry-automatic-tuple requires --retry automatic.')

        if ns_hasattr(parsed, 'retry_automatic_tuple') and ns_hasattr(parsed, 'retry_automatic_exit_status'):
            parser.error('--retry-automatic-tuple can not be combined with --retry-automatic-exit-status.')

        if ns_hasattr(parsed, 'retry_automatic_tuple') and ns_hasattr(parsed, 'retry_automatic_limit'):
            parser.error('--retry-automatic-tuple can not be combined with --retry-automatic-limit.')

        if not ns_hasattr(parsed, 'retry') or (ns_hasattr(parsed, 'retry') and parsed.retry != 'manual'):
            if ns_hasattr(parsed, 'retry_manual_allowed') and parsed.retry_manual_allowed is not retry_manual_allowed_default:
                parser.error('--[no-]retry-manual-allowed requires --retry manual.')

            if ns_hasattr(parsed, 'retry_manual_permit_on_passed') and parsed.retry_manual_permit_on_passed is not retry_manual_permit_on_passed_default:
                parser.error('--[no-]retry-manual-permit-on-passed requires --retry manual.')

            if ns_hasattr(parsed, 'retry_manual_reason'):
                parser.error('--retry-manual-reason requires --retry manual.')

    @staticmethod
    def command(namespace):
        step = {}

        # label
        if ns_hasattr(namespace, 'label'):
            step['label'] = namespace.label

        # command (required)
        assert ns_hasattr(namespace, 'command')
        command = sum(namespace.command, [])
        assert command
        step['command'] = singlify(command)

        # branches
        if ns_hasattr(namespace, 'branches'):
            step['branches'] = ' '.join(namespace.branches)

        # env
        if ns_hasattr(namespace, 'env'):
            step['env'] = tuples_to_dict(namespace.env)

        # agents
        if ns_hasattr(namespace, 'agents'):
            step['agents'] = tuples_to_dict(namespace.agents)

        # artifact_paths
        if ns_hasattr(namespace, 'artifact_paths'):
            artifact_paths = sum(namespace.artifact_paths, [])
            if artifact_paths:
                step['artifact_paths'] = singlify(artifact_paths)

        # parallelism
        if ns_hasattr(namespace, 'parallelism'):
            assert check_positive(namespace.parallelism)
            if namespace.parallelism > 1:
                step['parallelism'] = namespace.parallelism

        # concurrency and concurrency_group
        if ns_hasattr(namespace, 'concurrency') and ns_hasattr(namespace, 'concurrency_group'):
            assert check_positive(namespace.concurrency)
            step['concurrency'] = namespace.concurrency
            step['concurrency_group'] = namespace.concurrency_group

        # timeout_in_minutes
        if ns_hasattr(namespace, 'timeout_in_minutes') and namespace.timeout_in_minutes > 0:
            step['timeout_in_minutes'] = namespace.timeout_in_minutes

        # skip
        if ns_hasattr(namespace, 'skip') and (namespace.skip is True or type(namespace.skip) is str):
            step['skip'] = namespace.skip

        # retry
        if ns_hasattr(namespace, 'retry'):
            retry = {}
            retry[namespace.retry] = {}

            if namespace.retry == 'automatic':
                if ns_hasattr(namespace, 'retry_automatic_exit_status'):
                    retry[namespace.retry]['exit_status'] = namespace.retry_automatic_exit_status
                if ns_hasattr(namespace, 'retry_automatic_limit'):
                    retry[namespace.retry]['limit'] = min(10, namespace.retry_automatic_limit)
                if ns_hasattr(namespace, 'retry_automatic_tuple'):
                    if namespace.retry_automatic_tuple:
                        retry[namespace.retry] = []
                        for tpl in namespace.retry_automatic_tuple:
                            retry[namespace.retry].append({
                                'exit_status': int_or_star(tpl[0]),
                                'limit': min(10, check_positive(tpl[1])),
                            })
            elif namespace.retry == 'manual':
                if ns_hasattr(namespace, 'retry_manual_allowed') and not namespace.retry_manual_allowed:
                    retry[namespace.retry]['allowed'] = namespace.retry_manual_allowed
                if ns_hasattr(namespace, 'retry_manual_reason'):
                    retry[namespace.retry]['reason'] = namespace.retry_manual_reason
                if ns_hasattr(namespace, 'retry_manual_permit_on_passed') and namespace.retry_manual_permit_on_passed:
                    retry[namespace.retry]['permit_on_passed'] = namespace.retry_manual_permit_on_passed
            else:
                raise argparse.ArgumentTypeError("%s is an invalid retry value" % namespace.retry)

            if not retry[namespace.retry]:
                retry[namespace.retry] = True
            step['retry'] = retry

        yaml.indent(sequence=4, offset=2)
        return yaml.dump([step])

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

    Comment.install(subparsers)
    Steps.install(subparsers)
    Env.install(subparsers)
    Command.install(subparsers)

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
    Command.assert_post_parse(parsed, parser)
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
    return None

def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    ret = parse_main(args)
    _logger.debug("Calling function")
    if ret is not None:
        print(ret)
    _logger.info("Script ends here")

def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
