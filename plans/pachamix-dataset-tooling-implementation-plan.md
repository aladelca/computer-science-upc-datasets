# PachaMix Dataset Tooling Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use core-executing-plans to implement this plan task-by-task.

**Goal:** Build a tested Python toolkit that generates structured course datasets for PachaMix from public metadata, audio-feature, lyric, and playlist sources without relying on mp3 files.

**Architecture:** The toolkit will be a small Python package under `src/` with dataset-specific builders for FMA audio metadata/features, musiXmatch lyrics, MPD playlist events, and MPD-derived song graphs. The implementation will be `polars`-first for structured data processing and parquet outputs, with a simple CLI entrypoint and test fixtures covering each builder on small synthetic samples.

**Reasoning:** The course requirement emphasizes structured data and lyrics rather than raw audio files, so the implementation will center on metadata tables, sparse text features, and playlist interactions. `pyspark` was considered, but the current local environment cannot launch Spark because the installed Java runtime is too old for Spark 4.1, so the practical working choice is `polars` plus `pyarrow`.

**Tech Stack:** Python 3.11, polars, pyarrow, pytest

---

### Task 1: Scaffold the project and lock the execution path

**Files:**
- Create: `pyproject.toml`
- Create: `README.md`
- Create: `src/pachamix_data/__init__.py`
- Create: `src/pachamix_data/cli.py`
- Create: `tests/test_cli.py`

**Step 1: Write the failing test**

Add `tests/test_cli.py` covering:
- package import
- CLI help output
- builder list output

**Step 2: Run test to verify it fails**

Command:

```bash
pytest tests/test_cli.py
```

Expected outcome:
- tests fail because package and CLI do not exist yet

**Step 3: Write minimal implementation**

Implement:
- package scaffold
- CLI with `--help`
- subcommands or a builder listing command
- basic README with source list and runtime note about Spark being blocked locally

**Step 4: Run test to verify it passes**

Command:

```bash
pytest tests/test_cli.py
```

**Step 5: Verification evidence**

- CLI test passes
- `python3 -m pachamix_data.cli --help` works

---

### Task 2: Implement the FMA audio-core builder

**Files:**
- Create: `src/pachamix_data/builders/__init__.py`
- Create: `src/pachamix_data/builders/audio_core.py`
- Create: `tests/fixtures/fma/tracks.csv`
- Create: `tests/fixtures/fma/features.csv`
- Create: `tests/test_audio_core_builder.py`

**Step 1: Write the failing test**

Add tests that verify:
- FMA tracks and features are joined by `track_id`
- only structured metadata and numeric feature columns are retained
- parquet output is created
- unsupported file shapes fail clearly

**Step 2: Run test to verify it fails**

Command:

```bash
pytest tests/test_audio_core_builder.py
```

Expected outcome:
- tests fail because builder does not exist yet

**Step 3: Write minimal implementation**

Implement an FMA builder that:
- loads `tracks.csv`
- loads `features.csv`
- flattens multi-index feature columns
- selects stable metadata columns
- joins tables by `track_id`
- writes parquet output

**Step 4: Run test to verify it passes**

Command:

```bash
pytest tests/test_audio_core_builder.py
```

**Step 5: Verification evidence**

- builder test passes
- output parquet schema matches expected core columns

---

### Task 3: Implement the lyrics builder for structured lyric features

**Files:**
- Create: `src/pachamix_data/builders/lyrics_core.py`
- Create: `tests/fixtures/lyrics/musixmatch_sample.txt`
- Create: `tests/test_lyrics_builder.py`
- Modify: `README.md`
- Modify: `big_data_dataset_generation_plan.md`

**Step 1: Write the failing test**

Add tests that verify:
- lyric input is parsed into structured rows
- token filtering works
- per-track sparse-like aggregated feature rows are produced
- parquet output is created

**Step 2: Run test to verify it fails**

Command:

```bash
pytest tests/test_lyrics_builder.py
```

Expected outcome:
- tests fail because builder does not exist yet

**Step 3: Write minimal implementation**

Implement a lyrics builder that:
- reads a simple musiXmatch-style text sample
- parses track ids and token counts into structured rows
- supports top-N token filtering
- writes tidy parquet outputs for downstream TF-IDF or sparse processing

Update documentation so the source provenance and licensing rationale are explicit.

**Step 4: Run test to verify it passes**

Command:

```bash
pytest tests/test_lyrics_builder.py
```

**Step 5: Verification evidence**

- lyrics builder test passes
- source documentation clearly distinguishes lyrics data from raw scraped lyrics

---

### Task 4: Implement the MPD playlist-events builder

**Files:**
- Create: `src/pachamix_data/builders/playlist_events.py`
- Create: `tests/fixtures/mpd/sample_playlists.json`
- Create: `tests/test_playlist_builder.py`

**Step 1: Write the failing test**

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_playlist_builder.py
```

**Step 3: Write minimal implementation**

Build a parser that:
- reads MPD playlist JSON
- explodes track rows into one row per `(playlist_id, track_uri)`
- computes basic popularity summaries

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_playlist_builder.py
```

**Step 5: Verification evidence**

- playlist builder produces stable event rows and summary tables

---

### Task 5: Implement the song-graph builder

**Files:**
- Create: `src/pachamix_data/builders/song_graph.py`
- Create: `tests/test_song_graph_builder.py`

**Step 1: Write the failing test**

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_song_graph_builder.py
```

**Step 3: Write minimal implementation**

Build a graph generator that:
- reads playlist events
- creates weighted song-song co-occurrence edges
- supports full co-occurrence mode
- writes edge parquet output

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_song_graph_builder.py
```

**Step 5: Verification evidence**

- graph builder outputs expected weighted edges from sample playlists

---

### Task 6: Add integration documentation and end-to-end verification

**Files:**
- Modify: `README.md`
- Modify: `big_data_14_week_plan.md`
- Modify: `big_data_dataset_generation_plan.md`
- Create: `tests/test_end_to_end_generation.py`

**Step 1: Write the failing test**

Add an integration test that:
- runs the FMA and lyrics builders on sample fixtures
- verifies output files exist and contain expected record counts

**Step 2: Run test to verify it fails**

Command:

```bash
pytest tests/test_end_to_end_generation.py
```

**Step 3: Write minimal implementation**

Wire the builder APIs and CLI commands so the sample end-to-end flow works from a clean temp directory.

**Step 4: Run test to verify it passes**

Command:

```bash
pytest tests/test_end_to_end_generation.py
pytest
```

**Step 5: Verification evidence**

- integration test passes
- full pytest suite passes
- README contains reproducible commands and source documentation

---

## Stop Conditions

- If `polars` cannot be installed or imported, stop and switch to a documented `pyarrow`-only fallback plan.
- If any test fails for an unexpected reason, stop and report before proceeding to later tasks.
- If source formats differ materially from the documented assumptions, update the builder interface and source documentation before continuing.
- Do not add mp3 or waveform processing anywhere in scope.

## Verification Commands

Primary:

```bash
pytest
```

Targeted:

```bash
pytest tests/test_cli.py
pytest tests/test_audio_core_builder.py
pytest tests/test_lyrics_builder.py
pytest tests/test_playlist_builder.py
pytest tests/test_song_graph_builder.py
pytest tests/test_end_to_end_generation.py
```

CLI sanity:

```bash
python3 -m pachamix_data.cli --help
```

## Completion Criteria

- A working Python package exists under `src/pachamix_data/`
- FMA, lyrics, playlist, and graph builders are implemented
- Tests are written red-first and pass green after implementation
- Documentation clearly cites dataset sources and explains why the course avoids raw mp3 pipelines
- Outputs are structured parquet datasets suitable for teaching structured data, lyrics, recommendation, and graph analytics

---

### Task 7: Support official musiXmatch and multi-file MPD inputs

**Files:**
- Modify: `src/pachamix_data/builders/lyrics_core.py`
- Modify: `src/pachamix_data/builders/playlist_events.py`
- Create: `tests/fixtures/lyrics/mxm_dataset_train.txt`
- Create: `tests/fixtures/lyrics/mxm_dataset_test.txt`
- Create: `tests/fixtures/mpd/slices/sample_slice_0.json`
- Create: `tests/fixtures/mpd/slices/sample_slice_1.json`
- Create: `tests/test_lyrics_official_format.py`
- Create: `tests/test_playlist_directory_builder.py`

**Step 1: Write the failing tests**

Add tests that verify:
- the lyrics builder can parse official `musiXmatch/MSD` bag-of-words text files
- multiple lyrics files can be merged in one build
- the playlist builder can ingest a directory of MPD JSON slices

**Step 2: Run tests to verify they fail**

Command:

```bash
pytest tests/test_lyrics_official_format.py tests/test_playlist_directory_builder.py
```

**Step 3: Write minimal implementation**

Implement:
- official musiXmatch parser for `%word1,...` plus `TID,MXMID,idx:cnt,...`
- support for multiple lyrics files or lyrics directories
- support for a directory of MPD JSON files

**Step 4: Run tests to verify they pass**

Command:

```bash
pytest tests/test_lyrics_official_format.py tests/test_playlist_directory_builder.py
```

**Step 5: Verification evidence**

- official-format lyrics parsing works
- directory-based MPD ingestion works

---

### Task 8: Add one-command course dataset orchestration

**Files:**
- Create: `src/pachamix_data/pipeline.py`
- Modify: `src/pachamix_data/cli.py`
- Create: `Makefile`
- Create: `tests/test_course_dataset_pipeline.py`
- Modify: `README.md`
- Modify: `big_data_dataset_generation_plan.md`
- Modify: `runbooks/03-build-course-datasets.md`

**Step 1: Write the failing test**

Add a test that verifies one command can:
- build audio-core
- build lyrics-core
- build playlist events
- build the song graph

from a single `raw-root`.

**Step 2: Run test to verify it fails**

Command:

```bash
pytest tests/test_course_dataset_pipeline.py
```

**Step 3: Write minimal implementation**

Implement:
- `build-course-dataset` CLI command
- a small orchestration layer that discovers expected raw inputs
- a `Makefile` target for one-command execution

**Step 4: Run test to verify it passes**

Command:

```bash
pytest tests/test_course_dataset_pipeline.py
pytest
```

**Step 5: Verification evidence**

- one-command build works on fixtures
- README and runbooks document the exact one-command workflow

---

### Task 9: Make playlist-behavior ingestion Playlist2vec-first

**Files:**
- Modify: `src/pachamix_data/builders/playlist_events.py`
- Modify: `src/pachamix_data/pipeline.py`
- Modify: `src/pachamix_data/cli.py`
- Create: `tests/fixtures/playlist2vec/playlist.csv`
- Create: `tests/fixtures/playlist2vec/track.csv`
- Create: `tests/fixtures/playlist2vec/track_playlist1.csv`
- Create: `tests/test_playlist2vec_builder.py`
- Create: `tests/test_course_dataset_pipeline_playlist2vec.py`
- Modify: `README.md`
- Modify: `big_data_dataset_generation_plan.md`
- Modify: `big_data_14_week_plan.md`
- Modify: `runbooks/03-build-course-datasets.md`
- Modify: `runbooks/05-troubleshooting.md`

**Step 1: Write the failing tests**

Add tests that verify:
- playlist events can be built from exported `Playlist2vec` tables
- the course pipeline can run from `FMA + musiXmatch/MSD + Playlist2vec`

**Step 2: Run tests to verify they fail**

Command:

```bash
pytest tests/test_playlist2vec_builder.py tests/test_course_dataset_pipeline_playlist2vec.py
```

**Step 3: Write minimal implementation**

Implement:
- playlist-behavior ingestion from `playlist.csv`, `track.csv`, and `track_playlist1.csv`
- pipeline source discovery that prefers `playlist2vec/` and treats `mpd/` as optional
- documentation that explains `Playlist2vec` is the current practical unblocker and `MPD` may require separate access

**Step 4: Run tests to verify they pass**

Command:

```bash
pytest tests/test_playlist2vec_builder.py tests/test_course_dataset_pipeline_playlist2vec.py
pytest
```

**Step 5: Verification evidence**

- playlist-behavior build works without MPD
- one-command course build works with Playlist2vec fixtures
