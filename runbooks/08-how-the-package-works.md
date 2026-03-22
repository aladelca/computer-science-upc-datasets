# Runbook 08: How the Package Works

## Goal

Explain how the `upc-datasets` package is structured, what it exposes, how it resolves datasets, and how the publication channels are split between package assets and Kaggle datasets.

## High-Level Model

The repository contains two related Python packages:

- `upc_datasets`
  The student-facing public package
- `pachamix_data`
  The lower-level builder and compatibility layer

In practice:

- students should import and run `upc_datasets`
- maintainers can still use the builder functions exposed through `pachamix_data`

The package is intentionally built around `structured parquet datasets`, not raw audio or streaming APIs.

## What The Package Exposes

The public package re-exports a small set of functions from the internal implementation:

- dataset catalog access
- data dictionary rendering
- parquet loading and download helpers
- release asset staging
- dataset builders

The main entrypoint is:

- `src/upc_datasets/__init__.py`

The main CLI entrypoint is:

- `src/upc_datasets/cli.py`

## Main Modules

### `catalog.py`

This file is the contract for the package-facing dataset registry.

It defines, for each dataset:

- canonical dataset name
- local parquet path
- public asset name
- optional legacy asset names
- source metadata
- schema metadata
- publication channel metadata

The catalog is the source of truth for:

- `list_datasets()`
- `list_public_release_datasets()`
- `list_kaggle_datasets()`
- `get_dataset_definition()`
- `get_dataset_asset_name()`
- `get_dataset_asset_names()`

### `loader.py`

This file implements the runtime dataset resolution logic.

It supports three ways to resolve a dataset:

1. local project or processed directory
2. configured cache directory
3. published remote asset URL

Key functions:

- `load_dataset()`
- `download_dataset()`

### `presentation.py`

This file renders the packaged data dictionary in:

- English
- Spanish
- bilingual mode

Key functions:

- `show_dataset_definition()`
- `show_data_dictionary()`

### `release.py`

This file stages local parquet outputs into a folder with the correct published asset names.

Key function:

- `stage_release_assets()`

### `cli.py`

This file maps the package features to the `upc-datasets` command.

It exposes:

- builder commands
- data dictionary commands
- dataset listing commands
- download commands
- release staging commands

## Dataset Resolution Rules

When the package tries to load a dataset, it follows this model.

### Local First

If you pass `root=...`, the package resolves the dataset relative to that root.

Examples:

- project root containing `data/processed/...`
- processed directory itself

If `UPC_DATASETS_ROOT` is set, the package uses that automatically.

### Download When Missing

If the dataset is not found locally and `download=True` is passed, the package attempts to download it.

The remote URL resolution follows this order:

1. per-dataset override environment variable
2. package-wide base URL override
3. default release channel URL

Relevant environment variables:

- `UPC_DATASETS_ROOT`
- `UPC_DATASETS_BASE_URL`
- `UPC_DATASETS_CACHE_DIR`
- `UPC_DATASETS_<DATASET_NAME>_URL`

### Package Channel vs Kaggle Channel

Not every dataset should be distributed through the package release assets.

Current split:

Package release assets:

- `pachamix_audio_core`
- `pachamix_lyrics_long`

Kaggle datasets:

- `pachamix_playlist_events`
- `pachamix_playlist_stats`

Why:

- the small core datasets fit the package-release workflow
- the playlist behavior datasets are materially larger and are better handled by Kaggle

If a user tries to download a Kaggle-routed dataset through the default package channel, the package raises an explicit runtime error telling them to:

- fetch it from Kaggle
- point the package to a local copy with `UPC_DATASETS_ROOT`
- or override the download URL manually

## CLI Mental Model

The CLI is organized around four usage patterns.

### 1. Inspect the package contract

```bash
upc-datasets list-datasets
upc-datasets list-public-datasets
upc-datasets list-kaggle-datasets
upc-datasets show-dataset pachamix_audio_core
upc-datasets show-data-dictionary --format text --language bilingual
```

### 2. Load small published datasets

```bash
upc-datasets download pachamix_audio_core
```

or in Python:

```python
import upc_datasets

frame = upc_datasets.load_dataset("pachamix_audio_core", download=True)
```

### 3. Build datasets from raw inputs

```bash
upc-datasets build-audio-core ...
upc-datasets build-lyrics-core ...
upc-datasets build-playlist-events ...
upc-datasets build-song-graph ...
upc-datasets build-course-dataset ...
```

### 4. Prepare publication assets

```bash
upc-datasets stage-release-assets --root . --output-dir dist/release-assets
```

By default this stages only the datasets intended for the package release asset channel.

If you need a non-default staging flow, pass explicit dataset names:

```bash
upc-datasets stage-release-assets \
  --root . \
  --output-dir dist/custom-assets \
  --dataset-name pachamix_playlist_events \
  --dataset-name pachamix_playlist_stats \
  --no-legacy-aliases
```

## Python Usage Model

The package has two main usage styles.

### Metadata-first usage

This is useful for teaching, notebooks, and student orientation.

```python
import upc_datasets

print(upc_datasets.list_datasets())
print(upc_datasets.get_dataset_definition("pachamix_lyrics_long"))
print(upc_datasets.show_data_dictionary(language="bilingual"))
```

### Data-loading usage

This is useful for assignments and experiments.

```python
import upc_datasets

audio = upc_datasets.load_dataset("pachamix_audio_core", download=True)
lyrics = upc_datasets.load_dataset("pachamix_lyrics_long", download=True, lazy=True)
```

## Builder Layer

The package still exposes builder functions because maintainers may want one import surface for:

- building datasets
- loading datasets
- reading the data dictionary

That means these builder functions remain available from `upc_datasets`:

- `build_audio_core`
- `build_lyrics_core`
- `build_playlist_events`
- `build_song_graph`
- `build_course_dataset`

This is convenient operationally, but conceptually they are maintainership tools, not student download APIs.

## Release Model

The release model now has two channels.

### Channel 1: Python package + GitHub release assets

Used for:

- `upc-datasets` on PyPI
- small parquet assets attached to GitHub Releases

This channel is for:

- package code
- `pachamix_audio_core.parquet`
- `pachamix_lyrics_long.parquet`

### Channel 2: Kaggle dataset publication

Used for:

- large playlist behavior outputs

This channel is for:

- `pachamix_playlist_events.parquet`
- `pachamix_playlist_stats.parquet`

## Typical Maintainer Flow

1. Update code, tests, and catalog metadata.
2. Build or refresh the local parquet outputs.
3. Run tests and package validation.
4. Stage small assets for the package release channel.
5. Publish large playlist datasets to Kaggle.
6. Publish the package to PyPI.

## Typical Student Flow

1. Install `upc-datasets`.
2. Inspect available datasets and their schema.
3. Download or load the small published package datasets.
4. For large playlist datasets, use the Kaggle publication or a local instructor-provided copy.

## Where To Read Next

- `README.md`
  Public package overview and examples
- `runbooks/03-build-course-datasets.md`
  End-to-end local dataset construction
- `runbooks/06-playlist2vec-prep.md`
  Playlist2vec acquisition and export preparation
- `runbooks/07-package-and-publish.md`
  Publication workflow
