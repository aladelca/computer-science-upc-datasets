from __future__ import annotations

from pathlib import Path

from pachamix_data.builders.playlist_events import build_playlist_events


FIXTURES = Path(__file__).parent / "fixtures" / "mpd" / "slices"


def test_build_playlist_events_reads_directory_of_mpd_slices(tmp_path: Path) -> None:
    result = build_playlist_events(
        mpd_json=FIXTURES,
        output_dir=tmp_path / "playlist_outputs",
    )

    assert result.events.shape == (4, 7)
    playlist_ids = result.events.get_column("playlist_id").to_list()
    assert playlist_ids == [100, 100, 200, 200]

    popularity = {
        row["track_uri"]: row["playlist_count"]
        for row in result.track_popularity.to_dicts()
    }
    assert popularity["spotify:track:A"] == 2
    assert popularity["spotify:track:B"] == 1
    assert popularity["spotify:track:C"] == 1
