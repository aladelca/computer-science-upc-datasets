# Week 1 - Big Data, Advanced Analytics, and Data Science

## Position in the Semester

- Arc: Framing the Problem
- Main datasets: `pachamix_audio_core`
- Supporting repo documents:
  - `big_data_14_week_plan.md`
  - `big_data_dataset_generation_plan.md`
  - `big_data_pachamix_narrative_script.md`
  - `data_dictionary.md`

## PachaMix Story Frame

### Cold Open

> Mathias: "I have a genius idea. A playlist assistant for students."
>
> Yunguri: "That sentence has committed no crime yet. Continue."

### Narrative Role of the Week

This week exists to stop the project from collapsing into vague enthusiasm.
Mathias wants "an app that recommends songs." Yunguri insists on five prior questions:

1. What data do we have?
2. What data do we wish we had?
3. What exact question are we answering?
4. What decision will the system support?
5. What counts as success?

The correct intellectual mood is disciplined skepticism.

## Dataset Anchor in This Repo

Use `pachamix_audio_core` as the first classroom dataset because it is structured, tabular, and numerically rich.

### Relevant facts from the repo

- Grain: one row per FMA track.
- Current documented shape: `106,574 x 522`.
- Four high-level metadata fields are immediately interpretable:
  - `track_id`
  - `title`
  - `genre_top`
  - `artist_name`
- The remaining `518` columns are numeric audio descriptors.

### Why this is pedagogically useful

- It is large enough to justify memory, storage, and throughput analysis.
- It is clean enough for first-week inspection.
- It does not require raw audio decoding.
- It already demonstrates the difference between metadata and feature matrices.

## Theory Objectives

By the end of the week, students must be able to:

- distinguish Big Data from generic "lots of data" rhetoric
- place machine learning inside the broader analytics workflow
- separate product questions from modeling questions
- estimate whether a dataset fits comfortably in local memory
- justify when a single-machine workflow is acceptable and when it is not

## Conceptual Core

### 1. Big Data Is Not Defined by Hype

The phrase "Big Data" is meaningful only when scale or complexity alters method choice.
The usual `5Vs` are:

- volume
- velocity
- variety
- veracity
- value

A dataset is not "big" because it looks intimidating.
It is "big" when at least one of the following changes:

- the computational architecture
- the storage strategy
- the algorithmic design
- the evaluation protocol

### 2. Analytics Is a Family of Tasks

The same course dataset can support multiple analytics questions.

| Analytics type | Formal question | PachaMix example |
| --- | --- | --- |
| Descriptive | What is happening? | What genres dominate the current catalog? |
| Diagnostic | Why is it happening? | Why do some feature clusters contain mixed genres? |
| Predictive | What will happen? | Which song is likely to fit a future playlist? |
| Prescriptive | What should we do? | Which top-`k` songs should PachaMix recommend now? |

### 3. Data Science Is a Workflow, Not a Synonym for Modeling

Data science includes:

- data acquisition
- schema understanding
- cleaning
- feature construction
- modeling
- evaluation
- deployment
- monitoring

Machine learning is one component of that pipeline, not the whole pipeline.

## Mathematical Development

### 1. Memory Footprint

Let:

- $n$ be the number of rows
- $d$ be the number of numeric columns
- $b$ be the bytes per stored value

Then a first-order numeric memory estimate is

$$
M \approx ndb.
$$

For the numeric block of `pachamix_audio_core`,

$$
n = 106{,}574, \qquad d = 518, \qquad b = 8 \text{ bytes for Float64}.
$$

Hence

$$
M \approx 106{,}574 \times 518 \times 8 = 441{,}642{,}656 \text{ bytes} \approx 421.18 \text{ MiB}.
$$

This estimate excludes:

- string columns
- indexing overhead
- temporary copies created during preprocessing
- additional memory consumed by linear algebra routines

Therefore, "it fits in memory" is not the same as "it is safe to process casually."

### 2. Throughput and Latency

If a system processes $N$ records in time $\tau$, then throughput is

$$
\text{throughput} = \frac{N}{\tau}.
$$

If a single request takes time $\ell$, then $\ell$ is latency.

This distinction matters immediately:

- model training often optimizes throughput
- user-facing serving often optimizes latency

### 3. Data Size Versus Algorithmic Complexity

An algorithm with cost $O(nd)$ may be acceptable on the full audio table.
An algorithm with cost $O(n^2d)$ may already be problematic.
For $n = 106{,}574$,

$$
n^2 \approx 1.136 \times 10^{10},
$$

which means naive pairwise comparison is already expensive before any constant factors are considered.

This is why course topics such as dimensionality reduction and approximate structure discovery are not optional decoration.

## Extended Theoretical Notes

### 1. Formal Separation Between Data Complexity and Model Complexity

Students often speak imprecisely about "a complex problem" as if there were only one source of complexity.
This is mathematically weak.
At minimum, the following quantities must be separated:

- `data complexity`
  quantified by sample count, feature dimension, missingness pattern, heterogeneity, and update frequency
- `model complexity`
  quantified by hypothesis-class richness, parameter count, VC-style capacity intuition, or functional flexibility
- `computational complexity`
  quantified by time and memory cost of the algorithm used to fit or query the model

These are related but not identical.
For example:

- a low-capacity linear model may still be expensive if trained on massive data
- a high-capacity model may be computationally cheap on small data
- a moderate-size table may still be operationally difficult if it is updated rapidly or stored across many files

### 2. A Minimal Cost Model for Analytical Workflows

Suppose a workflow has three major stages:

1. load data
2. transform data
3. compute a learning or ranking result

Then total runtime can be idealized as

$$
T_{\text{total}} = T_{\text{I/O}} + T_{\text{transform}} + T_{\text{algorithm}}.
$$

This decomposition matters because many failures attributed to "slow models" are actually:

- storage bottlenecks
- repeated serialization costs
- unnecessary copies in memory

It is bad analytical hygiene to discuss runtime without naming which term dominates.

### 3. Why Quadratic and Cubic Growth Are Strategic Boundaries

If an algorithm has complexity:

$$
O(n), \quad O(n \log n), \quad O(nd),
$$

then doubling the data may still be manageable.
But if the algorithm has cost

$$
O(n^2), \quad O(n^2d), \quad O(n^3),
$$

then scale changes strategy.

For example, if $n \approx 10^5$, then:

$$
n^2 \approx 10^{10}, \qquad n^3 \approx 10^{15}.
$$

Even before considering implementation constants, these orders indicate that:

- exact pairwise methods may require approximation
- matrix decompositions may require randomized or truncated variants
- classroom workflows must often use subsets or reduced representations

### 4. Why Big Data Is About Regime Change

The mathematically correct way to explain Big Data is not:

> "There is a lot of data."

It is:

> "The scale or structure of the data forces a different computational regime."

The regime changes may include:

- in-memory to out-of-core processing
- local execution to distributed execution
- exact methods to approximate methods
- manual analysis to pipeline-based repeated execution

This is the week's core theoretical idea.

## Mathematical Checkpoint

Students should be able to state and justify the following claims precisely:

1. A dataset can be moderate in row count but difficult because of dimensionality, heterogeneity, or update rate.
2. A method that is valid on `10,000` rows can fail at `10,000,000` rows because asymptotic growth matters.
3. Memory feasibility must include both stored data and computational working memory.
4. Product language such as "predict vibes" is not a formal objective.

## Laboratory Session

## Mission

Audit the course data before making any modeling promise.

## Required Dataset

- `pachamix_audio_core`

## Suggested loading path

```python
import upc_datasets

audio = upc_datasets.load_dataset("pachamix_audio_core", root="data/processed")
print(audio.shape)
```

If the dataset has not been built yet, the instructor must rebuild it before the lab.

## Mandatory tasks

1. Separate metadata columns from numeric feature columns.
2. Count null values by column family.
3. Estimate the numeric memory footprint of the matrix.
4. Propose:
   - one descriptive question
   - one predictive question
   - one prescriptive question
5. Explain which of those questions can be answered this week and which cannot.

## Deliverable format

Students submit:

- one schema summary table
- one quantitative memory estimate
- one paragraph defining three analytics questions
- one paragraph explaining why only some of them are currently operational

## Strict standards

- "Interesting dataset" is not an acceptable conclusion.
- Every memory estimate must show the arithmetic.
- Every analytics question must identify:
  - input data
  - target output
  - decision supported
- Any claim that the dataset is "too big" or "small enough" must cite a concrete quantitative criterion.

## Frequent Errors to Correct Immediately

- treating Big Data as a synonym for machine learning
- confusing `genre_top` with a universally reliable label
- using only row count and ignoring feature count
- forgetting that string-heavy tables often consume much more memory than raw numeric estimates suggest
- claiming production readiness after a single notebook inspection

## Extended Python Practice Session (2 Hours)

### Lab format

- `0:00-0:20` dataset loading, schema inspection, and feature-family audit
- `0:20-0:45` memory and storage calculations in Python
- `0:45-1:15` pairwise-matrix feasibility analysis and simple visualization
- `1:15-1:45` formulation of descriptive, predictive, and prescriptive questions
- `1:45-2:00` short technical write-up and instructor discussion

### Python environment

```python
# Colab / fresh environment only
!pip install -q upc-datasets polars pyarrow numpy pandas matplotlib
```

### Guided notebook

#### 1. Load the processed audio dataset

```python
import upc_datasets
import polars as pl
import numpy as np
import matplotlib.pyplot as plt

audio = upc_datasets.load_dataset(
    "pachamix_audio_core",
    root="data/processed",   # change if your processed folder is elsewhere
    download=False,          # change to True if you want release download fallback
)

audio.shape
```

#### 2. Separate metadata from numeric features

```python
metadata_cols = ["track_id", "title", "genre_top", "artist_name"]
feature_cols = [c for c in audio.columns if c not in metadata_cols]

print("metadata columns:", metadata_cols)
print("number of numeric feature columns:", len(feature_cols))

audio.select(metadata_cols).head(5)
```

#### 3. Inspect missingness and feature families

```python
def infer_family(col: str) -> str:
    parts = col.split("_")
    if len(parts) < 3:
        return "other"
    return "_".join(parts[:-2])

family_rows = []
for col in feature_cols:
    family_rows.append(
        {
            "column": col,
            "family": infer_family(col),
            "null_count": audio.get_column(col).null_count(),
        }
    )

family_df = pl.DataFrame(family_rows)

family_summary = (
    family_df.group_by("family")
    .agg(
        pl.len().alias("n_columns"),
        pl.sum("null_count").alias("total_nulls"),
    )
    .sort("n_columns", descending=True)
)

family_summary
```

#### 4. Reproduce the memory-footprint formula in Python

```python
n_rows = audio.height
n_features = len(feature_cols)
bytes_per_float64 = 8

numeric_bytes = n_rows * n_features * bytes_per_float64
numeric_mib = numeric_bytes / (1024 ** 2)

print(f"Rows: {n_rows:,}")
print(f"Numeric features: {n_features}")
print(f"Approximate Float64 numeric block: {numeric_bytes:,} bytes")
print(f"Approximate Float64 numeric block: {numeric_mib:.2f} MiB")
```

#### 5. Compare Float64, Float32, and pairwise-distance storage

```python
float32_bytes = n_rows * n_features * 4
pairwise_float64_bytes = n_rows * n_rows * 8

summary = pl.DataFrame(
    {
        "artifact": [
            "numeric feature block (Float64)",
            "numeric feature block (Float32)",
            "full pairwise distance matrix (Float64)",
        ],
        "bytes": [
            numeric_bytes,
            float32_bytes,
            pairwise_float64_bytes,
        ],
    }
).with_columns(
    (pl.col("bytes") / (1024 ** 2)).alias("MiB"),
    (pl.col("bytes") / (1024 ** 3)).alias("GiB"),
)

summary
```

#### 6. Visualize feature-family width

```python
plot_df = family_summary.to_pandas()

plt.figure(figsize=(12, 4))
plt.bar(plot_df["family"], plot_df["n_columns"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("Number of columns")
plt.title("PachaMix audio feature families")
plt.tight_layout()
plt.show()
```

#### 7. Visualize null burden by family

```python
plt.figure(figsize=(12, 4))
plt.bar(plot_df["family"], plot_df["total_nulls"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("Total null count")
plt.title("Null counts by feature family")
plt.tight_layout()
plt.show()
```

#### 8. Mathematical feasibility check for throughput

```python
# Example engineering question:
# If we process 25,000 rows per second, how long would one full pass take?

throughput_rows_per_sec = 25_000
seconds = n_rows / throughput_rows_per_sec

print(f"Full scan time at {throughput_rows_per_sec:,} rows/sec: {seconds:.2f} seconds")
```

### Mathematical demonstration in Python

The week's formal result is the scaling law

$$
M \approx ndb.
$$

Verify its sensitivity numerically:

```python
def memory_mib(n: int, d: int, bytes_per_value: int) -> float:
    return n * d * bytes_per_value / (1024 ** 2)

for scale in [1, 2, 5, 10]:
    mib = memory_mib(scale * n_rows, n_features, 8)
    print(f"{scale:>2}x rows -> {mib:8.2f} MiB")
```

Interpretation:

- growth is linear in the number of rows if the number of columns is fixed
- growth is also linear in the number of columns if the row count is fixed
- quadratic objects such as pairwise distance matrices change the feasibility regime entirely

### Required exercises

1. Replace the pairwise-distance example with a pairwise cosine-similarity matrix. Does the storage order change?
2. Compute the memory footprint of:
   - the full numeric matrix
   - a `10,000 x 518` classroom subset
   - a hypothetical `1,000,000 x 518` dataset
3. Write one descriptive, one predictive, and one prescriptive question using the actual schema.
4. Identify one question that cannot be answered from `pachamix_audio_core` alone and explain why.

### Deliverables

- one table with row count, feature count, and memory scenarios
- one bar chart of feature-family widths
- one paragraph on whether a laptop workflow is sufficient for the current dataset
- one paragraph distinguishing data scale from algorithmic scale

## Bridge to Week 2

Mathias wants to classify, cluster, and deploy on day one.
Yunguri's response defines the next week:

> "Before we run algorithms, we must decide what kind of learning problem we actually have."
