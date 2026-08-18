---
title: workspace.name Is Deprecated in Favor of .gc/site.toml
type: discovery
tags:
  - discovery
  - gas-city
  - drift
created: 2026-08-17
updated: 2026-08-17
status: draft
source: agent
---

# workspace.name Is Deprecated in Favor of .gc/site.toml

Found during the same `gc config show` schema probing that produced ADR-003, and
deliberately **not** migrated in that change — this is a separate deprecation with
its own harness implications, not part of the rig-imports schema break.

## Evidence

`gc config show` on Gas City 1.4.1 warns:

```
workspace identity fields are deprecated in v2; move them to .gc/site.toml
  (workspace.name); move them to .gc/site.toml (run `gc doctor --fix` if this is
  the root city.toml; fragments must be updated by hand)
```

`my-factory/city.toml.template` still sets `workspace.name = "my-factory"`
directly, as does every inline `city.toml` heredoc in
`test-harness/walkthroughs/{L2,L3,L4,C1}.sh`.

## Why this was not migrated alongside ADR-003

- `gc doctor --fix` reportedly handles this automatically for a root `city.toml` —
  unverified this session, but if true it may need no template change at all,
  only confirmation.
- `test-harness/walkthroughs/L1.sh` line ~118 (`sed -i '' "s/name = \"my-factory\"/..."`)
  sed-patches this exact literal line for scratch-city isolation. Moving the field
  to `.gc/site.toml` would require rewriting that isolation mechanism, not just the
  template — a second harness change with its own risk of the same
  "fix-the-template-but-not-the-harness" trap ADR-003 hit once already.
- It is a warning, not a hard error (unlike the rig-imports break), so it does not
  block the quickstart. Lower urgency than what ADR-003 fixed.

## Resolution

Not resolved. Tracked here rather than fixed under time pressure in the same round
as the higher-urgency schema break. If picked up: first confirm whether
`gc doctor --fix` actually relocates `workspace.name` for a root `city.toml`
(the warning text hedges "if this is the root city.toml" — the scratch cities this
harness creates via `gc register .` likely qualify, but this is unverified), then
decide whether the harness's sed-based isolation trick still works against
`.gc/site.toml` or needs its own fix.
