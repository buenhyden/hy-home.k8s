---
title: "Selective Validation Environment and Aggregate Resource Boundary Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-11-20"
artifact_id: "SPEC-0229-PLAN-0001"
parent_ids: ["SPEC-0229"]
---

# Selective Validation Environment and Aggregate Resource Boundary Implementation Plan

## 문서 개요

### 목적과 독자

This Plan orders the P07 environment change under the [Spec](spec.md).
Implementers, reviewers, quality owners and the operator use it to distinguish
planned checks from observed results.

### 책임과 적용 범위

The Spec owns behavior and six criteria. This Plan owns dependencies, work
order, risks, verification and promotion. The [Task](01.tasks/tsk-0001-selective-environment.md)
owns actual execution, evidence and criterion decisions.

## 내용 계약

### 입력과 전제

The current P07 request authorizes bounded implementation, validation and
ordinary Git delivery. Package D07, Q03, the k8s profile/findings and the
current repository are design inputs. The intake branch and HEAD are
`codex/p01-ci-routing` and `c7ed0be33e60e05294e341b46a395215c4345900`.
P00–P06 and the eleven earlier merged streams are predecessor evidence;
their matching implementations are reused. Draft parents require an actual
exact-byte review and a current scoped DOCLIFE-R008 execution receipt before
dependent source implementation. Neither step is criterion acceptance.

### 본문과 규칙

#### Overview

##### Outcome

Provide shared admission and recoverable ownership for selected k3d runs;
enforce production LAN denial at the actual host/container or VM boundary;
reconcile installed native routes, limits and remaining P06 evidence. The
result is not a full-stack test, product deployment or automatic P08 run.

##### Constraints

[AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md)
separates native configuration and runtime evidence. [AD-0007](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md)
and [ADR-0014](../../02.architecture/02.decisions/0014-current-local-gitops-platform-contract.md)
describe the current product and network owner. The existing k3d runner's
loopback API, dedicated kubeconfig and owned cleanup remain. W09-H02 is an
observed egress failure, not a request for one more NetworkPolicy. W07-H05
records an original Desktop→SSH failure even if the current CLI route works.

###### Global Constraints

Every work unit inherits the [draft Spec](spec.md#scope) boundaries. The
resource values below are provisional engineering caps, not a new approval
gate or an assertion of host capacity: no more than 3 vCPU (operator,
2026-11-24), 4 GiB memory,
4 GiB writable disk and 600 seconds per small run, subject to actual host
headroom and the existing tighter limits. Admission refuses any unbounded
field; a reservation alone is not a disk bound, so the host route adds the
Spec's watchdog. Select fewer than all
product Applications, even across simultaneous runs. Provider calls stay
within the existing accounts, model availability and quota, at most two
actual parallel workers, one initial and one repaired attempt, sequential
providers and six task turns where the installed CLI supports it. The actual
charge is `null` when unobserved.

###### Risks and Mitigations

An atomic lease can be lost between spawn and status write; record intent
before spawn, gate the child until started ownership is durably confirmed, and
tombstone that gate under the same lock before recovery can release a lease.
A delayed child seeing the tombstone exits. Verify owned labels and process
start identity; ambiguous ownership retains the lease for operator inspection
without scanning `/proc/*/environ` or secrets. Split requests can assemble the full stack; compare the
union of active closure against the current full inventory under one lock.
Host Docker or VM isolation can leave IPv6, default route, proxy, mounts or
privileged pod paths; verify each before product workload startup. After
topology preflight, run one disposable probe pod in the selected product
namespace against controlled positive and negative endpoints. Leave W09-H02
failed if either path fails. An apparent disk
reservation is not a quota; product startup needs the hard cap or the Spec's
accounted watchdog bound, whose polling limit stays a recorded residual. Native quota can be exhausted;
reuse matching P06 evidence and stop only the dependent paid call. These are
high-impact boundary risks for platform and security review, not invented
probability scores.

###### Escalation

If this host lacks a supported scoped network or disk bound, retain
the selected static and render/API work, name the failed or unavailable
product-start condition and the environment operator. A host firewall or VM
change requires its exact target, authority, rollback and evidence; global
rules or another owner's resources are outside this work. An actual new
subscription, privilege, cost or deletion conflict outside current Q03 scope
returns only that affected decision to the user.

#### Dependencies

##### Prerequisites

Read the current inventory, manifests, `scripts/test_cluster.py`,
`scripts/work_parallel.py`, existing tests and actual host capabilities.
Confirm current Git binding and status. Review exact draft Spec/Plan/Task,
record scoped execution receipt and then edit implementation. Select the
existing local validation environment and relevant provider route before
native calls; no secret values are input.

##### Shared Resources

One workspace admission owner and lock bind direct starts, dispatchers and
worker attempts. One selected profile owns ports, network, namespace and
run-token labels; each run cleans only its own resources. Stage 03 Task 223
and ledger retain prior failures while this Task records P07 evidence. The
environment Guide is a durable operating consumer, not a second policy owner.

#### Work Breakdown

##### Work Units

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [AC-0001](spec.md#criteria), [AC-0002](spec.md#criteria), [AC-0003](spec.md#criteria), [AC-0004](spec.md#criteria), [AC-0005](spec.md#criteria), [AC-0006](spec.md#criteria) | Inspect actual host and inventory; add shared admission and selected environment; prove or precisely block actual LAN/native boundaries; record evidence | Exact draft review and scoped execution receipt before source mutation; actual host isolation and controlled probe before product workload pods | [Task](01.tasks/tsk-0001-selective-environment.md) | Focused concurrency/cleanup tests, selected k3d depth, controlled deny, document checks, selected QA and hosted PR |

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | P07 selective environment and aggregate boundary | Current P07 request, exact draft review, R008 receipt and actual host facts | platform | `scripts/test_cluster.py`, `scripts/work_parallel.py`, minimal shared admission helper only if existing state cannot be reused, `tests/test_test_cluster.py`, `tests/test_work_parallel.py`, `scripts/validation/registry.json` only to select their existing focused regressions, `scripts/README.md`, `docs/00.workspace/05.environment/0013-selective-execution-environment.md` and its README, the bounded test-environment section of `docs/02.architecture/01.descriptions/0007-current-local-gitops-platform.md`, current provider notes only for changed facts, SPEC-0223 Task/ledger only for actual residue disposition, this package and Stage 03 README; `.secrets.baseline` only for individually reviewed public R008 digest false positives, without filter or setting changes | AC-0001–AC-0006 | aggregate-admission, selected-k3d, lan-boundary, native-boundary, document-contract, selected-qa |

###### Change and Rollback

Inventory and actual host measurement precede budget selection. Start with
focused failing races and interrupted-start cases, then repair one shared
admission path used by direct and dispatcher entries. Connect selected
component requirements and scoped host isolation; render and API checks may
run before any product pod. Add an operating guide using its own draft,
in-review and active lifecycle. Integrate source, consumers and tests once,
review the exact candidate and run selected QA. Revert the ordinary reviewed
commit if code contracts regress; preserve factual live failures and never
rollback by opening production LAN access.

##### Dependency Edges

Current inventory and host limits precede reservation configuration. Atomic
intent precedes process or cluster spawn. Actual network and disk-bound
enforcement and controlled selected-namespace probe precede product workload startup. Selected live checks follow only
their required dependency closure. P06 read-only evidence may carry only
under the same version/configuration/scope; any repaired route gets its own
small probe. Operator criterion acceptance follows concrete evidence and is
not inferred from Task status, CI or a merge.

#### Verification Plan

##### Selected Checks

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| aggregate-admission | Two direct/dispatcher runs and interrupted starts preserve closure and resource caps | Focused races, duplicate selection, stale and live lease fixtures | Local lock and state, not OS disk/network isolation | Admission code change | Task Results |
| selected-k3d | Selected Application support, dedicated kubeconfig, quotas/limits, readiness and owned cleanup | Current manifest inventory and one small profile | Local cluster only | Environment ready and authorized | Task Results |
| lan-boundary | Denied and allowed paths on an isolated network with no production request | Controlled endpoints, actual host/container/VM rule and one disposable selected-namespace probe pod | Host or VM networking plus actual product policy, not static NetworkPolicy | Before product workload pods | Task Results and W09-H02 disposition after both paths PASS |
| native-boundary | Effective provider path and source-write behavior match the reviewed route | P06 same-condition record or bounded repaired probe | Provider runtime | Permission boundary changed or P06 observation still required | Task Results |
| document-contract | Draft package, eventual Guide and owners meet profile, links and lifecycle | Exact files/index and later commits | Repository static | Document change | Task Results |
| selected-qa | Required affected local and hosted leaves pass | Final index and PR candidate | Local and hosted only | Delivery | Task Results and PR run |

##### Evidence Plan

Record intake and current tool/host identity first. Preserve RED/GREEN tests,
the exact reviewed draft bytes and R008 receipt before source changes. Each
actual selected run records command, environment, input, result, cleanup and
limits; a static check never substitutes for a host/network or provider
observation. Run the selected affected lane on the final candidate and hosted
purpose/style on the actual PR run. Do not replay unchanged model probes or
whole-suite QA at each commit. Task-only factual postflight may carry review
only under the current review-delta rule.

#### Promotion Map

##### Durable Owners

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| P07-PRODUCT-BOUNDARY | [AD-0007](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md) | Update the current platform view with the selected test-cluster and host/VM isolation contract; distinguish intended controls from actual network proof | Current local runtime and namespace policy section, with Task evidence for the actual tested boundary |

##### Consumer Updates

[GDE-0013](../../00.workspace/05.environment/README.md) will guide local
operators through selected execution and finite native reuse; its own active
state will follow the Guide lifecycle. Existing GDE-0011 Python setup and
GDE-0012 reviewer boundary remain their respective owners. The selected
scripts README and P08/P12 Task inputs name current entry points and limits.

## 적용과 확인

### 적용 방법

Use WORK-001 in the [Task](01.tasks/tsk-0001-selective-environment.md) to
record actual results. Product startup waits for actual isolation proof.

### 확인 기준

The planned checks close only with their stated input and guarantee. Static,
native, live, hosted and operator decisions remain separate.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [P07 Spec](spec.md) |
| implements | [P07 Task](01.tasks/tsk-0001-selective-environment.md) |
| cites | [AD-0007](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md) |

### 외부 근거

The package D07 and sources summarize primary k3d, Kubernetes, Git,
Codex and Claude capabilities. Installed and runtime behavior must be
checked before recording current success.
