#!/usr/bin/env bash
set -euo pipefail

fail() {
  echo "[FAIL] $*" >&2
  exit 1
}

TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/verify-gitops.XXXXXXXX")" ||
  fail "cannot create private temporary directory"
ROOT_PLATFORM_OUTPUT="$TEMP_DIR/root-platform.yaml"

cleanup() {
  local status=$?
  trap - EXIT INT TERM
  if ! rm -rf -- "$TEMP_DIR"; then
    echo "[FAIL] cannot remove private temporary directory" >&2
    [ "$status" -ne 0 ] || status=1
  fi
  exit "$status"
}

trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

echo "[INFO] Checking ArgoCD GitOps contracts"

kubectl version --request-timeout=5s >/dev/null 2>&1 ||
  fail "kubectl cannot reach cluster (check kubeconfig/context)"

kubectl -n argocd get application root-platform -o yaml >"$ROOT_PLATFORM_OUTPUT"

rg -q 'path: gitops/apps/root' "$ROOT_PLATFORM_OUTPUT" ||
  fail "root-platform path contract mismatch"
rg -q 'targetRevision: main' "$ROOT_PLATFORM_OUTPUT" ||
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
