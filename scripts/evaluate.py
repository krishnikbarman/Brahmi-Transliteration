"""Evaluation entry point for the Brahmi character recognizer.

Use this file to load a trained model, run inference on the validation or test
split, and write metrics into the configured results directory.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import PROCESSED_DATASET_DIR, RESULTS_DIR  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate the Brahmi character model.")
    parser.add_argument("--data-dir", type=Path, default=PROCESSED_DATASET_DIR)
    parser.add_argument("--results-dir", type=Path, default=RESULTS_DIR)
    return parser


def main() -> None:
    args = build_parser().parse_args()

    # TODO: load the saved model, compute predictions, and write evaluation artifacts.
    y_true = np.array([])
    y_pred = np.array([])
    if y_true.size and y_pred.size:
        print(f"Accuracy: {accuracy_score(y_true, y_pred):.4f}")
        print(classification_report(y_true, y_pred))
        matrix = confusion_matrix(y_true, y_pred)
        sns.heatmap(matrix, annot=False, cmap="Blues")
        plt.tight_layout()

    print("Evaluation scaffold is ready.")
    print(f"Data directory: {args.data_dir}")
    print(f"Results directory: {args.results_dir}")


if __name__ == "__main__":
    main()
