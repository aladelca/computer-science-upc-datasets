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
    get_dataset_asset_name,
    get_dataset_asset_names,
    get_dataset_definition,
    list_datasets,
    list_kaggle_datasets,
    list_public_release_datasets,
)
from upc_datasets.loader import download_dataset, load_dataset
from upc_datasets.presentation import show_data_dictionary, show_dataset_definition
from upc_datasets.release import stage_release_assets

__all__ = [
    "__version__",
    "build_audio_core",
    "build_lyrics_core",
    "build_playlist_events",
    "build_song_graph",
    "build_course_dataset",
    "download_dataset",
    "get_data_dictionary",
    "get_dataset_asset_name",
    "get_dataset_asset_names",
    "get_dataset_definition",
    "list_datasets",
    "list_kaggle_datasets",
    "list_public_release_datasets",
    "load_dataset",
    "show_data_dictionary",
    "show_dataset_definition",
    "stage_release_assets",
]
