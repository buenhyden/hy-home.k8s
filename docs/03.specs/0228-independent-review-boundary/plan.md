---
title: "Independent Review and Read-Only Boundary Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-11-20"
artifact_id: "SPEC-0228-PLAN-0001"
parent_ids: ["SPEC-0228"]
---

# Independent Review and Read-Only Boundary Implementation Plan

## 문서 개요

### 목적과 독자

This Plan orders the P06 review and native-boundary correction for the
[Spec](spec.md). Implementers, reviewers, quality owners and the operator use
it to distinguish code changes, checked evidence and acceptance.

### 책임과 적용 범위

The Spec owns behavior and criteria. This Plan owns order, scope, risks,
selected checks, rollback and durable promotion. The [Task](01.tasks/tsk-0001-independent-review-boundary.md)
owns actual commands, results, failures and criterion decisions.

## 내용 계약

### 입력과 전제

The current user's P06 request authorizes the bounded implementation,
verification and Git delivery. D06, D07, the decided Q03 scope, current k8s
profile/findings and repository code are inputs. Initial branch and HEAD are
`codex/p01-ci-routing` at `598d8e4a47f21cc68f494155febb1227bf6bf12f`.
P00–P05 and the earlier eleven streams remain predecessor evidence.

### 본문과 규칙

#### Overview

##### Outcome

Correct false evidence-only carry, align review risk and authority owners,
establish a supported read-only review route or a precise failed/environment
handoff, and record the selected static/native results without inventing user
acceptance. No later prompt is executed as part of P06.

##### Constraints

The current Desktop→SSH reviewer permission observation is a real failure;
the alternate CLI route must be identified independently. Current Task 223
and its ledger remain the only residue owner. Provider configurations are
intent until an installed runtime applies them. The already completed P00–P05
contracts are reused where their conditions still match. The architecture
boundary is [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md);
no product or cluster architecture migration is planned.

###### Global Constraints

Every work unit inherits the [Spec](spec.md#scope) exclusions. Actual model
calls use current accounts, allowed models and existing limits, sequentially,
with a 600-second run ceiling and six turns where supported. Initial attempt
and one repaired confirmation share those bounds. An unknown cost remains
`null` with a reason. Do not change global trust, secrets, subscriptions or
native permission policy to make a probe green.

###### Risks and Mitigations

False carry can conceal an authority change; add RED/GREEN negative cases
before classifier repair. A role projection may appear read-only while a
writable parent controls the child; record parent and actual dummy-source
write denial. A temporary probe may touch sensitive state; use only disposable
source and fake sentinel, inspect its cleanup. Native readiness failure may
block a provider; preserve `failed` and route only the dependent observation
to P07 with a specific repair condition. The platform owner reviews all four
risks before delivery.

###### Escalation

Stop a dependent high-risk reviewer claim if its source write is allowed,
the OS boundary cannot start, or an actual permission is unknown. The
platform owner selects a verified alternate route or records a P07
environment repair with the original route still failed. Only a newly found
account, cost, permission or deletion conflict outside the decided Q03 scope
returns to the user; Q03 itself is settled.

#### Dependencies

##### Prerequisites

Current [quality](../../00.workspace/04.quality/quality.md),
[approval](../../00.workspace/04.quality/approval-and-safety.md),
[SDLC](../../00.workspace/03.process/sdlc.md),
[environment](../../00.workspace/05.environment/README.md),
[agent registry](../../../.agents/roles/registry.json), provider notes and
existing `scripts/review_delta.py` are the actual owners/consumers. Draft
Spec/Plan require exact-byte review and a current scoped DOCLIFE-R008 receipt
before Task execution; that receipt is execution authority only.

##### Shared Resources

Quality and provider rules, Stage 99 workspace binding and Task 223/ledger
are shared across work units. Freeze one reviewed contract before parallel
source changes, then integrate and check the same candidate. The native
provider probes run sequentially. Review and receipt updates happen after
final contract bytes are fixed.

#### Work Breakdown

##### Work Units

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [AC-0001](spec.md#criteria), [AC-0002](spec.md#criteria), [AC-0003](spec.md#criteria), [AC-0004](spec.md#criteria), [AC-0005](spec.md#criteria), [AC-0006](spec.md#criteria) | Correct P06 review/carry/authority consumers, validate native routes and hand off honest outcomes | Current scoped execution receipt | [Task](01.tasks/tsk-0001-independent-review-boundary.md) | Focused regressions, document/owner checks, named native probes and selected QA |

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | Review and read-only boundary correction | Current P06 request, exact-byte review and R008 receipt | platform | `.agents/governance/approval-and-safety.md`; `.agents/roles/code-reviewer.md`; `.agents/prompts/change-review.md`; actual review skill if used; `.codex/provider.md`; `.claude/provider.md`; actual native bindings/projections only if required; `docs/00.workspace/03.process/sdlc.md`; `docs/00.workspace/04.quality/quality.md`; `docs/00.workspace/05.environment/0012-independent-review-environment.md`; `scripts/review_delta.py`; `scripts/validate-document-lifecycle.py`; `scripts/README.md`; focused tests; Stage 99 workspace binding/schema and scoped regression; `docs/03.specs/0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md`; `docs/03.specs/work-residue-ledger.json`; this package/index; `.secrets.baseline` only for reviewed public R008 digest false positives | AC-0001–AC-0006 | review-delta, approval-negative, review-contract, native-boundary, document-contract, selected-qa |

###### Change and Rollback

First pin the current consumer and failure evidence, then implement focused
classifier tests and repair. Update the quality, process, approval, review
role/prompt and provider consumers at their current owners. Add the smallest
environment guide required by the native route. Add only needed Stage 99
binding and tests, then reconcile Task 223/ledger. Run selected checks on the
integrated candidate. Revert the ordinary reviewed commit/PR if the new
contract breaks a consumer; retain factual failed native evidence. Do not
rollback by widening reviewer authority or erasing a failed result.

##### Dependency Edges

The exact draft review and execution receipt precede source mutation.
Classifier tests precede classifier repair. Native route selection precedes
paid probes; a failed readiness condition selects repair or P07 handoff.
Consumer and document checks precede delivery. Actual criterion acceptance
follows operator review of concrete evidence, never a passing QA label alone.

#### Verification Plan

##### Selected Checks

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| review-delta | Evidence carry rejects normative/new obligations and preserves factual rows | Focused fixture diffs | Local classifier | Script change | Task Results |
| approval-negative | Verdict/hash/role cannot become user approval | Current receipt shape and negative fixtures | Repository static | Approval consumer change | Task Results |
| review-contract | Risk, scope and consumers follow the Spec and AD-0006 | Integrated policy/provider/reviewer diff | Independent semantic review | Contract change | Task Results |
| native-boundary | A verified primary or alternative route reads permitted source, denies source write and outside-scope fake read, blocks external connection through a network-capable tool, exposes effective shell/file/MCP/hook inventory and reviews the focused diff | Installed provider, isolated source, fake sentinel and limits | Native runtime only | Supported selected route ready | Task Results or P07 handoff |
| document-contract | New package, guide, Stage 99 binding and current links conform | Exact candidate tree/index | Repository static | Document change | Task Results |
| selected-qa | Registered affected checks report actual selected result | Current index/PR candidate | Local and hosted only | Delivery | Task Results and PR checks |

Architecture compliance is checked in `review-contract`: each corrected
policy/provider boundary stays under AD-0006. A departure returns the Spec
to review. A static PASS never closes a missing actual source-write denial.

##### Evidence Plan

Record RED/GREEN focused regression inputs, exact draft review and R008
receipt, native provider/version/route/permission observation, selected local
QA on its snapshot, staged hook result, hosted PR result and merge identity in
the Task. Repeat only checks whose input or trusted boundary changed.
Source change, runtime success, integration and operator acceptance have
different evidence rows and must not be conflated.

#### Promotion Map

##### Durable Owners

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| P06-RISK | [Quality policy](../../00.workspace/04.quality/quality.md) | Current risk, review and carry semantics are reflected and selected checks pass | Risk/semantic review clauses |
| P06-AUTH | [Agent approval and safety](../../../.agents/governance/approval-and-safety.md) | Reviewer boundary no longer implies approval or sandbox from role text | SAFE-R018 and related clauses |
| P06-HANDOFF | [SDLC process](../../00.workspace/03.process/sdlc.md) | Review timing and author/reviewer/operator handoff match the observed route | Review/handoff section |
| P06-ENV | [Review environment](../../00.workspace/05.environment/0012-independent-review-environment.md) | Actual route, limits, failure and re-observation steps are stated without claiming unrun success | Route and verification sections |

##### Consumer Updates

The role/prompt and provider notes consume the durable rules. The classifier
and focused tests implement carry meaning; Stage 99 binds this workspace
package, while Task 223/ledger retain only current residue status. Neither
README routers nor Stage 90 evidence become promotion authorities.

## 적용과 확인

### 적용 방법

Execute WORK-001 only under the current scoped authority and update the Task
with factual results. P07 is a separate prompt after a specific environment
dependent observation handoff.

### 확인 기준

Check each selected input and its trust boundary. Mark any native route
failure, hosted absence or pending user criterion decision explicitly.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [P06 Spec](spec.md) |
| implements | [P06 Task](01.tasks/tsk-0001-independent-review-boundary.md) |

### 외부 근거

Package D06/D07 aggregate the dated official provider sources. Installed
versions and Task observations decide what this checkout can claim.
