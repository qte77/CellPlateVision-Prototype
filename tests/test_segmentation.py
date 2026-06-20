"""Tests for Otsu segmentation and the low-confidence flag."""

import numpy as np

from cellplatevision.analysis import compute_confluence
from cellplatevision.dish_finder import SingleDishFinder, circular_mask
from cellplatevision.segmentation import OtsuBackend
from tests.generate_synthetic import generate_dish


def _dish_mask(image: np.ndarray) -> np.ndarray:
    rois = SingleDishFinder().find_rois(image)
    return circular_mask((image.shape[0], image.shape[1]), rois[0])


def test_segments_colonies_into_plausible_confluence() -> None:
    image = generate_dish(confluence=0.3, seed=1)
    mask = _dish_mask(image)
    cells = OtsuBackend().segment(image, mask)
    assert cells.shape == image.shape
    assert 0.1 < compute_confluence(cells, mask) < 0.6


def test_empty_dish_is_low_confidence() -> None:
    image = generate_dish(confluence=0.0, seed=2)
    mask = _dish_mask(image)
    assert OtsuBackend().is_low_confidence(image, mask)


def test_normal_dish_is_confident() -> None:
    image = generate_dish(confluence=0.3, seed=3)
    mask = _dish_mask(image)
    assert not OtsuBackend().is_low_confidence(image, mask)
