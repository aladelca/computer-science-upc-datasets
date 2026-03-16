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
