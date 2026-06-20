"""Tests for image I/O helpers."""

from pathlib import Path

import numpy as np
import pytest

from cellplatevision.imaging import save_image


def test_save_image_raises_on_unwritable_path(tmp_path: Path) -> None:
    image = np.zeros((4, 4), dtype=np.uint8)
    target = tmp_path / "missing_dir" / "out.png"  # parent directory does not exist
    with pytest.raises(OSError, match="could not write"):
        save_image(target, image)
