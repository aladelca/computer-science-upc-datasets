# Week 12 - PageRank on the Playlist Graph

## Position in the Semester

- Arc: Seeing Music as a Network
- Main dataset: `pachamix_song_graph_edges`

## PachaMix Story Frame

### Cold Open

> Mathias: "At last, an algorithm that tells us which songs are the kings of the graph."
>
> Yunguri: "Or central stochastic entities. Let us not let the notation become feudal."

### Narrative Role of the Week

This week is one of the mathematically richest in the semester.
Students must understand fixed points, stochastic matrices, and convergence, not merely call a library function.

### Short Dialogue on the Core Concept

> Mathias: "Teleportation in a Markov chain feels unfair."
>
> Yunguri: "It is regularization with theatrical flair."
>
> Mathias: "So the random walker is allowed drama?"
>
> Yunguri: "Only the mathematically justified kind."
>
> Mathias: "Then PageRank rewards nodes endorsed by important neighbors."
>
> Yunguri: "With damping, yes."
>
> Mathias: "So popularity alone is not enough?"
>
> Yunguri: "Correct. The prestige of the incoming path matters, not just the crowd size."

## Dataset Anchor in This Repo

The repository's graph output is:

- `pachamix_song_graph_edges`

with undirected weighted edges.

### Critical modeling step

PageRank is defined on a directed transition process.
Therefore, before applying PageRank, convert each undirected edge $(i,j,w)$ into two directed edges:

- $i \to j$ with weight $w$
- $j \to i$ with weight $w$

Only after that conversion should students build the transition matrix.

## Theory Objectives

Students must be able to:

- define PageRank as a fixed-point equation
- explain teleportation and dangling-node handling
- interpret PageRank as the stationary distribution of a modified Markov chain
- justify power iteration convergence at a rigorous high level

## Transition Matrix Construction

Let $A$ be the weighted directed adjacency matrix after symmetrizing the undirected edges into two directions.
Define the out-degree matrix

$$
D_{\text{out}} = \operatorname{diag}\left(\sum_j A_{1j}, \dots, \sum_j A_{nj}\right).
$$

Then the raw transition matrix is

$$
P = D_{\text{out}}^{-1} A.
$$

If a node has zero out-degree, it is dangling.
Its row must be replaced by a valid probability distribution.

## PageRank Equation

Let $\pi \in \mathbb{R}^n$ be the PageRank vector and $v$ a teleportation distribution, typically uniform.
With damping factor $\alpha \in (0,1)$,

$$
\pi = \alpha P^\top \pi + (1-\alpha)v.
$$

Equivalently, with the Google matrix

$$
G = \alpha P + (1-\alpha)\mathbf{1}v^\top,
$$

PageRank is the stationary distribution satisfying

$$
\pi^\top = \pi^\top G.
$$

## Why Damping Matters

Without damping:

- reducibility can create multiple stationary distributions
- dangling behavior can break the random walk
- convergence can depend sensitively on graph structure

With a strictly positive teleportation distribution, the Google matrix is positive.
By Perron-Frobenius reasoning:

- a unique stationary distribution exists
- it is strictly positive
- power iteration converges under standard conditions

## Power Iteration

Starting from some initial distribution $\pi^{(0)}$, iterate

$$
\pi^{(t+1)} = \alpha P^\top \pi^{(t)} + (1-\alpha)v.
$$

Stop when

$$
\lVert \pi^{(t+1)} - \pi^{(t)} \rVert_1 < \varepsilon
$$

for a chosen tolerance $\varepsilon$.

## Interpretation for PachaMix

Degree says:

- "this song co-occurs with many others"

PageRank says:

- "this song is connected to structurally important songs"

These are not the same statement.
In recommendation terms, PageRank can identify strong seeds or bridge tracks that do not maximize raw popularity alone.

## Extended Theoretical Notes

### 1. Fixed-Point Thinking

PageRank is pedagogically important because it trains students to reason with recursive definitions.
The statement

> "important nodes are linked from important nodes"

becomes mathematically meaningful only when written as a fixed-point equation.

This is a major conceptual advance from local metrics such as degree.

### 2. Stochastic Matrices and Stationary Distributions

If $P$ is row-stochastic and the chain is sufficiently well behaved, a stationary distribution $\pi$ satisfies

$$
\pi^\top = \pi^\top P.
$$

This means that if the chain is initialized in distribution $\pi$, it remains in that distribution after one transition step.

PageRank modifies this idea so that the resulting chain has stronger existence and uniqueness properties.

### 3. Why Teleportation Changes the Theory

Teleportation converts a potentially reducible or periodic walk into one with a more robust stochastic structure.
If the teleportation distribution is strictly positive, then the Google matrix has positive entries.

This yields, at a high level:

- irreducibility
- aperiodicity
- uniqueness of the stationary distribution

Students do not need a full proof of Perron-Frobenius at this stage, but they should understand what the theorem is buying them operationally.

### 4. Power Iteration as Repeated Propagation

Power iteration repeatedly applies the ranking operator.
Conceptually, it is a propagation scheme:

- current importance scores are pushed through the graph
- teleportation prevents pathological trapping
- repeated application stabilizes toward the fixed point

Thus PageRank sits at the intersection of:

- linear algebra
- probability
- iterative numerical methods

### 5. Dependence on Graph Definition

PageRank is not an intrinsic property of "the songs."
It is a property of the graph representation chosen.

If one changes:

- edge construction
- weighting
- filtering
- directionality rules

then the ranking may change materially.
This is one reason graph algorithms must always be interpreted together with the data-construction logic.

## Mathematical Checkpoint

Students must be able to explain:

1. Why the undirected repo graph must be converted into a directed transition structure.
2. Why damping ensures a well-defined unique ranking vector.
3. Why PageRank is a fixed-point problem.
4. Why PageRank and degree need not rank songs identically.

## Laboratory Session

## Mission

Rank songs by structural importance in the playlist ecosystem.

## Required tasks

1. Load `pachamix_song_graph_edges`.
2. Expand each undirected edge into two directed edges.
3. Build the weighted transition matrix.
4. Run power iteration for several values of $\alpha$, for example:
   - $\alpha = 0.70$
   - $\alpha = 0.85$
   - $\alpha = 0.95$
5. Compare:
   - PageRank ranking
   - weighted degree ranking

## Required reporting

Students must include:

- damping factor
- stopping tolerance
- number of iterations
- top-ranked songs
- at least one example where PageRank and weighted degree disagree

## Strict standards

- No PageRank implementation is accepted without a documented handling of dangling nodes.
- Students must state whether the teleportation vector was uniform or customized.
- A claim of convergence must cite an explicit stopping rule.
- Any interpretation of "importance" must refer to the graph construction used in this repo.

## Common failure modes

- using the undirected edge table directly as if it were already a transition matrix
- forgetting to normalize outgoing weights
- failing to renormalize probability mass after dangling correction
- interpreting PageRank as a universal measure of musical quality

## Extended Python Practice Session (2 Hours)

### Lab format

- `0:00-0:20` convert the undirected edge table into a directed transition structure
- `0:20-0:50` implement PageRank from scratch with damping
- `0:50-1:15` inspect convergence and top-ranked nodes
- `1:15-1:40` compare PageRank to weighted degree
- `1:40-2:00` discuss damping sensitivity

### Python environment

```python
# Colab / fresh environment only
!pip install -q upc-datasets polars pyarrow numpy pandas matplotlib networkx
```

### Guided notebook

#### 1. Load and filter the graph

```python
import upc_datasets
import polars as pl
import numpy as np
import matplotlib.pyplot as plt

edges = upc_datasets.load_dataset("pachamix_song_graph_edges", root="data/processed", download=False)
edges_small = edges.sort("weight", descending=True).head(3000)
edges_small.shape
```

#### 2. Expand each undirected edge into two directed edges

```python
src = edges_small.select(
    pl.col("src_track_uri").alias("u"),
    pl.col("dst_track_uri").alias("v"),
    pl.col("weight"),
)

dst = edges_small.select(
    pl.col("dst_track_uri").alias("u"),
    pl.col("src_track_uri").alias("v"),
    pl.col("weight"),
)

directed_edges = pl.concat([src, dst])
directed_edges.head(5)
```

#### 3. Build the transition matrix

```python
nodes = sorted(set(directed_edges.get_column("u").to_list()) | set(directed_edges.get_column("v").to_list()))
idx = {node: i for i, node in enumerate(nodes)}

A = np.zeros((len(nodes), len(nodes)), dtype=float)
for row in directed_edges.iter_rows(named=True):
    A[idx[row["u"]], idx[row["v"]]] += float(row["weight"])

row_sums = A.sum(axis=1)
P = np.divide(A, row_sums[:, None], out=np.zeros_like(A), where=row_sums[:, None] > 0)
```

#### 4. Implement PageRank with damping and dangling handling

```python
def pagerank_power_iteration(P, alpha=0.85, tol=1e-10, max_iter=500):
    n = P.shape[0]
    v = np.full(n, 1.0 / n)
    pi = np.full(n, 1.0 / n)
    history = []

    dangling = np.where(P.sum(axis=1) == 0)[0]
    P_work = P.copy()
    if len(dangling) > 0:
        P_work[dangling] = v

    for _ in range(max_iter):
        new_pi = alpha * (P_work.T @ pi) + (1 - alpha) * v
        err = np.linalg.norm(new_pi - pi, ord=1)
        history.append(err)
        pi = new_pi
        if err < tol:
            break

    return pi, history

pi, history = pagerank_power_iteration(P, alpha=0.85, tol=1e-10, max_iter=500)
len(history), history[-1]
```

#### 5. Rank songs and compare with weighted degree

```python
weighted_degree = A.sum(axis=1)

rank_df = pl.DataFrame(
    {
        "track_uri": nodes,
        "pagerank": pi,
        "weighted_degree": weighted_degree,
    }
)

rank_df.sort("pagerank", descending=True).head(10)
```

#### 6. Visualize convergence

```python
plt.figure(figsize=(8, 4))
plt.plot(history)
plt.yscale("log")
plt.xlabel("Iteration")
plt.ylabel("L1 error")
plt.title("PageRank power-iteration convergence")
plt.tight_layout()
plt.show()
```

#### 7. Compare PageRank with weighted degree

```python
pdf = rank_df.to_pandas()

plt.figure(figsize=(6, 5))
plt.scatter(pdf["weighted_degree"], pdf["pagerank"], alpha=0.6, s=12)
plt.xlabel("Weighted degree")
plt.ylabel("PageRank")
plt.title("Degree versus PageRank")
plt.tight_layout()
plt.show()
```

### Mathematical demonstration in Python

Check that the PageRank vector is a probability distribution and approximately satisfies the fixed-point equation:

```python
print("sum(pi) =", pi.sum())

v = np.full(len(nodes), 1.0 / len(nodes))
lhs = pi
rhs = 0.85 * (P.T @ pi) + 0.15 * v
print("fixed-point residual L1 =", np.linalg.norm(lhs - rhs, ord=1))
```

### Required exercises

1. Repeat the experiment for damping factors `0.70`, `0.85`, and `0.95`.
2. Identify one node whose PageRank rank is much higher than its weighted-degree rank.
3. Remove the dangling-node correction and observe what fails.
4. Explain why PageRank is a structural importance measure rather than a direct popularity measure.

### Deliverables

- one convergence plot
- one top-10 PageRank table
- one PageRank-versus-degree scatterplot
- one short explanation of why the undirected edge list must be expanded before ranking

## Bridge to Week 13

At this point PachaMix has become a serious analytical prototype.
The next step is not another model.
It is operational discipline:

the prototype must become a reproducible pipeline.
