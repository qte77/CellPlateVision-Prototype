"""End-to-end pipeline orchestration (assembled in M3)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from cellplatevision.config import Settings


def run_pipeline(image_path: Path, settings: Settings) -> str:
    """Run detection → segmentation → confluence → classification → logging.

    Args:
        image_path: Path to the dish image to analyse.
        settings: Loaded runtime configuration.

    Returns:
        The growth-classification label for the dish.

    Raises:
        NotImplementedError: The full pipeline is assembled in milestone M3.
    """
    raise NotImplementedError("run_pipeline is assembled in M3")
