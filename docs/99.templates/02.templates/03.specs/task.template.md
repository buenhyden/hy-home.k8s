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

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Give authors one form for the execution of one Plan work unit set that records its scope and authority, its work and decisions, its observed evidence, its criterion decisions and its handoff. -->

### 책임과 적용 범위

<!-- 작성 규칙: A Task owns the actual execution of the work its Plan orders: the inputs and authority it ran under, what was done and decided, each observed result with its evidence, the decision on each assigned Spec criterion and the residue and next owner it hands off; the change contract stays with the Spec and the work order with the Plan. -->

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 이 문서를 작성할 때 필요한 실제 입력, 권한과 전제를 밝힌다. -->

### 본문과 규칙

<!-- 작성 규칙: 아래 역할별 절의 내용과 표를 해당 문서의 실제 사실로 채운다. -->

#### Scope
##### Objective and Parent
<!-- 작성 규칙: identify the bounded execution stream, its direct Plan and work units, the Spec criteria it serves and its completion evidence. -->

##### Inputs and Authority
<!-- 작성 규칙: link the approved Plan, Spec, decisions, and required evidence inputs, and name the input revision, the allowed files and the authority this Task runs under. -->

- **Allowed Paths**: `<repository-relative paths>`
- **Forbidden Paths**: `<repository-relative paths or none>`
- **Approval Required**: `<current scoped authorization and protected actions still awaiting approval; use the operator approval route in docs/00.workspace/04.quality/approval-and-safety.md>`
- **Static Validation**: `<commands and expected evidence>`
- **Live Validation**: `<approved lane or DEFER with reason>`
- **Secret / Vault Handling**: `<no-read/no-print boundary and owner>`
- **Rollback Plan**: `<reversible steps or commit>`
- **Evidence Location**: `<durable repository path>`

<!-- 작성 규칙: add GitOps, Kubernetes, or Runbook impact fields only when applicable. -->

<!-- 작성 규칙: for an actual protected action, record the operator-supplied approving actor, executor, operation, subject/target, reviewed revision/snapshot, original approval reference, validity and current revocation verification under Approval Required. Missing facts mean DEFER for that action. These are non-secret authoring records, never authentication or standing authority. -->

#### Execution Log
##### Work Performed
<!-- 작성 규칙: record the actual change, command, time and owner of each work item; the rows below hold the state of each item, so point to them rather than copy them. -->

<!-- 작성 규칙: only when the Task tracks more than one item (core condition multiple_items), add the core Work Items table `| Item | Work Unit | Owner | Status | Blocker |` as the first table under Work Performed, one row per Item with its Plan Work Unit, its owner, its status (draft, ready, in-progress, blocked, completed or cancelled) and its Blocker (the block or cancellation reason and next owner, or none), and delete the frontmatter status line; readers derive the summary from these rows. For one item, add no Work Items table: the frontmatter status key holds the state. -->

##### Blockers and Decisions
<!-- 작성 규칙: record each failure, question, answer and resume condition, or say that none is open. -->

##### Lifecycle Traceability
<!-- 작성 규칙: keep one row per executable item, keyed by the Item of its Work Items row or, for one item, by its work unit ID, and link each upstream AC criterion to the owning Spec, using comma-space between links. The status of an item lives in the Work Items table, or in the frontmatter status key for one item. See the document lifecycle policy for the status rules. Result is observed execution outcome; the sole criterion decision belongs under Criterion Decisions. -->

| Item | Upstream criterion | Result | Evidence |
| --- | --- | --- | --- |
| WORK-001 | [AC-0001]({{SPEC_RELATIVE_PATH}}#criteria) | NOT_RUN | Pending named repository evidence |

#### Verification Evidence
##### Results
<!-- 작성 규칙: record each factual check with an exact input and location. Method is automated, review or observation; Tool and Config names the tool, its version and configuration, or none; Exit is the exit code, or none when nothing ran (never 0 for an unrun check). Required is true or false. Resolves is none or comma-space separated earlier Evidence IDs. A required FAIL, DEFER, or NOT_RUN is closed only by a later PASS for the same Command, Work Unit, and Criteria that explicitly names its Evidence ID. Keep failed rows as history. -->

<!-- 작성 규칙: write residue (an open handoff, conflict, adoption or survey item) only in one `### Residue Handoff` table under this section, after the evidence table, with the columns ID, Residue, State, Owner, Resume condition and Closure, and add the matching entry to `docs/03.specs/work-residue-ledger.json` in the same change. State is open or terminal; Closure is none or a PASS Evidence ID of this Task. -->

| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [AC-0001]({{SPEC_RELATIVE_PATH}}#criteria) | WORK-001 | automated | Exact revision or fixture | none | Named deterministic check | none | NOT_RUN | none | true | none |

##### Resolution Links
<!-- 작성 규칙: say that the Resolves column names the earlier row each PASS row closes, or explain that no earlier failure is open. -->

#### Acceptance Decision
##### Criterion Decisions
<!-- 작성 규칙: keep this table when the Task owns the acceptance of its assigned criteria (core condition owns_acceptance), with exactly one decision row for each assigned Spec criterion. An agent never writes an acceptance or an acceptor: until the operator's recorded Decision, Intent is undecided, Acceptance is pending, and Accepted By and Reassigned To are none. Accepted requires relevant concrete PASS evidence and no unresolved required failure. Not-required requires an actual Spec scope basis; a Task cannot waive an assigned required criterion by itself. -->

| Criterion | Intent | Acceptance | Evidence | Decision | Accepted By | Current Owner | Reassigned To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [AC-0001]({{SPEC_RELATIVE_PATH}}#criteria) | undecided | pending | none | none | none | {{OWNER}} | none |

##### Remaining Conditions
<!-- 작성 규칙: name each unrun, unaccepted or operational condition that remains with its owner, or say that none remains. -->

#### Handoff
##### Promotion Receipt
<!-- 작성 규칙: record the actual reflection and verification receipt of each Plan promotion row, or say that the Plan promotes none. -->

##### Next Owner
<!-- 작성 규칙: summarize per-lane outcomes, limitations, review disposition and residual risk, and name the next work, the current owner and the resume or exit condition. -->

## 적용과 확인

### 적용 방법

<!-- 작성 규칙: 실제 사용 방법과 적용 대상을 설명한다. -->

### 확인 기준

<!-- 작성 규칙: 이 문서 유형에 해당하는 확인 방법과 한계를 적는다. -->

## 관계와 출처

### 관련 문서

<!-- 작성 규칙: 현재 정본의 관계와 탐색 링크만 연결한다. 실제 의미 관계가 있으면 Relation에 requires/designs/implements/verifies/operates/defines/cites 중 하나를, Target에 현재 문서의 상대 Markdown 링크 하나를 적는다. 단순 탐색 링크는 표 밖에 둔다. -->

| Relation | Target |
| --- | --- |

### 외부 근거

<!-- 작성 규칙: 외부 근거가 있으면 출처와 채택 범위를 적고, 없으면 그 이유를 명시한다. -->
