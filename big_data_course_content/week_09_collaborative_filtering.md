# Week 9 - Collaborative Filtering

## Position in the Semester

- Arc: Recommending Music
- Main datasets: `pachamix_playlist_events`, `pachamix_playlist_stats`, `pachamix_track_popularity`

## PachaMix Story Frame

### Cold Open

> Mathias: "What if we ignore the songs and just copy the taste of people who seem cool?"
>
> Yunguri: "Methodologically reckless. Socially realistic."

### Narrative Role of the Week

This week introduces behavior as a signal.
The system stops asking only "What is this song?" and starts asking "How do songs co-occur in actual listening collections?"

## Dataset Anchor in This Repo

### Required processed datasets

- `pachamix_playlist_events`
- `pachamix_playlist_stats`
- `pachamix_track_popularity`

### Important operational note

These datasets are optional in the repo and require a staged behavior source such as `Playlist2vec` or `MPD`.
If they are not yet built, the instructor must generate them before the lab.

### Why playlists can act as "users"

In this course design, a playlist is treated as a temporary preference profile.
That lets students build a playlist-track matrix even when no long-term individual user identifiers are available.

## Theory Objectives

Students must be able to:

- construct an interaction matrix from playlist data
- distinguish user-based and item-based collaborative filtering
- compute cosine and Pearson similarities
- define sparsity and cold start precisely
- explain why behavior-space similarity can differ from content-space similarity

## Matrix Formulation

Let $R \in \mathbb{R}^{m \times n}$ be the playlist-track interaction matrix, where:

- $m$ = number of playlists
- $n$ = number of tracks
- $R_{pj} = 1$ if track $j$ appears in playlist $p$, else $0$

This is an implicit-feedback matrix.

## Similarity Measures

### Cosine similarity

For playlists $p$ and $q$,

$$
\operatorname{sim}_{\cos}(p,q)
= \frac{R_{p\cdot}^\top R_{q\cdot}}{\lVert R_{p\cdot} \rVert_2 \lVert R_{q\cdot} \rVert_2}.
$$

For tracks $i$ and $j$,

$$
\operatorname{sim}_{\cos}(i,j)
= \frac{R_{\cdot i}^\top R_{\cdot j}}{\lVert R_{\cdot i} \rVert_2 \lVert R_{\cdot j} \rVert_2}.
$$

### Pearson correlation

Pearson correlation is more common with explicit ratings, but it can still be taught conceptually as a centered similarity:

$$
\operatorname{corr}(a,b)
= \frac{\sum_t (a_t - \bar{a})(b_t - \bar{b})}{\sqrt{\sum_t (a_t - \bar{a})^2}\sqrt{\sum_t (b_t - \bar{b})^2}}.
$$

For binary playlist membership, cosine similarity is often more natural.

## Neighborhood-Based Prediction

For a playlist $p$ and candidate track $j$, one user-based style estimate is

$$
\hat{r}_{pj}
= \frac{\sum_{q \in N_k(p)} \operatorname{sim}(p,q) R_{qj}}
{\sum_{q \in N_k(p)} |\operatorname{sim}(p,q)|}.
$$

An item-based analogue uses track-to-track similarity relative to tracks already present in the target playlist.

## Sparsity and Reliability

If the matrix is very sparse, similarity estimates can be unstable because they are computed from tiny overlaps.
Thus two playlists with one shared song may appear deceptively similar.

This is why support thresholds and overlap-aware diagnostics matter.

## Evaluation Logic

Following the dataset generation plan, a practical evaluation protocol is:

1. use the first part of each playlist as observed history
2. hold out the last `1-3` tracks as ground truth
3. rank candidate tracks
4. evaluate with top-`k` metrics or hit-rate metrics

For explicit-score demonstrations, `RMSE` and `MAE` may still be shown, but the playlist continuation setting is inherently a ranking task.

## Extended Theoretical Notes

### 1. Collaborative Filtering as Matrix Completion Intuition

The interaction matrix is mostly unobserved.
Collaborative filtering asks whether the observed pattern of co-occurrence contains enough structure to infer good missing entries or good ranked candidates.

This is why the matrix view is central:

- rows encode playlist-like preference contexts
- columns encode items
- missing entries are not all equivalent

### 2. Similarity in Behavior Space

Two tracks can be behaviorally similar even if they are acoustically dissimilar.
Formally, item-based collaborative filtering compares column vectors:

$$
R_{\cdot i}, R_{\cdot j}.
$$

If those columns have similar support patterns across playlists, then the items are neighbors in interaction space.
This is a fundamentally different geometry from feature-space similarity.

### 3. Sparsity and Variance of Similarity Estimates

When overlap is small, similarity estimates have high variance.
This is especially clear for cosine similarity or correlation computed from tiny intersections.

Thus a rigorous collaborative system often needs:

- support thresholds
- shrinkage logic
- minimum-overlap rules

The classroom version need not implement every refinement, but students should understand why raw similarity scores can be misleading.

### 4. Implicit Feedback Is Not a Standard Regression Target

In the playlist setting, a missing entry does not necessarily mean dislike.
It often means:

- unobserved
- not yet encountered
- absent from the limited playlist context

Therefore the interpretation of $R_{ui}=0$ differs from explicit rating problems.
This is one reason ranking metrics are more natural than naive pointwise error metrics here.

### 5. Baselines Are Theoretical Controls, Not Mere Practical Formalities

The popularity baseline matters because it isolates the value of personalization.
If a complex collaborative model does not beat a simple popularity ranking, then either:

- the method is weak
- the evaluation split is too easy
- the available data do not justify the added complexity

This is why baselines are part of mathematical rigor, not an afterthought.

## Mathematical Checkpoint

Students must be able to explain:

1. Why playlists can be treated as user proxies.
2. Why binary implicit data changes the meaning of prediction.
3. Why similarity in interaction space can reveal relationships absent from feature space.
4. Why sparsity weakens trust in naive neighborhood scores.

## Laboratory Session

## Mission

Make PachaMix learn from listening behavior.

## Required tasks

1. Build a sparse playlist-track matrix from `pachamix_playlist_events`.
2. Compute:
   - playlist similarities, or
   - track similarities
3. Create a hold-out evaluation split.
4. Produce ranked continuations for partially observed playlists.
5. Compare the collaborative recommender against:
   - random baseline
   - popularity baseline from `pachamix_track_popularity`

## Required reporting

Students must report:

- matrix dimensions
- density or sparsity level
- similarity metric
- neighborhood size
- evaluation split logic
- recommendation metric

## Strict standards

- A collaborative system must be compared against at least a popularity baseline.
- Students must report the matrix sparsity explicitly.
- If cosine similarity is used, the report must state whether vectors were binarized or frequency-weighted.
- Claims about "similar taste" are invalid without specifying the overlap regime that produced the similarity.

## Common failure modes

- leaking held-out tracks into the observed playlist history
- treating popularity as a nuisance instead of a necessary baseline
- using RMSE on implicit binary data without explaining why
- forgetting that playlist continuation is a ranking problem

## Extended Python Practice Session (2 Hours)

### Lab format

- `0:00-0:20` load and filter playlist behavior
- `0:20-0:45` construct a manageable playlist-track matrix
- `0:45-1:15` compute item-item similarity and playlist continuation scores
- `1:15-1:40` evaluate against a hold-out and popularity baseline
- `1:40-2:00` discuss sparsity and reliability

### Python environment

```python
# Colab / fresh environment only
!pip install -q upc-datasets polars pyarrow numpy pandas matplotlib scikit-learn
```

### Guided notebook

#### 1. Load the behavior datasets

```python
import upc_datasets
import polars as pl
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import normalize

events = upc_datasets.load_dataset("pachamix_playlist_events", root="data/processed", download=False)
popularity = upc_datasets.load_dataset("pachamix_track_popularity", root="data/processed", download=False)
playlist_stats = upc_datasets.load_dataset("pachamix_playlist_stats", root="data/processed", download=False)

events.shape, popularity.shape, playlist_stats.shape
```

#### 2. Build a dense enough classroom subset

```python
active_playlists = (
    playlist_stats.filter(pl.col("track_count") >= 8)
    .head(800)
    .get_column("playlist_id")
    .to_list()
)

top_tracks = popularity.sort("playlist_count", descending=True).head(500).get_column("track_uri").to_list()

events_small = events.filter(
    pl.col("playlist_id").is_in(active_playlists) & pl.col("track_uri").is_in(top_tracks)
)

events_small.shape
```

#### 3. Create a playlist-track matrix

```python
matrix_df = (
    events_small.select(["playlist_id", "track_uri"])
    .with_columns(pl.lit(1).alias("value"))
    .pivot(index="playlist_id", on="track_uri", values="value")
    .fill_null(0)
)

playlist_ids = matrix_df.get_column("playlist_id").to_list()
track_cols = [c for c in matrix_df.columns if c != "playlist_id"]
R = matrix_df.drop("playlist_id").to_numpy().astype(float)

print("matrix shape:", R.shape)
print("density:", float(R.sum() / (R.shape[0] * R.shape[1])))
```

#### 4. Create a hold-out playlist-continuation task

```python
target_row = 0
target_vector = R[target_row].copy()
observed_track_idx = np.where(target_vector > 0)[0]

holdout_size = min(2, len(observed_track_idx) // 2)
held_out_idx = observed_track_idx[-holdout_size:]
observed_idx = observed_track_idx[:-holdout_size]

R_train = R.copy()
R_train[target_row, held_out_idx] = 0

ground_truth_tracks = {track_cols[i] for i in held_out_idx}
observed_tracks = {track_cols[i] for i in observed_idx}

ground_truth_tracks, observed_tracks
```

#### 5. Compute item-item cosine similarity

```python
item_matrix = R_train.T
item_matrix = normalize(item_matrix)
similarity = item_matrix @ item_matrix.T

scores = np.zeros(len(track_cols))
for idx in observed_idx:
    scores += similarity[idx]

for idx in observed_idx:
    scores[idx] = -np.inf

ranked_idx = np.argsort(scores)[::-1]
top_k = 10
predicted_tracks = [track_cols[i] for i in ranked_idx[:top_k]]
predicted_tracks
```

#### 6. Evaluate collaborative filtering and popularity baseline

```python
def precision_at_k(predicted, ground_truth, k):
    return len(set(predicted[:k]) & set(ground_truth)) / k

def recall_at_k(predicted, ground_truth, k):
    return len(set(predicted[:k]) & set(ground_truth)) / max(len(ground_truth), 1)

cf_precision = precision_at_k(predicted_tracks, ground_truth_tracks, top_k)
cf_recall = recall_at_k(predicted_tracks, ground_truth_tracks, top_k)

pop_rank = popularity.sort("playlist_count", descending=True).get_column("track_uri").to_list()
pop_pred = [uri for uri in pop_rank if uri not in observed_tracks][:top_k]

pop_precision = precision_at_k(pop_pred, ground_truth_tracks, top_k)
pop_recall = recall_at_k(pop_pred, ground_truth_tracks, top_k)

print("CF precision@10 :", cf_precision)
print("CF recall@10    :", cf_recall)
print("POP precision@10:", pop_precision)
print("POP recall@10   :", pop_recall)
```

#### 7. Visualize sparsity

```python
plt.figure(figsize=(6, 5))
plt.imshow(R[:100, :100], aspect="auto", cmap="Greys")
plt.xlabel("Tracks")
plt.ylabel("Playlists")
plt.title("Binary playlist-track matrix (100 x 100 view)")
plt.tight_layout()
plt.show()
```

### Mathematical demonstration in Python

Collaborative filtering quality depends on overlap.
Measure the number of common playlists between the first few observed tracks:

```python
for a in observed_idx[: min(3, len(observed_idx))]:
    for b in observed_idx[: min(3, len(observed_idx))]:
        overlap = int(np.sum(R_train[:, a] * R_train[:, b]))
        print(track_cols[a], track_cols[b], overlap)
```

Small overlaps can make similarity estimates unstable even when cosine scores look large.

### Required exercises

1. Vary the track vocabulary size from `500` to `1000`. What happens to sparsity and precision@10?
2. Compare item-based and playlist-based similarity.
3. Hold out the last `1`, `2`, and `3` tracks of the target playlist. How stable are the results?
4. Explain why the popularity baseline is necessary even when collaborative filtering seems more sophisticated.

### Deliverables

- one summary of matrix shape and density
- one collaborative-filtering recommendation list
- one popularity-baseline recommendation list
- one short analysis of how sparsity affected trust in the similarity scores

## Bridge to Week 10

By now PachaMix has two kinds of evidence:

- content
- behavior

The next week asks how to combine them, and then pushes the class toward latent-factor models.
