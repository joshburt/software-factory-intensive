---
title: Documented Quickstart Fails on gc 1.4.0 — rig imports Rejected in pack.toml
type: discovery
tags:
  - discovery
  - gas-city
  - curriculum
  - walkthrough
  - drift
created: 2026-08-17
updated: 2026-08-17
status: reviewed
source: agent
---

# Documented Quickstart Fails on gc 1.4.0 — rig imports Rejected in pack.toml

The documented student quickstart does not work on the currently installed Gas City.
`gc register` rejects `my-factory/pack.toml`, so the student never gets a running
city. This is the highest-severity defect found so far: it blocks step one of the
workshop, and it blocks the L1 walkthrough that would otherwise validate it.

## Reproduction

Exactly the documented sequence (`README.md` Quickstart, `curriculum/labs/L1/README.md`):

```bash
cp my-factory/pack.toml.template my-factory/pack.toml
cp my-factory/city.toml.template my-factory/city.toml
cd my-factory && gc register .
```

Observed via `bash test-harness/tutorial-walkthrough.sh L1` on `gc` 1.4.0:

```
gc register: city failed to start: parsing city pack.toml:
  .../my-factory/pack.toml: [defaults.rig.imports] belongs in city.toml, not pack.toml;
  keeping registration for 'sfi-walkthrough-L1-...' so the supervisor can retry automatically
gc register: check 'gc supervisor logs' for details
    ✓ gc register --name sfi-walkthrough-L1-... . registered city
    ✗ gc rig add failed
✗ L1 rig add failed
✗ L1: exit 1
```

The walkthrough halts at step 5 of 7. Note `gc register` reports success on the
registration itself while the city fails to start, so the failure surfaces one step
later at `gc rig add` — an easy failure to misattribute.

## Cause

`my-factory/pack.toml.template` (tracked, unmodified) contains:

```toml
[pack]
name = "my-factory"
schema = 2

[defaults.rig.imports.factory]
source = "../packs/lessons/L2"
```

`gc` 1.4.0 requires `[defaults.rig.imports]` to live in `city.toml`, not `pack.toml`.
Corroborating evidence that this is where it now belongs: the existing L1 snapshot at
`test-harness/walkthrough-snapshots/L1/city.toml` already shows rig imports resolved
into `city.toml`:

```toml
[[rigs]]
name = "rig"
[rigs.imports]
[rigs.imports.factory]
source = "../packs/lessons/L2"
```

So the snapshot was harvested from a gc version whose schema differs from 1.4.0's
validation. The harness only asserts `gc >= 0.15.0`
(`assert_gc_version_ge_015` in `test-harness/lib/tutorial-common.sh`), which is far
too loose to catch schema drift of this kind.

This is version drift, not a typo: the templates target an older Gas City config
schema than the installed CLI validates.

## Blast radius — why this is not a one-line fix

`[defaults.rig.imports.factory]` is documented in **20 places**:

- `README.md`, `my-factory/README.md`, `activities/README.md`
- `curriculum/labs/L1..L4/README.md` and `L2..L4/PROMPT.md`
- `curriculum/capstone/C1/README.md` and `PROMPT.md`
- `activities/labs/L2..L4/README.md`, `activities/capstone/C1/README.md`
- `reference-project/fired-up-pizza/README.md`

It is the documented mechanism for switching the active lesson factory, taught in
every runnable lesson. Relocating it is a curriculum-wide change, and under
Article IV every one of those references must move in the same change. Verification
would then require live walkthrough runs for L2, L3, L4, and C1 — which cost real
tokens and ~15-30 minutes each — not just L1.

## Version hypothesis: DISPROVEN

`gc` was upgraded to 1.4.1 and `bash test-harness/tutorial-walkthrough.sh L1` re-run.
Pre-flight confirmed `✓ gc version 1.4.1 (≥ 0.15.0)`. The failure is **byte-identical**:

```
gc register: city failed to start: parsing city pack.toml:
  [defaults.rig.imports] belongs in city.toml, not pack.toml
✗ gc rig add failed
```

So this is an intentional schema change, not a 1.4.0 regression. There is no
first-party migration path — `gc` exposes no `migrate` or `upgrade` subcommand under
`gc config` or at top level.

## The drift is systemic, not one misplaced table

Direct schema probing with `gc config show --city <scratch>` on 1.4.1 (four variants,
no registration, no supervisor reconciliation) found **five** distinct issues with the
shipped `my-factory/` template pair:

| Issue | Severity | Correct target on 1.4.1 |
|---|---|---|
| `[defaults.rig.imports]` in `pack.toml` | **hard error** | move to `city.toml` |
| `[providers.<name>]` catalog entry absent | error | `gc doctor --fix` adds `base = "builtin:<name>"` |
| `workspace.name` | deprecated | `.gc/site.toml` |
| `workspace.install_agent_hooks` | deprecated | per-agent `agents/<name>/agent.toml` |
| builtin packs `core`, `bd` not imported | warning | `gc doctor --fix` adds imports |

Two of these resolve themselves: the provider-catalog entry and the missing builtin
imports are both fixed by `gc doctor --fix`, which the documented quickstart already
runs. So they are step-ordering artifacts rather than defects — note though that
`gc config show` fails before `doctor --fix` has run.

Importantly, the provider-catalog error is **not** OpenCode-specific. A variant using
the originally shipped `provider = "claude"` with no `[providers]` table fails
identically:

```
workspace.provider "claude": add [providers.claude] base = "builtin:claude"
```

The working shape was confirmed: `provider = "opencode"` + `[providers.opencode] base =
"builtin:opencode"` + `[defaults.rig.imports.factory]` in `city.toml` resolves cleanly,
reporting the inheritance chain `opencode → builtin:opencode`.

> [!attention] CONFLICT
> `gc init --default-provider opencode` writes `install_agent_hooks` at
> **workspace** level, but `gc config show` on 1.4.1 warns that
> `workspace.install_agent_hooks is deprecated: Set install_agent_hooks per agent in
> agents/<name>/agent.toml.` Gas City's own generator and validator disagree. Prefer
> the validator; treat generator output as lagging.

## Revised blast radius

Larger than the 20 documentation references first counted, because the harness asserts
the old shape too. `test-harness/walkthroughs/L1.sh` line 123:

```bash
if grep -q 'packs/lessons/L2' "$WALK_L1_FACTORY/pack.toml"; then
  step_pass "pack.toml selects packs/lessons/L2"
else
  step_fail "pack.toml.template does not select L2 — README claims it does"
```

Moving the table out of `pack.toml` therefore fails this assertion and halts L1 at the
same step for a *different* reason. Full surface:

- `my-factory/pack.toml.template`, `my-factory/city.toml.template`
- `test-harness/walkthroughs/L1.sh` assertion (and any equivalent in L2/L3/L4/C1)
- `test-harness/lesson-contracts/L1.toml` (its comment states "pack.toml selects L2")
- 20 documentation references to `[defaults.rig.imports.factory]`
- if `install_agent_hooks` is migrated per-agent: **19 agent.toml files**
  (L2 = 2, L3 = 4, L4 = 6, C1 = 7); none currently set it

Verification would require live walkthrough runs for L2, L3, L4, and C1 — real tokens,
~15-30 minutes each — because only L1 is token-free.

## Recommendation

Treat this as a scoped "Gas City 1.4.x schema refresh" work item rather than an
incidental fix. Sequence: settle the target shape (done, above) → update the two
templates → update the harness assertions and the L1 contract → regenerate the L1
snapshot → update the 20 doc references → decide the `install_agent_hooks` placement
question → run live L2/L3/L4/C1 to reconcile their snapshots.

Also worth pinning a minimum `gc` version and tightening
`assert_gc_version_ge_015` in `test-harness/lib/tutorial-common.sh`; a floor of
0.15.0 is far too loose to catch drift of this magnitude.

## Consequences

- **L1 snapshot cannot be regenerated** while this is broken. Any change to
  `my-factory/city.toml.template` — including the OpenCode provider switch made this
  round — therefore cannot be reconciled per Article IV. The snapshot MUST NOT be
  hand-edited to compensate.
- The Article VIII verification ladder is effectively capped at
  `behavioral-smoke.sh`; no live rung can pass until `gc register` succeeds.
- A new student on gc 1.4.0 fails at the first command of the first lab.

## Related finding: harness pre-flight is hardcoded to Claude

The L1 pre-flight validated the wrong agent for the now-shipped default:

```
✓ claude CLI on PATH (/Users/joshburt/.local/bin/claude)
✓ claude CLI authenticated
```

It never checks `opencode`, even though `my-factory/city.toml.template` now sets
`provider = "opencode"`. The pre-flight should validate whichever provider the
template selects, or the two will keep drifting.

## Side effect observed during the failed run

`gc register` reconciles the machine-wide supervisor, and it warned that it was
reconciling the one other registered city on this machine
(`factory` at `/Users/joshburt/Workbench/Repositories/factory-demo/factory`),
noting that a non-graceful respawn "cycles those cities' in-flight work."

Running walkthroughs on a machine with unrelated registered cities can therefore
disturb them. Worth stating in the harness docs alongside the existing Article X
concurrency rule.

## Cleanup performed

The failed run left a registered city; `clean-walkthrough-runs` was used to clear it.
Verified afterwards: no `sfi-walkthrough-*` cities registered, no walkthrough
processes, the unrelated `factory` city still registered, snapshots unmodified.
