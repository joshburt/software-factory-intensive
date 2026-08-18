---
title: C1 Release Gate Failed Due to a Concurrent Walkthrough Chain (Not a Defect)
type: discovery
tags:
  - discovery
  - walkthrough
  - gas-city
created: 2026-08-17
updated: 2026-08-17
status: reviewed
source: agent
---

> [!attention] CORRECTION
> This note's root-cause framing — "a second walkthrough chain" — is too narrow and is
> **superseded** by
> [[2026-08-17-live-agent-sessions-unreliable-with-co-registered-factory]], written
> independently in a parallel work round. That note isolates the actual shared
> resource: agent sessions live on a **shared tmux socket**, so *any* other registered
> Gas City factory on the machine (not specifically another walkthrough) prevents
> reliable agent-session creation, reproduced under two different providers with two
> different symptoms each time. My working `factory` city — registered for the entire
> session, unrelated to any walkthrough — is therefore independently sufficient to
> explain the C1 failure; the other chain observed in `ps` at the same moment may have
> been a compounding factor rather than the sole cause. Original text kept below for
> the timeline; treat the other note as authoritative on mechanism.

# C1 Release Gate Failed Due to a Concurrent Walkthrough Chain (Not a Defect)

An isolated `C1` run failed at its final stage (Release Gate). Six of seven agents
completed successfully first. The cause is **not** a defect in the tmux transport
fix, the budget changes, or C1's pack — it is Article X's concurrency rule being
violated by a second, independently-running walkthrough chain that this session did
not launch.

## What happened

Ran `bash test-harness/tutorial-walkthrough.sh C1` in isolation
(`TUTORIAL_WALKTHROUGH_KEEP_SCRATCH=1`). Six stages completed normally:

| Stage | Time | % of budget |
|---|---|---|
| Planner | 429s / 1800s | 24% |
| Architect | 753s / 1800s | 42% |
| Designer | 652s / 1800s | 36% |
| Builder | 894s / 2700s | 33% |
| Validator | 696s / 1800s | 39% |
| Reviewer | 554s / 1800s | 31% |

Release Gate then went `asleep` with `REASON: city-stop`, alongside
`rig/core.control-dispatcher` — the supervisor's own control process — showing the
identical `city-stop` reason at the same moment. The tmux state cache reported
`no tmux server running`. `gc cities` subsequently showed the C1 walkthrough city
**not registered at all**, while the harness process was still alive and polling.
This is a whole-city teardown, not an agent-level failure — a live agent process
does not go `asleep` with reason `city-stop` while its own control-dispatcher
survives; here both died together.

## Root cause

While this run was in progress, `gc supervisor logs` showed a 404 storm: repeated
polls, every ~15s, against `sfi-walkthrough-L4-1787016303-84731` — a city from an
**earlier, already-cleaned-up run in this same session** (its scratch directory had
been deleted hours prior). A `ps` snapshot at the same time found a second,
independently-running walkthrough chain:

```
bash test-harness/tutorial-walkthrough.sh L1 L2 L3 L4 C1   (PID 18710)
  parent: bash test-harness/behavioral-smoke.sh            (PID 18582/18580)
```

This was not launched by this session. It was actively executing L2 at the moment
C1's release gate failed. This is exactly the scenario
`.claude/skills/clean-walkthrough-runs/SKILL.md` and Article X forbid: *"Never run
multiple live walkthrough chains at once. They share `gc` registry state and
`/tmp/sfi-tutorial-walkthrough`."* Two chains sharing one `gc` supervisor produced
supervisor confusion (the stale L4 polling loop) and, plausibly, a reconciliation
that stopped this session's C1 city.

## What I did and did not do

- Verified the other chain's processes were alive and untouched **before and after**
  running `clean-walkthrough-runs --clean --kill` — the skill's cleanup correctly
  scoped to this session's own dead/orphaned state and did not disturb the other
  chain (confirmed via `ps -p <pid>` on each of its process IDs immediately after).
- Did **not** retry C1. Article X — never run two live chains at once — makes a
  retry incorrect right now; the other chain was mid-run (observed at L3 shortly
  after).
- Preserved the failed C1 scratch (`1787024227-18088`) as evidence rather than
  cleaning it immediately.

## Constitutional status

Not a defect in this session's work. The tmux transport fix and the raised timeout
budgets are validated through six of seven C1 stages with no anomaly — the same
success pattern as L2/L3/L4. This is an **environmental interruption**, and Article
X's own text anticipates it: concurrent chains corrupt shared state, which is what
this looks like.

## Next step

Re-run `C1` in isolation once no other walkthrough chain is active. Check with
`.claude/skills/clean-walkthrough-runs/scripts/cleanup_walkthrough_state.sh status`
immediately before launching, not just at session start — a chain can start after
the initial check, as happened here.
