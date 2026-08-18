---
title: Software Factory Intensive Vault — Home
type: reference
tags:
  - reference
  - vault
created: 2026-08-17
updated: 2026-08-17
status: draft
source: agent
---

# Software Factory Intensive Vault — Home

Maintainer memory for this curriculum: why it is shaped the way it is, what
was discovered while building it, and what happened in each work round. This
is not student-facing material — per Article V, no vault path may appear in
curriculum content.

Governed by **Article XV — Durable Project Memory** in
`.specify/memory/constitution.md`. Read that article before writing here.

## Navigation

| Directory | What it holds | Write here when |
|---|---|---|
| `Decisions/` | Curriculum-design and architectural decisions, as `ADR-NNN-Title.md` | A decision is made with stated reasons |
| `Discoveries/` | Non-obvious constraints, gaps, taught-vs-shipped conflicts | Something cost discovery time, or sources disagree |
| `Sessions/` | Work-round summaries, `YYYY-MM-DD-topic.md`, append-only | A work round concludes |
| `Reference/` | Dated assessments, guides, research corpus | A finding needs a durable home that isn't a decision, a discovery, or a session |
| `_meta/tags.md` | The controlled tag vocabulary | A genuinely new tag is needed |

## Where else truth lives

| Source | What it holds |
|---|---|
| `.specify/memory/constitution.md` | The constitution — supreme on all normative questions |
| `AGENTS.md` | How to operate in this repo as an agent; defers to the constitution |
| `bd` (Beads) | Work items and status — never markdown TODO lists |
| `test-harness/walkthrough-snapshots/` | Harvested run evidence; the source of truth for what lessons produce |
| `troubleshooting/` | Student-facing failure-mode guides |

## Read at session start

1. This file, for orientation.
2. `Decisions/` and `Discoveries/`, for prior decisions and known constraints.
3. The constitution, for the rules that bind the work.

## Open threads

Defects found and not yet resolved are tracked as `TODO(DEFECT-*)` in the
constitution's Sync Impact Report, each linked to a note in `Discoveries/`.

Defects in dependencies we do not control — and the local workarounds standing in for
them — are tracked in [[Upstream Issues]]. Check that file before removing any
workaround, and re-run its detection tests after adopting a new `gc` or `bd` release.
