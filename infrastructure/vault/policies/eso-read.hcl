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
