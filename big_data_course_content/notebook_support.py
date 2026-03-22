from __future__ import annotations

import json
import os
import warnings
from pathlib import Path
from typing import Any

import polars as pl
import upc_datasets

ARTIFACT_VERSION = 1
ARTIFACT_DIRNAME = "_classroom_artifacts"
MANIFEST_NAME = "artifact_manifest.json"

AUDIO_SAMPLE_NAME = "pachamix_audio_classroom.parquet"
LYRICS_SUBSET_NAME = "pachamix_lyrics_classroom.parquet"
BEHAVIOR_EVENTS_NAME = "pachamix_playlist_events_classroom.parquet"
BEHAVIOR_STATS_NAME = "pachamix_playlist_stats_classroom.parquet"
BEHAVIOR_POPULARITY_NAME = "pachamix_track_popularity_classroom.parquet"
GRAPH_SUBSET_NAME = "pachamix_song_graph_edges_classroom.parquet"

AUDIO_SAMPLE_SIZE = 6000
LYRICS_TOP_TOKENS = 500
LYRICS_TOP_TRACKS = 900
BEHAVIOR_TOP_PLAYLISTS = 900
BEHAVIOR_TOP_TRACKS = 700
BEHAVIOR_FINAL_PLAYLISTS = 600
BEHAVIOR_FINAL_TRACKS = 450
GRAPH_TOP_EDGES = 5000


def bootstrap_course_notebook(repo_root: str | Path | None = None) -> Path:
    root = _resolve_repo_root(repo_root)
    os.chdir(root)
    os.environ.setdefault("UPC_DATASETS_ROOT", str(root))

    cache_root = root / "big_data_course_content" / ".cache"
    cache_root.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("XDG_CACHE_HOME", str(cache_root))
    os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")

    mpl_config_dir = root / "big_data_course_content" / ".mplconfig"
    mpl_config_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(mpl_config_dir))
    os.environ.setdefault("MPLBACKEND", "Agg")

    warnings.filterwarnings(
        "ignore",
        message="FigureCanvasAgg is non-interactive, and thus cannot be shown",
    )
    return root


def prepare_classroom_artifacts(repo_root: str | Path | None = None) -> dict[str, Any]:
    root = bootstrap_course_notebook(repo_root)
    artifact_dir = _artifact_dir(root)
    artifact_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = artifact_dir / MANIFEST_NAME
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if _manifest_is_valid(root, manifest):
            return manifest

    audio_sample = _build_audio_sample(root)
    lyrics_subset = _build_lyrics_subset(root)
    behavior = _build_behavior_subset(root)
    graph_subset = _build_song_graph_subset(behavior["events"])

    graph_path = artifact_dir / GRAPH_SUBSET_NAME
    graph_subset.write_parquet(graph_path)

    manifest = {
        "artifact_version": ARTIFACT_VERSION,
        "repo_root": str(root),
        "artifact_dir": str(artifact_dir),
        "paths": {
            "audio_sample": str(artifact_dir / AUDIO_SAMPLE_NAME),
            "lyrics_subset": str(artifact_dir / LYRICS_SUBSET_NAME),
            "behavior_events": str(artifact_dir / BEHAVIOR_EVENTS_NAME),
            "behavior_stats": str(artifact_dir / BEHAVIOR_STATS_NAME),
            "behavior_popularity": str(artifact_dir / BEHAVIOR_POPULARITY_NAME),
            "graph_subset": str(graph_path),
        },
        "shapes": {
            "audio_sample": list(audio_sample.shape),
            "lyrics_subset": list(lyrics_subset.shape),
            "behavior_events": list(behavior["events"].shape),
            "behavior_stats": list(behavior["playlist_stats"].shape),
            "behavior_popularity": list(behavior["track_popularity"].shape),
            "graph_subset": list(graph_subset.shape),
        },
        "parameters": {
            "audio_sample_size": AUDIO_SAMPLE_SIZE,
            "lyrics_top_tokens": LYRICS_TOP_TOKENS,
            "lyrics_top_tracks": LYRICS_TOP_TRACKS,
            "behavior_top_playlists": BEHAVIOR_TOP_PLAYLISTS,
            "behavior_top_tracks": BEHAVIOR_TOP_TRACKS,
            "behavior_final_playlists": BEHAVIOR_FINAL_PLAYLISTS,
            "behavior_final_tracks": BEHAVIOR_FINAL_TRACKS,
            "graph_top_edges": GRAPH_TOP_EDGES,
        },
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def load_audio_dataset(repo_root: str | Path | None = None) -> pl.DataFrame:
    root = bootstrap_course_notebook(repo_root)
    return upc_datasets.load_dataset("pachamix_audio_core", root=root, download=False)


def load_lyrics_subset(repo_root: str | Path | None = None) -> pl.DataFrame:
    manifest = prepare_classroom_artifacts(repo_root)
    return pl.read_parquet(manifest["paths"]["lyrics_subset"])


def load_behavior_subset(
    repo_root: str | Path | None = None,
) -> tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
    manifest = prepare_classroom_artifacts(repo_root)
    events = pl.read_parquet(manifest["paths"]["behavior_events"])
    popularity = pl.read_parquet(manifest["paths"]["behavior_popularity"])
    playlist_stats = pl.read_parquet(manifest["paths"]["behavior_stats"])
    return events, popularity, playlist_stats


def load_song_graph_subset(repo_root: str | Path | None = None) -> pl.DataFrame:
    manifest = prepare_classroom_artifacts(repo_root)
    return pl.read_parquet(manifest["paths"]["graph_subset"])


def _resolve_repo_root(repo_root: str | Path | None) -> Path:
    if repo_root is not None:
        return Path(repo_root).resolve()

    current = Path.cwd().resolve()
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").exists():
            return candidate
    raise FileNotFoundError("Could not resolve the repository root from the current path.")


def _artifact_dir(repo_root: Path) -> Path:
    return repo_root / "big_data_course_content" / ARTIFACT_DIRNAME


def _manifest_is_valid(repo_root: Path, manifest: dict[str, Any]) -> bool:
    if manifest.get("artifact_version") != ARTIFACT_VERSION:
        return False

    expected_params = {
        "audio_sample_size": AUDIO_SAMPLE_SIZE,
        "lyrics_top_tokens": LYRICS_TOP_TOKENS,
        "lyrics_top_tracks": LYRICS_TOP_TRACKS,
        "behavior_top_playlists": BEHAVIOR_TOP_PLAYLISTS,
        "behavior_top_tracks": BEHAVIOR_TOP_TRACKS,
        "behavior_final_playlists": BEHAVIOR_FINAL_PLAYLISTS,
        "behavior_final_tracks": BEHAVIOR_FINAL_TRACKS,
        "graph_top_edges": GRAPH_TOP_EDGES,
    }
    if manifest.get("parameters") != expected_params:
        return False

    for path in manifest.get("paths", {}).values():
        if not Path(path).exists():
            return False

    return manifest.get("repo_root") == str(repo_root)


def _build_audio_sample(repo_root: Path) -> pl.DataFrame:
    audio = upc_datasets.load_dataset("pachamix_audio_core", root=repo_root, download=False)
    audio_sample = (
        audio.filter(pl.col("genre_top").is_not_null())
        .sample(n=min(AUDIO_SAMPLE_SIZE, audio.height), seed=42)
        .sort("track_id")
    )

    output_path = _artifact_dir(repo_root) / AUDIO_SAMPLE_NAME
    audio_sample.write_parquet(output_path)
    return audio_sample


def _build_lyrics_subset(repo_root: Path) -> pl.DataFrame:
    lyrics_path = repo_root / "data" / "processed" / "pachamix_lyrics_long.parquet"
    lyrics_scan = pl.scan_parquet(lyrics_path)

    top_tokens = (
        lyrics_scan.group_by("token")
        .agg(pl.sum("count").alias("total_count"))
        .sort("total_count", descending=True)
        .head(LYRICS_TOP_TOKENS)
        .collect()
        .get_column("token")
        .to_list()
    )

    top_tracks = (
        lyrics_scan.group_by("msd_track_id")
        .agg(pl.sum("count").alias("total_count"))
        .sort("total_count", descending=True)
        .head(LYRICS_TOP_TRACKS)
        .collect()
        .get_column("msd_track_id")
        .to_list()
    )

    lyrics_subset = (
        lyrics_scan.filter(
            pl.col("token").is_in(top_tokens)
            & pl.col("msd_track_id").is_in(top_tracks)
        )
        .collect()
        .sort(["msd_track_id", "token"])
    )

    output_path = _artifact_dir(repo_root) / LYRICS_SUBSET_NAME
    lyrics_subset.write_parquet(output_path)
    return lyrics_subset


def _build_behavior_subset(repo_root: Path) -> dict[str, pl.DataFrame]:
    stats_path = repo_root / "data" / "processed" / "pachamix_playlists" / "playlist_stats.parquet"
    popularity_path = repo_root / "data" / "processed" / "pachamix_playlists" / "track_popularity.parquet"
    events_path = repo_root / "data" / "processed" / "pachamix_playlists" / "playlist_events.parquet"

    top_playlist_ids = (
        pl.scan_parquet(stats_path)
        .filter(pl.col("track_count") >= 12)
        .sort("track_count", descending=True)
        .head(BEHAVIOR_TOP_PLAYLISTS)
        .collect()
        .get_column("playlist_id")
        .to_list()
    )

    top_track_uris = (
        pl.scan_parquet(popularity_path)
        .head(BEHAVIOR_TOP_TRACKS)
        .collect()
        .get_column("track_uri")
        .to_list()
    )

    events = (
        pl.scan_parquet(events_path)
        .filter(
            pl.col("playlist_id").is_in(top_playlist_ids)
            & pl.col("track_uri").is_in(top_track_uris)
        )
        .collect()
        .sort(["playlist_id", "position"])
    )

    playlist_stats = _playlist_stats_from_events(events)
    top_playlist_ids = (
        playlist_stats.filter(pl.col("track_count") >= 8)
        .sort("track_count", descending=True)
        .head(BEHAVIOR_FINAL_PLAYLISTS)
        .get_column("playlist_id")
        .to_list()
    )

    events = events.filter(pl.col("playlist_id").is_in(top_playlist_ids))
    track_popularity = _track_popularity_from_events(events)
    top_track_uris = (
        track_popularity.filter(pl.col("playlist_count") >= 5)
        .head(BEHAVIOR_FINAL_TRACKS)
        .get_column("track_uri")
        .to_list()
    )

    events = (
        events.filter(pl.col("track_uri").is_in(top_track_uris))
        .sort(["playlist_id", "position"])
        .unique(
            subset=["playlist_id", "track_uri", "position"],
            keep="first",
            maintain_order=True,
        )
    )

    playlist_stats = _playlist_stats_from_events(events).sort(
        ["track_count", "playlist_id"],
        descending=[True, False],
    )
    track_popularity = _track_popularity_from_events(events)

    output_dir = _artifact_dir(repo_root)
    events.write_parquet(output_dir / BEHAVIOR_EVENTS_NAME)
    playlist_stats.write_parquet(output_dir / BEHAVIOR_STATS_NAME)
    track_popularity.write_parquet(output_dir / BEHAVIOR_POPULARITY_NAME)

    return {
        "events": events,
        "playlist_stats": playlist_stats,
        "track_popularity": track_popularity,
    }


def _build_song_graph_subset(events: pl.DataFrame) -> pl.DataFrame:
    unique_events = events.select(["playlist_id", "track_uri"]).unique()
    left = unique_events.rename({"track_uri": "src_track_uri"})
    right = unique_events.rename({"track_uri": "dst_track_uri"})

    return (
        left.join(right, on="playlist_id", how="inner")
        .filter(pl.col("src_track_uri") < pl.col("dst_track_uri"))
        .group_by(["src_track_uri", "dst_track_uri"])
        .agg(pl.len().alias("weight"))
        .sort(
            ["weight", "src_track_uri", "dst_track_uri"],
            descending=[True, False, False],
        )
        .head(GRAPH_TOP_EDGES)
    )


def _playlist_stats_from_events(events: pl.DataFrame) -> pl.DataFrame:
    return (
        events.group_by(["playlist_id", "playlist_name"])
        .agg(pl.len().alias("track_count"))
        .sort("playlist_id")
    )


def _track_popularity_from_events(events: pl.DataFrame) -> pl.DataFrame:
    return (
        events.group_by("track_uri")
        .agg(pl.col("playlist_id").n_unique().alias("playlist_count"))
        .sort(["playlist_count", "track_uri"], descending=[True, False])
    )
