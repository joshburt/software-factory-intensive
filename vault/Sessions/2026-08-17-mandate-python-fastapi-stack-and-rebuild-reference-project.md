---
title: Mandate Python/FastAPI Stack and Rebuild the Reference Project
type: session
tags:
  - session
  - curriculum
  - manifest
  - agent-prompt
  - test-harness
  - enforcement
created: 2026-08-17
updated: 2026-08-17
status: draft
source: agent
---

# Mandate Python/FastAPI Stack and Rebuild the Reference Project

## Objective

End technology-agnosticism for student projects. Subsume the patterns of the
first-party `anvil` and `darkharbour` repositories into one binding engineering
standard, and rebuild `reference-project/fired-up-pizza` against it so the agentic
harness runs on a solid, patterned target.

## What was found before deciding

Direct inspection of both donor repositories contradicted the premise that they share
the requested patterns.

- **`anvil` is the architecture donor**: async SQLAlchemy 2.0, Alembic, 31 repository
  classes, a service layer, Playwright, and a hand-written SDK.
- **`darkharbour` is the tooling donor**: `src/` layout, `pydantic-settings`
  `BaseSettings`, a `create_app()` factory, structlog, and a compose test stack. It has
  **no** SQLAlchemy, **no** Alembic, **no** Playwright, and **no** SDK — it uses raw
  `aiosqlite` with hand-rolled migrations.
- **Neither supports PostgreSQL.** Both are SQLite-only.

Two named requirements — PostgreSQL and a client SDK in the requested form — were
therefore net-new design, not subsumed pattern. The generic `BaseRepository[TModel]`
and the `Depends`-provider composition root are also net-new. `ENGINEERING_STANDARD.md`
closes with a provenance table recording this, so invention is not later mistaken for
precedent.

A governance read established that **tech-agnosticism was never a constitutional
principle** — it was emergent from a blank Tech Stack table. No amendment was required.
An ADR was.

## Decisions taken

Recorded in `ADR-005`. Six donor conflicts resolved by the human: `Depends` providers
over `anvil`'s god class; `src/` layout; `anvil`-strict quality dials; two model layers;
generic `BaseRepository[TModel]`; hand-written SDK on `anvil`'s `Transport` pattern.
Database policy: SQLite for dev/test, PostgreSQL for production.

### The Article II mechanism

Article II is NON-NEGOTIABLE and requires pack prompts to be "liftable into a real
project unchanged." Hardcoding Python into `packs/lessons/*/agents/*/prompt.template.md`
would have violated it.

The mandate instead travels through the channel the constitution already provides:

```text
ENGINEERING_STANDARD.md -> PROJECT_MANIFEST_TEMPLATE.md -> student's rig -> agents
```

This also resolved a runtime constraint that would have made a curriculum-only standard
inert: **agents execute against the student's rig and cannot read `curriculum/` at
all.** Only the manifest crosses that boundary. Article XI already binds
`Tech Stack -> Architect` and `Conventions -> Builder`, so the `Conventions` section
gained a Commands table that prompts now read instead of guessing.

The pre-existing Node branches in three builder prompts and the C1 validator were
**removed, not retargeted** — they were simultaneously an Article II violation, a
`packs/README.md` violation, and factually wrong.

## What was built

- `vault/Decisions/ADR-005-...` and `curriculum/ENGINEERING_STANDARD.md` (the keystone)
- `curriculum/PROJECT_MANIFEST_TEMPLATE.md` pre-filled; React-shaped rows
  (`Frontend`/`Styling`/`State`/`Routing`) reshaped for a server-rendered stack, since
  both donors independently converged on Jinja2 + static assets with no SPA framework
- Four pack prompts made manifest-driven
- `fired-up-pizza` rebuilt: 53 source files, four-layer architecture, six domain
  entities, Alembic, four-tier test ladder, hand-written SDK, Jinja2 UI with
  `data-testid` hooks, multi-stage Dockerfile, compose with PostgreSQL
- Curriculum text re-grounded (W1 running example, L1 prompt, overview template,
  `installation.md` prerequisites)

## Verification

Every agent claim was re-verified independently rather than accepted.

| Check | Result |
|---|---|
| `make pr-ready` (fired-up-pizza) | **EXIT=0** |
| mypy `--strict` | clean, 53 source files |
| ruff / black / isort | clean, 62 files |
| bandit | 0 issues, Low 0 / High 0 |
| Tests | 20 unit + 42 integration passed; system 3 skip, ui 3 skip |
| Coverage | 75.53% against a 70% floor |
| Migrations | applied to SQLite; all 6 tables + `alembic_version` |
| Layer rules (Section 3) | proven by grep, not assertion |
| `lesson-pack-lint` (scoped) | 0 errors, 0 warnings |
| `migration-check.sh` | green |
| `behavioral-smoke.sh` | **EXIT=0**, 5 lessons dry-run |

Three defects were caught by verification that the sub-agents had reported as done:

1. **`make test-system` / `make test-ui` failed on any machine without Docker.** The
   coverage floor lives in `addopts`, so it applied to every pytest invocation; when
   those tiers skipped, coverage fell to 40% and the target errored. Fixed with
   `--no-cov` on both tiers, matching `anvil`'s precedent.
2. **`curriculum/labs/L2/README.md` still taught the `node:test` API** in its Context7
   MCP exercise — missed by the curriculum sweep. Re-grounded on pytest.
3. **bandit `B101` on two type-narrowing asserts.** Fixed by converting both to
   explicit raises rather than skipping the check — assertions are stripped under
   `python -O`, so relying on them for control flow was a genuine latent bug.

## Discoveries recorded

`vault/Discoveries/2026-08-17-content-lint-invocation-and-harness-prerequisite.md`
documents two pre-existing harness defects, both independent of this change:

- The bare `lesson-pack-lint.py` invocation that `AGENTS.md` documents scans the whole
  repo and reports 111 errors on a clean tree, flagging `README.md`, `AGENTS.md`, and
  the constitution itself. The real gate is the scoped `--lesson` form.
- `behavioral-smoke.sh` runs under `set -euo pipefail` and aborts at step 1 because
  `SFI100`/`SFI110` require the git-ignored `my-factory/{city,pack}.toml`. **The
  pre-commit hook therefore blocks every lesson-pack commit on a fresh clone** until
  the maintainer runs the two student Quickstart `cp` commands.

## State at close

Nothing committed. Nothing pushed. `reference-project/fired-up-pizza` is an initialized
submodule with an uncommitted working tree; committing it means committing to a
*different* repository, which was left for explicit human approval.

## Round 2 — proving the untested tiers, and a scope correction

### The system and UI tiers had never actually run

Bringing up PostgreSQL and exercising them surfaced **four defects** that had been
reported as complete:

1. **Alembic could never reach PostgreSQL.** `migrations/env.py` read the URL only from
   `alembic.ini`, ignoring `Settings` / `APP_DATABASE_URL`. `make db-upgrade` was
   therefore permanently pinned to SQLite, and Release Criteria #5 was unsatisfiable
   against Postgres. Fixed with a `_resolve_url()` helper that makes `Settings`
   authoritative. Now verified: upgrade, `downgrade base`, and re-upgrade all succeed
   against real PostgreSQL (`Context impl PostgresqlImpl`).
2. **`Order.status` was a native enum.** `Mapped[OrderStatus]` made SQLAlchemy infer a
   PostgreSQL `ENUM` type that the migration never created, while the migration declared
   `String(50)`. SQLite silently degrades `Enum` to VARCHAR, so the mismatch was
   invisible until Postgres returned `type "orderstatus" does not exist` as a 500.
   Changed to `Mapped[str]` + `String(50)` with `OrderStatus` retained as the only
   source of valid values — `anvil`'s own approach.
3. **The system round-trip test was not idempotent.** It used a fixed
   `system@test.com` and `Test Pizza` against a persistent database, so it passed once
   and then 409'd forever. Now uses a per-run `uuid4` suffix; verified by running it
   three times consecutively.
4. **The UI tests hung indefinitely instead of running.** They were `async def` using
   `pytest-playwright`'s **synchronous** `page` fixture, which cannot be driven from
   inside an asyncio event loop under `asyncio_mode = "auto"`. They also carried
   `page: object` plus a `# type: ignore[attr-defined]` on every call, and asserted a
   "No pizzas" empty state that is false whenever data exists. Rewritten as sync tests
   typed with `playwright.sync_api.Page`, no suppressions, and the count assertion now
   compares against the API rather than a hard-coded number.

Also fixed: `--no-cov` on the `test-system` / `test-ui` targets (the `addopts` coverage
floor made them fail on any machine without Docker), and registered the `system` / `ui`
pytest markers.

Final state, verified both ways: with the stack live, **20 unit + 42 integration +
3 system + 3 UI all pass** and `make pr-ready` exits 0; with the stack down, system and
UI **skip** at exit 0 and unit + integration still pass.

### The snapshot task was under-scoped and would have made things worse

Attempting the Article IV regeneration revealed that
`test-harness/tutorial-walkthrough-rig/` — the scratch project the harness slings agents
at — was a **Node.js calculator**, with all five walkthroughs asserting via
`node --test`. Regenerating snapshots first would have baked Node ground truth into a
Python-mandated curriculum and published it as verified fact. Recorded in
`vault/Discoveries/2026-08-17-walkthrough-rig-is-node-while-curriculum-mandates-python.md`.

Corrected order, and the deterministic parts are now done: the rig is a minimal Python
package (`pyproject.toml`, `Makefile`, `src/calculator/`, `tests/`) whose `make test`
passes from a clean copy with no pre-existing venv; all five walkthrough scripts drive
the Python command; `L1.sh`'s fallback manifest heredoc no longer claims Node. Zero
`node`/`npm` references remain anywhere in the rig or the walkthroughs, and
`behavioral-smoke.sh` still exits 0 across all five lessons.

The four `walkthrough-snapshots/*/node-test.txt` files were **deleted**: the scripts now
emit `test-output.txt`, so nothing regenerated them and their contents (Node runner
glyphs) were provably stale. This is removal of orphaned artifacts, not the forbidden
act of editing a snapshot to match stale prose.

## Round 3 — snapshot regeneration attempted; L1 done, the rest genuinely blocked

### A blocker claim of mine was wrong and is retracted

Round 2 closed by asserting that an unrelated live `factory-demo` city blocked live
walkthrough runs. **That was incorrect.** Isolating each step disproved it: both
`cleanup_walkthrough_state.sh status` and `clean --kill` complete in **0s**, and `gc`
warns but explicitly continues when a second city is registered
("Continuing (stdin is not a terminal...)"). The real cause of the earlier hangs was the
tool timeout killing the backgrounded process group — launching detached with
`( nohup ... & )` and polling in separate calls works. `setsid` does not exist on macOS.

**L1 then completed in roughly 90 seconds, not the 15-30 minutes estimated.**

### L1 snapshots regenerated and verified

`L1.sh` makes **zero** `gc sling` calls, so this cost no model tokens. Verified after the
run:

- `test-output.txt` now holds real pytest output (`2 passed`), replacing the deleted
  `node-test.txt`
- `PROJECT_MANIFEST.md` is now the `ADR-005` template — 5 matches for
  FastAPI/SQLAlchemy/pytest, **0** for the old `Frontend` row
- `CLAUDE.md` is the Python rig's

### The remaining four lessons are blocked by a provider defect, not by environment

A live `L2` run timed out at 1800s and halted the chain. The Planner did not fail to
work — it produced a well-formed plan with the required `## Goal` / `## User Stories` /
`## Acceptance Criteria` sections, and the Architect produced its artifact too. **Both
wrote to the city root instead of the project rig:**

| | Path |
|---|---|
| `L2.sh:153` polls | `.../L2/rig/docs/plans/*.md` |
| Planner wrote | `.../L2/my-factory/docs/plans/calculator-memory.md` |

Ruled out as causes, by inspection rather than assumption: the L2 planner/architect
prompts were never modified by this work; L2 receives no `PROJECT_MANIFEST.md` at all, so
the rewritten template cannot have influenced it; and the rig's language does not affect
city-vs-rig resolution. Prior L2 snapshots prove artifacts previously did land in the rig.

### Round 4 — the provider hypothesis was tested and refuted

Rather than leave "run L2 under `provider = claude`" as a recommendation, it was executed.
Doing so first required fixing a harness defect: `_common.sh` documents a `WALK_PROVIDER`
override and even ships a `claude` auth probe, but `L2.sh`/`L3.sh`/`L4.sh`/`C1.sh` each
**hardcoded** `provider = "opencode"` into the `city.toml` they generate, so the knob was
inert. All four now emit `${WALK_PROVIDER:-opencode}`, verified to still default to
`opencode`.

Under `claude` the failure was **different**, which refutes the provider explanation:
no artifact appeared in *either* directory, the wait oscillated between
`session=creating` and `session=missing`, and `gc session list` showed only
`rig/core.control-dispatcher` — the `factory.planner` session was **never created**.

The shared resource turned out to be the tmux socket. `tmux -L factory ls` lists only
`factory-demo`'s day-old sessions (`ascii-art--factory__manager`, `mayor`); the
walkthrough's planner session never appears there. `gc register` warns it may escalate to
a non-graceful supervisor respawn "which cycles those cities' in-flight work", then
continues.

So Round 2's retraction over-corrected. Both statements are true: `factory-demo` does
**not** block `gc` commands (cleanup and queries return in seconds), but it **does**
prevent reliable agent-session creation. Article X's prohibition on concurrent chains
applies more broadly than "don't start two walkthroughs" — any other live factory on the
machine is effectively a second chain.

Recorded in
`vault/Discoveries/2026-08-17-live-agent-sessions-unreliable-with-co-registered-factory.md`,
which supersedes and replaces the earlier note that blamed OpenCode.

`L3`/`L4`/`C1` were deliberately **not** run: same first gate, ~30 minutes and real tokens
each for a predictable result. Neither failed chain corrupted anything — both halted
before `save_all_artifacts`, and the `L2`/`L3`/`L4`/`C1` snapshot files remain
byte-identical.

## Outstanding

- **Snapshot regeneration for L2/L3/L4/C1 is blocked on machine state, not on this stack
  change.** While the `factory-demo` city is registered and its tmux sessions are live,
  agent sessions for a walkthrough city do not reliably start or survive. Unblocking is a
  human decision — stop the `factory-demo` factory (out of bounds for an agent under the
  `clean-walkthrough-runs` rules) or regenerate on a machine with no other registered
  city. Once clear, L1 is free to re-run and L2/L3/L4/C1 cost real tokens.
- **The `claude` auth probe in `_common.sh` is broken and should be fixed.**
  `claude auth status` is not a subcommand; the CLI answers it as a prompt and exits 0, so
  the probe passes unconditionally and spends tokens on every preflight.
- Whether the OpenCode city-root artifact write is an independent defect or just a
  consequence of mid-work session drain is **unresolved** and needs one clean run to
  isolate. It should not be cited as a known OpenCode bug until then.
- `walkthrough-snapshots/L4/PROJECT_MANIFEST.md` remains the pre-`ADR-005` template. It
  is regenerated by `L4.sh`, so it was deliberately left untouched rather than
  hand-edited. L1's equivalent is now correct.
- The two harness defects from Round 1 (broken documented lint invocation; pre-commit
  blocked on a fresh clone) are still unfixed and still only flagged.
- The converted rig pins `requires-python = ">=3.11"` and uv resolved CPython **3.14.3**
  for it, while `ENGINEERING_STANDARD.md` specifies `>=3.11,<3.14`. Harmless today
  because the rig is harness-internal and its tests pass, but the two should be
  reconciled.
