from __future__ import annotations

import logging
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODELS_DIR = PROJECT_ROOT / "models"

REPO_PREFIX = "Systran/faster-whisper-"
KNOWN_SIZES = ("tiny", "base", "small", "medium", "large-v3")

def _quiet_hf() -> None:
    os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
    os.environ.setdefault("HF_HUB_DISABLE_IMPLICIT_TOKEN", "1")
    logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

_quiet_hf()

def models_dir() -> Path:
    return Path(os.environ.get("TV_MODELS_DIR", str(DEFAULT_MODELS_DIR)))

def model_path(size: str) -> Path:
    return models_dir() / f"faster-whisper-{size}"

def is_cached(size: str) -> bool:
    return (model_path(size) / "model.bin").is_file()

def download_model(size: str) -> Path:
    from huggingface_hub import snapshot_download  # local import: heavy, opt-in

    size = size.lower()
    if size not in KNOWN_SIZES:
        raise ValueError(f"Unknown model size {size!r}; choose from {', '.join(KNOWN_SIZES)}")

    dest = model_path(size)
    dest.mkdir(parents=True, exist_ok=True)
    print(f"[model] Downloading '{size}' into {dest} ... (no token needed; progress bar below)", flush=True)
    snapshot_download(repo_id=f"{REPO_PREFIX}{size}", local_dir=str(dest))

def resolve(size: str, offline: bool = False) -> str:
    size = size.lower()
    if is_cached(size):
        return str(model_path(size))

    if offline:
        raise RuntimeError(
            f"Model '{size}' isn't downloaded and offline mode is on.\n"
            f"Run once with internet, then it works forever offline:\n"
            f"    python download_model.py --size {size}"
        )

    download_model(size)
    return str(model_path(size))
