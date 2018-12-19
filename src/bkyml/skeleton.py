#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Module to produce valid YAML for Buildkite
    see https://buildkite.com/docs/pipelines/defining-steps
'''
from __future__ import division, print_function, absolute_import

import argparse
import sys
import logging
from ruamel.yaml import YAML as RuamelYaml
from ruamel.yaml.compat import StringIO
from ruamel.yaml.comments import CommentedMap

from bkyml import __version__

__author__ = "Joscha Feth"
__copyright__ = "Joscha Feth"
__license__ = "mit"

LOGGER = logging.getLogger(__name__)


class MyYAML(RuamelYaml):
    def to_string(self, data):
        stream = StringIO()
        RuamelYaml.dump(self, data, stream)
        return stream.getvalue()


YAML = MyYAML()
YAML.default_flow_style = False

RETRY_MANUAL_ALLOWED_DEFAULT = True
RETRY_MANUAL_PERMIT_ON_PASSED_DEFAULT = False


def plugin_or_key_value_pair(value):
    if '=' in value:
        return value.split('=', 1)
    return value


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(
            "%s is an invalid positive int value" % value
        )
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
    ret = CommentedMap()
    for tpl in tuples:
        ret[tpl[0]] = tpl[1]
    return ret


def singlify(a_list):
    if len(a_list) == 1:
        return a_list[0]
    return a_list


def plugins_section(step, namespace):
    if ns_hasattr(namespace, 'plugin') and namespace.plugin:
        plugins = CommentedMap()

        for plugin in namespace.plugin:
            name, tuples = plugin[0], plugin[1:]
            plugins[name] = None
            if tuples:
                plugins[name] = tuples_to_dict(tuples)
        return plugins
    return None


class Block:

    @staticmethod
    def install(action):
        parser = action.add_parser('block')
        parser.add_argument(
            dest="label",
            help="Label of the block step. Supports emoji.",
            type=str,
            metavar="LABEL")
        parser.add_argument(
            '--prompt',
            help="The instructional message displayed in the dialog box when the unblock step is activated.", # NOQA
            type=str,
            metavar="PROMPT")
        parser.add_argument(
            '--branches',
            help="The branch pattern defining which branches will include this step in their builds.", # NOQA
            type=str,
            nargs='+',
            metavar="BRANCH_PATTERN"
        )
        parser.add_argument(
            '--field-text',
            help="A text field. \
                KEY is the meta-data key that stores the field's input. \
                LABEL is the label of the field. \
                HINT is the explanatory text that is shown after the label.\
                REQUIRED (true/false) A boolean value that defines whether the field is required for form submission. \
                DEFAULT is value that is pre-filled in the text field. \
                ", # NOQA
            type=str,
            nargs=5,
            action='append',
            metavar=('KEY', 'LABEL', 'HINT', 'REQUIRED', 'DEFAULT')
        )
        parser.add_argument(
            '--field-select',
            help="A select field. \
                KEY is the meta-data key that stores the field's input. \
                LABEL is the label of the field. \
                HINT is the explanatory text that is shown after the label.\
                REQUIRED (true/false) A boolean value that defines whether the field is required for form submission. \
                DEFAULT is value that is pre-selected. \
                KEY_VALUE_PAIRS is value that is pre-selected. \
                ", # NOQA
            type=str,
            nargs='+',  # TODO: This will produce an incorrect help entry
            action='append',
            metavar='KEY LABEL HINT REQUIRED DEFAULT KEY_VALUE_PAIRS [KEY_VALUE_PAIRS ...]'
        )
        parser.set_defaults(func=Block.block)

    @staticmethod
    def block(namespace):
        assert ns_hasattr(namespace, 'label')
        step = CommentedMap({
            'block': namespace.label
        })

        # prompt
        if ns_hasattr(namespace, 'prompt'):
            step['prompt'] = namespace.prompt

        # branches
        if ns_hasattr(namespace, 'branches'):
            step['branches'] = ' '.join(namespace.branches)

        # Fields
        has_text_fields = ns_hasattr(namespace, 'field_text')
        has_select_fields = ns_hasattr(namespace, 'field_select')

        if has_select_fields or has_text_fields:
            fields = step['fields'] = []
            if has_text_fields:
                for text_field in namespace.field_text:
                    [key, label, hint, required, default] = text_field
                    field = Block.gen_field('text', key, label, hint, required, default)
                    fields.append(field)
            if has_select_fields:
                for select_field in namespace.field_select:
                    if len(select_field) < 6:
                        raise argparse.ArgumentTypeError("Missing required parameters")
                    key, label, hint, required, default = select_field[0], \
                        select_field[1], \
                        select_field[2], \
                        select_field[3], \
                        select_field[4]
                    pairs = select_field[5:]
                    field = Block.gen_field('select', key, label, hint, required, default)

                    options = field['options'] = []
                    for pair in pairs:
                        [value, label] = pair.split('=', 1)
                        p = CommentedMap()
                        p['label'] = label
                        p['value'] = value
                        options.append(p)
                    fields.append(field)

        YAML.indent(sequence=4, offset=2)
        return YAML.to_string([step])

    @staticmethod
    def gen_field(type, key, label, hint, required, default):
        if key is None or key.strip() == '':
            raise argparse.ArgumentTypeError("'%s' is an invalid key" % key)
        if label is None or label.strip() == '':
            raise argparse.ArgumentTypeError("'%s' is an invalid label" % label)
        field = CommentedMap()
        field[type] = label
        field['key'] = key

        if hint:
            field['hint'] = hint
        if required.lower() == 'true':
            field['required'] = True
        if default:
            field['default'] = default
        return field


class Trigger:

    @staticmethod
    def install(action):
        parser = action.add_parser('trigger')
        parser.add_argument(
            dest="pipeline",
            help="Name of the pipeline to trigger",
            type=str,
            metavar="PIPELINE")
        parser.add_argument(
            '--label',
            dest="label",
            help="The label that will be displayed in the pipeline visualisation in Buildkite. Supports emoji.", # NOQA
            type=str,
            metavar="LABEL")
        parser.add_argument(
            '--async',
            dest="is_async",
            action='store_true',
            help="If given, the step will immediately continue, regardless of the success of the triggered build.", # NOQA
        )
        parser.add_argument(
            '--branches',
            help="The branch pattern defining which branches will include this step in their builds.", # NOQA
            type=str,
            nargs='+',
            metavar="BRANCH_PATTERN"
        )
        parser.add_argument(
            '--build-message',
            help="The message for the build. Supports emoji.",
            type=str,
            metavar="MESSAGE")
        parser.add_argument(
            '--build-commit',
            help="The commit hash for the build",
            type=str,
            metavar="SHA")
        parser.add_argument(
            '--build-branch',
            help="The branch for the build",
            type=str,
            metavar="BRANCH")
        parser.add_argument(
            '--build-env',
            help="A map of environment variables for the triggered build.",
            type=str,
            nargs=2,
            action='append',
            metavar=('KEY', 'VALUE')
        )
        parser.add_argument(
            '--build-meta-data',
            help="A map of meta-data for the triggered build.",
            type=str,
            nargs=2,
            action='append',
            metavar=('KEY', 'VALUE')
        )
        parser.set_defaults(func=Trigger.trigger)

    @staticmethod
    def trigger(namespace):
        assert ns_hasattr(namespace, 'pipeline')
        step = CommentedMap({
            'trigger': namespace.pipeline
        })

        # label
        if ns_hasattr(namespace, 'label'):
            step['label'] = namespace.label

        # async
        if ns_hasattr(namespace, 'is_async') and namespace.is_async:
            step['async'] = True

        # branches
        if ns_hasattr(namespace, 'branches'):
            step['branches'] = ' '.join(namespace.branches)

        # build vars
        has_build_branch = ns_hasattr(namespace, 'build_branch')
        has_build_commit = ns_hasattr(namespace, 'build_commit')
        has_build_message = ns_hasattr(namespace, 'build_message')
        has_build_env = ns_hasattr(namespace, 'build_env')
        has_build_meta_data = ns_hasattr(namespace, 'build_meta_data')
        if has_build_branch \
           or has_build_commit \
           or has_build_message \
           or has_build_env \
           or has_build_meta_data:
            build = step['build'] = CommentedMap()

            if has_build_branch:
                build['branch'] = namespace.build_branch
            if has_build_commit:
                build['commit'] = namespace.build_commit
            if has_build_message:
                build['message'] = namespace.build_message
            if has_build_env:
                build['env'] = tuples_to_dict(namespace.build_env)
            if has_build_meta_data:
                build['meta_data'] = tuples_to_dict(namespace.build_meta_data)

        YAML.indent(sequence=4, offset=2)
        return YAML.to_string([step])


class Plugin:

    @staticmethod
    def install(action):
        parser = action.add_parser('plugin')
        parser.add_argument(
            '--name',
            dest="name",
            help="Name of the plugin step",
            type=str,
            metavar="NAME")
        parser.add_argument(
            '--plugin',
            help="A plugin to run. Optionally key/value pairs for the plugin.",
            dest="plugin",
            nargs='+',
            action='append',
            type=plugin_or_key_value_pair,
            metavar=('PLUGIN', 'KEY_VALUE_PAIR'),
            required=True
        )
        parser.set_defaults(func=Plugin.plugin)

    @staticmethod
    def plugin(namespace):
        step = CommentedMap()

        if ns_hasattr(namespace, 'name') and namespace.name:
            step['name'] = namespace.name

        plugins = plugins_section(step, namespace)
        if plugins:
            step['plugins'] = plugins
        else:
            return ''

        YAML.indent(sequence=4, offset=2)
        return YAML.to_string([step])


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
        assert ns_hasattr(namespace, 'str')
        lines = "\n# ".join(["\n# ".join(line.splitlines()) for line in namespace.str])
        return "# {lines}".format(lines=lines)


class Steps:

    @staticmethod
    def install(action):
        parser = action.add_parser('steps')
        parser.set_defaults(func=Steps.steps)

    @staticmethod
    # pylint: disable=unused-argument
    def steps(namespace):
        return YAML.to_string({'steps': None})


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
        return YAML.to_string({
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
            help="The label that will be displayed in the pipeline visualisation in Buildkite. Supports emoji.", # NOQA
            type=str,
            metavar="LABEL")
        parser.add_argument(
            '--branches',
            help="The branch pattern defining which branches will include this step in their builds.", # NOQA
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
            help="The maximum number of jobs created from this step that are allowed to run at the same time. Requires --concurrency-group.", # NOQA
            type=check_positive,
            metavar="POSITIVE_INT"
        )
        parser.add_argument(
            '--concurrency-group',
            help="A unique name for the concurrency group that you are creating with the concurrency attribute.", # NOQA
            type=str,
            metavar="GROUP_NAME"
        )
        parser.add_argument(
            '--timeout-in-minutes',
            help="The number of minutes a job created from this step is allowed to run. If the job does not finish within this limit, it will be automatically cancelled and the build will fail.", # NOQA
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
            help="The number of times this job can be retried. The maximum value this can be set to is 10.", # NOQA
            type=check_positive,
            metavar="POSITIVE_INT"
        )
        parser.add_argument(
            '--retry-automatic-tuple',
            help="The exit status number that will cause this job to retry and a limit to go with it.", # NOQA
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
        parser.set_defaults(retry_manual_allowed=RETRY_MANUAL_ALLOWED_DEFAULT)
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
        parser.set_defaults(retry_manual_permit_on_passed=RETRY_MANUAL_PERMIT_ON_PASSED_DEFAULT)

        parser.add_argument(
            '--plugin',
            help="A plugin to run with this step. Optionally key/value pairs for the plugin.",
            dest="plugin",
            nargs='+',
            action='append',
            type=plugin_or_key_value_pair,
            metavar=('PLUGIN', 'KEY_VALUE_PAIR')
        )

        parser.set_defaults(func=Command.command)

    @staticmethod
    def assert_post_parse(parsed, parser):
        if ns_hasattr(parsed, 'concurrency') and not ns_hasattr(parsed, 'concurrency_group'):
            parser.error("--concurrency requires --concurrency-group.")

        if not ns_hasattr(parsed, 'retry') or parsed.retry != 'automatic':
            if ns_hasattr(parsed, 'retry_automatic_exit_status'):
                parser.error('--retry-automatic-exit-status requires --retry automatic.')

            if ns_hasattr(parsed, 'retry_automatic_limit'):
                parser.error('--retry-automatic-limit requires --retry automatic.')

            if ns_hasattr(parsed, 'retry_automatic_tuple'):
                parser.error('--retry-automatic-tuple requires --retry automatic.')

        if ns_hasattr(parsed, 'retry_automatic_tuple') and \
           ns_hasattr(parsed, 'retry_automatic_exit_status'):
                parser.error('--retry-automatic-tuple can not be combined with --retry-automatic-exit-status.') # NOQA

        if ns_hasattr(parsed, 'retry_automatic_tuple') and \
           ns_hasattr(parsed, 'retry_automatic_limit'):
                parser.error('--retry-automatic-tuple can not be combined with --retry-automatic-limit.') # NOQA

        if not ns_hasattr(parsed, 'retry') or parsed.retry != 'manual':
            if ns_hasattr(parsed, 'retry_manual_allowed') \
               and parsed.retry_manual_allowed is not RETRY_MANUAL_ALLOWED_DEFAULT:
                parser.error('--[no-]retry-manual-allowed requires --retry manual.')

            if ns_hasattr(parsed, 'retry_manual_permit_on_passed') \
               and parsed.retry_manual_permit_on_passed \
               is not RETRY_MANUAL_PERMIT_ON_PASSED_DEFAULT:
                parser.error('--[no-]retry-manual-permit-on-passed requires --retry manual.')

            if ns_hasattr(parsed, 'retry_manual_reason'):
                parser.error('--retry-manual-reason requires --retry manual.')

    @staticmethod
    def command(namespace):
        step = CommentedMap()

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
        if ns_hasattr(namespace, 'skip') \
           and (namespace.skip is True or isinstance(namespace.skip, str)):
            step['skip'] = namespace.skip

        # retry
        if ns_hasattr(namespace, 'retry'):
            retry = CommentedMap()
            retry[namespace.retry] = CommentedMap()

            if namespace.retry == 'automatic':
                if ns_hasattr(namespace, 'retry_automatic_exit_status'):
                    retry[namespace.retry]['exit_status'] = namespace.retry_automatic_exit_status
                if ns_hasattr(namespace, 'retry_automatic_limit'):
                    retry[namespace.retry]['limit'] = min(10, namespace.retry_automatic_limit)
                if ns_hasattr(namespace, 'retry_automatic_tuple'):
                    if namespace.retry_automatic_tuple:
                        retry[namespace.retry] = []
                        for tpl in namespace.retry_automatic_tuple:
                            t = CommentedMap()
                            t['exit_status'] = int_or_star(tpl[0])
                            t['limit'] = min(10, check_positive(tpl[1]))
                            retry[namespace.retry].append(t)
            elif namespace.retry == 'manual':
                if ns_hasattr(namespace, 'retry_manual_allowed') \
                   and not namespace.retry_manual_allowed:
                    retry[namespace.retry]['allowed'] = namespace.retry_manual_allowed
                if ns_hasattr(namespace, 'retry_manual_reason'):
                    retry[namespace.retry]['reason'] = namespace.retry_manual_reason
                if ns_hasattr(namespace, 'retry_manual_permit_on_passed') \
                   and namespace.retry_manual_permit_on_passed:
                    retry[namespace.retry]['permit_on_passed'] = namespace.retry_manual_permit_on_passed # NOQA
            else:
                raise argparse.ArgumentTypeError("%s is an invalid retry value" % namespace.retry)

            if not retry[namespace.retry]:
                retry[namespace.retry] = True

            step['retry'] = retry

        # plugins
        plugins = plugins_section(step, namespace)
        if plugins:
            step['plugins'] = plugins

        YAML.indent(sequence=4, offset=2)
        return YAML.to_string([step])


class Wait:

    @staticmethod
    def install(action):
        parser = action.add_parser('wait')
        parser.add_argument(
            '--continue-on-failure',
            action='store_true',
            help="Continue even if previous steps failed",
        )
        parser.set_defaults(func=Wait.wait)

    @staticmethod
    def wait(namespace):
        step = 'wait'

        if ns_hasattr(namespace, 'continue_on_failure') and namespace.continue_on_failure:
            step = CommentedMap()
            step['wait'] = None
            step['continue_on_failure'] = True

        YAML.indent(sequence=4, offset=2)
        return YAML.to_string([step])


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
    Plugin.install(subparsers)
    Wait.install(subparsers)
    Trigger.install(subparsers)
    Block.install(subparsers)

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

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

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
    return args.func(args)


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    LOGGER.debug("Calling function")
    print(parse_main(args))
    LOGGER.info("Script ends here")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
