---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
artifact_id: "{{ARTIFACT_ID}}"
parent_ids: ["{{PARENT_ID}}"]
---

# Task: [Task Name]

## Scope

### Objective and Parent

<!-- Author prompt: identify the bounded execution stream, its direct Plan and work units, the Spec criteria it serves and its completion evidence. -->

### Inputs and Authority

<!-- Author prompt: link the approved Plan, Spec, decisions, and required evidence inputs, and name the input revision, the allowed files and the authority this Task runs under. -->

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

## Execution Log

### Work Performed

<!-- Author prompt: record the actual change, command, time and owner of each work item; the rows below hold the state of each item, so point to them rather than copy them. -->

### Blockers and Decisions

<!-- Author prompt: record each failure, question, answer and resume condition, or say that none is open. -->

### Lifecycle Traceability

<!-- Author prompt: keep one row per executable item and link each upstream VAL criterion to the owning Spec, using comma-space between links. For exactly one row, write literal frontmatter in its Status cell and put the actual state only in the frontmatter status key. For multiple rows, use actual row states and delete the frontmatter status line; readers derive the summary from the rows. See the document lifecycle policy for the status rules. Result is observed execution outcome; the sole criterion decision belongs under Criterion Decisions. -->

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-FEATURE-001]({{SPEC_RELATIVE_PATH}}#criteria) | One bounded change | {{OWNER}} | frontmatter | NOT_RUN | Pending named repository evidence |

## Verification Evidence

### Results

<!-- Author prompt: record each factual check with an exact input and location; for a command, name it, its tool version, exit code and UTC time when they matter. Required is yes or no. Resolves is none or comma-space separated earlier Evidence IDs. A required FAIL, DEFER, or NOT_RUN is closed only by a later PASS for the same Command, Work Unit, and Consumer that explicitly names its Evidence ID. Keep failed rows as history. -->

<!-- Author prompt: write residue (an open handoff, conflict, adoption or survey item) only in one `### Residue Handoff` table under this section, after the evidence table, with the columns ID, Residue, State, Owner, Resume condition and Closure, and add the matching entry to `docs/03.specs/work-residue-ledger.json` in the same change. State is open or terminal; Closure is none or a PASS Evidence ID of this Task. -->

| Evidence ID | Consumer | Work Unit | Command | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-FEATURE-001]({{SPEC_RELATIVE_PATH}}#criteria) | WORK-001 | Named deterministic check | Exact revision or fixture | NOT_RUN | Pending | yes | none |

### Resolution Links

<!-- Author prompt: say that the Resolves column names the earlier row each PASS row closes, or explain that no earlier failure is open. -->

## Acceptance Decision

### Criterion Decisions

<!-- Author prompt: keep exactly one decision row for each assigned Spec criterion. Accepted requires relevant concrete PASS evidence and no unresolved required failure. Pending or rejected retains the current owner and next disposition. Not-required requires an actual Spec scope basis; a Task cannot waive an assigned required criterion by itself. -->

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-FEATURE-001]({{SPEC_RELATIVE_PATH}}#criteria) | pending | none | Run named deterministic check | {{OWNER}} |

### Remaining Conditions

<!-- Author prompt: name each unrun, unaccepted or operational condition that remains with its owner, or say that none remains. -->

## Handoff

### Promotion Receipt

<!-- Author prompt: record the actual reflection and verification receipt of each Plan promotion row, or say that the Plan promotes none. -->

### Next Owner

<!-- Author prompt: summarize per-lane outcomes, limitations, review disposition and residual risk, and name the next work, the current owner and the resume or exit condition. -->
