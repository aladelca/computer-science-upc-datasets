# PachaMix Dataset Course Viability Analysis

## Question

Is the dataset strategy in this repository good enough to support the whole Big Data course?

## Short Answer

`Yes, conditionally` if the course is taught with a `modular dataset stack`.

`No` if the requirement is:

- one single perfectly unified dataset for all 14 weeks, or
- a fully ready end-to-end semester package in the current workspace state, without further staging work

The correct verdict is:

> `The repository design is academically and pedagogically strong enough for the whole course, but the current staged data state is not yet sufficient for the whole course.`

More precisely:

- `Weeks 1-8`: largely supported by the current core dataset design
- `Weeks 9-12`: only supported after playlist behavior data are staged and processed
- `Weeks 13-14`: conceptually supported, but operationally stronger after the behavior and graph layers exist for real

---

## Basis of This Analysis

This assessment is based on the repository itself:

- `README.md`
- `data_dictionary.md`
- `big_data_dataset_generation_plan.md`
- `runbooks/03-build-course-datasets.md`
- `runbooks/06-playlist2vec-prep.md`
- the implemented builders in `src/pachamix_data/builders/`
- the student-facing dataset catalog and loader in `src/upc_datasets/`
- the existing test suite in `tests/`

Important limitation of the current assessment:

- the workspace currently has `no staged data/ directory`
- the local environment also lacks `.venv` and `pytest`, so the test suite could not be executed in this session
- therefore, the analysis distinguishes between:
  - `documented design`
  - `implemented support`
  - `currently present artifacts in this workspace`

---

## Observed Current State

## 1. What is actually present right now

In the working tree, there is:

- code for building the datasets
- documentation and runbooks
- tests and fixtures
- the weekly course content package

There is `not` currently a `data/` directory in the workspace root.

That means:

- no locally staged raw FMA data
- no locally staged musiXmatch/MSD raw data
- no locally staged Playlist2vec or MPD behavior data
- no locally staged processed parquet outputs

So, in the literal current workspace state, the answer is:

> `No, the dataset is not currently ready to run the entire course here and now.`

This is an operational statement, not a design statement.

## 2. What the docs claim is available as of the repo design

According to `data_dictionary.md`, the currently generated real outputs are:

- `pachamix_audio_core.parquet`
- `pachamix_lyrics_long.parquet`

and the following remain optional / not generated yet:

- `pachamix_playlists/playlist_events.parquet`
- `pachamix_playlists/playlist_stats.parquet`
- `pachamix_playlists/track_popularity.parquet`
- `pachamix_song_graph_edges.parquet`

This is the single most important fact for course viability.

It means:

- the `audio` and `lyrics` layers are present in the design and are documented as real outputs
- the `behavior` and `graph` layers are implemented in code but not yet staged as real course artifacts

---

## Executive Verdict

## Final verdict in one line

> `The dataset stack is good enough for the whole course only if you keep it modular and complete the optional behavior and graph layers before teaching Weeks 9-12.`

## Verdict by interpretation

| Interpretation of "the dataset" | Verdict |
| --- | --- |
| One single universal merged table for the whole semester | `No` |
| Modular family of course datasets, each used where mathematically appropriate | `Yes` |
| Current workspace state, without staging raw data and building outputs | `No` |
| Full 14-week course after generating audio, lyrics, playlist, and graph outputs | `Yes, conditionally` |

---

## Why the Modular Design Is Pedagogically Strong

The repository makes a correct strategic decision:

- `FMA` for audio-space methods
- `musiXmatch/MSD` for lyric-space methods
- `Playlist2vec` or `MPD` for behavioral recommendation and graph construction

This is better than forcing one fragile mega-table because:

- the raw sources come from different catalogs
- the identifiers do not naturally align
- the licenses and data-access conditions differ
- the course topics themselves do not require one single joined schema

Pedagogically, this is a strength.
It lets each method operate on a data representation that fits the mathematics of the week.

That is exactly what a rigorous Big Data course should do.

---

## Dataset-by-Dataset Assessment

## A. `pachamix_audio_core`

### What it is

- source family: `FMA`
- grain: one row per track
- documented shape: `106,574 x 522`
- practical role: audio descriptors plus lightweight metadata

### Why it is strong

This is the strongest single dataset in the repository for course use.

It is well suited for:

- Week 1: data audit, schema reasoning, memory and complexity
- Week 2: supervised versus unsupervised framing
- Week 3: curse of dimensionality
- Week 4: PCA
- Week 5: SVD and dimensionality reduction comparisons
- Week 6: K-means
- Week 7: DBSCAN
- part of Week 8: audio-based content recommendation

### Mathematical adequacy

It is strong mathematically because:

- it is already numeric
- it has enough dimension (`518` numeric features) to justify PCA, SVD, clustering, and high-dimensional geometry
- it includes metadata columns such as `genre_top` for weak interpretability and proxy supervised tasks

### Operational adequacy

The numeric block is large enough to feel real, but still manageable with:

- sampling
- subsets
- PCA-reduced workflows
- Colab or laptop-friendly slices

This is exactly the right regime for an undergraduate Big Data course.

### Weak points

- `genre_top` is nullable and should not be treated as ground-truth musical ontology
- it is not a user-behavior dataset
- it does not support collaborative filtering directly
- it does not solve the cross-catalog problem for hybrid recommendation

### Verdict

> `Excellent for Weeks 1-7 and useful for the content side of Week 8.`

---

## B. `pachamix_lyrics_long`

### What it is

- source family: `musiXmatch/MSD`
- grain: one row per `(msd_track_id, token)`
- documented shape: `19,045,332 x 16`
- raw content type: long-form token counts, not full lyrics text

### Why it is strong

This dataset is pedagogically strong for:

- text preprocessing
- sparse matrix construction
- TF-IDF
- lyric-space similarity
- text-oriented dimensionality reduction
- content-based recommendation in lyric space

### Mathematical adequacy

It is especially valuable because it exposes students to:

- high-dimensional sparse spaces
- vocabulary filtering
- term weighting
- long-to-wide transformations
- the difference between raw counts and weighted vector spaces

This is highly relevant for Big Data.

### Critical limitation

It does `not` natively join to `pachamix_audio_core`.

This is not a small inconvenience.
It is the central structural limitation of the whole dataset strategy if one insists on unified item-level modeling.

Therefore:

- Week 8 is fine if taught as `parallel content spaces`
- Week 10 hybrid recommendation cannot be treated as a trivial merge

### Operational limitation

The long table is large and not directly classroom-friendly for every lab.
Students should not be expected to use the raw `19M+` row long table interactively in every session.

The correct teaching pattern is:

- filter tokens
- sample tracks
- build a sparse or wide derived matrix for the relevant week

### Verdict

> `Very good for text and lyric-space weeks, but only as a parallel content view, not as a natural join partner for the audio table.`

---

## C. `pachamix_playlist_events`, `pachamix_playlist_stats`, and `pachamix_track_popularity`

### What they are

- source family: `Playlist2vec` exports or `MPD`
- grain:
  - playlist events: one row per `(playlist_id, track_uri, position)`
  - playlist stats: one row per playlist
  - track popularity: one row per track

### Why they matter

These artifacts are the bridge into:

- collaborative filtering
- popularity baselines
- playlist continuation
- graph construction
- part of pipeline / deployment evaluation

Without them, the course loses its behavioral layer.

### Current status

The code supports them.
The tests support them.
But `data_dictionary.md` states that they are `not generated yet`.

### What that means in practice

If these artifacts are not generated before the semester:

- Week 9 becomes blocked
- Week 10 becomes blocked or heavily weakened
- Week 11 cannot be grounded in real course data
- Week 12 cannot be grounded in real course data

This is the biggest readiness gap in the repository right now.

### Builder maturity

The implementation is simple and appropriate:

- `build_playlist_events()` supports both Playlist2vec exports and MPD JSON
- it writes:
  - `playlist_events.parquet`
  - `track_popularity.parquet`
  - `playlist_stats.parquet`
- tests exist for:
  - Playlist2vec ingestion
  - one-command course build
  - preference for Playlist2vec when both sources exist

This is good evidence that the feature is real, not just aspirational documentation.

### Operational friction

However, Playlist2vec preparation is not zero-friction.
The runbook explicitly requires:

- downloading the SQL dump
- loading it into MySQL or MariaDB
- exporting specific tables
- staging them under `data/raw/playlist2vec/`

This is manageable for an instructor.
It is not something to improvise in the middle of the semester.

### Verdict

> `Necessary and sufficient for Weeks 9-10 once staged, but they are currently the largest operational blocker.`

---

## D. `pachamix_song_graph_edges`

### What it is

- derived from playlist events
- grain: one row per undirected song pair
- columns:
  - `src_track_uri`
  - `dst_track_uri`
  - `weight`

### Why it is good

This is the right derived artifact for:

- graph construction
- centrality
- random-walk intuition
- PageRank after directed conversion

The builder is conceptually clean:

- deduplicate playlist-track membership
- self-join by playlist
- keep canonical song pairs
- aggregate co-occurrence count as edge weight

This is mathematically coherent and easy to teach.

### Limitation

The graph is undirected by construction.
That is fine for Week 11.
For Week 12 PageRank, a further modeling step is required:

- expand each undirected edge into two directed edges
- then normalize into a transition matrix

This is not a flaw.
It simply needs to be stated explicitly in the course.

### Readiness dependency

This artifact depends entirely on playlist events existing first.
So it inherits the operational readiness risk of the behavior layer.

### Verdict

> `Good for Weeks 11-12 once the behavior layer exists; unavailable otherwise.`

---

## Week-by-Week Readiness Matrix

| Weeks | Topic | Needed dataset(s) | Readiness | Comment |
| --- | --- | --- | --- | --- |
| 1 | Big Data framing | `pachamix_audio_core` | `Green` | Strong fit |
| 2 | Supervised / unsupervised learning | `pachamix_audio_core` | `Green` | Strong fit |
| 3 | Curse of dimensionality | `pachamix_audio_core`, optional lyric matrix | `Green` | Strong fit |
| 4 | PCA | `pachamix_audio_core` | `Green` | Strong fit |
| 5 | SVD, t-SNE, text-space representation | `pachamix_audio_core`, derived lyric matrix | `Green` | Strong fit with derived lyric views |
| 6 | K-means | `pachamix_audio_core` | `Green` | Strong fit |
| 7 | DBSCAN | `pachamix_audio_core` | `Green` | Strong fit |
| 8 | Content-based recommendation | `pachamix_audio_core`, `pachamix_lyrics_long` | `Amber` | Good if taught as parallel audio and lyric views |
| 9 | Collaborative filtering | behavior layer | `Red` today / `Green` after staging | Blocked until playlist data are built |
| 10 | Hybrid recommendation, matrix factorization | behavior layer, optional matched subset | `Amber` | Matrix factorization is fine; true hybrid needs a matched subset |
| 11 | Graph analytics foundations | `pachamix_song_graph_edges` | `Red` today / `Green` after staging | Depends on playlist events |
| 12 | PageRank | `pachamix_song_graph_edges` | `Red` today / `Green` after staging | Depends on playlist events and graph |
| 13 | Pipelines | all built artifacts | `Amber` | Conceptually fine; stronger with full artifact set |
| 14 | Serving and monitoring | all built artifacts | `Amber` | Conceptually fine; stronger with full artifact set |

---

## Detailed Strengths

## 1. Strong mathematical alignment with the syllabus

The dataset family is well aligned with the course mathematics:

- high-dimensional dense feature matrix for PCA / SVD / clustering
- high-dimensional sparse token structure for TF-IDF and text-space methods
- interaction matrix for collaborative filtering and factorization
- graph layer for Markov chains and PageRank

That is a major strength.

## 2. Avoids legally and operationally fragile dependencies

The repo explicitly avoids relying on:

- Spotify audio-feature endpoints
- raw lyrics scraping
- mp3 decoding and waveform processing in the classroom pipeline

This is a sound course-design decision.

## 3. Builder design is simple and teachable

The code is not overengineered.
Each builder has a clear pedagogical role:

- `build_audio_core`
- `build_lyrics_core`
- `build_playlist_events`
- `build_song_graph`

This is ideal for a teaching repo.

## 4. The student-facing package design is sensible

The `upc_datasets` package provides:

- dataset catalog metadata
- readable data dictionary presentation
- local loading
- optional download path from release assets

That is useful for course distribution.

---

## Detailed Weaknesses and Risks

## 1. No single unified item catalog

This is the biggest conceptual limitation.

There is no native direct key between:

- FMA audio tracks
- MSD / musiXmatch lyric tracks
- playlist-behavior tracks

Consequences:

- Week 8 must be designed carefully
- Week 10 hybrid recommendation cannot be naively operationalized
- any final project that assumes one fully joined table needs additional matching work

This is manageable, but it must be acknowledged explicitly.

## 2. Behavior layer is not staged yet

This is the biggest operational limitation.

Without generated playlist artifacts:

- collaborative filtering is theoretical only
- graph analytics is theoretical only
- PageRank cannot be grounded in the real course dataset

That is unacceptable if the semester is about to begin.

## 3. Recommendation evaluation artifacts are planned, not implemented

The dataset generation plan explicitly recommends:

- `playlist_train.parquet`
- `playlist_test.parquet`
- `candidate_pool.parquet`

and even mentions a possible `build_reco_splits.py`.

But this split builder is not currently implemented in `src/`.

This is not fatal, because the splits can be created in notebooks.
But it is a maturity gap.

## 4. Current workspace has no actual staged data

Even the core datasets are not present in this working tree right now.
So from an operational readiness perspective, the repository is currently:

- `design-ready`
- `code-ready`
- `not yet data-ready`

## 5. Spark path is not currently operational in the local environment

The README explicitly notes that Spark `4.1` cannot run in the current local environment because of the Java runtime mismatch.

This does not break the course, but it means:

- Spark demos are not yet locally turnkey
- the course should rely on `polars` / `pyarrow` locally and reserve Spark for external environments if needed

---

## Is It Good Enough for the Whole Course?

## If you mean "one dataset for every week, with no caveats"

`No.`

The repository does not provide one naturally unified dataset across:

- audio
- lyrics
- behavior
- graph structure

and it should not pretend to.

## If you mean "a coherent family of datasets that supports the whole semester"

`Yes, with conditions.`

Those conditions are:

1. build and stage the behavior layer before Weeks 9-12
2. teach Week 8 as parallel audio-space and lyric-space content recommendation unless a matched subset is created
3. do not build the semester around a perfect cross-catalog join
4. prepare classroom-sized subsets for local, Colab, and graph work
5. explicitly document evaluation splits for recommendation labs

---

## Minimum Actions Required Before Using This for the Full Semester

## Required

1. Stage real raw data under `data/raw/`:
   - `fma/`
   - `musixmatch_msd/`
   - `msd/track_metadata.db`
   - `playlist2vec/` or `mpd/`
2. Run the one-command course build.
3. Confirm the following real outputs exist:
   - `pachamix_audio_core.parquet`
   - `pachamix_lyrics_long.parquet`
   - `pachamix_playlists/playlist_events.parquet`
   - `pachamix_playlists/playlist_stats.parquet`
   - `pachamix_playlists/track_popularity.parquet`
   - `pachamix_song_graph_edges.parquet`
4. Prepare classroom subsets:
   - small
   - medium
   - instructor / large
5. Define recommendation evaluation splits for Week 9-10.

## Strongly recommended

1. Prepare a small matched capstone subset for optional Week 10 / final project enrichment.
2. Publish release assets so students can download prepared parquet files directly.
3. Validate the full pipeline in a clean environment, not only through fixture-based tests.
4. Decide in advance whether Spark is truly needed or whether `polars` plus sampling is sufficient.

---

## Final Recommendation

## Decision

> `Use this dataset strategy for the course, but do not treat the repository as fully semester-ready until the behavior and graph layers are actually generated and packaged.`

## Practical meaning

- `Go` for the course design itself
- `Go` for Weeks 1-8 with the current core dataset strategy
- `No-Go yet` for calling the semester fully ready in operational terms
- `Go after staging` for Weeks 9-14 once playlist and graph artifacts are built and distributed

## Bottom line

The dataset design is `good enough for the whole course as a modular teaching stack`.

The current repository state is `not yet sufficient for the whole course as a ready-to-run packaged dataset`.

That distinction is the correct one, and it should guide the next implementation steps.
