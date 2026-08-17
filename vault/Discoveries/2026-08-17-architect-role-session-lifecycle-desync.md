---
title: Architect Role Times Out — gc Session-Lifecycle Desync, Not Schema or Hooks
type: discovery
tags:
  - discovery
  - gas-city
  - walkthrough
created: 2026-08-17
updated: 2026-08-17
status: reviewed
source: agent
---

# Architect Role Times Out — gc Session-Lifecycle Desync, Not Schema or Hooks

Two independent live L2 walkthrough runs on the OpenCode provider (post-migration,
per ADR-003/ADR-004) both failed at the same step: the Architect agent times out
after 600s without producing `docs/architecture/*.md`. This is reproducible, and the
root cause is **not** the schema migration, **not** a missing lifecycle hook, and not
conclusively an OpenCode defect — it is a `gc` session-lifecycle desync.

## What did NOT fail

Both runs prove the schema migration (ADR-003) and the OpenCode provider default
(ADR-004) work correctly through real agent execution, not just `gc config show`:

- `gc register`, `gc rig add`, `gc --rig import remove/add factory`, `factory up`
  all succeeded on both runs.
- The Planner (OpenCode-backed) completed and produced a real artifact
  (`docs/plans/calculator-memory.md`) in both runs — 505s and 387s respectively, a
  ~30% spread, comfortably under the 600s budget both times.
- The `.opencode/plugins/gascity.js` lifecycle hook **is installed** — confirmed
  present on disk at
  `.gc/agents/rig/feature-intake-architect/.gc/agents/.../feature-intake-architect/.opencode/plugins/gascity.js`
  in the second run's preserved scratch. This rules out the hypothesis that removing
  `install_agent_hooks` from `city.toml.template` left agents unhooked — `gc`
  installs the plugin regardless of that (now-deprecated) workspace-level key.

## What did fail, and the evidence

Both runs: Architect transitions `start-pending` → `asleep`/`missing`, is polled
every 15s for 600s, and never produces its artifact. `gc supervisor logs` for the
second run shows the actual mechanism, repeated on every poll cycle:

```
idle-claim-nudge: factory__architect-swl19-wvc failed: agent "factory__architect-swl19-wvc"
  busy, timed out waiting for idle
session reconciler: confirming dead runtime session factory__architect-swl19-wvc:
  tmux -u: can't find window: factory__architect-swl19-wvc
```

Two independent gc subsystems disagree about the same session at the same moment:

- The **idle-claim-nudge** path believes the session is `busy` and refuses to
  deliver work to it (it waits for idle, times out, gives up).
- The **session reconciler** independently confirms the backing tmux window does
  not exist — the session is not busy, it is dead.

The work item is never delivered to a live process. This is a **state desync
between gc's session-busy tracking and its own tmux-backed reality**, not a model
latency problem and not a hook problem.

## What is still open

Two live data points is not enough to say whether this is OpenCode-specific or a
general `gc` session-lifecycle bug that happens to have surfaced on the Architect
role under this run's timing:

> [!question] UNDOCUMENTED
> Whether the same failure occurs on the `claude` provider is not established — no
> comparison run has been made. The mechanism (`tmux -u: can't find window`) is
> generic to gc's tmux-based session management and is not obviously
> OpenCode-specific, but the Planner (also OpenCode-backed) did not exhibit it in
> either run, so role, prompt size, or ordering may matter. Resolve by watching
> whether the same "busy but window-missing" pattern recurs on the Architect (or
> any role) across the pending L3/L4/C1 live runs, which exercise the same role
> under OpenCode again as a byproduct of already-planned work — no separate
> isolation test has been run yet.

## Constitutional status

This is a candidate `TODO(ENFORCE)`-class finding once resolved: Article XIII (every
verdict/step needs a defined consequence) arguably extends to "every session-busy
determination needs to agree with the runtime it claims to describe." Not filing a
new article for a single reproduction; tracking as a discovery until the pattern is
confirmed or ruled out across the remaining live runs.

## Relationship to ADR-004

ADR-004's revisit trigger names exactly this class of finding: "an OpenCode-specific
reliability or throughput problem" under sustained multi-agent load. This finding is
real and reproducible but not yet attributable to OpenCode specifically — the
`tmux -u: can't find window` mechanism could equally be a latent gc bug that
OpenCode's process lifecycle happens to trigger, or a general race independent of
provider. **Do not action the ADR-004 revisit trigger on this evidence alone.** Wait
for the L3/L4/C1 data points, which will show whether this is per-role, per-provider,
or intermittent.

## Cleanup performed

Both runs left registered `sfi-walkthrough-*` cities on failure; the first was
auto-cleaned by the harness itself (`TUTORIAL_WALKTHROUGH_KEEP_SCRATCH` was not set),
the second was cleaned via `clean-walkthrough-runs --clean --kill`, which also killed
one stray process. Verified after cleanup: no `sfi-walkthrough-*` cities registered,
no stray processes, the user's own `factory` city untouched, preserved scratch
directories removed.
