# Runbook 04: Test and Verify

## Goal

Confirm that the toolkit and its builder flows are working correctly.

## Run the Full Test Suite

```bash
.venv/bin/ruff format --check src tests scripts
.venv/bin/ruff check src tests scripts
.venv/bin/mypy src
.venv/bin/pytest
```

## Run Targeted Tests

```bash
.venv/bin/pytest tests/test_cli.py
.venv/bin/pytest tests/test_audio_core_builder.py
.venv/bin/pytest tests/test_lyrics_builder.py
.venv/bin/pytest tests/test_playlist_builder.py
.venv/bin/pytest tests/test_song_graph_builder.py
.venv/bin/pytest tests/test_end_to_end_generation.py
```

## Verify the CLI

```bash
.venv/bin/python -m pachamix_data.cli --help
.venv/bin/python -m pachamix_data.cli list-builders
```

## Verify the Outputs

Check that parquet files exist after each build:

- audio-core output exists
- lyrics output exists
- playlist outputs exist
- song graph output exists

## Suggested Manual Sanity Checks

### Audio-Core

- confirm `track_id` exists
- confirm metadata columns are present
- confirm audio feature columns are numeric

### Lyrics

- confirm the output has `msd_track_id`, `token`, and `count`
- confirm there can be multiple rows per track
- confirm counts are positive and sorted sensibly by track/token

### Playlist Events

- confirm one row per `(playlist_id, track_uri, position)`
- confirm `position_observed` exists
- confirm `position_observed=true` for `MPD`
- confirm `position_observed=false` when `Playlist2vec` exports did not include real order
- confirm playlist counts and popularity summaries look reasonable

### Song Graph

- confirm edge weights are positive
- confirm no self-loops are present in the default output

## Expected Current Status

At the time of this runbook update, the verified baseline is:

- full `pytest` passes
- CLI help works
- end-to-end sample generation works
