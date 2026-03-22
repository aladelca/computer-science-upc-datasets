# PachaMix Dataset Generation Plan

## Goal

This document explains how to build the course datasets for `PachaMix`, the semester-long playlist and recommendation narrative used by `Mathias` and `Yunguri`.

The design goal is not to create one perfect universal music table. The design goal is to create a `feasible`, `public`, and `pedagogically coherent` dataset stack that supports:

- Big Data framing
- dimensionality reduction
- clustering
- content-based recommendation
- collaborative filtering
- graph analytics
- deployment exercises

The recommended approach is `modular`.

Use:

- `FMA` for audio and metadata
- `musiXmatch/MSD` for lyric-derived features
- `Playlist2vec` for playlists, recommendation, and graph construction
- optional `Spotify MPD` when access is available

The implementation scope is explicitly:

- `metadata`
- `audio features`
- `lyrics bag-of-words or TF-IDF style structures`
- `playlist interaction tables`

The implementation scope is explicitly **not**:

- mp3 files
- waveform extraction
- spectrogram pipelines
- raw audio decoding during classroom dataset generation

---

## Why a Modular Dataset Stack Is Better

It is tempting to try to build one massive merged dataset with:

- audio features
- lyrics
- playlists
- user behavior
- graph relationships

That sounds elegant, but in practice it creates several problems:

- different datasets use different identifiers
- track matching across catalogs is noisy
- lyrics licensing is stricter than metadata licensing
- playlist data and audio feature data do not naturally live in the same schema
- undergraduates learn better when each method uses a well-shaped dataset rather than a fragile mega-table

So the recommended strategy is:

- `one source family for audio-space methods`
- `one source family for lyric-space methods`
- `one source family for behavior and graph methods`

The story remains unified because the product is unified, even if the raw data sources are not.

---

## Source Selection

## 1. FMA for Audio and Metadata

Use `FMA` as the main source for:

- Weeks `1-7`
- exploratory analysis
- curse of dimensionality
- PCA
- SVD
- t-SNE
- K-means
- DBSCAN

Useful files in the FMA release:

- `tracks.csv`
- `features.csv`
- `echonest.csv` if you want extra descriptors

Official source:

- [FMA dataset repository](https://github.com/mdeff/fma)

Why it is suitable:

- public and research-friendly
- includes metadata
- includes precomputed audio features
- includes smaller subsets (`small`, `medium`) that are classroom-friendly
- avoids the need to ship or decode mp3 files inside course tooling

## 2. musiXmatch for Lyrics

Use the `musiXmatch lyrics collection for the Million Song Dataset` as the lyric source.

Use it for:

- lyric bag-of-words
- TF-IDF
- text-space similarity
- content-based recommendation experiments with textual features

Official source:

- [musiXmatch dataset for the Million Song Dataset](https://millionsongdataset.com/musixmatch/)

Why it is suitable:

- public research companion dataset
- legally cleaner than scraping raw lyrics
- already designed for music analysis workflows
- naturally supports structured token-count and TF-IDF pipelines

Important limitation:

- it is not the same catalog as FMA
- therefore, lyric experiments should be taught as a `parallel content view`, not forced into one fully merged classroom table

## 3. Playlist2vec for Behavior and Graphs

Use `Playlist2vec` as the main public source for:

- Weeks `8-12`
- collaborative filtering
- playlist continuation logic
- song co-occurrence graphs
- PageRank on music networks

Official source:

- [Playlist2vec on Zenodo](https://zenodo.org/records/5002584)

Why it is suitable:

- public and currently downloadable
- playlist-native
- ideal for recommendation
- ideal for graph construction
- directly aligned with the `PachaMix` narrative

Recommended practical ingestion strategy:

- load the SQL dump into a relational database such as MySQL or MariaDB
- export the three tables needed by the toolkit as csv files:
  - `playlist.csv`
  - `track.csv`
  - `track_playlist1.csv`

The toolkit is designed to ingest those exported structured tables directly.

Important source note:

- the official `Playlist2vec` schema documents `track_playlist1` as a track-playlist association table
- it does not document an observed playlist-order column
- therefore `Playlist2vec` is excellent for:
  - collaborative filtering
  - popularity baselines
  - matrix factorization
  - co-occurrence graph construction
- but it should not be treated as a faithful sequential playlist source unless you add an explicit ordering strategy outside the raw source

## 4. Important Spotify Constraint

As of `March 15, 2026`, do **not** make the semester depend on the live Spotify Web API for audio features.

Reasons:

- the official `Get Track's Audio Features` endpoint is deprecated
- Spotify's developer policy explicitly says Spotify Platform content may not be used to train machine learning or AI models

Official sources:

- [Spotify audio features endpoint](https://developer.spotify.com/documentation/web-api/reference/get-audio-features)
- [Spotify Developer Policy](https://developer.spotify.com/policy/)

This is why the course should use:

- `FMA` for audio features
- `musiXmatch/MSD` for lyric features
- `Playlist2vec` for playlist behavior by default

## 5. Optional Spotify MPD Path

`Spotify MPD` remains useful if you already have access, but it should now be treated as optional.

Official source:

- [Spotify Million Playlist Dataset Remastered](https://research.atspotify.com/2020/9/the-million-playlist-dataset-remastered)

Important access note:

- the historical challenge distribution is no longer openly downloadable
- access may require a separate request to Spotify Research

---

## Recommended Processed Datasets

Build `processed` teaching datasets rather than teaching directly from raw files.

## Dataset A. `pachamix_audio_core.parquet`

Purpose:

- exploratory analysis
- high-dimensional geometry
- PCA/SVD/t-SNE
- clustering

Built from:

- `FMA tracks.csv`
- `FMA features.csv`
- optional `FMA echonest.csv`

Suggested columns:

- `track_id`
- `title`
- `artist_name`
- `album_title`
- `genre_top`
- `track_duration`
- numeric audio features
- optional extra descriptors

Recommended classroom versions:

- `audio_core_small.parquet` with `5,000-10,000` songs for laptops
- `audio_core_medium.parquet` with `20,000-40,000` songs for Colab
- `audio_core_full.parquet` for Spark or instructor demos

## Dataset B. `pachamix_lyrics_long.parquet`

Purpose:

- lyric feature engineering
- TF-IDF
- text similarity
- content-based recommendation with lyrics

Built from:

- `musiXmatch/MSD` lyric data
- optional MSD `track_metadata.db` for song-level metadata enrichment

Suggested columns:

- `msd_track_id`
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
- `token`
- `count`
- optional downstream `tfidf` or embedding features built later

Recommended classroom versions:

- full long-form lyrics table
- optional filtered token subsets for classroom exercises

## Dataset C. `pachamix_playlist_events.parquet`

Purpose:

- collaborative filtering
- popularity baselines
- ranking
- train/test split creation

Built from:

- `Playlist2vec` table exports or `MPD` raw playlist JSON slices

Suggested columns:

- `playlist_id`
- `track_uri`
- `track_name`
- `artist_name`
- `album_name`
- `position`
- `position_observed`
- optional `playlist_name`

Recommended classroom versions:

- `playlist_events_small.parquet` with `20,000-50,000` playlists
- `playlist_events_medium.parquet` with `100,000-200,000` playlists
- `playlist_events_full.parquet` for large-scale demos

## Dataset D. `pachamix_song_graph_edges.parquet`

Purpose:

- graph analytics
- centrality
- PageRank
- playlist-network interpretation

Built from:

- `pachamix_playlist_events.parquet`

Suggested columns:

- `src_track_uri`
- `dst_track_uri`
- `weight`
- optional `cooccurrence_count`

Recommended classroom versions:

- `song_graph_small.parquet` for NetworkX and local Python
- `song_graph_medium.parquet` for Colab or instructor demos
- `song_graph_spark.parquet` for distributed graph workflows

---

## Folder Layout

Use a clean folder structure so the course data pipeline looks professional and reproducible.

```text
data/
  raw/
    fma/
    musixmatch_msd/
    playlist2vec/
  interim/
    pachamix_audio_core/
    pachamix_lyrics/
    pachamix_playlists/
    pachamix_graph/
  processed/
    pachamix_audio_core.parquet
    pachamix_lyrics_long.parquet
    pachamix_playlist_events.parquet
    pachamix_song_graph_edges.parquet
    subsets/
      small/
      medium/
      spark/
```

---

## Generation Workflow

## Step 1. Build the Audio Dataset from FMA

### Objective

Create a clean table where each row is a song and columns contain:

- metadata
- audio features
- optional genre labels

### Raw Inputs

- `tracks.csv`
- `features.csv`
- optional `echonest.csv`

### Processing Tasks

1. Load `tracks.csv`
2. Keep only useful metadata columns
3. Load `features.csv`
4. Flatten the multi-index column structure if needed
5. Join metadata and features by `track_id`
6. Remove duplicates and obviously corrupted rows
7. Keep only numeric columns for PCA/clustering views
8. Store metadata and features together in a processed parquet file

### Suggested Additional Cleaning

- drop rows with too many missing numeric features
- standardize genre labels if you need them for interpretation only
- create a `feature_matrix` view without text columns
- keep a separate `metadata_lookup` table for plotting and cluster interpretation

### Optional Derived Files

- `pachamix_audio_numeric.npy` or parquet matrix
- `pachamix_audio_metadata.csv`

---

## Step 2. Build the Lyrics Dataset from musiXmatch/MSD

### Objective

Create a sparse textual feature matrix for lyric-based analysis.

### Raw Inputs

- the official `musiXmatch/MSD` lyric package

### Processing Tasks

1. Load the lyric bag-of-words data
2. Remove extremely rare words
3. Remove very frequent stop-like tokens if necessary
4. Keep the top `N` words by document frequency or information value
5. Build a sparse document-term matrix
6. Optionally compute `TF-IDF`
7. Save:
   - sparse matrix
   - vocabulary
   - track mapping table

### Suggested Teaching Outputs

- `lyrics_bow_sparse.npz`
- `lyrics_vocab.csv`
- `lyrics_tfidf_sparse.npz`
- `lyrics_track_index.csv`

### Important Teaching Note

This dataset can be used for:

- text similarity
- lyric-driven recommendation features
- dimensionality reduction in text spaces

It does not need to be perfectly joined to FMA to be valuable pedagogically.

---

## Step 3. Build the Playlist Interaction Dataset from Playlist2vec or MPD

### Objective

Turn the raw playlist JSON files into a clean interaction table for recommendation and graph work.

### Raw Inputs

- `Playlist2vec` exported tables or
- `MPD` playlist slices in JSON format

### Processing Tasks

If using Playlist2vec exports:

1. export:
   - `playlist.csv`
   - `track.csv`
   - `track_playlist1.csv`
2. join playlist metadata with track membership and track metadata
3. create one row per playlist-track interaction

When `Playlist2vec` does not provide observed order:

4. create a deterministic technical `position` per playlist
5. mark `position_observed = false`

If using MPD:

1. parse every playlist JSON slice
2. extract each playlist
3. for every track inside each playlist, create one row with:
   - `playlist_id`
   - `track_uri`
   - `track_name`
   - `artist_name`
   - `album_name`
   - `position`
   - `position_observed = true`
4. concatenate all rows into one long interaction table
5. remove exact duplicate rows if necessary
6. compute popularity statistics:
   - number of playlists per track
   - number of tracks per playlist
7. filter out tracks with extremely low support if needed for classroom subsets

### Recommended Derived Tables

- `playlist_events.parquet`
- `track_popularity.parquet`
- `playlist_stats.parquet`

### Recommended Filtering for Teaching

For a stable classroom subset:

- keep playlists with at least `5` tracks
- keep tracks that appear in at least `10-20` playlists

This reduces sparsity and makes collaborative filtering labs much more manageable.

---

## Step 4. Build the Song Graph from Playlist Co-Occurrence

### Objective

Generate a weighted graph where two songs are linked if they appear in the same playlist.

### Raw Input

- `pachamix_playlist_events.parquet`

### Graph Construction Logic

For each playlist:

- take all songs in the playlist
- create song-song pairs
- increment the edge weight for each co-occurring pair

### Two Construction Options

#### Option A. Full Co-Occurrence Graph

Connect every pair of songs in the same playlist.

Pros:

- simple
- intuitive
- easy to explain

Cons:

- dense for long playlists

#### Option B. Sliding-Window Graph

Connect only songs within a local playlist window, for example `window = 3` or `5`.

Pros:

- better local structure
- less dense graph
- more realistic sequence-based proximity

Cons:

- slightly more complex to explain

### Recommendation

For undergraduates, use:

- `full co-occurrence` first for simplicity
- then mention `sliding window` as an extension

### Output Columns

- `src_track_uri`
- `dst_track_uri`
- `weight`

### Additional Derived Measures

- weighted degree
- normalized transition probabilities
- PageRank scores

---

## Step 5. Create Train/Test Splits for Recommendation

### Objective

Create evaluation-ready subsets so recommendation is taught as a measurable task, not just as a demo.

### From Playlist Events

Possible split strategies:

- `hold out one track per playlist`
- `hold out last k tracks in each playlist`
- `random hold-out with fixed seed`

### Recommended Strategy

For playlist continuation exercises:

- use the first part of each playlist as input
- hold out the last `1-3` tracks as ground truth

This makes recommendation evaluation concrete and intuitive.

### Useful Evaluation Files

- `playlist_train.parquet`
- `playlist_test.parquet`
- `candidate_pool.parquet`

---

## Step 6. Create Small, Medium, and Spark-Scale Classroom Packages

Do not give all students the full raw datasets immediately.

Prepare three versions:

## A. Small

For:

- local laptops
- quick labs
- debugging

Suggested scale:

- `5,000-10,000` songs for audio work
- `20,000-50,000` playlists for recommendation
- `10,000-30,000` graph edges for NetworkX work

## B. Medium

For:

- Google Colab
- group projects
- slightly heavier experimentation

Suggested scale:

- `20,000-40,000` songs
- `100,000-200,000` playlists
- `100,000+` graph edges

## C. Spark

For:

- PySpark demonstrations
- instructor-led scale examples
- final pipeline and deployment topics

Suggested scale:

- the largest stable subset you can process comfortably in your environment

---

## Suggested Course-to-Dataset Mapping

Use this mapping when updating slides and labs.

| Weeks | Main Topic | Recommended Dataset |
| --- | --- | --- |
| 1-2 | Big Data, analytics, ML framing | `pachamix_audio_core.parquet` |
| 3 | Curse of dimensionality | `pachamix_audio_core.parquet` |
| 4-5 | PCA, SVD, t-SNE | `pachamix_audio_core.parquet` and optional derived matrices from `pachamix_lyrics_long.parquet` |
| 6-7 | K-means, DBSCAN | `pachamix_audio_core.parquet` |
| 8 | Content-based recommendation | `pachamix_audio_core.parquet` + derived text features from `pachamix_lyrics_long.parquet` |
| 9-10 | Collaborative and hybrid recommendation | `pachamix_playlist_events.parquet` from Playlist2vec or MPD |
| 11-12 | Graph analytics and PageRank | `pachamix_song_graph_edges.parquet` from Playlist2vec or MPD |
| 13-14 | Deployment and monitoring | reuse all processed datasets in pipeline form |

---

## Optional Unified Capstone Dataset

If you want a more ambitious final project, you can build a `small matched capstone set`.

Recommended rule:

- use `playlist data` as the behavioral core
- enrich only a subset of tracks with matched external features

### Practical Matching Strategy

1. Normalize:
   - `track_name`
   - `artist_name`
2. Lowercase text
3. Remove punctuation
4. Compare normalized artist-title pairs
5. Keep only exact or near-exact matches with a manual review sample

### Important Warning

Do **not** build the semester around this matching step.

Use it only for:

- capstone enrichment
- instructor demos
- advanced student projects

The core course should still work even if the matching is partial.

---

## Minimal Implementation Outline

If you later want to turn this plan into scripts, the processing pipeline can be organized into four jobs:

1. `build_audio_core.py`
   - reads FMA metadata and features
   - writes `pachamix_audio_core.parquet`
2. `build_lyrics_core.py`
   - reads musiXmatch/MSD lyrics
   - writes `pachamix_lyrics_long.parquet`
3. `build_playlist_events.py`
   - reads Playlist2vec exports or MPD JSON slices
   - writes `pachamix_playlist_events.parquet`
4. `build_song_graph.py`
   - reads playlist events
   - writes `pachamix_song_graph_edges.parquet`

If desired, add:

5. `build_reco_splits.py`
   - reads playlist events
   - writes training and evaluation splits

## Toolkit Command Examples

If you use the local PachaMix toolkit in this workspace, the equivalent commands are:

### One-command build

```bash
.venv/bin/python -m pachamix_data.cli build-course-dataset \
  --raw-root data/raw \
  --processed-root data/processed
```

Expected raw-root layout:

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

This command builds:

- `data/processed/pachamix_audio_core.parquet`
- `data/processed/pachamix_lyrics_long.parquet`

Optional behavior sources:

```text
data/raw/playlist2vec/
  playlist.csv
  track.csv
  track_playlist1.csv
```

or:

```text
data/raw/mpd/
  *.json
```

When one of those is present, the same command also builds:

- `data/processed/pachamix_playlists/playlist_events.parquet`
- `data/processed/pachamix_song_graph_edges.parquet`

When both are present, the pipeline prefers `playlist2vec/`.

### Individual commands

```bash
.venv/bin/python -m pachamix_data.cli build-audio-core \
  --tracks-csv data/raw/fma/tracks.csv \
  --features-csv data/raw/fma/features.csv \
  --output-parquet data/processed/pachamix_audio_core.parquet

.venv/bin/python -m pachamix_data.cli build-lyrics-core \
  --lyrics-txt data/raw/musixmatch_msd \
  --output-parquet data/processed/pachamix_lyrics_long.parquet \
  --metadata-db data/raw/msd/track_metadata.db

.venv/bin/python -m pachamix_data.cli build-playlist-events \
  --mpd-json data/raw/playlist2vec \
  --output-dir data/processed/pachamix_playlists

.venv/bin/python -m pachamix_data.cli build-song-graph \
  --playlist-events-parquet data/processed/pachamix_playlists/playlist_events.parquet \
  --output-parquet data/processed/pachamix_song_graph_edges.parquet
```

This keeps the operational workflow aligned with the course emphasis:

- structured metadata
- audio-feature tables
- lyrics token data
- playlist event tables
- graph edges

---

## Final Recommendation

The best course-ready dataset design is:

- `FMA` for audio-space modeling
- `musiXmatch/MSD` for lyric-space modeling
- `Playlist2vec` for collaborative filtering and graph analytics
- optional `MPD` when access is already available
- derived classroom-sized subsets for local, Colab, and Spark use

This gives you:

- a coherent story
- public sources
- feasible classroom pipelines
- mathematically meaningful feature spaces
- behavior data for recommender systems
- a natural path into song-network analysis and PageRank

That combination is much more realistic and teachable than trying to force one single, perfectly matched mega-dataset.
