# Contributing Guide

## Scope

- If it can run with few dependencies in the browser
- If the workflow can be constructed so that each cell in a notebook is independent and does something useful
- Simple input/output transforms work

## Setup

### Development dependencies and setup

```
# Install all required development and build dependencies
pip install .[dev,build-jupyterlite]
# Integrate nbstripout with git, so we can never check in notebook code cell output. 
nbstripout --install
```


## Managing Dependencies


### Dependency Constraints

- Avoid the numerical Python ecosystem: unfortunately just NumPy itself is over 10MB. The pyodide framework we're using is already quite large so we want to avoid dependencies that further compound the download and startup resources needed.
- Pure Python packages much preferred. Some important packages are already compiled for WASM, but not everything, and sticking to pure Python and the standard library is much preferred.
- Keep jupyter and ipywidget specific functionality in notebooks, and not in the simple_prep package: we may want to deploy that separately to PYPI as a little toolkit in the future.


## Testing and Linting

- Standard testing for the utility libraries?
- TBD: testing for notebook interfaces!


### Unknown

Testing the GUI interface of the notebooks?





