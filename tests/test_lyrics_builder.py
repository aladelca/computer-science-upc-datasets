from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from pachamix_data.builders.lyrics_core import build_lyrics_core


FIXTURES = Path(__file__).parent / "fixtures" / "lyrics"


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
                    "Song One",
                    "SO001",
                    "Album One",
                    "AR001",
                    "MBID001",
                    "Artist One",
                    180.5,
                    0.5,
                    0.7,
                    2010,
                ),
                (
                    "TR002",
                    "Song Two",
                    "SO002",
                    "Album Two",
                    "AR002",
                    "MBID002",
                    "Artist Two",
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


def test_build_lyrics_core_creates_structured_track_features(tmp_path: Path) -> None:
    output_path = tmp_path / "lyrics_core.parquet"

    frame = build_lyrics_core(
        lyrics_txt=FIXTURES / "musixmatch_sample.txt",
        output_parquet=output_path,
    )

    assert output_path.exists()
    assert frame.columns == ["msd_track_id", "token", "count"]
    assert frame.shape == (8, 3)
    assert frame.sort(["msd_track_id", "token"]).to_dicts() == [
        {"msd_track_id": "TR001", "token": "bright", "count": 2},
        {"msd_track_id": "TR001", "token": "love", "count": 3},
        {"msd_track_id": "TR001", "token": "night", "count": 1},
        {"msd_track_id": "TR002", "token": "love", "count": 1},
        {"msd_track_id": "TR002", "token": "night", "count": 4},
        {"msd_track_id": "TR002", "token": "storm", "count": 2},
        {"msd_track_id": "TR003", "token": "bright", "count": 1},
        {"msd_track_id": "TR003", "token": "calm", "count": 6},
    ]


def test_build_lyrics_core_rejects_bad_token_pairs(tmp_path: Path) -> None:
    broken_input = tmp_path / "broken.txt"
    broken_input.write_text("TR001,love=3,night:1\n", encoding="utf-8")

    with pytest.raises(ValueError, match="token:count"):
        build_lyrics_core(
            lyrics_txt=broken_input,
            output_parquet=tmp_path / "ignored.parquet",
        )


def test_build_lyrics_core_joins_track_metadata(tmp_path: Path) -> None:
    output_path = tmp_path / "lyrics_with_metadata.parquet"
    metadata_db = _create_track_metadata_db(tmp_path / "track_metadata.db")

    frame = build_lyrics_core(
        lyrics_txt=FIXTURES / "musixmatch_sample.txt",
        output_parquet=output_path,
        metadata_db=metadata_db,
    )

    assert output_path.exists()
    assert {
        "msd_track_id",
        "title",
        "song_id",
        "release",
        "artist_id",
        "artist_mbid",
        "artist_name",
        "duration",
        "artist_familiarity",
        "artist_hotttnesss",
        "year",
        "token",
        "count",
    }.issubset(frame.columns)
    rows = frame.filter(frame["msd_track_id"] == "TR001").sort("token").to_dicts()
    assert rows[0]["title"] == "Song One"
    assert rows[0]["artist_name"] == "Artist One"
    assert rows[0]["year"] == 2010
    missing_metadata = frame.filter(frame["msd_track_id"] == "TR003").select(
        ["title", "artist_name", "release"]
    ).row(0)
    assert missing_metadata == (None, None, None)
