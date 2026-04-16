from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Protocol

from PIL import Image

if TYPE_CHECKING:
    from upc_datasets.week_3_presentation_redesign import RenderedSlide


@dataclass(frozen=True)
class ImageEditResult:
    image: Image.Image
    provider: str
    model: str
    metadata: dict[str, Any]


class ImageEditProvider(Protocol):
    provider_name: str

    def edit_slide(
        self,
        *,
        slide: RenderedSlide,
        prompt: str,
        model: str | None,
    ) -> ImageEditResult:
        ...
