# Clamp Operation Architecture

## Context

The project needs a `clamp(x, lo, hi)` function that returns `x` bounded to the inclusive interval `[lo, hi]`. This is a single pure function addition to an existing calculator library that currently exports `add` and `subtract` from a single file (`src/calculator.js`). The test suite (`test/calculator.test.js`) uses `node:test` with `assert.strict`.

The planner artifact (`docs/plans/clamp.md`) explicitly delegates two decisions to the architect:

1. **Where to place the implementation**: Add to the existing `src/calculator.js` (matching the single-file structure) or create a new `src/clamp.js` module.
2. **Contract for undefined behaviors**: Whether `lo > hi` (inverted bounds) and non-numeric inputs need an explicit contract, or remain unspecified.

## Options Considered

### Option A — Add `clamp` to existing `src/calculator.js` (keep single-file structure)

- **Placement**: `clamp` function added to `src/calculator.js`; tests added to `test/calculator.test.js`.
- **Tradeoffs**:
  - Matches current project convention of one source file and one test file.
  - Minimal structural change — no new files, no import path changes.
  - Keeps all calculator operations co-located, which is convenient while the module is small.
  - As the project grows, the file becomes a dumping ground for unrelated functions, increasing cognitive load and merge conflict risk.
  - The planner recommends this as the default path for matching current structure.

### Option B — New `src/clamp.js` and `test/clamp.test.js` (one-function-per-file)

- **Placement**: `clamp` in its own `src/clamp.js` module; tests in `test/clamp.test.js`; `src/calculator.js` re-exports `clamp` (or consumers import directly).
- **Tradeoffs**:
  - Better separation of concerns — each function is independently testable and maintainable.
  - Follows a modular pattern that scales well as more functions are added.
  - Introduces a re-export pattern or a second import path, which is a departure from the current single-file convention.
  - Adds more files and a slight increase in project complexity for a single small function.
  - Premature modularization for a 3-line function — the project currently has only 2 functions.

### Option C — Explicit contract for undefined behaviors

- **What this means**: Define behavior for `lo > hi` (e.g., clamp to `[hi, lo]` or throw) and for non-numeric inputs (e.g., coerce via `Number()` or throw).
- **Tradeoffs**:
  - Makes the function more robust and predictable for all callers.
  - Adds code paths, tests, and potential `throw` statements — increasing surface area and deviating from the "no validation" stance in the existing `add`/`subtract` functions.
  - The planner explicitly excludes this from scope for this feature, and the existing `add`/`subtract` functions do not validate types.
  - Adding validation now would be inconsistent with the rest of the codebase.

### Option D — Keep undefined behaviors unspecified (default)

- **What this means**: `clamp` assumes numeric inputs and `lo <= hi`; no validation, no error-throwing, no special-case handling for inverted bounds or non-numeric inputs.
- **Tradeoffs**:
  - Matches the existing codebase pattern (no validation in `add`/`subtract`).
  - Keeps the function minimal and pure — a single expression with `Math.min`/`Math.max`.
  - Consistent with the planner's explicit out-of-scope list.
  - Callers who pass invalid inputs get silent NaN/undefined behavior — this is a conscious design choice that matches the calculator's convention.

## Decision

### Implementation placement: Option A

Add `clamp` to the existing `src/calculator.js` and tests to `test/calculator.test.js`. Rationale:

- The project currently has a single source file and a single test file. Adding to the same files preserves the existing structure.
- A 3-line pure function does not warrant a new module. Premature modularization adds overhead without benefit.
- The export pattern remains consistent: `module.exports = { add, subtract, clamp }`.
- The planner recommends this approach, and there is no evidence the project intends to scale beyond a handful of functions.

### Undefined behaviors: Option D — Keep unspecified

No explicit contract for `lo > hi` or non-numeric inputs. Rationale:

- The existing `add`/`subtract` functions do not validate their inputs. Consistency is more important than defensive programming in this context.
- The planner explicitly excludes validation and error-throwing from scope.
- The function will naturally degrade to `NaN` for invalid inputs (e.g., `Math.min(NaN, ...)` returns `NaN`), which is acceptable for a calculator that does not validate arguments.

## Consequences

- **Positive**: Zero structural changes to the project. Existing import paths, test patterns, and export conventions remain untouched.
- **Positive**: The new `clamp` function is a single addition to the export list — easy to review, test, and merge.
- **Positive**: No new failure modes introduced. Behavior for invalid inputs is undefined, matching the rest of the codebase.
- **Negative**: As the project grows, `src/calculator.js` may become a "god module" if all functions continue to be added to the same file. A future architecture decision may need to split it.
- **Negative**: Callers who pass `lo > hi` or non-numeric inputs will get silent `NaN` results with no diagnostic feedback.

## Risks

- **Low risk**: If the project later adopts input validation, retrofitting `clamp` to throw or coerce would be a breaking change for any caller that relied on the current undefined behavior. This risk is acceptable because the project currently has no consumers beyond its own tests.
- **Low risk**: Adding `clamp` to the existing test file increases the chance of merge conflicts when multiple features touch the same file simultaneously. Mitigation: the test file is small (11 lines) and the factory workflow processes one feature at a time.

## References

- [Feature Plan](docs/plans/clamp.md) — the planner artifact that defines scope, stories, and acceptance criteria.
- [CLAUDE.md](CLAUDE.md) — project conventions (CommonJS, `node:test`, pure functions, one test file per src file).
- [src/calculator.js](src/calculator.js) — existing implementation (add, subtract).
- [test/calculator.test.js](test/calculator.test.js) — existing test suite.