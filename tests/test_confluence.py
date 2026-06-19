"""Tests for confluence computation."""

import numpy as np
import pytest

from cellplatevision.confluence import compute_confluence


def test_full_confluence() -> None:
    dish = np.ones((10, 10), dtype=bool)
    cells = np.ones((10, 10), dtype=bool)
    assert compute_confluence(cells, dish) == 1.0


def test_half_confluence() -> None:
    dish = np.ones((10, 10), dtype=bool)
    cells = np.zeros((10, 10), dtype=bool)
    cells[:5, :] = True
    assert compute_confluence(cells, dish) == 0.5


def test_empty_dish_returns_zero() -> None:
    dish = np.zeros((10, 10), dtype=bool)
    cells = np.ones((10, 10), dtype=bool)
    assert compute_confluence(cells, dish) == 0.0


def test_cells_outside_dish_are_ignored() -> None:
    dish = np.zeros((10, 10), dtype=bool)
    dish[:, :5] = True
    cells = np.zeros((10, 10), dtype=bool)
    cells[:, 5:] = True
    assert compute_confluence(cells, dish) == 0.0


def test_shape_mismatch_raises() -> None:
    with pytest.raises(ValueError, match="same shape"):
        compute_confluence(np.ones((4, 4), dtype=bool), np.ones((5, 5), dtype=bool))
