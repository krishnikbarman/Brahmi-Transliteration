"""Preprocess the Brahmi dataset into the configured output directory.

This starter script intentionally leaves the raw dataset untouched and keeps
all path handling centralized in configs/config.py.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import cv2
from PIL import Image
from tqdm import tqdm


SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp"}


def detect_project_root(start_path: Path) -> Path:
    """Find the repository root by walking upward until configs/config.py exists."""

    for candidate in [start_path, *start_path.parents]:
        if (candidate / "configs" / "config.py").is_file():
            return candidate
    raise RuntimeError("Unable to locate PROJECT_ROOT from preprocess_dataset.py")


def configure_utf8_console() -> None:
    """Make stdout/stderr safe for Unicode dataset paths on Windows consoles."""

    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

PROJECT_ROOT = detect_project_root(Path(__file__).resolve())
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import (  # noqa: E402
    DATASET_DIR,
    IMAGE_SIZE,
    IGNORED_DIR_NAMES,
    PROCESSED_DATASET_DIR,
    TEST_MODE,
    TEST_OUTPUT_DIR,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Preprocess the Brahmi dataset.")
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=DATASET_DIR,
        help="Directory containing the raw character folders.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=TEST_OUTPUT_DIR if TEST_MODE else PROCESSED_DATASET_DIR,
        help="Directory where processed samples will be written.",
    )
    return parser


def inspect_image(image_path: Path) -> tuple[int, int]:
    """Load an image in a safe, minimal way so preprocessing can evolve later."""

    with Image.open(image_path) as image:
        image = image.convert("L").resize(IMAGE_SIZE)
        array = np.asarray(image)
    return array.shape

def should_crop(image: np.ndarray, margin: int = 20) -> bool:

    coords = cv2.findNonZero(255 - image)

    if coords is None:
        return False

    x, y, w, h = cv2.boundingRect(coords)

    height, width = image.shape

    left = x
    top = y
    right = width - (x + w)
    bottom = height - (y + h)

    return (
        left > margin
        or right > margin
        or top > margin
        or bottom > margin
    )


def iter_class_folders(source_dir: Path) -> list[Path]:
    """Return class folders under the source dataset directory."""

    return sorted(
        path
        for path in source_dir.iterdir()
        if path.is_dir() and path.name not in IGNORED_DIR_NAMES
    )


def iter_image_files(class_folder: Path) -> list[Path]:
    """Return valid image files inside a class folder."""

    return sorted(
        path
        for path in class_folder.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
    )


def save_processed_image(processed_image: np.ndarray, output_path: Path) -> None:
    """Save a processed grayscale image as PNG."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image_array = np.clip(processed_image, 0.0, 1.0)
    image = Image.fromarray((image_array * 255).astype(np.uint8), mode="L")
    image.save(output_path, format="PNG")

def preprocess_image(image_path: Path) -> np.ndarray:
    """
    Read image and preprocess it.
    """

    with Image.open(image_path) as image:
        gray = np.asarray(image.convert("L"))

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    thresh = cv2.resize(
        thresh,
        IMAGE_SIZE,
        interpolation=cv2.INTER_AREA,
    )

    thresh = thresh.astype(np.float32) / 255.0

    return thresh


def process_image(image_path: Path, source_dir: Path, output_dir: Path) -> str:
    """Process one image and save it under the mirrored output structure."""

    processed = preprocess_image(image_path)
    relative_path = image_path.relative_to(source_dir).with_suffix(".png")
    output_path = output_dir / relative_path
    save_processed_image(processed, output_path)
    return f"{image_path} -> {output_path}"


def main() -> None:
    configure_utf8_console()

    args = build_parser().parse_args()
    source_dir = args.source_dir
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    character_folders = iter_class_folders(source_dir)
    processed_images = 0
    skipped_images = 0
    failed_images = 0

    print(f"Source dataset: {source_dir}")
    print(f"Processed output: {output_dir}")
    print(f"Discovered {len(character_folders)} character folders.")

    for folder in tqdm(character_folders, desc="Inspecting folders", unit="folder"):

        image_files = iter_image_files(folder)

        for image_path in image_files:
            try:
                message = process_image(image_path, source_dir, output_dir)
                processed_images += 1
                print(message)
            except (OSError, ValueError) as exc:
                skipped_images += 1
                print(f"Warning: skipping unreadable image {image_path}: {exc}")
            except Exception as exc:
                failed_images += 1
                print(f"Warning: failed to process image {image_path}: {exc}")

    print("Final summary:")
    print(f"Processed images: {processed_images}")
    print(f"Skipped images: {skipped_images}")
    print(f"Failed images: {failed_images}")


if __name__ == "__main__":
    main()
