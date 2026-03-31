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
  grep -Pq -- "$pattern" "$path" || fail "pattern not found in ${path}: ${pattern}"
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
APPPROJECT_PLATFORM="$ROOT_DIR/gitops/clusters/local/appproject-platform.yaml"

for file in \
  "$ROOT_APP" \
  "$POSTGRES_EXTERNAL" \
  "$VAULT_EXTERNAL" \
  "$VALKEY_EXTERNAL" \
  "$ARGOCD_VALUES" \
  "$INGRESS_APP" \
  "$VAULT_POLICY" \
  "$APPPROJECT_APPS" \
  "$APPPROJECT_PLATFORM"; do
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
require_pattern '172\.18\.0\.15' "$POSTGRES_EXTERNAL"

require_pattern 'name:\s*vault-external' "$VAULT_EXTERNAL"
require_pattern 'port:\s*8200' "$VAULT_EXTERNAL"
require_pattern '172\.18\.0\.8' "$VAULT_EXTERNAL"

require_pattern 'name:\s*valkey-external' "$VALKEY_EXTERNAL"
require_pattern 'name:\s*valkey-external-1' "$VALKEY_EXTERNAL"
require_pattern 'port:\s*6379' "$VALKEY_EXTERNAL"
require_pattern '172\.18\.0\.9' "$VALKEY_EXTERNAL"

echo "[INFO] verify ArgoCD host/TLS/ingress contracts"
require_pattern 'domain:\s*argocd\.127\.0\.0\.1\.nip\.io' "$ARGOCD_VALUES"
require_pattern 'hosts:\s*$' "$ARGOCD_VALUES"
require_pattern 'argocd\.127\.0\.0\.1\.nip\.io' "$ARGOCD_VALUES"
require_pattern 'secretName:\s*argocd-local-tls' "$ARGOCD_VALUES"
require_pattern 'type:\s*LoadBalancer' "$INGRESS_APP"

echo "[INFO] verify vault least-privilege contract"
require_pattern 'path "secret/data/platform/argocd"' "$VAULT_POLICY"
require_pattern 'path "secret/data/platform/postgres-app"' "$VAULT_POLICY"
if grep -Pq 'secret/data/platform/\*' "$VAULT_POLICY"; then
  fail 'vault policy must not allow wildcard secret/data/platform/*'
fi

echo "[INFO] verify AppProject wildcard ban and allow-list"
if grep -Pq 'group:\s*"\*"|kind:\s*"\*"' "$APPPROJECT_APPS"; then
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

echo "[INFO] verify platform AppProject app-of-apps permission"
require_pattern 'group:\s*argoproj\.io' "$APPPROJECT_PLATFORM"
require_pattern 'kind:\s*Application' "$APPPROJECT_PLATFORM"

echo "[INFO] verify apps AppProject Rollout permission"
APPPROJECT_APPS="$ROOT_DIR/gitops/clusters/local/appproject-apps.yaml"
require_pattern 'kind:\s*Rollout' "$APPPROJECT_APPS"

echo "[INFO] verify platform AppProject apps namespace destination"
require_pattern 'namespace:\s*apps' "$APPPROJECT_PLATFORM"

echo "[INFO] verify platform AppProject new component contracts"
require_pattern 'https://charts\.jetstack\.io' "$APPPROJECT_PLATFORM"
require_pattern 'https://kubernetes-sigs\.github\.io/headlamp/' "$APPPROJECT_PLATFORM"
require_pattern 'https://istio-release\.storage\.googleapis\.com/charts' "$APPPROJECT_PLATFORM"
require_pattern 'https://kiali\.org/helm-charts' "$APPPROJECT_PLATFORM"
require_pattern 'namespace:\s*cert-manager' "$APPPROJECT_PLATFORM"
require_pattern 'namespace:\s*istio-system' "$APPPROJECT_PLATFORM"
require_pattern 'kind:\s*ClusterIssuer' "$APPPROJECT_PLATFORM"

echo "[INFO] verify observability external service contracts"
PROMETHEUS_EXTERNAL="$ROOT_DIR/gitops/platform/external-services/prometheus-external.yaml"
LOKI_EXTERNAL="$ROOT_DIR/gitops/platform/external-services/loki-external.yaml"
TEMPO_EXTERNAL="$ROOT_DIR/gitops/platform/external-services/tempo-external.yaml"
ALLOY_EXTERNAL="$ROOT_DIR/gitops/platform/external-services/alloy-external.yaml"
GRAFANA_EXTERNAL="$ROOT_DIR/gitops/platform/external-services/grafana-external.yaml"

for file in \
  "$PROMETHEUS_EXTERNAL" \
  "$LOKI_EXTERNAL" \
  "$TEMPO_EXTERNAL" \
  "$ALLOY_EXTERNAL" \
  "$GRAFANA_EXTERNAL"; do
  require_file "$file"
done

require_pattern 'name:\s*prometheus-external' "$PROMETHEUS_EXTERNAL"
require_pattern 'port:\s*9090' "$PROMETHEUS_EXTERNAL"
require_pattern '172\.18\.0\.10' "$PROMETHEUS_EXTERNAL"

require_pattern 'name:\s*loki-external' "$LOKI_EXTERNAL"
require_pattern 'port:\s*3100' "$LOKI_EXTERNAL"
require_pattern '172\.18\.0\.13' "$LOKI_EXTERNAL"

require_pattern 'name:\s*tempo-external' "$TEMPO_EXTERNAL"
require_pattern 'port:\s*3200' "$TEMPO_EXTERNAL"
require_pattern '172\.18\.0\.12' "$TEMPO_EXTERNAL"

require_pattern 'name:\s*alloy-external' "$ALLOY_EXTERNAL"
require_pattern 'port:\s*4317' "$ALLOY_EXTERNAL"
require_pattern '172\.18\.0\.11' "$ALLOY_EXTERNAL"

require_pattern 'name:\s*grafana-external' "$GRAFANA_EXTERNAL"
require_pattern 'port:\s*3000' "$GRAFANA_EXTERNAL"
require_pattern '172\.18\.0\.14' "$GRAFANA_EXTERNAL"

echo "[INFO] verify ClusterIssuer source"
CLUSTER_ISSUER="$ROOT_DIR/gitops/platform/cert-manager/cluster-issuer-mkcert.yaml"
require_file "$CLUSTER_ISSUER"
require_pattern 'name:\s*mkcert-ca-issuer' "$CLUSTER_ISSUER"
require_pattern 'secretName:\s*mkcert-root-ca' "$CLUSTER_ISSUER"

echo "[INFO] verify Kiali egress NetworkPolicy"
KIALI_NP="$ROOT_DIR/gitops/platform/network-policies/kiali-egress-to-observability.yaml"
require_file "$KIALI_NP"
require_pattern '172\.18\.0\.10/32' "$KIALI_NP"
require_pattern '172\.18\.0\.14/32' "$KIALI_NP"
require_pattern '172\.18\.0\.12/32' "$KIALI_NP"

echo "[INFO] verify adminer workload contracts"
ADMINER_ROLLOUT="$ROOT_DIR/gitops/workloads/adminer/rollout.yaml"
ADMINER_SERVICE="$ROOT_DIR/gitops/workloads/adminer/service.yaml"
ADMINER_INGRESS="$ROOT_DIR/gitops/workloads/adminer/ingress.yaml"
ADMINER_PA="$ROOT_DIR/gitops/workloads/adminer/peer-authentication.yaml"
ADMINER_AT="$ROOT_DIR/gitops/workloads/adminer/analysis-template.yaml"

for file in "$ADMINER_ROLLOUT" "$ADMINER_SERVICE" "$ADMINER_INGRESS" "$ADMINER_PA" "$ADMINER_AT"; do
  require_file "$file"
done

require_pattern 'kind:\s*Rollout' "$ADMINER_ROLLOUT"
require_pattern 'image:\s*adminer:' "$ADMINER_ROLLOUT"
require_pattern 'templateName:\s*adminer-stability' "$ADMINER_ROLLOUT"
require_pattern 'host:\s*adminer\.127\.0\.0\.1\.nip\.io' "$ADMINER_INGRESS"
require_pattern 'ingressClassName:\s*nginx' "$ADMINER_INGRESS"
require_pattern 'mode:\s*STRICT' "$ADMINER_PA"
require_pattern 'name:\s*adminer-stability' "$ADMINER_AT"

echo "[INFO] verify apps namespace NetworkPolicy"
APPS_NP="$ROOT_DIR/gitops/platform/network-policies/apps-egress.yaml"
require_file "$APPS_NP"
require_pattern '172\.18\.0\.15/32' "$APPS_NP"
require_pattern 'port:\s*15432' "$APPS_NP"

echo "[INFO] verify monitoring namespace NetworkPolicy"
MONITORING_NP="$ROOT_DIR/gitops/platform/network-policies/monitoring-egress.yaml"
require_file "$MONITORING_NP"
require_pattern '172\.18\.0\.13/32' "$MONITORING_NP"
require_pattern 'port:\s*3100' "$MONITORING_NP"

echo "[PASS] static contract verification passed"
