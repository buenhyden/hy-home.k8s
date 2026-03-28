#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLUSTER_NAME="hyhome"
K3D_HTTP_PORT="${K3D_HTTP_PORT:-80}"
K3D_HTTPS_PORT="${K3D_HTTPS_PORT:-443}"
VAULT_ADDR="${VAULT_ADDR:-https://vault.127.0.0.1.nip.io}"
VAULT_SKIP_VERIFY="${VAULT_SKIP_VERIFY:-true}"
POSTGRES_WRITE_ADDR="${POSTGRES_WRITE_ADDR:-172.30.0.11}"
POSTGRES_WRITE_PORT="${POSTGRES_WRITE_PORT:-15432}"
POSTGRES_READ_ADDR="${POSTGRES_READ_ADDR:-172.30.0.11}"
POSTGRES_READ_PORT="${POSTGRES_READ_PORT:-15433}"
VALKEY_ADDR="${VALKEY_ADDR:-172.30.0.12}"
VALKEY_PORT="${VALKEY_PORT:-26379}"

port_in_use() {
  local port="$1"
  ss -ltn "( sport = :$port )" | awk 'NR>1 {print $4}' | grep -q .
}

for cmd in k3d kubectl helm docker curl jq; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "required command not found: $cmd" >&2
    exit 1
  fi
done

: "${VAULT_TOKEN:?Set VAULT_TOKEN before running this script}"

vault_curl() {
  if [ "$VAULT_SKIP_VERIFY" = "true" ]; then
    curl -ksS "$@"
  else
    curl -sS "$@"
  fi
}

check_tcp_dependency() {
  local name="$1"
  local host="$2"
  local port="$3"
  if timeout 3 bash -c ":</dev/tcp/${host}/${port}" >/dev/null 2>&1; then
    echo "  - ${name}: ${host}:${port} reachable"
  else
    echo "${name} is not reachable at ${host}:${port}" >&2
    return 1
  fi
}

wait_for_vault_ready() {
  local vault_status_code="000"
  for _ in $(seq 1 30); do
    vault_status_code="$(vault_curl -o /dev/null -w '%{http_code}' \
      -H "X-Vault-Token: $VAULT_TOKEN" \
      "$VAULT_ADDR/v1/sys/health" || true)"
    if [ "$vault_status_code" = "200" ] || [ "$vault_status_code" = "429" ] || [ "$vault_status_code" = "472" ] || [ "$vault_status_code" = "473" ]; then
      return 0
    fi
    sleep 1
  done

  if [ "$vault_status_code" = "503" ]; then
    echo "vault is sealed (status=503). unseal Vault first." >&2
  else
    echo "vault is not ready after 30s (status=${vault_status_code:-000})" >&2
  fi
  return 1
}

if ! k3d cluster list 2>/dev/null | awk 'NR>1 {print $1}' | grep -qx "$CLUSTER_NAME"; then
  if port_in_use "$K3D_HTTP_PORT"; then
    if [ "$K3D_HTTP_PORT" = "80" ]; then
      K3D_HTTP_PORT=8080
      echo "port 80 already in use, fallback to $K3D_HTTP_PORT"
    else
      echo "configured K3D_HTTP_PORT=$K3D_HTTP_PORT is already in use" >&2
      exit 1
    fi
  fi

  if port_in_use "$K3D_HTTPS_PORT"; then
    if [ "$K3D_HTTPS_PORT" = "443" ]; then
      K3D_HTTPS_PORT=8443
      echo "port 443 already in use, fallback to $K3D_HTTPS_PORT"
    else
      echo "configured K3D_HTTPS_PORT=$K3D_HTTPS_PORT is already in use" >&2
      exit 1
    fi
  fi

  K3D_CONFIG_TMP="$(mktemp)"
  trap 'rm -f "$K3D_CONFIG_TMP"' EXIT
  sed \
    -e "s/port: 80:80/port: ${K3D_HTTP_PORT}:80/" \
    -e "s/port: 443:443/port: ${K3D_HTTPS_PORT}:443/" \
    "$ROOT_DIR/infrastructure/k3d/k3d-cluster.yaml" >"$K3D_CONFIG_TMP"

  echo "[1/8] Create k3d cluster"
  k3d cluster create --config "$K3D_CONFIG_TMP"
else
  echo "[1/8] Reuse existing k3d cluster: $CLUSTER_NAME"
fi

echo "[2/8] Validate external dependencies"
wait_for_vault_ready
check_tcp_dependency "postgres-write" "$POSTGRES_WRITE_ADDR" "$POSTGRES_WRITE_PORT"
check_tcp_dependency "postgres-read" "$POSTGRES_READ_ADDR" "$POSTGRES_READ_PORT"
check_tcp_dependency "valkey" "$VALKEY_ADDR" "$VALKEY_PORT"

vault_secret_json="$(vault_curl \
  -H "X-Vault-Token: $VAULT_TOKEN" \
  "$VAULT_ADDR/v1/secret/data/platform/argocd" || true)"
VALKEY_PASSWORD="$(printf '%s' "$vault_secret_json" | jq -r '.data.data.valkey_password // empty' 2>/dev/null || true)"

if [ -z "$VALKEY_PASSWORD" ]; then
  echo "could not read secret key valkey_password from Vault path secret/platform/argocd" >&2
  exit 1
fi

if docker inspect "k3d-${CLUSTER_NAME}-serverlb" >/dev/null 2>&1; then
  DETECTED_HTTPS_PORT="$(docker inspect -f '{{(index (index .NetworkSettings.Ports "443/tcp") 0).HostPort}}' "k3d-${CLUSTER_NAME}-serverlb" 2>/dev/null || true)"
  if [ -n "$DETECTED_HTTPS_PORT" ]; then
    K3D_HTTPS_PORT="$DETECTED_HTTPS_PORT"
  fi
fi

echo "[3/8] External services are managed in a separate workspace/repo"

echo "[4/8] Create argocd namespace"
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -

echo "[5/8] Create ArgoCD external Valkey secret"
kubectl -n argocd create secret generic argocd-external-valkey \
  --from-literal=redis-password="$VALKEY_PASSWORD" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "[6/8] Validate Vault KV for ESO sync"

echo "[7/8] Install ArgoCD via Helm"
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm upgrade --install argocd argo/argo-cd \
  -n argocd \
  -f "$ROOT_DIR/infrastructure/argocd/values-local.yaml"

echo "[8/8] Apply GitOps bootstrap resources"
kubectl apply -f "$ROOT_DIR/gitops/clusters/local/appproject-platform.yaml"
kubectl apply -f "$ROOT_DIR/gitops/clusters/local/appproject-apps.yaml"
kubectl apply -f "$ROOT_DIR/gitops/clusters/local/applicationset-apps.yaml"
kubectl apply -f "$ROOT_DIR/gitops/clusters/local/root-application.yaml"

echo "[INFO] Wait for ArgoCD control-plane readiness"
kubectl -n argocd wait --for=condition=available deployment --all --timeout=180s

echo "Done"
if [ "$K3D_HTTPS_PORT" = "443" ]; then
  echo "ArgoCD URL: https://argocd.local (hosts + mkcert 필요)"
else
  echo "ArgoCD URL: https://argocd.local:$K3D_HTTPS_PORT (hosts + mkcert 필요)"
fi
