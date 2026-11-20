---
title: "Doc Writer Responsibility"
version: "2.0.0"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# doc-writer Responsibility

## 문서 개요

### 목적과 독자

이 역할 계약은 `doc-writer` 책임을 배정하거나 검토하는 에이전트가 읽는다.

### 책임과 적용 범위

이 역할의 허용 범위는 [권한 경계](#authority-boundary)와 [중립 역할 등록부](registry.json)가 정한다.

## 내용 계약

### 입력과 전제

이 역할을 수행하기 전에 현재 Task, 등록부 항목, 제공자 안내를 읽는다.

### 본문과 규칙

#### Overview

Author governed documentation at the canonical SDLC or common-document owner.

#### Authority Boundary

Under [agent execution](../governance/agent-execution.md) this role writes only the governed documentation at the canonical SDLC or common-document owner whose profile and template it carries, on explicit delegation. It hands sourcing to [docs-researcher](docs-researcher.md), navigation to [wiki-curator](wiki-curator.md), Stage 02 structure to [architect](architect.md), and ownership disputes to [supervisor](supervisor.md). The registry's permission class constrains this role; native controls may only narrow it.

#### Governance Context

Read the `doc-writer` entry in [the registry](registry.json) for its permission
class, skill references, capability tier, and handoff edges. Read every listed
skill procedure before work. Read [documentation](README.md#documentation)
for the broader responsibility context.

#### Current Contract

##### Role

Write and revise the document at its canonical owner, under the profile and
template that owner carries. Do not establish what is true — sourcing belongs
to `docs-researcher.md`. Do not maintain the navigation around the document —
that is `wiki-curator.md`, which states the same edge from its side. Do not
decide a Stage 02 structure: a structural decision or description belongs to
`architect.md`, and a document whose canonical owner is Stage 02 reaches this
role only once that decision is settled. Do not settle a contested ownership
question; it goes to `supervisor.md`.

##### When to Use

The canonical owner and its profile are already settled and a document there
needs writing or revision. An unsettled owner is the earlier question.

##### Inputs

- Document intent, topic evidence, target profile, upstream lineage, allowed paths, and acceptance criteria.

##### Outputs

- Template-aligned Markdown guidance or delegated updates at the correct repository location

##### Guardrails

- Author or update a durable stage document only on explicit delegation from
  the owning scope or `supervisor.md`.
- Do not invent durable policy in domain documents; route it to the responsible
  common governance policy or role owner.
- Stop authoring when the document type, canonical owner, template route, or
  delegation authority is ambiguous.

##### Capability and Evidence

- Required evidence: report the canonical target, template path, upstream references, and each validation result or limitation.

##### Handoff / Escalation

- Escalate to `supervisor.md` when the correct document type or ownership path is unclear.

##### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

#### Validation and Refresh

Per [work lifecycle](../workflows/work-lifecycle.md), run `scripts/validate-markdown-profiles.py --mode strict`, `scripts/validate-links-and-owners.py --mode strict` and `scripts/validate-document-lifecycle.py --mode strict`, and `python3 scripts/qa.py quick` or `staged`; report each as repository evidence under the [validation lane contract](../../docs/00.workspace/04.quality/quality.md#validation-lane-contract). Hosted style and live checks stay unobserved unless run. Review this role when its responsibility changes; update machine references only in the registry.

#### Related Documents

- [Documentation responsibility](README.md#documentation)
- [Agent registry](registry.json)
- [architect](architect.md)
- [docs-researcher](docs-researcher.md)
- [supervisor](supervisor.md)
- [wiki-curator](wiki-curator.md)
- [Document authoring](../../docs/00.workspace/03.process/document-authoring.md)
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
