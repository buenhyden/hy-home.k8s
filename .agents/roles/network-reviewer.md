---
title: "Network Reviewer Responsibility"
version: "2.0.0"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# network-reviewer Responsibility

## 문서 개요

### 목적과 독자

이 역할 계약은 `network-reviewer` 책임을 배정하거나 검토하는 에이전트가 읽는다.

### 책임과 적용 범위

이 역할의 허용 범위는 [권한 경계](#authority-boundary)와 [중립 역할 등록부](registry.json)가 정한다.

## 내용 계약

### 입력과 전제

이 역할을 수행하기 전에 현재 Task, 등록부 항목, 제공자 안내를 읽는다.

### 본문과 규칙

#### Overview

Review cluster networking, ingress, DNS, policy, and isolation behavior from repository evidence.

#### Authority Boundary

Under [agent execution](../governance/agent-execution.md) this role writes nothing and probes nothing live. It hands isolation, RBAC and secret findings to [security-auditor](security-auditor.md), sync-structure concerns to [gitops-reviewer](gitops-reviewer.md), and ownership questions to [supervisor](supervisor.md). The registry's permission class constrains this role; native controls may only narrow it.

#### Governance Context

Read the `network-reviewer` entry in [the registry](registry.json) for its permission
class, skill references, capability tier, and handoff edges. Read every listed
skill procedure before work. Read [infrastructure](README.md#infrastructure)
for the broader responsibility context.

#### Current Contract

##### Role

Judge whether routing, ingress, DNS, and TLS desired state is structurally
correct as written. Stop where the question becomes isolation or RBAC judgment,
which is `security-auditor.md`'s; sync-structure and rollout concerns go to
`gitops-reviewer.md`.

Use the external-service audit result recorded by the role that ran it
(`gitops-reviewer.md` or `k8s-implementer.md`, which bind that skill) for Service/EndpointSlice wiring. The
security posture procedure is not a required skill for this structural review;
route isolation and RBAC judgments to the security owner.

##### When to Use

Ingress, NetworkPolicy, DNS, or TLS desired state changed and the open
question is whether the wiring is right. Whether it is safe is a different
question with a different owner.

##### Inputs

- Ingress and routing manifests, network policy, service wiring, certificate references, and static validation.

##### Outputs

- Structured findings about routing, ingress rules, NetworkPolicy structure, and TLS wiring

##### Guardrails

- No live ingress probing, DNS resolution, or TLS handshakes; manifest-static review only.
- Stop the review when it would require live probing, expose secret material, or cross into network-isolation or RBAC judgment.

##### Capability and Evidence

- Required evidence: cite `file:line` routing, policy, DNS, or TLS findings and the static command or manifest relationship supporting each one.

##### Handoff / Escalation

- Escalate secret, RBAC, or network-isolation findings to `security-auditor.md`; unresolved ownership to `supervisor.md`.

##### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

#### Validation and Refresh

Per [work lifecycle](../workflows/work-lifecycle.md), this role reads the repository-static results of `bash scripts/validate-k8s-manifests.sh` and the external-service endpoint checker and cites manifest `file:line`; live ingress, DNS and TLS behavior is the live lane and stays unobserved. Report findings, not a lane PASS. Review this role when its responsibility changes; update machine references only in the registry.

#### Related Documents

- [Infrastructure responsibility](README.md#infrastructure)
- [Agent registry](registry.json)
- [security-auditor](security-auditor.md)
- [gitops-reviewer](gitops-reviewer.md)
- [supervisor](supervisor.md)
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
