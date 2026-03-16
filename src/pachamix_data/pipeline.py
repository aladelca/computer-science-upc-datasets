from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pachamix_data.builders import (
    build_audio_core,
    build_lyrics_core,
    build_playlist_events,
    build_song_graph,
)


@dataclass(slots=True)
class CourseDatasetBuildResult:
    audio_core_path: Path
    lyrics_core_path: Path
    playlist_events_path: Path | None
    song_graph_path: Path | None


def _require_path(path: Path, description: str) -> Path:
    if not path.exists():
        raise FileNotFoundError(f"missing {description}: {path}")
    return path


def _is_playlist2vec_export(path: Path) -> bool:
    required_files = (
        path / "playlist.csv",
        path / "track.csv",
        path / "track_playlist1.csv",
    )
    return path.is_dir() and all(file.exists() for file in required_files)


def _has_mpd_json(path: Path) -> bool:
    return path.is_dir() and any(path.rglob("*.json"))


def _discover_playlist_root(raw_path: Path) -> Path | None:
    playlist2vec_root = raw_path / "playlist2vec"
    if _is_playlist2vec_export(playlist2vec_root):
        return playlist2vec_root
    mpd_root = raw_path / "mpd"
    if _has_mpd_json(mpd_root):
        return mpd_root
    return None


def _discover_msd_metadata_db(raw_path: Path) -> Path | None:
    candidates = (
        raw_path / "msd" / "track_metadata.db",
        raw_path / "track_metadata.db",
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def build_course_dataset(
    raw_root: str | Path,
    processed_root: str | Path,
    lyrics_top_n_tokens: int = 0,
) -> CourseDatasetBuildResult:
    raw_path = Path(raw_root)
    processed_path = Path(processed_root)

    fma_root = _require_path(raw_path / "fma", "FMA directory")
    lyrics_root = _require_path(raw_path / "musixmatch_msd", "musiXmatch/MSD directory")
    playlist_root = _discover_playlist_root(raw_path)
    metadata_db = _discover_msd_metadata_db(raw_path)

    audio_core_path = processed_path / "pachamix_audio_core.parquet"
    lyrics_core_path = processed_path / "pachamix_lyrics_long.parquet"
    playlist_output_dir = processed_path / "pachamix_playlists"
    song_graph_path = processed_path / "pachamix_song_graph_edges.parquet"

    build_audio_core(
        tracks_csv=_require_path(fma_root / "tracks.csv", "FMA tracks.csv"),
        features_csv=_require_path(fma_root / "features.csv", "FMA features.csv"),
        output_parquet=audio_core_path,
    )
    build_lyrics_core(
        lyrics_txt=lyrics_root,
        output_parquet=lyrics_core_path,
        top_n_tokens=lyrics_top_n_tokens,
        metadata_db=metadata_db,
    )

    playlist_events_path: Path | None = None
    built_song_graph_path: Path | None = None
    if playlist_root is not None:
        playlist_result = build_playlist_events(
            mpd_json=playlist_root,
            output_dir=playlist_output_dir,
        )
        playlist_events_path = playlist_result.events_path
        build_song_graph(
            playlist_events_parquet=playlist_result.events_path,
            output_parquet=song_graph_path,
        )
        built_song_graph_path = song_graph_path

    return CourseDatasetBuildResult(
        audio_core_path=audio_core_path,
        lyrics_core_path=lyrics_core_path,
        playlist_events_path=playlist_events_path,
        song_graph_path=built_song_graph_path,
    )
