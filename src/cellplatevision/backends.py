"""Selectable segmentation backends and the backend factory.

``OtsuBackend`` (classical) lives in :mod:`cellplatevision.segmentation`. This module
adds the optional Cellpose (Tier 2) backend and a LandingLens stub, plus
:func:`get_backend` to choose one from configuration. Cellpose is imported lazily so
it remains an optional dependency (never required by CI).
"""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

import numpy as np

from cellplatevision.imaging import to_grayscale
from cellplatevision.segmentation import OtsuBackend, SegmentationBackend

if TYPE_CHECKING:
    from typing import Any

    from numpy.typing import NDArray

    from cellplatevision.config import Settings

_CELLPOSE_HINT = (
    "Cellpose backend requires the optional 'cellpose' dependency "
    "(install it into the project venv, e.g. `uv pip install 'cellpose>=4.2'`)."
)


class CellposeBackend(SegmentationBackend):
    """Deep-learning segmentation via Cellpose (optional, Tier 2)."""

    def __init__(self, model: str = "cyto3", *, use_gpu: bool = False) -> None:
        """Store the Cellpose model name and device choice.

        Args:
            model: Cellpose model name (``cyto3`` on CPU, ``cpsam_v2`` on GPU).
            use_gpu: Whether to run inference on the GPU.
        """
        self._model = model
        self._use_gpu = use_gpu
        self._model_obj: Any = None

    def segment(
        self,
        image: NDArray[np.uint8],
        dish_mask: NDArray[np.bool_],
    ) -> NDArray[np.bool_]:
        """Segment cells with Cellpose, intersected with the dish mask.

        The Cellpose model is loaded once (weights read from disk) and reused across
        calls.

        Args:
            image: Grayscale or BGR image as a NumPy array.
            dish_mask: Boolean mask of the dish interior.

        Returns:
            A boolean cell mask.

        Raises:
            ImportError: If the optional ``cellpose`` dependency is not installed.
        """
        if self._model_obj is None:
            try:
                cellpose_models: Any = importlib.import_module("cellpose.models")
            except ImportError as exc:
                raise ImportError(_CELLPOSE_HINT) from exc
            self._model_obj = cellpose_models.CellposeModel(
                gpu=self._use_gpu, model_type=self._model
            )
        masks = self._model_obj.eval(to_grayscale(image))[0]
        labels = np.asarray(masks, dtype=np.intp)
        return (labels > 0) & dish_mask


class LandingLensBackend(SegmentationBackend):
    """Documented optional cloud backend (LandingLens) -- not implemented.

    A clearly-marked stub: LandingLens is cloud-only, defaults to AWS US-East, and the
    free tier caps at ~1k credits/month. See ``docs/prototype-roadmap.md``.
    """

    def segment(
        self,
        image: NDArray[np.uint8],
        dish_mask: NDArray[np.bool_],
    ) -> NDArray[np.bool_]:
        """Not implemented -- LandingLens is a documented optional path only.

        Raises:
            NotImplementedError: Always.
        """
        raise NotImplementedError(
            "LandingLens backend is a documented optional path only "
            "(cloud-only, US-East default, ~1k credits/month). See docs/prototype-roadmap.md."
        )


def get_backend(name: str, settings: Settings) -> SegmentationBackend:
    """Construct a segmentation backend by name.

    Args:
        name: One of ``otsu``, ``cellpose``, ``landinglens``.
        settings: Runtime configuration.

    Returns:
        The selected segmentation backend.

    Raises:
        ValueError: If ``name`` is not a known backend.
    """
    if name == "otsu":
        return OtsuBackend(settings.otsu)
    if name == "cellpose":
        model = settings.cellpose_model_gpu if settings.use_gpu else settings.cellpose_model
        return CellposeBackend(model=model, use_gpu=settings.use_gpu)
    if name == "landinglens":
        return LandingLensBackend()
    raise ValueError(f"unknown backend: {name}")
