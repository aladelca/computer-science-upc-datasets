from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from io import BytesIO
from typing import Mapping
from urllib import parse, request

from PIL import Image

from upc_datasets.week_3_presentation_ai import ImageEditResult


def _image_to_png_bytes(image: Image.Image) -> bytes:
    buffer = BytesIO()
    image.convert("RGBA").save(buffer, format="PNG")
    return buffer.getvalue()


@dataclass
class GeminiImageEditProvider:
    api_key: str
    endpoint_template: str = (
        "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    )
    provider_name: str = "gemini"

    @classmethod
    def from_env(cls, env: Mapping[str, str]) -> "GeminiImageEditProvider":
        api_key = env.get("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required for Gemini Week 3 redesign")
        return cls(api_key=api_key)

    def edit_slide(self, *, slide, prompt: str, model: str | None) -> ImageEditResult:
        resolved_model = model or "gemini-3.1-flash-image-preview"
        image_bytes = _image_to_png_bytes(slide.image)
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": base64.b64encode(image_bytes).decode("utf-8"),
                            }
                        },
                    ]
                }
            ]
        }
        url = self.endpoint_template.format(
            model=parse.quote(resolved_model, safe=""),
            api_key=parse.quote(self.api_key, safe=""),
        )
        req = request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req) as response:
            body = json.loads(response.read().decode("utf-8"))

        image_data = ""
        for candidate in body.get("candidates", []):
            parts = candidate.get("content", {}).get("parts", [])
            for part in parts:
                inline_data = part.get("inline_data", {})
                if inline_data.get("data"):
                    image_data = str(inline_data["data"])
                    break
            if image_data:
                break
        if not image_data:
            raise ValueError("Gemini response did not include edited image data")

        edited = Image.open(BytesIO(base64.b64decode(image_data))).convert("RGBA")
        return ImageEditResult(
            image=edited,
            provider=self.provider_name,
            model=resolved_model,
            metadata={"response": body},
        )
