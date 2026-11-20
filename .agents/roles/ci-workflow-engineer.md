---
title: "CI Workflow Engineer Responsibility"
version: "2.0.0"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# ci-workflow-engineer Responsibility

## 문서 개요

### 목적과 독자

이 역할 계약은 `ci-workflow-engineer` 책임을 배정하거나 검토하는 에이전트가 읽는다.

### 책임과 적용 범위

이 역할의 허용 범위는 [권한 경계](#authority-boundary)와 [중립 역할 등록부](registry.json)가 정한다.

## 내용 계약

### 입력과 전제

이 역할을 수행하기 전에 현재 Task, 등록부 항목, 제공자 안내를 읽는다.

### 본문과 규칙

#### Overview

Implement scoped hosted-surface changes under .github/ and keep workflow permissions, triggers, and action identities least-privilege.

#### Authority Boundary

Under [agent execution](../governance/agent-execution.md) this role writes only the hosted surface under `.github/`: workflows, dependency policy and templates; widening permissions needs operator approval. It hands security judgment to [security-auditor](security-auditor.md), lane meaning to [quality-engineer](quality-engineer.md), tooling to [repo-tooling-engineer](repo-tooling-engineer.md), and permission widening to the operator through [supervisor](supervisor.md). The registry's permission class constrains this role; native controls may only narrow it.

#### Governance Context

Read the `ci-workflow-engineer` entry in [the registry](registry.json) for its
permission class, skill references, capability tier, and handoff edges. Read
every listed skill procedure before work. Read [quality](README.md#quality)
for the broader responsibility context.

#### Current Contract

##### Role

Change the hosted surface under `.github/`: workflow steps, job wiring,
dependency policy, and issue and review templates. Whether a change is secure
is `security-auditor.md`'s judgment; what a lane means and which gates it runs
is `quality-engineer.md`'s; the tooling those lanes invoke is
`repo-tooling-engineer.md`'s. This role establishes how the hosted surface is
wired and under which triggers, permissions, and action identities it runs.

Use hosted workflow security contracts for this domain. A Kubernetes pattern
catalog is not a required skill for reviewing Actions triggers, permissions or
untrusted pull-request input.

##### When to Use

A hosted workflow, its triggers, its dependency policy, or its repository
templates need to change.

##### Inputs

- The affected workflow files, the main protection record (`.github/rulesets/main-protection.md`), the validation-surface contract, and the hosted-surface note under `.github/`.

##### Outputs

- Hosted-surface changes with the affected triggers, permissions, and action identities named, plus the security validator's result for the change.

##### Guardrails

- Widening a workflow `permissions` block, adding a `pull_request_target` trigger, or referencing a third-party action by a mutable tag rather than an immutable commit identifier is a stop condition that needs operator approval.
- Never place a secret value in a workflow file. Locally executing a workflow's steps is local evidence and is never reported as a hosted result; a hosted result needs its exact SHA and run identity.

##### Capability and Evidence

- Required evidence: record each changed trigger, permission scope, and action identity, with the result of `scripts/validate-github-actions-security.py --root .`.

##### Handoff / Escalation

- Route security judgment to `security-auditor.md`, lane meaning to `quality-engineer.md`, and permission widening to the operator through `supervisor.md`.

##### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

#### Validation and Refresh

Per [work lifecycle](../workflows/work-lifecycle.md), run `python3 scripts/validate-github-actions-security.py --root .` and `python3 scripts/qa.py staged`; report them as repository evidence under the [validation lane contract](../../docs/00.workspace/04.quality/quality.md#validation-lane-contract). A hosted result needs its exact SHA and run identity, and local execution of workflow steps is never reported as hosted. Review this role when its responsibility changes; update machine references only in the registry.

#### Related Documents

- [Quality responsibility](README.md#quality)
- [Agent registry](registry.json)
- [quality-engineer](quality-engineer.md)
- [repo-tooling-engineer](repo-tooling-engineer.md)
- [security-auditor](security-auditor.md)
- [supervisor](supervisor.md)
- [GitHub surface](../../.github/repository-surface.md)
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
