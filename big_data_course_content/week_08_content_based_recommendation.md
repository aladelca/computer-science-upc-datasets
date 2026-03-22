# Week 8 - Content-Based Recommendation

## Position in the Semester

- Arc: Recommending Music
- Main datasets: `pachamix_audio_core`, `pachamix_lyrics_long`

## PachaMix Story Frame

### Cold Open

> Mathias: "If a student likes one sad acoustic song, we recommend forty more."
>
> Yunguri: "That is not personalization. That is emotional recursion."

### Narrative Role of the Week

This week is where the course starts making actual ranking decisions.
Students move from representation and grouping to retrieval.

## Dataset Anchor in This Repo

This week must be taught with methodological honesty.

### Audio-content view

Use `pachamix_audio_core` to build an audio-only content recommender.

### Lyric-content view

Use a derived TF-IDF or sparse lyric vectorization from `pachamix_lyrics_long` to build a lyric-only content recommender.

### Critical source constraint

The repo explicitly states that `pachamix_audio_core` and `pachamix_lyrics_long` do not share a native key.
Therefore the base classroom design should treat them as two parallel content spaces.

Allowed teaching paths:

1. Build two separate content recommenders:
   - audio-space recommender
   - lyric-space recommender
2. Build a small matched capstone subset only if the instructor explicitly performs cross-catalog matching.

Not allowed:

- pretending that a fully joined audio-plus-lyrics table already exists in the repo by default

## Theory Objectives

Students must be able to:

- represent items as vectors
- construct a user profile from historical preferences
- compute similarity scores
- explain TF-IDF mathematically
- evaluate ranked outputs with top-`k` metrics
- identify overspecialization as a structural weakness

## Vector-Space Formulation

Let each song be represented by a feature vector $x_j \in \mathbb{R}^d$.
Suppose a user has interacted positively with songs in a history set $H$.
A simple user profile is

$$
u = \frac{1}{|H|}\sum_{j \in H} x_j.
$$

A candidate song $c$ can be scored by cosine similarity:

$$
\operatorname{score}(u, x_c)
= \frac{u^\top x_c}{\lVert u \rVert_2 \lVert x_c \rVert_2}.
$$

The system then ranks candidates by descending score.

## TF-IDF for Lyric Features

If $tf_{t,d}$ is the term frequency of token $t$ in document $d$, and $df_t$ is the number of documents containing token $t$, then

$$
\operatorname{idf}(t) = \log \frac{N}{df_t},
$$

and

$$
\operatorname{tfidf}_{t,d} = tf_{t,d}\operatorname{idf}(t).
$$

This downweights ubiquitous tokens and upweights terms that are more discriminative across songs.

## Ranking Metrics

If $G$ is the set of relevant items and $\hat{L}_k$ is the top-$k$ list, then

$$
\operatorname{Precision@k} = \frac{|\hat{L}_k \cap G|}{k},
$$

$$
\operatorname{Recall@k} = \frac{|\hat{L}_k \cap G|}{|G|}.
$$

If the relevant items are ordered by importance, metrics such as `MAP` or `NDCG` can also be introduced.

## Structural Limitations

Pure content-based systems tend to:

- recommend items near what the user already consumed
- underexplore cross-style bridges
- depend heavily on feature quality
- struggle when user intent is not visible in item descriptors

This is not a bug in the implementation.
It is a limitation of the information source.

## Extended Theoretical Notes

### 1. Content Recommendation as a Projection of Preference into Feature Space

The core modeling assumption is that user taste can be represented in the same feature space as items.
If this is true, then recommendation reduces to comparing:

- an estimated user vector $u$
- candidate item vectors $x_j$

This is mathematically elegant, but also restrictive:
it assumes that preference is largely recoverable from observable item attributes.

### 2. Cosine Similarity and Angular Geometry

Cosine similarity measures the angle between vectors, not their Euclidean separation.
For nonzero vectors $a$ and $b$,

$$
\cos(\theta) = \frac{a^\top b}{\|a\|_2\|b\|_2}.
$$

So content recommendation under cosine similarity is fundamentally an angular-neighborhood method.
This is often appropriate when:

- vector magnitude is less informative than direction
- features have been normalized
- sparse TF-IDF representations are used

### 3. TF-IDF as Reweighting by Discriminative Value

Raw term counts overemphasize globally frequent tokens.
TF-IDF can be viewed as a diagonal reweighting of the term space:

$$
x_d^{(\text{tfidf})} = D_{\text{idf}} x_d^{(\text{tf})},
$$

where $D_{\text{idf}}$ is diagonal with larger weights for rarer terms.

This is mathematically useful because it changes the inner product geometry:

- common terms contribute less
- rare, discriminative terms contribute more

### 4. User-Profile Construction Is a Modeling Choice

The simple average

$$
u = \frac{1}{|H|}\sum_{j \in H} x_j
$$

is not the only possibility.
More generally one can write

$$
u = \sum_{j \in H} \alpha_j x_j, \qquad \sum_{j \in H}\alpha_j = 1,
$$

where the weights $\alpha_j$ may depend on:

- recency
- explicit ratings
- interaction strength
- trust in the signal

Thus even in a "simple" content-based system, the user model is an inferential object, not a fixed fact.

### 5. Overspecialization as a Geometric Consequence

If ranking is based mainly on nearest neighbors in feature space, then recommended items will often lie in the same local region as the observed history.
That creates:

- high local consistency
- low novelty
- weak long-range discovery

This is not accidental.
It is the geometric consequence of local similarity ranking.

## Mathematical Checkpoint

Students must be able to explain:

1. Why cosine similarity is scale-invariant.
2. Why TF-IDF can outperform raw counts for textual similarity.
3. Why overspecialization emerges from local similarity ranking.
4. Why evaluation of top-`k` ranking differs from regression-style loss evaluation.

## Laboratory Session

## Mission

Make PachaMix recommend songs from what the songs are.

## Required tasks

### Audio recommender

1. Select an audio feature representation from `pachamix_audio_core`.
2. Construct user profiles from selected seed songs.
3. Rank unseen tracks by cosine similarity.

### Lyric recommender

1. Build a sparse lyric matrix from `pachamix_lyrics_long`.
2. Optionally compute TF-IDF.
3. Construct profile vectors from seed songs within the lyric catalog.
4. Rank unseen tracks by cosine similarity.

## Required reporting

Students must report separately for the audio and lyric spaces:

- feature construction method
- normalization choices
- similarity metric
- top-`k` outputs
- at least one failure case

## Strict standards

- No cross-source hybrid claims are allowed without an explicit matching protocol.
- Any use of lyric features must state whether the representation is:
  - raw count
  - normalized count
  - TF-IDF
- A recommendation list must exclude seed songs unless the exercise explicitly allows self-recommendation.
- Evaluation must compare against at least one baseline, such as popularity or random ranking.

## Common failure modes

- forgetting to normalize vectors before cosine similarity
- mixing feature spaces without a justified common key
- treating top-`k` examples as evidence of global quality without a metric
- using all songs in the catalog as user history and then declaring the system accurate

## Extended Python Practice Session (2 Hours)

### Lab format

- `0:00-0:25` audio-space recommender setup
- `0:25-0:55` user-profile construction and cosine ranking
- `0:55-1:25` lyric-space TF-IDF recommender on a sampled catalog
- `1:25-1:45` score-distribution visualization and overspecialization analysis
- `1:45-2:00` reflection on parallel content spaces

### Python environment

```python
# Colab / fresh environment only
!pip install -q upc-datasets polars pyarrow numpy pandas matplotlib scikit-learn
```

### Guided notebook

#### 1. Audio-space content recommender

```python
import upc_datasets
import polars as pl
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler, normalize
from sklearn.feature_extraction.text import TfidfTransformer

audio = upc_datasets.load_dataset("pachamix_audio_core", root="data/processed", download=False)
metadata_cols = ["track_id", "title", "genre_top", "artist_name"]
feature_cols = [c for c in audio.columns if c not in metadata_cols]

audio_small = audio.filter(pl.col("genre_top").is_not_null()).sample(n=min(5000, audio.height), seed=42)

X_audio = audio_small.select(feature_cols).fill_null(0.0).to_numpy()
X_audio = StandardScaler().fit_transform(X_audio)
X_audio = normalize(X_audio)
```

#### 2. Construct a synthetic user profile from seed songs

```python
# Example: choose three seed tracks from the same top genre
seed_genre = (
    audio_small.group_by("genre_top")
    .len()
    .sort("len", descending=True)
    .item(0, "genre_top")
)

seed_df = audio_small.filter(pl.col("genre_top") == seed_genre).head(3)
seed_ids = seed_df.get_column("track_id").to_list()

audio_ids = audio_small.get_column("track_id").to_list()
id_to_idx = {track_id: i for i, track_id in enumerate(audio_ids)}
seed_idx = [id_to_idx[sid] for sid in seed_ids]

user_profile = X_audio[seed_idx].mean(axis=0)
user_profile = user_profile / np.linalg.norm(user_profile)

scores = X_audio @ user_profile
ranked_idx = np.argsort(scores)[::-1]

recommendation_rows = []
for idx in ranked_idx:
    track_id = audio_ids[idx]
    if track_id in seed_ids:
        continue
    row = audio_small.row(idx, named=True)
    recommendation_rows.append(
        {
            "track_id": row["track_id"],
            "title": row["title"],
            "artist_name": row["artist_name"],
            "genre_top": row["genre_top"],
            "score": float(scores[idx]),
        }
    )
    if len(recommendation_rows) == 10:
        break

audio_recommendations = pl.DataFrame(recommendation_rows)
audio_recommendations
```

#### 3. Visualize the audio recommendation scores

```python
plt.figure(figsize=(8, 4))
plt.hist(scores, bins=40, alpha=0.8)
plt.xlabel("Cosine score")
plt.ylabel("Number of candidate tracks")
plt.title("Audio-space recommendation score distribution")
plt.tight_layout()
plt.show()
```

#### 4. Lyric-space recommender on a sampled vocabulary

```python
lyrics = upc_datasets.load_dataset("pachamix_lyrics_long", root="data/processed", download=False)

top_tokens = (
    lyrics.group_by("token")
    .agg(pl.sum("count").alias("total_count"))
    .sort("total_count", descending=True)
    .head(400)
    .get_column("token")
    .to_list()
)

track_ids = lyrics.get_column("msd_track_id").unique().head(700).to_list()

lyrics_small = (
    lyrics.filter(pl.col("token").is_in(top_tokens) & pl.col("msd_track_id").is_in(track_ids))
    .group_by("msd_track_id", "token")
    .agg(pl.sum("count").alias("count"))
)

lyrics_wide = lyrics_small.pivot(index="msd_track_id", on="token", values="count").fill_null(0)
track_index = lyrics_wide.get_column("msd_track_id").to_list()
X_counts = lyrics_wide.drop("msd_track_id").to_numpy()

tfidf = TfidfTransformer()
X_tfidf = tfidf.fit_transform(X_counts).toarray()
X_tfidf = normalize(X_tfidf)
```

#### 5. Build a lyric-based user profile

```python
seed_lyric_idx = [0, 1, 2]
lyric_profile = X_tfidf[seed_lyric_idx].mean(axis=0)
lyric_profile = lyric_profile / np.linalg.norm(lyric_profile)

lyric_scores = X_tfidf @ lyric_profile
lyric_rank = np.argsort(lyric_scores)[::-1]

lyric_recommendation_rows = []
for idx in lyric_rank:
    if idx in seed_lyric_idx:
        continue
    lyric_recommendation_rows.append(
        {
            "msd_track_id": track_index[idx],
            "score": float(lyric_scores[idx]),
        }
    )
    if len(lyric_recommendation_rows) == 10:
        break

pl.DataFrame(lyric_recommendation_rows)
```

### Mathematical demonstration in Python

Show that cosine similarity is invariant to positive scaling:

```python
v = X_audio[0]
w = X_audio[1]

cos_original = float(v @ w / (np.linalg.norm(v) * np.linalg.norm(w)))
cos_scaled = float((3 * v) @ w / (np.linalg.norm(3 * v) * np.linalg.norm(w)))

print("original cosine:", cos_original)
print("scaled cosine  :", cos_scaled)
```

### Required exercises

1. Replace cosine similarity with raw dot product in the audio recommender. How does the ranking change?
2. Change the seed set from one genre to a mixed-genre profile. Does the recommendation list diversify?
3. Compare lyric recommendations with and without TF-IDF weighting.
4. Write one paragraph explaining why the audio and lyric recommenders in this repo are parallel content systems rather than one unified content system.

### Deliverables

- one top-10 audio recommendation table
- one top-10 lyric recommendation table
- one score-distribution plot
- one written diagnosis of overspecialization in at least one of the two spaces

## Bridge to Week 9

Content is only one source of evidence.
The next week asks a stronger social question:

what can we infer from how listeners organize songs together?
