# Big Data Weekly Content Package for PachaMix

## Purpose

This folder turns the semester plan into a teachable weekly package in English.
Each week is written against the actual dataset strategy and tooling documented in this repository, not against an imaginary unified music warehouse.

The package is intentionally strict:

- every week states the mathematical objects explicitly
- every algorithm is introduced through an objective function, a proof idea, or a linear algebra / probabilistic formulation
- every lab is anchored to a real dataset name produced by this repo
- every recommendation or graph topic respects the repository's source constraints

## Folder Contents

| Week | File |
| --- | --- |
| 1 | [week_01_big_data_foundations.md](./week_01_big_data_foundations.md) |
| 2 | [week_02_supervised_and_unsupervised_learning.md](./week_02_supervised_and_unsupervised_learning.md) |
| 3 | [week_03_curse_of_dimensionality.md](./week_03_curse_of_dimensionality.md) |
| 4 | [week_04_pca.md](./week_04_pca.md) |
| 5 | [week_05_svd_tsne_and_embeddings.md](./week_05_svd_tsne_and_embeddings.md) |
| 6 | [week_06_kmeans.md](./week_06_kmeans.md) |
| 7 | [week_07_dbscan_and_validation.md](./week_07_dbscan_and_validation.md) |
| 8 | [week_08_content_based_recommendation.md](./week_08_content_based_recommendation.md) |
| 9 | [week_09_collaborative_filtering.md](./week_09_collaborative_filtering.md) |
| 10 | [week_10_hybrid_recommendation_and_matrix_factorization.md](./week_10_hybrid_recommendation_and_matrix_factorization.md) |
| 11 | [week_11_graph_analytics_foundations.md](./week_11_graph_analytics_foundations.md) |
| 12 | [week_12_pagerank.md](./week_12_pagerank.md) |
| 13 | [week_13_pipelines.md](./week_13_pipelines.md) |
| 14 | [week_14_serving_monitoring_and_defense.md](./week_14_serving_monitoring_and_defense.md) |
| Project | [semester_group_assignment_brief.md](./semester_group_assignment_brief.md) |

## Dataset Ground Truth for This Repo

The material in this folder is built around the processed datasets defined in `data_dictionary.md` and the build workflow described in `README.md` and `runbooks/03-build-course-datasets.md`.

### Core datasets already supported by the codebase

| Dataset | Status in repo design | Typical weeks | Grain |
| --- | --- | --- | --- |
| `pachamix_audio_core` | core | 1-7, 8 | one row per FMA track |
| `pachamix_lyrics_long` | core | 5, 8 | one row per `(msd_track_id, token)` |
| `pachamix_playlist_events` | optional behavior layer | 9-11, 13-14 | one row per `(playlist_id, track_uri, position)` |
| `pachamix_playlist_stats` | optional behavior summary | 9, 13-14 | one row per playlist |
| `pachamix_track_popularity` | optional behavior summary | 9-10, 14 | one row per `track_uri` |
| `pachamix_song_graph_edges` | optional graph layer | 11-12, 14 | one row per undirected song pair |

### Non-negotiable source constraints

- `FMA` and `musiXmatch/MSD` are parallel source families, not a naturally joined single table.
- A direct row-level join between `pachamix_audio_core` and `pachamix_lyrics_long` does not exist by default in this repo.
- Weeks that discuss hybrid recommendation must either:
  - operate on a matched capstone subset built by explicit title/artist matching, or
  - present the hybrid model mathematically while keeping the lab on the behavioral matrix alone.
- PageRank must be run on a directed transition structure. Because `pachamix_song_graph_edges` is undirected, the lab first expands each undirected edge into two directed edges of equal weight.
- The course must not rely on the live Spotify Web API for audio features.

## Build Prerequisites

If the instructor needs to rebuild the processed data locally, use the repo tooling.

### One-command build

```bash
.venv/bin/python -m upc_datasets.cli build-course-dataset \
  --raw-root data/raw \
  --processed-root data/processed
```

Equivalent builder entrypoint:

```bash
.venv/bin/python -m pachamix_data.cli build-course-dataset \
  --raw-root data/raw \
  --processed-root data/processed
```

### Minimum raw layout

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

### Optional behavior raw layout

```text
data/raw/playlist2vec/
  playlist.csv
  track.csv
  track_playlist1.csv
```

or

```text
data/raw/mpd/
  *.json
```

## Recommended Weekly Dataset Mapping

| Weeks | Topic family | Primary processed datasets |
| --- | --- | --- |
| 1-4 | framing, geometry, PCA | `pachamix_audio_core` |
| 5 | SVD, t-SNE, text-space representation | `pachamix_audio_core`, `pachamix_lyrics_long` |
| 6-7 | clustering | `pachamix_audio_core` |
| 8 | content-based recommendation | `pachamix_audio_core` and a separate lyric-space view from `pachamix_lyrics_long` |
| 9-10 | collaborative / hybrid recommendation | `pachamix_playlist_events`, `pachamix_track_popularity`, optional matched capstone subset |
| 11-12 | graph analytics / PageRank | `pachamix_song_graph_edges` derived from `pachamix_playlist_events` |
| 13-14 | pipelines, serving, monitoring | reuse all processed datasets and build artifacts |

## Recommended Lab Stack

The repo itself only packages `polars` and `pyarrow`, but the weekly practice sessions in this folder assume a teaching environment with the following Python stack available:

- `numpy`
- `pandas`
- `matplotlib`
- `scikit-learn`
- `networkx` for graph weeks

Suggested installation in Colab or a fresh virtual environment:

```bash
pip install upc-datasets polars pyarrow numpy pandas matplotlib scikit-learn networkx
```

When a weekly lab only needs part of the stack, students may install only the required subset.

## Shared Mathematical Conventions

The weekly notes use the following symbols consistently:

- $n$: number of observations
- $d$: number of input dimensions or features
- $k$: reduced dimension, number of clusters, or neighborhood size depending on context
- $X \in \mathbb{R}^{n \times d}$: data matrix
- $x_i \in \mathbb{R}^d$: feature vector for observation $i$
- $\mu$: mean vector
- $\Sigma$: covariance matrix
- $A$: adjacency matrix
- $D$: degree matrix
- $P$: row-stochastic transition matrix
- $\Omega$: observed entries in a partially observed matrix

## Pedagogical Rules for This Package

- A diagram without a formula is incomplete.
- A formula without assumptions is incomplete.
- An experiment without an evaluation protocol is incomplete.
- A recommendation result without a baseline is incomplete.
- A graph ranking result without an interpretation of edge construction is incomplete.
- A pipeline demo without artifact lineage is incomplete.

## How to Use the Weekly Files

Each file is designed to be used as:

- instructor lecture notes
- the written backbone of a lab handout
- a rigorous study guide for students
- a starting point for slide decks or notebook instructions

The files are intentionally comprehensive. They can be trimmed for a shorter class, but they should not be made less rigorous.
