from __future__ import annotations

from pathlib import Path

from pachamix_data.builders.playlist_events import build_playlist_events

FIXTURES = Path(__file__).parent / "fixtures" / "playlist2vec"


def test_build_playlist_events_reads_playlist2vec_exports(tmp_path: Path) -> None:
    result = build_playlist_events(
        mpd_json=FIXTURES,
        output_dir=tmp_path / "playlist_outputs",
    )

    assert result.events.shape == (4, 8)
    assert result.events.columns == [
        "playlist_id",
        "playlist_name",
        "track_uri",
        "track_name",
        "artist_name",
        "album_name",
        "position",
        "position_observed",
    ]

    rows = result.events.sort(["playlist_id", "position"]).to_dicts()
    assert rows[0]["playlist_name"] == "Focus Mode"
    assert rows[0]["track_uri"] == "playlist2vec:track:1"
    assert rows[3]["track_name"] == "Gamma"
    assert all(row["position_observed"] is True for row in rows)

    popularity = {
        row["track_uri"]: row["playlist_count"]
        for row in result.track_popularity.to_dicts()
    }
    assert popularity["playlist2vec:track:1"] == 2


def test_build_playlist_events_reads_official_like_playlist2vec_without_position(
    tmp_path: Path,
) -> None:
    result = build_playlist_events(
        mpd_json=Path(__file__).parent / "fixtures" / "playlist2vec_no_position",
        output_dir=tmp_path / "playlist_outputs",
    )

    assert result.events.shape == (4, 8)
    rows = result.events.sort(["playlist_id", "position"]).to_dicts()
    assert rows[0]["playlist_id"] == 10
    assert rows[0]["position"] == 0
    assert rows[1]["position"] == 1
    assert rows[2]["playlist_id"] == 20
    assert rows[2]["position"] == 0
    assert rows[3]["position"] == 1
    assert all(row["position_observed"] is False for row in rows)
