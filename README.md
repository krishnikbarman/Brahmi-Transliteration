# Brahmi Character Recognition

A research-oriented Brahmi character recognition project structured for dataset preprocessing, model training, evaluation, and prediction. The repository is organized so that all paths are derived from a single project root and the raw dataset remains untouched.

## Project Overview

This project is designed for OCR-style recognition of Brahmi character classes stored in class-specific folders under `dataset/`. The scaffold separates raw data, processed data, model artifacts, logs, experiment outputs, and reusable scripts so the research workflow stays reproducible.

## Dataset Structure

The dataset follows a folder-per-class layout:

```text
Brahmi_Project/
└── dataset/
    ├── अ/
    ├── अं/
    ├── अः/
    ├── आ/
    ├── इ/
    └── ...
```

Each folder represents one character class. The project currently contains 429 character folders.

## Installation

1. Create and activate the project virtual environment:

```bash
python -m venv .venv
```

2. Activate it on Windows:

```bash
.venv\Scripts\activate
```

3. Install the project dependencies:

```bash
pip install -r requirements.txt
```

4. Run the environment check:

```bash
python scripts/environment_check.py
```

## Development Tooling

- Black is configured as the default formatter.
- Ruff is configured for linting and import hygiene.
- VS Code recommendations include Python, Pylance, Jupyter, GitHub Copilot, Black Formatter, Ruff, and Error Lens.
- `pathlib` is part of the Python standard library, so it is used in code but not installed through `pip`.

### Recommended VS Code Extensions

- `ms-python.python`
- `ms-python.vscode-pylance`
- `ms-toolsai.jupyter`
- `GitHub.copilot`
- `ms-python.black-formatter`
- `charliermarsh.ruff`
- `usernamehw.errorlens`

### VS Code Tasks and Debugging

- Use `Terminal -> Run Task` for:
    - `Environment Check`
    - `Dataset Preprocessing`
    - `Model Training`
    - `Evaluation`
- Use `Run and Debug` configurations for the same four workflows.

## Usage

All scripts resolve paths from `configs/config.py`, which automatically detects `PROJECT_ROOT`.

### Preprocessing

```bash
python scripts/preprocess_dataset.py
```

Optional arguments:

```bash
python scripts/preprocess_dataset.py --source-dir dataset --output-dir processed_dataset
```

### Training

```bash
python scripts/train.py
```

Optional arguments:

```bash
python scripts/train.py --epochs 25 --batch-size 32 --data-dir processed_dataset
```

### Evaluation

```bash
python scripts/evaluate.py
```

### Prediction

```bash
python scripts/predict.py path/to/image.png
```

## Folder Structure

```text
Brahmi_Project/
├── dataset/
├── processed_dataset/
├── test_output/
├── scripts/
│   ├── preprocess_dataset.py
│   ├── train.py
│   ├── evaluate.py
│   ├── predict.py
│   └── utils.py
├── models/
├── checkpoints/
├── logs/
├── results/
├── notebooks/
├── docs/
├── configs/
│   └── config.py
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

## Notes

- `dataset/` is treated as read-only input.
- `processed_dataset/`, `checkpoints/`, `logs/`, `results/`, and `test_output/` are intended for generated artifacts.
- The scripts are starter entry points and should be extended with the final preprocessing policy, model architecture, and experiment logic.
