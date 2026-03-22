from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import polars as pl


@dataclass(slots=True)
class PlaylistBuildResult:
    events: pl.DataFrame
    track_popularity: pl.DataFrame
    playlist_stats: pl.DataFrame
    events_path: Path
    track_popularity_path: Path
    playlist_stats_path: Path


def _is_playlist2vec_export(path: Path) -> bool:
    if not path.is_dir():
        return False
    required = (
        path / "playlist.csv",
        path / "track.csv",
        path / "track_playlist1.csv",
    )
    return all(file.exists() for file in required)


def _iter_mpd_files(path: Path) -> list[Path]:
    if path.is_dir():
        return sorted(file for file in path.rglob("*.json") if file.is_file())
    return [path]


def _build_events_from_playlist2vec(path: Path) -> pl.DataFrame:
    playlists = pl.read_csv(path / "playlist.csv")
    tracks = pl.read_csv(path / "track.csv")
    memberships = pl.read_csv(path / "track_playlist1.csv")

    if "position" in memberships.columns:
        memberships = memberships.with_columns(
            pl.col("position").cast(pl.Int64),
            pl.lit(True).alias("position_observed"),
        )
    else:
        memberships = memberships.sort(["playlist_id", "track_id"]).with_columns(
            (pl.col("track_id").cum_count().over("playlist_id") - 1)
            .cast(pl.Int64)
            .alias("position"),
            pl.lit(False).alias("position_observed"),
        )

    events = (
        memberships.join(playlists, on="playlist_id", how="left")
        .join(tracks, on="track_id", how="left")
        .with_columns(
            pl.format("playlist2vec:track:{}", pl.col("track_id")).alias("track_uri"),
            pl.col("name").fill_null("").alias("playlist_name"),
            pl.col("track_name").fill_null(""),
            pl.col("artist_name").fill_null(""),
            pl.col("album_name").fill_null(""),
            pl.col("position").cast(pl.Int64),
            pl.col("position_observed").cast(pl.Boolean),
        )
        .select(
            [
                "playlist_id",
                "playlist_name",
                "track_uri",
                "track_name",
                "artist_name",
                "album_name",
                "position",
                "position_observed",
            ]
        )
        .sort(["playlist_id", "position"])
    )
    return events


def _build_events_from_mpd(path: Path) -> pl.DataFrame:
    rows: list[dict[str, object]] = []
    for json_file in _iter_mpd_files(path):
        payload = json.loads(json_file.read_text(encoding="utf-8"))
        playlists = payload.get("playlists", [])
        for playlist in playlists:
            playlist_id = int(playlist["pid"])
            playlist_name = playlist.get("name", "")
            for track in playlist.get("tracks", []):
                rows.append(
                    {
                        "playlist_id": playlist_id,
                        "playlist_name": playlist_name,
                        "track_uri": track["track_uri"],
                        "track_name": track.get("track_name", ""),
                        "artist_name": track.get("artist_name", ""),
                        "album_name": track.get("album_name", ""),
                        "position": int(track.get("pos", 0)),
                        "position_observed": True,
                    }
                )
    return pl.DataFrame(rows)


def build_playlist_events(
    mpd_json: str | Path,
    output_dir: str | Path,
) -> PlaylistBuildResult:
    input_path = Path(mpd_json)
    destination = Path(output_dir)

    events = (
        (
            _build_events_from_playlist2vec(input_path)
            if _is_playlist2vec_export(input_path)
            else _build_events_from_mpd(input_path)
        )
        .sort(["playlist_id", "position"])
        .unique(
            subset=["playlist_id", "track_uri", "position"],
            keep="first",
            maintain_order=True,
        )
    )
    track_popularity = (
        events.group_by("track_uri")
        .agg(pl.col("playlist_id").n_unique().alias("playlist_count"))
        .sort(["playlist_count", "track_uri"], descending=[True, False])
    )
    playlist_stats = (
        events.group_by(["playlist_id", "playlist_name"])
        .agg(pl.len().alias("track_count"))
        .sort("playlist_id")
    )

    destination.mkdir(parents=True, exist_ok=True)
    events_path = destination / "playlist_events.parquet"
    track_popularity_path = destination / "track_popularity.parquet"
    playlist_stats_path = destination / "playlist_stats.parquet"

    events.write_parquet(events_path)
    track_popularity.write_parquet(track_popularity_path)
    playlist_stats.write_parquet(playlist_stats_path)

    return PlaylistBuildResult(
        events=events,
        track_popularity=track_popularity,
        playlist_stats=playlist_stats,
        events_path=events_path,
        track_popularity_path=track_popularity_path,
        playlist_stats_path=playlist_stats_path,
    )
