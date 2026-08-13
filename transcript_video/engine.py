from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import whisper_engine, youtube
from .outputs import write_outputs

# Raised when the given source cannot be transcribed.
class SourceError(RuntimeError):
    pass

def is_url(source: str) -> bool:
    return source.lower().startswith(("http://", "https://"))

def base_name_for(source: str) -> str:
    if is_url(source):
        video_id = youtube.extract_video_id(source)
        return video_id or "video"
    return Path(source).stem

def transcribe(
    source: str,
    model_size: str = "small",
    language: Optional[str] = None,
    device: str = "cpu",
    compute_type: str = "int8",
    languages: Optional[List[str]] = None,
    offline: bool = False,
) -> Dict[str, Any]:
    if is_url(source):
        return _transcribe_url(source, model_size, language, device, compute_type, languages, offline)
    return _transcribe_file(source, model_size, language, device, compute_type, offline)

def _transcribe_file(
    path: str,
    model_size: str,
    language: Optional[str],
    device: str,
    compute_type: str,
    offline: bool,
) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise SourceError(f"File not found: {p}")
    result = whisper_engine.transcribe(str(p), model_size, language, device, compute_type, offline)
    result["source_type"] = "file"
    return result

def _transcribe_url(
    url: str,
    model_size: str,
    language: Optional[str],
    device: str,
    compute_type: str,
    languages: Optional[List[str]],
    offline: bool,
) -> Dict[str, Any]:
    print("[youtube] Trying native transcript...", flush=True)
    native = youtube.transcript_from_youtube(url, languages)
    if native:
        print("[youtube] Native transcript found. Skipping Whisper.", flush=True)
        return {"segments": native["segments"], "duration": _estimate_duration(native["segments"]), "source_type": "youtube"}

    print("[youtube] No native transcript; downloading audio for Whisper...", flush=True)
    tmp = tempfile.mkdtemp(prefix="transcript_tmp_")
    try:
        audio = youtube.download_audio(url, tmp_dir=tmp)
        result = whisper_engine.transcribe(audio, model_size, language, device, compute_type, offline)
        result["source_type"] = "youtube"
        return result
    finally:
        import shutil

        shutil.rmtree(tmp, ignore_errors=True)

def _estimate_duration(segments: List[Dict[str, Any]]) -> float:
    return max((s["end"] for s in segments), default=0.0)

def save_outputs(
    segments: List[Dict[str, Any]],
    source: str,
    output_dir: str,
    formats: List[str],
    meta: Optional[Dict[str, Any]] = None,
) -> Dict[str, Path]:
    return write_outputs(segments, base_name_for(source), output_dir, formats, meta=meta)