=====
bkyml
=====

A CLI tool to generate a `pipeline.yaml` file for Buildkite on the fly.


Sub-Commands
===========


## steps

Example:
```sh
bkyml steps
```

will produce
```yaml
steps:
```

## comment

Example:
```sh
bkyml comment bla foo
```

will produce
```yaml
# bla foo
```

## env

Example:
```sh
bkyml env var=vale voo=bla blubb=2=s
```

will produce
```yaml
env:
  blubb: 2=s
  var: vale
  voo: bla
```