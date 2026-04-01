# Week 6 - K-means and Prototype-Based Clustering

## Position in the Semester

- Arc: Discovering Structure
- Main dataset: `pachamix_audio_core`

## PachaMix Story Frame

### Cold Open

> Mathias: "I have decided there are exactly seven types of songs."
>
> Yunguri: "Based on what?"
>
> Mathias: "A feeling."

### Narrative Role of the Week

Students now move from representation to unsupervised structure discovery.
The week must make one methodological principle explicit:

algorithms are optimization procedures, not rituals.

### Short Dialogue on the Core Concept

> Mathias: "If I pick `K` confidently enough, is it scientific?"
>
> Yunguri: "Confidence is not a loss function."
>
> Mathias: "But the centroids look serious."
>
> Yunguri: "So do many errors."
>
> Mathias: "The elbow plot bent a little. I felt chosen."
>
> Yunguri: "The elbow plot owes you nothing."
>
> Mathias: "Then K-means wants spherical clusters and disciplined preprocessing?"
>
> Yunguri: "Exactly. At last, one sentence from you could survive peer review."

## Dataset Anchor in This Repo

`pachamix_audio_core` is the correct base dataset for K-means because:

- it provides dense numeric vectors
- it does not require cross-catalog matching
- it can be standardized and optionally reduced by PCA before clustering

Recommended practice:

- cluster on a standardized numeric matrix
- optionally use the first several principal components instead of the raw `518`-feature space

## Theory Objectives

Students must be able to:

- define clustering as an unsupervised partitioning problem
- write the K-means objective function exactly
- derive the centroid update rule
- explain why Lloyd's algorithm monotonically decreases the objective
- discuss initialization sensitivity and local minima

## Mathematical Formulation

Let:

- $x_i \in \mathbb{R}^d$ be the data points
- $\mu_k \in \mathbb{R}^d$ be cluster centroids
- $r_{ik} \in \{0,1\}$ indicate assignment of point $i$ to cluster $k$

subject to

$$
\sum_{k=1}^K r_{ik} = 1 \quad \text{for all } i.
$$

The K-means objective is

$$
J(R, \mu) = \sum_{i=1}^n \sum_{k=1}^K r_{ik}\lVert x_i - \mu_k \rVert_2^2.
$$

## Assignment Step

If centroids are fixed, the best assignment for each point is

$$
r_{ik} =
\begin{cases}
1 & \text{if } k = \arg\min_j \lVert x_i - \mu_j \rVert_2^2, \\
0 & \text{otherwise.}
\end{cases}
$$

This minimizes the contribution of point $i$ independently.

## Centroid Update Step

If assignments are fixed, the objective for cluster $k$ becomes

$$
\sum_{i: r_{ik}=1} \lVert x_i - \mu_k \rVert_2^2.
$$

Differentiate with respect to $\mu_k$:

$$
\frac{\partial}{\partial \mu_k}
\sum_{i: r_{ik}=1} \lVert x_i - \mu_k \rVert_2^2
= -2 \sum_{i: r_{ik}=1}(x_i - \mu_k).
$$

Setting the derivative to zero gives

$$
\mu_k = \frac{1}{n_k}\sum_{i: r_{ik}=1} x_i,
$$

where $n_k = \sum_i r_{ik}$.

Thus the centroid is the arithmetic mean of the assigned points.

## Monotonic Descent of Lloyd's Algorithm

Each full iteration alternates:

1. assignment with centroids fixed
2. centroid update with assignments fixed

Each substep exactly minimizes $J$ with respect to one block of variables, so:

$$
J^{(t+1)} \le J^{(t)}.
$$

Because the objective is bounded below by $0$, the sequence converges to a local optimum or stationary partition.

Important limitation:

- monotonic descent does not imply global optimality

## Practical Interpretation for PachaMix

When applied to song vectors, K-means assumes that useful groups are approximately:

- compact
- convex
- well represented by means

This can be useful for discovering broad audio moods or production styles.
It can fail badly on irregular or density-based structure.

## Extended Theoretical Notes

### 1. K-means as Coordinate Descent

Lloyd's algorithm is best understood as a block coordinate descent procedure over two variable sets:

- assignments $R$
- centroids $\mu$

It does not solve a joint convex optimization problem.
Instead, it alternates exact minimization over one block while holding the other fixed.

This explains both of its main properties:

- monotonic decrease of the objective
- vulnerability to local minima

### 2. Relation to Within-Cluster Variance Decomposition

For any cluster $C_k$ with centroid $\mu_k$,

$$
\sum_{x_i \in C_k} \|x_i - \mu_k\|_2^2
$$

measures within-cluster scatter.
The global K-means objective is the sum of these clusterwise scatters.

This connects K-means to variance decomposition:

- low within-cluster scatter means compact clusters
- high between-cluster separation is desirable but not explicitly optimized by the basic objective

That distinction matters.
K-means is not directly maximizing semantic separation.
It is minimizing squared reconstruction error around centroids.

### 3. Why Squared Euclidean Distance Is Special

The arithmetic mean is optimal because the loss is squared Euclidean distance.
If the objective were based on:

- $\ell_1$ distance
- cosine dissimilarity
- general Bregman divergences

the optimal representative would not necessarily be the arithmetic mean.

This is an important mathematical point:
the update rule is not universal.
It is a consequence of the particular geometry encoded in the objective.

### 4. Initialization Theory in Practice

Because the objective is non-convex in the joint variables, initialization matters.
Poor initialization can lead to:

- empty or tiny clusters
- slow convergence
- high final SSE

This is why practical implementations often use `k-means++`, whose goal is to spread initial centroids across the space.
The method does not guarantee global optimality, but it generally improves the starting configuration.

### 5. What K-means Is Really Optimizing

K-means is often marketed as if it "finds natural groups."
That is mathematically sloppy.
More precisely, it finds a partition that is locally good under:

$$
\text{squared-distance distortion to centroids}.
$$

That is a narrower claim, and it is the correct one.

## Mathematical Checkpoint

Students must be able to explain:

1. Why the centroid is the least-squares representative of a cluster.
2. Why each Lloyd step cannot increase the objective.
3. Why different initial seeds may produce different local optima.
4. Why K-means on unscaled raw features is often meaningless.

## Laboratory Session

## Mission

Build the first mood partition of the PachaMix audio universe.

## Required tasks

1. Choose a feature representation:
   - standardized full audio space, or
   - standardized PCA space
2. Run K-means for several values of $K$.
3. Use multiple random initializations.
4. Report:
   - within-cluster sum of squares
   - cluster sizes
   - centroid summaries
   - sample tracks nearest each centroid

## Recommended interpretation workflow

For each cluster:

- list dominant `genre_top` labels if present
- inspect a few representative tracks
- identify whether the cluster looks acoustically coherent

## Strict standards

- A chosen value of $K$ must be justified, even if only heuristically.
- A cluster label such as "study music" must not be assigned without evidence.
- Any comparison across runs must control random seed or explicitly report it.
- Students must report whether clustering was performed in raw feature space or reduced space.

## Common failure modes

- clustering on mixed-scale features without standardization
- choosing $K$ by aesthetics alone
- interpreting empty or tiny unstable clusters as profound discoveries
- assuming K-means works because it produced colored scatterplots

## Extended Python Practice Session (2 Hours)

### Lab format

- `0:00-0:20` data preparation and PCA-based working representation
- `0:20-0:50` one manual Lloyd iteration in Python
- `0:50-1:20` full K-means with multiple values of `K`
- `1:20-1:40` visualization and centroid inspection
- `1:40-2:00` interpretation and failure analysis

### Python environment

```python
# Colab / fresh environment only
!pip install -q upc-datasets polars pyarrow numpy pandas matplotlib scikit-learn
```

### Guided notebook

#### 1. Load and prepare the audio space

```python
import upc_datasets
import polars as pl
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

audio = upc_datasets.load_dataset("pachamix_audio_core", root="data/processed", download=False)
metadata_cols = ["track_id", "title", "genre_top", "artist_name"]
feature_cols = [c for c in audio.columns if c not in metadata_cols]

audio_small = audio.sample(n=min(4000, audio.height), seed=42)
X = audio_small.select(feature_cols).fill_null(0.0).to_numpy()
X = StandardScaler().fit_transform(X)

# Use a lower-dimensional working space for stable classroom experiments.
pca = PCA(n_components=10, random_state=42)
X_work = pca.fit_transform(X)
```

#### 2. Perform one manual Lloyd iteration

```python
rng = np.random.default_rng(42)
K = 6
init_idx = rng.choice(X_work.shape[0], size=K, replace=False)
centroids = X_work[init_idx].copy()

def assign_points(X, centroids):
    dists = np.linalg.norm(X[:, None, :] - centroids[None, :, :], axis=2)
    return np.argmin(dists, axis=1)

def update_centroids(X, labels, K):
    new_centroids = []
    for k in range(K):
        members = X[labels == k]
        if len(members) == 0:
            new_centroids.append(np.zeros(X.shape[1]))
        else:
            new_centroids.append(members.mean(axis=0))
    return np.vstack(new_centroids)

def sse_objective(X, labels, centroids):
    return float(np.sum((X - centroids[labels]) ** 2))

labels_0 = assign_points(X_work, centroids)
obj_0 = sse_objective(X_work, labels_0, centroids)

centroids_1 = update_centroids(X_work, labels_0, K)
labels_1 = assign_points(X_work, centroids_1)
obj_1 = sse_objective(X_work, labels_1, centroids_1)

print("objective before update:", obj_0)
print("objective after update :", obj_1)
```

#### 3. Run full K-means for several values of `K`

```python
rows = []
models = {}

for k in [4, 6, 8, 10]:
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(X_work)
    inertia = model.inertia_
    silhouette = silhouette_score(X_work, labels)
    rows.append({"k": k, "inertia": float(inertia), "silhouette": float(silhouette)})
    models[k] = (model, labels)

k_summary = pl.DataFrame(rows)
k_summary
```

#### 4. Visualize the partition in the first two principal coordinates

```python
chosen_k = 6
model, labels = models[chosen_k]

plt.figure(figsize=(7, 6))
plt.scatter(X_work[:, 0], X_work[:, 1], c=labels, s=10, alpha=0.6)
plt.scatter(model.cluster_centers_[:, 0], model.cluster_centers_[:, 1], c="black", s=100, marker="X")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title(f"K-means clustering in PCA space (K={chosen_k})")
plt.tight_layout()
plt.show()
```

#### 5. Inspect cluster composition

```python
cluster_df = audio_small.select(["track_id", "title", "genre_top", "artist_name"]).with_columns(
    pl.Series("cluster", labels)
)

cluster_summary = (
    cluster_df.group_by(["cluster", "genre_top"])
    .len()
    .sort(["cluster", "len"], descending=[False, True])
)

cluster_summary.head(20)
```

### Mathematical demonstration in Python

The week's proof claim is that Lloyd's steps do not increase the objective.
The manual step above should satisfy:

$$
J^{(1)} \le J^{(0)}.
$$

To reinforce the point, repeat the experiment with several random initializations:

```python
objective_rows = []

for seed in [1, 2, 3, 4, 5]:
    rng = np.random.default_rng(seed)
    init_idx = rng.choice(X_work.shape[0], size=K, replace=False)
    centroids = X_work[init_idx].copy()
    labels_a = assign_points(X_work, centroids)
    obj_a = sse_objective(X_work, labels_a, centroids)
    centroids_b = update_centroids(X_work, labels_a, K)
    labels_b = assign_points(X_work, centroids_b)
    obj_b = sse_objective(X_work, labels_b, centroids_b)
    objective_rows.append({"seed": seed, "before": obj_a, "after": obj_b})

pl.DataFrame(objective_rows)
```

### Required exercises

1. Compare clustering in:
   - the full standardized feature space
   - the 10-dimensional PCA space
2. Change `K` from `4` to `12` and discuss the elbow-versus-silhouette tradeoff.
3. For one cluster, inspect five tracks nearest the centroid and decide whether the cluster is interpretable.
4. Explain why a low SSE does not guarantee semantic usefulness.

### Deliverables

- one table of inertia and silhouette across several values of `K`
- one scatterplot with centroids
- one cluster-composition table using `genre_top`
- one short note explaining the monotonic-descent property observed in Python

## Bridge to Week 7

K-means is elegant, but its geometry is restrictive.
The next week asks what happens when clusters are irregular, noisy, or not well summarized by centroids.
