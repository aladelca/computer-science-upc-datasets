# Runbook 06: Prepare Playlist2vec Exports

## Goal

Prepare the `Playlist2vec` dataset so it can be consumed by the local `pachamix_data` toolkit.

The playlist builder expects exported structured tables:

- `playlist.csv`
- `track.csv`
- `track_playlist1.csv`

These files should be placed under:

```text
data/raw/playlist2vec/
```

## Source

Official public source:

- [Playlist2vec on Zenodo](https://zenodo.org/records/5002584)

Official files on Zenodo:

- `spotifydbdumpschemashare.sql`
- `spotifydbdumpshare.sql`

Important source fact:

- the official `track_playlist1` schema on Zenodo contains:
  - `track_id`
  - `playlist_id`
- it does **not** document an observed `position` column
- in the real Playlist2vec dump, `playlist.id` is a string identifier, not a numeric MPD-style PID

## Practical Workflow

### Step 1: Download the Playlist2vec SQL dump

Download the dataset from Zenodo and save it locally.

Recommended helper:

```bash
bash scripts/playlist2vec/download_playlist2vec.sh ~/datasets/playlist2vec
```

Manual alternative:

```bash
mkdir -p ~/datasets/playlist2vec
cd ~/datasets/playlist2vec

curl -L "https://zenodo.org/records/5002584/files/spotifydbdumpschemashare.sql?download=1" -o spotifydbdumpschemashare.sql
curl -L "https://zenodo.org/records/5002584/files/spotifydbdumpshare.sql?download=1" -o spotifydbdumpshare.sql
```

### Step 2A: Load it into MySQL or MariaDB

Example:

```bash
mysql -u root -p -e "CREATE DATABASE playlist2vec;"
mysql -u root -p playlist2vec < spotifydbdumpshare.sql
```

The exact dump filename in the official record is `spotifydbdumpshare.sql`.

### Step 2B: MySQL-free fallback with SQLite

If you do not have MySQL or MariaDB installed, use the repo extractor:

```bash
.venv/bin/python -m pachamix_data.cli extract-playlist2vec-sql \
  --sql-dump ~/datasets/playlist2vec/spotifydbdumpshare.sql \
  --output-dir data/raw/playlist2vec \
  --sqlite-db data/interim/playlist2vec.sqlite \
  --processed-root data/processed
```

This command:

- loads the relevant tables into SQLite
- exports `playlist.csv`, `track.csv`, and `track_playlist1.csv`

If you use this path, you can skip directly to verification.

For real full-scale Playlist2vec exports, build the behavior parquets with DuckDB:

```bash
.venv/bin/python scripts/playlist2vec/build_behavior_duckdb.py \
  --raw-playlist2vec-dir data/raw/playlist2vec \
  --output-dir data/processed/pachamix_playlists \
  --db-path data/interim/playlist2vec_behavior.duckdb \
  --temp-dir data/interim/duckdb_tmp
```

This produces:

- `playlist_events.parquet`
- `playlist_stats.parquet`
- `track_popularity.parquet`

### Step 3: Export the required tables manually from MySQL

You need:

- `playlist`
- `track`
- `track_playlist1`

How you export them depends on your environment:

- DBeaver table export
- MySQL Workbench export
- `SELECT ... INTO OUTFILE` if your MySQL permissions allow it
- command-line export using `mysql` plus shell redirection

This repo ships SQL helpers in:

- `scripts/playlist2vec/export_playlist.sql`
- `scripts/playlist2vec/export_track.sql`
- `scripts/playlist2vec/export_track_playlist1.sql`

Recommended export contract:

- `playlist.csv`
  - `playlist_id`
  - `name`
- `track.csv`
  - `track_id`
  - `track_name`
  - `artist_name`
  - `album_name`
- `track_playlist1.csv`
  - `playlist_id`
  - `track_id`

If you already have a trustworthy `position` column from your own export process, you may include it.
The builder will preserve it and mark `position_observed=true`.
If you do not include `position`, the builder will synthesize a deterministic per-playlist order and mark `position_observed=false`.

### Step 4: Save the exports under `data/raw/playlist2vec/`

Expected layout:

```text
data/raw/playlist2vec/
  playlist.csv
  track.csv
  track_playlist1.csv
```

### Step 5: Run the one-command course build

```bash
make build-course-dataset RAW_ROOT=data/raw PROCESSED_ROOT=data/processed LYRICS_TOP_N_TOKENS=0
```

or:

```bash
.venv/bin/python -m pachamix_data.cli build-course-dataset \
  --raw-root data/raw \
  --processed-root data/processed \
  --lyrics-top-n-tokens 0
```

If you used the SQLite fallback in Step 2B with `--processed-root data/processed`, this step is already covered for the playlist and graph outputs.

## Minimum Required Columns

For the toolkit to work as currently implemented, the exports should contain at least:

### `playlist.csv`

- `playlist_id`
- `name`

### `track.csv`

- `track_id`
- `track_name`
- `artist_name`
- `album_name`

### `track_playlist1.csv`

- `playlist_id`
- `track_id`

Optional:

- `position`

The official Zenodo schema does not require `position`.

## Notes

- If your export uses slightly different column names, the toolkit will need a small adapter update.
- `Playlist2vec` is now the preferred public workaround when `MPD` access is unavailable.
- If you already have `MPD`, the toolkit still supports it.
- Treat `Playlist2vec` as a set-based playlist membership source unless you independently recover trustworthy order information.
