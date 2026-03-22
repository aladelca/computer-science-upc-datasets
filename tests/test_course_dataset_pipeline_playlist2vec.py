from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import polars as pl

ROOT = Path(__file__).resolve().parents[1]
RAW_FIXTURES = ROOT / "tests" / "fixtures" / "course_raw_playlist2vec"
RAW_FIXTURES_NO_POSITION = (
    ROOT / "tests" / "fixtures" / "course_raw_playlist2vec_no_position"
)


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    return subprocess.run(
        [sys.executable, "-m", "pachamix_data.cli", *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_build_course_dataset_prefers_playlist2vec_when_available(
    tmp_path: Path,
) -> None:
    processed_root = tmp_path / "processed"

    result = run_cli(
        "build-course-dataset",
        "--raw-root",
        str(RAW_FIXTURES),
        "--processed-root",
        str(processed_root),
    )

    assert result.returncode == 0, result.stderr
    assert (processed_root / "pachamix_lyrics_long.parquet").exists()
    playlist_events = pl.read_parquet(
        processed_root / "pachamix_playlists" / "playlist_events.parquet"
    )
    assert playlist_events.height == 4
    assert (
        playlist_events.get_column("track_uri")
        .to_list()[0]
        .startswith("playlist2vec:track:")
    )
    assert playlist_events.get_column("position_observed").to_list() == [
        True,
        True,
        True,
        True,
    ]


def test_build_course_dataset_supports_official_like_playlist2vec_without_position(
    tmp_path: Path,
) -> None:
    processed_root = tmp_path / "processed"

    result = run_cli(
        "build-course-dataset",
        "--raw-root",
        str(RAW_FIXTURES_NO_POSITION),
        "--processed-root",
        str(processed_root),
    )

    assert result.returncode == 0, result.stderr
    playlist_events = pl.read_parquet(
        processed_root / "pachamix_playlists" / "playlist_events.parquet"
    )
    assert playlist_events.height == 4
    assert playlist_events.columns == [
        "playlist_id",
        "playlist_name",
        "track_uri",
        "track_name",
        "artist_name",
        "album_name",
        "position",
        "position_observed",
    ]
    assert playlist_events.get_column("position_observed").to_list() == [
        False,
        False,
        False,
        False,
    ]
