"""Central project configuration for the Brahmi Character Recognition project.

All filesystem paths are derived from PROJECT_ROOT so the project can move
between machines without hardcoded Windows-specific locations.
"""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_DIR = PROJECT_ROOT / "dataset"
PROCESSED_DATASET_DIR = PROJECT_ROOT / "processed_dataset"
TEST_OUTPUT_DIR = PROJECT_ROOT / "test_output"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
MODELS_DIR = PROJECT_ROOT / "models"
CHECKPOINTS_DIR = PROJECT_ROOT / "checkpoints"
LOGS_DIR = PROJECT_ROOT / "logs"
RESULTS_DIR = PROJECT_ROOT / "results"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
DOCS_DIR = PROJECT_ROOT / "docs"
CONFIGS_DIR = PROJECT_ROOT / "configs"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 25
RANDOM_STATE = 42
NUM_WORKERS = 0
NUM_CLASSES = 416
TEST_MODE = os.getenv("TEST_MODE", "0").strip().lower() in {"1", "true", "yes", "on"}
IGNORED_DIR_NAMES = {".venv", ".git", "__pycache__", "processed_dataset", "test_output"}

PATHS = {
    "project_root": PROJECT_ROOT,
    "dataset": DATASET_DIR,
    "processed_dataset": PROCESSED_DATASET_DIR,
    "test_output": TEST_OUTPUT_DIR,
    "scripts": SCRIPTS_DIR,
    "models": MODELS_DIR,
    "checkpoints": CHECKPOINTS_DIR,
    "logs": LOGS_DIR,
    "results": RESULTS_DIR,
    "notebooks": NOTEBOOKS_DIR,
    "docs": DOCS_DIR,
    "configs": CONFIGS_DIR,
}

DIRECTORIES = (
    DATASET_DIR,
    PROCESSED_DATASET_DIR,
    TEST_OUTPUT_DIR,
    SCRIPTS_DIR,
    MODELS_DIR,
    CHECKPOINTS_DIR,
    LOGS_DIR,
    RESULTS_DIR,
    NOTEBOOKS_DIR,
    DOCS_DIR,
    CONFIGS_DIR,
)


def ensure_project_directories() -> None:
    """Create all expected top-level directories if they do not exist."""

    for directory in DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)
