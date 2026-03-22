from __future__ import annotations

from pathlib import Path

import polars as pl

from pachamix_data.playlist2vec_sql import extract_playlist2vec_exports


def test_extract_playlist2vec_exports_without_mysql(tmp_path: Path) -> None:
    sql_dump = tmp_path / "playlist2vec.sql"
    sql_dump.write_text(
        """
INSERT INTO `album` VALUES ('alb1','Album One',NULL),('alb2','Album Two',NULL);
INSERT INTO `artist` VALUES ('art1','Artist One',NULL),('art2','Artist Two',NULL);
INSERT INTO `playlist` VALUES ('10','Focus Mix',NULL,NULL,2),('20','Run Mix',NULL,NULL,1);
INSERT INTO `track` VALUES ('trk1','Song One',180,10,'false',NULL,'spotify:track:trk1','alb1'),('trk2','Song Two',200,20,'false',NULL,'spotify:track:trk2','alb2');
INSERT INTO `track_artist1` VALUES ('trk1','art1'),('trk1','art2'),('trk2','art2');
INSERT INTO `track_playlist1` VALUES ('trk1','10'),('trk2','10'),('trk2','20');
        """.strip()
        + "\n",
        encoding="latin-1",
    )

    exports_dir = tmp_path / "playlist2vec"
    processed_root = tmp_path / "processed"
    result = extract_playlist2vec_exports(
        sql_dump,
        output_dir=exports_dir,
        sqlite_db_path=tmp_path / "playlist2vec.sqlite",
        processed_root=processed_root,
        batch_size=2,
    )

    assert result.playlist_rows == 2
    assert result.track_rows == 2
    assert result.membership_rows == 3

    playlist_csv = (exports_dir / "playlist.csv").read_text(encoding="utf-8")
    assert "playlist_id,name" in playlist_csv
    assert "10,Focus Mix" in playlist_csv

    track_csv = pl.read_csv(exports_dir / "track.csv").sort("track_id")
    assert track_csv.to_dicts() == [
        {
            "track_id": "trk1",
            "track_name": "Song One",
            "artist_name": "Artist One | Artist Two",
            "album_name": "Album One",
        },
        {
            "track_id": "trk2",
            "track_name": "Song Two",
            "artist_name": "Artist Two",
            "album_name": "Album Two",
        },
    ]

    memberships = pl.read_csv(exports_dir / "track_playlist1.csv").sort(
        ["playlist_id", "track_id"]
    )
    assert memberships.to_dicts() == [
        {"playlist_id": 10, "track_id": "trk1"},
        {"playlist_id": 10, "track_id": "trk2"},
        {"playlist_id": 20, "track_id": "trk2"},
    ]

    playlist_events = pl.read_parquet(
        processed_root / "pachamix_playlists" / "playlist_events.parquet"
    ).sort(["playlist_id", "position"])
    assert playlist_events.height == 3
    assert playlist_events.get_column("position_observed").to_list() == [
        False,
        False,
        False,
    ]
    assert playlist_events.get_column("track_uri").to_list() == [
        "playlist2vec:track:trk1",
        "playlist2vec:track:trk2",
        "playlist2vec:track:trk2",
    ]

    song_graph = pl.read_parquet(processed_root / "pachamix_song_graph_edges.parquet")
    assert song_graph.to_dicts() == [
        {
            "src_track_uri": "playlist2vec:track:trk1",
            "dst_track_uri": "playlist2vec:track:trk2",
            "weight": 1,
        }
    ]
