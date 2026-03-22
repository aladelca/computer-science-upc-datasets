from __future__ import annotations

import re
from pathlib import Path

import nbformat as nbf

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = REPO_ROOT / "big_data_course_content"
OUTPUT_DIR = SOURCE_DIR / "notebooks"

BOOTSTRAP_CODE = """from pathlib import Path
import sys

repo_candidate = Path.cwd().resolve()
for candidate in (repo_candidate, *repo_candidate.parents):
    if (candidate / "pyproject.toml").exists():
        REPO_ROOT = candidate
        break
else:
    raise FileNotFoundError("Could not locate the repository root from the current path.")

course_dir = REPO_ROOT / "big_data_course_content"
if str(course_dir) not in sys.path:
    sys.path.insert(0, str(course_dir))

import notebook_support as course_support

REPO_ROOT = course_support.bootstrap_course_notebook(REPO_ROOT)
CLASSROOM = course_support.prepare_classroom_artifacts(REPO_ROOT)
CLASSROOM
"""

NOTEBOOK_PREAMBLE = """This notebook was generated from `{source_name}`.

It keeps the weekly theory and lab structure from `big_data_course_content`, while making the code executable against the local repo data.

Data sources used in this notebook:

- package-backed class datasets: `pachamix_audio_core`, `pachamix_lyrics_long`
- behavior / playlist layer already staged in this repo from the class Kaggle workflow: `pachamix_playlist_events`, `pachamix_playlist_stats`, `pachamix_track_popularity`

For the large lyric and behavior tables, the notebook support layer builds deterministic classroom-sized artifacts under `big_data_course_content/_classroom_artifacts/` so the live session stays runnable on a laptop.
"""

PRACTICE_GUIDE = """## Practice-First Use

This notebook is designed for the practice block of the course, not just for passive reading.

Recommended classroom flow:

1. Run the baseline workflow from top to bottom once.
2. Pause after each major result and explain the objective, the data representation, and the metric being used.
3. Use the extension section at the end to change one modeling choice at a time.
4. Record at least one success case, one failure case, and one interpretation limit before closing the notebook.

Robustness rule:

- do not trust a plot until you can explain the preprocessing
- do not trust a metric until you can name the baseline
- do not trust a result until you can say what changes when a parameter moves
"""

END_CHECKLIST = """## End-of-Class Checklist

Before the session ends, the student group should be able to answer all of the following:

- What exact object was optimized in this notebook?
- Which preprocessing choices had the biggest downstream effect?
- Which result was only descriptive, and which result was evaluative?
- Which baseline, counterexample, or failure case prevented overclaiming?
- Which output should be kept as the main practice deliverable for this week?
"""

LOAD_BLOCK = """events = upc_datasets.load_dataset("pachamix_playlist_events", root="data/processed", download=False)
popularity = upc_datasets.load_dataset("pachamix_track_popularity", root="data/processed", download=False)
playlist_stats = upc_datasets.load_dataset("pachamix_playlist_stats", root="data/processed", download=False)"""

TRANSFORMS = {
    'audio = upc_datasets.load_dataset("pachamix_audio_core", root="data/processed", download=False)': 'audio = course_support.load_audio_dataset(REPO_ROOT)',
    'lyrics = upc_datasets.load_dataset("pachamix_lyrics_long", root="data/processed", download=False)': 'lyrics = course_support.load_lyrics_subset(REPO_ROOT)',
    LOAD_BLOCK: "events, popularity, playlist_stats = course_support.load_behavior_subset(REPO_ROOT)",
    'edges = upc_datasets.load_dataset("pachamix_song_graph_edges", root="data/processed", download=False)': 'edges = course_support.load_song_graph_subset(REPO_ROOT)',
    'LogisticRegression(max_iter=2000, multi_class="auto")': "LogisticRegression(max_iter=2000)",
    "contrast_audio = (farthest_audio - nearest_audio) / nearest_audio": """contrast_audio = np.divide(
    farthest_audio - nearest_audio,
    nearest_audio,
    out=np.full_like(nearest_audio, np.nan),
    where=nearest_audio > 0,
)""",
    'audio = upc_datasets.load_dataset(cfg.dataset_name, root="data/processed", download=False)': 'audio = course_support.load_audio_dataset(REPO_ROOT)',
    """def run_pipeline(cfg: PipelineConfig) -> dict:
    t0 = time.perf_counter()""": """def run_pipeline(cfg: PipelineConfig) -> dict:
    t0 = time.perf_counter()
    run_output_dir = Path(cfg.output_dir)
    run_output_dir.mkdir(parents=True, exist_ok=True)""",
    '.write_parquet(output_dir / "embedding_clusters.parquet")': '.write_parquet(run_output_dir / "embedding_clusters.parquet")',
    'with open(output_dir / "metrics.json", "w", encoding="utf-8") as f:': 'with open(run_output_dir / "metrics.json", "w", encoding="utf-8") as f:',
    'with open(output_dir / "config.json", "w", encoding="utf-8") as f:': 'with open(run_output_dir / "config.json", "w", encoding="utf-8") as f:',
}

EXTRA_PRACTICE: dict[str, list[dict[str, str]]] = {
    "week_01_big_data_foundations": [
        {
            "type": "markdown",
            "content": """## Additional Practice Example

Use the same dataset dimensions to stress-test memory and throughput assumptions instead of relying on a single back-of-the-envelope estimate.
""",
        },
        {
            "type": "code",
            "content": """import polars as pl

# Compare memory budgets under multiple storage assumptions.
memory_rows = []
for label, bytes_per_value, working_copies in [
    ("float32, 1 copy", 4, 1),
    ("float64, 1 copy", 8, 1),
    ("float64, 2 copies", 8, 2),
    ("float64, 3 copies", 8, 3),
]:
    estimated_bytes = audio.height * len(feature_cols) * bytes_per_value * working_copies
    memory_rows.append(
        {
            "scenario": label,
            "estimated_mib": float(estimated_bytes / 1024**2),
        }
    )

memory_budget_df = pl.DataFrame(memory_rows)
memory_budget_df

# Compare processing times under several throughput assumptions.
throughput_rows = []
for rows_per_second in [5_000, 10_000, 25_000, 50_000, 100_000]:
    throughput_rows.append(
        {
            "rows_per_second": rows_per_second,
            "full_pass_seconds": float(audio.height / rows_per_second),
            "full_pass_minutes": float(audio.height / rows_per_second / 60),
        }
    )

pl.DataFrame(throughput_rows)
""",
        },
    ],
    "week_02_supervised_and_unsupervised_learning": [
        {
            "type": "markdown",
            "content": """## Additional Practice Example

Add one more supervised baseline and inspect whether the unsupervised partition merely reproduces the label space or reveals a different structure.
""",
        },
        {
            "type": "code",
            "content": """from sklearn.neighbors import NearestCentroid

# Baseline 2: nearest-centroid classification on the same split.
centroid_clf = Pipeline(
    [
        ("scaler", StandardScaler()),
        ("model", NearestCentroid()),
    ]
)
centroid_clf.fit(X_train, y_train)
centroid_pred = centroid_clf.predict(X_test)

baseline_compare_df = pl.DataFrame(
    [
        {"model": "logistic_regression", "accuracy": float(accuracy_score(y_test, pred))},
        {"model": "nearest_centroid", "accuracy": float(accuracy_score(y_test, centroid_pred))},
    ]
)
baseline_compare_df

# Inspect how mixed each cluster is with respect to the proxy genre labels.
cluster_mix_df = (
    pl.DataFrame({"cluster": cluster_labels, "genre_top": unsup_df.get_column("genre_top")})
    .group_by(["cluster", "genre_top"])
    .len()
    .sort(["cluster", "len"], descending=[False, True])
)

cluster_mix_df.head(18)
""",
        },
    ],
    "week_03_curse_of_dimensionality": [
        {
            "type": "markdown",
            "content": """## Additional Practice Example

Compare how the contrast statistic changes when the metric or preprocessing changes, instead of discussing the curse of dimensionality as if it were metric-independent.
""",
        },
        {
            "type": "code",
            "content": """def contrast_stat(X: np.ndarray, metric: str) -> float:
    D = pairwise_distances(X, metric=metric)
    np.fill_diagonal(D, np.nan)
    nearest = np.nanmin(D, axis=1)
    farthest = np.nanmax(D, axis=1)
    contrast = np.divide(
        farthest - nearest,
        nearest,
        out=np.full_like(nearest, np.nan),
        where=nearest > 0,
    )
    return float(np.nanmean(contrast))

X_audio_raw = audio_sample.select(feature_cols).fill_null(0.0).to_numpy()

contrast_compare_df = pl.DataFrame(
    [
        {"representation": "audio_raw", "metric": "euclidean", "mean_contrast": contrast_stat(X_audio_raw, "euclidean")},
        {"representation": "audio_standardized", "metric": "euclidean", "mean_contrast": contrast_stat(X_audio, "euclidean")},
        {"representation": "audio_standardized", "metric": "manhattan", "mean_contrast": contrast_stat(X_audio, "manhattan")},
    ]
)

contrast_compare_df
""",
        },
    ],
    "week_04_pca": [
        {
            "type": "markdown",
            "content": """## Additional Practice Example

Turn the explained-variance discussion into a concrete decision by finding the first component count that crosses several practical variance thresholds.
""",
        },
        {
            "type": "code",
            "content": """threshold_rows = []
for threshold in [0.70, 0.80, 0.90, 0.95]:
    k_star = int(np.argmax(cum_explained >= threshold) + 1)
    threshold_rows.append(
        {
            "target_variance": threshold,
            "minimum_k": k_star,
            "achieved_variance": float(cum_explained[k_star - 1]),
            "reconstruction_mse_at_k": float(
                reconstruction_df.filter(pl.col("k") == k_star).get_column("reconstruction_mse").item()
            ) if k_star in reconstruction_df.get_column("k").to_list() else None,
        }
    )

variance_threshold_df = pl.DataFrame(threshold_rows)
variance_threshold_df
""",
        },
    ],
    "week_05_svd_tsne_and_embeddings": [
        {
            "type": "markdown",
            "content": """## Additional Practice Example

Compare PCA and SVD energy retention explicitly, then inspect whether the lyric latent space produces stable nearest neighbors.
""",
        },
        {
            "type": "code",
            "content": """pca_svd_compare_rows = []
for k in [5, 10, 20, 50]:
    pca_k = PCA(n_components=k, random_state=42).fit(X_audio)
    pca_svd_compare_rows.append(
        {
            "k": k,
            "pca_explained_variance": float(pca_k.explained_variance_ratio_.sum()),
            "svd_retained_energy": float(np.sum(s[:k] ** 2) / total_energy),
        }
    )

pca_svd_compare_df = pl.DataFrame(pca_svd_compare_rows)
pca_svd_compare_df

track_index = lyrics_wide.get_column("msd_track_id").to_list()
latent_similarity = Z_lyrics @ Z_lyrics.T
np.fill_diagonal(latent_similarity, -np.inf)

neighbor_rows = []
for anchor_idx in [0, 1, 2]:
    neighbor_idx = int(np.argmax(latent_similarity[anchor_idx]))
    neighbor_rows.append(
        {
            "anchor_track": track_index[anchor_idx],
            "neighbor_track": track_index[neighbor_idx],
            "latent_similarity": float(latent_similarity[anchor_idx, neighbor_idx]),
        }
    )

pl.DataFrame(neighbor_rows)
""",
        },
    ],
    "week_06_kmeans": [
        {
            "type": "markdown",
            "content": """## Additional Practice Example

Push the `K` sweep further and inspect how the elbow-style inertia trend compares with the silhouette trend.
""",
        },
        {
            "type": "code",
            "content": """extended_rows = []
for k in range(2, 13):
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels_k = model.fit_predict(X_work)
    extended_rows.append(
        {
            "k": k,
            "inertia": float(model.inertia_),
            "silhouette": float(silhouette_score(X_work, labels_k)),
        }
    )

extended_k_summary = pl.DataFrame(extended_rows)
extended_k_summary
""",
        },
    ],
    "week_07_dbscan_and_validation": [
        {
            "type": "markdown",
            "content": """## Additional Practice Example

Find the best non-trivial DBSCAN configuration on the classroom grid and inspect which genres are overrepresented among the noise points.
""",
        },
        {
            "type": "code",
            "content": """candidate_df = (
    dbscan_summary
    .drop_nulls("silhouette_non_noise")
    .filter(pl.col("n_clusters") >= 2)
    .sort("silhouette_non_noise", descending=True)
)

best_cfg = candidate_df.row(0, named=True)
best_labels = dbscan_runs[(best_cfg["eps"], best_cfg["min_pts"])]

noise_genre_df = (
    audio_small.select(["genre_top"])
    .with_columns(pl.Series("label", best_labels))
    .filter(pl.col("label") == -1)
    .group_by("genre_top")
    .len()
    .sort("len", descending=True)
)

candidate_df.head(5), noise_genre_df.head(10)
""",
        },
    ],
    "week_08_content_based_recommendation": [
        {
            "type": "markdown",
            "content": """## Additional Practice Example

Compare cosine ranking with a raw dot-product ranking, then compare lyric recommendations with and without TF-IDF weighting.
""",
        },
        {
            "type": "code",
            "content": """# Audio ranking: cosine versus raw dot product.
raw_profile = X_audio[seed_idx].mean(axis=0)
dot_scores = X_audio @ raw_profile
dot_rank = np.argsort(dot_scores)[::-1]
dot_top10 = [audio_ids[i] for i in dot_rank if audio_ids[i] not in seed_ids][:10]
cosine_top10 = audio_recommendations.get_column("track_id").to_list()

ranking_compare_df = pl.DataFrame(
    {
        "cosine_top10_track_id": cosine_top10,
        "dot_top10_track_id": dot_top10,
    }
)
ranking_compare_df

# Lyric ranking: TF-IDF versus raw count profile.
raw_lyric_profile = X_counts[seed_lyric_idx].mean(axis=0)
raw_lyric_scores = X_counts @ raw_lyric_profile
raw_lyric_rank = np.argsort(raw_lyric_scores)[::-1]
raw_lyric_top10 = [track_index[i] for i in raw_lyric_rank if i not in seed_lyric_idx][:10]
tfidf_lyric_top10 = [row["msd_track_id"] for row in lyric_recommendation_rows]

pl.DataFrame(
    {
        "tfidf_top10_track_id": tfidf_lyric_top10,
        "raw_count_top10_track_id": raw_lyric_top10,
    }
)
""",
        },
    ],
    "week_09_collaborative_filtering": [
        {
            "type": "markdown",
            "content": """## Additional Practice Example

Add a user-based collaborative filtering baseline and compare it with the item-based baseline already built in the notebook.
""",
        },
        {
            "type": "code",
            "content": """playlist_matrix = normalize(R_train)
user_similarity = playlist_matrix @ playlist_matrix.T

user_scores = user_similarity[target_row] @ R_train
user_scores = np.asarray(user_scores).ravel()
user_scores[R_train[target_row] > 0] = -np.inf

user_pred = [track_cols[i] for i in np.argsort(user_scores)[::-1][:top_k]]

comparison_df = pl.DataFrame(
    [
        {
            "method": "item_based_cf",
            "precision_at_10": float(precision_at_k(predicted_tracks, ground_truth_tracks, top_k)),
            "recall_at_10": float(recall_at_k(predicted_tracks, ground_truth_tracks, top_k)),
        },
        {
            "method": "user_based_cf",
            "precision_at_10": float(precision_at_k(user_pred, ground_truth_tracks, top_k)),
            "recall_at_10": float(recall_at_k(user_pred, ground_truth_tracks, top_k)),
        },
        {
            "method": "popularity",
            "precision_at_10": float(precision_at_k(pop_pred, ground_truth_tracks, top_k)),
            "recall_at_10": float(recall_at_k(pop_pred, ground_truth_tracks, top_k)),
        },
    ]
)

comparison_df
""",
        },
    ],
    "week_10_hybrid_recommendation_and_matrix_factorization": [
        {
            "type": "markdown",
            "content": """## Additional Practice Example

Treat the factorization model as an experimental object: sweep latent dimension and regularization instead of reporting a single run.
""",
        },
        {
            "type": "code",
            "content": """def evaluate_mf_config(k_value: int, reg_value: float, epochs_value: int = 8) -> float:
    local_rng = np.random.default_rng(42)
    local_P = 0.1 * local_rng.standard_normal((n_users, k_value))
    local_Q = 0.1 * local_rng.standard_normal((n_items, k_value))

    for _ in range(epochs_value):
        local_rng.shuffle(observed_pairs)
        for u, i in observed_pairs:
            pred_ui = local_P[u] @ local_Q[i]
            err_ui = R_train[u, i] - pred_ui
            p_old = local_P[u].copy()
            q_old = local_Q[i].copy()
            local_P[u] += lr * (err_ui * q_old - reg_value * p_old)
            local_Q[i] += lr * (err_ui * p_old - reg_value * q_old)

    pred_matrix_local = local_P @ local_Q.T
    hits_local = 0
    tested_local = 0
    for u, i_true in held_out.items():
        scores_local = pred_matrix_local[u].copy()
        scores_local[R_train[u] > 0] = -np.inf
        top10_local = np.argsort(scores_local)[::-1][:10]
        hits_local += int(i_true in top10_local)
        tested_local += 1
    return hits_local / tested_local

sweep_rows = []
for k_value in [10, 20, 40]:
    for reg_value in [0.001, 0.01, 0.05]:
        sweep_rows.append(
            {
                "k": k_value,
                "reg": reg_value,
                "hit_rate_at_10": float(evaluate_mf_config(k_value, reg_value)),
            }
        )

mf_sweep_df = pl.DataFrame(sweep_rows).sort("hit_rate_at_10", descending=True)
mf_sweep_df
""",
        },
    ],
    "week_11_graph_analytics_foundations": [
        {
            "type": "markdown",
            "content": """## Additional Practice Example

Compare weighted degree with plain degree and inspect what happens when weak co-occurrence edges are removed.
""",
        },
        {
            "type": "code",
            "content": """unweighted_degree = dict(G.degree())
unweighted_df = pl.DataFrame(
    {
        "track_uri": list(unweighted_degree.keys()),
        "degree": list(unweighted_degree.values()),
    }
)

rank_compare_df = degree_df.join(unweighted_df, on="track_uri").head(10)
rank_compare_df

cut_rows = []
for threshold in [1, 2, 3]:
    G_cut = nx.Graph()
    for row in edges_small.filter(pl.col("weight") >= threshold).iter_rows(named=True):
        G_cut.add_edge(row["src_track_uri"], row["dst_track_uri"], weight=row["weight"])
    component_sizes_cut = sorted((len(c) for c in nx.connected_components(G_cut)), reverse=True) if G_cut.number_of_nodes() else []
    cut_rows.append(
        {
            "weight_threshold": threshold,
            "nodes": G_cut.number_of_nodes(),
            "edges": G_cut.number_of_edges(),
            "largest_component": component_sizes_cut[0] if component_sizes_cut else 0,
        }
    )

pl.DataFrame(cut_rows)
""",
        },
    ],
    "week_12_pagerank": [
        {
            "type": "markdown",
            "content": """## Additional Practice Example

Vary the damping factor and check how stable the ranking is relative to weighted degree.
""",
        },
        {
            "type": "code",
            "content": """alpha_rows = []
for alpha_value in [0.60, 0.75, 0.85, 0.95]:
    pi_alpha, history_alpha = pagerank_power_iteration(P, alpha=alpha_value, tol=1e-10, max_iter=500)
    alpha_rows.append(
        {
            "alpha": alpha_value,
            "iterations": len(history_alpha),
            "top_track": nodes[int(np.argmax(pi_alpha))],
            "top_score": float(np.max(pi_alpha)),
        }
    )

alpha_summary_df = pl.DataFrame(alpha_rows)
alpha_summary_df

top_pr = rank_df.sort("pagerank", descending=True).head(10).get_column("track_uri").to_list()
top_deg = rank_df.sort("weighted_degree", descending=True).head(10).get_column("track_uri").to_list()
print("top-10 overlap between PageRank and weighted degree:", len(set(top_pr) & set(top_deg)))
""",
        },
    ],
    "week_13_pipelines": [
        {
            "type": "markdown",
            "content": """## Additional Practice Example

Run the pipeline with multiple configurations and compare both metrics and artifact destinations.
""",
        },
        {
            "type": "code",
            "content": """trial_rows = []
for n_components, n_clusters in [(5, 4), (10, 6), (15, 8)]:
    trial_cfg = PipelineConfig(
        sample_size=cfg.sample_size,
        n_components=n_components,
        n_clusters=n_clusters,
        random_state=cfg.random_state,
        output_dir=f"artifacts/week13_pipeline_{n_components}_{n_clusters}",
    )
    trial_metrics = run_pipeline(trial_cfg)
    trial_rows.append(
        {
            "n_components": n_components,
            "n_clusters": n_clusters,
            "silhouette": float(trial_metrics["silhouette"]),
            "inertia": float(trial_metrics["inertia"]),
            "runtime_seconds": float(trial_metrics["runtime_seconds"]),
            "output_dir": trial_cfg.output_dir,
        }
    )

trial_df = pl.DataFrame(trial_rows)
trial_df
""",
        },
    ],
    "week_14_serving_monitoring_and_defense": [
        {
            "type": "markdown",
            "content": """## Additional Practice Example

Extend the monitoring view beyond one metric by bootstrapping recall and simulating a degraded production day.
""",
        },
        {
            "type": "code",
            "content": """recall_values = metric_df.get_column("recall_at_10").to_numpy()
boot_recall = []
for _ in range(1000):
    recall_sample = rng.choice(recall_values, size=len(recall_values), replace=True)
    boot_recall.append(np.mean(recall_sample))

recall_ci_low, recall_ci_high = np.percentile(boot_recall, [2.5, 97.5])

degraded_latencies_ms = [value * 2.5 for value in latencies_ms]
degraded_precision = point_estimate * 0.5

scenario_df = pl.DataFrame(
    [
        {
            "scenario": "baseline",
            "precision_at_10": float(point_estimate),
            "recall_ci_low": float(recall_ci_low),
            "recall_ci_high": float(recall_ci_high),
            "p95_latency_ms": float(np.quantile(latencies_ms, 0.95)),
        },
        {
            "scenario": "degraded",
            "precision_at_10": float(degraded_precision),
            "recall_ci_low": float(recall_ci_low * 0.5),
            "recall_ci_high": float(recall_ci_high * 0.5),
            "p95_latency_ms": float(np.quantile(degraded_latencies_ms, 0.95)),
        },
    ]
)

scenario_df
""",
        },
    ],
}


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for source_path in sorted(SOURCE_DIR.glob("week_*.md")):
        nb = build_notebook(source_path)
        output_path = OUTPUT_DIR / f"{source_path.stem}.ipynb"
        nbf.write(nb, output_path)
        print(f"generated {output_path.relative_to(REPO_ROOT)}")


def build_notebook(source_path: Path) -> nbf.NotebookNode:
    text = source_path.read_text(encoding="utf-8")
    cells = [
        nbf.v4.new_markdown_cell(
            NOTEBOOK_PREAMBLE.format(source_name=source_path.relative_to(REPO_ROOT))
        ),
        nbf.v4.new_code_cell(BOOTSTRAP_CODE),
        nbf.v4.new_markdown_cell(PRACTICE_GUIDE),
    ]
    last_heading = "Notebook setup"

    for kind, value in iter_markdown_and_code(text):
        if kind == "markdown":
            stripped = value.strip()
            if stripped:
                last_heading = extract_latest_heading(stripped, last_heading)
                cells.append(nbf.v4.new_markdown_cell(stripped))
            continue

        language, code = value
        if (
            language != "python"
            or "!pip install" in code
            or ("content_scores" in code and "collab_scores" in code)
        ):
            rendered = f"```{language}\n{code.rstrip()}\n```" if language else code.rstrip()
            cells.append(nbf.v4.new_markdown_cell(rendered))
            continue

        transformed = transform_code(code.rstrip())
        transformed = decorate_code(transformed, last_heading)
        cells.append(nbf.v4.new_code_cell(transformed))

    for extra_cell in extra_practice_cells(source_path.stem):
        if extra_cell["type"] == "markdown":
            cells.append(nbf.v4.new_markdown_cell(extra_cell["content"].strip()))
        else:
            cells.append(
                nbf.v4.new_code_cell(
                    decorate_code(extra_cell["content"].strip(), "Additional practice example")
                )
            )

    cells.append(nbf.v4.new_markdown_cell(END_CHECKLIST))

    return nbf.v4.new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.12",
            },
        },
    )


def iter_markdown_and_code(text: str):
    pattern = re.compile(r"```([a-zA-Z0-9_+-]*)\n(.*?)```", re.DOTALL)
    cursor = 0

    for match in pattern.finditer(text):
        if match.start() > cursor:
            yield "markdown", text[cursor : match.start()]
        language = match.group(1).strip()
        code = match.group(2)
        yield "code", (language, code)
        cursor = match.end()

    if cursor < len(text):
        yield "markdown", text[cursor:]


def transform_code(code: str) -> str:
    transformed = code
    for old, new in TRANSFORMS.items():
        transformed = transformed.replace(old, new)
    return transformed


def extract_latest_heading(markdown_text: str, fallback: str) -> str:
    headings = []
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            headings.append(stripped.lstrip("#").strip())
    return headings[-1] if headings else fallback


def decorate_code(code: str, heading: str) -> str:
    comment_header = (
        f"# Practice step: {heading}\n"
        "# Run the baseline first, inspect the resulting objects and metrics,\n"
        "# and only then change one modeling choice at a time in the extension work.\n\n"
    )
    return comment_header + code


def extra_practice_cells(week_stem: str) -> list[dict[str, str]]:
    return EXTRA_PRACTICE.get(week_stem, [])


if __name__ == "__main__":
    main()
