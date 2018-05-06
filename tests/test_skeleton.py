#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=unused-variable
# pylint: disable=missing-docstring

import argparse
import sys
from unittest.mock import patch
import pytest
from bkyml.skeleton import  Comment, \
                            Steps, \
                            Env, \
                            Command, \
                            parse_main, \
                            run, \
                            check_positive, \
                            bool_or_string

__author__ = "Joscha Feth"
__copyright__ = "Joscha Feth"
__license__ = "mit"

def describe_bkyaml():
    @pytest.fixture
    def run_run(capsys, snapshot, args):
        with patch.object(sys, 'argv', [''] + args):
            run()
        captured = capsys.readouterr()
        snapshot.assert_match(captured.out)

    @pytest.fixture
    def namespace():
        return argparse.Namespace()

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
        def test_comment(namespace, snapshot):
            namespace.str = ['a', 'b']
            snapshot.assert_match(Comment.comment(namespace))

    def describe_steps():
        def test_steps(namespace, snapshot):
            snapshot.assert_match(Steps.steps(namespace))

    def describe_env():
        def test_env_all(namespace, snapshot):
            namespace.var = [['a', 'b'], ['c', 'd']]
            snapshot.assert_match(Env.env(namespace))

    def describe_command():
        @pytest.fixture
        def generic_command_call(namespace, snapshot):
            namespace.command = [['cmd']]
            snapshot.assert_match(Command.command(namespace))

        @pytest.fixture
        def assert_command_call_error(capsys, command_args, message):
            with pytest.raises(SystemExit) as sys_exit:
                parse_main(['command', '--command', 'cmd'] + command_args)
            assert '2' in str(sys_exit.value)
            captured = capsys.readouterr()
            assert message in captured.err

        def test_command_1(namespace, snapshot):
            namespace.command = [["my-command arg1 'arg 2'"]]
            snapshot.assert_match(Command.command(namespace))

        def test_command_n(namespace, snapshot):
            namespace.command = [['a', 'b'], ['c', 'd']]
            snapshot.assert_match(Command.command(namespace))

        def test_label(namespace, snapshot):
            namespace.label = 'My label'
            generic_command_call(namespace, snapshot)

        def test_branches(namespace, snapshot):
            namespace.branches = ['master', 'release-*']
            generic_command_call(namespace, snapshot)

        def test_env(namespace, snapshot):
            namespace.env = [['a', 'b'], ['c', 'd']]
            generic_command_call(namespace, snapshot)

        def test_agents(namespace, snapshot):
            namespace.agents = [['npm', 'true'], ['mvn', 'true']]
            generic_command_call(namespace, snapshot)

        def test_artifact_paths_0(namespace, snapshot):
            namespace.artifact_paths = []
            generic_command_call(namespace, snapshot)

        def test_artifact_paths_1(namespace, snapshot):
            namespace.artifact_paths = [["logs/**/*;coverage/**/*"]]
            generic_command_call(namespace, snapshot)

        def test_artifact_paths_n(namespace, snapshot):
            namespace.artifact_paths = [["logs/**/*", "coverage/**/*"]]
            generic_command_call(namespace, snapshot)

        def test_parallelism(namespace, snapshot):
            namespace.parallelism = 4
            generic_command_call(namespace, snapshot)

        def test_parallelism_1(namespace, snapshot):
            namespace.parallelism = 1
            generic_command_call(namespace, snapshot)

        def test_concurrency(namespace, snapshot):
            namespace.concurrency = 2
            namespace.concurrency_group = 'my/group'
            generic_command_call(namespace, snapshot)

        def test_concurrency_cli(capsys):
            assert_command_call_error(
                capsys,
                ['--concurrency', '1'],
                '--concurrency requires --concurrency-group'
            )

        def test_timeout_in_minutes_minus(namespace, snapshot):
            namespace.timeout_in_minutes = -1
            generic_command_call(namespace, snapshot)

        def test_timeout_in_minutes_0(namespace, snapshot):
            namespace.timeout_in_minutes = 0
            generic_command_call(namespace, snapshot)

        def test_timeout_in_minutes_1(namespace, snapshot):
            namespace.timeout_in_minutes = 1
            generic_command_call(namespace, snapshot)

        def test_skip_bool_true(namespace, snapshot):
            namespace.skip = True
            generic_command_call(namespace, snapshot)

        def test_skip_bool_false(namespace, snapshot):
            namespace.skip = False
            generic_command_call(namespace, snapshot)

        def test_skip_string(namespace, snapshot):
            namespace.skip = 'Some reason'
            generic_command_call(namespace, snapshot)

        def describe_retry():
            def test_retry_unknown(namespace, snapshot):
                namespace.retry = 'unknown'
                with pytest.raises(argparse.ArgumentTypeError) as err:
                    generic_command_call(namespace, snapshot)
                assert 'unknown is an invalid retry value' in str(err.value)

            def describe_manual():
                def test_retry_manual(namespace, snapshot):
                    namespace.retry = 'manual'
                    generic_command_call(namespace, snapshot)

                def test_retry_manual_allowed(namespace, snapshot):
                    namespace.retry = 'manual'
                    namespace.retry_manual_allowed = True
                    generic_command_call(namespace, snapshot)
                    namespace.retry_manual_allowed = False
                    generic_command_call(namespace, snapshot)

                def test_retry_reason(namespace, snapshot):
                    namespace.retry = 'manual'
                    namespace.retry_manual_reason = 'Some reason why'
                    generic_command_call(namespace, snapshot)

                # pylint: disable=invalid-name
                def test_retry_manual_permit_on_passed(namespace, snapshot):
                    namespace.retry = 'manual'
                    namespace.retry_manual_permit_on_passed = True
                    generic_command_call(namespace, snapshot)
                    namespace.retry_manual_permit_on_passed = False
                    generic_command_call(namespace, snapshot)

                def test_retry_manual_cli_missing_allowed_missing_retry(capsys):
                    assert_command_call_error(
                        capsys,
                        ['--no-retry-manual-allowed'],
                        '--[no-]retry-manual-allowed requires --retry manual'
                    )

                def test_retry_manual_cli_reason_missing_retry(capsys):
                    assert_command_call_error(
                        capsys,
                        ['--retry-manual-reason', 'My reason'],
                        '--retry-manual-reason requires --retry manual'
                    )

                # pylint: disable=invalid-name
                def test_retry_manual_cli_permit_on_passed_missing_retry(capsys):
                    assert_command_call_error(
                        capsys,
                        ['--retry-manual-permit-on-passed'],
                        '--[no-]retry-manual-permit-on-passed requires --retry manual'
                    )

                # pylint: disable=invalid-name
                def test_retry_manual_cli_permit_on_passed_manual_retry(capsys, snapshot):
                    run_run(
                        capsys,
                        snapshot,
                        ['command',
                         '--command', 'cmd',
                         '--retry', 'manual',
                         '--retry-manual-permit-on-passed']
                    )

            def describe_automatic():
                def test_retry_automatic(namespace, snapshot):
                    namespace.retry = 'automatic'
                    generic_command_call(namespace, snapshot)

                def test_retry_automatic_limit(namespace, snapshot):
                    namespace.retry = 'automatic'
                    namespace.retry_automatic_limit = 2
                    generic_command_call(namespace, snapshot)

                def test_retry_automatic_limit_11(namespace, snapshot):
                    namespace.retry = 'automatic'
                    namespace.retry_automatic_limit = 11
                    generic_command_call(namespace, snapshot)

                def test_retry_automatic_exit_status_star(namespace, snapshot):
                    namespace.retry = 'automatic'
                    namespace.retry_automatic_exit_status = '*'
                    generic_command_call(namespace, snapshot)

                def test_retry_automatic_exit_status_number(namespace, snapshot):
                    namespace.retry = 'automatic'
                    namespace.retry_automatic_exit_status = 1
                    generic_command_call(namespace, snapshot)

                def test_retry_automatic_exit_status_and_limit(namespace, snapshot):
                    namespace.retry = 'automatic'
                    namespace.retry_automatic_limit = 2
                    namespace.retry_automatic_exit_status = 1
                    generic_command_call(namespace, snapshot)

                def test_retry_automatic_tuple_0(namespace, snapshot):
                    namespace.retry = 'automatic'
                    namespace.retry_automatic_tuple = []
                    generic_command_call(namespace, snapshot)

                def test_retry_automatic_tuple_n(namespace, snapshot):
                    namespace.retry = 'automatic'
                    namespace.retry_automatic_tuple = [['*', 2], [1, 3]]
                    generic_command_call(namespace, snapshot)

                def test_retry_automatic_cli_exit_status_string(capsys):
                    assert_command_call_error(
                        capsys,
                        ['--retry', 'automatic', '--retry-automatic-exit-status', 'xxx'],
                        'xxx is an invalid value'
                    )

                def test_retry_automatic_cli_exit_status_missing_retry(capsys):
                    assert_command_call_error(
                        capsys,
                        ['--retry-automatic-exit-status', '*'],
                        '--retry-automatic-exit-status requires --retry automatic'
                    )

                def test_retry_automatic_cli_limit_missing_retry(capsys):
                    assert_command_call_error(
                        capsys,
                        ['--retry-automatic-limit', '2'],
                        '--retry-automatic-limit requires --retry automatic'
                    )

                def test_retry_automatic_cli_tuple_missing_retry(capsys):
                    assert_command_call_error(
                        capsys,
                        ['--retry-automatic-tuple', '*', '2'],
                        '--retry-automatic-tuple requires --retry automatic'
                    )

                def test_retry_automatic_cli_tuple_missing_combine_exit_status(capsys):
                    assert_command_call_error(
                        capsys,
                        ['--retry', 'automatic',
                         '--retry-automatic-tuple', '*', '2',
                         '--retry-automatic-exit-status', '*'],
                        '--retry-automatic-tuple can not be combined with'
                        + ' --retry-automatic-exit-status'
                    )

                def test_retry_automatic_cli_tuple_missing_combine_limit(capsys):
                    assert_command_call_error(
                        capsys,
                        ['--retry', 'automatic',
                         '--retry-automatic-tuple', '*', '2',
                         '--retry-automatic-limit', '2'],
                        '--retry-automatic-tuple can not be combined with --retry-automatic-limit'
                    )

    def describe_parse_main():
        def test_main(snapshot):
            snapshot.assert_match(parse_main(['command', '--command', 'x']))

    def describe_cli():
        def test_command(snapshot, capsys):
            run_run(capsys, snapshot, ['command', '--command', 'x'])

        def test_empty_command(snapshot, capsys):
            run_run(capsys, snapshot, [])

        def test_help(snapshot, capsys):
            for subcommand in ['comment', 'steps', 'env', 'command']:
                with pytest.raises(SystemExit):
                    with patch.object(sys, 'argv', ['', subcommand, '--help']):
                        run()
                captured = capsys.readouterr()
                snapshot.assert_match(captured.out)
