# Percent Operation Architecture

## Context

The calculator project must add a `percent(whole, fraction)` operation that
returns `whole * fraction / 100`. The feature request is defined in
`docs/plans/percent-operation.md`.

The existing codebase is a minimal CommonJS calculator:

- `src/calculator.js` exports `add` and `subtract` via a single
  `module.exports = { add, subtract }` object. No input validation — the
  functions rely on JavaScript coercion.
- `test/calculator.test.js` uses `node:test` and `node:assert/strict`, one
  happy-path test per function.
- No build tooling, no production or dev dependencies; tests run via
  `npm test` (`node --test`).

The plan's Handoff section delegates two decisions to the Architect:

1. Module placement: keep `percent` in the existing `src/calculator.js` or
   introduce a new source module.
2. Error semantics: validate inputs (e.g., `TypeError` on non-numeric input)
   or match the existing JS-coercion behavior of `add`/`subtract`.

## Options Considered

### Option A: Add `percent` to the existing `src/calculator.js` (chosen)

Extend the single calculator module with a pure `percent(whole, fraction)`
function and export it alongside `add`/`subtract`. Add one happy-path test to
the existing `test/calculator.test.js`.

- Tradeoffs:
  - Pros: Matches the existing single-module pattern; zero new files; no
    changes to module layout, test layout, or tooling; smallest diff; the
    export surface stays cohesive for a calculator library.
  - Cons: `calculator.js` grows slightly; if the module later becomes large,
    a future refactor into per-operation files would be needed.

### Option B: Introduce a new `src/percent.js` module

Create a dedicated `src/percent.js` with its own `module.exports` and a
matching `test/percent.test.js`.

- Tradeoffs:
  - Pros: Isolates the new operation; scales if each operation is intended to
    live in its own file.
  - Cons: Diverges from the established single-module convention; adds two new
    files for one small pure function; increases surface area and review cost
    for no functional benefit; the plan's default recommendation is the
    existing module.

### Option C: Add input validation (`TypeError` on non-numeric arguments)

Wrap the formula in validation that throws for non-numeric inputs.

- Tradeoffs:
  - Pros: Explicit failure semantics; guards callers from silent `NaN`
    propagation.
  - Cons: Diverges from `add`/`subtract`, which do no validation; adds code
    and test burden beyond the acceptance criteria; the formula contract
    (`whole * fraction / 100`) holds for standard numeric inputs without it;
    the plan's open question notes matching `add`/`subtract` behavior is the
    smallest assumption.

## Decision

1. **Module placement**: Add `percent(whole, fraction)` to the existing
   `src/calculator.js` and export it via the existing
   `module.exports = { add, subtract, percent }` object. Do not introduce a
   new source file.
2. **Error semantics**: Do not add input validation. Match the existing
   `add`/`subtract` convention — the formula is evaluated directly and relies
   on JavaScript coercion. Non-numeric inputs therefore yield `NaN`, and
   negative inputs work as-is (`percent(-200, 10)` → `-20`).
3. **Tests**: Add at least one happy-path test for `percent` to the existing
   `test/calculator.test.js` using `node:test` and `node:assert/strict`,
   e.g., `percent(200, 10)` → `20`, plus a zero boundary case
   (`percent(0, 50)` → `0`). Parameter order is `percent(whole, fraction)` per
   the request.

Rationale: The decision minimizes diff size and risk, preserves the project's
conventions (single pure-function module, coercion-based semantics, one test
file per source file), and satisfies every acceptance criterion in the plan
without adding dependencies, build tooling, or new module structure.

## Consequences

- `src/calculator.js` gains a third pure function and export.
- `test/calculator.test.js` gains at least two tests (happy path + zero
  boundary), keeping the "one test file per src file" convention intact.
- No dependencies, build steps, or CLI surface are added.
- The existing `add`/`subtract` behavior and signatures are untouched.
- Callers of `percent` get the documented formula for numeric inputs and the
  same coercion behavior as the rest of the module for non-numeric inputs.

## Risks

- **Low**: Silent `NaN` for non-numeric input — accepted by design to match
  `add`/`subtract`; documented in this artifact and the plan.
- **Low**: Floating-point precision for fractional results (e.g.,
  `percent(3, 33)` → `0.99`) — inherent to the formula and consistent with
  existing behavior; no rounding is specified.
- **Low**: Negative inputs are unclamped — the formula handles them
  deterministically; no requirement to clamp exists.

## References

- Planning artifact: `docs/plans/percent-operation.md`
- Project conventions: `CLAUDE.md` (module layout, artifact structure,
  zero-dependency rule)
- Existing implementation: `src/calculator.js`, `test/calculator.test.js`
