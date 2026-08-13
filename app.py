"""CLI entry point.

Usage:
    python app.py <video_path_or_url> [options]

Examples:
    python app.py my_video.mp4
    python app.py https://www.youtube.com/watch?v=XXXX --model base
    python app.py clip.webm --format srt vtt --output-dir ./out
"""

from __future__ import annotations

import argparse
import sys

from transcript_video import __version__, engine

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="transcript-video",
        description="Extract a timestamped transcript from a local video file or YouTube URL.",
    )
    p.add_argument("source", help="Path to a local video/audio file or a YouTube URL.")
    p.add_argument("--model", default="small", help="Whisper model size: tiny/base/small/medium/large-v3 (default: small).")
    p.add_argument("--language", default=None, help="Audio language code, e.g. 'en'. Leave unset to auto-detect.")
    p.add_argument(
        "--format",
        nargs="+",
        choices=["srt", "vtt", "txt", "json"],
        default=["srt", "txt", "json"],
        help="Output formats (default: srt txt json).",
    )
    p.add_argument("--output-dir", default="./output", help="Directory for generated files (default: ./output).")
    p.add_argument("--device", choices=["cpu", "cuda"], default="cpu", help="Compute device for Whisper (default: cpu).")
    p.add_argument("--compute-type", default="int8", help="CTranslate2 compute type, e.g. int8/float16 (default: int8).")
    p.add_argument(
        "--youtube-languages",
        nargs="+",
        default=["en", "en-US", "en-GB"],
        help="Preferred YouTube transcript languages, in order (default: en en-US en-GB).",
    )
    p.add_argument(
        "--offline",
        action="store_true",
        help="Never download anything: require models already in ./models (and fail fast otherwise).",
    )
    p.add_argument("--version", action="version", version=f"transcript-video {__version__}")
    return p

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        result = engine.transcribe(
            args.source,
            model_size=args.model,
            language=args.language,
            device=args.device,
            compute_type=args.compute_type,
            languages=args.youtube_languages,
            offline=args.offline,
        )
    except engine.SourceError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # network, API, whisper errors
        print(f"error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    segments = result["segments"]
    if not segments:
        print("No segments transcribed.")
        return 1

    written = engine.save_outputs(
        segments,
        args.source,
        args.output_dir,
        args.format,
        meta={
            "source": args.source,
            "source_type": result["source_type"],
            "model": args.model,
            "language": args.language,
            "device": args.device,
        },
    )

    print(f"\nTranscribed {len(segments)} segments over {result['duration']:.1f}s of audio.")
    print(f"Source type: {result['source_type']}")
    for fmt, path in written.items():
        print(f"  {fmt.upper():4s} -> {path}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())