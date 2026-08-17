---
title: Constitution Ratification and Vault Adoption
type: session
tags:
  - session
  - governance
  - vault
  - curriculum
created: 2026-08-17
updated: 2026-08-17
status: reviewed
source: agent
agent: Sisyphus
---

# Constitution Ratification and Vault Adoption

## Summary

Ratified this repository's first constitution and amended it twice in the same
round, ending at v1.2.0 with 15 articles. Adopted a maintainer vault and authored
the first repo-level `AGENTS.md`. Succeeded, with two real curriculum defects
found and deferred rather than silently patched.

## Work Done

- `.specify/memory/constitution.md`: filled from the unfilled 50-line template.
  - **v1.0.0** — Articles I–X, each derived from an already-enforced mechanism
    (`lesson-pack-lint.py` SFI001–SFI008, `migration-check.sh`,
    `.githooks/pre-commit`, the two maintainer skills, `.gitignore` credential
    policy, `lesson-contracts/*.toml`). Style synthesized from `darkharbour`,
    `anvil`, and `oldgrowth`.
  - **v1.1.0** — Articles XI–XIV added (Manifest Authority; Step Contracts and
    Done-Conditions; Failure Path; Human Decision Authority). Article IV expanded
    from snapshot fidelity to taught-capability fidelity.
  - **v1.2.0** — Article XV (Durable Project Memory) added. Spec Kit flow
    corrected. Beads/vault division of labor stated.
- `.specify/templates/plan-template.md`: Constitution Check replaced the generic
  placeholder with a 15-row gate table plus the verification command ladder.
- `vault/`: created with `index.md`, `_meta/tags.md`, `Sessions/About Sessions.md`,
  two ADRs, and three discovery notes.
- `AGENTS.md`: created.

## Discoveries

- [[2026-08-17-release-gate-verdict-has-no-consumer]] — the L4 README promises
  `else loop back to Coder`; no formula has that edge, and the release-gate
  PASS/FAIL verdict has no consumer at all. Both drift and a design defect.
- [[2026-08-17-human-gates-taught-not-shipped]] — two Human Gates taught in the
  manifest template, zero implemented in any pack, gap never disclosed. Nuance:
  this repo's own `speckit` workflow *does* have human gates.
- [[2026-08-17-grep-zero-hits-is-not-a-violation]] — a keyword absence in packs
  is not a violation unless the curriculum claimed the mechanism. Two of four
  candidate findings dissolved.

## Decisions

- [[ADR-001-Adopt-Constitution-And-Vault]] — ratify governance; adopt the
  convergent vault core from the three reference repos; omit the MOC ceremony.
- [[ADR-002-Descriptive-Constitution-Scope]] — codify enforced practice, not
  aspiration; handle taught-but-unshipped doctrine via Article IV generalization
  plus a curriculum-level Article XIV rather than runtime mandates.

Oracle was consulted on the descriptive-vs-aspirational question and
independently reached the same conclusion on the two dissolving findings, which
raised confidence in the scoping decision.

## Open Questions

- **Article XIV has no mechanical check.** It rests on Article IV plus review
  discipline until `TODO(ENFORCE-XIV)` ships. Should it be softened to a
  documentation-only obligation in the interim, or held back entirely? Deferred
  to the human ratifier.
- **Five enforcement TODOs are unbuilt** (`ENFORCE-XI` … `XV`). Until they land,
  Articles XI–XV are weaker than I–X, which are script-backed. This asymmetry is
  disclosed in the Sync Impact Report rather than hidden.
- **Two defects are open** (`DEFECT-B1`, `DEFECT-B3`). Both need a curriculum or
  pack change, which is outside the constitution workflow's scope.
- **Ratification date** was set to 2026-08-17 rather than backdated to when the
  practices actually became binding (the harness and hooks predate it).
