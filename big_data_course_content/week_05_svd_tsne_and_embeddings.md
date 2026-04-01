# Week 5 - SVD, t-SNE, and the Difference Between Compression and Visualization

## Position in the Semester

- Arc: Fighting High Dimensionality
- Main datasets: `pachamix_audio_core`, `pachamix_lyrics_long`

## PachaMix Story Frame

### Cold Open

> Mathias: "I used t-SNE. The clusters look beautiful."
>
> Yunguri: "Do they mean anything?"

### Narrative Role of the Week

This week teaches a crucial intellectual discipline:

- not every low-dimensional picture is a good compressed representation
- not every compressed representation is a good visualization

Students must learn to ask what notion of structure each method preserves.

### Short Dialogue on the Core Concept

> Mathias: "If the t-SNE plot looks like islands, the islands are real."
>
> Yunguri: "A map is not a treaty with reality."
>
> Mathias: "Then what does t-SNE preserve?"
>
> Yunguri: "Mostly your obligation to stop overclaiming."
>
> Mathias: "Then SVD is the adult in the room?"
>
> Yunguri: "SVD at least tells you what it is optimizing."
>
> Mathias: "And embeddings?"
>
> Yunguri: "Coordinates learned from context, which is powerful and dangerous in equal measure."

## Dataset Anchor in This Repo

### Audio matrix

Use the numeric feature matrix from `pachamix_audio_core` for:

- PCA comparison
- SVD reconstruction
- low-rank error analysis

### Lyric matrix

Derive a sparse document-term or TF-IDF matrix from `pachamix_lyrics_long` for:

- text-space dimensionality reduction
- sparse high-dimensional comparison
- nonlinear visualization demonstrations

Important constraint:

- `pachamix_lyrics_long` is long-form token data
- students must build the wide sparse matrix explicitly
- the repo does not provide a prejoined audio-plus-lyrics mega-table

## Theory Objectives

Students must be able to:

- state the singular value decomposition precisely
- connect SVD with PCA
- explain the low-rank approximation problem
- describe t-SNE as a neighborhood-preserving visualization objective
- explain why t-SNE is usually not a production-time replacement for linear feature reduction

## Singular Value Decomposition

For a matrix $X \in \mathbb{R}^{n \times d}$,

$$
X = U \Sigma V^\top,
$$

where:

- $U \in \mathbb{R}^{n \times r}$ has orthonormal columns
- $V \in \mathbb{R}^{d \times r}$ has orthonormal columns
- $\Sigma \in \mathbb{R}^{r \times r}$ is diagonal with singular values
  $$
  \sigma_1 \ge \sigma_2 \ge \cdots \ge \sigma_r > 0
  $$
- $r = \operatorname{rank}(X)$

## Truncated SVD

The best rank-$k$ approximation in Frobenius norm is

$$
X_k = U_k \Sigma_k V_k^\top.
$$

By the Eckart-Young theorem,

$$
X_k = \arg\min_{\operatorname{rank}(Y) \le k} \lVert X - Y \rVert_F.
$$

The squared reconstruction error is

$$
\lVert X - X_k \rVert_F^2 = \sum_{j=k+1}^r \sigma_j^2.
$$

This gives an exact spectral measure of what is lost under rank truncation.

## Relation Between PCA and SVD

If $X$ is centered, then

$$
X^\top X = V \Sigma^2 V^\top.
$$

Therefore:

- right singular vectors are eigenvectors of $X^\top X$
- squared singular values are proportional to covariance eigenvalues

So PCA on centered data can be computed through SVD.

## t-SNE Formulation

t-SNE constructs pairwise neighborhood probabilities in the high-dimensional space:

$$
p_{j|i} = \frac{\exp\left(-\lVert x_i - x_j \rVert_2^2 / 2\sigma_i^2\right)}{\sum_{k \ne i} \exp\left(-\lVert x_i - x_k \rVert_2^2 / 2\sigma_i^2\right)}.
$$

These are symmetrized into $p_{ij}$.
In the low-dimensional map with points $y_i$, t-SNE defines

$$
q_{ij} = \frac{(1 + \lVert y_i - y_j \rVert_2^2)^{-1}}{\sum_{k \ne l}(1 + \lVert y_k - y_l \rVert_2^2)^{-1}}.
$$

It then minimizes the Kullback-Leibler divergence

$$
\operatorname{KL}(P \Vert Q) = \sum_{i \ne j} p_{ij} \log \frac{p_{ij}}{q_{ij}}.
$$

Interpretation:

- large $p_{ij}$ values correspond to close neighbors in the original space
- t-SNE attempts to keep those neighbors close in the map
- global distances are not the primary preservation target

## Extended Theoretical Notes

### 1. Singular Values as Ordered Energy Levels

The singular values quantify how strongly the matrix varies along orthogonal directions.
Because

$$
\|X\|_F^2 = \sum_{j=1}^r \sigma_j^2,
$$

the squared singular values partition the total Frobenius energy of the matrix.
This gives a precise notion of retained information under rank truncation:

$$
\text{retained energy at rank } k
= \frac{\sum_{j=1}^k \sigma_j^2}{\sum_{j=1}^r \sigma_j^2}.
$$

### 2. Why SVD Is More General Than PCA

PCA is usually applied to a centered data matrix and interpreted through covariance.
SVD, by contrast, is a matrix factorization that applies whether or not the matrix is:

- square
- centered
- interpreted as a covariance structure

That is why SVD appears later in recommendation, text analysis, and low-rank approximation more broadly.

### 3. Latent Semantic Structure in Sparse Text

When SVD is applied to a term-document matrix, the low-rank factors often behave like latent semantic axes.
This does not mean the factors are uniquely interpretable.
It means co-occurrence patterns are being summarized in a lower-dimensional linear space.

For the lyric dataset, this is mathematically valuable because:

- vocabulary spaces are high-dimensional
- exact token matching is brittle
- low-rank structure can capture broader co-usage patterns

### 4. KL Divergence as an Asymmetric Objective in t-SNE

t-SNE minimizes

$$
\operatorname{KL}(P\|Q),
$$

not

$$
\operatorname{KL}(Q\|P).
$$

This asymmetry matters.
Roughly speaking, it penalizes failures to preserve high-probability neighbors from the original space more strongly than failures to preserve all global distances uniformly.

This is one reason t-SNE tends to preserve local neighborhoods well while distorting global geometry.

### 5. Optimization Caveats in t-SNE

t-SNE depends on:

- initialization
- perplexity
- learning rate
- random seed

Therefore the map is not a canonical geometric truth.
It is an optimization output under a particular parameterization.
Students should be trained to ask:

- is the structure stable under reruns?
- is the method being used for exploration or for operational compression?
- what notion of neighborhood does the perplexity imply?

## Mathematical Checkpoint

Students must be able to say exactly:

1. What truncated SVD optimizes.
2. Why PCA and SVD are closely related on centered data.
3. Why t-SNE is a visualization method, not a generic low-rank compression method.
4. Why a visually separated t-SNE plot is not itself a proof of cluster validity.

## Laboratory Session

## Mission

Compare representations, not just plots.

## Required tasks

1. On `pachamix_audio_core`, compare:
   - PCA projection
   - truncated SVD reconstruction
2. On an instructor-built lyric TF-IDF matrix from `pachamix_lyrics_long`, compare:
   - truncated SVD for semantic compression
   - t-SNE for visualization
3. For several values of $k$, measure:
   - explained variance or energy retained
   - reconstruction error
   - visual interpretability

## Required discussion

Students must answer:

- Which method is best for compression?
- Which method is best for visualization?
- Which method would they trust as preprocessing for downstream clustering?
- Which method would they not use directly in a production recommender pipeline, and why?

## Strict standards

- A beautiful plot is not an acceptable argument.
- Every low-dimensional representation must be evaluated against a stated objective.
- t-SNE runs must report hyperparameters such as perplexity and random seed.
- Reconstruction claims must include a quantitative error measure.

## Common failure modes

- comparing t-SNE with PCA as if they solve the same optimization problem
- forgetting that t-SNE is stochastic
- using t-SNE coordinates as if they preserved global Euclidean geometry
- claiming that low reconstruction error implies better class separation

## Extended Python Practice Session (2 Hours)

### Lab format

- `0:00-0:25` truncated SVD on the audio matrix
- `0:25-0:50` reconstruction error and retained energy
- `0:50-1:20` lyric-space TF-IDF plus truncated SVD
- `1:20-1:45` t-SNE visualization on a reduced representation
- `1:45-2:00` comparison of compression and visualization goals

### Python environment

```python
# Colab / fresh environment only
!pip install -q upc-datasets polars pyarrow numpy pandas matplotlib scikit-learn
```

### Guided notebook

#### 1. Audio-space truncated SVD

```python
import upc_datasets
import polars as pl
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD, PCA
from sklearn.manifold import TSNE

audio = upc_datasets.load_dataset("pachamix_audio_core", root="data/processed", download=False)
metadata_cols = ["track_id", "title", "genre_top", "artist_name"]
feature_cols = [c for c in audio.columns if c not in metadata_cols]

audio_small = audio.sample(n=min(2500, audio.height), seed=42)
X_audio = audio_small.select(feature_cols).fill_null(0.0).to_numpy()
X_audio = StandardScaler().fit_transform(X_audio)
```

#### 2. Compute SVD and retained energy

```python
U, s, Vt = np.linalg.svd(X_audio, full_matrices=False)
total_energy = np.sum(s ** 2)

rows = []
for k in [2, 5, 10, 20, 50]:
    Xk = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
    retained = np.sum(s[:k] ** 2) / total_energy
    mse = np.mean((X_audio - Xk) ** 2)
    rows.append({"k": k, "retained_energy": float(retained), "reconstruction_mse": float(mse)})

svd_summary = pl.DataFrame(rows)
svd_summary
```

#### 3. Build a compact lyric matrix

```python
lyrics = upc_datasets.load_dataset("pachamix_lyrics_long", root="data/processed", download=False)

top_tokens = (
    lyrics.group_by("token")
    .agg(pl.sum("count").alias("total_count"))
    .sort("total_count", descending=True)
    .head(300)
    .get_column("token")
    .to_list()
)

track_ids = lyrics.get_column("msd_track_id").unique().head(600).to_list()

lyrics_small = (
    lyrics.filter(pl.col("token").is_in(top_tokens) & pl.col("msd_track_id").is_in(track_ids))
    .group_by("msd_track_id", "token")
    .agg(pl.sum("count").alias("count"))
)

lyrics_wide = lyrics_small.pivot(index="msd_track_id", on="token", values="count").fill_null(0)
X_lyrics = lyrics_wide.drop("msd_track_id").to_numpy()
```

#### 4. Apply truncated SVD to lyric counts

```python
tsvd = TruncatedSVD(n_components=20, random_state=42)
Z_lyrics = tsvd.fit_transform(X_lyrics)

print("lyrics latent shape:", Z_lyrics.shape)
print("cumulative explained variance (20 comps):", float(tsvd.explained_variance_ratio_.sum()))
```

#### 5. Prepare a t-SNE visualization

```python
# Reduce first, then visualize.
# This is standard practice because direct t-SNE on very high-dimensional spaces is costly and noisy.

audio_pca_30 = PCA(n_components=30, random_state=42).fit_transform(X_audio)

tsne = TSNE(
    n_components=2,
    perplexity=30,
    learning_rate="auto",
    init="pca",
    random_state=42,
)
audio_tsne = tsne.fit_transform(audio_pca_30)
```

#### 6. Visualize the t-SNE embedding

```python
genre = audio_small.get_column("genre_top").fill_null("Unknown").to_numpy()

plt.figure(figsize=(7, 6))
for g in np.unique(genre)[:8]:
    idx = genre == g
    plt.scatter(audio_tsne[idx, 0], audio_tsne[idx, 1], s=8, alpha=0.5, label=g)

plt.xlabel("t-SNE dimension 1")
plt.ylabel("t-SNE dimension 2")
plt.title("t-SNE visualization of the audio feature space")
plt.legend(markerscale=2, fontsize=8)
plt.tight_layout()
plt.show()
```

#### 7. Compare retained energy visually

```python
svd_pdf = svd_summary.to_pandas()

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].plot(svd_pdf["k"], svd_pdf["retained_energy"], marker="o")
ax[0].set_title("Retained spectral energy")
ax[0].set_xlabel("k")
ax[0].set_ylabel("Energy ratio")

ax[1].plot(svd_pdf["k"], svd_pdf["reconstruction_mse"], marker="s")
ax[1].set_title("Reconstruction MSE")
ax[1].set_xlabel("k")
ax[1].set_ylabel("MSE")

plt.tight_layout()
plt.show()
```

### Mathematical demonstration in Python

Numerically verify

$$
\|X - X_k\|_F^2 = \sum_{j=k+1}^r \sigma_j^2.
$$

```python
for k in [2, 5, 10]:
    Xk = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
    lhs = np.linalg.norm(X_audio - Xk, ord="fro") ** 2
    rhs = np.sum(s[k:] ** 2)
    print(f"k={k:>2} -> lhs={lhs:.6f}, rhs={rhs:.6f}")
```

### Required exercises

1. Change the t-SNE perplexity to `10`, `50`, and `80`. How stable is the visual structure?
2. Compare a `20`-component PCA representation and a `20`-component truncated SVD representation on the audio matrix.
3. Increase the lyric vocabulary from `300` to `1000` tokens and observe the effect on truncated SVD.
4. Write one paragraph answering: which method would you use for compression, and which for visualization?

### Deliverables

- one SVD retained-energy table
- one reconstruction-error plot
- one t-SNE scatterplot
- one short numerical verification of the truncated-SVD error identity

## Bridge to Week 6

By the end of this week, students have learned to represent songs in cleaner low-dimensional spaces.
The next question is now operational:

how do we partition that space into meaningful groups?
