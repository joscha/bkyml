=====
bkyml
=====
.. image:: https://travis-ci.org/joscha/bkyml.svg?branch=master
    :target: https://travis-ci.org/joscha/bkyml
    
.. image:: https://coveralls.io/repos/github/joscha/bkyml/badge.svg?branch=master
    :target: https://coveralls.io/github/joscha/bkyml?branch=master

A CLI tool to generate a `pipeline.yaml` file for Buildkite on the fly.


Example:

.. code:: shell

  bkyaml comment 'Frontend tests pipeline'
  bkyaml env FORCE_COLOR=1
  bkyaml steps
  bkyml command \
    --command 'yarn install' \
    --command 'yarn test' \
    --label ':karma: tests'

will produce

.. code:: yaml

  # Frontend tests pipeline
  env:
    FORCE_COLOR: 1
  steps:
    - label: ':karma: tests'
      command:
        - yarn install
        - yarn test


This allows you to dynamically generate pipelines:

.. code:: bash

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

  bkyml comment bla foo

will produce

.. code:: yaml

  # bla foo


env
---

Example:

.. code:: shell

  bkyaml env --var A B --var C D

will produce

.. code:: yaml

  env:
    A: B
    C: D

command
-------

Example:

..code:: shell

  bkyaml command \
      --command 'yarn install' \
      --command 'yarn test' \
      --env FORCE_COLOR 1 \
      --branches master \
      --label ':yarn: tests' \
      --agents yarn true \
      --artifact-paths 'logs/**/*' 'coverage/**/*' \
      --parallelism 5


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