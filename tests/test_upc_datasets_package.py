from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = {"PYTHONPATH": str(SRC)}
    return subprocess.run(
        [sys.executable, "-m", "upc_datasets.cli", *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_upc_datasets_package_can_be_imported() -> None:
    import upc_datasets

    assert upc_datasets.__version__
    assert "pachamix_audio_core" in upc_datasets.list_datasets()


def test_upc_datasets_dictionary_api_exposes_lyrics_dataset() -> None:
    import upc_datasets

    dataset = upc_datasets.get_dataset_definition("pachamix_lyrics_long")

    assert dataset["grain"] == "one row per (msd_track_id, token)"
    column_names = [column["name"] for column in dataset["columns"]]
    assert "title" in column_names
    assert "token" in column_names
    assert "count" in column_names


def test_upc_datasets_cli_can_show_dataset_dictionary_as_json() -> None:
    result = run_cli("show-dataset", "pachamix_lyrics_long", "--format", "json")

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["name"] == "pachamix_lyrics_long"
    assert payload["grain"] == "one row per (msd_track_id, token)"
    assert any(column["name"] == "artist_name" for column in payload["columns"])


def test_upc_datasets_cli_lists_datasets() -> None:
    result = run_cli("list-datasets")

    assert result.returncode == 0, result.stderr
    assert "pachamix_audio_core" in result.stdout
    assert "pachamix_lyrics_long" in result.stdout
