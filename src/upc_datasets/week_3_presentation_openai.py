from __future__ import annotations

import base64
import json
import uuid
from dataclasses import dataclass
from io import BytesIO
from typing import Mapping
from urllib import request

from PIL import Image

from upc_datasets.week_3_presentation_ai import ImageEditResult


def _image_to_png_bytes(image: Image.Image) -> bytes:
    buffer = BytesIO()
    image.convert("RGBA").save(buffer, format="PNG")
    return buffer.getvalue()


def _build_multipart_form(fields: list[tuple[str, str]], files: list[tuple[str, str, bytes, str]]) -> tuple[bytes, str]:
    boundary = f"week3-{uuid.uuid4().hex}"
    body = bytearray()
    for name, value in fields:
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        body.extend(value.encode("utf-8"))
        body.extend(b"\r\n")
    for field_name, filename, payload, content_type in files:
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(
            (
                f'Content-Disposition: form-data; name="{field_name}"; '
                f'filename="{filename}"\r\n'
            ).encode("utf-8")
        )
        body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
        body.extend(payload)
        body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode("utf-8"))
    return bytes(body), boundary


@dataclass
class OpenAIImageEditProvider:
    api_key: str
    endpoint: str = "https://api.openai.com/v1/images/edits"
    provider_name: str = "openai"

    @classmethod
    def from_env(cls, env: Mapping[str, str]) -> "OpenAIImageEditProvider":
        api_key = env.get("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAI Week 3 redesign")
        return cls(api_key=api_key)

    def edit_slide(self, *, slide, prompt: str, model: str | None) -> ImageEditResult:
        image_bytes = _image_to_png_bytes(slide.image)
        request_body, boundary = _build_multipart_form(
            fields=[
                ("model", model or "gpt-image-1.5"),
                ("prompt", prompt),
                ("size", "1536x1024"),
            ],
            files=[
                ("image[]", f"slide-{slide.index:02d}-{uuid.uuid4().hex}.png", image_bytes, "image/png"),
            ],
        )
        req = request.Request(
            self.endpoint,
            data=request_body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
            method="POST",
        )
        with request.urlopen(req) as response:
            payload = json.loads(response.read().decode("utf-8"))
        image_b64 = str(payload["data"][0]["b64_json"])
        edited = Image.open(BytesIO(base64.b64decode(image_b64))).convert("RGBA")
        return ImageEditResult(
            image=edited,
            provider=self.provider_name,
            model=model or "gpt-image-1.5",
            metadata={"response": payload},
        )
