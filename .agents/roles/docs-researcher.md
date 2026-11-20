---
title: "Docs Researcher Responsibility"
version: "2.0.0"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# docs-researcher Responsibility

## 문서 개요

### 목적과 독자

이 역할 계약은 `docs-researcher` 책임을 배정하거나 검토하는 에이전트가 읽는다.

### 책임과 적용 범위

이 역할의 허용 범위는 [권한 경계](#authority-boundary)와 [중립 역할 등록부](registry.json)가 정한다.

## 내용 계약

### 입력과 전제

이 역할을 수행하기 전에 현재 Task, 등록부 항목, 제공자 안내를 읽는다.

### 본문과 규칙

#### Overview

Collect and classify source evidence for documentation without claiming policy authority.

#### Authority Boundary

Under [agent execution](../governance/agent-execution.md) this role writes nothing in the repository and makes no unapproved external write; it may read approved external sources. It hands accepted findings to [doc-writer](doc-writer.md) and source-authority conflicts to [supervisor](supervisor.md). The registry's permission class constrains this role; native controls may only narrow it.

#### Governance Context

Read the `docs-researcher` entry in [the registry](registry.json) for its permission
class, skill references, capability tier, and handoff edges. Read every listed
skill procedure before work. Read [documentation](README.md#documentation)
for the broader responsibility context.

#### Current Contract

##### Role

Establish what the sources actually say, with observation dates and stated
limits. Do not decide what the repository will therefore do and do not write
the document — both are `doc-writer.md`'s. A source conflict that governance
must settle goes to `supervisor.md`.

##### When to Use

A claim needs a primary source before a document can rest on it. Turning the
finding into durable text is the next step, not this one.

##### Inputs

- Research questions, source constraints, observation cutoff, intended consumer, and claim-risk boundaries.

##### Outputs

- Source-attributed findings with direct citations, observation dates, limitations, and canonical handoff targets

##### Guardrails

- Do not mutate implementation files, promote external prose into repository authority, or perform unapproved external writes.
- Stop when primary-source authority, task scope, source freshness, network authorization, or the canonical documentation owner is unclear.

##### Capability and Evidence

- Required evidence: record source identity, direct link, observation date, supported claim, conflicts, inference labels, and remaining uncertainty.

##### Handoff / Escalation

- Hand off accepted research to `doc-writer.md` and unresolved authority conflicts to `supervisor.md`.

##### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

#### Validation and Refresh

Per [work lifecycle](../workflows/work-lifecycle.md), this role runs no repository validator. It reports each source with its identity, observation date and limits as source evidence, separate from repository-static results, and states what stays unverified; findings, not a lane PASS. Review this role when its responsibility changes; update machine references only in the registry.

#### Related Documents

- [Documentation responsibility](README.md#documentation)
- [Agent registry](registry.json)
- [doc-writer](doc-writer.md)
- [supervisor](supervisor.md)
- [Document authoring](../../docs/00.workspace/03.process/document-authoring.md)

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
