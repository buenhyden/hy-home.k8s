---
title: "Shared Memory Meaning"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0232"
---

# Shared Memory Meaning Technical Specification (Spec)

## 문서 개요

### 목적과 독자

This Spec states the P09 change contract for the shared workspace memory and
the promotion of session-analysis candidates into it. The platform owner,
reviewers and implementers use it to judge whether the existing store
exposes the common memory meaning and keeps its writes and promotions atomic
without a new store or search engine.

### 책임과 적용 범위

This Spec owns the P09 behavior and acceptance criteria. The [Plan](plan.md)
owns the work order, risks and rollback, and the
[Task](01.tasks/tsk-0001-shared-memory-meaning.md) owns execution and
evidence.

## 내용 계약

### 입력과 전제

The operator entered `prompts/P09-MEMORY.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-24 at `main@499851eb8e2e5d34ec7f39f984d9d38ae771df65`. Its D09
design and the k8s finding K23-08 keep the existing SQLite store, revision
compare-and-set, idempotency, search, erase and backup, and ask for the
common item and result meaning, typed request digests, the default exclusion
of candidate, retracted and conflicted items, source states, and an atomic
promotion outbox with consistent retry and erase. The live store holds schema
2 with one memory; the live analysis store holds nine candidates.

### 본문과 규칙

#### Overview

##### Goal

Every memory read returns a `common` view next to the existing fields:
identity, scope, kind, state, revision, sensitivity, owner, retention and
each source's path, digest, observation time and status. Default query and
search leave out conflicted items as they already leave out non-current and
stale ones. A request digest refuses non-finite numbers. A session-analysis
promotion is bound to the reviewed content and runs as an outbox.

###### Owning Requirements

[REQ-0003-FR-0022 and FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md)
keep memory apart from Task status and evidence and require one shared
implementation behind thin provider surfaces.
[AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md)
keeps one store per Git common directory; no new architecture decision is
needed.

##### Consumers

`scripts/workspace_memory.py` and its CLI, used by both providers;
`scripts/session_analysis.py` promotion; the
[context and memory policy](../../../.agents/governance/context-and-memory.md).

#### Scope

##### In Scope

- The `common` view, source statuses and conflicted exclusion on reads.
- Typed request digests that refuse non-finite numbers.
- Review receipts and the promotion outbox in the analysis store.
- Regressions, policy text and one live read observation.

##### Out of Scope

A database, search engine or vector store change; CAS, erase or backup
rewrites; a memory schema migration; session content retention and
`content_expired` producers (P10); generation fences (P17); deletion of real
memory content.

#### Behavior Contract

##### Inputs and Outputs

Reads add `open_conflicts` and `common`. The common state maps `current` to
`active`, `candidate` and `needs-review` to `candidate`, `superseded` and
`withdrawn` to `retracted`, and any unresolved conflict at the current
revision to `conflicted`. A source status is `current`, `changed` or
`unavailable`; `content_expired` is reserved. Retention is
`until-approved-erase`. The analysis store gains `review_receipt` and
`promotion` tables through its existing create-if-missing schema.

##### Failure Behavior

A non-finite number fails with `MEMORY_SCHEMA`. A promotion whose candidate
changed after review fails with `ANALYSIS_REVIEW_STALE` and cancels a pending
intent; a review during a pending intent fails with `ANALYSIS_PROMOTING`; an
intent whose memory was erased ends with `ANALYSIS_PROMOTION_ERASED` and
writes nothing.

#### Acceptance Criteria

##### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| AC-0001 | Memory reads return the common view, distinguish current, changed and unavailable sources, and default query and search exclude candidate, retracted, conflicted and stale items unless requested. |
| AC-0002 | Request digests keep typed values distinct and refuse non-finite numbers; the existing CAS, idempotency, capacity and erase behavior is unchanged. |
| AC-0003 | A promotion is bound to the reviewed content, writes one memory across an interruption, never proceeds after a content change and never recreates an erased memory. |

##### Verification Strategy

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-MEMORY | Common view, source states, exclusion and typed digests | Temporary Git repositories | Module behavior only | Every store change | `workspace-memory-regressions` |
| CHK-PROMOTION | Review binding, outbox, retry and erase | Temporary capture, analysis and memory stores | Module behavior only | Every promotion change | `session-analysis-regressions` |
| CHK-LIVE | The live stores read through the changed code | The local live stores | Local read and additive table creation | Once for this change | Task Results |

###### Normative and Evidence

The [context and memory policy](../../../.agents/governance/context-and-memory.md)
owns the store rules (CTX-R012, R014, R015, R021, R023). The package D09
design is a dated input.

###### Historical and Navigation

None apply.

##### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0001 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Memory regressions |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0002 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Memory regressions |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0003 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Analysis regressions |

## 적용과 확인

### 적용 방법

Both providers use the same CLI; the analysis promotion uses the store API.

### 확인 기준

Regressions prove the module behavior; the live observation shows the
changed code reading the local stores.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [Workspace governance requirements](../../01.requirements/0003-workspace-agent-governance-platform.md) |
| designs | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) |

### 외부 근거

The package D09 design and K23-08 are dated inputs; no external standard is
adopted.
