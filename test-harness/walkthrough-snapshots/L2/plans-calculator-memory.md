# Calculator Memory Work Package

## Goal

Add a memory feature to the minimal JavaScript calculator so a user can
**store** the current result in a single memory slot, **recall** it back into
the calculation, and **clear** it. The feature must follow the project's
existing conventions: CommonJS modules, small pure functions, and
`node:test`-based tests.

## User Stories

- As a user, I can store the current result in calculator memory so I can reuse
  it in a later calculation without writing it down.
- As a user, I can recall the stored value so I can use it as an operand in a
  new calculation (e.g., `add(memoryRecall(), 5)`).
- As a user, I can clear the memory so a stale value no longer affects my
  calculations.
- As a user, I expect the memory to persist within a session until I clear it
  or store a new value.

## Acceptance Criteria

- [ ] A `memoryStore(value)` function is exported that saves a numeric value to
      a single memory slot and returns the stored value.
- [ ] A `memoryRecall()` function is exported that returns the currently stored
      value.
- [ ] A `memoryClear()` function is exported that empties the memory slot and
      returns a defined "cleared" result.
- [ ] Recalling when memory is empty has a well-defined behavior (documented
      and implemented; see Open Questions for the allowed options).
- [ ] Storing a new value overwrites the previous value in the single slot.
- [ ] Each new function has at least one happy-path test in a matching test
      file under `test/`, using `node:test` and `node:assert/strict`.
- [ ] All tests pass with `node --test` and existing `add`/`subtract` tests
      still pass.
- [ ] The feature adds no new dependencies and introduces no build tooling.

## Scope Boundary

**In scope:**
- Single-slot memory with store / recall / clear semantics on the calculator
  module (`src/calculator.js`).
- Pure-function API design — memory functions should be deterministic and
  side-effect free where possible (no UI, no CLI, no persistent storage).
- Tests covering the new memory behavior, plus keeping existing tests green.

**Out of scope:**
- Multiple memory slots, named memory registers, or M+/M- style arithmetic
  accumulation.
- Any UI, CLI, REPL, or web interface for the calculator.
- Persistence across process restarts (memory is in-process only).
- Changing the existing `add`/`subtract` signatures or behavior.
- Creating downstream work items or design/architecture artifacts — those are
  owned by later formula steps (Architect: `docs/architecture/<slug>.md`).

## Dependencies

- Existing project conventions from `CLAUDE.md`: CommonJS
  (`require`/`module.exports`), zero dependencies, `node --test`.
- Existing `src/calculator.js` as the home for the new exports.
- Existing `test/calculator.test.js` as the pattern for new test files
  (one test file per src file, named `<name>.test.js`).
- No external packages are required.

## Open Questions

- **Empty-recall semantics**: What should `memoryRecall()` return when nothing
  has been stored yet? Options: (a) `null`, (b) `undefined`, (c) `0`, or
  (d) throw an error. Default assumption: return `null` — record the chosen
  behavior in the architecture doc.
- **Value validation**: Should store reject non-numeric values (e.g., `NaN`,
  strings, `undefined`), or store whatever is passed? Default assumption:
  accept only finite numbers and treat anything else as a no-op — confirm in
  the architecture doc.
- **File layout**: Should memory functions live in `src/calculator.js` or a new
  `src/calculator-memory.js`? Default assumption: a new
  `src/calculator-memory.js` module re-exported from `src/calculator.js`, but
  either is acceptable.
- **Cleared return value**: What should `memoryClear()` return? Default
  assumption: `null` to signal the slot is now empty.

## Architect Handoff

The architect must resolve these key technical decisions:

1. **State modeling**: How the single memory slot is represented. Decide between
   (a) module-level closure state inside `src/calculator-memory.js` with
   pure-ish functions that read/write the closure, (b) explicit state passed
   in/out of functions (fully pure, `{ value } -> { value, next }` style), or
   (c) a small factory that returns a stateful object (`createMemory()`).
   The choice affects testability and the `add`/`subtract` integration story.
2. **API shape and integration**: Exact export names
   (`memoryStore`, `memoryRecall`, `memoryClear`) and whether they are exported
   from `src/calculator.js` directly or via re-export from a new module.
3. **Empty-recall and validation semantics**: Finalize the behavior for
   empty recall, non-numeric store input, and the `memoryClear()` return value
   (see Open Questions).
4. **Test strategy**: Confirm the test file layout (`test/calculator-memory.test.js`
   vs. extending `test/calculator.test.js`) and the minimum test cases
   required for acceptance.
