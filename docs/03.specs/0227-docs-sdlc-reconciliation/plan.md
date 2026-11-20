---
title: "Current Documentation and SDLC Reconciliation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-11-20"
artifact_id: "SPEC-0227-PLAN-0001"
parent_ids: ["SPEC-0227"]
---

# Current Documentation and SDLC Reconciliation Implementation Plan

## 문서 개요

### 목적과 독자

This Plan orders P05's current-owner corrections, focused checks and handoff.
Document and quality owners use it with the [Spec](spec.md) and [Task](01.tasks/tsk-0001-docs-sdlc-reconciliation.md).

### 책임과 적용 범위

The Spec owns what P05 must achieve; this Plan owns dependencies, work order,
selected checks, risks and durable promotion. The Task alone records observed
implementation, check results and criterion decisions.

## 내용 계약

### 입력과 전제

The user selected only P05 from the 1.1.0 package. D05, fixed decisions,
sources and the current k8s profile/findings constrain the work. Existing
P00–P04 implementations and the eleven accepted work streams are predecessors.
The 30-row [residue ledger](../work-residue-ledger.json) and its
[owning Task](../0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md)
already enumerate remaining work. Current scoped user execution authority is
recorded in this package's Task separately from approval of this draft Plan.

### 본문과 규칙

#### Overview

##### Outcome

The current documents and real consumers agree on document purpose, CI
selection, authority and operating failure boundaries. Each changed or
retained residue has one future owner. The P06 input can use these owners
without claiming P06 work or native/live success.

##### Constraints

Current architecture, approval and source-freshness boundaries constrain the
work units below; their detailed owners remain in the linked current documents.

###### Global Constraints

The [Spec](spec.md#scope) limits P05 to current document owners and their
consumers. Draft authoring is allowed; dependent execution uses the current
separately verified user request under DOCLIFE-R008. Formal Spec/Plan approval,
new common-edition adoption and criterion acceptance remain separate decisions.
Do not broaden this work into historical accepted scopes, fixed corpus counts,
a per-work SHA approval gate or another permanent progress ledger.

###### Risks and Mitigations

The main compatibility risk is a stale claim being removed while a real
consumer still reads it. Check links, owner routing and the existing residue
gate on the actual changed tree. Runbook wording must not grant standing
break-glass approval or assert a live test. Preserve the actual reviewer
read-only and LAN egress failures as open repair targets. Roll back through a
reviewed revert with the matching registry binding and documents together.

###### Escalation

If an actual prior user decision conflicts with P05, isolate that clause and
request a choice while independent corrections proceed. If an operating owner
or approver is unknown, stop only the affected operation and record its owner
and resume condition. A failed required validator or hosted check is not
accepted by changing its label.

#### Dependencies

##### Prerequisites

Read the package README, P05, D05, decisions, execution contract, questions,
sources and current k8s profile/findings. Reobserve Git, the existing stage
owners and relevant merged PR/CI facts. Stage 99's current common shell and
role profiles are the form input. No other workspace is an implementation
input.

##### Shared Resources

The Stage 99 registry/schema and this package are shared with the source
owners. One writer owns each file; synchronize the SPEC-0227 scope binding
before strict profile checks. The Task records actual check inputs and the
SPEC-0223 Task/ledger pair changes only together where residue state changes.

#### Work Breakdown

##### Work Units

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [AC-0001](spec.md#criteria), [AC-0002](spec.md#criteria), [AC-0003](spec.md#criteria), [AC-0004](spec.md#criteria), [AC-0005](spec.md#criteria) | Reconcile current owners, operating gaps, residue and selected checks in one reviewed P05 change | Current P00–P04 delivery and scoped user request | [Task](01.tasks/tsk-0001-docs-sdlc-reconciliation.md) | Strict profile, lifecycle, link, residue and scope binding checks; selected local and hosted QA |

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | Current P05 documents and handoff agree | none | platform | `docs/00.workspace/`, `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/05.operations/`, `docs/90.references/`, `docs/98.archive/`, `docs/99.templates/`, `gitops/README.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.secrets.baseline`, focused `tests/` | AC-0001 to AC-0005 | Scope binding, strict document/lifecycle/link/residue, selected QA and review |

###### Change and Rollback

First inventory current paths and consumers, then correct each canonical
document and matching readers. Add the SPEC-0227 workspace binding and check
it. Record item-by-item residue disposition in the existing Task/ledger only
where evidence changes its current state. Revert this P05 delivery as one
reviewed change if a contract regression is found; earlier accepted records
and P04 bytes remain available in Git history.

##### Dependency Edges

WORK-001 starts after P00–P04 integration evidence and a current scoped user
request are observed. Strict checks require the new profile binding and all
changed consumers. Final handoff follows actual selected checks and review;
user criterion acceptance does not follow automatically from a PR merge.

#### Verification Plan

##### Selected Checks

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| scope-binding | Exact new workspace scope and negative cases | Registry, schema, focused test | Repository static | Binding edit | Task Results |
| document-profiles | Profile, heading and role payload agreement | Changed docs and registry | Repository static | Authored change | Task Results |
| document-lifecycle | Draft execution and Task state authority | New package and previous tree | Repository static | New active Task | Task Results |
| links-and-owners | Current local links and owners | Changed links and tree | Repository static | Router or link change | Task Results |
| residue-ledger | Existing Task/ledger agreement | 30 rows and their owners | Repository static | Residue update | Task Results |
| selected-qa | Required local/hosted purpose checks | Exact index and PR head | Each observed lane only | Delivery | Task Results and PR run |

##### Evidence Plan

Run focused validators on the changed tree, then selected quick/staged QA on
the reviewed local candidate. The active commit hooks check the final index.
After push, read required hosted checks for the exact PR head; do not replay
unchanged leaves merely for a new receipt. Record an unrun check as NOT_RUN or
DEFER with its owner, never as PASS. Review architecture compliance against
the [workspace description](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md);
a structural departure returns this draft to review.

#### Promotion Map

##### Durable Owners

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| P05-SDLC | [SDLC flow](../../00.workspace/03.process/sdlc.md#rules) | Current authority, status axes and CI description agree with readers | SDLC-R003/R016/R021/R027/R028 and linked quality guide |
| P05-REQUIREMENT | [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md#functional-requirements) | Current requirement and real CI observation align | FR-0017 and current source/lineage note |
| P05-OPERATIONS | [Rollout operations policy](../../05.operations/02.policies/0004-rollouts-notifications-headlamp-policy.md) | The current enforcement and escalation rules name their real owner without inventing a live run or standing break-glass approval | The policy's rule rows and changed current runbooks |
| P05-REFERENCE | [Reference maintenance runbook](../../00.workspace/06.maintenance/0011-reference-maintenance-runbook.md) | A current consumer's source/version need triggers a dated recheck; historical blanks create no standing bulk-refresh duty | The runbook's refresh rule and [m0027 source applicability](../../90.references/01.research/0001-workspace-engineering/m0027-source-and-audit-applicability.md) |
| P05-FORM | [Document authoring](../../00.workspace/03.process/document-authoring.md#registry-forms) | Stage 99 binding and surviving role guidance agree | Registry/schema and focused binding test |

##### Consumer Updates

Stage routers and current architecture, requirement, operations and reference
owners retain their own meaning. The SPEC-0223 Task and ledger remain the
single residue source; P06 picks up actual reviewer/approval defects, P07 and
P14 the egress defect, and P17 the final identity/history transition. Existing
publication runbook remains an operational procedure, not a common Release
document lifecycle.

## 적용과 확인

### 적용 방법

Use the [Task](01.tasks/tsk-0001-docs-sdlc-reconciliation.md) for the actual
result and follow the corrected current owners. This Plan orders no later P
prompt automatically.

### 확인 기준

Promotions count only after their receiving owner changes and the affected
checks pass. A document, merge or static PASS alone does not establish native
operation or user criterion acceptance.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| implements | [Spec](spec.md) |

Navigate to the [Task](01.tasks/tsk-0001-docs-sdlc-reconciliation.md) and
[Stage 03 index](../README.md).

### 외부 근거

The bundled D05 source summary uses Diátaxis for document reader roles,
arc42 for significant decisions and Google review guidance for proportional
review. They inform the local plan, not its implementation authority.
