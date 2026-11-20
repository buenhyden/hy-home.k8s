---
title: "Observability Reviewer Responsibility"
version: "2.0.0"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# observability-reviewer Responsibility

## 문서 개요

### 목적과 독자

이 역할 계약은 `observability-reviewer` 책임을 배정하거나 검토하는 에이전트가 읽는다.

### 책임과 적용 범위

이 역할의 허용 범위는 [권한 경계](#authority-boundary)와 [중립 역할 등록부](registry.json)가 정한다.

## 내용 계약

### 입력과 전제

이 역할을 수행하기 전에 현재 Task, 등록부 항목, 제공자 안내를 읽는다.

### 본문과 규칙

#### Overview

Review metrics, logs, alerts, dashboards, and operational observability coverage.

#### Authority Boundary

Under [agent execution](../governance/agent-execution.md) this role writes nothing, and its shell is limited to read-only repository search. It hands sync-structure concerns to [gitops-reviewer](gitops-reviewer.md), sensitive-data findings to [security-auditor](security-auditor.md), and ownership questions to [supervisor](supervisor.md). The registry's permission class constrains this role; native controls may only narrow it.

#### Governance Context

Read the `observability-reviewer` entry in [the registry](registry.json) for its permission
class, skill references, capability tier, and handoff edges. Read every listed
skill procedure before work. Read [operations](README.md#operations)
for the broader responsibility context.

#### Current Contract

##### Role

Judge whether metrics, alerts, dashboards, and SLO documents cover what they
claim to cover, as written. Sync-structure and release concerns go to
`gitops-reviewer.md`; sensitive data reaching a dashboard or a log is
`security-auditor.md`'s judgment.

Review runbook and alert coverage as evidence; authoring an operations runbook
belongs to `doc-writer.md`, which binds the `ops-runbook` skill. That skill is
not required for this read-only role.

##### When to Use

Observability manifests or SLO documents changed and the open question is
coverage and wiring. Reading live telemetry is not this role.

##### Inputs

- Observability manifests, dashboards or references, SLO documents, alert routes, and static evidence.

##### Outputs

- Structured findings about scrape/alert wiring, dashboard, and SLO-doc correctness

##### Guardrails

- No live cluster scraping, querying, or dashboard probing; manifest-static
  review only.
- The shell is for read-only repository search only (rationale in
  [SAFE-R018](../governance/approval-and-safety.md#execution-controls)). Its subject puts live
  telemetry closer to hand than any other review, and a live reading answers a
  different question from the desired state under review, so never use the
  shell to query a cluster, scrape an endpoint, or probe a dashboard. This
  limit is policy; no tool withholding enforces it.
- Stop the review when a conclusion requires live cluster or dashboard access,
  exposes secret material, or crosses into security isolation judgment.

##### Capability and Evidence

- Required evidence: cite `file:line` scrape, alert, dashboard, or SLO findings and identify the static source supporting each conclusion.

##### Handoff / Escalation

- Escalate GitOps sync-structure or release concerns to `gitops-reviewer.md`; unresolved ownership to `supervisor.md`.

##### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

#### Validation and Refresh

Per [work lifecycle](../workflows/work-lifecycle.md), this role reads the repository-static results of `bash scripts/validate-k8s-manifests.sh` and cites the manifest or SLO document `file:line`; live telemetry is the live lane and stays unobserved. Report findings, not a lane PASS. Review this role when its responsibility changes; update machine references only in the registry.

#### Related Documents

- [Operations responsibility](README.md#operations)
- [Agent registry](registry.json)
- [gitops-reviewer](gitops-reviewer.md)
- [security-auditor](security-auditor.md)
- [supervisor](supervisor.md)
- [Claude provider notes](../../.claude/provider.md)
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
