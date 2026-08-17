---
title: installation.md Understates OpenCode Support and Links a Moved Repository
type: discovery
tags:
  - discovery
  - curriculum
  - gas-city
  - drift
created: 2026-08-17
updated: 2026-08-17
status: reviewed
source: agent
---

# installation.md Understates OpenCode Support and Links a Moved Repository

`installation.md` lists OpenCode under a heading that reads "Others (compatibility
not guaranteed)" and links it to a repository that no longer hosts the project.
Both claims are wrong, and they steer students away from a fully supported path.

## Evidence

`installation.md` line 68 heads the list "Others (compatibility not guaranteed)",
and line 71 reads:

```markdown
- [OpenCode](https://github.com/opencode-ai/opencode)
```

Against that, Gas City treats OpenCode as a first-class harness. Verified in
`gastownhall/gascity` at commit `0b10e4e4d9648cdaf913193b3eed207e71bbdbb9` (v1.4.1):

| Capability | Location |
|---|---|
| Provider definition | `internal/worker/builtin/profiles.go` → `"opencode"`, with `SupportsACP: true`, `SupportsHooks: true`, `InstructionsFile: "AGENTS.md"` |
| Native plugin | `internal/bootstrap/packs/core/overlay/per-provider/opencode/.opencode/plugins/gascity.js` |
| Hook install target | `cmd/gc/cmd_start.go` → `.opencode/plugins/gascity.js` |
| Versioned hook upgrades | `internal/hooks.opencodeHookVersion`, `opencodeHookNeedsUpgrade` |
| Skill sink | `.opencode/skills` |
| Session log reader | `internal/sessionlog/opencode_reader.go` |
| MCP projection | `internal/materialize.MCPProjection` writes `opencode.json` |
| Gateway presets | `groq` and `cerebras` both run on the OpenCode provider |

Upstream docs list it as supported in `docs/getting-started/faq.md`
("sixteen built-in harnesses, including … OpenCode"),
`docs/tutorials/01-cities-and-rigs.md`, and `docs/guides/harness-recipes.md`,
which carries a full OpenCode recipe.

The repository moved: the project was `sst/opencode`, then `anomalyco/opencode`.
`opencode-ai/opencode` is not the current home.

## Secondary finding: the `gc-*` skills were never Claude-specific

A related misconception this document invites. The seven Gas City skills
(`gc-agents`, `gc-city`, `gc-dashboard`, `gc-dispatch`, `gc-mail`, `gc-rigs`,
`gc-work`) ship from `internal/bootstrap/packs/core/skills/` as plain `SKILL.md`
files documenting `gc` CLI commands. `gc` materializes them per vendor:

```
claude   → .claude/skills
opencode → .opencode/skills
codex    → .agents/skills
gemini   → .gemini/skills
mimocode → .mimocode/skills
```

Independently, OpenCode itself scans six skill locations — including
`.claude/skills/` and `.agents/skills/`, project and global — and ignores unknown
frontmatter keys, so Claude-format skills load unchanged
(`packages/opencode/src/skill/index.ts`: `CLAUDE_EXTERNAL_DIR = ".claude"`,
`AGENTS_EXTERNAL_DIR = ".agents"`, globbed with `symlink: true`).

This also explains the 14 broken symlinks committed under
`reference-project/fired-up-pizza/.claude/skills/`. They target
`/Users/csells/.gc/cache/repos/…/skills/` and
`/Users/csells/Code/…/review-city/.gc/system/packs/core/skills/` — the gc cache and
city system-pack paths. They are **materialization output** from a previous
maintainer's machine that got committed. Generated sinks are machine-specific by
construction and will be broken for everyone else.

> [!attention] CONFLICT
> `README.md` line 49 tells students "Claude Code reads `.claude/skills`,
> OpenCode/Codex CLI/etc. read other paths." OpenCode in fact reads
> `.claude/skills` as well. The statement is not merely vague, it is incorrect for
> OpenCode specifically. Not fixed in this round — see Open items.

## Constitutional status

Article IX (Reproducible Student Path): required tool information must be accurate,
and a stale link is a dead end for a self-paced student with no instructor.
Marking a fully supported provider "compatibility not guaranteed" also fails the
Article IV honesty standard in the opposite direction from the usual case — here the
material *understates* what ships.

## Resolution taken

`installation.md` updated: OpenCode moved out of the "compatibility not guaranteed"
list into the supported set, repository URL corrected to `anomalyco/opencode`, and
a pointer added to where `provider` is set. `installation.md` is not captured by any
walkthrough snapshot, so this edit carries no Article IV snapshot obligation.

## Open items

- `README.md:49` skill-path claim is still incorrect for OpenCode (see CONFLICT above).
- The 14 broken symlinks under `reference-project/fired-up-pizza/.claude/skills/`
  are still committed and should be removed and gitignored.
