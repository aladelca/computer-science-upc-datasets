# Week 7 - DBSCAN, Density, and Cluster Validation

## Position in the Semester

- Arc: Discovering Structure
- Main dataset: `pachamix_audio_core`

## PachaMix Story Frame

### Cold Open

> Mathias: "K-means says these songs belong together."
>
> Yunguri: "Do they?"
>
> Mathias: "Not emotionally."

### Narrative Role of the Week

Students now confront the limits of centroid-based reasoning.
The week is successful only if they understand that different clustering algorithms encode different assumptions about geometry.

### Short Dialogue on the Core Concept

> Mathias: "DBSCAN found noise. I feel represented."
>
> Yunguri: "Good. Now distinguish outliers from parameter mistakes."
>
> Mathias: "Can epsilon be vibes-based?"
>
> Yunguri: "Only if the report is fiction."
>
> Mathias: "And `min_samples`?"
>
> Yunguri: "The number of neighbors required before you stop hallucinating structure."
>
> Mathias: "So density is local evidence, not global popularity."
>
> Yunguri: "Correct. One crowded region does not certify the whole map."

## Dataset Anchor in This Repo

Use `pachamix_audio_core`, preferably after:

- standardization
- optional PCA reduction to a moderate dimension

Why not the raw lyric long table directly?

- DBSCAN depends on a neighborhood structure
- extremely sparse text spaces are harder to interpret under naive Euclidean distance
- a reduced lyric embedding can be used as an optional extension, but the primary teaching dataset should remain the audio space

## Theory Objectives

Students must be able to:

- define epsilon-neighborhoods formally
- distinguish core, border, and noise points
- explain density reachability and density connectivity
- compare DBSCAN with K-means at the assumption level
- interpret cluster validation metrics critically

## Mathematical Formulation

Let $(\mathcal{X}, d)$ be a metric space.
For a point $x$ and radius $\epsilon > 0$, define the $\epsilon$-neighborhood

$$
N_\epsilon(x) = \{y \in \mathcal{X} : d(x,y) \le \epsilon\}.
$$

Given a threshold `minPts`, a point $x$ is a core point if

$$
|N_\epsilon(x)| \ge \text{minPts}.
$$

A point $y$ is directly density-reachable from a core point $x$ if

$$
y \in N_\epsilon(x).
$$

A point $y$ is density-reachable from $x$ if there exists a chain

$$
x = x_0, x_1, \dots, x_m = y
$$

such that each $x_{j+1}$ is directly density-reachable from $x_j$.

Two points are density-connected if there exists some point $z$ from which both are density-reachable.

Clusters are maximal density-connected sets.

## Conceptual Comparison with K-means

| Property | K-means | DBSCAN |
| --- | --- | --- |
| Main assumption | spherical / centroid-separable groups | locally dense regions |
| Number of clusters | must choose $K$ | emerges from density |
| Noise handling | poor | explicit |
| Outlier robustness | weak | stronger |
| Scale sensitivity | high | high |

DBSCAN is not "better."
It is better only when its geometric assumptions are better matched to the data.

## Validation Metrics

### Silhouette Score

For point $i$,

$$
s_i = \frac{b_i - a_i}{\max(a_i, b_i)},
$$

where:

- $a_i$ is mean distance to points in the same cluster
- $b_i$ is the smallest mean distance to points in another cluster

Average silhouette can be useful, but it is biased toward compact, well-separated clusters.
Therefore it is not always fair to density-based or non-convex structure.

### Davies-Bouldin Index

This index favors small intra-cluster scatter and large inter-cluster separation.
Again, it assumes a certain compactness logic and must not be used as an infallible oracle.

## Extended Theoretical Notes

### 1. DBSCAN as a Level-Set View of Density

Although DBSCAN is implemented through neighborhoods and graph-style reachability, its intuition is closely related to the idea that clusters correspond to dense regions of the sample space.

In that sense, DBSCAN is better aligned with the question:

> "Where does the data mass concentrate?"

than with the question:

> "Which centroid best summarizes this region?"

This is the conceptual reason it can recover irregular shapes.

### 2. Reachability Is Not Symmetry

Direct density reachability is not, in general, symmetric.
If $x$ is a core point and $y$ lies in its neighborhood, then $y$ may be directly density-reachable from $x$ even when the reverse is not true.

This asymmetry is why the definitions are layered:

- direct density reachability
- density reachability
- density connectivity

The final cluster definition uses density connectivity because it yields the right equivalence-like grouping behavior.

### 3. Parameter Meaning in High Dimension

The choice of $\epsilon$ is not merely a hyperparameter tweak.
It defines the scale at which locality is judged.
As dimension increases, neighborhoods become harder to calibrate because:

- distances concentrate
- relative local density becomes less stable
- small metric changes can alter adjacency structure sharply

This is one reason DBSCAN is often more reliable after dimension reduction than in raw ambient high-dimensional space.

### 4. Noise Is a Modeling Decision

DBSCAN's ability to label points as noise is a major strength, but it is still model-dependent.
A point is not "intrinsically noise."
It is noise relative to the density scale encoded by:

- the metric
- preprocessing
- $\epsilon$
- `minPts`

Thus the noise label must be interpreted as an analytical conclusion under a chosen geometric model, not as an ontological truth.

### 5. Why Validation Must Be Multi-Criteria

For density-based clustering, relying only on compactness-oriented metrics can be misleading.
A rigorous evaluation should combine:

- geometric plausibility
- metric summaries
- parameter sensitivity
- domain interpretability

This is methodologically stricter than accepting the output of any single cluster score.

## Mathematical Checkpoint

Students must be able to answer:

1. What is a core point?
2. What is density reachability?
3. Why can DBSCAN recover irregular shapes that K-means misses?
4. Why can a validation metric disagree with a visually plausible density structure?

## Laboratory Session

## Mission

Decide when density-based reasoning serves PachaMix better than centroid-based reasoning.

## Required tasks

1. Use the same representation used in Week 6 or justify a new one.
2. Run K-means and DBSCAN on the same data view.
3. Sweep multiple values of:
   - $\epsilon$
   - `minPts`
4. Record:
   - number of discovered clusters
   - number of noise points
   - silhouette score if defined
   - qualitative cluster geometry

## Required analysis

Students must identify:

- songs marked as noise
- whether those songs are true outliers or merely parameter casualties
- which algorithm better supports the pedagogical objective:
  discovering interpretable musical structure

## Strict standards

- Parameter values must be documented.
- A DBSCAN run that labels almost everything as noise is not automatically "robust."
- A K-means result with forced partitions is not automatically "useful."
- Validation must combine:
  - metric evidence
  - geometric evidence
  - domain interpretation

## Common failure modes

- using default parameters and pretending they are justified
- comparing algorithms on differently preprocessed feature spaces without saying so
- treating silhouette as universal truth
- ignoring the effect of standardization on neighborhood geometry

## Extended Python Practice Session (2 Hours)

### Lab format

- `0:00-0:20` prepare a reduced, standardized feature space
- `0:20-0:45` build a k-distance diagnostic for epsilon selection
- `0:45-1:15` run DBSCAN over multiple parameter settings
- `1:15-1:40` compare DBSCAN with K-means on the same representation
- `1:40-2:00` noise analysis and validation discussion

### Python environment

```python
# Colab / fresh environment only
!pip install -q upc-datasets polars pyarrow numpy pandas matplotlib scikit-learn
```

### Guided notebook

#### 1. Prepare the audio representation

```python
import upc_datasets
import polars as pl
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN, KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import silhouette_score

audio = upc_datasets.load_dataset("pachamix_audio_core", root="data/processed", download=False)
metadata_cols = ["track_id", "title", "genre_top", "artist_name"]
feature_cols = [c for c in audio.columns if c not in metadata_cols]

audio_small = audio.sample(n=min(3000, audio.height), seed=42)
X = audio_small.select(feature_cols).fill_null(0.0).to_numpy()
X = StandardScaler().fit_transform(X)
X_work = PCA(n_components=10, random_state=42).fit_transform(X)
```

#### 2. Build a k-distance plot for `minPts = 10`

```python
min_pts = 10
nn = NearestNeighbors(n_neighbors=min_pts)
nn.fit(X_work)
distances, _ = nn.kneighbors(X_work)

kdist = np.sort(distances[:, -1])

plt.figure(figsize=(8, 4))
plt.plot(kdist)
plt.xlabel("Points sorted by k-distance")
plt.ylabel(f"Distance to {min_pts}-th nearest neighbor")
plt.title("k-distance plot for DBSCAN epsilon selection")
plt.tight_layout()
plt.show()
```

#### 3. Sweep DBSCAN parameters

```python
rows = []
dbscan_runs = {}

for eps in [2.5, 3.0, 3.5, 4.0]:
    for min_pts in [5, 10, 15]:
        model = DBSCAN(eps=eps, min_samples=min_pts)
        labels = model.fit_predict(X_work)
        n_noise = int(np.sum(labels == -1))
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        if n_clusters >= 2 and np.sum(labels != -1) > n_clusters:
            sil = float(silhouette_score(X_work[labels != -1], labels[labels != -1]))
        else:
            sil = np.nan
        rows.append(
            {
                "eps": eps,
                "min_pts": min_pts,
                "n_clusters": n_clusters,
                "n_noise": n_noise,
                "noise_fraction": n_noise / len(labels),
                "silhouette_non_noise": sil,
            }
        )
        dbscan_runs[(eps, min_pts)] = labels

dbscan_summary = pl.DataFrame(rows).sort(["eps", "min_pts"])
dbscan_summary
```

#### 4. Compare with K-means on the same representation

```python
kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
kmeans_labels = kmeans.fit_predict(X_work)

print("K-means silhouette:", silhouette_score(X_work, kmeans_labels))
```

#### 5. Visualize one DBSCAN configuration

```python
eps, min_pts = 3.5, 10
labels = dbscan_runs[(eps, min_pts)]

plt.figure(figsize=(7, 6))
plt.scatter(X_work[:, 0], X_work[:, 1], c=labels, s=10, alpha=0.6, cmap="tab20")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title(f"DBSCAN in PCA space (eps={eps}, minPts={min_pts})")
plt.tight_layout()
plt.show()
```

#### 6. Inspect noise points

```python
noise_df = audio_small.select(["track_id", "title", "genre_top", "artist_name"]).with_columns(
    pl.Series("dbscan_label", labels)
).filter(pl.col("dbscan_label") == -1)

noise_df.head(10)
```

### Mathematical demonstration in Python

Density-based clustering is sensitive to neighborhood scale.
The k-distance plot is a computational proxy for the neighborhood radius that separates dense regions from sparse regions.

To quantify the effect, compare noise fraction as a function of `eps`:

```python
pdf = dbscan_summary.to_pandas()

plt.figure(figsize=(8, 4))
for min_pts in sorted(pdf["min_pts"].unique()):
    sub = pdf[pdf["min_pts"] == min_pts]
    plt.plot(sub["eps"], sub["noise_fraction"], marker="o", label=f"minPts={min_pts}")

plt.xlabel("eps")
plt.ylabel("Noise fraction")
plt.title("DBSCAN sensitivity to neighborhood radius")
plt.legend()
plt.tight_layout()
plt.show()
```

### Required exercises

1. Find one parameter setting where DBSCAN labels almost everything as noise. Explain why that happens geometrically.
2. Find one parameter setting where DBSCAN merges too many points. Explain why that also fails.
3. Compare DBSCAN and K-means on the same subset. Which method produces more interpretable outlier handling?
4. Explain why silhouette score can be unfair to non-convex clusters.

### Deliverables

- one DBSCAN parameter table
- one k-distance plot
- one DBSCAN scatterplot
- one comparison paragraph between DBSCAN and K-means

## Bridge to Week 8

Once the class can discover groups of songs, the next question changes from:

"Which songs resemble each other structurally?"

to:

"Which songs should PachaMix actually recommend?"
