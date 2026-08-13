from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

def fmt_ts(seconds: float, sep: str = ",") -> str:
    ms = int(round(max(0.0, seconds) * 1000))
    hours, rem = divmod(ms, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, msecs = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}{sep}{msecs:03d}"

def to_srt(segments: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    for i, seg in enumerate(segments, 1):
        lines.append(str(i))
        lines.append(f"{fmt_ts(seg['start'])} --> {fmt_ts(seg['end'])}")
        lines.append(seg["text"].strip())
        lines.append("")
    return "\n".join(lines)

def to_vtt(segments: List[Dict[str, Any]]) -> str:
    lines: List[str] = ["WEBVTT", ""]
    for seg in segments:
        lines.append(f"{fmt_ts(seg['start'], '.')} --> {fmt_ts(seg['end'], '.')}")
        lines.append(seg["text"].strip())
        lines.append("")
    return "\n".join(lines)   

def to_txt(segments: List[Dict[str, Any]]) -> str:
    lines = []
    for seg in segments:
        lines.append(f"[{fmt_ts(seg['start'])} --> {fmt_ts(seg['end'])}] {seg['text'].strip()}")
    return "\n".join(lines)

def to_json(segments: List[Dict[str, Any]], meta: Dict[str, Any] | None = None) -> str:
    return json.dumps(
        {"meta": meta or {}, "segments": segments},
        ensure_ascii=False,
        indent=2,
    )


WRITERS = {
    "srt": to_srt,
    "vtt": to_vtt,
    "txt": to_txt,
    "json": to_json,
}


def write_outputs(
    segments: List[Dict[str, Any]],
    base_name: str,
    output_dir: str | os.PathLike[str],
    formats: List[str],
    meta: Dict[str, Any] | None = None,
) -> Dict[str, Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    safe_base = "".join(c if c.isalnum() or c in "-_." else "_" for c in base_name) or "transcript"
    written: Dict[str, Path] = {}
    for fmt in formats:
        writer = WRITERS.get(fmt.lower())
        if writer is None:
            continue
        path = out / f"{safe_base}.{fmt.lower()}"
        content = writer(segments, meta) if fmt.lower() == "json" else writer(segments)
        path.write_text(content, encoding="utf-8")
        written[fmt.lower()] = path
    return written
