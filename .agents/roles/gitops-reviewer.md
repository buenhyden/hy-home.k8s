---
title: "Gitops Reviewer Responsibility"
version: "2.0.0"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# gitops-reviewer Responsibility

## 문서 개요

### 목적과 독자

이 역할 계약은 `gitops-reviewer` 책임을 배정하거나 검토하는 에이전트가 읽는다.

### 책임과 적용 범위

이 역할의 허용 범위는 [권한 경계](#authority-boundary)와 [중립 역할 등록부](registry.json)가 정한다.

## 내용 계약

### 입력과 전제

이 역할을 수행하기 전에 현재 Task, 등록부 항목, 제공자 안내를 읽는다.

### 본문과 규칙

#### Overview

Review GitOps manifests and reconciliation behavior without assuming mutation authority.

#### Authority Boundary

Under [agent execution](../governance/agent-execution.md) this role writes nothing and mutates no cluster. It hands manifest repair to [k8s-implementer](k8s-implementer.md), secret or privilege findings to [security-auditor](security-auditor.md), and ownership questions to [supervisor](supervisor.md). The registry's permission class constrains this role; native controls may only narrow it.

#### Governance Context

Read the `gitops-reviewer` entry in [the registry](registry.json) for its permission
class, skill references, capability tier, and handoff edges. Read every listed
skill procedure before work. Read [infrastructure](README.md#infrastructure)
for the broader responsibility context.

#### Current Contract

##### Role

Judge whether a desired-state change reconciles safely: sync targets, Kustomize
structure, and rollout behavior. Repairing what the review finds is
`k8s-implementer.md`'s work, and a secret or privilege finding is
`security-auditor.md`'s judgment. This role changes nothing itself.

##### When to Use

A manifest or Kustomize change is ready and the open question is whether Argo CD
will apply it the way the change intends.

##### Inputs

- Changed desired-state paths, rendered or static output, application hierarchy, and release constraints.

##### Outputs

- Structured findings about sync targets, Kustomize layout, and release risk

##### Guardrails

- Enforce GitOps-first boundaries; no direct cluster mutation is allowed in this role.
- Stop the review when a sync target is missing or ambiguous, rollout safety cannot be established, or a sensitive-data boundary is crossed.

##### Capability and Evidence

- Required evidence: identify each affected sync target, Kustomize path, rollout risk, and repository-backed validation result.

##### Handoff / Escalation

- Escalate implementation tasks to `k8s-implementer.md`; unresolved ownership to `supervisor.md`.

##### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

#### Validation and Refresh

Per [work lifecycle](../workflows/work-lifecycle.md), read the results of `bash scripts/validate-k8s-manifests.sh` and the external-service endpoint checker (`.agents/skills/external-service-contract-audit/scripts/validate-service-endpoints.py --root .`) as repository-static evidence; a live Argo CD sync is the live lane and stays unobserved. Report findings, not a lane PASS. Review this role when its responsibility changes; update machine references only in the registry.

#### Related Documents

- [Infrastructure responsibility](README.md#infrastructure)
- [Agent registry](registry.json)
- [k8s-implementer](k8s-implementer.md)
- [security-auditor](security-auditor.md)
- [supervisor](supervisor.md)
- [GitOps tree](../../gitops/README.md)
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
