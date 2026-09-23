# ESO가 실제로 참조하는 경로만 허용
path "secret/data/platform/argocd" {
  capabilities = ["read", "list"]
}

path "secret/metadata/platform/argocd" {
  capabilities = ["read", "list"]
}

path "secret/data/platform/postgres-app" {
  capabilities = ["read", "list"]
}

path "secret/metadata/platform/postgres-app" {
  capabilities = ["read", "list"]
}

path "secret/data/platform/notifications" {
  capabilities = ["read", "list"]
}

path "secret/metadata/platform/notifications" {
  capabilities = ["read", "list"]
}

# Prometheus HTTP API Basic Auth for Alloy, Kiali and Rollouts (ADR-0046)
path "secret/data/platform/prometheus-api" {
  capabilities = ["read", "list"]
}

path "secret/metadata/platform/prometheus-api" {
  capabilities = ["read", "list"]
}

# Grafana Viewer service account token for Kiali (ADR-0046)
path "secret/data/platform/grafana-api" {
  capabilities = ["read", "list"]
}

path "secret/metadata/platform/grafana-api" {
  capabilities = ["read", "list"]
}
