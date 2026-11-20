---
title: "{{TITLE}}"
version: "0.1.0"
type: "governance/skill"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
---

# [Workflow Name]

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Give authors one form for a common workflow that states when it applies, its ordered procedure, its inputs and outputs, and how it is checked and handed off. -->

### 책임과 적용 범위

<!-- 작성 규칙: A workflow under .agents/workflows/ owns one invoked procedure and its own authority boundary as a registered local heading; policy, role and skill authority stay with their owners and are linked, not copied. -->

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 이 문서를 작성할 때 필요한 실제 입력, 권한과 전제를 밝힌다. -->

### 본문과 규칙

<!-- 작성 규칙: 아래 역할별 절의 내용과 표를 해당 문서의 실제 사실로 채운다. -->

#### Trigger
##### When to Use
<!-- 작성 규칙: state the input, the purpose and the trigger that make this procedure apply, and link the owners it relies on. -->

###### Inputs
<!-- 작성 규칙: list the documents, data and approvals the procedure reads, and link their owners. -->

##### When Not to Use
<!-- 작성 규칙: state the cases and standing rules that exclude this procedure and name the procedure or owner to use instead. -->

##### Authority Boundary
<!-- 작성 규칙: optional. State that this workflow applies existing policy and grants no new scope, only when it states its own authority boundary; otherwise delete this section. -->

#### Procedure
##### Steps
<!-- 작성 규칙: write the ordered steps with their gates and stop conditions, and add no step beyond the owning policy. -->

<!-- 작성 규칙: use the Steps table below only when listing each step with its input and output helps the reader; otherwise delete the table. -->

| Step | Input | Output |
| --- | --- | --- |
| Name one stable step number or name. | State what the step reads or needs. | State what the step produces or records. |

##### Failure Handling
<!-- 작성 규칙: state how to stop, recover or escalate when a step fails, or state that the procedure names none. -->

#### Outputs
##### Artifacts
<!-- 작성 규칙: list what the procedure produces or records and where the result is kept. -->

##### Handoff
<!-- 작성 규칙: state when the procedure is complete, what is recorded, and who owns the next step. -->

#### Verification
##### Checks
<!-- 작성 규칙: list the checks that show the procedure was followed, with their exact commands and pass and fail meaning. -->

##### Limits
<!-- 작성 규칙: state what the checks and outputs of this skill do not establish, using only facts from this skill. -->

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
