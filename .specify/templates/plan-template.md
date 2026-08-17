# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]

**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command; its definition describes the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]

**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]

**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]

**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]

**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]

**Project Type**: [e.g., library/cli/web-service/mobile-app/compiler/desktop-app or NEEDS CLARIFICATION]

**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]

**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]

**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Gates are derived from the ratified constitution at `.specify/memory/constitution.md`.
Record each applicable article as PASS, N/A, or a justified violation. Violations MUST be
recorded in the Complexity Tracking table below — never silently accepted.

| Article | Gate | Status |
|---------|------|--------|
| I — Config Over Prompting | Behavior changes land in committed config, not chat corrections | [PASS/N/A] |
| II — Curriculum-Blind Pack Internals | No class/lab/workshop/lesson language inside `packs/**` | [PASS/N/A] |
| III — Self-Contained Lesson Packs | Pack is complete and standalone; current formula contract; binding-qualified routes | [PASS/N/A] |
| IV — Walkthroughs Are the Source of Truth | Curriculum claims reconciled against `test-harness/walkthrough-snapshots/<lesson>/`; taught capabilities match shipped pack behavior or are explicitly disclaimed | [PASS/N/A] |
| V — No Internal Tooling Leakage | No harness/snapshot references or version-branded names in student-facing content | [PASS/N/A] |
| VI — Formula-Owned Orchestration | No agent-side scheduling; no banned patterns SFI001–SFI008 | [PASS/N/A] |
| VII — Every Session Has a Named Deliverable | `## Deliverable` section present; lesson contract updated if runnable | [PASS/N/A] |
| VIII — Layered Verification Gates | Applicable harness rungs identified and run; no check weakened or deleted | [PASS/N/A] |
| IX — Reproducible Student Path | Clean-machine path verified; tool versions asserted; troubleshooting linked | [PASS/N/A] |
| X — Isolated, Reversible Harness Runs | Runs isolated and self-cleaning; no concurrent live chains; surgical cleanup | [PASS/N/A] |
| XI — Manifest Authority | Each agent prompt names its authoritative manifest section; explicit fallback when absent | [PASS/N/A] |
| XII — Step Contracts and Explicit Done-Conditions | Each step declares target, deps, inputs, artifact, close condition, failure behavior; handoffs explicit | [PASS/N/A] |
| XIII — Every Procedure Specifies Its Failure Path | Concrete failure response per procedure; rollback declared; every verdict has a consequence or is advisory-only | [PASS/N/A] |
| XIV — Human Decision Authority | Human-owned decision domains taught with reasoning; gates justified with PASS/FAIL/resumption; unimplemented gates disclosed; named review owner | [PASS/N/A] |

Verification commands (cheapest first):

```bash
python3 test-harness/lesson-pack-lint.py
bash test-harness/migration-check.sh
bash test-harness/tutorial-check.sh
bash test-harness/behavioral-smoke.sh
bash test-harness/tutorial-walkthrough.sh <lesson>   # live tokens; pre-release only
```

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
