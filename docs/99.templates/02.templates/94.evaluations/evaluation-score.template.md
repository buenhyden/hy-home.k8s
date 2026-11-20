---
title: "{{TITLE}}"
version: "0.1.0"
type: "evaluation/score"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
---

# [Evaluation Score]

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Give authors one form for a score for one paired trial. -->

### 책임과 적용 범위

<!-- 작성 규칙: The score document owns the observed hashes, signals and scores of one paired trial; it does not prove that a provider session ran or that a score is true. -->

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 이 문서를 작성할 때 필요한 실제 입력, 권한과 전제를 밝힌다. -->

### 본문과 규칙

<!-- 작성 규칙: 아래 역할별 절의 내용과 표를 해당 문서의 실제 사실로 채운다. -->

#### Overview

| Field | Observed value |
| --- | --- |
| Cycle ID and trial ID | {{CYCLE_AND_TRIAL_ID}} |
| Task declaration | `task.md` (link after the instance exists) |
| Grader ID and revision | {{GRADER_ID_AND_REVISION}} |
| Granularity | one paired trial |
| Declared pair count | 1 (from `task.md`) |
| Observed complete pair count | {{OBSERVED_PAIR_COUNT}} |
| Input ID and hash | {{INPUT_ID_AND_HASH}} |
| Partial reason | {{PARTIAL_REASON}} |

<!-- 작성 규칙: A document and a score do not prove a provider session ran. -->

#### Trial Evidence

| Trial ID | Baseline output and hash | With-skill output and hash | Session references | Evidence status |
| --- | --- | --- | --- | --- |
| {{TRIAL_ID}} | `baseline.md` {{BASELINE_SHA256}} | `with-skill.md` {{WITH_SKILL_SHA256}} | {{SESSION_REFERENCES}} | incomplete |

<!-- 작성 규칙: Record actual output hashes and session references; leave a missing condition incomplete. -->

#### Criterion Scores

| Trial ID | Criterion ID | Baseline observed signal and raw locator | With-skill observed signal and raw locator | Baseline score | With-skill score |
| --- | --- | --- | --- | --- | --- |
| {{TRIAL_ID}} | {{CRITERION_ID}} | {{BASELINE_SIGNAL_AND_LOCATOR}} | {{WITH_SKILL_SIGNAL_AND_LOCATOR}} | pending | pending |

<!-- 작성 규칙: Link an output only after it exists; score actual pairs using task.md criteria. -->

#### Human Calibration
<!-- 작성 규칙: Record the observed calibration decision and any unresolved disagreement. -->

#### Related Documents
<!-- 작성 규칙: Link task.md and the evaluation router. -->

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
