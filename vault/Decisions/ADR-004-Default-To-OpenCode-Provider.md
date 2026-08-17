---
title: ADR-004 Default to OpenCode Provider, Promote It to Recommended
type: decision
tags:
  - decision
  - gas-city
  - curriculum
created: 2026-08-17
updated: 2026-08-17
status: draft
source: agent
---

# ADR-004: Default to OpenCode Provider, Promote It to Recommended

## Context

This session switched `my-factory/city.toml.template`'s `provider` from `claude` to
`opencode` on explicit instruction. That template edit created a direct contradiction
in `installation.md`: the "### Recommended" section still names only Claude Code and
Codex CLI, each tied to a specific paid subscription tier ("Claude Max 20×", "Codex
Pro 20× or similar") described as sufficient "for sustained multi-agent runs." A
participant following the guide top to bottom would install a Recommended agent, then
find the shipped template already configured for a different, non-recommended one.

Evidence available this session on OpenCode's Gas City support (verified directly
against upstream source, not inferred):

- A dedicated, versioned Gas City plugin (`internal/bootstrap/packs/core/overlay/per-provider/opencode/.opencode/plugins/gascity.js`)
  providing the same session-lifecycle hooks Claude gets.
- A first-class skill sink (`.opencode/skills`), MCP projection to `opencode.json`,
  and a dedicated session-log reader — none of this is a shim.
- OpenCode itself requires no paid subscription; it runs against pay-as-you-go API
  credits (Anthropic, OpenRouter) or provider-native auth (GitHub Copilot oauth). This
  environment already has all three configured (`opencode auth list`).
- No hard evidence yet on whether OpenCode sustains a 6-7 agent factory's throughput
  as reliably as the paid Claude/Codex tiers the Recommended section calls out for
  that exact reason. That evidence is what the pending live L2/L3/L4/C1 walkthrough
  runs will produce.

## Decision

Promote OpenCode into the "### Recommended" tier in `installation.md`, alongside
Claude Code and Codex CLI, rather than reverting the shipped default back to Claude.

Reject reverting the default: it would contradict this session's explicit
instruction to configure the factory for OpenCode, and it would discard genuine,
verified first-party support in favor of the status quo for no stated reason beyond
inertia.

This decision is **provisional on the live walkthrough runs** already queued
(L2, L3, L4, C1) actually passing on the OpenCode provider. If a live run surfaces an
OpenCode-specific reliability or throughput problem under sustained multi-agent load,
that is the revisit trigger below, and the Recommended promotion should be reverted
or qualified before this ADR is considered settled rather than provisional.

## Consequences

- **Easier**: `installation.md`'s Recommended section and the shipped template agree.
  A participant who follows the guide top-to-bottom gets a config that matches what
  they installed.
- **Easier**: no paid subscription is required to start the workshop — participants
  can begin with pay-as-you-go credits and upgrade later if they hit throughput limits.
- **Harder**: the curriculum now recommends three agents instead of two, and the
  "Minimum: one of the above at a paid tier" framing needs adjusting since OpenCode
  doesn't require a paid tier at all — a follow-on doc fix, tracked separately.
- **Harder**: this is provisional. If it's wrong, it's wrong in a way that costs a
  student real setup time before they discover it.

## Alternatives Considered

### Alternative 1: Revert the default to `claude`

Rejected. Discards this session's explicit instruction and genuine, verified
first-party OpenCode support, for no reason beyond "that's what it was before."

### Alternative 2: Leave the contradiction as-is, fix only the template

Rejected. This is exactly the taught-vs-shipped inconsistency Article IV forbids —
the install guide would recommend one thing while the shipped config defaults to
another, with no acknowledgment either way.

### Alternative 3: Make OpenCode the *sole* recommendation, demote Claude/Codex

Rejected as premature. Claude Code and Codex CLI are what the existing reference
project (`reference-project/fired-up-pizza/CLAUDE.md`) and most walkthrough snapshots
were authored against. Demoting them is a larger claim than this session's evidence
supports.

## Revisit Trigger

Revisit immediately if any of the live L2/L3/L4/C1 walkthrough runs (queued this
session) fail on the OpenCode provider for a reason attributable to OpenCode itself
(rate limits, model reliability, missing hook behavior) rather than to the schema
migration being validated. If that happens, downgrade OpenCode's `installation.md`
tier back to "Also fully supported" and record the failure mode here.
