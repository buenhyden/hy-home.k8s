---
title: "Wiki Curator Responsibility"
version: "2.0.0"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# wiki-curator Responsibility

## 문서 개요

### 목적과 독자

이 역할 계약은 `wiki-curator` 책임을 배정하거나 검토하는 에이전트가 읽는다.

### 책임과 적용 범위

이 역할의 허용 범위는 [권한 경계](#authority-boundary)와 [중립 역할 등록부](registry.json)가 정한다.

## 내용 계약

### 입력과 전제

이 역할을 수행하기 전에 현재 Task, 등록부 항목, 제공자 안내를 읽는다.

### 본문과 규칙

#### Overview

Maintain knowledge navigation and canonical links without creating duplicate policy authority.

#### Authority Boundary

Under [agent execution](../governance/agent-execution.md) this role writes only navigation: entry-point READMEs, index rows and the owner maps under `.agents/knowledge/` (not `glossary.md`, which [doc-writer](doc-writer.md) writes), never policy or generated artifacts. It hands new durable documents to [doc-writer](doc-writer.md) and contested ownership to [supervisor](supervisor.md). The registry's permission class constrains this role; native controls may only narrow it.

#### Governance Context

Read the `wiki-curator` entry in [the registry](registry.json) for its permission
class, skill references, capability tier, and handoff edges. Read every listed
skill procedure before work. Read [documentation](README.md#documentation)
for the broader responsibility context.

#### Current Contract

##### Role

Keep the entry points and hand-maintained owner maps pointing at the current
canonical owners, and keep the Repository Vocabulary reachable from the knowledge index. No generator writes to that surface, and the retired
generated index is not recreated. Write navigation, never policy: when the answer needs a
durable document rather than a better route, that is `doc-writer.md`'s work,
and a contested ownership question goes to `supervisor.md`.

Apply the current document-authoring boundary to outside-doc navigation: route
to current owners or stage README indexes. Check observation metadata and
invalidation without promoting it into policy or a progress ledger.

##### When to Use

The owner of a subject is hard to find, or an index has drifted from what it
indexes. Producing the document the index points at is a different role.

##### Inputs

- Canonical owner paths, current taxonomy, owner-map and stage README index rows, stale-link evidence, and delegated scope.

##### Outputs

- Updated navigation entry points, index rows, and cross-links at their
  canonical owners, with each stale route classified rather than silently
  rewritten

##### Guardrails

- Do not create vector stores, embeddings, retrieval services, runtime caches, package manifests, lockfiles, or static wiki site artifacts.
- Stop curation when ownership is ambiguous, content would duplicate a canonical contract, or the request requires a new runtime or generated artifact.

##### Capability and Evidence

- Required evidence: identify each changed entrypoint, canonical owner target, stale-link result, and the link/owner and knowledge-surface validator results.

##### Handoff / Escalation

- Escalate to `doc-writer.md` when a new operations guide, runbook, incident note, or template-aligned document is needed.

##### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

#### Validation and Refresh

Per [work lifecycle](../workflows/work-lifecycle.md), run `python3 scripts/validate-knowledge-surface.py`, `scripts/validate-links-and-owners.py --mode strict` and `scripts/validate-markdown-profiles.py --mode strict`; report each as repository evidence under the [validation lane contract](../../docs/00.workspace/04.quality/quality.md#validation-lane-contract). Hosted and live lanes are not observed by this role. Review this role when its responsibility changes; update machine references only in the registry.

#### Related Documents

- [Documentation responsibility](README.md#documentation)
- [Agent registry](registry.json)
- [doc-writer](doc-writer.md)
- [supervisor](supervisor.md)
- [Knowledge maps](../knowledge/README.md)
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
