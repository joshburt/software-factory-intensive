---
title: ADR-001 Adopt a Constitution and a Maintainer Vault
type: decision
tags:
  - decision
  - governance
  - vault
created: 2026-08-17
updated: 2026-08-17
status: draft
source: agent
---

# ADR-001: Adopt a Constitution and a Maintainer Vault

## Context

Before 2026-08-17 this repository had no ratified governance. The Spec Kit
constitution at `.specify/memory/constitution.md` was still the unfilled
50-line template, and there was no repo-level `AGENTS.md` and no maintainer
memory of any kind. Real engineering norms existed, but only as scripts:
`test-harness/lesson-pack-lint.py` (banned patterns SFI001–SFI008),
`test-harness/migration-check.sh`, `.githooks/pre-commit`, the
`validate-lesson-content` and `clean-walkthrough-runs` skills, and the
`.gitignore` credential policy. `.gitignore` line 79 even referred to "the
constitution" — a forward reference to a document that did not exist.

Three sibling repositories in the same ecosystem — `darkharbour`, `anvil`, and
`oldgrowth` — each run a ratified constitution plus an Obsidian-style vault for
durable memory, and each independently converged on the same core mechanics.

## Decision

Ratify a constitution derived strictly from already-enforced practice, and adopt
a maintainer vault at `vault/` with the convergent core of the three reference
repositories: three record types (`Decisions/`, `Discoveries/`, `Sessions/`), the
`draft → reviewed → canonical` lifecycle with `canonical` human-only, a required
frontmatter field set, and a controlled tag vocabulary in `_meta/tags.md`.

Deliberately omit the ceremony that does not fit a nine-session curriculum:
`oldgrowth`'s three-tier Maps of Content and its ~250-line vault article, and
(for now) a mechanical vault audit script.

## Consequences

- **Easier**: decisions and discoveries stop vanishing at the end of a session.
  Governance becomes citable in plan-phase Constitution Checks.
- **Easier**: agents get a single operational entry point in `AGENTS.md` instead
  of inferring norms from scripts.
- **Harder**: the vault only pays off if it is maintained. An unmaintained vault
  is worse than none, per Article XV. Enforcement is currently review discipline
  only — there is no vault audit yet (`TODO(ENFORCE-XV)`).
- **Harder**: two more surfaces must stay consistent with the constitution.

## Alternatives Considered

### Alternative 1: Constitution only, no vault

Rejected. The v1.1.0 audit produced two real defect findings and several
governance decisions whose only record would have been an HTML comment inside
the constitution and a chat transcript. The Sync Impact Report was already being
overloaded as a decision log.

### Alternative 2: Port the reference vaults wholesale

Rejected as disproportionate. `darkharbour` carries 63 ADRs and ~90 discoveries;
`oldgrowth`'s constitution is 1558 lines. This repository has no note volume to
justify a MOC hierarchy, and building one first would be speculative structure.

## Revisit Trigger

Revisit if `Decisions/` exceeds roughly 20 notes or `Discoveries/` exceeds
roughly 40 — at that volume, navigation without Maps of Content starts to fail
and the reference repos' MOC tiers become worth their cost. Also revisit if a
vault note is ever found stale for more than one work round, which would mean
review discipline alone is insufficient and `TODO(ENFORCE-XV)` must be built.
