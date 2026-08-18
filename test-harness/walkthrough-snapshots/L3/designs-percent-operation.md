# Percent Operation Design

## Interface

Add a pure CommonJS function `percent(whole, fraction)` to the existing
`src/calculator.js` module and export it alongside `add`/`subtract`.

```js
// src/calculator.js
function percent(whole, fraction) {
  return whole * fraction / 100;
}

module.exports = { add, subtract, percent };
```

- **Signature**: `percent(whole, fraction)` — parameter order per the root
  request. `whole` is the base value; `fraction` is the percentage amount
  (already in percent units, e.g. `10` for 10%).
- **Return**: `whole * fraction / 100`, a `Number`.
- **Export**: added to the existing `module.exports = { add, subtract, percent }`
  object. No new source file, no new dependencies, no build tooling.
- **Consumers**: `require('../src/calculator')` and destructure `percent` the
  same way as `add`/`subtract`.
- **Semantics**: no input validation. Matches the existing `add`/`subtract`
  convention — arguments are coerced by JavaScript arithmetic (`*` and `/`).
  Non-numeric arguments yield `NaN`, not a thrown error.

## Behavior

- **Formula**: `percent(whole, fraction) === whole * fraction / 100` for all
  numeric inputs, evaluated with standard JavaScript arithmetic.
- **Happy path**: `percent(200, 10)` → `20` (10% of 200);
  `percent(100, 50)` → `50`.
- **Zero boundary**: `percent(0, 50)` → `0` (zero whole, any fraction).
  `percent(200, 0)` → `0` (0% of anything). `percent(0, 0)` → `0`.
- **Negative inputs**: unclamped and deterministic. `percent(-200, 10)` → `-20`;
  `percent(200, -10)` → `-20`. Consistent with `add`/`subtract` accepting
  negatives without restriction.
- **Non-numeric inputs**: no validation; JS coercion applies.
  - `percent('200', '10')` → `20` (numeric strings coerce).
  - `percent('abc', 10)` → `NaN` (non-numeric string coerces to `NaN`).
  - `percent(null, 10)` → `0` (`null` coerces to `0` via `*`).
  - `percent(undefined, 10)` → `NaN`.
  - `percent(NaN, 10)` → `NaN`.
- **Floating-point**: results are not rounded. `percent(3, 33)` → `0.99`
  (i.e. `3 * 33 / 100 = 99/100`); `percent(1, 10)` → `0.1` (binary float).
  Any IEEE-754 imprecision is accepted as inherent to the formula and
  consistent with existing module behavior. Tests must use exact `assert.equal`
  only for values that are exactly representable (`20`, `50`, `0`, `0.99`,
  `-20`), or `assert.equal` with the same computed expression for imprecise
  expectations.
- **Infinities**: `percent(Infinity, 10)` → `Infinity`;
  `percent(200, Infinity)` → `Infinity`; `percent(0, Infinity)` → `NaN`
  (standard `0 * Infinity`). No special handling.

## Edge Cases

| Input `(whole, fraction)` | Expected | Notes |
|---|---|---|
| `(200, 10)` | `20` | canonical happy path |
| `(100, 50)` | `50` | 50% of 100 |
| `(0, 50)` | `0` | zero whole — acceptance-criteria boundary |
| `(200, 0)` | `0` | zero fraction (0%) |
| `(0, 0)` | `0` | zero/zero |
| `(-200, 10)` | `-20` | negative whole, unclamped |
| `(200, -10)` | `-20` | negative fraction, unclamped |
| `('200', '10')` | `20` | numeric strings coerce |
| `('abc', 10)` | `NaN` | non-numeric string |
| `(null, 10)` | `0` | `null` coerces to `0` |
| `(undefined, 10)` | `NaN` | `undefined` coerces to `NaN` |
| `(NaN, 10)` | `NaN` | NaN propagates |
| `(Infinity, 10)` | `Infinity` | infinity propagates |
| `(0, Infinity)` | `NaN` | `0 * Infinity` is `NaN` per IEEE-754 |
| `(3, 33)` | `0.99` | exactly representable fraction result |

Design decisions on open questions from the plan:

1. **Non-numeric handling**: no `TypeError`; silent `NaN` via coercion. Matches
   `add`/`subtract` and the Architect's Decision 2. Rationale: smallest
   assumption, zero added code/test burden, formula contract holds for numeric
   inputs.
2. **Negative inputs**: accepted as-is, no clamping. Formula is deterministic;
   no requirement exists to reject or clamp negatives.
3. **Placement**: existing `src/calculator.js` (Architect Decision 1). No new
   source file or test file; "one test file per src file" convention stays
   intact.

## Test Plan

All tests go in the existing `test/calculator.test.js` using `node:test` and
`node:assert/strict`. Import must be extended to
`const { add, subtract, percent } = require('../src/calculator');`.

Required tests:

1. **Happy path**: `percent(200, 10)` → `20` (mirrors the acceptance criteria;
   title e.g. `'percent returns the percentage of a whole number'`).
2. **Zero boundary**: `percent(0, 50)` → `0` (per Architect Decision 3).
3. **Additional boundary**: `percent(200, 0)` → `0` (fraction of zero), keeping
   parity with the existing one-test-per-function convention plus the
   Architect-required zero case. Optional but recommended:
   `percent(100, 50)` → `50` and `percent(-200, 10)` → `-20` to pin the
   formula for 50% and negatives.

Optional edge-case tests (add only if they stay cheap and deterministic —
non-numeric coercion is an *observable consequence* of no-validation, not a
required contract):

- `percent('200', '10')` → `20` (numeric string coercion).
- `percent(3, 33)` → `0.99` (floating-point exactly-representable case).

Test style must match existing tests:

```js
test('percent returns the percentage of a whole number', () => {
  assert.equal(percent(200, 10), 20);
});

test('percent returns zero when the whole is zero', () => {
  assert.equal(percent(0, 50), 0);
});
```

Verification:

- `npm test` (runs `node --test`) exits 0 with no failures.
- No new dependencies, no build tooling.
- Existing `add`/`subtract` tests remain untouched and pass.

## Build Notes

Files the builder should inspect or change:

- **`src/calculator.js`** — add the `percent` function and include it in the
  existing `module.exports` object. This is the only production change.
- **`test/calculator.test.js`** — extend the destructured import to include
  `percent`; add the happy-path and zero-boundary tests (plus optional cases
  from the Test Plan) using `node:test` / `node:assert/strict`.
- **`package.json`** — read-only reference; confirms `npm test` →
  `node --test`. No changes.
- **`CLAUDE.md`** — read-only reference for conventions (CommonJS export style,
  one test file per src file, zero-dependency rule, `feature/<slug>` branch
  requirement). No changes.

Conventions the builder must honor (from `CLAUDE.md`):

- Export via `module.exports = { add, subtract, percent }`.
- Pure function, no classes, no validation logic.
- Commit on a `feature/percent-operation` branch, never straight to main.
- Do not modify `add`/`subtract` behavior or signatures, module structure,
  test layout, or tooling.

## References

- Root request: `rig-c4v` — "Add a percent operation: percent(whole, fraction)
  returns whole*fraction/100"
- Planning artifact: `docs/plans/percent-operation.md`
- Architecture artifact: `docs/architecture/percent-operation.md` (decisions:
  existing module placement; no input validation; happy-path + zero-boundary
  tests)
- Project conventions: `CLAUDE.md`
- Existing implementation: `src/calculator.js`, `test/calculator.test.js`
