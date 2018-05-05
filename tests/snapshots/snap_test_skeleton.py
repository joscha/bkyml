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
    command: cmd
'''

snapshots['test_command_branches 1'] = '''  - command: cmd
    branches: master release-*
'''

snapshots['test_parse_main 1'] = '''  - command: x
'''

snapshots['test_command_env 1'] = '''  - command: cmd
    env:
      a: b
      c: d
      e: f=g
      j: ''
'''
