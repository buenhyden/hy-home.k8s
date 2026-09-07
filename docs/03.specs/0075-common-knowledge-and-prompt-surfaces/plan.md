---
title: "Common Knowledge and Prompt Surfaces Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "active"
owner: "platform"
updated: "2026-09-07"
layer: "specs"
artifact_id: "SPEC-0075-PLAN-0001"
---

# Common Knowledge and Prompt Surfaces Implementation Plan

## Global Constraints

- One work package is one logical commit. Rollback is `git revert` of that
  commit; no history rewrite, force update, branch deletion, or worktree
  removal is authorized.
- A behavior change demonstrates its failing case before its fix and shows the
  passing result after it.
- The staged profile gates each logical commit; the full profile gates handoff.
  Neither is repeated on unchanged bytes and `--no-verify` is never used.
- Repository-static results never report as native discovery, native
  enforcement, hosted CI, or live behavior.
- Push, pull-request creation, merge, and hosted execution are not authorized
  by this plan and are not implied by any passing check in it.
- The recorded pre-change baseline is twenty-one gates passing under
  `python3 scripts/qa.py full`.
- A folder-level add, move, or removal updates the owning `README.md` in the
  same change.
- No new document schema or registry is created; the Stage 99 registry is
  extended and existing profiles are reused where they already fit.
- No entry point makes a paid model call mandatory, and no commit-time hook
  gains a network dependency.
- Configuration under the user's home directory, including the global hook
  path, is not modified.

## Overview

This plan executes [SPEC-0075](spec.md). Its first work package is a successor
architecture decision, because ADR-0035 currently decides that optional prompt
directories are not created and adding one while that clause stands would leave
two contradictory contracts in the tree. The remaining packages create the two
surfaces with their consumers and validation, add the document profiles they
need, and settle the adjacent inaccuracies the same review unit touches.

## Context

`.agents/README.md` records optional memory, rule, prompt, and script
directories as unadopted and states that the MIG-0009 memory retirement remains
effective. ADR-0035, status accepted, decides that optional memory, rules,
prompts, evaluations, and scripts folders are not created.
`.agents/governance/context-and-memory.md` states that no governance memory
directory remains and routes durable knowledge to the responsible policy,
skill, operating document, or reference owner. A generated knowledge index was
retired on 2026-08-31 as a duplicate navigation control plane.

The governance validator's retired-surface list contains `.agents/memory`,
`.agents/rules`, `.agents/agents`, `.agents/hooks`, `.agents/providers`, and
`.codex/skills`, but not a knowledge or prompt path, so neither adoption is
blocked by that check. The list already carries a precedent for revision: the
Codex hook surface left it once the installed client shipped one.

The Stage 99 registry holds sixty-nine profiles matched by anchored path
expression. None matches a knowledge index, a prompt contract, or an evaluation
rubric. The collection-index profile already describes routers of the kind the
two surface READMEs are.

Seven documents under `.agents/roles/` carry no registry entry. Their consumers
are the responsibility router and a Stage 90 index that maps each to
requirement identifiers and repository path scopes.

`docs/90.references/research/README.md` states that current report filenames use
no numeric order prefix while the registry mandates an `m####-` identity prefix
for those same files; it carries the same navigation link twice; and the pack
uses a retired stage label. `m0001` records a dated four-provider,
forty-eight-adapter observation; the registry now reports two providers, twelve
roles, and thirty-six projections. `m0009` pins the upstream comparison at
`ebe9c99a`; the upstream head is `1454492577d1af4884722837f491fef14b501e21`,
authored 2026-09-05, MIT licensed, organized as division directories of persona
prompt files.

This workspace does not use VS Code, so `.vscode/` and the two validation
routes naming it are removed rather than filled. On this workstation the
global `core.hooksPath`
points outside the repository, so the repository's commit-time hooks are inert
and the conventional-commit check does not run at commit time. Because of that,
the commit hook suite's execution inside the full profile is the only place it
runs and is retained rather than treated as duplication.

## Goals & In-Scope

- A narrow successor decision that revises only the unadopted-directory clause.
- A knowledge surface of hand-maintained pointers with a non-duplication rule
  and validation, plus named consumers.
- A prompt surface of input and output contracts with a deterministic builder
  that makes no model call, plus command entry points.
- Two document profiles with templates, and reuse of the collection-index
  profile for the two surface READMEs.
- Consolidation of the seven responsibility documents with consumer succession.
- Reference pack corrections and a dated upstream re-observation.
- One execution owner per duplicated rule, with retained duplicates justified.
- A recorded commit-tooling limitation with a user-run remediation.

## Non-Goals & Out-of-Scope

- No `.agents/evaluations/`, `.agents/rules/`, or `.agents/scripts/` directory.
- No revival of the retired progress ledger and no second progress ledger.
- No separate orchestrator, state machine, or loop runtime.
- No role adopted from the upstream persona catalog.
- No hosted continuous integration workflow for automated review while no
  credential exists to run it.
- No editor integration and nothing under `.vscode/`.
- No change to guard ownership, patch parsing, or permission scope; SPEC-0074
  owns those.
- No change to `gitops/`, `infrastructure/`, `traefik/`, `policy/`, or
  `examples/` behavior.

## Work Breakdown

| ID     | Work package                                                                                                     | Depends on             | Entry gate                        | Exit evidence                                                                              |
| ------ | ---------------------------------------------------------------------------------------------------------------- | ---------------------- | --------------------------------- | ------------------------------------------------------------------------------------------ |
| WP-001 | Author the successor decision revising only the unadopted-directory clause and mark ADR-0035 superseded            | None                   | VAL-CKP-002 approved              | Both decision bodies intact with a reciprocal successor row; lifecycle and link validation   |
| WP-002 | Amend the governance README and the context-and-memory routing sentence so no file states the superseded position  | WP-001                 | VAL-CKP-002 approved              | Repository search for the superseded wording returns no active file                          |
| WP-003 | Add the knowledge and prompt profiles with templates and extend the collection-index path expression               | WP-002                 | VAL-CKP-003 approved              | Document contract registry reports no uncovered and no ambiguous path                        |
| WP-004 | Create the knowledge surface and register it in the validation-surface contract                                    | WP-003                 | VAL-CKP-001 approved              | Affected-surface contract with no uncovered path; profile validation                         |
| WP-005 | Add the knowledge owner-path and non-duplication validator                                                         | WP-004                 | VAL-CKP-004 approved              | Failing validator cases before, passing after                                                |
| WP-006 | Wire the knowledge consumers at the navigation skill and the work-lifecycle intake step                            | WP-005                 | VAL-CKP-001 approved              | Named consumer reads with stated inputs; governance validator                                |
| WP-007 | Create the prompt surface with its four contracts                                                                  | WP-003                 | VAL-CKP-001 approved              | Profile validation; each contract names inputs, outputs, and refusal conditions               |
| WP-008 | Implement the deterministic prompt input builder                                                                   | WP-007                 | VAL-CKP-005 approved              | Failing builder tests before, passing after; no network and no repository write               |
| WP-009 | Add the command entry points and retire the VS Code surface                                                        | WP-008                 | VAL-CKP-001 approved              | Affected-surface contract with no uncovered path; no route left naming a removed file         |
| WP-010 | Consolidate the seven responsibility documents into the router and carry every consumer to a section anchor        | WP-006                 | VAL-CKP-006, VAL-CKP-010 approved | Link and owner validation; no dangling link; retained documents recorded with reasons          |
| WP-011 | Correct the reference pack wording, the duplicate link, and the retired stage label, and add the current observation | WP-010                 | VAL-CKP-007 approved              | Reviewed pack text; past observations unchanged in wording, subject, and date                  |
| WP-012 | Record the dated upstream re-observation and the zero-adoption conclusion                                          | WP-011                 | VAL-CKP-008 approved              | Registry role count unchanged; upstream head, licence, and observation date recorded            |
| WP-013 | Give the container-manifest linter one execution owner and record why each retained duplicate is retained          | WP-012                 | VAL-CKP-009 approved              | Before-and-after full profile comparison; no rule lost and no required-tool failure skipped     |
| WP-014 | Record the commit-tooling limitation with a user-run remediation                                                   | WP-013                 | VAL-CKP-011 approved              | Task evidence review; no limitation reported as a working control                              |

### WP-001: Author the successor decision

**Files:** Create
`docs/02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md`.
Modify `docs/02.architecture/decisions/0035-common-agents-authority-and-native-skill-routing.md`,
`docs/02.architecture/decisions/README.md`.

**Interfaces.** Produces ADR-0036 with `supersedes: "ADR-0035"`, and ADR-0035
with `status: "superseded"` and `superseded_by: "ADR-0036"`. Consumes nothing
from earlier packages.

- [ ] Copy ADR-0035's authority-location, skill-routing, gateway,
      preservation, and validation clauses into ADR-0036 unchanged, restating
      them rather than referring to them, so ADR-0036 stands alone.
- [ ] Revise only the unadopted-directory clause: adopt a knowledge surface and
      a prompt surface; keep evaluation, rule, and script directories unadopted
      and record the reason for each.
- [ ] Record why the adopted knowledge surface is not the retired generated
      index: it is hand-maintained pointer material bound by a non-duplication
      rule that WP-005 enforces.
- [ ] Record the considered alternatives and why each was rejected: absorbing
      the material into existing documents, which leaves the prompt input and
      output contracts without an owner; and adopting every optional directory,
      which duplicates an evaluation harness that already owns its runner,
      cases, and validation surface and creates two directories with no
      consumer.
- [ ] Set ADR-0035 to superseded with the reciprocal successor row, leaving its
      body intact.
- [ ] Add both rows to the decisions README index.
- [ ] Run `python3 scripts/validate-document-lifecycle.py --root . --mode strict`
      through `python3 scripts/qa.py staged`. Expected: PASS.
- [ ] Commit.

### WP-002: Align the policy text

**Files:** Modify `.agents/README.md`,
`.agents/governance/context-and-memory.md`.

- [ ] Replace the sentence stating that optional memory, rule, prompt, and
      script directories are not adopted with the position ADR-0036 records,
      keeping the memory retirement effective.
- [ ] Add the two surfaces to the governance README structure table with their
      responsibilities.
- [ ] Amend the context-and-memory routing sentence so it names the knowledge
      surface as a map to owners while keeping the rule that durable knowledge
      stays with its domain owner and that no duplicate current-state ledger is
      created.
- [ ] Run `grep -rn "are not adopted" .agents/ docs/02.architecture/` and
      confirm no active file states the superseded position.
- [ ] Run `python3 scripts/qa.py staged` and commit.

### WP-003: Add the document profiles

**Files:** Modify `docs/99.templates/registry.json`,
`docs/99.templates/README.md`, `docs/99.templates/templates/README.md`. Create
one template per new profile under `docs/99.templates/templates/governance/`.

**Interfaces.** Produces two profiles with anchored path expressions, one
covering `.agents/knowledge/` documents other than its README, one covering
`.agents/prompts/` contracts other than its README; and an extension of the
collection-index path expression by the two README paths. Each new profile
names a template source, and each new physical template form gets its
accompanying meta-profile.

- [ ] Add the knowledge-document profile with its required frontmatter set,
      required section list, fixed type constant, status domain, and template
      source.
- [ ] Add the prompt-contract profile the same way, with sections covering
      purpose, inputs, output, validation, and refusal conditions.
- [ ] Extend the collection-index path expression by the two README paths.
- [ ] Add the two template forms and their meta-profiles, and index them in the
      template catalog README.
- [ ] Run `python3 scripts/validate-document-contract-registry.py --root . --mode strict`
      through `python3 scripts/qa.py staged`. Expected: no uncovered and no
      ambiguous path.
- [ ] Commit.

### WP-004: Create the knowledge surface

**Files:** Create `.agents/knowledge/README.md`,
`.agents/knowledge/project-map.md`, `.agents/knowledge/domains.md`. Modify
`.agents/README.md`, `scripts/validation/registry.json`.

**Interfaces.** Produces a knowledge row shape of owner path, entry path, and
validity condition, consumed by WP-005's validator and WP-006's consumers.

- [ ] Write the README stating the surface contract: pointers only, no policy
      text, no generated content, and what belongs at its owner instead.
- [ ] Write the project map naming which top-level tree owns what and the entry
      document for each.
- [ ] Write the domain index with one row per domain: Kubernetes and GitOps
      desired state, networking and ingress, Vault and External Secrets,
      observability, and documents and validation. Each row carries the
      canonical owner, the entry path, and the validity condition.
- [ ] Add the surface to the governance README structure table.
- [ ] Register the surface in the validation-surface contract so its paths route
      to the validators that judge them.
- [ ] Run `python3 scripts/validate-affected-surfaces.py --root .` through
      `python3 scripts/qa.py staged`. Expected: no uncovered path.
- [ ] Commit.

### WP-005: Add the knowledge validator

**Files:** Create the validator under `scripts/`. Modify
`scripts/validation/registry.json`. Test under `tests/`.

**Interfaces.** Produces a validator that fails when a knowledge row names an
owner or entry path that does not exist, and when a knowledge document
reproduces a span of policy text from an owner it points at. Consumes the row
shape from WP-004.

- [ ] Write the failing tests: a row naming a missing owner path; a row naming
      a missing entry path; a document reproducing a policy span from an owner
      it points at; and a valid document that must pass.
- [ ] Run `python3 -m unittest` on the new module. Expected: FAIL, because the
      validator does not exist.
- [ ] Implement the validator with bounded reads and deterministic output.
- [ ] Run the tests. Expected: PASS.
- [ ] Register the gate in the validation registry on the lanes its paths reach.
- [ ] Run `python3 scripts/qa.py staged` and commit.

### WP-006: Wire the knowledge consumers

**Files:** Modify `.agents/skills/knowledge-map/SKILL.md`,
`.agents/workflows/work-lifecycle.md`.

- [ ] Name the knowledge surface as an input to the navigation skill, stating
      what the skill reads from it and what it returns.
- [ ] Name the surface at the work-lifecycle intake step that selects owning
      documents, stating when it is read.
- [ ] Confirm each consumer states a read point and its inputs, so no surface
      is delivered whose only reader is its own README.
- [ ] Run `python3 scripts/validate-agent-governance.py --root .` through
      `python3 scripts/qa.py staged` and commit.

### WP-007: Create the prompt surface

**Files:** Create `.agents/prompts/README.md`,
`.agents/prompts/handoff.md`, `.agents/prompts/change-review.md`,
`.agents/prompts/commit-message.md`, `.agents/prompts/doc-update.md`. Modify
`.agents/README.md`.

**Interfaces.** Produces four contracts, each stating an identifier, a purpose,
an input list with the command producing each input, an output shape, a
validation rule, and refusal conditions. Consumed by WP-008's builder, which
reads the input list to know what to collect.

- [ ] Write the handoff contract, reusing the handoff fields the quality policy
      already owns rather than redefining them.
- [ ] Write the change-review contract over a local difference.
- [ ] Write the commit-message contract accepting the staged difference only,
      with refusal conditions covering an empty staged difference and a message
      the user has already written.
- [ ] Write the documentation-update contract that locates the canonical owner
      for a change and proposes a difference against it.
- [ ] Add the surface to the governance README structure table.
- [ ] Run `python3 scripts/qa.py staged` and commit.

### WP-008: Implement the prompt input builder

**Files:** Create `scripts/prompt-input.py`. Test under `tests/`.

**Interfaces.** Produces a command-line interface taking a contract identifier
and writing the assembled request to standard output, exiting non-zero with a
diagnostic when a declared input cannot be produced. Consumes the contract
files from WP-007.

- [ ] Write the failing tests: an unknown identifier exits non-zero with a
      diagnostic; the commit-message identifier with an empty staged difference
      exits non-zero and emits no draft; the commit-message identifier reads the
      staged difference and not the working tree; no invocation writes to the
      repository or changes Git state; and no invocation opens a network
      connection.
- [ ] Run `python3 -m unittest` on the new module. Expected: FAIL.
- [ ] Implement the builder. It resolves the contract, runs only the commands
      the contract declares, and writes the assembled request to standard
      output. It makes no model call.
- [ ] Run the tests. Expected: PASS.
- [ ] Run `python3 scripts/qa.py staged` and commit.

### WP-009: Add the entry points

**Files:** Create `.claude/commands/` entries, one per contract.

- [ ] Confirm none of the four contract identifiers collides with an existing
      skill identifier before creating a command entry.
- [ ] Add one command entry per contract, each invoking the builder with its
      identifier.
- [ ] Confirm the affected-surface contract reports no uncovered path and no
      route naming a file this workspace no longer carries.
- [ ] Run `python3 scripts/qa.py staged` and commit.

### WP-010: Consolidate the responsibility documents

**Files:** Modify `.agents/roles/README.md`,
`docs/90.references/research/0001-workspace-engineering/m0013-scope-application-index.md`.
Remove the seven category documents under `.agents/roles/`.

- [ ] Absorb each category document's domain boundary statement into a section
      of the responsibility router, keeping the concrete role bodies unchanged.
- [ ] Repoint every consumer reference at a section anchor in the same change,
      including the Stage 90 index rows that map each category to requirement
      identifiers and path scopes.
- [ ] Repair the responsibility router's reference to a root `DESIGN.md`,
      which names no file in the tree. Either point it at the owner that holds
      the guidance or remove the clause; the reference escapes link validation
      today because it is inline code rather than a link.
- [ ] Run `python3 scripts/validate-links-and-owners.py --root . --mode strict`
      through `python3 scripts/qa.py staged`. Expected: no dangling link.
- [ ] If a consumer cannot be served by a section anchor, retain that category
      document and record the reason rather than breaking the link.
- [ ] Commit.

### WP-011: Correct the reference pack

**Files:** Modify `docs/90.references/research/README.md`,
`docs/90.references/research/0001-workspace-engineering/m0001-workspace-governance-and-common-agent-environment.md`.

- [ ] Reword the filename guidance so the registry-mandated identity prefix is
      explicitly outside the prohibition on ordering prefixes.
- [ ] Remove the duplicated navigation link.
- [ ] Replace the retired stage label where the sentence describes the present;
      leave it where the sentence describes a dated past observation.
- [ ] Add a current dated observation of the two-provider, twelve-role,
      thirty-six-projection registry beside the four-provider observation,
      changing neither the wording, the subject, nor the date of the original.
- [ ] Add the three-way comparison the pack currently lacks: per capability,
      what the installed client documents, what the repository implements
      statically, and what runtime evidence exists. Every runtime column entry
      is an observation or an explicit absence, never an inference from the
      static column.
- [ ] Run `python3 scripts/qa.py staged` and commit.

### WP-012: Record the upstream re-observation

**Files:** Modify
`docs/90.references/research/0001-workspace-engineering/m0009-ai-agents-and-agency-agents.md`,
`docs/90.references/research/0001-workspace-engineering/m0012-source-coverage.md`.

- [ ] Add a new dated observation recording the upstream head identity, its
      authored date, its MIT licence, and its division-directory organization,
      leaving the retained comparison pin's wording and date unchanged.
- [ ] Record the conclusion: the catalog is persona prompt material, the
      existing twelve-role roster has no concrete gap it fills for this
      workspace, and no role is adopted.
- [ ] Confirm the registry role count is unchanged.
- [ ] Run `python3 scripts/qa.py staged` and commit.

### WP-013: Give each duplicated rule one execution owner

**Files:** Modify `.pre-commit-config.yaml`,
`docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md`.

- [ ] Prove that the validation script's file scope covers the commit hook's
      scope before removing anything. If it does not, stop and record why.
- [ ] Remove the duplicate container-manifest linter hook entry, leaving the
      script as its single execution owner.
- [ ] Record why the action-pinning pair is retained: the repository validator
      guards against the third-party rule being disabled, so the pair is a
      deliberate interlock.
- [ ] Record why the commit hook suite inside the full profile is retained: the
      global hook path override makes the commit-time run inert here, so the
      profile run is the only execution.
- [ ] Run `python3 scripts/qa.py full` and compare gate results with the
      recorded baseline. Expected: no rule lost and no required-tool failure
      converted to a skip.
- [ ] Commit.

### WP-014: Record the tooling limitations

**Files:** Modify the package Task and
`docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md`.

- [ ] Record the global hook path override, its consequence that the
      conventional-commit check and the commit hook suite do not run at commit
      time on this workstation, and a repository-local remediation the user
      runs themselves.
- [ ] Record the model, cost, and throughput conclusion: the registry's
      capability-to-model binding is owned by SPEC-0073, was re-checked against
      the observed client identities during this package, and needs no change;
      concurrency, retry, and escalation limits stay with the loop conditions
      the work lifecycle already owns; and no hard cost ceiling is enforceable
      locally, so any budget statement is recorded as a soft budget.
- [ ] Confirm no limitation is reported as a working control.
- [ ] Run `python3 scripts/qa.py staged` and commit.

## Verification Plan

Each work package runs its focused checks during implementation, then the
staged profile against its exact index snapshot before its commit. The full
profile runs at WP-013 for the gate comparison and once more on the final
working tree before handoff.

A behavior change runs its failing case first and records the failure, then
runs the same case after the fix and records the pass. A document-only package
runs the profile, link, and lifecycle validators that its paths route to.

Invoking a document validator directly rather than through `scripts/qa.py`
compares against the Git index and is not a substitute for the lane the entry
point selects; the direct invocation is not used as evidence.

No command in this plan establishes native discovery of a surface or loading of
a contract.

## Risks & Mitigations

A new surface could end up with no real reader. The consumer wiring package
requires each consumer to state a read point and its inputs, and the plan
states that a surface whose only reader is its own README is not delivered.

The knowledge surface could drift back into a second authority. The
non-duplication validator fails a document that reproduces a policy span from an
owner it points at, and the surface is hand-maintained so no generation step can
reintroduce the retired navigation plane.

Consolidating the responsibility documents could break a Stage 90 consumer. The
package repoints every consumer in the same change and retains any document a
section anchor cannot serve, with the reason recorded.

Correcting research prose could overwrite a past observation. The plan permits
only rewording present-tense claims and adding new dated observations, and the
criterion checks that wording, subject, and date of past observations are
unchanged.

Removing a duplicate hook could drop coverage. The package proves scope
coverage before removal and compares full profile results before and after.

The successor decision could be declined. In that case no directory is created;
the remaining hygiene packages are independent of the surfaces and can proceed
alone.

## Completion Criteria

Every criterion from VAL-CKP-001 through VAL-CKP-011 has its named evidence.
Each new surface has a named consumer that reads it. The full profile matches
the recorded baseline. Each work package is one revertible commit. Every
deferred item names its blocker and next owner, and no limitation is reported
as a working control.

## Traceability

[SPEC-0075](spec.md) owns the change contract and the criteria. The package
Task owns execution results, per-lane evidence, and the limits that remain
unobserved.

### Lifecycle Traceability

| Spec criterion                                             | Work package           | Expected Task                                                          |
| ---------------------------------------------------------- | ---------------------- | ---------------------------------------------------------------------- |
| [VAL-CKP-001](spec.md#success-criteria--verification-plan) | WP-004, WP-006, WP-007, WP-009 | [tsk-0001](tasks/tsk-0001-adopt-common-knowledge-and-prompt-surfaces.md) |
| [VAL-CKP-002](spec.md#success-criteria--verification-plan) | WP-001, WP-002         | [tsk-0001](tasks/tsk-0001-adopt-common-knowledge-and-prompt-surfaces.md) |
| [VAL-CKP-003](spec.md#success-criteria--verification-plan) | WP-003                 | [tsk-0001](tasks/tsk-0001-adopt-common-knowledge-and-prompt-surfaces.md) |
| [VAL-CKP-004](spec.md#success-criteria--verification-plan) | WP-005                 | [tsk-0001](tasks/tsk-0001-adopt-common-knowledge-and-prompt-surfaces.md) |
| [VAL-CKP-005](spec.md#success-criteria--verification-plan) | WP-008                 | [tsk-0001](tasks/tsk-0001-adopt-common-knowledge-and-prompt-surfaces.md) |
| [VAL-CKP-006](spec.md#success-criteria--verification-plan) | WP-010                 | [tsk-0001](tasks/tsk-0001-adopt-common-knowledge-and-prompt-surfaces.md) |
| [VAL-CKP-007](spec.md#success-criteria--verification-plan) | WP-011                 | [tsk-0001](tasks/tsk-0001-adopt-common-knowledge-and-prompt-surfaces.md) |
| [VAL-CKP-008](spec.md#success-criteria--verification-plan) | WP-012                 | [tsk-0001](tasks/tsk-0001-adopt-common-knowledge-and-prompt-surfaces.md) |
| [VAL-CKP-009](spec.md#success-criteria--verification-plan) | WP-013                 | [tsk-0001](tasks/tsk-0001-adopt-common-knowledge-and-prompt-surfaces.md) |
| [VAL-CKP-010](spec.md#success-criteria--verification-plan) | WP-010                 | [tsk-0001](tasks/tsk-0001-adopt-common-knowledge-and-prompt-surfaces.md) |
| [VAL-CKP-011](spec.md#success-criteria--verification-plan) | WP-009, WP-014         | [tsk-0001](tasks/tsk-0001-adopt-common-knowledge-and-prompt-surfaces.md) |
