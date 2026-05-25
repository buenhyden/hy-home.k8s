#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLUSTER_NAME="hyhome"
ARGOCD_HOST="${ARGOCD_HOST:-argocd.127.0.0.1.nip.io}"
K3D_HTTP_PORT="${K3D_HTTP_PORT:-80}"
K3D_HTTPS_PORT="${K3D_HTTPS_PORT:-443}"
CERT_DIR="${CERT_DIR:-$ROOT_DIR/secrets/certs}"
CERT_FILE="${CERT_FILE:-$CERT_DIR/cert.pem}"
KEY_FILE="${KEY_FILE:-$CERT_DIR/key.pem}"
ROOT_CA_FILE="${ROOT_CA_FILE:-$CERT_DIR/rootCA.pem}"
ROOT_CA_KEY_FILE="${ROOT_CA_KEY_FILE:-$CERT_DIR/rootCA-key.pem}"
VAULT_ADDR="${VAULT_ADDR:-https://vault.127.0.0.1.nip.io}"
VAULT_SKIP_VERIFY="${VAULT_SKIP_VERIFY:-true}"
POSTGRES_WRITE_ADDR="${POSTGRES_WRITE_ADDR:-172.18.0.15}"
POSTGRES_WRITE_PORT="${POSTGRES_WRITE_PORT:-15432}"
POSTGRES_READ_ADDR="${POSTGRES_READ_ADDR:-172.18.0.15}"
POSTGRES_READ_PORT="${POSTGRES_READ_PORT:-15433}"
VALKEY_ADDR="${VALKEY_ADDR:-172.18.0.9}"
VALKEY_PORT="${VALKEY_PORT:-6379}"

port_in_use() {
  local port="$1"
  ss -ltn "( sport = :$port )" | awk 'NR>1 {print $4}' | grep -q .
}

fail() {
  echo "[FAIL] $*" >&2
  exit 1
}

for cmd in k3d kubectl helm docker curl jq openssl rg; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    fail "required command not found: $cmd"
  fi
done

# Bootstrap-only exception:
# this script may use kubectl apply before ArgoCD owns the cluster because it creates
# the initial namespaces, secrets, MetalLB primitives, and root GitOps applications.
# Steady-state infrastructure changes must remain repo-backed and reconciled by ArgoCD.

if [ -z "${VAULT_TOKEN:-}" ]; then
  fail "Set VAULT_TOKEN before running this script"
fi

INOTIFY_INSTANCES="$(cat /proc/sys/fs/inotify/max_user_instances 2>/dev/null || echo 0)"
if [ "${INOTIFY_INSTANCES}" -lt 512 ]; then
  fail "fs.inotify.max_user_instances=${INOTIFY_INSTANCES} is too low for k3d (need >=512). Run: sudo sysctl -w fs.inotify.max_user_instances=1024 && echo 'fs.inotify.max_user_instances=1024' | sudo tee /etc/sysctl.d/99-k3d.conf"
fi

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
    echo "[FAIL] ${name} is not reachable at ${host}:${port}" >&2
    return 1
  fi
}

warn_tcp_dependency() {
  local name="$1"
  local host="$2"
  local port="$3"
  if timeout 3 bash -c ":</dev/tcp/${host}/${port}" >/dev/null 2>&1; then
    echo "  - ${name}: ${host}:${port} reachable"
  else
    echo "[WARN] ${name} is not reachable at ${host}:${port} (observability, non-critical)" >&2
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
    echo "[FAIL] vault is sealed (status=503). unseal Vault first." >&2
  else
    echo "[FAIL] vault is not ready after 30s (status=${vault_status_code:-000})" >&2
  fi
  return 1
}

require_file() {
  local path="$1"
  if [ ! -f "$path" ]; then
    echo "[FAIL] required file not found: $path" >&2
    return 1
  fi
}

validate_cert_for_host() {
  local cert_file="$1"
  local host="$2"
  local sans
  sans="$(openssl x509 -in "$cert_file" -noout -ext subjectAltName 2>/dev/null || true)"
  if [ -z "$sans" ]; then
    echo "[FAIL] failed to read certificate SAN from: $cert_file" >&2
    return 1
  fi

  if printf '%s' "$sans" | rg -q "DNS:${host}(,|$)"; then
    return 0
  fi

  if printf '%s' "$host" | rg -q '^.+\.127\.0\.0\.1\.nip\.io$' && \
    printf '%s' "$sans" | rg -q 'DNS:\*\.127\.0\.0\.1\.nip\.io(,|$)'; then
    return 0
  fi

  echo "[FAIL] certificate SAN does not include host=${host}. reissue cert in $CERT_DIR" >&2
  return 1
}

if ! k3d cluster list 2>/dev/null | awk 'NR>1 {print $1}' | grep -qx "$CLUSTER_NAME"; then
  if port_in_use "$K3D_HTTP_PORT"; then
    if [ "$K3D_HTTP_PORT" = "80" ]; then
      K3D_HTTP_PORT=8080
      echo "port 80 already in use, fallback to $K3D_HTTP_PORT"
    else
      fail "configured K3D_HTTP_PORT=$K3D_HTTP_PORT is already in use"
    fi
  fi

  if port_in_use "$K3D_HTTPS_PORT"; then
    if [ "$K3D_HTTPS_PORT" = "443" ]; then
      K3D_HTTPS_PORT=8443
      echo "port 443 already in use, fallback to $K3D_HTTPS_PORT"
    else
      fail "configured K3D_HTTPS_PORT=$K3D_HTTPS_PORT is already in use"
    fi
  fi

  K3D_CONFIG_TMP="$(mktemp)"
  trap 'rm -f "$K3D_CONFIG_TMP"' EXIT
  sed \
    -e "s/port: 80:80/port: ${K3D_HTTP_PORT}:80/" \
    -e "s/port: 443:443/port: ${K3D_HTTPS_PORT}:443/" \
    "$ROOT_DIR/infrastructure/k3d/k3d-cluster.yaml" >"$K3D_CONFIG_TMP"

  echo "[1/11] Create k3d cluster"
  k3d cluster create --config "$K3D_CONFIG_TMP"
else
  echo "[1/11] Reuse existing k3d cluster: $CLUSTER_NAME"
fi

echo "[2/11] Validate external dependencies"
wait_for_vault_ready
check_tcp_dependency "postgres-write" "$POSTGRES_WRITE_ADDR" "$POSTGRES_WRITE_PORT"
check_tcp_dependency "postgres-read" "$POSTGRES_READ_ADDR" "$POSTGRES_READ_PORT"
check_tcp_dependency "valkey" "$VALKEY_ADDR" "$VALKEY_PORT"

vault_secret_json="$(vault_curl \
  -H "X-Vault-Token: $VAULT_TOKEN" \
  "$VAULT_ADDR/v1/secret/data/platform/argocd" || true)"
VALKEY_PASSWORD="$(printf '%s' "$vault_secret_json" | jq -r '.data.data.valkey_password // empty' 2>/dev/null || true)"

if [ -z "$VALKEY_PASSWORD" ]; then
  fail "could not read secret key valkey_password from Vault path secret/platform/argocd"
fi

if docker inspect "k3d-${CLUSTER_NAME}-serverlb" >/dev/null 2>&1; then
  DETECTED_HTTPS_PORT="$(docker inspect -f '{{(index (index .NetworkSettings.Ports "443/tcp") 0).HostPort}}' "k3d-${CLUSTER_NAME}-serverlb" 2>/dev/null || true)"
  if [ -n "$DETECTED_HTTPS_PORT" ]; then
    K3D_HTTPS_PORT="$DETECTED_HTTPS_PORT"
  fi
fi

echo "[3/11] Validate TLS certificate inputs"
require_file "$CERT_FILE"
require_file "$KEY_FILE"
require_file "$ROOT_CA_FILE"
require_file "$ROOT_CA_KEY_FILE"
validate_cert_for_host "$CERT_FILE" "$ARGOCD_HOST"

echo "[4/11] Pre-check observability endpoints (warn-only)"
warn_tcp_dependency "prometheus" "172.18.0.10" "9090"
warn_tcp_dependency "loki" "172.18.0.13" "3100"
warn_tcp_dependency "tempo" "172.18.0.12" "3200"
warn_tcp_dependency "alloy" "172.18.0.11" "4317"
warn_tcp_dependency "grafana" "172.18.0.14" "3000"

echo "[5/11] Install MetalLB and configure IP pool"
helm repo add metallb https://metallb.github.io/metallb
helm repo update metallb
helm upgrade --install metallb metallb/metallb \
  -n metallb-system --create-namespace \
  --set frr-k8s.prometheus.serviceMonitor.enabled=false \
  --wait --timeout=300s
kubectl apply -f "$ROOT_DIR/infrastructure/ipaddresspool.yaml"
kubectl apply -f "$ROOT_DIR/infrastructure/l2advertisement.yaml"

echo "[6/11] Bootstrap argocd namespace and secrets"
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
kubectl -n argocd create secret generic argocd-external-valkey \
  --from-literal=redis-password="$VALKEY_PASSWORD" \
  --dry-run=client -o yaml | kubectl apply -f -
kubectl -n argocd create secret tls argocd-local-tls \
  --cert="$CERT_FILE" \
  --key="$KEY_FILE" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "[7/11] Bootstrap cert-manager prerequisites"
kubectl create namespace cert-manager --dry-run=client -o yaml | kubectl apply -f -
kubectl -n cert-manager create secret tls mkcert-root-ca \
  --cert="$ROOT_CA_FILE" \
  --key="$ROOT_CA_KEY_FILE" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "[7.5/11] Pre-create platform namespace and external service endpoints"
kubectl create namespace platform --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -k "$ROOT_DIR/gitops/platform/external-services"

echo "[8/11] Install ArgoCD via Helm"
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update argo
helm upgrade --install argocd argo/argo-cd \
  -n argocd \
  -f "$ROOT_DIR/infrastructure/argocd/values-local.yaml"

echo "[9/11] Apply GitOps bootstrap resources"
kubectl apply -f "$ROOT_DIR/gitops/clusters/local/appproject-platform.yaml"
kubectl apply -f "$ROOT_DIR/gitops/clusters/local/appproject-apps.yaml"
kubectl apply -f "$ROOT_DIR/gitops/clusters/local/applicationset-apps.yaml"
kubectl apply -f "$ROOT_DIR/gitops/clusters/local/root-application.yaml"

echo "[10/11] Wait for ArgoCD control-plane readiness"
if ! kubectl -n argocd wait --for=condition=available deployment --all --timeout=300s; then
  echo "[WARN] some ArgoCD deployments not ready within 300s — current state:" >&2
  kubectl -n argocd get deployment -o wide >&2
  kubectl -n argocd get pods --field-selector=status.phase!=Running >&2
  fail "ArgoCD control-plane did not become fully available"
fi

echo "[11/11] Done"
if [ "$K3D_HTTPS_PORT" = "443" ]; then
  echo "ArgoCD URL: https://$ARGOCD_HOST (Traefik 443 경유)"
else
  echo "ArgoCD URL: https://$ARGOCD_HOST:$K3D_HTTPS_PORT (fallback direct)"
fi

if [ -f "$ROOT_CA_FILE" ]; then
  echo "Root CA hint: import $ROOT_CA_FILE into local trust store when browser trust is required"
fi
