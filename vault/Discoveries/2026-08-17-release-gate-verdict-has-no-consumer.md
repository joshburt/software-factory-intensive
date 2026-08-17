---
title: Release-Gate PASS/FAIL Verdict Has No Consumer
type: discovery
tags:
  - discovery
  - lesson-pack
  - formula
  - verdict
  - drift
created: 2026-08-17
updated: 2026-08-17
status: reviewed
source: agent
---

# Release-Gate PASS/FAIL Verdict Has No Consumer

The shipped L4 and C1 factories produce a release-gate verdict that nothing acts
on, and the L4 curriculum promises routing behavior that no formula implements.
This is both curriculum drift and a pack-internal design defect.

## Evidence

`curriculum/labs/L4/README.md` line 24 shows, in the architecture diagram:

```
│  verdict: APPROVE (else loop back to Coder)
```

No loop-back edge exists. `packs/lessons/L4/formulas/mol-delivery-review.toml`
is a strict linear chain — `plan → architecture → design → build → review →
release` — with five `needs` edges and no conditional routing, no `actor` field,
and no branch. `packs/lessons/C1/formulas/mol-release-delivery.toml` is the same
shape with a `validate` step inserted (seven steps, six `needs` edges).

Meanwhile `packs/lessons/C1/agents/release-gate/prompt.template.md` requires:

> The Verdict section must contain exactly one of `PASS` or `FAIL`.

So the terminal step renders a verdict, and the graph has no consumer for it.
The run ends identically whether the verdict is PASS or FAIL.

## Why this matters

W3 teaches conditional branching and names this exact case as a *good* reason to
branch (`curriculum/workshops/W3/README.md`): "release gate should stop if
validation fails." The shipped exemplar therefore violates a rule the curriculum
itself teaches. Students copy the exemplar, not the prose, so the practical
lesson is that a gate is a document rather than a control.

## Constitutional status

Violates Article IV (taught capability must match shipped behavior, or be
disclosed) and Article XIII (a step that produces a verdict must have a defined
consequence or be declared advisory-only). Tracked as `TODO(DEFECT-B3)`.

## Resolution options

1. Add a conditional edge so a FAIL verdict stops the run or routes back to
   `build` — matches what W3 teaches and what L4's diagram promises.
2. Declare the verdict advisory-only in the pack and correct the L4 diagram.

Option 1 is the better teaching outcome; option 2 is the smaller change. Either
satisfies Article XIII; only option 1 satisfies W3's own stated doctrine.
