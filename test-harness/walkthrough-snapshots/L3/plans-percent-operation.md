# Percent Operation Work Package

## Goal

Add a `percent(whole, fraction)` operation to the calculator so that
`percent(whole, fraction)` returns `whole * fraction / 100`. The operation
follows the existing project conventions: pure function, CommonJS export,
tested with `node:test`.

## User Stories

- As a user of the calculator, I can compute a percentage of a whole number so
  that `percent(200, 10)` returns `20` (10% of 200).
- As a developer, I can import `percent` alongside the existing `add` and
  `subtract` functions from `src/calculator.js` without adding dependencies or
  build tooling.
- As a maintainer, I can run the full test suite with `node --test` and see the
  new operation covered by at least one happy-path test.

## Acceptance Criteria

1. `src/calculator.js` exports a `percent` function:
   `percent(whole, fraction)` returns `whole * fraction / 100`.
2. Behavior matches the formula exactly for standard numeric inputs, e.g.:
   - `percent(200, 10)` → `20`
   - `percent(100, 50)` → `50`
   - `percent(0, 50)` → `0`
3. The function is exported via `module.exports` in the existing
   `src/calculator.js` module (or, if a new source file is introduced per
   Architect/Designer decision, a matching test file must be added).
4. A test for the happy path exists in `test/calculator.test.js` using
   `node:test` and `node:assert/strict`, consistent with existing tests.
5. The full suite passes: `npm test` (which runs `node --test`) exits 0 with no
   failures.
6. No production or dev dependencies are added; no build tooling is
   introduced.

## Scope Boundary

In scope:

- Adding the `percent(whole, fraction)` operation and its export.
- Adding matching unit tests.
- Any doc updates needed to describe the new operation.

Out of scope:

- Changing the behavior or signature of existing `add`/`subtract` functions.
- Refactoring the existing module structure, test layout, or tooling.
- Adding new dependencies, TypeScript, build steps, or CLI surface.
- Handling currency/formatting, percentage of multiple values, or any
  operation beyond `whole * fraction / 100`.
- Changing the formula graph, step routing, or any factory configuration.

## Dependencies

- Existing `src/calculator.js` module and its `module.exports` convention.
- Existing `test/calculator.test.js` test conventions (`node:test`,
  `node:assert/strict`).
- Node runtime with built-in `node:test` (no external packages).

## Open Questions

1. **Non-numeric input handling**: Should `percent` validate types and return
   `NaN` for non-numeric arguments, or return a thrown `TypeError`? The
   existing `add`/`subtract` do no validation (they rely on JS coercion), so
   matching that behavior (return `NaN` implicitly) is the smallest
   assumption.
2. **Negative inputs**: No explicit requirement; the formula works for
   negatives as-is (`percent(-200, 10)` → `-20`). Confirm this is acceptable
   or should be clamped.
3. **Placement**: Whether `percent` lives in the existing `src/calculator.js`
   (recommended, matches current single-module pattern) or a new
   `src/percent.js` file with a new test file.

## Handoff

Decisions for the **Architect** to resolve:

- Whether to keep `percent` in the existing `src/calculator.js` module or
  introduce a new source module (and the resulting export surface).
- Whether argument validation/error semantics are required beyond the raw
  formula (e.g., `TypeError` on non-numeric input) or JS-coercion behavior is
  acceptable, consistent with `add`/`subtract`.

Decisions for the **Designer** to resolve:

- Exact function signature and naming (`percent(whole, fraction)` per the
  request; confirm parameter order).
- Behavior for edge cases: zero values, negative values, non-numeric
  arguments, and floating-point precision.
- The concrete test plan: happy path, at least one boundary case (zero), and
  any edge cases agreed with the Architect.
