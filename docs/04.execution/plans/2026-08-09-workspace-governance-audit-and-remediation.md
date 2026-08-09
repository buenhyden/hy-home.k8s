---
title: 'Workspace Governance Audit and Remediation Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-08-09
---

# Workspace Governance Audit and Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILLS: Use
> `superpowers:subagent-driven-development` for each bounded WGIA work package,
> `superpowers:executing-plans` to follow this order and its checkpoints, and
> `superpowers:finishing-a-development-branch` only after WGIA-014 closes.
> Every implementation worker receives the full work-package text and is
> followed by a specification-compliance review and a quality review before the
> next dependent package begins.

**Goal:** Publish the exact ten-file `2026-08-09-wgia` audit pack as the sole
Current workspace-governance audit, correct proof-complete conflicts in their
canonical owners, migrate every mutable consumer, and remove only artifacts
that pass the approved deletion contract.

**Architecture:** The implementation uses a fail-closed evidence pipeline:
freeze the observation commit, establish the report schemas and exact 30-scope
ownership, audit the current canonical owners, build an integrated disposition
and remediation ledger, apply bounded owner-family corrections, then switch
the audit Current pointer and its RIA projections atomically. Historical audit
packs and Stage 98 remain immutable; deeper evidence lanes remain `DEFER`.

**Tech Stack:** Git tracked-object plumbing, Markdown Stage 90 audit profiles,
JSON Schema and closed JSON contracts, Python 3 standard-library validators and
unittest fixtures, shell validation entrypoints, GitHub Actions YAML, the
existing RIA producer, document-profile registry, LLM-WIKI generator, agent
harness validators, pre-commit when available, and logical Git commits.

### Global Constraints

- The approved specification is
  [Spec 054](../../03.specs/054-workspace-governance-audit-and-remediation/spec.md).
- The output root is exactly
  `docs/90.references/audits/2026-08-09-wgia/` and contains exactly the ten
  filenames declared by Spec 054.
- The pack README owns exactly 30 sequential `REQ-WGA-001` through
  `REQ-WGA-030` rows, with one primary report heading per row.
- Stage 90 is descriptive evidence. Active rules remain in their canonical
  root, Stage 00, Stage 01-05, Stage 90 data, Stage 99, `.github`, `scripts`,
  `tests`, or provider-adapter owners.
- Existing audit-pack bodies remain source-commit-bounded historical evidence;
  they are not rewritten or deleted because a newer audit exists.
- `docs/98.archive/**` is immutable. Every task checks that the branch has no
  Stage 98 diff.
- Evidence depths are closed to `repository-static`, `hosted`,
  `provider-runtime`, and `live`; unavailable or unauthorized deeper evidence
  remains `DEFER`.
- Validation and Verification are separate results. A schema-valid artifact
  does not prove that it meets the approved requirements.
- A deletion needs an exact tracked path and source commit, zero current
  consumers, a surviving replacement owner, a historical evidence route, and
  green post-delete validation. Otherwise the disposition is `DEFER`.
- No live Kubernetes, Argo CD, Vault, ESO, cloud, provider-runtime, hosted-CI,
  remote, credential-bearing, secret-reading, push, merge, publication, or
  external mutation is authorized.
- Each non-empty WGIA work package is one logical commit. A work package with
  no required repository delta is closed as reviewed evidence in the next
  evidence-bearing commit; empty commits are forbidden.
- Task-created caches and scratch artifacts stay under ignored SDD state or
  `/tmp` and are removed before branch finishing.

---

## Overview

This Plan activates the direct-human-approved standalone execution relation
for Spec 054. It audits and, where proof permits, reconciles the current
workspace governance system across purpose, roles, SDLC, documentation, CI/CD,
QA, harness, loop, fixtures, scripts, blockers, LLM-WIKI, memory, agents,
security, and cleanup. The resulting pack becomes a current lookup and dated
analysis surface; it does not replace the machine or policy owners it audits.

The human approved the specification and selected subagent-driven execution on
2026-08-09. Implementation therefore proceeds task-by-task in this isolated
worktree. The primary agent owns task dispatch, exact staged-scope checks,
review gates, commits, and lifecycle closure. Workers are not authorized to
stage, commit, push, merge, or remove worktrees.

## Context

The design commit is `d9ffa12a` on branch
`codex/2026-08-09-workspace-governance-audit`. The repository currently treats
`docs/90.references/audits/2026-07-11-weia/` as the Current audit through the
audit collection README, `document-profiles.json`, the RIA data contract,
`scripts/reference_information_architecture.py`, and exact tests and fixtures.
That pack remains protected historical evidence after cutover; its body is not
rewritten.

Current active authorities include the root purpose statement, Stage 00 agent
governance, Stage 01-05 SDLC owners, the Stage 99 document-profile registry and
templates, Stage 90 RIA and LLM-WIKI data, `.github` workflows, validation
scripts, tests, and provider-specific adapters. The audit must derive current
counts and ownership from those sources at the observation commit instead of
copying conclusions from prior audits.

The current QA contract explicitly describes tracked Prettier configuration as
dormant. WGIA-004 must determine whether any current surface incorrectly claims
coverage and either correct that claim, admit one safe owner through a separate
reviewed remediation, remove a truly unused configuration after proof, or keep
it as a documented `DEFER`. Presence is not enforcement evidence.

[ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
governs the direct-approval relation for this exact Spec/Plan/Task pair. No PRD
or ARD authority is asserted by this Plan.

## Goals & In-Scope

- Activate one reciprocal Spec 054 / Plan / Task execution relation.
- Freeze an exact observation commit and complete a tracked-surface inventory.
- Create the exact ten-file pack and exact 30-row request ownership matrix.
- Audit every requested scope against current canonical workspace evidence.
- Record every material finding with the full Spec 054 finding shape.
- Distinguish repository-static, hosted, provider-runtime, and live evidence.
- Correct unambiguous purpose conflicts in the canonical owner and affected
  projections without turning the audit into policy.
- Build a proof-complete Legacy, Deprecated, duplicate, and one-shot candidate
  ledger and integrated remediation roadmap.
- Make `2026-08-09-wgia` the sole Current audit through an atomic RIA/profile/
  index/link/fixture/test transition.
- Delete only proof-complete candidates, run post-delete validation, re-audit
  the target state, obtain independent reviews, and close honestly.

## Non-Goals & Out-of-Scope

- Rewriting or deleting any of the six existing audit-pack bodies.
- Modifying Stage 98 archive records, digests, envelopes, or payloads.
- Treating filename vocabulary such as `legacy`, `deprecated`, `fixture`, or
  `validator` as deletion evidence.
- Creating a new machine contract when an existing RIA, document-profile, or
  validation-surface interface can express the invariant.
- Changing approved PRD, ARD, accepted ADR, active Spec, operations policy, or
  permission model without a separate human decision.
- Claiming provider discovery, authentication, model resolution, hosted run,
  cluster state, GitOps convergence, Vault/ESO behavior, or deployment
  readiness from repository-static evidence.
- Hand-editing generated LLM-WIKI or RIA output.
- Pushing, opening a pull request, merging, or deleting the branch/worktree
  before the finishing skill presents the human-owned integration choices.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WGIA-000 | Activate the standalone Spec/Plan/Task execution path | Spec design commit | Human approval of Spec 054 | Active reciprocal documents, standalone registry row, green lifecycle gates |
| WGIA-001 | Freeze observation identity and establish the exact pack/finding contracts | WGIA-000 | Clean activation commit | Ten-file skeleton, 30-row ownership, source/canonical-owner inventory, focused negative tests |
| WGIA-002 | Audit purpose, roles, governance, operating contracts, and provider shims | WGIA-001 | Pack contract green | Reviewed governance report and finding rows |
| WGIA-003 | Audit spec-driven SDLC, documents, templates, README rules, and integration guides | WGIA-001 | Pack contract green | Reviewed documentation/SDLC report and registry evidence |
| WGIA-004 | Audit CI/CD, GitHub Actions, QA, formatting, linting, syntax, tests, fixtures, Validation, and Verification | WGIA-001 | Pack contract green | Reviewed delivery/QA report and dormant-control disposition |
| WGIA-005 | Audit harness, loop, scripts, fixtures, checkpoints, blockers, recovery, and handoff | WGIA-001 | Pack contract green | Reviewed harness/loop report and state-machine evidence |
| WGIA-006 | Audit LLM-WIKI, knowledge routing, and all memory classes | WGIA-001 | Pack contract green | Reviewed knowledge/memory report and generator evidence |
| WGIA-007 | Audit integrated orchestration, every current agent role, adapters, models, evaluation, and admission | WGIA-001 | Pack contract green | Reviewed agent report and exact machine-derived role matrix |
| WGIA-008 | Audit security, supply chain, approvals, secrets, GitOps, infrastructure, destructive, remote, and live boundaries | WGIA-001 | Pack contract green | Reviewed security report with static/deeper-lane separation |
| WGIA-009 | Build the candidate disposition ledger and integrated remediation roadmap | WGIA-002–008 | All topic findings reviewed | Complete candidate rows, dependency graph, owner-family remediation queue |
| WGIA-010 | Correct proof-complete governance, SDLC, documentation, and knowledge-owner conflicts | WGIA-009 | Approved unambiguous Correct/Integrate rows | Canonical owner plus projections green, or reviewed no-delta evidence |
| WGIA-011 | Correct proof-complete delivery, harness, agent, and security-owner conflicts | WGIA-009 | Approved unambiguous Correct/Integrate rows | Canonical owner plus projections green, or reviewed no-delta evidence |
| WGIA-012 | Cut over the sole Current audit pointer and all mutable consumers atomically | WGIA-010–011 | Final report headings and remediation state stable | New Current identity, protected prior Current, RIA/profile/link/tests green |
| WGIA-013 | Delete only proof-complete candidate artifacts | WGIA-012 | Delete rows pass pre-delete gate | Exact deletions, zero consumers, post-delete clone/staged checks, rollback commit |
| WGIA-014 | Re-audit, close criteria, run full gates/reviews, clean residue, and finish the branch | WGIA-013 | All implementation units reviewed | VAL-WGA-001–012 evidence, terminal QA, clean residue, done lifecycle |

### File Structure

#### New audit pack

- `docs/90.references/audits/2026-08-09-wgia/README.md` — observation
  identity, evidence/verdict vocabulary, reading order, exact ten-file index,
  exact 30-row request-to-owner matrix, and Current/descriptive boundary.
- `workspace-purpose-governance-and-operating-contracts.md` — purpose, roles,
  authority hierarchy, provider shims, approvals, and owner conflicts.
- `spec-driven-sdlc-documentation-and-templates.md` — SDD, SDLC, document
  families, routes, lifecycle, templates, README and integration-guide rules.
- `ci-cd-github-actions-qa-and-validation.md` — workflows, triggers, affected
  surfaces, formatting/lint/syntax/tests, fixtures, evidence, Validation and
  Verification, dormant controls, and fallback semantics.
- `harness-loop-fixtures-scripts-and-blockers.md` — harness/loop state,
  scripts, fixtures, checkpoints, retry/stop/recovery, blockers, and handoffs.
- `llm-wiki-memory-and-knowledge-management.md` — generated knowledge routing,
  four memory classes, authority, conflict, redaction, freshness, promotion,
  and retention.
- `ai-agents-integrated-and-role-specific-agents.md` — integrated supervisor,
  exact current role roster, responsibilities, inputs, outputs, prohibited
  actions, stops, adapters, model routing, admission, evaluation, and evidence
  limits.
- `security-and-approval-boundaries.md` — repository, workflow, supply-chain,
  agent, secret, GitOps, infrastructure, permission, destructive, remote, and
  live controls.
- `legacy-deprecated-and-one-shot-disposition-ledger.md` — exact candidates,
  source commits, consumers, replacement owners, decisions, proof, and
  historical routes.
- `remediation-and-integration-roadmap.md` — integrated finding register,
  dependencies, priorities, canonical owners, implementation/rollback order,
  blockers, verification, and residual `DEFER` backlog.

#### Lifecycle and indexes

- Modify Spec 054, `docs/03.specs/README.md`, this Plan, its Task,
  `docs/04.execution/plans/README.md`, `docs/04.execution/tasks/README.md`, and
  `docs/99.templates/support/document-profiles.json` for the exact active
  standalone relation.
- Update `docs/00.agent-governance/memory/progress.md` only with durable,
  bounded progress and terminal evidence; detailed worker reports remain under
  ignored `.superpowers/sdd/2026-08-09-workspace-governance-audit-and-remediation/`.

#### Current audit and RIA cutover

- Modify `docs/90.references/audits/README.md` and, only if currentness wording
  requires it, `docs/90.references/README.md`.
- Modify `docs/99.templates/support/document-profiles.json` so
  `referenceCurrentPacks.packs` names only `audits/2026-08-09-wgia` with the
  exact nine non-README members.
- Modify `docs/90.references/data/reference-information-architecture.json`,
  its schema only if the existing shape cannot preserve the historical
  baseline, and the canonical producer
  `scripts/reference_information_architecture.py`.
- Modify `tests/test_reference_information_architecture.py` and affected
  fixtures under `tests/fixtures/reference-information-architecture/`.
- Inspect and update `tests/fixtures/links-and-owners.json` and
  `tests/fixtures/validation-surfaces.json` when their current-audit projection
  requires the new exact owner.
- Run `bash scripts/generate-llm-wiki-index.sh --check`; change its canonical
  inputs and regenerate only when a topic owner is intentionally added to its
  source map.

#### Canonical remediation surfaces

- Governance candidates: `README.md`, `AGENTS.md`,
  `docs/00.agent-governance/**`, and tracked provider shims.
- SDLC/document candidates: `docs/01.requirements/**` through
  `docs/05.operations/**`, `docs/99.templates/**`, document schemas,
  registries, templates, and their validators/tests.
- Delivery candidates: `.github/**`, `.pre-commit-config.yaml`, formatter/
  linter configuration, validation-surface contracts, scripts, and tests.
- Agent/knowledge/security candidates: Stage 00 machine contracts, provider
  adapters, LLM-WIKI canonical sources, security scripts, manifests, and static
  infrastructure tests.
- The exact delta is determined by WGIA-002–009 evidence. This Plan does not
  pre-authorize speculative edits or deletion by path name.

### Interfaces and Invariants

#### Audit finding interface

Every material finding must expose: stable finding ID, request IDs, scope,
expected state, observed state, exact path plus anchor/selector evidence,
evidence depth, closed verdict, impact, closed disposition, canonical owner,
verification commands, uncertainty, blocker or explicit `None`, and review
state. Report-local prose may explain a row but may not omit these fields.

#### Cleanup interface

Every candidate row must expose: exact tracked path, full source commit,
candidate class, every current consumer type, replacement owner and heading or
interface, Keep/Integrate/Correct/Delete/DEFER decision, evidence, historical
route, pre-delete status, post-delete status, and reviewer. `Delete` is invalid
until every field is complete and the target is absent in a staged or isolated
post-delete validation tree.

#### Current transition interface

The transition has one old ID, one new ID, one full cutover commit, exact new
members, exact old historical baseline, and mutable-consumer dispositions. The
audit collection, document profiles, RIA data, producer, schema, fixtures,
tests, and links must agree in one commit. Two Current packs or an unprotected
old Current snapshot fail closed.

#### Review interface

Each work package uses a fresh implementation worker when code/content changes
are needed, then a fresh specification reviewer, then a fresh quality reviewer.
Critical or Important findings return to the same implementation worker for a
bounded fix round and both reviewers re-check. The primary agent alone stages,
commits, and advances the Task ledger.

### Detailed Tasks

#### WGIA-000 — Activate the execution relation

**Files:** Spec 054; ADR-0022; this Plan; the reciprocal Task;
Specs/Plans/Tasks indexes; `document-profiles.json`;
`scripts/validate-links-and-owners.py`; `tests/fixtures/links-and-owners.json`;
durable progress only if activation evidence is recorded.

- [x] Add a positive fixture for a different valid ISO approval date and
  capture the intended `STANDALONE-EXECUTION-APPROVAL` RED under the prior
  first-relation date constant.
- [x] Generalize the approval statement parser to an exact ISO calendar date,
  add an invalid-date negative, and make the same self-test GREEN.
- [x] Change Spec 054 from `draft` to `active` and state that the approved Plan
  and Task activate its ADR-0022 standalone execution relation.
- [x] Add the exact Plan and Task to their tree and table indexes as `Active`.
- [x] Add sorted standalone relation `spec=054`, exact Plan/Task paths,
  `state=active`, `decision=0022`, `approvalMode=spec-body-record`.
- [x] Stage only the activation files so tracked-path identity checks see the
  exact intended index.
- [x] Run strict document registry, Markdown profile, strict links/owners,
  `git diff --cached --check`, and the full repository quality gate.
- [x] Update WGIA-000 evidence and prepare the logical commit
  `docs: activate workspace governance audit`; WGIA-001 records its resulting
  full 40-hex hash as the observation commit before creating the pack.

#### WGIA-001 — Freeze evidence and create the exact pack contract

**Files:** the exact ten new pack files; audit collection README only if needed
for draft discovery; focused fixtures/tests that own exact membership and
finding/request schemas; Task/progress evidence.

- [x] Capture the activation commit with `git rev-parse HEAD`, enumerate all
  tracked files with `git ls-files`, and record inventory commands and counts.
- [x] Write failing tests or deterministic probes for missing/duplicate/unknown
  member, wrong 30-row sequence, duplicate owner, incomplete finding fields,
  invalid verdict/evidence depth, and forbidden Stage 98 delta.
- [x] Create exactly ten files in profile-compliant final form: `README.md`
  uses the frontmatter-free `readme/snapshot-pack` contract and its required
  headings, while the nine non-README reports use required final frontmatter,
  final `content/reference` headings, report-local finding registers, Sources,
  Review and Freshness, and Related Documents.
- [x] Populate README with exact `REQ-WGA-001`–`030` primary owners and current
  workspace evidence; do not mark unreviewed report findings `Aligned`.
- [x] Build canonical-owner/source inventories from the observation commit and
  label unavailable hosted/provider/live evidence `DEFER`.
- [x] Make focused pack checks GREEN; run profiles, strict links, diff, and full
  gate; complete both reviews; commit `docs: establish governance audit pack`.

#### WGIA-002 — Purpose, roles, governance, and operating contracts

**Files:** `workspace-purpose-governance-and-operating-contracts.md`, README
coverage/verdict cells, roadmap/ledger rows needed by the findings, Task and
progress evidence.

- [x] Inspect root purpose and root/provider shim routing, Stage 00 authority,
  approval boundaries, operating rules, role owners, and overview consistency.
- [x] Derive a canonical-owner matrix and identify duplication, stale routing,
  missing authority, and purpose conflicts without changing owners yet.
- [x] Populate full finding rows and As-Is/Gap/Target analysis; keep provider
  discovery/auth/runtime claims separate from tracked adapters.
- [x] Run governance/closure, registry, profile, links, and harness-focused
  checks; review content against VAL-WGA-003.
- [x] Record remediation candidates in the roadmap/ledger and commit
  `docs: audit workspace governance contracts`.

#### WGIA-003 — Spec-driven SDLC, documentation, and templates

**Files:** `spec-driven-sdlc-documentation-and-templates.md`, README coverage,
roadmap/ledger rows, Task and progress evidence.

- [x] Inventory Stage 01-05 routes, PRD/ARD/ADR/Spec/Plan/Task/Guide/Incident/
  Postmortem/Policy/Release/Runbook roles, lifecycle rules, indexes, and owners.
- [x] Compare document profiles, schema, templates, source/template parity,
  README rules, integration guides, Diataxis routing, and generated documents.
- [x] Record gaps such as an absent active profile or unsupported lifecycle as
  findings rather than inventing a template or route.
- [x] Run document registry self-tests/strict production, Markdown profiles,
  lifecycle, and strict links; review against VAL-WGA-004.
- [x] Record remediation candidates and commit
  `docs: audit spec driven documentation system`.

#### WGIA-004 — CI/CD, GitHub Actions, QA, Validation, and Verification

**Files:** `ci-cd-github-actions-qa-and-validation.md`, README coverage,
roadmap/ledger rows, Task and progress evidence.

- [x] Inventory workflow triggers/jobs/actions/pins/permissions/concurrency,
  pre-commit lanes, affected surfaces, formatting, linting, syntax, unit,
  integration, contract, security, and policy checks.
- [x] Map each lane to trigger, exact command/tool, result class, evidence depth,
  fallback/SKIP semantics, artifact, and remediation owner.
- [x] Write a failing evidence probe for any current claim that treats dormant
  Prettier configuration or a non-invoked tool as coverage; otherwise record a
  reviewed dormant `DEFER` without manufacturing a failure.
- [x] Preserve distinct Validation and Verification results across report rows.
- [x] Run Actions security, CI Python contract, affected surfaces, profiles,
  links, and relevant workflow tests; review against VAL-WGA-005.
- [x] Record remediation candidates and commit `docs: audit ci and qa controls`.

#### WGIA-005 — Harness, loop, fixtures, scripts, and blockers

**Files:** `harness-loop-fixtures-scripts-and-blockers.md`, README coverage,
roadmap/ledger rows, Task and progress evidence.

- [x] Trace harness contract, catalog, implementation map, loop lifecycle,
  checkpoint, memory, handoff, retry/stop/recovery, and approval interfaces.
- [x] Inventory script entrypoints and fixtures by production contract owner;
  identify tests that mask missing production behavior or duplicate ownership.
- [x] Model every blocker with cause, impact, affected requirements, release
  condition, owner, and evidence depth.
- [x] Run harness contract/semantics, loop lifecycle, checkpoint, roster
  currentness, provider-boundary checks, profiles, and links.
- [x] Review static/runtime separation against VAL-WGA-006, record candidates,
  and commit `docs: audit harness and loop controls`.

#### WGIA-006 — LLM-WIKI, knowledge routing, and memory

**Files:** `llm-wiki-memory-and-knowledge-management.md`, README coverage,
roadmap/ledger rows, Task and progress evidence.

- [x] Inspect LLM-WIKI canonical sources, generator, generated output,
  freshness/drift checks, and current lookup routes.
- [x] Audit working/short-term, durable/long-term, domain-scoped, and
  provider-local auxiliary memory for authority, promotion, conflict,
  redaction, freshness, retention, and deletion rules.
- [x] Prove repository-wins and generated-output ownership; do not hand-edit the
  generated wiki index.
- [x] Run the LLM-WIKI generator check, loop/checkpoint/memory-related checks,
  profiles, and links; review against VAL-WGA-007.
- [x] Record candidates and commit `docs: audit knowledge and memory controls`.

#### WGIA-007 — Integrated and role-specific AI agents

**Files:** `ai-agents-integrated-and-role-specific-agents.md`, README coverage,
roadmap/ledger rows, Task and progress evidence.

- [x] Derive the exact role inventory, adapter surfaces, and model/evaluation/
  admission state from current machine owners at the observation commit.
- [x] Give every role one responsibility, inputs, outputs, prohibited actions,
  stop conditions, downstream handoff, adapters, model rule, evaluation state,
  and evidence boundary.
- [x] Audit integrated supervisor orchestration, delegation, isolation,
  checkpointing, escalation, and completion gates separately from workers.
- [x] Keep repo-static adapter parity separate from native/provider discovery,
  authenticated execution, and effective model resolution.
- [x] Run roster currentness/admission/evaluation, harness semantics, model
  fitness, provider config/evidence/canary checks; review VAL-WGA-008.
- [x] Record candidates and commit `docs: audit agent system and roles`.

#### WGIA-008 — Security and approval boundaries

**Files:** `security-and-approval-boundaries.md`, README coverage,
roadmap/ledger rows, Task and progress evidence.

- [x] Inventory repository, workflow, supply-chain, agent, secret, GitOps,
  infrastructure, permission, destructive, remote, and live trust boundaries.
- [x] Map each control to owner, threat, enforcement point, evidence artifact,
  bypass/exception route, failure mode, and approval authority.
- [x] Inspect only structure and metadata needed by the approved static lane;
  never print secret values or perform live/provider/remote mutation.
- [x] Run GitHub Actions security, secret handling, policy, Vault/ESO static,
  manifest/GitOps/static-infrastructure, profile, and link gates.
- [x] Obtain a security-focused review against VAL-WGA-009, record candidates,
  and commit `docs: audit security and approval boundaries`.

#### WGIA-009 — Disposition ledger and integrated roadmap

**Files:** `legacy-deprecated-and-one-shot-disposition-ledger.md`,
`remediation-and-integration-roadmap.md`, cross-report finding references,
README final verdict cells, Task and progress evidence.

- [x] Search tracked names, links, imports, schemas, workflows, invocations,
  generated owners, fixtures, and machine contracts for candidate consumers.
- [x] Add one complete disposition row per candidate using full Git source
  commit, exact consumers, replacement owner, decision, proof, and reviewer.
- [x] Reject name-only and no-rendered-link-only deletion claims; retain active
  legacy validators/contracts and unique evidence.
- [x] De-duplicate cross-report findings into one roadmap row with dependencies,
  priority, canonical owner, rollback, verification, blocker, and status.
- [x] Independently review every Delete/Correct/Integrate row and run legacy,
  active-corpus, RIA, link, archive, profile, and diff gates.
- [x] Commit `docs: classify governance remediation and cleanup`.

#### WGIA-010 — Governance, SDLC, documentation, and knowledge remediation

**Files:** only canonical owner families named by accepted WGIA-009 rows, their
schemas/projections/fixtures/tests, audit finding status, Task/progress evidence.

- [x] Select only unambiguous `Correct` or `Integrate` rows in governance,
  SDLC, documentation, templates, README routing, LLM-WIKI, or memory.
- [x] Add the smallest failing regression at the current contract owner; record
  exact RED output before production edits.
- [x] Correct the canonical owner and every affected projection without copying
  policy into Stage 90 or hand-editing generated output.
- [x] Make focused tests GREEN, regenerate through canonical producers when
  needed, and re-audit the finding expected/observed state.
- [x] Run strict registry/profiles/links, RIA/LLM-WIKI as affected, archive,
  full gate, both reviews, and commit
  `fix: reconcile governance documentation owners` when non-empty.

WGIA-010 is `Done`: focused repository-static checks, exact staged aggregate,
generator parity, and both fresh reviews pass. Normal unstaged RIA production
rejected the intentionally dirty comparison inputs before staging; the staged
full gate passed the RIA boundary. Commit evidence is recorded in the Task.

#### WGIA-011 — Delivery, harness, agent, and security remediation

**Files:** only canonical owner families named by accepted WGIA-009 rows, their
schemas/projections/fixtures/tests, audit finding status, Task/progress evidence.

- [x] Select only unambiguous `Correct` or `Integrate` rows in CI/QA, scripts,
  fixtures, harness, loop, agents, models, providers, or security.
- [x] Add focused RED tests that preserve existing negative coverage and do not
  infer deeper evidence from static configuration.
- [x] Correct one owner family and all affected projections per reviewable
  sub-unit; do not combine unrelated workflow, agent, and security changes.
- [x] Run the exact affected validator/test matrix, re-audit each finding, and
  keep hosted/provider/live rows `DEFER`.
- [x] Run full gate, harness, security review, both task reviews, and commit one
  logical sub-unit per non-empty owner family using `fix:` messages.

WGIA-011 is `Done`: exact staged repository gates, focused harness/provider
tests, and fresh specification/content, Python/quality, and security reviews
pass. Provider-native permission loading and effective enforcement remain
`DEFER`; logical commit evidence is recorded in the Task.

#### WGIA-012 — Atomic Current audit cutover

**Files:** audit collection/root README as needed, document profiles, RIA data/
schema/producer/validator, RIA tests/fixtures, links/owners and validation-
surface fixtures as affected, mutable current links, Task/progress evidence.

- [ ] Write RED cases for sole new Current selection, exact nine non-README
  members, old-Current historical preservation, baseline byte drift, missing/
  duplicate members, stale current navigation, and broken mutable links.
- [ ] Replace the Current registry ID with `audits/2026-08-09-wgia`, preserve
  `audits/2026-07-11-weia` as source-commit-bounded historical evidence, and
  update the collection README in the same index state.
- [ ] Update RIA canonical data and producer, extending its schema only if the
  existing shape cannot preserve the old historical baseline without loss.
- [ ] Migrate mutable links and fixtures to exact new headings; retain dated or
  source-commit-pinned historical observations without rewriting their truth.
- [ ] Make focused RIA/registry/profile/link tests GREEN in a staged or isolated
  tree; run LLM-WIKI check, archive validation, full gate, harness, both reviews.
- [ ] Commit `docs: cut over current governance audit` as one atomic unit.

#### WGIA-013 — Evidence-gated deletion

**Files:** only exact `Delete` rows and necessary mutable consumers, the
disposition ledger, roadmap, Task/progress evidence. Stage 98 is forbidden.

- [ ] Re-run zero-consumer and replacement-owner proof at current HEAD for each
  Delete row; demote any incomplete row to `DEFER`.
- [ ] Simulate the exact deletions in an isolated clone or staged index and run
  affected link/RIA/archive/import/invocation/fixture checks before committing.
- [ ] Delete only proof-complete exact paths, update the ledger post-delete
  evidence and surviving current indexes, and verify no unrelated file is gone.
- [ ] Run strict registry/profiles/links, affected tests, RIA, legacy and active-
  corpus validators, archive validation, full gate, harness, and both reviews.
- [ ] Commit `chore: remove retired governance artifacts`; if there are no
  valid Delete rows, record the reviewed no-deletion result without an empty
  commit and advance.

#### WGIA-014 — Re-audit, closure, and branch handoff

**Files:** all ten pack files for final observed-state reconciliation; Spec,
Plan, Task and indexes; document profiles standalone state; durable progress;
ignored SDD reports only until cleanup.

- [ ] Re-run the exact tracked inventory and all 30 request rows against the
  final tree; reconcile As-Is/Target, finding status, blockers, roadmap, and
  deletion evidence without erasing dated observations.
- [ ] Walk VAL-WGA-001–012 one by one and record deterministic command/result,
  limitations, commit, and review evidence in the Task.
- [ ] Run strict registry, profiles, links, RIA, LLM-WIKI, CI/QA, harness/loop/
  model/roster, security, legacy/active corpus, archive, full quality gate,
  full harness, diff checks, and scoped/all-files pre-commit when available.
- [ ] Obtain a whole-branch correctness/security/coverage review; resolve all
  Critical and Important findings and rerun affected plus terminal gates.
- [ ] Verify zero Stage 98 diff, zero tracked scratch, no unclassified mutable
  consumer, and logical commit history; remove task-created one-off files.
- [ ] Set Spec/Plan/Task/indexes/standalone relation to `done`, commit
  `docs: close workspace governance audit`, then invoke branch finishing.

## Verification Plan

| Work package | Deterministic checks | Evidence lane |
| --- | --- | --- |
| WGIA-000 | strict registry, profiles, links/owners, cached diff, full gate | repository-static |
| WGIA-001 | exact 10/30 shape, closed vocabulary, negative fixtures, profiles, links | repository-static |
| WGIA-002 | governance/closure, registry, links, harness, content review | repository-static |
| WGIA-003 | registry self-test/strict, template parity, profiles, lifecycle, links | repository-static |
| WGIA-004 | Actions security, CI Python, affected surfaces, workflow/QA tests | repository-static; hosted DEFER |
| WGIA-005 | harness contract/semantics, loop, checkpoint, roster/provider checks | repository-static; provider-runtime DEFER |
| WGIA-006 | LLM-WIKI generator, memory/loop/checkpoint, profiles, links | repository-static |
| WGIA-007 | roster, admission, evaluations, model fitness, provider boundaries | repository-static; provider-runtime DEFER |
| WGIA-008 | secret/policy/workflow/static platform/security checks | repository-static; live DEFER |
| WGIA-009 | exact candidate/consumer ledger, legacy/active corpus/RIA/archive gates | repository-static |
| WGIA-010 | TDD RED/GREEN plus exact owner-family gates and full gate | repository-static |
| WGIA-011 | TDD RED/GREEN, harness/security/affected gates and full gate | repository-static; deeper lanes DEFER |
| WGIA-012 | RIA RED/GREEN, sole Current, historical-byte guard, links, full gate | repository-static |
| WGIA-013 | zero-consumer proof, isolated/staged post-delete checks, full gate | repository-static |
| WGIA-014 | VAL walk, complete QA, whole-branch review, residue/history checks | repository-static |

Commands are evidence only after their current CLI is confirmed with `--help`
or source inspection. The expected command inventory includes:

```bash
git diff --check
git diff --cached --check
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-reference-information-architecture.py --root .
bash scripts/generate-llm-wiki-index.sh --check
python3 scripts/validate-github-actions-security.py --root .
python3 scripts/validate-ci-python-contract.py --root .
python3 scripts/validate-affected-surfaces.py --root .
python3 scripts/validate-agent-legacy-cutover.py --root .
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-loop-lifecycle.py --root .
python3 scripts/validate-agent-model-fitness.py --root .
python3 scripts/validate-agent-roster-currentness.py --root .
python3 scripts/archive_validation.py
bash scripts/validate-repo-quality-gates.sh .
bash scripts/validate-harness.sh
pre-commit run --all-files
```

An optional tool that is unavailable, times out, or is not configured is
reported as `SKIP` or bounded fallback evidence. It never replaces a required
repository gate or becomes a false PASS.

## Risks & Mitigations

| Risk | Mitigation | Owner |
| --- | --- | --- |
| The new audit becomes a competing policy owner | Keep rules in canonical owners and link from Stage 90 findings | Every topic reviewer |
| Current identity is split across prose and machine projections | Change collection, profiles, RIA, fixtures, tests, and links atomically | WGIA-012 reviewer |
| Prior Current audit loses byte protection | Add RED historical-baseline tests before transition; do not rewrite old body | WGIA-012 reviewer |
| A broad audit creates speculative owner changes | Require exact finding, unambiguous authority, RED test, and accepted roadmap row | WGIA-010/011 reviewers |
| Dormant tooling is mistaken for coverage | Require a real consumer or keep/remove it with explicit evidence | WGIA-004 reviewer |
| Legacy-name search deletes active controls | Require import/invocation/schema/workflow/fixture consumers and reviewer | WGIA-009/013 reviewers |
| Historical evidence is falsified by current link migration | Preserve dated text and source commit; add a separate current lookup | WGIA-012 reviewer |
| Generated output is edited manually | Change canonical input and regenerate; verify with `--check` | WGIA-006/010 reviewer |
| Static checks are promoted to runtime claims | Closed evidence-depth vocabulary and independent content review | Every reviewer |
| A worker changes shared or forbidden files | Assign exact ownership, inspect branch diff, reject Stage 98 or unrelated changes | Primary agent |
| A gate passes only because coverage was removed | Preserve negative fixtures and compare affected-surface/role counts | Quality reviewer |
| Deletion fails after commit | Validate in staged/isolated tree first; keep deletion in one revertible commit | WGIA-013 reviewer |

Rollback is commit-scoped. Before WGIA-012, reverting a report or remediation
commit leaves the old Current audit in place. WGIA-012 is one atomic Current
transition and can be reverted without altering historical pack bodies.
WGIA-013 contains only independently proven deletions and can be reverted
without history rewriting.

## Completion Criteria

- The exact ten new files exist and the README owns exactly 30 sequential,
  unique request rows with one primary heading each.
- Every material finding contains the complete Spec 054 fields and a reviewed
  evidence depth, verdict, disposition, blocker state, and verification route.
- Purpose, governance, SDLC/docs/templates, delivery/QA, harness/loop,
  knowledge/memory, agents, and security reports derive from current owners.
- Every candidate has a full source/consumer/replacement disposition, and only
  proof-complete Delete rows are absent.
- The new pack is the sole Current audit; the prior Current is protected
  historical evidence; mutable consumers and machine projections agree.
- Existing audit bodies and `docs/98.archive/**` have no unauthorized diff.
- All required focused and terminal gates pass; optional evidence is reported
  honestly; deeper lanes remain `DEFER` unless separately authorized.
- Every non-empty work package has specification and quality approval and one
  logical commit; the whole-branch review has no unresolved Critical/Important
  finding.
- Spec, Plan, Task, collection indexes, standalone relation, task evidence, and
  durable progress agree on `done`; task-created one-off artifacts are gone.

## Traceability

- [Spec 054](../../03.specs/054-workspace-governance-audit-and-remediation/spec.md)
- [ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [WGIA Task](../tasks/2026-08-09-workspace-governance-audit-and-remediation.md)
- [Current audit collection](../../90.references/audits/README.md)
- [RIA data owner](../../90.references/data/reference-information-architecture.json)

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-WGA-001](../../03.specs/054-workspace-governance-audit-and-remediation/spec.md#success-criteria--verification-plan) | WGIA-001, WGIA-014 | [Exact ten-file and 30-row evidence](../tasks/2026-08-09-workspace-governance-audit-and-remediation.md#task-table). |
| N/A — VAL-WGA-002 shares the Spec source above | WGIA-001–009, WGIA-014 | [Finding-field completeness and independent reviews](../tasks/2026-08-09-workspace-governance-audit-and-remediation.md#task-table). |
| N/A — VAL-WGA-003 shares the Spec source above | WGIA-002, WGIA-010, WGIA-014 | [Purpose/governance owner matrix and remediation evidence](../tasks/2026-08-09-workspace-governance-audit-and-remediation.md#task-table). |
| N/A — VAL-WGA-004 shares the Spec source above | WGIA-003, WGIA-010, WGIA-014 | [SDLC/document/profile/template evidence](../tasks/2026-08-09-workspace-governance-audit-and-remediation.md#task-table). |
| N/A — VAL-WGA-005 shares the Spec source above | WGIA-004, WGIA-011, WGIA-014 | [CI/QA/fixture/Validation/Verification evidence](../tasks/2026-08-09-workspace-governance-audit-and-remediation.md#task-table). |
| N/A — VAL-WGA-006 shares the Spec source above | WGIA-005, WGIA-011, WGIA-014 | [Harness/loop/script/blocker evidence](../tasks/2026-08-09-workspace-governance-audit-and-remediation.md#task-table). |
| N/A — VAL-WGA-007 shares the Spec source above | WGIA-006, WGIA-010, WGIA-014 | [LLM-WIKI and memory lifecycle evidence](../tasks/2026-08-09-workspace-governance-audit-and-remediation.md#task-table). |
| N/A — VAL-WGA-008 shares the Spec source above | WGIA-007, WGIA-011, WGIA-014 | [Exact agent/adapter/model/evaluation evidence](../tasks/2026-08-09-workspace-governance-audit-and-remediation.md#task-table). |
| N/A — VAL-WGA-009 shares the Spec source above | WGIA-008, WGIA-011, WGIA-014 | [Security/approval/static platform evidence](../tasks/2026-08-09-workspace-governance-audit-and-remediation.md#task-table). |
| N/A — VAL-WGA-010 shares the Spec source above | WGIA-009, WGIA-013, WGIA-014 | [Candidate ledger and post-delete evidence](../tasks/2026-08-09-workspace-governance-audit-and-remediation.md#task-table). |
| N/A — VAL-WGA-011 shares the Spec source above | WGIA-012, WGIA-014 | [Sole Current transition and historical protection evidence](../tasks/2026-08-09-workspace-governance-audit-and-remediation.md#task-table). |
| N/A — VAL-WGA-012 shares the Spec source above | WGIA-010–014 | [Re-audit, blocker closure, reviews, full QA, and commit ledger](../tasks/2026-08-09-workspace-governance-audit-and-remediation.md#task-table). |
