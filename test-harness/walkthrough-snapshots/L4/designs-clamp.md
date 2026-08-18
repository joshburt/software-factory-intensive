# Clamp Operation Design

## Interface

A single pure function added to the existing calculator module.

```js
clamp(x, lo, hi) // returns a Number
```

- `x` (Number) — the value to bound.
- `lo` (Number) — the inclusive lower bound.
- `hi` (Number) — the inclusive upper bound.
- Returns (Number) — `x` clamped to the inclusive interval `[lo, hi]`.

Placement (per architecture decision, Option A):

- `clamp` lives in `src/calculator.js`, alongside `add` and `subtract`, with
  no comment or JSDoc block (matching the existing bare-function style of that
  file).
- Exported via the existing object-literal pattern:
  `module.exports = { add, subtract, clamp };`
- Tests are added to the existing `test/calculator.test.js`.

The function is a single-expression implementation; the canonical form is:

```js
function clamp(x, lo, hi) {
  return Math.max(lo, Math.min(x, hi));
}
```

The equivalent `Math.min(hi, Math.max(lo, x))` is acceptable — pick one and
keep it consistent. Both forms yield identical results for all numeric inputs.

## Behavior

Given numeric inputs:

- If `lo <= x <= hi`, returns `x` unchanged.
- If `x < lo`, returns `lo`.
- If `x > hi`, returns `hi`.

The bounds are inclusive on both ends: `clamp(lo, lo, hi) === lo` and
`clamp(hi, lo, hi) === hi`.

Behavioral properties (matching the existing calculator conventions):

- Pure function: no mutation of inputs, no side effects, no state.
- No validation, no coercion, no error-throwing. Inputs are assumed to be
  numbers; behavior for non-numeric or inverted-bound (`lo > hi`) inputs is
  intentionally undefined (architecture decision, Option D). With the
  `Math.min`/`Math.max` form, such inputs naturally degrade to `NaN`, which is
  consistent with the rest of the codebase and is not a contract.
- Single expression — no `if`/`else` branches needed.

## Edge Cases

Cases that must behave predictably and be covered by tests:

1. **Strictly in range**: `clamp(5, 0, 10) === 5`.
2. **Below floor**: `clamp(-3, 0, 10) === 0`.
3. **Above ceiling**: `clamp(12, 0, 10) === 10`.
4. **Inclusive lower bound**: `clamp(0, 0, 10) === 0`.
5. **Inclusive upper bound**: `clamp(10, 0, 10) === 10`.
6. **Equal bounds (`lo === hi`)**: `clamp(7, 5, 5) === 5` — a degenerate
   interval; the only legal result is the shared boundary value. This is
   well-defined and should be asserted.
7. **Fractional values**: `clamp(2.5, 0, 5) === 2.5` — no integer truncation.
8. **Negative values and negative bounds**:
   - `clamp(-5, -10, -1) === -5` (in range),
   - `clamp(-20, -10, -1) === -10` (below floor),
   - `clamp(0, -10, -1) === -1` (above ceiling).

Explicitly out of scope (do NOT add tests that assert a specific result):

- Non-numeric inputs (`NaN`, strings, `undefined`) — behavior undefined.
- Inverted bounds (`lo > hi`) — behavior undefined.
- `Infinity` / `-Infinity` — numerically valid but not part of the required
  matrix; optional, but keep the suite focused on the cases above.

## Test Plan

All tests go in the existing `test/calculator.test.js`, using the existing
style: `node:test` + `node:assert/strict`, one `test(...)` per behavior. The
`require` at the top must be updated to destructure `clamp`:

```js
const { add, subtract, clamp } = require('../src/calculator');
```

Required test cases (minimal set satisfying acceptance criteria 2 and 4):

| Test name | Assertion |
|---|---|
| `clamp returns the value when it is within bounds` | `assert.equal(clamp(5, 0, 10), 5)` |
| `clamp returns the lower bound when below the floor` | `assert.equal(clamp(-3, 0, 10), 0)` |
| `clamp returns the upper bound when above the ceiling` | `assert.equal(clamp(12, 0, 10), 10)` |
| `clamp treats the lower bound as inclusive` | `assert.equal(clamp(0, 0, 10), 0)` |
| `clamp treats the upper bound as inclusive` | `assert.equal(clamp(10, 0, 10), 10)` |
| `clamp returns the shared value when bounds are equal` | `assert.equal(clamp(7, 5, 5), 5)` |
| `clamp preserves fractional values` | `assert.equal(clamp(2.5, 0, 5), 2.5)` |
| `clamp handles negative values within bounds` | `assert.equal(clamp(-5, -10, -1), -5)` |
| `clamp clamps negative values below the floor` | `assert.equal(clamp(-20, -10, -1), -10)` |
| `clamp clamps positive values above a negative ceiling` | `assert.equal(clamp(0, -10, -1), -1)` |

Verification:

- Run `npm test` (which runs `node --test`). All new `clamp` tests must pass
  and the existing `add`/`subtract` tests must remain green.
- No new dependencies, no `package.json` changes, no build tooling changes.

## Build Notes

Files the builder should inspect or change:

- **Change — `src/calculator.js`**: add the `clamp` function (single
  expression, see Interface) and update the export to
  `module.exports = { add, subtract, clamp };`.
- **Change — `test/calculator.test.js`**: update the destructured `require` to
  include `clamp`; add the test cases from the Test Plan. Keep the existing
  `add` and `subtract` tests untouched.
- **Inspect — `docs/plans/clamp.md`**: scope, acceptance criteria, and the
  explicit out-of-scope list (no validation, no `lo > hi` contract).
- **Inspect — `docs/architecture/clamp.md`**: confirmed decisions — Option A
  (existing files) and Option D (undefined behaviors unspecified).
- **Inspect — `CLAUDE.md`**: project conventions (CommonJS,
  `module.exports = { ... }`, one test file per src file, `node:test`).
- **Inspect — `package.json`**: `npm test` runs `node --test`; must remain
  unchanged.

Process requirements:

- Implement on a `feature/clamp` branch, never straight to main.
- Do not modify `package.json`, add dependencies, refactor `add`/`subtract`,
  or introduce validation/error-throwing for invalid inputs.

## References

- [Feature Plan](docs/plans/clamp.md) — scope, stories, acceptance criteria.
- [Architecture Decision](docs/architecture/clamp.md) — placement (Option A)
  and undefined-behavior (Option D) decisions.
- [CLAUDE.md](CLAUDE.md) — project conventions and workflow expectations.
- [src/calculator.js](src/calculator.js) — existing implementation.
- [test/calculator.test.js](test/calculator.test.js) — existing test suite.
