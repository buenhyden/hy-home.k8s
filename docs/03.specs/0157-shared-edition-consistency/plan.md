---
title: "Shared Edition Consistency Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0157-PLAN-0001"
parent_ids: ["SPEC-0157"]
---

# Shared Edition Consistency Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two execution constraints. First, no repository file changes outside this package, the Stage 03 README, one back-link sentence in the Traceability section of [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md#traceability), `scripts/document_contracts.py`, `scripts/validate-document-contract-registry.py`, `tests/test_shared_contract_binding.py`, one sentence in `.agents/governance/document-lifecycle.md` with its patch `version` bump (2.5.0 to 2.5.1) and `updated` date, and `.secrets.baseline` entries marking this Task's reviewed SHA-256 document digests as non-secret. Second, negative cases run only on disposable copies outside the repository.

## Overview

Add the shared-edition consistency check defined in [SPEC-0157](spec.md). [Task 0001](tasks/tsk-0001-shared-edition-consistency.md) owns execution evidence and criterion acceptance.

## Context

Completed SPEC-0156 recorded W01's rejected clauses, and completed SPEC-0158 closed W00. A W01 re-audit on a disposable copy found that rule documents naming another WGOV-CORE edition than the registry's adopted `3.0.0` pass every document validator. On 2026-11-11 the user chose to finish W01 on branch `claude/w01-edition-check`, which starts at `18ef5024`, the tip of open PR #223. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) constrains the design; no interface, migration or rollback surface beyond the validator and this package changes.

## Goals & In-Scope

- Write failing tests first, then the pure function and its validator call.
- State the rule in one sentence of `.agents/governance/document-lifecycle.md`, naming no edition other than the adopted one, and bump its patch version and `updated` date.
- Show the validator passing on the current tree and failing on a disposable copy with a wrong edition; confirm the existing projection and approval refusals still fail.
- Add this package to the Stage 03 README and link it from REQ-0003 Traceability.

## Non-Goals & Out-of-Scope

- Registry schema, binding fields, provider settings and workflows, and any other governance policy text.
- Any edit to historical Spec packages, the archive or `CHANGELOG.md`.
- Any push, PR, merge or package exit without separate user approval.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-EDITION-001](spec.md#success-criteria--verification-plan) | Write the focused tests, see them fail, implement the function and its call, see them pass; add the policy sentence. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-shared-edition-consistency.md) | `python3 -m unittest tests.test_shared_contract_binding`, RED then GREEN. |
| WORK-002 | [VAL-EDITION-002](spec.md#success-criteria--verification-plan), [VAL-EDITION-003](spec.md#success-criteria--verification-plan) | Run the validator on the current tree and on disposable negative copies; obtain independent review; run commit checks. | WORK-001. | [Task 0001](tasks/tsk-0001-shared-edition-consistency.md) | Negative copies, independent review, strict document checks and commit hooks. |

## Verification Plan

- Focused unit tests fail before the implementation and pass after it.
- The registry validator passes on the current tree, fails with `REGISTRY_SHARED_EDITION_MISMATCH` on a disposable copy, and the earlier projection-drift and adoption refusals still fail.
- An independent read-only reviewer checks the code, tests and scope.
- Strict document checks, the staged lifecycle check and the active commit hooks run on the exact index.
- Architecture compliance: confirm no AD or ADR changed and the only policy change is the one lifecycle sentence.

## Risks & Mitigations

- **A legitimate current mention of another edition is refused.** Mitigation: history paths are excluded; any other need returns to Spec review.
- **The pattern misses a written form.** Mitigation: tests cover both recognized forms and code formatting; other forms are named in the Spec.

## Completion Criteria

All three criteria need observed PASS evidence, no unresolved required failure, an independent review with no blocking finding, and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Rule documents name the registry's adopted shared-contract edition | [Document lifecycle policy](../../../.agents/governance/document-lifecycle.md) | The shared-contract rule list, enforced by `REGISTRY_SHARED_EDITION_MISMATCH` in the registry validator |
