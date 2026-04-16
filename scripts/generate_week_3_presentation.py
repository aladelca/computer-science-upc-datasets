from __future__ import annotations

import argparse
import math
import sys
import tempfile
import textwrap
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from upc_datasets.week_3_presentation_redesign import (  # noqa: E402
    RenderedSlide,
    SlideKind,
    load_redesign_config,
    load_redesign_profile,
    run_redesign_pipeline,
)

matplotlib.use("Agg")
plt.rcParams["mathtext.fontset"] = "dejavusans"

WIDTH = 1920
HEIGHT = 1080
ACCENT_RED = "#ff2d2d"
TEXT = "#111111"
MUTED = "#666666"
GRAY = "#cfcfcf"
LIGHT_GRAY = "#f5f5f5"
ASSET_XREFS = {
    "cover_photo": 48,
    "logo": 51,
    "llama": 52,
    "boar": 54,
    "robot": 111,
    "reduction_plot": 333,
}


@dataclass(frozen=True)
class Fonts:
    title: ImageFont.FreeTypeFont
    title_small: ImageFont.FreeTypeFont
    heading: ImageFont.FreeTypeFont
    subheading: ImageFont.FreeTypeFont
    body: ImageFont.FreeTypeFont
    body_small: ImageFont.FreeTypeFont
    bubble: ImageFont.FreeTypeFont
    bubble_small: ImageFont.FreeTypeFont
    bold: ImageFont.FreeTypeFont
    mono_big: ImageFont.FreeTypeFont
    mono_huge: ImageFont.FreeTypeFont


def load_font(size: int, *, bold: bool = False, serif: bool = False) -> ImageFont.FreeTypeFont:
    if serif:
        family = "DejaVu Serif"
    else:
        family = "DejaVu Sans"
    weight = "bold" if bold else "normal"
    font_path = font_manager.findfont(
        font_manager.FontProperties(family=family, weight=weight),
        fallback_to_default=True,
    )
    return ImageFont.truetype(font_path, size=size)


def load_fonts() -> Fonts:
    return Fonts(
        title=load_font(72, bold=True),
        title_small=load_font(42, bold=True),
        heading=load_font(50, bold=True),
        subheading=load_font(34, bold=True),
        body=load_font(30),
        body_small=load_font(24),
        bubble=load_font(42),
        bubble_small=load_font(34),
        bold=load_font(30, bold=True),
        mono_big=load_font(112, bold=True),
        mono_huge=load_font(148, bold=True),
    )


def ensure_rgb(image: Image.Image) -> Image.Image:
    if image.mode == "RGBA":
        return image
    return image.convert("RGBA")


def extract_assets(pdf_path: Path) -> dict[str, Image.Image]:
    import fitz

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        doc = fitz.open(pdf_path)
        smasks: dict[int, int] = {}
        for page in doc:
            for image_info in page.get_images(full=True):
                smasks[image_info[0]] = image_info[1]
        assets: dict[str, Image.Image] = {}
        for name, xref in ASSET_XREFS.items():
            pix = fitz.Pixmap(doc, xref)
            smask = smasks.get(xref, 0)
            if smask:
                mask = fitz.Pixmap(doc, smask)
                pix = fitz.Pixmap(pix, mask)
            output = temp_path / f"{name}.png"
            if pix.alpha or pix.n < 5:
                pix.save(output)
            else:
                fitz.Pixmap(fitz.csRGB, pix).save(output)
            assets[name] = Image.open(output).convert("RGBA")
        return assets


def new_slide() -> Image.Image:
    return Image.new("RGBA", (WIDTH, HEIGHT), "white")


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    if not text:
        return 0, 0
    bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=8, align="left")
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
) -> str:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        words = paragraph.split()
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if draw.textlength(candidate, font=font) <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return "\n".join(lines)


def fit_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    *,
    max_width: int,
    max_height: int,
    start_size: int,
    min_size: int,
    bold: bool = False,
    serif: bool = False,
) -> tuple[ImageFont.FreeTypeFont, str]:
    for size in range(start_size, min_size - 1, -2):
        font = load_font(size, bold=bold, serif=serif)
        wrapped = wrap_text(draw, text, font, max_width)
        width, height = text_size(draw, wrapped, font)
        if width <= max_width and height <= max_height:
            return font, wrapped
    font = load_font(min_size, bold=bold, serif=serif)
    return font, wrap_text(draw, text, font, max_width)


def paste_scaled(
    slide: Image.Image,
    image: Image.Image,
    *,
    box: tuple[int, int, int, int],
    anchor: str = "center",
) -> None:
    x0, y0, x1, y1 = box
    max_w = x1 - x0
    max_h = y1 - y0
    img = ensure_rgb(image)
    ratio = min(max_w / img.width, max_h / img.height)
    new_size = (max(1, int(img.width * ratio)), max(1, int(img.height * ratio)))
    resized = img.resize(new_size, Image.LANCZOS)
    if anchor == "center":
        px = x0 + (max_w - new_size[0]) // 2
        py = y0 + (max_h - new_size[1]) // 2
    elif anchor == "bottom_left":
        px = x0
        py = y1 - new_size[1]
    elif anchor == "bottom_right":
        px = x1 - new_size[0]
        py = y1 - new_size[1]
    else:
        px = x0
        py = y0
    slide.alpha_composite(resized, (px, py))


def add_logo(slide: Image.Image, assets: dict[str, Image.Image]) -> None:
    paste_scaled(slide, assets["logo"], box=(36, 28, 96, 88))


def draw_slide_title(
    draw: ImageDraw.ImageDraw,
    fonts: Fonts,
    title: str,
    *,
    subtitle: str | None = None,
) -> None:
    draw.text((110, 70), title, fill=TEXT, font=fonts.heading)
    if subtitle:
        draw.text((110, 135), subtitle, fill=MUTED, font=fonts.body_small)


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    *,
    box: tuple[int, int, int, int],
    font: ImageFont.FreeTypeFont,
    fill: str = TEXT,
    align: str = "center",
) -> None:
    x0, y0, x1, y1 = box
    wrapped = wrap_text(draw, text, font, x1 - x0)
    width, height = text_size(draw, wrapped, font)
    if align == "center":
        x = x0 + ((x1 - x0) - width) / 2
    else:
        x = x0
    y = y0 + ((y1 - y0) - height) / 2
    draw.multiline_text((x, y), wrapped, fill=fill, font=font, spacing=8, align=align)


def draw_speech_bubble(
    slide: Image.Image,
    fonts: Fonts,
    *,
    box: tuple[int, int, int, int],
    text: str,
    tail: str,
) -> None:
    overlay = Image.new("RGBA", slide.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    x0, y0, x1, y1 = box
    draw.ellipse((x0, y0, x1, y1), fill="white", outline="black", width=5)
    w = x1 - x0
    h = y1 - y0
    if tail == "left":
        points = [
            (x0 + int(0.15 * w), y0 + int(0.80 * h)),
            (x0 + int(0.04 * w), y1 + 56),
            (x0 + int(0.28 * w), y0 + int(0.90 * h)),
        ]
    else:
        points = [
            (x0 + int(0.75 * w), y0 + int(0.88 * h)),
            (x0 + int(0.92 * w), y1 + 52),
            (x0 + int(0.64 * w), y0 + int(0.82 * h)),
        ]
    draw.polygon(points, fill="white", outline="black")
    slide.alpha_composite(overlay)

    draw = ImageDraw.Draw(slide)
    font, wrapped = fit_text(
        draw,
        text,
        max_width=int(0.72 * w),
        max_height=int(0.60 * h),
        start_size=42,
        min_size=28,
    )
    width, height = text_size(draw, wrapped, font)
    tx = x0 + (w - width) / 2
    ty = y0 + (h - height) / 2 - 10
    draw.multiline_text((tx, ty), wrapped, fill=TEXT, font=font, spacing=8, align="center")


def add_dialogue_characters(slide: Image.Image, assets: dict[str, Image.Image]) -> None:
    paste_scaled(slide, assets["llama"], box=(120, 690, 360, 1040), anchor="bottom_left")
    paste_scaled(slide, assets["boar"], box=(1450, 720, 1870, 1000), anchor="bottom_right")


def add_dialogue_slide(
    assets: dict[str, Image.Image],
    fonts: Fonts,
    *,
    left_text: str | None = None,
    right_text: str | None = None,
    title: str | None = None,
) -> Image.Image:
    slide = new_slide()
    add_logo(slide, assets)
    add_dialogue_characters(slide, assets)
    draw = ImageDraw.Draw(slide)
    if title:
        draw.text((110, 78), title, fill=MUTED, font=fonts.body_small)
    if left_text and right_text:
        draw_speech_bubble(
            slide,
            fonts,
            box=(150, 110, 760, 430),
            text=left_text,
            tail="left",
        )
        draw_speech_bubble(
            slide,
            fonts,
            box=(870, 95, 1440, 455),
            text=right_text,
            tail="right",
        )
    elif left_text:
        draw_speech_bubble(
            slide,
            fonts,
            box=(540, 90, 1180, 420),
            text=left_text,
            tail="left",
        )
    elif right_text:
        draw_speech_bubble(
            slide,
            fonts,
            box=(650, 90, 1290, 420),
            text=right_text,
            tail="right",
        )
    return slide


def figure_to_image(fig: plt.Figure) -> Image.Image:
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    buffer.seek(0)
    return Image.open(buffer).convert("RGBA")


def make_equation_panel(
    equations: list[str],
    *,
    notes: list[str] | None = None,
    figsize: tuple[float, float] = (7.2, 4.2),
    equation_fontsize: int = 28,
    note_fontsize: int = 13,
) -> Image.Image:
    fig = plt.figure(figsize=figsize, facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    y = 0.92
    for equation in equations:
        ax.text(
            0.02,
            y,
            rf"${equation}$",
            fontsize=equation_fontsize,
            ha="left",
            va="top",
            color=TEXT,
        )
        y -= 0.24
    if notes:
        y -= 0.02
        for note in notes:
            ax.text(
                0.03,
                y,
                textwrap.fill(note, width=48),
                fontsize=note_fontsize,
                ha="left",
                va="top",
                color=TEXT,
            )
            y -= 0.12
    return figure_to_image(fig)


def make_distance_intuition_figure() -> Image.Image:
    rng = np.random.default_rng(7)
    query = np.array([0.52, 0.48])
    points = rng.uniform(0.05, 0.95, size=(14, 2))
    distances_2d = np.linalg.norm(points - query, axis=1)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.4))
    ax = axes[0]
    ax.scatter(points[:, 0], points[:, 1], s=60, color="#999999")
    ax.scatter(query[0], query[1], s=120, color=ACCENT_RED, marker="*")
    near_idx = int(np.argmin(distances_2d))
    far_idx = int(np.argmax(distances_2d))
    ax.scatter(points[near_idx, 0], points[near_idx, 1], s=80, color="#2a9d8f")
    ax.scatter(points[far_idx, 0], points[far_idx, 1], s=80, color="#264653")
    ax.plot(
        [query[0], points[near_idx, 0]],
        [query[1], points[near_idx, 1]],
        color="#2a9d8f",
        linewidth=2.5,
    )
    ax.plot(
        [query[0], points[far_idx, 0]],
        [query[1], points[far_idx, 1]],
        color="#264653",
        linewidth=2.5,
        linestyle="--",
    )
    ax.set_title("2D: close and far are visually distinct", fontsize=12, fontweight="bold")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    for spine in ax.spines.values():
        spine.set_visible(False)

    rng = np.random.default_rng(7)
    query_hd = rng.random(100)
    points_hd = rng.random((14, 100))
    distances_hd = np.sort(np.linalg.norm(points_hd - query_hd, axis=1))
    ax = axes[1]
    ax.bar(np.arange(1, len(distances_hd) + 1), distances_hd, color="#777777")
    ax.bar(1, distances_hd[0], color="#2a9d8f")
    ax.bar(len(distances_hd), distances_hd[-1], color="#264653")
    ax.set_title("100D: distances bunch together", fontsize=12, fontweight="bold")
    ax.set_xlabel("Candidate songs")
    ax.set_ylabel("Distance to query")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    return figure_to_image(fig)


def volume_ratio(dim: int) -> float:
    return math.pi ** (dim / 2) / (2**dim * math.gamma(dim / 2 + 1))


def make_volume_ratio_plot() -> Image.Image:
    dims = np.arange(1, 21)
    ratios = np.array([volume_ratio(int(dim)) for dim in dims])
    fig, ax = plt.subplots(figsize=(6.2, 4.5))
    ax.plot(dims, ratios, color=ACCENT_RED, linewidth=3)
    ax.scatter(dims, ratios, color=ACCENT_RED, s=25)
    ax.set_yscale("log")
    ax.set_xlabel("Dimension d")
    ax.set_ylabel("Ball volume / cube volume")
    ax.set_title("Inscribed ball share vanishes quickly", fontsize=13, fontweight="bold")
    ax.grid(alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return figure_to_image(fig)


def synthetic_distance_stats() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    dims = np.array([2, 5, 10, 20, 50, 100, 200, 500])
    means = []
    contrasts = []
    for dim in dims:
        rng = np.random.default_rng(100 + int(dim))
        query = rng.random(dim)
        points = rng.random((700, dim))
        distances = np.linalg.norm(points - query, axis=1)
        means.append(float(distances.mean()))
        contrasts.append(float((distances.max() - distances.min()) / distances.min()))
    return dims, np.array(means), np.array(contrasts)


def make_mean_distance_plot() -> Image.Image:
    dims, means, _ = synthetic_distance_stats()
    theory = np.sqrt(dims / 6)
    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    ax.plot(dims, means, color="#264653", linewidth=3, label="simulation")
    ax.plot(dims, theory, color=ACCENT_RED, linewidth=2.5, linestyle="--", label=r"$\sqrt{d/6}$")
    ax.scatter(dims, means, color="#264653", s=30)
    ax.set_xlabel("Dimension d")
    ax.set_ylabel("Mean Euclidean distance")
    ax.set_title("Typical distance grows with dimension", fontsize=13, fontweight="bold")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return figure_to_image(fig)


def make_contrast_plot() -> Image.Image:
    dims, _, contrasts = synthetic_distance_stats()
    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    ax.plot(dims, contrasts, color=ACCENT_RED, linewidth=3)
    ax.scatter(dims, contrasts, color=ACCENT_RED, s=35)
    ax.set_xlabel("Dimension d")
    ax.set_ylabel("(farthest - nearest) / nearest")
    ax.set_title("Contrast collapses as d increases", fontsize=13, fontweight="bold")
    ax.grid(alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return figure_to_image(fig)


def make_dense_sparse_figure() -> Image.Image:
    rng = np.random.default_rng(12)
    dense = rng.normal(loc=0.0, scale=1.0, size=(25, 45))
    sparse = np.zeros((25, 45))
    mask = rng.random((25, 45)) < 0.08
    sparse[mask] = rng.normal(loc=2.2, scale=0.6, size=mask.sum())

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.4))
    axes[0].imshow(dense, aspect="auto", cmap="viridis")
    axes[0].set_title("Dense audio descriptors", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("518 engineered features")
    axes[0].set_ylabel("Tracks")
    axes[0].set_xticks([])
    axes[0].set_yticks([])

    axes[1].imshow(sparse, aspect="auto", cmap="magma")
    axes[1].set_title("Sparse lyric matrix", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Vocabulary / n-grams")
    axes[1].set_ylabel("Tracks")
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    fig.tight_layout()
    return figure_to_image(fig)


def make_reduction_figure() -> Image.Image:
    rng = np.random.default_rng(21)
    centers = np.array(
        [
            [0.2, 0.4, 0.6],
            [1.0, 1.3, 0.3],
            [1.5, 0.6, 1.1],
        ]
    )
    colors = ["#5cc8d7", "#8cc63e", "#d97991"]
    clouds = [center + 0.12 * rng.normal(size=(12, 3)) for center in centers]

    fig = plt.figure(figsize=(10.2, 3.8))
    ax1 = fig.add_subplot(1, 3, 1, projection="3d")
    ax2 = fig.add_subplot(1, 3, 2)
    ax3 = fig.add_subplot(1, 3, 3)

    for cloud, color in zip(clouds, colors):
        ax1.scatter(cloud[:, 0], cloud[:, 1], cloud[:, 2], color=color, s=26)
    ax1.set_title("Original space", fontsize=12, fontweight="bold")
    ax1.set_xlabel("x1")
    ax1.set_ylabel("x2")
    ax1.set_zlabel("x3")
    ax1.view_init(elev=18, azim=-58)

    for cloud, color in zip(clouds, colors):
        projected = cloud[:, :2]
        ax2.scatter(projected[:, 0], projected[:, 1], color=color, s=26)
    ax2.set_title("Reduced to 2D", fontsize=12, fontweight="bold")
    ax2.set_xlabel("z1")
    ax2.set_ylabel("z2")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    for cloud, color in zip(clouds, colors):
        line = cloud[:, 0] + 0.35 * cloud[:, 1]
        y = np.zeros_like(line)
        ax3.scatter(line, y, color=color, s=26)
    ax3.set_title("Even fewer coordinates", fontsize=12, fontweight="bold")
    ax3.set_xlabel("z1")
    ax3.set_yticks([])
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.spines["left"].set_visible(False)

    fig.tight_layout()
    return figure_to_image(fig)


def make_hypercube_formula_panel() -> Image.Image:
    return make_equation_panel(
        [
            r"V_d(1)=\frac{\pi^{d/2}}{\Gamma\left(\frac{d}{2}+1\right)}",
            r"\mathrm{Vol}([-1,1]^d)=2^d",
            r"\frac{V_d(1)}{2^d}=\frac{\pi^{d/2}}{2^d\Gamma\left(\frac{d}{2}+1\right)}\to 0",
        ],
        notes=[
            "The d-dimensional unit ball occupies a vanishing fraction of the surrounding cube as dimension grows."
        ],
        figsize=(8.0, 4.8),
        equation_fontsize=30,
    )


def make_expected_distance_panel() -> Image.Image:
    return make_equation_panel(
        [
            r"x,y\sim \mathrm{Unif}([0,1]^d)",
            r"\mathrm{E}\|x-y\|_2^2=\sum_{j=1}^{d}\mathrm{E}(x_j-y_j)^2",
            r"=d\cdot\frac{1}{6}=\frac{d}{6}",
        ],
        notes=[
            "Each coordinate contributes 1/6 in expectation, so squared distances add linearly with d.",
            "That is why the Euclidean distance itself typically scales like sqrt(d).",
        ],
        figsize=(8.0, 4.8),
        equation_fontsize=30,
    )


def make_concentration_panel() -> Image.Image:
    return make_equation_panel(
        [
            r"\frac{\max_i d(x,x_i)-\min_i d(x,x_i)}{\min_i d(x,x_i)}\to 0",
        ],
        figsize=(7.0, 1.8),
        equation_fontsize=34,
    )


def make_sample_complexity_panel() -> Image.Image:
    return make_equation_panel(
        [
            r"N(\varepsilon)\approx \left(\frac{1}{\varepsilon}\right)^d",
            r"d\uparrow \ \mathrm{or}\ \varepsilon\downarrow \ \Rightarrow\ N(\varepsilon)\ \mathrm{explodes}",
        ],
        figsize=(6.4, 2.7),
        equation_fontsize=30,
    )


def make_recommendation_boxes(draw: ImageDraw.ImageDraw, fonts: Fonts) -> None:
    boxes = [
        (
            140,
            290,
            560,
            780,
            "K-nearest neighbors",
            "Nearest is only marginally closer than the rest, so the ranking becomes fragile.",
        ),
        (
            760,
            290,
            1180,
            780,
            "Clustering",
            "Clusters depend on weak distance contrast, noise, and preprocessing choices.",
        ),
        (
            1380,
            290,
            1800,
            780,
            "Recommendation",
            "A 'similar song' may be a metric artifact rather than a meaningful neighbor.",
        ),
    ]
    for x0, y0, x1, y1, title, body in boxes:
        draw.rounded_rectangle((x0, y0, x1, y1), radius=32, outline=GRAY, width=4, fill=LIGHT_GRAY)
        draw.text((x0 + 30, y0 + 35), title, fill=TEXT, font=fonts.subheading)
        font, wrapped = fit_text(
            draw,
            body,
            max_width=(x1 - x0) - 60,
            max_height=(y1 - y0) - 130,
            start_size=30,
            min_size=24,
        )
        draw.multiline_text(
            (x0 + 30, y0 + 120),
            wrapped,
            fill=TEXT,
            font=font,
            spacing=8,
        )


def make_feature_table(draw: ImageDraw.ImageDraw, fonts: Fonts) -> None:
    x0, y0, x1, y1 = 120, 300, 1260, 760
    cols = ["song", "tempo", "energy", "dance", "lyrics", "embed_1", "embed_2", "...", "embed_2000"]
    draw.rounded_rectangle((x0, y0, x1, y1), radius=24, outline=GRAY, width=4, fill="white")
    col_width = (x1 - x0) // len(cols)
    values = [
        ["Track A", "128", "0.83", "0.71", "142", "0.31", "-0.22", "...", "0.05"],
        ["Track B", "91", "0.42", "0.37", "601", "-0.07", "0.44", "...", "-0.19"],
        ["Track C", "147", "0.91", "0.88", "88", "0.54", "-0.38", "...", "0.11"],
    ]
    row_height = (y1 - y0) // (len(values) + 1)
    for idx in range(1, len(cols)):
        x = x0 + idx * col_width
        draw.line((x, y0, x, y1), fill=GRAY, width=2)
    for idx in range(1, len(values) + 1):
        y = y0 + idx * row_height
        draw.line((x0, y, x1, y), fill=GRAY, width=2)

    for idx, col in enumerate(cols):
        tx = x0 + idx * col_width + 12
        draw.text((tx, y0 + 18), col, fill=TEXT, font=fonts.body_small)

    for row_idx, row in enumerate(values):
        ty = y0 + (row_idx + 1) * row_height + 18
        for col_idx, value in enumerate(row):
            tx = x0 + col_idx * col_width + 12
            draw.text((tx, ty), value, fill=TEXT, font=fonts.body_small)

    note_box = (1330, 310, 1810, 770)
    draw.rounded_rectangle(note_box, radius=30, fill=LIGHT_GRAY, outline=GRAY, width=4)
    draw.text((1365, 350), "More columns can add:", fill=TEXT, font=fonts.subheading)
    bullets = [
        "noise",
        "sparsity",
        "distance instability",
        "sample complexity",
    ]
    for idx, item in enumerate(bullets):
        draw.text((1380, 430 + idx * 72), f"- {item}", fill=TEXT, font=fonts.body)


def draw_sample_complexity_table(slide: Image.Image, draw: ImageDraw.ImageDraw, fonts: Fonts) -> None:
    dims = [2, 5, 10]
    epsilons = [0.5, 0.2, 0.1]
    values = [[int((1 / eps) ** dim) for dim in dims] for eps in epsilons]
    x0, y0, x1, y1 = 230, 300, 1180, 760
    draw.rounded_rectangle((x0, y0, x1, y1), radius=26, outline=GRAY, width=4, fill="white")
    col_width = (x1 - x0) // (len(dims) + 1)
    row_height = (y1 - y0) // (len(epsilons) + 1)
    for idx in range(1, len(dims) + 1):
        x = x0 + idx * col_width
        draw.line((x, y0, x, y1), fill=GRAY, width=2)
    for idx in range(1, len(epsilons) + 1):
        y = y0 + idx * row_height
        draw.line((x0, y, x1, y), fill=GRAY, width=2)

    draw.text((x0 + 24, y0 + 20), "ε", fill=TEXT, font=fonts.body)
    for idx, dim in enumerate(dims, start=1):
        draw.text((x0 + idx * col_width + 22, y0 + 20), f"d = {dim}", fill=TEXT, font=fonts.body)
    for row_idx, eps in enumerate(epsilons, start=1):
        draw.text((x0 + 28, y0 + row_idx * row_height + 20), f"{eps:.1f}", fill=TEXT, font=fonts.body)
        for col_idx, value in enumerate(values[row_idx - 1], start=1):
            label = f"{value:,}" if value < 1_000_000 else f"{value:.1e}"
            draw.text(
                (x0 + col_idx * col_width + 18, y0 + row_idx * row_height + 20),
                label,
                fill=TEXT,
                font=fonts.body,
            )

    draw.rounded_rectangle((1310, 320, 1770, 720), radius=30, outline=GRAY, width=4, fill=LIGHT_GRAY)
    paste_scaled(slide, make_sample_complexity_panel(), box=(1330, 350, 1750, 690))


def draw_reduction_comparison(draw: ImageDraw.ImageDraw, fonts: Fonts) -> None:
    left = (120, 300, 870, 790)
    right = (1020, 300, 1770, 790)
    draw.rounded_rectangle(left, radius=28, outline=GRAY, width=4, fill="white")
    draw.rounded_rectangle(right, radius=28, outline=GRAY, width=4, fill="white")
    draw.text((160, 340), "Feature selection", fill=TEXT, font=fonts.subheading)
    draw.text((1060, 340), "Dimensionality reduction", fill=TEXT, font=fonts.subheading)

    selected = [
        "keep tempo",
        "keep energy",
        "drop lyric_bigram_1421",
        "drop embed_998",
    ]
    reduced = [
        "z1 = mix of rhythm + energy",
        "z2 = mix of timbre + lyrics",
        "new axes preserve structure",
        "visualization becomes usable",
    ]
    for idx, line in enumerate(selected):
        draw.text((170, 430 + idx * 72), f"- {line}", fill=TEXT, font=fonts.body)
    for idx, line in enumerate(reduced):
        draw.text((1070, 430 + idx * 72), f"- {line}", fill=TEXT, font=fonts.body)
    draw.text((350, 700), "choose original coordinates", fill=MUTED, font=fonts.body_small)
    draw.text((1210, 700), "construct new coordinates", fill=MUTED, font=fonts.body_small)


def cover_slide(assets: dict[str, Image.Image], fonts: Fonts) -> Image.Image:
    slide = new_slide()
    photo = assets["cover_photo"]
    scale = max(WIDTH / photo.width, HEIGHT / photo.height)
    resized = photo.resize((int(photo.width * scale), int(photo.height * scale)), Image.LANCZOS)
    offset_x = (resized.width - WIDTH) // 2
    offset_y = (resized.height - HEIGHT) // 2
    slide.alpha_composite(resized.crop((offset_x, offset_y, offset_x + WIDTH, offset_y + HEIGHT)))

    overlay = Image.new("RGBA", slide.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rounded_rectangle((110, 720, 1120, 990), radius=36, fill=(255, 255, 255, 220))
    slide.alpha_composite(overlay)

    draw = ImageDraw.Draw(slide)
    draw.text((160, 770), "Week 3", fill=TEXT, font=fonts.title_small)
    draw.text((160, 830), "The Curse of Dimensionality", fill=TEXT, font=fonts.title)
    draw.text(
        (165, 925),
        "Why more features can make distance, clustering, and recommendation less reliable.",
        fill=TEXT,
        font=fonts.body_small,
    )
    return slide


def code_sleep_repeat_slide(fonts: Fonts) -> Image.Image:
    slide = new_slide()
    draw = ImageDraw.Draw(slide)
    draw.text((700, 170), "CODE", fill=TEXT, font=fonts.mono_huge)
    draw.rounded_rectangle((690, 430, 1235, 545), radius=2, fill=ACCENT_RED)
    draw.text((760, 398), "SLEEP", fill="black", font=fonts.mono_big)
    draw.text((700, 565), "REPEAT", fill=TEXT, font=fonts.mono_huge)
    return slide


def build_slides(assets: dict[str, Image.Image], fonts: Fonts) -> list[RenderedSlide]:
    slides: list[RenderedSlide] = []

    def push(
        image: Image.Image,
        *,
        kind: SlideKind,
        title: str,
        subtitle: str | None = None,
        prompt_context: str | None = None,
    ) -> None:
        slides.append(
            RenderedSlide(
                index=len(slides) + 1,
                kind=kind,
                title=title,
                subtitle=subtitle,
                prompt_context=prompt_context,
                image=image,
            )
        )

    push(
        cover_slide(assets, fonts),
        kind=SlideKind.COVER,
        title="The Curse of Dimensionality",
        subtitle="Why more features can make distance, clustering, and recommendation less reliable.",
        prompt_context="Andean mountain cover slide with editorial title panel.",
    )
    first_dialogue = (
        "I made a feature vector with tempo, energy, danceability, acousticness, "
        "lyric counts, n-grams, embeddings, playlist statistics, and 2,000 extra "
        "columns just in case."
    )
    push(
        add_dialogue_slide(
            assets,
            fonts,
            left_text=first_dialogue,
            title="Mathias expands the feature space again.",
        ),
        kind=SlideKind.COMIC,
        title="Mathias expands the feature space again.",
        prompt_context=first_dialogue,
    )
    push(
        add_dialogue_slide(
            assets,
            fonts,
            left_text=first_dialogue,
            right_text="That is not a feature space. That is a cry for help.",
        ),
        kind=SlideKind.COMIC,
        title="Feature-space dialogue",
        prompt_context=f"{first_dialogue} | That is not a feature space. That is a cry for help.",
    )
    push(
        add_dialogue_slide(
            assets,
            fonts,
            right_text="Excellent. More dimensions means more nuance.",
        ),
        kind=SlideKind.COMIC,
        title="More dimensions means more nuance",
        prompt_context="Excellent. More dimensions means more nuance.",
    )
    push(
        add_dialogue_slide(
            assets,
            fonts,
            left_text="And also more ways for distance to become useless.",
        ),
        kind=SlideKind.COMIC,
        title="Distance becomes less useful",
        prompt_context="And also more ways for distance to become useless.",
    )
    push(
        add_dialogue_slide(
            assets,
            fonts,
            left_text="Now you are finally being harmed by geometry in the correct way.",
            right_text="So the nearest neighbor may not be near?",
        ),
        kind=SlideKind.COMIC,
        title="Geometry harms correctly",
        prompt_context="Now you are finally being harmed by geometry in the correct way. | So the nearest neighbor may not be near?",
    )

    slide = new_slide()
    add_logo(slide, assets)
    draw = ImageDraw.Draw(slide)
    title = "More variables do not guarantee more usable information"
    subtitle = "PachaMix audio has 518 numeric descriptors; lyric spaces are even larger."
    draw_slide_title(draw, fonts, title, subtitle=subtitle)
    make_feature_table(draw, fonts)
    push(
        slide,
        kind=SlideKind.CHART,
        title=title,
        subtitle=subtitle,
        prompt_context="Feature table plus callout notes about noise, sparsity, and instability.",
    )

    slide = new_slide()
    add_logo(slide, assets)
    draw = ImageDraw.Draw(slide)
    title = "Distance intuition fails in high dimension"
    subtitle = "The nearest and farthest candidates stop looking meaningfully different."
    draw_slide_title(draw, fonts, title, subtitle=subtitle)
    figure = make_distance_intuition_figure()
    paste_scaled(slide, figure, box=(160, 240, 1760, 840))
    draw.multiline_text((240, 870), "In 2D the query has a visibly close neighbor.\nIn 100D the sorted distances bunch together.", fill=TEXT, font=fonts.body, spacing=6)
    push(slide, kind=SlideKind.CHART, title=title, subtitle=subtitle, prompt_context="Two-panel distance intuition figure contrasting 2D and 100D.")

    slide = new_slide()
    add_logo(slide, assets)
    draw = ImageDraw.Draw(slide)
    title = "Hypercube versus hypersphere"
    subtitle = "The geometry itself changes as dimension grows."
    draw_slide_title(draw, fonts, title, subtitle=subtitle)
    paste_scaled(slide, make_hypercube_formula_panel(), box=(120, 240, 980, 760))
    draw.rounded_rectangle((1040, 290, 1650, 700), radius=24, outline=GRAY, width=4)
    draw.rectangle((1120, 350, 1510, 640), outline="#264653", width=5)
    draw.ellipse((1190, 395, 1440, 595), outline=ACCENT_RED, width=5)
    draw.text((1100, 720), "Even an inscribed ball occupies a vanishing share of the cube.", fill=TEXT, font=fonts.body_small)
    push(slide, kind=SlideKind.CHART, title=title, subtitle=subtitle, prompt_context="Formula panel with cube and sphere diagram.")

    slide = new_slide()
    add_logo(slide, assets)
    draw = ImageDraw.Draw(slide)
    title = "The inscribed ball vanishes inside the cube"
    subtitle = "Most of the ambient volume moves away from the center."
    draw_slide_title(draw, fonts, title, subtitle=subtitle)
    figure = make_volume_ratio_plot()
    paste_scaled(slide, figure, box=(180, 220, 1080, 860))
    draw.rounded_rectangle((1180, 270, 1760, 780), radius=30, outline=GRAY, width=4, fill=LIGHT_GRAY)
    draw.multiline_text((1220, 350), textwrap.fill("As dimension increases, local neighborhoods stop behaving like the ones we imagine from 2D or 3D drawings. That is why 'near' becomes harder to interpret.", width=26), fill=TEXT, font=fonts.body, spacing=10)
    push(slide, kind=SlideKind.CHART, title=title, subtitle=subtitle, prompt_context="Log-scale chart on the left, explanatory note card on the right.")

    slide = new_slide()
    add_logo(slide, assets)
    draw = ImageDraw.Draw(slide)
    title = "Expected squared distance in the unit hypercube"
    subtitle = "The first quantitative sign of the curse is that distances expand with dimension."
    draw_slide_title(draw, fonts, title, subtitle=subtitle)
    paste_scaled(slide, make_expected_distance_panel(), box=(110, 220, 1070, 840))
    draw.rounded_rectangle((1160, 260, 1760, 790), radius=30, outline=GRAY, width=4, fill=LIGHT_GRAY)
    draw.multiline_text((1210, 360), textwrap.fill("The derivation is simple but important: squared distances add coordinate by coordinate. More dimensions therefore stretch the ambient space even before we discuss nearest neighbors.", width=28), fill=TEXT, font=fonts.body, spacing=10)
    push(slide, kind=SlideKind.CHART, title=title, subtitle=subtitle, prompt_context="Equation panel with explanation card.")

    slide = new_slide()
    add_logo(slide, assets)
    draw = ImageDraw.Draw(slide)
    title = "Expected distance grows with dimension"
    subtitle = "Simulation follows the theoretical √d scaling very closely."
    draw_slide_title(draw, fonts, title, subtitle=subtitle)
    figure = make_mean_distance_plot()
    paste_scaled(slide, figure, box=(170, 240, 1040, 830))
    draw.rounded_rectangle((1160, 260, 1760, 790), radius=30, outline=GRAY, width=4, fill=LIGHT_GRAY)
    draw.multiline_text((1210, 360), textwrap.fill("Distances get larger on average, but that alone is not the deepest problem. The harder part is that relative contrast shrinks while computation gets harder.", width=28), fill=TEXT, font=fonts.body, spacing=10)
    push(slide, kind=SlideKind.CHART, title=title, subtitle=subtitle, prompt_context="Mean distance chart with theory line and callout.")

    slide = new_slide()
    add_logo(slide, assets)
    draw = ImageDraw.Draw(slide)
    title = "Distance concentration heuristic"
    subtitle = "Nearest and farthest candidates become less distinguishable in relative terms."
    draw_slide_title(draw, fonts, title, subtitle=subtitle)
    figure = make_contrast_plot()
    paste_scaled(slide, figure, box=(170, 240, 1040, 830))
    draw.rounded_rectangle((1140, 240, 1780, 790), radius=30, outline=GRAY, width=4, fill=LIGHT_GRAY)
    paste_scaled(slide, make_concentration_panel(), box=(1180, 285, 1740, 470))
    draw.multiline_text((1190, 520), textwrap.fill("This heuristic is the curse in operational form: the nearest and farthest songs become relatively indistinguishable. When contrast collapses, distance ranking stops being a strong source of information.", width=32), fill=TEXT, font=fonts.body_small, spacing=10)
    push(slide, kind=SlideKind.CHART, title=title, subtitle=subtitle, prompt_context="Contrast plot with equation inset and explanatory card.")

    slide = new_slide()
    add_logo(slide, assets)
    draw = ImageDraw.Draw(slide)
    title = "Why recommendation, KNN, and clustering suffer"
    subtitle = "Distance-based methods depend on neighborhoods that still carry contrast."
    draw_slide_title(draw, fonts, title, subtitle=subtitle)
    make_recommendation_boxes(draw, fonts)
    push(slide, kind=SlideKind.CHART, title=title, subtitle=subtitle, prompt_context="Three recommendation-method panels explaining weak neighborhood contrast.")

    push(
        code_sleep_repeat_slide(fonts),
        kind=SlideKind.DIVIDER,
        title="CODE SLEEP REPEAT",
        prompt_context="Bold interstitial divider with monospace emphasis.",
    )

    push(
        add_dialogue_slide(
            assets,
            fonts,
            left_text="Good. Now the distances are consistently misleading.",
            right_text="But we standardized the features.",
        ),
        kind=SlideKind.COMIC,
        title="Standardized but still misleading",
        prompt_context="Good. Now the distances are consistently misleading. | But we standardized the features.",
    )

    slide = new_slide()
    add_logo(slide, assets)
    draw = ImageDraw.Draw(slide)
    title = "Dense and sparse high-dimensional spaces fail differently"
    subtitle = "Audio features and lyric vocabularies are both high-dimensional, but not in the same way."
    draw_slide_title(draw, fonts, title, subtitle=subtitle)
    figure = make_dense_sparse_figure()
    paste_scaled(slide, figure, box=(170, 240, 1260, 840))
    note_box = (1280, 250, 1810, 840)
    draw.rounded_rectangle(note_box, radius=30, outline=GRAY, width=4, fill=LIGHT_GRAY)
    note_text = "- Dense audio spaces: many coordinates contribute small amounts.\n\n- Sparse lyric spaces: overlap of non-zero terms dominates similarity.\n\n- Sparsity changes the geometry. It does not remove the curse."
    note_font, wrapped_note = fit_text(draw, note_text, max_width=note_box[2] - note_box[0] - 70, max_height=note_box[3] - note_box[1] - 90, start_size=30, min_size=22)
    draw.multiline_text((note_box[0] + 40, note_box[1] + 45), wrapped_note, fill=TEXT, font=note_font, spacing=12)
    push(slide, kind=SlideKind.CHART, title=title, subtitle=subtitle, prompt_context="Dense vs sparse matrix heatmaps with explanatory note card.")

    slide = new_slide()
    add_logo(slide, assets)
    draw = ImageDraw.Draw(slide)
    title = "Sample complexity explodes"
    subtitle = "Trying to cover high-dimensional space with fine resolution becomes infeasible quickly."
    draw_slide_title(draw, fonts, title, subtitle=subtitle)
    draw_sample_complexity_table(slide, draw, fonts)
    draw.multiline_text((1350, 565), textwrap.fill("A naive grid argument is crude, but it exposes the exponential dependence on dimension immediately.", width=25), fill=TEXT, font=fonts.body_small, spacing=10)
    push(slide, kind=SlideKind.CHART, title=title, subtitle=subtitle, prompt_context="Sample complexity table with formula inset.")

    slide = new_slide()
    add_logo(slide, assets)
    draw = ImageDraw.Draw(slide)
    title = "Dimensionality reduction is structural, not cosmetic"
    subtitle = "It is different from merely dropping columns."
    draw_slide_title(draw, fonts, title, subtitle=subtitle)
    draw_reduction_comparison(draw, fonts)
    push(slide, kind=SlideKind.CHART, title=title, subtitle=subtitle, prompt_context="Side-by-side comparison of feature selection and dimensionality reduction.")

    push(
        add_dialogue_slide(
            assets,
            fonts,
            left_text="Precisely. Welcome to high-dimensional disappointment.",
            right_text="So more features can mean less useful signal?",
        ),
        kind=SlideKind.COMIC,
        title="High-dimensional disappointment",
        prompt_context="Precisely. Welcome to high-dimensional disappointment. | So more features can mean less useful signal?",
    )

    slide = new_slide()
    add_logo(slide, assets)
    draw = ImageDraw.Draw(slide)
    title = "The escape route is a better representation"
    subtitle = "We look for fewer coordinates that preserve the strongest structure."
    draw_slide_title(draw, fonts, title, subtitle=subtitle)
    paste_scaled(slide, assets["robot"], box=(170, 400, 620, 880))
    paste_scaled(slide, make_reduction_figure(), box=(700, 220, 1790, 810))
    draw.multiline_text((720, 840), "High-dimensional points\n-> lower-dimensional representation\n-> more interpretable structure", fill=TEXT, font=fonts.body_small, spacing=8)
    push(slide, kind=SlideKind.CHART, title=title, subtitle=subtitle, prompt_context="Robot illustration and dimensionality reduction figure.")

    push(
        add_dialogue_slide(
            assets,
            fonts,
            left_text="We reduce dimension, carefully, and with linear algebra.",
            right_text="So how do we escape?",
        ),
        kind=SlideKind.COMIC,
        title="How do we escape",
        prompt_context="We reduce dimension, carefully, and with linear algebra. | So how do we escape?",
    )

    slide = new_slide()
    add_logo(slide, assets)
    draw = ImageDraw.Draw(slide)
    title = "Week 3 takeaways"
    subtitle = "The theory sets up the PCA lecture that follows next week."
    draw_slide_title(draw, fonts, title, subtitle=subtitle)
    paste_scaled(slide, make_reduction_figure(), box=(1010, 210, 1820, 760))
    bullets = [
        "More dimensions can increase noise, sparsity, and instability.",
        "The inscribed ball shrinks relative to the cube as d grows.",
        "Distances grow but become less contrastive.",
        "Recommendation and clustering need structure beyond raw ambient coordinates.",
        "Dimensionality reduction creates a workable representation.",
    ]
    cursor = 280
    for item in bullets:
        wrapped = textwrap.fill(item, width=42)
        draw.multiline_text((160, cursor), f"- {wrapped}", fill=TEXT, font=fonts.body, spacing=8)
        cursor += 96
    draw.text((160, 910), "Next week: PCA and the geometry of variance.", fill=ACCENT_RED, font=fonts.subheading)
    push(slide, kind=SlideKind.CHART, title=title, subtitle=subtitle, prompt_context="Takeaways slide with bullet list and reduction visual.")

    push(
        code_sleep_repeat_slide(fonts),
        kind=SlideKind.DIVIDER,
        title="CODE SLEEP REPEAT",
        prompt_context="Bold closing divider with monospace emphasis.",
    )
    return slides


def _slide_images(slides: list[RenderedSlide]) -> list[Image.Image]:
    return [slide.image for slide in slides]


def save_pdf(slides: list[RenderedSlide], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rgb_slides = [slide.convert("RGB") for slide in _slide_images(slides)]
    first, *rest = rgb_slides
    first.save(output_path, save_all=True, append_images=rest, resolution=150.0)


def save_pptx(slides: list[RenderedSlide], output_path: Path) -> None:
    from pptx import Presentation
    from pptx.util import Inches

    output_path.parent.mkdir(parents=True, exist_ok=True)
    presentation = Presentation()
    presentation.slide_width = Inches(13.333333)
    presentation.slide_height = Inches(7.5)
    blank_layout = presentation.slide_layouts[6]

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        for index, slide_image in enumerate(_slide_images(slides), 1):
            slide = presentation.slides.add_slide(blank_layout)
            image_path = temp_path / f"slide_{index:02d}.png"
            slide_image.convert("RGB").save(image_path)
            slide.shapes.add_picture(
                str(image_path),
                0,
                0,
                width=presentation.slide_width,
                height=presentation.slide_height,
            )

        # Remove the default empty slide if it exists and is still blank.
        if len(presentation.slides) > len(slides):
            xml_slides = presentation.slides._sldIdLst  # type: ignore[attr-defined]
            xml_slides.remove(xml_slides[0])

        presentation.save(output_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate the Week 3 curse of dimensionality deck.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("big_data_course_content/presentations/week_3.pdf"),
        help="Output PDF path.",
    )
    parser.add_argument(
        "--source-pdf",
        type=Path,
        default=Path("big_data_course_content/presentations/week_2.pdf"),
        help="Week 2 PDF used as the asset source.",
    )
    parser.add_argument(
        "--output-pptx",
        type=Path,
        default=Path("big_data_course_content/presentations/week_3.pptx"),
        help="Optional PowerPoint output path. Use an empty string to skip PPTX export.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    fonts = load_fonts()
    assets = extract_assets(args.source_pdf)
    slides = build_slides(assets, fonts)
    redesign_config = load_redesign_config(cwd=Path.cwd())
    if redesign_config.enabled or redesign_config.dry_run:
        profile = load_redesign_profile(redesign_config.profile_path)
        slides = run_redesign_pipeline(
            slides=slides,
            config=redesign_config,
            profile=profile,
        )
    save_pdf(slides, args.output)
    if str(args.output_pptx).strip():
        save_pptx(slides, args.output_pptx)
        print(
            f"Generated {len(slides)} slides at {args.output} and {args.output_pptx}"
        )
    else:
        print(f"Generated {len(slides)} slides at {args.output}")


if __name__ == "__main__":
    main()
