"""Tests for dish detection."""

import numpy as np

from cellplatevision.dish_finder import ROI, SingleDishFinder, circular_mask
from tests.generate_synthetic import generate_dish


def test_detects_single_dish() -> None:
    image = generate_dish(size=512, dish_radius=220, confluence=0.3, seed=0)
    rois = SingleDishFinder().find_rois(image)
    assert len(rois) == 1
    roi = rois[0]
    assert abs(roi.radius - 220) < 35
    assert abs(roi.center_x - 256) < 35
    assert abs(roi.center_y - 256) < 35


def test_circular_mask_area_matches_radius() -> None:
    roi = ROI(center_x=50, center_y=50, radius=20)
    mask = circular_mask((100, 100), roi)
    expected = np.pi * 20**2
    assert abs(int(mask.sum()) - expected) < 100
