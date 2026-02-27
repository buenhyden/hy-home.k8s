# Sealed Secrets (Vendored Manifests)

This directory vendors the Bitnami Sealed Secrets controller manifest to ensure deterministic, repeatable local cluster bootstrapping.

## Version Pin

- Sealed Secrets: `v0.33.1`
- Source manifest: `controller.yaml` (GitHub release asset)
- Vendored file: `infrastructure/sealed-secrets/sealed-secrets.yaml`
- SHA256 (vendored): `9ff0eac43ceff60b1fa9ca369e65e3d0fbee19d4c2ca5b9aa51c4dab0cbbf7a4`

## Install

```bash
kubectl apply -f infrastructure/sealed-secrets/sealed-secrets.yaml
```

## Verify

```bash
kubectl -n kube-system get pods -l name=sealed-secrets-controller
```
