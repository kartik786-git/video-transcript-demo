from __future__ import annotations

import argparse
import sys

from transcript_video import models


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--size",
        nargs="+",
        choices=list(models.KNOWN_SIZES),
        default=["small"],
        help="Whisper model size(s) to download (default: small).",
    )
    args = ap.parse_args(argv)

    try:
        for size in args.size:
            dest = models.download_model(size)
            print(f"  ✓ {size} -> {dest}")
        print(f"\nDone. Models are in {models.models_dir()} and work offline with no token.")
    except Exception as exc:  # noqa: BLE001 - network errors etc.
        print(f"error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())