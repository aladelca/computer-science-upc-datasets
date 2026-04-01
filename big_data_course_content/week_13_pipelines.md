# Week 13 - From Notebook to Pipeline

## Position in the Semester

- Arc: Making the System Real
- Main datasets: all processed PachaMix outputs
- Main operational references:
  - `README.md`
  - `runbooks/03-build-course-datasets.md`
  - `runbooks/04-test-and-verify.md`

## PachaMix Story Frame

### Cold Open

> Mathias: "The notebook works."
>
> Yunguri: "On whose machine?"

### Narrative Role of the Week

This week shifts the class from analysis to systems thinking.
Students must learn that reproducibility is a mathematical and engineering property, not a matter of style.

### Short Dialogue on the Core Concept

> Mathias: "I ran every cell. That is reproducibility."
>
> Yunguri: "That is choreography."
>
> Mathias: "Then what is a pipeline?"
>
> Yunguri: "A workflow that survives amnesia, restarts, and other people."
>
> Mathias: "If the file names are manual, the process is artisanal."
>
> Yunguri: "And fragile."
>
> Mathias: "So parameters, outputs, and dependencies must be explicit."
>
> Yunguri: "Exactly. Good engineering is memory externalized."

## Dataset Anchor in This Repo

The repo already provides a structured build workflow.
The canonical build command is:

```bash
.venv/bin/python -m upc_datasets.cli build-course-dataset \
  --raw-root data/raw \
  --processed-root data/processed
```

Equivalent builder command:

```bash
.venv/bin/python -m pachamix_data.cli build-course-dataset \
  --raw-root data/raw \
  --processed-root data/processed
```

This can produce:

- `data/processed/pachamix_audio_core.parquet`
- `data/processed/pachamix_lyrics_long.parquet`
- `data/processed/pachamix_playlists/playlist_events.parquet`
- `data/processed/pachamix_playlists/playlist_stats.parquet`
- `data/processed/pachamix_playlists/track_popularity.parquet`
- `data/processed/pachamix_song_graph_edges.parquet`

## Theory Objectives

Students must be able to:

- define a data pipeline as an ordered artifact-generating system
- distinguish batch from streaming workloads
- specify lineage between raw inputs and processed outputs
- quantify latency, throughput, and reproducibility constraints
- explain why hidden notebook state invalidates scientific repeatability

## Pipeline Abstraction

Represent the build as a directed acyclic graph of artifacts:

$$
\text{raw inputs} \to \text{intermediate transforms} \to \text{processed datasets} \to \text{models} \to \text{reports or services}.
$$

In this repo, a simplified lineage is:

$$
\text{FMA files} \to \texttt{pachamix\_audio\_core},
$$

$$
\text{musiXmatch/MSD files} \to \texttt{pachamix\_lyrics\_long},
$$

$$
\text{Playlist2vec / MPD files} \to \texttt{playlist\_events} \to \texttt{song\_graph\_edges}.
$$

## Quantitative Engineering Concepts

### Throughput

If a pipeline processes $N$ records in $\tau$ seconds, then

$$
\text{throughput} = \frac{N}{\tau}.
$$

### Latency

Latency is the delay from request or trigger to completed output.

### Reproducibility

Reproducibility means the pipeline yields the same artifact, up to controlled stochasticity, when run again under the same:

- code version
- parameter settings
- data snapshot
- runtime environment

### Drift

If the input distribution changes from $p_{\text{old}}(x)$ to $p_{\text{new}}(x)$, then a pipeline that once produced useful features or recommendations may degrade.
Operational systems must therefore measure stability over time.

## Notebook Versus Pipeline

A notebook is not a pipeline unless it has:

- defined inputs
- deterministic or controlled transformations
- documented outputs
- versioned dependencies
- rerunnable execution without hidden state

Yunguri's rule should be adopted literally:

> "Run all cells and hope" is not a deployment strategy.

## Extended Theoretical Notes

### 1. Pipelines as Composed Functions

At an abstract level, a reproducible pipeline is a composition of transformations:

$$
f = f_k \circ f_{k-1} \circ \cdots \circ f_1.
$$

Each stage should have:

- explicit inputs
- explicit outputs
- well-defined side effects

This functional view matters because it makes lineage and testing possible.

### 2. Determinism, Stochasticity, and Reproducibility

Not every pipeline stage must be deterministic.
But any stochastic stage must be controlled by:

- fixed seeds
- documented randomness sources
- repeated-run evaluation if variability matters

Thus reproducibility is not equivalent to determinism.
It is the ability to rerun a process under controlled conditions and obtain consistent or explainably variable results.

### 3. Data Validation as a Mathematical Guardrail

A pipeline step implicitly assumes:

- certain columns exist
- certain domains are valid
- certain null rates are tolerable
- certain distributions are not degenerate

These assumptions can be formalized as predicates.
For example:

$$
\text{null\_rate}(c) \le \tau
$$

for a chosen threshold $\tau$.

This is why validation is part of the theory of reliable systems, not mere engineering housekeeping.

### 4. Offline and Online Objectives Need Not Coincide

An offline workflow may optimize:

- reconstruction error
- cluster stability
- ranking quality on held-out data

But the deployed system must also satisfy:

- latency constraints
- freshness constraints
- artifact integrity

Therefore the operational objective is multi-criteria.
A pipeline is good only if it is both analytically valid and operationally executable.

### 5. Artifact Lineage as an Inference Trace

Every produced artifact should answer:

- from which raw sources was I built?
- with which parameters?
- under which code version?
- at what time?

This is not bureaucracy.
It is the minimal inference trace needed to defend results scientifically.

## Mathematical Checkpoint

Students must be able to explain:

1. Why reproducibility is a measurable systems property.
2. Why hidden state can invalidate an apparently successful result.
3. Why batch and streaming designs imply different latency and throughput objectives.
4. Why pipeline design must include artifact lineage, not just model code.

## Laboratory Session

## Mission

Turn one PachaMix analysis into a repeatable pipeline.

## Required tasks

1. Choose one prior workflow:
   - PCA / clustering
   - content recommendation
   - collaborative recommendation
   - graph ranking
2. Define:
   - input artifact(s)
   - output artifact(s)
   - preprocessing steps
   - evaluation step
3. Write a reproducible execution procedure.
4. State how the pipeline would fail if:
   - a raw file changes
   - a schema changes
   - a random seed changes

## Recommended repo-aligned deliverables

- one pipeline diagram
- one artifact lineage table
- one executable command or command sequence
- one verification checklist

## Strict standards

- Every artifact must have a source and destination path.
- Every pipeline must identify which parts are deterministic and which are stochastic.
- Every rerunnable workflow must name its dependencies and configuration parameters.
- A notebook screenshot is not accepted as a pipeline deliverable.

## Common failure modes

- reading from undocumented local paths
- relying on interactive state instead of explicit inputs
- mixing raw, interim, and processed files without lineage notes
- calling a workflow "production-ready" because it worked once

## Extended Python Practice Session (2 Hours)

### Lab format

- `0:00-0:20` choose one prior analytical workflow and define artifacts
- `0:20-0:50` refactor the workflow into pure functions
- `0:50-1:20` save metrics and outputs deterministically
- `1:20-1:40` add simple validation and timing instrumentation
- `1:40-2:00` discuss reproducibility failure modes

### Python environment

```python
# Colab / fresh environment only
!pip install -q upc-datasets polars pyarrow numpy pandas matplotlib scikit-learn
```

### Guided notebook

The example below converts a PCA plus K-means workflow into a small reproducible pipeline.

#### 1. Define configuration and artifact paths

```python
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import time

import upc_datasets
import polars as pl
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

@dataclass
class PipelineConfig:
    dataset_name: str = "pachamix_audio_core"
    sample_size: int = 4000
    n_components: int = 10
    n_clusters: int = 6
    random_state: int = 42
    output_dir: str = "artifacts/week13_pipeline"

cfg = PipelineConfig()
output_dir = Path(cfg.output_dir)
output_dir.mkdir(parents=True, exist_ok=True)
```

#### 2. Write pure pipeline functions

```python
def load_audio_sample(cfg: PipelineConfig) -> pl.DataFrame:
    audio = upc_datasets.load_dataset(cfg.dataset_name, root="data/processed", download=False)
    return audio.sample(n=min(cfg.sample_size, audio.height), seed=cfg.random_state)

def build_matrix(df: pl.DataFrame) -> tuple[np.ndarray, list[str]]:
    metadata_cols = ["track_id", "title", "genre_top", "artist_name"]
    feature_cols = [c for c in df.columns if c not in metadata_cols]
    X = df.select(feature_cols).fill_null(0.0).to_numpy()
    return X, feature_cols

def fit_representation_and_clusters(X: np.ndarray, cfg: PipelineConfig) -> dict:
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=cfg.n_components, random_state=cfg.random_state)
    Z = pca.fit_transform(X_scaled)

    kmeans = KMeans(n_clusters=cfg.n_clusters, random_state=cfg.random_state, n_init=10)
    labels = kmeans.fit_predict(Z)

    metrics = {
        "silhouette": float(silhouette_score(Z, labels)),
        "inertia": float(kmeans.inertia_),
        "explained_variance_sum": float(pca.explained_variance_ratio_.sum()),
    }

    return {
        "scaled": X_scaled,
        "embedding": Z,
        "labels": labels,
        "metrics": metrics,
    }
```

#### 3. Add timing and artifact persistence

```python
def run_pipeline(cfg: PipelineConfig) -> dict:
    t0 = time.perf_counter()
    df = load_audio_sample(cfg)
    X, feature_cols = build_matrix(df)
    fit = fit_representation_and_clusters(X, cfg)
    elapsed = time.perf_counter() - t0

    metrics = {
        **fit["metrics"],
        "runtime_seconds": elapsed,
        "n_rows": int(X.shape[0]),
        "n_features": int(X.shape[1]),
    }

    pl.DataFrame(
        {
            "pc1": fit["embedding"][:, 0],
            "pc2": fit["embedding"][:, 1],
            "cluster": fit["labels"],
        }
    ).write_parquet(output_dir / "embedding_clusters.parquet")

    with open(output_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    with open(output_dir / "config.json", "w", encoding="utf-8") as f:
        json.dump(asdict(cfg), f, indent=2)

    return metrics

metrics = run_pipeline(cfg)
metrics
```

#### 4. Validate artifacts

```python
assert (output_dir / "embedding_clusters.parquet").exists()
assert (output_dir / "metrics.json").exists()
assert (output_dir / "config.json").exists()

print("artifact validation passed")
```

#### 5. Inspect the persisted metrics

```python
with open(output_dir / "metrics.json", "r", encoding="utf-8") as f:
    saved_metrics = json.load(f)

saved_metrics
```

### Mathematical demonstration in Python

Quantitative engineering constraints are still numerical objects.
For example, compute throughput as

$$
\text{throughput} = \frac{N}{\tau}.
$$

```python
throughput = saved_metrics["n_rows"] / saved_metrics["runtime_seconds"]
print("rows per second:", throughput)
```

### Required exercises

1. Add a seed parameter to every stochastic stage and verify that rerunning the pipeline yields the same metrics.
2. Intentionally change `n_components` from `10` to `20`. Which artifacts change, and which should remain versioned?
3. Add a schema check that fails if a required column is missing.
4. Write one paragraph explaining how this pipeline differs from a notebook executed manually cell by cell.

### Deliverables

- one configuration file
- one metrics file
- one saved artifact table
- one paragraph explaining reproducibility risks and how the pipeline controls them

## Bridge to Week 14

Once the pipeline is reproducible, the last week asks the final operational questions:

- how is the system served?
- how is it monitored?
- how is failure detected and defended?
