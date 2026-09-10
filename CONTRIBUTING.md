# Contributing Guide

## Scope

Simple data transformation tools that have a simple(ish) upload -> configure -> transform -> download workflow.

- If it can run with few dependencies in the browser
- If the workflow can be constructed so that each cell in a notebook is independent and does something useful
- Simple input/output transformations that help people move from their conventional data formats to tools from other disciplines/that assume other conventions.

## Setup

### Development dependencies and setup

```
# Install all required development and build dependencies
pip install .[dev]

```

### Building the site

```
# Building the jupyterlite site
tox -e build_web

```

### Serving the site locally

```
# Serve the locally built site on http://localhost:8000
python -m http.server -d docs 8000

```

## Managing Dependencies

1. Top level (abstract) dependencies go in `pyproject.toml`.
2. A specific known configuration of dependencies is generated from that using `tox -e bump_environment` which uses `pip-compile` from `pip-tools`.
3. Specific packages from that to be locked in the pyodide distribution are added to `jupyter_lite_config.json` under the `PyodideLockAddon` and `PyodideLockOfflineAddon` sections. 


### Dependency Considerations

- Every dependency is an additional cost in download and startup time for the user: bring in only what's needed. In particular be mindful of the numerical Python ecosystem as just numpy is a 15MiB extra download.
- Pure Python wheels work well out of the box, but you need to check their dependencies.
- The pyodide distribution itself includes a number of prebuilt packages, including a range of useful things.
- A WASM platform tag for wheels was supported in PyPI as mid 2026: this landscape is likely to change quite a bit as more packages built directly for that environment.   





