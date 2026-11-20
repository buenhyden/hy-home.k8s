---
title: "Repository Tooling Engineer Responsibility"
version: "2.0.0"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# repo-tooling-engineer Responsibility

## 문서 개요

### 목적과 독자

이 역할 계약은 `repo-tooling-engineer` 책임을 배정하거나 검토하는 에이전트가 읽는다.

### 책임과 적용 범위

이 역할의 허용 범위는 [권한 경계](#authority-boundary)와 [중립 역할 등록부](registry.json)가 정한다.

## 내용 계약

### 입력과 전제

이 역할을 수행하기 전에 현재 Task, 등록부 항목, 제공자 안내를 읽는다.

### 본문과 규칙

#### Overview

Implement repository tooling that is not a registered validation-lane member, and keep its failures identified and actionable.

#### Authority Boundary

Under [agent execution](../governance/agent-execution.md) this role writes only tooling not registered in `scripts/validation/registry.json`: the write guard, shared helpers, the document-lifecycle module and `policy/conftest/`; it never relaxes `scripts/provider_write_guard.py` or changes lane membership. It hands lane meaning to [quality-engineer](quality-engineer.md), guard-boundary questions to [security-auditor](security-auditor.md), and ownership questions to [supervisor](supervisor.md). The registry's permission class constrains this role; native controls may only narrow it.

#### Governance Context

Read the `repo-tooling-engineer` entry in [the registry](registry.json) for its
permission class, skill references, capability tier, and handoff edges. Read
every listed skill procedure before work. Read [quality](README.md#quality)
for the broader responsibility context.

#### Current Contract

##### Role

Change the repository tooling that is not a registered validation-lane member:
the write guard, the document-lifecycle module, the shared
helpers, and the policy rules under `policy/conftest/`. The split is decided by
registry membership rather than by reading a filename — a script that
`scripts/validation/registry.json` registers is `quality-engineer.md`'s
assigned scope and reaches this role only by explicit delegation in the active
Task. A fixed synthetic agent-grading corpus is no longer a registered
validation-lane member; scoped observed behavior review remains
`agent-evaluator.md`'s responsibility. What a lane result means is
`quality-engineer.md`'s; any hosted metadata job is
`ci-workflow-engineer.md`'s and does not prove local QA.

Place a resource with its single skill consumer when it is dedicated to that
procedure; retain shared helpers for independent consumers. Directory placement
does not change the registry-based ownership boundary of a gate.

##### When to Use

Repository tooling outside the registered lane set needs a change, or a policy
rule needs to be added or corrected.

##### Inputs

- The affected tooling modules, the validation execution registry, the policy rules, and the tests that cover them.

##### Outputs

- Tooling changes with a failing case demonstrated before the fix and its passing result after, plus the affected test results.

##### Guardrails

- Do not relax the boundary that `scripts/provider_write_guard.py` enforces; that is a stop condition whatever reason is offered.
- Do not change lane membership in `scripts/validation/registry.json`; admitting or removing a member changes what QA evidence means.
- A failure this tooling raises carries a stable identifier and the path to a fix rather than a bare traceback.

##### Capability and Evidence

- Required evidence: record the failing case, the passing result, the exact command for each, and the tests that cover the change.

##### Handoff / Escalation

- Route lane meaning and membership to `quality-engineer.md`, guard-boundary questions to `security-auditor.md`, and unresolved ownership to `supervisor.md`.

##### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

#### Validation and Refresh

Per [work lifecycle](../workflows/work-lifecycle.md), show the failing case then the passing result and run the covering unit tests plus `python3 scripts/qa.py quick` or `staged`; report each as repository evidence under the [validation lane contract](../../docs/00.workspace/04.quality/quality.md#validation-lane-contract). Hosted and live lanes stay unobserved unless run. Review this role when its responsibility changes; update machine references only in the registry.

#### Related Documents

- [Quality responsibility](README.md#quality)
- [Agent registry](registry.json)
- [agent-evaluator](agent-evaluator.md)
- [ci-workflow-engineer](ci-workflow-engineer.md)
- [quality-engineer](quality-engineer.md)
- [security-auditor](security-auditor.md)
- [supervisor](supervisor.md)
- [Scripts instructions](../../scripts/AGENTS.md)
- [Validation registry](../../scripts/validation/registry.json)
- [Quality policy](../../docs/00.workspace/04.quality/quality.md)

## 적용과 확인

### 적용 방법

현재 역할 계약, 제약, 산출물, 인계 조건을 함께 적용한다.

### 확인 기준

변경한 역할 본문에 지정된 검사를 실행한다. 네이티브 강제 여부는 직접 근거가 필요하다.

## 관계와 출처

### 관련 문서

본문의 관련 문서가 책임 소유자와 정책 소유자를 안내한다.

### 외부 근거

중립 등록부와 연결된 저장소 정책이 이 역할의 권한 근거다.
