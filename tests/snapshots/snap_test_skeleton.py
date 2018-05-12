# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

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

snapshots['test_steps 1'] = '''steps:
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

snapshots['test_help 6'] = '''usage:  wait [-h] [--continue-on-failure]

optional arguments:
  -h, --help            show this help message and exit
  --continue-on-failure
                        Continue even if previous steps failed
'''

snapshots['test_wait 1'] = '''  - wait
'''

snapshots['test_wait_continue_on_failure 1'] = '''  - wait:
    continue_on_failure: true
'''

snapshots['test_comment 1'] = '''# a
# b'''

snapshots['test_comment_multiline 1'] = '''# multiline
# comments
# are fun'''

snapshots['test_trigger_simple 1'] = '''  - trigger: my-pipeline
'''

snapshots['test_trigger_label 1'] = '''  - trigger: my-pipeline
    label: ':rocket: Deploy'
'''

snapshots['test_help 7'] = '''usage:  trigger [-h] [--label LABEL] [--async]
                [--branches BRANCH_PATTERN [BRANCH_PATTERN ...]]
                [--build-message MESSAGE] [--build-commit SHA]
                [--build-branch BRANCH] [--build-env KEY VALUE]
                [--build-meta-data KEY VALUE]
                PIPELINE

positional arguments:
  PIPELINE              Name of the pipeline to trigger

optional arguments:
  -h, --help            show this help message and exit
  --label LABEL         The label that will be displayed in the pipeline
                        visualisation in Buildkite. Supports emoji.
  --async               If given, the step will immediately continue,
                        regardless of the success of the triggered build.
  --branches BRANCH_PATTERN [BRANCH_PATTERN ...]
                        The branch pattern defining which branches will
                        include this step in their builds.
  --build-message MESSAGE
                        The message for the build. Supports emoji.
  --build-commit SHA    The commit hash for the build
  --build-branch BRANCH
                        The branch for the build
  --build-env KEY VALUE
                        A map of environment variables for the triggered
                        build.
  --build-meta-data KEY VALUE
                        A map of meta-data for the triggered build.
'''

snapshots['test_trigger_async 1'] = '''  - trigger: my-pipeline
    async: true
'''

snapshots['test_trigger_branches 1'] = '''  - trigger: my-pipeline
    branches: master release-*
'''

snapshots['test_trigger_build_branch 1'] = '''  - trigger: my-pipeline
    build:
      branch: master
'''

snapshots['test_trigger_build_message 1'] = '''  - trigger: my-pipeline
    build:
      message: Put the lime in the coconut
'''

snapshots['test_trigger_build_commit 1'] = '''  - trigger: my-pipeline
    build:
      commit: c0ffee
'''

snapshots['test_trigger_build_env 1'] = '''  - trigger: my-pipeline
    build:
      env:
        a: b
'''

snapshots['test_trigger_build_meta_data 1'] = '''  - trigger: my-pipeline
    build:
      meta_data:
        a: b
'''

snapshots['test_empty_command 1'] = '''usage:  [-h] [--version] [-v] [-vv]
        {comment,steps,env,command,plugin,wait,trigger,block} ...

Generate pipeline YAML for Buildkite

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbose         set loglevel to INFO
  -vv, --very-verbose   set loglevel to DEBUG

subcommands:
  valid subcommands

  {comment,steps,env,command,plugin,wait,trigger,block}
                        additional help
'''

snapshots['test_help 8'] = '''usage:  block [-h] [--prompt PROMPT]
              [--branches BRANCH_PATTERN [BRANCH_PATTERN ...]]
              [--field-text KEY LABEL HINT REQUIRED DEFAULT]
              [--field-select KEY LABEL HINT REQUIRED DEFAULT KEY_VALUE_PAIRS [KEY_VALUE_PAIRS ...]
              [KEY LABEL HINT REQUIRED DEFAULT KEY_VALUE_PAIRS [KEY_VALUE_PAIRS ...]
              ...]]
              LABEL

positional arguments:
  LABEL                 Label of the block step. Supports emoji.

optional arguments:
  -h, --help            show this help message and exit
  --prompt PROMPT       The instructional message displayed in the dialog box
                        when the unblock step is activated.
  --branches BRANCH_PATTERN [BRANCH_PATTERN ...]
                        The branch pattern defining which branches will
                        include this step in their builds.
  --field-text KEY LABEL HINT REQUIRED DEFAULT
                        A text field. KEY is the meta-data key that stores the
                        field's input. LABEL is the label of the field. HINT
                        is the explanatory text that is shown after the label.
                        REQUIRED (true/false) A boolean value that defines
                        whether the field is required for form submission.
                        DEFAULT is value that is pre-filled in the text field.
  --field-select KEY LABEL HINT REQUIRED DEFAULT KEY_VALUE_PAIRS [KEY_VALUE_PAIRS ...] [KEY LABEL HINT REQUIRED DEFAULT KEY_VALUE_PAIRS [KEY_VALUE_PAIRS ...] ...]
                        A select field. KEY is the meta-data key that stores
                        the field's input. LABEL is the label of the field.
                        HINT is the explanatory text that is shown after the
                        label. REQUIRED (true/false) A boolean value that
                        defines whether the field is required for form
                        submission. DEFAULT is value that is pre-selected.
                        KEY_VALUE_PAIRS is value that is pre-selected.
'''

snapshots['test_block_simple 1'] = '''  - block: ':rocket: Release'
'''

snapshots['test_cli_command 1'] = '''  - command: x

'''

snapshots['test_block_prompt 1'] = '''  - block: ':rocket: Release'
    prompt: Really release?
'''

snapshots['test_block_branches 1'] = '''  - block: ':rocket: Release'
    branches: master release-*
'''

snapshots['test_block_field_text 1'] = '''  - block: ':rocket: Release'
    fields:
      - text: label
        key: key
        hint: hint
        default: default
'''

snapshots['test_block_field_text_required 1'] = '''  - block: ':rocket: Release'
    fields:
      - text: label
        key: key
        hint: hint
        required: true
        default: default
'''

snapshots['test_block_field_text_no_hint 1'] = '''  - block: ':rocket: Release'
    fields:
      - text: label
        key: key
        default: default
'''

snapshots['test_block_field_text_no_default 1'] = '''  - block: ':rocket: Release'
    fields:
      - text: label
        key: key
        hint: hint
'''

snapshots['test_block_field_select 1'] = '''  - block: ':rocket: Release'
    fields:
      - select: label
        key: key
        hint: hint
        default: default
        options:
          - label: Label1
            value: opt1
          - label: Label2
            value: opt2
'''

snapshots['test_block_field_multi_fields 1'] = '''  - block: ':rocket: Release'
    fields:
      - text: label
        key: key
        hint: hint
        default: default
      - select: label
        key: key
        hint: hint
        default: default
        options:
          - label: Label1
            value: opt1
          - label: Label2
            value: opt2
'''
