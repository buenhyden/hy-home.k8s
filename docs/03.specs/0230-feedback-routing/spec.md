---
title: "Feedback Routing Repair"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-23"
artifact_id: "SPEC-0230"
---

# Feedback Routing Repair Technical Specification (Spec)

## 문서 개요

### 목적과 독자

This Spec states the R01 change contract for validation routing. The
platform owner, reviewers and implementers use it to judge whether a narrow
change selects the checks its real consumers need and no more.

### 책임과 적용 범위

This Spec owns the R01 behavior and acceptance criteria. The [Plan](plan.md)
owns the work order, risks and rollback, and the
[Task](01.tasks/tsk-0001-feedback-routing.md) owns execution and evidence.

## 내용 계약

### 입력과 전제

The operator entered `prompts/R01-FEEDBACK.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-23 at `main@0c2b98e47a91e67c7b655289a8ba99e293d7290f`. Its D18
design and the k8s profile select two routing defects measured on PR341
(run 45105112715): a seven-line suite registration selected every contract
suite, and a general workspace guide body selected the full document contract
regression. P01 and P02 are not re-executed.

### 본문과 규칙

#### Overview

##### Goal

A suite registration change selects that suite and the registration checks;
a change to the shared runner still selects every suite. A numbered workspace
guide body change selects its own document, lifecycle, link, registry and
owner checks, while policy owners, the workspace architecture, agent
governance documents and documents the document suite reads by name keep the
full document contract regression.

###### Owning Requirements

[REQ-0003-FR-0016, FR-0018 and NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md)
require one machine owner for routing, proportional selection of affected
checks and no blanket rerun. [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md)
keeps the validation registry as that owner. This change adds registry rows
and a data file layout and needs no new architecture decision.

##### Consumers

`scripts/validation/registry.json`, `scripts/validate-affected-surfaces.py`,
`scripts/run-contract-tests.py`, `scripts/qa.py` and the hosted affected
route read the result; contributors read the selected check list.

#### Scope

##### In Scope

- Move each suite's module list into its own file under
  `scripts/validation/contract-suites/` and route each file to its suite and
  the registration checks.
- Keep the runner engine routed to every suite and add the missing
  `test-cluster` suite to that route.
- Route numbered workspace guides outside the document suite's named inputs
  away from the full document contract regression.
- Persistent routing regressions and a drift guard for named inputs.

##### Out of Scope

Validator implementations, result aggregation, the shared links and markdown
run, local snapshot and cache work, other workspaces and P07 runtime work.

#### Behavior Contract

##### Inputs and Outputs

The input is a set of changed paths; the output is the selected validator
set. A suite data file must be a non-empty JSON list of unique
`tests.test_*` module names within 64 KiB. Every test module still belongs to
exactly one suite gate selected by its own file.

##### Failure Behavior

A malformed, empty or oversized suite file, or no suite at all, fails the
runner with the file name. An unmatched or ambiguous path still fails routing.
A numbered guide that the document suite names in its code is refused by the
drift guard if it is routed as a general guide.

#### Acceptance Criteria

##### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| AC-0001 | A suite registration file selects its suite and `validation-routing-tests` and no other suite; the runner engine selects every suite including `test-cluster`. |
| AC-0002 | A general numbered workspace guide selects the document, lifecycle, link, registry and owner checks without `document-contract-tests`; policy owners, architecture, agent governance and named inputs still select it. |
| AC-0003 | On the same inputs, the before and after selection, estimated and measured time and the detection of registration and guide defects are recorded. |

##### Verification Strategy

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-ROUTE | Path-to-validator selection for registration, engine, guide and consumer paths | Registry and fixture paths | Selection only; does not run the selected checks | Every change to routing data | `validation-routing` suite result |
| CHK-DETECT | Selected checks still fail on a registration defect and a guide link or profile defect | Temporary mutations, reverted | One representative defect per class | Once for this change | Recorded mutation results |
| CHK-TIME | Before and after cost on the same input | PR341 leaf times and one local suite run | Single samples, not p95 | Once for this change | Task Results |

###### Normative and Evidence

The [validation registry](../../../scripts/validation/registry.json) and the
[quality policy](../../00.workspace/04.quality/quality.md) are the current
owners. PR341 timing comes from the package evidence.

###### Historical and Navigation

None apply.

##### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0001 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Routing regressions in the validation-routing suite |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0002 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Guide and consumer routing regressions and drift guard |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0003 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Recorded before and after selection, time and mutation results |

## 적용과 확인

### 적용 방법

Apply these routes through `scripts/validation/registry.json`; contributors
register a test module by editing its suite file.

### 확인 기준

Routing regressions prove selection, and mutation results prove detection for
the sampled defects. Hosted timing after merge is a separate observation.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [Workspace governance requirements](../../01.requirements/0003-workspace-agent-governance-platform.md) |
| designs | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) |

### 외부 근거

The package D18 design and PR341 timing are dated inputs; no external
standard is adopted.
