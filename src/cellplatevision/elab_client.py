"""eLabFTW REST API client.

Wraps the official ``elabapi-python`` SDK (API v2). Authentication uses the raw API
key in the ``Authorization`` header (NOT a ``Bearer`` prefix).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import elabapi_python

if TYPE_CHECKING:
    from pathlib import Path


class ElabClient:
    """Minimal eLabFTW client for experiments and file uploads."""

    def __init__(self, host: str, api_key: str) -> None:
        """Configure the SDK client.

        Args:
            host: Base API URL, e.g. ``http://localhost:3148/api/v2``.
            api_key: eLabFTW API key, sent raw in the ``Authorization`` header.
        """
        configuration = elabapi_python.Configuration()
        configuration.host = host
        self._api_client = elabapi_python.ApiClient(configuration)
        self._api_client.set_default_header("Authorization", api_key)
        self._experiments = elabapi_python.ExperimentsApi(self._api_client)
        self._uploads = elabapi_python.UploadsApi(self._api_client)

    def get_experiment(self, experiment_id: int) -> dict[str, object]:
        """Fetch experiment metadata.

        Args:
            experiment_id: Target experiment id.

        Returns:
            The experiment metadata as a dictionary.
        """
        experiment = self._experiments.get_experiment(experiment_id)
        data = self._api_client.sanitize_for_serialization(experiment)
        return dict(data) if isinstance(data, dict) else {"value": data}

    def patch_experiment(self, experiment_id: int, body: str) -> None:
        """Update an experiment's body text.

        Args:
            experiment_id: Target experiment id.
            body: New experiment body content.
        """
        self._experiments.patch_experiment(body={"body": body}, id=experiment_id)

    def upload_file(self, experiment_id: int, path: Path, comment: str) -> None:
        """Attach a file to an experiment.

        Args:
            experiment_id: Target experiment id.
            path: Path to the file to upload.
            comment: Upload comment.
        """
        self._uploads.post_upload("experiments", experiment_id, file=str(path), comment=comment)
