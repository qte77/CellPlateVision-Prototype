"""Cell-vs-background segmentation backends.

``SegmentationBackend`` defines the interface; ``OtsuBackend`` is the default
classical backend. Cellpose and LandingLens backends are added in later milestones
and selected via configuration.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import cv2
import numpy as np
from scipy import ndimage
from skimage.filters import threshold_otsu

from cellplatevision.config import OtsuParams
from cellplatevision.imaging import to_grayscale

if TYPE_CHECKING:
    from numpy.typing import NDArray


def _remove_small_objects(mask: NDArray[np.bool_], min_size: int) -> NDArray[np.bool_]:
    """Drop connected components smaller than ``min_size`` pixels.

    Args:
        mask: Boolean foreground mask.
        min_size: Minimum component size to keep, in pixels.

    Returns:
        The mask with small components removed.
    """
    count, labeled = cv2.connectedComponents(mask.astype(np.uint8))
    if count <= 1:
        return mask
    labels = np.asarray(labeled, dtype=np.intp)
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    keep = sizes >= min_size
    return np.asarray(keep[labels], dtype=bool)


class SegmentationBackend(ABC):
    """Abstract base class for cell segmentation backends."""

    @abstractmethod
    def segment(
        self,
        image: NDArray[np.uint8],
        dish_mask: NDArray[np.bool_],
    ) -> NDArray[np.bool_]:
        """Segment cells within the dish ROI.

        Args:
            image: Grayscale or BGR image as a NumPy array.
            dish_mask: Boolean mask of the dish interior.

        Returns:
            A boolean mask where ``True`` marks pixels classified as cells.
        """

    def is_low_confidence(
        self,
        image: NDArray[np.uint8],
        dish_mask: NDArray[np.bool_],
    ) -> bool:
        """Whether the backend deems the segmentation unreliable.

        Backends may override; the default assumes the result is reliable.

        Args:
            image: Grayscale or BGR image as a NumPy array.
            dish_mask: Boolean mask of the dish interior.

        Returns:
            ``False`` by default.
        """
        return False


class OtsuBackend(SegmentationBackend):
    """Classical Otsu-threshold segmentation backend.

    Otsu thresholds the dish interior to separate cells from agar. Optional
    flat-field correction (``OtsuParams.flat_field``) divides out a blurred
    background for real images with uneven illumination; it is off by default
    because it is unnecessary (and adds edge artefacts) under even lighting.
    """

    def __init__(self, params: OtsuParams | None = None) -> None:
        """Store segmentation parameters.

        Args:
            params: Otsu parameters; defaults to :class:`OtsuParams` defaults.
        """
        self._params = params or OtsuParams()

    def _prepare(self, image: NDArray[np.uint8]) -> NDArray[np.float64]:
        """Convert to grayscale float, optionally applying flat-field correction."""
        gray = to_grayscale(image).astype(np.float64)
        if self._params.flat_field:
            background = ndimage.gaussian_filter(gray, self._params.flat_field_blur_sigma)
            return gray / (background + 1e-6)
        return gray

    def segment(
        self,
        image: NDArray[np.uint8],
        dish_mask: NDArray[np.bool_],
    ) -> NDArray[np.bool_]:
        """Segment cells via Otsu thresholding inside the dish, then clean up.

        Args:
            image: Grayscale or BGR image as a NumPy array.
            dish_mask: Boolean mask of the dish interior.

        Returns:
            A boolean cell mask.
        """
        prepared = self._prepare(image)
        values = prepared[dish_mask]
        if values.size == 0 or float(values.min()) == float(values.max()):
            return np.zeros(dish_mask.shape, dtype=bool)
        threshold = threshold_otsu(values)
        binary = (prepared > threshold) & dish_mask
        filled = np.asarray(ndimage.binary_fill_holes(binary), dtype=bool)
        return _remove_small_objects(filled, self._params.min_object_size)

    def is_low_confidence(
        self,
        image: NDArray[np.uint8],
        dish_mask: NDArray[np.bool_],
    ) -> bool:
        """Flag dishes where Otsu is unreliable (no clear bright-vs-dark split).

        Uses the relative P20-P80 intensity spread inside the dish: near-empty and
        near-confluent dishes are close to unimodal and produce a small spread.

        Args:
            image: Grayscale or BGR image as a NumPy array.
            dish_mask: Boolean mask of the dish interior.

        Returns:
            ``True`` when the dish intensity contrast is below the configured ratio.
        """
        prepared = self._prepare(image)
        values = prepared[dish_mask]
        if values.size == 0:
            return True
        low = float(np.percentile(values, 20))
        high = float(np.percentile(values, 80))
        contrast = (high - low) / (low + 1e-6)
        return bool(contrast < self._params.min_contrast_ratio)
