"""Generate a dataset statistics report for the Brahmi character dataset.

The script scans class folders under the configured dataset directory,
counts valid images, detects corrupted image files, and writes a summary report
to the results directory without modifying the dataset.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
from PIL import Image, UnidentifiedImageError
from tqdm import tqdm


def detect_project_root(start_path: Path) -> Path:
    """Walk upward from this file until the repository root is found."""

    for candidate in [start_path, *start_path.parents]:
        if (candidate / "configs" / "config.py").is_file():
            return candidate
    raise RuntimeError("Unable to locate PROJECT_ROOT for dataset_stats.py")


PROJECT_ROOT = detect_project_root(Path(__file__).resolve())
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import DATASET_DIR, RESULTS_DIR  # noqa: E402


IMAGE_EXTENSIONS = {
    ".bmp",
    ".gif",
    ".jpeg",
    ".jpg",
    ".png",
    ".tif",
    ".tiff",
    ".webp",
}


def build_parser() -> argparse.ArgumentParser:
    """Create the command line interface for the stats script."""

    parser = argparse.ArgumentParser(description="Generate Brahmi dataset statistics.")
    parser.add_argument("--dataset-dir", type=Path, default=DATASET_DIR)
    parser.add_argument("--results-dir", type=Path, default=RESULTS_DIR)
    return parser


def is_image_file(file_path: Path) -> bool:
    """Return True when a file looks like an image based on its extension."""

    return file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS


def is_corrupted_image(file_path: Path) -> bool:
    """Check whether an image file can be opened and verified by Pillow."""

    try:
        with Image.open(file_path) as image:
            image.verify()
        return False
    except (UnidentifiedImageError, OSError, ValueError):
        return True


def analyze_class_folder(class_folder: Path) -> dict[str, object]:
    """Collect image counts and corruption information for one class folder."""

    image_files = [file_path for file_path in class_folder.iterdir() if is_image_file(file_path)]
    valid_images = 0
    corrupted_images = 0

    for image_path in image_files:
        if is_corrupted_image(image_path):
            corrupted_images += 1
        else:
            valid_images += 1

    return {
        "class_name": class_folder.name,
        "image_count": valid_images,
        "corrupted_images": corrupted_images,
        "total_files": len(list(class_folder.iterdir())),
        "empty_folder": valid_images == 0,
    }


def build_summary(report_df: pd.DataFrame) -> list[str]:
    """Create human-readable summary lines from the report dataframe."""

    total_classes = int(report_df.shape[0])
    total_images = int(report_df["image_count"].sum()) if total_classes else 0
    average_images = float(report_df["image_count"].mean()) if total_classes else 0.0

    if total_classes:
        largest_row = report_df.sort_values(["image_count", "class_name"], ascending=[False, True]).iloc[0]
        smallest_row = report_df.sort_values(["image_count", "class_name"], ascending=[True, True]).iloc[0]
        empty_folders = report_df.loc[report_df["image_count"] == 0, "class_name"].tolist()
    else:
        largest_row = {"class_name": "N/A", "image_count": 0}
        smallest_row = {"class_name": "N/A", "image_count": 0}
        empty_folders = []

    return [
        f"Project root: {PROJECT_ROOT}",
        f"Dataset directory: {DATASET_DIR}",
        f"Total classes: {total_classes}",
        f"Total images: {total_images}",
        f"Average images per class: {average_images:.2f}",
        f"Largest class: {largest_row['class_name']} ({int(largest_row['image_count'])} images)",
        f"Smallest class: {smallest_row['class_name']} ({int(smallest_row['image_count'])} images)",
        f"Empty folders: {', '.join(empty_folders) if empty_folders else 'None'}",
    ]


def save_reports(report_df: pd.DataFrame, summary_lines: list[str], results_dir: Path) -> tuple[Path, Path]:
    """Write the CSV and text summary into the configured results directory."""

    results_dir.mkdir(parents=True, exist_ok=True)
    csv_path = results_dir / "dataset_report.csv"
    summary_path = results_dir / "dataset_summary.txt"

    report_df.to_csv(csv_path, index=False)
    summary_path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    return csv_path, summary_path


def main() -> None:
    """Run the dataset scan and print a concise report to the console."""

    args = build_parser().parse_args()
    dataset_dir = args.dataset_dir
    results_dir = args.results_dir

    if not dataset_dir.exists():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")

    class_folders = sorted([path for path in dataset_dir.iterdir() if path.is_dir()])
    rows: list[dict[str, object]] = []

    for class_folder in tqdm(class_folders, desc="Analyzing class folders", unit="class"):
        rows.append(analyze_class_folder(class_folder))

    report_columns = ["class_name", "image_count", "corrupted_images", "total_files", "empty_folder"]
    report_df = pd.DataFrame(rows, columns=report_columns)
    if not report_df.empty:
        report_df = report_df.sort_values(["class_name"]).reset_index(drop=True)
    summary_lines = build_summary(report_df)
    csv_path, summary_path = save_reports(report_df, summary_lines, results_dir)

    for line in summary_lines:
        print(line)
    print(f"Saved CSV report: {csv_path}")
    print(f"Saved summary report: {summary_path}")


if __name__ == "__main__":
    main()