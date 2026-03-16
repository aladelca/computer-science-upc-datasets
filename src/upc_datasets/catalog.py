from __future__ import annotations

import copy
from typing import Any


DATASET_CATALOG: dict[str, dict[str, Any]] = {
    "pachamix_audio_core": {
        "name": "pachamix_audio_core",
        "path": "data/processed/pachamix_audio_core.parquet",
        "status": "generated",
        "source": ["FMA"],
        "grain": "one row per FMA track",
        "primary_key": ["track_id"],
        "description": "Structured audio-feature table with FMA metadata and precomputed descriptors.",
        "columns": [
            {"name": "track_id", "dtype": "Int64", "description": "FMA track identifier."},
            {"name": "title", "dtype": "String", "description": "Track title from FMA metadata."},
            {"name": "genre_top", "dtype": "String", "description": "Top-level genre label from FMA metadata."},
            {"name": "artist_name", "dtype": "String", "description": "Artist name from FMA metadata."},
        ],
        "feature_families": [
            {
                "family": "chroma_cens",
                "column_count": 84,
                "components": 12,
                "stats": ["kurtosis", "max", "mean", "median", "min", "skew", "std"],
                "description": "Chroma features from the CENS representation.",
            },
            {
                "family": "chroma_cqt",
                "column_count": 84,
                "components": 12,
                "stats": ["kurtosis", "max", "mean", "median", "min", "skew", "std"],
                "description": "Chroma features from the constant-Q transform.",
            },
            {
                "family": "chroma_stft",
                "column_count": 84,
                "components": 12,
                "stats": ["kurtosis", "max", "mean", "median", "min", "skew", "std"],
                "description": "Chroma features from the STFT representation.",
            },
            {
                "family": "mfcc",
                "column_count": 140,
                "components": 20,
                "stats": ["kurtosis", "max", "mean", "median", "min", "skew", "std"],
                "description": "Mel-frequency cepstral coefficients.",
            },
            {
                "family": "rmse",
                "column_count": 7,
                "components": 1,
                "stats": ["kurtosis", "max", "mean", "median", "min", "skew", "std"],
                "description": "Root mean square energy summary.",
            },
            {
                "family": "spectral_bandwidth",
                "column_count": 7,
                "components": 1,
                "stats": ["kurtosis", "max", "mean", "median", "min", "skew", "std"],
                "description": "Spectral bandwidth summary.",
            },
            {
                "family": "spectral_centroid",
                "column_count": 7,
                "components": 1,
                "stats": ["kurtosis", "max", "mean", "median", "min", "skew", "std"],
                "description": "Spectral centroid summary.",
            },
            {
                "family": "spectral_contrast",
                "column_count": 49,
                "components": 7,
                "stats": ["kurtosis", "max", "mean", "median", "min", "skew", "std"],
                "description": "Spectral contrast band summaries.",
            },
            {
                "family": "spectral_rolloff",
                "column_count": 7,
                "components": 1,
                "stats": ["kurtosis", "max", "mean", "median", "min", "skew", "std"],
                "description": "Spectral rolloff summary.",
            },
            {
                "family": "tonnetz",
                "column_count": 42,
                "components": 6,
                "stats": ["kurtosis", "max", "mean", "median", "min", "skew", "std"],
                "description": "Tonal centroid features.",
            },
            {
                "family": "zcr",
                "column_count": 7,
                "components": 1,
                "stats": ["kurtosis", "max", "mean", "median", "min", "skew", "std"],
                "description": "Zero-crossing-rate summary.",
            },
        ],
    },
    "pachamix_lyrics_long": {
        "name": "pachamix_lyrics_long",
        "path": "data/processed/pachamix_lyrics_long.parquet",
        "status": "generated",
        "source": ["musiXmatch/MSD", "MSD track_metadata.db (optional enrichment)"],
        "grain": "one row per (msd_track_id, token)",
        "primary_key": ["msd_track_id", "token"],
        "description": "Long-form lyric token counts enriched with MSD song metadata when track_metadata.db is available.",
        "columns": [
            {"name": "msd_track_id", "dtype": "String", "description": "MSD track identifier; joins to songs.track_id."},
            {"name": "title", "dtype": "String", "description": "Track title from MSD metadata."},
            {"name": "song_id", "dtype": "String", "description": "MSD / Echo Nest song identifier."},
            {"name": "release", "dtype": "String", "description": "Release or album name from MSD metadata."},
            {"name": "artist_id", "dtype": "String", "description": "MSD / Echo Nest artist identifier."},
            {"name": "artist_mbid", "dtype": "String", "description": "MusicBrainz artist identifier."},
            {"name": "artist_name", "dtype": "String", "description": "Artist name from MSD metadata."},
            {"name": "duration", "dtype": "Float64", "description": "Track duration in seconds."},
            {"name": "artist_familiarity", "dtype": "Float64", "description": "Echo Nest artist familiarity score."},
            {"name": "artist_hotttnesss", "dtype": "Float64", "description": "Echo Nest artist hotttnesss score."},
            {"name": "year", "dtype": "Int64", "description": "Release year; often 0 when unavailable."},
            {"name": "track_7digitalid", "dtype": "Int64", "description": "7digital track identifier from MSD metadata."},
            {"name": "shs_perf", "dtype": "Int64", "description": "SecondHandSongs performance identifier or sentinel value."},
            {"name": "shs_work", "dtype": "Int64", "description": "SecondHandSongs work identifier or sentinel value."},
            {"name": "token", "dtype": "String", "description": "Lyric token from the official musiXmatch/MSD vocabulary."},
            {"name": "count", "dtype": "Int64", "description": "Token frequency for the track."},
        ],
    },
    "pachamix_playlist_events": {
        "name": "pachamix_playlist_events",
        "path": "data/processed/pachamix_playlists/playlist_events.parquet",
        "status": "optional",
        "source": ["Playlist2vec or MPD"],
        "grain": "one row per (playlist_id, track_uri, position)",
        "primary_key": ["playlist_id", "track_uri", "position"],
        "description": "Playlist membership table used for collaborative filtering and graph construction.",
        "columns": [
            {"name": "playlist_id", "dtype": "Int64", "description": "Playlist identifier."},
            {"name": "playlist_name", "dtype": "String", "description": "Playlist name."},
            {"name": "track_uri", "dtype": "String", "description": "Canonical track identifier from the playlist source."},
            {"name": "track_name", "dtype": "String", "description": "Track title from the playlist source."},
            {"name": "artist_name", "dtype": "String", "description": "Artist name from the playlist source."},
            {"name": "album_name", "dtype": "String", "description": "Album name from the playlist source."},
            {"name": "position", "dtype": "Int64", "description": "Track order in the playlist."},
        ],
    },
    "pachamix_playlist_stats": {
        "name": "pachamix_playlist_stats",
        "path": "data/processed/pachamix_playlists/playlist_stats.parquet",
        "status": "optional",
        "source": ["derived from playlist events"],
        "grain": "one row per playlist",
        "primary_key": ["playlist_id"],
        "description": "Playlist-level summary table.",
        "columns": [
            {"name": "playlist_id", "dtype": "Int64", "description": "Playlist identifier."},
            {"name": "playlist_name", "dtype": "String", "description": "Playlist name."},
            {"name": "track_count", "dtype": "Int64", "description": "Number of tracks in the playlist."},
        ],
    },
    "pachamix_track_popularity": {
        "name": "pachamix_track_popularity",
        "path": "data/processed/pachamix_playlists/track_popularity.parquet",
        "status": "optional",
        "source": ["derived from playlist events"],
        "grain": "one row per track_uri",
        "primary_key": ["track_uri"],
        "description": "Track popularity summary based on distinct playlist membership counts.",
        "columns": [
            {"name": "track_uri", "dtype": "String", "description": "Track identifier from the playlist source."},
            {"name": "playlist_count", "dtype": "Int64", "description": "Number of distinct playlists containing the track."},
        ],
    },
    "pachamix_song_graph_edges": {
        "name": "pachamix_song_graph_edges",
        "path": "data/processed/pachamix_song_graph_edges.parquet",
        "status": "optional",
        "source": ["derived from playlist events"],
        "grain": "one row per undirected song pair",
        "primary_key": ["src_track_uri", "dst_track_uri"],
        "description": "Weighted song co-occurrence edges for graph analytics and PageRank.",
        "columns": [
            {"name": "src_track_uri", "dtype": "String", "description": "First song in the co-occurrence pair."},
            {"name": "dst_track_uri", "dtype": "String", "description": "Second song in the co-occurrence pair."},
            {"name": "weight", "dtype": "Int64", "description": "Number of playlists where the pair co-occurs."},
        ],
    },
}


def list_datasets() -> list[str]:
    return sorted(DATASET_CATALOG)


def get_dataset_definition(name: str) -> dict[str, Any]:
    try:
        return copy.deepcopy(DATASET_CATALOG[name])
    except KeyError as exc:
        raise KeyError(f"unknown dataset: {name}") from exc


def get_data_dictionary() -> dict[str, dict[str, Any]]:
    return {name: get_dataset_definition(name) for name in list_datasets()}
