#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import argparse
from bkyml.skeleton import comment, steps

__author__ = "Joscha Feth"
__copyright__ = "Joscha Feth"
__license__ = "mit"

def test_comment(snapshot):
    args = argparse.Namespace()
    args.str = ['a', 'b']

    snapshot.assert_match(comment(args))

def test_steps(snapshot):
    args = argparse.Namespace()
    snapshot.assert_match(steps(args))