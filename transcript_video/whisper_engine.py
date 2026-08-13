from __future__ import annotations

import sys

from typing import Any, Dict, List, Optional

from . import models

def transcribe(
    audio_path: str,
    model_size: str = "small",
    language: Optional[str] = None,
    device: str = "cpu",
    compute_type: str = "int8",
    offline: bool = False,
) -> Dict[str, Any]:
    try:
        from faster_whisper import WhisperModel  # heavy import, do it lazily
    except ImportError as exc:  # friendly env hint; callers surface the message
        raise RuntimeError(
            "Missing dependency 'faster-whisper'. Install with:\n"
            "    pip install -r requirements.txt"
        ) from exc

    model_path = models.resolve(model_size, offline=offline)
    status = "cached" if models.is_cached(model_size) else "freshly downloaded"
    print(f"[whisper] Loading model '{model_size}' on {device} ({compute_type}) [{status}]...", file=sys.stderr)
    model = WhisperModel(model_path, device=device, compute_type=compute_type)

    print(f"[whisper] Transcribing {audio_path}...", file=sys.stderr)
    segments_iter, info = model.transcribe(
        audio_path,
        language=language or None,
        vad_filter=True,
        beam_size=5,
    )

    segments: List[Dict[str, Any]] = []
    for seg in segments_iter:
        text = (seg.text or "").strip()
        if not text:
            continue
        segments.append({"start": float(seg.start), "end": float(seg.end), "text": text})

    return {"segments": segments, "duration": getattr(info, "duration", 0.0) or 0.0}