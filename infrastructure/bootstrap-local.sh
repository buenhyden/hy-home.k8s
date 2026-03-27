#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLUSTER_NAME="hyhome"

for cmd in k3d kubectl helm docker; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "required command not found: $cmd" >&2
    exit 1
  fi
done

: "${VALKEY_PASSWORD:?Set VALKEY_PASSWORD before running this script}"

if ! k3d cluster list 2>/dev/null | awk 'NR>1 {print $1}' | grep -qx "$CLUSTER_NAME"; then
  echo "[1/7] Create k3d cluster"
  k3d cluster create --config "$ROOT_DIR/infrastructure/k3d/k3d-cluster.yaml"
else
  echo "[1/7] Reuse existing k3d cluster: $CLUSTER_NAME"
fi

echo "[2/7] Start external docker services"
docker compose -f "$ROOT_DIR/infrastructure/docker/docker-compose.external.yaml" up -d

echo "[3/7] Create argocd namespace"
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -

echo "[4/7] Create ArgoCD external Valkey secret"
kubectl -n argocd create secret generic argocd-external-valkey \
  --from-literal=password="$VALKEY_PASSWORD" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "[5/7] Seed Vault KV for ESO sync"
docker exec -e VALKEY_PASSWORD="$VALKEY_PASSWORD" vault-external sh -lc 'export VAULT_ADDR=http://127.0.0.1:8200 VAULT_TOKEN=root; vault kv put secret/platform/argocd valkey_password="$VALKEY_PASSWORD" >/dev/null'

echo "[6/7] Install ArgoCD via Helm"
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm upgrade --install argocd argo/argo-cd \
  -n argocd \
  -f "$ROOT_DIR/infrastructure/argocd/values-local.yaml"

echo "[7/7] Apply GitOps bootstrap resources"
kubectl apply -f "$ROOT_DIR/gitops/clusters/local/appproject-platform.yaml"
kubectl apply -f "$ROOT_DIR/gitops/clusters/local/appproject-apps.yaml"
kubectl apply -f "$ROOT_DIR/gitops/clusters/local/applicationset-apps.yaml"
kubectl apply -f "$ROOT_DIR/gitops/clusters/local/root-application.yaml"

echo "Done"
echo "ArgoCD URL: https://argocd.local (hosts + mkcert 필요)"
