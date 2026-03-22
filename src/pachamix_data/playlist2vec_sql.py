from __future__ import annotations

import argparse
import csv
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Sequence

from pachamix_data.builders import build_playlist_events, build_song_graph


@dataclass(slots=True)
class Playlist2vecSqlExportResult:
    sqlite_db_path: Path
    playlist_csv_path: Path
    track_csv_path: Path
    track_playlist_csv_path: Path
    playlist_rows: int
    track_rows: int
    membership_rows: int
    playlist_events_path: Path | None = None
    playlist_stats_path: Path | None = None
    track_popularity_path: Path | None = None
    song_graph_path: Path | None = None


@dataclass(frozen=True, slots=True)
class _TableSpec:
    name: str
    insert_sql: str
    source_indexes: tuple[int, ...]


TABLE_SPECS: dict[str, _TableSpec] = {
    "album": _TableSpec(
        name="album",
        insert_sql="INSERT OR REPLACE INTO album (id, name) VALUES (?, ?)",
        source_indexes=(0, 1),
    ),
    "artist": _TableSpec(
        name="artist",
        insert_sql="INSERT OR REPLACE INTO artist (id, name) VALUES (?, ?)",
        source_indexes=(0, 1),
    ),
    "playlist": _TableSpec(
        name="playlist",
        insert_sql="INSERT OR REPLACE INTO playlist (id, name) VALUES (?, ?)",
        source_indexes=(0, 1),
    ),
    "track": _TableSpec(
        name="track",
        insert_sql="INSERT OR REPLACE INTO track (id, name, album_id) VALUES (?, ?, ?)",
        source_indexes=(0, 1, 7),
    ),
    "track_artist1": _TableSpec(
        name="track_artist1",
        insert_sql="INSERT INTO track_artist1 (track_id, artist_id) VALUES (?, ?)",
        source_indexes=(0, 1),
    ),
    "track_playlist1": _TableSpec(
        name="track_playlist1",
        insert_sql="INSERT INTO track_playlist1 (track_id, playlist_id) VALUES (?, ?)",
        source_indexes=(0, 1),
    ),
}


def _decode_mysql_escape(character: str) -> str:
    mapping = {
        "0": "\0",
        "b": "\b",
        "n": "\n",
        "r": "\r",
        "t": "\t",
        "Z": "\x1a",
        "\\": "\\",
        "'": "'",
        '"': '"',
    }
    return mapping.get(character, character)


def _normalize_unquoted_value(value: str) -> str | None:
    stripped = value.strip()
    if stripped.upper() == "NULL":
        return None
    return stripped


def _iter_insert_rows(values_chunk: str) -> Iterator[list[str | None]]:
    index = 0
    chunk_length = len(values_chunk)

    while index < chunk_length:
        while index < chunk_length and values_chunk[index] in " \t\r\n,":
            index += 1

        if index >= chunk_length:
            return

        if values_chunk[index] != "(":
            raise ValueError(
                f"unexpected token while parsing INSERT chunk at position {index}"
            )

        index += 1
        row: list[str | None] = []
        field_chars: list[str] = []
        field_is_quoted = False
        field_was_quoted = False

        def flush_field() -> None:
            raw_field = "".join(field_chars)
            if field_was_quoted:
                row.append(raw_field)
            else:
                row.append(_normalize_unquoted_value(raw_field))

        while index < chunk_length:
            character = values_chunk[index]

            if field_is_quoted:
                if character == "\\":
                    index += 1
                    if index >= chunk_length:
                        raise ValueError("unterminated escape sequence in SQL string")
                    field_chars.append(_decode_mysql_escape(values_chunk[index]))
                    index += 1
                    continue
                if character == "'":
                    field_is_quoted = False
                    index += 1
                    continue
                field_chars.append(character)
                index += 1
                continue

            if character == "'":
                field_is_quoted = True
                field_was_quoted = True
                index += 1
                continue

            if character == ",":
                flush_field()
                field_chars = []
                field_was_quoted = False
                index += 1
                continue

            if character == ")":
                flush_field()
                index += 1
                yield row
                break

            field_chars.append(character)
            index += 1


def _iter_relevant_inserts(sql_dump_path: Path) -> Iterator[tuple[str, str]]:
    with sql_dump_path.open("r", encoding="latin-1", errors="replace") as handle:
        for line in handle:
            if not line.startswith("INSERT INTO `"):
                continue
            table_start = len("INSERT INTO `")
            table_end = line.find("`", table_start)
            if table_end == -1:
                continue
            table_name = line[table_start:table_end]
            if table_name not in TABLE_SPECS:
                continue
            values_marker = " VALUES "
            values_index = line.find(values_marker)
            if values_index == -1:
                continue
            values_chunk = line[values_index + len(values_marker) :].rstrip(";\n")
            yield table_name, values_chunk


def _initialize_sqlite_db(sqlite_db_path: Path) -> sqlite3.Connection:
    sqlite_db_path.parent.mkdir(parents=True, exist_ok=True)
    if sqlite_db_path.exists():
        sqlite_db_path.unlink()

    connection = sqlite3.connect(sqlite_db_path)
    connection.execute("PRAGMA journal_mode = WAL")
    connection.execute("PRAGMA synchronous = OFF")
    connection.execute("PRAGMA temp_store = MEMORY")
    connection.execute("PRAGMA cache_size = -200000")
    connection.executescript(
        """
        DROP TABLE IF EXISTS album;
        DROP TABLE IF EXISTS artist;
        DROP TABLE IF EXISTS playlist;
        DROP TABLE IF EXISTS track;
        DROP TABLE IF EXISTS track_artist1;
        DROP TABLE IF EXISTS track_playlist1;

        CREATE TABLE album (
            id TEXT PRIMARY KEY,
            name TEXT
        );

        CREATE TABLE artist (
            id TEXT PRIMARY KEY,
            name TEXT
        );

        CREATE TABLE playlist (
            id TEXT PRIMARY KEY,
            name TEXT
        );

        CREATE TABLE track (
            id TEXT PRIMARY KEY,
            name TEXT,
            album_id TEXT
        );

        CREATE TABLE track_artist1 (
            track_id TEXT,
            artist_id TEXT
        );

        CREATE TABLE track_playlist1 (
            track_id TEXT,
            playlist_id TEXT
        );
        """
    )
    return connection


def _flush_batch(
    connection: sqlite3.Connection,
    table_name: str,
    rows: list[tuple[str | None, ...]],
) -> None:
    if not rows:
        return
    connection.executemany(TABLE_SPECS[table_name].insert_sql, rows)
    connection.commit()
    rows.clear()


def _selected_values(
    row: Sequence[str | None],
    source_indexes: Sequence[int],
) -> tuple[str | None, ...]:
    return tuple(row[index] if index < len(row) else None for index in source_indexes)


def _load_sql_dump_into_sqlite(
    sql_dump_path: Path,
    sqlite_db_path: Path,
    *,
    batch_size: int = 5000,
) -> tuple[sqlite3.Connection, dict[str, int]]:
    connection = _initialize_sqlite_db(sqlite_db_path)
    counts = {table_name: 0 for table_name in TABLE_SPECS}
    batches: dict[str, list[tuple[str | None, ...]]] = {
        table_name: [] for table_name in TABLE_SPECS
    }

    for table_name, values_chunk in _iter_relevant_inserts(sql_dump_path):
        spec = TABLE_SPECS[table_name]
        batch = batches[table_name]
        for row in _iter_insert_rows(values_chunk):
            batch.append(_selected_values(row, spec.source_indexes))
            counts[table_name] += 1
            if len(batch) >= batch_size:
                _flush_batch(connection, table_name, batch)

    for table_name, batch in batches.items():
        _flush_batch(connection, table_name, batch)

    connection.executescript(
        """
        CREATE INDEX IF NOT EXISTS idx_track_album_id ON track (album_id);
        CREATE INDEX IF NOT EXISTS idx_track_artist_track_id ON track_artist1 (track_id);
        CREATE INDEX IF NOT EXISTS idx_track_artist_artist_id ON track_artist1 (artist_id);
        CREATE INDEX IF NOT EXISTS idx_track_playlist_track_id ON track_playlist1 (track_id);
        CREATE INDEX IF NOT EXISTS idx_track_playlist_playlist_id ON track_playlist1 (playlist_id);
        """
    )
    connection.commit()
    return connection, counts


def _write_csv(
    path: Path, header: Sequence[str], rows: Iterable[Sequence[object]]
) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)
            written += 1
    return written


def _export_playlist_csv(
    connection: sqlite3.Connection, output_dir: Path
) -> tuple[Path, int]:
    output_path = output_dir / "playlist.csv"
    cursor = connection.execute(
        """
        SELECT id AS playlist_id, COALESCE(name, '') AS name
        FROM playlist
        ORDER BY id
        """
    )
    row_count = _write_csv(output_path, ["playlist_id", "name"], cursor)
    return output_path, row_count


def _export_track_csv(
    connection: sqlite3.Connection, output_dir: Path
) -> tuple[Path, int]:
    output_path = output_dir / "track.csv"
    cursor = connection.execute(
        """
        WITH ordered_artists AS (
            SELECT ta.track_id, COALESCE(a.name, '') AS artist_name
            FROM track_artist1 AS ta
            JOIN artist AS a ON a.id = ta.artist_id
            ORDER BY ta.track_id, a.name
        ),
        track_artists AS (
            SELECT track_id, GROUP_CONCAT(artist_name, ' | ') AS artist_name
            FROM ordered_artists
            GROUP BY track_id
        )
        SELECT
            t.id AS track_id,
            COALESCE(t.name, '') AS track_name,
            COALESCE(track_artists.artist_name, '') AS artist_name,
            COALESCE(album.name, '') AS album_name
        FROM track AS t
        LEFT JOIN track_artists ON track_artists.track_id = t.id
        LEFT JOIN album ON album.id = t.album_id
        ORDER BY t.id
        """
    )
    row_count = _write_csv(
        output_path,
        ["track_id", "track_name", "artist_name", "album_name"],
        cursor,
    )
    return output_path, row_count


def _export_track_playlist_csv(
    connection: sqlite3.Connection,
    output_dir: Path,
) -> tuple[Path, int]:
    output_path = output_dir / "track_playlist1.csv"
    cursor = connection.execute(
        """
        SELECT playlist_id, track_id
        FROM track_playlist1
        ORDER BY playlist_id, track_id
        """
    )
    row_count = _write_csv(output_path, ["playlist_id", "track_id"], cursor)
    return output_path, row_count


def extract_playlist2vec_exports(
    sql_dump_path: str | Path,
    *,
    output_dir: str | Path,
    sqlite_db_path: str | Path | None = None,
    processed_root: str | Path | None = None,
    batch_size: int = 5000,
) -> Playlist2vecSqlExportResult:
    sql_dump = Path(sql_dump_path)
    exports_dir = Path(output_dir)
    sqlite_db = (
        Path(sqlite_db_path)
        if sqlite_db_path is not None
        else exports_dir.parent / "playlist2vec.sqlite"
    )

    connection, _ = _load_sql_dump_into_sqlite(
        sql_dump,
        sqlite_db,
        batch_size=batch_size,
    )
    try:
        playlist_csv_path, playlist_rows = _export_playlist_csv(connection, exports_dir)
        track_csv_path, track_rows = _export_track_csv(connection, exports_dir)
        track_playlist_csv_path, membership_rows = _export_track_playlist_csv(
            connection,
            exports_dir,
        )
    finally:
        connection.close()

    result = Playlist2vecSqlExportResult(
        sqlite_db_path=sqlite_db,
        playlist_csv_path=playlist_csv_path,
        track_csv_path=track_csv_path,
        track_playlist_csv_path=track_playlist_csv_path,
        playlist_rows=playlist_rows,
        track_rows=track_rows,
        membership_rows=membership_rows,
    )

    if processed_root is not None:
        processed_root_path = Path(processed_root)
        playlist_result = build_playlist_events(
            mpd_json=exports_dir,
            output_dir=processed_root_path / "pachamix_playlists",
        )
        graph_result = build_song_graph(
            playlist_events_parquet=playlist_result.events_path,
            output_parquet=processed_root_path / "pachamix_song_graph_edges.parquet",
        )
        result.playlist_events_path = playlist_result.events_path
        result.playlist_stats_path = playlist_result.playlist_stats_path
        result.track_popularity_path = playlist_result.track_popularity_path
        result.song_graph_path = graph_result.edges_path

    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m pachamix_data.playlist2vec_sql",
        description=(
            "Extract Playlist2vec CSV exports from the official SQL dump using "
            "SQLite instead of MySQL."
        ),
    )
    parser.add_argument("--sql-dump", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--sqlite-db")
    parser.add_argument("--processed-root")
    parser.add_argument("--batch-size", type=int, default=5000)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    result = extract_playlist2vec_exports(
        args.sql_dump,
        output_dir=args.output_dir,
        sqlite_db_path=args.sqlite_db,
        processed_root=args.processed_root,
        batch_size=args.batch_size,
    )
    print(f"sqlite-db: {result.sqlite_db_path}")
    print(f"playlist.csv: {result.playlist_csv_path} ({result.playlist_rows} rows)")
    print(f"track.csv: {result.track_csv_path} ({result.track_rows} rows)")
    print(
        f"track_playlist1.csv: {result.track_playlist_csv_path} "
        f"({result.membership_rows} rows)"
    )
    if result.playlist_events_path is not None:
        print(f"playlist-events: {result.playlist_events_path}")
        print(f"playlist-stats: {result.playlist_stats_path}")
        print(f"track-popularity: {result.track_popularity_path}")
        print(f"song-graph: {result.song_graph_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
