"""Project version — single source of truth is pyproject.toml's ``[project].version``."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__: str = version("cellplatevision")
except PackageNotFoundError:  # pragma: no cover - package not installed
    __version__ = "0.0.0"
