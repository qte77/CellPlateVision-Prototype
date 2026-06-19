.SILENT:
.ONESHELL:
.PHONY: setup lint autofix check_types check_complexity lint_md test test_cov validate clean help
.DEFAULT_GOAL := help

COV_PKG := cellplatevision

setup:  ## Install toolchain and sync deps (uv)
	uv sync

lint:  ## ruff check
	uv run ruff check .

autofix:  ## ruff format + ruff check --fix
	uv run ruff format .
	uv run ruff check --fix .

check_types:  ## pyright type check (src)
	uv run pyright src

check_complexity:  ## complexipy cognitive complexity gate (max 10)
	uv run complexipy src --max-complexity-allowed 10

lint_md:  ## markdownlint (skipped if markdownlint is not installed)
	if command -v markdownlint >/dev/null 2>&1; then \
		markdownlint --config .markdownlint.json '**/*.md' --ignore '.venv/**'; \
	else \
		echo "markdownlint not installed; skipping"; \
	fi

test:  ## pytest
	uv run pytest

test_cov:  ## pytest with coverage
	uv run pytest --cov=$(COV_PKG) --cov-fail-under=0

validate:  ## CI gate: lint + format + types + complexity + tests
	set -e
	uv run ruff check .
	uv run ruff format --check .
	uv run pyright src
	uv run complexipy src --max-complexity-allowed 10
	uv run pytest --cov=$(COV_PKG) --cov-fail-under=0

clean:  ## remove tooling caches
	rm -rf .pytest_cache .ruff_cache .pyright_cache .coverage htmlcov
	find . -name "__pycache__" -type d -exec rm -rf {} +

help:  ## show available recipes
	echo "Usage: make [recipe]"
	grep -E '^[a-zA-Z0-9_-]+:.*?##' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  %-18s %s\n", $$1, $$2}'
