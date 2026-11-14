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

## Purpose

### Objective

<!-- Author prompt: 정책의 목표와 통제하려는 위험을 사실·가정과 구분해 밝히고 상위 owner는 실제 참조로 연결한다. -->

### Authority

<!-- Author prompt: 정책 소유자와 개정 근거, 권한 경계를 밝히고 규범 문서는 실제 참조로 연결한다. -->

## Scope

### Applies To

<!-- Author prompt: 통제 대상 시스템, 환경, 소비자를 구체적으로 정하고 적용 영역은 실제 참조로 연결한다. -->

### Exclusions

<!-- Author prompt: 제외 대상과 그 대상을 다루는 다른 owner를 밝히거나, 없으면 없다는 사실과 이유를 적는다. -->

## Rules

### Requirements

<!-- Author prompt: 통제의 의도와 책임을 실제 절차와 구분해 적는다. 정책이 규범적 규칙을 진술하면 규칙마다 <CODE>-R<NNN> 형식의 안정적인 ID와 조건, required·recommended·optional 중 하나의 수준을 두고, ID는 규칙의 목록 항목·표 첫 셀·H4 단락 맨 앞에 코드 스팬으로 적는다. -->

<!-- Author prompt: 정책이 규범적 규칙을 진술하면 아래 Rules 표를 유지해 규칙마다 한 행을 두고, 번호는 001부터 빈틈없이 올리며, Status는 active 또는 retired; 뒤에 후속 규칙 ID나 none을 적고, 같은 변경에서 정책의 code를 docs/99.templates/registry.json의 policy_rule_ids에 등록한다. 그렇지 않으면 표를 지운다. -->

| Rule ID | Condition | Level | Evidence | Status |
| --- | --- | --- | --- | --- |
| CODE-R001 | State when the rule applies. | required | Name where compliance is observed. | active |

#### Control Register

| Control | Accountable role | Enforcement surface | Evidence |
| --- | --- | --- | --- |
| CTRL-001 | Accountable role | Validator, review, or platform boundary | Named control evidence |

### Enforcement

<!-- Author prompt: 각 통제의 검사 및 증거와 검토 owner, 변경 트리거, 주기, 폐기 조건을 밝히고 검증 owner는 실제 참조로 연결한다. -->

## Exceptions

### Exception Conditions

<!-- Author prompt: 예외의 근거, 범위, 위험, 만료와 보완 통제를 정하거나, 없으면 없다는 사실과 이유를 적는다. -->

### Approval and Review

<!-- Author prompt: 예외의 승인 주체, 증거, 재검토, 철회와 에스컬레이션 경로를 정하거나, 없으면 없다는 사실과 이유를 적는다. -->

## Ownership

### Responsibilities

<!-- Author prompt: 정책의 작성·검토·승인·실행 책임을 구분해 밝힌다. -->

| Role | Responsibility | Escalation owner |
| --- | --- | --- |
| Accountable role | State one policy responsibility. | Named escalation owner |

### Change and Adoption

<!-- Author prompt: 정책의 판본, 이행, 채택과 드리프트 검증 경로를 밝히거나, 없으면 없다는 사실과 이유를 적는다. -->

### Lifecycle Traceability

<!-- Author prompt: 승격된 권한, 통제 owner, 적용 영역과 집행 표면을 구체적으로 적는다. -->

| Promoted owner | Control owner | Enforcement surface |
| --- | --- | --- |
| Specification or Task owner | Named accountable role | Validator, review, or platform boundary |
