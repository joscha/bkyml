# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_comment 1'] = '# a b'

snapshots['test_steps 1'] = 'steps:'

snapshots['test_env_empty 1'] = None

snapshots['test_env 1'] = '''env:
  a: b
  c: d
  e: f=g
  j: ''
'''

snapshots['test_command_1 1'] = '''  - command: my-command arg1 'arg 2'
'''

snapshots['test_command_n 1'] = '''  - command:
      - a
      - b
      - c
      - d
'''

snapshots['test_command_label 1'] = '''  - label: My label
    command: a
'''
