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

Three independent live walkthrough runs on the OpenCode provider (post-migration,
per ADR-003/ADR-004) — L2 run 1, L2 run 2, L3 run 1 — all failed at the same
structural point: the second agent in the formula chain (named `Architect` in both
lessons; step id `architecture`, `needs = ["plan"]` in both `packs/lessons/L2` and
`packs/lessons/L3` formulas) times out after 600s without producing
`docs/architecture/*.md`. 3/3 reproduction rate. The root cause is **not** the schema
migration, **not** a missing lifecycle hook, and is likely **not** OpenCode-specific
— it is a `gc` session-lifecycle desync tied to handoff position in the chain, not to
the Architect role's identity.

## What did NOT fail

All three runs prove the schema migration (ADR-003) and the OpenCode provider
default (ADR-004) work correctly through real agent execution, not just
`gc config show`:

- `gc register`, `gc rig add`, `gc --rig import remove/add factory`, `factory up`
  all succeeded on all three runs, across two different lesson packs.
- The Planner (OpenCode-backed) completed and produced a real artifact
  (`docs/plans/*.md`) in all three runs — 505s, 387s, and (implicitly, since L3
  reached the Architect wait) comfortably under budget a third time. ~30% timing
  spread across runs, all safely under the 600s budget.
- The `.opencode/plugins/gascity.js` lifecycle hook **is installed** — confirmed
  present on disk in the L2 run 2 scratch. This rules out the hypothesis that
  removing `install_agent_hooks` from `city.toml.template` left agents unhooked —
  `gc` installs the plugin regardless of that (now-deprecated) workspace-level key.

## What did fail, and the evidence

All three runs: the second agent transitions `start-pending`/`missing` →
`asleep`, is polled every 15s for 600s, and never produces its artifact.
`gc supervisor logs`, captured live during the L3 run, shows the identical
mechanism as L2 run 2, byte-for-byte, down to the log line shape (only the session
ID differs):

```
idle-claim-nudge: factory__architect-swl11-d55 failed: agent "factory__architect-swl11-d55"
  busy, timed out waiting for idle
session reconciler: confirming dead runtime session factory__architect-swl11-d55:
  tmux -u: can't find window: factory__architect-swl11-d55
```

Two independent gc subsystems disagree about the same session at the same moment:

- The **idle-claim-nudge** path believes the session is `busy` and refuses to
  deliver work to it (it waits for idle, times out, gives up).
- The **session reconciler** independently confirms the backing tmux window does
  not exist — the session is not busy, it is dead.

The work item is never delivered to a live process. This is a **state desync
between gc's session-busy tracking and its own tmux-backed reality**, not a model
latency problem and not a hook problem.

**New in the L3 run**: while the Architect step was waiting, `ps` showed two
concurrent `gc nudge poll --session factory__architect-...` processes for two
*different* session IDs (`-yvd` and `-d55`) running against the same city
simultaneously. This means gc had already churned through at least one prior
session attempt for this same step before the one that ultimately timed out —
session replacement/replay is itself part of the failure mode, not just a single
stuck session.

## RCA CORRECTION (same day, after root-cause analysis)

> [!warning] The "chain position" framing below was a correct *observation* with the
> wrong *mechanism*. A subsequent RCA identified the actual causal chain. Chain
> position only correlates; it is not causal. Read this section first — the two
> sections below it are retained for provenance but are superseded.

**Actual mechanism: work-delivery path, not chain position.**

Both agents run over ACP (stdio pipes), not tmux — proven by `gc session peek`
returning **empty for the Planner too**, in the very same runs where the Planner
succeeded. "No tmux window" is therefore not fatal and not distinguishing; it is
true of every agent in these runs.

What differs is how each agent receives its work:

| | Planner (step 1) | Architect (step 2+) |
|---|---|---|
| Session created by | `gc sling` (explicit, foreground) | supervisor pool scale-up (0→1) on graph advancement |
| Work delivered | at session creation / ACP handshake | *after* creation, via `idle-claim-nudge` |
| Outcome | succeeded 3/3 (went `asleep`, still produced artifact) | failed 3/3 |

The Planner already holds its prompt before any session churn can matter. The
Architect depends on post-creation nudge delivery, and that delivery never lands.

**Causal chain:**

1. Supervisor scales the second agent 0→1 and creates an ACP-backed session.
2. The session reconciler probes liveness with `tmux -u ... can't find window` — a
   **transport-inappropriate probe** for an ACP/stdio-pipe session, which by
   construction has no tmux window.
3. Reconciler concludes "confirming dead runtime session" and tears it down.
4. Pool controller still sees `poolDesired = 1`, `actual = 0` → creates a new
   session with a new ID. Observed directly: three distinct architect session IDs in
   L2 run 1 (`5jd`, `03j`, `wvc`), two concurrent `gc nudge poll` processes for two
   different IDs in L3 (`yvd`, `d55`).
5. Meanwhile `idle-claim-nudge` holds a reference to a session record that is being
   replaced. It reports `busy, timed out waiting for idle`, then once the process
   behind it is gone, `sending prompt to ...: write: write |1: file already closed`.
6. Loop repeats until the harness's 600s budget expires. The work is never delivered.

**Root cause statement:** a transport-inappropriate liveness probe (tmux window
check applied to ACP/pipe-backed sessions) causes an unbounded
create → false-dead → recreate loop, which starves the post-creation nudge
delivery path that every agent after the first depends on.

**Contributing factor:** two gc subsystems (`idle-claim-nudge` and the session
reconciler) make contradictory liveness determinations about the same session in the
same second, with no reconciliation between them — `busy` and `dead` simultaneously.
Either alone would be recoverable; together they deadlock.

**Provider attribution, corrected.** ACP is **not** OpenCode-exclusive: `claude`,
`codex`, `gemini`, and `cursor` all accept `session = "acp"` on gc 1.4.1 (verified by
scratch-city probe; validation confirmed to have teeth by checking that a bogus
transport value *is* rejected). So the defect is provider-agnostic *in mechanism*.
The remaining open variable is narrower than "is this OpenCode-specific": it is
**whether gc defaults to ACP for providers other than OpenCode**. No lesson agent
sets `session` explicitly, so the transport is gc's provider default in every case.
If claude defaults to tmux, the tmux probe would be correct for claude and this would
be OpenCode-specific *in practice* while remaining provider-agnostic *in principle*.

## CONFIRMED AND FIXED — controlled experiment

Set `session = "tmux"` on **only** the L2 architect, leaving the planner on the ACP
default as a control, and re-ran L2 live. Result: **`✓ L2 passed`** — the first full
lesson pass achieved. Root cause is confirmed, not merely correlated.

**Before vs after, same lesson, single variable changed:**

| Signal | ACP (default) | tmux (pinned) |
|---|---|---|
| Architect session states | `missing` → `asleep`, forever | `missing` → `creating` → **`active`** |
| Nudge delivery | `busy, timed out waiting for idle`, every cycle | `nudged ... to claim rig-6sf (attempt 1/3)` — **succeeded first attempt** |
| Reconciler | `confirming dead runtime session: tmux -u: can't find window` every cycle | **absent** |
| `gc session peek` | **empty** | returns the agent's live prompt and output |
| Artifact | never produced (3/3 timeouts) | `docs/architecture/calculator-memory.md`, 580s |
| Formula graph | stalled at step 2 | all steps closed incl. `Finalize workflow` |

`session=active` had never appeared in any prior run. The disappearance of both the
`busy` and `can't find window` lines together is the direct confirmation that the
transport-inappropriate probe was causal.

**The control validated itself.** The run's one remaining (non-fatal) timeout was the
*second* re-sling's **planner** — still on ACP, `session=asleep`, timed out at 600s.
So within a single run: tmux agent succeeded, ACP agent failed. That is as clean an
A/B as this harness can produce.

**Second defect fixed by the same change.** `gc session peek` is taught in **9 places**
across the curriculum (L2 calls it "Live view of what an agent is doing now"; W3 lists
it as a core observability tool; it's in the root README quickstart). On ACP it returns
empty, so a student following the taught path sees nothing and would reasonably
conclude their factory is broken. On tmux it returns real content. This is an Article IV
defect independent of the timeout bug, and it means pinning tmux is the *correct*
configuration for this curriculum rather than merely a workaround.

## Fix applied

`session = "tmux"` added to all **19** lesson-pack agents (L2=2, L3=4, L4=6, C1=7).
Placed per-agent rather than as a city-level `[agent_defaults]` one-liner, to keep packs
self-contained and portable per Article III — a student lifting a pack into their own
city gets the working transport with it. All 19 verified to parse and pin tmux; lint and
migration-check green.

Note this is the mirror image of the `install_agent_hooks` decision (which was
*declined* for these same 19 files). The reasoning is consistent, not contradictory:
config gets added when evidence demands it and withheld when it does not. There was no
evidence hooks were needed; there is direct experimental evidence tmux is.

## Residual risk

The architect completed in **580s against a 600s budget — 97%**. The fix works but has
almost no margin on this hardware. A slower machine, a slower model, or a larger prompt
would still time out. The budget should be raised (or made configurable) independently
of this fix; that is a separate concern from the transport bug and is not addressed here.

## Still worth reporting upstream

The gc-side defect is real regardless of this workaround: the session reconciler probes
tmux for ACP-backed sessions, and `idle-claim-nudge` and the reconciler assert
contradictory liveness (`busy` and `dead`) for the same session in the same second with
no reconciliation between them. Pinning tmux avoids the broken path; it does not fix it.

## Position, not role, is the common factor (SUPERSEDED — see RCA CORRECTION above)

`architecture` is step id 2 in both formula graphs, with `needs = ["plan"]`, in
both `packs/lessons/L2/formulas/mol-feature-intake.toml` and
`packs/lessons/L3/formulas/mol-feature-delivery.toml`. The failure is not "the
Architect role is broken" — it is "the second agent in a chain, immediately after
the first agent's handoff, fails to receive its wake/nudge reliably." This points at
gc's step-transition/handoff logic specifically, not at anything role-named or
prompt-specific.

## What is still open

> [!question] UNDOCUMENTED
> Whether the same failure occurs on the `claude` provider is not established — no
> comparison run has been made. The mechanism (`tmux -u: can't find window`) is
> generic to gc's tmux-based session management and is not obviously
> OpenCode-specific; a provider-agnostic gc handoff bug remains at least as likely
> an explanation as an OpenCode-specific one, given the signature is identical to
> ordinary tmux session bookkeeping and does not reference OpenCode, ACP, or the
> plugin at all. Resolving this conclusively would need one comparison run with
> `provider = "claude"` — not performed, on the judgment that 3/3 reproduction with a
> clear, gc-internal, provider-silent signature already outweighs the value of a
> 4th confirmatory run at further live-run cost. If resumed, this is the next
> concrete step.

## Decision: live-run track paused here

L4 and C1 were not run. Both share the same chain-position structure (a second
agent immediately following a first agent's handoff), so both would very likely
reproduce this identical failure at their own second step for no new diagnostic
value — the open question above is answered by a targeted comparison run, not by
more same-shaped reproductions. Continuing to spend live-run budget confirming an
already-3x-reproduced pattern would not be the minimum work that resolves the
outstanding question. What the pending L4/C1 runs were meant to validate (schema
migration, provider default) is already independently proven by all three
completed runs succeeding through registration, rig sync, and the first agent's
full execution.

## Constitutional status

This is a candidate `TODO(ENFORCE)`-class finding once resolved: Article XIII (every
verdict/step needs a defined consequence) arguably extends to "every session-busy
determination needs to agree with the runtime it claims to describe." Not filing a
new article for a `gc`-internal defect outside this repository's control; tracking
as a discovery.

## Relationship to ADR-004

ADR-004's revisit trigger names "an OpenCode-specific reliability or throughput
problem" under sustained multi-agent load as its downgrade condition. This finding
does not meet that bar: it is reproducible and real, but its signature is
provider-silent and its common factor is chain position, not OpenCode identity, so
it is at least as consistent with a general `gc` bug as with an OpenCode defect.
**The ADR-004 revisit trigger is not actioned on this evidence.** ADR-004 is updated
instead to disclose this open, orthogonal reliability finding rather than let its
"provisional on live runs passing" language stand as if runs had cleanly passed.

## Cleanup performed

All three runs left registered `sfi-walkthrough-*` cities on failure; run 1 was
auto-cleaned by the harness itself (`TUTORIAL_WALKTHROUGH_KEEP_SCRATCH` was not
set), runs 2 and 3 were cleaned via `clean-walkthrough-runs --clean --kill`, each of
which also killed one stray process. Verified after each cleanup: no
`sfi-walkthrough-*` cities registered, no stray processes, the user's own `factory`
city untouched throughout, preserved scratch directories removed.
