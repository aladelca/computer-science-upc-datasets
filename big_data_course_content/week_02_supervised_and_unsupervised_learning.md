# Week 2 - Supervised and Unsupervised Learning

## Position in the Semester

- Arc: Framing the Problem
- Main datasets: `pachamix_audio_core`
- Secondary reference: `pachamix_lyrics_long` as an example of an unlabeled representation space

## PachaMix Story Frame

### Cold Open

> Mathias: "I have solved it. PachaMix is supervised learning."
>
> Yunguri: "What is the label?"
>
> Mathias: "Good music."

### Narrative Role of the Week

The pedagogical objective is to prevent students from calling every data problem "AI."
PachaMix contains several mathematically distinct tasks:

- prediction
- clustering
- dimensionality reduction
- recommendation
- ranking

Each one requires different data assumptions, losses, and evaluation logic.

## Dataset Anchor in This Repo

### Primary dataset

- `pachamix_audio_core`

This table is useful because it contains:

- many numeric predictors
- a nullable semantic field `genre_top`
- no native user preference labels

That is precisely why it is educational:

- it can support a supervised proxy task such as genre prediction
- it can also support an unsupervised task such as clustering or PCA

### Secondary dataset

- `pachamix_lyrics_long`

This table is naturally unsupervised at raw ingestion time.
It contains token counts, not ready-made labels.

## Theory Objectives

Students must be able to:

- formalize supervised learning with labeled pairs
- formalize unsupervised learning without explicit targets
- separate prediction error from structure quality
- justify train, validation, and test splits
- explain why recommendation is not reducible to a single classical category

## Formal Problem Statements

### 1. Supervised Learning

We observe labeled data

$$
\{(x_i, y_i)\}_{i=1}^n,
$$

where:

- $x_i \in \mathbb{R}^d$ is the feature vector
- $y_i$ is the target

The goal is to learn a function $f_\theta$ by minimizing empirical risk:

$$
\hat{R}(\theta) = \frac{1}{n}\sum_{i=1}^n \ell(f_\theta(x_i), y_i).
$$

Typical examples:

- regression: $\ell(\hat{y}, y) = (\hat{y} - y)^2$
- classification: $\ell$ may be cross-entropy or another classification loss

### 2. Unsupervised Learning

We observe only

$$
\{x_i\}_{i=1}^n.
$$

There is no externally supplied target variable.
Instead, we optimize a structure criterion, for example:

- cluster compactness
- variance preserved after projection
- density connectivity

In general, the objective has the form

$$
\min_{\Theta, Z} J(X; \Theta, Z),
$$

where $\Theta$ denotes model parameters and $Z$ denotes latent assignments or lower-dimensional coordinates.

### 3. Recommendation as a Mixed Task Family

Recommendation may involve:

- supervised components
- unsupervised representation learning
- ranking losses
- interaction matrices with missing-not-at-random entries

Therefore, it is better to say that recommendation is a task family rather than a single canonical algorithm.

## Mathematical Development

### 1. Mean Squared Error

For regression,

$$
\text{MSE} = \frac{1}{n}\sum_{i=1}^n (\hat{y}_i - y_i)^2.
$$

MSE penalizes large errors quadratically and is differentiable, which makes it convenient for optimization.

### 2. Training, Validation, and Test Logic

If the same data are used both to fit and evaluate a model, the resulting estimate is optimistically biased.
Thus we separate:

- training set: fit model parameters
- validation set: choose hyperparameters or model class
- test set: estimate final generalization performance

This is not bureaucracy.
It is the minimal structure needed to avoid self-deception.

### 3. Supervised Versus Unsupervised Objective Comparison

In supervised learning, the loss is evaluated against observed targets.
In unsupervised learning, the objective is internal to the representation.

Examples:

$$
\hat{R}_{\text{supervised}}(\theta) = \frac{1}{n}\sum_{i=1}^n \ell(f_\theta(x_i), y_i),
$$

versus

$$
J_{\text{K-means}}(R, \mu) = \sum_{i=1}^n \sum_{k=1}^K r_{ik}\lVert x_i - \mu_k \rVert_2^2,
$$

or

$$
J_{\text{PCA}}(W) = -\operatorname{tr}(W^\top \Sigma W)
$$

under orthonormality constraints.

The supervised criterion is externally anchored.
The unsupervised criteria are structurally anchored.

## Extended Theoretical Notes

### 1. Empirical Risk Minimization as a Unifying View

A large fraction of machine learning can be written as:

$$
\min_{\theta \in \Theta} \hat{R}(\theta) + \lambda \Omega(\theta),
$$

where:

- $\hat{R}(\theta)$ is an empirical data-fit term
- $\Omega(\theta)$ is a complexity penalty or regularizer
- $\lambda \ge 0$ controls the fit-complexity tradeoff

This is useful because it clarifies what changes between methods:

- the hypothesis space $\Theta$
- the loss $\ell$
- the regularizer $\Omega$
- the data structure over which the loss is computed

### 2. Supervised Learning as Conditional Prediction

In supervised learning, the object of interest is often the conditional relation

$$
y \approx f(x),
$$

or more formally, the conditional distribution

$$
p(y \mid x).
$$

Classification and regression differ not because one is "harder" than the other, but because:

- the codomain of $y$ differs
- the loss geometry differs
- the induced decision rules differ

For classification, the decision rule can be written as

$$
\hat{y}(x) = \arg\max_c \hat{p}(y=c \mid x).
$$

This explicitly separates probability estimation from the final decision.

### 3. Unsupervised Learning as Latent-Structure Inference

Unsupervised learning is often misunderstood as "learning without answers."
That is too vague.
More rigorously, it seeks latent structure not externally annotated in the data.

Examples:

- clustering introduces latent assignments $z_i$
- PCA introduces latent coordinates $W^\top x_i$
- matrix factorization later in the course introduces latent factors for rows and columns

Thus unsupervised learning is not absence of structure.
It is structure inferred from internal regularities rather than from supplied labels.

### 4. Generalization and the Role of the Split

The training / validation / test split is a finite-sample response to the fact that:

$$
\hat{R}(\theta) \neq R(\theta)
$$

in general, where

$$
R(\theta) = \mathbb{E}_{(x,y)\sim \mathcal{D}}[\ell(f_\theta(x), y)]
$$

is the population risk.

The distinction matters because:

- training loss can always be reduced by memorization in sufficiently rich models
- validation logic is needed for model selection
- the test set estimates out-of-sample behavior only if it remains untouched during tuning

### 5. Why Recommendation Does Not Fit Neatly into One Box

Recommendation can involve:

- missing-not-at-random observations
- implicit rather than explicit feedback
- ranking rather than point prediction
- interaction effects between users, items, and context

So even when recommendation borrows tools from supervised learning, it usually requires a distinct evaluation logic.
This will matter later when the course shifts from accuracy-style thinking to top-`k` ranking and continuation tasks.

## Mathematical Checkpoint

Students must be able to answer all of the following without ambiguity:

1. What is the target variable?
2. If there is no target, what criterion is being optimized instead?
3. What exactly is the evaluation metric?
4. What would constitute overfitting in this setting?
5. What is the unit of prediction, grouping, or ranking?

## Laboratory Session

## Mission

Separate PachaMix tasks by learning type before choosing models.

## Required tasks

1. Use `pachamix_audio_core` to define one plausible supervised proxy task.
   Example: predict `genre_top` after filtering missing labels.
2. Use the same dataset to define one unsupervised task.
   Example: discover clusters in the numeric feature space.
3. Explain why a recommendation task based on `playlist_id` and `track_uri` belongs to a different evaluation regime.
4. Build:
   - one baseline supervised pipeline
   - one baseline unsupervised workflow

## Minimum reporting requirements

For the supervised task, students must report:

- target definition
- class balance or label distribution
- split logic
- loss or metric

For the unsupervised task, students must report:

- feature subset used
- preprocessing applied
- objective or validation criterion
- interpretation limits

## Strict standards

- "The model learned patterns" is not acceptable unless the pattern is operationally defined.
- A train/test split must be justified, not merely executed.
- If `genre_top` is used as a target, the report must state that it is a metadata label, not a perfect ontology of musical meaning.
- Any unsupervised result must specify what notion of structure it optimized.

## Extended Python Practice Session (2 Hours)

### Lab format

- `0:00-0:20` define one supervised and one unsupervised task from the same dataset
- `0:20-0:55` build a supervised baseline for `genre_top`
- `0:55-1:25` build an unsupervised pipeline with PCA plus K-means
- `1:25-1:45` compare losses, metrics, and objectives
- `1:45-2:00` answer reflection questions on problem framing

### Python environment

```python
# Colab / fresh environment only
!pip install -q upc-datasets polars pyarrow numpy pandas matplotlib scikit-learn
```

### Guided notebook

#### 1. Load and sample the audio dataset

```python
import upc_datasets
import polars as pl
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, silhouette_score, log_loss

audio = upc_datasets.load_dataset("pachamix_audio_core", root="data/processed", download=False)

metadata_cols = ["track_id", "title", "genre_top", "artist_name"]
feature_cols = [c for c in audio.columns if c not in metadata_cols]

supervised_df = (
    audio.filter(pl.col("genre_top").is_not_null())
    .sample(n=min(12000, audio.filter(pl.col("genre_top").is_not_null()).height), seed=42)
)

supervised_df.shape
```

#### 2. Stabilize the label space

```python
top_genres = (
    supervised_df.group_by("genre_top")
    .len()
    .sort("len", descending=True)
    .head(6)
    .get_column("genre_top")
    .to_list()
)

supervised_df = supervised_df.filter(pl.col("genre_top").is_in(top_genres))
supervised_df.group_by("genre_top").len().sort("len", descending=True)
```

#### 3. Build a supervised baseline

```python
X = supervised_df.select(feature_cols).fill_null(0.0).to_numpy()
y = supervised_df.get_column("genre_top").to_numpy()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

clf = Pipeline(
    [
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=2000, multi_class="auto")),
    ]
)

clf.fit(X_train, y_train)
pred = clf.predict(X_test)
proba = clf.predict_proba(X_test)

print("accuracy =", accuracy_score(y_test, pred))
print("log-loss =", log_loss(y_test, proba))
print(classification_report(y_test, pred))
```

#### 4. Visualize the supervised class distribution

```python
label_counts = supervised_df.group_by("genre_top").len().sort("len", descending=True).to_pandas()

plt.figure(figsize=(8, 4))
plt.bar(label_counts["genre_top"], label_counts["len"])
plt.xticks(rotation=30, ha="right")
plt.ylabel("Number of tracks")
plt.title("Supervised proxy label distribution")
plt.tight_layout()
plt.show()
```

#### 5. Build an unsupervised pipeline on the same feature space

```python
unsup_df = supervised_df.clone()
X_unsup = unsup_df.select(feature_cols).fill_null(0.0).to_numpy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_unsup)

pca = PCA(n_components=10, random_state=42)
X_pca = pca.fit_transform(X_scaled)

kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_pca)

print("inertia =", kmeans.inertia_)
print("silhouette =", silhouette_score(X_pca, cluster_labels))
```

#### 6. Visualize the unsupervised result

```python
plot_df = pl.DataFrame(
    {
        "pc1": X_pca[:, 0],
        "pc2": X_pca[:, 1],
        "cluster": cluster_labels,
        "genre_top": unsup_df.get_column("genre_top"),
    }
).to_pandas()

plt.figure(figsize=(7, 6))
plt.scatter(plot_df["pc1"], plot_df["pc2"], c=plot_df["cluster"], s=10, alpha=0.6)
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("Unsupervised clustering in PCA space")
plt.tight_layout()
plt.show()
```

### Mathematical demonstration in Python

Compare supervised empirical loss with unsupervised structure quality:

```python
empirical_0_1_loss = np.mean(pred != y_test)
print("empirical 0-1 loss =", empirical_0_1_loss)

cluster_sizes = pl.DataFrame({"cluster": cluster_labels}).group_by("cluster").len().sort("cluster")
cluster_sizes
```

Interpretation:

- supervised loss is measured against known labels
- clustering metrics are internal to the partition and need not align with metadata labels

### Required exercises

1. Replace logistic regression with a baseline nearest-centroid classifier and compare accuracy.
2. Change the number of clusters from `6` to `4`, `8`, and `10`. How does the silhouette score change?
3. Compare cluster composition against `genre_top`. Are the clusters merely reproducing metadata labels?
4. Write a short note explaining why the supervised and unsupervised evaluations are not directly comparable.

### Deliverables

- one supervised metric table with at least accuracy and log-loss
- one unsupervised metric table with at least inertia and silhouette
- one PCA scatterplot colored by cluster
- one paragraph distinguishing "predicting labels" from "discovering structure"

## Recommended Discussion Prompt

Ask students:

> If two teams obtain "good results" on the same dataset but optimize different objectives, are the results comparable?

The correct answer is: not automatically.

## Bridge to Week 3

Once students believe the problem framing is finally under control, the next failure mode appears:

the feature space itself becomes hostile.
