---
title: 'Workspace Governance Audit and Remediation Implementation Plan'
version: "1.0.0"
type: sdlc/plan
layer: "specs"
status: done
owner: platform
updated: 2026-08-09
artifact_id: "SPEC-0055-PLAN-0001"
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

**Global Constraints**

- The approved specification is
  [Spec 0055](./spec.md).
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

[ADR-0022](../../../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
governs the direct-approval relation for this exact Spec/Plan/Task pair. No PRD
or AD authority is asserted by this Plan.

### Legacy Task ledger inputs

This Task is the durable execution and evidence ledger for the approved
[Workspace Governance Audit and Remediation Plan](./plan.md)
and [Spec 0055](./spec.md).
It tracks the exact ten-file Current audit pack, canonical-owner audit and
remediation, machine-contract cutover, evidence-gated cleanup, independent
reviews, terminal verification, and lifecycle closure.

Detailed worker and review reports live under the ignored SDD directory
`.superpowers/sdd/2026-08-09-workspace-governance-audit-and-remediation/` while
the branch is active. This Task records only durable results, exact evidence,
limitations, logical commits, and unresolved blockers.

- [Spec 0055](./spec.md)
- [Implementation Plan](./plan.md)
- [ADR-0022](../../../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [Stage 90 reference router](../../../../90.references/README.md)
- [Document profile registry](../../../../99.templates/registry.json)
- [Current source coverage](../../../../90.references/research/0001-workspace-engineering/m0012-source-coverage.md)
- Direct human design approval and Spec approval on 2026-08-09
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
- Changing approved PRD, AD, accepted ADR, active Spec, operations policy, or
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
  `docs/03.specs/0055-workspace-governance-audit-and-remediation/plan.md`, `docs/03.specs/0055-workspace-governance-audit-and-remediation/README.md#task-records`, and
  `docs/99.templates/registry.json` for the exact active
  standalone relation.
- Update `docs/00.agent-governance/memory/progress.md` only with durable,
  bounded progress and terminal evidence; detailed worker reports remain under
  ignored `.superpowers/sdd/2026-08-09-workspace-governance-audit-and-remediation/`.

#### Current audit and RIA cutover

- Modify `docs/90.references/audits/README.md` and, only if currentness wording
  requires it, `docs/90.references/README.md`.
- Modify `docs/99.templates/registry.json` so
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
- Treat the former LLM Wiki generator and generated index as retired; do not
  recreate that parallel owner map when a topic owner changes.

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

- [x] Inventory Stage 01-05 routes, PRD/AD/ADR/Spec/Plan/Task/Guide/Incident/
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

- [x] Write RED cases for sole new Current selection, exact nine non-README
  members, old-Current historical preservation, baseline byte drift, missing/
  duplicate members, stale current navigation, and broken mutable links.
- [x] Replace the Current registry ID with `audits/2026-08-09-wgia`, preserve
  `audits/2026-07-11-weia` as source-commit-bounded historical evidence, and
  update the collection README in the same index state.
- [x] Update RIA canonical data and producer, extending its schema only if the
  existing shape cannot preserve the old historical baseline without loss.
- [x] Migrate mutable links and fixtures to exact new headings; retain dated or
  source-commit-pinned historical observations without rewriting their truth.
- [x] Make focused RIA/registry/profile/link tests GREEN in staged or isolated
  trees; run LLM-WIKI check, archive validation, full gate, and harness.
- [x] Complete fresh specification/content and Python/quality review; both are
  Approved after clean fix rounds 1-2 with no remaining Critical/Important.
- [x] Commit `docs: cut over current governance audit` as one atomic unit.

WGIA-012 is `Done` in commit
`dcc0a0e9fbb9587c211fd457414f9dfe2e6924de`: the sole-Current, exact-member, retired-baseline,
audit-settlement, literal-projection, registry, profile, link, affected,
archive, generator, and isolated exact-index RIA checks pass. Fresh reviews,
including clean fix rounds 1-2, are Approved. The final 17-path affected and
staged lanes, plain pre-commit, direct repository gate, full harness, all-files,
formatter-review, and rerun pass. Hosted, remote, and live evidence remains
`DEFER`.

Primary final evidence expanded the initial exact 15-file index to 17 only
after formatter/QA review. The accepted additions are `.secrets.baseline` and
`docs/03.specs/0055-workspace-governance-audit-and-remediation/plan.md`.
The first plain pre-commit failed on detect-secrets baseline mutation plus WGIA
Plan MD001; the WGIA `Global Constraints` heading became a profile-compatible
bold label, and baseline formatter security review was Approved. The first
all-files lane failed on eight reviewed false-positive metadata/prose candidates
plus pre-existing WERPC Plan MD001. The regenerated baseline has exactly 18
entries across seven paths, every `is_secret` is false, no detector was
weakened, security review is Approved, and WERPC `Global Constraints` is bold.
Final PASS covers affected paths=17, staged paths=17, plain pre-commit, RIA
94/94, production RIA settled, LLM-WIKI, archive, direct repository gate, full
harness, final all-files, formatter-review, and rerun. Primary final diff-checks
remain pending.

#### WGIA-013 — Evidence-gated deletion

**Files:** only exact `Delete` rows and necessary mutable consumers, the
disposition ledger, roadmap, Task/progress evidence. Stage 98 is forbidden.

- [x] Re-run zero-consumer and replacement-owner proof at current HEAD for each
  Delete row; demote any incomplete row to `DEFER`.
- [x] Stop before isolated deletion simulation because the exact ledger has no
  `Delete` row; no post-delete claim or destructive action is applicable.
- [x] Preserve all fifteen exact paths because every row remains `Integrate`
  with at least one tracked external live consumer; no file or index is removed.
- [x] Run focused strict registry/profiles/links and diff checks for the
  no-deletion evidence unit; broader terminal validation remains WGIA-014-owned.
- [x] Commit `chore: remove retired governance artifacts`; if there are no
  valid Delete rows, record the reviewed no-deletion result without an empty
  commit and advance.

WGIA-013 is `Done` with a fail-closed no-deletion result recorded by commit
`4e4adcf3a120d1cd25006c7116f3f1cbbe29edae`. At the revalidation source HEAD
`dcc0a0e9fbb9587c211fd457414f9dfe2e6924de`, the candidate ledger has exactly
15 unique tracked rows, all `Integrate`, and `Delete=0`. Its 114 current-
consumer selectors resolve to tracked paths, every candidate has an external
live consumer and a surviving owner, and all 15 source commits recover the
candidate bytes. Spec 052 `WORK-001` remains `Queued` and `Not executed` with
zero of five execution steps complete. Therefore deletion simulation,
post-delete validation, removal, and a deletion commit are inapplicable; this
bounded evidence update has fresh review approval with no Critical or Important
finding. No empty deletion commit or file removal occurred.

#### WGIA-014 — Re-audit, closure, and branch handoff

**Files:** all ten pack files for final observed-state reconciliation; Spec,
Plan, Task and indexes; document profiles standalone state; durable progress;
ignored SDD reports only until cleanup.

- [x] Re-run the exact tracked inventory and all 30 request rows against the
  final tree; reconcile As-Is/Target, finding status, blockers, roadmap, and
  deletion evidence without erasing dated observations.
- [x] Walk VAL-WGA-001–012 one by one and record deterministic command/result,
  limitations, commit, and review evidence in the Task.
- [x] Run strict registry, profiles, links, RIA, LLM-WIKI, CI/QA, harness/loop/
  model/roster, security, legacy/active corpus, archive, full quality gate,
  full harness, diff checks, and scoped/all-files pre-commit when available.
- [x] Obtain a whole-branch correctness/security/coverage review; resolve all
  Critical and Important findings and rerun affected plus terminal gates.
- [x] Verify zero Stage 98 diff, zero tracked scratch, no unclassified mutable
  consumer, and logical commit history; remove task-created one-off files.
- [x] Set Spec/Plan/Task/indexes/standalone relation to `done`, commit
  `docs: close workspace governance audit`, then invoke branch finishing.

WGIA-014 is `Done`. The terminal criterion record in the Task closes
VAL-WGA-001–012, the 17 pre-closure logical commits, the 53-to-57 self-test
expectation repair, and focused protected-surface checks. The primary agent
records fresh whole-branch review, the exact terminal aggregate/harness/all-files
matrix, reciprocal `done` transition, and logical closure handoff. Hosted CI,
provider-runtime, authenticated, credential-bearing, remote, and live evidence
remains `DEFER`.

The first whole-branch security review found that seven exact repo-script
auto-allows remained mutable command trampolines. The terminal fix removes all
repo-script entries from Claude `permissions.allow`, retains seven fixed
read-only Git metadata commands, and adds a no-trampoline regression. Focused
provider checks pass; fresh security/Python re-review is Approved with no
remaining Critical or Important finding, and the exact terminal matrix is the
closure gate for this final index.

The first exact `done` quality-gate run then failed closed on
`CLOSURE-AUTHORITY-SCOPE` because the terminal active-corpus authority contract
did not yet admit Spec 054 as a later standalone done specification. The
focused RED expected the exact 054 path and failed against the seven-path set;
GREEN adds only that path to the typed post-closure Spec authority set. The
focused test, 49-test closure class, 25-case self-test, production final
frontier, complete repository quality gate, and full harness pass on the exact
staged terminal tree. Plain and all-files pre-commit pass, and fresh
correctness, security, coverage, Python/quality, and specification/content
reviews are Approved with no remaining Critical or Important finding.

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

### Legacy Task verification evidence

WGIA-000 through WGIA-013 are complete. WGIA-012's atomic Current-pointer
implementation is committed: the 2026-08-09 audit is the sole
Current owner and the 2026-07-11 audit is protected historical evidence in the
same exact index state at commit
`dcc0a0e9fbb9587c211fd457414f9dfe2e6924de`. WGIA-013's reviewed no-deletion
result is committed at `4e4adcf3a120d1cd25006c7116f3f1cbbe29edae` because all
15 candidate rows remain `Integrate` with live consumers and Spec 052
`WORK-001` remains queued. WGIA-014 is `In Review`; the reciprocal lifecycle
stays active until the primary agent completes exact-tree terminal gates and
whole-branch review. Hosted, provider-runtime, remote, credential-bearing, and
live evidence remains `DEFER`.

WGIA-001 is complete as a bounded draft successor foundation. Its conservative
`Partial` findings establish source and owner inventories; focused, staged,
and complete repository validation pass, and specification, quality, and
Python reviews are Approved. It does not complete WGIA-002 through WGIA-009 or
promote any scope to `Aligned`.

WGIA-002 is complete. The pinned repository-static comparison found one
aligned purpose/JIT/approval/role-owner control, two root README conflicts, and
one provider-runtime `DEFER`. Focused and complete repository gates pass, and
specification and quality reviews are Approved. It did not change any active canonical owner,
Current pointer, disposition-ledger decision, historical audit body, or Stage
98 path. WGIA-009 owns provisional roadmap admission and WGIA-010 owns any
later root README correction.

WGIA-003 is complete. The pinned repository-static audit found eleven
requested document families structurally aligned, a `Gap` in mapping the broad
Release request to approved DOC-G5's narrower no-release-notes decision, and a
`Partial` approved Guide Type enum whose deterministic enforcement is queued in
WORK-013. Repository-static guide conformance passes while live usability stays
`DEFER`. Two provisional WGIA-009 inputs deduplicate and route to Spec 052 and
WORK-013 rather than reopening decisions. No active registry, schema, template,
lifecycle, stage/index owner, Current pointer, disposition ledger, historical
audit body, or Stage 98 path changed. Independent specification/content
re-review is Approved with no remaining Critical or Important finding.

WGIA-004 is complete. The pinned repository-static audit found tracked
GitHub Actions security and quality-lane ownership `Aligned`, accurate dormant
Prettier reporting at `DEFER`, and a `Partial` boundary between local Validation
and unobserved hosted Verification/deployment CD. No false formatter coverage
claim existed, so the conditional TDD workflow did not run and no failing probe
was manufactured. No canonical owner, roadmap candidate, Current/RIA surface,
historical audit body, or Stage 98 path changed. Fresh specification/content
and quality reviews are Approved with no Critical or Important finding.

### WGIA-001 Focused Evidence

- **Scope and changed paths**: the exact ten files under
  `docs/90.references/audits/2026-08-09-wgia/`, this Task's WGIA-001 evidence,
  the bounded Plan/progress entries, and the README profile inventory fixture,
  validator expectations, and fixture documentation. No Current audit collection pointer,
  `referenceCurrentPacks`, RIA owner/schema/producer/test, historical pack body,
  or Stage 98 path changed.
- **Acceptance IDs**: VAL-WGA-001 and the WGIA-001 foundation portion of
  VAL-WGA-002.
- **Observation and inventory**: `git rev-parse HEAD` returned exact SHA
  `50628b84165479b03efc0a25be075a49c91a9aef`; `git ls-tree -r --name-only
  <SHA> | wc -l` returned 848. Bounded path counts include 461 `docs/`, 48
  `scripts/`, 67 `tests/`, 16 `.github/`, 35 `.agents/`, 17 `.claude/`, 18
  `.codex/`, 13 `.gemini/`, 81 `gitops/`, and 44 protected Stage 98 files.
- **RED**: the pre-creation exact shell probe exited 1 with
  `WGIA-PACK-EXACT FAIL expected=10 actual=0` and
  `WGIA-REQUEST-EXACT FAIL expected=30 actual=0`.
- **Negative probes**: an in-memory Node probe rejected missing and duplicate
  members, corrected unknown-member input, duplicate owner, incomplete finding,
  invalid verdict, invalid evidence depth, and synthetic Stage 98 delta with
  their closed failure codes. No new machine contract or tracked fixture was
  created.
- **GREEN**: the post-write Node parser returned
  `WGIA-PACK-EXACT PASS files=10 requests=30 reports=9` and
  `WGIA-FINDING-CONTRACT PASS`; each finding has one ID heading plus 13 labeled
  fields, for 14 conceptual fields total, and uses the closed eight-verdict and
  four-depth vocabularies.
- **Evidence normalization**: quality-review fix round 2 replaced generic
  finding/source evidence in all nine reports with exact repository-relative
  paths and selectors. The observation-commit probe passed 203 references over
  94 unique paths with zero missing and zero broad-directory values; the
  selector probe passed 122 unique references with zero invalid heading, JSON
  key, script, workflow, manifest, or configuration selectors.
- **Focused profiles and links**:
  `python3 scripts/validate-markdown-profiles.py --root . --mode strict`
  returned zero violations; `python3 scripts/validate-links-and-owners.py
  --root . --mode strict` returned `PASS CROSS-DOCUMENT`.
- **Focused registry and diff**:
  `python3 scripts/validate-document-contract-registry.py --root . --mode
  strict` passed with 502 paths, zero uncovered, and zero ambiguous. The first
  untracked-file `git diff --no-index --check` probe found one trailing blank
  line in four reports; removing only those lines made the exact ten-file rerun
  pass. The first complete gate run then reproduced
  `README program-created active paths must equal the current new inventory`.
  GREEN added the exact lexicographic WGIA snapshot-pack README row and advanced
  only active/program-created counts from 51/6 to 52/7 while preserving
  baseline67, active-baseline45, retired-baseline22, retired-program-created1,
  and retired23. Registry and Markdown self-tests, `git diff --check`, and
  `git diff --cached --check` pass; the observation-commit Stage 98 diff is
  empty. Final count commands return 10 pack files and 30 request rows.
- **Lane results**: targeted `PASS`; affected/staged checks and the complete
  `bash scripts/validate-repo-quality-gates.sh .` lane `PASS` with final exit
  0. Formatter-review and rerun are `SKIP` because no formatter was invoked.
  Hosted CI and remote/live are `DEFER` because no hosted, provider-runtime,
  authenticated, credential-bearing, remote, or live action was authorized.
- **Tool limitation**: RTK 0.34.3 is available, but `rtk gain` failed to
  initialize its tracking database with error code 14. Per the Codex provider
  contract, underlying read-only/focused commands were used without inspecting
  private databases or credential files. Recorded tool versions are Git 2.43.0,
  Python 3.12.3, and Node v24.16.0.
- **Reviewer and disposition**: specification review, final quality re-review,
  and the README-inventory Python review are `Approved` with no remaining
  Critical or Important finding. The foundation remains `draft`; WGIA-014 owns
  final whole-branch review.
- **Rollback**: remove only the exact ten new pack files and revert the bounded
  WGIA-001 Task/progress entries before any later task consumes them.
- **Residual risk and next owner**: source inventories are intentionally
  incomplete topical analysis. WGIA-002 through WGIA-009 own audit/review;
  WGIA-012 alone owns Current cutover.

### WGIA-002 Focused Evidence

- **Scope and changed paths**: the purpose/governance report, the
  `REQ-WGA-001`, `REQ-WGA-002`, and `REQ-WGA-012` pack cells, one provisional
  roadmap row, this Task, one top durable progress entry, and ignored worker
  state. The disposition ledger has no WGIA-002 candidate because no reviewed
  artifact met the Legacy/Deprecated/one-shot threshold.
- **Acceptance IDs**: VAL-WGA-002 and VAL-WGA-003 at repository-static depth.
- **Pinned-source identity**: active governance owners are identical between
  observation commit `50628b84165479b03efc0a25be075a49c91a9aef` and the
  WGIA-002 starting HEAD; only the durable progress ledger differs under Stage
  00 because WGIA-001 recorded its completed evidence.
- **Contradiction probe**: the pre-edit Node probe exited 1 with
  `WGIA-GOV-ROOT-ROUTING FAIL` and exact findings
  `THIN_GATEWAY_AS_CANONICAL_OWNER,GEMINI_NATIVE_SURFACE_OMITTED`. The root
  canonical-owner list names thin `AGENTS.md` rather than the Stage 00 policy
  SSoT, while the top-level area summary omits `.gemini/` and blurs the
  `.agents/` local/shared boundary.
- **No-conflict proof**: the corrected deterministic probe returned
  `WGIA-GOV-NO-CONFLICT PASS explicit_jit=7/7 delegated_jit=1/1 roles=12
  surfaces=4 adapters=48`. Purpose, canonical JIT order, approval owner,
  completion owner, machine role owner, and readable role view therefore have
  no separately identified repository-static conflict.
- **Findings and candidate**: `WGA-GOV-001` is `Aligned` at
  `repository-static`; `WGA-GOV-002` and `WGA-GOV-003` are `Conflict`;
  `WGA-GOV-004` is `DEFER` at `provider-runtime`. `WGA-RMP-GOV-001` combines
  only the two root README corrections as a provisional WGIA-009 input; it is
  not implementation approval.
- **Focused validation**: `python3 scripts/validate-agent-governance-closure.py
  --root .` passed; harness contract passed at 12/4/48 with four evidence and
  four memory classes; harness semantics passed at 12 roles/48 adapters/eight
  categories; roster currentness passed; strict document registry passed at
  502 paths with zero uncovered/ambiguous; strict Markdown profiles reported
  zero violations; strict links/owners returned `PASS CROSS-DOCUMENT`; `git
  diff --check` passed; the Stage 98 path diff is empty.
- **Lanes and limitations**: targeted repository-static, affected/staged, and
  complete `bash scripts/validate-repo-quality-gates.sh .` checks `PASS` with
  final exit 0. Formatter-review and rerun are `SKIP` because no formatter
  ran. Hosted CI, provider-runtime, authenticated, credential-bearing, remote,
  and live lanes remain `DEFER`; no secret or runtime state was accessed.
- **Review, rollback, and next owner**: specification and quality reviews are
  `Approved` with no Critical or Important finding; quality review also
  resolved 43 unique cited `path#selector` values in the pinned/current trees
  with zero invalid. Rollback is limited to the WGIA-002 report/cell/roadmap/
  Task/progress edits. WGIA-009 owns candidate admission, WGIA-010 owns any
  accepted root README correction, and WGIA-014 owns whole-branch review.

### WGIA-003 Focused Evidence

- **Scope and changed paths**: the SDLC/documentation report, the
  `REQ-WGA-005`, `REQ-WGA-016`, `REQ-WGA-018`, `REQ-WGA-019`, and
  `REQ-WGA-023` pack cells, two provisional roadmap rows, this Task, one top
  durable progress entry, and ignored worker state. No disposition-ledger row
  was added because WGIA-003 found no exact Legacy, Deprecated, or one-shot
  candidate.
- **Acceptance IDs**: VAL-WGA-002 and VAL-WGA-004 at repository-static depth.
- **Pinned-source identity**: Stage 01-05 and Stage 99 document-contract owners
  are identical between observation commit
  `50628b84165479b03efc0a25be075a49c91a9aef` and the WGIA-003 starting HEAD
  `a59177cab0229868052f687532e175022c08d652`; only the active Plan and Task
  differ in the bounded owner surface due prior WGIA work.
- **RED and no-conflict proof**: the pre-edit Release probe exited 1 with
  `WGIA-DOC-RELEASE FAIL profile_route=0 template=0 lifecycle=0
  role_validator=0`; this proves the broad contract absence but does not reopen
  approved DOC-G5's narrower negative release-notes decision. The existing-family proof returned
  `WGIA-DOC-EXISTING PASS families=11/11 templates=11/11 lifecycles=11/11
  readme_profiles=6 guides=8`.
- **Findings and candidates**: `WGA-DOC-001` is `Aligned`, `WGA-DOC-002` is a
  broad-versus-narrow semantic `Gap`, and `WGA-DOC-003` plus `WGA-DOC-004` are
  `Partial`, all at `repository-static` depth. `WGA-RMP-DOC-001` integrates the
  broad Release mapping with approved DOC-G5; `WGA-RMP-DOC-002` routes Guide
  Type enforcement to existing WORK-013. Both remain `Provisional` WGIA-009
  dedupe inputs, not new taxonomy decisions or implementation approval.
- **Focused validation**:
  `python3 scripts/validate-document-contract-registry.py --root . --self-test`
  passed 132 cases, 64 profiles, 30 templates, and template/source parity
  11/11; strict mode passed 502 paths with zero uncovered/ambiguous.
  `python3 scripts/validate-markdown-profiles.py --root . --self-test` passed
  including native surfaces 10/10; strict mode reported zero violations.
  `python3 scripts/validate-document-lifecycle.py --root . --self-test` passed
  696 cases; snapshot mode returned the expected `DEFER` because it has no
  comparison base. Strict links/owners returned `PASS CROSS-DOCUMENT`; `git
  diff --check` passed; and `git diff --name-only HEAD -- docs/98.archive`
  returned empty. The report-local contract/selector probe passed four findings
  with 14 conceptual fields each, 49 evidence references, 28 unique references,
  and 21 unique pinned paths with zero missing or invalid selectors. The first
  probe implementation over-escaped heading whitespace; after that was fixed,
  it correctly exposed the stale JSON selector `#mutations`, which was changed
  to the exact existing `#cases` key before final PASS. The complete repository
  quality gate then passed against the exact staged five-file scope.
- **Deeper evidence and limitations**: integration-guide live usability,
  hosted CI, provider runtime, authenticated, credential-bearing, remote, and
  live lanes remain `DEFER`; no secret, remote, runtime, or live state was
  accessed.
- **Quality-review fix**: the first quality review found two Important owner/
  dependency errors. The fix recognizes active approved Spec 052 DOC-G1/DOC-G5,
  the WDTC Plan's exact registry/template/all-eight-guide/deliberate-absence
  work, and queued Task WORK-013. Both roadmap rows now deduplicate and route to
  that program instead of seeking fresh decisions.
- **Review, rollback, and next owner**: specification review and the fix-round
  quality re-review are `Approved`; the two first-round Important findings are
  resolved with no remaining Critical or Important finding. Rollback is
  limited to WGIA-003 report/cell/roadmap/Task/progress/Plan edits. WGIA-009
  owns candidate deduplication/admission, the WDTC program owns WORK-013
  implementation, and WGIA-014 owns whole-branch review.

### WGIA-004 Focused Evidence

- **Scope and changed paths**: the CI/QA report, eight relevant request cells,
  this Task, one top durable progress entry, and ignored worker progress/report.
  The roadmap and disposition ledger have no WGIA-004 row because the dormant
  formatter and evidence-depth boundaries already have accurate current owners.
- **Acceptance IDs**: VAL-WGA-002 and VAL-WGA-005 at repository-static depth.
- **Pinned/current identity**: workflow, pre-commit, affected-surface,
  quality-standard, CI lock, and focused validator owners are identical between
  observation commit `50628b84165479b03efc0a25be075a49c91a9aef` and starting
  HEAD `f2b9c2b9450431a253b328c48d5ba174cdb3ba86`.
- **Workflow inventory**: deterministic proof returned `workflows=5 jobs=11
  uses=15 full_sha=15 unique_actions=7 concurrency=5
  root_read_permissions=5`. The matrix records all triggers, jobs, Actions,
  pins, permissions, concurrency, selection, and artifact boundaries.
- **Dormant-control proof**: deterministic proof returned `config=2
  routed_inputs=2 consumers=0 owner_claim=1 red_required=0`. The current
  quality owner already forbids reporting Prettier coverage, so no contradictory
  claim, manufactured RED, or TDD-workflow invocation exists.
- **Findings**: `WGA-QA-001` and `WGA-QA-002` are `Aligned`;
  `WGA-QA-003` is `DEFER`; `WGA-QA-004` is `Partial`, all at strongest observed
  `repository-static` depth. Hosted/provider/remote/live evidence remains
  explicitly separate.
- **Focused workflow/contract results**: Actions security self-test and
  production `PASS`; CI Python contract self-test passed 13 rules/33 cases and
  production passed four jobs/three pins; affected-surface self-test passed 22
  surfaces, 38 mutations, and all selection/range cases; production passed 858
  paths, 22/22 surfaces, 22 validators, four CI jobs, zero uncovered/ambiguous.
  Agent-governance CI self-test passed six truth/45 mutation cases and production
  passed 12 route classes, 18 delegated checks, six truth rows, one deferred
  owner, and ten QA surfaces. The two relevant workflow modules passed 110 tests.
- **Finding and document checks**: the pinned finding/source-selector probe
  passed four findings with 14 conceptual fields each, 49 references, 32 unique
  references, and 21 unique paths with zero missing/invalid. Strict Markdown
  profiles returned zero violations; strict links/owners returned `PASS
  CROSS-DOCUMENT`; `git diff --check` passed; and the Stage 98 path diff is
  empty.
- **Ordered lane results**: targeted `PASS`; direct tests `PASS`; affected,
  staged, all-files, message/manual, and hosted CI `DEFER` to the controlling
  completion owner because WGIA-004 neither stages nor runs the prohibited full
  aggregate/pre-commit lanes; formatter-review and rerun `SKIP` because no
  formatter ran; diff checks `PASS`; provider-runtime, remote, credential, and
  live lanes `DEFER`. The complete repository quality gate passed against the
  exact staged four-file scope.
- **Review, rollback, and next owner**: specification/content and quality
  reviews are `Approved` with no Critical or Important finding. Rollback is
  limited to the WGIA-004 report/cells/Task/progress/Plan edits. WGIA-009 may
  integrate the reviewed no-remediation result; WGIA-014 owns whole-branch
  completion evidence.

### WGIA-005 Focused Evidence

- **Scope and changed paths**: the harness/loop report, five relevant request
  cells, one provisional roadmap row, this Task, one top durable progress
  entry, and ignored worker progress/report. No disposition-ledger row was
  added because neither omitted helper is Legacy, Deprecated, one-shot, or a
  deletion candidate.
- **Acceptance IDs**: VAL-WGA-002 and VAL-WGA-006 at repository-static depth.
- **Pinned/current identity**: harness, loop, checkpoint, memory, provider,
  script, and fixture owners are identical between observation commit
  `50628b84165479b03efc0a25be075a49c91a9aef` and starting HEAD
  `fd68251715bf2631fc50c7c603000a525539a901`. Relevant current drift is limited
  to prior WGIA-001 document-registry/profile work.
- **Inventory and findings**: the corrected deterministic observation probe is
  `WGIA-HAR-SCRIPT-INVENTORY RED scripts=47 cli=41 helpers=6
  human_inventory_missing=2`; it prints all six helper paths and the exact
  missing `scripts/archive_cutover_manifest.py` and
  `scripts/reference_information_architecture.py` paths. Fixture proof remains
  37 files (31 JSON and six YAML) across six production-owner families.
  `WGA-HAR-001` and `WGA-HAR-002` are `Aligned`, `WGA-HAR-003` is `Partial`,
  and `WGA-HAR-004` is `DEFER`, all at strongest observed
  `repository-static` depth. `WGA-RMP-HAR-001` is a provisional bounded human-
  index repair, not implementation approval; the complete blocker object
  limits only provider-runtime evidence promotion.
- **Harness/loop/checkpoint results**: harness contract self-test passed 37
  cases and production passed exact 12/4/48, four evidence classes, four memory
  classes, and 14 consumers. Harness semantics self-test passed 768 cases plus
  33 adversarial probes and production passed 12 roles/48 adapters/eight
  categories. Loop self-test passed 66 cases and production passed eight
  states, nine transitions, two same-signature retries, three recovery actions,
  two-result no-progress stop, six non-retryable conditions, five progress
  classes, and six interfaces. Checkpoint self-test passed 110 mutations and
  production passed four memory classes, two completed/two remaining items,
  and two validation records.
- **Roster/provider results**: roster-currentness self-test and production both
  passed. Provider config self-test passed 13 cases and production passed four
  providers, ten sources, eight models, and seven MCP entries. Canary self-test
  passed eight cases and production passed 12 records/four providers. Provider
  evidence aggregate passed both self-test and production modes with two
  focused validators. The first roster invocation used unsupported `--root`
  and exited 2; corrected positional-root commands passed. This was a command
  syntax limitation, not a product-contract failure.
- **Focused tests and document checks**: the harness-contract,
  lifecycle, checkpoint, provider-config, and provider-canary modules passed
  119 tests in the fix-round rerun. The finding probe passes four complete
  findings, 64 exact observation paths with zero missing, and 29 JSON/Python
  selectors with zero invalid. Strict registry reports 502 paths with zero uncovered/ambiguous;
  full and report-local strict Markdown profiles report zero violations;
  strict links exits 0; `git diff --check` passes; both HEAD-worktree and
  observation-to-HEAD Stage 98 path diffs are empty. The exact tracked dirty
  scope is the WGIA-005 report, five request cells, one provisional roadmap
  row, Task, and progress ledger. The complete repository quality gate passed
  against the exact staged five-file scope. Initial
  `--strict` profile/link invocations exited 2 because the validators require
  `--mode strict`; corrected commands passed.
- **Lanes and limitations**: targeted repository-static checks `PASS` so far;
  staged, all-files, aggregate/full, hosted CI, provider-runtime,
  authenticated, credential-bearing, remote, ignored-checkpoint, and live
  lanes remain `DEFER`. No secret, runtime state, or ignored checkpoint was
  accessed.
- **Quality-review fix**: quality review found one Important count and coverage
  overclaim: two import-only helpers had been counted as CLI, and two tracked
  helpers were absent from the claimed complete canonical human inventory. The
  fix records exact 47 = 41 + 6, changes `WGA-HAR-003`/`REQ-WGA-017` to
  `Partial`, preserves separately supported fixture alignment, and routes one
  provisional bounded repair to WGIA-009. The same quality re-review is
  Approved with no remaining Critical or Important finding.
- **Review, rollback, and next owner**: specification/content and fix-round
  quality reviews are `Approved`. Rollback is limited to the WGIA-005 report/cells/Task/
  progress/provisional-roadmap/ignored-worker edits. WGIA-014 owns whole-branch
  completion evidence.

### WGIA-006 Focused Evidence

- **Scope and changed paths**: the knowledge/memory report, `REQ-WGA-022` and
  `REQ-WGA-027` cells, one provisional roadmap row, this Task, one top durable
  progress entry, and ignored worker progress/report. No disposition-ledger row
  was added because no Legacy, Deprecated, one-shot, or deletion candidate was
  found. The generated index, generator, canonical memory owners, Stage 98,
  Current, and RIA remain unchanged.
- **Acceptance IDs**: VAL-WGA-002 and VAL-WGA-007 at repository-static depth.
- **Pinned/current identity**: LLM-WIKI, generator/output, memory, harness,
  lifecycle, checkpoint, and closure owners are identical between observation
  commit `50628b84165479b03efc0a25be075a49c91a9aef` and starting HEAD
  `d56f2c3429065e9c4642028f905dfcf2a9f748a7`; relevant current drift is prior
  WGIA progress and document-contract fixture documentation only.
- **RED and findings**: deterministic proof returns `WGIA-KNW-FRESHNESS RED
  declared_inputs=6 changed_after_review=6 review_date=2026-05-10` with exact
  path/date/commit rows and latest input date 2026-08-02. `WGA-KNW-001` and
  `WGA-KNW-003` are `Aligned`, `WGA-KNW-002` is a freshness `Gap`, and `WGA-KNW-004` is
  `DEFER`, all at strongest observed `repository-static` depth.
  `WGA-RMP-KNW-001` is a provisional bounded source-review/metadata repair,
  not implementation approval or generated-output hand-edit authority.
- **Historical generator and current memory validation**: the former LLM Wiki
  generated-index check reported current bytes at execution time; that generator
  and output are now retired. Harness contract self-test passes 37 cases and
  production passes 12/4/48,
  four evidence classes, four memory classes, and 14 consumers. Loop self-test
  passes 66 cases and production passes eight states/nine transitions/two
  signature retries/three recovery actions/two-result no-progress stop/six
  non-retryable conditions/five progress classes/six interfaces. Checkpoint
  self-test passes 110 mutations and production passes four memory classes.
  Governance closure self-test and production both pass.
- **Focused tests and document checks**: harness, loop, checkpoint, closure,
  and three RIA generator-relation tests pass 115 tests. The report probe passes
  four complete findings, 28 exact observation paths with zero missing, and 14
  JSON/Python/shell selectors with zero invalid. Strict registry reports 502
  paths with zero uncovered/ambiguous; full and report-local strict Markdown
  profiles report zero violations; strict links exits 0; `git diff --check`
  passes; HEAD-worktree and observation-to-HEAD Stage 98 diffs are empty. The
  generated index/generator, memory contracts/README, and RIA dirty diff is
  empty; exact tracked dirty scope is report, two request cells, roadmap, Task,
  and durable progress. The initial freshness probe command had unmatched
  shell quoting and exited 1; the corrected bounded Python command produced the
  exact RED above. The complete repository quality gate passed against the
  exact staged five-file scope.
- **Lanes and limitations**: targeted repository-static checks `PASS` so far;
  staged, all-files, aggregate/full, hosted CI, provider-runtime,
  authenticated, credential-bearing, private-memory, ignored-checkpoint,
  remote/retrieval, and live lanes remain `DEFER`. No secret, runtime/private
  memory, ignored checkpoint, provider, remote, or live state was accessed.
- **Review, rollback, and next owner**: specification/content and quality
  reviews are `Approved`. Rollback is limited to the WGIA-006 report/cells/
  roadmap/Task/progress/ignored-worker edits. WGIA-009 owns candidate admission,
  WGIA-010 only an accepted knowledge-owner correction, and WGIA-014 terminal
  whole-branch completion evidence.

### WGIA-007 Focused Evidence

- **Scope and changed paths**: the AI-agent report, `REQ-WGA-028` through
  `REQ-WGA-030` cells, this Task, one top durable progress entry, and ignored
  worker progress/report. No roadmap or disposition-ledger row was added
  because no repair, duplication, Legacy, Deprecated, one-shot, or deletion
  candidate was proven. Harness/model/admission/evaluation/provider contracts,
  adapters, other reports, Stage 98, Current, and RIA remain unchanged.
- **Acceptance IDs**: VAL-WGA-002 and VAL-WGA-008 at repository-static depth.
- **Pinned/current identity**: the reviewed harness, roster, evaluation, model,
  provider-evidence, protocol, catalog, and four adapter families are identical
  between observation commit
  `50628b84165479b03efc0a25be075a49c91a9aef` and starting HEAD
  `e4ed34d56f7b90a12771232c7bfe54d5c4d6f94e`.
- **Inventory and findings**: machine owners select exactly 12 current roles,
  four current surfaces, and 48 current projections. `WGA-AGT-001` and
  `WGA-AGT-002` are `Aligned`; `WGA-AGT-003` is `Partial`; `WGA-AGT-004` is
  `DEFER`. Every role row records responsibility, inputs, outputs, prohibited
  actions, stop conditions, downstream handoff, four exact adapters, exact
  permission class, exact required evidence, model rule, evaluation/admission
  state, and boundary. The integrated-supervisor
  matrix separately covers delegation, isolation, checkpoint, escalation, and
  completion. `BLK-WGA-AGT-001` is a complete provider-runtime evidence limit,
  not a blocker to the static audit.
- **Focused contract validation**: harness contract self-test passes 37 cases
  and production passes 12/4/48; semantics self-test passes 768 cases and
  production passes 12 roles/48 adapters; roster currentness self-test and
  production pass; roster admission self-test passes 59 cases and production
  preserves two projected candidates, seven conditions, current/target 12/4/48,
  four evaluation classes, and nine deferred evidence classes. Evaluation
  self-test passes 60 cases and production passes 12 roles/48 corpus records/12
  adjudication records. Model fitness self-test passes 33 cases and production
  proves 48 tuples, 21 mapping-ready, 27 mapping-deferred, and 48 each fitness,
  threshold, promotion, canary, and runtime `DEFER`. Provider config,
  aggregate evidence, and canary self-tests/production pass for four providers,
  ten sources, eight models, seven MCP declarations, and 12 canary records.
- **Focused tests and document checks**: six harness/roster/evaluation/model/
  provider modules pass 150 tests. The quality-fix equality probe compares the
  observation contract with 12 expected/12 actual matrix roles and reports zero
  malformed, missing, unknown, permission-class, or required-evidence mismatch.
  The final report probe passes four findings, 14 conceptual fields, 12 role
  rows, 30 exact observation references, and zero missing fields/paths/invalid
  selectors. Strict registry reports 502 paths
  with zero uncovered/ambiguous; strict Markdown reports zero violations;
  strict links exits 0; `git diff --check`, protected-owner worktree identity,
  observation-to-HEAD owner identity, and both Stage 98 checks pass.
- **Lanes and limitations**: targeted repository-static checks and the complete
  staged repository quality gate `PASS`; provider-runtime, authenticated, hosted CI,
  evaluation execution/adjudication, remote, and live lanes remain `DEFER`.
  No dispatch, runtime/auth/secret/remote/live action or provider state access
  occurred.
- **Review, rollback, and next owner**: specification/content and fix-round
  quality reviews are `Approved`; the first quality review's one Important
  missing-field finding is fixed with exact 12-role equality. The complete
  repository quality gate passes against the staged WGIA-007 scope. Rollback
  is limited to the WGIA-007 Plan/report/cells/Task/progress/ignored-worker
  edits. No agent-owner correction or roadmap candidate was accepted;
  WGIA-014 owns whole-branch completion evidence.

### WGIA-008 Focused Evidence

- **Scope and changed paths**: the security report, `REQ-WGA-024` cell, six
  provisional WGIA-009 roadmap rows, this Task, one top durable progress entry,
  and ignored worker progress/report. No disposition-ledger row is warranted:
  none of the reviewed security owners is proven Legacy, Deprecated, one-shot,
  or deletion-ready. Canonical policy/config/manifest/script/test owners, other
  reports, Stage 98, Current, and RIA remain unchanged.
- **Acceptance IDs**: VAL-WGA-002 and VAL-WGA-009 at `repository-static`
  depth. Evidence is pinned to observation commit
  `50628b84165479b03efc0a25be075a49c91a9aef`; current matching security owners
  were reviewed separately from later implementation drift.
- **Control inventory and findings**: the report maps repository/workflow,
  supply-chain, agent, secret, GitOps/infrastructure, permission, destructive,
  remote, and live boundaries to their owner, threat, enforcement point,
  evidence, bypass/exception, failure mode, approval authority, depth, and
  result. Nine complete findings record two `Aligned`, two `Partial`, three
  `Gap`, one `Conflict`, and one `DEFER` result. Two blockers preserve the
  provider/hosted/live evidence limit and the untriaged redacted history scan.
- **Deterministic probes**: repository-static inventory finds nine Namespace
  objects, six egress-oriented NetworkPolicies, zero ingress/default-deny
  policy, four namespaces without a policy object, five RBAC objects with no
  wildcard rule, three raw pod templates, zero `latest` images, zero
  digest-pinned images, and zero tracked raw Secret kinds. Kube-state-metrics
  has exact cluster-wide Secret `list`/`watch` access and a mounted
  service-account token. Adminer lacks the hardening visible on the other two
  raw pod templates. Tracked PSA/admission-policy ownership is absent.
- **Secret-scanning RED and limitation**: the bounded secret-handling check
  passes 100 selected files. Redacted Gitleaks current-worktree probing exits 1
  with four candidates (two tracked documents and two ignored compiled-test
  artifacts); redacted history probing exits 1 with eleven candidates across
  1,136 commits. Match/secret payloads were neither inspected nor recorded.
  `BLK-WGA-SEC-002` therefore blocks any clean-history claim until approved
  non-disclosing triage, rotation if necessary, and exact false-positive
  classification complete.
- **Focused static validation**: Actions security and CI-Python contract
  self-tests/production pass; Vault/ESO and GitOps-change self-tests/production
  pass; secret handling, GitOps structure, static infrastructure contracts, and
  104-manifest validation pass. Policy validation passes through the built-in
  fallback while optional Conftest is `SKIP`; KubeLinter is available and
  reports no lint errors under the repository's documented exclusions. The
  final report probe passes nine findings, 14 conceptual fields each, the exact
  2/2/3/1/1 closed-verdict distribution, six candidate rows, and 42 unique
  observation evidence paths with zero missing. Strict registry passes 502
  paths; Markdown profiles report zero violations; strict links are valid;
  diff and both Stage 98 checks pass. The first strict-document invocation used
  unsupported `--strict` and exited 2 at argument parsing; the corrected
  `--mode strict` commands pass.
- **Lanes and limitations**: repository-static validation is evidence, not live
  enforcement. Hosted branch/ruleset, provider-native permission consumption,
  credentials, registry identity, cluster admission/RBAC/CNI, GitOps
  reconciliation, Vault/ESO delivery, destructive action, remote mutation, and
  live workload behavior remain `DEFER`. No secret value, provider/runtime,
  remote, cluster, or live state was accessed.
- **Review, rollback, and next owner**: fresh independent specification/content
  and security fix-round reviews are `Approved` with no Critical/Important
  finding. Rollback is limited to the
  WGIA-008 report/cell/roadmap/Task/progress/ignored-worker edits. WGIA-009 owns
  deduplication/admission; WGIA-011 may implement only accepted security rows;
  WGIA-014 owns whole-branch completion evidence.

### WGIA-009 Focused Evidence

- **Scope and changed paths**: the disposition ledger, integrated roadmap,
  `REQ-WGA-025`/`REQ-WGA-026` final verdict cells and report-index summaries,
  this Task, one top durable progress entry, and ignored worker progress/report.
  No source report finding, canonical implementation owner, Current/RIA owner,
  historical audit body, Stage 98 path, provider/remote/live surface, or secret
  value changed.
- **Acceptance IDs**: VAL-WGA-010 and VAL-WGA-012 at `repository-static`
  depth. Candidate evidence is pinned to observation commit
  `50628b84165479b03efc0a25be075a49c91a9aef` and compared with starting HEAD
  `5db8fa365d1953861e80f1031003b08f69b132fd`.
- **Candidate inventory**: observation has six exact legacy-name paths and the
  starting HEAD has those six plus the dated ledger. All seven are active or
  durable evidence owners with exact consumers and are rejected as name-only
  noncandidates. The approved Spec 052 `WORK-001` globs identify exactly
  fifteen one-shot data/script/test paths. Each has its observation-state full
  last-change commit, exact current consumers, surviving owner, history route,
  focused/aggregate gates, and decision `Integrate`; live consumers keep
  `Delete=0`.
- **Rejected name-only evidence**: the exact current tracked probe
  `git grep -n -I -E '(legacy|Legacy|deprecated|Deprecated|one[- ]shot|one_shot|duplicate|Duplicate)' -- ':!docs/98.archive/**' ':!docs/90.references/audits/**' ':!docs/00.agent-governance/memory/progress.md'`
  reports 2,355 matching lines at starting HEAD; the authored worktree reports
  2,360 because this Task contributes five matched evidence lines. Both counts
  are triage only, not candidate or deletion proof. Five machine-declared
  retired agent surfaces are already
  absent with five replacements and zero active consumers; absent paths are not
  new tracked candidates. Six prior audit packs and Stage 98 remain protected.
- **Integrated remediation**: one contiguous 12-row table represents each
  reviewed topical input once. `WGA-RMP-GOV-001` and `WGA-RMP-KNW-001` are
  admitted `Correct` inputs to WGIA-010; `WGA-RMP-HAR-001` and
  `WGA-RMP-SEC-CLAUDE-001` are admitted `Correct` inputs to WGIA-011; the two
  DOC rows `Integrate` with existing Spec 052 WORK-013 without duplicate
  implementation; `WGA-RMP-DSP-001` integrates the fifteen one-shot paths with
  existing Spec 052 WORK-001 without authorizing deletion. SCAN is hard
  `DEFER` for credential/security triage; KSM, NET, ADM, and SC remain `DEFER`
  for architecture/owner/live evidence.
- **Validation results and boundary**: the ledger records focused and aggregate
  post-delete commands for every row, but no post-delete gate was run or claimed
  because no `Delete` row exists. The fix-round structural target is one
  seven-row rejected-name table, one contiguous fifteen-row/12-column ledger,
  and one contiguous 12-row/14-column roadmap (`Integrate=15`, `Delete=0`,
  admitted=7, `DEFER=5`, two 14-field findings); the corrected parser and all
  15 observation last-change hashes pass. Other PASS evidence:
  legacy-cutover self-test and production (five retired, five replacements,
  zero active consumers); active-corpus role self-test/production; migration
  self-test; RIA self-test; 22 archive unit tests and archive production (43
  records, 362 historical links, 43 secret-clean records); strict registry
  (502 paths, zero uncovered/ambiguous), Markdown profiles (zero violations),
  strict links, diff, and observation/worktree Stage 98 identity. RED:
  initial unstaged active-corpus migration production reported path-only
  `MIGRATION-SECRET-CLASSIFIER` for the protected historical
  `docs/98.archive/04.execution/plans/2026-07-12-affected-surface-agent-qa.md`;
  no payload was inspected and no archive edit was authorized. Initial RIA
  production also rejected dirty/unsettled comparison input. After exact
  staging, the complete repository quality gate passed, including active-corpus
  migration production and RIA self-test/production; `BLK-WGA-DSP-001` and
  `BLK-WGA-DSP-002` are resolved. The same exact staged state runs 150 focused
  active-corpus tests with 149 PASS and one eligibility count mismatch
  (expected 53, actual 57); `BLK-WGA-DSP-003` remains open.
- **Specification review fix round 1**: the reviewer found a four-cell
  delimiter beneath the three-cell Candidate Discovery header. The delimiter
  is now exactly three cells. The first width-aware parser run also exposed the
  same delimiter-only defect under the 12-cell Candidate Disposition Ledger
  header (13 cells); that delimiter is now exactly 12 cells. The parser covers
  every table changed by WGIA-009.
- **Fresh-review fix round 2**: content and quality reviewers found incomplete
  live-consumer coverage, invalid JSON pointers/test anchors, two prose-only
  self references, and a stale two-versus-three blocker count. The corrected
  ledger explicitly separates live consumers from dated decision/history
  evidence and resolves 114 consumer path/selectors with zero missing/invalid
  results across all fifteen rows. `git diff --check`, strict registry, and
  Markdown profiles pass after the fix. Both fix-round re-reviews are Approved.
- **Review, rollback, and next owner**: independent content and quality reviews
  are Approved. Rollback is limited to the WGIA-009 ledger/roadmap/
  README/Task/progress/ignored-worker edits. WGIA-010/011 may implement only
  admitted rows; WORK-013 and WORK-001 retain their existing integration
  authority; WGIA-012 owns Current cutover; WGIA-013 applies only the
  then-current reviewed WGIA disposition; WGIA-014 owns terminal QA.

### WGIA-010 Focused Evidence

- **Scope**: root `README.md`; LLM-WIKI README, generator, and producer-owned
  `wiki-index.md`; WGA-GOV-002/003 and WGA-KNW-002 re-audit state; DOC-001/002
  integration/no-delta evidence; affected pack/roadmap cells; this Task, Plan,
  durable progress, and ignored worker report. No Stage 99 registry/template,
  Spec 052, guide, RIA owner, Current pointer, Stage 98, provider, remote, live,
  or secret surface changed.
- **RED**: the pre-edit probe exited 1 with
  `ROOT_STAGE00_OWNER_MISSING ROOT_THIN_GATEWAY_PROMOTED
  ROOT_SURFACE_MISSING:.gemini/ LLM_SOURCE_REVIEW_STALE
  LLM_FRESHNESS_REVIEW_STALE` plus stale generator `updated`, source, and review
  metadata. The existing generator byte check still passed, proving byte
  equality alone did not establish source-trigger review freshness.
- **GREEN**: the corrected probe reports
  `root_owner=stage00 thin_gateway=true surfaces=4/4 llm_inputs=6/6
  source_checked=2026-08-09 last_reviewed=2026-08-09`. The first GREEN probe's
  prefix-count assertion omitted `scripts/README.md`; the corrected assertion
  compares the exact six-path set and required no production change.
- **Canonical remediation**: `README.md#canonical-owners` routes to the Stage 00
  hub, while `README.md#top-level-areas` distinguishes `.agents/`, `.claude/`,
  `.codex/`, and `.gemini/` without promoting provider-runtime consumption.
  The LLM-WIKI README records each of the six RIA-declared input identities;
  the generator emits 2026-08-09 source/review metadata and alone regenerated
  `docs/90.references/llm-wiki/wiki-index.md`.
- **Documentation integration/no delta**: WGA-DOC-002/003 and roadmap DOC-001/
  DOC-002 now record integration with existing approved Spec 052/queued
  WORK-013. WGIA-010 changed no document profile, schema, template, Guide,
  Spec 052, or WDTC execution owner and did not reopen DOC-G1/DOC-G5.
- **Validation and review**: producer generation and `--check`; three focused
  RIA generator-relation tests; governance closure self-test/production; RIA
  self-test; strict registry (502 paths, zero uncovered/ambiguous), Markdown
  profiles (zero violations), links, archive cutover (43 records, 362
  historical links, 43 secret-clean records), DOC/WORK-013 no-delta, RIA owner-
  family no-delta, diff, and both Stage 98 boundaries pass. Normal RIA
  production is a bounded dirty-worktree RED: required progress and the three
  changed generator-relation paths are unavailable for duplicate/index
  comparison. No RIA owner changed; staged/settled RIA evidence remains for
  primary/terminal validation. The first parallel archive invocation yielded a
  session without final output; polling the recovered session `33794` returned
  PASS. Fresh specification/content and quality reviews are Approved. The exact
  staged complete repository quality gate then passed, including RIA,
  active-corpus, harness/provider, document, archive, and cross-document lanes.
- **Content review fix round**: the reviewer found one Important contradiction:
  the report's Freshness Proof still described the 2026-05-10 RED baseline in
  present tense and called the already admitted/implemented roadmap row
  provisional. The section now labels the observation/pre-remediation state
  explicitly, records the 2026-08-09 current GREEN state, and names
  `WGA-RMP-KNW-001` as admitted by WGIA-009 and implemented by WGIA-010.
  Report-local profile/link checks and `git diff --check` were rerun; the fresh
  specification/content re-review and the separate quality review are
  Approved.
- **Rollback and next owner**: revert only the root README unit or the
  LLM-WIKI README/generator/generated-output unit. WORK-013 retains DOC
  execution; WGIA-014 owns terminal QA and deeper provider/live evidence stays
  `DEFER`.

### WGIA-011 Focused Evidence

- **Scope**: admitted rows `WGA-RMP-HAR-001` and
  `WGA-RMP-SEC-CLAUDE-001` only. The script owner family is
  `scripts/README.md` plus the existing aggregate inventory projection; the
  provider owner family is `.claude/settings.json`, its focused validator, and
  existing focused regression module. Affected audit reports, roadmap/index,
  Plan/Task, durable progress, and ignored worker evidence record the result.
  No workflow, CI topology, agent role/model, shared approval policy, Stage 98,
  Current/RIA, secret payload, provider process, remote, or live surface changed.
- **RED**: the deterministic script probe exited 1 with
  `total=47 cli=41 helpers=6` and exactly two missing names:
  `archive_cutover_manifest.py,reference_information_architecture.py`. The
  tracked Claude probe exited 1 with seven broad allows (`ls`, `grep`, `cat`,
  `git`, and kubectl get/describe/logs) plus missing Vault/Kubernetes secret-
  read and ordinary Git/GitHub remote-mutation stops. The first focused test
  failed because the required closed Claude permission contract did not yet
  exist (`AttributeError: CLAUDE_ALLOWED_PERMISSIONS`).
- **Script GREEN**: `scripts/README.md` names both omitted helpers and records
  the exact 47 tracked scripts = 41 CLI entrypoints + six import-only helpers.
  The existing aggregate now derives the tracked set and accepts only the exact
  top-level AST main guard `__name__ == "__main__"`; embedded probes reject a
  wrong left operand, `NotEq`, and chained comparison. It rejects count/helper-
  set drift and requires all 47 names plus the exact summary. The same
  deterministic probe reports zero missing names; shell syntax and the
  extracted embedded aggregate contract pass. No script behavior, caller,
  entrypoint, import, or fixture changed.
- **Claude GREEN**: the tracked allow list is closed to exact repository-static
  validator and metadata-only Git commands, with literal `.` roots, generator
  `--check`, and no wildcard or caller-selected suffix. Broad shell reads, broad Git,
  kubectl reads, raw Helm, and k3d runtime listing are no longer pre-allowed.
  Explicit deny rules cover `.env` reads, environment dumps, Vault reads,
  Kubernetes Secret reads, ordinary push/merge, and GitHub PR/release/workflow
  mutation. The validator reads `.claude/settings.json` through its existing
  descriptor-safe JSON boundary, enforces unique string lists, the exact allow
  set, and the exact complete 62-entry deny tuple. The aggregate delegates all
  Claude permission semantics to that focused owner and retains only unrelated
  Claude hook-wiring checks.
- **Focused validation**: the provider-config regression module passes 32
  tests, including every forbidden broad allow, wildcard mutation, alternate-
  root mutation, and removal of each of the 62 required denies;
  provider-config self-test reports 13 fixture mutations and production reports
  four providers, ten sources, eight model candidates, and seven MCP servers.
  Harness contract reports 12/4/48, harness semantics reports 12 roles/48
  adapters/eight categories, roster currentness passes, Python compile/shell
  syntax pass, and the embedded aggregate contract reports repository quality
  PASS. Strict registry passes 502 paths with zero uncovered/ambiguous,
  Markdown profiles report zero violations, strict links report `PASS
  CROSS-DOCUMENT`, diff check passes, and both HEAD/observation Stage 98 diffs
  are empty.
- **Evidence boundary and review**: this is repository-static configuration
  and test evidence only. Native Claude loading, permission precedence,
  interactive prompting, effective enforcement, provider discovery,
  authenticated execution, hosted CI, remote state, credentials, and live
  cluster behavior remain `DEFER`. Fresh specification/content, Python/quality,
  and security reviews are `Approved`; the exact staged complete repository
  quality gate passes, including harness/provider and RIA lanes.
- **Logical split and rollback**: commit the script-inventory owner family as
  `fix: complete script inventory`, then the Claude owner family as
  `fix: narrow Claude approval boundaries`; lifecycle evidence may accompany
  the second reviewed unit. Revert either family independently without changing
  production script semantics or the shared Stage 00 policy.

### WGIA-012 Focused Evidence

- **Scope and acceptance**: VAL-WGA-011 only. The audit collection and new pack
  README, exact `referenceCurrentPacks` projection, RIA JSON/schema/producer,
  focused RIA and link/owner semantics, and exact current-pack fixtures changed
  atomically. The initial exact 15-file index expanded to 17 after formatter/QA
  review with exactly two accepted additions: `.secrets.baseline` and
  `docs/03.specs/0055-workspace-governance-audit-and-remediation/plan.md`.
  The six old report bodies, Stage 98, LLM-WIKI output, provider configuration,
  secret values, remote resources, and live systems did not change.
- **RED**: the first exact production test failed because
  `currentPackBaselines` still selected
  `audits/2026-07-11-weia@15bba3d436ee2818f29d6f6880c7d5c4901aa0fe`
  instead of
  `audits/2026-08-09-wgia@e09a0b976a555c5200cdab2aeb9abf6759b77588`.
  The first isolated production run then rejected an incompletely projected
  new README and exposed pre-existing old-roadmap overlays; strict links also
  rejected the thematic Report Index order against the registry order.
- **GREEN contract**: the Current registry has one ID, state `draft`, and exact
  nine non-README members. `currentPackBaselines` has that same sole key at
  `e09a0b976a555c5200cdab2aeb9abf6759b77588`; `baselineTransitions` is empty.
  One closed audit settlement records old-to-new, source and protected-final
  commits, and member counts 6-to-9. One retired record has exactly
  `id/sourceCommit/allowedStates/members/retiredBy/reason`. Its source registry
  is read from `15bba3d436ee2818f29d6f6880c7d5c4901aa0fe`, while unchanged
  retired final bytes are guarded at settlement `toCommit`
  `e09a0b976a555c5200cdab2aeb9abf6759b77588`; this preserves approved overlays
  without permitting new drift. New navigation and exact Report Index order
  use counted literal replacements only; no `completeBody` projection exists.
- **Negative coverage**: hostile tests reject unknown retired fields, malformed
  SHA, bad or duplicate members, empty states, duplicate retired records,
  current/retired overlap, wrong member, wrong settlement commit/count,
  nonempty transition, historical-registry member loss, and retired byte drift.
  Five focused tests pass, and the final exact-index RIA suite passes 94 tests.
- **Primary formatter/QA RED and correction**: the first plain pre-commit failed
  because detect-secrets updated its baseline and the WGIA Plan raised MD001.
  `Global Constraints` became a profile-compatible bold label; baseline
  formatter security review was Approved. The first all-files lane then failed
  on eight reviewed false-positive metadata/prose candidates and pre-existing
  WERPC Plan MD001. The regenerated baseline has exactly 18 entries across
  seven paths with every `is_secret` false, no detector weakening, and Approved
  security review; WERPC `Global Constraints` is now bold.
- **Final primary validation sequence**: affected `PASS` (paths=17); staged
  `PASS` (paths=17); plain pre-commit `PASS`; RIA `PASS` (94/94); production RIA
  settled `PASS`; LLM-WIKI `PASS`; archive `PASS`; direct repository gate
  `PASS`; full harness `PASS`; final all-files `PASS`; formatter-review `PASS`;
  rerun `PASS`. Primary final diff-checks remain pending.
- **Fresh-review fix round 1**: RED `test_production_audit_collection_routes_current_comparison_to_wgia`
  failed on the stale 2026-07-11 Current-comparison literal; the real-e09
  regression raised `RIA-CONTRACT retiredCurrentPackBaselines: must be an
  array` instead of reaching the original explicit FSM result; and link
  self-test stopped on the new missing-final-blob mutation because its fixture
  lacked `baselineSettlements`. GREEN adds one exact counted collection
  replacement, limits legacy-v2 compatibility to commit-anchored loading while
  keeping the proposed loader/schema strict, and consumes the audit settlement
  as two authorities: registry membership from retired `sourceCommit=15bba3d...`
  and protected final bytes from `toCommit=e09a0b9...`. Focused RIA is 7/7;
  link self-test, strict registry (502 paths), Markdown profiles (0), strict
  links, and `git diff --check` pass. Only the mutable collection/projection,
  RIA historical-loader boundary, retired link guard/fixture, focused tests,
  and this evidence changed in the round; old pack bodies and Stage 98 remain
  untouched.
- **Fresh-review fix round 2**: RED link self-test reported `retired link
  fixture source and final commits are conflated`; the missing-final probe
  expected the C1 registry read followed by the unreadable final-body read but
  observed `actual []`. GREEN creates two real fixture commits, binds retired
  `sourceCommit`/settlement `fromCommit` to C1, and binds the Current baseline,
  settlement `toCommit`, and snapshot final bytes to distinct C2. The valid
  probe observes C1 registry then C2 retired body. Missing-final changes both
  the Current baseline and `toCommit` to the same unreadable OID, observes C1
  registry then the attempted missing body read, and returns `LINK-BROKEN`;
  byte drift remains a separate negative. Links self/strict, three focused RIA
  tests, pycompile, Ruff, and `git diff --check` pass. The round changed only
  link-validator fixture construction/read-path coverage and this evidence.
- **Limitations, review, rollback, next owner**: repository-static evidence
  only; hosted/provider/remote/live remain `DEFER`. Fresh specification/content
  and Python/quality reviews are Approved after clean fix rounds 1-2 with no
  remaining Critical/Important. The atomic unit is commit
  `dcc0a0e9fbb9587c211fd457414f9dfe2e6924de`. Roll back that entire commit;
  never partially revert registry, RIA, index, or fixtures. WGIA-013 owns the
  current disposition revalidation.

### WGIA-013 Focused Evidence

- **Scope and acceptance**: VAL-WGA-010 only. This unit revalidates the exact
  WGIA disposition at Current HEAD
  `dcc0a0e9fbb9587c211fd457414f9dfe2e6924de`; it does not execute Spec 052
  `WORK-001`, simulate deletions, remove files, change indexes, or touch Stage
  98.
- **Fail-closed structural proof**: the Candidate Disposition Ledger has
  exactly 15 unique 12-column rows. All 15 decisions are `Integrate`, no
  decision is `Delete`, every candidate remains tracked, each row has a
  non-empty surviving owner, and the exact WORK-001 globs equal the same
  fifteen-path set. The proof reports `rows=15 integrate=15 delete=0
  tracked=15 live-consumer-rows=15 replacement-rows=15`.
- **Consumer and recovery proof**: all 114 current-consumer selectors route to
  tracked paths, each candidate has at least one consumer outside the
  candidate set, and all 15 full source commits recover their candidate bytes.
  The second proof reports `candidates=15 selectors=114
  source-recoverable=15 external-live-consumer-rows=15 delete-authorized=0`.
- **Existing owner and stop**: the Spec 052 Task still records `WORK-001` as
  `Queued` and `Not executed`; its Plan retains all five unchecked execution
  steps. Because the zero-consumer entry gate is false for every candidate,
  WGIA-013 stops before isolated deletion simulation, post-delete checks,
  removal, or a deletion commit. All fifteen paths and their current indexes
  remain unchanged.
- **Validation and lanes**: targeted structural/consumer/recovery proof
  `PASS`; strict registry passes 502 paths with zero uncovered or ambiguous,
  Markdown profiles report zero violations, strict links/owners returns `PASS
  CROSS-DOCUMENT`, worktree/cached diff checks pass, Stage 98 has zero diff,
  and the Current pack has zero diff. Production RIA intentionally reports
  only the mutable dirty-progress comparison limitation; after reversing an
  attempted pack evidence edit, it reports no Current-pack member or overlay
  diagnostic. Affected, staged, tests, all-files, formatter-review, rerun, full
  gate, and harness are owned by the primary agent after fresh review and by
  WGIA-014 for terminal closure. Hosted CI, provider runtime, authenticated,
  credential-bearing, remote, and live lanes remain `DEFER`.
- **Review, rollback, residual risk, next owner**: fresh review is Approved
  with no Critical or Important finding. The independent structural replay
  confirms 15 unique `Integrate` rows, `Delete=0`, 114 selectors, 15 external-
  consumer/owner/source-recovery rows, WORK-001 at zero of five steps, and no
  protected-scope diff. Rollback is limited to this no-deletion evidence unit;
  there is no file-deletion rollback. Live consumers and the open eligibility-
  test count blocker remain with the active-corpus owner and existing Spec 052
  `WORK-001`; WGIA-014 owns terminal validation after the evidence commit.

### WGIA-014 Terminal Evidence

- **Bounded repair**: before the one-line test edit, the focused active-corpus
  eligibility test failed with exact `AssertionError: 57 != 53`. The validator
  now names four additional terminal-standalone negative cases, so the test
  expectation changed from 53 to 57 without changing production behavior.
  The focused test and full test module pass; CLI self-test reports 58 cases
  (57 named cases plus its wrapper) and production reports `candidates=110
  eligible=12 defer=98 controls=2`.
- **VAL-WGA-001**: the Current pack remains exactly ten tracked files and its
  README retains exactly 30 sequential request rows. No pack member body was
  edited during closure.
- **VAL-WGA-002**: the nine report bodies retain the reviewed closed finding
  fields, verdicts, evidence depths, exact selectors, and blockers established
  by WGIA-001–009; closure adds no competing finding or policy owner.
- **VAL-WGA-003–009**: the final tree retains the reviewed purpose/governance,
  SDLC/documentation, CI/QA, harness/loop, knowledge/memory, agent/model, and
  security evidence plus their canonical-owner corrections in commits
  `a59177ca` through `e09a0b97`. Repository-static results remain separate from
  hosted, provider-runtime, credential-bearing, remote, and live `DEFER` rows.
- **VAL-WGA-010**: commit `4e4adcf3a120d1cd25006c7116f3f1cbbe29edae`
  records the reviewed no-deletion result: 15 unique `Integrate` rows,
  `Delete=0`, 114 tracked consumer selectors, 15 external-consumer rows, and
  Spec 052 `WORK-001` still queued with zero of five execution steps complete.
- **VAL-WGA-011**: commit
  `dcc0a0e9fbb9587c211fd457414f9dfe2e6924de` owns the atomic cutover. The
  2026-08-09 pack remains the sole Current nine-member report set; the six-
  member 2026-07-11 pack remains source-registered and final-byte protected.
  Stage 98 and both audit-pack bodies have zero closure diff.
- **VAL-WGA-012**: the branch preserves 17 logical pre-closure commits from
  design `d9ffa12a` through the no-deletion result `4e4adcf3`. The terminal
  in-review scope changes only the focused test, Plan, Task, durable progress,
  and ignored task evidence. Spec/Plan/Task frontmatter, the three indexes, and
  the standalone relation remain atomically `active`. Strict registry,
  profiles, links, RIA, LLM-WIKI, active-corpus, diff, protected-scope,
  terminal aggregate, harness, all-files, and fresh whole-branch review
  evidence are required before the later logical
  `docs: close workspace governance audit` commit.
- **Residue and boundaries**: tracked scratch-name and protected-scope scans
  are empty. Current audit member bodies, the retired audit body, Stage 98,
  RIA data/projection/baseline, Spec 052 `WORK-001`, provider state, and live
  resources are unchanged. Direct production RIA stops at its known
  `RIA-DUPLICATE` dirty-progress comparison boundary because this Task updates
  durable progress before commit; it reports no Current-pack or baseline
  mutation. The primary exact-tree/staged and clean-tree lanes own the terminal
  RIA result. Deeper evidence lanes remain `DEFER`.
- **Handoff**: after terminal gates and fresh correctness/security/coverage
  review approve this exact tree with no Critical or Important finding, the
  primary agent owns the closure commit and branch-finishing workflow.
- **Implementation reviews**: fresh Python/quality and specification/content
  reviews are Approved with no Critical or Important finding on the exact
  four-file in-review diff. Whole-branch terminal review remains pending.
- **Whole-branch security fix**: the first review found one Important command-
  trampoline risk: seven exact auto-allowed commands invoked repo-mutable
  scripts. RED proved an allow entry did not satisfy the immutable Git-only
  boundary. GREEN removes all repo-script auto-allows, retains exactly seven
  fixed read-only Git metadata commands, and adds a no-trampoline regression.
  The provider suite passes 32/32 plus config/evidence self/production, Ruff,
  Python compile, and diff checks. The complete 62-entry deny tuple and native
  runtime `DEFER` boundary remain unchanged. Fresh security and Python
  re-reviews are Approved with no remaining Critical or Important finding.
- **Terminal closure-authority RED/GREEN**: the first exact `done` repository
  gate failed with `CLOSURE-AUTHORITY-SCOPE` on Spec 054. A focused test first
  expanded the expected later-spec set and failed against the seven-path
  production constant. GREEN adds only the exact Spec 054 path to
  `POST_CLOSURE_SPEC_AUTHORITY_PATHS`; the focused test, 49-test closure class,
  25-case self-test, and production final frontier pass with
  `active_controls=0/0`, `terminal_controls=6/3`, `terminal_specs=3`, and
  guards `13/29`.
- **Exact terminal aggregate**: strict registry reports 502 paths with zero
  uncovered or ambiguous, Markdown profiles report zero violations, strict
  links and settled RIA pass, provider tests pass 32/32, eligibility tests pass
  7/7, affected surfaces report 858 paths and 22/22 coverage, and the complete
  repository quality gate plus full harness pass on the staged `done` tree.
- **Terminal review and pre-commit**: plain staged pre-commit and all-files
  pre-commit pass, including strict repository quality, detect-secrets,
  Markdown, shell, Actions, and Kubernetes hooks. Fresh whole-branch
  correctness, security, and coverage reviews plus the final Python/quality
  and lifecycle consistency re-reviews are Approved with no remaining
  Critical or Important finding. Independent replay passes 126 focused tests,
  affected and staged lanes for 14 paths, the full gate, and the harness.
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

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: repository-static owners under root governance adapters,
  `docs/00.agent-governance/**`, `docs/01.requirements/**` through
  `docs/05.operations/**`, `docs/90.references/**` except protected historical
  bodies unless navigation metadata is explicitly mutable, `docs/99.templates/**`,
  `.github/**`, `scripts/**`, `tests/**`, and exact proven deletion candidates.
- **Forbidden Paths**: every existing `docs/98.archive/**` payload, digest,
  envelope, and record; unrelated user changes; user/global provider config;
  secret values; remote or live resources.
- **Approval Required**: any change to approved PRD/AD/accepted ADR/operations
  policy, ambiguous architecture or authority, live/provider/hosted/remote
  action, credential handling, destructive external action, push, PR, or merge.
- **Static Validation**: exact work-package checks plus strict registry,
  Markdown profiles, links/owners, RIA, generated-index checks, affected
  validators, archive validation, full quality gate, harness, diff checks, and
  pre-commit when available.
- **Live Validation**: `DEFER`; this execution has no live, hosted, provider-
  runtime, authenticated, credential-bearing, or remote authorization.
- **Secret / Vault Handling**: do not read, print, copy, rotate, or write secret
  values. Static secret-reference and policy structure may be inspected.
- **Rollback Plan**: keep every non-empty work package in a logical commit;
  revert the affected unit. Current-pointer and deletion changes are separate
  commits validated in staged or isolated trees before commit.
- **Evidence Location**: this Task, the ten-file audit pack, canonical owner
  diffs and tests, durable progress, Git commits, and ignored task/review
  reports while execution is active.
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

- [Spec 0055](./spec.md)
- [ADR-0022](../../../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [WGIA Task](./plan.md)
- [Stage 90 reference router](../../../../90.references/README.md)
- [Current source coverage](../../../../90.references/research/0001-workspace-engineering/m0012-source-coverage.md)

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-WGA-001](./spec.md#success-criteria--verification-plan) | WGIA-001, WGIA-014 | [Exact ten-file and 30-row evidence](./tasks/tsk-0002-wgia-001.md). |
| N/A — VAL-WGA-002 shares the Spec source above | WGIA-001–009, WGIA-014 | [Finding-field completeness and independent reviews](./tasks/tsk-0002-wgia-001.md). |
| N/A — VAL-WGA-003 shares the Spec source above | WGIA-002, WGIA-010, WGIA-014 | [Purpose/governance owner matrix and remediation evidence](./tasks/tsk-0003-wgia-002.md). |
| N/A — VAL-WGA-004 shares the Spec source above | WGIA-003, WGIA-010, WGIA-014 | [SDLC/document/profile/template evidence](./tasks/tsk-0004-wgia-003.md). |
| N/A — VAL-WGA-005 shares the Spec source above | WGIA-004, WGIA-011, WGIA-014 | [CI/QA/fixture/Validation/Verification evidence](./tasks/tsk-0005-wgia-004.md). |
| N/A — VAL-WGA-006 shares the Spec source above | WGIA-005, WGIA-011, WGIA-014 | [Harness/loop/script/blocker evidence](./tasks/tsk-0006-wgia-005.md). |
| N/A — VAL-WGA-007 shares the Spec source above | WGIA-006, WGIA-010, WGIA-014 | [LLM-WIKI and memory lifecycle evidence](./tasks/tsk-0007-wgia-006.md). |
| N/A — VAL-WGA-008 shares the Spec source above | WGIA-007, WGIA-011, WGIA-014 | [Exact agent/adapter/model/evaluation evidence](./tasks/tsk-0008-wgia-007.md). |
| N/A — VAL-WGA-009 shares the Spec source above | WGIA-008, WGIA-011, WGIA-014 | [Security/approval/static platform evidence](./tasks/tsk-0009-wgia-008.md). |
| N/A — VAL-WGA-010 shares the Spec source above | WGIA-009, WGIA-013, WGIA-014 | [Candidate ledger and post-delete evidence](./tasks/tsk-0010-wgia-009.md). |
| N/A — VAL-WGA-011 shares the Spec source above | WGIA-012, WGIA-014 | [Sole Current transition and historical protection evidence](./tasks/tsk-0013-wgia-012.md). |
| N/A — VAL-WGA-012 shares the Spec source above | WGIA-010–014 | [Re-audit, blocker closure, reviews, full QA, and commit ledger](./tasks/tsk-0011-wgia-010.md). |

### Legacy Task traceability

#### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WGIA-000](./plan.md#work-breakdown) | Done. | RED: the different valid approval date was rejected with `STANDALONE-EXECUTION-APPROVAL`. GREEN: links/owners self-test accepts both valid dates and rejects the invalid calendar date. Strict registry reports 492 paths with 0 uncovered/ambiguous; Markdown profiles report 0 violations; strict links, Ruff, Python compile, cached diff, and complete repository quality gate pass. Python review is Approved; the Spec review's sole index-drift finding was fixed and no other Critical/Important finding remained. |
| N/A — WGIA-001 shares the Plan and Spec sources above | Done as a bounded draft foundation. | Exact observation SHA; RED 0/0 pack/request probe and README current-inventory mismatch; malformed-fixture rejection; GREEN 10 files, 30 sequential request rows, 9 reports, 14 conceptual finding fields, 8 verdicts, 4 evidence depths, and exact observation-commit evidence paths; strict registry 502 paths, Markdown profiles 0, strict links/owners, cached/worktree diff, and complete repository quality gate PASS; specification, quality, and Python reviews Approved; Stage 98 and Current-pointer boundaries preserved. WGIA-014 owns whole-branch review. |
| N/A — WGIA-002 shares the Plan and Spec sources above | Done. | Four complete findings: one repository-static `Aligned`, two root README `Conflict`, and one provider-runtime `DEFER`; one reviewed provisional WGIA-009 roadmap input; focused governance/closure, 12/4/48 harness contract, 12-role/48-adapter semantics, roster currentness, strict registry/profile/link, diff, Stage 98, and complete repository gate checks PASS. Specification and quality reviews Approved. |
| N/A — WGIA-003 shares the Plan and Spec sources above | Done. | Four complete repository-static findings: eleven requested families structurally `Aligned`; broad Release mapping to DOC-G5 is a `Gap`; approved Guide Type enum enforcement under WORK-013 is `Partial`; and integration guides are `Partial` with live usability `DEFER`. Two provisional WGIA-009 dedupe/routing inputs; first quality review findings fixed; specification and fix-round quality reviews Approved; complete repository quality gate PASS. |
| N/A — WGIA-004 shares the Plan and Spec sources above | Done. | Four complete findings: Actions and lane ownership `Aligned`, accurate dormant Prettier `DEFER`, and repository-static Validation versus hosted Verification/CD `Partial`; focused workflow/contract checks and 110 tests PASS; specification/content and quality reviews Approved; complete repository quality gate PASS. |
| N/A — WGIA-005 shares the Plan and Spec sources above | Done. | Four complete findings: repository-static harness topology and loop/checkpoint controls `Aligned`; fixture production evidence remains aligned within `WGA-HAR-003`, but canonical script human inventory is `Partial`; provider runtime and actual ignored-checkpoint execution `DEFER`. Exact proof is 47 scripts = 41 CLI + six helpers with two human-index omissions, 37 fixtures, one provisional roadmap row, and one complete evidence-depth blocker; specification/content and fix-round quality reviews Approved; complete repository quality gate PASS. |
| N/A — WGIA-006 shares the Plan and Spec sources above | Done. | Four complete findings: generated ownership/lookup and four-class memory lifecycle `Aligned`; stale LLM-WIKI source-trigger review metadata is a `Gap`; provider-local/actual lifecycle execution `DEFER`. Exact proof shows all six declared inputs changed after the 2026-05-10 review date; one provisional freshness repair and one complete provider-runtime blocker are recorded; specification/content and quality reviews Approved; complete repository quality gate PASS. |
| N/A — WGIA-007 shares the Plan and Spec sources above | Done. | Four complete findings: exact 12-role/four-surface/48-projection inventory and integrated supervisor orchestration `Aligned`; model/evaluation/admission state `Partial`; native provider execution `DEFER`. Focused contract self-tests/production and 150 tests pass; specification/content and fix-round quality reviews Approved; complete repository quality gate PASS. |
| N/A — WGIA-008 shares the Plan and Spec sources above | Done. | Nine complete findings and a full control matrix distinguish static alignment from one permission conflict, three gaps, two partial controls, and deeper `DEFER`; six provisional WGIA-009 inputs are recorded. Focused static security checks pass with optional Conftest `SKIP`; redacted Gitleaks candidates remain intentionally untriaged; fresh specification/content and security fix-round reviews are Approved with no Critical/Important finding. |
| N/A — WGIA-009 shares the Plan and Spec sources above | Done with bounded `Partial` findings and one routed blocker. | Seven legacy-name active surfaces are rejected as noncandidates; fifteen exact Spec 052 WORK-001 paths are `Integrate`, `Delete=0`, and 2,355 starting-HEAD/2,360 authored-worktree vocabulary line hits remain rejected as name-only evidence. Twelve inputs are deduplicated once: seven bounded Correct/Integrate admissions and five explicit `DEFER` decisions. Structural, 114-selector, strict document/link, legacy-cutover, active-corpus production/self-test/role-production, archive, RIA, complete repository gate, diff, and Stage 98 checks pass. The exact staged 150-test run has 149 PASS and one expected-53/actual-57 eligibility failure under open `BLK-WGA-DSP-003`; `BLK-WGA-DSP-001`/`002` are resolved. Fix-round content and quality reviews are Approved. |
| N/A — WGIA-010 shares the Plan and Spec sources above | Done. | Deterministic RED/GREEN and producer-only generation pass; three RIA generator tests, governance closure, RIA self-test, strict registry/profile/link, archive, DOC and RIA-owner no-delta, diff, and Stage 98 pass. The exact staged complete repository quality gate passes the RIA and aggregate boundary; fresh specification/content and quality reviews are Approved. |
| N/A — WGIA-011 shares the Plan and Spec sources above | Done. | Script inventory RED/GREEN reaches exact 47/41/6 with zero missing names and exact-AST negative probes; Claude permission RED/GREEN removes seven broad allows and enforces exact no-wildcard/no-alternate-root commands plus the focused-owned complete 62-entry deny tuple. Thirty-two focused provider tests, provider self/production, harness contract/semantics/currentness, syntax, the embedded aggregate contract, and exact staged complete repository quality gate pass. Fresh specification/content, Python/quality, and security reviews are Approved; provider-runtime/hosted/remote/live evidence stays `DEFER`. |
| N/A — WGIA-012 shares the Plan and Spec sources above | Done. | Exact sole Current, 9-member registry, retired 6-member source/final-byte guard, closed 6-to-9 settlement, literal projections, and RIA 94/94 pass. The final exact index is 17 paths after Approved formatter/security review of exactly `.secrets.baseline` and the WERPC Plan additions; affected, staged, plain pre-commit, production RIA settled, LLM-WIKI, archive, direct repository gate, full harness, final all-files, formatter-review, and rerun pass. Fresh specification/content and Python/quality reviews are Approved after clean fix rounds 1-2 with no remaining Critical/Important; atomic commit `dcc0a0e9fbb9587c211fd457414f9dfe2e6924de`. Hosted/remote/live remain `DEFER`. |
| N/A — WGIA-013 shares the Plan and Spec sources above | Done: no deletion. | Exact Current-HEAD proof reports 15 unique tracked `Integrate` rows, `Delete=0`, 114 tracked consumer selectors, an external live consumer and surviving owner for every row, 15 recoverable source commits, and Spec 052 `WORK-001` queued/unexecuted with zero of five steps complete. No deletion simulation, removal, post-delete claim, empty deletion commit, or Stage 98 change occurred; fresh review is Approved with no Critical or Important finding; commit `4e4adcf3a120d1cd25006c7116f3f1cbbe29edae`. |
| N/A — WGIA-014 shares the Plan and Spec sources above | Done. | [Terminal evidence](#wgia-014-terminal-evidence) records the criterion closure, focused 53-to-57 RED/GREEN, exact staged terminal gates, whole-branch review approval, protected-scope and residue checks, logical history, reciprocal `done` lifecycle, and deeper-lane `DEFER` state. |
