---
title: "Selective Validation Environment and Aggregate Resource Boundary"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-20"
artifact_id: "SPEC-0229"
---

# Selective Validation Environment and Aggregate Resource Boundary Technical Specification (Spec)

## 문서 개요

### 목적과 독자

This change gives local validation operators a selected k3d environment with
aggregate resource admission, recoverable ownership and an actual production
LAN boundary. Implementers, reviewers and operators use the contract.

### 책임과 적용 범위

This Spec owns P07 behavior and acceptance. The [Plan](plan.md) orders the
work; the [Task](01.tasks/tsk-0001-selective-environment.md) owns execution,
observations and criterion decisions. Workspace preparation belongs to the
[environment collection](../../00.workspace/05.environment/README.md),
product structure to [AD-0007](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md),
and provider facts to their respective notes. This draft grants no separate
parent approval, live-cluster operation or criterion acceptance.

## 내용 계약

### 입력과 전제

The current human P07-ENVIRONMENT request in the 1.1.0 package authorizes
scoped implementation, verification and ordinary Git delivery. D07, the Q03
decision, execution contract, k8s profile/findings and current repository are
design inputs. Intake was on `codex/p01-ci-routing` at
`c7ed0be33e60e05294e341b46a395215c4345900`, clean. The eleven earlier
streams and P00–P06 remain predecessor evidence, not repeated work. The
[SPEC-0223 Task](../0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md)
retains W09-H02's actual LAN isolation failure and W07-H05's distinct
Desktop→SSH reviewer failure. A passing static configuration cannot close
either failure.

### 본문과 규칙

#### Overview

##### Goal

Keep the existing small k3d, dedicated kubeconfig and owned cleanup while
making direct starts and dispatcher starts share one admission limit. Each run
selects only required GitOps components and dependencies, reserves finite
resources before spawning, and proves its network and native boundaries at
their actual execution surfaces.

###### Owning Requirements

[REQ-0003-FR-0007, FR-0009, FR-0010, FR-0022, FR-0026 and NFR-0004](../../01.requirements/0003-workspace-agent-governance-platform.md)
constrain authority, native enforcement, ownership, scratch and evidence.
[REQ-0004-FR-0008 and FR-0010](../../01.requirements/0004-current-local-gitops-platform.md)
require validation depth and fail-closed platform contracts. [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md)
separates provider configuration from runtime evidence; [AD-0007](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md)
and [ADR-0014](../../02.architecture/02.decisions/0014-current-local-gitops-platform-contract.md)
identify the current local GitOps platform. This bounded correction does not
claim a new product architecture decision.

##### Consumers

`scripts/test_cluster.py` direct commands, `scripts/work_parallel.py`
dispatches, their focused tests, selected GitOps Application inventory,
environment guidance, provider notes, quality checks and the existing residue
Task consume the result. P08 and P12 consume the finite native execution plan.

#### Scope

##### In Scope

Current Linux host tool and account metadata without secret values; a durable
selective-environment guide at `docs/00.workspace/05.environment/0013-selective-execution-environment.md`;
one
supported Codex and Claude route each; workspace/common-dir binding; shared
admission across direct and dispatched runs; final component closure; bounded
CPU, memory, disk and time; pre-spawn intent and interrupted-run recovery;
owned cleanup; selected k3d and API validation; host or VM production LAN deny
with a controlled endpoint; focused checks and honest status handoff.

##### Out of Scope

Earlier accepted implementations, a full product stack start, requests to a
real production endpoint, broad host firewall replacement, trust bypass,
credential or subscription change, repeated paid probes, P08–P17 execution,
and deletion of the input package before P17. P12's separate untrusted worker
containment defect remains its own work.

#### Behavior Contract

##### Inputs and Outputs

The run identity binds this checkout, Git common directory and whether it is
an independent clone or linked worktree. Selection resolves the current
repository's full product inventory, requested GitOps Applications and actual
dependency closure. Missing, wildcard, or full-product selections fail. Two
small requests cannot admit a union equal to the forbidden full inventory.
Direct starts and dispatchers use one owner of atomic reservations. Aggregate
CPU, memory and disk reservations and active closure stay within host-derived
finite limits; a selector count is not an OS resource limit. A reservation
records the run token, owner intent and discoverable cluster/process labels
before spawn. A child cannot execute side effects until durable started
ownership is confirmed under the lease lock. Recovery records a tombstone
under that same lock before release; a delayed child seeing the tombstone
exits without creating resources. A plain parent `Popen` return followed by
a status write does not meet this gate. Recovery verifies owned labels,
process start identity and actual liveness before reclaiming only its run's
resources. Ambiguous ownership retains the lease for operator inspection;
`/proc/*/environ` and secret values are never scanned. A timer or reusable
PID alone never frees a lease.
Timeout and cancellation propagate to children. On the host route the
operator chose on 2026-11-24 an accounted disk bound instead of a hard cap:
admission reserves the run's disk, and a watchdog measures the node's
writable layer and data volumes, kills the node when use passes the
reservation or cannot be measured three times in a row, and fails the run
with `CLUSTER_DISK_LIMIT`. It is a polling bound, not a kernel quota, and is
never presented as one; the bounded VM route remains the hard-cap option.

The existing one-server/no-load-balancer k3d setup retains loopback API and
dedicated kubeconfig without changing the default context. Components start
only after dependency calculation and admission. Per-Application support
records source type, fixed chart/version or local source, CRD/controller
dependencies, namespace, render/API/live depth, readiness, secret substitute
and cleanup. Unsupported remote charts or CRDs fail for the selected
component; a full root sync is not a fallback. Test namespace quota and
limits, host/container caps and runtime egress are distinct controls.

Production LAN isolation is enforced outside additive product NetworkPolicy,
through a scoped host/container boundary or isolated VM. On the host route
the owned network is internal with isolated gateway mode, so the host holds
no address on the bridge and `kubectl` runs inside the node. The isolation also
covers IPv6 or disables it, and verifies the owned interface and network,
default route, proxy configuration, and absence of host mounts, Docker socket
and privileged product pods before startup. The k3d node's required privilege
does not grant product pods or untrusted workers a broader boundary. A controlled test
endpoint checks allowed and denied paths; no real production service receives
a probe. After topology preflight, one disposable controlled probe pod may
run in the selected product namespace under its actual policies. No product
workload pod starts until this probe confirms both paths. Native
reviewer state records effective parent, tools, file/MCP/hook/network scope and
actual denied-write result. The previously verified Codex CLI and Claude
review routes may be reused only when binary, version, configuration, input
and permission boundary match. The original Desktop→SSH failure remains
separate.

Provider attempts use existing accounts, available models and current quota.
Each representative call is at most 600 seconds and six task turns where the
installed client supports that limit; actual parallel workers are at most two.
Initial and one repaired confirmation are the planned limit, not a repeated
CI job. Actual monetary charge remains unknown when no billing result exists.
`ready`, `missing`, `unsupported`, `unobserved`, `failed` and `not-applicable`
describe distinct capabilities; source write is separately `denied`,
`allowed` or `unobserved`.

##### Failure Behavior

Admission refuses missing inventory, unbounded resource budgets, aggregate
limit breaches and full-product closure before starting a resource. A start
failure retains discoverable ownership until inspected cleanup succeeds. A
stale lease is recovered only after the child gate is tombstoned and identity
and liveness checks succeed; ambiguous orphans retain their reservations.
If host isolation cannot be applied or a controlled negative or positive
probe fails, W09-H02 stays `failed` and product workload startup is
blocked. If native authentication, quota or permission is unavailable, only
the dependent attempt stops and its actual cause is recorded. An actual
allowed source write is `failed`, never relabelled `unobserved`.

#### Acceptance Criteria

##### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| AC-0001 | Current host, Git binding, toolchain, container/cluster/CI runner and supported Codex/Claude account, binary, version, options and trust state are recorded without secret values; finite native calls and prior valid observations are mapped to one route per provider. |
| AC-0002 | Direct and dispatcher starts atomically share inventory and aggregate component, CPU, memory, disk and time admission; split selections and concurrent over-budget requests fail before spawn, while pre-spawn intent permits recovery after an interrupted start. |
| AC-0003 | Selected k3d Applications run with only their dependency closure, bounded resources, dedicated kubeconfig, explicit readiness and owned cleanup; unsupported charts/CRDs fail closed at the affected depth, and disk use stays within the reserved budget through a hard cap or an accounted watchdog bound that aborts the run. |
| AC-0004 | The production LAN deny is enforced at a host/container or VM boundary; one disposable probe pod in the selected product namespace confirms controlled denied and allowed paths before any product workload pod runs. Prior W09-H02 failure remains open until both actual paths pass. |
| AC-0005 | P06's matching native reviewer evidence is reused, any still-required permission probe runs once after environment readiness, and original Desktop→SSH failure, static configuration, provider runtime and actual source-write outcomes stay distinct. |
| AC-0006 | Focused races, cancellation/orphan and component regressions, selected local and hosted checks, cleanup, outstanding limits and next P08/P12 consumers are recorded with implementation, verification and user acceptance as separate states. |

##### Verification Strategy

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| aggregate-admission | Two competing direct/dispatcher runs cannot exceed closure or resource caps; crash-window intent remains recoverable | Focused concurrent fixtures and existing runner entry points | Local code and filesystem lock, not OS isolation | Admission code changes | Task Results |
| selected-k3d | Selected components, dependencies, limits, readiness and owned cleanup behave on a dedicated cluster | Current inventory and selected small profile | Local container/cluster only | Environment ready and scoped run authorized | Task Results |
| lan-boundary | Controlled allowed/denied endpoint behavior under actual host/container/VM isolation | Isolated test network and disposable probe pod in selected product namespace, no production endpoint | Host network and selected product policy path | Before product workload pods | Task Results; W09-H02 closure only after both paths PASS |
| native-boundary | Installed provider route actually confines source write and exposes effective scope | Reused matching P06 result or one bounded repaired route probe | Provider runtime, not static configuration | Environment/permission boundary changed | Task Results and P06 handoff |
| document-contract | New Spec/Plan/Task and affected current owners satisfy profile, link and lifecycle rules | Exact candidate index | Repository static | Document change | Task Results |
| selected-qa | Current candidate's affected checks and hosted selected leaves pass | Exact local index and PR candidate | Local/hosted, not live | Delivery | Task Results and PR run |

###### Normative and Evidence

[Quality](../../00.workspace/04.quality/quality.md),
[approval](../../00.workspace/04.quality/approval-and-safety.md),
[environment](../../00.workspace/05.environment/README.md),
[SPEC-0223 Task](../0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md)
and its ledger own current rules and prior results. D07/Q03 are the design
input; observed runtime state belongs in this Task.

###### Historical and Navigation

[SPEC-0228](../0228-independent-review-boundary/spec.md) and its Task record
P06's verified routes and limits. They do not prove P07 LAN isolation or
admission across runs.

##### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0009](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0001 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Actual installed tool and account metadata, route comparison |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0002 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Competing admission and interrupted-start regression |
| [REQ-0004-FR-0008](../../01.requirements/0004-current-local-gitops-platform.md) | AC-0003 | [AD-0007](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md) | Selected k3d render/API/live and cleanup evidence |
| [REQ-0004-FR-0010](../../01.requirements/0004-current-local-gitops-platform.md) | AC-0004 | [AD-0007](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md) | Controlled host network denial before product pods |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0005 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Named native route, denied source write and retained failure |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0006 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Named local, hosted and runtime evidence |

## 적용과 확인

### 적용 방법

Use the [Plan](plan.md) for P07 work and stop at the actual host or provider
boundary when it cannot be proven. No later prompt runs automatically.

### 확인 기준

Static contracts, actual sandbox/network behavior, hosted CI and operator
criterion acceptance each require their own result.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) |
| requires | [REQ-0004](../../01.requirements/0004-current-local-gitops-platform.md) |
| designs | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) |
| designs | [AD-0007](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md) |
| implements | [P07 Plan](plan.md) |

### 외부 근거

The package's D07 and sources summarize dated primary Kubernetes, k3d,
Codex and Claude documentation. Installed options and local runtime behavior
must be observed on this workspace before a capability claim is made.
