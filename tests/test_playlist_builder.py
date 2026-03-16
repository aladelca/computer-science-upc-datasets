from __future__ import annotations

from pathlib import Path

from pachamix_data.builders.playlist_events import build_playlist_events


FIXTURES = Path(__file__).parent / "fixtures" / "mpd"


def test_build_playlist_events_creates_events_and_summary_tables(tmp_path: Path) -> None:
    output_dir = tmp_path / "playlist_outputs"

    result = build_playlist_events(
        mpd_json=FIXTURES / "sample_playlists.json",
        output_dir=output_dir,
    )

    assert result.events_path.exists()
    assert result.track_popularity_path.exists()
    assert result.playlist_stats_path.exists()

    assert result.events.shape == (5, 7)
    assert result.events.columns == [
        "playlist_id",
        "playlist_name",
        "track_uri",
        "track_name",
        "artist_name",
        "album_name",
        "position",
    ]

    popularity = {
        row["track_uri"]: row["playlist_count"]
        for row in result.track_popularity.to_dicts()
    }
    assert popularity["spotify:track:A"] == 2
    assert popularity["spotify:track:B"] == 1

    stats = {
        row["playlist_id"]: row["track_count"]
        for row in result.playlist_stats.to_dicts()
    }
    assert stats[100] == 3
    assert stats[200] == 2
