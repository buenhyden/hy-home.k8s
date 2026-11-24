---
title: "Linked Run Observation"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0236"
---

# Linked Run Observation Technical Specification (Spec)

## 문서 개요

### 목적과 독자

This Spec states the P13 change contract for observing work runs and the
effect of improvement candidates. The platform owner and reviewers use it to
judge whether the facts already kept by forecasting, parallel work and
session analysis are joined without a new store, whether every missing or
unmeasured fact stays visible instead of counting as zero, and whether cost
estimates stay apart from actual charges.

### 책임과 적용 범위

This Spec owns the P13 behavior and acceptance criteria. The [Plan](plan.md)
owns the work order, risks and rollback, and the
[Task](01.tasks/tsk-0001-linked-run-observation.md) owns execution and
evidence.

## 내용 계약

### 입력과 전제

The operator entered `prompts/P13-OBSERVABILITY.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-24 at `main@e45125dc`. Design D13 and finding K23-13 ask to reuse
the existing run logs, link run, task, provider, stage times, outcome and
cost, carry candidates from source to observed effect, keep unknown values
null with a reason, and separate the CLI estimate from the actual charge.
K23-03 (CI routing) and K23-10 (the per-workspace timer) were closed by
earlier packages. Residue W10-H04 was due: the first recheck of candidate 1.

### 본문과 규칙

#### Overview

##### Goal

A read-only `scripts/work_observe.py report --key` joins forecast records,
parallel run reports and promoted analysis candidates that already name a
Task key. Each candidate reports an `effect` with a state and reason instead
of an `acceptance` label that read like the user's acceptance. A provider
worker's report carries the CLI's cost estimate with the actual charge null,
and its raw output is deleted once parsed. W10-H04 closes from the live
rechecks.

###### Owning Requirements

[REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md)
keeps session and planning state apart from Task status and evidence.
[AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md)
keeps one store per Git common directory; no new architecture decision is
needed.

##### Consumers

`scripts/work_observe.py`, `scripts/session_analysis.py candidates`, the
parallel run `report.json`, the
[context and memory policy](../../../.agents/governance/context-and-memory.md)
CTX-R023, the
[delegated development workflow](../../../.agents/workflows/delegated-development.md)
and the [scripts index](../../../scripts/README.md).

#### Scope

##### In Scope

- A read-only join of existing local run facts by Task key.
- An explicit effect state for every analysis candidate.
- Cost labels and raw-output deletion in parallel run reports.
- Closing the due runtime hold W10-H04 in its owning Task.

##### Out of Scope

A new telemetry store, a dashboard, copying hosted CI logs, P95 or billed
cost, rerunning paid observations, the Codex observations still blocked by
quota, the first scheduled timer firing on 2026-11-25, and the P15 and P17
cleanups.

#### Behavior Contract

##### Inputs and Outputs

A key is an artifact ID, optionally narrowed; a record matches when its task
reference equals the key or continues it after a space. The join returns
forecast records (verified against their digests), parallel run units with
provider, state, times, session, turns, cost estimate, charge and note, and
promoted candidates with rechecks and effect. An effect is `recurred`,
`met`, `unobserved` with a reason, or `not-tracked` with a reason.

##### Failure Behavior

A missing store or runtime and a store with no record for the key are both
null with a reason; the join never creates a store. A blank or padded key is
refused. An unreadable report is skipped as no fact.

#### Acceptance Criteria

##### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| AC-0001 | Existing forecast, parallel and analysis facts are joined read-only by Task key, with a missing source null with a reason and no store created or raw text copied. |
| AC-0002 | Every analysis candidate ends its chain in an effect state with a reason, never a zero count, and distinct from user acceptance. |
| AC-0003 | Parallel run reports split the CLI cost estimate from a null actual charge and keep no raw provider output after collection. |
| AC-0004 | The due runtime hold W10-H04 is closed in its owning Task from the live rechecks, and the holds that remain are named with their owners. |

##### Verification Strategy

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-OBSERVE | Join, key matching, null reasons, no store creation | Temporary stores | Module behavior only | Every join change | `work-observe-regressions` |
| CHK-EFFECT | Effect states and reasons | Temporary stores | Module behavior only | Every analysis change | `session-analysis-regressions` |
| CHK-COST | Cost labels and raw-output deletion | Temporary repositories and a stand-in CLI | Local host | Every dispatcher change | `work-parallel-regressions` |
| CHK-LIVE | Live join and the W10-H04 recheck | Live local stores | Local host only | Once for this change | Task Results |

###### Normative and Evidence

CTX-R023 of the
[context and memory policy](../../../.agents/governance/context-and-memory.md)
owns the effect and join rule. Design D13 and K23-13 are dated inputs.

###### Historical and Navigation

None apply.

##### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0001 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Join regressions and live join |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0002 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Analysis regressions |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0003 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Dispatcher regressions |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0004 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Live observation |

## 적용과 확인

### 적용 방법

Run `scripts/work_observe.py report --key <artifact>` and cite its output in
the Task; read `session_analysis.py candidates` for effects.

### 확인 기준

Regressions prove module behavior; the live join and recheck show the local
stores.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [Workspace governance requirements](../../01.requirements/0003-workspace-agent-governance-platform.md) |
| designs | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) |

### 외부 근거

Design D13 is a dated input; no external standard is adopted.
