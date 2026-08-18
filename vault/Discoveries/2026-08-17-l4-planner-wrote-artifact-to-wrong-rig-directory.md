---
title: L4 Planner Wrote Its Artifact to my-factory/ Instead of rig/ (Did Not Recur)
type: discovery
tags:
  - discovery
  - gas-city
  - walkthrough
  - drift
created: 2026-08-17
updated: 2026-08-17
status: reviewed
source: agent
---

# L4 Planner Wrote Its Artifact to my-factory/ Instead of rig/ (Did Not Recur)

## Follow-up: isolated re-run did NOT reproduce this

Ran `L4` in isolation immediately after (not chained with L3/C1), same fix set
(`session = "tmux"`, `WALK_AGENT_BUDGET=1800`). Result: **`✓ L4 passed`**, all six
stages completed with correct artifact placement every time:

| Stage | Time | % of 1800s budget |
|---|---|---|
| Planner | 492s | 27% |
| Architect | 462s | 26% |
| Designer | 604s | 34% |
| Builder | 1069s | 40% (of 2700s builder budget) |
| Reviewer | 779s | 43% |
| Release Gate | 844s | 31% |

Every artifact landed in `rig/docs/...` as expected — no recurrence of the
`my-factory/docs/...` misplacement. This is now treated as a one-off, most likely
agent inference variance rather than a systemic defect, per the resolution path this
note originally proposed.

**Worth flagging, not yet actionable**: budget consumption trended upward across
later pipeline stages in this run (Reviewer 43%, Builder 40%) compared to the
20-30% band seen in Planner/Architect stages across L2/L3/L4. Single run, no
comparison point yet — noted here so a future maintainer with more data points can
tell whether later stages genuinely need more headroom or this run was simply on the
slower end of normal variance.

## Original report (unreproduced at time of writing, retained for provenance)

During the L3→L4→C1 live chain that validated the `session = "tmux"` fix
([[2026-08-17-architect-role-session-lifecycle-desync]]), L4 timed out at its first
step even though the artifact the step waits for had existed for 24 minutes — just
in the wrong directory. This is a single occurrence, not yet reproduced, and its
cause is not established.

## What happened

`test-harness/walkthroughs/L4.sh`'s `plan_check` polls
`$WALK_L4_RIG/docs/plans/*.md` (`WALK_L4_RIG="$WALK_L4_SCRATCH/rig"`). The L4
Planner instead wrote to `$WALK_L4_FACTORY/docs/plans/clamp-operation.md`
(`WALK_L4_FACTORY="$WALK_L4_SCRATCH/my-factory"`) — a sibling directory, not a
subdirectory, so no glob or relative-path mistake in the check itself could explain
it.

Timeline (`TUTORIAL_WALKTHROUGH_KEEP_SCRATCH=1`, scratch preserved at
`/private/tmp/sfi-tutorial-walkthrough/1787010570-22655/L4`):

- 17:44:13 — `my-factory/docs/plans/clamp-operation.md` written (confirmed by file
  mtime).
- Some point before 18:08 — `bd list` shows `Write the feature plan` **and**
  `Write the architecture decision` both closed (`✓`), meaning the Architect had
  already run and completed on top of the misplaced plan.
- 18:08:34 — harness gives up: `✗ TIMEOUT after 1800s waiting for: Planner to write
  docs/plans/*.md`, having polled `rig/docs/plans/` (empty) the entire time.

So the pipeline actually progressed two steps past the point the harness believed it
was stuck — the harness's completion signal for step 1 never fired, while step 2 ran
on the real artifact regardless (presumably because the Architect reads via `gc
prime`/formula routing, not via the harness's own filesystem poll).

## What this is not

- **Not the transport bug (GC-1).** That defect manifests as a session that never
  reaches `active` and never produces output at all. Here the Planner completed,
  produced correct content, and the pipeline advanced — the failure is purely in
  *where* the file landed relative to what the harness watches.
- **Not a harness path bug.** `L3.sh` and `L4.sh` use the identical
  `$WALK_LN_RIG/docs/plans` pattern, and L3's Planner, in the very same chain run
  minutes earlier, wrote correctly to `L3/rig/docs/plans/`. The check logic is not
  the variable.
- **Not a config difference.** `packs/lessons/{L3,L4}/agents/planner/agent.toml`
  differ only in `work_dir` and `default_sling_formula` values that are expected to
  differ per lesson (lesson name embedded in a path/formula-name string) — no
  structural difference, both files identical in shape.

## What remains open

> [!question] UNDOCUMENTED
> Root cause not established. This is a single occurrence. Candidate explanations,
> none confirmed:
> - Non-deterministic agent behavior: the planner prompt references "the project
>   rig" and "my-factory" in the same context; the model may have picked the wrong
>   one this run by chance, and could as easily pick correctly on a re-run.
>   `wake_mode = "fresh"` per-agent config was identical between L3 and L4, so this
>   would be inference variance, not a config difference.
> - Ambient working-directory state left over from L3 within the same chain run
>   (this was a `tutorial-walkthrough.sh L3 L4 C1` chain, not an isolated `L4`
>   invocation) — possible but no evidence collected linking L3's teardown to L4's
>   CWD.
> - A `gc` scheduling/context issue that handed the agent the wrong CWD or rig
>   binding on this particular wake — no gc log line was captured pointing at this
>   specifically, unlike GC-1 which has a precise log signature.
>
> Resolve by re-running `L4` in isolation (not chained) 2-3 times. If it recurs,
> capture the planner's `gc session peek` transcript from that run to see what
> context it was given about which directory to write to. If it does not recur, this
> is likely inference variance and not worth further engineering effort — a single
> instance in an LLM-driven step is not automatically a systemic defect.

## Why this does not retroactively cast doubt on the L2/L3 passes

L2 and L3 both completed multiple runs with artifacts landing in the correct,
harness-expected location every time, including elsewhere in this exact chain run
(L3, immediately before this). The transport fix (GC-1's workaround) is validated
independently of this finding — this is a new, distinct, unreproduced anomaly
discovered *because* the transport fix let the pipeline run far enough to expose it.

## Cleanup performed

`clean-walkthrough-runs --clean --kill` run after the failure; verified no
`sfi-walkthrough-*` cities registered, no stray processes, the user's own `factory`
city untouched. Scratch at `1787010570-22655` was **retained** (not the usual
auto-cleanup) specifically to preserve this evidence — clean it up once this note's
open question is resolved or judged not worth pursuing.
