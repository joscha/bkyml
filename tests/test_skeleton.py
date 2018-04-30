#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import argparse
from bkyml.skeleton import comment, steps, env

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
    ns.env_pairs = [ 'a=b', 'c=d', 'e=f=g', 'h', '=i', 'j=']
    snapshot.assert_match(env(ns))
