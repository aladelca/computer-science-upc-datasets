from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import polars as pl


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    return subprocess.run(
        [sys.executable, "-m", "pachamix_data.cli", *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_end_to_end_generation_via_cli(tmp_path: Path) -> None:
    audio_out = tmp_path / "audio_core.parquet"
    lyrics_out = tmp_path / "lyrics_core.parquet"
    playlist_dir = tmp_path / "playlist_outputs"
    graph_out = tmp_path / "song_graph.parquet"

    audio_result = run_cli(
        "build-audio-core",
        "--tracks-csv",
        str(FIXTURES / "fma" / "tracks.csv"),
        "--features-csv",
        str(FIXTURES / "fma" / "features.csv"),
        "--output-parquet",
        str(audio_out),
    )
    assert audio_result.returncode == 0, audio_result.stderr

    lyrics_result = run_cli(
        "build-lyrics-core",
        "--lyrics-txt",
        str(FIXTURES / "lyrics" / "musixmatch_sample.txt"),
        "--output-parquet",
        str(lyrics_out),
    )
    assert lyrics_result.returncode == 0, lyrics_result.stderr

    playlist_result = run_cli(
        "build-playlist-events",
        "--mpd-json",
        str(FIXTURES / "mpd" / "sample_playlists.json"),
        "--output-dir",
        str(playlist_dir),
    )
    assert playlist_result.returncode == 0, playlist_result.stderr

    graph_result = run_cli(
        "build-song-graph",
        "--playlist-events-parquet",
        str(playlist_dir / "playlist_events.parquet"),
        "--output-parquet",
        str(graph_out),
    )
    assert graph_result.returncode == 0, graph_result.stderr

    assert pl.read_parquet(audio_out).height == 2
    assert pl.read_parquet(lyrics_out).height == 8
    assert pl.read_parquet(playlist_dir / "playlist_events.parquet").height == 5
    assert pl.read_parquet(graph_out).height == 3
