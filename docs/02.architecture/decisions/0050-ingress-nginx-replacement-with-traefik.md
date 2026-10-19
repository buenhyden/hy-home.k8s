---
title: "Ingress-NGINX Replacement with Traefik"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
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
- Per the Traefik documentation read on 2026-10-16, Traefik v3.7 supports all
  five annotations through its `kubernetesIngressNGINX` provider, and the
  provider has not been experimental since v3.6.2. Traefik publishes a
  side-by-side migration guide. The seven Traefik advisories published from
  2026-10-07 to 2026-10-16 are fixed in 3.7.15. As read, they concern provider
  features that the current routes do not use; the cutover confirms this
  against the route inventory.
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
  - During the overlap, the ingress-nginx release keeps owning `IngressClass`
    `nginx`. Traefik does not create or manage that class, so Argo CD sees one
    owner. Traefik is reached through a temporary Service on other ports for
    per-route checks, because NodePorts `30080` and `30443` stay with
    ingress-nginx until the cutover.
  - At the cutover, the Traefik release takes over the `IngressClass`.
  - The apex redirect Ingresses in
    `gitops/platform/ingress-routes/apex-redirects.yaml` live in the
    `ingress-nginx` namespace and use Service `ingress-nginx-controller` as
    their backend. They move to the Traefik namespace with the Traefik Service
    as their backend.
  - The platform AppProject in `gitops/clusters/local/appproject-platform.yaml`
    gains the Traefik chart repository and namespace before the overlap. It
    loses the ingress-nginx entries after the removal.
- Make the validator change in the same pull request as the cutover. Update
  `CONTROLLER` in `scripts/validation/platform/ingress.py`, including its
  namespace and Service name. Add Traefik chart value checks for the NodePorts,
  the enabled providers and the class. Update the live `verify-ingress-tls.sh`
  names at the same time.
- Keep chart 4.15.1 as the interim controller until the cutover.

## Explicit Non-goals

- Adopting Gateway API, `HTTPRoute` or the Istio ingress gateway (revisit after
  the Istio upgrade). This deferral stands whether or not ADR-0051 is accepted
  in its current form.
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
  advisories need tracking. Some behaviors differ from nginx. No annotation
  configures forward auth, retries, buffering or strict path types. The routes
  still rely on nginx defaults that Traefik may handle differently:
  - WebSocket and streaming for Headlamp and Kiali;
  - `X-Forwarded-*` headers;
  - request body size and timeouts;
  - trailing-slash handling for Kiali's `app-root` with a `Prefix` path.
- Operational: pin Traefik 3.7.15 or later and follow its security advisories.
  Before the cutover, confirm these live:
  - the redirect status codes;
  - the `IngressClass` handling;
  - the adminer `503`/`200` mesh check;
  - the nginx defaults listed above.

  Update everything that names ingress-nginx:
  - `gitops/README.md`;
  - the namespace manifest;
  - the PeerAuthentication comment;
  - the NetworkPolicies;
  - the operations policies.

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

The operator accepted Option B (Traefik provider) on 2026-10-16, after a
comparison with Istio Gateway API.

The research behind this decision was read on 2026-10-16. Sources:
- the ingress-nginx retirement statement and repository archive notice;
- the Traefik Kubernetes Ingress-NGINX provider and annotation-support
  documentation;
- the Traefik security advisories at
  `https://github.com/traefik/traefik/security/advisories`;
- the Istio supported-releases page;
- the Gateway API and cert-manager release pages.

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0043](./0043-dedicated-k8s-ingress-router.md) | Replaces only its non-goal that excludes replacing the ingress controller, and its naming of ingress-nginx as the controller. Preserves the dedicated address, NodePort, host and apex redirect contract | N/A — the cutover Spec is not written yet; it will link this decision |
| [ADR-0051](./0051-istio-supported-release-upgrade.md) | Not replaced. Gateway API adoption is deferred to a decision after that upgrade | N/A — no Spec implements the deferral |
