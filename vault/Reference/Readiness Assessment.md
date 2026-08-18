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

**Revised status**: L1 verified green. L2 verified green end-to-end. L3/L4/C1 now
expected to pass (same fix, same mechanism) but **not yet run** — that is the
remaining verification gap, not a known defect.

### What's explicitly still not known

- **L3/L4/C1 have not been run** since the fix. Expected to pass; unverified.
- **Timing margin is thin.** The architect completed at 580s against a 600s budget
  (97%). On slower hardware, a slower model, or with larger prompts this would still
  time out. The budget likely needs raising independently of the transport fix.
- Whether `claude` defaults to tmux or ACP (now much lower stakes, since transport is
  pinned explicitly rather than left to the provider default).

### Recommendation

The L2 pass is a genuine milestone: the schema fix, the OpenCode default, and the
transport fix now hold together through a complete real lesson run. But do not yet
claim "run C1 end-to-end" reliability — run L3, L4, and C1 first, and treat the 97%
timing margin as the most likely source of the next failure.
