---
title: "Forecast Consumer Link"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0234"
---

# Forecast Consumer Link Technical Specification (Spec)

## 문서 개요

### 목적과 독자

This Spec states the P11 change contract for P30, P50 and P80 work
forecasts. The platform owner and reviewers use it to judge whether the
existing forecast tool keeps its meaning, reaches a real work unit through
the request brief, and starts a new baseline after the final cutover.

### 책임과 적용 범위

This Spec owns the P11 behavior and acceptance criteria. The [Plan](plan.md)
owns the work order, risks and rollback, and the
[Task](01.tasks/tsk-0001-forecast-consumer-link.md) owns execution and
evidence.

## 내용 계약

### 입력과 전제

The operator entered `prompts/P11-FORECAST.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-24 at `main@bdb2d39b`. Design D11, finding K23-11 and the
Kubernetes design delta ask to keep the existing quantile, censoring,
coverage, pinball loss and uncalibrated label, to confirm only the link from
the brief and the actual work unit to a forecast and its measured result,
and not to keep trial runs removed at P17 as calibration samples. The live
store held 19 records; residue W10-H01, the same round trip from a Codex
session, was open.

### 본문과 규칙

#### Overview

##### Goal

`scripts/work_forecast.py` is kept unchanged. SDLC-R038 states that P80 is
a completion probability, not progress, that the task reference names the
work unit and the request whose brief it serves, and that a final cutover
sets the store aside so the new baseline starts at N=0. One real work unit,
this change, is forecast before it starts and scored after it ends.

###### Owning Requirements

[REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md)
keeps session and planning state apart from Task status and evidence.
[AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md)
keeps one store per Git common directory; no new architecture decision is
needed.

##### Consumers

`scripts/work_forecast.py` (`forecast`, `start`, `finish`, `list`,
`score`), the request brief of `scripts/request_brief.py`, the Task that
cites the record, and [SDLC-R038](../../00.workspace/03.process/sdlc.md).

#### Scope

##### In Scope

- The meaning of P30, P50 and P80, the brief and work-unit key and the
  cutover reset in SDLC-R038.
- One live forecast round trip by Claude, cited by ID and digest.

##### Out of Scope

Rewriting the calculator, a commit or merge gate on forecast error, the
DAG and resource bounds of parallel work (P12), the analysis of under- and
over-estimates (P13), the cutover itself (P17), and the Codex round trip
while its quota is used up.

#### Behavior Contract

##### Inputs and Outputs

A forecast carries its task reference, type, time basis, unit, P30 to P80,
start and end definitions, reference class, assumptions, risks, the number
of earlier completed runs of its group and the label `uncalibrated`. A
finished run is completed with an actual, or censored as cancelled, failed
or incomplete with no actual. The score reports N, coverage and pinball loss
of completed runs per group, beside censored, open, unstarted and
superseded counts.

##### Failure Behavior

The tool refuses unordered, negative or non-finite quantiles, a start
before its forecast, a clock that moves backwards, a second live forecast
for one task reference and any rewrite. A forecast error never blocks a
commit.

#### Acceptance Criteria

##### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| AC-0001 | The existing forecast tool keeps quantile order, non-finite refusal, censoring, coverage, pinball loss, sample size and the uncalibrated label, proven by its regressions, and no forecast gate is added. |
| AC-0002 | SDLC-R038 states completion probability, the brief and work-unit key and the cutover reset, and one real work unit is forecast before it starts, finished and scored, with its ID and digest cited in the Task. |

##### Verification Strategy

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-FORECAST | Quantiles, censoring, scoring and immutability | Temporary stores | Module behavior only | Every forecast change | `work-forecast-regressions` |
| CHK-LIVE | One real round trip and its score | Live forecast store | Local host only | Once for this change | Task Results |

###### Normative and Evidence

[SDLC-R038](../../00.workspace/03.process/sdlc.md) owns the forecast rule.
Design D11 and K23-11 are dated inputs.

###### Historical and Navigation

None apply.

##### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0001 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Forecast regressions |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0002 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Policy review and live observation |

## 적용과 확인

### 적용 방법

Record the forecast before the work starts with the request ID in its task
reference, then start, finish and score it, and cite it in the Task.

### 확인 기준

Regressions prove module behavior; the live observation shows the store and
its score.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [Workspace governance requirements](../../01.requirements/0003-workspace-agent-governance-platform.md) |
| designs | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) |

### 외부 근거

Design D11 cites the quantile accuracy chapter of Forecasting: Principles
and Practice as a dated input; no external standard is adopted.
