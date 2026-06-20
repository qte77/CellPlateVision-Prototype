"""Benchmark segmentation backends (Otsu vs Cellpose) over data/raw/ images.

Usage:
    python scripts/benchmark_backends.py [image_dir]

Writes <image_dir>/benchmark.csv with confluence per backend. Cellpose cells are left
blank unless the optional 'cellpose' dependency is installed. Processes the first 50
images found. Not run in CI (dataset- and cellpose-gated).
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

from cellplatevision.analysis import compute_confluence
from cellplatevision.backends import get_backend
from cellplatevision.config import load_settings
from cellplatevision.dish_finder import SingleDishFinder, circular_mask
from cellplatevision.imaging import load_image

LIMIT = 50
SUFFIXES = {".png", ".jpg", ".jpeg", ".tif", ".tiff"}


def _confluence_for(name, image, dish_mask, settings):
    try:
        mask = get_backend(name, settings).segment(image, dish_mask)
    except (ImportError, NotImplementedError):
        return ""
    return f"{compute_confluence(mask, dish_mask):.4f}"


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    image_dir = Path(args[0]) if args else Path("data/raw")
    settings = load_settings(Path("config.yaml"))
    images = sorted(p for p in image_dir.rglob("*") if p.suffix.lower() in SUFFIXES)[:LIMIT]
    if not images:
        print(f"no images found under {image_dir}")
        return 0
    finder = SingleDishFinder(settings.hough)
    out = image_dir / "benchmark.csv"
    with out.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["image", "otsu", "cellpose"])
        for path in images:
            image = load_image(path)
            rois = finder.find_rois(image)
            if not rois:
                writer.writerow([path.name, "", ""])
                continue
            dish_mask = circular_mask((image.shape[0], image.shape[1]), rois[0])
            writer.writerow(
                [
                    path.name,
                    _confluence_for("otsu", image, dish_mask, settings),
                    _confluence_for("cellpose", image, dish_mask, settings),
                ]
            )
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
