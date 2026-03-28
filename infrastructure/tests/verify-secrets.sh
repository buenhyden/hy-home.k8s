#!/usr/bin/env bash
set -euo pipefail

fail() {
  echo "[FAIL] $*" >&2
  exit 1
}

echo "[INFO] Checking ESO + Vault integration contracts"

kubectl version --request-timeout=5s >/dev/null 2>&1 || \
  fail "kubectl cannot reach cluster (check kubeconfig/context)"

store_ready="$(kubectl -n external-secrets get clustersecretstore vault-backend -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}' 2>/dev/null || true)"
[ "$store_ready" = "True" ] || fail "vault-backend Ready is not True (actual=$store_ready)"

es_ready="$(kubectl -n argocd get externalsecret argocd-external-valkey -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}' 2>/dev/null || true)"
[ "$es_ready" = "True" ] || fail "argocd-external-valkey Ready is not True (actual=$es_ready)"

echo "[PASS] ESO + Vault checks passed"
