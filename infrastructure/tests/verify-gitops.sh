#!/usr/bin/env bash
set -euo pipefail

fail() {
  echo "[FAIL] $*" >&2
  exit 1
}

echo "[INFO] Checking ArgoCD GitOps contracts"

kubectl version --request-timeout=5s >/dev/null 2>&1 || \
  fail "kubectl cannot reach cluster (check kubeconfig/context)"

kubectl -n argocd get application root-platform -o yaml >/tmp/root-platform.yaml

rg -q 'path: gitops/apps/root' /tmp/root-platform.yaml || \
  fail "root-platform path contract mismatch"
rg -q 'targetRevision: main' /tmp/root-platform.yaml || \
  fail "root-platform targetRevision contract mismatch"

check_app() {
  local app="$1"
  local health
  health="$(kubectl -n argocd get app "$app" -o jsonpath='{.status.health.status}' 2>/dev/null || true)"
  [ -n "$health" ] || fail "${app} app not found in argocd namespace"
  echo "  - ${app}: health=${health}"
}

echo "[INFO] Checking platform application presence"
check_app "platform-eso-config"
check_app "platform-cert-manager"
check_app "platform-cert-manager-config"
check_app "platform-istio-base"
check_app "platform-istiod"
check_app "platform-headlamp"
check_app "platform-headlamp-config"
check_app "platform-kiali"
check_app "platform-kiali-config"

echo "[PASS] GitOps contract check passed"
