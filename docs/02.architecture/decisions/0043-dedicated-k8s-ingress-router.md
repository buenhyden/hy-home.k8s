---
title: "Dedicated Kubernetes Ingress Router on hy-k8s.home.arpa"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-26"
layer: "architecture"
artifact_id: "ADR-0043"
---

# ADR-0043: Dedicated Kubernetes Ingress Router on hy-k8s.home.arpa

## Overview

This ADR gives the UIs and apps that k8s serves an entry point and domain
separate from the external services workspace's Traefik. k8s host names are
`<name>.hy-k8s.home.arpa`, and the entry point is the k3d serverlb bound to the
dedicated host IP `192.168.0.14`. The ArgoCD UI is `argo.hy-k8s.home.arpa`.
`hy.home.arpa`, which [ADR-0042](./0042-linux-server-single-host-baseline.md)
set as the local UI domain, remains only for the external services workspace's
host names.

## Context

- The Traefik of the external services workspace (`hy-home.docker`) holds the
  host's `0.0.0.0:80` and `0.0.0.0:443`. The k3d configuration also maps
  `80:80` and `443:443` on the serverlb, so the two entry points cannot coexist
  on the same host address.
- k8s routes reached k3d through dynamic config placed in that Traefik's file
  provider. This repository's `traefik/` reference files and the external
  workspace's actual files named different backends, and every k8s route
  change had to touch both repositories.
- ingress-nginx is a LoadBalancer Service on MetalLB `172.18.0.240`. That
  address sits on the Docker bridge `k3d-hyhome`, so only the server itself can
  reach it; LAN clients cannot.
- The host uses the static address `192.168.0.13/24` on `enp4s0`, and at the
  time of the decision `192.168.0.14` gave no ARP reply.

## Decision

- The host names k8s serves are `<name>.hy-k8s.home.arpa`. The current names
  are `argo` (ArgoCD), `kiali`, `headlamp`, `rollouts`, and `adminer`; a new app
  uses `<appname>.hy-k8s.home.arpa`. That subdomain is the reference address the
  app answers on.
- A request to the apex `hy-k8s.home.arpa/<name>` is sent with a 301 to
  `https://<name>.hy-k8s.home.arpa/` through the ingress-nginx
  `permanent-redirect` annotation. Apps' root path settings do not change, and
  no snippet annotation is used. The TLS certificate's SAN carries both the
  apex and the app subdomains.
- The dedicated k8s entry point is the k3d serverlb. The serverlb binds only
  the host's `192.168.0.14:80` and `192.168.0.14:443` and forwards them to the
  fixed ingress-nginx NodePorts `30080` and `30443`. ingress-nginx terminates
  TLS.
- The ingress-nginx Service keeps its LoadBalancer (`172.18.0.240`). That
  address is the server-internal validation path.
- The external services workspace's Traefik carries no k8s routes. This
  repository's `traefik/` reference files and the sample app's Traefik example
  are retired.
- The operator and the external workspace own assigning the host address
  `192.168.0.14`, resolving `*.hy-k8s.home.arpa`, and binding the external
  Traefik only to `192.168.0.13`. Repository static validation does not prove
  this state.

## Explicit Non-goals

- Changing the host names of external services (OpenBao, Grafana, Keycloak, and others)
- Replacing the ingress controller or adopting the Gateway API
- Public certificates, ACME, or running a wildcard DNS server
- Changing the MetalLB address pool

## Consequences

- **Positive**:
  - Adding or changing a k8s route takes only this repository's Ingress
    declarations.
  - The two entry points have different host addresses, so host port conflicts
    disappear.
  - k8s and external services have separate domains, so the name tells which
    router answers.
- **Trade-offs**:
  - The host needs a second address, and LAN clients must resolve
    `hy-k8s.home.arpa` names to `192.168.0.14`.
  - Clients that used the old `*.hy.home.arpa` k8s addresses must move to the
    new names.
- **Operational**:
  - The k3d serverlb's host address is fixed when the cluster is created.
    Changing it means recreating the cluster.

## Alternatives

### Keep the external Traefik forwarding k8s routes

- Good:
  - No host address or DNS change.
- Bad:
  - Every k8s route needs both repositories changed together, and the request
    owner explicitly ruled it out.

### An alternate port (`8443`) on the same host address

- Good:
  - No host network change.
- Bad:
  - Every URL carries a port, which complicates clients that expect standard
    ports and OAuth redirect settings.

### Resolve names directly to the MetalLB address

- Good:
  - No extra router.
- Bad:
  - It is a Docker bridge address, so LAN clients cannot reach it.

## Traceability

- **PRD**: [`../../01.requirements/0004-current-local-gitops-platform.md`](../../01.requirements/0004-current-local-gitops-platform.md)
- **AD**: [`../descriptions/0007-current-local-gitops-platform.md`](../descriptions/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Related ADR**: [`./0042-linux-server-single-host-baseline.md`](./0042-linux-server-single-host-baseline.md)

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0042](./0042-linux-server-single-host-baseline.md) | Narrows ADR-0042's `hy.home.arpa` clause to external service hosts; k8s hosts move to `hy-k8s.home.arpa` | [SPEC-0008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
