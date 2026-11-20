---
title: "Current Documentation and SDLC Reconciliation"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-20"
artifact_id: "SPEC-0227"
---

# Current Documentation and SDLC Reconciliation Technical Specification (Spec)

## 문서 개요

### 목적과 독자

This change makes current documentation, execution authority and remaining work
describe the same behavior. Document owners, operators, validators and the next
P06 worker use the resulting current owners and handoffs.

### 책임과 적용 범위

This Spec owns only the P05 documentation and SDLC reconciliation. Durable
requirements stay in [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md),
workspace rules in [SDLC](../../00.workspace/03.process/sdlc.md), document
mechanics in [Stage 99](../../99.templates/README.md), and remaining execution
in the [SPEC-0223 Task](../0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md).
Its draft state is not implementation approval or criterion acceptance.

## 내용 계약

### 입력과 전제

The current user request selects P05-DOCS-SDLC from the 1.1.0 package and
authorizes this scoped implementation, verification and Git delivery. Its D05,
decisions, execution contract, questions, sources and k8s profile/findings are
candidate design evidence. The actual intake is clean
`codex/p01-ci-routing` at `1e71cef52c64c617e4a7cd7a2f2191f74c6dd8ab`.
P00–P04 delivery and the eleven earlier accepted streams are predecessor
facts, not work to repeat. The 2026-11-19 profile's 28-open count is stale:
the current [ledger](../work-residue-ledger.json) has 30 entries, 27 open and
three terminal after W06-H03 closure.

### 본문과 규칙

#### Overview

##### Goal

Align current owners and readers across stages 00, 01, 02, 03, 05, 90, 98
and 99; correct stale claims about CI and document authority; repair P05
operating/reference gaps; and hand off every genuinely unfinished condition.
Design state, implemented behavior, check result and user acceptance remain
separate. A merged PR records integration, not acceptance.

###### Owning Requirements

[REQ-0003-FR-0012, FR-0014, FR-0015, FR-0017, FR-0026, FR-0027 and
NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md)
govern the route, succession, evidence and selected checks. The
[workspace architecture](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md)
places human rules in stage 00 and machine forms in stage 99. The current
[document lifecycle](../../00.workspace/03.process/document-lifecycle.md)
already admits a separately verified scoped user execution request with draft
parents; this change keeps that boundary and the distinct final approval and
acceptance conditions.

##### Consumers

Authors and operators follow stage routers, SDLC rules, runbooks and policy;
Stage 99 and the strict profile, lifecycle, link and residue validators consume
the changed documents; the affected local and hosted QA selectors consume the
new package binding and changed paths. The SPEC-0223 Task and ledger remain
the single owner of residue status.

#### Scope

##### In Scope

Current document role and consumer inventory; corrections at present owners;
P05 W04-H02 through W04-H07 content, authority and escalation gaps; the
SPEC-0205/0211 stale form descriptions; one new P05 change package and its
Stage 99 workspace-scope binding; selected static checks and honest handoff.
The existing P04 common envelope and role forms stay compatible.

##### Out of Scope

Earlier accepted implementation and criterion decisions; P04 common-edition
adoption without a user decision; P06–P17 implementation; live cluster,
provider or break-glass execution; history rewrite, final numbering reset,
other workspaces and deletion of the input package. A future improvement with
no current consumer is conditional rather than a present failure.

#### Behavior Contract

##### Inputs and Outputs

Each current document has one semantic owner and actual reader. Stage 01
states requirements, Stage 02 design and decisions, Stage 03 bounded change
contracts/work/evidence, Stage 05 operation, Stage 90 research and audit facts,
Stage 98 unvalidated recovery and Stage 99 form mechanics. A repository
capability is not evidence that product or native behavior ran.

Draft Spec/Plan may be authored and reviewed. Dependent execution uses a
current approved basis or the separately reviewed, scoped user request under
DOCLIFE-R008. A draft alone grants no implementation, operation or completion
authority. Final package completion still requires its own approved contract,
observed work and checks, criterion decisions and handoff. No common Release
document role is added; the real repository publication procedure remains at
its existing operating owner.

Current corrections update their canonical owner and real consumers together.
An earlier accepted Spec/Plan remains a historical decision for its original
scope. A conflicting current clause loses execution authority only after its
still-valid obligation is assigned to a present owner; neither a prior filename
nor a document count proves completion. Each residue row retains one Task
state and a matching ledger pointer. Actual Desktop reviewer read-only and
production LAN egress failures stay repair targets in P06 and P07/P14.

##### Failure Behavior

A missing owner, invalid link, duplicate or unknown scope binding, unreviewed
draft execution receipt, mismatch between Task and ledger, or required check
failure reports its existing diagnostic and stops the dependent transition.
Unknown emergency contact or approver stops a break-glass step until the
operator supplies it; a named contact is not standing approval. Unobserved
native and cluster behavior remains unobserved. Revert a failed ordinary
documentation change through a normal reviewed commit/PR, preserving the
earlier evidence and scoped owner.

#### Acceptance Criteria

##### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| AC-0001 | Current stage documents and consumers are inventoried; stale owner and CI claims are corrected at canonical owners while completed P00–P04 and earlier accepted scopes are excluded with evidence. |
| AC-0002 | Current SDLC and validators retain separate draft authoring, scoped execution authority, implementation, checks and user acceptance; a draft without its own authority is refused. |
| AC-0003 | P05 W04-H02 through W04-H07 and stale Stage 99 descriptions are repaired at their actual owners; operating failure and escalation paths remain executable without invented live results or standing approval. |
| AC-0004 | The 30 existing residue entries are individually disposed through their existing Task/ledger owners; actual reviewer and egress failures remain open, conditional improvements retain their triggering conditions, and P17 alone owns final renumber/history cutover. |
| AC-0005 | New package and changed consumers pass selected strict form, lifecycle, owner/link, residue and relevant contract checks on recorded inputs; hosted and user acceptance results are recorded separately. |

##### Verification Strategy

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| scope-binding | SPEC-0227 resolves to one current workspace profile and rejects duplicate/unknown binding | Stage 99 registry, schema and focused tests | Repository static | New package binding | Task Results |
| document-profiles | Changed current documents satisfy their registered roles and sections | Changed paths and current registry | Repository static | Every authored change | Task Results |
| document-lifecycle | Draft execution receipt and state transitions retain separate authority | New Spec/Plan/Task and prior tree | Repository static | New executable Task | Task Results |
| links-and-owners | Changed links and current consumers resolve | Changed paths and tree inventory | Repository static | Link/router change | Task Results |
| residue-ledger | Task states and ledger pointers agree | Current 30-entry ledger and Task rows | Repository static | Residue update | Task Results |
| selected-qa | Affected checks actually run and report failures | Reviewed index or PR head | Local or hosted as named; no live proof | Delivery | Task Results and PR run |

###### Normative and Evidence

[Document authoring](../../00.workspace/03.process/document-authoring.md),
[lifecycle](../../00.workspace/03.process/document-lifecycle.md),
[quality](../../00.workspace/04.quality/quality.md) and the
[SPEC-0223 Task](../0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md)
own current rules and item states. The 1.1.0 package's D05 and sources are
candidate evidence; the [P04 Task](../0226-common-document-contract/01.tasks/tsk-0001-common-document-contract.md)
and [PR 338 checks](https://github.com/buenhyden/hy-home.k8s/pull/338/checks)
record predecessor integration without asserting common-edition adoption.

###### Historical and Navigation

The accepted [SPEC-0223](../0223-work-residue-handoff/spec.md),
[SPEC-0224](../0224-workspace-path-cutover/spec.md) and
[SPEC-0225](../0225-q07-history-bound-checks/spec.md) retain their original
accepted scope until P17 disposition. Their old Plans are historical input,
not P05 execution authority. The [P04 Spec](../0226-common-document-contract/spec.md)
and Plan remain draft with criterion acceptance pending.

##### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0001 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Owner/consumer review and changed link/profile checks |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0002 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Lifecycle negative case and current receipt check |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0003 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Document and owner/link checks plus semantic review |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0004 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Existing Task and ledger agreement check |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0005 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Selected exact-index and PR check results |

## 적용과 확인

### 적용 방법

The [Plan](plan.md) orders this bounded reconciliation. Current readers follow
the corrected stage owners and the Task's residue handoff; they do not infer
P06–P17 completion from this P05 document.

### 확인 기준

Acceptance requires the changed owners and their actual selected checks,
followed by a separate user decision for each criterion. Static document PASS
does not prove live break-glass, native reviewer or cluster isolation.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) |
| designs | [Workspace architecture](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) |

Navigate to the [Plan](plan.md), [Task](01.tasks/tsk-0001-docs-sdlc-reconciliation.md)
and [Stage 03 index](../README.md).

### 외부 근거

The bundled D05 design applies [Diátaxis](https://diataxis.fr/) to reader
roles, [arc42 decisions](https://docs.arc42.org/section-9/) to lasting design
choices and the [Google review standard](https://google.github.io/eng-practices/review/reviewer/standard.html)
to proportional review. They inform this local contract; none grants user
approval or proves repository runtime behavior.
