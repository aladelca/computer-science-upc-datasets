from __future__ import annotations

import os
import sqlite3
import shutil
import subprocess
import sys
from pathlib import Path

import polars as pl


ROOT = Path(__file__).resolve().parents[1]
RAW_FIXTURES = ROOT / "tests" / "fixtures" / "course_raw"


def _create_track_metadata_db(path: Path) -> Path:
    connection = sqlite3.connect(path)
    try:
        connection.execute(
            """
            CREATE TABLE songs (
                track_id TEXT PRIMARY KEY,
                title TEXT,
                song_id TEXT,
                release TEXT,
                artist_id TEXT,
                artist_mbid TEXT,
                artist_name TEXT,
                duration REAL,
                artist_familiarity REAL,
                artist_hotttnesss REAL,
                year INTEGER
            )
            """
        )
        connection.executemany(
            """
            INSERT INTO songs (
                track_id, title, song_id, release, artist_id, artist_mbid,
                artist_name, duration, artist_familiarity, artist_hotttnesss, year
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    "TR001",
                    "Fixture Song One",
                    "SO001",
                    "Fixture Album One",
                    "AR001",
                    "MBID001",
                    "Fixture Artist One",
                    180.5,
                    0.5,
                    0.7,
                    2010,
                ),
                (
                    "TR002",
                    "Fixture Song Two",
                    "SO002",
                    "Fixture Album Two",
                    "AR002",
                    "MBID002",
                    "Fixture Artist Two",
                    200.0,
                    0.6,
                    0.8,
                    2011,
                ),
            ],
        )
        connection.commit()
    finally:
        connection.close()
    return path


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


def test_build_course_dataset_succeeds_without_playlist_behavior_data(
    tmp_path: Path,
) -> None:
    raw_root = tmp_path / "raw"
    shutil.copytree(RAW_FIXTURES / "fma", raw_root / "fma")
    shutil.copytree(RAW_FIXTURES / "musixmatch_msd", raw_root / "musixmatch_msd")
    processed_root = tmp_path / "processed"

    result = run_cli(
        "build-course-dataset",
        "--raw-root",
        str(raw_root),
        "--processed-root",
        str(processed_root),
    )

    assert result.returncode == 0, result.stderr
    assert (processed_root / "pachamix_audio_core.parquet").exists()
    assert (processed_root / "pachamix_lyrics_long.parquet").exists()
    assert not (processed_root / "pachamix_playlists").exists()
    assert not (processed_root / "pachamix_song_graph_edges.parquet").exists()
    assert "playlist-events: skipped" in result.stdout
    assert "song-graph: skipped" in result.stdout

    assert pl.read_parquet(processed_root / "pachamix_audio_core.parquet").height == 2
    assert pl.read_parquet(processed_root / "pachamix_lyrics_long.parquet").height == 8


def test_build_course_dataset_ignores_empty_playlist_directory(
    tmp_path: Path,
) -> None:
    raw_root = tmp_path / "raw"
    shutil.copytree(RAW_FIXTURES / "fma", raw_root / "fma")
    shutil.copytree(RAW_FIXTURES / "musixmatch_msd", raw_root / "musixmatch_msd")
    (raw_root / "mpd").mkdir(parents=True)
    processed_root = tmp_path / "processed"

    result = run_cli(
        "build-course-dataset",
        "--raw-root",
        str(raw_root),
        "--processed-root",
        str(processed_root),
    )

    assert result.returncode == 0, result.stderr
    assert not (processed_root / "pachamix_playlists").exists()
    assert not (processed_root / "pachamix_song_graph_edges.parquet").exists()
    assert "playlist-events: skipped" in result.stdout


def test_build_course_dataset_enriches_lyrics_with_msd_metadata(
    tmp_path: Path,
) -> None:
    raw_root = tmp_path / "raw"
    shutil.copytree(RAW_FIXTURES / "fma", raw_root / "fma")
    shutil.copytree(RAW_FIXTURES / "musixmatch_msd", raw_root / "musixmatch_msd")
    msd_root = raw_root / "msd"
    msd_root.mkdir(parents=True)
    _create_track_metadata_db(msd_root / "track_metadata.db")
    processed_root = tmp_path / "processed"

    result = run_cli(
        "build-course-dataset",
        "--raw-root",
        str(raw_root),
        "--processed-root",
        str(processed_root),
    )

    assert result.returncode == 0, result.stderr
    lyrics = pl.read_parquet(processed_root / "pachamix_lyrics_long.parquet")
    assert {"title", "artist_name", "release", "year"}.issubset(lyrics.columns)
    matched_rows = lyrics.filter(lyrics["msd_track_id"] == "TR001").sort("token").to_dicts()
    assert matched_rows[0]["title"] == "Fixture Song One"
    assert matched_rows[0]["artist_name"] == "Fixture Artist One"
