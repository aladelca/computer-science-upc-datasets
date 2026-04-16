from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from upc_datasets.weekly_presentation import (  # noqa: E402
    build_outline_scaffold_slides,
    discover_week_material_paths,
    save_pdf,
    save_pptx,
    write_generator_scaffold,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a week presentation generator and optional base deck."
    )
    parser.add_argument("week", type=int, help="Week number to scaffold.")
    parser.add_argument(
        "--generator-output",
        type=Path,
        default=None,
        help="Override the generated generator script path.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Override the generated PDF path.",
    )
    parser.add_argument(
        "--output-pptx",
        type=Path,
        default=None,
        help="Override the generated PPTX path. Pass an empty string to skip PPTX export.",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Only write the generator scaffold without exporting the base deck.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing generator scaffold.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = discover_week_material_paths(ROOT, week_number=args.week)

    target_script = args.generator_output or paths.generator_script_path
    if target_script.exists() and not args.force:
        print(f"Generator already exists at {target_script}; leaving it unchanged.")
    else:
        written = write_generator_scaffold(
            paths,
            output_path=target_script,
            force=args.force,
        )
        print(f"Wrote generator scaffold to {written}")

    if args.skip_build:
        print(
            f"Week {paths.week_number} scaffold ready. "
            f"Markdown: {paths.markdown_path} | Notebook: {paths.notebook_path}"
        )
        return

    pdf_output = args.output or paths.presentation_pdf
    pptx_output = paths.presentation_pptx if args.output_pptx is None else args.output_pptx

    slides = build_outline_scaffold_slides(paths)
    save_pdf(slides, pdf_output)
    if str(pptx_output).strip():
        save_pptx(slides, pptx_output)
        print(
            f"Generated {len(slides)} scaffold slides at {pdf_output} and {pptx_output}"
        )
        return

    print(f"Generated {len(slides)} scaffold slides at {pdf_output}")


if __name__ == "__main__":
    main()
