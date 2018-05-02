#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import argparse
from bkyml.skeleton import comment, steps, env, command, parse_main

__author__ = "Joscha Feth"
__copyright__ = "Joscha Feth"
__license__ = "mit"

def test_comment(snapshot):
    ns = argparse.Namespace()
    ns.str = ['a', 'b']

    snapshot.assert_match(comment(ns))

def test_steps(snapshot):
    ns = argparse.Namespace()
    snapshot.assert_match(steps(ns))

def test_env(snapshot):
    ns = argparse.Namespace()
    ns.env_pairs = [ 'a=b', 'c=d', 'e=f=g', 'h', '=i', 'j=' ]
    snapshot.assert_match(env(ns))

def test_env_empty(snapshot):
    ns = argparse.Namespace()
    ns.env_pairs = [ '', '' ]
    snapshot.assert_match(env(ns))

def test_command_1(snapshot):
    ns = argparse.Namespace()
    ns.command = [[ "my-command arg1 'arg 2'" ]]
    snapshot.assert_match(command(ns))

def test_command_n(snapshot):
    ns = argparse.Namespace()
    ns.command = [ [ 'a', 'b' ], [ 'c', 'd' ] ]
    snapshot.assert_match(command(ns))

def test_command_label(snapshot):
    ns = argparse.Namespace()
    ns.command = [ [ 'a'] ]
    ns.label = 'My label'
    snapshot.assert_match(command(ns))

def test_cli(snapshot):
    snapshot.assert_match(parse_main(['command', '--command', 'x']))
