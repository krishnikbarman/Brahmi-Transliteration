"""Training entry point for the Brahmi character recognizer.

This is a starter file. Add the model definition, training loop, and checkpoint
saving logic here once the preprocessing pipeline is finalized.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import BATCH_SIZE, CHECKPOINTS_DIR, EPOCHS, LOGS_DIR, MODELS_DIR, PROCESSED_DATASET_DIR, RANDOM_STATE  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Train the Brahmi character model.")
    parser.add_argument("--epochs", type=int, default=EPOCHS)
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument("--data-dir", type=Path, default=PROCESSED_DATASET_DIR)
    return parser


def main() -> None:
    args = build_parser().parse_args()

    # TODO: load processed samples, split train/validation sets, and train the model.
    # All outputs should be written under the configured checkpoints, logs, and models paths.
    empty_features = np.empty((0, 0))
    empty_labels = np.empty((0,))
    _ = train_test_split(empty_features, empty_labels, random_state=RANDOM_STATE) if empty_features.size else None

    print("Training scaffold is ready.")
    print(f"Data directory: {args.data_dir}")
    print(f"Epochs: {args.epochs}")
    print(f"Batch size: {args.batch_size}")
    print(f"Checkpoints: {CHECKPOINTS_DIR}")
    print(f"Models: {MODELS_DIR}")
    print(f"Logs: {LOGS_DIR}")


if __name__ == "__main__":
    main()
