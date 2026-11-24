---
title: "Product Test Boundary"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0237"
---

# Product Test Boundary Technical Specification (Spec)

## 문서 개요

### 목적과 독자

This Spec states the P14 change contract for the Kubernetes product's test
boundary. The platform owner and reviewers use it to judge whether the
product architecture describes only the product, whether the workspace test
environment states its current facts, whether the production LAN residue is
closed by an observed boundary, and whether documentation changes stay free
of product rollout.

### 책임과 적용 범위

This Spec owns the P14 behavior and acceptance criteria. The [Plan](plan.md)
owns the work order, risks and rollback, and the
[Task](01.tasks/tsk-0001-product-test-boundary.md) owns execution and
evidence.

## 내용 계약

### 입력과 전제

The operator entered `prompts/P14-K8S.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-24 at `main@94b3ed72`. Design D14 and finding K23-14 assign the
product to the current manifests, charts and selected cluster, and the
workspace harness and local VM to `docs/00.workspace` and `.agents`; they ask
to keep the GitOps tree and the selected k3d runner, reuse the P07 isolation
evidence, mark refused Applications as unvalidated rather than complete, and
keep documentation changes free of full rollout. Residues W09-H02 and W06-H02
were open. No product manifest, chart or Application changes.

### 본문과 규칙

#### Overview

##### Goal

[AD-0007](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md)
keeps only the product-facing boundary: product policies allow LAN egress to
the external services, test clusters deny the host and LAN below them, and
only 5 of 20 Applications are selectable, none starting a pod. The runner's
mechanics move to
[GDE-0013](../../00.workspace/05.environment/0013-selective-execution-environment.md),
which states the host route, the observed LAN denial and the current VM
result. W09-H02 closes from the P07 observation.

###### Owning Requirements

[REQ-0004-FR-0003](../../01.requirements/0004-current-local-gitops-platform.md)
owns the product's external interface, and
[REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md)
the shared workspace tooling. [AD-0007](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md)
and [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md)
stay the architecture owners; no new decision is needed.

##### Consumers

AD-0007, GDE-0013, the SPEC-0223 residue handoff and ledger, and the
affected-surface selection in `scripts/validation/registry.json`.

#### Scope

##### In Scope

- The product and environment documentation split and their current facts.
- The W09-H02 closure from reused P07 evidence.
- Confirmation of the documentation-only validation route.

##### Out of Scope

Manifest, chart, Application or runner changes, a new or repeated cluster
run, support for remote charts or CRDs without a change targeting them, the
SPEC-0229 criterion decisions, and W06-H02, which waits for a manifest or CI
lock change.

#### Behavior Contract

##### Inputs and Outputs

AD-0007 names the selectable Applications and the reason the others are
refused, states product workload readiness as unobserved, and links the
environment guide for the runner. GDE-0013 states admission, the isolated
host route, the disk watchdog as a polling bound, the observed probes and the
current VM result, and points to the P07 Task for its review history.

##### Failure Behavior

A refused Application is not reported as validated product scope. A change
that targets a refused Application must design and pin its chart or CRD for
that Application; syncing the whole root is not a substitute.

#### Acceptance Criteria

##### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| AC-0001 | AD-0007 describes only the product-facing test boundary and the real selectable scope, and GDE-0013 owns the runner's current mechanics and results. |
| AC-0002 | W09-H02 is closed in its owning Task from the observed P07 host-route LAN denial below the product policies, without a new cluster. |
| AC-0003 | Documentation changes under the product trees and the product architecture select document checks only, while a manifest change selects the offline render, schema and policy gates, and none requires a live rollout. |

##### Verification Strategy

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-DOCS | Profile, links and lifecycle of the changed documents | Staged index | Repository static | Every document change | Staged QA |
| CHK-SELECT | Selected validators per path | Registry and selector | Repository static | Once for this change | Task Results |
| CHK-CATALOG | Current selectable Applications | Current checkout | Local read-only | Once for this change | Task Results |

###### Normative and Evidence

AD-0007 owns the product boundary and GDE-0013 the environment procedure.
Design D14 and K23-14 are dated inputs.

###### Historical and Navigation

None apply.

##### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0004-FR-0003](../../01.requirements/0004-current-local-gitops-platform.md) | AC-0001 | [AD-0007](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md) | Document review and catalog |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0002 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Reused observation and source read |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0003 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Selector run |

## 적용과 확인

### 적용 방법

Read AD-0007 for the product boundary and GDE-0013 for the runner; select
only Applications the catalog supports.

### 확인 기준

Static checks and the selector are repository evidence; the reused P07 rows
are the live boundary evidence.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [Current local GitOps platform requirements](../../01.requirements/0004-current-local-gitops-platform.md) |
| designs | [AD-0007](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md) |

### 외부 근거

Design D14 is a dated input; no external standard is adopted.
