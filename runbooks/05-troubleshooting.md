# Runbook 05: Troubleshooting

## Problem: `pachamix_data` Cannot Be Imported

Cause:

- the virtual environment is not set up
- the editable install was not run

Fix:

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
```

## Problem: `polars` Is Missing

Cause:

- dependencies were not installed into `.venv`

Fix:

```bash
.venv/bin/pip install -e '.[dev]'
```

## Problem: Spark Does Not Start

Cause:

- local Java runtime is too old for the installed Spark version

What to do:

- use the verified `polars` workflow in this workspace
- do not block the course dataset generation on Spark

## Problem: The Builder Expects Structured Inputs but I Only Have Raw Audio Files

Cause:

- the toolkit is not designed for raw media processing

What to do:

- convert your workflow to metadata and feature tables first
- do not attempt to feed mp3 files to these builders

## Problem: Lyrics Input Format Fails

Cause:

- the current lyrics builder expects `track_id,token:count,token:count,...`

Fix:

- normalize the source export before running the builder
- make sure every token/count pair uses the `token:count` format

## Problem: Playlist Graph Looks Too Dense

Cause:

- full co-occurrence graph generation creates many edges for long playlists

What to do:

- filter long playlists before graph creation
- create a smaller classroom subset first
- add a sliding-window graph variant later if needed

## Problem: I Do Not Have MPD Access

Cause:

- the historical Spotify challenge distribution is no longer openly downloadable

What to do:

- use `Playlist2vec` exports instead
- place them under:

```text
data/raw/playlist2vec/
  playlist.csv
  track.csv
  track_playlist1.csv
```

- rerun the one-command build

## Problem: Outputs Were Written but Look Wrong

What to check:

- source file paths
- identifier columns
- token filtering threshold
- whether the wrong raw dataset slice was used

## Recovery Path

When in doubt:

1. rerun [02-run-sample-data.md](./02-run-sample-data.md)
2. run [04-test-and-verify.md](./04-test-and-verify.md)
3. compare your real input files with the expected structured formats
