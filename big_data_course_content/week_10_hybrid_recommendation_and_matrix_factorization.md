# Week 10 - Hybrid Recommendation and Matrix Factorization

## Position in the Semester

- Arc: Recommending Music
- Main dataset: `pachamix_playlist_events`
- Optional matched enrichment: small capstone subset aligned with content features

## PachaMix Story Frame

### Cold Open

> Mathias: "What if we combine everything?"
>
> Yunguri: "That depends. Are you combining methods or just stacking optimism?"

### Narrative Role of the Week

This is the week where recommendation matures from local heuristics to learned latent structure.
It must also be the week where students learn not to lie about data integration.

## Dataset Anchor in This Repo

### Behavior-first baseline

The required part of the week should use:

- `pachamix_playlist_events`
- optional `pachamix_track_popularity`

This supports matrix factorization directly.

### Optional hybrid extension

A full hybrid recommender in this repository requires a small matched capstone subset because:

- playlist tracks live in the behavior catalog
- audio and lyrics live in different source families
- the repo does not provide a complete automatic crosswalk by default

Therefore there are two rigorously acceptable teaching variants:

1. Required baseline:
   teach hybrid scoring mathematically, but implement matrix factorization on the behavior matrix.
2. Optional advanced variant:
   create a manually validated matched subset and combine collaborative scores with content scores.

## Theory Objectives

Students must be able to:

- explain why content and collaborative methods fail in complementary ways
- define a weighted hybrid score
- derive the regularized matrix factorization objective
- write gradient updates for latent factors
- distinguish low-rank structure from mere memorization

## Hybrid Scoring

A simple hybrid score for playlist $p$ and candidate track $j$ is

$$
s_{\text{hybrid}}(p,j)
= \alpha s_{\text{content}}(p,j) + (1-\alpha)s_{\text{collab}}(p,j),
$$

with $0 \le \alpha \le 1$.

Interpretation:

- larger $\alpha$ favors item-description evidence
- smaller $\alpha$ favors behavior evidence

This formula is easy to state.
Its validity depends entirely on whether the scores refer to the same item universe.

## Matrix Factorization Objective

Let $R \in \mathbb{R}^{m \times n}$ be the playlist-track interaction matrix and $\Omega$ the set of observed entries.
We seek latent playlist factors $P \in \mathbb{R}^{m \times k}$ and latent track factors $Q \in \mathbb{R}^{n \times k}$.

The classical regularized objective is

$$
\min_{P,Q}
\sum_{(u,i)\in\Omega} \left(R_{ui} - p_u^\top q_i\right)^2
+ \lambda \sum_u \lVert p_u \rVert_2^2
+ \lambda \sum_i \lVert q_i \rVert_2^2.
$$

This is pedagogically convenient because it connects directly to least squares and low-rank approximation.

## Gradient Updates

For one observed pair $(u,i)$ with error

$$
e_{ui} = R_{ui} - p_u^\top q_i,
$$

the stochastic gradient updates are

$$
p_u \leftarrow p_u + \eta(e_{ui} q_i - \lambda p_u),
$$

$$
q_i \leftarrow q_i + \eta(e_{ui} p_u - \lambda q_i).
$$

These updates make the optimization logic explicit:

- fit observed interactions
- penalize large factor norms

## Low-Rank Interpretation

Matrix factorization assumes that observed behavior can be approximated by a small number of latent dimensions.
Those latent dimensions are not directly observed features.
They are learned coordinates that summarize co-occurrence structure.

This is why latent-factor models can recover meaningful structure even when explicit item descriptors are weak or unavailable.

## Important Methodological Warning

For implicit feedback, ranking-aware objectives are often preferable in real systems.
However, the squared-loss factorization objective remains an excellent teaching model because:

- it is mathematically transparent
- it exposes the low-rank idea cleanly
- it connects naturally to SVD-style thinking

## Extended Theoretical Notes

### 1. Hybridization as Bias-Variance and Information-Source Balancing

Content models and collaborative models fail differently:

- content models can generalize to new items but may overspecialize
- collaborative models can exploit collective behavior but suffer under sparsity and cold start

Hybridization is not just "combining scores."
It is a principled attempt to combine information sources with complementary failure modes.

### 2. Why Low-Rank Factorization Is a Structural Assumption

Matrix factorization assumes the large interaction matrix can be approximated by:

$$
R \approx P Q^\top
$$

with $k \ll \min(m,n)$.

This is a strong structural claim:

- preferences and items live in a low-dimensional latent space
- observed interactions are generated approximately by inner products in that space

The model succeeds when this low-rank hypothesis is sufficiently accurate.

### 3. Regularization as Capacity Control

The penalty

$$
\lambda \sum_u \|p_u\|_2^2 + \lambda \sum_i \|q_i\|_2^2
$$

controls the scale of the latent factors.
Without it, the model may fit observed entries too aggressively and generalize poorly.

Regularization is therefore not a numerical trick.
It is the formal mechanism that constrains factor magnitude and limits overfitting.

### 4. Missing Data and the Difference from Classical SVD

Classical SVD factorizes a fully observed matrix.
Recommendation matrices are only partially observed.
Therefore matrix factorization for recommendation is not identical to taking the SVD of the raw interaction table.

The optimization is over observed entries:

$$
(u,i) \in \Omega,
$$

which means the model is learning under missingness rather than under full-matrix reconstruction.

### 5. Interpretation Limits of Latent Dimensions

Latent factors may correlate with intuitive notions such as mood, popularity, or genre blending.
But the factor coordinates are identified only up to rotations and sign changes under many formulations.

So statements like:

> "Factor 3 means sadness."

are generally too strong unless supported by additional evidence.
The correct language is:

> "Factor 3 appears empirically associated with a certain behavioral pattern."

## Mathematical Checkpoint

Students must be able to explain:

1. Why hybrid systems often outperform single-signal systems.
2. Why matrix factorization is a latent representation model.
3. What regularization does in the objective.
4. Why a hybrid implementation is only legitimate if the underlying item identity mapping is legitimate.

## Laboratory Session

## Mission

Build the most mature recommender seen so far, without violating the repo's data constraints.

## Required tasks

### Required baseline

1. Build a playlist-track matrix from `pachamix_playlist_events`.
2. Train a low-rank latent-factor model.
3. Compare against:
   - popularity baseline
   - neighborhood collaborative baseline

### Optional advanced extension

If the instructor has created a matched capstone subset:

1. compute a content score on the matched catalog
2. combine it with the collaborative or latent-factor score
3. sweep $\alpha$

## Required reporting

Students must include:

- latent dimension $k$
- regularization strength $\lambda$
- optimization schedule or stopping rule
- evaluation metric
- baseline comparison
- explicit statement of whether a real matched content-behavior subset was used

## Strict standards

- No student may claim to have built a hybrid recommender unless the item identity alignment is documented.
- Latent factors must not be described as "genres" or "moods" unless interpretation is supported empirically.
- A matrix factorization result without a baseline is incomplete.
- Hyperparameter choices must be stated, not hidden inside library defaults.

## Common failure modes

- claiming hybrid gains without a valid cross-catalog match
- overinterpreting latent dimensions
- reporting only one run of a stochastic optimizer
- comparing models under different candidate pools

## Extended Python Practice Session (2 Hours)

### Lab format

- `0:00-0:20` prepare a classroom-sized playlist-track matrix
- `0:20-0:55` implement matrix factorization with SGD
- `0:55-1:20` monitor loss and inspect latent predictions
- `1:20-1:40` compare with a popularity or similarity baseline
- `1:40-2:00` optional hybrid-score extension on a matched subset

### Python environment

```python
# Colab / fresh environment only
!pip install -q upc-datasets polars pyarrow numpy pandas matplotlib scikit-learn
```

### Guided notebook

#### 1. Rebuild a compact playlist-track matrix

```python
import upc_datasets
import polars as pl
import numpy as np
import matplotlib.pyplot as plt

events = upc_datasets.load_dataset("pachamix_playlist_events", root="data/processed", download=False)
popularity = upc_datasets.load_dataset("pachamix_track_popularity", root="data/processed", download=False)
playlist_stats = upc_datasets.load_dataset("pachamix_playlist_stats", root="data/processed", download=False)

active_playlists = (
    playlist_stats.filter(pl.col("track_count") >= 8)
    .head(400)
    .get_column("playlist_id")
    .to_list()
)

top_tracks = popularity.sort("playlist_count", descending=True).head(300).get_column("track_uri").to_list()

events_small = events.filter(
    pl.col("playlist_id").is_in(active_playlists) & pl.col("track_uri").is_in(top_tracks)
)

matrix_df = (
    events_small.select(["playlist_id", "track_uri"])
    .with_columns(pl.lit(1.0).alias("value"))
    .pivot(index="playlist_id", on="track_uri", values="value")
    .fill_null(0.0)
)

playlist_ids = matrix_df.get_column("playlist_id").to_list()
track_cols = [c for c in matrix_df.columns if c != "playlist_id"]
R = matrix_df.drop("playlist_id").to_numpy().astype(float)

R.shape
```

#### 2. Hold out one positive item per playlist for evaluation

```python
rng = np.random.default_rng(42)
R_train = R.copy()
held_out = {}

for u in range(R.shape[0]):
    pos = np.where(R[u] > 0)[0]
    if len(pos) >= 2:
        i = rng.choice(pos)
        R_train[u, i] = 0.0
        held_out[u] = int(i)

len(held_out)
```

#### 3. Train a simple matrix factorization model

```python
n_users, n_items = R_train.shape
k = 20
lr = 0.03
reg = 0.01
epochs = 20

P = 0.1 * rng.standard_normal((n_users, k))
Q = 0.1 * rng.standard_normal((n_items, k))

observed_pairs = np.argwhere(R_train > 0)
loss_history = []

for epoch in range(epochs):
    rng.shuffle(observed_pairs)
    for u, i in observed_pairs:
        pred = P[u] @ Q[i]
        err = R_train[u, i] - pred
        p_old = P[u].copy()
        q_old = Q[i].copy()
        P[u] += lr * (err * q_old - reg * p_old)
        Q[i] += lr * (err * p_old - reg * q_old)

    pred_matrix = P @ Q.T
    obs_pred = pred_matrix[R_train > 0]
    obs_true = R_train[R_train > 0]
    loss = np.mean((obs_true - obs_pred) ** 2) + reg * (np.mean(P ** 2) + np.mean(Q ** 2))
    loss_history.append(float(loss))

loss_history[:5], loss_history[-5:]
```

#### 4. Evaluate hit-rate at 10

```python
pred_matrix = P @ Q.T
hits = 0
tested = 0

for u, i_true in held_out.items():
    scores = pred_matrix[u].copy()
    scores[R_train[u] > 0] = -np.inf
    top10 = np.argsort(scores)[::-1][:10]
    hits += int(i_true in top10)
    tested += 1

hit_rate_at_10 = hits / tested
print("MF hit-rate@10:", hit_rate_at_10)
```

#### 5. Compare with popularity baseline

```python
track_pop_rank = popularity.sort("playlist_count", descending=True).get_column("track_uri").to_list()
track_to_idx = {track_uri: idx for idx, track_uri in enumerate(track_cols)}
popular_idx = [track_to_idx[uri] for uri in track_pop_rank if uri in track_to_idx]

hits_pop = 0
tested = 0
for u, i_true in held_out.items():
    observed = set(np.where(R_train[u] > 0)[0])
    pred = [idx for idx in popular_idx if idx not in observed][:10]
    hits_pop += int(i_true in pred)
    tested += 1

print("Popularity hit-rate@10:", hits_pop / tested)
```

#### 6. Visualize the optimization curve

```python
plt.figure(figsize=(8, 4))
plt.plot(loss_history, marker="o")
plt.xlabel("Epoch")
plt.ylabel("Regularized training loss")
plt.title("Matrix factorization optimization")
plt.tight_layout()
plt.show()
```

### Mathematical demonstration in Python

The code implements the updates

$$
p_u \leftarrow p_u + \eta(e_{ui} q_i - \lambda p_u), \qquad
q_i \leftarrow q_i + \eta(e_{ui} p_u - \lambda q_i).
$$

Check numerically that the training loss decreases across epochs:

```python
for epoch, loss in enumerate(loss_history, start=1):
    print(epoch, loss)
```

### Optional hybrid extension

If, and only if, the instructor has built a valid matched content-behavior subset:

```python
# Suppose content_scores and collab_scores are aligned to the same candidate track set.
alpha = 0.3
hybrid_scores = alpha * content_scores + (1 - alpha) * collab_scores
```

Without a documented cross-catalog match, this step must remain theoretical.

### Required exercises

1. Change the latent dimension from `20` to `10` and `50`. How does hit-rate@10 change?
2. Change the regularization strength. What happens to the loss curve?
3. Compare MF hit-rate@10 with the popularity baseline. Does added complexity help?
4. Write one paragraph explaining why the hybrid extension is conditional in this repo.

### Deliverables

- one loss-versus-epoch plot
- one hit-rate comparison against a baseline
- one short note interpreting the role of latent dimension and regularization
- one explicit statement on whether a true matched hybrid experiment was or was not possible

## Bridge to Week 11

At this point PachaMix can rank songs by content and by behavior.
The next conceptual leap is to notice that behavior also creates a network, and networks carry structure beyond matrix entries alone.
