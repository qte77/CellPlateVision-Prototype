"""Dish boundary detection: locate the Petri-dish ROI(s) in an image.

``DishFinder`` defines the detection interface so the single-dish (Hough) and a
future multi-well implementation are interchangeable without touching the rest of
the pipeline.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import cv2
import numpy as np
from pydantic import BaseModel, Field

from cellplatevision.config import HoughParams
from cellplatevision.imaging import to_grayscale

if TYPE_CHECKING:
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


def circular_mask(shape: tuple[int, int], roi: ROI) -> NDArray[np.bool_]:
    """Build a boolean mask of the dish interior for a circular ROI.

    Args:
        shape: ``(height, width)`` of the target mask.
        roi: The circular region of interest.

    Returns:
        A boolean mask that is ``True`` inside the ROI circle.
    """
    height, width = shape
    rows, cols = np.ogrid[:height, :width]
    distance_sq = (cols - roi.center_x) ** 2 + (rows - roi.center_y) ** 2
    return distance_sq <= roi.radius**2


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
    """Detect a single round Petri dish via the Hough circle transform."""

    def __init__(self, params: HoughParams | None = None) -> None:
        """Store detection parameters.

        Args:
            params: Hough parameters; defaults to :class:`HoughParams` defaults.
        """
        self._params = params or HoughParams()

    def find_rois(self, image: NDArray[np.uint8]) -> list[ROI]:
        """Detect the single dish ROI via Hough, falling back to contours.

        Args:
            image: Grayscale or BGR image as a NumPy array.

        Returns:
            A list with the detected dish ROI, or empty if none is found.
        """
        gray = to_grayscale(image)
        blurred = np.asarray(cv2.GaussianBlur(gray, (9, 9), 2), dtype=np.uint8)
        roi = self._detect_hough(blurred) or self._detect_contour(gray)
        return [roi] if roi is not None else []

    def _detect_hough(self, gray: NDArray[np.uint8]) -> ROI | None:
        """Run the Hough circle transform and return the strongest circle."""
        half = min(gray.shape[0], gray.shape[1]) / 2.0
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=self._params.dp,
            minDist=self._params.min_dist,
            param1=self._params.param1,
            param2=self._params.param2,
            minRadius=int(self._params.min_radius_ratio * half),
            maxRadius=int(self._params.max_radius_ratio * half),
        )
        if circles is None:
            return None
        x, y, radius = circles[0][0]
        return ROI(center_x=int(x), center_y=int(y), radius=int(radius))

    def _detect_contour(self, gray: NDArray[np.uint8]) -> ROI | None:
        """Fallback: enclose the largest Otsu foreground contour in a circle."""
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
        largest = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(largest)
        if int(radius) <= 0:
            return None
        return ROI(center_x=int(x), center_y=int(y), radius=int(radius))
