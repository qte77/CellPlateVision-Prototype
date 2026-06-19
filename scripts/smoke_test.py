"""Smoke-test the pipeline over local images in data/raw/.

Usage:
    python scripts/smoke_test.py [image_dir]

Prints confluence and label per image and writes annotated_<name>.png alongside
each source image. Processes at most the first 20 images found.
"""

from __future__ import annotations

import sys
from pathlib import Path

from cellplatevision.config import load_settings
from cellplatevision.pipeline import DishNotFoundError, run_pipeline

LIMIT = 20
SUFFIXES = {".png", ".jpg", ".jpeg", ".tif", ".tiff"}


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    image_dir = Path(args[0]) if args else Path("data/raw")
    settings = load_settings(Path("config.yaml"))
    images = sorted(p for p in image_dir.rglob("*") if p.suffix.lower() in SUFFIXES)
    if not images:
        print(f"no images found under {image_dir}")
        return 0
    if len(images) > LIMIT:
        print(f"found {len(images)} images; processing the first {LIMIT}")
    for image_path in images[:LIMIT]:
        annotated = image_path.with_name(f"annotated_{image_path.name}")
        try:
            result = run_pipeline(image_path, settings, output_path=annotated)
        except DishNotFoundError as exc:
            print(f"{image_path.name}: {exc}")
            continue
        print(f"{image_path.name}: {result.label} ({result.confluence * 100:.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
