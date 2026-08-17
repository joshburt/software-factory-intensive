---
title: Human Gates Are Taught but Not Shipped in Any Lesson Pack
type: discovery
tags:
  - discovery
  - human-gate
  - lesson-pack
  - manifest
  - drift
created: 2026-08-17
updated: 2026-08-17
status: reviewed
source: agent
---

# Human Gates Are Taught but Not Shipped in Any Lesson Pack

The curriculum teaches human approval gates in two places and no shipped lesson
pack implements one. The gap is never acknowledged to the student.

## Evidence

`curriculum/SOFTWARE_FACTORY_MANIFEST_TEMPLATE.md` defines a `## Human Gates`
section with two gates:

> **Gate 1 — After Architect:** Human approves ADR before Designer runs.
> **Gate 2 — After Reviewer:** Human approves review report before Deployer runs.

`curriculum/workshops/W3/README.md` ships a Decision Boundaries table assigning
database schema changes, new dependencies, and API contract changes to **Human**,
with the rationales "Irreversible", "Security burden", and "Cross-system". W3
further requires `activities/workshops/W3/gates/<name>.md` docs explaining "why a
human decision is required", what PASS and FAIL mean, and how the run resumes.

Against that, across `packs/lessons/**`:

- `approve` — 0 matches
- `human` — 1 match, and it is incidental: `packs/lessons/L2/agents/planner/prompt.template.md`
  says the plan is written so "a human and the architect can inspect" it
- no `actor` field, no approval step, no gate step in any formula

## Important nuance

Human gates are **not** absent from the repository as a whole. This repo's own
development process has them: `.specify/workflows/speckit/workflow.yml` defines
`review-spec` and `review-plan` steps with `type: gate` and `on_reject: abort`.
The gap is specifically between what the curriculum teaches students to build and
what the reference factories they run actually do.

## Constitutional status

Violates Article XIV clause 3 (a taught gate the reference pack omits must be
plainly disclosed in student-facing text, with the reason) and Article IV
(taught-capability fidelity). Tracked as `TODO(DEFECT-B1)`.

Note the resolution constraint: Article XIV clause 1 forbids resolving this by
deleting the Human Gates teaching. The doctrine must remain taught.

## Resolution options

1. Implement a gate mechanism in the reference packs.
2. Disclose plainly in student-facing text that the reference factory ships
   without gates, and why — for example, that wiring the gate is the W3 exercise.

Option 2 is legitimate: an unhardened teaching exemplar is defensible. Silence
is not.
