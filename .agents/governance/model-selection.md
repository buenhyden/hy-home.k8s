---
title: "Model Selection Policy"
version: "2.0.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# Model Selection Policy

## 문서 개요

### 목적과 독자

Workers and reviewers use Model Selection Policy for the rules in its stated scope.

### 책임과 적용 범위

The policy's coverage is defined in [Purpose and Scope](#purpose-and-scope) and [Applies To](#applies-to).

## 내용 계약

### 입력과 전제

Read the current request, owner and rule conditions before applying this policy.

### 본문과 규칙

#### Purpose and Scope

##### Objective

Use capability appropriate to the task without turning model age, role names,
or static configuration into claims of observed fitness.

##### Applies To

Capability, permissions, and responsibility are independent. Escalating a
bounded task to a stronger permitted model does not grant new tools, writes,
delegation, or approval, and does not change the role's registry membership.

###### Exclusions

This policy excludes no subject within its scope; if one is excluded, name it and its owner here.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| MODEL-R001 | For high-risk synthesis, orchestration, or complex security and incident judgment | Use the strongest permitted capability for high-risk synthesis, orchestration, or complex security and incident judgment. The stable anchor is `#top`; resolve membership from the registry rather than inferring it from a role name. | `agent-governance` | none |
| MODEL-R002 | For focused implementation, documentation, validation, or review | Use a bounded capable model for focused implementation, documentation, validation, or review. The stable anchor is `#worker`; a difficult assignment may justify explicit escalation. | `agent-governance` | none |
| MODEL-R003 | Always | Capability selection carries a spend and latency boundary as well as a quality one. Keep a bounded task on the worker tier and state the expected cost boundary when escalating. Prefer one focused delegation over a broad sweep: each concurrent worker carries its own context window, so cost scales with the number of active workers rather than with the size of the work. | Semantic review | none |
| MODEL-R004 | During a documentation or routing change | Preserve configured native model and effort values during a documentation or routing change. Model promotion requires separately authorized scope and task-relevant evidence. The neutral registry names a tier and class; each provider binding table maps that tier to its model and effort and records any role-specific native departure. Projections remain checked consumers, not another authoring location. | `agent-governance` | none |
| MODEL-R005 | When a model or effort change is actually requested | Shared reasoning intent is not a universal provider enum. Check the intended client's supported native configuration when a model or effort change is actually requested. | Semantic review | none |
| MODEL-R006 | Always | Record the selection rationale, expected quality/cost boundary, and any unavailable runtime verification in the owning Task. | Semantic review | none |
| MODEL-R007 | Always | Do not maintain dated per-model fitness snapshots, branch pins, or copied role censuses as current policy. Evidence belongs to its dated owner. | Semantic review | none |

| Rule ID | Level | Status |
| --- | --- | --- |
| MODEL-R001 | required | active |
| MODEL-R002 | required | active |
| MODEL-R003 | required | active |
| MODEL-R004 | required | active |
| MODEL-R005 | required | active |
| MODEL-R006 | required | active |
| MODEL-R007 | required | active |

###### Top

`MODEL-R001`

###### Worker

`MODEL-R002`

###### Cost and throughput

`MODEL-R003`

Usage windows, rate limits and per-request budgets belong to the provider
account, not to this repository. Repository-static checks do not establish
them; an authorized provider response may establish an observed limit or
`Retry-After` for that actual request. When a real limit interrupts dependent
work, record the response, remaining scope and next owner in the Task.

Use only an available, permitted model. An unsupported or rejected model is
DEFER for that dependent selection until an authorized supported choice is
established. Deadlines, timeboxes, allocations and reserves are governed by
[quality](../../docs/00.workspace/04.quality/quality.md#validation-runner-envelope). Respect actual cancellation,
observed account/request limits and technical process bounds; honor an actual
`Retry-After` when the authorized request can resume, otherwise defer that
request and continue independent local work. Never silently choose a more
expensive fallback. Unknown cost, RPM, TPM and subscription/API limits are
unverified, not an invented task-wide stop or a claim of native enforcement.

###### Selection and escalation

- `MODEL-R004`
- `MODEL-R005`
- `MODEL-R006`
- `MODEL-R007`

##### Exceptions

Exception and escalation conditions are stated under Requirements.

###### Approval and Review

This policy defines no exception approval or review step of its own; the approval and safety policy's operator approval route applies. If it needs its own, state it here.

#### Enforcement

##### Mechanisms

Validate registry tier references, native binding tables, neutral permission
ceilings and provider projections after changes.
Assess model behavior with authorized, secret-free task evidence before
claiming improved fitness.

##### Limits

The enforcement checks cover registry tier references, native binding tables, permission ceilings and provider projections. Escalating a bounded task to a stronger permitted model does not grant new tools, writes, delegation or approval, and improved model fitness is not claimed without authorized, secret-free task evidence.

#### Ownership

##### Owner

The [agent registry](../roles/registry.json) owns each role's
capability-tier reference and neutral permission class. This policy defines
the tier meanings and escalation boundary. The native binding tables at
`.claude/bindings.json` and `.codex/bindings.json` own their respective
configured model, reasoning and permission values. Role projections consume
those tables under the neutral class ceiling; neither table nor projection
proves availability, entitlement, resolution or execution.

- [Agent Registry](../roles/registry.json)
- [Codex Provider](../../.codex/provider.md)
- [Claude Provider](../../.claude/provider.md)
- [Quality Policy](../../docs/00.workspace/04.quality/quality.md)

###### Responsibilities

Responsibilities are stated under Owner and Requirements.

##### Review Triggers

Change and adoption conditions are stated under Enforcement.

## 적용과 확인

### 적용 방법

Apply the rule, enforcement and exception clauses in the payload together.

### 확인 기준

Check named enforcement on actual input and report its evidence level accurately.

## 관계와 출처

### 관련 문서

The ownership and related documents in the payload link adjacent owners.

### 외부 근거

Repository decisions and cited sources support these rules; external sources alone grant no authority.
