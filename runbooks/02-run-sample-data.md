# Runbook 02: Run the Sample Data

## Goal

Run the toolkit against the included fixture files to confirm that everything works end to end before touching real datasets.

## Step 1: Make Sure Setup Is Complete

Follow [01-setup.md](./01-setup.md) first.

## Step 2: Build the Audio-Core Fixture

```bash
.venv/bin/python -m pachamix_data.cli build-audio-core \
  --tracks-csv tests/fixtures/fma/tracks.csv \
  --features-csv tests/fixtures/fma/features.csv \
  --output-parquet tmp/audio_core.parquet
```

## Step 3: Build the Lyrics Fixture

```bash
.venv/bin/python -m pachamix_data.cli build-lyrics-core \
  --lyrics-txt tests/fixtures/lyrics/musixmatch_sample.txt \
  --output-parquet tmp/lyrics_core.parquet
```

## Step 4: Build Playlist Events

```bash
.venv/bin/python -m pachamix_data.cli build-playlist-events \
  --mpd-json tests/fixtures/mpd/sample_playlists.json \
  --output-dir tmp/playlist_outputs
```

## Step 5: Build the Song Graph

```bash
.venv/bin/python -m pachamix_data.cli build-song-graph \
  --playlist-events-parquet tmp/playlist_outputs/playlist_events.parquet \
  --output-parquet tmp/song_graph.parquet
```

## Expected Outputs

```text
tmp/
  audio_core.parquet
  lyrics_core.parquet
  playlist_outputs/
    playlist_events.parquet
    playlist_stats.parquet
    track_popularity.parquet
  song_graph.parquet
```

## What This Proves

- the package imports correctly
- the CLI is wired correctly
- parquet outputs are generated
- the builder interfaces are functioning end to end
