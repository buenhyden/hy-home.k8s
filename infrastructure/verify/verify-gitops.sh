#!/usr/bin/env bash
set -euo pipefail

fail() {
  echo "[FAIL] $*" >&2
  exit 1
}

TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/verify-gitops.XXXXXXXX")" ||
  fail "cannot create private temporary directory"
ROOT_PLATFORM_OUTPUT="$TEMP_DIR/root-platform-path.txt"

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

kubectl -n argocd get application root-platform -o jsonpath='{.spec.source.path}' >"$ROOT_PLATFORM_OUTPUT"

[ "$(<"$ROOT_PLATFORM_OUTPUT")" = 'gitops/apps/root' ] ||
  fail "root-platform path contract mismatch"
[ "$(kubectl -n argocd get application root-platform -o jsonpath='{.spec.source.targetRevision}' 2>/dev/null)" = 'main' ] ||
  fail "root-platform targetRevision contract mismatch"

check_app() {
  local app="$1"
  local health
  local sync
  health="$(kubectl -n argocd get app "$app" -o jsonpath='{.status.health.status}' 2>/dev/null || true)"
  [ -n "$health" ] || fail "${app} app not found in argocd namespace"
  [ "$health" = "Healthy" ] || fail "${app} app health is ${health}, expected Healthy"
  sync="$(kubectl -n argocd get app "$app" -o jsonpath='{.status.sync.status}' 2>/dev/null || true)"
  [ "$sync" = "Synced" ] || fail "${app} app sync is ${sync:-missing}, expected Synced"
  echo "  - ${app}: health=${health}, sync=${sync}"
}

echo "[INFO] Checking root and platform application reconciliation"
check_app "root-platform"
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
