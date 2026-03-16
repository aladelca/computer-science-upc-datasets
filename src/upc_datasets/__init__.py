"""Student-facing public package for UPC course datasets."""

from pachamix_data import __version__
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
from upc_datasets.loader import load_dataset

__all__ = [
    "__version__",
    "build_audio_core",
    "build_lyrics_core",
    "build_playlist_events",
    "build_song_graph",
    "build_course_dataset",
    "get_data_dictionary",
    "get_dataset_definition",
    "list_datasets",
    "load_dataset",
]
