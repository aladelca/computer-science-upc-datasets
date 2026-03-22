# Week 11 - Graph Analytics Foundations

## Position in the Semester

- Arc: Seeing Music as a Network
- Main datasets: `pachamix_playlist_events`, `pachamix_song_graph_edges`

## PachaMix Story Frame

### Cold Open

> Mathias: "I thought songs were rows in a table."
>
> Yunguri: "They are. Until they become nodes in a graph."

### Narrative Role of the Week

This week changes the representation itself.
Songs are no longer only feature vectors or matrix columns.
They become vertices in a co-occurrence network induced by playlists.

## Dataset Anchor in This Repo

### Input layer

- `pachamix_playlist_events`

This table gives one row per `(playlist_id, track_uri, position)`.

### Derived graph layer

- `pachamix_song_graph_edges`

This table gives one row per undirected song pair:

- `src_track_uri`
- `dst_track_uri`
- `weight`

The graph is built from playlist co-occurrence.

### Construction rule

If songs $i$ and $j$ appear together in a playlist, the edge weight increases.
Thus the graph captures behavioral proximity, not acoustic or lyrical similarity.

## Theory Objectives

Students must be able to:

- move between tabular, matrix, and graph views of the same phenomenon
- define adjacency, weighted degree, paths, and connectivity
- construct a transition matrix from a weighted graph
- explain how a random walk arises from playlist co-occurrence

## Graph Representation

Let $G = (V,E)$ be a weighted graph with $|V| = n$ songs.
Its weighted adjacency matrix is

$$
A \in \mathbb{R}^{n \times n},
$$

where

$$
A_{ij} =
\begin{cases}
w_{ij} & \text{if songs } i \text{ and } j \text{ co-occur}, \\
0 & \text{otherwise.}
\end{cases}
$$

For the undirected co-occurrence graph,

$$
A = A^\top.
$$

## Degree and Weighted Degree

The weighted degree of node $i$ is

$$
d_i = \sum_{j=1}^n A_{ij}.
$$

Define the diagonal degree matrix

$$
D = \operatorname{diag}(d_1, \dots, d_n).
$$

If $d_i > 0$ for all $i$, a row-stochastic transition matrix is

$$
P = D^{-1}A.
$$

Each row of $P$ sums to one, so $P$ defines a random walk:

$$
\Pr(X_{t+1}=j \mid X_t=i) = P_{ij}.
$$

## Why the Graph View Matters

A feature table answers questions about attributes.
A graph answers questions about structure such as:

- which songs occupy central positions
- which songs connect otherwise separate communities
- which songs act as bridges between listening patterns

This makes graph analysis a natural continuation of collaborative filtering.

## Centrality Preview

Before PageRank, students should understand simpler structural summaries:

- degree centrality
- weighted degree
- connected components
- bridge-like nodes

The point is not to memorize metrics.
The point is to understand what kind of structural importance each metric captures.

## Extended Theoretical Notes

### 1. Representation Determines the Question

The same musical ecosystem can be written as:

- a feature matrix
- an interaction matrix
- a graph

These are not interchangeable cosmetic formats.
They induce different mathematical objects and different admissible questions.

For example:

- feature matrices favor geometric similarity
- interaction matrices favor co-occurrence and missing-data reasoning
- graphs favor connectivity, flow, and structural centrality

This is one of the deepest conceptual moves in the course.

### 2. Adjacency Matrices as Linear Operators

The adjacency matrix is not just storage.
It acts as a linear operator on node-score vectors.
If $z \in \mathbb{R}^n$ is any score vector, then

$$
Az
$$

aggregates neighboring scores according to graph connectivity.

This operator viewpoint is essential because many graph algorithms, including PageRank, repeatedly apply matrix-based propagation.

### 3. Weighted Degree and Local Influence

Weighted degree is a first-order structural statistic:

$$
d_i = \sum_j A_{ij}.
$$

It says how much total edge mass touches node $i$.
But it remains local.
It does not account for whether the neighbors themselves are central, peripheral, or bridge-like.

Thus weighted degree is useful but incomplete, which motivates recursive ranking later.

### 4. Markov Interpretation Requires Normalization

A weighted adjacency matrix by itself is not a transition matrix.
To interpret movement on the graph probabilistically, rows must be normalized:

$$
P = D^{-1}A.
$$

Only then can one say that:

$$
P_{ij} = \Pr(X_{t+1}=j \mid X_t=i).
$$

This normalization step is conceptually crucial.
Without it, one has connectivity weights, not transition probabilities.

### 5. Graph Construction Choices Matter

If edges are created from full playlist co-occurrence, the graph captures broad co-membership structure.
If edges are created from sliding windows, the graph captures more local sequential proximity.

Thus graph analysis is only as meaningful as the edge-construction rule.
Students should always be trained to ask:

- what is a node?
- what is an edge?
- what does edge weight mean?
- what has been discarded in the construction?

## Mathematical Checkpoint

Students must be able to explain:

1. How to construct an adjacency matrix from playlist events.
2. Why a weighted co-occurrence graph encodes a different signal than feature similarity.
3. How degree normalization yields a transition matrix.
4. Why a random walk interpretation is mathematically natural once $P$ is row-stochastic.

## Laboratory Session

## Mission

Build the PachaMix song graph from playlist behavior and inspect its structure.

## Required tasks

1. Load `pachamix_song_graph_edges`.
2. Construct the weighted adjacency representation.
3. Compute:
   - node count
   - edge count
   - weighted degree distribution
   - connected component summary
4. Identify:
   - high-degree songs
   - potential bridge songs
   - whether popularity and structural connectivity coincide

## Suggested implementation note

Because the graph can grow quickly, students should:

- start with a classroom subset for local analysis
- document filtering rules if they restrict the graph

## Strict standards

- Any graph result must state exactly how edges were defined.
- Degree counts must distinguish:
  - unweighted degree
  - weighted degree
- A graph plot without a numeric summary is insufficient.
- Students must not interpret co-occurrence edges as causal relations.

## Common failure modes

- constructing self-loops accidentally
- forgetting that edge weights matter
- confusing popularity with structural centrality
- comparing graph results across differently filtered datasets without saying so

## Extended Python Practice Session (2 Hours)

### Lab format

- `0:00-0:20` load and inspect the co-occurrence edge list
- `0:20-0:45` build a weighted graph in Python
- `0:45-1:15` compute degree-based summaries and components
- `1:15-1:40` visualize a manageable subgraph
- `1:40-2:00` interpret centrality versus popularity

### Python environment

```python
# Colab / fresh environment only
!pip install -q upc-datasets polars pyarrow numpy pandas matplotlib networkx
```

### Guided notebook

#### 1. Load the song graph edges

```python
import upc_datasets
import polars as pl
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

edges = upc_datasets.load_dataset("pachamix_song_graph_edges", root="data/processed", download=False)
edges.shape
```

#### 2. Filter to a classroom-sized weighted graph

```python
edges_small = (
    edges.sort("weight", descending=True)
    .head(3000)
)

edges_small.head(5)
```

#### 3. Build the graph

```python
G = nx.Graph()

for row in edges_small.iter_rows(named=True):
    G.add_edge(row["src_track_uri"], row["dst_track_uri"], weight=row["weight"])

print("nodes:", G.number_of_nodes())
print("edges:", G.number_of_edges())
```

#### 4. Compute weighted degree and connected components

```python
weighted_degree = dict(G.degree(weight="weight"))

degree_df = (
    pl.DataFrame(
        {
            "track_uri": list(weighted_degree.keys()),
            "weighted_degree": list(weighted_degree.values()),
        }
    )
    .sort("weighted_degree", descending=True)
)

component_sizes = sorted((len(c) for c in nx.connected_components(G)), reverse=True)

print("largest component sizes:", component_sizes[:10])
degree_df.head(10)
```

#### 5. Build the adjacency and transition matrices on the giant component

```python
largest_component_nodes = max(nx.connected_components(G), key=len)
H = G.subgraph(largest_component_nodes).copy()

nodes = list(H.nodes())
idx = {node: i for i, node in enumerate(nodes)}

A = np.zeros((len(nodes), len(nodes)), dtype=float)
for u, v, data in H.edges(data=True):
    i, j = idx[u], idx[v]
    w = float(data["weight"])
    A[i, j] = w
    A[j, i] = w

d = A.sum(axis=1)
P = np.divide(A, d[:, None], out=np.zeros_like(A), where=d[:, None] > 0)

print("A shape:", A.shape)
print("Row sums of P (first 5):", P.sum(axis=1)[:5])
```

#### 6. Visualize a small subgraph

```python
top_nodes = degree_df.head(40).get_column("track_uri").to_list()
V = H.subgraph(top_nodes).copy()

plt.figure(figsize=(9, 7))
pos = nx.spring_layout(V, seed=42)
edge_widths = [0.2 + 0.02 * V[u][v]["weight"] for u, v in V.edges()]
node_sizes = [20 + 2 * V.degree(node, weight="weight") for node in V.nodes()]

nx.draw_networkx(
    V,
    pos=pos,
    with_labels=False,
    node_size=node_sizes,
    width=edge_widths,
    alpha=0.7,
)
plt.title("Weighted co-occurrence subgraph of top-degree songs")
plt.axis("off")
plt.show()
```

### Mathematical demonstration in Python

Verify that degree normalization creates a row-stochastic matrix:

```python
row_sums = P.sum(axis=1)
print("min row sum:", row_sums.min())
print("max row sum:", row_sums.max())
```

This numerically checks the claim

$$
\sum_j P_{ij} = 1
$$

for all nodes with positive degree.

### Required exercises

1. Compare unweighted degree and weighted degree. Which nodes change rank?
2. Restrict the graph to edges with `weight >= 2` and recompute the component structure.
3. Build the graph directly from `pachamix_playlist_events` and verify that it matches the edge dataset on a sample.
4. Explain why graph structure is not equivalent to acoustic similarity.

### Deliverables

- one summary of node count, edge count, and component sizes
- one table of top weighted-degree nodes
- one graph visualization
- one short note explaining how the transition matrix is built from the edge list

## Bridge to Week 12

Once the graph exists, the natural ranking question is no longer:

"Which songs have many neighbors?"

It becomes:

"Which songs are connected to important songs?"
