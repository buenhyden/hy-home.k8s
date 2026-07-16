---
title: 'Task: Document Schema and Lifecycle Contract'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-16
---

# Task: Document Schema and Lifecycle Contract

## Overview

This Task is the mutable execution and review ledger for DSLC-001 through
DSLC-006 under [Spec 035](../../03.specs/035-document-schema-and-lifecycle-contract/spec.md).
It records test-first results, logical commits, rollback parents, independent
reviews, and explicit static/live evidence boundaries.

## Inputs

- [Implementation Plan](../plans/2026-07-16-document-schema-and-lifecycle-contract.md)
- [Spec 035](../../03.specs/035-document-schema-and-lifecycle-contract/spec.md)
- [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- [ADR-0017](../../02.architecture/decisions/0017-program-follow-up-lineage-semantics.md)
- [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)
- [Document type, format, and evidence research](../../90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md)
- [Current implementation audit pack](../../90.references/audits/2026-07-11-weia/README.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| DSLC-001 | VAL-DSLC-001, VAL-DSLC-002, VAL-DSLC-003, VAL-DSLC-007, VAL-DSLC-008 | Add closed registry v7 value, role, lifecycle, evidence, and compatibility schema plus typed projection. | platform | Queued | Not executed | RED/GREEN registry cases, strict load, review verdict, logical commit |
| DSLC-002 | VAL-DSLC-001, VAL-DSLC-002, VAL-DSLC-005 | Enforce metadata values, template/source parity, and baseline-only Tombstone admission. | platform | Queued | Not executed | Metadata/parity/admission mutations, current-corpus result, review, commit |
| DSLC-003 | VAL-DSLC-003, VAL-DSLC-004, VAL-DSLC-008 | Implement exact staged, CI, explicit-ref, and snapshot comparison modes and transition graph validation. | platform | Queued | Not executed | Isolated Git fixtures, lifecycle diagnostics, review, commit |
| DSLC-004 | VAL-DSLC-004, VAL-DSLC-008 | Enforce edge-specific rendered-link, state, same-diff, and body-contract evidence. | platform | Queued | Not executed | Predicate mutation matrix, strict cross-document result, review, commit |
| DSLC-005 | VAL-DSLC-005, VAL-DSLC-006, VAL-DSLC-007 | Close native, role/source, Stage 00/99, and directly implicated consumer drift without bulk corpus rewrite. | platform | Queued | Not executed | Native/overlap fixtures, drift ledger, full static result, review, commit |
| DSLC-006 | VAL-DSLC-001 through VAL-DSLC-008 | Run full QA, whole-tranche review, and atomic lifecycle closure. | platform | Queued | Not executed | Done lineage, command matrix, review verdicts, rollback parent, closure commit |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/00.agent-governance/**` only where named by the
  Plan; `docs/03.specs/035-document-schema-and-lifecycle-contract/**` and its
  Stage 03 index; this Plan/Task and Stage 04 indexes;
  `docs/05.operations/incidents/README.md`; the directly implicated Stage 90
  research ledger/pointer; `docs/99.templates/support/**` and canonical forms
  implicated by v7; `scripts/document_contracts.py`, document/lifecycle/link
  validators and `scripts/README.md`; focused fixtures; program relation and
  migration-ledger closure rows.
- **Forbidden Paths**: Kubernetes/GitOps desired state, infrastructure,
  policies, secrets, provider runtime adapters, generated outputs, accepted or
  completed historical bodies, archive corpus conversion, bulk Stage 05/helper
  body normalization, completed Plan/Task movement, and Spec 036-040 bodies
  except read-only boundary verification.
- **Approval Required**: Any live system, secret, remote GitHub setting, push,
  publication, dependency installation, or scope expansion requires separate
  explicit approval.
- **Static Validation**: Registry, Markdown-profile, lifecycle,
  cross-document, native available-linter, repository-quality, Markdown lint,
  staged diff, and all-files pre-commit commands from the Plan.
- **Live Validation**: DEFER. Spec 035 authorizes no remote/provider/live lane.
- **Secret / Vault Handling**: Do not read, print, move, or infer ignored
  secrets, credentials, tokens, auth files, shell history, kubeconfigs, or
  Vault values.
- **Rollback Plan**: Before closure, revert the newest open DSLC package first
  and remove v7 consumers before v7 schema/data. After DSLC-006, do not reopen
  terminal evidence in isolation: apply DSLC-006 through DSLC-001 newest-first
  with `git revert --no-commit`, validate only the complete staged v6/active
  state, and create one atomic rollback commit. Record every commit parent in
  this Task.
- **Evidence Location**: This Task, logical Git commits, focused fixtures,
  validator outputs summarized here, and the durable migration ledger.

## Verification Summary

Planning baseline: registry v6 classifies 430 paths through 64 profiles and 30
templates with zero uncovered or ambiguous routes. Registry self-test has 78
cases; cross-document self-test has 344 cases. Current frontmatter/profile
validation passes. No Spec 035 implementation work has run yet. The isolated
filesystem reproduces one known `os.mkfifo` `Errno 95` in the all-files
repository-quality hook; Spec 039 owns that portability fix, and it may be
recorded as DEFER only when every other hook passes.

Planning review first rejected underspecified creation/movement admission,
edge evidence, Git comparison interfaces, native syntax claims, closure order,
null-body profile handling, and post-closure rollback. The remediated Plan now
owns exact admission defaults, an edge/predicate matrix, the lifecycle
module/CLI/fixture and exit contract, staged closure review, explicit native
syntax DEFER, heading-set predicates for null-body profiles, and one atomic
post-closure rollback. Independent re-review returned
`REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`. The staged planning set passes
strict registry, Markdown-profile, cross-document, diff-check, and changed-file
Markdown lint validation.

## Traceability

- **Spec**: [Spec 035](../../03.specs/035-document-schema-and-lifecycle-contract/spec.md)
- **Plan**: [Implementation Plan](../plans/2026-07-16-document-schema-and-lifecycle-contract.md)
- **Predecessor Task**: [Spec 034 execution evidence](./2026-07-15-authority-and-lineage-foundation.md)

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [DSLC-001](../plans/2026-07-16-document-schema-and-lifecycle-contract.md#dslc-001-registry-v7-contract) | Queued. | Registry v7 RED/GREEN and review evidence will be recorded here. |
| [DSLC-002](../plans/2026-07-16-document-schema-and-lifecycle-contract.md#dslc-002-metadata-template-and-compatibility-enforcement) | Queued. | Metadata, parity, Tombstone admission, and current-corpus evidence will be recorded here. |
| [DSLC-003](../plans/2026-07-16-document-schema-and-lifecycle-contract.md#dslc-003-base-and-transition-engine) | Queued. | Git base-mode and transition evidence will be recorded here. |
| [DSLC-004](../plans/2026-07-16-document-schema-and-lifecycle-contract.md#dslc-004-transition-evidence) | Queued. | Edge predicate and cross-document evidence will be recorded here. |
| [DSLC-005](../plans/2026-07-16-document-schema-and-lifecycle-contract.md#dslc-005-native-role-and-support-drift) | Queued. | Native, role, support, and consumer-drift evidence will be recorded here. |
| [DSLC-006](../plans/2026-07-16-document-schema-and-lifecycle-contract.md#dslc-006-closure) | Queued. | Full QA, independent reviews, and atomic closure evidence will be recorded here. |
