from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from upc_datasets.catalog import get_dataset_asset_names, list_public_release_datasets
from upc_datasets.loader import _resolve_dataset_path


@dataclass(frozen=True)
class ReleaseAsset:
    dataset_name: str
    source_path: Path
    asset_name: str
    target_path: Path
    is_legacy_alias: bool = False


def stage_release_assets(
    output_dir: str | Path,
    *,
    root: str | Path | None = None,
    dataset_names: Sequence[str] | None = None,
    overwrite: bool = False,
    include_legacy_aliases: bool = True,
) -> list[ReleaseAsset]:
    target_dir = Path(output_dir).expanduser()
    target_dir.mkdir(parents=True, exist_ok=True)

    names = list(dataset_names) if dataset_names is not None else list_public_release_datasets()
    staged_assets: list[ReleaseAsset] = []

    for dataset_name in names:
        source_path = _resolve_dataset_path(dataset_name, root=root)
        asset_names = get_dataset_asset_names(dataset_name)
        if not include_legacy_aliases:
            asset_names = asset_names[:1]

        for asset_index, asset_name in enumerate(asset_names):
            target_path = target_dir / asset_name

            if target_path.exists() and not overwrite:
                raise FileExistsError(
                    f"release asset already exists: {target_path}. "
                    "Pass overwrite=True to replace it."
                )

            shutil.copy2(source_path, target_path)
            staged_assets.append(
                ReleaseAsset(
                    dataset_name=dataset_name,
                    source_path=source_path,
                    asset_name=asset_name,
                    target_path=target_path,
                    is_legacy_alias=asset_index > 0,
                )
            )

    return staged_assets
