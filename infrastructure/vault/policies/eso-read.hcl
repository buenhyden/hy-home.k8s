# Namespace/Path 단위 least privilege 예시
path "secret/data/platform/*" {
  capabilities = ["read", "list"]
}

path "secret/metadata/platform/*" {
  capabilities = ["read", "list"]
}
