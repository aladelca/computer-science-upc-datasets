from __future__ import annotations

import argparse
from typing import Sequence

from pachamix_data.builders import (
    build_audio_core,
    build_lyrics_core,
    build_playlist_events,
    build_song_graph,
)
from pachamix_data.pipeline import build_course_dataset
from pachamix_data.playlist2vec_sql import extract_playlist2vec_exports

SUPPORTED_BUILDERS = (
    "audio-core",
    "lyrics-core",
    "playlist-events",
    "playlist2vec-sql",
    "song-graph",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pachamix-data",
        description="Structured dataset builders for the PachaMix course.",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list-builders", help="List supported dataset builders.")

    audio_parser = subparsers.add_parser(
        "build-audio-core",
        help="Build the structured FMA audio feature dataset.",
    )
    audio_parser.add_argument("--tracks-csv", required=True)
    audio_parser.add_argument("--features-csv", required=True)
    audio_parser.add_argument("--output-parquet", required=True)

    lyrics_parser = subparsers.add_parser(
        "build-lyrics-core",
        help="Build structured lyric token features.",
    )
    lyrics_parser.add_argument("--lyrics-txt", required=True)
    lyrics_parser.add_argument("--output-parquet", required=True)
    lyrics_parser.add_argument("--top-n-tokens", type=int, default=0)
    lyrics_parser.add_argument("--metadata-db")

    playlist_parser = subparsers.add_parser(
        "build-playlist-events",
        help="Build playlist event and summary parquet outputs from MPD JSON.",
    )
    playlist_parser.add_argument("--mpd-json", required=True)
    playlist_parser.add_argument("--output-dir", required=True)

    graph_parser = subparsers.add_parser(
        "build-song-graph",
        help="Build weighted song-song co-occurrence edges from playlist events.",
    )
    graph_parser.add_argument("--playlist-events-parquet", required=True)
    graph_parser.add_argument("--output-parquet", required=True)

    playlist2vec_sql_parser = subparsers.add_parser(
        "extract-playlist2vec-sql",
        help=(
            "Extract Playlist2vec CSV exports from the official SQL dump using "
            "SQLite instead of MySQL."
        ),
    )
    playlist2vec_sql_parser.add_argument("--sql-dump", required=True)
    playlist2vec_sql_parser.add_argument("--output-dir", required=True)
    playlist2vec_sql_parser.add_argument("--sqlite-db")
    playlist2vec_sql_parser.add_argument("--processed-root")
    playlist2vec_sql_parser.add_argument("--batch-size", type=int, default=5000)

    course_parser = subparsers.add_parser(
        "build-course-dataset",
        help="Build all core course datasets from a raw-root layout.",
    )
    course_parser.add_argument("--raw-root", required=True)
    course_parser.add_argument("--processed-root", required=True)
    course_parser.add_argument("--lyrics-top-n-tokens", type=int, default=0)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "list-builders":
        print("\n".join(SUPPORTED_BUILDERS))
        return 0
    if args.command == "build-audio-core":
        frame = build_audio_core(
            tracks_csv=args.tracks_csv,
            features_csv=args.features_csv,
            output_parquet=args.output_parquet,
        )
        print(f"wrote {frame.height} rows to {args.output_parquet}")
        return 0
    if args.command == "build-lyrics-core":
        frame = build_lyrics_core(
            lyrics_txt=args.lyrics_txt,
            output_parquet=args.output_parquet,
            top_n_tokens=args.top_n_tokens,
            metadata_db=args.metadata_db,
        )
        print(f"wrote {frame.height} rows to {args.output_parquet}")
        return 0
    if args.command == "build-playlist-events":
        playlist_result = build_playlist_events(
            mpd_json=args.mpd_json,
            output_dir=args.output_dir,
        )
        print(
            f"wrote {playlist_result.events.height} playlist events to "
            f"{playlist_result.events_path}"
        )
        return 0
    if args.command == "build-song-graph":
        graph_result = build_song_graph(
            playlist_events_parquet=args.playlist_events_parquet,
            output_parquet=args.output_parquet,
        )
        print(
            f"wrote {graph_result.edges.height} graph edges to "
            f"{graph_result.edges_path}"
        )
        return 0
    if args.command == "extract-playlist2vec-sql":
        export_result = extract_playlist2vec_exports(
            args.sql_dump,
            output_dir=args.output_dir,
            sqlite_db_path=args.sqlite_db,
            processed_root=args.processed_root,
            batch_size=args.batch_size,
        )
        print(f"sqlite-db: {export_result.sqlite_db_path}")
        print(
            f"playlist.csv: {export_result.playlist_csv_path} "
            f"({export_result.playlist_rows} rows)"
        )
        print(
            f"track.csv: {export_result.track_csv_path} "
            f"({export_result.track_rows} rows)"
        )
        print(
            f"track_playlist1.csv: {export_result.track_playlist_csv_path} "
            f"({export_result.membership_rows} rows)"
        )
        if export_result.playlist_events_path is not None:
            print(f"playlist-events: {export_result.playlist_events_path}")
            print(f"playlist-stats: {export_result.playlist_stats_path}")
            print(f"track-popularity: {export_result.track_popularity_path}")
            print(f"song-graph: {export_result.song_graph_path}")
        return 0
    if args.command == "build-course-dataset":
        course_result = build_course_dataset(
            raw_root=args.raw_root,
            processed_root=args.processed_root,
            lyrics_top_n_tokens=args.lyrics_top_n_tokens,
        )
        print("built course datasets:")
        print(f"- audio-core: {course_result.audio_core_path}")
        print(f"- lyrics-core: {course_result.lyrics_core_path}")
        if course_result.playlist_events_path is None:
            print("- playlist-events: skipped (no playlist behavior source found)")
            print("- song-graph: skipped (no playlist behavior source found)")
        else:
            print(f"- playlist-events: {course_result.playlist_events_path}")
            print(f"- song-graph: {course_result.song_graph_path}")
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
