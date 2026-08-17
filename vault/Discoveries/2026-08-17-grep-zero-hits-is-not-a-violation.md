---
title: Zero Grep Hits in Packs Is Not Evidence of a Violation
type: discovery
tags:
  - discovery
  - improvement-loop
  - curriculum
  - drift
created: 2026-08-17
updated: 2026-08-17
status: reviewed
source: agent
---

# Zero Grep Hits in Packs Is Not Evidence of a Violation

While auditing W4 doctrine against the shipped packs, a search for
`retrospective`, `signal`, `improve`, and `metric` across `packs/lessons/**`
returned zero hits for each. That was initially read as four taught-but-unshipped
capabilities. Two of the four dissolved on inspection, and codifying them would
have manufactured phantom constitutional violations.

## What the absence actually meant

**The retrospective is a student deliverable, not a pack artifact.** No agent was
ever claimed to write it:

- `curriculum/capstone/C1/README.md` line 169: "Create
  `activities/capstone/C1/retrospective.md`"
- `activities/capstone/C1/README.md` line 41 lists it as the deliverable, "with
  W4 criteria evaluation"
- `test-harness/walkthroughs/C1.sh` lines 240, 269, 291 create it, assert it
  exists, and snapshot it

So it is produced, validated, and already governed by Article VII.

**The W4 improvement loop is human-operated by design.** W4's own steps put the
human in the loop ("Choose one rule and make the smallest real config change"),
and the signals it names are real pack outputs — `docs/reviews/*.md` and
`docs/releases/*.md` are written by the reviewer and release-gate agents. W4 even
teaches gap discipline explicitly: "Don't invent signals. If a row has 'Volume so
far' = 0 … record it as a gap." Nothing claims autonomous signal consumption.

That is Article I (Config Over Prompting) working as designed: the human reads
signals and edits config.

## The lesson

A grep for a mechanism name conflates two different findings:

- *claimed and absent* — a real taught-vs-shipped defect
- *never claimed to be there* — not a defect at all

Only the first is an Article IV violation. Distinguishing them requires reading
what the curriculum actually promises, not just whether a keyword appears in the
pack. Of four candidate findings, two were real (`DEFECT-B1`, `DEFECT-B3`) and
two dissolved.

## Consequence

Two proposed constitutional articles — "Signal-Anchored Improvement" and
"Retrospective Artifact" — were dropped. See
`vault/Decisions/ADR-002-Descriptive-Constitution-Scope.md`. The rejection is
recorded in the constitution's Sync Impact Report under "Considered and
deliberately NOT added" so the reasoning is not lost and the question is not
reopened without new evidence.
