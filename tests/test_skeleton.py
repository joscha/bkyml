#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=unused-variable

import sys
import pytest
import argparse
from unittest.mock import patch
from bkyml.skeleton import Comment, Steps, Env, Command, parse_main, run, check_positive, parse_args, bool_or_string

__author__ = "Joscha Feth"
__copyright__ = "Joscha Feth"
__license__ = "mit"

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
    def test_comment(snapshot):
        ns = argparse.Namespace()
        ns.str = ['a', 'b']
        snapshot.assert_match(Comment.comment(ns))

def describe_steps():
    def test_steps(snapshot):
        ns = argparse.Namespace()
        snapshot.assert_match(Steps.steps(ns))

def describe_env():
    def test_env_all(snapshot):
        ns = argparse.Namespace()
        ns.var = [ ['a', 'b'], ['c', 'd'] ]
        snapshot.assert_match(Env.env(ns))

def describe_command():

    @pytest.fixture
    def ns():
        return argparse.Namespace()

    @pytest.fixture
    def generic_command_call(ns, snapshot):
        ns.command = [[ 'cmd' ]]
        snapshot.assert_match(Command.command(ns))

    @pytest.fixture
    def assert_command_call_error(capsys, command_args, message):
        with pytest.raises(SystemExit) as sys_exit:
            parse_main(['command', '--command', 'cmd'] + command_args)
        assert '2' in str(sys_exit.value)
        captured = capsys.readouterr()
        assert message in captured.err

    def test_command_1(ns, snapshot):
        ns.command = [[ "my-command arg1 'arg 2'" ]]
        snapshot.assert_match(Command.command(ns))

    def test_command_n(ns, snapshot):
        ns.command = [ [ 'a', 'b' ], [ 'c', 'd' ] ]
        snapshot.assert_match(Command.command(ns))

    def test_label(ns, snapshot):
        ns.label = 'My label'
        generic_command_call(ns, snapshot)

    def test_branches(ns, snapshot):
        ns.branches = ['master', 'release-*']
        generic_command_call(ns, snapshot)

    def test_env(ns, snapshot):
        ns.env = [['a', 'b'], ['c', 'd']]
        generic_command_call(ns, snapshot)

    def test_agents(ns, snapshot):
        ns.agents = [['npm', 'true'], ['mvn', 'true']]
        generic_command_call(ns, snapshot)

    def test_artifact_paths_0(ns, snapshot):
        ns.artifact_paths = []
        generic_command_call(ns, snapshot)

    def test_artifact_paths_1(ns, snapshot):
        ns.artifact_paths = [[ "logs/**/*;coverage/**/*" ]]
        generic_command_call(ns, snapshot)

    def test_artifact_paths_n(ns, snapshot):
        ns.artifact_paths = [[ "logs/**/*", "coverage/**/*" ]]
        generic_command_call(ns, snapshot)

    def test_parallelism(ns, snapshot):
        ns.parallelism = 4
        generic_command_call(ns, snapshot)

    def test_parallelism_1(ns, snapshot):
        ns.parallelism = 1
        generic_command_call(ns, snapshot)

    def test_concurrency(ns, snapshot):
        ns.concurrency = 2
        ns.concurrency_group = 'my/group'
        generic_command_call(ns, snapshot)

    def test_concurrency_cli(capsys):
        assert_command_call_error(
            capsys,
            ['--concurrency', '1'],
            '--concurrency requires --concurrency-group'
        )

    def test_timeout_in_minutes_minus(ns, snapshot):
        ns.timeout_in_minutes = -1
        generic_command_call(ns, snapshot)

    def test_timeout_in_minutes_0(ns, snapshot):
        ns.timeout_in_minutes = 0
        generic_command_call(ns, snapshot)

    def test_timeout_in_minutes_1(ns, snapshot):
        ns.timeout_in_minutes = 1
        generic_command_call(ns, snapshot)

    def test_skip_bool_true(ns, snapshot):
        ns.skip = True
        generic_command_call(ns, snapshot)

    def test_skip_bool_false(ns, snapshot):
        ns.skip = False
        generic_command_call(ns, snapshot)

    def test_skip_string(ns, snapshot):
        ns.skip = 'Some reason'
        generic_command_call(ns, snapshot)

    def test_retry_manual(ns, snapshot):
        ns.retry = 'manual'
        generic_command_call(ns, snapshot)

    def test_retry_automatic(ns, snapshot):
        ns.retry = 'automatic'
        generic_command_call(ns, snapshot)

    def test_retry_automatic_limit(ns, snapshot):
        ns.retry = 'automatic'
        ns.retry_automatic_limit = 2
        generic_command_call(ns, snapshot)

    def test_retry_automatic_limit_11(ns, snapshot):
        ns.retry = 'automatic'
        ns.retry_automatic_limit = 11
        generic_command_call(ns, snapshot)

    def test_retry_automatic_exit_status_star(ns, snapshot):
        ns.retry = 'automatic'
        ns.retry_automatic_exit_status = '*'
        generic_command_call(ns, snapshot)

    def test_retry_automatic_exit_status_number(ns, snapshot):
        ns.retry = 'automatic'
        ns.retry_automatic_exit_status = 1
        generic_command_call(ns, snapshot)

    def test_retry_automatic_exit_status_and_limit(ns, snapshot):
        ns.retry = 'automatic'
        ns.retry_automatic_limit = 2
        ns.retry_automatic_exit_status = 1
        generic_command_call(ns, snapshot)

    def test_retry_automatic_tuple_0(ns, snapshot):
        ns.retry = 'automatic'
        ns.retry_automatic_tuple = []
        generic_command_call(ns, snapshot)

    def test_retry_automatic_tuple_n(ns, snapshot):
        ns.retry = 'automatic'
        ns.retry_automatic_tuple = [['*', 2], [ 1, 3 ]]
        generic_command_call(ns, snapshot)

    def test_retry_automatic_cli_exit_status_string(capsys):
        assert_command_call_error(
            capsys,
            ['--retry', 'automatic', '--retry-automatic-exit-status', 'xxx'],
            'xxx is an invalid value'
        )

    def test_retry_automatic_cli_exit_status_no_retry(capsys):
        assert_command_call_error(
            capsys,
            ['--retry-automatic-exit-status', '*'],
            '--retry-automatic-exit-status requires --retry automatic'
        )

    def test_retry_automatic_cli_limit_no_retry(capsys):
        assert_command_call_error(
            capsys,
            ['--retry-automatic-limit', '2'],
            '--retry-automatic-limit requires --retry automatic'
        )

    def test_retry_automatic_cli_tuple_no_retry(capsys):
        assert_command_call_error(
            capsys,
            ['--retry-automatic-tuple', '*', '2'],
            '--retry-automatic-tuple requires --retry automatic'
        )

    def test_retry_automatic_cli_tuple_no_combine_exit_status(capsys):
        assert_command_call_error(
            capsys,
            ['--retry', 'automatic', '--retry-automatic-tuple', '*', '2', '--retry-automatic-exit-status', '*'],
            '--retry-automatic-tuple can not be combined with --retry-automatic-exit-status'
        )

    def test_retry_automatic_cli_tuple_no_combine_limit(capsys):
        assert_command_call_error(
            capsys,
            ['--retry', 'automatic', '--retry-automatic-tuple', '*', '2', '--retry-automatic-limit', '2'],
            '--retry-automatic-tuple can not be combined with --retry-automatic-limit'
        )

def describe_parse_main():
    def test_main(snapshot):
        snapshot.assert_match(parse_main(['command', '--command', 'x']))

def describe_cli():

    @pytest.fixture
    def run_run(capsys, snapshot, args):
        with patch.object(sys, 'argv', [''] + args):
            run()
        captured = capsys.readouterr()
        snapshot.assert_match(captured.out)

    def test_command(snapshot, capsys):
        run_run(capsys, snapshot, ['command', '--command', 'x'])

    def test_no_command(snapshot, capsys):
        run_run(capsys, snapshot, [])

    def test_help(snapshot, capsys):
        for subcommand in ['comment', 'steps', 'env', 'command']:
            with pytest.raises(SystemExit):
                with patch.object(sys, 'argv', ['', subcommand, '--help']):
                    run()
            captured = capsys.readouterr()
            snapshot.assert_match(captured.out)
