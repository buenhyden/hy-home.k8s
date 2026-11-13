---
title: "{{TITLE}}"
version: "0.1.0"
type: "operation/policy"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "operations"
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

<!-- Author prompt: 통제의 의도와 책임을 실제 절차와 구분해 적고, 규칙마다 안정적인 ID와 조건을 둔다. -->

<!-- Author prompt: 규칙별로 조건과 증거를 나열하는 편이 읽기 쉬울 때만 아래 Rules 표를 사용하고, 그렇지 않으면 표를 지운다. -->

| Rule | Condition | Evidence |
| --- | --- | --- |
| Name one stable rule ID. | State when the rule applies. | Name where compliance is observed. |

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
