---
title: ADR-003 Migrate Rig Imports From pack.toml to city.toml
type: decision
tags:
  - decision
  - gas-city
  - curriculum
  - drift
created: 2026-08-17
updated: 2026-08-17
status: reviewed
source: agent
---

# ADR-003: Migrate Rig Imports From pack.toml to city.toml

## Context

The documented student quickstart failed at its first command on the installed Gas
City (confirmed on both 1.4.0 and 1.4.1 — see
`vault/Discoveries/2026-08-17-quickstart-broken-pack-toml-rig-imports.md` for the
full reproduction):

```
gc register: city failed to start: parsing city pack.toml:
  [defaults.rig.imports] belongs in city.toml, not pack.toml
```

`my-factory/pack.toml.template` (unmodified since before this work round) placed
`[defaults.rig.imports.factory]` in `pack.toml`. The version hypothesis was tested
directly and disproven: 1.4.1 rejects the identical shape. This is an intentional
Gas City schema change with no first-party migration tool (`gc` has no `migrate` or
`upgrade` subcommand).

Direct schema probing against `gc config show` on scratch cities (no registration, no
tokens) established the correct target shape empirically rather than by guessing:
`[defaults.rig.imports.factory]` belongs in `city.toml`; a `[providers.<name>]`
catalog entry is also required (this affects every provider, not just OpenCode);
`workspace.name` and `workspace.install_agent_hooks` are both deprecated in favor of
`.gc/site.toml` and per-agent `agent.toml` respectively.

## Decision

Move `[defaults.rig.imports.factory]` from `pack.toml` to `city.toml` everywhere it
is defined or taught in this repository:

- `my-factory/pack.toml.template` and `my-factory/city.toml.template`
- The inline config heredocs in `test-harness/walkthroughs/{L2,L3,L4,C1}.sh`
- The assertion in `test-harness/walkthroughs/L1.sh` that greps for the pack
  selection (was checking `pack.toml`; now checks `city.toml`)
- The stale `lesson-pack-lint.py` check `SFI112`, which asserted the import table
  belongs in `pack.toml` and would have silently validated the broken shape as
  correct for every future contributor
- All student-facing documentation teaching the old shape (tracked separately as the
  16-file docs sweep)

Do not attempt a `workspace.name` → `.gc/site.toml` migration or a per-agent
`install_agent_hooks` migration in the same change — both are separate, narrower
questions with their own decision needs (see Consequences and the vault backlog).

## Consequences

- **Easier**: `gc register` succeeds on the currently installed Gas City. The L1
  walkthrough is green and its snapshots are current.
- **Easier**: the lint rule that should have caught this regression now actually
  catches it — verified by reproducing the old broken shape in a scratch directory
  and confirming `SFI112` fires on it.
- **Harder**: the migration surface is larger than the naive doc-only count. The
  harness asserts the old shape too (`L1.sh` originally grepped `pack.toml`), so
  fixing only the templates without fixing the harness would have halted L1 at the
  same step for a different reason.
- **Harder**: 16 more student-facing documents still teach the old shape as of this
  writing and must be swept in the same effort to avoid an active Article IV
  violation (taught capability must match shipped behavior).

## Alternatives Considered

### Alternative 1: Pin an older `gc` version

Rejected. There is no first-party migration path forward from an old version, no
stated support window for old versions, and pinning defers the problem onto whoever
upgrades next rather than solving it. It also does not fix the underlying repo/tool
schema mismatch — it just delays the day it's discovered again.

### Alternative 2: Ship a compatibility shim (accept both shapes)

Rejected. `gc` itself is the wall here — it hard-errors on the old shape, so no shim
in this repository can make the old shape work. There is nothing to shim against.

### Alternative 3: Migrate only the templates, defer the harness and docs

Rejected during this same work round after the harness assertion was found. Fixing
only the templates would have moved the failure to a different line
(`L1.sh`'s `pack.toml` grep) rather than removing it, and left 16 documents actively
teaching a shape the shipped templates no longer use — an Article IV violation
introduced by the fix itself.

## Revisit Trigger

Revisit if Gas City ships a first-party config migration command, or if a future
schema version relocates rig imports again. If that happens, this ADR's approach
(probe the schema directly with `gc config show` in a scratch directory before
touching any shipped file) is the reusable part — repeat it rather than guessing from
error text alone.
