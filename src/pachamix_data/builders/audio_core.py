from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Iterable

import polars as pl


PREFERRED_TRACK_COLUMNS = (
    "track_id",
    "title",
    "genre_top",
    "artist_name",
)

TRACK_COLUMN_RENAMES = {
    "track__id": "track_id",
    "track__title": "title",
    "track__genre_top": "genre_top",
    "artist__name": "artist_name",
}


def _normalize_token(token: str) -> str:
    value = token.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def _flatten_headers(header_rows: list[list[str]]) -> list[str]:
    width = max(len(row) for row in header_rows)
    headers: list[str] = []
    for idx in range(width):
        pieces = []
        for row in header_rows:
            if idx < len(row):
                value = _normalize_token(row[idx])
                if value:
                    pieces.append(value)
        header = "__".join(pieces) or f"column_{idx}"
        headers.append(header)
    return headers


def _looks_like_data_row(row: list[str]) -> bool:
    if not row:
        return False
    first_value = row[0].strip()
    return first_value.isdigit()


def _read_multi_header_csv(path: Path) -> pl.DataFrame:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        headers: list[list[str]] = []
        records: list[list[str]] = []
        for row in reader:
            if not any(cell.strip() for cell in row):
                continue
            if _looks_like_data_row(row):
                records.append(row)
                break
            headers.append(row)
        records.extend(row for row in reader if any(cell.strip() for cell in row))
    if not headers:
        raise ValueError(f"expected at least one header row in {path}")
    columns = _flatten_headers(headers)
    padded_records = [
        row + [""] * (len(columns) - len(row))
        for row in records
    ]
    return pl.DataFrame(padded_records, schema=columns, orient="row")


def _find_track_id_column(columns: Iterable[str]) -> str | None:
    for column in columns:
        if "track" in column and "id" in column:
            return column
    return None


def build_audio_core(
    tracks_csv: str | Path,
    features_csv: str | Path,
    output_parquet: str | Path,
) -> pl.DataFrame:
    tracks_path = Path(tracks_csv)
    features_path = Path(features_csv)
    output_path = Path(output_parquet)

    tracks = _read_multi_header_csv(tracks_path)
    track_renames = {
        source: target
        for source, target in TRACK_COLUMN_RENAMES.items()
        if source in tracks.columns
    }
    if track_renames:
        tracks = tracks.rename(track_renames)
    if "track_id" not in tracks.columns:
        track_id_column = _find_track_id_column(tracks.columns)
        if track_id_column is None:
            raise ValueError("tracks input must include a track_id column")
        tracks = tracks.rename({track_id_column: "track_id"})

    selected_track_columns = [
        column for column in PREFERRED_TRACK_COLUMNS if column in tracks.columns
    ]
    tracks = tracks.select(selected_track_columns).with_columns(
        pl.col("track_id").cast(pl.Int64)
    )

    raw_features = _read_multi_header_csv(features_path)
    feature_track_id = _find_track_id_column(raw_features.columns)
    if feature_track_id is None:
        raise ValueError("features input must include a track_id column")

    feature_renames = {
        column: column.replace("__", "_")
        for column in raw_features.columns
        if column != feature_track_id
    }
    feature_renames[feature_track_id] = "track_id"
    features = raw_features.rename(feature_renames).with_columns(
        pl.col("track_id").cast(pl.Int64)
    )

    numeric_feature_columns = [
        column for column in features.columns if column != "track_id"
    ]
    if numeric_feature_columns:
        features = features.with_columns(
            [pl.col(column).cast(pl.Float64) for column in numeric_feature_columns]
        )

    frame = tracks.join(features, on="track_id", how="inner")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame.write_parquet(output_path)
    return frame
