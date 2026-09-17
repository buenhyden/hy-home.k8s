---
title: "Cut Over Archive Reappraisal and Verifiable Sources"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-17"
layer: "specs"
artifact_id: "SPEC-0085-TSK-0002"
---

# Task: Cut Over Archive Reappraisal and Verifiable Sources

## Overview

This Task owns WP-003 and WP-004 of the [Implementation Plan](../plan.md): the
acceptance of ADR-0040 with its registry, index, validator, and test cutover,
and the envelope verification against the default branch. It closes with
focused, staged, and full evidence.

## Inputs

- [SPEC-0085](../spec.md) and its [Implementation Plan](../plan.md).
- [ADR-0040](../../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md),
  once the request owner approves the written decision.
- The survey in
  [SPEC-0085-TSK-0001](tsk-0001-propose-archive-reappraisal-and-document-standards.md).

## Task Table

| ID       | Upstream criterion | Work item                                                                          | Owner    | Status | Result       | Evidence                |
| -------- | ------------------ | ---------------------------------------------------------------------------------- | -------- | ------ | ------------ | ----------------------- |
| WORK-001 | VAL-ARS-009        | Accept ADR-0040, supersede ADR-0039, amend REQ-0003-FR-0020, activate this package | platform | Queued | Not executed | Lifecycle gate          |
| WORK-002 | VAL-ARS-004        | Registry assessment contract and removal transition, RED then GREEN                | platform | Queued | Not executed | Archive contract tests  |
| WORK-003 | VAL-ARS-005        | Treat a `git-history-only` unit as available in Git, not as a missing payload      | platform | Queued | Not executed | Archive contract tests  |
| WORK-004 | VAL-ARS-006        | Availability and assessment rule in the citation table                             | platform | Queued | Not executed | Citation decision tests |
| WORK-005 | VAL-ARS-007        | Reject every `purged` row                                                          | platform | Queued | Not executed | Archive contract tests  |
| WORK-006 | VAL-ARS-008        | Default branch, object-format length, and Git object fixtures                      | platform | Queued | Not executed | Git fixture tests       |
| WORK-007 | VAL-ARS-012        | Staged and full evidence                                                           | platform | Queued | Not executed | QA results              |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/99.templates/registry.json`,
  `docs/99.templates/contracts/`, `docs/98.archive/README.md` outside existing
  catalog rows, `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `docs/02.architecture/decisions/`, this package, `scripts/archive_*.py`,
  `scripts/document_*.py`, `scripts/validate-document-lifecycle.py`,
  `scripts/validate-links-and-owners.py`, `scripts/run-archive-contract-tests.py`,
  and `tests/`.
- **Forbidden Paths**: every retained body, sealed record, ledger, and existing
  catalog row; `gitops/`; secrets and private configuration.
- **Approval Required**: WORK-001 needs the request owner's approval of the
  written ADR-0040. Removing or reappraising a real unit is not approved. Push,
  pull request, and merge are not approved.
- **Static Validation**: focused tests per work item, the quick profile on the
  working tree, the staged profile per logical commit, and one full profile on
  the final tree.
- **Live Validation**: not run. No live cluster, provider runtime, or network
  action is authorized.
- **Secret / Vault Handling**: no secret, credential, or private configuration
  is read or printed. Fixtures use synthetic content only.
- **Rollback Plan**: revert the cutover commits together; no frozen byte or
  catalog row changes, so a revert restores ADR-0039 enforcement.
- **Evidence Location**: this Task record.

## Verification Summary

Not executed. Results are recorded as each work item runs.

## Traceability

### Lifecycle Traceability

| Criterion / work item                 | Result       | Evidence                |
| ------------------------------------- | ------------ | ----------------------- |
| [WORK-001](../plan.md#work-breakdown) | Not executed | Lifecycle gate          |
| [WORK-002](../plan.md#work-breakdown) | Not executed | Archive contract tests  |
| [WORK-003](../plan.md#work-breakdown) | Not executed | Archive contract tests  |
| [WORK-004](../plan.md#work-breakdown) | Not executed | Citation decision tests |
| [WORK-005](../plan.md#work-breakdown) | Not executed | Archive contract tests  |
| [WORK-006](../plan.md#work-breakdown) | Not executed | Git fixture tests       |
| [WORK-007](../plan.md#work-breakdown) | Not executed | QA results              |
