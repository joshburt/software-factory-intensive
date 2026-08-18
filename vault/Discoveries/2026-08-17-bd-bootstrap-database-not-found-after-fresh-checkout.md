---
title: bd bootstrap Leaves the Database Unreachable on a Fresh Checkout
type: discovery
tags:
  - discovery
  - beads
  - drift
created: 2026-08-17
updated: 2026-08-17
status: draft
source: agent
---

# bd bootstrap Leaves the Database Unreachable on a Fresh Checkout

Attempting to file this round's remaining backlog as `bd` beads (Article XV) surfaced
a separate, real problem unrelated to anything else in this round: on a fresh
checkout, `bd`'s own documented first-run path does not produce a working database.

## Reproduction

This checkout is genuinely a fresh one for `bd` purposes — `.beads/{README.md,
config.yaml, metadata.json}` are tracked (per this repo's own `.gitignore` rule
and the constitution's Article XV/Additional Constraints), but `.beads/dolt/` (the
actual Dolt data) is gitignored and had never been created locally.

```
$ bd create "..."
Error: failed to open database: Dolt server unreachable at 127.0.0.1:24126:
  dial tcp 127.0.0.1:24126: connect: connection refused
```

Followed the tool's own suggested path in order:

1. `bd dolt start` → server starts (confirmed via `bd dolt status`).
2. `bd create "..."` → `Error: failed to open database: database "sfi" not found
   on Dolt server`. Tool suggests `bd bootstrap`.
3. `bd bootstrap --dry-run` → `Bootstrap plan: create fresh database. Database: sfi`
   — looked correct and safe (no remote, nothing existing to conflict with).
4. `bd bootstrap` → `Created fresh database with prefix "sfi"`.
5. `bd create "..."` → **same error, database "sfi" not found**, despite step 4
   reporting success.
6. `bd dolt stop && bd dolt start` (hypothesis: stale server didn't see the new
   database) → new PID confirmed, but **same error persists**.
7. Inspected `.beads/dolt-server.log`: at 15:44:09 the server logs
   `error="table not found: issues"` — meaning the database briefly existed and was
   queried, but had no schema. 40 seconds later: `unable to process ComInitDB:
   database not found: sfi` — the database is gone entirely, not just missing tables.
8. `bd dolt show` reports `✓ Server connection OK` and `Database: sfi` throughout —
   the client-side config believes everything is fine while the server-side state
   disagrees.

## What this looks like

A directory-layout or timing mismatch between what `bd bootstrap` creates and what
the already-running `dolt sql-server` process expects to find as a named database —
plausibly the bootstrap wrote a Dolt repo at the data root itself rather than in a
`sfi`-named subdirectory the multi-database server process scans for, though this was
not confirmed by reading Dolt's server source. Not investigated further: the tool
also distinguishes `bd bootstrap` (existing-project recovery) from `bd init`
(brand-new project, no existing data) as the correct path for exactly this
situation, and this checkout matches "brand-new" — but `bd init` creates a new
`.beads/` directory, and this repo's `.beads/{config.yaml,metadata.json,README.md}`
are already tracked and present. Attempting `bd init` risked an unpredictable
interaction with those tracked files, for a side investigation outside this round's
actual authorized scope. Stopped there rather than guess further.

## Resolution

Not resolved. `bd dolt stop` run to leave no server process running. Verified
`git status --short .beads/` is empty — nothing tracked was touched; only the
gitignored `.beads/dolt/` data directory (created by the bootstrap attempt) exists
locally now, harmlessly.

This round's remaining backlog is recorded durably regardless: in full, with the
same task descriptions that were meant for `bd create`, in
`vault/Sessions/2026-08-17-gas-city-schema-migration-and-opencode-validation.md`'s
Open Questions section, and traceable from there to each item's own Discovery or
Decision note. Article XV's substance (durable, non-lossy memory) is satisfied even
though its letter (use `bd`, not a list) could not be, because `bd` itself was not
functional in this checkout for a reason outside this round's scope.

## Next step if resumed

Try `bd init --database sfi` (per `--help`: "specify an existing server database
name, overriding the default prefix-based naming... useful when an external tool has
already created the database") against the already-bootstrapped `.beads/dolt/`
directory, rather than a second `bd bootstrap`. If that also fails, this is worth
reporting upstream to the `beads` project with the exact repro above.
