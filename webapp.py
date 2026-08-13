from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from transcript_video import engine, models
from transcript_video.outputs import to_json, to_srt, to_txt, to_vtt

st.set_page_config(page_title="Transcript Video", page_icon="🎬", layout="wide")
st.title("🎬 Video Transcript Extractor")
st.caption("Extract a timestamped transcript from a local video file or a YouTube URL.")

MODELS = ["tiny", "base", "small", "medium", "large-v3"]
FORMATS = ["srt", "vtt", "txt", "json"]

with st.sidebar:
    st.header("Settings")
    model_size = st.selectbox("Whisper model", MODELS, index=MODELS.index("small"))
    if models.is_cached(model_size):
        st.caption(f"✓ '{model_size}' downloaded locally")
    else:
        st.caption(f"⚠ '{model_size}' not downloaded yet — first use fetches it once, then it works offline.")
        if st.button(f"Download '{model_size}' now", key="dl_model", help="Saved into ./models; progress bar appears in the server terminal."):
            with st.status(f"Downloading '{model_size}'...", expanded=True) as status:
                models.download_model(model_size)
                status.update(label=f"'{model_size}' downloaded", state="complete")
            st.rerun()
    device = st.radio("Device", ["cpu", "cuda"], horizontal=True)
    language = st.text_input("Language (leave empty for auto-detect)", value="")
    youtube_langs = st.text_input("YouTube transcript languages (comma-separated)", value="en,en-US,en-GB")
    offline = st.checkbox("Offline mode (no network)", value=False, help="Fail fast instead of downloading if a model is missing.")

source_mode = st.radio("Input type", ["YouTube URL", "Upload file"], horizontal=True)

source: str | None = None
uploaded_bytes_path: str | None = None

if source_mode == "YouTube URL":
    url = st.text_input("Paste a YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    source = url or None
else:
    uploaded = st.file_uploader(
        "Choose a video or audio file",
        type=["mp4", "webm", "mkv", "mov", "avi", "m4a", "mp3", "wav", "ogg"],
    )
    if uploaded is not None:
        # faster-whisper reads from a path, so persist the upload to a temp file.
        # Stream in chunks so huge files don't balloon RAM (no getvalue()).
        suffix = Path(uploaded.name).suffix or ".mp4"
        tmp = Path(tempfile.gettempdir()) / f"tv_upload_{os.urandom(4).hex()}{suffix}"
        with tmp.open("wb") as out:
            shutil.copyfileobj(uploaded, out, 1024 * 1024)
        uploaded_bytes_path = str(tmp)
        source = uploaded_bytes_path
        size_mb = (uploaded.size or 0) / 1024 / 1024
        st.success(f"Uploaded {uploaded.name} ({size_mb:.1f} MB)")

transcribe_clicked = st.button("Transcribe", type="primary", disabled=not source)

if transcribe_clicked:
    try:
        with st.spinner("Transcribing — the first run downloads the Whisper model, this can take a while..."):
            result = engine.transcribe(
                source,
                model_size=model_size,
                language=language.strip() or None,
                device=device,
                compute_type="int8",
                languages=[x.strip() for x in youtube_langs.split(",") if x.strip()],
                offline=offline,
            )
        st.session_state["segments"] = result["segments"]
        st.session_state["base_name"] = (
            Path(uploaded.name).stem
            if source_mode == "Upload file"
            else engine.base_name_for(source)
        )
        st.session_state["meta"] = {
            "source": source,
            "source_type": result["source_type"],
            "model": model_size,
            "device": device,
            "language": language.strip() or None,
        }
    except Exception as exc:  # noqa: BLE001 - surface failures in the UI
        st.error(f"Transcription failed: {type(exc).__name__}: {exc}")
    finally:
        if uploaded_bytes_path and Path(uploaded_bytes_path).exists():
            Path(uploaded_bytes_path).unlink(missing_ok=True)

segments = st.session_state.get("segments")

if segments:
    st.subheader(f"Transcript — {len(segments)} segments")

    table = pd.DataFrame(
        [
            {"Start": f"{s['start']:08.3f}", "End": f"{s['end']:08.3f}", "Text": s["text"]}
            for s in segments
        ]
    )
    st.dataframe(table, use_container_width=True, hide_index=True)

    st.markdown("### Download")
    stem = st.session_state.get("base_name", "transcript")
    meta = st.session_state.get("meta", {})
    payloads = {
        "srt": to_srt(segments),
        "vtt": to_vtt(segments),
        "txt": to_txt(segments),
        "json": to_json(segments, meta),
    }
    mimes = {
        "srt": "application/x-subrip",
        "vtt": "text/vtt",
        "txt": "text/plain",
        "json": "application/json",
    }
    cols = st.columns(len(FORMATS))
    for col, fmt in zip(cols, FORMATS):
        col.download_button(
            label=f"Download .{fmt}",
            data=payloads[fmt],
            file_name=f"{stem}.{fmt}",
            mime=mimes[fmt],
        )

