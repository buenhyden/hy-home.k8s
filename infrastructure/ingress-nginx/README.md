# ingress-nginx (Vendored Manifests)

This directory vendors the ingress-nginx controller install manifest to ensure deterministic, repeatable local cluster bootstrapping.

## Version Pin

- ingress-nginx: `controller-v1.14.1`
- Source manifest: `deploy/static/provider/cloud/deploy.yaml`

## Install

```bash
kubectl apply -f infrastructure/ingress-nginx/ingress-nginx.yaml
kubectl apply -f infrastructure/ingress-nginx/nodeport-service.yaml
```

## Host Access (localhost)

The additional NodePort service pins deterministic ports for k3d host mapping:

- HTTP: `30080` (published as `127.0.0.1:18080` via `infrastructure/k3d/k3d-cluster.yaml`)
- HTTPS: `30443` (published as `127.0.0.1:18443` via `infrastructure/k3d/k3d-cluster.yaml`)

## Lifecycle Note

As of 2026-02-27, ingress-nginx has a publicly stated retirement timeline (planned around 2026-03). For v1, we accept ingress-nginx; plan a follow-up ADR to migrate to an alternative controller (e.g., Traefik or Gateway API) if long-term patch availability becomes a concern.

