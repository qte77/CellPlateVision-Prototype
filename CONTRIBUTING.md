# Contributing

## Development setup

This project uses [uv](https://docs.astral.sh/uv/). Python 3.12 is required.

```bash
uv sync          # create .venv and install runtime + dev + test deps
```

## Quality gates

All of these must pass before opening a PR (CI runs the same via
`.github/workflows/validate.yaml`):

```bash
make validate    # ruff + format check + pyright + complexipy + pytest
```

Or individually:

```bash
make lint              # ruff check
make autofix           # ruff format + ruff check --fix
make check_types       # pyright src
make check_complexity  # complexipy (max 10)
make test              # pytest (excludes network tests)
```

`make lint_md` runs markdownlint if it is installed (Node tool, not part of CI).

## Tests

- Unit tests run fully offline against synthetic fixtures
  (`tests/generate_synthetic.py`).
- Tests needing network or a local eLabFTW instance are marked
  `@pytest.mark.network` and excluded by default. Run them with `uv run pytest -m network`.

## Commits and PRs

- Use [Conventional Commits](https://www.conventionalcommits.org/)
  (`feat`, `fix`, `chore`, `docs`, `ci`, `test`, `refactor`).
- Keep commits scoped by topic.
- PRs are squash-merged into `main`.

## Conventions

See [AGENTS.md](AGENTS.md) for the full list. Highlights: `src/` layout, uv-only,
pydantic for config/payloads, type-only imports under `TYPE_CHECKING`, and
SHA-pinned GitHub Actions.
