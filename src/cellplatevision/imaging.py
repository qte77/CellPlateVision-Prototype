"""Image utilities shared across the pipeline."""

from __future__ import annotations

from typing import TYPE_CHECKING

import cv2
import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray


def to_grayscale(image: NDArray[np.uint8]) -> NDArray[np.uint8]:
    """Convert a BGR image to grayscale; pass through if already 2-D.

    Args:
        image: A 2-D grayscale or 3-D BGR image.

    Returns:
        A 2-D ``uint8`` grayscale image.
    """
    if image.ndim == 3:
        return np.asarray(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), dtype=np.uint8)
    return image
