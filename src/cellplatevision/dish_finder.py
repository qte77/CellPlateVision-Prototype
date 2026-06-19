"""Dish boundary detection: locate the Petri-dish ROI(s) in an image.

``DishFinder`` defines the detection interface so the single-dish (Hough) and a
future multi-well implementation are interchangeable without touching the rest of
the pipeline.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray


class ROI(BaseModel):
    """A circular region of interest describing a detected dish.

    Attributes:
        center_x: X coordinate of the dish centre, in pixels.
        center_y: Y coordinate of the dish centre, in pixels.
        radius: Dish radius, in pixels.
    """

    center_x: int = Field(ge=0)
    center_y: int = Field(ge=0)
    radius: int = Field(gt=0)


class DishFinder(ABC):
    """Abstract base class for locating dish ROIs within an image."""

    @abstractmethod
    def find_rois(self, image: NDArray[np.uint8]) -> list[ROI]:
        """Detect dish ROIs in an image.

        Args:
            image: Grayscale or BGR image as a NumPy array.

        Returns:
            A list of detected circular ROIs (possibly empty).
        """


class SingleDishFinder(DishFinder):
    """Detect a single round Petri dish via the Hough circle transform (M1)."""

    def find_rois(self, image: NDArray[np.uint8]) -> list[ROI]:
        """Detect the single dish ROI.

        Args:
            image: Grayscale or BGR image as a NumPy array.

        Returns:
            A list with the detected dish ROI.

        Raises:
            NotImplementedError: Implemented in milestone M1.
        """
        raise NotImplementedError("SingleDishFinder.find_rois is implemented in M1")
