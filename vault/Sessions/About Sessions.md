---
title: About Sessions
type: reference
tags:
  - reference
  - vault
created: 2026-08-17
updated: 2026-08-17
status: draft
source: agent
---

# About Sessions

Session notes are the append-only record of what happened in a work round.
They exist so a future maintainer or agent can reconstruct not just what
changed but what was tried, what was rejected, and what remained open.

## Convention

- **Filename**: `YYYY-MM-DD-topic-slug.md`. One note per work round. If a
  round spans days, keep the start date and note the span in the body.
- **Append-only**: correct a session note by appending, never by rewriting
  history. If a later round proves a session's conclusion wrong, add a
  `> [!warning] STALE` marker and link to the note that supersedes it.
- **Required frontmatter**: `title`, `type: session`, `tags`, `created`,
  `updated`, plus `status` and `source`. Add `agent:` when an agent authored it.

## Body skeleton

```markdown
## Summary
One paragraph: what this round set out to do and whether it succeeded.

## Work Done
What actually changed, with paths.

## Discoveries
Non-obvious findings. Each one that matters gets its own note in
`Discoveries/` — link it here rather than duplicating it.

## Decisions
Decisions made, with reasons. Each one gets an ADR in `Decisions/` — link it.

## Open Questions
What was left unresolved, and what would resolve it.
```

## What does not go here

Routine mechanical work with no discovery and no decision does not need a
session note. The git history covers it. Write a session note when the round
produced reasoning worth keeping.
