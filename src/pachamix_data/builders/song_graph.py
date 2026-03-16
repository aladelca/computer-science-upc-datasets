from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import polars as pl


@dataclass(slots=True)
class SongGraphBuildResult:
    edges: pl.DataFrame
    edges_path: Path


def build_song_graph(
    playlist_events_parquet: str | Path,
    output_parquet: str | Path,
) -> SongGraphBuildResult:
    input_path = Path(playlist_events_parquet)
    output_path = Path(output_parquet)

    events = (
        pl.read_parquet(input_path)
        .select(["playlist_id", "track_uri"])
        .unique()
    )

    left = events.rename({"track_uri": "src_track_uri"})
    right = events.rename({"track_uri": "dst_track_uri"})

    edges = (
        left.join(right, on="playlist_id", how="inner")
        .filter(pl.col("src_track_uri") < pl.col("dst_track_uri"))
        .group_by(["src_track_uri", "dst_track_uri"])
        .agg(pl.len().alias("weight"))
        .sort(["weight", "src_track_uri", "dst_track_uri"], descending=[True, False, False])
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    edges.write_parquet(output_path)
    return SongGraphBuildResult(edges=edges, edges_path=output_path)
