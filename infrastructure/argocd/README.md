# ArgoCD (Vendored Manifests)

This directory vendors the ArgoCD install manifest to ensure deterministic, repeatable local cluster bootstrapping.

## Version Pin

- ArgoCD: `v3.3.0`
- Source manifest: `manifests/install.yaml`
- Vendored file: `infrastructure/argocd/argocd-install.yaml`
- SHA256 (vendored): `a6120f20bb0b8d458fa1753fefe7dd2c36eadfd8e09bbdf81ca61849ef6a2f6f`

## Install

```bash
kubectl apply -f infrastructure/argocd/argocd-install.yaml
```

## Access (v1 Standard: port-forward)

```bash
kubectl -n argocd port-forward svc/argocd-server 8080:443
```

Then open `https://127.0.0.1:8080`.

## Initial Admin Password (Reference)

ArgoCD typically stores the initial password in the `argocd-initial-admin-secret` secret.

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d; echo
```

> Note: Depending on your ArgoCD version/configuration, the initial secret may be deleted after first login. If it no longer exists, reset the password per ArgoCD docs.

## Uninstall

```bash
kubectl delete -f infrastructure/argocd/argocd-install.yaml
kubectl delete namespace argocd --ignore-not-found
```
