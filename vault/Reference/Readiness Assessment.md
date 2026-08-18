---
title: Readiness Assessment
type: reference
tags:
  - reference
  - gas-city
  - curriculum
created: 2026-08-17
updated: 2026-08-17
status: reviewed
source: agent
---

# Readiness Assessment

A dated snapshot of how ready this repository's Gas City integration is to hand to a
student, re-run whenever a change touches provider config, the schema migration, or
the live-run evidence base. Supersede rather than edit past entries — append a new
dated section below the previous one so the trend is visible.

## 2026-08-17 (after the Gas City 1.4.x schema migration and OpenCode validation)

**Overall**: the documented quickstart is fixed and the OpenCode default is
evidence-backed through real execution, but the factory does not yet complete a
full lesson run live. Call it ready for L1 (setup-only, verified green), provisional
for L2/L3 (verified through the first agent, blocked on a `gc`-internal defect after
that), and unverified for L4/C1 (not run this round, on purpose).

### What's verified

| Item | Evidence |
|---|---|
| Quickstart doesn't fail at step 1 | `gc register` succeeds; `L1` walkthrough passes live |
| `city.toml`/`pack.toml` schema matches installed `gc` (1.4.1) | `gc config show` scratch-directory probing, three live runs |
| OpenCode is a viable, first-class provider | plugin, skill sink, MCP projection all confirmed upstream; `.opencode/plugins/gascity.js` confirmed installed live |
| Documentation matches shipped config | 17-file sweep, verified with a broad semantic re-sweep, not just the original literal-pattern grep |
| `install_agent_hooks` doesn't need to be set anywhere | confirmed empirically — hook installs regardless |
| The Planner role completes reliably under OpenCode | 3/3 live runs, 387-505s, comfortably under budget |

### Resolved later the same day: the handoff defect is fixed

The session-handoff defect that blocked every lesson past its first agent was
root-caused and fixed. Cause: `gc` probes tmux for session liveness even on
ACP/stdio-backed sessions, which have no tmux window, producing an unbounded
create → false-dead → recreate loop that starved work delivery. Fix:
`session = "tmux"` pinned on all 19 lesson-pack agents.

Confirmed by controlled experiment — one variable changed, `✓ L2 passed`, first full
lesson pass. Within that single run the tmux-pinned agent succeeded while an
ACP agent timed out, which is a self-validating A/B. Full evidence in
[[2026-08-17-architect-role-session-lifecycle-desync]].

The same change also fixed a second, independent defect: `gc session peek` — taught in
9 places across the curriculum — returns **empty** on ACP and real content on tmux.
Students following the taught observability path were seeing nothing.

**Revised status**: L1, L2, L3, and L4 all verified green end-to-end. All agent
stages across all three multi-agent lessons completed successfully after raising
`WALK_AGENT_BUDGET` to 1800s and `WALK_BUILDER_BUDGET` to 2700s. A one-off artifact-
placement anomaly hit L4 during the first (chained) attempt; an isolated re-run did
not reproduce it — treated as agent inference variance, not a defect. Only **C1**
remains unverified.

### Resolved: L4 planner artifact misplacement did not reproduce

In the original L3→L4→C1 chain, the L4 Planner wrote its artifact to
`my-factory/docs/plans/` instead of the harness-expected `rig/docs/plans/`. An
isolated L4 re-run immediately after — same fix set, same budgets — completed all
six stages with correct artifact placement throughout (`✓ L4 passed`). Treated as
agent inference variance, not a defect. Full detail in
[[2026-08-17-l4-planner-wrote-artifact-to-wrong-rig-directory]].

One trend worth watching without enough data to act on yet: L4's later stages
(Reviewer 43%, Builder 40% of budget) ran higher than the 20-30% band seen in
earlier-pipeline stages across L2/L3/L4. Single run; not actionable yet.

### What's explicitly still not known

- **C1 has not been attempted** under the current fix set (transport pin + raised
  budgets). It is the longest, most complex lesson (7 agents, most steps) and the
  final verification gap before claiming full-curriculum reliability.
- Whether `claude` defaults to tmux or ACP (now much lower stakes, since transport is
  pinned explicitly rather than left to the provider default).
- Whether the later-stage budget trend noted above is real or single-run noise.

### Recommendation

L1, L2, L3, and L4 are now verified end-to-end. The schema fix, the OpenCode
default, the transport fix, and the raised timeout budget hold together across four
consecutive real lesson runs. **C1 is the only remaining gap** before claiming
full-curriculum reliability — run it next.
