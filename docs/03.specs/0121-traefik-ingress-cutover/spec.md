---
title: "Traefik Ingress Cutover"
version: "0.3.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-10-20"
layer: "specs"
artifact_id: "SPEC-0121"
---

# Traefik Ingress Cutover Technical Specification (Spec)

## Overview

[ADR-0050](../../02.architecture/decisions/0050-ingress-nginx-replacement-with-traefik.md)
replaces the retired ingress-nginx controller with Traefik. Traefik runs only
its Kubernetes Ingress-NGINX provider, so the existing `Ingress` objects and
annotations keep working. This Spec owns the cutover:
- ingress-nginx first gives up IngressClass ownership and its admission
  webhook;
- Traefik runs next to it, and every route is verified through Traefik;
- the router contract then moves to Traefik in a defined order, and
  ingress-nginx is removed.

The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-traefik-ingress-cutover.md) records it.

"Traefik" here means the in-cluster controller. The Traefik of the external
services workspace (`hy-home.docker`), which
[ADR-0043](../../02.architecture/decisions/0043-dedicated-k8s-ingress-router.md)
keeps separate from k8s routes, is a different component. The k3s bundled Traefik stays disabled
(`--disable=traefik` in `infrastructure/k3d/k3d-cluster.yaml`).

## Strategic Boundaries & Non-goals

- In scope:
  - moving IngressClass `nginx` to a neutral manifest, and disabling the
    ingress-nginx admission webhook;
  - a Traefik Argo CD Application (Traefik 3.7.15 or later, `traefik` chart
    v42 or later) in a dedicated `traefik` namespace, with its AppProject
    entries;
  - live per-route verification during the overlap;
  - the cutover, the removal of ingress-nginx, the validator swap and the
    documents listed under "Documents to update at the cutover".
- Non-goals:
  - Gateway API, `HTTPRoute`, the Istio ingress gateway or Traefik CRD
    routing (ADR-0050 non-goals);
  - the Istio rebuild
    ([ADR-0051](../../02.architecture/decisions/0051-istio-supported-release-upgrade.md)),
    which is planned to run after this cutover;
  - changing host names, TLS issuance, the MetalLB pool or the serverlb
    address;
  - adding annotations;
  - rewriting archived or completed Spec evidence that names ingress-nginx.

### Documents to update at the cutover

These name ingress-nginx as the current controller:
- `README.md`, `.env.example`, `gitops/README.md`, `gitops/platform/README.md`;
- `infrastructure/README.md` and `infrastructure/verify/README.md`;
- `examples/README.md`, `examples/sample-app/README.md`,
  `examples/sample-app/ingress.yaml` and
  `examples/aws/kubernetes/external-services-aws.yaml`;
- the comments in:
  - `gitops/workloads/adminer/ingress.yaml`;
  - `gitops/workloads/adminer/peer-authentication.yaml`;
  - `gitops/apps/root/platform-istiod-app.yaml`;
  - `infrastructure/k3d/k3d-cluster.yaml`;
- `tests/test_platform_ingress.py` and `tests/test_infrastructure_tempfiles.py`;
- ADR-0008, ADR-0028 and ADR-0043, which get a pointer to ADR-0050;
- AD-0004 and AD-0007;
- operations policies 0001, 0003, 0004 and 0007;
- runbooks 0002 and 0004;
- `.agents/skills/vulnerability-patterns/references/manifest-patterns.md`.

## Contracts

- The router contract does not change for clients, except for the short
  cutover outage named below:
  - `192.168.0.14:80/443` reaches NodePorts `30080` and `30443`;
  - the router Service keeps MetalLB address `172.18.0.240`;
  - every current route serves with cert-manager `mkcert-ca-issuer` TLS.
- IngressClass `nginx` (controller `k8s.io/ingress-nginx`) has one owner at
  every step: a neutral manifest in `gitops/platform/ingress-routes`, tracked
  by the `platform-ingress-routes` Application. Neither controller's chart
  renders it after the preparation pull request.
- During the overlap:
  - only the ingress-nginx Service holds the router NodePorts and the MetalLB
    address;
  - Traefik is reached only through its chart's ClusterIP Service;
  - Traefik creates no IngressClass (`ingressClass.enabled=false`) and
    publishes no Ingress status, so `status.loadBalancer` stays with
    ingress-nginx.
- Traefik enables only the `kubernetesIngressNGINX` provider. The plain
  `kubernetesIngress` and `kubernetesCRD` providers are disabled.
- The Traefik namespace uses the labels of the current ingress namespace,
  per [ADR-0028](../../02.architecture/decisions/0028-pod-security-admission-per-namespace-adoption.md):
  - `audit` and `warn` at `baseline`;
  - `istio-injection: enabled`.

  Its pods set `seccompProfile: RuntimeDefault` at pod level so the injected
  sidecars are covered.
- The adminer mesh path is kept: Traefik runs with an injected sidecar, the
  adminer route returns `503` without mesh identity and `200` through the
  ingress, and a Rollout canary step still shifts traffic.
- The validator `CONTROLLER` and the live check change in the cutover pull
  request. Before it, they describe ingress-nginx, which is still the router.

## Core Design

The work is four units. The first is two pull requests:
1. **Prepare ingress-nginx, then run Traefik side by side.**
   - The preparation pull request:
     - adds the neutral IngressClass manifest;
     - sets `controller.ingressClassResource.enabled=false` and
       `controller.admissionWebhooks.enabled=false` on ingress-nginx;
     - adds `resources-finalizer.argocd.argoproj.io` to the
       `platform-ingress-nginx` Application, so removing it at the cutover
       deletes its resources, including the cluster-scoped ones.

     The class must exist throughout, tracked by `platform-ingress-routes`.
     ingress-nginx syncs in wave 2 and `platform-ingress-routes` in wave 4,
     so ingress-nginx could prune the old class before the neutral manifest
     is applied. Before this pull request merges, the operator therefore
     annotates the live class `argocd.argoproj.io/sync-options: Prune=false`.
     This is an approved live step. Without it, a short gap with no class is
     expected, and the routes do not serve during that gap. With the webhook
     gone, it cannot reject the duplicate apex Ingresses at the cutover.
   - The side-by-side pull request, after the class check passes, adds the
     namespace, the AppProject entries and the Application. Traefik uses its
     ClusterIP Service only, with no IngressClass and no published status.
2. **Live verification** (operator-run, Task evidence only): through
   `kubectl port-forward` to the Traefik ClusterIP Service, with `Host` and
   SNI set per route.
3. **Cutover** (a pull request). It:
   - removes the ingress-nginx Application, namespace and AppProject entries;
   - moves the apex redirect Ingresses to the `traefik` namespace, with the
     Traefik Service as backend, and changes the `platform-ingress-routes`
     destination namespace to `traefik`;
   - makes the Traefik Service the `LoadBalancer` with NodePorts `30080` and
     `30443` and address `172.18.0.240`;
   - swaps `CONTROLLER` and adds the Traefik value checks;
   - updates `verify-ingress-tls.sh` and the documents.

   The root sync prunes the `platform-ingress-nginx` Application. Its
   finalizer then deletes the Service, the workloads and the cluster-scoped
   objects. Until the Service is gone, the Traefik Service cannot take the
   NodePorts or the address, so its sync fails and succeeds on retry.
   Clients see a short outage between the deletion and the retry. The
   operator may instead sync manually: first the root removal, waiting for
   the cascade, then the Traefik Application.
4. **Revert evidence**: reverting the cutover pull request is expected to
   restore ingress-nginx. The Traefik Service returns to ClusterIP, the root
   sync recreates the `platform-ingress-nginx` Application, and its Service
   takes the NodePorts and the address back on a sync retry once Traefik has
   released them. The
   Task records whether the revert was exercised live or only rendered.

## Data Modeling & Storage Strategy

GitOps manifests and validator declarations only. Traefik keeps no
persistent state.

## Interfaces & Data Structures

- New Argo CD Application `platform-traefik` (chart `traefik` from
  `https://traefik.github.io/charts`) in namespace `traefik`.
- New neutral manifest: IngressClass `nginx` with controller
  `k8s.io/ingress-nginx`, in `gitops/platform/ingress-routes`.
- `CONTROLLER` in `scripts/validation/platform/ingress.py` becomes the Traefik
  identity. Its kind, namespace `traefik`, Application and Service name change.
  The NodePorts and the annotation set stay. The apex `ROUTES` keys move from
  namespace `ingress-nginx` to `traefik`.
- The routes verified live are the current `ROUTES`:
  - `adminer`, `headlamp` and `kiali`, under `hy-k8s.home.arpa`;
  - the five apex redirects on `hy-k8s.home.arpa`: `/argo`, `/kiali`,
    `/headlamp`, `/rollouts` and `/adminer`.

## Edge Cases & Error Handling

- If a route behaves differently through Traefik, the cutover stops. The
  behaviors to check are:
  - WebSocket and streaming for Headlamp and Kiali;
  - `X-Forwarded-*` headers;
  - request body size and timeouts;
  - Kiali's `app-root` trailing slash;
  - the apex redirect status codes.

  The Task records the difference. ADR-0050 is revisited if no configuration
  resolves it.
- If the IngressClass is missing at any point after WORK-001, both
  controllers stop serving. The class is checked live after the preparation
  pull request, before anything else proceeds.

## Failure Modes & Fallback / Human Escalation

- A failed check before the cutover: keep ingress-nginx 4.15.1 as the router,
  and fix or remove the Traefik Application.
- A failed check after the cutover: revert the cutover pull request, in the
  order above.
- A live mutation outside Argo CD sync needs operator approval.

## Verification Commands

- `python3 scripts/qa.py staged` on each pull request.
- `bash scripts/render-platform-chart-kinds.sh` for both charts.
- `python3 scripts/run-contract-tests.py --root . --suite cluster-gate`.
- Live, operator-run:
  - `kubectl get ingressclass nginx` and its tracking label after the
    preparation pull request;
  - curl per route through the port-forward before the cutover, and through
    the router address after it;
  - `infrastructure/verify/verify-ingress-tls.sh` with
    `CHECK_K8S_ROUTER=true` after the cutover;
  - the adminer `503`/`200` mesh check and one Rollout canary step.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-TC-001 | IngressClass `nginx` exists throughout, tracked by `platform-ingress-routes`, and ingress-nginx renders no class and no admission webhook. Traefik then runs side by side: Synced and Healthy, only the Ingress-NGINX provider enabled, a ClusterIP Service only, no IngressClass, and every Ingress `status.loadBalancer` unchanged. |
| VAL-TC-002 | Every route in `ROUTES` passes through the port-forward, together with the apex redirect status codes, the adminer mesh path, a Rollout canary step and the listed nginx-default behaviors. |
| VAL-TC-003 | After the cutover, the router address serves every route through Traefik. The validators and the live check describe Traefik, and ingress-nginx is gone. The observed outage and sync order are recorded. |
| VAL-TC-004 | The revert path is recorded: either a live revert restored ingress-nginx, or a branch render plus the stated order, with that limitation named. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0004-FR-0010](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-TC-001 | Staged QA, chart render, live class check and live Argo CD status |
| [REQ-0004-FR-0011](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-TC-002 | Operator-run live route checks |
| [REQ-0004-FR-0010](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-TC-003 | Validator tests, staged QA and live router checks |
| [REQ-0004-FR-0011](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-TC-004 | Revert evidence |

The decision is
[ADR-0050](../../02.architecture/decisions/0050-ingress-nginx-replacement-with-traefik.md),
and the router contract it keeps is
[ADR-0043](../../02.architecture/decisions/0043-dedicated-k8s-ingress-router.md).
