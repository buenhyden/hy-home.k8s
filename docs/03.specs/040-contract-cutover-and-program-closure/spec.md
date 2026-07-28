---
title: 'Contract Cutover and Program Closure Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-07-28
---

# Contract Cutover and Program Closure Technical Specification (Spec)

## Overview

This Spec removes temporary compatibility, proves the integrated repository
contract, completes indexes and migration evidence, performs independent
whole-branch review, and closes the document lifecycle and evidence program
without claiming unobserved remote or live results.

Spec 039 closed in
`e1d1e910840337327a557ab4b84e86f8fced11d6`, and its repository-static
postflight passed. Commit
`11a020d9b299ae91b7af9278c22ed89ffccb5cfc` records that observed closure and
hands the program frontier to this Spec. The current hosted, provider, and live
lanes remain `DEFER`; they are not inferred from the local PASS. Reciprocal
Plan/Task activation is observed in
`5c7bb820d9b424577eda3eb3a5c368f0c7cfc656`. CCPC-001 strict-only cutover is
observed in `0ae1fcd300d43914901d0eb2f0fd929bfe65cb1d`. CCPC-002 now records the
complete repository-static closure matrix, exact advanced terminal frontier,
and Current-audit reconciliation; CCPC-003 whole-branch QA and independent
review is the active work package.

## Strategic Boundaries & Non-goals

- **In scope**: Compatibility removal, strict registry/profile cutover, all
  indexes and cross-links, final migration ledger, historical-body guards,
  Current audit overlay, full QA, independent review, status transitions, and
  branch completion evidence.
- **Non-goals**: New functional scope, deferred live assurance, remote
  publication without approval, renumbering, or waiver-based closure.

## Contracts

- Specs 034-039 must satisfy their criteria before final cutover.
- Spec 039 must close its repository-local workflow and dependency contract.
  An unexecuted post-change remote run remains an owned DEFER and is not
  relabeled as PASS.
- Retired Stage 99 archive routes, forms, active-reader wording, and
  compatibility behavior are absent after cutover.
- All governed current and archive records resolve exactly one final profile.
- Every migration row has a final disposition and rollback reference.
- Final QA separates static PASS from optional SKIP and remote/live DEFER.
- Independent reviewers approve both requirement compliance and implementation
  quality before program status changes.

## Core Design

The cutover runs a preflight inventory, removes temporary compatibility,
regenerates derived outputs, validates the entire corpus, and compares results
with tranche acceptance evidence. A closure matrix maps every PRD requirement
and Spec criterion to a command, result, commit range, reviewer, limitation,
and rollback.

The Current audit overlay records repository-static closure and retains
remaining lifecycle, provider, platform, and live findings with their existing
owners. Program documents move through allowed states only after evidence is
committed.

## Data Modeling & Storage Strategy

The durable closure record contains:

- program and tranche commit ranges;
- final registry version and corpus counts;
- archive and execution migration summaries;
- unresolved DEFER rows and owners;
- verification commands and result classes;
- independent review verdicts;
- rollback mapping.

Ignored SDD and dry-run scratch remain non-durable. Required results are
promoted to canonical Plan, Task, Spec, audit overlay, or archive index before
cleanup.

## Interfaces & Data Structures

- Final inventory: routes, profiles, states, owners, links, indexes, generated
  outputs, archive payloads, and execution dispositions.
- Closure matrix: requirement, criterion, evidence, result class, commit,
  reviewer, limitation, and rollback.
- Branch handoff: clean worktree, logical history, merge base, validation
  summary, and explicit integration options.

## Edge Cases & Error Handling

- A compatibility-only pass is a failure at this stage.
- A DEFER with no owner or trigger blocks closure.
- A remote check not executed remains DEFER regardless of local similarity.
- An observed remote failure for an older SHA remains attached to that SHA and
  cannot block repository-local closure after the defect is fixed and the
  retry trigger has an owner; it still blocks a remote-current PASS claim.
- Formatter changes discovered by all-files pre-commit are reviewed and
  recommitted before rerun.
- A new broken link or duplicate owner introduced by final index work fails the
  complete corpus.

## Failure Modes & Fallback / Human Escalation

- If cutover fails, revert the smallest responsible logical unit. Do not
  restore an active compatibility reader or weaken strict rules; retain only
  pinned, private, fail-closed historical transition proof.
- If independent review finds Critical or Important issues, fix and re-review
  before closure.
- If merge integration would overwrite unrelated user work, stop and request
  direction.

## Verification Commands

- Run every registry, Markdown, transition, owner/link, archive, migration,
  reference, generated-output, workflow, GitOps, manifest, and repository
  self-test.
- Run pre-commit across all files and git diff checks.
- Generate a whole-branch review package from the main merge base.
- Verify the merged result again if local integration is selected.

## Success Criteria & Verification Plan

- **VAL-CCPC-001**: Active compatibility behavior, retired Stage 99 archive
  profile/form claims, and stale wording are zero.
- **VAL-CCPC-002**: Uncovered routes, ambiguous routes, duplicate current
  owners, invalid transitions, and broken current links are zero.
- **VAL-CCPC-003**: Archive provenance and historical links pass for every
  archived record.
- **VAL-CCPC-004**: Every baseline Plan/Task has a final migration disposition.
- **VAL-CCPC-005**: References, generated outputs, workflows, selectors, and
  result classes pass their complete contract.
- **VAL-CCPC-006**: All-files pre-commit and independent whole-branch review
  pass, with remote/live limitations preserved.

## Traceability

- **Predecessors**: [Spec 037](../037-active-corpus-and-execution-retention/spec.md), [Spec 038](../038-reference-information-architecture/spec.md), and [Spec 039](../039-github-ci-qa-evidence/spec.md)
- **Program PRD**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **Program ARD**: [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- **Decisions**: [ADR-0017](../../02.architecture/decisions/0017-program-follow-up-lineage-semantics.md), [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md), and [ADR-0020](../../02.architecture/decisions/0020-document-lifecycle-program-closure-evidence.md)
- **Execution Plan**: [Contract Cutover and Program Closure Implementation Plan](../../04.execution/plans/2026-07-27-contract-cutover-and-program-closure.md)
- **Task Evidence**: [Contract Cutover and Program Closure Task](../../04.execution/tasks/2026-07-27-contract-cutover-and-program-closure.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-WDLEC-003](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-CCPC-001 | Final stale-route and compatibility scans report zero. |
| [REQ-WDLEC-001](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-CCPC-002 | Strict registry, profile, transition, owner, and link gates pass. |
| [REQ-WDLEC-004](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-CCPC-003 | Complete archive integrity and historical-link checks pass. |
| [REQ-WDLEC-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-CCPC-004 | Final migration ledger has no unowned disposition. |
| [REQ-WDLEC-008](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-CCPC-005 | References, generation, workflow, and selector suites pass. |
| [REQ-WDLEC-011](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-CCPC-006 | All-files QA and independent review produce clean verdicts. |
