=====
bkyml
=====
.. image:: https://travis-ci.org/joscha/bkyml.svg?branch=master
    :target: https://travis-ci.org/joscha/bkyml
    
.. image:: https://coveralls.io/repos/github/joscha/bkyml/badge.svg?branch=master
    :target: https://coveralls.io/github/joscha/bkyml?branch=master

A CLI tool to generate a ``pipeline.yaml`` file for Buildkite on the fly.

Install via :code:`pip install bkyml` (see https://pypi.org/project/bkyml/)


Example:

.. code:: shell

  bkyml comment 'Frontend tests pipeline'
  bkyml env \
      --var FORCE_COLOR 1
  bkyml steps
  bkyml command \
      --command 'yarn install' \
      --command 'yarn test' \
      --label ':karma: tests'
  bkyml wait
  bkyml plugin \
      --plugin 'org/upload-coverage#1.0.0' dir=./coverage

will produce

.. code:: yaml

  # Frontend tests pipeline
  env:
    FORCE_COLOR: '1'

  steps:

    - label: ':karma: tests'
      command:
        - yarn install
        - yarn test

    - wait

    - plugins:
        org/upload-coverage#1.0.0:
          dir: ./coverage


This allows you to dynamically generate pipelines:

.. code:: shell

  #!/bin/env bash
  set -eu -o pipefail

  bkyml comment "Pipeline for running all tests in test/*"
  bkyml steps

  # add a new command step to run the tests in each test directory
  for test_dir in test/*/; do
    bkyml command \
        --command "run_tests ${test_dir}" \
        --label "Run tests for '${test_dir}'"
  done


Sub-Commands
============


steps
-----

Example:

.. code:: shell

  bkyml steps

will produce

.. code:: yaml

  steps:

comment
-------

Example:

.. code:: shell

  bkyml comment \
      'Hello world!' 'What a nice day :)'

will produce

.. code:: yaml

  # Hello world!
  # What a nice day :)


env
---

Example:

.. code:: shell

  bkyml env \
      --var A B \
      --var C D

will produce

.. code:: yaml

  env:
    A: B
    C: D

command
-------

Example:

.. code:: shell

  bkyml command \
      --command 'yarn install' \
      --command 'yarn test' \
      --env FORCE_COLOR 1 \
      --branches master \
      --label ':yarn: tests' \
      --agents yarn true \
      --artifact-paths 'logs/**/*' 'coverage/**/*' \
      --parallelism 5 \
      --concurrency 2 \
      --concurrency-group my/group \
      --timeout-in-minutes 60 \
      --skip 'Some reason' \
      --retry automatic \
      --retry-automatic-tuple '*' 2 \
      --retry-automatic-tuple 1 3 \
      --plugin docker-compose#v1.3.2 build=app image-repository=index.docker.io/org/repo

will produce

.. code:: yaml

  - label: ':yarn: tests'
    command:
      - yarn install
      - yarn test
    branches: master
    env:
      FORCE_COLOR: '1'
    agents:
      yarn: 'true'
    artifact_paths:
      - logs/**/*
      - coverage/**/*
    parallelism: 5
    concurrency: 2
    concurrency_group: my/group
    timeout_in_minutes: 60
    skip: Some reason
    retry:
      automatic:
        - exit_status: '*'
          limit: 2
        - exit_status: 1
          limit: 3
    plugins:
      docker-compose#v1.3.2:
        build: app
        image-repository: index.docker.io/org/repo

There is also:

* :code:`--retry-automatic-limit`
* :code:`--retry-automatic-exit-code`

which can't be used in conjunction with --retry-automatic-tuple

And:

* :code:`--retry-manual-allowed` (allowing manual retries, default)
* :code:`--no-retry-manual-allowed` (disallowing manual retries)
* :code:`--retry-manual-reason REASON` (giving a reason why retries are forbidden)
* :code:`--retry-manual-permit-on-passed` (allowing retries after the job has passed)
* :code:`--no-retry-manual-permit-on-passed` (disallowing retries after the job has passed, default)

Example:

.. code:: shell

  bkyml command \
      --command 'x' \
      --retry manual \
      --retry-manual-permit-on-passed \
      --no-retry-manual-allowed \
      --retry-manual-reason "Just because"

will result in

.. code:: yaml

  - command: x
    retry:
      manual:
        allowed: false
        reason: Just because
        permit_on_passed: true

plugin
------

Example:

.. code:: shell

  bkyaml plugin \
      --plugin 'org/repo#1.0.0' some=var other=var \
      --plugin 'org/other_repo' more=var \
      --name 'My name is working'

will result in

.. code:: yaml

  - name: My name is working
    plugins:
      org/repo#1.0.0:
        some: var
        other: var
      org/other_repo:
        more: var

wait
----

Example:

.. code:: shell

  bkyaml wait \
      --continue-on-failure


will result in

.. code:: yaml

  - wait:
    continue_on_failure: true

trigger
-------

Example:

.. code:: shell

  bkyaml trigger 'my-pipeline' \
      --branches master '*-release' \
      --build-message 'My build message' \
      --build-commit c0ffee \
      --build-branch green \
      --build-env FORCE_COLOR 1 \
      --build-meta-data release-name 1.0.0

will result in

.. code:: yaml

  - trigger: my-pipeline
    branches: master *-release
    build:
      branch: green
      commit: c0ffee
      message: My build message
      env:
        FORCE_COLOR: '1'
      meta_data:
        release-name: 1.0.0

block
-----

Example:

.. code:: shell

  bkyaml block ':rocket: Release'

will result in

.. code:: yaml

  - block: ':rocket: Release'

Example with a select field:

.. code:: shell

  bkyaml block ':rocket: Release!' \
      --field-select \
          'key' \
          'Field label' \
          'Some hint' \
          true \
          a \
          'a=A label' \
          'b=B label'

will result in:

.. code:: yaml

  - block: ':rocket: Release!'
    fields:
      - text: Field label
        key: key
        hint: Some hint
        required: true
        default: a
        options:
          - label: A label
            value: a
          - label: B label
            value: b

Example with a text field:

.. code:: shell

  bkyaml block ':rocket: Release!' \
      --field-text \
          'release-name' \
          'Release name' \
          'What should the next release name be?' \
          true \
          'Some release name'

will result in:

.. code:: yaml

  - block: ':rocket: Release!'
    fields:
      - text: Release name
        key: release-name
        hint: What should the next release name be?
        required: true
        default: Some release name
