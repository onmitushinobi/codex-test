#!/usr/bin/env python3
"""Batch resize JPG images to 1536x1024 with sequential file names."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError


DEFAULT_WIDTH = 1536
DEFAULT_HEIGHT = 1024


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert JPG/JPEG files from an input directory into fixed-size JPG files "
            "with sequential names."
        )
    )
    parser.add_argument("--input", default="images", help="Input directory (default: images)")
    parser.add_argument("--output", default="out", help="Output directory (default: out)")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH, help=f"Output width (default: {DEFAULT_WIDTH})")
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT, help=f"Output height (default: {DEFAULT_HEIGHT})")
    parser.add_argument(
        "--start-number",
        type=int,
        default=1,
        help="Starting number for sequential filenames (default: 1)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be processed without writing files",
    )
    return parser.parse_args()


def collect_images(input_dir: Path) -> list[Path]:
    patterns = ("*.jpg", "*.jpeg", "*.JPG", "*.JPEG")
    files: list[Path] = []
    for pattern in patterns:
        files.extend(input_dir.glob(pattern))
    return sorted(set(files), key=lambda p: p.name.lower())


def make_output_name(index: int) -> str:
    return f"{index:04d}.jpg"


def process_image(src: Path, dst: Path, width: int, height: int) -> None:
    with Image.open(src) as img:
        rgb = img.convert("RGB")
        fitted = ImageOps.fit(rgb, (width, height), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
        fitted.save(dst, format="JPEG", quality=95, optimize=True)


def main() -> int:
    args = parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if args.width <= 0 or args.height <= 0:
        print("[ERROR] --width and --height must be positive integers.", file=sys.stderr)
        return 2

    if args.start_number <= 0:
        print("[ERROR] --start-number must be a positive integer.", file=sys.stderr)
        return 2

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"[ERROR] Input directory not found: {input_dir}", file=sys.stderr)
        print("[FIX] Create the folder or use --input to point to an existing directory.", file=sys.stderr)
        return 1

    images = collect_images(input_dir)
    if not images:
        print(f"[ERROR] No JPG/JPEG files found in: {input_dir}", file=sys.stderr)
        print("[FIX] Put .jpg/.jpeg files in the folder or check --input path.", file=sys.stderr)
        return 1

    print(f"Found {len(images)} image(s) in {input_dir}")
    if args.dry_run:
        print("[DRY-RUN] No files will be written.")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)

    success = 0
    failures = 0

    for offset, src in enumerate(images):
        output_name = make_output_name(args.start_number + offset)
        dst = output_dir / output_name

        if args.dry_run:
            print(f"[PLAN] {src} -> {dst}")
            success += 1
            continue

        try:
            process_image(src, dst, args.width, args.height)
            print(f"[OK] {src} -> {dst}")
            success += 1
        except (UnidentifiedImageError, OSError) as err:
            failures += 1
            print(f"[ERROR] Failed: {src}", file=sys.stderr)
            print(f"[CAUSE] {err}", file=sys.stderr)
            print(
                "[FIX] Ensure the file is a valid JPG/JPEG and not locked by another application.",
                file=sys.stderr,
            )

    print(f"Done. success={success}, failed={failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
