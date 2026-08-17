<!--
SYNC IMPACT REPORT — Constitution Amendment
Version change: 1.2.0 → 1.3.0 (MINOR: new governance mechanism)
Date: 2026-08-17
Rationale: DEFECT-B3 (orphaned release-gate verdict, Article XIII) cannot be fixed in
  this change — the correct fix touches shipped pack formulas and requires live
  walkthrough re-verification, which is a separate, larger effort already underway
  (the Gas City 1.4.x schema migration). Ratifying this constitution's Governance
  section without acknowledging that violation would be exactly the "silent dilution"
  Compliance already forbids. A generic escape hatch was rejected in favor of a
  narrowly-scoped, mandatory-fields, dated exception mechanism, so that any future
  exception is itself auditable rather than a loophole.
Added sections:
  - Governance → Transitional Exceptions: a bounded exception mechanism. Every entry
    must name the defect, the article violated, why it can't be fixed in the same
    change, and a concrete expiry condition (no open-ended exceptions permitted).
    Seeded with DEFECT-B3, expiring when the affected formulas branch on the verdict
    or declare it advisory-only.
Removed sections: none
Templates / docs propagated:
  - ✅ curriculum/SOFTWARE_FACTORY_MANIFEST_TEMPLATE.md — added a disclosure note under
    Human Gates: the shipped lesson packs do not implement these as automated
    stop-and-wait steps (resolves DEFECT-B1's Article XIV clause 3 requirement)
  - ✅ curriculum/labs/L4/README.md — architecture diagram corrected; no longer claims
    an "else loop back to Coder" edge that no formula implements (resolves DEFECT-B3's
    Article IV half; the Article XIII half is the Transitional Exception above)
  - ✅ test-harness/lesson-pack-lint.py — fixed a stale check (SFI112) that asserted
    rig imports belong in pack.toml; also fixed a crash on Python <3.11 (missing
    tomllib) that was silently breaking the pre-commit hook's smoke-test rung
  - ⚠ .specify/templates/plan-template.md — no change (Article XIII gate row already
    covers "every verdict has a consequence or is advisory-only"; this amendment adds
    a governance mechanism, not a new article)
Follow-up TODOs: none new; TODO(DEFECT-B3) from v1.2.0 is now tracked via the
  Transitional Exception's expiry condition instead of a bare TODO.
-->

<!--
SUPERSEDED SYNC IMPACT REPORT — v1.1.0 → 1.2.0 (retained for amendment history)
Version change: 1.1.0 → 1.2.0 (MINOR: new article + corrected workflow + expanded guidance)
Date: 2026-08-17
Rationale: two corrections and one addition. (1) The Development Workflow section stated an
  incomplete Spec Kit flow — it omitted `speckit.implement` and the `speckit.converge` loop
  entirely, and did not acknowledge the human review gates already defined in
  .specify/workflows/speckit/workflow.yml. (2) Maintainer reasoning had no durable home:
  the governance decisions and the two defects found during the v1.1.0 audit existed only
  in an HTML comment and a chat transcript. A survey of the three reference factories
  (darkharbour, anvil, oldgrowth) found all three independently converged on the same
  memory mechanics, so the convergent core was adopted and the per-repo ceremony (3-tier
  MOCs, 1500-line articles) was deliberately left out as disproportionate here.
Modified principles:
  - Development Workflow & Quality Gates: Spec Kit flow corrected to the full ordered
    pipeline `specify → clarify → plan → tasks → analyze → implement ⇄ converge`, with the
    implement/converge loop stated as a termination condition; the workflow.yml
    `review-spec` / `review-plan` human gates are now named and protected from removal.
  - Additional Constraints: the Beads bullet now states the bd-vs-vault division of labor.
Added sections:
  - Article XV — Durable Project Memory. Ported convergent core from all three reference
    factories: three record types (Decisions/Discoveries/Sessions), the
    draft→reviewed→canonical lifecycle with canonical human-only, required frontmatter
    {title,type,tags,created,updated}, controlled tag vocabulary in vault/_meta/tags.md,
    write-as-you-go with an end-of-round enrichment pass, notes ship in the PR, nothing
    invented, flag conflicts rather than resolving silently, stale worse than missing, and
    the bd/vault/constitution division of labor.
Deliberately NOT ported (disproportionate for a 9-session curriculum):
  - oldgrowth's 3-tier Maps of Content (folder/domain/concept MOCs) and its ~250-line
    vault article — this repo has no note volume to justify a MOC hierarchy.
  - A mechanical vault audit script (darkharbour's tools/vault_health, anvil's
    make vault-audit). Warranted eventually; it is code, so it is out of scope for the
    constitution workflow and is tracked as TODO(ENFORCE-XV).
Removed sections: none
Templates / docs propagated:
  - ✅ AGENTS.md — CREATED. First repo-level agent guidance; operationalizes Articles I–XV
    for agent sessions. Follows the reference-repo pattern of a terse constitution plus a
    detailed operational companion that defers to it on all normative questions.
  - ✅ vault/ — CREATED. index.md, _meta/tags.md, Decisions/, Discoveries/, Sessions/,
    seeded with the decision records and discoveries produced during this work round.
  - ✅ .specify/templates/plan-template.md — Constitution Check gate table extended from
    14 to 15 rows for Article XV
  - ⚠ .specify/templates/spec-template.md — no change (no constitution references)
  - ⚠ .specify/templates/tasks-template.md — no change (no constitution references)
  - ⚠ .specify/templates/checklist-template.md — no change (no constitution references)
  - ⚠ .opencode/commands/speckit.*.md — no change (all 10 files agent-neutral)
  - ⚠ .specify/workflows/speckit/workflow.yml — no change; it is now CITED by the
    Development Workflow section as the source of the repo's own human review gates. Note
    it implements a reduced pipeline (specify → gate → plan → gate → tasks → implement) and
    does not itself invoke clarify, analyze, or converge; those are invoked directly.
  - ⚠ README.md — no change (student-facing; the vault is maintainer infrastructure and
    per Article V MUST NOT appear in student-facing content)
Follow-up TODOs (carried forward from v1.1.0, plus one new):
  - TODO(ENFORCE-XV): add a vault audit (frontmatter fields, tag vocabulary, ISO dates,
    broken wikilinks, orphans) wired into .githooks/pre-commit, modeled on darkharbour's
    tools/vault_health/audit.py
  - TODO(ENFORCE-XI): lint check asserting each agent prompt names its authoritative
    manifest section
  - TODO(ENFORCE-XII): lesson-contract fields asserting per-step close condition and
    failure behavior
  - TODO(ENFORCE-XIII): lint check flagging a verdict-producing step whose verdict has no
    graph consequence and no advisory-only declaration
  - TODO(ENFORCE-XIV): text-consistency check flagging curriculum that teaches a human gate
    without a corresponding pack capability or an explicit omission note
  - TODO(DEFECT-B1): curriculum teaches two Human Gates that no shipped pack implements —
    see vault/Discoveries/2026-08-17-human-gates-taught-not-shipped.md
  - TODO(DEFECT-B3): L4 README promises a loop-back edge that no formula has, and the
    release-gate verdict has no consumer — see
    vault/Discoveries/2026-08-17-release-gate-verdict-has-no-consumer.md
-->
<!--
SUPERSEDED SYNC IMPACT REPORT — v1.0.0 → 1.1.0 (retained for amendment history)
Rationale: v1.0.0 derived Articles I–X exclusively from mechanically enforced
  practice (lint, hooks, harness scripts, skills). A subsequent audit of the
  workshop curriculum (W1–W4), the three curriculum/*_TEMPLATE.md manifest
  templates, and the shipped packs/lessons/C1 factory found normative doctrine
  the curriculum teaches and the packs implement that v1.0.0 left uncodified.
Modified principles:
  - Article IV — Walkthroughs Are the Source of Truth: scope expanded from
    snapshot/output fidelity to taught-capability fidelity. Core principle is
    unchanged (what the material actually produces outranks what it claims); the
    obligation now also covers taught capabilities, diagrams, and stated
    deliverables. Treated as MINOR expansion, not MAJOR redefinition.
Added sections:
  - Article XI — Manifest Authority (from SOFTWARE_FACTORY_MANIFEST_TEMPLATE.md
    Pipeline Sequence; C1 reviewer/release-gate prompts treat Review Standards and
    Release Criteria as authoritative; curriculum/labs/L4/README.md "Prove the
    manifest is load-bearing")
  - Article XII — Step Contracts and Explicit Done-Conditions (from W2 role table
    Reads/Writes/Done When; W3 step contract close condition + failure behavior;
    C1 formula artifact_path metadata; all seven C1 agent Close Behavior blocks)
  - Article XIII — Every Procedure Specifies Its Failure Path (from W1 "The
    Iteration Loop says what happens when a gate fails"; W3 "Dependency closure
    alone does not mean success"; W4 required Rollback field; C1 prompts "record
    the blocker in the step notes")
  - Article XIV — Human Decision Authority (NON-NEGOTIABLE) (from
    SOFTWARE_FACTORY_MANIFEST_TEMPLATE.md "## Human Gates"; W3 Decision
    Boundaries table assigning schema/dependency/API-contract decisions to Human
    with rationale Irreversible / Security burden / Cross-system; W1 Decision
    Checkpoint; W3 gate-doc requirements; W4 "owner for review")
Removed sections: none
Considered and deliberately NOT added:
  - "Signal-Anchored Improvement" — W4's improvement loop is human-operated by
    design (the student reads signals and edits config), and the signals it cites
    (docs/reviews/*.md, docs/releases/*.md) are real pack outputs. No taught
    claim of autonomous signal consumption exists, so there is no gap to codify.
    Article I already governs the config-edit discipline this loop depends on.
  - "Retrospective Artifact" — activities/capstone/C1/retrospective.md is a
    student-authored deliverable already governed by Article VII, and it is
    created and snapshot-verified by test-harness/walkthroughs/C1.sh.
Templates / docs propagated:
  - ✅ .specify/templates/plan-template.md — Constitution Check gate table extended
    from 10 to 14 rows for Articles XI–XIV
  - ⚠ .specify/templates/spec-template.md — no change (no constitution references)
  - ⚠ .specify/templates/tasks-template.md — no change (no constitution references)
  - ⚠ .specify/templates/checklist-template.md — no change (no constitution references)
  - ⚠ .opencode/commands/speckit.*.md — no change (all 10 files agent-neutral)
  - ⚠ README.md — no change (Config Over Prompting section consistent with Article I)
  - ⚠ curriculum/SOFTWARE_FACTORY_MANIFEST_TEMPLATE.md — no change required; its
    Pipeline Sequence and Human Gates sections are the source of Articles XI and
    XIV and are already consistent with them
Follow-up TODOs (enforcement mechanisms, tracked as separate work — code changes
  are out of scope for the constitution workflow):
  - TODO(ENFORCE-XI): add a lesson-pack-lint.py check asserting each agent prompt
    names the manifest section it treats as authoritative
  - TODO(ENFORCE-XII): add lesson-contract fields asserting per-step close
    condition and failure behavior
  - TODO(ENFORCE-XIII): add a lint check flagging a verdict-producing step whose
    verdict has no graph consequence and no advisory-only declaration
  - TODO(ENFORCE-XIV): add a text-consistency check flagging curriculum that
    teaches a human gate without a corresponding pack capability or an explicit
    omission note
  - TODO(DEFECT-B1): curriculum teaches two Human Gates that no shipped pack
    implements — resolve per Article XIV clause (c)
  - TODO(DEFECT-B3): curriculum/labs/L4/README.md line 24 promises "verdict:
    APPROVE (else loop back to Coder)" but no lesson formula has a loop-back
    edge, and the release-gate PASS/FAIL verdict has no graph consequence —
    resolve per Articles IV and XIII
-->
# Software Factory Intensive Constitution

> **Canonical source** — this is the single authoritative constitution for this
> repository. All agents, pull requests, specs, and plans MUST comply with it. Where any
> other document conflicts with this constitution, the constitution wins and the other
> document MUST be corrected.

This repository is a curriculum, not a product. It teaches participants to build a
software factory — a system of AI agents that plan, architect, design, code, review, and
release software continuously — using the Gas City framework. Every principle below
therefore serves two audiences at once: the student who must be able to follow the
material successfully, and the maintainer who must keep the material true.

## Core Principles

### Article I — Config Over Prompting (NON-NEGOTIABLE)

Agent behavior MUST be changed through configuration, not through ad-hoc corrections
typed into a chat session. When an agent produces wrong output, the fix belongs in that
agent's `agent.toml`, `prompt.template.md`, formula step, doctor check, or command
sidecar — then the work is re-run.

- Curriculum text MUST teach and model this discipline, never demonstrate a fix by
  telling the student to "just tell the agent to try again."
- Fixes to factory behavior in `packs/**` MUST land as committed config changes that a
  student can inspect, diff, and re-run deterministically.
- A behavior that exists only in a transcript and not in a file does not exist.

**Rationale:** this is the single discipline the workshop exists to transfer. It is the
bridge between individual AI use and a factory that runs unattended, and it is the one
principle whose violation invalidates the curriculum's central claim.

### Article II — Curriculum-Blind Pack Internals (NON-NEGOTIABLE)

Files inside `packs/**` MUST read like production factory definitions. No agent prompt,
formula, command, or doctor check may tell an agent that it is in a class, lab, workshop,
lesson, or exercise. The directory name MAY carry a lesson identifier for student
navigation; the contents MUST NOT.

- Agent prompts MUST be portable: liftable into a real project unchanged.
- Curriculum framing, session numbers, and pedagogical asides belong in
  `curriculum/**` and `activities/**` — never in pack internals.

**Rationale:** students graduate by carrying the pack into their own repository. Any
teaching language baked into the pack becomes dead weight or active confusion the moment
the factory leaves the classroom, and it teaches the wrong shape of a real system.

### Article III — Self-Contained Lesson Packs

Each runnable lesson MUST ship one complete factory under `packs/lessons/<lesson>/`
containing its own `agents/`, `formulas/`, `commands/`, `doctor/`, and `pack.toml`.

- Packs MUST NOT depend on a separate composition layer or an aggregate pack.
- Agents MUST be rig-scoped; routes MUST be binding-qualified.
- Every workflow formula MUST use the current formula contract; legacy pack and formula
  shapes are prohibited.
- Structure is enforced mechanically by `test-harness/migration-check.sh` and
  `test-harness/lesson-pack-lint.py`; the authoring rules in `packs/README.md` are
  binding.

**Rationale:** a student must be able to open one directory and see the entire system.
Indirection through a shared composition layer hides the very primitives — agents, packs,
rigs, formulas, routes — the workshop is trying to make legible.

### Article IV — Walkthroughs Are the Source of Truth (NON-NEGOTIABLE)

What a walkthrough actually produces outranks what a README claims. When curriculum text
and harness output disagree, the text is wrong until proven otherwise.

- Every command and every quoted output block in student-facing curriculum MUST match
  the corresponding snapshot under `test-harness/walkthrough-snapshots/<lesson>/`.
- Curriculum READMEs MUST be reconciled against snapshots whenever a walkthrough script,
  lesson pack, or README changes. The `validate-lesson-content` skill is the required
  procedure for that reconciliation.
- Snapshot claims MUST NOT be invented, extrapolated, or optimistically tidied. Output a
  student will not see MUST NOT be shown as output a student will see.
- Reconciliation MUST fix the curriculum text. Editing a snapshot or a lesson contract to
  match a stale README is prohibited; lesson contracts under
  `test-harness/lesson-contracts/` change only when the teaching architecture itself
  changes.
- **Taught capability MUST match shipped behavior.** This obligation extends beyond
  commands and output blocks to capabilities: any behavior the curriculum teaches,
  diagrams, or names as a deliverable — routing and loop-back edges, gates, verdict
  consequences, artifacts, agent abilities — the shipped pack MUST actually exhibit, or
  the curriculum MUST state plainly, in student-facing text, that it does not and why. A
  capability discrepancy is a defect of the same severity as a snapshot mismatch.
  Teaching a capability the reference factory lacks, without acknowledgement, is
  prohibited.

**Rationale:** a student following a command that does not work, or waiting for output
that never appears, loses trust in the whole factory and cannot distinguish their own
mistake from the material's. Curriculum drift is the highest-severity defect this
repository can ship. A taught capability that the reference factory silently lacks is the
same defect wearing a diagram: the student copies the exemplar, not the prose, so an
unacknowledged gap teaches the opposite of the lesson.

### Article V — No Internal Tooling Leakage

`test-harness/**`, `.githooks/**`, and the maintainer skills are private quality-assurance
tooling. They MUST NOT appear in student-facing content.

- Student-facing Markdown MUST NOT mention the test harness, walkthrough scripts,
  snapshots, snapshot directories, validation runs, test fixtures, run identifiers,
  scratch paths, or any choice made only to satisfy the harness.
- Version-branded compound nouns (for example `FormulaV2`, `PackV2`, `PacksV2`,
  `FormulasV2`) are prohibited in student-facing content. Use plain "formula" and "pack".
- Harness-only affordances MUST NOT be presented as part of the student path.

**Rationale:** the student is being taught a factory, not our regression suite. Internal
tooling references send students down paths that do not exist for them, and
version-branded names date the material and imply migrations students never lived
through.

### Article VI — Formula-Owned Orchestration

The formula graph owns work ordering. Agents execute steps; they do not schedule them.

- An agent MUST NOT create the next stage's bead, relabel work to advance a pipeline, or
  wake another agent.
- Stage labels are metadata for search and reporting — never the workflow engine.
- Label-queue polling, manual stage-labelled bead creation, legacy label schedulers, and
  workspace-scope terminology are prohibited and are enforced as banned patterns
  (`SFI001`–`SFI008`) by `test-harness/lesson-pack-lint.py`.

**Rationale:** coordination expressed as an explicit graph is inspectable, testable, and
reproducible. Coordination smuggled into prompts and labels is invisible, order-dependent,
and the exact failure mode students are here to learn to avoid.

### Article VII — Every Session Has a Named Deliverable

Each of the nine sessions MUST state exactly what the participant walks away having
produced.

- Every session MUST provide `curriculum/<type>/<ID>/README.md` and a companion
  `PROMPT.md`, and the README MUST open with a `## Deliverable` section naming the exact
  files, paths, and runtime state produced.
- Runnable lessons MUST have a lesson contract under `test-harness/lesson-contracts/`
  declaring the expected artifact shape.
- Sessions MUST NOT end in an ambiguous state where a participant cannot tell whether
  they succeeded.

**Rationale:** self-paced participants have no instructor to adjudicate completion. A
named, checkable artifact is the only honest completion signal, and it is what makes each
session independently verifiable by the harness.

### Article VIII — Layered Verification Gates

Changes MUST pass the repository's verification ladder before merge, at the depth the
change warrants.

- The scope-based hook at `.githooks/pre-commit` is the standing gate; contributors MUST
  enable it with `git config core.hooksPath .githooks`.
- The ladder, cheapest first: `test-harness/lesson-pack-lint.py` (static content
  architecture) → `test-harness/migration-check.sh` (structural invariants) →
  `test-harness/tutorial-check.sh` (dry-run command flow) →
  `test-harness/behavioral-smoke.sh` (combined, no LLM tokens) →
  `test-harness/tutorial-walkthrough.sh <lesson>` (live end-to-end, real tokens).
- Live end-to-end walkthroughs MUST be run for every affected lesson before a release
  that changes lesson packs, walkthrough scripts, or the student command path. They are
  deliberately excluded from the pre-commit hook because they require authenticated
  provider sessions.
- `--no-verify` is an exception, not a workflow. A repeatedly flaking check MUST be
  fixed, never routinely bypassed.
- Failing checks MUST NOT be deleted, weakened, or narrowed to obtain a pass.
  Pre-existing failures unrelated to a change MUST be reported explicitly rather than
  silently absorbed or attributed to the change.

**Rationale:** this repository has no hosted CI. The hook and the harness are the entire
safety net, so their authority has to be mechanical and non-negotiable or it is nothing.

### Article IX — Reproducible Student Path

The documented path MUST work on a clean machine, in the documented order, without
undocumented steps.

- Local runtime configuration MUST be created from tracked templates
  (`my-factory/pack.toml.template`, `my-factory/city.toml.template`); generated local
  state MUST NOT be committed.
- Required tool versions MUST be asserted, not assumed. The harness enforces
  `gc` ≥ 0.15.0, and `gc doctor --fix` MUST report healthy before a lesson is declared
  runnable.
- Every known failure mode a student can hit MUST have a guide under `troubleshooting/`,
  and the curriculum MUST link to it at the point of failure rather than leaving the
  student to search.
- Instructions MUST state which directory each command runs in whenever the working
  directory changes.

**Rationale:** a self-paced participant who stalls has no fallback. Unstated
prerequisites, drifting tool versions, and ambiguous working directories are the dominant
causes of a stalled run, and every one of them is preventable.

### Article X — Isolated, Reversible Harness Runs

Validation runs MUST be isolated from each other and MUST clean up after themselves.

- Live walkthrough chains MUST NOT be run concurrently; concurrent runs corrupt shared
  Dolt state and invalidate results.
- Each run MUST operate in its own scratch city and rig, and MUST own the teardown of
  what it created. Cleanup ownership is itself tested by
  `test-harness/walkthrough-cleanup-test.sh`.
- Cleanup MUST be surgical. Broadly killing `gc`, `dolt`, `tmux`, or agent processes is
  prohibited, as it destroys unrelated work on the same machine.
- A launch that reports bead creation without confirming workflow attachment MUST be
  treated as a failed launch, cleaned up, and retried — never interpreted as a pass.
- A run MUST NOT be declared successful on the basis of a snapshot directory that does
  not exist for that lesson.

**Rationale:** the harness runs real agents against real state on a developer's machine.
Runs that bleed into each other produce confidently wrong validation results, which is
worse than no validation at all.

### Article XI — Manifest Authority

The project manifest is the contract between a student's project and their agents. Where
a manifest section exists, it outranks an agent's default judgment.

- Every agent prompt MUST name the manifest section it treats as authoritative for its
  role. The taught mapping is binding: Tech Stack → Architect, Domain Model → Designer,
  Conventions → Coder/Builder, Review Standards → Reviewer, Release Criteria → Release
  Gate, and the whole manifest → Planner.
- An agent whose manifest section is present MUST structure its output against that
  section and cite the specific standard or criterion it applied. A Release Gate MUST
  render a verdict per declared criterion with evidence, not a single unattributed
  judgment.
- Fallback MUST be explicit: where the section is absent, the prompt MUST say it falls
  back to general judgment rather than silently inventing standards.
- Curriculum that instructs a student to add a manifest section MUST be accompanied by a
  demonstration that the section changes agent behavior.

**Rationale:** the manifest is what makes a factory the student's own rather than a
generic demo, and it is the highest-leverage config surface Article I points at. An agent
that ignores a declared standard makes the manifest decorative, which teaches students
that writing standards down is pointless.

### Article XII — Step Contracts and Explicit Done-Conditions

Every workflow step MUST declare a contract. Producing an artifact is not the same as
finishing a step.

- Each step MUST specify: its target, its upstream dependencies, its expected inputs, its
  expected artifact path, its close condition, and its failure behavior.
- Each role MUST specify what it reads, what it writes, and what proves it done.
- Close conditions MUST be checkable statements about the artifact, not restatements that
  the step ran. Dependency closure alone MUST NOT be treated as success.
- Handoffs MUST be explicit about what the upstream step provides, what the downstream
  step may assume, and what the downstream step MUST NOT guess.
- A step MUST NOT be able to complete in a state where neither the student nor the next
  step can tell whether it succeeded.

**Rationale:** a factory is only inspectable if each step can be judged independently.
Without a close condition, a run that produced files looks identical to a run that
produced correct files, and the student learns to accept output rather than verify it.

### Article XIII — Every Procedure Specifies Its Failure Path

Any procedure this repository teaches or ships MUST define what happens when it fails.
The failure path is where the disciplines in this constitution are actually won or lost.

- Every taught procedure MUST state the failure response concretely enough to follow:
  which file to edit, which command to run, and what to re-run. "Fix it and retry" is not
  a failure path.
- Every workflow step MUST declare its failure behavior; every improvement or config rule
  MUST declare its rollback condition.
- A step that produces a verdict MUST have a defined consequence: the graph consumes the
  verdict, or the verdict is explicitly declared advisory-only. A produced PASS/FAIL that
  nothing acts on and nothing acknowledges as advisory is prohibited.
- Failure paths MUST route through configuration per Article I — never through a
  correction typed at an agent.

**Rationale:** the moment a gate fails is precisely the moment ad-hoc prompting sneaks
back in, so an unspecified failure path silently undoes Article I. And a verdict with no
consequence is worse than no verdict: it looks like a gate, teaches that gates are
theater, and leaves the student unable to tell a blocked run from a passed one.

### Article XIV — Human Decision Authority (NON-NEGOTIABLE)

Some decisions belong to a human regardless of how capable the factory becomes. The
curriculum MUST teach this as a safety principle, not a matter of taste.

- The material MUST teach that the following are human-owned by default: irreversible
  changes (schema and data migrations), decisions that expand the trust surface (new
  dependencies), and cross-system commitments (API contract changes) — together with the
  reasoning that makes each one human-owned.
- Where the curriculum teaches a human gate, that gate MUST specify what signal it
  checks, why a human decision is required, what PASS and FAIL each mean, and how the run
  resumes after the decision. An unjustified gate is as defective as a missing one.
- Where the curriculum teaches a human gate that the shipped reference factory does not
  implement, the curriculum MUST say so plainly in student-facing text and explain why.
  Silence is prohibited. Deleting the teaching to resolve the discrepancy is prohibited —
  the doctrine in the first clause MUST remain taught.
- Every durable change to factory configuration MUST have a named human owner
  accountable for reviewing it.
- Agents MUST NOT be taught or configured to expand their own authority: no agent may
  create downstream work, relabel work to advance a pipeline, or wake another agent.

**Rationale:** this curriculum teaches students to build pipelines that write code and
create commits in their own repositories, and it is followed self-paced with no
instructor to catch a bad lesson. This constitution cannot reach a student's runtime, so
the only place it can enforce human sovereignty is in what the material teaches and in
whether the material is honest about the reference factory's limits. A curriculum that
teaches gates while shipping an exemplar without them teaches, in practice, that gates
are optional — because students copy the exemplar, not the prose.

### Article XV — Durable Project Memory

Maintainer knowledge about why this curriculum is shaped the way it is MUST outlive the
session that produced it. The vault at `vault/` is that record.

- **Three record types, written where they belong.** Curriculum-design and architectural
  decisions with stated reasons → `vault/Decisions/` as `ADR-NNN-Descriptive-Title.md`.
  Non-obvious constraints, gaps, and taught-vs-shipped conflicts → `vault/Discoveries/`.
  Work-round summaries → `vault/Sessions/` as `YYYY-MM-DD-topic.md`, append-only.
- **Write as work happens, never in batches at the end.** A decision recorded after the
  fact is a reconstruction. At the end of a work round, do an enrichment pass: add the
  session note, promote verified drafts, and confirm every decision made has a note.
- **Vault notes ship with the change.** A pull request that made a decision or hit a
  non-obvious constraint MUST include the corresponding note in the same changeset.
- **Status lifecycle.** Agent-authored notes start at `status: draft`, `source: agent`. An
  agent MAY self-promote to `reviewed` after verifying the note's claims in that same
  session. An agent MUST NEVER set `canonical` — that is a human-only action.
- **Required frontmatter.** Every note MUST carry `title`, `type`, `tags`, `created`, and
  `updated`, with ISO dates and `updated` bumped on every edit. Tags MUST come from
  `vault/_meta/tags.md`; introducing a new tag requires updating that file first.
- **Nothing is invented.** Every claim MUST trace to a source — a file, a command output, a
  commit, or a decision made in the recorded session. Genuine gaps are marked
  `> [!question] UNDOCUMENTED`.
- **Flag conflicts; do not resolve them silently.** Where sources disagree, record
  `> [!attention] CONFLICT` describing both sides.
- **A stale note is worse than a missing one.** A note that can no longer be verified MUST
  be marked `> [!warning] STALE` rather than left standing as if current.
- **Division of labor.** Work items and status live in Beads (`bd`) — never in markdown
  TODO lists. Reasoning, constraints, and history live in the vault. Governance rules live
  in this constitution. No loose `MEMORY.md` files.
- **The vault is maintainer infrastructure.** It is not student-facing curriculum, and
  Article V applies to it: no vault path may appear in student-facing content.

**Rationale:** this repository's decisions are unusually easy to lose. Commit messages are
terse, the reasoning behind a curriculum choice rarely survives in the diff, and a
taught-vs-shipped defect found by cross-checking is invisible to the next maintainer unless
it is written down. Every reference factory in this ecosystem independently converged on the
same three record types and the same draft/reviewed/canonical lifecycle; adopting that
convergent core costs little and stops decisions from being re-litigated and gotchas from
being re-discovered.

## Additional Constraints

- **Secrets never touch git.** Credential material is denied by default in `.gitignore`
  (`*.pem`, `*.p12`, `*.pfx`, `*.key`, `*_rsa`, `*_ed25519`, `*.private-key*`, `id_rsa*`,
  `*.agekey`, `*.age.key`). Tracking any such file requires an explicit, justified
  negation entry. Secrets MUST NOT appear in curriculum text, snapshots, or transcripts.
- **Local state stays local.** Per-checkout Beads/Dolt state (`/.beads/`, except its
  `README.md`) and generated `my-factory/` runtime configuration are not git-tracked.
- **Durable work is tracked in Beads; durable reasoning is tracked in the vault.** Work
  items and status belong in `bd`, not in ad-hoc markdown TODO lists. Decisions,
  constraints, and session history belong in `vault/` per Article XV. Neither belongs in a
  loose `MEMORY.md`.
- **Snapshots are evidence.** Files under `test-harness/walkthrough-snapshots/**` are
  harvested output, not hand-authored prose. They MUST be regenerated by a run, never
  edited to produce a desired result.
- **Student artifacts are examples, not dependencies.** Content under
  `reference-project/` illustrates completed deliverables and MUST NOT become a runtime
  dependency of any lesson pack.
- **Naming conventions are binding.** Session identifiers (`W1`–`W4`, `L1`–`L4`, `C1`),
  the `curriculum/<type>/<ID>/` layout, the `activities/<type>/<ID>/` layout, and the
  `packs/lessons/<lesson>/` layout MUST be preserved; cross-references MUST be updated in
  the same change that moves a file.

## Development Workflow & Quality Gates

- **Spec Kit flow** for non-trivial features, in order:
  `speckit.specify` → `speckit.clarify` → `speckit.plan` → `speckit.tasks` →
  `speckit.analyze` → `speckit.implement` ⇄ `speckit.converge`.
  `speckit.implement` and `speckit.converge` form a loop: `converge` assesses the codebase
  against the spec, plan, and tasks and appends remaining unbuilt work to `tasks.md` so
  `implement` can finish it. The loop MUST run until `converge` finds no remaining work —
  a feature is not done while `converge` still appends tasks.
- **Plans MUST include a Constitution Check** that gates Phase 0 and is re-checked after
  design. Accepted violations MUST be recorded in the plan's Complexity Tracking table.
- **The `speckit.specify` and `speckit.plan` review gates are human gates.** The bundled
  workflow at `.specify/workflows/speckit/workflow.yml` defines `review-spec` and
  `review-plan` gate steps with `on_reject: abort`. These MUST NOT be removed or
  auto-approved; they are the Article XIV human-authority checkpoints of this repository's
  own development process.
- **Pre-commit scope map** (`.githooks/pre-commit`): pack and hook changes trigger
  structural and behavioral checks; student command-path and harness changes additionally
  trigger the dry-run command flow; curriculum-only Markdown changes skip the mechanical
  checks and are instead governed by Article IV reconciliation.
- **Curriculum changes** MUST be accompanied by snapshot reconciliation per Article IV
  whenever they touch a command, an output block, or a stated deliverable.
- **Lesson additions** MUST follow the procedure in `test-harness/README.md` and ship a
  lesson contract, a walkthrough script, and snapshots.
- **Commits and pushes** occur only when explicitly requested. Constitution amendments
  MUST be committed separately using the message format
  `docs: amend constitution to vX.Y.Z (description)`.

## Governance

### Compliance

- This constitution supersedes ad-hoc practice for all work in this repository. Agent
  guidance files and skills operationalize it; where they conflict with it, the
  constitution wins and the guidance file MUST be updated.
- Every `plan.md` MUST include a Constitution Check verifying compliance with these
  articles. Intentionally accepted violations MUST be recorded with rationale in the
  plan's Complexity Tracking table.
- Undocumented violations are blockers. Work MUST NOT proceed past a phase with an
  undocumented constitutional violation.
- `/speckit.analyze` treats constitution conflicts as CRITICAL.

### Amendment Process

Amendments are proposed via a pull request that touches this file and MUST include:

1. Explicit rationale for the change.
2. A Sync Impact Report at the top of this file.
3. A semantic version bump: **MAJOR** for principle removal or redefinition; **MINOR**
   for a new article or materially expanded guidance; **PATCH** for clarification and
   wording that does not change intent.
4. Propagation to dependent templates, commands, and guidance docs, with each one marked
   updated or explicitly marked as requiring no change.
5. Human approval. Constitutional amendments are human-only.

Agents MUST NOT weaken, dilute, or bypass a principle in order to make work pass.

### Transitional Exceptions

An exception recorded here is not a general escape hatch. It MUST name a specific
defect, the article it violates, why the defect cannot be fixed in the same change
that ratifies or amends this constitution, and a concrete condition under which it
expires. An exception with no expiry condition is not permitted. Deleting the
teaching that exposes a defect is never an acceptable resolution (Article XIV).

- **DEFECT-B3 — orphaned release-gate verdict (Article XIII).** The `release-gate`
  step in `packs/lessons/L4` and `packs/lessons/C1` renders a PASS/FAIL verdict that
  the formula graph does not act on; the run's outcome is the same either way. Article
  XIII requires a verdict-producing step to have a defined graph consequence or be
  declared advisory-only. Fixing this correctly means changing a shipped pack's
  formula and re-verifying it against a live walkthrough, which is out of scope for a
  constitution amendment. Recorded here rather than silently ratified over.
  **Expires** when `packs/lessons/L4/formulas/mol-delivery-review.toml` and
  `packs/lessons/C1/formulas/mol-release-delivery.toml` either branch on the verdict
  or declare it advisory-only in the pack, whichever comes first — expected within
  this repository's current Gas City 1.4.x schema migration. See
  `vault/Discoveries/2026-08-17-release-gate-verdict-has-no-consumer.md`.

**Version**: 1.3.0 | **Ratified**: 2026-08-17 | **Last Amended**: 2026-08-17
