---
title: Live Agent Sessions Do Not Complete While an Unrelated Gas City Factory Is Registered
type: discovery
tags:
  - discovery
  - conflict
  - walkthrough
  - snapshot
  - gas-city
  - test-harness
  - enforcement
created: 2026-08-17
updated: 2026-08-17
status: reviewed
source: agent
---

# Live Agent Sessions Do Not Complete While an Unrelated Gas City Factory Is Registered

This note supersedes an earlier draft of mine that blamed the OpenCode provider for
writing artifacts to the wrong directory. Testing the second provider disproved that
framing. The accurate finding is broader and is recorded here with both observations.

## What was attempted

Article IV snapshot regeneration for the sling-bearing lessons, after the walkthrough rig
was converted to Python.

- **`L1` succeeded** in ~90s and its snapshots are correct. `L1.sh` makes **zero**
  `gc sling` calls, so it involves no live agent and no model tokens.
- **`L2` failed under both providers**, in two *different* ways.

## Observation 1 — `provider = "opencode"`

The run timed out at 1800s. The Planner *did* work: it produced a well-formed plan with
the required `## Goal` / `## User Stories` / `## Acceptance Criteria` sections, and the
Architect produced its artifact too. Both landed in the wrong directory.

| | Path |
|---|---|
| `L2.sh:153` polls | `.../L2/rig/docs/plans/*.md` |
| Planner wrote | `.../L2/my-factory/docs/plans/calculator-memory.md` |
| Architect wrote | `.../L2/my-factory/docs/architecture/calculator-memory.md` |

`my-factory/` is the city root — the agent's working directory. The event log recorded
`session.stopped subject=rig/factory.planner msg=drain acknowledged by agent`, i.e. the
session was **drained mid-work**.

## Observation 2 — `provider = "claude"`

Re-run with `WALK_PROVIDER=claude`. Preflight passed (`claude CLI on PATH`,
`claude CLI authenticated`) and the formula attached correctly. Then:

- **No artifact appeared in *either* location** — not the rig, not the city root.
- The wait state oscillated between `session=creating` and `session=missing` for 780s+.
- `gc session list` showed only `rig/core.control-dispatcher` active — and notably its
  `WORKDIR` was correctly `.../L2/rig`. **The `factory.planner` session was never
  created at all.**
- The event log contained **no** `factory.planner` events whatsoever, only repeated
  `session.woke subject=rig/core.control-dispatcher`.

So the provider is **not** the variable that explains the failure. Under one provider the
planner ran and was drained; under the other it never started.

## The shared resource

Both runs happened while an unrelated city was registered:

```text
$ gc cities
NAME                                 PATH
factory                              /Users/joshburt/Workbench/Repositories/factory-demo/factory
sfi-walkthrough-L2-1787038510-26864  /tmp/sfi-tutorial-walkthrough/.../L2/my-factory
```

The `factory-demo` city has been running for over a day. Critically, agent sessions live
on a **shared tmux socket**:

```text
$ tmux -L factory ls
ascii-art--factory__manager: 1 windows (created Sun Aug 16 16:11:42 2026)
mayor:                       1 windows (created Sun Aug 16 16:11:42 2026)
```

Both of those belong to `factory-demo`. The walkthrough's planner session never appears
on this socket.

`gc register` warns about this at registration time, verbatim from the run log:

> Reload normally uses a graceful socket reload (same supervisor PID), but escalates to a
> non-graceful kill-and-respawn if the supervisor is absent, drifted, or in a zombie
> state — which cycles those cities' in-flight work.
> Continuing (stdin is not a terminal; pass `--yes` to silence this notice in scripted
> contexts).

It warns and proceeds. It does **not** block, and ordinary `gc` commands stay responsive
— `gc cities`, `gc session list`, and the cleanup script all return in seconds. What does
not survive is **agent session creation and retention**.

## Conclusion

Article X's rule — "Live walkthrough chains MUST NOT be run concurrently" — is usually
read as "don't start two walkthroughs." The operative condition is broader: **any other
live Gas City factory on the same machine is effectively a second concurrent chain**,
because supervisor and tmux socket state are shared.

While `factory-demo` is live, no sling-bearing lesson (`L2`, `L3`, `L4`, `C1` — 6, 5, 5,
and 4 `gc sling` calls) can produce trustworthy Article IV snapshot evidence.

`L3`/`L4`/`C1` were deliberately not attempted after `L2` failed twice: same first gate,
~30 minutes and real tokens each for a predictable result. No snapshots were corrupted —
both failed chains halted before `save_all_artifacts`, and `L2`/`L3`/`L4`/`C1` snapshot
files remain byte-identical.

> [!question] UNDOCUMENTED
> Whether the OpenCode city-root write in Observation 1 is an independent provider defect
> or purely a consequence of being drained mid-work cannot be determined while the
> contention exists. It needs one clean run on a machine with no other registered city.
> Until then, treat it as unexplained rather than as a known OpenCode bug.

## Two harness defects found along the way

1. **`WALK_PROVIDER` was documented but inert.** `_common.sh:532-534` states "Override
   with WALK_PROVIDER to test another" and the preflight honors it, including a dedicated
   `claude` auth probe — but `L2.sh`, `L3.sh`, `L4.sh`, and `C1.sh` each **hardcoded**
   `provider = "opencode"` plus a `[providers.opencode]` block into the `city.toml` they
   generate, so the documented knob never reached the actual run. **Fixed** in this
   session: all four now emit `${WALK_PROVIDER:-opencode}`, verified to still default to
   `opencode`.

2. **The `claude` auth probe cannot fail, and costs tokens.** `_common.sh` probes with
   `claude auth status >/dev/null 2>&1`. `auth status` is not a `claude` subcommand — the
   CLI treats the words as a *prompt* and answers conversationally, exiting 0. So the
   probe reports "claude CLI authenticated" unconditionally, cannot detect an
   unauthenticated CLI, and spends model tokens on every preflight. Not fixed; needs a
   real non-interactive auth check.
