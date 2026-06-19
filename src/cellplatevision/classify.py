"""Growth classification from a confluence value."""

from __future__ import annotations

from typing import Literal

GrowthLabel = Literal["growing", "not_growing", "low_confidence"]


def classify_growth(
    confluence: float,
    threshold: float,
    *,
    low_confidence: bool = False,
) -> GrowthLabel:
    """Classify dish growth from a confluence ratio.

    Args:
        confluence: Confluence ratio in ``[0.0, 1.0]``.
        threshold: Minimum confluence to count as growing.
        low_confidence: If ``True``, the upstream segmentation flagged the result
            as unreliable, which overrides the threshold decision.

    Returns:
        ``"low_confidence"`` if flagged, else ``"growing"`` when confluence meets
        the threshold, else ``"not_growing"``.
    """
    if low_confidence:
        return "low_confidence"
    return "growing" if confluence >= threshold else "not_growing"
