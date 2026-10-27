---
title: "Traefik Ingress Cutover Execution"
version: "0.4.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0121-TSK-0001"
parent_ids: ["SPEC-0121-PLAN-0001"]
---

# Task: Traefik Ingress Cutover Execution

## Overview

Execute [SPEC-0121](../spec.md) through [WORK-001–004](../plan.md#work-breakdown):
preparing ingress-nginx and running Traefik side by side, live verification,
the cutover and its revert evidence.

## Inputs

- The operator's 2026-10-20 instruction to write the ADR-0050 cutover Spec,
  with the Spec, Plan and Task approved in this round and the live cutover in
  later implementation pull requests.
- Start: main `8686ca24` (PR #162 merge), branch
  `docs/spec-0121-traefik-cutover` in a separate worktree.
- The 2026-10-20 observation of the first ingress-nginx v1.15.1 sync:
  - the Application Synced and Healthy at revision 4.15.1;
  - both admission hook Jobs succeeded;
  - the admission webhook carried its CA bundle;
  - `verify-ingress-tls.sh` passed.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-TC-001](../spec.md#success-criteria--verification-plan) | Prepare ingress-nginx, then Traefik side by side | platform | completed | PASS | EVD-006 preparation render, EVD-007 class handover, EVD-008 and EVD-010 side-by-side render, EVD-009 side-by-side status |
| WORK-002 | [VAL-TC-002](../spec.md#success-criteria--verification-plan) | Live per-route verification | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-TC-003](../spec.md#success-criteria--verification-plan) | Cutover and ingress-nginx removal | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-004 | [VAL-TC-004](../spec.md#success-criteria--verification-plan) | Revert evidence | platform | ready | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-TC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Side-by-side Application status | Live Argo CD status of `platform-traefik` after WORK-001 merges | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-TC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Live IngressClass handover check | `kubectl get ingressclass nginx` and its tracking label after the preparation pull request merges | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-TC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Live route checks | Per-route curl through the Traefik port-forward | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-TC-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Live router checks after cutover | `verify-ingress-tls.sh` with `CHECK_K8S_ROUTER=true` and per-route curl after WORK-003 merges | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-TC-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Revert evidence | Live revert or branch render of the cutover revert | NOT_RUN | Pending | yes | none |
| EVD-006 | [VAL-TC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Preparation chart render | `helm template` of `ingress-nginx` 4.15.1 with the preparation values, against the same chart without them; `kustomize build gitops/platform/ingress-routes` | PASS | Chart IngressClass 1 to 0, ValidatingWebhookConfiguration 1 to 0, hook Jobs 2 to 0; the controller keeps `--ingress-class=nginx` and `--controller-class=k8s.io/ingress-nginx`; the neutral manifest renders IngressClass `nginx` with controller `k8s.io/ingress-nginx` | no | none |
| EVD-007 | [VAL-TC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Live IngressClass handover check | Operator-approved read-only `kubectl` and route probes on 2026-10-27, after main `01f08f41` (PR #166) synced | PASS | IngressClass `nginx` carries tracking id `platform-ingress-routes:networking.k8s.io/IngressClass:ingress-nginx/nginx`; no ingress-nginx ValidatingWebhookConfiguration remains; `platform-ingress-nginx` Synced and Healthy, controller 1/1; all six route hosts answered (200, 301 or 302) through `172.18.0.240`. `argo` and `rollouts` timed out once during the controller rollout and answered on the next probe. The live `Prune=false` annotation, the old Helm labels on the class and the orphaned `ingress-nginx-admission` Secret remain | yes | EVD-002 |
| EVD-008 | [VAL-TC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Side-by-side chart render | `helm template` of `traefik` 42.1.3 (Traefik v3.7.16) with the `platform-traefik` values and `--skip-crds`; `bash scripts/render-platform-chart-kinds.sh` | PASS | Rendered kinds are ServiceAccount, ClusterRole, ClusterRoleBinding, Deployment and a `ClusterIP` Service, with no IngressClass and no CRD; the only provider flags are `--providers.kubernetesingressnginx` with `ingressClass=nginx` and `controllerClass=k8s.io/ingress-nginx`; the pod sets seccompProfile RuntimeDefault; the chart-kind check passes against the platform AppProject | no | none |
| EVD-009 | [VAL-TC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Side-by-side Application status | Read-only `kubectl` on 2026-10-27, after main `5f68e9c3` (PR #168) synced | PASS | `platform-traefik` Synced and Healthy; namespace `traefik` has baseline audit and warn and `istio-injection=enabled`; Deployment `docker.io/traefik:v3.7.16` 1/1 with its pod 2/2 (sidecar injected); Service `traefik` is `ClusterIP` only; IngressClass `nginx` is still the only class; no Traefik CRD exists; every Ingress `status.loadBalancer` is still `172.18.0.240`; no error in the Traefik log | yes | EVD-001 |
| EVD-010 | [VAL-TC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Side-by-side render scope | PR #168 independent review of EVD-008 | PASS | Narrows EVD-008: "no CRD" holds for the `--skip-crds` render that matches `skipCrds: true`; `scripts/render-platform-chart-kinds.sh` ignores `skipCrds` and lists CustomResourceDefinition, which the AppProject allows. Besides the provider flag with `ingressClass` and `controllerClass`, the render carries the chart defaults `ingressClassByName=false`, `watchIngressWithoutClass=false`, `disableSvcExternalName=false` and the entrypoint flags. The chart ClusterRole can update Ingress status; that stays inert while `publishService` and `publishStatusAddress` are unset, and the cutover revisits it | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-TC-001](../spec.md#success-criteria--verification-plan) | pending | EVD-006, EVD-007, EVD-008, EVD-009, EVD-010 | Evidence complete; operator acceptance remains | platform |
| [VAL-TC-002](../spec.md#success-criteria--verification-plan) | pending | none | Live route checks remain | platform |
| [VAL-TC-003](../spec.md#success-criteria--verification-plan) | pending | none | Cutover pull request remains | platform |
| [VAL-TC-004](../spec.md#success-criteria--verification-plan) | pending | none | Revert evidence remains | platform |

## Approval and Safety Boundaries

- **Allowed Paths**:
  - `docs/03.specs/0121-traefik-ingress-cutover/**`
  - `docs/03.specs/README.md`
  - `docs/01.requirements/0004-current-local-gitops-platform.md`
  - `docs/02.architecture/**`
  - `docs/05.operations/**`
  - `gitops/**`
  - `infrastructure/**`
  - `examples/**`
  - `scripts/validation/**`
  - `scripts/validate-infrastructure-contracts.sh`
  - `tests/**`
  - `README.md`
  - `.env.example`
- **Forbidden Paths**: `.github/workflows/**`, provider settings, other Spec
  packages' evidence, credentials.
- **Approval Required**:
  - The operator's 2026-10-20 instruction is recorded as approval of SPEC-0121
    and its Plan as written on that date. The operator may revoke or amend it.
  - Each implementation pull request, and each live change outside Argo CD
    sync, needs its own operator approval.
  - Push, pull request and merge follow RUN-0013.
  - On 2026-10-27 the operator approved authoring the WORK-001 preparation
    pull request. Its merge still needs the live `Prune=false` annotation on
    IngressClass `nginx` first, then the EVD-002 check after the sync.
  - On 2026-10-27, after EVD-007 passed, the operator approved the WORK-001
    side-by-side pull request. Its merge starts the `platform-traefik` sync;
    EVD-001 follows that sync.
- **Static Validation**: Focused tests, the chart render and `qa.py staged` on
  the exact index.
- **Live Validation**: Operator-run checks for WORK-001 to WORK-004.
- **Secret / Vault Handling**: No secret is read or written.
- **Rollback Plan**: Revert the pull request of the affected work unit through
  Git; Argo CD restores the previous controller state.
- **Evidence Location**: This Task.

## Verification Summary

WORK-001 passed: the preparation render (EVD-006), the live class handover
(EVD-007), the side-by-side render (EVD-008, narrowed by EVD-010) and the
side-by-side Application status (EVD-009). VAL-TC-001 awaits operator
acceptance. The WORK-002 port-forward route checks are operator-run and
remain NOT_RUN.
