# Engineering Standard

**Status**: binding. **Last updated**: 2026-08-17.
**Decision record**: [`ADR-005`](../vault/Decisions/ADR-005-Mandate-Python-FastAPI-Engineering-Standard.md).

This document defines the mandated technology stack and architecture for the software
you build during this workshop. It is the source your project manifest summarizes and
the standard your factory's agents hold your code to.

## How this standard reaches your agents

Your agents run against **your project rig**. They cannot read this file. The mandate
travels one way only:

```text
ENGINEERING_STANDARD.md  ->  docs/PROJECT_MANIFEST.md  ->  your agents
     (you read it)            (lands in your rig)         (they read it)
```

`curriculum/PROJECT_MANIFEST_TEMPLATE.md` ships pre-filled with this stack. Copy it
into your project as `docs/PROJECT_MANIFEST.md` and your agents inherit the standard
automatically. Every agent prompt names the manifest section it treats as
authoritative — `Tech Stack` for the Architect, `Conventions` for the Builder,
`Review Standards` for the Reviewer, `Release Criteria` for the Release Gate.

If your manifest and this document disagree, fix the manifest.

## 1. Mandated stack

| Layer | Technology | Notes |
|---|---|---|
| Language | Python `>=3.11,<3.14` | pin the exact version in `.python-version` |
| Web framework | FastAPI | `create_app()` factory, never a module-level app |
| Validation / schemas | Pydantic v2 | HTTP boundary only |
| Configuration | pydantic-settings v2 | `BaseSettings`, `frozen=True` |
| ORM | SQLAlchemy 2.0, async | `Mapped` / `mapped_column` typed style |
| Migrations | Alembic | async `env.py`, autogenerate from `Base.metadata` |
| Database (dev/test) | SQLite via `aiosqlite` | file for dev, in-memory for tests |
| Database (production) | PostgreSQL via `asyncpg` | same models, same migrations |
| Server | `uvicorn[standard]` | |
| Templates | Jinja2 | server-rendered; no SPA framework |
| Static assets | plain CSS + vanilla JS | no build step, no bundler |
| Logging | structlog | structured, JSON in production |
| Dependencies / env | `uv` | committed `uv.lock`; never pip, poetry, or conda |
| Build backend | setuptools | `src/` layout |
| Task runner | GNU Make | `Makefile` + `shared/*.mk` |
| Lint | ruff | linting only — ruff does not format here |
| Format | black + isort | line length 88 |
| Types | mypy `strict` | whole package, no exemptions by default |
| Security | bandit | every skip needs a written rationale |
| Tests | pytest + pytest-asyncio | `asyncio_mode = "auto"` |
| UI tests | Playwright via `pytest-playwright` | Chromium |
| Containers | Docker, multi-stage | non-root uid 1000 |
| Commits | Conventional Commits via commitizen | `tag_format = "v$version"` |

Nothing here is optional. Adding a dependency outside this list is a human decision
(Article XIV), not an agent decision.

## 2. Repository layout

`src/` layout. The package name is your project's slug in `snake_case`.

```text
your-project/
├── .githooks/                  # pre-commit, commit-msg
├── .python-version
├── Makefile                    # thin dispatcher; includes shared/*.mk
├── shared/                     # helper.mk python.mk testing.mk database.mk docker.mk
├── pyproject.toml              # single source of config for every tool
├── uv.lock                     # committed
├── alembic.ini
├── Dockerfile                  # multi-stage
├── compose.yaml                # app + postgres
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── PROJECT_MANIFEST.md     # authoritative for your agents
│   └── SOFTWARE_FACTORY_MANIFEST.md
├── src/your_project/
│   ├── __init__.py
│   ├── py.typed                # zero-byte PEP 561 marker
│   ├── settings.py             # pydantic-settings BaseSettings
│   ├── errors.py               # domain exception hierarchy
│   ├── db/
│   │   ├── base.py             # DeclarativeBase
│   │   ├── session.py          # async engine + sessionmaker + get_session
│   │   ├── mixins.py           # TimestampMixin
│   │   ├── models/             # one SQLAlchemy model per file
│   │   └── repositories/
│   │       ├── base.py         # BaseRepository[TModel]
│   │       └── <entity>.py     # one repository per entity
│   ├── services/               # one service per aggregate
│   ├── api/
│   │   ├── app.py              # create_app() + create_app_from_settings()
│   │   ├── providers.py        # Depends providers
│   │   ├── exception_handlers.py
│   │   ├── schemas/            # Pydantic request/response models
│   │   ├── routers/            # one router module per resource
│   │   ├── templates/          # Jinja2
│   │   └── static/             # css/ js/
│   ├── client/                 # hand-written SDK
│   │   ├── client.py           # top-level facade
│   │   ├── _shared/            # Transport, config, error hierarchy
│   │   └── <domain>/           # per-domain sub-client
│   └── migrations/             # Alembic env.py, script.py.mako, versions/
└── tests/
    ├── conftest.py
    ├── unit/
    ├── integration/
    ├── system/
    └── ui/
```

## 3. Layer architecture

Four layers. Dependencies point **one way only**.

```text
models  <-  repositories  <-  services  <-  routers
                                   ^
                              providers (wiring)
```

Binding rules:

- A **model** imports only `db.base`, `db.mixins`, and SQLAlchemy. Nothing else.
- A **repository** imports models and SQLAlchemy. It MUST NOT import a service, a
  router, or anything from `api/`.
- A **service** imports repositories, models, and `errors`. It MUST NOT import
  `fastapi` — no `Depends`, no `HTTPException`, no `Request`. A service that needs to
  signal failure raises a domain error from `errors.py`.
- A **router** imports schemas, services, and providers. It MUST NOT import a
  repository or a model directly.
- Raw SQL and ORM query primitives (`select`, `update`, `delete`) appear **only** in
  `db/repositories/`. A `select(` outside that directory is a defect.

### Composition root

Wiring lives in `api/providers.py` as one provider per service. No god class, no
service locator, no closure capture.

```python
async def get_session() -> AsyncIterator[AsyncSession]: ...          # db/session.py

def get_widget_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> WidgetRepository:
    return WidgetRepository(session)

def get_widget_service(
    repo: Annotated[WidgetRepository, Depends(get_widget_repository)],
) -> WidgetService:
    return WidgetService(repo)
```

Routes depend on the service, never on the session or the repository:

```python
@router.get("/widgets/{widget_id}", response_model=WidgetRead)
async def read_widget(
    widget_id: int,
    service: Annotated[WidgetService, Depends(get_widget_service)],
) -> Widget:
    return await service.get_widget(widget_id)
```

Overriding a provider in a test is the supported way to substitute a fake:
`app.dependency_overrides[get_widget_service] = ...`.

## 4. Data layer

### Models

Two layers only: the SQLAlchemy model **is** the domain object. There is no separate
domain dataclass. Pydantic appears only at the HTTP boundary.

```python
class Widget(Base, TimestampMixin):
    __tablename__ = "widgets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
```

Conventions:

- Table names are plural `snake_case`.
- Primary keys are `int` autoincrement unless a natural key is justified in an ADR.
- `TimestampMixin` supplies `created_at` and `updated_at` server-side.
- One model per file, named after the entity.
- Models MUST stay dialect-agnostic. No `PRAGMA`, no SQLite-only types, no
  `batch_alter_table` in migrations — those foreclose PostgreSQL.

### Repositories

Every repository extends the generic base and declares its model.

```python
TModel = TypeVar("TModel", bound=Base)

class BaseRepository(Generic[TModel]):
    model: type[TModel]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, entity_id: int) -> TModel | None: ...
    async def list(self, *, limit: int | None = None, offset: int = 0) -> Sequence[TModel]: ...
    async def add(self, entity: TModel) -> TModel: ...
    async def update(self, entity: TModel) -> TModel: ...
    async def delete(self, entity_id: int) -> bool: ...
    async def count(self) -> int: ...
```

A subclass adds only what is specific to its entity:

```python
class WidgetRepository(BaseRepository[Widget]):
    model = Widget

    async def get_by_name(self, name: str) -> Widget | None:
        result = await self._session.execute(select(Widget).where(Widget.name == name))
        return result.scalar_one_or_none()
```

Repositories `flush()` and `refresh()`; they do **not** `commit()`. Transaction
boundaries belong to the session dependency, so one request is one transaction.

### Sessions

Async engine and `async_sessionmaker` with `expire_on_commit=False`. The `get_session`
dependency yields a session, commits on success, rolls back on exception, and always
closes.

### Migrations

Alembic, async `env.py`, `target_metadata = Base.metadata`. A registry module imports
every model so autogenerate sees the full schema.

- Revisions are sequential and zero-padded: `0001_initial.py`, `0002_add_widgets.py`.
- Every migration implements both `upgrade()` and `downgrade()`.
- Autogenerated migrations MUST be read and corrected by hand before commit.
- Schema migrations are a human decision (Article XIV). An agent may draft one; a
  human approves it.

### Database policy

One `DATABASE_URL` setting selects the dialect. Nothing else in the code branches on it.

| Context | URL |
|---|---|
| Development | `sqlite+aiosqlite:///./data/app.db` |
| Unit / integration tests | `sqlite+aiosqlite://` (in-memory) |
| System tests / production | `postgresql+asyncpg://...` |

## 5. HTTP layer

### Application construction

```python
def create_app(widget_service: WidgetService | None = None) -> FastAPI:
    """Build the application. Optional arguments exist for test injection."""

def create_app_from_settings(settings: Settings | None = None) -> FastAPI:
    """Production wiring. This is the uvicorn entry point."""
```

Startup and shutdown use an `asynccontextmanager` lifespan. Never a module-level
`app = FastAPI(...)`.

### Routers

One router module per resource, mounted under a version prefix:

```python
app.include_router(widgets_router, prefix="/v1")
```

Routers are thin: validate input, call one service method, return a response model.
No business logic, no query construction, no session handling.

### Schemas

Pydantic v2, in `api/schemas/`, named for intent:

| Suffix | Purpose |
|---|---|
| `...Create` | request body for create |
| `...Update` | request body for partial update |
| `...Read` | response body |

Read schemas set `model_config = ConfigDict(from_attributes=True)` so they serialize
ORM instances directly. Request schemas set `extra="forbid"`.

### Errors

A domain hierarchy in `errors.py`, mapped to HTTP once in `api/exception_handlers.py`:

| Domain error | Status |
|---|---|
| `NotFoundError` | 404 |
| `ConflictError` | 409 |
| `ValidationError` | 422 |
| `AppError` (base) | 500 |

Services raise domain errors. Routers do not translate them — the registered handlers
do. `except:` with an empty body is never acceptable.

## 6. Configuration

`settings.py`, a single `Settings(BaseSettings)`:

```python
model_config = SettingsConfigDict(
    env_prefix="APP_",
    env_file=".env",
    extra="ignore",
    frozen=True,
)
```

Precedence, highest first: explicit constructor arguments, `APP_*` environment
variables, `.env`, field defaults. Secrets are read from the environment and never
committed — `.env` is git-ignored, `.env.example` is committed with placeholder values.

## 7. Client SDK

Hand-written, in `src/your_project/client/`. A shared `Transport` owns the `httpx`
client, base URL, auth header, timeout, and retries. One sub-client per API domain,
exposed as a lazy property on the facade:

```python
client = AppClient(base_url="http://localhost:8000", api_key="...")
widget = await client.widgets.get(1)
```

The SDK has its own error hierarchy — `ApiError` as base, with `AuthenticationError`,
`NotFoundError`, `ValidationError`, `RateLimitError`, `ServerError` — so callers never
handle raw HTTP status codes. When an endpoint changes, the SDK changes in the same
commit.

## 8. Test ladder

Four tiers. Each has a distinct contract and its own Make target.

| Tier | Directory | May touch | Speed | Target |
|---|---|---|---|---|
| Unit | `tests/unit/` | pure logic; fakes for repositories. **No DB, no HTTP, no filesystem** | milliseconds | `make test-unit` |
| Integration | `tests/integration/` | real repositories against in-memory SQLite; API through `httpx.ASGITransport` — no network | sub-second | `make test-integration` |
| System | `tests/system/` | the built container against real PostgreSQL via `compose.yaml` | seconds | `make test-system` |
| UI | `tests/ui/` | Playwright/Chromium against the running stack | seconds | `make test-ui` |

`make test` runs unit + integration. System and UI tiers are separate because they
require Docker.

Fixture contract in `tests/conftest.py`:

- `session` — in-memory SQLite, schema created and dropped per test.
- `client` — `httpx.AsyncClient` over `ASGITransport`, provider overrides applied.
- Each test is fully isolated. No test may depend on another test's writes.

### TDD

Red-green-refactor is required, not encouraged. The failing test is written and
observed failing **before** the implementation. An implementation commit with no
corresponding test change is a defect the Reviewer rejects.

Coverage is a ratchet: `fail_under` in `pyproject.toml` may only ever increase.
Lowering it to make a build pass is prohibited (Article VIII).

## 9. Tooling

### Make targets

`Makefile` is a thin dispatcher; the logic lives in `shared/*.mk`. Every target
carries a `##` comment so `make help` can discover it.

| Target | Purpose |
|---|---|
| `help` | list documented targets (default goal) |
| `install` | `uv sync --all-extras` |
| `format` | black + isort, writing changes |
| `lint` | ruff + `black --check` + `isort --check` |
| `typecheck` | mypy strict |
| `security` | bandit |
| `test` | unit + integration with coverage |
| `test-unit` / `test-integration` / `test-system` / `test-ui` | single tier |
| `db-upgrade` / `db-downgrade` / `db-revision` / `db-current` / `db-history` | Alembic |
| `run` | uvicorn, reload enabled |
| `build` | `uv build --wheel` |
| `compose-up` / `compose-down` | container stack |
| `setup-hooks` | `git config core.hooksPath .githooks` |
| `clean` | remove build, cache, and coverage artifacts |
| `pr-ready` | `format` -> `lint` -> `typecheck` -> `security` -> `test` |

`make pr-ready` is the gate. It is what `.githooks/pre-commit` runs.

The venv bootstraps itself through a real file dependency, so no target ever runs
against a stale environment:

```makefile
$(VENV_DIR)/activate: pyproject.toml uv.lock
	@test -d $(VENV_DIR) || uv venv $(VENV_DIR)
	uv sync --all-extras
	@touch $(VENV_DIR)/activate
```

### Git hooks

Custom hooks in `.githooks/`, enabled by `make setup-hooks`. The `pre-commit` hook runs
`make pr-ready`; the `commit-msg` hook runs `commitizen check`. The `pre-commit`
*framework* is not used.

`--no-verify` is an exception, not a workflow. A check that flakes repeatedly gets
fixed, never deleted or weakened.

### Quality configuration

All tool configuration lives in `pyproject.toml`. There are no separate `setup.cfg`,
`.flake8`, `mypy.ini`, or `pytest.ini` files.

```toml
[tool.ruff]
target-version = "py311"
line-length = 88

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "B", "C4", "I", "N", "UP", "ASYNC", "RUF", "D"]
ignore = ["E501", "B008", "D205"]           # B008 is required by FastAPI Depends

[tool.ruff.lint.pydocstyle]
convention = "numpy"

[tool.black]
line-length = 88
target-version = ["py311"]

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.11"
strict = true
plugins = ["pydantic.mypy"]
warn_unused_ignores = true
enable_error_code = ["ignore-without-code", "possibly-undefined", "redundant-expr"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --cov=your_project --cov-report=term-missing --cov-branch"
```

Type errors are fixed, never suppressed. `# type: ignore` without a specific error
code is rejected by `ignore-without-code`, and a blanket `Any` cast to silence mypy is
a defect.

Docstrings are NumPy-style and required on every module, class, and public function —
ruff `D` enforces this. This exists because most of this code is written by agents:
enforced docstrings make generated code self-describing.

### Containers

Multi-stage Dockerfile. The builder stage runs `uv build --wheel`; the runtime stage
installs only that wheel — no source tree — and runs as a non-root user at uid 1000.
`compose.yaml` defines the app plus PostgreSQL with a real healthcheck, and host ports
bind to `127.0.0.1`.

## 10. Provenance

Recorded so nobody mistakes invention for precedent.

| Element | Source |
|---|---|
| `uv` + committed lock, setuptools, `py.typed`, Python >= 3.11 | both donors |
| Makefile + `shared/*.mk`, help idiom, venv bootstrap, `pr-ready` | both donors |
| Custom `.githooks/` over the pre-commit framework | both donors |
| ruff-lints / black-formats / isort / mypy / bandit | both donors |
| pytest `asyncio_mode = "auto"`, commitizen, conventional commits | both donors |
| Multi-stage Dockerfile, non-root uid 1000 | both donors |
| Async SQLAlchemy 2.0, Alembic async `env.py`, repository + service layers | `anvil` |
| Playwright UI tier, hand-written SDK `Transport` + sub-clients | `anvil` |
| `anvil`-strict quality dials, NumPy docstring enforcement | `anvil` |
| `src/` layout, pydantic-settings `BaseSettings`, `create_app()` factory | `darkharbour` |
| structlog, compose test stack, `uv` dependency groups | `darkharbour` |
| **Generic `BaseRepository[TModel]`** | **net-new** — neither donor has one |
| **PostgreSQL support** | **net-new** — both donors are SQLite-only |
| **`Depends`-provider composition root** | **net-new** — replaces `anvil`'s god class |
| **Four-tier test ladder** | **net-new** — reconciles two different tier schemes |
