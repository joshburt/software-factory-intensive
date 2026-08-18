---
title: Content Lint Has a Broken Documented Invocation and an Undocumented Harness Prerequisite
type: discovery
tags:
  - discovery
  - test-harness
  - lint
  - githooks
  - enforcement
created: 2026-08-17
updated: 2026-08-17
status: reviewed
source: agent
---

# Content Lint Has a Broken Documented Invocation and an Undocumented Harness Prerequisite

Two separate defects in the verification ladder, both found while validating the
ADR-005 stack change. Both are pre-existing and independent of that change. Both were
verified directly this session, not inferred.

## Defect 1 — the documented bare invocation is unusable

`AGENTS.md` documents the content lint as:

```bash
python3 test-harness/lesson-pack-lint.py          # static content architecture
```

Run exactly that way on a clean tree, it reports **111 `SFI320` findings across 361
lines of output and exits 1**. `SFI320` (`check_pack_runtime_language`) matches the
regex `\b(?:lesson|workshop|student|lab|curriculum|SFI|Software Factory Intensive|L[0-9]+|C[0-9]+)\b`
and, in the bare form, applies it to the **entire repository**. The result flags files
whose whole purpose is to discuss lessons and workshops:

```text
ERROR SFI320 AGENTS.md:1
ERROR SFI320 README.md:1
ERROR SFI320 .specify/memory/constitution.md:21
ERROR SFI320 troubleshooting/beads.md:1
ERROR SFI320 .opencode/node_modules/uuid/README.md:475
ERROR SFI320 vault/index.md
```

It even flags `node_modules` and the constitution itself.

The invocation the harness actually uses is scoped, in `test-harness/behavioral-smoke.sh:14`:

```bash
test-harness/lesson-pack-lint.py --lesson L2 --lesson L3 --lesson L4 --lesson C1
```

Scoped that way the same tree reports **0 errors, 0 warnings**.

So the bare form is not a weaker version of the gate — it is a different, meaningless
check. Anyone following `AGENTS.md` sees ~111 errors, has no way to tell signal from
noise, and may reasonably conclude the tree is broken when it is clean.

**Consequence**: `AGENTS.md`'s Verification section is wrong and should show the scoped
form, or `--lesson` should default to all lessons with `--no-repo-scan` behavior when
no lesson is named.

## Defect 2 — the pre-commit gate fails on a clean checkout

`behavioral-smoke.sh` runs under `set -euo pipefail` and calls the lint as step `[1]`.
On a clean checkout the scoped lint reports:

```text
ERROR SFI100 my-factory/city.toml   city config is missing
ERROR SFI110 my-factory/pack.toml   root pack config is missing
```

Both files are **intentionally git-ignored** (`my-factory/.gitignore:6-7`) local runtime
config that the student creates during Quickstart:

```bash
cp my-factory/pack.toml.template my-factory/pack.toml
cp my-factory/city.toml.template my-factory/city.toml
```

Because step `[1]` exits 1 and `set -e` is in force, `behavioral-smoke.sh` aborts
before steps `[2]`, `[3]`, and `[4]` ever run. Verified: `SMOKE EXIT=1`, output ends at
step `[1]`.

`.githooks/pre-commit` invokes `behavioral-smoke.sh` for any staged change under
`packs/**`, `my-factory/*.template`, or `test-harness/**`. Therefore:

> **On a fresh clone, the pre-commit hook blocks every commit touching a lesson pack
> until the maintainer has run the two student Quickstart `cp` commands.**

The harness silently assumes the maintainer has completed student setup. Nothing in
`AGENTS.md`, `test-harness/README.md`, or the hook's own comments states this.

After creating both files from their templates, the same tree yields `0 errors,
0 warnings` and the full `behavioral-smoke.sh` passes end to end (`EXIT=0`, all four
steps, five lessons dry-run). The files remain git-ignored and do not enter any commit.

**Consequence**: this is a first-run trap for any new maintainer, and it makes the
lint's two structural checks (`SFI100`, `SFI110`) fire as environment errors rather
than as content defects. Either the hook should bootstrap the local config, or the
harness should skip `SFI100`/`SFI110` when the templates exist but the local copies do
not, or the prerequisite must be documented alongside `git config core.hooksPath`.

## Related observation

Initializing the `reference-project/fired-up-pizza` submodule adds **56 further
`SFI320` findings** to the bare invocation, because the submodule's markdown becomes
visible to the repo-wide scan. This does not affect the scoped gate. It does mean the
bare invocation's output volume depends on whether a submodule happens to be checked
out — further evidence that repo-wide `SFI320` is not a meaningful check.

> [!question] UNDOCUMENTED
> Whether `SFI320`'s repo-wide application is intentional (a deliberately advisory
> whole-repo sweep) or an unintended default is not recorded anywhere. The hint text
> — "keep lesson framing in tutorials; pack internals should read like a portable
> small factory" — implies it was only ever meant for `packs/**`.
