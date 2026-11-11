---
title: "Designated Source Applicability Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0155-PLAN-0001"
parent_ids: ["SPEC-0155"]
---

# Designated Source Applicability Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two execution constraints. First, no repository file changes outside this package, the Stage 03 README, one back-link sentence in the Traceability section of [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md#traceability) that the cross-document validator requires, and `.secrets.baseline` entries that mark this Task's reviewed SHA-256 document digests as non-secret, following the reviewed-digest precedent of commit `f3dcab6d`. Second, research agents and the supervising session write nothing else to the repository; their working files stay in the session scratchpad, and external pages are read only as data.

## Overview

Record and verify the [SPEC-0155](spec.md) tables: SUP-02 (72 source-perspective rows), SUP-01 (52 legacy work-package links and preserved history identities) and USER22-21 (4 official sources). [Task 0001](tasks/tsk-0001-designated-source-applicability.md) owns the execution evidence, the tables and criterion acceptance.

## Context

Completed SPEC-0154 (commits `c9cbe522` and `fafd7a09` on branch `claude/requirement-owner-crosswalk`) recorded the requirement crosswalk this package links to. Its Task listed SUP-01 as not selected and did not cover SUP-02 or USER22-21. On 2026-11-11 the user chose to close these W00 obligations in a follow-up package. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) and [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) constrain the design; this plan changes no interface, migration or rollback surface beyond this package.

## Goals & In-Scope

- Read each of the 12 designated sources directly and record the six perspective rows with access level, retrieval date and decision.
- Link the 52 hy-home-k8s legacy work packages to SPEC-0154 crosswalk IDs and current state, and record SHA-256 identities of the preserved history files without re-analysis.
- Record the four official sources cited by W00 with their applicability to current owners.
- Check completeness with a negative fixture, obtain an independent review, and record handoffs of any open row.
- Add this package to the Stage 03 README and link it from REQ-0003 Traceability.

## Non-Goals & Out-of-Scope

- Implementing any gap a source suggests: each one goes to its stage owner.
- Re-running the earlier atomization, the 168-row crosswalk or the 14,028-pair classification.
- Correcting the package's own ledgers or URLs; corrections found here are recorded as observations only.
- Any commit, push, PR, merge, package exit, cluster access or secret read without separate user approval.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SRC-001](spec.md#success-criteria--verification-plan), [VAL-SRC-002](spec.md#success-criteria--verification-plan), [VAL-SRC-003](spec.md#success-criteria--verification-plan) | Record the three tables, check completeness, obtain independent review, and record handoffs. | Approved Spec and Plan; package input files hashed in the Task; completed SPEC-0154 crosswalk. | [Task 0001](tasks/tsk-0001-designated-source-applicability.md) | Completeness check with negative fixture, independent review, strict document checks and commit hooks. |

## Verification Plan

- Check that the three tables contain exactly the expected IDs once each, with no empty access, decision or current state, and that a negative fixture detects each injected defect.
- Have an independent reviewer that produced no rows sample-check access levels and decisions against the sources and cited owners, covering every UNVERIFIED, NOT_ADOPTED and BLOCKED/UNMAPPED row.
- Run the strict document checks, the staged lifecycle check and the active commit hooks on the exact index.
- Architecture compliance: confirm that no policy, ADR or AD file changed. Any such change returns the Spec to review.

## Risks & Mitigations

- **A fetch tool summarizes rather than quoting.** Mitigation: rows record this limitation, and reviewers spot-check claims that drive a decision.
- **A source page changes after retrieval.** Mitigation: each row keeps its retrieval date or commit.
- **Treating a source as authority.** Mitigation: decisions cite repository owners, and conflicting recommendations are recorded as not adopted.

## Completion Criteria

All three criteria need observed PASS evidence, no unresolved required failure, an independent review with no blocking finding, and the operator's acceptance. Completion closes the remaining W00 obligations only; handed-off rows stay open with their stage owners.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
