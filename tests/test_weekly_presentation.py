from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))


def load_weekly_presentation_module():
    module_path = ROOT / "src" / "upc_datasets" / "weekly_presentation.py"
    spec = importlib.util.spec_from_file_location("weekly_presentation", module_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_discover_week_material_paths_resolves_week_3_assets() -> None:
    module = load_weekly_presentation_module()
    paths = module.discover_week_material_paths(ROOT, 3)

    assert paths.week_number == 3
    assert paths.topic_slug == "curse_of_dimensionality"
    assert paths.markdown_path.name == "week_03_curse_of_dimensionality.md"
    assert paths.notebook_path is not None
    assert paths.notebook_path.name == "week_03_curse_of_dimensionality.ipynb"
    assert paths.presentation_pdf.name == "week_3.pdf"
    assert paths.presentation_pptx.name == "week_3.pptx"
    assert paths.class_script_path.name == "week_03_curse_of_dimensionality_class_script.md"


def test_parse_week_3_markdown_and_notebook_outlines() -> None:
    module = load_weekly_presentation_module()
    paths = module.discover_week_material_paths(ROOT, 3)

    title, intro_lines, sections = module.parse_markdown_outline(paths.markdown_path)
    notebook_headings = module.parse_notebook_outline(paths.notebook_path)

    assert "Curse of Dimensionality" in title
    assert intro_lines == []
    assert sections
    assert any("Mathematical" in section.heading for section in sections)
    assert notebook_headings
    assert any("Curse of Dimensionality" in heading for heading in notebook_headings)


def test_build_outline_scaffold_slides_returns_structured_week_deck() -> None:
    module = load_weekly_presentation_module()
    paths = module.discover_week_material_paths(ROOT, 3)

    slides = module.build_outline_scaffold_slides(paths)

    assert len(slides) >= 5
    assert slides[0].kind is module.SlideKind.COVER
    assert slides[-1].kind is module.SlideKind.DIVIDER
    assert all(
        slide.image.size == (module.DEFAULT_SLIDE_WIDTH, module.DEFAULT_SLIDE_HEIGHT)
        for slide in slides
    )
    assert any(slide.title == "Notebook Flow" for slide in slides)


def test_build_generator_scaffold_uses_week_specific_naming() -> None:
    module = load_weekly_presentation_module()
    paths = module.discover_week_material_paths(ROOT, 4)

    script = module.build_generator_scaffold(paths)

    assert "WEEK_NUMBER = 4" in script
    assert "Generate the Week 4 scaffold deck." in script
    assert "discover_week_material_paths(ROOT, week_number=WEEK_NUMBER)" in script
    assert "save_pdf(slides, args.output)" in script
    assert "save_pptx(slides, args.output_pptx)" in script


def test_write_generator_scaffold_creates_script_file(tmp_path: Path) -> None:
    module = load_weekly_presentation_module()
    paths = module.WeekMaterialPaths(
        week_number=5,
        topic_slug="svd_tsne_and_embeddings",
        markdown_path=ROOT / "big_data_course_content" / "week_05_svd_tsne_and_embeddings.md",
        notebook_path=ROOT / "big_data_course_content" / "notebooks" / "week_05_svd_tsne_and_embeddings.ipynb",
        generator_script_path=tmp_path / "scripts" / "generate_week_5_presentation.py",
        presentation_pdf=tmp_path / "presentations" / "week_5.pdf",
        presentation_pptx=tmp_path / "presentations" / "week_5.pptx",
        class_script_path=tmp_path / "week_05_svd_tsne_and_embeddings_class_script.md",
    )

    output = module.write_generator_scaffold(paths)

    assert output.exists()
    content = output.read_text(encoding="utf-8")
    assert "WEEK_NUMBER = 5" in content
    assert 'default=WEEK_PATHS.presentation_pdf' in content
