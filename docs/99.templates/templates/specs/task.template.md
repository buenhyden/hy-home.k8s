---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "specs"
artifact_id: "{{ARTIFACT_ID}}"
parent_ids: ["{{PARENT_ID}}"]
---

# Task: [Task Name]

## Overview

<!-- Author prompt: identify the bounded execution stream and its completion evidence. -->

## Inputs

<!-- Author prompt: link the approved Plan, Spec, decisions, and required evidence inputs. -->

## Task Table

<!-- Author prompt: keep one row per executable item and link each upstream VAL criterion to the owning Spec, using comma-space between links. For exactly one row, write literal frontmatter in its Status cell and put the actual state only in the frontmatter status key. For multiple rows, use actual row states; the frontmatter status summarizes them. Preview the summary with scripts/sync-task-status.py using an explicit --root and one current --path; add --write only to synchronize that scalar after the rows are valid and the lifecycle edge is legal. This never generates Result, Evidence, criterion acceptance, or approval. See the Stage 99 author guide for usage. Result is observed execution outcome; the sole criterion decision belongs below. -->

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-FEATURE-001]({{SPEC_RELATIVE_PATH}}#success-criteria--verification-plan) | One bounded change | {{OWNER}} | frontmatter | NOT_RUN | Pending named repository evidence |

## Task Evidence

<!-- Author prompt: record each factual check with an exact input and location. Required is yes or no. Resolves is none or comma-space separated earlier Evidence IDs. A required FAIL, DEFER, or NOT_RUN is closed only by a later PASS for the same Check, Work Unit, and Criteria that explicitly names its Evidence ID. Keep failed rows as history. -->

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-FEATURE-001]({{SPEC_RELATIVE_PATH}}#success-criteria--verification-plan) | WORK-001 | Named deterministic check | Exact revision or fixture | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

<!-- Author prompt: keep exactly one decision row for each assigned Spec criterion. Accepted requires relevant concrete PASS evidence and no unresolved required failure. Pending or rejected retains the current owner and next disposition. Not-required requires an actual Spec scope basis; a Task cannot waive an assigned required criterion by itself. -->

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-FEATURE-001]({{SPEC_RELATIVE_PATH}}#success-criteria--verification-plan) | pending | none | Run named deterministic check | {{OWNER}} |

## Approval and Safety Boundaries

- **Allowed Paths**: `<repository-relative paths>`
- **Forbidden Paths**: `<repository-relative paths or none>`
- **Approval Required**: `<current scoped authorization and protected actions still awaiting approval; use the operator approval route in .agents/governance/approval-and-safety.md>`
- **Static Validation**: `<commands and expected evidence>`
- **Live Validation**: `<approved lane or DEFER with reason>`
- **Secret / Vault Handling**: `<no-read/no-print boundary and owner>`
- **Rollback Plan**: `<reversible steps or commit>`
- **Evidence Location**: `<durable repository path>`

<!-- Author prompt: add GitOps, Kubernetes, or Runbook impact fields only when applicable. -->

<!-- Author prompt: for an actual protected action, record the operator-supplied approving actor, executor, operation, subject/target, reviewed revision/snapshot, original approval reference, validity and current revocation verification under Approval Required. Missing facts mean DEFER for that action. These are non-secret authoring records, never authentication or standing authority. -->

## Verification Summary

<!-- Author prompt: summarize per-lane outcomes, limitations, review disposition, and residual risk. -->
