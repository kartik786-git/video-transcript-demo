from __future__ import annotations

import re
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

VIDEO_ID_RE = re.compile(r"(?:v=|youtu\.be/|shorts/|embed/|live/)([A-Za-z0-9_-]{11})")


def extract_video_id(url: str) -> Optional[str]:
    match = VIDEO_ID_RE.search(url)
    return match.group(1) if match else None

def transcript_from_youtube(url: str, languages: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
    languages = languages or ["en", "en-US", "en-GB"]
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError(f"Could not parse a YouTube video ID from: {url}")

    from youtube_transcript_api import YouTubeTranscriptApi, YouTubeTranscriptApiException

    try:
        if hasattr(YouTubeTranscriptApi, "get_transcript"):
            # Legacy classmethod API
            raw = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        else:
            # Modern instance API
            raw = YouTubeTranscriptApi().fetch(video_id, languages=languages).to_raw_data()
    except YouTubeTranscriptApiException:
        # Any "this video has no usable transcript" case -> try Whisper instead.
        return None

    segments = [
        {
            "start": float(item["start"]),
            "end": float(item["start"] + item["duration"]),
            "text": (item.get("text") or "").strip(),
        }
        for item in raw
        if item.get("text", "").strip()
    ]
    return {"segments": segments, "title": video_id}

def download_audio(url: str, tmp_dir: Optional[str] = None, force_wav: bool = False) -> str:
    import yt_dlp

    workdir = Path(tmp_dir) if tmp_dir else Path(tempfile.mkdtemp(prefix="ytaudio_"))
    workdir.mkdir(parents=True, exist_ok=True)

    opts: Dict[str, Any] = {
        "format": "bestaudio/best",
        "outtmpl": str(workdir / "%(id)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "paths": {"home": str(workdir)},
    }
    if force_wav:
        opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "0",
            }
        ]

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)

    video_id = info.get("id")
    if not video_id:
        raise RuntimeError("yt-dlp returned no video ID")

    candidates = list(workdir.glob(f"{video_id}.*"))
    if not candidates:
        raise RuntimeError(f"yt-dlp downloaded nothing for {video_id}")

    # Prefer a transcoded .wav over the raw stream when both exist.
    wav = next((c for c in candidates if c.suffix.lower() == ".wav"), None)
    return str(wav if wav else candidates[0])