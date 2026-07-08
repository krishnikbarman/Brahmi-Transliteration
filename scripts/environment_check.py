"""Print a professional environment report for Brahmi model development.

This script is designed to validate the local Python and ML toolchain before
training starts.
"""

from __future__ import annotations

import platform
import sys
from pathlib import Path
from typing import Any
import os

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import PROJECT_ROOT as CONFIG_PROJECT_ROOT  # noqa: E402


def format_bytes(value: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


def safe_import(module_name: str) -> Any:
    try:
        return __import__(module_name)
    except Exception as exc:  # pragma: no cover - environment dependent
        return exc


def get_tensorflow_details() -> dict[str, Any]:
    details: dict[str, Any] = {
        "version": "Not available",
        "gpu_devices": [],
        "cuda_enabled": "Not available",
        "cudnn_version": "Not available",
    }

    try:
        import tensorflow as tf

        details["version"] = tf.__version__
        details["gpu_devices"] = [device.name for device in tf.config.list_physical_devices("GPU")]
        details["cuda_enabled"] = tf.test.is_built_with_cuda()
        build_info = tf.sysconfig.get_build_info()
        details["cudnn_version"] = build_info.get("cudnn_version", "Not reported")
        details["cuda_version"] = build_info.get("cuda_version", "Not reported")
    except Exception as exc:  # pragma: no cover - environment dependent
        details["error"] = str(exc)

    return details


def main() -> None:
    python_version = platform.python_version()
    system = platform.platform()
    cpu_name = platform.processor() or "Unavailable"

    try:
        import psutil

        virtual_memory = psutil.virtual_memory()
        cpu_physical = psutil.cpu_count(logical=False)
        cpu_logical = psutil.cpu_count(logical=True)
    except Exception:  # pragma: no cover - environment dependent
        psutil = None
        virtual_memory = None
        cpu_physical = None
        cpu_logical = os.cpu_count()

    tensorflow_details = get_tensorflow_details()
    opencv = safe_import("cv2")
    numpy = safe_import("numpy")
    pandas = safe_import("pandas")
    pillow = safe_import("PIL")
    matplotlib = safe_import("matplotlib")

    print("=" * 72)
    print("Brahmi Character Recognition - Environment Report")
    print("=" * 72)
    print(f"Project root          : {CONFIG_PROJECT_ROOT}")
    print(f"Python version        : {python_version}")
    print(f"Platform              : {system}")
    print(f"CPU                   : {cpu_name}")
    print(f"CPU cores (physical)  : {cpu_physical if cpu_physical is not None else 'Unavailable'}")
    print(f"CPU cores (logical)   : {cpu_logical if cpu_logical is not None else 'Unavailable'}")

    if virtual_memory is not None:
        print(f"RAM total             : {format_bytes(int(virtual_memory.total))}")
        print(f"RAM available         : {format_bytes(int(virtual_memory.available))}")
    else:
        print("RAM total             : Unavailable")
        print("RAM available         : Unavailable")

    print("-" * 72)
    print("Library Versions")
    print(f"TensorFlow            : {tensorflow_details.get('version')}")
    print(f"OpenCV                : {getattr(opencv, '__version__', 'Not available') if not isinstance(opencv, Exception) else 'Not available'}")
    print(f"NumPy                 : {getattr(numpy, '__version__', 'Not available') if not isinstance(numpy, Exception) else 'Not available'}")
    print(f"Pandas                : {getattr(pandas, '__version__', 'Not available') if not isinstance(pandas, Exception) else 'Not available'}")
    print(f"PIL/Pillow            : {getattr(pillow, '__version__', 'Not available') if not isinstance(pillow, Exception) else 'Not available'}")
    print(f"Matplotlib            : {getattr(matplotlib, '__version__', 'Not available') if not isinstance(matplotlib, Exception) else 'Not available'}")

    print("-" * 72)
    print("Accelerator Support")
    print(f"GPU available         : {bool(tensorflow_details.get('gpu_devices'))}")
    print(f"GPU devices           : {tensorflow_details.get('gpu_devices')}")
    print(f"CUDA enabled          : {tensorflow_details.get('cuda_enabled')}")
    print(f"CUDA version          : {tensorflow_details.get('cuda_version', 'Not reported')}")
    print(f"cuDNN version         : {tensorflow_details.get('cudnn_version')}")
    if "error" in tensorflow_details:
        print(f"TensorFlow import note: {tensorflow_details['error']}")

    print("-" * 72)
    print("Environment Status")
    print("Project root detected : Yes")
    print("Dependencies loaded   : Report complete")
    print("=" * 72)


if __name__ == "__main__":
    main()
