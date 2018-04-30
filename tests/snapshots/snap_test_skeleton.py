# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_comment 1'] = '''# a b
'''

snapshots['test_steps 1'] = '''steps:
'''

snapshots['test_env 1'] = '''env:
  a: b
  c: d
  e: f=g
  j: ''
'''
