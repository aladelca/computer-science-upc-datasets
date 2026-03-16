from __future__ import annotations

import argparse
import json
from typing import Sequence

from pachamix_data.builders import (
    build_audio_core,
    build_lyrics_core,
    build_playlist_events,
    build_song_graph,
)
from pachamix_data.pipeline import build_course_dataset
from upc_datasets.catalog import (
    get_data_dictionary,
    get_dataset_definition,
    list_datasets,
)
from upc_datasets.loader import download_dataset
from upc_datasets.presentation import show_data_dictionary, show_dataset_definition


SUPPORTED_BUILDERS = (
    "audio-core",
    "lyrics-core",
    "playlist-events",
    "song-graph",
)
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="upc-datasets",
        description="Student-facing dataset toolkit for the UPC big data course.",
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list-builders", help="List supported dataset builders.")
    subparsers.add_parser("list-datasets", help="List datasets in the packaged data dictionary.")

    download_parser = subparsers.add_parser(
        "download",
        help="Download a packaged dataset parquet asset to a local cache or root directory.",
    )
    download_parser.add_argument("dataset_name")
    download_parser.add_argument("--root")
    download_parser.add_argument("--cache-dir")
    download_parser.add_argument("--force", action="store_true")

    show_dataset_parser = subparsers.add_parser(
        "show-dataset",
        help="Show the data dictionary entry for a dataset.",
    )
    show_dataset_parser.add_argument("dataset_name")
    show_dataset_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
    )
    show_dataset_parser.add_argument(
        "--language",
        choices=("en", "es", "bilingual"),
        default="bilingual",
    )

    show_dictionary_parser = subparsers.add_parser(
        "show-data-dictionary",
        help="Show the full packaged data dictionary.",
    )
    show_dictionary_parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
    )
    show_dictionary_parser.add_argument(
        "--language",
        choices=("en", "es", "bilingual"),
        default="bilingual",
    )

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
        help="Build playlist event and summary parquet outputs from MPD JSON or Playlist2vec exports.",
    )
    playlist_parser.add_argument("--mpd-json", required=True)
    playlist_parser.add_argument("--output-dir", required=True)

    graph_parser = subparsers.add_parser(
        "build-song-graph",
        help="Build weighted song-song co-occurrence edges from playlist events.",
    )
    graph_parser.add_argument("--playlist-events-parquet", required=True)
    graph_parser.add_argument("--output-parquet", required=True)

    course_parser = subparsers.add_parser(
        "build-course-dataset",
        help="Build all supported course datasets from a raw-root layout.",
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
    if args.command == "list-datasets":
        print("\n".join(list_datasets()))
        return 0
    if args.command == "download":
        download_path = download_dataset(
            args.dataset_name,
            root=args.root,
            cache_dir=args.cache_dir,
            force=args.force,
        )
        print(f"downloaded {args.dataset_name} to {download_path}")
        return 0
    if args.command == "show-dataset":
        dataset = get_dataset_definition(args.dataset_name)
        if args.format == "json":
            print(json.dumps(dataset, indent=2))
        else:
            print(show_dataset_definition(args.dataset_name, language=args.language))
        return 0
    if args.command == "show-data-dictionary":
        if args.format == "json":
            print(json.dumps(get_data_dictionary(), indent=2))
        else:
            print(show_data_dictionary(language=args.language))
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
        result = build_playlist_events(
            mpd_json=args.mpd_json,
            output_dir=args.output_dir,
        )
        print(f"wrote {result.events.height} playlist events to {result.events_path}")
        return 0
    if args.command == "build-song-graph":
        result = build_song_graph(
            playlist_events_parquet=args.playlist_events_parquet,
            output_parquet=args.output_parquet,
        )
        print(f"wrote {result.edges.height} graph edges to {result.edges_path}")
        return 0
    if args.command == "build-course-dataset":
        result = build_course_dataset(
            raw_root=args.raw_root,
            processed_root=args.processed_root,
            lyrics_top_n_tokens=args.lyrics_top_n_tokens,
        )
        print("built course datasets:")
        print(f"- audio-core: {result.audio_core_path}")
        print(f"- lyrics-core: {result.lyrics_core_path}")
        if result.playlist_events_path is None:
            print("- playlist-events: skipped (no playlist behavior source found)")
            print("- song-graph: skipped (no playlist behavior source found)")
        else:
            print(f"- playlist-events: {result.playlist_events_path}")
            print(f"- song-graph: {result.song_graph_path}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
