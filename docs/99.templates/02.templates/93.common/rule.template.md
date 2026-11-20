---
title: "{{TITLE}}"
version: "0.1.0"
type: "governance/rule"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
---

# [Rule Topic] Policy

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Give authors one form for a governance rule that states one normative rule set with its purpose, scope, requirements, exceptions and ownership. -->

### 책임과 적용 범위

<!-- 작성 규칙: A governance rule owns the rules, their enforcement and the exceptions and ownership of one governed concern; procedures stay with runbooks and explanations with guides. -->

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 이 문서를 작성할 때 필요한 실제 입력, 권한과 전제를 밝힌다. -->

### 본문과 규칙

<!-- 작성 규칙: 아래 역할별 절의 내용과 표를 해당 문서의 실제 사실로 채운다. -->

#### Purpose and Scope
##### Objective
<!-- 작성 규칙: name the governed concern, intended reader, current outcome and the risk the rule controls, and link the canonical upstream owners. -->

##### Applies To
<!-- 작성 규칙: state the decisions, constraints, targets, environments and consumers that shape this rule, and link the downstream owners and navigation entries. -->

###### Exclusions
<!-- 작성 규칙: state what this rule does not cover and which other owner governs it, or state that none exists and why. -->

#### Rules
##### Requirements
<!-- 작성 규칙: write enforceable responsibilities and boundaries for this topic. When the policy states normative rules, give each rule one stable ID of the form <CODE>-R<NNN>, a condition and a level of required, recommended or optional. Write the rule's text in its Rules row; supporting paragraphs, lists and tables stay under an H4 that names the rule with its ID as a code span on a line of its own. -->

<!-- 작성 규칙: when the policy states normative rules, keep the Rules table below with one row per active rule, and the Rule Levels table with one row per issued rule ID, numbers ascending from 001 without a gap, a level and a Status of active or retired; followed by a successor rule ID or none. Register the policy's code in policy_rule_ids of docs/99.templates/registry.json in the same change; otherwise delete both tables. -->

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| CODE-R001 | State when the rule applies. | State what is allowed, required or forbidden. | Name where the rule is enforced, or manual review. | Name how compliance is checked, or none. |

| Rule ID | Level | Status |
| --- | --- | --- |
| CODE-R001 | required | active |

##### Exceptions
<!-- 작성 규칙: state the reason, scope, risk and expiry under which an exception is allowed, or state that none exists and why. -->

###### Approval and Review
<!-- 작성 규칙: state who may approve, verify, re-review or revoke an exception, or state that none exists and why. -->

#### Enforcement
##### Mechanisms
<!-- 작성 규칙: define deterministic checks, manual confirmation, failure handling, refresh triggers and evidence limits, and link the validation owners. -->

##### Limits
<!-- 작성 규칙: state what the enforcement does not cover or guarantee: advisory checks, manual steps, unobserved runtime and residual risk. -->

#### Ownership
##### Owner
<!-- 작성 규칙: name the owner and the basis for amending this rule, distinguish this authority from adjacent contracts and runtime state, and link the normative documents. -->

###### Responsibilities
<!-- 작성 규칙: state who writes, reviews, approves and executes this rule. -->

##### Review Triggers
<!-- 작성 규칙: state the canonical version, migration, adoption and drift verification path, or state that none exists and why. -->

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
