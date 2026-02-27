# Workload Namespaces

This directory defines workload namespaces used by `hy-home.k8s`.

## Pod Security Admission (PSA)

Namespaces in this directory are labeled with:

- `pod-security.kubernetes.io/enforce=restricted`
- `pod-security.kubernetes.io/audit=restricted`
- `pod-security.kubernetes.io/warn=restricted`

These labels MUST NOT be applied to system namespaces (`kube-system`, `metallb-system`, `ingress-nginx`, etc.).

## Apply

```bash
kubectl apply -f infrastructure/namespaces/
```
