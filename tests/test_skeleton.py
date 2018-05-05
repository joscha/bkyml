#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pytest
import argparse
from unittest.mock import patch
from bkyml.skeleton import Comment, Steps, Env, Command, parse_main, run, check_positive, parse_args

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
    def test_command_1(snapshot):
        ns = argparse.Namespace()
        ns.command = [[ "my-command arg1 'arg 2'" ]]
        snapshot.assert_match(Command.command(ns))

    def test_command_n(snapshot):
        ns = argparse.Namespace()
        ns.command = [ [ 'a', 'b' ], [ 'c', 'd' ] ]
        snapshot.assert_match(Command.command(ns))

    def test_label(snapshot):
        ns = argparse.Namespace()
        ns.command = [ [ 'cmd' ] ]
        ns.label = 'My label'
        snapshot.assert_match(Command.command(ns))

    def test_branches(snapshot):
        ns = argparse.Namespace()
        ns.command = [ [ 'cmd' ] ]
        ns.branches = [ 'master', 'release-*' ]
        snapshot.assert_match(Command.command(ns))

    def test_env(snapshot):
        ns = argparse.Namespace()
        ns.command = [ [ 'cmd' ] ]
        ns.env = [ ['a', 'b'], ['c', 'd'] ]
        snapshot.assert_match(Command.command(ns))

    def test_agents(snapshot):
        ns = argparse.Namespace()
        ns.command = [ [ 'cmd' ] ]
        ns.agents = [ ['npm', 'true'], ['mvn', 'true'] ]
        snapshot.assert_match(Command.command(ns))

    def test_artifact_paths_1(snapshot):
        ns = argparse.Namespace()
        ns.command = [ [ 'cmd' ] ]
        ns.artifact_paths = [[ "logs/**/*;coverage/**/*" ]]
        snapshot.assert_match(Command.command(ns))

    def test_artifact_paths_n(snapshot):
        ns = argparse.Namespace()
        ns.command = [ [ 'cmd' ] ]
        ns.artifact_paths = [[ "logs/**/*", "coverage/**/*" ]]
        snapshot.assert_match(Command.command(ns))

    def test_parallelism(snapshot):
        ns = argparse.Namespace()
        ns.command = [ [ 'cmd' ] ]
        ns.parallelism = 4
        snapshot.assert_match(Command.command(ns))

    def test_parallelism_1(snapshot):
        ns = argparse.Namespace()
        ns.command = [ [ 'cmd' ] ]
        ns.parallelism = 1
        snapshot.assert_match(Command.command(ns))

    def test_concurrency(snapshot):
        ns = argparse.Namespace()
        ns.command = [ [ 'cmd' ] ]
        ns.concurrency = 2
        ns.concurrency_group = 'my/group'
        snapshot.assert_match(Command.command(ns))

    def test_concurrency_cli(capsys):
        with pytest.raises(SystemExit) as sys_exit:
            parse_main(['command', '--command', 'x', '--concurrency', '1'])
        assert '2' in str(sys_exit.value)
        captured = capsys.readouterr()
        assert '--concurrency requires --concurrency-group' in captured.err

    def test_timeout_in_minutes_minus(snapshot):
        ns = argparse.Namespace()
        ns.command = [ [ 'cmd' ] ]
        ns.timeout_in_minutes = -1
        snapshot.assert_match(Command.command(ns))

    def test_timeout_in_minutes_0(snapshot):
        ns = argparse.Namespace()
        ns.command = [ [ 'cmd' ] ]
        ns.timeout_in_minutes = 0
        snapshot.assert_match(Command.command(ns))

    def test_timeout_in_minutes_1(snapshot):
        ns = argparse.Namespace()
        ns.command = [ [ 'cmd' ] ]
        ns.timeout_in_minutes = 1
        snapshot.assert_match(Command.command(ns))

def describe_parse_main():
    def test_main(snapshot):
        snapshot.assert_match(parse_main(['command', '--command', 'x']))

def describe_cli():
    def test_command(snapshot, capsys):
        with patch.object(sys, 'argv', ['', 'command', '--command', 'x']):
            run()
        captured = capsys.readouterr()
        snapshot.assert_match(captured.out)

    def test_no_command(snapshot, capsys):
        with patch.object(sys, 'argv', ['']):
            run()
        captured = capsys.readouterr()
        snapshot.assert_match(captured.out)

    def test_help(snapshot, capsys):
        for subcommand in ['comment', 'steps', 'env', 'command']:
            with pytest.raises(SystemExit):
                with patch.object(sys, 'argv', ['', subcommand, '--help']):
                    run()
            captured = capsys.readouterr()
            snapshot.assert_match(captured.out)