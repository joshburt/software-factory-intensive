---
title: Upstream Issues
type: reference
tags:
  - reference
  - gas-city
  - beads
created: 2026-08-17
updated: 2026-08-17
status: draft
source: agent
---

# Upstream Issues

Defects in dependencies this repository does not control, which affect the
curriculum. Tracked here so their status can be followed and so local workarounds
can be removed when the upstream fix lands — a workaround with no tracking record
becomes permanent by accident.

**Update this file when**: an issue is filed upstream (add the URL), a new upstream
release is adopted (re-run the detection test, update Status), or a workaround is
removed.

## Status summary

| ID | Dependency | Severity | Status | Local workaround in place |
|---|---|---|---|---|
| [[#GC-1]] | Gas City `gc` 1.4.1 | **High** — blocks every lesson past its first agent | Open, not yet filed | Yes — `session = "tmux"` on all 19 lesson agents |
| [[#GC-2]] | Gas City `gc` 1.4.1 | Low — cosmetic/config hygiene | Open, not yet filed | No — deprecation warnings tolerated |
| [[#BD-1]] | Beads `bd` 1.2.2 | Medium — blocks `bd` use in a fresh checkout | Open, not yet filed | No — backlog recorded in vault instead |

---

## GC-1 — Session reconciler probes tmux for ACP-backed sessions

**Affects**: `gc` 1.4.1 (and 1.4.0 — reproduced identically on both).
**Impact on us**: every agent after the first in a formula chain never receives its
work. 3/3 reproduction across two lesson packs before the workaround.

### Summary

`gc` supports two per-agent session transports (`session = "acp"` / `"tmux"`, or
omitted to take the provider default). When a session is ACP-backed (stdio pipes),
the session reconciler nevertheless probes liveness by looking for a **tmux window**.
An ACP session has no tmux window by construction, so the probe always fails and the
reconciler declares a healthy session dead. The pool controller then recreates it,
and the cycle repeats indefinitely, starving the `idle-claim-nudge` path that delivers
work to any agent created by pool scale-up.

### Evidence

Two gc subsystems assert contradictory liveness for the same session in the same
second, with no reconciliation between them:

```
idle-claim-nudge: factory__architect-swl19-wvc failed: agent "factory__architect-swl19-wvc"
  busy, timed out waiting for idle
session reconciler: confirming dead runtime session factory__architect-swl19-wvc:
  tmux -u: can't find window: factory__architect-swl19-wvc
```

Then, once the process behind the stale record is gone, the pipe write fails —
confirming the transport really was ACP/stdio, not tmux:

```
acp: readLoop exit: read |0: file already closed
idle-claim-nudge: ... sending prompt to "factory__architect-swl19-wvc":
  write: write |1: file already closed
```

Session churn is directly observable: three distinct session IDs for one step in one
run (`5jd`, `03j`, `wvc`), and two concurrent `gc nudge poll` processes for two
different session IDs in another.

### Why the first agent in a chain is unaffected

The first agent is created by an explicit `gc sling`, which delivers its prompt at
session creation. It therefore does not depend on post-creation nudge delivery and
completes even while the churn happens around it. Every subsequent agent is created
by pool scale-up (0→1) on graph advancement and *must* receive work via
`idle-claim-nudge` — which never lands. This is why the defect looks like "the second
step is broken" rather than "ACP is broken."

### Minimal reproduction

1. `gc` 1.4.1, a provider whose default transport is ACP (observed with `opencode`).
2. A two-step formula graph, `step2.needs = ["step1"]`, distinct agents, each with
   `min_active_sessions = 0` and `wake_mode = "fresh"`, and **no** explicit `session`
   key (so transport is the provider default).
3. Sling step 1. It completes and writes its artifact.
4. Step 2's agent cycles `missing` → `asleep` indefinitely and never produces its
   artifact. `gc supervisor logs` shows the contradictory pair above on every cycle.

### Secondary symptom (independently user-visible)

On an ACP-backed session, `gc session peek` returns **empty** — it is a tmux
operation. This is not just an internal inconsistency: `gc session peek` is a
documented, user-facing observability command, so on an ACP transport it silently
reports nothing for a perfectly healthy agent.

### Suggested fix (upstream)

1. Make the liveness probe transport-aware: probe the ACP process/pipe for ACP
   sessions rather than querying tmux.
2. Reconcile the two liveness authorities. `idle-claim-nudge` reporting `busy` while
   the reconciler reports `dead` for the same session is unrecoverable by design;
   whichever is authoritative should be the single source.
3. Make `gc session peek` transport-aware (or state plainly that it is tmux-only).

### Our workaround

`session = "tmux"` pinned explicitly on all 19 lesson-pack agents
(`packs/lessons/{L2,L3,L4,C1}/agents/*/agent.toml`). This avoids the broken path
entirely and additionally restores `gc session peek`, which the curriculum teaches in
9 places. Confirmed by controlled experiment — see
[[2026-08-17-architect-role-session-lifecycle-desync]].

### Detection test — how we will know it is fixed

Remove `session = "tmux"` from one lesson agent (the L2 architect is the cheapest),
then run:

```bash
bash test-harness/tutorial-walkthrough.sh L2
```

- **Still broken**: architect cycles `missing` → `asleep`, times out, and
  `gc supervisor logs` shows the `busy` + `can't find window` pair.
- **Fixed**: architect reaches `active` and produces `docs/architecture/*.md`, and
  `gc session peek` returns content on the ACP transport.

If fixed, remove the workaround from all 19 agents and record it here.

> [!question] UNDOCUMENTED
> Not filed upstream yet. Also unverified: whether providers other than `opencode`
> default to ACP. All of `claude`, `codex`, `gemini`, and `cursor` *accept*
> `session = "acp"` on 1.4.1, so the defect is provider-agnostic in mechanism, but
> which providers *default* to ACP was never established. Lower stakes now that
> transport is pinned explicitly rather than inherited.

---

## GC-2 — Deprecated config surfaces still warned on with no migration path

**Affects**: `gc` 1.4.1. **Impact on us**: warning noise; no functional failure.

`gc config show` warns that `workspace.name` and `workspace.install_agent_hooks` are
deprecated in v2 (belonging in `.gc/site.toml` and per-agent `agent.toml`
respectively), but:

- `gc` provides no `migrate`/`upgrade` subcommand to perform the move.
- The warning hedges (`run gc doctor --fix if this is the root city.toml`), leaving it
  unclear whether `doctor --fix` handles it for the scratch cities the harness creates.

Related but distinct: `gc` 1.4.x **hard-errors** on `[defaults.rig.imports]` in
`pack.toml` (it belongs in `city.toml`). That one we have already migrated — see
[[ADR-003-Migrate-Rig-Imports-To-City-Toml]] — and it is *not* an upstream bug, just
an unannounced schema change with no migration tooling.

Our state: `workspace.name` deliberately not migrated (see
[[2026-08-17-workspace-name-deprecated-to-gc-site-toml]]);
`workspace.install_agent_hooks` removed rather than relocated, since the live runs
proved it is unnecessary.

---

## BD-1 — `bd bootstrap` leaves the database unreachable on a fresh checkout

**Affects**: `bd` 1.2.2. **Impact on us**: `bd` unusable in this checkout, so durable
work items could not be filed there.

Full reproduction and diagnosis in
[[2026-08-17-bd-bootstrap-database-not-found-after-fresh-checkout]]. Short version:
`bd bootstrap` reports `Created fresh database with prefix "sfi"`, but every
subsequent `bd` command fails with `database "sfi" not found on Dolt server`, and the
server log shows the database briefly existing without a schema
(`table not found: issues`) before disappearing entirely. Surviving a full
`bd dolt stop && bd dolt start`.

Next step if resumed: try `bd init --database sfi` against the already-bootstrapped
`.beads/dolt/` directory rather than a second `bd bootstrap`.
