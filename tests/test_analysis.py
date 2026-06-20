"""Tests for confluence computation and growth classification."""

import numpy as np
import pytest

from cellplatevision.analysis import classify_growth, compute_confluence


def test_confluence_ratio() -> None:
    dish = np.ones((10, 10), dtype=bool)
    cells = np.zeros((10, 10), dtype=bool)
    cells[:5, :] = True
    assert compute_confluence(cells, dish) == 0.5


def test_confluence_empty_dish_returns_zero() -> None:
    dish = np.zeros((10, 10), dtype=bool)
    cells = np.ones((10, 10), dtype=bool)
    assert compute_confluence(cells, dish) == 0.0


def test_confluence_ignores_cells_outside_dish() -> None:
    dish = np.zeros((10, 10), dtype=bool)
    dish[:, :5] = True
    cells = np.zeros((10, 10), dtype=bool)
    cells[:, 5:] = True
    assert compute_confluence(cells, dish) == 0.0


def test_confluence_shape_mismatch_raises() -> None:
    with pytest.raises(ValueError, match="same shape"):
        compute_confluence(np.ones((4, 4), dtype=bool), np.ones((5, 5), dtype=bool))


def test_classify_threshold_is_inclusive() -> None:
    assert classify_growth(0.2, 0.2) == "growing"
    assert classify_growth(0.19, 0.2) == "not_growing"


def test_classify_low_confidence_overrides_threshold() -> None:
    assert classify_growth(0.9, 0.2, low_confidence=True) == "low_confidence"


def test_classify_rejects_out_of_range_confluence() -> None:
    with pytest.raises(ValueError, match="confluence"):
        classify_growth(1.5, 0.2)
    with pytest.raises(ValueError, match="confluence"):
        classify_growth(-0.1, 0.2)
