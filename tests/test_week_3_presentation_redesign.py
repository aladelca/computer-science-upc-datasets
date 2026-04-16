from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from upc_datasets.week_3_presentation_redesign import (  # noqa: E402
    RenderedSlide,
    SlideKind,
    compute_cache_key,
    load_redesign_config,
    load_redesign_profile,
    render_slide_prompt,
    run_redesign_pipeline,
)


def test_load_redesign_config_defaults_to_disabled() -> None:
    config = load_redesign_config({})

    assert config.provider == "none"
    assert config.enabled is False
    assert config.dry_run is False
    assert config.only_kind is None


def test_load_redesign_config_supports_openai_and_kind_filter(tmp_path: Path) -> None:
    config = load_redesign_config(
        {
            "WEEK3_REDESIGN_PROVIDER": "openai",
            "WEEK3_REDESIGN_MODEL": "gpt-image-1.5",
            "WEEK3_REDESIGN_DRY_RUN": "1",
            "WEEK3_REDESIGN_CACHE_DIR": str(tmp_path / "cache"),
            "WEEK3_REDESIGN_WORK_DIR": str(tmp_path / "work"),
            "WEEK3_REDESIGN_ONLY_KIND": "comic",
        }
    )

    assert config.provider == "openai"
    assert config.enabled is True
    assert config.model == "gpt-image-1.5"
    assert config.dry_run is True
    assert config.cache_dir == tmp_path / "cache"
    assert config.work_dir == tmp_path / "work"
    assert config.only_kind is SlideKind.COMIC


def test_load_redesign_profile_and_render_prompt() -> None:
    profile_path = (
        ROOT / "big_data_course_content" / "presentations" / "week_3_redesign_profile.json"
    )
    profile = load_redesign_profile(profile_path)
    slide = RenderedSlide(
        index=1,
        kind=SlideKind.COVER,
        title="The Curse of Dimensionality",
        subtitle="Why more features can make distance unreliable.",
        prompt_context="Andean mountain cover with strong editorial typography.",
        image=Image.new("RGBA", (64, 64), "white"),
    )

    prompt = render_slide_prompt(profile, slide, provider="openai")

    assert "The Curse of Dimensionality" in prompt
    assert "Andean" in prompt
    assert "preserve all readable text" in prompt.lower()
    assert profile.provider_defaults["openai"]
    assert profile.prompt_templates[SlideKind.COVER]


def test_compute_cache_key_changes_when_prompt_changes() -> None:
    slide = RenderedSlide(
        index=1,
        kind=SlideKind.CHART,
        title="Distance concentration heuristic",
        subtitle=None,
        prompt_context="Chart slide with red accent and callout box.",
        image=Image.new("RGBA", (32, 32), "white"),
    )

    key_a = compute_cache_key(
        slide=slide,
        prompt="prompt-a",
        provider="openai",
        model="gpt-image-1.5",
        profile_version="v1",
    )
    key_b = compute_cache_key(
        slide=slide,
        prompt="prompt-b",
        provider="openai",
        model="gpt-image-1.5",
        profile_version="v1",
    )

    assert key_a != key_b


def test_run_redesign_pipeline_dry_run_writes_manifest(tmp_path: Path) -> None:
    profile_path = (
        ROOT / "big_data_course_content" / "presentations" / "week_3_redesign_profile.json"
    )
    profile = load_redesign_profile(profile_path)
    config = load_redesign_config(
        {
            "WEEK3_REDESIGN_PROVIDER": "openai",
            "WEEK3_REDESIGN_MODEL": "gpt-image-1.5",
            "WEEK3_REDESIGN_DRY_RUN": "1",
            "WEEK3_REDESIGN_CACHE_DIR": str(tmp_path / "cache"),
            "WEEK3_REDESIGN_WORK_DIR": str(tmp_path / "work"),
        }
    )
    slides = [
        RenderedSlide(
            index=1,
            kind=SlideKind.DIVIDER,
            title="CODE SLEEP REPEAT",
            subtitle=None,
            prompt_context="Bold divider slide.",
            image=Image.new("RGBA", (80, 60), "white"),
        )
    ]

    result = run_redesign_pipeline(slides=slides, config=config, profile=profile)

    assert result == slides
    manifest = tmp_path / "work" / "manifest.json"
    original = tmp_path / "work" / "slides" / "slide_01_original.png"
    prompt_manifest = tmp_path / "work" / "prompts.json"
    assert manifest.exists()
    assert original.exists()
    assert prompt_manifest.exists()

    manifest_payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert manifest_payload["provider"] == "openai"
    assert manifest_payload["dry_run"] is True
    assert manifest_payload["slides"][0]["kind"] == "divider"

