---
title: "{{TITLE}}"
version: "0.1.0"
type: "operation/policy"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
artifact_id: "{{ARTIFACT_ID}}"
---

# [Policy or Standard Name] Operations Policy

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Give authors one form for a operations policy that states one normative rule set with its purpose, scope, requirements, exceptions and ownership. -->

### 책임과 적용 범위

<!-- 작성 규칙: A operations policy owns the rules, their enforcement and the exceptions and ownership of one governed concern; procedures stay with runbooks and explanations with guides. -->

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 이 문서를 작성할 때 필요한 실제 입력, 권한과 전제를 밝힌다. -->

### 본문과 규칙

<!-- 작성 규칙: 아래 역할별 절의 내용과 표를 해당 문서의 실제 사실로 채운다. -->

#### Purpose and Scope
##### Objective
<!-- 작성 규칙: 정책의 목표와 통제하려는 위험을 사실·가정과 구분해 밝히고 상위 owner는 실제 참조로 연결한다. -->

##### Applies To
<!-- 작성 규칙: 통제 대상 시스템, 환경, 소비자를 구체적으로 정하고 적용 영역은 실제 참조로 연결한다. -->

###### Exclusions
<!-- 작성 규칙: 제외 대상과 그 대상을 다루는 다른 owner를 밝히거나, 없으면 없다는 사실과 이유를 적는다. -->

#### Rules
##### Requirements
<!-- 작성 규칙: 통제의 의도와 책임을 실제 절차와 구분해 적는다. 정책이 규범적 규칙을 진술하면 규칙마다 <CODE>-R<NNN> 형식의 안정적인 ID와 조건, required·recommended·optional 중 하나의 수준을 두고, 규칙의 내용은 Rules 표의 행에 적는다. 보충 단락·목록·표는 규칙 ID를 코드 스팬 한 줄로 둔 H4 아래에 둔다. -->

<!-- 작성 규칙: 정책이 규범적 규칙을 진술하면 아래 Rules 표에 현재 규칙마다 한 행을, Rule Levels 표에 발급한 규칙 ID마다 한 행을 두고, 번호는 001부터 빈틈없이 올리며, 수준과 Status(active 또는 retired; 뒤에 후속 규칙 ID나 none)를 적는다. 같은 변경에서 정책의 code를 docs/99.templates/registry.json의 policy_rule_ids에 등록한다. 그렇지 않으면 두 표를 지운다. -->

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| CODE-R001 | State when the rule applies. | State what is allowed, required or forbidden. | Name where the rule is enforced, or manual review. | Name how compliance is checked, or none. |

| Rule ID | Level | Status |
| --- | --- | --- |
| CODE-R001 | required | active |

###### Control Register

| Control | Accountable role | Enforcement surface | Evidence |
| --- | --- | --- | --- |
| CTRL-001 | Accountable role | Validator, review, or platform boundary | Named control evidence |

##### Exceptions
<!-- 작성 규칙: 예외의 근거, 범위, 위험, 만료와 보완 통제를 정하거나, 없으면 없다는 사실과 이유를 적는다. -->

###### Approval and Review
<!-- 작성 규칙: 예외의 승인 주체, 증거, 재검토, 철회와 에스컬레이션 경로를 정하거나, 없으면 없다는 사실과 이유를 적는다. -->

#### Enforcement
##### Mechanisms
<!-- 작성 규칙: 각 통제의 검사 및 증거와 검토 owner, 변경 트리거, 주기, 폐기 조건을 밝히고 검증 owner는 실제 참조로 연결한다. -->

##### Limits
<!-- 작성 규칙: 집행이 다루거나 보장하지 않는 것을 적는다: 권고성 검사, 수동 단계, 관측하지 않은 런타임과 잔여 위험. -->

#### Ownership
##### Owner
<!-- 작성 규칙: 정책 소유자와 개정 근거, 권한 경계를 밝히고 규범 문서는 실제 참조로 연결한다. -->

###### Responsibilities
<!-- 작성 규칙: 정책의 작성·검토·승인·실행 책임을 구분해 밝힌다. -->

| Role | Responsibility | Escalation owner |
| --- | --- | --- |
| Accountable role | State one policy responsibility. | Named escalation owner |

##### Review Triggers
<!-- 작성 규칙: 정책의 판본, 이행, 채택과 드리프트 검증 경로를 밝히거나, 없으면 없다는 사실과 이유를 적는다. -->

##### Lifecycle Traceability
<!-- 작성 규칙: 승격된 권한, 통제 owner, 적용 영역과 집행 표면을 구체적으로 적는다. -->

| Promoted owner | Control owner | Enforcement surface |
| --- | --- | --- |
| Specification or Task owner | Named accountable role | Validator, review, or platform boundary |

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
