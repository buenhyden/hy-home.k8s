---
title: "{{TITLE}}"
version: "0.1.0"
type: "evaluation/task"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
---

# [Evaluation Task]

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Give authors one form for an evaluation task declaration. -->

### 책임과 적용 범위

<!-- 작성 규칙: The task document owns the declared trials and the criteria it fixes before either condition is collected; it does not prove that a provider session ran or that a score is true. -->

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 이 문서를 작성할 때 필요한 실제 입력, 권한과 전제를 밝힌다. -->

### 본문과 규칙

<!-- 작성 규칙: 아래 역할별 절의 내용과 표를 해당 문서의 실제 사실로 채운다. -->

#### Overview

| Field | Declared value |
| --- | --- |
| Cycle ID | {{CYCLE_ID}} |
| Exact task/prompt or immutable source | {{TASK_PROMPT_SOURCE}} |
| Input ID and hash | {{INPUT_ID_AND_HASH}} |
| Baseline input, mode, tool, config and trust source | {{BASELINE_CONDITION_SOURCE}} |
| With-skill input, mode, tool, config and trust source | {{WITH_SKILL_CONDITION_SOURCE}} |
| Skill revision | {{SKILL_REVISION}} |
| Provider and baseline session | {{BASELINE_PROVIDER_SESSION}} |
| Provider and with-skill session | {{WITH_SKILL_PROVIDER_SESSION}} |
| Declared pair count | 1 |

<!-- 작성 규칙: One harness directory is one paired trial. A reevaluation uses a new cycle ID. -->

#### Declared Trials

| Trial ID | Baseline output | With-skill output | Pair status | Partial reason |
| --- | --- | --- | --- | --- |
| {{TRIAL_ID}} | `baseline.md` (NOT_OBSERVED until captured) | `with-skill.md` (NOT_OBSERVED until captured) | pending | {{PARTIAL_REASON}} |

<!-- 작성 규칙: Declare the count before scoring. Link each output only after its file exists. -->

#### Signals and Criteria

| Criterion ID | Observable signal | Scoring rule | Scorer ID |
| --- | --- | --- | --- |
| {{CRITERION_ID}} | {{SIGNAL}} | {{SCORING_RULE}} | {{SCORER_ID}} |

<!-- 작성 규칙: Define each criterion and its observable signal before collecting either condition. -->

#### Human Calibration
<!-- 작성 규칙: Name the reviewer, calibration input and decision boundary before scoring. -->

#### Related Documents
<!-- 작성 규칙: Link the evaluation router and the owner of the evaluated skill. -->

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
