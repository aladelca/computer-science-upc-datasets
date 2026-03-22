from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = {"PYTHONPATH": str(SRC)}
    return subprocess.run(
        [sys.executable, "-m", "pachamix_data.cli", *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_package_can_be_imported() -> None:
    import pachamix_data

    assert pachamix_data.__version__


def test_cli_help_succeeds() -> None:
    result = run_cli("--help")

    assert result.returncode == 0
    assert "usage:" in result.stdout.lower()


def test_cli_lists_supported_builders() -> None:
    result = run_cli("list-builders")

    assert result.returncode == 0
    assert "audio-core" in result.stdout
    assert "lyrics-core" in result.stdout
    assert "playlist2vec-sql" in result.stdout


def test_cli_can_extract_playlist2vec_sql_without_mysql(tmp_path: Path) -> None:
    sql_dump = tmp_path / "playlist2vec.sql"
    sql_dump.write_text(
        """
INSERT INTO `album` VALUES ('alb1','Album One',NULL);
INSERT INTO `artist` VALUES ('art1','Artist One',NULL);
INSERT INTO `playlist` VALUES ('10','Focus Mix',NULL,NULL,1);
INSERT INTO `track` VALUES ('trk1','Song One',180,10,'false',NULL,'spotify:track:trk1','alb1');
INSERT INTO `track_artist1` VALUES ('trk1','art1');
INSERT INTO `track_playlist1` VALUES ('trk1','10');
        """.strip()
        + "\n",
        encoding="latin-1",
    )

    result = run_cli(
        "extract-playlist2vec-sql",
        "--sql-dump",
        str(sql_dump),
        "--output-dir",
        str(tmp_path / "playlist2vec"),
        "--sqlite-db",
        str(tmp_path / "playlist2vec.sqlite"),
        "--processed-root",
        str(tmp_path / "processed"),
        "--batch-size",
        "2",
    )

    assert result.returncode == 0, result.stderr
    assert "playlist.csv:" in result.stdout
    assert "song-graph:" in result.stdout
    assert (tmp_path / "playlist2vec" / "playlist.csv").exists()
    assert (
        tmp_path / "processed" / "pachamix_playlists" / "playlist_events.parquet"
    ).exists()
