from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import polars as pl
import pytest


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


def test_upc_datasets_can_render_bilingual_data_dictionary() -> None:
    import upc_datasets

    rendered = upc_datasets.show_data_dictionary(language="bilingual")

    assert "Dataset / Conjunto de datos: pachamix_audio_core" in rendered
    assert "Description / Descripcion:" in rendered
    assert "Structured audio-feature table" in rendered
    assert "Tabla estructurada de caracteristicas de audio" in rendered


def test_upc_datasets_can_render_spanish_dataset_definition() -> None:
    import upc_datasets

    rendered = upc_datasets.show_dataset_definition(
        "pachamix_lyrics_long",
        language="es",
    )

    assert "Conjunto de datos: pachamix_lyrics_long" in rendered
    assert "Descripcion:" in rendered
    assert "Conteos de tokens liricos en formato largo" in rendered
    assert "Columnas:" in rendered


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


def test_upc_datasets_cli_can_show_bilingual_dictionary_text() -> None:
    result = run_cli(
        "show-data-dictionary",
        "--format",
        "text",
        "--language",
        "bilingual",
    )

    assert result.returncode == 0, result.stderr
    assert "Dataset / Conjunto de datos: pachamix_audio_core" in result.stdout
    assert "Columns / Columnas:" in result.stdout


def test_upc_datasets_load_dataset_reads_from_project_root(tmp_path: Path) -> None:
    import upc_datasets

    output_path = tmp_path / "data" / "processed" / "pachamix_audio_core.parquet"
    output_path.parent.mkdir(parents=True)
    expected = pl.DataFrame(
        {
            "track_id": [101, 202],
            "title": ["River Echo", "Andes Loop"],
            "artist_name": ["Mathias", "Yunguri"],
        }
    )
    expected.write_parquet(output_path)

    loaded = upc_datasets.load_dataset("pachamix_audio_core", root=tmp_path)

    assert loaded.shape == (2, 3)
    assert loaded.to_dict(as_series=False) == expected.to_dict(as_series=False)


def test_upc_datasets_load_dataset_uses_env_root_and_can_return_lazy_frame(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    import upc_datasets

    processed_root = tmp_path / "course_outputs"
    output_path = processed_root / "pachamix_lyrics_long.parquet"
    output_path.parent.mkdir(parents=True)
    pl.DataFrame(
        {
            "msd_track_id": ["TR1", "TR1"],
            "token": ["llama", "playlist"],
            "count": [2, 1],
        }
    ).write_parquet(output_path)
    monkeypatch.setenv("UPC_DATASETS_ROOT", str(processed_root))

    loaded = upc_datasets.load_dataset("pachamix_lyrics_long", lazy=True)

    assert isinstance(loaded, pl.LazyFrame)
    assert loaded.collect().shape == (2, 3)


def test_upc_datasets_load_dataset_raises_helpful_error_when_dataset_file_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import upc_datasets

    monkeypatch.delenv("UPC_DATASETS_ROOT", raising=False)

    with pytest.raises(FileNotFoundError) as excinfo:
        upc_datasets.load_dataset("pachamix_playlist_events", root=ROOT / "tests" / "fixtures")

    assert "pachamix_playlist_events" in str(excinfo.value)
    assert "UPC_DATASETS_ROOT" in str(excinfo.value)


def test_upc_datasets_download_dataset_fetches_to_cache_dir(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    import upc_datasets

    asset_dir = tmp_path / "assets"
    asset_dir.mkdir()
    source_path = asset_dir / "pachamix_audio_core.parquet"
    expected = pl.DataFrame({"track_id": [1], "title": ["PachaMix"]})
    expected.write_parquet(source_path)

    cache_dir = tmp_path / "cache"
    monkeypatch.setenv("UPC_DATASETS_BASE_URL", source_path.parent.as_uri())

    downloaded_path = upc_datasets.download_dataset(
        "pachamix_audio_core",
        cache_dir=cache_dir,
    )

    assert downloaded_path == cache_dir / "pachamix_audio_core.parquet"
    loaded = pl.read_parquet(downloaded_path)
    assert loaded.to_dict(as_series=False) == expected.to_dict(as_series=False)


def test_upc_datasets_load_dataset_can_download_when_missing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    import upc_datasets

    asset_dir = tmp_path / "assets"
    asset_dir.mkdir()
    source_path = asset_dir / "playlist_events.parquet"
    expected = pl.DataFrame(
        {
            "playlist_id": [99],
            "track_uri": ["spotify:track:test"],
            "position": [0],
        }
    )
    expected.write_parquet(source_path)

    cache_dir = tmp_path / "cache"
    monkeypatch.setenv("UPC_DATASETS_BASE_URL", source_path.parent.as_uri())
    monkeypatch.setenv("UPC_DATASETS_CACHE_DIR", str(cache_dir))
    monkeypatch.delenv("UPC_DATASETS_ROOT", raising=False)

    loaded = upc_datasets.load_dataset("pachamix_playlist_events", download=True)

    assert loaded.shape == (1, 3)
    assert loaded.to_dict(as_series=False) == expected.to_dict(as_series=False)


def test_upc_datasets_cli_can_download_dataset(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    asset_dir = tmp_path / "assets"
    asset_dir.mkdir()
    source_path = asset_dir / "pachamix_audio_core.parquet"
    pl.DataFrame({"track_id": [7], "title": ["Andes"]}).write_parquet(source_path)

    cache_dir = tmp_path / "cache"
    env = {
        "PYTHONPATH": str(SRC),
        "UPC_DATASETS_BASE_URL": source_path.parent.as_uri(),
        "UPC_DATASETS_CACHE_DIR": str(cache_dir),
    }
    result = subprocess.run(
        [sys.executable, "-m", "upc_datasets.cli", "download", "pachamix_audio_core"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "pachamix_audio_core.parquet" in result.stdout
    assert (cache_dir / "pachamix_audio_core.parquet").exists()
