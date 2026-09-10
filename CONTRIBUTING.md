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

1. Top level (abstract) dependencies for building the site go in `pyproject.toml`. Make sure to include any packages that have jupyter extensions, such as `ipywidgets` which depends on `jupyterlab-widgets`.
2. Specific packages that need to be locked in the pyodide distribution (ie. because you're importing them directly) are added to `jupyter_lite_config.json` under the `PyodideLockAddon` and `PyodideLockOfflineAddon` sections. 
3. Directly imported dependencies (especially those imported in a module and not the Jupyter notebook directly) should also be added to `prefetch_extras` section, so they're ready and available. The Jupyterlite environment will not retrieve packages until first import, and the detection of imports from other modules outside the notebook is not reliable.


### Dependency Considerations

- Every dependency is an additional cost in download and startup time for the user: bring in only what's needed. In particular be mindful of the numerical Python ecosystem as just numpy is a 15MiB extra download.
- Pure Python wheels work well out of the box, but you need to check their dependencies.
- The pyodide distribution itself includes a number of prebuilt packages, including a range of useful things.
- A WASM platform tag for wheels was supported in PyPI as mid 2026: this landscape is likely to change quite a bit as more packages built directly for that environment.   





