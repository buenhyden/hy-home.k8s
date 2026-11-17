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

<!-- Author prompt: only when the Task tracks more than one item (core condition multiple_items), add the core Work Items table `| Item | Work Unit | Owner | Status | Blocker |` as the first table under Work Performed, one row per Item with its Plan Work Unit, its owner, its status (draft, ready, in-progress, blocked, completed or cancelled) and its Blocker (the block or cancellation reason and next owner, or none), and delete the frontmatter status line; readers derive the summary from these rows. For one item, add no Work Items table: the frontmatter status key holds the state. -->

### Blockers and Decisions

<!-- Author prompt: record each failure, question, answer and resume condition, or say that none is open. -->

### Lifecycle Traceability

<!-- Author prompt: keep one row per executable item, keyed by the Item of its Work Items row or, for one item, by its work unit ID, and link each upstream VAL criterion to the owning Spec, using comma-space between links. The status of an item lives in the Work Items table, or in the frontmatter status key for one item. See the document lifecycle policy for the status rules. Result is observed execution outcome; the sole criterion decision belongs under Criterion Decisions. -->

| Item | Upstream criterion | Result | Evidence |
| --- | --- | --- | --- |
| WORK-001 | [VAL-FEATURE-001]({{SPEC_RELATIVE_PATH}}#criteria) | NOT_RUN | Pending named repository evidence |

## Verification Evidence

### Results

<!-- Author prompt: record each factual check with an exact input and location. Method is automated, review or observation; Tool and Config names the tool, its version and configuration, or none; Exit is the exit code, or none when nothing ran (never 0 for an unrun check). Required is true or false. Resolves is none or comma-space separated earlier Evidence IDs. A required FAIL, DEFER, or NOT_RUN is closed only by a later PASS for the same Command, Work Unit, and Criteria that explicitly names its Evidence ID. Keep failed rows as history. -->

<!-- Author prompt: write residue (an open handoff, conflict, adoption or survey item) only in one `### Residue Handoff` table under this section, after the evidence table, with the columns ID, Residue, State, Owner, Resume condition and Closure, and add the matching entry to `docs/03.specs/work-residue-ledger.json` in the same change. State is open or terminal; Closure is none or a PASS Evidence ID of this Task. -->

| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-FEATURE-001]({{SPEC_RELATIVE_PATH}}#criteria) | WORK-001 | automated | Exact revision or fixture | none | Named deterministic check | none | NOT_RUN | none | true | none |

### Resolution Links

<!-- Author prompt: say that the Resolves column names the earlier row each PASS row closes, or explain that no earlier failure is open. -->

## Acceptance Decision

### Criterion Decisions

<!-- Author prompt: keep this table when the Task owns the acceptance of its assigned criteria (core condition owns_acceptance), with exactly one decision row for each assigned Spec criterion. An agent never writes an acceptance or an acceptor: until the operator's recorded Decision, Intent is undecided, Acceptance is pending, and Accepted By and Reassigned To are none. Accepted requires relevant concrete PASS evidence and no unresolved required failure. Not-required requires an actual Spec scope basis; a Task cannot waive an assigned required criterion by itself. -->

| Criterion | Intent | Acceptance | Evidence | Decision | Accepted By | Current Owner | Reassigned To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [VAL-FEATURE-001]({{SPEC_RELATIVE_PATH}}#criteria) | undecided | pending | none | none | none | {{OWNER}} | none |

### Remaining Conditions

<!-- Author prompt: name each unrun, unaccepted or operational condition that remains with its owner, or say that none remains. -->

## Handoff

### Promotion Receipt

<!-- Author prompt: record the actual reflection and verification receipt of each Plan promotion row, or say that the Plan promotes none. -->

### Next Owner

<!-- Author prompt: summarize per-lane outcomes, limitations, review disposition and residual risk, and name the next work, the current owner and the resume or exit condition. -->
