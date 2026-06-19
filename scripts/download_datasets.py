"""Download public Petri-dish datasets into ``data/raw/`` for parameter tuning.

Most research datasets require registration or resolve via a DOI landing page, so
this script prints where to obtain each and downloads any direct (https) zip URL
passed on the CLI::

    python scripts/download_datasets.py                 # list datasets
    python scripts/download_datasets.py <https-zip-url> [name]

See ``docs/prototype-roadmap.md`` for the full list, licenses, and links.
"""

from __future__ import annotations

import sys
from pathlib import Path

import requests

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

DATASETS = {
    "AGAR": {
        "url": "https://agar.neurosys.com/",
        "license": "CC-BY-NC 2.0",
        "note": "18k top-down Petri dish photos. Free sample + full set via registration.",
    },
    "scientific-data-2023": {
        "url": "https://www.nature.com/articles/s41597-023-02404-8",
        "license": "CC-BY 4.0",
        "note": "369 Petri-dish images, 56,865 annotated colonies (DOI landing page).",
    },
    "LIVECell": {
        "url": "https://github.com/sartorius-research/LIVECell",
        "license": "CC-BY 4.0",
        "note": "Phase-contrast cell images (cropped wells; segmentation benchmarking).",
    },
}


def print_registry():
    print(f"Datasets (download into {DATA_DIR}):\n")
    for name, meta in DATASETS.items():
        print(f"- {name} [{meta['license']}]: {meta['url']}")
        print(f"    {meta['note']}")
    print("\nTo fetch a direct zip URL: python scripts/download_datasets.py <https-url> [name]")


def download_url(url, name="dataset"):
    if not url.lower().startswith("https://"):
        raise ValueError("only https:// URLs are allowed")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    dest = DATA_DIR / f"{name}.zip"
    print(f"Downloading {url} -> {dest}")
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()
    with dest.open("wb") as handle:
        for chunk in response.iter_content(chunk_size=8192):
            handle.write(chunk)
    print("Done.")


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print_registry()
        return 0
    name = args[1] if len(args) > 1 else "dataset"
    download_url(args[0], name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
