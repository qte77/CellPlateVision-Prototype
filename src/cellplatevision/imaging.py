"""Image utilities shared across the pipeline."""

from __future__ import annotations

from typing import TYPE_CHECKING

import cv2
import numpy as np

if TYPE_CHECKING:
    from pathlib import Path

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


def to_bgr(image: NDArray[np.uint8]) -> NDArray[np.uint8]:
    """Convert a 2-D grayscale image to 3-channel BGR; pass through if already BGR.

    Args:
        image: A 2-D grayscale or 3-D BGR image.

    Returns:
        A 3-channel ``uint8`` BGR image.
    """
    if image.ndim == 2:
        return np.asarray(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR), dtype=np.uint8)
    return image


def load_image(path: Path) -> NDArray[np.uint8]:
    """Read an image from disk as a BGR array.

    Args:
        path: Path to the image file.

    Returns:
        The image as a ``uint8`` array.

    Raises:
        FileNotFoundError: If the image cannot be read.
    """
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"could not read image: {path}")
    return np.asarray(image, dtype=np.uint8)


def save_image(path: Path, image: NDArray[np.uint8]) -> None:
    """Write an image to disk.

    Args:
        path: Destination path.
        image: Image array to write.
    """
    cv2.imwrite(str(path), image)
