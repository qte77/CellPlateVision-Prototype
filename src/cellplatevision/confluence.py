"""Confluence estimation: fraction of dish area covered by cells."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray


def compute_confluence(
    cell_mask: NDArray[np.bool_],
    dish_mask: NDArray[np.bool_],
) -> float:
    """Compute confluence as the ratio of cell pixels to dish pixels.

    Args:
        cell_mask: Boolean mask where ``True`` marks pixels classified as cells.
        dish_mask: Boolean mask where ``True`` marks pixels inside the dish ROI.

    Returns:
        Confluence in the range ``[0.0, 1.0]``; ``0.0`` when the dish mask is empty.

    Raises:
        ValueError: If the two masks do not share the same shape.
    """
    if cell_mask.shape != dish_mask.shape:
        raise ValueError("cell_mask and dish_mask must have the same shape")
    dish_pixels = int(np.count_nonzero(dish_mask))
    if dish_pixels == 0:
        return 0.0
    cells_in_dish = int(np.count_nonzero(cell_mask & dish_mask))
    return cells_in_dish / dish_pixels
