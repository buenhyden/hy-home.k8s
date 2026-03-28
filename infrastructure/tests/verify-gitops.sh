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

app_health="$(kubectl -n argocd get app platform-eso-config -o jsonpath='{.status.health.status}' 2>/dev/null || true)"
[ -n "$app_health" ] || fail "platform-eso-config app not found"

echo "[PASS] GitOps contract check passed (platform-eso-config health=$app_health)"
