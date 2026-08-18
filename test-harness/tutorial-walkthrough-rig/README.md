# Calculator

Minimal Python calculator project.

This project is intentionally tiny: just enough structure for agents to produce
meaningful planning artifacts and implementation changes.

## Contents

| Path | Purpose |
|---|---|
| `pyproject.toml` | Project metadata and tool configuration |
| `Makefile` | Task runner (test, lint, format, typecheck) |
| `src/calculator/__init__.py` | Basic calculator functions |
| `tests/test_calculator.py` | Passing tests that demonstrate the test conventions |
| `CLAUDE.md` | Minimal project rules agents read for context |

## Why Python

The `pyproject.toml` + `src/` + `tests/` shape follows the curriculum's
engineering standard and uses the mandated toolchain (uv, pytest, ruff,
black, mypy).