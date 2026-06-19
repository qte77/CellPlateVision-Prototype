"""Tests for the eLabFTW client.

The wiring tests run offline (the SDK constructs its client without any network
call). The round-trip test is marked ``network`` and excluded by default; run it
against a local eLabFTW instance with ``uv run pytest -m network`` and
``CPV_ELABFTW_API_KEY`` set (see docker-compose.dev.yml).
"""

import os

import pytest

from cellplatevision.elab_client import ElabClient


def test_authorization_header_is_raw_key() -> None:
    client = ElabClient(host="http://localhost:3148/api/v2", api_key="abc123")
    headers = client._api_client.default_headers
    assert headers["Authorization"] == "abc123"  # raw key, NOT "Bearer abc123"


def test_get_experiment_returns_dict(monkeypatch: pytest.MonkeyPatch) -> None:
    client = ElabClient(host="http://localhost:3148/api/v2", api_key="k")
    monkeypatch.setattr(
        client._experiments, "get_experiment", lambda _id: {"id": 7, "title": "demo"}
    )
    assert client.get_experiment(7) == {"id": 7, "title": "demo"}


def test_patch_experiment_passes_body(monkeypatch: pytest.MonkeyPatch) -> None:
    client = ElabClient(host="http://localhost:3148/api/v2", api_key="k")
    captured: dict[str, object] = {}

    def fake_patch(body: dict[str, object], id: int) -> None:
        captured["body"] = body
        captured["id"] = id

    monkeypatch.setattr(client._experiments, "patch_experiment", fake_patch)
    client.patch_experiment(3, "new body")
    assert captured == {"body": {"body": "new body"}, "id": 3}


@pytest.mark.network
def test_experiment_roundtrip() -> None:
    api_key = os.environ.get("CPV_ELABFTW_API_KEY", "")
    if not api_key:
        pytest.skip("CPV_ELABFTW_API_KEY not set")
    host = os.environ.get("CPV_ELABFTW_HOST", "http://localhost:3148/api/v2")
    client = ElabClient(host, api_key)
    experiment = client.get_experiment(1)
    assert "id" in experiment
