---
title: The Walkthrough Rig Is a Node Project While the Curriculum Mandates Python
type: discovery
tags:
  - discovery
  - conflict
  - test-harness
  - walkthrough
  - snapshot
  - curriculum
  - drift
created: 2026-08-17
updated: 2026-08-17
status: reviewed
source: agent
---

# The Walkthrough Rig Is a Node Project While the Curriculum Mandates Python

Found while attempting the Article IV snapshot regeneration required by `ADR-005`.
The regeneration task as originally scoped was **wrong**, and running it would have
made the repository worse.

## The conflict

`ADR-005` mandates Python/FastAPI for student projects. The verification harness slings
agents at its own scratch project, and that project is a **Node.js calculator**:

`test-harness/tutorial-walkthrough-rig/`

```text
CLAUDE.md
package.json          -> {"name": "calculator", "scripts": {"test": "node --test"}}
README.md
src/calculator.js
test/calculator.test.js
```

All five walkthroughs assert against it with `node --test`:

```text
test-harness/walkthroughs/L1.sh:173   node --test
test-harness/walkthroughs/L3.sh:185   node --test
test-harness/walkthroughs/L4.sh:???   node --test
test-harness/walkthroughs/C1.sh:203   node --test
```

`L1.sh:78` goes further and writes the stack into generated student-visible content:

```text
Node.js, native test runner (node --test).
```

So after `ADR-005` the curriculum teaches one stack while its own end-to-end
verification exercises a different one. The harness would be proving that the factory
works on a path no student follows.

## Why regenerating snapshots first would have been actively harmful

Snapshots are ground truth under Article IV. Regenerating them against the current rig
would have **baked Node ground truth into a Python-mandated curriculum** and then
presented it as verified fact. Two snapshot files make this concrete:

- `test-harness/walkthrough-snapshots/{L1,L3,L4,C1}/node-test.txt` — captured
  `node --test` output. Meaningless once the stack is Python.
- `test-harness/walkthrough-snapshots/{L1,L4}/PROJECT_MANIFEST.md` — still the **old
  blank Tech Stack template**, which `ADR-005` replaced with a pre-filled Python one.
  Already stale the moment the template changed.

The correct dependency order is therefore:

1. Convert `test-harness/tutorial-walkthrough-rig/` to a Python project conforming to
   `curriculum/ENGINEERING_STANDARD.md`.
2. Update the five walkthrough scripts to drive the Python test command, and remove
   `L1.sh`'s hard-coded Node stack text.
3. **Then** regenerate snapshots.

Steps 1 and 2 are deterministic and consume no model tokens. Only step 3 requires live
runs, and Article X forbids running the chains concurrently.

## Scope note

This is harness-internal, not student-facing, so Article V's content boundaries do not
apply to the rig's own files — but the rig's *generated* artifacts do reach snapshots
that the curriculum is validated against, which is why the mismatch matters.

The rig should stay deliberately small. It exists to prove the factory routes work, not
to be a second reference implementation — `reference-project/fired-up-pizza` already
fills that role. A minimal Python package with a `Makefile`, a `pyproject.toml`, one
module, and one test suite is sufficient, and keeping it minimal keeps walkthrough runs
fast.

> [!attention] CONFLICT
> Taught vs verified. `curriculum/ENGINEERING_STANDARD.md` and the pre-filled
> `curriculum/PROJECT_MANIFEST_TEMPLATE.md` mandate Python/FastAPI/pytest. The harness
> at `test-harness/tutorial-walkthrough-rig/` plus `test-harness/walkthroughs/*.sh`
> exercise Node.js with `node --test`. Both sides are quoted above. Until the rig is
> converted, no snapshot in `test-harness/walkthrough-snapshots/` can be treated as
> valid evidence for the current curriculum.
