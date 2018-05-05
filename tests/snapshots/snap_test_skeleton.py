# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_steps 1'] = 'steps:'

snapshots['test_env 1'] = '''  - command: cmd
    env:
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

snapshots['test_comment 1'] = '# a b'

snapshots['test_label 1'] = '''  - label: My label
    command: cmd
'''

snapshots['test_branches 1'] = '''  - command: cmd
    branches: master release-*
'''

snapshots['test_agents 1'] = '''  - command: cmd
    agents:
      npm: 'true'
      mvn: 'true'
'''

snapshots['test_artifact_paths_1 1'] = '''  - command: cmd
    artifact_paths: logs/**/*;coverage/**/*
'''

snapshots['test_artifact_paths_n 1'] = '''  - command: cmd
    artifact_paths:
      - logs/**/*
      - coverage/**/*
'''

snapshots['test_parallelism 1'] = '''  - command: cmd
    parallelism: 4
'''

snapshots['test_parallelism_1 1'] = '''  - command: cmd
'''

snapshots['test_concurrency 1'] = '''  - command: cmd
    concurrency: 2
    concurrency_group: my/group
'''

snapshots['test_main 1'] = '''  - command: x
'''

snapshots['test_command 1'] = '''  - command: x

'''

snapshots['test_no_command 1'] = ''

snapshots['test_help 1'] = '''usage:  comment [-h] COMMENT [COMMENT ...]

positional arguments:
  COMMENT     Comment

optional arguments:
  -h, --help  show this help message and exit
'''

snapshots['test_help 2'] = '''usage:  steps [-h]

optional arguments:
  -h, --help  show this help message and exit
'''

snapshots['test_help 3'] = '''usage:  env [-h] --var KEY VALUE

optional arguments:
  -h, --help       show this help message and exit
  --var KEY VALUE  A map of environment variables for this pipeline.
'''

snapshots['test_help 4'] = '''usage:  command [-h] --command COMMAND [COMMAND ...] [--label LABEL]
                [--branches BRANCH_PATTERN [BRANCH_PATTERN ...]]
                [--env KEY VALUE] [--agents KEY VALUE]
                [--artifact-paths GLOB_OR_PATH [GLOB_OR_PATH ...]]
                [--parallelism POSITIVE_NUMBER]
                [--concurrency POSITIVE_NUMBER]
                [--concurrency-group GROUP_NAME]
                [--timeout-in-minutes TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  --command COMMAND [COMMAND ...]
                        The shell command/s to run during this step.
  --label LABEL         The label that will be displayed in the pipeline
                        visualisation in Buildkite. Supports emoji.
  --branches BRANCH_PATTERN [BRANCH_PATTERN ...]
                        The branch pattern defining which branches will
                        include this step in their builds.
  --env KEY VALUE       A map of environment variables for this step.
  --agents KEY VALUE    A map of meta-data keys to values to target specific
                        agents for this step.
  --artifact-paths GLOB_OR_PATH [GLOB_OR_PATH ...]
                        The glob path or paths where artifacts from this step
                        will be uploaded.
  --parallelism POSITIVE_NUMBER
                        The number of parallel jobs that will be created based
                        on this step.
  --concurrency POSITIVE_NUMBER
                        The maximum number of jobs created from this step that
                        are allowed to run at the same time. Requires
                        --concurrency-group.
  --concurrency-group GROUP_NAME
                        A unique name for the concurrency group that you are
                        creating with the concurrency attribute.
  --timeout-in-minutes TIMEOUT
                        The number of minutes a job created from this step is
                        allowed to run. If the job does not finish within this
                        limit, it will be automatically cancelled and the
                        build will fail.
'''

snapshots['test_env_all 1'] = '''env:
  a: b
  c: d
'''

snapshots['test_timeout_in_minutes_minus 1'] = '''  - command: cmd
'''

snapshots['test_timeout_in_minutes_0 1'] = '''  - command: cmd
'''

snapshots['test_timeout_in_minutes_1 1'] = '''  - command: cmd
    timeout_in_minutes: 1
'''
