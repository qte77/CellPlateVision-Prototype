"""Tests for the segmentation backend factory and optional backends."""

import importlib.util

import numpy as np
import pytest

from cellplatevision.backends import CellposeBackend, LandingLensBackend, get_backend
from cellplatevision.config import Settings
from cellplatevision.segmentation import OtsuBackend

cellpose_installed = importlib.util.find_spec("cellpose") is not None


def test_get_backend_otsu() -> None:
    assert isinstance(get_backend("otsu", Settings()), OtsuBackend)


def test_get_backend_landinglens() -> None:
    assert isinstance(get_backend("landinglens", Settings()), LandingLensBackend)


def test_get_backend_unknown_raises() -> None:
    with pytest.raises(ValueError, match="unknown backend"):
        get_backend("nope", Settings())


def test_landinglens_segment_not_implemented() -> None:
    image = np.zeros((4, 4), dtype=np.uint8)
    dish_mask = np.ones((4, 4), dtype=bool)
    with pytest.raises(NotImplementedError, match="LandingLens"):
        LandingLensBackend().segment(image, dish_mask)


@pytest.mark.skipif(cellpose_installed, reason="cellpose installed; ImportError path moot")
def test_cellpose_segment_requires_dependency() -> None:
    image = np.zeros((4, 4), dtype=np.uint8)
    dish_mask = np.ones((4, 4), dtype=bool)
    with pytest.raises(ImportError, match="cellpose"):
        CellposeBackend().segment(image, dish_mask)
