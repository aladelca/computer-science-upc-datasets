from __future__ import annotations

import os
import shutil
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import urlopen

import polars as pl

from upc_datasets.catalog import get_dataset_definition


DATA_ROOT_ENV_VAR = "UPC_DATASETS_ROOT"
DATASETS_BASE_URL_ENV_VAR = "UPC_DATASETS_BASE_URL"
DATASETS_CACHE_DIR_ENV_VAR = "UPC_DATASETS_CACHE_DIR"
DEFAULT_RELEASE_BASE_URL = (
    "https://github.com/aladelca/computer-science-upc-datasets/releases/latest/download/"
)


def _dataset_url_env_var(name: str) -> str:
    return f"UPC_DATASETS_{name.upper()}_URL"


def _dataset_asset_name(name: str) -> str:
    dataset = get_dataset_definition(name)
    return Path(str(dataset["path"])).name


def _resolve_download_url(name: str) -> str:
    env_url = os.environ.get(_dataset_url_env_var(name))
    if env_url:
        return env_url

    base_url = os.environ.get(DATASETS_BASE_URL_ENV_VAR, DEFAULT_RELEASE_BASE_URL)
    return urljoin(f"{base_url.rstrip('/')}/", _dataset_asset_name(name))


def _default_cache_dir() -> Path:
    return Path.home() / ".cache" / "upc_datasets"


def _target_path_from_root(name: str, root: Path) -> Path:
    relative_path = Path(str(get_dataset_definition(name)["path"]))
    expanded_root = root.expanduser()
    relative_parent_parts = relative_path.parent.parts

    if tuple(expanded_root.parts[-len(relative_parent_parts):]) == relative_parent_parts:
        return expanded_root / relative_path.name

    return expanded_root / relative_path


def _download_target_path(
    name: str,
    *,
    root: str | Path | None = None,
    cache_dir: str | Path | None = None,
) -> Path:
    if root is not None:
        return _target_path_from_root(name, Path(root))

    env_root = os.environ.get(DATA_ROOT_ENV_VAR)
    if env_root:
        return _target_path_from_root(name, Path(env_root))

    cache_base = Path(
        cache_dir
        if cache_dir is not None
        else os.environ.get(DATASETS_CACHE_DIR_ENV_VAR, _default_cache_dir())
    ).expanduser()
    return cache_base / _dataset_asset_name(name)


def _candidate_dataset_paths(name: str, root: str | Path | None = None) -> list[Path]:
    dataset = get_dataset_definition(name)
    relative_path = Path(str(dataset["path"]))
    candidate_paths: list[Path] = []
    seen: set[Path] = set()

    def add_candidates(base: Path) -> None:
        expanded_base = base.expanduser()
        for candidate in (
            expanded_base / relative_path,
            expanded_base / relative_path.name,
        ):
            resolved_candidate = candidate.resolve(strict=False)
            if resolved_candidate not in seen:
                seen.add(resolved_candidate)
                candidate_paths.append(resolved_candidate)

    if root is not None:
        add_candidates(Path(root))

    env_root = os.environ.get(DATA_ROOT_ENV_VAR)
    if env_root:
        add_candidates(Path(env_root))

    package_root = Path(__file__).resolve().parents[2]
    add_candidates(package_root)
    add_candidates(Path.cwd())
    return candidate_paths


def _resolve_dataset_path(name: str, root: str | Path | None = None) -> Path:
    candidate_paths = _candidate_dataset_paths(name, root=root)

    for candidate_path in candidate_paths:
        if candidate_path.exists():
            return candidate_path

    looked_in = "\n".join(f"- {candidate}" for candidate in candidate_paths)
    raise FileNotFoundError(
        f"dataset '{name}' was not found.\n"
        f"Looked for parquet files in:\n{looked_in}\n"
        f"Pass root='/path/to/project-or-processed-dir' or set {DATA_ROOT_ENV_VAR}."
    )


def download_dataset(
    name: str,
    *,
    root: str | Path | None = None,
    cache_dir: str | Path | None = None,
    force: bool = False,
) -> Path:
    target_path = _download_target_path(name, root=root, cache_dir=cache_dir)
    target_path.parent.mkdir(parents=True, exist_ok=True)

    if target_path.exists() and not force:
        return target_path

    download_url = _resolve_download_url(name)
    try:
        with urlopen(download_url) as response, target_path.open("wb") as target_file:
            shutil.copyfileobj(response, target_file)
    except (HTTPError, URLError) as exc:
        raise RuntimeError(
            f"failed to download dataset '{name}' from {download_url}. "
            f"Set {DATASETS_BASE_URL_ENV_VAR} or {_dataset_url_env_var(name)} "
            "to a valid release-asset URL."
        ) from exc

    return target_path


def load_dataset(
    name: str,
    *,
    root: str | Path | None = None,
    lazy: bool = False,
    download: bool = False,
    cache_dir: str | Path | None = None,
    force_download: bool = False,
) -> pl.DataFrame | pl.LazyFrame:
    try:
        dataset_path = _resolve_dataset_path(name, root=root)
    except FileNotFoundError:
        if not download:
            raise
        dataset_path = download_dataset(
            name,
            root=root,
            cache_dir=cache_dir,
            force=force_download,
        )

    if lazy:
        return pl.scan_parquet(dataset_path)

    return pl.read_parquet(dataset_path)
