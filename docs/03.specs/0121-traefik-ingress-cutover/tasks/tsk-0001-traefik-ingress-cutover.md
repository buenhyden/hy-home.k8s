---
title: "Traefik Ingress Cutover Execution"
version: "0.8.0"
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
| WORK-002 | [VAL-TC-002](../spec.md#success-criteria--verification-plan) | Live per-route verification | platform | completed | PASS | EVD-011 routes; EVD-012 differences fixed by PR #170 (EVD-013, EVD-016); EVD-014 mesh path; EVD-015 forwarded headers; EVD-017 closes EVD-003; EVD-018 narrows them. The Rollout canary step moves to VAL-TC-003 (Spec 0.5.0) by operator decision |
| WORK-003 | [VAL-TC-003](../spec.md#success-criteria--verification-plan) | Cutover and ingress-nginx removal | platform | completed | PASS | EVD-019 static checks; EVD-020 cutover; EVD-021 canary; EVD-022 closes EVD-004 |
| WORK-004 | [VAL-TC-004](../spec.md#success-criteria--verification-plan) | Revert evidence | platform | in-progress | PASS | EVD-023 revert render closes EVD-005; the live revert was not exercised; completes when the operator accepts VAL-TC-004 |

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
| EVD-011 | [VAL-TC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Live route checks through Traefik | Operator-run `kubectl port-forward` to `svc/traefik` and curl with `Host` and SNI per route, 2026-10-27, compared with the same requests through `172.18.0.240` | PASS | Same status on both routers: adminer 200, headlamp 200, kiali 302 to `/kiali`, the five apex paths 301 to their hosts. Headlamp `/wsMultiplexer` over HTTP/1.1 upgrades with 101 on both. Adminer answers 200 through the Traefik sidecar under STRICT mTLS | no | none |
| EVD-012 | [VAL-TC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | nginx-default comparison | The same port-forward, 2026-10-27: POST of 512 KiB and 2 MiB to adminer, response headers of `/kiali/` | FAIL | ingress-nginx answers 200 and 413 and sends `strict-transport-security: max-age=31536000; includeSubDomains`. Traefik answers 200 and 200 and sends no HSTS header. Traefik v3.7.16 enforces `proxyBodySize` only in its buffering middleware (`pkg/provider/kubernetes/ingress-nginx/middleware.go`), which is skipped while `proxyRequestBuffering` is false, its default; the provider has no HSTS setting. Traefik also passes the upstream `server: envoy` header | no | none |
| EVD-013 | [VAL-TC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Parity values render | `helm template` of `traefik` 42.1.3 with the amended `platform-traefik` values and `--skip-crds` | PASS | Adds `--providers.kubernetesingressnginx.proxyRequestBuffering=true`, `--providers.file.directory=/etc/traefik/dynamic` with a ConfigMap holding only the `hsts` headers middleware, and `--entryPoints.websecure.http.middlewares=hsts@file`; the Service stays `ClusterIP`, no IngressClass, no CRD | no | none |
| EVD-014 | [VAL-TC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Adminer mesh path | Operator-run `kubectl run` of a `curlimages/curl:8.11.1` pod with `sidecar.istio.io/inject=false` in `default`, calling `http://adminer.apps.svc.cluster.local:8080/`, 2026-10-27 | PASS | curl exit 56 (connection reset): STRICT mTLS refuses a caller without mesh identity. Through Traefik adminer answers 200 (EVD-011). Two earlier probes to port 80, where the Service does not listen, timed out (exit 28) and are not evidence | no | none |
| EVD-015 | [VAL-TC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Forwarded headers | Operator-applied temporary `traefik/whoami:v1.11.0` Pod, Service and Ingress (class `nginx`, no TLS) in `default`, requested through `172.18.0.240:80` and through the Traefik port-forward with a spoofed `X_Forwarded_For` header, then deleted, 2026-10-27 | PASS | Both send `X-Forwarded-For`, `X-Real-Ip`, `X-Forwarded-Host`, `X-Forwarded-Port`, `X-Forwarded-Proto` and `X-Request-Id` with the values each router sees; host port and client address differ only by the port-forward. Neither passes the underscore header. Remaining differences: only ingress-nginx sends `X-Forwarded-Scheme` and `X-Scheme`, only Traefik sends `X-Forwarded-Server`; no backend configuration in this repository reads them. Traefik logs that `aliasHeadersStrategy` is unset; setting it to `delete`, as nginx drops such headers, is left to the cutover pull request | no | none |
| EVD-016 | [VAL-TC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Recheck after PR #170 | Read-only `kubectl` after main `36ffc574` synced, then the operator-run port-forward: POST of 512 KiB and 2 MiB to adminer, `/kiali/` headers, Headlamp `/wsMultiplexer` upgrade, 2026-10-27 | PASS | `platform-traefik` Synced and Healthy, pod rolled with `proxyRequestBuffering=true` and ConfigMap `traefik-file-provider`; Service still `ClusterIP`, IngressClass `nginx` the only class, no Traefik CRD, all ten Ingresses still at `172.18.0.240`. Traefik now answers 200 and 413, sends `strict-transport-security: max-age=31536000; includeSubDomains`, and upgrades the WebSocket with 101 | no | none |
| EVD-017 | [VAL-TC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Live route checks | EVD-011, EVD-014, EVD-015 and EVD-016 | PASS | Every route in `ROUTES`, the apex redirect status codes, the adminer mesh path and the listed nginx-default behaviors match ingress-nginx after PR #170. The Rollout canary step is verified at the cutover (EVD-004), as the operator chose | yes | EVD-003 |
| EVD-018 | [VAL-TC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Evidence scope after review | PR #171 independent review of EVD-014, EVD-015 and EVD-017; `kubectl get networkpolicy -A` | PASS | Narrows three rows. EVD-014 observed a reset connection (curl exit 56), not an HTTP `503`: the plaintext caller never completes a request, which is how STRICT mTLS refuses it, and no NetworkPolicy selects ingress in `apps`, so the reset is not a policy drop; Spec 0.5.0 accepts either form. EVD-015 shows no real client address (`127.0.0.6` is the ingress-nginx sidecar, `127.0.0.1` the port-forward), so client-address preservation is checked through the router address after the cutover (EVD-004). EVD-017 no longer needs the canary step: Spec 0.5.0 moves it to VAL-TC-003 | no | none |
| EVD-019 | [VAL-TC-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Cutover static checks | Branch `feat/spec-0121-traefik-cutover`: `helm template` of `traefik` 42.1.3 with the cutover values, `python3 -m unittest tests.test_platform_ingress tests.test_infrastructure_tempfiles`, `bash scripts/validate-infrastructure-contracts.sh`, `bash scripts/render-platform-chart-kinds.sh`, `kubectl kustomize` of the changed directories | PASS | Service `traefik` renders as `LoadBalancer` with NodePorts 30080 and 30443 and `metallb.io/loadBalancerIPs: 172.18.0.240`; `--providers.kubernetesingressnginx.publishservice=traefik/traefik`; `aliasHeadersStrategy=delete` on both entrypoints. The validator `CONTROLLER` describes Traefik and fails closed on each changed Traefik value (15 tests); the tempfile tests (19) and the contract script pass; chart kinds stay inside the AppProject allow-lists | no | none |
| EVD-020 | [VAL-TC-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Live cutover | PR #173 merged as main `bab91b87` at 2026-10-27T05:44:01Z; read-only `kubectl` and curl through `192.168.0.14` every 5 s, then per route; `CHECK_K8S_ROUTER=true bash infrastructure/verify/verify-ingress-tls.sh`; operator-applied temporary whoami through the router | PASS | The router answered until 05:44:42 and again from 05:44:54 (about 12 to 17 s outage). Traefik took `172.18.0.240` and NodePorts 30080 and 30443 on its first sync, no retry needed; `platform-ingress-nginx` was gone by 05:45:58 and Namespace `ingress-nginx` finished terminating within the controller grace period. The new Traefik pod restarted once during startup (exit 137) and has run since. Through the router: argo, adminer and headlamp 200, kiali 302 to `/kiali`, rollouts 302 to `/rollouts/`, the five apex paths 301 to their hosts, HTTP 308 to HTTPS, HSTS present; the apex certificate was re-issued by the mkcert CA in `traefik`. All ten Ingresses report `172.18.0.240` from Traefik; no ingress-nginx ClusterRole, ClusterRoleBinding or webhook remains, only the neutral IngressClass. `verify-ingress-tls.sh` passed. The whoami backend saw `X-Forwarded-For` and `X-Real-Ip` `127.0.0.6`, `X-Forwarded-Port` 80 and the canonical host, as under ingress-nginx: the mesh sidecar address, so neither router preserves the client address | no | none |
| EVD-021 | [VAL-TC-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Rollout canary through Traefik | PR #174 (pod-template annotation `rollouts.hy-home/canary-check`) merged as main `c090747b` at 05:57:39Z; Rollout step, VirtualService weights and adminer through `192.168.0.14` sampled every 3 s | PASS | Canary `8497748d9c` started at 05:59:12, VirtualService 80/20 at 05:59:42, analysis `adminer-8497748d9c-5-1` Successful with measurements 0, 0, 0, 0, then 40/60 at 06:01:43 and Healthy with the new stable at 06:02:13, back to 100/0. All 82 router samples returned 200. The `adminer` and `platform-traefik` Applications are Synced and Healthy afterwards | no | none |
| EVD-022 | [VAL-TC-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Live router checks after cutover | EVD-020 and EVD-021 | PASS | The router address serves every route through Traefik, one Rollout canary step shifted adminer traffic through it, the validators and the live check describe Traefik, and ingress-nginx is gone. Narrows EVD-019: its tests mutate 13 of the Traefik value checks, not each one | yes | EVD-004 |
| EVD-023 | [VAL-TC-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Revert evidence | Detached worktree at `bab91b87` with `git revert -m 1 --no-commit bab91b87`: `python3 -m unittest tests.test_platform_ingress tests.test_infrastructure_tempfiles`, `bash scripts/validate-infrastructure-contracts.sh`, `bash scripts/render-platform-chart-kinds.sh`, `kubectl kustomize` of the changed directories | PASS | The revert restores `platform-ingress-nginx` (chart 4.15.1, LoadBalancer on NodePorts 30080 and 30443), the `ingress-nginx` namespace and the apex routes there, and returns the Traefik Service to `ClusterIP`; all checks pass on the reverted tree. Limitation: the revert was rendered, not exercised live. Its restored Application retries three times (about 70 s); if the NodePorts or the address are still held when they run out, the operator syncs `platform-ingress-nginx` manually | yes | EVD-005 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-TC-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-006, EVD-007, EVD-008, EVD-009, EVD-010 | Accepted by the operator on 2026-10-27 | platform |
| [VAL-TC-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-011, EVD-014, EVD-015, EVD-016, EVD-017, EVD-018 | Accepted by the operator on 2026-10-27 | platform |
| [VAL-TC-003](../spec.md#success-criteria--verification-plan) | pending | EVD-019, EVD-020, EVD-021, EVD-022 | Evidence complete; operator acceptance remains | platform |
| [VAL-TC-004](../spec.md#success-criteria--verification-plan) | pending | EVD-023 | Render evidence complete, live revert not exercised; operator acceptance remains | platform |

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
  - On 2026-10-27 the operator accepted VAL-TC-001 and approved the
    body-size and HSTS comparison. For the EVD-012 differences the operator
    chose to amend the Spec (0.4.0): request buffering on, and the file
    provider for one HSTS middleware. The operator also chose a temporary
    `traefik/whoami` workload, applied and deleted by the operator, for the
    `X-Forwarded-*` check, and to verify the Rollout canary step at the
    cutover (EVD-004).
  - On 2026-10-27 the operator accepted VAL-TC-002 and approved the WORK-003
    cutover pull request. Its merge removes ingress-nginx and starts the
    expected short outage until Traefik holds the NodePorts and the address.
    EVD-004 then covers `verify-ingress-tls.sh` with `CHECK_K8S_ROUTER=true`,
    per-route curl through the router address, the HTTP-to-HTTPS redirect,
    client-address preservation and one Rollout canary step.
  - Deviation: the cutover keeps the platform AppProject's ingress-nginx source
    and destination. The `platform-ingress-nginx` finalizer deletes only
    resources the project still permits, so removing them in the same sync
    could orphan the old Service holding the NodePorts and the address. A
    follow-up pull request removes them once the cascade is observed.
- **Static Validation**: Focused tests, the chart render and `qa.py staged` on
  the exact index.
- **Live Validation**: Operator-run checks for WORK-001 to WORK-004.
- **Secret / Vault Handling**: No secret is read or written.
- **Rollback Plan**: Revert the pull request of the affected work unit through
  Git; Argo CD restores the previous controller state.
- **Evidence Location**: This Task.

## Verification Summary

WORK-001 passed and the operator accepted VAL-TC-001. WORK-002 passed:
every route matches ingress-nginx (EVD-011); the body-size and HSTS
differences (EVD-012) are fixed by PR #170 and rechecked live (EVD-016);
the adminer mesh path (EVD-014) and the forwarded headers (EVD-015) match.
The operator accepted VAL-TC-002. WORK-003 passed: the cutover merged with
a 12 to 17 s outage (EVD-020), every route serves through Traefik, and one
canary step shifted adminer traffic through it (EVD-021, EVD-022). WORK-004
passed by render (EVD-023). VAL-TC-003 and VAL-TC-004 await operator
acceptance; the AppProject cleanup follows.
