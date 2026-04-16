from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from enum import StrEnum
from io import BytesIO
from pathlib import Path
from typing import Any, Mapping, cast

from PIL import Image, ImageDraw

from upc_datasets.week_3_presentation_ai import ImageEditProvider
from upc_datasets.week_3_presentation_gemini import GeminiImageEditProvider
from upc_datasets.week_3_presentation_openai import OpenAIImageEditProvider


class SlideKind(StrEnum):
    COVER = "cover"
    COMIC = "comic"
    CHART = "chart"
    DIVIDER = "divider"


@dataclass
class RenderedSlide:
    index: int
    kind: SlideKind
    title: str
    subtitle: str | None
    prompt_context: str | None
    image: Image.Image
    notes: str | None = None


@dataclass(frozen=True)
class RedesignConfig:
    provider: str
    enabled: bool
    model: str | None
    dry_run: bool
    cache_dir: Path
    work_dir: Path
    only_kind: SlideKind | None
    profile_path: Path


@dataclass(frozen=True)
class RedesignProfile:
    version: str
    style_direction: str
    negative_constraints: list[str]
    prompt_templates: dict[SlideKind, str]
    provider_defaults: dict[str, dict[str, str]]


def _parse_bool(raw: str | None, *, default: bool) -> bool:
    if raw is None:
        return default
    normalized = raw.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default


def load_redesign_config(
    env: Mapping[str, str] | None = None,
    *,
    cwd: Path | None = None,
) -> RedesignConfig:
    values = env if env is not None else os.environ
    base_dir = cwd or Path.cwd()
    provider = values.get("WEEK3_REDESIGN_PROVIDER", "none").strip().lower() or "none"
    if provider not in {"none", "openai", "gemini"}:
        raise ValueError(f"unsupported WEEK3_REDESIGN_PROVIDER: {provider}")
    only_kind_raw = values.get("WEEK3_REDESIGN_ONLY_KIND")
    only_kind = SlideKind(only_kind_raw.strip().lower()) if only_kind_raw else None
    enabled_default = provider != "none"
    enabled = _parse_bool(values.get("WEEK3_REDESIGN_ENABLED"), default=enabled_default)
    profile_path = Path(
        values.get(
            "WEEK3_REDESIGN_PROFILE",
            "big_data_course_content/presentations/week_3_redesign_profile.json",
        )
    )
    return RedesignConfig(
        provider=provider,
        enabled=enabled,
        model=values.get("WEEK3_REDESIGN_MODEL"),
        dry_run=_parse_bool(values.get("WEEK3_REDESIGN_DRY_RUN"), default=False),
        cache_dir=base_dir
        / Path(
            values.get(
                "WEEK3_REDESIGN_CACHE_DIR",
                ".artifacts/week3-redesign/cache",
            )
        ),
        work_dir=base_dir
        / Path(
            values.get(
                "WEEK3_REDESIGN_WORK_DIR",
                ".artifacts/week3-redesign/work",
            )
        ),
        only_kind=only_kind,
        profile_path=base_dir / profile_path,
    )


def load_redesign_profile(path: Path) -> RedesignProfile:
    payload = json.loads(path.read_text(encoding="utf-8"))
    prompt_templates = {
        SlideKind(key): value for key, value in cast(dict[str, str], payload["prompt_templates"]).items()
    }
    provider_defaults = cast(dict[str, dict[str, str]], payload["provider_defaults"])
    return RedesignProfile(
        version=str(payload["version"]),
        style_direction=str(payload["style_direction"]),
        negative_constraints=[str(item) for item in payload["negative_constraints"]],
        prompt_templates=prompt_templates,
        provider_defaults=provider_defaults,
    )


def render_slide_prompt(
    profile: RedesignProfile,
    slide: RenderedSlide,
    *,
    provider: str,
) -> str:
    template = profile.prompt_templates[slide.kind]
    default_model = profile.provider_defaults.get(provider, {}).get("model", "")
    rendered_template = template.format(
        title=slide.title or "Untitled",
        subtitle=slide.subtitle or "",
        prompt_context=slide.prompt_context or "",
        notes=slide.notes or "",
    ).strip()
    negative = " ".join(profile.negative_constraints)
    return (
        f"Style direction: {profile.style_direction}\n"
        f"Provider target: {provider}\n"
        f"Default model hint: {default_model}\n"
        f"Slide kind: {slide.kind.value}\n"
        f"{rendered_template}\n"
        f"Constraints: {negative}"
    ).strip()


def compute_cache_key(
    *,
    slide: RenderedSlide,
    prompt: str,
    provider: str,
    model: str | None,
    profile_version: str,
) -> str:
    buffer = BytesIO()
    slide.image.save(buffer, format="PNG")
    digest = hashlib.sha256()
    digest.update(buffer.getvalue())
    digest.update(prompt.encode("utf-8"))
    digest.update(provider.encode("utf-8"))
    digest.update((model or "").encode("utf-8"))
    digest.update(profile_version.encode("utf-8"))
    digest.update(slide.kind.value.encode("utf-8"))
    return digest.hexdigest()


def _resolve_provider(config: RedesignConfig, env: Mapping[str, str] | None = None) -> ImageEditProvider:
    values = env if env is not None else os.environ
    if config.provider == "openai":
        return OpenAIImageEditProvider.from_env(values)
    if config.provider == "gemini":
        return GeminiImageEditProvider.from_env(values)
    raise ValueError("cannot resolve provider for redesign when provider is 'none'")


def _save_image(path: Path, image: Image.Image) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGBA").save(path)


def _write_contact_sheet(slides: list[RenderedSlide], work_dir: Path) -> None:
    if not slides:
        return
    thumbs: list[Image.Image] = []
    for slide in slides:
        thumb = slide.image.copy()
        thumb.thumbnail((320, 180))
        canvas = Image.new("RGBA", (340, 220), "white")
        canvas.alpha_composite(thumb, ((340 - thumb.width) // 2, 20))
        draw = ImageDraw.Draw(canvas)
        draw.text((12, 190), f"{slide.index:02d} {slide.kind.value}", fill="black")
        thumbs.append(canvas)
    cols = 2
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * 340, rows * 220), "#f0f0f0")
    for idx, thumb in enumerate(thumbs):
        x = (idx % cols) * 340
        y = (idx // cols) * 220
        sheet.alpha_composite(thumb, (x, y))
    _save_image(work_dir / "contact_sheet.png", sheet)


def run_redesign_pipeline(
    *,
    slides: list[RenderedSlide],
    config: RedesignConfig,
    profile: RedesignProfile,
    env: Mapping[str, str] | None = None,
    provider_factory=None,
) -> list[RenderedSlide]:
    config.work_dir.mkdir(parents=True, exist_ok=True)
    config.cache_dir.mkdir(parents=True, exist_ok=True)
    selected_kind = config.only_kind

    provider = None
    if config.enabled and not config.dry_run and config.provider != "none":
        if provider_factory is not None:
            provider = provider_factory(config)
        else:
            provider = _resolve_provider(config, env)

    prompt_entries: list[dict[str, Any]] = []
    manifest_entries: list[dict[str, Any]] = []
    redesigned_slides: list[RenderedSlide] = []

    for slide in slides:
        prompt = render_slide_prompt(profile, slide, provider=config.provider)
        cache_key = compute_cache_key(
            slide=slide,
            prompt=prompt,
            provider=config.provider,
            model=config.model or profile.provider_defaults.get(config.provider, {}).get("model"),
            profile_version=profile.version,
        )
        selected = selected_kind is None or slide.kind is selected_kind
        original_path = config.work_dir / "slides" / f"slide_{slide.index:02d}_original.png"
        _save_image(original_path, slide.image)

        prompt_entries.append(
            {
                "index": slide.index,
                "kind": slide.kind.value,
                "title": slide.title,
                "prompt": prompt,
                "selected": selected,
                "cache_key": cache_key,
            }
        )

        output_slide = slide
        cache_path = config.cache_dir / f"{cache_key}.png"
        redesigned_path = config.work_dir / "slides" / f"slide_{slide.index:02d}_redesigned.png"
        provider_metadata: dict[str, Any] = {}
        if selected and config.enabled and config.provider != "none" and not config.dry_run:
            if cache_path.exists():
                cached = Image.open(cache_path).convert("RGBA")
                output_slide = RenderedSlide(
                    index=slide.index,
                    kind=slide.kind,
                    title=slide.title,
                    subtitle=slide.subtitle,
                    prompt_context=slide.prompt_context,
                    image=cached,
                    notes=slide.notes,
                )
                provider_metadata = {"cache_hit": True}
            else:
                assert provider is not None
                result = provider.edit_slide(slide=slide, prompt=prompt, model=config.model)
                _save_image(cache_path, result.image)
                output_slide = RenderedSlide(
                    index=slide.index,
                    kind=slide.kind,
                    title=slide.title,
                    subtitle=slide.subtitle,
                    prompt_context=slide.prompt_context,
                    image=result.image,
                    notes=slide.notes,
                )
                provider_metadata = result.metadata
            _save_image(redesigned_path, output_slide.image)

        redesigned_slides.append(output_slide)
        manifest_entries.append(
            {
                "index": slide.index,
                "kind": slide.kind.value,
                "title": slide.title,
                "selected": selected,
                "original_path": str(original_path),
                "redesigned_path": str(redesigned_path) if redesigned_path.exists() else None,
                "cache_key": cache_key,
                "provider_metadata": provider_metadata,
            }
        )

    (config.work_dir / "prompts.json").write_text(
        json.dumps(prompt_entries, indent=2),
        encoding="utf-8",
    )
    (config.work_dir / "manifest.json").write_text(
        json.dumps(
            {
                "provider": config.provider,
                "enabled": config.enabled,
                "dry_run": config.dry_run,
                "model": config.model or profile.provider_defaults.get(config.provider, {}).get("model"),
                "profile_version": profile.version,
                "slides": manifest_entries,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    _write_contact_sheet(redesigned_slides, config.work_dir)
    return redesigned_slides
