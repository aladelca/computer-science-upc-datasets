# Week 3 - The Curse of Dimensionality

## Position in the Semester

- Arc: Fighting High Dimensionality
- Main datasets: `pachamix_audio_core`, `pachamix_lyrics_long`

## PachaMix Story Frame

### Cold Open

> Mathias: "I made a feature vector with tempo, energy, danceability, acousticness, lyric counts, n-grams, embeddings, playlist statistics, and 2,000 extra columns just in case."
>
> Yunguri: "That is not a feature space. That is a cry for help."

### Narrative Role of the Week

Students must discover that more variables do not automatically imply more usable information.
This week is the first major mathematical warning shot of the course.

## Dataset Anchor in This Repo

### Audio space

`pachamix_audio_core` already contains `518` numeric descriptors per track.
That is enough to make:

- pairwise distances expensive
- nearest-neighbor reasoning unstable
- naive clustering sensitive to scale and noise

### Text space

`pachamix_lyrics_long` is even more extreme once converted into a bag-of-words or TF-IDF matrix.
Its natural sparse vocabulary space is much larger than the audio space.

## Theory Objectives

Students must be able to:

- explain why geometric intuition fails in high dimension
- derive the shrinking volume share of the inscribed hypersphere
- interpret distance concentration
- connect dimensionality to sample complexity and instability

## Mathematical Development

### 1. Hypercube Versus Hypersphere

The volume of the $d$-dimensional unit-radius ball is

$$
V_d(1) = \frac{\pi^{d/2}}{\Gamma\left(\frac{d}{2} + 1\right)}.
$$

The volume of the cube $[-1, 1]^d$ is

$$
2^d.
$$

Hence the fraction of the cube occupied by the inscribed unit ball is

$$
\frac{V_d(1)}{2^d} = \frac{\pi^{d/2}}{2^d \Gamma\left(\frac{d}{2} + 1\right)}.
$$

As $d \to \infty$, this ratio goes to $0$.

Interpretation:

- in high dimension, most cube volume lies far from the center
- local neighborhoods become unintuitive
- "inside" and "near the boundary" cease to behave as in two or three dimensions

### 2. Expected Squared Distance in the Unit Hypercube

Let $x, y \sim \text{Unif}([0,1]^d)$ independently.
Then

$$
\mathbb{E}\left[\lVert x - y \rVert_2^2\right]
= \sum_{j=1}^d \mathbb{E}\left[(x_j - y_j)^2\right]
= d \cdot \frac{1}{6}
= \frac{d}{6}.
$$

Therefore the typical squared distance grows linearly with $d$, while relative variation becomes comparatively smaller.

### 3. Distance Concentration

A useful heuristic statement is:

$$
\frac{\max_i d(x, x_i) - \min_i d(x, x_i)}{\min_i d(x, x_i)} \to 0
$$

in many high-dimensional regimes.

This means the nearest and farthest points become less distinguishable in relative terms.
When this happens, methods that rely on distance ranking lose discriminatory power.

### 4. Why This Matters for PachaMix

If song vectors are high-dimensional and poorly scaled, then:

- nearest-neighbor recommendation becomes noisy
- clustering quality deteriorates
- visualization is misleading without reduction
- more samples are needed to estimate local structure reliably

## Extended Theoretical Notes

### 1. Concentration of Measure Intuition

A broad high-dimensional phenomenon is that many quantities concentrate around typical values.
For distance-based learning, this means:

- distances become less contrastive
- neighborhoods become less informative
- volume moves into unintuitive regions of the space

The precise theorems depend on the data-generating distribution, but the practical implication is robust:

high-dimensional nearest-neighbor reasoning is fragile unless the data have additional structure.

### 2. Sparse Versus Dense High-Dimensional Regimes

Not all high-dimensional spaces fail in the same way.
There is an important distinction:

- `dense high-dimensional data`
  where many coordinates contribute nontrivially to distance
- `sparse high-dimensional data`
  where vectors occupy tiny fractions of the ambient space

Sparse text vectors, such as those derived from `pachamix_lyrics_long`, create additional issues:

- many orthogonal or nearly orthogonal observations
- rare-token instability
- cosine or Euclidean similarity heavily affected by support overlap

So sparsity does not rescue high dimension automatically.
It changes the geometry, but it does not eliminate the curse.

### 3. Sample Complexity Intuition

Suppose a resolution $\varepsilon$ is desired in each coordinate of a unit hypercube.
Then a naive grid argument requires roughly

$$
\left(\frac{1}{\varepsilon}\right)^d
$$

cells to cover the space.

This shows the exponential dependence on $d$ directly.
Even if such a grid is too crude for practical modeling, it gives the right strategic message:

fine-grained coverage becomes impossible quickly as dimension grows.

### 4. Why Feature Selection and Reduction Are Different

It is important to separate:

- `feature selection`
  choosing a subset of original coordinates
- `dimensionality reduction`
  constructing new coordinates, often as combinations of the originals

Feature selection assumes many original variables are dispensable.
Dimensionality reduction assumes useful information may be spread across many variables but lie near a lower-dimensional manifold or subspace.
The course first emphasizes reduction because the PachaMix audio features are engineered families rather than arbitrary redundant spreadsheet columns.

## Mathematical Checkpoint

Students must prove or justify:

1. Why the hyperball occupies a vanishing fraction of the hypercube.
2. Why pairwise distances can become less informative as dimension grows.
3. Why sparse text vectors are particularly exposed to the curse of dimensionality.
4. Why dimensionality reduction is not cosmetic, but structural.

## Laboratory Session

## Mission

Measure the curse rather than reciting it.

## Required tasks

1. Simulate random points in dimensions such as:
   - $d = 2$
   - $d = 10$
   - $d = 50$
   - $d = 100$
   - $d = 500$
2. For each $d$, compute:
   - mean pairwise distance
   - nearest-neighbor distance
   - farthest-neighbor distance
   - contrast ratio
3. Repeat the analysis on:
   - the standardized numeric matrix from `pachamix_audio_core`
   - an instructor-built sparse lyric matrix derived from `pachamix_lyrics_long`

## Recommended processing notes

- Standardize the audio numeric matrix before Euclidean analysis.
- For lyrics, first pivot to a sparse document-term representation.
- If memory is limited, sample documents or tracks rather than pretending exact full-matrix pairwise computations are cheap.

## Strict standards

- No student may claim "high-dimensional data is bad" without naming the mechanism.
- Any distance-based conclusion must specify:
  - the metric used
  - the preprocessing used
  - whether the data were dense or sparse
- A plot without a numerical concentration statistic is insufficient.

## Common misconceptions

- "More features always improve accuracy."
- "Sparse vectors are automatically easy because most entries are zero."
- "If the nearest neighbor exists, it must be meaningful."
- "Dimensionality problems disappear once we have more rows."

None of these statements survives rigorous inspection without strong additional assumptions.

## Extended Python Practice Session (2 Hours)

### Lab format

- `0:00-0:25` simulation in synthetic spaces of increasing dimension
- `0:25-0:50` numerical measurement of nearest/farthest contrast
- `0:50-1:20` repeat the experiment on `pachamix_audio_core`
- `1:20-1:40` optional lyric-space extension
- `1:40-2:00` written interpretation of the geometric collapse

### Python environment

```python
# Colab / fresh environment only
!pip install -q upc-datasets polars pyarrow numpy pandas matplotlib scikit-learn
```

### Guided notebook

#### 1. Simulate random points in increasing dimensions

```python
import upc_datasets
import polars as pl
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances

rng = np.random.default_rng(42)

def distance_summary(n_points: int, d: int) -> dict:
    X = rng.uniform(0.0, 1.0, size=(n_points, d))
    D = pairwise_distances(X, metric="euclidean")
    np.fill_diagonal(D, np.nan)
    nearest = np.nanmin(D, axis=1)
    farthest = np.nanmax(D, axis=1)
    contrast = (farthest - nearest) / nearest
    return {
        "dimension": d,
        "mean_nearest": float(np.nanmean(nearest)),
        "mean_farthest": float(np.nanmean(farthest)),
        "mean_contrast": float(np.nanmean(contrast)),
    }

sim_rows = [distance_summary(n_points=400, d=d) for d in [2, 5, 10, 20, 50, 100, 200]]
sim_df = pl.DataFrame(sim_rows)
sim_df
```

#### 2. Visualize the contrast-ratio decay

```python
pdf = sim_df.to_pandas()

plt.figure(figsize=(8, 4))
plt.plot(pdf["dimension"], pdf["mean_contrast"], marker="o")
plt.xscale("log")
plt.xlabel("Dimension (log scale)")
plt.ylabel("Mean contrast ratio")
plt.title("Distance contrast decreases as dimension grows")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

#### 3. Verify the expected squared-distance growth

```python
def expected_squared_distance_demo(n_points: int, d: int) -> dict:
    X = rng.uniform(0.0, 1.0, size=(n_points, d))
    D_sq = pairwise_distances(X, metric="sqeuclidean")
    iu = np.triu_indices_from(D_sq, k=1)
    empirical = float(np.mean(D_sq[iu]))
    theory = d / 6.0
    return {"dimension": d, "empirical": empirical, "theory": theory}

sq_df = pl.DataFrame([expected_squared_distance_demo(300, d) for d in [2, 10, 50, 100]])
sq_df
```

#### 4. Repeat the experiment on real audio data

```python
audio = upc_datasets.load_dataset("pachamix_audio_core", root="data/processed", download=False)
metadata_cols = ["track_id", "title", "genre_top", "artist_name"]
feature_cols = [c for c in audio.columns if c not in metadata_cols]

audio_sample = audio.sample(n=min(1500, audio.height), seed=42)
X_audio = audio_sample.select(feature_cols).fill_null(0.0).to_numpy()
X_audio = StandardScaler().fit_transform(X_audio)

D_audio = pairwise_distances(X_audio, metric="euclidean")
np.fill_diagonal(D_audio, np.nan)

nearest_audio = np.nanmin(D_audio, axis=1)
farthest_audio = np.nanmax(D_audio, axis=1)
contrast_audio = (farthest_audio - nearest_audio) / nearest_audio

print("mean nearest:", float(np.nanmean(nearest_audio)))
print("mean farthest:", float(np.nanmean(farthest_audio)))
print("mean contrast:", float(np.nanmean(contrast_audio)))
```

#### 5. Optional lyric-space extension

```python
lyrics = upc_datasets.load_dataset("pachamix_lyrics_long", root="data/processed", download=False)

top_tokens = (
    lyrics.group_by("token")
    .agg(pl.sum("count").alias("total_count"))
    .sort("total_count", descending=True)
    .head(250)
    .get_column("token")
    .to_list()
)

lyrics_small = (
    lyrics.filter(pl.col("token").is_in(top_tokens))
    .group_by("msd_track_id", "token")
    .agg(pl.sum("count").alias("count"))
)

track_ids = lyrics_small.get_column("msd_track_id").unique().head(400).to_list()
lyrics_small = lyrics_small.filter(pl.col("msd_track_id").is_in(track_ids))

wide = lyrics_small.pivot(index="msd_track_id", on="token", values="count").fill_null(0)
X_lyrics = wide.drop("msd_track_id").to_numpy()

if X_lyrics.shape[0] > 2:
    D_lyrics = pairwise_distances(X_lyrics, metric="cosine")
    np.fill_diagonal(D_lyrics, np.nan)
    print("lyric-space mean nearest cosine distance:", float(np.nanmean(np.nanmin(D_lyrics, axis=1))))
    print("lyric-space mean farthest cosine distance:", float(np.nanmean(np.nanmax(D_lyrics, axis=1))))
```

### Mathematical demonstration in Python

The analytic benchmark is

$$
\mathbb{E}\left[\|x-y\|_2^2\right] = \frac{d}{6}
$$

for independent uniform points on $[0,1]^d$.
Use the `sq_df` table above to compare empirical and theoretical values.

### Required exercises

1. Repeat the simulation with Manhattan distance instead of Euclidean distance. Does contrast decay in the same way?
2. Compare the audio-space contrast before and after standardization.
3. Increase the vocabulary size in the lyric experiment from `250` tokens to `1000` tokens. What happens to nearest-neighbor behavior?
4. Explain, in one paragraph, why dimensionality hurts both clustering and recommendation.

### Deliverables

- one simulation table over multiple dimensions
- one contrast-ratio plot
- one real-data audio-space contrast summary
- one short discussion relating the Python results to the theoretical formulas

## Bridge to Week 4

Once the class accepts that the raw feature space is geometrically unstable, the next logical question is unavoidable:

how do we reduce dimension without discarding the structure we care about?
