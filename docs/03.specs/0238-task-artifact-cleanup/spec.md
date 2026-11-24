---
title: "Task Artifact Cleanup"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0238"
---

# Task Artifact Cleanup Technical Specification (Spec)

## 문서 개요

### 목적과 독자

This Spec states the P15 change contract for one-off work material. The
platform owner and reviewers use it to judge whether finished temporary
material is removed, persistent material is kept, the end-of-work cleanup
rule lives with its owners, and no current owner depends on an input package
that P17 will remove.

### 책임과 적용 범위

This Spec owns the P15 behavior and acceptance criteria. The [Plan](plan.md)
owns the work order, risks and rollback, and the
[Task](01.tasks/tsk-0001-task-artifact-cleanup.md) owns execution and
evidence.

## 내용 계약

### 입력과 전제

The operator entered `prompts/P15-CLEANUP.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-24 at `main@a4968ee5`. Design D15 and finding K23-15 ask to sort
one-off material by its real consumers, delete only what the task owns,
record the cleanup rule in the workspace process and the agent execution
rules, move any durable dependency on the package to a current owner, and
keep the 1.2.0 package for P16 and P17. The operator approved deleting the
superseded 1.1.0 input package.

### 본문과 규칙

#### Overview

##### Goal

The finished legacy-timer retirement in `install_timer` leaves with its
test, which is rewritten to the current install contract. QUAL-R025 states
the end-of-work sort of temporary and persistent material, and the work
lifecycle's Completion step applies it. This session's finished scratch and
the 1.1.0 package are removed; persistent stores, regressions, timers and
the 1.2.0 package stay.

###### Owning Requirements

[REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md)
requires one shared implementation and workflow for every provider.
[AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md)
stays the architecture owner; no new decision is needed.

##### Consumers

`scripts/session_analysis.py install-timer`, the
[quality policy](../../00.workspace/04.quality/quality.md) QUAL-R025, the
[work lifecycle](../../../.agents/workflows/work-lifecycle.md) Completion
step and the
[context and memory policy](../../../.agents/governance/context-and-memory.md)
CTX-R023.

#### Scope

##### In Scope

- Removing finished one-off code and its test, and stating the current
  install contract.
- The end-of-work cleanup rule.
- Deleting this work's finished temporary material and the approved 1.1.0
  package.

##### Out of Scope

The 1.2.0 package and other P16 and P17 inputs, persistent stores, other
workspaces' timers and material, `sessions/`, the set-aside forecast trial
store, host-wide pruning, and P16 acceptance.

#### Behavior Contract

##### Inputs and Outputs

`install_timer` writes and enables only this clone's named timer and service
and returns the timer name and directory; any other unit is left alone.
QUAL-R025 sorts temporary from persistent material, limits deletion to what
the task made inside the checkout or its scratch area, and requires an owner,
resume point and deletion condition for kept recovery material.

##### Failure Behavior

A deletion outside the task's own material, through a link or mount, or by a
host-wide prune is refused by the rule. An input package stays until its
last reading prompt is finished and its deletion is approved.

#### Acceptance Criteria

##### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| AC-0001 | The finished legacy-timer retirement and its test are removed, and a regression states the current install contract. |
| AC-0002 | QUAL-R025 and the work lifecycle state the end-of-work sort, the deletion limits and the recovery material conditions. |
| AC-0003 | This work's finished temporary material and the approved 1.1.0 package are deleted, while persistent material and the 1.2.0 package stay and no current owner reads a package. |

##### Verification Strategy

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-ANALYSIS | The install contract | Temporary home directory | Module behavior only | Every analysis change | `session-analysis-regressions` |
| CHK-DOCS | Profile, links and lifecycle | Staged index | Repository static | Every document change | Staged QA |
| CHK-LOCAL | Deleted and kept local material | Local host | Local host only | Once for this change | Task Results |

###### Normative and Evidence

QUAL-R025 owns the cleanup rule. Design D15 and K23-15 are dated inputs.

###### Historical and Navigation

None apply.

##### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0001 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Analysis regressions |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0002 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Document review |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0003 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Local observation |

## 적용과 확인

### 적용 방법

Apply QUAL-R025 at the end of each task; record kept recovery material in
the Task.

### 확인 기준

Regressions and static checks are repository evidence; the deletions are
observed on the local host.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [Workspace governance requirements](../../01.requirements/0003-workspace-agent-governance-platform.md) |
| designs | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) |

### 외부 근거

Design D15 is a dated input; no external standard is adopted.
