# Project Manifest: [Project Name]

> This manifest is the contract between your project and your agents. Each agent reads
> the section it treats as authoritative: **Tech Stack** -> Architect, **Domain Model**
> -> Designer, **Conventions** -> Builder, **Review Standards** -> Reviewer, **Release
> Criteria** -> Release Gate, and the whole manifest -> Planner.
>
> The **Tech Stack**, **Conventions**, **Review Standards**, and **Release Criteria**
> sections are pre-filled from the binding
> [`ENGINEERING_STANDARD.md`](ENGINEERING_STANDARD.md). Do not weaken them. Fill in the
> sections describing *your* project: Overview, Project Structure, Domain Model,
> Constraints, Task Inputs, Services to Connect, and Success Criteria.

## Overview

[One paragraph: what the software does and who uses it.]

## Tech Stack

| Layer | Technology | Notes |
|---|---|---|
| Language | Python `>=3.11,<3.14` | exact version pinned in `.python-version` |
| Web framework | FastAPI | `create_app()` factory; never a module-level app |
| Templates | Jinja2 | server-rendered; no SPA framework |
| Static assets | plain CSS + vanilla JS | no bundler, no build step |
| Validation / schemas | Pydantic v2 | HTTP boundary only, never in services |
| Configuration | pydantic-settings v2 | `BaseSettings`, `frozen=True`, `APP_` env prefix |
| ORM | SQLAlchemy 2.0 (async) | `Mapped` / `mapped_column` typed style |
| Migrations | Alembic | async `env.py`, autogenerate from `Base.metadata` |
| Database | SQLite (dev + test), PostgreSQL (production) | one `DATABASE_URL`; models stay dialect-agnostic |
| Server | `uvicorn[standard]` | |
| Logging | structlog | structured; JSON in production |
| Dependencies / env | `uv` + committed `uv.lock` | never pip, poetry, or conda |
| Build backend | setuptools, `src/` layout | |
| Task runner | GNU Make | `Makefile` + `shared/*.mk` |
| Lint | ruff | linting only; black is the formatter |
| Format | black + isort | line length 88 |
| Types | mypy `strict` | whole package |
| Security | bandit | every skip needs a written rationale |
| Tests | pytest + pytest-asyncio | `asyncio_mode = "auto"` |
| UI tests | Playwright (`pytest-playwright`) | Chromium |
| Containers | Docker, multi-stage | non-root uid 1000 |
| Commits | Conventional Commits (commitizen) | `tag_format = "v$version"` |

Adding a dependency outside this table is a human decision, not an agent decision.

## Project Structure

[Top-level directory tree, annotated. Label `(proposed)` if pre-code. It MUST follow
the `src/` layout and the four-layer split defined in `ENGINEERING_STANDARD.md`:
`db/models` <- `db/repositories` <- `services` <- `api/routers`.]

## Domain Model

[Core entities, their fields, and their relationships. Each entity becomes one
SQLAlchemy model in `src/<pkg>/db/models/`, one repository in `db/repositories/`, and
one service in `services/`.]

## Conventions

- **File naming**: `snake_case.py`. One model per file, one repository per entity, one
  router per resource.
- **Test files**: `tests/<tier>/test_<module>.py`, where `<tier>` is `unit`,
  `integration`, `system`, or `ui`. Test functions are `test_<behavior>_<condition>`.
- **API routes**: plural nouns under a version prefix — `/v1/widgets`,
  `/v1/widgets/{widget_id}`.
- **Layer boundaries**: dependencies point one way — models <- repositories <- services
  <- routers. Services MUST NOT import `fastapi`. `select(`, `update(`, and `delete(`
  appear only in `db/repositories/`.
- **Errors**: services raise domain errors from `errors.py`; registered exception
  handlers map them to status codes. Routers do not translate errors.
- **Docstrings**: NumPy style, required on every module, class, and public function
  (enforced by ruff `D`).
- **Types**: mypy strict. Never suppress an error with a bare `# type: ignore` or an
  `Any` cast.
- **TDD**: write the failing test first and observe it fail. An implementation change
  with no corresponding test change is a defect.
- **Commands** — agents MUST use these rather than invoking tools directly:

  | Purpose | Command |
  |---|---|
  | Install / sync deps | `make install` |
  | Format | `make format` |
  | Lint | `make lint` |
  | Type check | `make typecheck` |
  | Security scan | `make security` |
  | Run tests (unit + integration) | `make test` |
  | Run one tier | `make test-unit` / `make test-integration` / `make test-system` / `make test-ui` |
  | Create a migration | `make db-revision MESSAGE="..."` |
  | Apply migrations | `make db-upgrade` |
  | Full pre-commit gate | `make pr-ready` |

- **Commits**: Conventional Commits — `feat:`, `fix:`, `docs:`, `test:`, `refactor:`,
  `chore:`.
- **Branches**: `<type>/<short-slug>` — for example `feat/loyalty-points`.

## Constraints

- [Explicit out-of-scope items or disallowed approaches for your project.]
- Schema migrations, new dependencies, and public API contract changes are human
  decisions. An agent may draft them; a human approves them.

---

## Task Inputs

| Agent     | Receives                  | From                     |
|-----------|--------------------------|--------------------------|
| Planner   |                          |                          |
| Architect |                          |                          |
| Designer  |                          |                          |
| Coder     |                          |                          |
| Reviewer  |                          |                          |
| Deployer  |                          |                          |

## Services to Connect

| Service | Purpose | Config |
|---------|---------|--------|
|         |         |        |

## Success Criteria

### Per-Feature Success

- [ ]
- [ ]

### Factory-Level Success

- [ ]
- [ ]

---

## Review Standards

### Spec Compliance

- Every acceptance criterion in the design artifact maps to at least one test.
- No behavior ships that the design artifact does not describe.
- The failing-test-first sequence is evident: tests changed in the same commit as, or
  before, the implementation.

### Style

- Layer boundaries hold: no `fastapi` import inside `services/`, no ORM query
  primitive outside `db/repositories/`, no repository or model imported by a router.
- Pydantic appears only at the HTTP boundary.
- `make lint`, `make format --check` equivalent, and `make typecheck` are clean.
- NumPy docstrings present on every module, class, and public function.
- No suppressed type errors, no empty `except` blocks.

### Security

- No secret, token, or credential in source or in a committed `.env`.
- All input crosses a Pydantic schema before reaching a service.
- No string-interpolated SQL — parameterized queries only.
- `make security` (bandit) is clean, or each skip carries a written rationale.

### Severity Scale

- **Low**: cosmetic issues, minor inconsistencies
- **Medium**: functional gaps, missing edge cases
- **High**: data loss, security vulnerability, spec violation, layer-boundary breach

---

## Release Criteria

### Required (all must PASS)

1. [ ] `make pr-ready` passes — format, lint, typecheck, security, unit + integration tests.
2. [ ] `make test-system` passes against PostgreSQL in the container stack.
3. [ ] `make test-ui` passes.
4. [ ] Coverage is at or above the `fail_under` floor in `pyproject.toml`. The floor may
       only increase — never lower it to obtain a pass.
5. [ ] Alembic migration chain applies cleanly from empty, and `downgrade()` is implemented.
6. [ ] No new dependency was added without human approval.

### Informational (reported but non-blocking)

- Coverage delta versus the previous release
- Count of new or changed public API endpoints
- Migration count in this release
