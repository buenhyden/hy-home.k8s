---
title: "Ingress-NGINX Replacement with Traefik"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "platform"
updated: "2026-10-16"
layer: "architecture"
artifact_id: "ADR-0050"
---

# ADR-0050: Ingress-NGINX Replacement with Traefik

## Overview

This decision replaces the retired ingress-nginx controller with Traefik. Traefik
runs its Kubernetes Ingress-NGINX provider, so the existing `Ingress` objects
and their annotations keep working unchanged. The
[ADR-0043](./0043-dedicated-k8s-ingress-router.md) router contract stays: the
dedicated host address, the fixed NodePorts, the host names and the apex
redirects. Gateway API is deferred until the Istio upgrade in
[ADR-0051](./0051-istio-supported-release-upgrade.md).

## Context

- The Kubernetes project retired ingress-nginx. Best-effort maintenance ended
  in March 2026, and the repository was archived on 2026-03-24. The last
  release is controller v1.15.1 (chart 4.15.1, 2026-03-19). No further
  security fixes will ship, while the bundled nginx 1.27.1 keeps receiving
  upstream advisories. The 2026-01-29 Steering and Security Response Committee
  statement says staying on it leaves users vulnerable.
- The live cluster declared chart 4.12.0 (controller v1.12.0). That version is
  affected by CVE-2025-1974 (admission webhook remote code execution) and by
  the later ingress-nginx CVEs through CVE-2026-4342. An interim pull request
  moves it to chart 4.15.1, which fixes those CVEs only until the next
  unpatched issue.
- The current Ingresses use five ingress-nginx annotations:
  - `ssl-redirect` on all routes;
  - `permanent-redirect` on the apex routes;
  - `app-root` on Kiali;
  - `service-upstream` and `upstream-vhost` on adminer.

  The last two make the injected controller reach the STRICT-mTLS workload
  through its mesh host, which keeps the Argo Rollouts canary on the adminer
  `VirtualService` working.
- Traefik v3.7 supports all five annotations through its
  `kubernetesIngressNGINX` provider. The provider has not been experimental
  since v3.6.2. Traefik publishes a side-by-side migration guide. Seven Traefik
  advisories from 2026-10-07 to 2026-10-16 concern provider features that this
  repository does not use, and they are fixed in 3.7.15.
- Istio Gateway API is the long-term direction Kubernetes recommends. It
  requires the Istio upgrade first, because 1.25.2 is end of life and outside
  its supported Kubernetes range. It also requires rewriting every route,
  replacing the canary mechanism and adding a new validator.
- [SPEC-0119](../../03.specs/0119-ingress-controller-identity/spec.md) moved the
  validator's controller identity into one `CONTROLLER` declaration, so
  swapping controllers no longer means rewriting QA.

## Decision

- Replace ingress-nginx with Traefik 3.7.15 or later, through the `traefik` Helm
  chart (v42 or later), in a dedicated namespace with Istio sidecar injection
  and the restricted Pod Security profile that the current namespace uses.
- Enable only the `kubernetesIngressNGINX` provider, and disable the plain
  `kubernetesIngress` and `kubernetesCRD` providers. Keep `IngressClass`
  `nginx` (controller `k8s.io/ingress-nginx`) so that no `Ingress` changes.
- Keep the router contract: a `LoadBalancer` Service with NodePorts `30080` and
  `30443`, the k3d serverlb binding on `192.168.0.14`, the `hy-k8s.home.arpa`
  hosts, cert-manager `mkcert-ca-issuer` TLS and the apex permanent redirects.
- Migrate side by side. Run Traefik next to ingress-nginx and verify each route,
  including the adminer mesh path and a Rollout canary step. Then move the
  NodePorts and remove the ingress-nginx Application and namespace.
- Make the validator change in the same pull request: update `CONTROLLER` in
  `scripts/validation/platform/ingress.py` and add Traefik chart value checks
  (NodePorts, enabled providers, class), together with the live
  `verify-ingress-tls.sh` names.
- Keep chart 4.15.1 as the interim controller until the cutover.

## Explicit Non-goals

- Adopting Gateway API, `HTTPRoute` or the Istio ingress gateway (revisit after
  ADR-0051).
- Upgrading Istio (ADR-0051).
- Changing host names, TLS issuance, the MetalLB pool or the serverlb address.
- Adding annotations or Traefik CRD routing.

## Consequences

- Positive: the unmaintained controller leaves the cluster without rewriting
  any route. The adminer mesh path and canary keep their current mechanism.
  Traefik is maintained and conformant with Gateway API, so a later Gateway API
  move does not need another controller swap.
- Negative: the provider is a bridge on the Ingress API, which Kubernetes no
  longer develops. Traefik's provider is still being hardened and its
  advisories need tracking. Some behaviors differ from nginx: forward auth,
  load balancing, retries, trailing slashes, buffering and strict path types.
  None of these is used by the current routes.
- Operational: pin Traefik 3.7.15 or later and follow its security advisories.
  Confirm live the redirect status codes, the `IngressClass` handling and the
  adminer `503`/`200` mesh check before cutover. Update
  `gitops/README.md`, the NetworkPolicies and the operations policies that
  name ingress-nginx.

## Alternatives

- **Istio Gateway API now:** rejected for this step. It depends on a
  six-minor-version Istio upgrade, rewrites every route as `HTTPRoute`, and
  breaks the canary until the alpha Argo Rollouts Gateway API plugin or a
  rework replaces it. It also needs a Gateway API validator and new schema and
  AppProject coverage. It remains the preferred end state after ADR-0051.
- **Another Gateway API implementation:** Envoy Gateway, kgateway and NGINX
  Gateway Fabric would add a second control plane next to Istio, with the same
  route rewrite. Rejected.
- **Stay on ingress-nginx 4.15.1:** rejected as an end state. There will be no
  further upstream fixes. It is kept only as the interim controller.

## Traceability

The research behind this decision was read on 2026-10-16 from the Kubernetes,
Istio, Traefik, Gateway API and cert-manager release pages and advisories.

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0043](./0043-dedicated-k8s-ingress-router.md) | Replaces only its non-goal that excludes replacing the ingress controller, and its naming of ingress-nginx as the controller. Preserves the dedicated address, NodePort, host and apex redirect contract | N/A — the cutover Spec is not written yet; it will link this decision |
| [ADR-0051](./0051-istio-supported-release-upgrade.md) | Not replaced. Gateway API adoption is deferred to a decision after that upgrade | N/A — no Spec implements the deferral |
