from __future__ import annotations

from pathlib import Path

from pachamix_data.builders.playlist_events import build_playlist_events
from pachamix_data.builders.song_graph import build_song_graph


FIXTURES = Path(__file__).parent / "fixtures" / "mpd"


def test_build_song_graph_creates_weighted_cooccurrence_edges(tmp_path: Path) -> None:
    playlist_result = build_playlist_events(
        mpd_json=FIXTURES / "sample_playlists.json",
        output_dir=tmp_path / "playlist_outputs",
    )

    graph_result = build_song_graph(
        playlist_events_parquet=playlist_result.events_path,
        output_parquet=tmp_path / "song_graph.parquet",
    )

    assert graph_result.edges_path.exists()
    assert graph_result.edges.columns == ["src_track_uri", "dst_track_uri", "weight"]

    weights = {
        (row["src_track_uri"], row["dst_track_uri"]): row["weight"]
        for row in graph_result.edges.to_dicts()
    }
    assert weights[("spotify:track:A", "spotify:track:B")] == 1
    assert weights[("spotify:track:A", "spotify:track:C")] == 2
    assert weights[("spotify:track:B", "spotify:track:C")] == 1
