from __future__ import annotations

import sqlite3
from pathlib import Path

import polars as pl


def _iter_lyrics_files(path: Path) -> list[Path]:
    if path.is_dir():
        return sorted(file for file in path.rglob("*.txt") if file.is_file())
    return [path]


def _parse_simple_line(track_id: str, parts: list[str]) -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for pair in parts[1:]:
        if ":" not in pair:
            raise ValueError("lyrics rows must use token:count pairs")
        token, count_text = pair.split(":", 1)
        rows.append(
            {
                "msd_track_id": track_id,
                "token": token.strip(),
                "count": int(count_text),
            }
        )
    return rows


def _parse_official_lines(lines: list[str]) -> list[dict[str, str | int]]:
    vocabulary: list[str] | None = None
    rows: list[dict[str, str | int]] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("%"):
            vocabulary = [token.strip() for token in line[1:].split(",") if token.strip()]
            continue
        parts = [part.strip() for part in line.split(",") if part.strip()]
        if not parts:
            continue
        track_id = parts[0]
        if vocabulary is None:
            rows.extend(_parse_simple_line(track_id, parts))
            continue
        for pair in parts[2:]:
            if ":" not in pair:
                raise ValueError("lyrics rows must use token:count pairs")
            index_text, count_text = pair.split(":", 1)
            token_index = int(index_text) - 1
            if token_index < 0 or token_index >= len(vocabulary):
                raise ValueError("lyrics token index is out of vocabulary bounds")
            rows.append(
                {
                    "msd_track_id": track_id,
                    "token": vocabulary[token_index],
                    "count": int(count_text),
                }
            )
    return rows


def _parse_lyrics_rows(lyrics_txt: Path) -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for file_path in _iter_lyrics_files(lyrics_txt):
        lines = file_path.read_text(encoding="utf-8").splitlines()
        rows.extend(_parse_official_lines(lines))
    return rows


def _read_msd_metadata(metadata_db: Path) -> pl.DataFrame:
    connection = sqlite3.connect(metadata_db)
    try:
        cursor = connection.execute("SELECT * FROM songs")
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
    finally:
        connection.close()

    if not rows:
        return pl.DataFrame(schema={"msd_track_id": pl.String})

    frame = pl.DataFrame(rows, schema=columns, orient="row")
    if "track_id" not in frame.columns:
        raise ValueError("MSD metadata database must include songs.track_id")
    return frame.rename({"track_id": "msd_track_id"})


def build_lyrics_core(
    lyrics_txt: str | Path,
    output_parquet: str | Path,
    top_n_tokens: int | None = None,
    metadata_db: str | Path | None = None,
) -> pl.DataFrame:
    input_path = Path(lyrics_txt)
    output_path = Path(output_parquet)

    long_rows = pl.DataFrame(_parse_lyrics_rows(input_path))
    if long_rows.is_empty():
        raise ValueError("lyrics input produced no structured rows")

    frame = (
        long_rows.group_by(["msd_track_id", "token"])
        .agg(pl.col("count").sum().alias("count"))
        .sort(["msd_track_id", "token"])
    )
    if top_n_tokens is not None and top_n_tokens > 0:
        top_tokens = (
            frame.group_by("token")
            .agg(pl.col("count").sum().alias("total_count"))
            .sort(by=["total_count", "token"], descending=[True, False])
            .head(top_n_tokens)
            .get_column("token")
            .to_list()
        )
        frame = frame.filter(pl.col("token").is_in(top_tokens)).sort(
            ["msd_track_id", "token"]
        )
    if metadata_db is not None:
        metadata = _read_msd_metadata(Path(metadata_db))
        frame = frame.join(metadata, on="msd_track_id", how="left").select(
            [
                "msd_track_id",
                *[column for column in metadata.columns if column != "msd_track_id"],
                "token",
                "count",
            ]
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame.write_parquet(output_path)
    return frame
