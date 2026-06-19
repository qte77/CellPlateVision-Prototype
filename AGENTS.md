# AGENTS.md

Behavioural constraints for AI agents working in this repo. Operational details
(IDs, secrets, environment quirks) belong in per-project memory, not here.

## Principles

- **KISS / DRY / YAGNI / AHA** — simplest thing that works; don't abstract early.
- Touch only code relevant to the task. Prefer reuse over new code.
- Never delete working code or tests without explicit instruction.

## Toolchain (non-negotiable)

- **uv only** — `uv sync`, `uv run <tool>`. No bare `pip`/`venv`.
- Python **3.12** (`requires-python = ">=3.12,<3.13"`).
- `src/` layout; package is `src/cellplatevision/`.

## Quality gates (must pass before every PR)

Run `make validate` (or the individual steps):

- `ruff check .` and `ruff format --check .` (line length 100, google docstrings).
- `pyright src` (basic mode) — zero errors.
- `complexipy src --max-complexity-allowed 10`.
- `pytest` — all green; default run excludes `@pytest.mark.network` tests.

## Conventions

- **pydantic** `BaseModel` for structured payloads and `pydantic-settings`
  `BaseSettings` for runtime config (env prefix `CPV_`). No `dataclass` / `TypedDict`.
- Type-only imports go under `if TYPE_CHECKING:` (the `TC` ruleset enforces this).
- Conventional Commits (`feat`, `fix`, `chore`, `docs`, `ci`, `test`, `refactor`).
- Pin every GitHub Actions `uses:` to a full commit SHA.
- Network/integration tests are marked `@pytest.mark.network` and excluded by default.

## Roadmap

See `docs/prototype-roadmap.md` for the M0–M5 milestone plan and open decisions.
