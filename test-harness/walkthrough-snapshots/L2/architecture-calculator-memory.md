# Calculator Memory Architecture

## Context

The calculator needs single-slot memory: `memoryStore(value)`, `memoryRecall()`, and `memoryClear()` functions. The planner's work package (`docs/plans/calculator-memory.md`) defines user stories, acceptance criteria, and scope. The architect must resolve four technical decisions:

1. **State modeling** — how the single memory slot is represented
2. **API shape and integration** — file layout and export strategy
3. **Empty-recall and validation semantics** — edge-case behavior
4. **Test strategy** — where tests live and minimum coverage

Project conventions (from `CLAUDE.md`): CommonJS modules, zero dependencies, `node:test` runner, one test file per source file, small pure functions preferred, no build tooling. No existing ADRs, manifest files, or prior architecture docs exist in this project.

## Options Considered

### Option A — Module-level closure state (new `src/calculator-memory.js`)

A dedicated module holds a single `let memory = null;` in its closure scope. The three functions read/write this variable directly and are exported via `module.exports`. The calculator module (`src/calculator.js`) re-exports them to preserve a unified public surface.

**Tradeoffs:**

| Pro | Con |
|---|---|
| Idiomatic CommonJS singleton — zero new concepts | Mutable module state; functions are technically impure |
| Trivial to implement (≈10 lines of code) | Cross-test state pollution — tests must reset state |
| Matches named export signatures from acceptance criteria exactly | State is global per process; cannot create independent instances |
| Re-export preserves a single `require('../src/calculator')` surface | Re-export couples calculator.js to calculator-memory.js |

### Option B — Explicit state-passing (fully pure)

Memory functions take and return state explicitly: `memoryStore(value, { memory })` returns `{ memory: value }`, `memoryRecall({ memory })` returns the value, `memoryClear({ memory })` returns `{ memory: null }`. The calculator module exposes a thin wrapper that manages the current state.

**Tradeoffs:**

| Pro | Con |
|---|---|
| Fully deterministic and testable without state setup | Breaks the no-arg signatures from acceptance criteria (`memoryRecall()` with no args) |
| No cross-test pollution | Every caller must thread state — awkward for `add(memoryRecall(), 5)` |
| Easier to later extend to multi-slot | More boilerplate than the feature warrants |
| Aligns with "prefer pure functions" convention | Would require changing the acceptance criteria or adding a wrapper layer |

### Option C — Factory function (`createMemory()`)

A `createMemory()` factory returns a stateful object with `.store(`, `.recall()`, `.clear()` methods. The flat `memoryStore`/`memoryRecall`/`memoryClear` functions are derived from a default singleton instance.

**Tradeoffs:**

| Pro | Con |
|---|---|
| Testable via fresh factory instances per test | Diverges from "small pure functions over classes" convention |
| Future-proof for multi-slot or multiple independent memory contexts | Factory pattern is over-engineering for a single slot |
| Can still expose flat API via singleton | Two API surfaces: factory and singleton — confusing which to use |
| Isolates memory state naturally | Adds conceptual weight for a trivial feature |

## Decision

**Chosen: Option A — Module-level closure state in a new `src/calculator-memory.js` module, re-exported from `src/calculator.js`.**

**Rationale:**

1. **Best fit for scope.** The feature is a single memory slot with three functions. Option A is the simplest, most direct expression of the acceptance criteria. Option B's purity is architecturally elegant but forces a mismatch with the specified no-arg API. Option C's factory is over-engineered for a single-slot memory on a zero-dependency calculator.

2. **Matches project conventions.** CommonJS modules are the only pattern in the project. A module-level closure is the idiomatic "module singleton" — every `require('./calculator-memory')` gets the same instance. This is natural in Node.js and requires no new patterns.

3. **Re-export preserves the public surface.** `calculator.js` gains three re-exports so consumers can `const { add, subtract, memoryStore, memoryRecall, memoryClear } = require('../src/calculator')`. The coupling is minimal and symmetrical with the existing pattern.

4. **Testability is manageable.** Although module state persists across tests within the same file, the `beforeEach` hook (or each test calling `memoryClear()`) resolves ordering sensitivity. `node --test` runs each test file in a separate process, so cross-file pollution does not occur.

**Resolved semantics (from the plan's open questions):**

| Decision | Choice | Rationale |
|---|---|---|
| Empty recall | Return `null` | `null` is semantically "no value stored"; distinguishable from `0` (valid number). `undefined` is ambiguous with "not exported"; throwing would break the `add(memoryRecall(), 5)` composition. |
| Invalid store input | Leave slot unchanged, return current stored value | Accept only finite numbers (`Number.isFinite`). Invalid input is a no-op — the slot is unchanged, and the function returns the current slot value (observable, deterministic). |
| `memoryClear()` return | Return `null` | Consistent with empty-recall `null` — signals "slot is now empty." |
| File layout | `src/calculator-memory.js` re-exported from `src/calculator.js` | One file per feature, matching CLAUDE.md convention. Re-export keeps a single `require('calculator')` entry point. |
| Test file | `test/calculator-memory.test.js` | One test file per source file per CLAUDE.md. |

## Consequences

- **Positive:** The implementation is trivial (~10 lines of code). Zero new dependencies. Existing `add`/`subtract` are untouched. The re-export pattern means existing consumers of `calculator.js` automatically get memory functions.
- **Positive:** Tests are straightforward: happy paths, empty recall, overwrite, clear, invalid input. Each test file runs in its own process, so no cross-file contamination.
- **Negative:** Module-level mutable state introduces test-ordering sensitivity within the memory test file. Every test must start with a known-clean state (via `beforeEach` or manual clear).
- **Negative:** Re-export creates a one-way dependency from `calculator.js` to `calculator-memory.js`. If memory is later removed, `calculator.js` must be edited.
- **Neutral:** The memory is process-scoped. If the calculator is later embedded in a server or UI, each request/user would share the same memory slot. Evolving to a factory pattern (Option C) at that point is a natural migration.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Consumer treats `null` from recall as an error rather than "empty" | Low | Document the behavior; tests confirm `null` is the expected empty value |
| Silent no-op on invalid input hides bugs | Low | The function returns the current value on invalid input, making the no-op observable; tests document the contract |
| Cross-test state pollution in the same file | Medium | Document in test file that `memoryClear()` is required in `beforeEach`; test file structure ensures this is visible |
| Future multi-slot would require refactor | Low | Single-slot requirement is explicit in scope; migration to factory is straightforward if needed |

## References

- Planner artifact: `docs/plans/calculator-memory.md`
- Project conventions: `CLAUDE.md` (CommonJS, `node:test`, file layout, export style)
- Source: `src/calculator.js` (existing `add`/`subtract` functions and export pattern)
- Tests: `test/calculator.test.js` (test convention model)