from __future__ import annotations

import os
from pathlib import Path

import polars as pl

from upc_datasets.catalog import get_dataset_definition


DATA_ROOT_ENV_VAR = "UPC_DATASETS_ROOT"


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


def load_dataset(
    name: str,
    *,
    root: str | Path | None = None,
    lazy: bool = False,
) -> pl.DataFrame | pl.LazyFrame:
    dataset_path = _resolve_dataset_path(name, root=root)

    if lazy:
        return pl.scan_parquet(dataset_path)

    return pl.read_parquet(dataset_path)
