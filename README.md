# UPC Datasets

This workspace contains a small Python toolkit for generating structured teaching datasets for the `PachaMix` course narrative.

The implementation is designed around:

- structured tables
- metadata
- audio-feature tables
- lyrics-derived features
- playlist interactions
- parquet outputs

It intentionally avoids:

- raw mp3 processing
- waveform pipelines
- dependence on live Spotify audio-feature endpoints

## Data Sources

- `FMA` for metadata and audio features
- `musiXmatch/MSD` for lyrics-derived features
- `Playlist2vec` table exports for playlist interactions and graph construction
- optional `Spotify MPD` support when access is already available

Official source references:

- `FMA`: https://github.com/mdeff/fma
- `musiXmatch/MSD`: https://millionsongdataset.com/musixmatch/
- `Playlist2vec`: https://zenodo.org/records/5002584
- `Spotify MPD`: https://research.atspotify.com/2020/9/the-million-playlist-dataset-remastered

The codebase is intentionally focused on `structured data`, not raw media. That means:

- no mp3 decoding
- no spectrogram generation
- no waveform feature extraction inside the course toolkit

Instead, the builders assume the inputs are already in the form of:

- csv metadata tables
- csv feature tables
- lyric token-count text exports
- playlist membership tables or json playlist metadata

Detailed source notes are documented in [big_data_dataset_generation_plan.md](./big_data_dataset_generation_plan.md).

The processed schema reference is documented in [data_dictionary.md](./data_dictionary.md).

The student-oriented quickstart is documented in [STUDENT_GUIDE.md](./STUDENT_GUIDE.md).

Operational instructions are documented in [runbooks/README.md](./runbooks/README.md).

## Runtime Note

`pyspark` was evaluated for large-scale processing, but the current local environment cannot launch Spark because the installed Java runtime is older than the version required by Spark `4.1`. For that reason, the working implementation uses `polars` plus `pyarrow`.

## Quick Start

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/python -m upc_datasets.cli --help
.venv/bin/pytest
```

## Student Package

The distribution name is `upc-datasets`.

If you want the shortest student path, read [STUDENT_GUIDE.md](./STUDENT_GUIDE.md).

Local development install:

```bash
pip install -e .
```

Student install after publishing to PyPI:

```bash
pip install upc-datasets
```

Python usage:

```python
import upc_datasets

print(upc_datasets.list_datasets())
lyrics = upc_datasets.get_dataset_definition("pachamix_lyrics_long")
print(lyrics["grain"])
```

CLI usage:

```bash
upc-datasets list-datasets
upc-datasets show-dataset pachamix_lyrics_long
upc-datasets show-dataset pachamix_lyrics_long --format json
upc-datasets show-data-dictionary
```

## One-Command Course Build

If your raw data is arranged under `data/raw/` like this:

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

then build the core course dataset with:

```bash
.venv/bin/python -m upc_datasets.cli build-course-dataset \
  --raw-root data/raw \
  --processed-root data/processed
```

or:

```bash
make build-course-dataset RAW_ROOT=data/raw PROCESSED_ROOT=data/processed
```

This always builds:

- `data/processed/pachamix_audio_core.parquet`
- `data/processed/pachamix_lyrics_long.parquet`

When `data/raw/msd/track_metadata.db` is present, the lyrics dataset is enriched with MSD metadata columns such as:

- `title`
- `song_id`
- `release`
- `artist_id`
- `artist_mbid`
- `artist_name`
- `duration`
- `artist_familiarity`
- `artist_hotttnesss`
- `year`
- `track_7digitalid`
- `shs_perf`
- `shs_work`

If you also want recommendation and graph data, add one of these optional behavior sources.

`Playlist2vec`:

```text
data/raw/playlist2vec/
  playlist.csv
  track.csv
  track_playlist1.csv
```

Official `MPD`:

```text
data/raw/mpd/
  *.json
```

When either optional source is present, the same one-command build also writes:

- `data/processed/pachamix_playlists/playlist_events.parquet`
- `data/processed/pachamix_song_graph_edges.parquet`

When both are present, the pipeline prefers `playlist2vec/`.

## Example Commands

```bash
.venv/bin/python -m upc_datasets.cli build-audio-core \
  --tracks-csv data/raw/fma/tracks.csv \
  --features-csv data/raw/fma/features.csv \
  --output-parquet data/processed/pachamix_audio_core.parquet

.venv/bin/python -m upc_datasets.cli build-lyrics-core \
  --lyrics-txt data/raw/musixmatch_msd \
  --output-parquet data/processed/pachamix_lyrics_long.parquet \
  --metadata-db data/raw/msd/track_metadata.db

.venv/bin/python -m upc_datasets.cli build-playlist-events \
  --mpd-json data/raw/playlist2vec \
  --output-dir data/processed/pachamix_playlists

.venv/bin/python -m upc_datasets.cli build-song-graph \
  --playlist-events-parquet data/processed/pachamix_playlists/playlist_events.parquet \
  --output-parquet data/processed/pachamix_song_graph_edges.parquet
```
