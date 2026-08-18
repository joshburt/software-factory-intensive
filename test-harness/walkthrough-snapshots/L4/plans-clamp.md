# Clamp Operation Work Package

## Goal

Add a `clamp(x, lo, hi)` function to the calculator project that returns `x`
bounded to the inclusive interval `[lo, hi]`. The function must follow the
existing project conventions (CommonJS, pure functions, `node:test` coverage)
and ship with a matching test file, with no changes to existing behavior.

## User Stories

- As a user of the calculator library, I can call `clamp(5, 0, 10)` and receive
  `5` when the input is already within bounds, so I can use the function as a
  drop-in guard for out-of-range values.
- As a user of the calculator library, I can call `clamp(-3, 0, 10)` and
  `clamp(12, 0, 10)` and receive the boundary values `0` and `10` respectively,
  so values below the floor are raised and values above the ceiling are capped.
- As a user of the calculator library, I can rely on `clamp` returning the
  boundary values when `x` is exactly `lo` or exactly `hi`, so the bounds are
  inclusive and predictable.
- As a developer, I can run the existing test suite and see passing tests for
  the new `clamp` behavior alongside the existing tests, so I know the change is
  verified and does not regress `add` or `subtract`.

## Acceptance Criteria

1. `src/calculator.js` exports a `clamp` function via
   `module.exports = { add, subtract, clamp }`.
2. `clamp(x, lo, hi)` returns:
   - `x` when `lo <= x <= hi`,
   - `lo` when `x < lo`,
   - `hi` when `x > hi`.
3. The bounds are inclusive: `clamp(lo, lo, hi) === lo` and
   `clamp(hi, lo, hi) === hi`.
4. The behavior matches the existing pure-function style: it takes primitive
   number arguments and returns a number; it does not mutate inputs or throw
   for ordinary numeric inputs.
5. `test/calculator.test.js` (or a new test file following the
   `<name>.test.js` convention) adds at least one happy-path test and covers
   all three cases from criterion 2 (in-range, below floor, above ceiling),
   plus the inclusive-boundary cases from criterion 4.
6. `npm test` (which runs `node --test`) passes with the new tests included,
   and all pre-existing tests for `add` and `subtract` still pass.
7. The change is implemented on a `feature/clamp` branch, never straight to
   main.

## Scope Boundary

In scope:

- Adding the `clamp` function to `src/calculator.js` and exporting it.
- Adding tests for `clamp` in `test/`.
- Updating `docs/` artifacts produced by the factory workflow (plan,
  architecture, design, review, release gate) for this feature.

Out of scope (explicitly excluded):

- No new dependencies (production or dev) and no build tooling changes.
- No refactoring of the existing `add`/`subtract` functions.
- No type-checking, validation of `lo > hi`, or error/throw behavior for
  non-numeric or inverted-bound inputs — such behavior is intentionally
  undefined for this feature and should not be added unless a later feature
  requests it.
- No CLI, UI, or public API surface beyond the exported function.
- No changes to `package.json`, project structure, or test runner setup.

## Dependencies

- Existing project conventions defined in `CLAUDE.md` (CommonJS, `node:test`,
  pure functions, `module.exports = { ... }` export style, one test file per
  src file).
- Existing code in `src/calculator.js` (the `clamp` function will be added to
  this file) and `test/calculator.test.js` (existing tests must continue to
  pass).
- The factory workflow graph, which owns step routing: the Architect step
  (next) must read this plan and produce `docs/architecture/clamp.md`; the
  Designer step produces `docs/designs/clamp.md`; the Builder implements and
  tests on a `feature/clamp` branch; the Reviewer and Release-Gate steps
  follow. No downstream beads are created by this plan step.

## Open Questions

- Should `clamp` live in `src/calculator.js` alongside `add`/`subtract`, or in
  a new `src/clamp.js` file with its own `test/clamp.test.js`? The existing
  project has a single src file and single test file, so adding to the existing
  files matches current structure; a new file is reasonable if the project
  prefers one-function-per-file. This decision is left to the architect.
- What should happen when `lo > hi` (inverted bounds)? The smallest
  reasonable assumption is that behavior is undefined and unspecified for this
  feature; the architect should confirm no explicit contract is needed.
- Are arguments guaranteed to be numbers in practice? The plan assumes numeric
  inputs (matching the pure-function calculator style); no validation or error
  handling is specified.

## Handoff

The **Architect** should decide:

- Where `clamp` is implemented: adding to `src/calculator.js` (recommended to
  match the current single-file structure) versus a new `src/clamp.js` module,
  and the corresponding test file layout (`test/calculator.test.js` vs.
  `test/clamp.test.js`).
- Whether the undefined behaviors noted in Open Questions (`lo > hi`, non-
  numeric inputs) need an explicit contract, or remain unspecified.

The **Designer** should decide:

- The exact test matrix: which cases (in-range, below floor, above ceiling,
  inclusive bounds) to cover and any additional edge cases (e.g., equal
  bounds `lo === hi`, fractional values, negatives) worth adding to the test
  plan.
- Naming and documentation conventions for the new function to match existing
  code style.
