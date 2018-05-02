=====
bkyml
=====

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

  bkyaml env FORCE_COLOR=1 A B=2=

will produce

.. code:: yaml

  env:
    FORCE_COLOR: 1
    A: ''
    B: 2=