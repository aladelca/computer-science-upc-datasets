# Runbook 07: Package and Publish

## Goal

Build the `upc-datasets` distribution and publish it so students can install it with:

```bash
pip install upc-datasets
```

## Preconditions

- you have a PyPI account
- you own the target project name on PyPI
- the project version in `pyproject.toml` has been bumped

## Step 1: Install Packaging Tools

```bash
.venv/bin/pip install build twine
```

## Step 2: Run the Test Suite

```bash
.venv/bin/pytest
```

Do not publish if the suite is failing.

## Step 3: Build the Distribution

```bash
.venv/bin/python -m build
```

Expected outputs:

```text
dist/
  upc_datasets-<version>.tar.gz
  upc_datasets-<version>-py3-none-any.whl
```

## Step 4: Validate the Distribution

```bash
.venv/bin/python -m twine check dist/*
```

## Step 5: Upload to TestPyPI First

```bash
.venv/bin/python -m twine upload --repository testpypi dist/*
```

Then verify installation from TestPyPI in a clean environment.

## Step 6: Upload to PyPI

```bash
.venv/bin/python -m twine upload dist/*
```

## Step 7: Smoke Test the Published Package

In a clean virtual environment:

```bash
pip install upc-datasets
python -c "import upc_datasets; print(upc_datasets.list_datasets())"
upc-datasets show-dataset pachamix_lyrics_long
```

## Notes

- The import package is `upc_datasets`.
- The CLI command is `upc-datasets`.
- The internal compatibility package `pachamix_data` remains available in the source tree, but students should use `upc_datasets`.
