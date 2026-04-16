from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from upc_datasets.week_3_presentation_redesign import SlideKind  # noqa: E402


def load_week_3_script_module():
    script_path = ROOT / "scripts" / "generate_week_3_presentation.py"
    spec = importlib.util.spec_from_file_location("generate_week_3_presentation", script_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_build_slides_returns_structured_slide_metadata() -> None:
    module = load_week_3_script_module()
    fonts = module.load_fonts()
    assets = {
        "cover_photo": Image.new("RGBA", (400, 300), "#dddddd"),
        "logo": Image.new("RGBA", (80, 80), "#ff2d2d"),
        "llama": Image.new("RGBA", (120, 180), "#f6eadf"),
        "boar": Image.new("RGBA", (150, 110), "#8b5a3c"),
        "robot": Image.new("RGBA", (120, 180), "#a0c4ff"),
        "reduction_plot": Image.new("RGBA", (320, 180), "#ffffff"),
    }

    slides = module.build_slides(assets, fonts)

    assert len(slides) == 24
    assert slides[0].kind is SlideKind.COVER
    counts = Counter(slide.kind for slide in slides)
    assert counts[SlideKind.COVER] == 1
    assert counts[SlideKind.COMIC] == 8
    assert counts[SlideKind.DIVIDER] == 2
    assert counts[SlideKind.CHART] == 13
    assert all(slide.image.size == (module.WIDTH, module.HEIGHT) for slide in slides)
