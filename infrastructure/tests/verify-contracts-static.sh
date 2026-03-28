#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

fail() {
  echo "[FAIL] $*" >&2
  exit 1
}

require_file() {
  local path="$1"
  [ -f "$path" ] || fail "required file not found: $path"
}

require_pattern() {
  local pattern="$1"
  local path="$2"
  rg -q -- "$pattern" "$path" || fail "pattern not found in ${path}: ${pattern}"
}

echo "[INFO] static contract verification started"

ROOT_APP="$ROOT_DIR/gitops/clusters/local/root-application.yaml"
POSTGRES_EXTERNAL="$ROOT_DIR/gitops/platform/external-services/postgres-external.yaml"
VAULT_EXTERNAL="$ROOT_DIR/gitops/platform/external-services/vault-external.yaml"
VALKEY_EXTERNAL="$ROOT_DIR/gitops/platform/external-services/valkey-external.yaml"
ARGOCD_VALUES="$ROOT_DIR/infrastructure/argocd/values-local.yaml"
INGRESS_APP="$ROOT_DIR/gitops/apps/root/platform-ingress-nginx-app.yaml"
VAULT_POLICY="$ROOT_DIR/infrastructure/vault/policies/eso-read.hcl"
APPPROJECT_APPS="$ROOT_DIR/gitops/clusters/local/appproject-apps.yaml"

for file in \
  "$ROOT_APP" \
  "$POSTGRES_EXTERNAL" \
  "$VAULT_EXTERNAL" \
  "$VALKEY_EXTERNAL" \
  "$ARGOCD_VALUES" \
  "$INGRESS_APP" \
  "$VAULT_POLICY" \
  "$APPPROJECT_APPS"; do
  require_file "$file"
done

echo "[INFO] verify root app source contract"
require_pattern 'path:\s*gitops/apps/root' "$ROOT_APP"
require_pattern 'targetRevision:\s*main' "$ROOT_APP"

echo "[INFO] verify external service contracts"
require_pattern 'name:\s*postgres-write-external' "$POSTGRES_EXTERNAL"
require_pattern 'port:\s*15432' "$POSTGRES_EXTERNAL"
require_pattern 'name:\s*postgres-read-external' "$POSTGRES_EXTERNAL"
require_pattern 'port:\s*15433' "$POSTGRES_EXTERNAL"
require_pattern '172\.30\.0\.11' "$POSTGRES_EXTERNAL"

require_pattern 'name:\s*vault-external' "$VAULT_EXTERNAL"
require_pattern 'port:\s*8200' "$VAULT_EXTERNAL"
require_pattern '172\.30\.0\.10' "$VAULT_EXTERNAL"

require_pattern 'name:\s*valkey-external' "$VALKEY_EXTERNAL"
require_pattern 'name:\s*valkey-external-1' "$VALKEY_EXTERNAL"
require_pattern 'port:\s*26379' "$VALKEY_EXTERNAL"
require_pattern '172\.30\.0\.12' "$VALKEY_EXTERNAL"

echo "[INFO] verify ArgoCD host/TLS/ingress contracts"
require_pattern 'domain:\s*argocd\.127\.0\.0\.1\.nip\.io' "$ARGOCD_VALUES"
require_pattern 'hosts:\s*$' "$ARGOCD_VALUES"
require_pattern 'argocd\.127\.0\.0\.1\.nip\.io' "$ARGOCD_VALUES"
require_pattern 'secretName:\s*argocd-local-tls' "$ARGOCD_VALUES"
require_pattern 'type:\s*LoadBalancer' "$INGRESS_APP"

echo "[INFO] verify vault least-privilege contract"
require_pattern 'path "secret/data/platform/argocd"' "$VAULT_POLICY"
require_pattern 'path "secret/data/platform/postgres-app"' "$VAULT_POLICY"
if rg -q 'secret/data/platform/\*' "$VAULT_POLICY"; then
  fail 'vault policy must not allow wildcard secret/data/platform/*'
fi

echo "[INFO] verify AppProject wildcard ban and allow-list"
if rg -q 'group:\s*"\*"|kind:\s*"\*"' "$APPPROJECT_APPS"; then
  fail 'appproject apps must not contain wildcard namespaceResourceWhitelist'
fi

require_pattern 'kind:\s*Deployment' "$APPPROJECT_APPS"
require_pattern 'kind:\s*StatefulSet' "$APPPROJECT_APPS"
require_pattern 'kind:\s*DaemonSet' "$APPPROJECT_APPS"
require_pattern 'kind:\s*Service' "$APPPROJECT_APPS"
require_pattern 'kind:\s*ConfigMap' "$APPPROJECT_APPS"
require_pattern 'kind:\s*Secret' "$APPPROJECT_APPS"
require_pattern 'kind:\s*Ingress' "$APPPROJECT_APPS"
require_pattern 'kind:\s*HorizontalPodAutoscaler' "$APPPROJECT_APPS"
require_pattern 'kind:\s*PodDisruptionBudget' "$APPPROJECT_APPS"
require_pattern 'kind:\s*ServiceAccount' "$APPPROJECT_APPS"
require_pattern 'kind:\s*Role' "$APPPROJECT_APPS"
require_pattern 'kind:\s*RoleBinding' "$APPPROJECT_APPS"
require_pattern 'kind:\s*NetworkPolicy' "$APPPROJECT_APPS"

echo "[PASS] static contract verification passed"
