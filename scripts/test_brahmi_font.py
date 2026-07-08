"""Render a Brahmi Unicode sample using a Brahmi-compatible font.

The script creates a 224x224 white image, centers the target character pair in
black, and saves the result to results/test_brahmi.png.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def detect_project_root(start_path: Path) -> Path:
    """Walk upward until the repository root is found."""

    for candidate in [start_path, *start_path.parents]:
        if (candidate / "configs" / "config.py").is_file():
            return candidate
    raise RuntimeError("Unable to locate PROJECT_ROOT for test_brahmi_font.py")


PROJECT_ROOT = detect_project_root(Path(__file__).resolve())
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import RESULTS_DIR  # noqa: E402


TARGET_TEXT = "𑀕𑀂"
IMAGE_SIZE = (224, 224)
FONT_SIZE = 128


def candidate_font_paths() -> list[Path]:
    """Return likely Brahmi font locations on Windows and in the repo."""

    candidates = [
        PROJECT_ROOT / "fonts" / "NotoSansBrahmi-Regular.ttf",
        PROJECT_ROOT / "fonts" / "NotoSansBrahmi.ttf",
        PROJECT_ROOT / "assets" / "fonts" / "NotoSansBrahmi-Regular.ttf",
        Path(r"C:\Windows\Fonts\NotoSansBrahmi-Regular.ttf"),
        Path(r"C:\Windows\Fonts\NotoSansBrahmi.ttf"),
        Path(r"C:\Windows\Fonts\NotoSansBrahmi-Regular.otf"),
    ]
    return candidates


def find_brahmi_font() -> Path:
    """Locate a font file capable of rendering Brahmi Unicode text."""

    for font_path in candidate_font_paths():
        if font_path.exists():
            return font_path
    raise FileNotFoundError(
        "No Brahmi-compatible font was found. Expected a font such as "
        "'NotoSansBrahmi-Regular.ttf' in the project fonts/ directory or in "
        r"C:\Windows\Fonts."
    )


def render_brahmi_text(font_path: Path, output_path: Path) -> None:
    """Create the image, center the sample text, and save the PNG output."""

    image = Image.new("RGB", IMAGE_SIZE, color="white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(str(font_path), FONT_SIZE)

    bbox = draw.textbbox((0, 0), TARGET_TEXT, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x_position = (IMAGE_SIZE[0] - text_width) / 2 - bbox[0]
    y_position = (IMAGE_SIZE[1] - text_height) / 2 - bbox[1]

    draw.text((x_position, y_position), TARGET_TEXT, fill="black", font=font)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


def main() -> None:
    """Render the Brahmi sample text or print a clear font error."""

    try:
        font_path = find_brahmi_font()
    except FileNotFoundError as exc:
        print(str(exc))
        print("Required font file: NotoSansBrahmi-Regular.ttf")
        sys.exit(1)

    output_path = RESULTS_DIR / "test_brahmi.png"
    render_brahmi_text(font_path, output_path)
    print(f"Saved Brahmi test image: {output_path}")
    print(f"Used font: {font_path}")


if __name__ == "__main__":
    main()