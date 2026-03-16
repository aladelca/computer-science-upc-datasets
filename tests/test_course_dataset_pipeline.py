from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import polars as pl


ROOT = Path(__file__).resolve().parents[1]
RAW_FIXTURES = ROOT / "tests" / "fixtures" / "course_raw"


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


def test_build_course_dataset_runs_all_builders_from_one_command(tmp_path: Path) -> None:
    processed_root = tmp_path / "processed"

    result = run_cli(
        "build-course-dataset",
        "--raw-root",
        str(RAW_FIXTURES),
        "--processed-root",
        str(processed_root),
    )

    assert result.returncode == 0, result.stderr
    assert (processed_root / "pachamix_audio_core.parquet").exists()
    assert (processed_root / "pachamix_lyrics_long.parquet").exists()
    assert (processed_root / "pachamix_playlists" / "playlist_events.parquet").exists()
    assert (processed_root / "pachamix_song_graph_edges.parquet").exists()

    assert pl.read_parquet(processed_root / "pachamix_audio_core.parquet").height == 2
    assert pl.read_parquet(processed_root / "pachamix_lyrics_long.parquet").height == 8
    assert (
        pl.read_parquet(processed_root / "pachamix_playlists" / "playlist_events.parquet").height
        == 4
    )
    assert pl.read_parquet(processed_root / "pachamix_song_graph_edges.parquet").height == 2
