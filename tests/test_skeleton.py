#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=unused-variable
# pylint: disable=missing-docstring

import argparse
import sys
from unittest.mock import patch
import pytest
from bkyml.skeleton import Comment, \
                           Steps, \
                           Env, \
                           Command, \
                           Plugin, \
                           parse_main, \
                           run, \
                           check_positive, \
                           bool_or_string, \
                           plugin_or_key_value_pair

__author__ = "Joscha Feth"
__copyright__ = "Joscha Feth"
__license__ = "mit"


def describe_bkyaml():

    @pytest.fixture
    def run_run(capsys, snapshot, argv):
        with patch.object(sys, 'argv', [''] + argv):
            run()
        captured = capsys.readouterr()
        snapshot.assert_match(captured.out)

    @pytest.fixture
    def args():
        return argparse.Namespace()

    def describe_plugin_or_key_value_pair():
        def test_plugin_or_key_value_pair_plugin():
            assert plugin_or_key_value_pair('org/repo#1.0.0') == 'org/repo#1.0.0'

        def test_plugin_or_key_value_pair_pair():
            assert plugin_or_key_value_pair('a=b=c') == ['a', 'b=c']

    def describe_check_positive():
        def test_check_positive_1():
            assert check_positive(1)

        def test_check_positive_minus_1():
            with pytest.raises(argparse.ArgumentTypeError) as err:
                check_positive(-1)
            assert '-1 is an invalid positive int value' in str(err.value)

    def describe_bool_or_string():
        def test_bool_or_string_true():
            assert bool_or_string('TRUE')

        def test_bool_or_string_false():
            assert bool_or_string('FALSE') is False

        def test_bool_or_string():
            assert bool_or_string('bla') == 'bla'

    def describe_comment():
        def test_comment(args, snapshot):
            args.str = ['a', 'b']
            snapshot.assert_match(Comment.comment(args))

    def describe_steps():
        def test_steps(args, snapshot):
            snapshot.assert_match(Steps.steps(args))

    def describe_env():
        def test_env_all(args, snapshot):
            args.var = [['a', 'b'], ['c', 'd']]
            snapshot.assert_match(Env.env(args))

    def describe_command():
        @pytest.fixture
        def generic_command_call(args, snapshot):
            args.command = [['cmd']]
            snapshot.assert_match(Command.command(args))

        @pytest.fixture
        def assert_command_call_error(capsys, command_args, message):
            with pytest.raises(SystemExit) as sys_exit:
                parse_main(['command', '--command', 'cmd'] + command_args)
            assert '2' in str(sys_exit.value)
            captured = capsys.readouterr()
            assert message in captured.err

        def test_command_1(args, snapshot):
            args.command = [["my-command arg1 'arg 2'"]]
            snapshot.assert_match(Command.command(args))

        def test_command_n(args, snapshot):
            args.command = [['a', 'b'], ['c', 'd']]
            snapshot.assert_match(Command.command(args))

        def test_label(args, snapshot):
            args.label = 'My label'
            generic_command_call(args, snapshot)

        def test_branches(args, snapshot):
            args.branches = ['master', 'release-*']
            generic_command_call(args, snapshot)

        def test_env(args, snapshot):
            args.env = [['a', 'b'], ['c', 'd']]
            generic_command_call(args, snapshot)

        def test_agents(args, snapshot):
            args.agents = [['npm', 'true'], ['mvn', 'true']]
            generic_command_call(args, snapshot)

        def test_artifact_paths_0(args, snapshot):
            args.artifact_paths = []
            generic_command_call(args, snapshot)

        def test_artifact_paths_1(args, snapshot):
            args.artifact_paths = [["logs/**/*;coverage/**/*"]]
            generic_command_call(args, snapshot)

        def test_artifact_paths_n(args, snapshot):
            args.artifact_paths = [["logs/**/*", "coverage/**/*"]]
            generic_command_call(args, snapshot)

        def test_parallelism(args, snapshot):
            args.parallelism = 4
            generic_command_call(args, snapshot)

        def test_parallelism_1(args, snapshot):
            args.parallelism = 1
            generic_command_call(args, snapshot)

        def test_concurrency(args, snapshot):
            args.concurrency = 2
            args.concurrency_group = 'my/group'
            generic_command_call(args, snapshot)

        def test_concurrency_cli(capsys):
            assert_command_call_error(
                capsys,
                ['--concurrency', '1'],
                '--concurrency requires --concurrency-group'
            )

        def test_timeout_in_minutes_minus(args, snapshot):
            args.timeout_in_minutes = -1
            generic_command_call(args, snapshot)

        def test_timeout_in_minutes_0(args, snapshot):
            args.timeout_in_minutes = 0
            generic_command_call(args, snapshot)

        def test_timeout_in_minutes_1(args, snapshot):
            args.timeout_in_minutes = 1
            generic_command_call(args, snapshot)

        def test_skip_bool_true(args, snapshot):
            args.skip = True
            generic_command_call(args, snapshot)

        def test_skip_bool_false(args, snapshot):
            args.skip = False
            generic_command_call(args, snapshot)

        def test_skip_string(args, snapshot):
            args.skip = 'Some reason'
            generic_command_call(args, snapshot)

        def describe_retry():
            def test_retry_unknown(args, snapshot):
                args.retry = 'unknown'
                with pytest.raises(argparse.ArgumentTypeError) as err:
                    generic_command_call(args, snapshot)
                assert 'unknown is an invalid retry value' in str(err.value)

            def describe_manual():
                def test_retry_manual(args, snapshot):
                    args.retry = 'manual'
                    generic_command_call(args, snapshot)

                def test_retry_manual_allowed(args, snapshot):
                    args.retry = 'manual'
                    args.retry_manual_allowed = True
                    generic_command_call(args, snapshot)
                    args.retry_manual_allowed = False
                    generic_command_call(args, snapshot)

                def test_retry_reason(args, snapshot):
                    args.retry = 'manual'
                    args.retry_manual_reason = 'Some reason why'
                    generic_command_call(args, snapshot)

                # pylint: disable=invalid-name
                def test_retry_manual_permit_on_passed(args, snapshot):
                    args.retry = 'manual'
                    args.retry_manual_permit_on_passed = True
                    generic_command_call(args, snapshot)
                    args.retry_manual_permit_on_passed = False
                    generic_command_call(args, snapshot)

                def test_retry_manual_missing_allowed_missing_retry(capsys):
                    assert_command_call_error(
                        capsys,
                        ['--no-retry-manual-allowed'],
                        '--[no-]retry-manual-allowed requires --retry manual'
                    )

                def test_retry_manual_reason_missing_retry(capsys):
                    assert_command_call_error(
                        capsys,
                        ['--retry-manual-reason', 'My reason'],
                        '--retry-manual-reason requires --retry manual'
                    )

                # pylint: disable=invalid-name
                def test_retry_manual_pop_missing_retry(capsys):
                    assert_command_call_error(
                        capsys,
                        ['--retry-manual-permit-on-passed'],
                        '--[no-]retry-manual-permit-on-passed'
                        + ' requires --retry manual'
                    )

                # pylint: disable=invalid-name
                def test_retry_manual_pop_manual_retry(capsys, snapshot):
                    run_run(
                        capsys,
                        snapshot,
                        ['command',
                         '--command', 'cmd',
                         '--retry', 'manual',
                         '--retry-manual-permit-on-passed']
                    )

            def describe_automatic():
                def test_retry_automatic(args, snapshot):
                    args.retry = 'automatic'
                    generic_command_call(args, snapshot)

                def test_retry_automatic_limit(args, snapshot):
                    args.retry = 'automatic'
                    args.retry_automatic_limit = 2
                    generic_command_call(args, snapshot)

                def test_retry_automatic_limit_11(args, snapshot):
                    args.retry = 'automatic'
                    args.retry_automatic_limit = 11
                    generic_command_call(args, snapshot)

                def test_retry_automatic_exit_status_star(args, snapshot):
                    args.retry = 'automatic'
                    args.retry_automatic_exit_status = '*'
                    generic_command_call(args, snapshot)

                def test_retry_automatic_exit_status_number(args, snapshot):
                    args.retry = 'automatic'
                    args.retry_automatic_exit_status = 1
                    generic_command_call(args, snapshot)

                def test_retry_automatic_exit_status_and_limit(args, snapshot):
                    args.retry = 'automatic'
                    args.retry_automatic_limit = 2
                    args.retry_automatic_exit_status = 1
                    generic_command_call(args, snapshot)

                def test_retry_automatic_tuple_0(args, snapshot):
                    args.retry = 'automatic'
                    args.retry_automatic_tuple = []
                    generic_command_call(args, snapshot)

                def test_retry_automatic_tuple_n(args, snapshot):
                    args.retry = 'automatic'
                    args.retry_automatic_tuple = [['*', 2], [1, 3]]
                    generic_command_call(args, snapshot)

                def test_exit_status_string(capsys):
                    assert_command_call_error(
                        capsys,
                        ['--retry', 'automatic',
                         '--retry-automatic-exit-status', 'xxx'],
                        'xxx is an invalid value'
                    )

                def test_retry_exit_status_missing_retry(capsys):
                    assert_command_call_error(
                        capsys,
                        ['--retry-automatic-exit-status', '*'],
                        '--retry-automatic-exit-status'
                        + ' requires --retry automatic'
                    )

                def test_retry_limit_missing_retry(capsys):
                    assert_command_call_error(
                        capsys,
                        ['--retry-automatic-limit', '2'],
                        '--retry-automatic-limit requires --retry automatic'
                    )

                def test_retry_tuple_missing_retry(capsys):
                    assert_command_call_error(
                        capsys,
                        ['--retry-automatic-tuple', '*', '2'],
                        '--retry-automatic-tuple requires --retry automatic'
                    )

                def test_retry_tuple_missing_combine_exit_status(capsys):
                    assert_command_call_error(
                        capsys,
                        ['--retry', 'automatic',
                         '--retry-automatic-tuple', '*', '2',
                         '--retry-automatic-exit-status', '*'],
                        '--retry-automatic-tuple can not be combined with'
                        + ' --retry-automatic-exit-status'
                    )

                def test_retry_tuple_missing_combine_limit(capsys):
                    assert_command_call_error(
                        capsys,
                        ['--retry', 'automatic',
                         '--retry-automatic-tuple', '*', '2',
                         '--retry-automatic-limit', '2'],
                        '--retry-automatic-tuple'
                        + ' can not be combined with '
                        + '--retry-automatic-limit'
                    )

        def describe_command_plugin_attr():

            def test_command_plugin_none(args, snapshot):
                args.plugin = []
                generic_command_call(args, snapshot)

            def test_command_plugin_no_args(args, snapshot):
                args.plugin = [['org/repo#1.0.0']]
                generic_command_call(args, snapshot)

            def test_command_plugin_1(args, snapshot):
                args.plugin = [
                    ['org/repo#1.0.0', ['a', 'b'], ['c', 'd']]
                ]
                generic_command_call(args, snapshot)

            def test_command_plugin_n(args, snapshot):
                args.plugin = [
                    ['org/repo#1.0.0', ['a', 'b'], ['c', 'd']],
                    ['other_org/other_repo', ['e', 'f'], ['g', 'h=i']],
                ]
                generic_command_call(args, snapshot)

    def describe_plugin():

        @pytest.fixture
        def generic_plugin_call(args, snapshot):
            args.command = [['plugin']]
            snapshot.assert_match(Plugin.plugin(args))

        def describe_plugin_name_attr():

            def test_plugin_name_attr(args, snapshot):
                args.plugin = [['org/repo#1.0.0']]
                args.name = 'My plugin run'
                generic_plugin_call(args, snapshot)

        def describe_plugin_plugin_attr():

            def test_plugin_plugin_none(args, snapshot):
                args.plugin = []
                generic_plugin_call(args, snapshot)

            def test_plugin_plugin_no_args(args, snapshot):
                args.plugin = [['org/repo#1.0.0']]
                generic_plugin_call(args, snapshot)

            def test_plugin_plugin_1(args, snapshot):
                args.plugin = [
                    ['org/repo#1.0.0', ['a', 'b'], ['c', 'd']]
                ]
                generic_plugin_call(args, snapshot)

            def test_plugin_plugin_n(args, snapshot):
                args.plugin = [
                    ['org/repo#1.0.0', ['a', 'b'], ['c', 'd']],
                    ['other_org/other_repo', ['e', 'f'], ['g', 'h=i']],
                ]
                generic_plugin_call(args, snapshot)

    def describe_parse_main():
        def test_main(snapshot):
            snapshot.assert_match(parse_main(['command', '--command', 'x']))

    def describe_cli():
        def test_command(snapshot, capsys):
            run_run(capsys, snapshot, ['command', '--command', 'x'])

        def test_empty_command(snapshot, capsys):
            run_run(capsys, snapshot, [])

        def test_help(snapshot, capsys):
            for subcommand in ['comment', 'steps', 'env', 'command', 'plugin']:
                with pytest.raises(SystemExit):
                    with patch.object(sys, 'argv', ['', subcommand, '--help']):
                        run()
                captured = capsys.readouterr()
                snapshot.assert_match(captured.out)
