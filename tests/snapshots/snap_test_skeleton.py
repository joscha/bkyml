# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_comment 1'] = '# a b'

snapshots['test_steps 1'] = 'steps:'

snapshots['test_env 1'] = '''env:
  a: b
  c: d
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

snapshots['test_command_env 1'] = '''  - command: cmd
    env:
      a: b
      c: d
'''

snapshots['test_command_agents 1'] = '''  - command: cmd
    agents:
      npm: 'true'
      mvn: 'true'
'''

snapshots['test_command_artifact_paths_1 1'] = '''  - command: cmd
    artifact_paths: logs/**/*;coverage/**/*
'''

snapshots['test_command_artifact_paths_n 1'] = '''  - command: cmd
    artifact_paths:
      - logs/**/*
      - coverage/**/*
'''

snapshots['test_command_parallelism 1'] = '''  - command: cmd
    parallelism: 4
'''

snapshots['test_command_parallelism_1 1'] = '''  - command: cmd
'''

snapshots['test_command_concurrency 1'] = '''  - command: cmd
    concurrency: 2
    concurrency_group: my/group
'''

snapshots['test_parse_main 1'] = '''  - command: x
'''
