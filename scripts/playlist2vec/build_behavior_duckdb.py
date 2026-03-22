from __future__ import annotations

import argparse
from pathlib import Path

import duckdb


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build large Playlist2vec behavior parquets with DuckDB using the "
            "CSV exports produced by the repo workflow."
        )
    )
    parser.add_argument("--raw-playlist2vec-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--db-path", required=True)
    parser.add_argument("--temp-dir", required=True)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--memory-limit", default="8GB")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    raw_dir = Path(args.raw_playlist2vec_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    db_path = Path(args.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    temp_dir = Path(args.temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    playlist_csv = (raw_dir / "playlist.csv").resolve()
    track_csv = (raw_dir / "track.csv").resolve()
    track_playlist_csv = (raw_dir / "track_playlist1.csv").resolve()

    events_path = (output_dir / "playlist_events.parquet").resolve()
    stats_path = (output_dir / "playlist_stats.parquet").resolve()
    popularity_path = (output_dir / "track_popularity.parquet").resolve()

    for path in (events_path, stats_path, popularity_path):
        if path.exists():
            path.unlink()

    connection = duckdb.connect(str(db_path))
    try:
        connection.execute(f"PRAGMA threads={args.threads}")
        connection.execute(f"PRAGMA memory_limit='{args.memory_limit}'")
        connection.execute(f"PRAGMA temp_directory='{temp_dir.resolve()}'")

        connection.execute(
            f"""
            COPY (
                WITH memberships AS (
                    SELECT
                        playlist_id,
                        track_id,
                        ROW_NUMBER() OVER (
                            PARTITION BY playlist_id
                            ORDER BY track_id
                        ) - 1 AS position,
                        FALSE AS position_observed
                    FROM read_csv(
                        '{track_playlist_csv}',
                        header = true,
                        columns = {{
                            'playlist_id': 'VARCHAR',
                            'track_id': 'VARCHAR'
                        }}
                    )
                ),
                playlists AS (
                    SELECT
                        playlist_id,
                        COALESCE(name, '') AS playlist_name
                    FROM read_csv(
                        '{playlist_csv}',
                        header = true,
                        columns = {{
                            'playlist_id': 'VARCHAR',
                            'name': 'VARCHAR'
                        }}
                    )
                ),
                tracks AS (
                    SELECT
                        track_id,
                        COALESCE(track_name, '') AS track_name,
                        COALESCE(artist_name, '') AS artist_name,
                        COALESCE(album_name, '') AS album_name
                    FROM read_csv(
                        '{track_csv}',
                        header = true,
                        columns = {{
                            'track_id': 'VARCHAR',
                            'track_name': 'VARCHAR',
                            'artist_name': 'VARCHAR',
                            'album_name': 'VARCHAR'
                        }}
                    )
                )
                SELECT
                    memberships.playlist_id,
                    COALESCE(playlists.playlist_name, '') AS playlist_name,
                    'playlist2vec:track:' || memberships.track_id AS track_uri,
                    COALESCE(tracks.track_name, '') AS track_name,
                    COALESCE(tracks.artist_name, '') AS artist_name,
                    COALESCE(tracks.album_name, '') AS album_name,
                    memberships.position,
                    memberships.position_observed
                FROM memberships
                LEFT JOIN playlists USING (playlist_id)
                LEFT JOIN tracks USING (track_id)
            ) TO '{events_path}' (FORMAT PARQUET, COMPRESSION ZSTD)
            """
        )

        connection.execute(
            f"""
            COPY (
                SELECT
                    playlist_id,
                    playlist_name,
                    COUNT(*) AS track_count
                FROM read_parquet('{events_path}')
                GROUP BY playlist_id, playlist_name
                ORDER BY playlist_id
            ) TO '{stats_path}' (FORMAT PARQUET, COMPRESSION ZSTD)
            """
        )

        connection.execute(
            f"""
            COPY (
                SELECT
                    track_uri,
                    COUNT(DISTINCT playlist_id) AS playlist_count
                FROM read_parquet('{events_path}')
                GROUP BY track_uri
                ORDER BY playlist_count DESC, track_uri
            ) TO '{popularity_path}' (FORMAT PARQUET, COMPRESSION ZSTD)
            """
        )

        for label, path in (
            ("events", events_path),
            ("stats", stats_path),
            ("popularity", popularity_path),
        ):
            count = connection.execute(
                f"SELECT COUNT(*) FROM read_parquet('{path}')"
            ).fetchone()[0]
            print(f"{label}: {path} ({count} rows)")
    finally:
        connection.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
