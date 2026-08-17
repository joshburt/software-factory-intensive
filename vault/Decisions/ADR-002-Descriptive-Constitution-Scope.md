---
title: ADR-002 Constitution Codifies Enforced Practice, Not Aspiration
type: decision
tags:
  - decision
  - governance
  - human-gate
created: 2026-08-17
updated: 2026-08-17
status: draft
source: agent
---

# ADR-002: Constitution Codifies Enforced Practice, Not Aspiration

## Context

The v1.1.0 amendment audited the workshop curriculum (W1–W4), the three
`curriculum/*_TEMPLATE.md` manifest templates, and the shipped
`packs/lessons/C1` factory. It found normative doctrine the curriculum teaches
that the constitution had not codified — but the doctrine split in two:

- **Taught and implemented**: manifest section authority, per-step
  done-conditions and failure behavior, role isolation.
- **Taught but absent from every shipped pack**: human approval gates
  (`SOFTWARE_FACTORY_MANIFEST_TEMPLATE.md` defines two; zero packs implement
  one), and conditional loop-back routing on a FAIL verdict.

This forced a governance-architecture question: should a constitution codify
what the repository *does*, or what it *teaches*?

## Decision

Codify enforced practice. Handle the taught-but-unshipped doctrine through two
mechanisms instead of aspirational mandates:

1. **Generalize Article IV** from snapshot fidelity to taught-capability
   fidelity — a taught capability the shipped pack lacks must be either
   implemented or plainly disclosed.
2. **Add Article XIV (Human Decision Authority)** as a *curriculum-level*
   doctrine: the material must teach human ownership of irreversible,
   trust-surface-expanding, and cross-system decisions, and must disclose where
   the reference factory omits a gate it teaches. Explicitly forbid resolving a
   gap by deleting the teaching.

Also rejected two candidate articles that dissolved under scrutiny — see
`vault/Discoveries/2026-08-17-grep-zero-hits-is-not-a-violation.md`.

## Consequences

- **Easier**: every article traces to a real mechanism, so the repository is
  compliant on ratification day and the plan-phase Constitution Check is
  meaningful rather than permanently red.
- **Easier**: the two real defects became ordinary tracked defects
  (`TODO(DEFECT-B1)`, `TODO(DEFECT-B3)`) rather than unfixable constitutional
  violations.
- **Harder**: Article XIV is the only article without a mechanical check. It
  rests on Article IV plus review discipline until `TODO(ENFORCE-XIV)` ships.
  This weakness is disclosed in the Sync Impact Report rather than hidden.

## Alternatives Considered

### Alternative 1: Aspirational — mandate human gates and improvement loops

Rejected. The repository would violate its own constitution on day one, and the
Governance section states that undocumented violations are blockers — creating a
permanent unfixable blocker state. Worse, it would normalize ignoring the
constitution, which is the "silent dilution" the Governance section forbids.

### Alternative 2: Pure consistency obligation, no human-authority article

Rejected as a dodge. A bare consistency rule can be satisfied by *deleting* the
Human Gates section from the manifest template — resolving the inconsistency by
removing the safety teaching. Article XIV clause 1 closes that exit by requiring
the doctrine to remain taught.

## Revisit Trigger

Revisit if the capstone is ever redesigned as a shared or hosted factory rather
than a per-student local run. At that point the repository would own the runtime,
and a runtime-enforceable human-safety article (in the style of `darkharbour`'s
Article VIII) would become both possible and necessary.
