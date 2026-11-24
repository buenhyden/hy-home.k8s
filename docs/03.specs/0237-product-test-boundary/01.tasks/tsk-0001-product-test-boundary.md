---
title: "Product Test Boundary Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0237-TSK-0001"
parent_ids: ["SPEC-0237-PLAN-0001"]
---

# Task: Product Test Boundary

## 문서 개요

### 목적과 독자

This Task records the P14 execution and evidence for the [Plan](../plan.md)
and [Spec](../spec.md). The operator and reviewers use it to separate
document changes, reused live evidence and criterion acceptance.

### 책임과 적용 범위

WORK-001 serves AC-0001 through AC-0003. This Task owns P14 work state,
results and criterion decisions.

## 내용 계약

### 입력과 전제

The operator entered `prompts/P14-K8S.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-24, authorizing bounded implementation, verification and
commit, push, pull request and merge. Intake found branch `main` at
`94b3ed72d43bbb7007524162546012f8c0e10ae2` with a clean worktree. Earlier
packages are not re-executed.

### 본문과 규칙

#### Scope

##### Objective and Parent

WORK-001 executes the [Plan work unit](../plan.md#work-units) for the three
[Spec criteria](../spec.md#criteria).

##### Inputs and Authority

The current user P14 message is the scoped request reference; EVD-001
records the execution receipt. The Spec and Plan stay `draft`; the receipt
grants no formal approval or criterion acceptance.

- **Allowed Paths**: the [Plan WORK-001](../plan.md#work-units) write scope; the runner is used read-only.
- **Forbidden Paths**: product manifests, charts and Applications, other repositories, the user's provider configuration, and P15–P17.
- **Approval Required**: none beyond the current P14 request for ordinary Git delivery; no cluster is started.
- **Static Validation**: staged document checks and the selector run.
- **Live Validation**: none new; the P07 host-route rows are reused.
- **Secret / Vault Handling**: no secret is read or printed.
- **Rollback Plan**: revert the commit.
- **Evidence Location**: this Task's Results.

#### Execution Log

##### Work Performed

AD-0007's selective test section, which described admission, dispatchers,
the host network, the VM route and guest transport and still called the LAN
denial unobserved, is replaced by the product-facing boundary: the product
policies allow LAN egress to the external services, a test cluster denies
the host and LAN below them (SPEC-0229 EVD-088 and EVD-089), only 5 of 20
Applications are selectable and none starts a pod, and support for a chart or
CRD is designed for the Application a change targets. GDE-0013 now states the
shared admission and the isolated host route moved from AD-0007, the disk
watchdog as a polling bound after option C, the observed probes, the current
VM result and the two applied Applications, and points to the P07 Task for
its review history instead of retelling it. W09-H02 is closed in the
SPEC-0223 Task (its EVD-046) and the ledger.

##### Blockers and Decisions

No cluster was started: no product manifest changed and no selectable
Application runs a pod, so a new run would repeat EVD-088 without a product
workload. P07's plan promoted the test-cluster contract to AD-0007; D14
assigns the runner to `docs/00.workspace`, so AD-0007 keeps the product-facing
boundary and GDE-0013 the contract. W06-H02 stays open until a pull request
changes a GitOps manifest or the CI lock. The 15 refused Applications stay
refused; their chart or CRD support waits for a change that targets one. The
SPEC-0229 criterion decisions stay with the operator.

##### Lifecycle Traceability

| Item | Upstream criterion | Result | Evidence |
| --- | --- | --- | --- |
| WORK-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | PASS | Catalog (EVD-002); selector (EVD-003); W09-H02 closure (EVD-004) |

#### Verification Evidence

##### Results

| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | observation | {"actor":"user","approval_ref":"Current human P14-K8S.md request of 2026-11-24 in this conversation for package workspace_governance_remediation_1_2_0_20261123, bounded implementation, verification and commit/push/PR/merge","scope":["SPEC-0237","SPEC-0237-PLAN-0001","SPEC-0237-TSK-0001"],"reviewed_spec_sha256":"f27c56d41ebd8b369da7ddf719c0a13173cf9243ab3a235a69252b2aeb0d8a62","reviewed_plan_sha256":"153331a2af0f349617bae8d1fe431284d19b39d78e692bdd06f9f7e8c16643ac","request_revision":"1cb89e9991114447c60ab82ebcaaabc251fe1403a9954bb76c296701ca50a656","validity":"confirmed","revocation":"none"} | Current trusted human request; request revision is the validator-defined digest of this Task's scope and work items; exact draft parent hashes | Scoped execution approval | none | PASS | Records the current P14 execution scope only; no formal Spec or Plan approval or criterion acceptance follows | true | none |
| EVD-002 | [AC-0001](../spec.md#criteria) | WORK-001 | observation | Checkout `94b3ed72`, 20 root Applications | `scripts/test_cluster.py` | `python3 scripts/test_cluster.py --root . catalog` | 0 | PASS | Supported: `platform-namespaces`, `platform-network-policies`, `platform-external-services`, `platform-headlamp-config`, `platform-ingress-routes`; root: `platform-cluster-config`; unsupported: 9 remote charts and 5 Applications needing the `external-secrets.io` or `cert-manager.io` CRD. The supported five hold only Namespace, NetworkPolicy, Service, EndpointSlice, Ingress and IngressClass objects | true | none |
| EVD-003 | [AC-0003](../spec.md#criteria) | WORK-001 | automated | One path at a time | `scripts/select-affected-surfaces.py --lane affected` | Select for `gitops/README.md`, the AD-0007 path and `gitops/platform/network-policies/kustomization.yaml` | 0 | PASS | README: the four document checks; AD-0007: the document checks and the residue ledger; manifest: `gitops-change-set`, `gitops-structure`, `k8s-manifests`, `platform-assurance`, `policy-gates`, `infrastructure-contracts`, `external-service-contracts`, `secret-handling`, `repository-quality` and `markdown-profiles`. No selection starts a cluster or rollout | true | none |
| EVD-004 | [AC-0002](../spec.md#criteria) | WORK-001 | observation | SPEC-0229 EVD-085 and EVD-088 to EVD-090; the `up` route code | Source read; no new run | Read the rows and `scripts/test_cluster.py` route selection | 0 | PASS | The host route always builds the isolated network before any apply; LAN and host denial were observed below the applied product policies and without policy, with owned cleanup. W09-H02 closed as SPEC-0223 EVD-046 and its ledger entry made terminal | true | none |

##### Resolution Links

None.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Intent | Acceptance | Evidence | Decision | Accepted By | Current Owner | Reassigned To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [AC-0001](../spec.md#criteria) | accept | pending | EVD-002 | Awaiting the operator's decision | none | platform | none |
| [AC-0002](../spec.md#criteria) | accept | pending | EVD-004 | Awaiting the operator's decision | none | platform | none |
| [AC-0003](../spec.md#criteria) | accept | pending | EVD-003 | Awaiting the operator's decision | none | platform | none |

##### Remaining Conditions

Hosted checks are recorded when they run. W06-H02 waits for a manifest or CI
lock change; product workload readiness in a test cluster stays unobserved.

#### Handoff

##### Promotion Receipt

P14-PRODUCT-BOUNDARY: [AD-0007](../../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md)
states the product-facing test boundary; the consumer
[GDE-0013](../../../00.workspace/05.environment/0013-selective-execution-environment.md)
states the runner's current mechanics and results.

##### Next Owner

The platform owner records hosted results; the operator decides the
criteria. The next package input is `prompts/P15-CLEANUP.md`; this Task does
not run it.

## 적용과 확인

### 적용 방법

Use this Task for P14 evidence and leave criteria pending until the operator
records decisions.

### 확인 기준

EVD-002 and EVD-003 are local and repository-static evidence; EVD-004
reuses the P07 live rows.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [SPEC-0237 Plan](../plan.md) |
| verifies | [SPEC-0237](../spec.md) |

### 외부 근거

Design D14 is a dated input; no external standard is adopted.
