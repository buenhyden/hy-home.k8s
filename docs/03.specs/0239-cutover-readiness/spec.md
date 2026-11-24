---
title: "Cutover Readiness"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0239"
---

# Cutover Readiness Technical Specification (Spec)

## 문서 개요

### 목적과 독자

This Spec states the P16 contract for judging whether the workspace is ready
for the P17 cutover. The operator and reviewers use it to see, for each
resumed R and P item through P16, what is designed, implemented, regressed,
observed live and accepted by the user, and which required items still block
the cutover.

### 책임과 적용 범위

This Spec owns the P16 acceptance criteria. The [Plan](plan.md) owns the work
order and the [Task](01.tasks/tsk-0001-cutover-readiness.md) owns the
readiness inventory, its evidence and the criterion decisions.

## 내용 계약

### 입력과 전제

The operator entered `prompts/P16-ACCEPT.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-24 at `main@a4968ee5`. Design D16 separates design, code,
regression, live environment and user acceptance, and forbids marking the
workspace ready for cutover while an unrepaired failure, an unobserved native
adapter, an unfinished operating handoff or a cancelled required check
remains. P17's own execution and post-checks are not prerequisites. The
operator answered three P16 questions on 2026-11-24.

### 본문과 규칙

#### Overview

##### Goal

The Task carries one readiness row per resumed item through P16 with its
five separate results and a single verdict. The operator's acceptances are
recorded in their own Tasks, W10-H03 is narrowed to its future-conditional
part, the observed Claude half of AGENT-04 is recorded, and the abandoned P07
VM route is retired by a narrow lifecycle rule so SPEC-0229 can be decided.

###### Owning Requirements

[REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md)
keeps progress and acceptance in Tasks.
[AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md)
stays the architecture owner; no new decision is needed.

##### Consumers

The Tasks of SPEC-0223 and SPEC-0227 to SPEC-0238, the work residue ledger,
the [document lifecycle policy](../../00.workspace/03.process/document-lifecycle.md)
and P17.

#### Scope

##### In Scope

- The readiness inventory and verdict.
- Recording the operator's P16 acceptances and narrowing W10-H03.
- The retired-route rule and its use in SPEC-0229.

##### Out of Scope

P17's execution, renumbering and remote history change, rerunning unchanged
checks, the Codex observations blocked by the account limit, and other
workspaces' Template and Blog boundaries.

#### Behavior Contract

##### Inputs and Outputs

Each readiness row names its package, the five results and its state:
`complete`, `accepted with a named follow-up`, `future-conditional`,
`blocked` or `P17-owned`. The verdict is `cutover_ready: false` while any row
is `blocked`.

##### Failure Behavior

A merge, a passing test or a prompt entry is never reported as user
acceptance. A blocked item names its owner and the condition that unblocks
it.

#### Acceptance Criteria

##### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| AC-0001 | The Task holds one readiness row per resumed R and P item through P16 with design, code, regression, live and user acceptance separated, and a verdict that stays false while a required item is blocked. |
| AC-0002 | The operator's P16 acceptances are recorded in their Tasks with relevant required evidence, and every fully accepted Task is completed. |
| AC-0003 | Each open required item names its owner and unblocking condition; W10-H03 is narrowed by the operator's decision and the observed Claude half of AGENT-04 is recorded. |
| AC-0004 | A narrow lifecycle rule lets an operator-retired route's failures be closed by a retirement row naming the replacing route's PASS, and SPEC-0229's VM-route failures use it. |

##### Verification Strategy

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-DOCS | Profiles, links, lifecycle and the residue ledger | Staged index | Repository static | Every change | Staged QA |
| CHK-RETIRE | Retired-route resolution and its refusals | Synthetic Tasks | Module behavior only | The rule change | Task-evidence regressions |

###### Normative and Evidence

The [document lifecycle policy](../../00.workspace/03.process/document-lifecycle.md)
owns the retired-route rule. Design D16 and K23-15 are dated inputs.

###### Historical and Navigation

None apply.

##### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0001 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Inventory review |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0002 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Lifecycle and profile checks |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0003 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Residue ledger check |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0004 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Task-evidence regressions |

## 적용과 확인

### 적용 방법

Read the Task's readiness table before P17; resolve each blocked row at its
owner.

### 확인 기준

Static checks are repository evidence; the readiness rows cite their own
Tasks' observed results.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [Workspace governance requirements](../../01.requirements/0003-workspace-agent-governance-platform.md) |
| designs | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) |

### 외부 근거

Design D16 is a dated input; no external standard is adopted.
