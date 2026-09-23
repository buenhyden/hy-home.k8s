#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

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

require_multiline_pattern() {
  local pattern="$1"
  local path="$2"
  grep -Pzoq -- "$pattern" "$path" || fail "multiline pattern not found in ${path}: ${pattern}"
}

echo "[INFO] static contract verification started"

ROOT_APP="$ROOT_DIR/gitops/clusters/local/root-application.yaml"
POSTGRES_EXTERNAL="$ROOT_DIR/gitops/platform/external-services/postgres-external.yaml"
COREDNS_CUSTOM="$ROOT_DIR/infrastructure/coredns-custom.yaml"
K3D_CONFIG="$ROOT_DIR/infrastructure/k3d/k3d-cluster.yaml"
VAULT_STORE="$ROOT_DIR/gitops/platform/eso/vault-secret-store.yaml"
VAULT_TOKEN_REVIEWER="$ROOT_DIR/gitops/platform/eso/vault-token-reviewer-binding.yaml"
VALKEY_EXTERNAL="$ROOT_DIR/gitops/platform/external-services/valkey-external.yaml"
ARGOCD_VALUES="$ROOT_DIR/infrastructure/argocd/values-local.yaml"
INGRESS_APP="$ROOT_DIR/gitops/apps/root/platform-ingress-nginx-app.yaml"
VAULT_POLICY="$ROOT_DIR/infrastructure/vault/policies/eso-read.hcl"
APPPROJECT_APPS="$ROOT_DIR/gitops/clusters/local/appproject-apps.yaml"
APPPROJECT_PLATFORM="$ROOT_DIR/gitops/clusters/local/appproject-platform.yaml"
ROOT_KUSTOMIZATION="$ROOT_DIR/gitops/apps/root/kustomization.yaml"
NAMESPACES_KUSTOMIZATION="$ROOT_DIR/gitops/platform/namespaces/kustomization.yaml"
ROLLOUTS_APP="$ROOT_DIR/gitops/apps/root/platform-rollouts-app.yaml"
ROLLOUTS_NAMESPACE="$ROOT_DIR/gitops/platform/namespaces/namespace-argo-rollouts.yaml"
ARGOCD_NOTIFICATIONS_CM="$ROOT_DIR/gitops/platform/argocd/argocd-notifications-cm.yaml"
ARGOCD_NOTIFICATIONS_SECRET="$ROOT_DIR/gitops/platform/argocd/argocd-notifications-secret.yaml"
ARGOCD_KUSTOMIZATION="$ROOT_DIR/gitops/platform/argocd/kustomization.yaml"
CLUSTER_LOCAL_KUSTOMIZATION="$ROOT_DIR/gitops/clusters/local/kustomization.yaml"
PLATFORM_CLUSTER_CONFIG_APP="$ROOT_DIR/gitops/apps/root/platform-cluster-config-app.yaml"
ESO_EGRESS_NP="$ROOT_DIR/gitops/platform/network-policies/external-secrets-egress-to-vault.yaml"
SAMPLE_EXTERNAL_SECRET="$ROOT_DIR/examples/sample-app/external-secret.yaml"

for file in \
  "$ROOT_APP" \
  "$ROOT_KUSTOMIZATION" \
  "$POSTGRES_EXTERNAL" \
  "$VAULT_STORE" \
  "$VAULT_TOKEN_REVIEWER" \
  "$VALKEY_EXTERNAL" \
  "$ARGOCD_VALUES" \
  "$INGRESS_APP" \
  "$VAULT_POLICY" \
  "$APPPROJECT_APPS" \
  "$APPPROJECT_PLATFORM" \
  "$NAMESPACES_KUSTOMIZATION" \
  "$ROLLOUTS_APP" \
  "$ROLLOUTS_NAMESPACE" \
  "$ARGOCD_NOTIFICATIONS_CM" \
  "$ARGOCD_NOTIFICATIONS_SECRET" \
  "$ARGOCD_KUSTOMIZATION" \
  "$CLUSTER_LOCAL_KUSTOMIZATION" \
  "$PLATFORM_CLUSTER_CONFIG_APP" \
  "$ESO_EGRESS_NP" \
  "$SAMPLE_EXTERNAL_SECRET"; do
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
require_pattern '192\.168\.0\.13' "$POSTGRES_EXTERNAL"

# External services are reached through host-published addresses (ADR-0046),
# never through k3d-hyhome container addresses.
if grep -rPn '172\.18\.0\.([0-9]|1[0-9])(/32)?$' \
  "$ROOT_DIR/gitops/platform/external-services" \
  "$ROOT_DIR/gitops/platform/network-policies"; then
  fail 'external service endpoints and egress must use the host address, not k3d-hyhome container addresses (ADR-0046)'
fi
[ ! -e "$ROOT_DIR/gitops/platform/external-services/vault-external.yaml" ] ||
  fail 'vault-external is retired; ESO reaches OpenBao through https://openbao.hy.home.arpa (ADR-0046)'
require_pattern 'server:\s*"https://openbao\.hy\.home\.arpa"' "$VAULT_STORE"
require_pattern 'name:\s*openbao-ca' "$VAULT_STORE"
require_file "$COREDNS_CUSTOM"
require_pattern '192\.168\.0\.13 openbao\.hy\.home\.arpa' "$COREDNS_CUSTOM"
require_pattern 'hostIP:\s*192\.168\.0\.13' "$K3D_CONFIG"
# istio-cni must install into the only CNI bin dir the k3s containerd reads.
require_pattern 'cniBinDir:\s*[/]var[/]lib/rancher/k3s/data/cni$' "$ROOT_DIR/gitops/apps/root/platform-istio-cni-app.yaml"

echo "[INFO] Vault/ESO local-only, identity, RBAC, and policy contracts are owned by scripts/validate-vault-eso-contracts.py"

require_pattern 'name:\s*valkey-external' "$VALKEY_EXTERNAL"
require_pattern 'name:\s*valkey-external-1' "$VALKEY_EXTERNAL"
require_pattern 'port:\s*6379' "$VALKEY_EXTERNAL"
require_pattern 'port:\s*26379' "$VALKEY_EXTERNAL"
require_pattern '192\.168\.0\.13' "$VALKEY_EXTERNAL"

echo "[INFO] verify ArgoCD host/TLS/ingress contracts"
require_pattern 'domain:\s*argo\.hy-k8s\.home\.arpa' "$ARGOCD_VALUES"
require_pattern 'hosts:\s*$' "$ARGOCD_VALUES"
require_pattern 'argo\.hy-k8s\.home\.arpa' "$ARGOCD_VALUES"
require_pattern 'secretName:\s*argocd-local-tls' "$ARGOCD_VALUES"
require_pattern 'type:\s*LoadBalancer' "$INGRESS_APP"

echo "[INFO] verify AppProject wildcard ban and allow-list"
if grep -Pq 'group:\s*"\*"|kind:\s*"\*"' "$APPPROJECT_APPS"; then
  fail 'appproject apps must not contain wildcard namespaceResourceWhitelist'
fi
if grep -Pq 'kind:\s*Namespace' "$APPPROJECT_APPS"; then
  fail 'appproject apps must not allow cluster-scoped Namespace resources'
fi

require_pattern 'kind:\s*Service' "$APPPROJECT_APPS"
require_pattern 'kind:\s*Ingress' "$APPPROJECT_APPS"
require_multiline_pattern 'group:\s*external-secrets\.io\n[[:space:]]+kind:\s*ExternalSecret' "$APPPROJECT_APPS"
for forbidden_apps_kind in \
  Deployment StatefulSet DaemonSet ConfigMap Secret HorizontalPodAutoscaler \
  PodDisruptionBudget ServiceAccount Role RoleBinding NetworkPolicy AnalysisRun; do
  if grep -Pq "kind:\\s*${forbidden_apps_kind}$" "$APPPROJECT_APPS"; then
    fail "appproject apps must not allow unused kind ${forbidden_apps_kind}"
  fi
done

echo "[INFO] verify platform AppProject app-of-apps permission"
require_pattern 'group:\s*argoproj\.io' "$APPPROJECT_PLATFORM"
require_pattern 'kind:\s*Application' "$APPPROJECT_PLATFORM"
require_pattern 'kind:\s*ApplicationSet' "$APPPROJECT_PLATFORM"
require_pattern 'kind:\s*AppProject' "$APPPROJECT_PLATFORM"

echo "[INFO] verify apps AppProject Rollout permission"
APPPROJECT_APPS="$ROOT_DIR/gitops/clusters/local/appproject-apps.yaml"
require_pattern 'kind:\s*Rollout' "$APPPROJECT_APPS"

echo "[INFO] verify platform AppProject apps namespace destination"
require_pattern 'namespace:\s*apps' "$APPPROJECT_PLATFORM"

echo "[INFO] verify cluster-local GitOps ownership contract"
CREATE_NAMESPACE_FINDINGS="$(find "$ROOT_DIR/gitops" -type f -name '*.yaml' -exec grep -H 'CreateNamespace=true' {} + || true)"
if [[ -n "$CREATE_NAMESPACE_FINDINGS" ]]; then
  fail 'GitOps YAML must not use CreateNamespace=true after namespace ownership hardening'
fi
require_pattern 'platform-cluster-config-app\.yaml' "$ROOT_KUSTOMIZATION"
require_pattern 'name:\s*platform-cluster-config' "$PLATFORM_CLUSTER_CONFIG_APP"
require_pattern 'path:\s*gitops/clusters/local' "$PLATFORM_CLUSTER_CONFIG_APP"
require_pattern 'root-application\.yaml' "$CLUSTER_LOCAL_KUSTOMIZATION"
require_pattern 'appproject-platform\.yaml' "$CLUSTER_LOCAL_KUSTOMIZATION"
require_pattern 'appproject-apps\.yaml' "$CLUSTER_LOCAL_KUSTOMIZATION"
require_pattern 'applicationset-apps\.yaml' "$CLUSTER_LOCAL_KUSTOMIZATION"

echo "[INFO] verify platform AppProject new component contracts"
require_pattern 'https://charts\.jetstack\.io' "$APPPROJECT_PLATFORM"
require_pattern 'https://kubernetes-sigs\.github\.io/headlamp/' "$APPPROJECT_PLATFORM"
require_pattern 'https://istio-release\.storage\.googleapis\.com/charts' "$APPPROJECT_PLATFORM"
require_pattern 'https://kiali\.org/helm-charts' "$APPPROJECT_PLATFORM"
require_pattern 'https://argoproj\.github\.io/argo-helm' "$APPPROJECT_PLATFORM"
require_pattern 'namespace:\s*cert-manager' "$APPPROJECT_PLATFORM"
require_pattern 'namespace:\s*istio-system' "$APPPROJECT_PLATFORM"
require_pattern 'namespace:\s*argo-rollouts' "$APPPROJECT_PLATFORM"
require_pattern 'kind:\s*ClusterIssuer' "$APPPROJECT_PLATFORM"

echo "[INFO] verify Argo Rollouts platform contracts"
require_pattern 'platform-rollouts-app\.yaml' "$ROOT_KUSTOMIZATION"
require_pattern 'namespace-argo-rollouts\.yaml' "$NAMESPACES_KUSTOMIZATION"
require_pattern 'name:\s*argo-rollouts' "$ROLLOUTS_NAMESPACE"
require_pattern 'name:\s*platform-rollouts' "$ROLLOUTS_APP"
require_pattern 'repoURL:\s*https://argoproj\.github\.io/argo-helm' "$ROLLOUTS_APP"
require_pattern 'chart:\s*argo-rollouts' "$ROLLOUTS_APP"
require_pattern 'targetRevision:\s*2\.40\.9' "$ROLLOUTS_APP"
require_pattern 'namespace:\s*argo-rollouts' "$ROLLOUTS_APP"
require_pattern 'rollouts\.hy-k8s\.home\.arpa' "$ROLLOUTS_APP"
require_pattern 'secretName:\s*rollouts-dashboard-tls' "$ROLLOUTS_APP"
require_multiline_pattern 'notifications:\n([[:space:]].*\n)*[[:space:]]+enabled:\s*false' "$ROLLOUTS_APP"

echo "[INFO] verify ArgoCD Notifications Slack contracts"
require_multiline_pattern 'notifications:\n([[:space:]].*\n)*[[:space:]]+enabled:\s*true' "$ARGOCD_VALUES"
require_pattern 'argocd-notifications-cm\.yaml' "$ARGOCD_KUSTOMIZATION"
require_pattern 'argocd-notifications-secret\.yaml' "$ARGOCD_KUSTOMIZATION"
require_pattern 'name:\s*argocd-notifications-cm' "$ARGOCD_NOTIFICATIONS_CM"
require_pattern 'service\.slack:' "$ARGOCD_NOTIFICATIONS_CM"
require_pattern "token:\\s*\\\$slack-token" "$ARGOCD_NOTIFICATIONS_CM"
require_pattern 'template\.app-health-degraded:' "$ARGOCD_NOTIFICATIONS_CM"
require_pattern 'template\.app-sync-failed:' "$ARGOCD_NOTIFICATIONS_CM"
require_pattern 'template\.rollout-completed:' "$ARGOCD_NOTIFICATIONS_CM"
require_pattern 'trigger\.on-health-degraded:' "$ARGOCD_NOTIFICATIONS_CM"
require_pattern 'trigger\.on-sync-failed:' "$ARGOCD_NOTIFICATIONS_CM"
require_pattern 'defaultTriggers:' "$ARGOCD_NOTIFICATIONS_CM"
require_pattern 'kind:\s*ExternalSecret' "$ARGOCD_NOTIFICATIONS_SECRET"
require_pattern 'kind:\s*ClusterSecretStore' "$ARGOCD_NOTIFICATIONS_SECRET"
require_pattern 'name:\s*vault-backend' "$ARGOCD_NOTIFICATIONS_SECRET"
require_pattern 'name:\s*argocd-notifications-secret' "$ARGOCD_NOTIFICATIONS_SECRET"
require_pattern 'secretKey:\s*slack-token' "$ARGOCD_NOTIFICATIONS_SECRET"
require_pattern 'key:\s*platform/notifications' "$ARGOCD_NOTIFICATIONS_SECRET"
require_pattern 'property:\s*slack_token' "$ARGOCD_NOTIFICATIONS_SECRET"

echo "[INFO] verify observability external service contracts"
LOKI_EXTERNAL="$ROOT_DIR/gitops/platform/external-services/loki-external.yaml"
TEMPO_EXTERNAL="$ROOT_DIR/gitops/platform/external-services/tempo-external.yaml"
ALLOY_EXTERNAL="$ROOT_DIR/gitops/platform/external-services/alloy-external.yaml"

for file in \
  "$LOKI_EXTERNAL" \
  "$TEMPO_EXTERNAL" \
  "$ALLOY_EXTERNAL"; do
  require_file "$file"
done

require_pattern 'name:\s*loki-external' "$LOKI_EXTERNAL"
require_pattern 'port:\s*3100' "$LOKI_EXTERNAL"
require_pattern '192\.168\.0\.13' "$LOKI_EXTERNAL"

require_pattern 'name:\s*tempo-external' "$TEMPO_EXTERNAL"
require_pattern 'port:\s*3200' "$TEMPO_EXTERNAL"
require_pattern '192\.168\.0\.13' "$TEMPO_EXTERNAL"

require_pattern 'name:\s*alloy-external' "$ALLOY_EXTERNAL"
require_pattern 'port:\s*4317' "$ALLOY_EXTERNAL"
require_pattern '192\.168\.0\.13' "$ALLOY_EXTERNAL"

# Prometheus API and Grafana are reached by name through the external Traefik
# (ADR-0046): no in-cluster Service for them, and every client uses HTTPS.
for retired in prometheus-external grafana-external; do
  [ ! -e "$ROOT_DIR/gitops/platform/external-services/${retired}.yaml" ] ||
    fail "${retired} is retired; clients call the external Traefik by name (ADR-0046)"
done
if grep -rn 'prometheus-external\|grafana-external' "$ROOT_DIR/gitops" "$ROOT_DIR/examples"; then
  fail 'Prometheus and Grafana clients must use https://prometheus.hy.home.arpa and https://grafana.hy.home.arpa (ADR-0046)'
fi
for host in prometheus grafana; do
  require_pattern "192\\.168\\.0\\.13 ${host}\\.hy\\.home\\.arpa" "$COREDNS_CUSTOM"
done
KIALI_APP="$ROOT_DIR/gitops/apps/root/platform-kiali-app.yaml"
require_pattern 'url:\s*"https://prometheus\.hy\.home\.arpa"' "$KIALI_APP"
require_pattern 'password:\s*secret:kiali-prometheus-auth:password' "$KIALI_APP"
require_pattern 'in_cluster_url:\s*"https://grafana\.hy\.home\.arpa"' "$KIALI_APP"
require_pattern 'token:\s*secret:kiali-grafana-auth:token' "$KIALI_APP"
require_pattern 'key:\s*platform/grafana-api' "$ROOT_DIR/gitops/platform/kiali/kiali-grafana-auth-externalsecret.yaml"
require_pattern 'name:\s*kiali-prometheus-auth' "$ROOT_DIR/gitops/platform/kiali/kiali-prometheus-auth-externalsecret.yaml"
require_pattern 'name:\s*prometheus-api-auth' "$ROOT_DIR/gitops/platform/monitoring/prometheus-api-auth-externalsecret.yaml"
require_pattern 'authorization:' "$ROOT_DIR/gitops/platform/eso/prometheus-api-auth-secret.yaml"
require_pattern 'value:\s*/etc/ssl/certs:/etc/hy-home-ca' "$ROLLOUTS_APP"
for template in "$ROOT_DIR/gitops/workloads/adminer/analysis-template.yaml" "$ROOT_DIR/examples/sample-app/analysis-template.yaml"; do
  require_pattern 'address:\s*https://prometheus\.hy\.home\.arpa' "$template"
  require_pattern 'name:\s*prometheus-api-auth' "$template"
done

echo "[INFO] verify ClusterIssuer source"
CLUSTER_ISSUER="$ROOT_DIR/gitops/platform/cert-manager/cluster-issuer-mkcert.yaml"
require_file "$CLUSTER_ISSUER"
require_pattern 'name:\s*mkcert-ca-issuer' "$CLUSTER_ISSUER"
require_pattern 'secretName:\s*mkcert-root-ca' "$CLUSTER_ISSUER"

echo "[INFO] verify Kiali egress NetworkPolicy"
KIALI_NP="$ROOT_DIR/gitops/platform/network-policies/kiali-egress-to-observability.yaml"
require_file "$KIALI_NP"
require_pattern '192\.168\.0\.13/32' "$KIALI_NP"
for port in 443 3200; do
  require_pattern "port:\\s*${port}" "$KIALI_NP"
done

echo "[INFO] verify adminer workload contracts"
ADMINER_ROLLOUT="$ROOT_DIR/gitops/workloads/adminer/rollout.yaml"
ADMINER_SERVICE="$ROOT_DIR/gitops/workloads/adminer/service.yaml"
ADMINER_INGRESS="$ROOT_DIR/gitops/workloads/adminer/ingress.yaml"
ADMINER_PA="$ROOT_DIR/gitops/workloads/adminer/peer-authentication.yaml"
ADMINER_AT="$ROOT_DIR/gitops/workloads/adminer/analysis-template.yaml"
ADMINER_VS="$ROOT_DIR/gitops/workloads/adminer/virtual-service.yaml"
ADMINER_DR="$ROOT_DIR/gitops/workloads/adminer/destination-rule.yaml"

for file in "$ADMINER_ROLLOUT" "$ADMINER_SERVICE" "$ADMINER_INGRESS" "$ADMINER_PA" "$ADMINER_AT" "$ADMINER_VS" "$ADMINER_DR"; do
  require_file "$file"
done

require_pattern 'kind:\s*Rollout' "$ADMINER_ROLLOUT"
require_pattern 'image:\s*adminer:' "$ADMINER_ROLLOUT"
require_pattern 'templateName:\s*adminer-stability' "$ADMINER_ROLLOUT"
require_pattern 'stableService:\s*adminer-stable' "$ADMINER_ROLLOUT"
require_pattern 'canaryService:\s*adminer-canary' "$ADMINER_ROLLOUT"
require_pattern 'host:\s*adminer\.hy-k8s\.home\.arpa' "$ADMINER_INGRESS"
require_pattern 'ingressClassName:\s*nginx' "$ADMINER_INGRESS"
require_pattern 'mode:\s*STRICT' "$ADMINER_PA"
require_pattern 'name:\s*adminer-stability' "$ADMINER_AT"
require_pattern 'kind:\s*VirtualService' "$ADMINER_VS"
require_pattern 'host:\s*adminer-stable' "$ADMINER_VS"
require_pattern 'kind:\s*DestinationRule' "$ADMINER_DR"

echo "[INFO] verify apps namespace NetworkPolicy"
APPS_NP="$ROOT_DIR/gitops/platform/network-policies/apps-egress.yaml"
require_file "$APPS_NP"
require_pattern '192\.168\.0\.13/32' "$APPS_NP"
require_pattern 'port:\s*15432' "$APPS_NP"

echo "[INFO] verify monitoring namespace NetworkPolicy"
MONITORING_NP="$ROOT_DIR/gitops/platform/network-policies/monitoring-egress.yaml"
require_file "$MONITORING_NP"
require_pattern '192\.168\.0\.13/32' "$MONITORING_NP"
require_pattern 'port:\s*3100' "$MONITORING_NP"
require_pattern 'port:\s*443' "$MONITORING_NP"

# In-cluster telemetry collection (ADR-0045): the in-cluster Alloy remote-writes
# k8s metrics to the external Prometheus instead of relying on NodePort scrapes.
ALLOY_K8S="$ROOT_DIR/gitops/platform/monitoring/alloy-k8s-logs.yaml"
require_pattern 'prometheus\.remote_write "external_prometheus"' "$ALLOY_K8S"
require_pattern 'url = "https://prometheus\.hy\.home\.arpa/api/v1/write"' "$ALLOY_K8S"
require_pattern 'password_file = "/etc/prometheus-api/password"' "$ALLOY_K8S"
require_pattern 'ca_file = "/etc/hy-home-ca/ca.crt"' "$ALLOY_K8S"
require_pattern 'cluster = "k3d-hyhome"' "$ALLOY_K8S"
for job in kubernetes-pods kubelet cadvisor; do
  require_pattern "job_name\s*=\s*\"${job}\"" "$ALLOY_K8S"
done
# The metrics NodePorts for the retired static scrape stay removed; only
# ingress-nginx keeps fixed NodePorts (router, ADR-0043).
if grep -rlP '^\s*type:\s*NodePort\b' "$ROOT_DIR/gitops/platform"; then
  fail 'metrics NodePort Services are retired; the in-cluster Alloy scrapes pods directly (ADR-0045)'
fi

echo "[INFO] verify external-secrets egress NetworkPolicy"
require_pattern '192\.168\.0\.13/32' "$ESO_EGRESS_NP"
require_pattern 'port:\s*443' "$ESO_EGRESS_NP"
require_multiline_pattern 'kubernetes\.io/metadata\.name:\s*kube-system\n([[:space:]].*\n)*[[:space:]]+k8s-app:\s*kube-dns' "$ESO_EGRESS_NP"
require_pattern 'port:\s*53' "$ESO_EGRESS_NP"
require_pattern '172\.18\.0\.0/24' "$ESO_EGRESS_NP"
require_pattern 'port:\s*6443' "$ESO_EGRESS_NP"

echo "[INFO] verify sample app ExternalSecret contract"
require_pattern 'kind:\s*ExternalSecret' "$SAMPLE_EXTERNAL_SECRET"
require_pattern 'key:\s*apps/<appname>/config' "$SAMPLE_EXTERNAL_SECRET"
if grep -Pq 'key:\s*secret/apps/<appname>/config' "$SAMPLE_EXTERNAL_SECRET"; then
  fail 'sample ExternalSecret remoteRef.key must omit ClusterSecretStore mount prefix'
fi

# k8s router contract (ADR-0043): the k3d serverlb binds only the dedicated
# host address and forwards to fixed ingress-nginx NodePorts; k8s hosts live
# under hy-k8s.home.arpa and the apex path redirects to the subdomain.
K3D_CONFIG="$ROOT_DIR/infrastructure/k3d/k3d-cluster.yaml"
APEX_REDIRECTS="$ROOT_DIR/gitops/platform/ingress-routes/apex-redirects.yaml"
require_pattern "port:\s*'?192\.168\.0\.14:80:30080'?" "$K3D_CONFIG"
require_pattern "port:\s*'?192\.168\.0\.14:443:30443'?" "$K3D_CONFIG"
if grep -Pq "port:\s*'?(80|443):(80|443)'?\s*$" "$K3D_CONFIG"; then
  fail 'k3d serverlb must not bind host 80/443 on every address (ADR-0043)'
fi
require_pattern 'http:\s*30080' "$INGRESS_APP"
require_pattern 'https:\s*30443' "$INGRESS_APP"
require_pattern '^\s*-\s*platform-ingress-routes-app\.yaml' "$ROOT_KUSTOMIZATION"
for app in argo kiali headlamp rollouts adminer; do
  require_pattern "path:\s*/${app}$" "$APEX_REDIRECTS"
  require_pattern "permanent-redirect:\s*https://${app}\.hy-k8s\.home\.arpa/$" "$APEX_REDIRECTS"
done
if grep -rPq '(argo|argocd|kiali|headlamp|rollouts|adminer)\.hy\.home\.arpa' \
  "$ROOT_DIR/gitops" "$ROOT_DIR/infrastructure" "$ROOT_DIR/examples"; then
  fail 'k8s hosts must use hy-k8s.home.arpa, not hy.home.arpa (ADR-0043)'
fi

echo "[PASS] static contract verification passed"
