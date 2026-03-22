# Week 14 - Serving, Monitoring, and the Final Defense of PachaMix

## Position in the Semester

- Arc: Making the System Real
- Main datasets: all processed artifacts, all evaluation outputs

## PachaMix Story Frame

### Cold Open

> Mathias: "At last. We deploy."
>
> Yunguri: "At last. We deploy responsibly."

### Narrative Role of the Week

The course closes here by forcing synthesis.
Students must show that they can connect:

- data representation
- mathematical objective
- evaluation logic
- operational constraints
- product judgment

## Dataset Anchor in This Repo

This final week should reuse the artifacts generated or discussed across the semester:

- `pachamix_audio_core`
- `pachamix_lyrics_long`
- `pachamix_playlist_events`
- `pachamix_track_popularity`
- `pachamix_song_graph_edges`
- any derived evaluation splits, embeddings, or model outputs created by the class

The final defense should state exactly which subset of these artifacts the proposed system actually uses.

## Theory Objectives

Students must be able to:

- distinguish offline evaluation from online service behavior
- define monitoring metrics for recommendation and pipeline health
- discuss uncertainty, repeated-run variability, and threshold selection
- compare the semester's methods under operational constraints
- defend a system choice with mathematical and engineering arguments

## Serving Architecture Concepts

Possible service patterns:

- batch generation of recommendation lists
- online retrieval plus ranking
- hybrid design with periodic offline recomputation and lightweight online serving

The correct choice depends on measurable constraints, not on fashion.

## Monitoring Metrics

A serious system should track at least four families of signals.

### 1. Recommendation quality

Examples:

- Precision@k
- Recall@k
- hit rate
- NDCG

### 2. Coverage and diversity

Examples:

- catalog coverage
- concentration of recommendations among a few popular tracks
- diversity across genres or learned clusters

### 3. System health

Examples:

- request latency
- batch completion time
- failure rate
- artifact freshness

### 4. Data quality and drift

Examples:

- missing-value rate
- distribution shifts in core features
- changes in playlist length distribution
- changes in graph density or degree distribution

## Quantifying Uncertainty

Suppose a metric estimate $\hat{m}$ is computed over repeated evaluation splits.
A classical confidence interval may be written as

$$
\hat{m} \pm z_{\alpha/2}\frac{\hat{\sigma}}{\sqrt{B}},
$$

where:

- $B$ is the number of repeated estimates
- $\hat{\sigma}$ is the sample standard deviation of those estimates

For complex ranking metrics, bootstrap procedures are often more practical than closed-form variance calculations.

The key principle is not the exact formula.
The key principle is that one run is rarely enough to justify a production claim.

## Monitoring Thresholds

If a monitored metric is $m_t$ at time $t$, then a threshold rule might be:

$$
\text{alert if } m_t < \tau_{\text{min}}
$$

or

$$
\text{alert if } |m_t - \mu_{\text{baseline}}| > c \sigma_{\text{baseline}}.
$$

The threshold must reflect operational tolerance, not panic.

## Comparative Synthesis of Semester Methods

Students should now be able to compare the semester's main tools:

| Method family | Core mathematical object | Strength | Weakness |
| --- | --- | --- | --- |
| PCA / SVD | covariance or matrix factorization | compression, denoising | linear assumptions |
| t-SNE | neighborhood probability matching | visualization | weak production utility |
| K-means | SSE minimization | simple partitioning | spherical bias |
| DBSCAN | density connectivity | irregular clusters, noise handling | parameter sensitivity |
| Content-based recommendation | vector similarity | interpretable, item cold start | overspecialization |
| Collaborative filtering | interaction matrix | captures collective taste | sparsity, cold start |
| Matrix factorization | low-rank latent structure | expressive behavioral model | harder interpretation |
| PageRank | fixed point on a stochastic graph | structural importance | depends on graph definition |

## Extended Theoretical Notes

### 1. Deployment as Constrained Optimization

A deployed analytical system is almost never optimizing a single scalar quantity.
Instead, one should think in terms of constrained optimization:

$$
\max \text{utility}
\quad \text{subject to} \quad
\text{latency} \le \tau,\;
\text{resource usage} \le \rho,\;
\text{quality} \ge q_{\min}.
$$

This is a more accurate mathematical view of production decision-making than simply "choose the best model."

### 2. Monitoring as Sequential Statistical Inference

Monitoring is not just dashboarding.
It is repeated quantitative checking of whether the system remains within an acceptable operating regime.

At a high level, this resembles sequential inference:

- observe metric stream $m_t$
- compare against baseline behavior
- trigger an alert when the deviation is materially large

Thus operational monitoring is an extension of the statistical mindset, not a separate discipline.

### 3. Confidence Intervals and Practical Uncertainty

A point estimate without uncertainty is too weak for a serious final defense.
If $\hat{m}$ is a measured quality metric, then the question is not only:

> "What is the mean?"

but also:

> "How variable is it under repeated sampling or reruns?"

This is why repeated splits, bootstrap intervals, and variability summaries are mathematically important even in applied systems work.

### 4. Drift as Distribution Shift

Data drift can be written abstractly as a change from

$$
p_{\text{train}}(x)
\quad \text{to} \quad
p_{\text{serve}}(x),
$$

or, more generally, a change in joint behavior

$$
p_{\text{train}}(x,y)
\quad \text{to} \quad
p_{\text{serve}}(x,y).
$$

This matters because a model can remain numerically stable while becoming behaviorally irrelevant if the serving distribution changes enough.

### 5. Final Defense Means Coherence Across Layers

The strongest student projects will show coherence across:

- data representation
- objective function
- optimization method
- evaluation protocol
- serving plan
- monitoring plan

This coherence is the real end point of the course.
Without it, even a technically interesting model remains only a partial prototype.

## Mathematical Checkpoint

Students must be able to defend:

1. Why their chosen objective function is compatible with their deployment goal.
2. Which monitoring signals would reveal degradation.
3. Which uncertainties remain even after offline evaluation.
4. Why their chosen representation, model, and serving mode form a coherent system.

## Laboratory Session

## Mission

Defend PachaMix as if it were a real system reviewed by a technical panel.

## Required deliverables

1. One architecture summary:
   - data inputs
   - model family
   - output type
2. One mathematical defense:
   - objective function
   - evaluation metric
   - baseline comparison
3. One operational defense:
   - serving mode
   - monitoring plan
   - failure detection rules
4. One limitations section:
   - catalog mismatch
   - data sparsity
   - uncertainty or drift risk

## Strict standards

- "It works on my machine" is not a defense.
- "The recommendations looked good" is not an evaluation.
- A monitoring plan without thresholds is incomplete.
- A hybrid claim without documented data alignment remains invalid.
- Students must name at least one failure mode their own system would not yet handle well.

## Suggested final oral defense questions

1. What is the precise objective your system optimizes?
2. Why is that objective compatible with your product goal?
3. What baseline would embarrass your system if you forgot to compare against it?
4. What operational metric would you page an engineer for?
5. Which assumption in your system is most fragile?

## Extended Python Practice Session (2 Hours)

### Lab format

- `0:00-0:20` define an offline evaluation table
- `0:20-0:50` compute ranking metrics and bootstrap confidence intervals
- `0:50-1:20` simulate latency and monitoring thresholds
- `1:20-1:45` compute a simple drift signal
- `1:45-2:00` prepare the final system defense

### Python environment

```python
# Colab / fresh environment only
!pip install -q numpy pandas matplotlib polars
```

### Guided notebook

The goal is not to build a web service from scratch inside class.
The goal is to operationalize a recommendation result quantitatively.

#### 1. Create a minimal offline evaluation table

```python
import numpy as np
import polars as pl
import matplotlib.pyplot as plt
import time

rng = np.random.default_rng(42)

# Synthetic but realistic classroom example:
# 100 playlists, each with a recommendation list and a held-out relevant set.
records = []
for playlist_id in range(100):
    relevant = set(rng.choice(200, size=3, replace=False).tolist())
    predicted = rng.choice(200, size=10, replace=False).tolist()
    records.append(
        {
            "playlist_id": playlist_id,
            "relevant_items": sorted(relevant),
            "predicted_items": predicted,
        }
    )

eval_df = pl.DataFrame(records)
eval_df.head(3)
```

#### 2. Compute Precision@10 and Recall@10

```python
def precision_at_k(predicted, relevant, k=10):
    return len(set(predicted[:k]) & set(relevant)) / k

def recall_at_k(predicted, relevant, k=10):
    return len(set(predicted[:k]) & set(relevant)) / max(len(relevant), 1)

metric_rows = []
for row in eval_df.iter_rows(named=True):
    p10 = precision_at_k(row["predicted_items"], row["relevant_items"], 10)
    r10 = recall_at_k(row["predicted_items"], row["relevant_items"], 10)
    metric_rows.append({"playlist_id": row["playlist_id"], "precision_at_10": p10, "recall_at_10": r10})

metric_df = pl.DataFrame(metric_rows)
metric_df.head()
```

#### 3. Bootstrap a confidence interval

```python
values = metric_df.get_column("precision_at_10").to_numpy()
boot = []
for _ in range(1000):
    sample = rng.choice(values, size=len(values), replace=True)
    boot.append(np.mean(sample))

ci_low, ci_high = np.percentile(boot, [2.5, 97.5])
point_estimate = float(np.mean(values))

print("Precision@10 mean:", point_estimate)
print("95% bootstrap CI :", (ci_low, ci_high))
```

#### 4. Visualize the bootstrap distribution

```python
plt.figure(figsize=(8, 4))
plt.hist(boot, bins=30, alpha=0.8)
plt.axvline(ci_low, color="red", linestyle="--", label="2.5%")
plt.axvline(ci_high, color="red", linestyle="--", label="97.5%")
plt.axvline(point_estimate, color="black", linestyle="-", label="mean")
plt.xlabel("Bootstrap mean Precision@10")
plt.ylabel("Frequency")
plt.title("Uncertainty in offline recommendation quality")
plt.legend()
plt.tight_layout()
plt.show()
```

#### 5. Simulate serving latency

```python
latencies_ms = []

for _ in range(200):
    t0 = time.perf_counter()
    # Placeholder scoring work
    scores = rng.normal(size=5000)
    _ = np.argsort(scores)[-10:]
    t1 = time.perf_counter()
    latencies_ms.append((t1 - t0) * 1000)

latency_df = pl.DataFrame({"latency_ms": latencies_ms})

latency_summary = {
    "mean_ms": float(np.mean(latencies_ms)),
    "p95_ms": float(np.quantile(latencies_ms, 0.95)),
    "max_ms": float(np.max(latencies_ms)),
}

latency_summary
```

#### 6. Define simple monitoring thresholds

```python
p95_threshold_ms = 5.0
precision_threshold = 0.03

alerts = {
    "latency_alert": float(np.quantile(latencies_ms, 0.95)) > p95_threshold_ms,
    "quality_alert": point_estimate < precision_threshold,
}

alerts
```

#### 7. Compute a simple drift indicator

```python
# Example: compare a baseline feature distribution with a later batch.
baseline = rng.normal(loc=0.0, scale=1.0, size=5000)
current = rng.normal(loc=0.3, scale=1.2, size=5000)

mean_shift = float(np.mean(current) - np.mean(baseline))
std_shift = float(np.std(current) - np.std(baseline))

print("mean shift:", mean_shift)
print("std shift :", std_shift)
```

#### 8. Visualize drift

```python
plt.figure(figsize=(8, 4))
plt.hist(baseline, bins=40, alpha=0.6, density=True, label="baseline")
plt.hist(current, bins=40, alpha=0.6, density=True, label="current")
plt.xlabel("Feature value")
plt.ylabel("Density")
plt.title("Example feature drift signal")
plt.legend()
plt.tight_layout()
plt.show()
```

### Mathematical demonstration in Python

This week's operational claim is that uncertainty and thresholding should be quantitative, not rhetorical.
The bootstrap interval above operationalizes:

$$
\hat{m} \pm \text{uncertainty band}
$$

without requiring a fragile closed-form variance formula for every ranking metric.

### Required exercises

1. Change the bootstrap size from `1000` to `200` and `5000`. Does the interval stabilize?
2. Tighten the latency threshold from `5 ms` to `1 ms`. What operational behavior would this trigger?
3. Create a diversity metric, for example the fraction of distinct recommended items across all playlists.
4. Write a final defense paragraph explaining:
   - the offline metric used
   - the uncertainty estimate
   - one serving threshold
   - one drift signal

### Deliverables

- one metric table
- one bootstrap-confidence-interval plot
- one latency summary
- one drift visualization
- one final system-defense paragraph

## Final Closing Note

The PachaMix narrative ends correctly only if the students understand Yunguri's standard:

the system is not successful because it produces recommendations.
It is successful only if those recommendations emerge from a defensible chain of:

- data design
- mathematical reasoning
- empirical evaluation
- operational discipline
