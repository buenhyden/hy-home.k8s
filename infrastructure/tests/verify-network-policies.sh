#!/usr/bin/env bash
set -euo pipefail

fail() {
  echo "[FAIL] $*" >&2
  exit 1
}

echo "[INFO] Checking network policy contracts"

kubectl version --request-timeout=5s >/dev/null 2>&1 || \
  fail "kubectl cannot reach cluster (check kubeconfig/context)"

# platform namespace policy
platform_np="$(kubectl -n platform get networkpolicy allow-egress-external-services -o name 2>/dev/null || true)"
[ -n "$platform_np" ] || fail "missing platform/allow-egress-external-services"

# argocd namespace policy for valkey
argocd_np="$(kubectl -n argocd get networkpolicy allow-argocd-egress-to-external-valkey -o name 2>/dev/null || true)"
[ -n "$argocd_np" ] || fail "missing argocd/allow-argocd-egress-to-external-valkey"

argocd_np_ip="$(kubectl -n argocd get networkpolicy allow-argocd-egress-to-external-valkey -o jsonpath='{.spec.egress[0].to[0].ipBlock.cidr}' 2>/dev/null || true)"
[ "$argocd_np_ip" = "172.19.0.12/32" ] || fail "argocd valkey egress cidr mismatch (actual=$argocd_np_ip)"

argocd_np_port="$(kubectl -n argocd get networkpolicy allow-argocd-egress-to-external-valkey -o jsonpath='{.spec.egress[0].ports[0].port}' 2>/dev/null || true)"
[ "$argocd_np_port" = "26379" ] || fail "argocd valkey egress port mismatch (actual=$argocd_np_port)"

# external-secrets namespace policy for vault
eso_np="$(kubectl -n external-secrets get networkpolicy allow-external-secrets-egress-to-vault -o name 2>/dev/null || true)"
[ -n "$eso_np" ] || fail "missing external-secrets/allow-external-secrets-egress-to-vault"

eso_np_ip="$(kubectl -n external-secrets get networkpolicy allow-external-secrets-egress-to-vault -o jsonpath='{.spec.egress[0].to[0].ipBlock.cidr}' 2>/dev/null || true)"
[ "$eso_np_ip" = "172.19.0.9/32" ] || fail "external-secrets vault egress cidr mismatch (actual=$eso_np_ip)"

eso_np_port="$(kubectl -n external-secrets get networkpolicy allow-external-secrets-egress-to-vault -o jsonpath='{.spec.egress[0].ports[0].port}' 2>/dev/null || true)"
[ "$eso_np_port" = "8200" ] || fail "external-secrets vault egress port mismatch (actual=$eso_np_port)"

echo "[PASS] network policy contract checks passed"
