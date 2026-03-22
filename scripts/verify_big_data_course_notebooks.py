from __future__ import annotations

import os
import sys
import time
import traceback
from pathlib import Path

import nbformat

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = REPO_ROOT / "big_data_course_content" / "notebooks"


def main() -> int:
    os.chdir(REPO_ROOT)
    os.environ.setdefault("MPLBACKEND", "Agg")
    cache_root = REPO_ROOT / "big_data_course_content" / ".cache"
    cache_root.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("XDG_CACHE_HOME", str(cache_root))
    os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")
    mpl_config_dir = REPO_ROOT / "big_data_course_content" / ".mplconfig"
    mpl_config_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(mpl_config_dir))

    notebook_paths = sorted(NOTEBOOK_DIR.glob("week_*.ipynb"))
    if not notebook_paths:
        print("No notebooks found to verify.")
        return 1

    failed = False
    for notebook_path in notebook_paths:
        started = time.perf_counter()
        try:
            execute_notebook(notebook_path)
        except Exception:
            failed = True
            print(f"FAILED {notebook_path.relative_to(REPO_ROOT)}")
            traceback.print_exc()
            break
        else:
            elapsed = time.perf_counter() - started
            print(f"OK {notebook_path.relative_to(REPO_ROOT)} ({elapsed:.1f}s)")

    return 1 if failed else 0


def execute_notebook(notebook_path: Path) -> None:
    notebook = nbformat.read(notebook_path, as_version=4)
    namespace: dict[str, object] = {"__name__": "__main__"}

    for index, cell in enumerate(notebook.cells, start=1):
        if cell.cell_type != "code":
            continue

        source = cell.source.strip()
        if not source:
            continue

        code = compile(
            cell.source,
            filename=f"{notebook_path.relative_to(REPO_ROOT)}#cell-{index}",
            mode="exec",
        )
        try:
            exec(code, namespace)
        except Exception as exc:  # noqa: BLE001
            preview = "\n".join(cell.source.splitlines()[:12])
            raise RuntimeError(
                f"{notebook_path.relative_to(REPO_ROOT)} failed at cell {index}:\n{preview}"
            ) from exc

    plt = namespace.get("plt")
    if plt is not None:
        try:
            plt.close("all")
        except Exception:  # noqa: BLE001
            pass


if __name__ == "__main__":
    sys.exit(main())
