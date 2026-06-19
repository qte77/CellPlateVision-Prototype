"""Cell-vs-background segmentation backends.

``SegmentationBackend`` defines the interface; ``OtsuBackend`` is the default
classical backend (implemented in M1). Cellpose and LandingLens backends are added
in later milestones and selected via configuration.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray


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


class OtsuBackend(SegmentationBackend):
    """Classical Otsu-threshold segmentation backend (implemented in M1)."""

    def segment(
        self,
        image: NDArray[np.uint8],
        dish_mask: NDArray[np.bool_],
    ) -> NDArray[np.bool_]:
        """Segment cells via flat-field correction and Otsu thresholding.

        Args:
            image: Grayscale or BGR image as a NumPy array.
            dish_mask: Boolean mask of the dish interior.

        Returns:
            A boolean cell mask.

        Raises:
            NotImplementedError: Implemented in milestone M1.
        """
        raise NotImplementedError("OtsuBackend.segment is implemented in M1")
