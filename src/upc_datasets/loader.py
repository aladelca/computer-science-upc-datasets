from __future__ import annotations

import os
import shutil
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import urlopen

import polars as pl

from upc_datasets.catalog import (
    get_dataset_asset_name,
    get_dataset_asset_names,
    get_dataset_definition,
)

DATA_ROOT_ENV_VAR = "UPC_DATASETS_ROOT"
DATASETS_BASE_URL_ENV_VAR = "UPC_DATASETS_BASE_URL"
DATASETS_CACHE_DIR_ENV_VAR = "UPC_DATASETS_CACHE_DIR"
DEFAULT_RELEASE_BASE_URL = "https://github.com/aladelca/computer-science-upc-datasets/releases/latest/download/"


def _dataset_url_env_var(name: str) -> str:
    return f"UPC_DATASETS_{name.upper()}_URL"


def _dataset_asset_name(name: str) -> str:
    return get_dataset_asset_name(name)


def _resolve_download_urls(name: str) -> list[str]:
    env_url = os.environ.get(_dataset_url_env_var(name))
    if env_url:
        return [env_url]

    base_url = os.environ.get(DATASETS_BASE_URL_ENV_VAR)
    if base_url:
        return [
            urljoin(f"{base_url.rstrip('/')}/", asset_name)
            for asset_name in get_dataset_asset_names(name)
        ]

    dataset = get_dataset_definition(name)
    distribution = dataset.get("distribution", {})
    if not bool(distribution.get("public_release")):
        if distribution.get("channel") == "kaggle":
            raise RuntimeError(
                f"dataset '{name}' is not distributed via the package release assets. "
                "Publish or fetch it from Kaggle, then point the package to a local copy "
                f"with {DATA_ROOT_ENV_VAR} or to an alternate mirror with "
                f"{DATASETS_BASE_URL_ENV_VAR} or {_dataset_url_env_var(name)}."
            )
        raise RuntimeError(
            f"dataset '{name}' is not distributed via the default package release assets."
        )

    base_url = DEFAULT_RELEASE_BASE_URL
    return [
        urljoin(f"{base_url.rstrip('/')}/", asset_name)
        for asset_name in get_dataset_asset_names(name)
    ]


def _default_cache_dir() -> Path:
    return Path.home() / ".cache" / "upc_datasets"


def _target_path_from_root(name: str, root: Path) -> Path:
    relative_path = Path(str(get_dataset_definition(name)["path"]))
    expanded_root = root.expanduser()
    relative_parent_parts = relative_path.parent.parts

    if (
        tuple(expanded_root.parts[-len(relative_parent_parts) :])
        == relative_parent_parts
    ):
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


def _candidate_dataset_paths(
    name: str,
    root: str | Path | None = None,
    *,
    include_fallback_paths: bool = True,
) -> list[Path]:
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
        return candidate_paths

    env_root = os.environ.get(DATA_ROOT_ENV_VAR)
    if env_root:
        add_candidates(Path(env_root))
        if not include_fallback_paths:
            return candidate_paths

    if not include_fallback_paths:
        return candidate_paths

    package_root = Path(__file__).resolve().parents[2]
    add_candidates(package_root)
    add_candidates(Path.cwd())
    return candidate_paths


def _resolve_dataset_path(
    name: str,
    root: str | Path | None = None,
    *,
    include_fallback_paths: bool = True,
) -> Path:
    candidate_paths = _candidate_dataset_paths(
        name,
        root=root,
        include_fallback_paths=include_fallback_paths,
    )

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

    last_error: HTTPError | URLError | None = None
    attempted_urls = _resolve_download_urls(name)

    for download_url in attempted_urls:
        temp_path = target_path.with_name(f".{target_path.name}.tmp")
        try:
            with urlopen(download_url) as response, temp_path.open("wb") as target_file:
                shutil.copyfileobj(response, target_file)
            temp_path.replace(target_path)
            return target_path
        except (HTTPError, URLError) as exc:
            temp_path.unlink(missing_ok=True)
            last_error = exc

    attempted_urls_rendered = "\n".join(f"- {url}" for url in attempted_urls)
    raise RuntimeError(
        f"failed to download dataset '{name}'. Tried release asset URLs:\n"
        f"{attempted_urls_rendered}\n"
        f"Set {DATASETS_BASE_URL_ENV_VAR} or {_dataset_url_env_var(name)} "
        "to a valid release-asset URL."
    ) from last_error


def load_dataset(
    name: str,
    *,
    root: str | Path | None = None,
    lazy: bool = False,
    download: bool = False,
    cache_dir: str | Path | None = None,
    force_download: bool = False,
) -> pl.DataFrame | pl.LazyFrame:
    include_fallback_paths = root is None and not download
    try:
        dataset_path = _resolve_dataset_path(
            name,
            root=root,
            include_fallback_paths=include_fallback_paths,
        )
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
