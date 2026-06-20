"""End-to-end pipeline orchestration.

Wires dish detection -> segmentation -> confluence -> classification, and
optionally writes an annotated image (dish boundary + cell overlay + confluence).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import cv2
import numpy as np
from pydantic import BaseModel

from cellplatevision.analysis import classify_growth, compute_confluence
from cellplatevision.backends import CellposeBackend, get_backend
from cellplatevision.dish_finder import ROI, SingleDishFinder, circular_mask
from cellplatevision.imaging import load_image, save_image, to_bgr
from cellplatevision.segmentation import OtsuBackend

if TYPE_CHECKING:
    from pathlib import Path

    from numpy.typing import NDArray

    from cellplatevision.config import Settings
    from cellplatevision.segmentation import SegmentationBackend


class DishNotFoundError(RuntimeError):
    """Raised when no dish can be detected in an image."""


class PipelineResult(BaseModel):
    """Outcome of analysing a single dish image.

    Attributes:
        roi: The detected dish region of interest.
        confluence: Confluence ratio in ``[0.0, 1.0]``.
        low_confidence: Whether the segmentation flagged the result as unreliable.
        label: The growth-classification label.
    """

    roi: ROI
    confluence: float
    low_confidence: bool
    label: str


def _annotate(
    image: NDArray[np.uint8],
    roi: ROI,
    cell_mask: NDArray[np.bool_],
    confluence: float,
) -> NDArray[np.uint8]:
    """Draw the dish boundary, a cell overlay, and the confluence percentage."""
    canvas = to_bgr(image).copy()
    canvas[cell_mask] = (0, 0, 255)
    cv2.circle(canvas, (roi.center_x, roi.center_y), roi.radius, (0, 255, 0), 2)
    cv2.putText(
        canvas,
        f"{confluence * 100:.1f}%",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 255),
        2,
    )
    return np.asarray(canvas, dtype=np.uint8)


def _is_low_confidence(
    backend: SegmentationBackend,
    image: NDArray[np.uint8],
    dish_mask: NDArray[np.bool_],
) -> bool:
    """Return the backend's low-confidence flag (only ``OtsuBackend`` provides one)."""
    if isinstance(backend, OtsuBackend):
        return backend.is_low_confidence(image, dish_mask)
    return False


def _segment(
    image: NDArray[np.uint8],
    dish_mask: NDArray[np.bool_],
    settings: Settings,
) -> tuple[NDArray[np.bool_], bool]:
    """Segment with the configured backend, escalating Otsu low-confidence to Cellpose.

    Args:
        image: Grayscale or BGR image as a NumPy array.
        dish_mask: Boolean mask of the dish interior.
        settings: Runtime configuration.

    Returns:
        ``(cell_mask, low_confidence)``. Escalation is a graceful no-op if Cellpose
        is not installed.
    """
    backend = get_backend(settings.backend, settings)
    cell_mask = backend.segment(image, dish_mask)
    low_confidence = _is_low_confidence(backend, image, dish_mask)
    if not (low_confidence and settings.escalate_on_low_confidence and settings.backend == "otsu"):
        return cell_mask, low_confidence
    model = settings.cellpose_model_gpu if settings.use_gpu else settings.cellpose_model
    try:
        escalated = CellposeBackend(model=model, use_gpu=settings.use_gpu).segment(image, dish_mask)
    except ImportError:
        return cell_mask, low_confidence
    return escalated, False


def run_pipeline(
    image_path: Path,
    settings: Settings,
    output_path: Path | None = None,
) -> PipelineResult:
    """Analyse a dish image end to end.

    Args:
        image_path: Path to the dish image.
        settings: Loaded runtime configuration.
        output_path: If given, write an annotated image to this path.

    Returns:
        The pipeline result (ROI, confluence, low-confidence flag, label).

    Raises:
        DishNotFoundError: If no dish is detected.
    """
    image = load_image(image_path)
    rois = SingleDishFinder(settings.hough).find_rois(image)
    if not rois:
        raise DishNotFoundError(f"no dish detected in {image_path}")
    roi = rois[0]
    dish_mask = circular_mask((image.shape[0], image.shape[1]), roi)
    cell_mask, low_confidence = _segment(image, dish_mask, settings)
    confluence = compute_confluence(cell_mask, dish_mask)
    label = classify_growth(
        confluence, settings.confluence_threshold, low_confidence=low_confidence
    )
    if output_path is not None:
        save_image(output_path, _annotate(image, roi, cell_mask, confluence))
    return PipelineResult(
        roi=roi,
        confluence=confluence,
        low_confidence=low_confidence,
        label=label,
    )
