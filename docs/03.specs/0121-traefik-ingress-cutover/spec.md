---
title: "Traefik Ingress Cutover"
version: "0.1.0"
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
annotations keep working. This Spec owns the cutover. Traefik first runs next
to ingress-nginx, every route is verified through Traefik, and then the router
contract moves to Traefik and ingress-nginx is removed. The [Plan](plan.md)
orders the work and [Task 0001](tasks/tsk-0001-traefik-ingress-cutover.md)
records it.

## Strategic Boundaries & Non-goals

- In scope:
  - a Traefik Argo CD Application (Traefik 3.7.15 or later, `traefik` chart
    v42 or later) in a dedicated `traefik` namespace, with Istio sidecar
    injection and the restricted Pod Security profile;
  - the platform AppProject entries for the Traefik chart repository and
    namespace;
  - live per-route verification through a temporary Traefik Service during
    the overlap;
  - the cutover:
    - moving the `LoadBalancer` Service with NodePorts `30080` and `30443`
      and IngressClass `nginx` to Traefik;
    - moving the apex redirect Ingresses;
    - swapping the validator `CONTROLLER` declaration and adding Traefik
      value checks;
    - updating `verify-ingress-tls.sh`;
    - removing the ingress-nginx Application, namespace and AppProject
      entries;
  - updating the documents that name ingress-nginx as the current controller.
- Non-goals:
  - Gateway API, `HTTPRoute`, the Istio ingress gateway or Traefik CRD
    routing (ADR-0050 non-goals);
  - the Istio upgrade
    ([ADR-0051](../../02.architecture/decisions/0051-istio-supported-release-upgrade.md));
  - changing host names, TLS issuance, the MetalLB pool or the serverlb
    address;
  - adding annotations;
  - rewriting archived or completed Spec evidence that names ingress-nginx.

## Contracts

- The router contract does not change for clients:
  - `192.168.0.14:80/443` reaches NodePorts `30080` and `30443`;
  - every current host serves the same route with cert-manager
    `mkcert-ca-issuer` TLS;
  - the apex hosts return a permanent redirect.
- During the overlap, the ingress-nginx release alone owns IngressClass
  `nginx` and the router NodePorts. Traefik creates no IngressClass. It is
  reached only through a temporary in-cluster Service.
- Traefik enables only the `kubernetesIngressNGINX` provider. The plain
  `kubernetesIngress` and `kubernetesCRD` providers are disabled.
- The adminer mesh path is kept: Traefik runs with an injected sidecar, the
  adminer route returns `503` without mesh identity and `200` through the
  ingress, and a Rollout canary step still shifts traffic.
- The validator and the live check change in the same pull request as the
  cutover. No pull request leaves the validators describing a controller that
  is not the router.
- The cutover can be reverted by one Git revert of its pull request, which
  restores ingress-nginx as the router.

## Core Design

The work is three pull requests, each with its own review, validation and
rollback:
1. Side by side: add the Traefik namespace, AppProject entries and
   Application. Traefik serves no client traffic yet.
2. Verification: operator-run live checks through the temporary Traefik
   Service, recorded in the Task. No repository change except evidence.
3. Cutover: one pull request moves the Service, NodePorts, IngressClass and
   apex redirects to Traefik. It also swaps the validators and removes
   ingress-nginx and its documents.

## Data Modeling & Storage Strategy

GitOps manifests and validator declarations only. Traefik keeps no
persistent state.

## Interfaces & Data Structures

- New Argo CD Application `platform-traefik` (chart `traefik` from
  `https://traefik.github.io/charts`) in namespace `traefik`.
- `CONTROLLER` in `scripts/validation/platform/ingress.py` becomes the Traefik
  identity: kind, namespace `traefik`, Application, Service name and the
  unchanged NodePorts and annotation set.
- The IngressClass name `nginx` and controller value `k8s.io/ingress-nginx`
  stay, so no `Ingress` object changes.

## Edge Cases & Error Handling

- If Traefik claims an `Ingress` during the overlap, both controllers serve
  it. The temporary Service keeps Traefik off the router ports, so clients
  still reach only ingress-nginx.
- If a route behaves differently through Traefik, cutover stops. The
  behaviors to check are WebSocket and streaming for Headlamp and Kiali,
  `X-Forwarded-*` headers, body size and timeouts, and Kiali's `app-root`
  trailing slash. The Task records the difference, and ADR-0050 is revisited
  if no configuration resolves it.
- An admission webhook for ingress-nginx must not outlive its controller.
  The cutover removes it with the release.

## Failure Modes & Fallback / Human Escalation

- A failed live check before cutover: keep ingress-nginx 4.15.1 as the
  router, and fix or remove the Traefik Application.
- A failed check after cutover: revert the cutover pull request. Argo CD
  restores ingress-nginx and its NodePorts.
- A live mutation outside Argo CD sync needs operator approval.

## Verification Commands

- `python3 scripts/qa.py staged` on each pull request.
- `bash scripts/render-platform-chart-kinds.sh` for the Traefik chart.
- `python3 scripts/run-contract-tests.py --root . --suite cluster-gate`.
- Live, operator-run:
  - `infrastructure/verify/verify-ingress-tls.sh` with
    `CHECK_K8S_ROUTER=true`;
  - curl checks per host, through the temporary Service before cutover and
    the router address after;
  - the adminer `503`/`200` mesh check and one Rollout canary step.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-TC-001 | Traefik runs side by side: the Application is Synced and Healthy, only the Ingress-NGINX provider is enabled, it creates no IngressClass and takes no router port, and staged QA passes. |
| VAL-TC-002 | Every current route, the apex redirects, the adminer mesh path, a Rollout canary step and the listed nginx-default behaviors pass through the temporary Traefik Service. |
| VAL-TC-003 | After the cutover pull request, the router address serves every route through Traefik. The validators and the live check describe Traefik, and ingress-nginx and its admission webhook are gone. |
| VAL-TC-004 | The revert path is proven: the cutover revert restores ingress-nginx, or it is exercised on a branch render with the evidence recorded. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0004-FR-0010](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-TC-001 | Staged QA, chart render and live Argo CD status |
| [REQ-0004-FR-0011](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-TC-002 | Operator-run live route checks |
| [REQ-0004-FR-0010](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-TC-003 | Validator tests, staged QA and live router checks |
| [REQ-0004-FR-0011](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-TC-004 | Revert evidence |

The decision is
[ADR-0050](../../02.architecture/decisions/0050-ingress-nginx-replacement-with-traefik.md),
and the router contract it keeps is
[ADR-0043](../../02.architecture/decisions/0043-dedicated-k8s-ingress-router.md).
