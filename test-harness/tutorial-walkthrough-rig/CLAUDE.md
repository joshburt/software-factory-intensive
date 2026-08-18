# Calculator Project Agent Rules

This is a minimal Python calculator project. Treat it as a real project
with the rules below. The active factory workflow owns step routing and
artifact contracts.

## Tech stack

- Python >= 3.11
- pytest for testing — run `make test`
- uv for dependency management
- ruff for linting, black + isort for formatting, mypy for type checking
- Zero production dependencies

## Project structure

- `src/calculator/` — implementation package
- `tests/` — test files (one per source package, named `test_<module>.py`)
- `docs/plans/` — Planner output, one markdown file per feature
- `docs/architecture/` — Architect output, one markdown file per feature
- `docs/designs/` — Designer output, one design spec per feature
- `docs/reviews/` — Reviewer output, one review report per feature
- `docs/releases/` — Release-Gate output, one gate report per feature

## Conventions

- Export functions at package level via `__init__.py`
- Every new source file needs a matching test file with at least one happy-path test
- Prefer small pure functions over classes
- Builder should commit each feature on a `feature/<slug>` branch — never straight to main
- **Commands** — use these rather than invoking tools directly:

  | Purpose | Command |
  |---|---|
  | Install / sync deps | `make install` |
  | Format | `make format` |
  | Lint | `make lint` |
  | Type check | `make typecheck` |
  | Run tests | `make test` |

## Workflow Expectations

The active formula creates and routes the step beads. Each agent should
work only the current routed formula step and close that step when its artifact
or implementation work is complete. Do not create the next stage's bead, relabel
work, or wake another agent; the formula graph owns the order.

| Stage        | Produces                                      | On finish                 |
|--------------|-----------------------------------------------|---------------------------|
| Planner      | `docs/plans/<slug>.md`                        | close current step        |
| Architect    | `docs/architecture/<slug>.md`                 | close current step        |
| Designer     | `docs/designs/<slug>.md`                      | close current step        |
| Builder      | code + tests on `feature/<slug>` branch       | close current step        |
| Reviewer     | `docs/reviews/<slug>.md`                      | close current step        |
| Release-Gate | `docs/releases/<slug>.md` with PASS/FAIL      | close current step        |

## Artifact content requirements

- **Planner** → Plan: sections `## Goal`, `## User Stories`,
  `## Acceptance Criteria`, and `## Scope Boundary`.
- **Architect** → Architecture: sections `## Context`,
  `## Options Considered` (2+ options), and `## Decision` with rationale.
- **Designer** → Design spec: sections covering interface, behavior/edge cases, and a test plan.
- **Reviewer** → Review report: each finding labelled with severity (Critical / High / Medium / Low), location, impact, and suggested fix.
- **Release-Gate** → Gate report: explicit `PASS` or `FAIL` verdict plus evidence per check.