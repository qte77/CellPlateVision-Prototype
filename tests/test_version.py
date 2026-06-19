"""Smoke test for package import and version metadata."""

from cellplatevision import __version__


def test_version_is_nonempty() -> None:
    assert isinstance(__version__, str)
    assert __version__
