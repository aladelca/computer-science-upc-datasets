# Runbook 06: Prepare Playlist2vec Exports

## Goal

Prepare the `Playlist2vec` dataset so it can be consumed by the local `pachamix_data` toolkit.

The toolkit does **not** read the raw SQL dump directly. It expects exported structured tables:

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

## Practical Workflow

### Step 1: Download the Playlist2vec SQL dump

Download the dataset from Zenodo and save it locally.

### Step 2: Load it into MySQL or MariaDB

Example:

```bash
mysql -u root -p -e "CREATE DATABASE playlist2vec;"
mysql -u root -p playlist2vec < playlist2vec.sql
```

The exact dump filename may vary depending on the downloaded archive.

### Step 3: Export the required tables

You need:

- `playlist`
- `track`
- `track_playlist1`

How you export them depends on your environment:

- DBeaver table export
- MySQL Workbench export
- `SELECT ... INTO OUTFILE` if your MySQL permissions allow it
- command-line export using `mysql` plus shell redirection

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
- `position`

## Notes

- If your export uses slightly different column names, the toolkit will need a small adapter update.
- `Playlist2vec` is now the preferred public workaround when `MPD` access is unavailable.
- If you already have `MPD`, the toolkit still supports it.
