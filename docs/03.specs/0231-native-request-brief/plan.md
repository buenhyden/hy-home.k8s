---
title: "Native Request Brief Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0231-PLAN-0001"
parent_ids: ["SPEC-0231"]
---

# Native Request Brief Implementation Plan

## 문서 개요

### 목적과 독자

This Plan orders the P08 request brief for [SPEC-0231](spec.md). The
platform owner and reviewers use it to follow the work unit, its checks and
its rollback.

### 책임과 적용 범위

This Plan owns the work order, risks, rollback and promotion. The Spec owns
the change contract and the [Task](01.tasks/tsk-0001-native-request-brief.md)
owns execution and evidence.

## 내용 계약

### 입력과 전제

The inputs are the P08 request recorded in the Spec, the current shared
write guard, both provider hook registrations and the installed Claude Code
and Codex clients.

### 본문과 규칙

#### Overview

##### Outcome

WORK-001 delivers the request brief module, the intake adapters and
registrations, first-change admission in the shared write guard, their
regressions and one native observation per provider. The worker handoff
check, review routes and other workspaces stay unchanged.

##### Constraints

The change stays within [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md):
the shared write guard remains the one pre-action boundary and the provider
directories hold thin adapters only.

###### Global Constraints

Every unit inherits the [Spec](spec.md#scope) scope. No approval step is
added for clear work, and no refusal is bypassed to finish an observation.

###### Risks and Mitigations

| Risk | Mitigation | Owner |
| --- | --- | --- |
| A failed intake leaves an older admitted receipt in place | Each prompt replaces the receipt; a failed intake is recorded as residual | platform |
| Codex runs the new entry only after the user trusts it | The existing pre-tool entry is unchanged; the user reviews the new entry in `/hooks` | operator |
| A shell write the guard does not detect passes ungated | Documented as outside the boundary; structured writes and patches are gated | platform |

###### Escalation

Stop if a provider refuses the hook or the user review is unavailable, and
record that surface as unobserved.

#### Dependencies

##### Prerequisites

The installed clients, the pinned validation environment and the user for
the native observation.

##### Shared Resources

`scripts/provider_write_guard.py` and both hook registrations are written by
this one unit only.

#### Work Breakdown

##### Work Units

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [AC-0001](spec.md#criteria), [AC-0002](spec.md#criteria), [AC-0003](spec.md#criteria) | Brief module, adapters, guard admission, regressions and native observation | None | [Task](01.tasks/tsk-0001-native-request-brief.md) | tooling suite, agent-governance and recorded observations |

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | Requests bound to a shown brief before the first change in both providers | none | platform | `scripts/request_brief.py`, `scripts/provider_write_guard.py`, `scripts/validate-agent-governance.py`, `scripts/validation/registry.json`, `scripts/validation/contract-suites/tooling.json`, `scripts/README.md`, `tests/test_request_brief.py`, `tests/test_k8s_pre_edit_hook.py`, `tests/test_agent_governance.py`, `.claude/settings.json`, `.claude/hooks/request-intake.sh`, `.claude/provider.md`, `.codex/hooks.json`, `.codex/hooks/request-intake.sh`, `.codex/provider.md`, `docs/03.specs/README.md`, this package | AC-0001, AC-0002, AC-0003 | CHK-UNIT, CHK-GUARD, CHK-HOOK, CHK-NATIVE |

###### Change and Rollback

Revert the implementation commit; the guard returns to its previous checks
and both registrations lose the intake entry. Receipts in the Git common
directory are local state and may be deleted.

##### Dependency Edges

None; there is one work unit.

#### Verification Plan

##### Selected Checks

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-UNIT | Intake, record and admit behavior | Temporary repositories | Module only | Module changes | tooling suite |
| CHK-GUARD | Guard refusal and admission for both adapters | Provider-shaped payloads | Hook program only | Guard changes | tooling suite |
| CHK-HOOK | Registrations run only the intake adapter | Provider settings | Configuration only | Registration changes | agent-governance |
| CHK-NATIVE | Installed client delivery and display | Real sessions | One observation per provider | Once | Task Results |

##### Evidence Plan

Selected checks run on the staged index before commit and in the hosted
affected route of the pull request; native observations are recorded in the
Task with the client version.

#### Promotion Map

##### Durable Owners

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| none | none | none | No durable contract was introduced |

##### Consumer Updates

`scripts/README.md` names the module; both provider notes describe the
intake entry and its limits.

## 적용과 확인

### 적용 방법

Follow WORK-001 in the Task and record each check there.

### 확인 기준

Completion needs the three criteria's evidence and the operator's criterion
decisions.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| implements | [SPEC-0231](spec.md) |

### 외부 근거

No external source is adopted.
