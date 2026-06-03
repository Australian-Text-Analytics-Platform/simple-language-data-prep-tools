# Contributing Guide

## Scope

- If it can run with few dependencies in the browser
- If the workflow can be constructed so that each cell in a notebook is independent and does something useful

## Setup

### Development dependencies



## Managing Dependencies


### Dependency Constraints

- Avoid the numerical Python ecosystem: unfortunately just NumPy itself is over 10MB. The pyodide framework we're using is already quite large so we want to avoid dependencies that further compound the download and startup resources needed.
- Pure Python packages much preferred. Some important packages are already compiled for WASM, but not everything, and sticking to pure Python and the standard library is much preferred.


## Testing and Linting

- Standard testing for the utility libraries

### Unknown

Testing the GUI interface of the notebooks?





