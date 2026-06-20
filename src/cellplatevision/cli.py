"""Command-line interface for CellPlateVision."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cellplatevision import __version__
from cellplatevision.config import load_settings
from cellplatevision.pipeline import DishNotFoundError, run_pipeline


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level argument parser.

    Returns:
        The configured argument parser with the ``run`` subcommand.
    """
    parser = argparse.ArgumentParser(prog="cellplatevision", description="CellPlateVision CLI")
    parser.add_argument("--version", action="version", version=f"cellplatevision {__version__}")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Analyse a dish image")
    run_parser.add_argument("--image", type=Path, required=True, help="Path to the dish image")
    run_parser.add_argument("--config", type=Path, default=None, help="Path to a config.yaml file")
    run_parser.add_argument(
        "--output", type=Path, default=None, help="Path for the annotated image"
    )
    run_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse inputs and load config without running the pipeline",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI.

    Args:
        argv: Optional argument vector (defaults to ``sys.argv``).

    Returns:
        Process exit code.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command != "run":
        parser.print_help()
        return 2
    settings = load_settings(args.config)
    if args.dry_run:
        return 0
    try:
        result = run_pipeline(args.image, settings, output_path=args.output)
    except (DishNotFoundError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"{result.label} (confluence {result.confluence * 100:.1f}%)")
    return 0
