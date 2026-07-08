"""Prediction entry point for the Brahmi character recognizer.

This file should later load a trained model and emit predictions for one image
or a batch of images without modifying the dataset.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import MODELS_DIR, TEST_OUTPUT_DIR  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Predict Brahmi characters from images.")
    parser.add_argument("image_path", type=Path, nargs="?", help="Path to an input image.")
    parser.add_argument("--models-dir", type=Path, default=MODELS_DIR)
    parser.add_argument("--output-dir", type=Path, default=TEST_OUTPUT_DIR)
    return parser


def preview_image(image_path: Path) -> tuple[int, int]:
    """Read an image safely so future inference code has a shared utility."""

    with Image.open(image_path) as image:
        image = image.convert("L")
        array = np.asarray(image)
    return array.shape


def main() -> None:
    args = build_parser().parse_args()

    # TODO: load the trained model and return the predicted Brahmi class label.
    if args.image_path is not None:
        shape = preview_image(args.image_path)
        print(f"Loaded image shape: {shape}")

    print("Prediction scaffold is ready.")
    print(f"Models directory: {args.models_dir}")
    print(f"Output directory: {args.output_dir}")


if __name__ == "__main__":
    main()
