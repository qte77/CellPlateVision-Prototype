"""eLabFTW REST API client (implemented in M2).

Wraps the official ``elabapi-python`` SDK. Authentication uses the raw API key in
the ``Authorization`` header (NOT a ``Bearer`` prefix).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class ElabClient:
    """Minimal eLabFTW client for experiments and file uploads."""

    def __init__(self, host: str, api_key: str) -> None:
        """Store connection parameters.

        Args:
            host: Base API URL, e.g. ``http://localhost:3148/api/v2``.
            api_key: eLabFTW API key (sent raw in the ``Authorization`` header).
        """
        self._host = host
        self._api_key = api_key

    def get_experiment(self, experiment_id: int) -> dict[str, object]:
        """Fetch experiment metadata.

        Args:
            experiment_id: Target experiment id.

        Returns:
            The experiment metadata as a dictionary.

        Raises:
            NotImplementedError: Implemented in milestone M2.
        """
        raise NotImplementedError("ElabClient.get_experiment is implemented in M2")

    def patch_experiment(self, experiment_id: int, body: str) -> None:
        """Update an experiment body/metadata.

        Args:
            experiment_id: Target experiment id.
            body: New experiment body content.

        Raises:
            NotImplementedError: Implemented in milestone M2.
        """
        raise NotImplementedError("ElabClient.patch_experiment is implemented in M2")

    def upload_file(self, experiment_id: int, path: Path, comment: str) -> None:
        """Attach a file to an experiment.

        Args:
            experiment_id: Target experiment id.
            path: Path to the file to upload.
            comment: Upload comment.

        Raises:
            NotImplementedError: Implemented in milestone M2.
        """
        raise NotImplementedError("ElabClient.upload_file is implemented in M2")
