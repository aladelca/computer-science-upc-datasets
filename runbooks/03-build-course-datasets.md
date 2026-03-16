# Runbook 03: Build the Course Datasets

## Goal

Generate the real structured teaching datasets for the course.

## Recommended Raw Sources

- `FMA` for metadata and audio features
- `musiXmatch/MSD` for lyrics token/count data
- optional `Playlist2vec` table exports for playlist events and graph construction
- optional `Spotify MPD` if you already have access

More detail:

- [README.md](../README.md)
- [big_data_dataset_generation_plan.md](../big_data_dataset_generation_plan.md)

## Input Assumptions

The toolkit expects structured inputs only:

- `csv` metadata tables
- `csv` audio feature tables
- text-based lyric token/count exports
- `csv` playlist membership tables or `json` playlist metadata

It does not accept mp3 files.

## Step 1: Build the FMA Audio-Core Dataset

## Fastest Path: One Command

If the raw data is already arranged under:

```text
data/raw/
  fma/
  musixmatch_msd/
  msd/
```

run:

```bash
.venv/bin/python -m pachamix_data.cli build-course-dataset \
  --raw-root data/raw \
  --processed-root data/processed
```

or:

```bash
make build-course-dataset RAW_ROOT=data/raw PROCESSED_ROOT=data/processed
```

This is the recommended workflow.

With `fma/` and `musixmatch_msd/`, the command builds the core structured datasets:

- `pachamix_audio_core.parquet`
- `pachamix_lyrics_long.parquet`

If `msd/track_metadata.db` is also staged, the lyrics dataset is automatically enriched with MSD metadata such as title, artist, release, duration, year, and the remaining columns from the `songs` table.

If you also stage `playlist2vec/` or `mpd/`, the same command adds:

- `pachamix_playlists/playlist_events.parquet`
- `pachamix_song_graph_edges.parquet`

## Manual Path

If you want to run each stage separately, use the commands below.

## Step 1: Build the FMA Audio-Core Dataset

```bash
.venv/bin/python -m pachamix_data.cli build-audio-core \
  --tracks-csv data/raw/fma/tracks.csv \
  --features-csv data/raw/fma/features.csv \
  --output-parquet data/processed/pachamix_audio_core.parquet
```

Recommended use:

- Weeks `1-7`
- exploratory analysis
- dimensionality reduction
- clustering

## Step 2: Build the Lyrics Dataset

```bash
.venv/bin/python -m pachamix_data.cli build-lyrics-core \
  --lyrics-txt data/raw/musixmatch_msd \
  --output-parquet data/processed/pachamix_lyrics_long.parquet \
  --metadata-db data/raw/msd/track_metadata.db
```

Recommended use:

- lyric similarity
- downstream vectorization or TF-IDF that you apply later
- content-based recommendation
- metadata-aware exploration by title, artist, release, and year

## Step 3: Build Playlist Events from Playlist2vec

This step is optional. It is only needed for collaborative filtering, playlist continuation, and graph analytics.

```bash
.venv/bin/python -m pachamix_data.cli build-playlist-events \
  --mpd-json data/raw/playlist2vec \
  --output-dir data/processed/pachamix_playlists
```

Generated outputs:

- `playlist_events.parquet`
- `playlist_stats.parquet`
- `track_popularity.parquet`

Recommended use:

- collaborative filtering
- popularity baselines
- graph input generation

## Optional MPD Path

If you already have `MPD` JSON slices, the same command still works.

Example:

```bash
.venv/bin/python -m pachamix_data.cli build-playlist-events \
  --mpd-json data/raw/mpd \
  --output-dir data/processed/pachamix_playlists
```

In the one-command pipeline, `playlist2vec/` is preferred over `mpd/`.

## Step 4: Build the Song Graph

This step is optional and depends on playlist events.

```bash
.venv/bin/python -m pachamix_data.cli build-song-graph \
  --playlist-events-parquet data/processed/pachamix_playlists/playlist_events.parquet \
  --output-parquet data/processed/pachamix_song_graph_edges.parquet
```

Recommended use:

- graph analytics
- centrality
- PageRank

## Recommended Teaching Output Set

At minimum, prepare:

- `data/processed/pachamix_audio_core.parquet`
- `data/processed/pachamix_lyrics_long.parquet`

Add these when you include a behavior dataset:

- `data/processed/pachamix_playlists/playlist_events.parquet`
- `data/processed/pachamix_song_graph_edges.parquet`

## Suggested Scaling Strategy

Prepare multiple versions:

- `small` for local laptops
- `medium` for Colab
- `large` for instructor demos

For the lyrics data, the default output is the full long-form token table. If you want filtering, use `--top-n-tokens`.
