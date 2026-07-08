"""Shared utilities for the Brahmi Character Recognition project.

Keep reusable helpers here so training, evaluation, and prediction scripts stay
thin and consistent with the path configuration in configs/config.py.
"""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image


def ensure_dir(path: Path) -> Path:
    """Create a directory if needed and return the same path."""

    path.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: Any, path: Path) -> None:
    """Write a JSON artifact with stable formatting."""

    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as file_handle:
        json.dump(data, file_handle, indent=2, ensure_ascii=False)
        file_handle.write("\n")


def load_json(path: Path) -> Any:
    """Load a JSON artifact from disk."""

    with path.open("r", encoding="utf-8") as file_handle:
        return json.load(file_handle)


def seed_everything(seed: int) -> None:
    """Seed the common random number generators used in ML experiments."""

    random.seed(seed)
    np.random.seed(seed)


def load_grayscale_image(image_path: Path) -> np.ndarray:
    """Load an image as a grayscale NumPy array for downstream preprocessing."""

    with Image.open(image_path) as image:
        return np.asarray(image.convert("L"))
