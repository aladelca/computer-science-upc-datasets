# Runbook 01: Setup

## Goal

Prepare the local environment so the `upc_datasets` toolkit can run reliably.

## Prerequisites

- `Python 3.11+`
- shell access in the project root
- enough disk space for local parquet outputs

## Project Root

Run all commands from:

```bash
/Users/alarcon/Documents/other/upc/big_data
```

## Create the Virtual Environment

```bash
python3 -m venv .venv
```

## Install the Toolkit and Test Dependencies

```bash
.venv/bin/pip install -e '.[dev]'
```

Installed distribution:

- `upc-datasets`

## Verify the Installation

```bash
.venv/bin/python -m upc_datasets.cli --help
.venv/bin/python -m upc_datasets.cli list-builders
.venv/bin/python -m upc_datasets.cli list-datasets
```

Expected builders:

- `audio-core`
- `lyrics-core`
- `playlist-events`
- `song-graph`

## Important Runtime Notes

- The toolkit uses `polars` and `pyarrow`.
- `pyspark` is not the active execution path in this workspace.
- Spark `4.1.1` is installed, but the local Java runtime is too old to launch it successfully.

## Recommended Directory Layout

```text
data/
  raw/
    fma/
    musixmatch_msd/
    msd/
    mpd/
  processed/
```
