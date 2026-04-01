# Week 4 - Principal Component Analysis

## Position in the Semester

- Arc: Fighting High Dimensionality
- Main dataset: `pachamix_audio_core`

## PachaMix Story Frame

### Cold Open

> Mathias: "Can we keep all the information and also reduce the dimensions?"
>
> Yunguri: "It sounds like a constrained optimization problem."

### Narrative Role of the Week

PCA is the first mathematically principled escape route from the raw feature space.
It must be taught as an optimization result, not as a magical plotting tool.

### Short Dialogue on the Core Concept

> Mathias: "So PCA keeps the important directions."
>
> Yunguri: "Variance-rich directions, not automatically emotionally important directions."
>
> Mathias: "What if the most dramatic feature has low variance?"
>
> Yunguri: "Then it may be dramatic and still mathematically unhelpful."
>
> Mathias: "So PCA compresses first and asks meaning later."
>
> Yunguri: "Correct. It is unsupervised elegance, not prophecy."
>
> Mathias: "Then principal components are new axes with better posture?"
>
> Yunguri: "Absurd phrasing. Technically acceptable."

## Dataset Anchor in This Repo

Use the numeric block of `pachamix_audio_core`.
The audio features are ideal because they are:

- high-dimensional enough to motivate reduction
- already numeric
- interpretable at the family level
- suitable for covariance-based analysis after centering and scaling

## Theory Objectives

Students must be able to:

- define covariance and projected variance
- derive PCA from a constrained optimization problem
- explain why eigenvectors of the covariance matrix define principal directions
- distinguish explained variance from semantic meaning

## Mathematical Setup

Let $X \in \mathbb{R}^{n \times d}$ be the centered data matrix, so each column has empirical mean zero.
The empirical covariance matrix is

$$
\Sigma = \frac{1}{n}X^\top X.
$$

For a unit vector $w \in \mathbb{R}^d$ with $\lVert w \rVert_2 = 1$, the scalar projection of $x_i$ is $w^\top x_i$.
The empirical variance along $w$ is

$$
\operatorname{Var}(Xw) = w^\top \Sigma w.
$$

## Derivation of the First Principal Component

We seek the direction of maximum projected variance:

$$
\max_{w \in \mathbb{R}^d} \quad w^\top \Sigma w
\quad \text{subject to} \quad
w^\top w = 1.
$$

Form the Lagrangian:

$$
\mathcal{L}(w, \lambda) = w^\top \Sigma w - \lambda(w^\top w - 1).
$$

Take the gradient with respect to $w$:

$$
\nabla_w \mathcal{L} = 2\Sigma w - 2\lambda w.
$$

Setting the gradient to zero yields

$$
\Sigma w = \lambda w.
$$

Thus any stationary point is an eigenvector of $\Sigma$.
The maximizer is the eigenvector associated with the largest eigenvalue $\lambda_1$.

Interpretation:

- the first principal component is the direction of maximum empirical variance
- the corresponding eigenvalue is the variance captured by that direction

## Multi-Component PCA

For $k$ components, let $W \in \mathbb{R}^{d \times k}$ satisfy

$$
W^\top W = I_k.
$$

Then the optimization problem is

$$
\max_{W^\top W = I_k} \operatorname{tr}(W^\top \Sigma W).
$$

The solution is given by the top $k$ eigenvectors of $\Sigma$.

## Reconstruction View

If $z_i = W^\top x_i$ and $\hat{x}_i = W z_i = W W^\top x_i$, then PCA also solves

$$
\min_{W^\top W = I_k} \sum_{i=1}^n \lVert x_i - W W^\top x_i \rVert_2^2.
$$

So PCA can be understood as both:

- variance maximization
- least-squares projection onto a $k$-dimensional subspace

## Extended Theoretical Notes

### 1. Rayleigh Quotient Interpretation

The first-component objective

$$
\max_{\|w\|_2=1} w^\top \Sigma w
$$

is a Rayleigh quotient problem.
For a symmetric matrix $\Sigma$, the Rayleigh quotient

$$
\mathcal{R}(w) = \frac{w^\top \Sigma w}{w^\top w}
$$

is maximized by the eigenvector associated with the largest eigenvalue.

This matters because it tells students that PCA is not an ad hoc recipe.
It is a direct consequence of a classical extremal property of symmetric matrices.

### 2. Orthogonality of Successive Components

Why must later components be orthogonal to earlier ones?
Because otherwise the same variance direction could be counted repeatedly.

The constrained problem for multiple components enforces

$$
W^\top W = I_k.
$$

This has two consequences:

- the component directions are mutually orthogonal
- the projected coordinates are uncorrelated in the empirical covariance sense

Thus PCA provides a decorrelated coordinate system aligned with maximal variance directions.

### 3. Spectral Ordering and Explained Variance

If the eigenvalues satisfy

$$
\lambda_1 \ge \lambda_2 \ge \cdots \ge \lambda_d \ge 0,
$$

then the explained variance ratio of the first $k$ components is

$$
\frac{\sum_{j=1}^k \lambda_j}{\sum_{j=1}^d \lambda_j}.
$$

This ratio has a clean interpretation:

- numerator: variance preserved in the retained subspace
- denominator: total variance in the centered data

It does not mean "semantic information preserved."
It means variance preserved under a specific second-order criterion.

### 4. PCA and Correlation Structure

If the features are on very different scales, covariance PCA may be dominated by high-variance coordinates.
Standardizing before PCA effectively moves from covariance-style thinking toward correlation-style thinking.

This is not a minor implementation detail.
It changes the optimization landscape because the matrix being diagonalized changes.

### 5. Limitations of PCA

PCA assumes that useful structure is captured by linear projections.
It will not generally preserve:

- nonlinear manifolds
- cluster separation if the variance directions do not align with labels
- local neighborhoods in the same way as nonlinear embedding methods

This is why the next week broadens the framework to SVD and t-SNE.

## Mathematical Checkpoint

Students must be able to reproduce:

1. The variance-maximization derivation.
2. The Lagrangian argument leading to the eigenvalue problem.
3. The interpretation of eigenvalues as explained variance.
4. The difference between maximizing variance and preserving semantic labels.

## Laboratory Session

## Mission

Build the first compressed map of the PachaMix audio space.

## Required tasks

1. Extract the numeric feature matrix from `pachamix_audio_core`.
2. Decide whether to standardize features and justify the decision.
3. Center the matrix.
4. Compute:
   - covariance matrix
   - eigenvalues
   - eigenvectors
5. Project tracks onto:
   - first principal component
   - first two principal components
   - first $k$ principal components for several values of $k$

## Required analysis

Students must report:

- cumulative explained variance curve
- first two-dimensional PCA map
- interpretation of which feature families dominate the first components
- whether `genre_top` becomes more separable after projection

## Strict standards

- No PCA plot is accepted without stating whether the input was standardized.
- "PC1 means happiness" is not an acceptable interpretation unless supported by loadings and domain evidence.
- Students must distinguish:
  - principal component scores
  - component loadings
  - explained variance ratios

## Common failure modes

- applying PCA directly to uncentered data
- treating a visualization as proof of cluster structure
- confusing correlation-scale reasoning with raw-scale covariance reasoning
- forgetting that components are linear combinations of the original features

## Extended Python Practice Session (2 Hours)

### Lab format

- `0:00-0:20` data preparation and centering
- `0:20-0:50` covariance matrix and eigen decomposition from scratch
- `0:50-1:20` projection, explained variance, and reconstruction
- `1:20-1:45` visualization in the first two principal components
- `1:45-2:00` interpretation and comparison with the formal derivation

### Python environment

```python
# Colab / fresh environment only
!pip install -q upc-datasets polars pyarrow numpy pandas matplotlib scikit-learn
```

### Guided notebook

#### 1. Load a manageable subset of the audio feature matrix

```python
import upc_datasets
import polars as pl
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA as SklearnPCA

audio = upc_datasets.load_dataset("pachamix_audio_core", root="data/processed", download=False)
metadata_cols = ["track_id", "title", "genre_top", "artist_name"]
feature_cols = [c for c in audio.columns if c not in metadata_cols]

audio_small = audio.sample(n=min(3000, audio.height), seed=42)
X_raw = audio_small.select(feature_cols).fill_null(0.0).to_numpy()
genre = audio_small.get_column("genre_top").fill_null("Unknown").to_numpy()
```

#### 2. Standardize, then center

```python
scaler = StandardScaler()
X = scaler.fit_transform(X_raw)

mu = X.mean(axis=0, keepdims=True)
X_centered = X - mu

print("Centered mean (first 5 coordinates):", X_centered.mean(axis=0)[:5])
```

#### 3. Compute covariance and eigen decomposition from scratch

```python
n = X_centered.shape[0]
cov = (X_centered.T @ X_centered) / n

eigvals, eigvecs = np.linalg.eigh(cov)
order = np.argsort(eigvals)[::-1]
eigvals = eigvals[order]
eigvecs = eigvecs[:, order]

explained_ratio = eigvals / eigvals.sum()
cum_explained = np.cumsum(explained_ratio)
```

#### 4. Project onto the principal components

```python
W2 = eigvecs[:, :2]
Z2 = X_centered @ W2

W10 = eigvecs[:, :10]
Z10 = X_centered @ W10

print("Projected shape in 2D:", Z2.shape)
print("Projected shape in 10D:", Z10.shape)
```

#### 5. Compare reconstruction error at multiple values of k

```python
ks = [2, 5, 10, 20, 50]
reconstruction_rows = []

for k in ks:
    Wk = eigvecs[:, :k]
    Zk = X_centered @ Wk
    X_hat = Zk @ Wk.T
    mse = np.mean((X_centered - X_hat) ** 2)
    reconstruction_rows.append(
        {
            "k": k,
            "reconstruction_mse": float(mse),
            "cumulative_explained_variance": float(cum_explained[k - 1]),
        }
    )

reconstruction_df = pl.DataFrame(reconstruction_rows)
reconstruction_df
```

#### 6. Visualize explained variance

```python
plt.figure(figsize=(8, 4))
plt.plot(np.arange(1, 21), explained_ratio[:20], marker="o", label="individual")
plt.plot(np.arange(1, 21), cum_explained[:20], marker="s", label="cumulative")
plt.xlabel("Principal component")
plt.ylabel("Explained variance ratio")
plt.title("PCA explained variance on the audio feature matrix")
plt.legend()
plt.tight_layout()
plt.show()
```

#### 7. Visualize the first two principal components

```python
genre_colors = {}
for g in np.unique(genre):
    genre_colors[g] = None

plt.figure(figsize=(7, 6))
for g in np.unique(genre)[:8]:
    idx = genre == g
    plt.scatter(Z2[idx, 0], Z2[idx, 1], s=8, alpha=0.5, label=g)

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("Audio tracks projected into the first two principal components")
plt.legend(markerscale=2, fontsize=8)
plt.tight_layout()
plt.show()
```

#### 8. Compare with scikit-learn PCA

```python
sk_pca = SklearnPCA(n_components=10, random_state=42)
Z_sk = sk_pca.fit_transform(X)

print("manual top-5 explained ratio:", explained_ratio[:5])
print("sklearn top-5 explained ratio:", sk_pca.explained_variance_ratio_[:5])
```

### Mathematical demonstration in Python

Verify numerically that the projected variance equals the leading eigenvalue:

```python
w1 = eigvecs[:, 0]
projected_var = np.var(X_centered @ w1)
leading_eigenvalue = eigvals[0]

print("projected variance on PC1 =", projected_var)
print("leading eigenvalue       =", leading_eigenvalue)
```

Up to small numerical differences in normalization convention, these quantities should agree.

### Required exercises

1. Repeat the experiment without standardization. Which feature families dominate the first components?
2. Find the smallest `k` such that cumulative explained variance exceeds:
   - `70%`
   - `80%`
   - `90%`
3. Compare reconstruction error using:
   - raw centered data
   - standardized data
4. Write one paragraph explaining why high explained variance does not automatically imply class separation.

### Deliverables

- one explained-variance plot
- one reconstruction table for several values of `k`
- one PC1-PC2 scatterplot
- one short verification that the first eigenvalue matches the variance of the first projected coordinate

## Bridge to Week 5

PCA is powerful, but it is not the only lens.
The next week broadens the picture:

- SVD for factorization and low-rank approximation
- t-SNE for local-neighborhood visualization
- a sharper distinction between compression and display
