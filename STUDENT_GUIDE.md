# Student Guide

This guide is the shortest path for students using `upc-datasets`.

## What This Package Gives You

The package gives you:

- a Python API
- a CLI
- a queryable data dictionary
- dataset builders for the course datasets

It does **not** ship the full raw or processed datasets inside the wheel, because those files are too large.

So there are two common student workflows:

1. install the package and query the data dictionary
2. install the package and work with datasets that the professor already generated

## Install

After publication to PyPI:

```bash
pip install upc-datasets
```

For local development from the repo:

```bash
pip install -e .
```

## Python API

### List datasets

```python
import upc_datasets

print(upc_datasets.list_datasets())
```

Expected dataset names include:

- `pachamix_audio_core`
- `pachamix_lyrics_long`
- `pachamix_playlist_events`
- `pachamix_song_graph_edges`

### Query one dataset definition

```python
import upc_datasets

dataset = upc_datasets.get_dataset_definition("pachamix_lyrics_long")
print(dataset["grain"])
print(dataset["columns"])
```

### Get the full data dictionary

```python
import upc_datasets

dictionary = upc_datasets.get_data_dictionary()
print(dictionary.keys())
```

### Load a dataset directly

```python
import upc_datasets

lyrics = upc_datasets.load_dataset(
    "pachamix_lyrics_long",
    root="/path/to/course-project-or-processed-dir",
)
print(lyrics.shape)
```

By default, `load_dataset()` returns a `polars.DataFrame`.

If you prefer lazy execution:

```python
import upc_datasets

lyrics_lazy = upc_datasets.load_dataset("pachamix_lyrics_long", lazy=True)
print(lyrics_lazy.collect_schema())
```

`root=` can point to either:

- the project root that contains `data/processed/`
- the directory that directly contains the parquet files

If you do not want to pass `root=` in every notebook, set:

```bash
export UPC_DATASETS_ROOT=/path/to/course-project-or-processed-dir
```

## CLI

### List datasets

```bash
upc-datasets list-datasets
```

### Show one dataset

```bash
upc-datasets show-dataset pachamix_lyrics_long
```

### Show one dataset as JSON

```bash
upc-datasets show-dataset pachamix_lyrics_long --format json
```

### Show the full dictionary

```bash
upc-datasets show-data-dictionary
```

## Load the Processed Data

If the professor shares the generated parquet files, students can load them directly with `upc_datasets.load_dataset()` or plain `polars`:

```python
import upc_datasets

audio = upc_datasets.load_dataset("pachamix_audio_core")
lyrics = upc_datasets.load_dataset("pachamix_lyrics_long")

print(audio.shape)
print(lyrics.shape)
```

Or directly with `polars`:

```python
import polars as pl

audio = pl.read_parquet("data/processed/pachamix_audio_core.parquet")
lyrics = pl.read_parquet("data/processed/pachamix_lyrics_long.parquet")

print(audio.shape)
print(lyrics.shape)
```

Or with `pandas`:

```python
import pandas as pd

audio = pd.read_parquet("data/processed/pachamix_audio_core.parquet")
lyrics = pd.read_parquet("data/processed/pachamix_lyrics_long.parquet")
```

## What The Main Datasets Mean

### `pachamix_audio_core`

- one row per song in the `FMA` dataset
- includes:
  - `track_id`
  - `title`
  - `genre_top`
  - `artist_name`
  - many numeric audio-feature columns

### `pachamix_lyrics_long`

- one row per `(msd_track_id, token)`
- includes:
  - lyric token counts
  - song title
  - artist name
  - release
  - year
  - other `MSD` metadata when available

Important:

- this dataset does **not** contain full raw lyrics
- it contains structured token/count data from the official `musiXmatch/MSD` release

### `pachamix_playlist_events`

- optional dataset
- one row per song occurrence inside a playlist
- needed for collaborative filtering and playlist-based recommendation

### `pachamix_song_graph_edges`

- optional dataset
- one row per song pair
- edge weight = number of playlists where both songs co-occur
- needed for graph analytics and PageRank

## Typical Student Tasks

### 1. Inspect the dictionary before using a dataset

```python
import upc_datasets

for column in upc_datasets.get_dataset_definition("pachamix_audio_core")["columns"]:
    print(column["name"], column["dtype"])
```

### 2. Build your own text features from lyrics

The package gives you the long-form lyrics table. Students can build:

- bag-of-words
- TF-IDF
- embeddings
- topic models

from:

- `msd_track_id`
- `token`
- `count`

### 3. Explore audio-space geometry

Students can use the audio dataset for:

- PCA
- SVD
- t-SNE
- clustering
- nearest-neighbor search

### 4. Explore graph methods later

If playlist data is available, students can move to:

- co-occurrence graphs
- centrality
- PageRank
- recommendation from behavior

## Build the Datasets Yourself

If you also have the raw sources, you can build the course datasets:

```bash
upc-datasets build-course-dataset \
  --raw-root data/raw \
  --processed-root data/processed
```

Expected raw structure:

```text
data/raw/
  fma/
    tracks.csv
    features.csv
  musixmatch_msd/
    mxm_dataset_train.txt
    mxm_dataset_test.txt
  msd/
    track_metadata.db
```

Optional later sources:

```text
data/raw/playlist2vec/
  playlist.csv
  track.csv
  track_playlist1.csv
```

or:

```text
data/raw/mpd/
  *.json
```

## Recommended Student Imports

```python
import upc_datasets
import polars as pl
```

## Where To Look Next

- Main package overview: [README.md](./README.md)
- Full schema reference: [data_dictionary.md](./data_dictionary.md)
- Operational runbooks: [runbooks/README.md](./runbooks/README.md)
