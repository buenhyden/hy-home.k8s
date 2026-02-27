# MetalLB (Vendored Manifests)

This directory vendors the MetalLB install manifest to ensure deterministic, repeatable local cluster bootstrapping.

## Version Pin

- MetalLB: `v0.15.3`
- Source manifest: `config/manifests/metallb-native.yaml`

## Install

```bash
kubectl apply -f infrastructure/metallb/metallb-native.yaml
```

## Next Step

After installation, apply the local address pool and L2 advertisement:

```bash
kubectl apply -f infrastructure/ipaddresspool.yaml
```
