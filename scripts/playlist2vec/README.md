# Playlist2vec Export Helpers

## Purpose

These helpers support the real acquisition workflow for the official `Playlist2vec` SQL dump from Zenodo.

They are designed to produce the three CSV files consumed by this repository:

- `playlist.csv`
- `track.csv`
- `track_playlist1.csv`

## Download

```bash
bash scripts/playlist2vec/download_playlist2vec.sh ~/datasets/playlist2vec
```

This downloads:

- `spotifydbdumpschemashare.sql`
- `spotifydbdumpshare.sql`

## Load the dump

```bash
mysql -u root -p -e "CREATE DATABASE playlist2vec;"
mysql -u root -p playlist2vec < ~/datasets/playlist2vec/spotifydbdumpshare.sql
```

If you do not want to install MySQL locally, use the repo's SQLite fallback instead:

```bash
.venv/bin/python -m pachamix_data.cli extract-playlist2vec-sql \
  --sql-dump ~/datasets/playlist2vec/spotifydbdumpshare.sql \
  --output-dir data/raw/playlist2vec \
  --sqlite-db data/interim/playlist2vec.sqlite \
  --processed-root data/processed
```

## Export strategy

Use the SQL files in this folder from your preferred SQL client or from `mysql`.

Recommended outputs:

- `data/raw/playlist2vec/playlist.csv`
- `data/raw/playlist2vec/track.csv`
- `data/raw/playlist2vec/track_playlist1.csv`

The SQLite fallback above produces these files directly and can also build the parquet behavior layer in one step.

For full-scale Playlist2vec exports, the in-memory Python builder may not be the right execution path.
This repo therefore also includes a DuckDB-based behavior builder:

```bash
.venv/bin/python scripts/playlist2vec/build_behavior_duckdb.py \
  --raw-playlist2vec-dir data/raw/playlist2vec \
  --output-dir data/processed/pachamix_playlists \
  --db-path data/interim/playlist2vec_behavior.duckdb \
  --temp-dir data/interim/duckdb_tmp
```

It writes:

- `playlist_events.parquet`
- `playlist_stats.parquet`
- `track_popularity.parquet`

## Important note about `position`

The official `Playlist2vec` schema documents `track_playlist1` as a track-playlist association table and does not provide observed playlist order.

Therefore:

- `export_track_playlist1.sql` exports only:
  - `playlist_id`
  - `track_id`
- the repo builder will synthesize a deterministic per-playlist `position`
- the resulting parquet output will mark:
  - `position_observed = false`

This is valid for:

- collaborative filtering
- popularity baselines
- matrix factorization
- graph construction

It is not equivalent to a real ordered playlist sequence.
