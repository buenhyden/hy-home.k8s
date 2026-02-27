# Baseline NetworkPolicy Templates

This directory provides baseline NetworkPolicy resources for workload namespaces (`apps`, `home`).

## Notes

- These policies are provided as a baseline and may need to be extended per workload (e.g., allow egress to external APIs).
- NetworkPolicy enforcement depends on the cluster networking implementation. Validate behavior in your environment before relying on it for isolation.

## Apply (Example)

```bash
kubectl apply -f infrastructure/networkpolicies/apps-default-deny.yaml
kubectl apply -f infrastructure/networkpolicies/apps-allow-dns-egress.yaml
kubectl apply -f infrastructure/networkpolicies/apps-allow-ingress-from-ingress-nginx.yaml
```
