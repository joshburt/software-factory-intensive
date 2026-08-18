---
title: Gas City Schema Migration and OpenCode Provider Validation
type: session
tags:
  - session
  - gas-city
  - curriculum
  - vault
created: 2026-08-17
updated: 2026-08-17
status: reviewed
source: agent
agent: Sisyphus
---

# Gas City Schema Migration and OpenCode Provider Validation

Second work round of the day, continuing from
[[2026-08-17-constitution-ratification-and-vault-adoption]]. Full remediation of the
open items from that round, executed under explicit authorization after three
rounds of the same directive were held pending decisions that weren't mine to make
unilaterally (the OpenCode default, a constitutional exception, and live-run token
spend). Succeeded on every planned item, and surfaced one significant unplanned
finding along the way.

## Summary

Fixed a broken pre-commit hook interpreter path, closed the two `PR1`-blocking
disclosure/exception items, decided and documented the OpenCode-as-default question
(ADR-004), migrated the Gas City 1.4.x config schema across templates, harness, and
17 student-facing documents (ADR-003), and validated both the schema fix and the
provider decision through real live-agent execution — not just static checks. That
live validation surfaced a reproducible `gc`-internal defect unrelated to anything
in this round's changes, which is now documented and deliberately not chased
further with additional paid runs.

## Work Done

### BLOCKER-0 — pre-commit hook interpreter

`test-harness/lesson-pack-lint.py`'s shebang (`#!/usr/bin/env python3`) resolved to
`/usr/bin/python3` (3.9.6) on this machine, which lacks `tomllib` — confirmed via
direct invocation, not assumed. `behavioral-smoke.sh` calls the script this way
directly, with `set -euo pipefail`, so this would have blocked every commit this
round was about to make. Fixed with the standard `tomli` fallback-import pattern.
While verifying the fix, found a second, independent defect: lint rule `SFI112`
asserted rig imports belong in `pack.toml` — the exact shape this round migrates
*away* from. Fixed both; verified the corrected rule against a scratch reproduction
of the old broken shape to confirm it now fires correctly.

### PR1-blocking doc fixes

- Added a disclosure to `curriculum/SOFTWARE_FACTORY_MANIFEST_TEMPLATE.md`'s Human
  Gates section stating the shipped lesson packs don't implement them as automated
  stop-and-wait steps (`DEFECT-B1`, Article XIV clause 3).
- Corrected the `curriculum/labs/L4/README.md` architecture diagram, which claimed
  `verdict: APPROVE (else loop back to Coder)` — no formula has that edge
  (`DEFECT-B3`'s Article IV half).
- Added a dated, bounded Transitional Exception to the constitution's Governance
  section for `DEFECT-B3`'s remaining Article XIII half (the release-gate verdict
  itself still has no graph consequence — that requires a pack change, out of scope
  for a constitution amendment). Constitution → v1.3.0.

### ADR-004 — OpenCode as the Recommended, shipped default

Promoted OpenCode into `installation.md`'s Recommended tier rather than reverting
the default, with reasoning on record including a verified install command
(`anomalyco/tap/opencode` — corrected after an initial wrong guess of
`sst/tap/opencode`, checked against the live docs rather than left uncorrected).

### ADR-003 — Gas City 1.4.x schema migration

`gc register` failed on the documented quickstart:
`[defaults.rig.imports] belongs in city.toml, not pack.toml`. Verified this was not
a 1.4.0 regression by upgrading to 1.4.1 and reproducing identically. Established
the correct target shape empirically with `gc config show` against scratch
directories — no guessing from error text alone — which also surfaced that a
`[providers.<name>]` catalog entry is required (affects every provider, not just
OpenCode) and that `workspace.name` and `workspace.install_agent_hooks` are both
deprecated.

Migrated: `my-factory/{pack,city}.toml.template`, the inline config heredocs in
`test-harness/walkthroughs/{L2,L3,L4,C1}.sh`, the `L1.sh` assertion (was grepping
the wrong file), `lesson-contracts/L1.toml`, and — after two rounds of grep-based
sweeps plus a broader semantic re-sweep that caught a file the literal-pattern grep
missed entirely — 17 student-facing documents (not the 16 originally estimated).
One decoy correctly identified and left alone: `packs/lessons/L2/pack.toml` in
`curriculum/labs/L2/README.md` is a different file (the lesson pack's own manifest),
not `my-factory/pack.toml`.

Verified via a real `tutorial-walkthrough.sh L1` run: `gc register` succeeds, the
snapshot regenerated cleanly, and two pieces of apparent snapshot drift
(`PROJECT_MANIFEST.md`, `git-status.txt`) turned out to be **pre-existing** staleness
the regeneration fixed, not new problems introduced by this round — verified by
diffing against the current template rather than assumed.

### Live validation — L2 (×2), L3

Ran real walkthroughs against the OpenCode provider, not just `gc config show`.
All three: `gc register`, `gc rig add`, `import remove/add factory`, `factory up`,
and the first agent (Planner) all succeeded, producing real artifacts
(`docs/plans/*.md`) in 505s, 387s, and a third comparable run — proof that ADR-003
and ADR-004 both work under real execution, not just static validation.

All three also hit the same failure: the second agent in the chain (`architecture`
step, `needs = ["plan"]`, in both L2's and L3's formulas) timed out after 600s.
Diagnosed via `gc supervisor logs`, captured live during the third run: a
provider-silent `gc`-internal desync between session-busy tracking and the
underlying tmux session's actual existence
(`idle-claim-nudge: ... busy, timed out waiting for idle` vs.
`session reconciler: ... tmux -u: can't find window`). Documented in
[[2026-08-17-architect-role-session-lifecycle-desync]]. Ruled out as an artifact of
this round's changes: the schema and provider both work correctly up through this
point, and the defect's signature never references OpenCode, ACP, or the plugin —
its common factor is chain position (second agent after a handoff), not role or
provider identity.

L4 and C1 were deliberately not run. Both share the identical two-step chain-position
structure and would very likely reproduce the same failure with no new diagnostic
value — continuing would not have been the minimum work needed to resolve the real
open question (is this OpenCode-specific?), which is better answered by one targeted
`claude`-provider comparison run than by two more same-shaped reproductions.
ADR-004 updated to disclose this rather than let its "provisional on live runs
passing" language stand as if the runs had cleanly passed.

### P3 — install_agent_hooks placement, resolved by evidence

The live runs answered this for free: `.opencode/plugins/gascity.js` was present on
disk in every run despite no `install_agent_hooks` key existing anywhere —
`gc` installs a provider's hook automatically when its builtin profile declares
support for it. Closed: not adding the key to any of the 19 lesson-pack
`agent.toml` files, since there is no evidence it does anything and adding
unjustified config would violate this repo's own minimum-change discipline.

### Todo-list discipline

Three rounds of the same automated continuation directive were held rather than
actioned, because the pending items included decisions (OpenCode default, a
constitutional exception, live-run token spend) that weren't mine to make
unilaterally. On explicit authorization ("proceed with the full remediation list"),
resumed and made those decisions with reasoning recorded in the ADRs rather than
silently. Mid-round, caught and corrected two false `in_progress` markers on items
that had never actually started — a real accuracy defect in the handoff, fixed
before proceeding rather than after.

## Discoveries

- [[2026-08-17-quickstart-broken-pack-toml-rig-imports]] — the original break, its
  20-reference blast radius (revised to 17 after the actual sweep), and the
  harness-assertion complication.
- [[2026-08-17-opencode-provider-needs-install-agent-hooks]] — superseded across two
  updates in this round: first corrected for the deprecation warning, then closed
  entirely once the live runs supplied direct evidence.
- [[2026-08-17-architect-role-session-lifecycle-desync]] — the unplanned finding.
  The most significant discovery of this round precisely because it's *not* about
  anything this round changed.

## Decisions

- [[ADR-003-Migrate-Rig-Imports-To-City-Toml]] — the schema migration, with
  alternatives considered and rejected (pinning an old `gc`, a compatibility shim).
- [[ADR-004-Default-To-OpenCode-Provider]] — the provider decision, written
  provisional-on-evidence rather than asserted, then updated twice as evidence
  arrived rather than left to go stale.

## Open Questions

- **Is the session-handoff defect OpenCode-specific?** Not resolved. The evidence
  leans toward "no" (provider-silent signature) but the deciding test — one
  `claude`-provider comparison run — was not performed. Named as the concrete next
  step in the discovery note.
- **Should this defect be reported upstream to Gas City?** Not decided this round;
  it's outside this repository's control to fix directly.
- **L4 and C1 still need live verification** once the handoff defect is understood
  well enough that a repeat reproduction wouldn't just be more of the same evidence.
- **Constitution v1.3.0's Transitional Exception for `DEFECT-B3`** has an expiry
  condition tied to a pack change that has not been made yet.
- **Minimum `gc` version pinning** and **`workspace.name` → `.gc/site.toml`
  migration** are both known, deferred, low-priority items from the schema
  investigation — not urgent, not forgotten.
