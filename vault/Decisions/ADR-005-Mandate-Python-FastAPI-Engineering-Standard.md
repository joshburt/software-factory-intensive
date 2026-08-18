---
title: ADR-005 Mandate a Python/FastAPI Engineering Standard for Student Projects
type: decision
tags:
  - decision
  - curriculum
  - manifest
  - agent-prompt
created: 2026-08-17
updated: 2026-08-17
status: draft
source: agent
---

# ADR-005: Mandate a Python/FastAPI Engineering Standard for Student Projects

## Context

Until this decision the curriculum was **technology-agnostic for student projects**.
That agnosticism was never a stated principle — it was emergent. A full read of
`.specify/memory/constitution.md` v1.3.0 finds no article, and no entry in Additional
Constraints, that establishes it. It existed only because
`curriculum/PROJECT_MANIFEST_TEMPLATE.md` shipped a blank Tech Stack table and because
agent prompts read whatever the student's rig happened to contain.

The cost of that agnosticism is borne by the agents. A planner, architect, designer,
builder, reviewer, and release gate that cannot assume a stack cannot assume a layer
boundary, a test command, a migration mechanism, or a definition of done. They produce
plausible-looking artifacts that do not compose. The curriculum's own builder prompts
had already drifted toward a de-facto default to compensate — `packs/lessons/{L3,L4,C1}/agents/builder/prompt.template.md`
carried `For a Node project with package.json containing "test": "node --test"` and
`When changing CommonJS modules, update module.exports`, and
`packs/lessons/C1/agents/validator/prompt.template.md` carried the same Node test
branch. No equivalent branch existed for any other ecosystem. So the practical
default was already Node, chosen by accident and stated nowhere.

The instruction driving this ADR is to subsume the patterns of two existing
first-party repositories — `anvil` and `darkharbour` — into one prescriptive
standard, with the reference project rebuilt against it so the agentic harness runs
against a solid, patterned target.

### What the two donor repositories actually contain

Direct inspection contradicted the initial framing that both repos carry the same
patterns. They do not.

| Capability | `anvil` | `darkharbour` |
|---|---|---|
| SQLAlchemy ORM | 2.0 async, `Mapped`/`mapped_column` | **absent** — raw `aiosqlite`, hand-written SQL |
| Alembic migrations | 16 revisions, async `env.py` | **absent** — hand-rolled `MIGRATIONS: list[tuple[int, Callable]]` |
| Repository layer | 31 hand-written repository classes | free functions taking `db` as first argument |
| Playwright UI tests | `pytest-playwright`, `tests/browser/`, `make test-browser` | **absent** |
| Client SDK | hand-written async SDK, shared `Transport`, 14 sub-clients | **absent** |
| PostgreSQL | **absent** — SQLite only | **absent** — SQLite only |
| `pydantic-settings` `BaseSettings` | absent — custom `get_config()` returning a flat dict | present, layered precedence, `frozen=True` |
| `create_app()` factory | absent — module-level `app = FastAPI(...)` | present |
| Package layout | flat (`anvil/` at root) | `src/` layout |

The conclusion: **`anvil` is the architecture donor; `darkharbour` is the tooling and
packaging donor.** Two named requirements — PostgreSQL and a client SDK — exist in
neither repository in the requested form and are therefore net-new design, not
subsumed pattern. This ADR records them as such rather than implying provenance the
code does not have.

Where the two agree, they agree strongly, and that agreement forms the uncontested
base: `uv` with a committed `uv.lock`, Python >= 3.11, a Makefile driver composed of
modular `shared/*.mk` includes with a byte-identical help-target idiom, the
`$(VENV_DIR)/activate: pyproject.toml uv.lock` bootstrap rule, a `make pr-ready`
composite gate, custom `.githooks/` enabled by `make setup-hooks` rather than the
`pre-commit` framework, ruff for linting with black as the formatter, isort, mypy,
bandit, pytest with `asyncio_mode = "auto"`, commitizen with conventional commits and
`tag_format = "v$version"`, a `py.typed` marker, and a multi-stage Dockerfile running
as a non-root uid 1000.

## Decision

Adopt a single mandated engineering standard for student projects, recorded normatively
in `curriculum/ENGINEERING_STANDARD.md`, and make it binding rather than advisory.

The six conflicts between the donor repositories are resolved as follows.

1. **Composition root — FastAPI `Depends` providers per service.** Rejects `anvil`'s
   `AnvilWorkbench` god class. A deliberate god class cannot be taught as an example
   of layer separation, which is the lesson the curriculum exists to convey.
2. **Package layout — `src/` layout.** Follows `darkharbour`. Prevents a
   current-working-directory import from shadowing the installed package, which
   surfaces packaging defects that flat layout conceals.
3. **Strictness — `anvil`-strict.** Line length 88, NumPy docstrings enforced through
   ruff `D` with `convention = "numpy"`, mypy strict across the whole package, and a
   ratcheting coverage floor. Applied because the primary author of this code is an
   agent: the linter catches what review misses, and enforced docstrings make agent
   output self-describing.
4. **Model layering — two layers.** The SQLAlchemy model is the domain object;
   Pydantic schemas appear only at the HTTP boundary. Rejects a third domain-dataclass
   layer: the per-entity mapping functions it requires are exactly the code agents
   drift on, and it triples per-entity file count for no benefit at this scale.
5. **Repository shape — generic typed `BaseRepository[TModel]` with per-entity
   subclasses.** Departs from `anvil`'s deliberate no-base-class stance. Agents
   otherwise regenerate ~40 lines of near-identical CRUD per entity, and every
   regeneration is a fresh opportunity to mishandle the session. Net-new.
6. **Client SDK — hand-written, on `anvil`'s `Transport` plus per-domain sub-client
   pattern.** Chosen over OpenAPI code generation.

Three further points were settled without conflict, since only one donor had a
defensible answer: `pydantic-settings` `BaseSettings` for configuration, a
`create_app()` factory for application construction, and async SQLAlchemy 2.0
throughout.

Database policy is **SQLite for development and test, PostgreSQL for production**,
driven by a single URL setting with dialect-agnostic models. Neither donor
repository supports PostgreSQL, so this is new work and the models must be kept free
of SQLite-only assumptions that `anvil` currently relies on (`PRAGMA` calls,
`batch_alter_table` migrations).

### How "mandated" is made legal under Article II

Article II is NON-NEGOTIABLE and requires that agent prompts "be portable: liftable
into a real project unchanged." `packs/README.md` states the same rule as an authoring
requirement. Hardcoding `uv run pytest`, FastAPI, or SQLAlchemy into
`packs/lessons/*/agents/*/prompt.template.md` would violate both.

The mandate is therefore delivered through the mechanism the constitution already
provides, not around it:

- Article XI already binds `Tech Stack -> Architect` and makes the manifest
  authoritative for each agent role.
- `curriculum/PROJECT_MANIFEST_TEMPLATE.md` ships **pre-filled** with the mandated
  stack, so the standard lands in the student's own rig as `docs/PROJECT_MANIFEST.md`.
- Pack prompts stay stack-neutral in mechanism and become **manifest-driven** in
  substance: they name the manifest section they treat as authoritative and read the
  concrete command from it.

This also resolves a runtime constraint that would otherwise have made a
curriculum-only standard inert: agents execute against the student's rig and cannot
read `curriculum/*` at all. Only the manifest crosses that boundary.

The existing Node-specific branches in the builder and validator prompts are
**removed**, not retargeted. They are simultaneously a portability violation, a
violation of `packs/README.md`, and now factually wrong.

## Consequences

- Tech-agnosticism ends for student projects. Students no longer bring an arbitrary
  stack; the templates stop being fill-in-the-blank for the Tech Stack section.
- **No constitution amendment is required.** No article is violated, because no
  article established agnosticism. A PATCH-level clarification remains optional.
- The Tech Stack table's current rows (`Frontend`, `Styling`, `State`, `Routing`) are
  React-shaped and are reshaped for a server-rendered stack. Both donor repositories
  independently converged on Jinja2 templates plus static CSS/JS with no SPA
  framework, which is also what makes Playwright UI tests coherent.
- **Article IV imposes the dominant cost.** Changing the reference stack invalidates
  walkthrough snapshots for L1-L4 and C1. Those must be regenerated by live runs,
  with real tokens, and Article X forbids running the chains concurrently.
- `reference-project/fired-up-pizza` is an external git submodule
  (`github.com/joshburt/fired-up-pizza`, pinned at `e19adae`) whose current stack is
  React/TypeScript/Express/SQLite. Rebuilding it as Python/FastAPI is a commit to a
  *different repository*. Additional Constraints keep it examples-only: it MUST NOT
  become a runtime dependency of any lesson pack.
- Lint is unaffected: none of `SFI001`-`SFI008` nor `SFI320` match technology names —
  `SFI320`'s regex matches curriculum vocabulary only. Lesson contracts constrain
  artifact *paths*, not artifact content.
- Editing `packs/**` triggers all three pre-commit harnesses; curriculum-only markdown
  triggers none.

## Alternatives Considered

- **Golden-path default with deviation allowed.** Rejected on instruction. It would
  have preserved the current templates and required no ADR, but it leaves agents in
  the same position of being unable to assume anything.
- **Prescriptive for the reference project only.** Rejected on instruction. It fixes
  the harness target without giving student-facing agents the same footing.
- **Amend the constitution to enshrine the stack.** Rejected as unnecessary. Article XI
  already supplies the enforcement path; adding stack specifics to the constitution
  would couple a supreme governance document to a technology choice it does not need
  to know about.
