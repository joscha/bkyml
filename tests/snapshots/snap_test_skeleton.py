# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_comment 1'] = '''# a
# b'''

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
                [--parallelism POSITIVE_NUMBER] [--concurrency POSITIVE_INT]
                [--concurrency-group GROUP_NAME]
                [--timeout-in-minutes TIMEOUT] [--skip BOOL_OR_STRING]
                [--retry {automatic,manual}]
                [--retry-automatic-exit-status INT_OR_STAR]
                [--retry-automatic-limit POSITIVE_INT]
                [--retry-automatic-tuple INT_OR_STAR POSITIVE_INT]
                [--retry-manual-allowed] [--no-retry-manual-allowed]
                [--retry-manual-reason REASON]
                [--retry-manual-permit-on-passed]
                [--no-retry-manual-permit-on-passed]
                [--plugin PLUGIN [KEY_VALUE_PAIR ...]]

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
  --concurrency POSITIVE_INT
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
  --skip BOOL_OR_STRING
                        Whether to skip this step or not.
  --retry {automatic,manual}
                        The conditions for retrying this step.
  --retry-automatic-exit-status INT_OR_STAR
                        The exit status number that will cause this job to
                        retry.
  --retry-automatic-limit POSITIVE_INT
                        The number of times this job can be retried. The
                        maximum value this can be set to is 10.
  --retry-automatic-tuple INT_OR_STAR POSITIVE_INT
                        The exit status number that will cause this job to
                        retry and a limit to go with it.
  --retry-manual-allowed
                        This job can be retried manually.
  --no-retry-manual-allowed
                        This job can not be retried manually.
  --retry-manual-reason REASON
                        A string that will be displayed in a tooltip on the
                        Retry button in Buildkite.
  --retry-manual-permit-on-passed
                        This job can be retried after it has passed.
  --no-retry-manual-permit-on-passed
                        This job can not be retried after it has passed.
  --plugin PLUGIN [KEY_VALUE_PAIR ...]
                        A plugin to run with this step. Optionally key/value
                        pairs for the plugin.
'''

snapshots['test_empty_command 1'] = ''

snapshots['test_steps 1'] = 'steps:'

snapshots['test_command 1'] = '''  - command: x

'''

snapshots['test_main 1'] = '''  - command: x
'''

snapshots['test_retry_automatic 1'] = '''  - command: cmd
    retry:
      automatic: true
'''

snapshots['test_retry_automatic_limit 1'] = '''  - command: cmd
    retry:
      automatic:
        limit: 2
'''

snapshots['test_retry_automatic_limit_11 1'] = '''  - command: cmd
    retry:
      automatic:
        limit: 10
'''

snapshots['test_retry_automatic_exit_status_star 1'] = '''  - command: cmd
    retry:
      automatic:
        exit_status: '*'
'''

snapshots['test_retry_automatic_exit_status_number 1'] = '''  - command: cmd
    retry:
      automatic:
        exit_status: 1
'''

snapshots['test_retry_automatic_exit_status_and_limit 1'] = '''  - command: cmd
    retry:
      automatic:
        exit_status: 1
        limit: 2
'''

snapshots['test_retry_automatic_tuple_0 1'] = '''  - command: cmd
    retry:
      automatic: true
'''

snapshots['test_retry_automatic_tuple_n 1'] = '''  - command: cmd
    retry:
      automatic:
        - exit_status: '*'
          limit: 2
        - exit_status: 1
          limit: 3
'''

snapshots['test_retry_manual 1'] = '''  - command: cmd
    retry:
      manual: true
'''

snapshots['test_retry_manual_allowed 1'] = '''  - command: cmd
    retry:
      manual: true
'''

snapshots['test_retry_manual_allowed 2'] = '''  - command: cmd
    retry:
      manual:
        allowed: false
'''

snapshots['test_retry_reason 1'] = '''  - command: cmd
    retry:
      manual:
        reason: Some reason why
'''

snapshots['test_retry_manual_permit_on_passed 1'] = '''  - command: cmd
    retry:
      manual:
        permit_on_passed: true
'''

snapshots['test_retry_manual_permit_on_passed 2'] = '''  - command: cmd
    retry:
      manual: true
'''

snapshots['test_command_1 1'] = '''  - command: my-command arg1 'arg 2'
'''

snapshots['test_command_n 1'] = '''  - command:
      - a
      - b
      - c
      - d
'''

snapshots['test_label 1'] = '''  - label: My label
    command: cmd
'''

snapshots['test_branches 1'] = '''  - command: cmd
    branches: master release-*
'''

snapshots['test_env 1'] = '''  - command: cmd
    env:
      a: b
      c: d
'''

snapshots['test_agents 1'] = '''  - command: cmd
    agents:
      npm: 'true'
      mvn: 'true'
'''

snapshots['test_artifact_paths_0 1'] = '''  - command: cmd
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

snapshots['test_timeout_in_minutes_minus 1'] = '''  - command: cmd
'''

snapshots['test_timeout_in_minutes_0 1'] = '''  - command: cmd
'''

snapshots['test_timeout_in_minutes_1 1'] = '''  - command: cmd
    timeout_in_minutes: 1
'''

snapshots['test_skip_bool_true 1'] = '''  - command: cmd
    skip: true
'''

snapshots['test_skip_bool_false 1'] = '''  - command: cmd
'''

snapshots['test_skip_string 1'] = '''  - command: cmd
    skip: Some reason
'''

snapshots['test_env_all 1'] = '''env:
  a: b
  c: d
'''

snapshots['test_retry_manual_pop_manual_retry 1'] = '''  - command: cmd
    retry:
      manual:
        permit_on_passed: true

'''

snapshots['test_help 5'] = '''usage:  plugin [-h] [--name NAME] --plugin PLUGIN [KEY_VALUE_PAIR ...]

optional arguments:
  -h, --help            show this help message and exit
  --name NAME           Name of the plugin step
  --plugin PLUGIN [KEY_VALUE_PAIR ...]
                        A plugin to run. Optionally key/value pairs for the
                        plugin.
'''

snapshots['test_command_plugin_none 1'] = '''  - command: cmd
'''

snapshots['test_command_plugin_no_args 1'] = '''  - command: cmd
    plugins:
      org/repo#1.0.0:
'''

snapshots['test_command_plugin_1 1'] = '''  - command: cmd
    plugins:
      org/repo#1.0.0:
        a: b
        c: d
'''

snapshots['test_command_plugin_n 1'] = '''  - command: cmd
    plugins:
      org/repo#1.0.0:
        a: b
        c: d
      other_org/other_repo:
        e: f
        g: h=i
'''

snapshots['test_plugin_plugin_none 1'] = ''

snapshots['test_plugin_plugin_no_args 1'] = '''  - plugins:
      org/repo#1.0.0:
'''

snapshots['test_plugin_plugin_1 1'] = '''  - plugins:
      org/repo#1.0.0:
        a: b
        c: d
'''

snapshots['test_plugin_plugin_n 1'] = '''  - plugins:
      org/repo#1.0.0:
        a: b
        c: d
      other_org/other_repo:
        e: f
        g: h=i
'''

snapshots['test_plugin_name_attr 1'] = '''  - name: My plugin run
    plugins:
      org/repo#1.0.0:
'''
