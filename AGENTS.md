# AGENTS.md

Structured process logger — distribution `entirius-py-process-logger`, import `process_logger`.

## Commands

| Command | Meaning |
|---|---|
| `make install` | sync dependencies (uv, incl. extras) |
| `make check` | lint + format-check (ruff) |
| `make fix` | auto-fix lint + format |
| `make test` | test suite (pytest) |

## Conventions

- English only: code, docs, commits, branches, PRs.
- MPL-2.0: every non-trivial source file carries the license header (pre-commit inserts it).
- Toolchain: uv + ruff + hatchling + pytest; all config in `pyproject.toml`; `uv.lock` committed.
- Git flow: `master` (production) + `develop` (integration); changes land via PR; semver tag on `master`.
- Never rename the import package `process_logger` — it is a public API contract.
- Default: do not commit — git is the user's call.
- No AI attribution in commits or PR descriptions.

## Architecture

`ProcessLogger(logging.LoggerAdapter)` and `ProcessLoggerMixin` in `process_logger/`:
attach contextual params (process name, code, locale, db-operation, function name) to log records,
with optional `QueueListener`-based async logging (`use_queue=True`). No runtime dependencies (stdlib).
