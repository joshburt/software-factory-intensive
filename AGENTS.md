# Software Factory Intensive — Agent Guidelines

**Last updated**: 2026-08-17

How to work in this repository as an agent. This file is operational; the
constitution is normative. Where the two conflict, the constitution wins and
this file MUST be updated.

## Agent Behavioral Principles

Four principles govern how you reason before any project-specific rule applies.
If they conflict with anything else here, they win.

1. Don't assume. Don't hide confusion. Surface tradeoffs.
2. Minimum change that solves the problem. Nothing speculative.
3. Touch only what you must. Clean up only your own mess.
4. Define success criteria. Loop until verified.

> **Authority:** governance is defined by `.specify/memory/constitution.md`
> (v1.2.0, Articles I–XV). Read the articles relevant to your task before
> starting. Articles I, II, IV, and XIV are NON-NEGOTIABLE.

## Project Overview

This repository is a **curriculum, not a product**. It is a self-paced workshop
that teaches participants to build a software factory — a system of AI agents
that plan, architect, design, code, review, and release software continuously —
on the [Gas City](https://github.com/gastownhall/gascity) framework.

Nine sessions: four workshops (`W1`–`W4`, design/thinking), four labs
(`L1`–`L4`, hands-on build), one capstone (`C1`, full end-to-end run).

Two audiences are served by every change: the **student** who must be able to
follow the material successfully, and the **maintainer** who must keep the
material true. When those conflict, truth wins — a lesson that reads well but
does not work is a defect.

The single discipline the workshop exists to transfer: **change agent behavior
through config, not through ad-hoc prompting** (Article I).

## Where Truth Lives

| Source | What it holds |
|---|---|
| `.specify/memory/constitution.md` | **Supreme.** 15 articles, Additional Constraints, Development Workflow, Governance |
| `AGENTS.md` (this file) | Operational guidance for agent sessions; defers to the constitution |
| `vault/` | Maintainer memory — Decisions, Discoveries, Sessions (Article XV) |
| `bd` (Beads) | Work items and status — never markdown TODO lists |
| `test-harness/walkthrough-snapshots/<lesson>/` | **Ground truth** for what a lesson actually produces (Article IV) |
| `test-harness/lesson-contracts/*.toml` | Expected artifact shape per runnable lesson |
| `packs/README.md` | Binding pack authoring rules |
| `curriculum/*_TEMPLATE.md` | The manifest contract between a student's project and their agents (Article XI) |
| `troubleshooting/` | Student-facing failure-mode guides |
| `reference-project/fired-up-pizza/` | **Examples only.** Completed student deliverables — never a runtime dependency |

## Repository Structure

```text
software-factory-intensive/
├── .specify/            # Spec Kit: constitution, templates, scripts, workflows
├── .claude/skills/      # Maintainer skills (clean-walkthrough-runs, validate-lesson-content)
├── .agents/skills       # symlink -> ../.claude/skills
├── .opencode/commands/  # 10 speckit.*.md commands
├── .githooks/           # pre-commit (the only CI in this repo)
├── .beads/              # Beads issue tracking; Dolt DB is NOT git-tracked
├── vault/               # Maintainer memory (Article XV)
├── curriculum/          # Long-form walkthroughs: workshops/ labs/ capstone/
├── activities/          # Student deliverables + short instructions
├── packs/lessons/       # Self-contained factory packs: L2 L3 L4 C1
├── my-factory/          # City templates + quickstart
├── test-harness/        # Private QA tooling — NEVER referenced in student content
├── reference-project/   # Example project artifacts
└── troubleshooting/     # Failure-mode guides
```

## Agent Workflow

For non-trivial features, follow the Spec Kit flow in order:

```text
speckit.specify → speckit.clarify → speckit.plan → speckit.tasks
  → speckit.analyze → speckit.implement ⇄ speckit.converge
```

`speckit.implement` and `speckit.converge` form a **loop**: `converge` assesses
the codebase against the spec, plan, and tasks, and appends remaining unbuilt
work to `tasks.md` so `implement` can finish it. Keep looping until `converge`
finds no remaining work. **A feature is not done while `converge` still appends
tasks.**

Plans MUST include a Constitution Check gating Phase 0, re-checked after design.
Accepted violations go in the plan's Complexity Tracking table — never silently.

`.specify/workflows/speckit/workflow.yml` defines `review-spec` and `review-plan`
gates with `on_reject: abort`. **Do not remove or auto-approve them.** They are
this repository's own human-authority checkpoints.

## Verification

There is **no hosted CI**. The pre-commit hook and the harness are the entire
safety net. Enable the hook once:

```bash
git config core.hooksPath .githooks
```

The ladder, cheapest first — run the rungs your change warrants:

```bash
python3 test-harness/lesson-pack-lint.py          # static content architecture
bash test-harness/migration-check.sh              # structural invariants (~2s)
bash test-harness/tutorial-check.sh               # dry-run command flow
bash test-harness/behavioral-smoke.sh             # combined, no LLM tokens (~60s)
bash test-harness/tutorial-walkthrough.sh <lesson>  # live E2E, real tokens (~15-30min)
```

Live walkthroughs are deliberately excluded from the hook — they need
authenticated provider sessions. Run them for every affected lesson before a
release that touches lesson packs, walkthrough scripts, or the student command
path.

Rules that are not negotiable (Article VIII):

- `--no-verify` is an exception, not a workflow. A repeatedly flaking check gets
  **fixed**, not bypassed.
- **Never** delete, weaken, or narrow a failing check to get a pass.
- Report pre-existing failures explicitly; never absorb them silently or blame
  them on your change.
- **Never** run two live walkthrough chains at once — concurrent runs corrupt
  shared Dolt state and invalidate results (Article X). Clean up with
  `.claude/skills/clean-walkthrough-runs/`.

## Editing Curriculum

Walkthrough output outranks README prose. Whenever you touch a command, an
output block, or a stated deliverable, reconcile against
`test-harness/walkthrough-snapshots/<lesson>/` using the
`validate-lesson-content` skill.

- Fix the **curriculum text**. Never edit a snapshot to match a stale README.
- Lesson contracts change only when the teaching architecture changes.
- A taught capability the shipped pack lacks MUST be implemented or plainly
  disclosed (Article IV).

Hard boundaries for student-facing content (Article V):

- **Never** mention `test-harness`, `.githooks`, snapshots, walkthrough scripts,
  run IDs, scratch paths, `vault/`, or harness-only choices.
- **Never** use version-branded compound nouns — no `FormulaV2`, `PackV2`,
  `PacksV2`, `FormulasV2`. Use plain "formula" and "pack".

## Editing Lesson Packs

Pack internals must read like production factory definitions. **No prompt,
formula, command, or doctor check may tell an agent it is in a class, lab,
workshop, or lesson** (Article II). The directory name may carry the lesson ID;
the contents may not.

- Each lesson ships one complete factory under `packs/lessons/<lesson>/` with its
  own `agents/`, `formulas/`, `commands/`, `doctor/`, `pack.toml`. No shared
  composition layer (Article III).
- Agents are rig-scoped; routes are binding-qualified (`factory.planner`).
- The formula graph owns ordering. An agent MUST NOT create downstream beads,
  relabel work to advance a pipeline, or wake another agent (Articles VI, XIV).
- Stage labels are metadata for search and reporting — never the workflow engine.
- Every step declares target, dependencies, inputs, artifact path, close
  condition, and failure behavior (Article XII). Dependency closure is not
  success.
- A step that produces a verdict must have a defined graph consequence, or be
  explicitly declared advisory-only (Article XIII).
- Every agent prompt names the manifest section it treats as authoritative, and
  states its fallback when that section is absent (Article XI).

Banned patterns enforced by `lesson-pack-lint.py` — `SFI001`–`SFI008`: label
schedulers, label-queue polling, manual stage-labelled bead creation, legacy rig
include wiring, composition-pack dependencies, graph-worker-as-fragment,
nonexistent dependency-graph commands, workspace-scope terminology.

## Memory Vault

Durable maintainer reasoning lives in `vault/` (Article XV).

**At session start**: read `vault/index.md` for orientation, then scan
`vault/Decisions/` and `vault/Discoveries/` for prior decisions and known
constraints before touching a subsystem.

**Write a note when**:

- a curriculum-design or architectural decision is made with stated reasons
  → `vault/Decisions/ADR-NNN-Descriptive-Title.md`
- a non-obvious constraint, gap, or taught-vs-shipped conflict is found
  → `vault/Discoveries/`
- a work round concludes → `vault/Sessions/YYYY-MM-DD-topic.md` (append-only)

**Do not** write a note for routine mechanical work with no discovery and no
decision — git history covers it.

**During work with a human**, enrich incrementally. Write decisions the moment
they are made, not batched at the end. At the end of a round, do an enrichment
pass: add the session note, promote verified drafts, confirm every decision has a
note. When opening a PR, include the vault notes from that round in the changeset.

Required frontmatter on every note: `title`, `type`, `tags`, `created`,
`updated` — ISO dates, `updated` bumped on every edit. Tags MUST come from
`vault/_meta/tags.md`; add the tag there first.

Notes start at `status: draft`, `source: agent`. You MAY self-promote to
`status: reviewed` after verifying the note's claims in that same session. You
MUST NEVER set `status: canonical` — human-only.

Never invent content. Mark genuine gaps `> [!question] UNDOCUMENTED`, disagreeing
sources `> [!attention] CONFLICT` (both sides), and unverifiable notes
`> [!warning] STALE`. A stale note is worse than a missing one.

## Work Tracking

Use Beads for durable work. The Dolt DB is local-only; only `README.md`,
`config.yaml`, and `metadata.json` are git-tracked.

```bash
bd create "description"        # file work
bd list                        # what's open
bd show <id>                   # detail
bd update <id> --claim         # claim
bd update <id> --status done   # close
```

- Use `bd` for **all** durable task tracking — never markdown TODO lists.
- Work items and status → `bd`. Reasoning and history → `vault/`. Governance →
  the constitution. No loose `MEMORY.md` files.
- Don't auto-close or mutate a bead unless the work is genuinely complete.

## Naming Conventions

| Thing | Convention | Example |
|---|---|---|
| Session IDs | `W1`–`W4`, `L1`–`L4`, `C1` | `L3` |
| Curriculum guides | `curriculum/<type>/<ID>/README.md` + `PROMPT.md` | `curriculum/labs/L3/README.md` |
| Activities | `activities/<type>/<ID>/` | `activities/workshops/W2/` |
| Lesson packs | `packs/lessons/<lesson>/` | `packs/lessons/C1/` |
| Formulas | `mol-<purpose>.toml` | `mol-release-delivery.toml` |
| Route targets | binding-qualified | `factory.planner` |
| ADRs | `ADR-NNN-Descriptive-Title.md` | `ADR-001-Adopt-Constitution-And-Vault.md` |
| Session notes | `YYYY-MM-DD-topic-slug.md` | `2026-08-17-constitution-ratification-and-vault-adoption.md` |
| Agent artifacts | `docs/<kind>/<slug>.md` in the student rig | `docs/reviews/<slug>.md` |

Cross-references MUST be updated in the same change that moves a file.

## Commits

- **Commit only when explicitly asked.** Never commit or push on your own
  initiative.
- Loosely conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, with an
  optional `(#NN)` PR suffix.
- Constitution amendments are committed **separately**, as
  `docs: amend constitution to vX.Y.Z (description)`.
- Secrets never touch git. Credential material is denied by default in
  `.gitignore`; tracking any such file needs an explicit justified negation.

## Quick Reference

```bash
# Enable the quality gate (once)
git config core.hooksPath .githooks

# Fast feedback before committing
bash test-harness/behavioral-smoke.sh

# Full validation for one lesson (real tokens)
bash test-harness/tutorial-walkthrough.sh L3

# Student quickstart (from repo root, then my-factory/)
cp my-factory/pack.toml.template my-factory/pack.toml
cp my-factory/city.toml.template my-factory/city.toml
cd my-factory && gc register . && gc rig add ~/path/to/your-repo/ && gc doctor --fix

# Switch the active lesson factory
gc --rig <rig> import remove factory
gc --rig <rig> import add ../packs/lessons/L3 --name factory

# Run and observe
gc sling <rig>/factory.planner "<feature>" --on mol-feature-delivery
gc events --follow
gc session peek <rig>/factory.planner
```

## Known Open Items

Tracked in the constitution's Sync Impact Report, with detail in `vault/`:

- `TODO(ENFORCE-XI…XV)` — Articles XI–XV lack mechanical checks and rest on
  review discipline. Articles I–X are script-backed.
- `TODO(DEFECT-B1)` — human gates taught but not shipped. See
  `vault/Discoveries/2026-08-17-human-gates-taught-not-shipped.md`.
- `TODO(DEFECT-B3)` — L4 promises a loop-back edge that no formula has, and the
  release-gate verdict has no consumer. See
  `vault/Discoveries/2026-08-17-release-gate-verdict-has-no-consumer.md`.

Do not "resolve" a defect by deleting the teaching that exposes it (Article XIV).
