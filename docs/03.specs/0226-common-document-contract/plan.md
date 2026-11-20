---
title: "Common Document Contract Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-11-20"
artifact_id: "SPEC-0226-PLAN-0001"
parent_ids: ["SPEC-0226"]
---

# Common Document Contract Implementation Plan

## 문서 개요

### 목적과 독자

This Plan orders the P04 form, producer and consumer transition for authors,
the Stage 99 owner and validators. It uses the [Spec](spec.md)'s seven criteria.

### 책임과 적용 범위

The Plan owns work order, file responsibility, checks and rollback. The Spec
owns observable behavior. The [Task](01.tasks/tsk-0001-common-document-contract.md)
records what actually ran and the user's later acceptance.

## 내용 계약

### 입력과 전제

The P04 1.1.0 request is current implementation authority. P00–P03 are
predecessors, and the 11 accepted streams are excluded from reimplementation.
The new Spec and this Plan begin as draft; adoption and criterion acceptance
need their own evidence. Existing Stage 99 profiles, the numeric-version
grammar, local `Lifecycle Traceability` rows and native output syntax are
compatibility inputs.

### 본문과 규칙

#### Overview

##### Outcome

Implement [SPEC-0226](spec.md) at each canonical owner and deliver a reviewed
candidate whose template outputs are readable by their real consumers.

##### Constraints

No old evidence cell, accepted retained form or native provider output is
changed merely to satisfy the new envelope. Do not add a universal full-SHA
gate, rename old criterion IDs in isolation, create another workspace ledger or
run external HTTP checks on every commit.

###### Global Constraints

Every work unit inherits the [Spec](spec.md)'s scope, failure behavior and
non-goals. Current [authoring](../../00.workspace/03.process/document-authoring.md)
and [quality](../../00.workspace/04.quality/quality.md) policies govern local
validation and edition changes.

###### Risks and Mitigations

- **Existing readers reject the envelope.** Update generator, parser, profile,
  lifecycle and link consumers with their focused negative tests before the
  final corpus check. A failed consumer blocks delivery.
- **Role meaning or evidence is lost.** Compare role tables, traceability and
  terminal Task evidence before and after; preserve native payload bytes.
- **Adoption is overstated.** Keep unverified approval facts explicit and
  record only the actual local candidate and validation in the Task.

###### Escalation

Stop the affected action if a current authorization conflicts with a protected
owner, a required check remains failing, or actual acceptance requires a
separate user decision. Continue independent in-scope authoring and checks.

#### Dependencies

##### Prerequisites

The user selected only P04 from the package on 2026-11-20. The merged P03
head is `0164ad34`; the Task records the direct read-back. No P05 input is
needed. The selected [Stage 99](../../99.templates/README.md) forms and
current [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
owners govern new documents.

##### Shared Resources

`docs/99.templates/registry.json`, its common forms and the new local common
contract feed the generator and validators. One writer owns each file, with
form authors, tooling authors and QA validators working in distinct paths;
integration checks run after their outputs meet.

#### Work Breakdown

##### Work Units

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [AC-0001](spec.md#criteria), [AC-0002](spec.md#criteria), [AC-0003](spec.md#criteria), [AC-0004](spec.md#criteria), [AC-0005](spec.md#criteria), [AC-0006](spec.md#criteria), [AC-0007](spec.md#criteria) | Bind common contract, migrate forms and current consumers, then validate actual outputs | P03 delivered | [Task](01.tasks/tsk-0001-common-document-contract.md) | Focused regressions, strict corpus, staged and hosted selected checks |

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | Common meanings and envelope have one local production and validation path | P03 | platform | `docs/99.templates/`, current governed documents, `scripts/` readers and generator, `tests/`, this package | AC-0001 to AC-0007 | document registry, generation, lifecycle, links, version and selected CI |

###### Change and Rollback

The implementation, regression and documentation edits form one reviewed
candidate. A normal reviewed revert restores the previous contract and all
its matching consumers; do not restore only the form or only the parser.

##### Dependency Edges

Map existing profiles to common kinds and settle the metadata adapter first.
Then edit forms and generation/readers together, run focused tests and one
related corpus check, review the integrated diff, and deliver through the
selected PR checks. This order creates no approval for a draft contract.

#### Verification Plan

##### Selected Checks

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| document-contract-registry | Forms, profiles and contract binding agree | Candidate Stage 99 | Repository static | Contract and form change | Task Results |
| document-contract-tests | Producers, readers and native-output failures are detected | Changed scripts and fixtures | Synthetic, not provider runtime | Changed executable behavior | Task Results |
| markdown-profiles | Current authored documents use their selected form | Related corpus | Repository static | Global envelope change | Task Results |
| document-lifecycle | State, evidence and identity remain coherent | Candidate tree and base | Repository static | Changed lifecycle/criteria | Task Results |
| links-and-owners | Current local links and moved-target inbound references resolve | Changed and related documents | Repository static | Link/parser change | Task Results |
| qa-staged | Selected checks pass on the exact index | Staged candidate | Repository static | Commit | Task Results |
| pull-request | Selected style and purpose checks pass on the merge candidate | PR cumulative diff | Hosted | PR delivery | PR run and Task Results |

##### Evidence Plan

The Task names each input, tool, command, outcome and limitation. Reuse a
matching prior check only where its input, tool, mode, scope and trust boundary
are unchanged. The one corpus pass verifies this global contract transition;
routine follow-up changes use the existing affected selector.

#### Promotion Map

##### Durable Owners

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| P04-DOCUMENT-FORM | [Document Authoring](../../00.workspace/03.process/document-authoring.md) | Current authoring rule delegates the reviewed common meaning and form to Stage 99 | Current authoring policy and Stage 99 registry/contract |
| P04-DOCUMENT-QUALITY | [Quality](../../00.workspace/04.quality/quality.md) | Selected local and hosted checks cover the actual changed consumers | Current validation registry and PR result |

##### Consumer Updates

Stage 99 keeps exact profile and template routes. Generator, profile, lifecycle
and link readers consume the common contract through one adapter. The Task
records whether each promoted owner actually received its change.

## 적용과 확인

### 적용 방법

Use the real template for each profile; preserve role payload and native
output. Review the final diff, then run required local and hosted checks on
their distinct snapshots.

### 확인 기준

All seven Spec criteria need concrete passing evidence and a separate user
decision before their acceptance is recorded. A merged PR is delivery, not
the missing user decision.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| implements | [Spec](spec.md) |

Navigate to the [Task](01.tasks/tsk-0001-common-document-contract.md),
[Stage 99](../../99.templates/README.md) and
[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md).

### 외부 근거

The supplied D04 design evaluates SemVer, CommonMark, URI and Diátaxis.
Their local application is bounded by this Spec and the current repository
owners; they do not themselves report implementation success.
