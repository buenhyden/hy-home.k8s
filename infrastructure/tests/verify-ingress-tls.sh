#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ARGOCD_HOST="${ARGOCD_HOST:-argocd.127.0.0.1.nip.io}"
ARGOCD_FALLBACK_PORT="${ARGOCD_FALLBACK_PORT:-8443}"
CHECK_TRAEFIK_443="${CHECK_TRAEFIK_443:-false}"

fail() {
  echo "[FAIL] $*" >&2
  exit 1
}

echo "[INFO] Checking ingress/TLS contracts"

kubectl version --request-timeout=5s >/dev/null 2>&1 || \
  fail "kubectl cannot reach cluster (check kubeconfig/context)"

svc_type="$(kubectl -n ingress-nginx get svc ingress-nginx-controller -o jsonpath='{.spec.type}' 2>/dev/null || true)"
[ "$svc_type" = "LoadBalancer" ] || fail "ingress-nginx-controller type mismatch (actual=$svc_type)"

ing_host="$(kubectl -n argocd get ingress argocd-server -o jsonpath='{.spec.rules[0].host}' 2>/dev/null || true)"
[ "$ing_host" = "$ARGOCD_HOST" ] || fail "argocd ingress host mismatch (actual=$ing_host)"

tls_host="$(kubectl -n argocd get ingress argocd-server -o jsonpath='{.spec.tls[0].hosts[0]}' 2>/dev/null || true)"
[ "$tls_host" = "$ARGOCD_HOST" ] || fail "argocd ingress tls host mismatch (actual=$tls_host)"

tls_secret="$(kubectl -n argocd get ingress argocd-server -o jsonpath='{.spec.tls[0].secretName}' 2>/dev/null || true)"
[ "$tls_secret" = "argocd-local-tls" ] || fail "argocd ingress tls secret mismatch (actual=$tls_secret)"

secret_type="$(kubectl -n argocd get secret argocd-local-tls -o jsonpath='{.type}' 2>/dev/null || true)"
[ "$secret_type" = "kubernetes.io/tls" ] || fail "argocd-local-tls type mismatch (actual=$secret_type)"

curl -kIs --max-time 5 "https://${ARGOCD_HOST}:${ARGOCD_FALLBACK_PORT}" >/tmp/argocd-tls-fallback.txt 2>/dev/null || \
  fail "https fallback endpoint is not reachable (${ARGOCD_HOST}:${ARGOCD_FALLBACK_PORT})"
rg -q '^HTTP/' /tmp/argocd-tls-fallback.txt || \
  fail "https fallback endpoint did not return HTTP response"

if [ "$CHECK_TRAEFIK_443" = "true" ]; then
  curl -kIs --max-time 5 "https://${ARGOCD_HOST}" >/tmp/argocd-tls-traefik443.txt 2>/dev/null || \
    fail "Traefik 443 endpoint is not reachable (${ARGOCD_HOST}:443)"
  rg -q '^HTTP/' /tmp/argocd-tls-traefik443.txt || \
    fail "Traefik 443 endpoint did not return HTTP response"
  echo "[INFO] Traefik 443 check passed"
else
  echo "[INFO] Traefik 443 check skipped (set CHECK_TRAEFIK_443=true to enforce)"
fi

echo "[INFO] Checking least-privilege consistency"

proj_has_allowlist="$(kubectl -n argocd get appproject platform -o jsonpath='{.spec.clusterResourceWhitelist[?(@.kind=="ClusterSecretStore")].kind}' 2>/dev/null || true)"
[ "$proj_has_allowlist" = "ClusterSecretStore" ] || \
  fail "AppProject allow-list mismatch (ClusterSecretStore missing)"

rg -q 'path "secret/data/platform/argocd"' "$ROOT_DIR/infrastructure/vault/policies/eso-read.hcl" || \
  fail "Vault policy missing secret/data/platform/argocd"
rg -q 'path "secret/data/platform/postgres-app"' "$ROOT_DIR/infrastructure/vault/policies/eso-read.hcl" || \
  fail "Vault policy missing secret/data/platform/postgres-app"

echo "[INFO] Checking Dashboard and Kiali ingress TLS"

dashboard_tls_secret="$(kubectl -n kubernetes-dashboard get ingress kubernetes-dashboard-kong-proxy -o jsonpath='{.spec.tls[0].secretName}' 2>/dev/null || true)"
[ "$dashboard_tls_secret" = "dashboard-tls" ] || \
  echo "[WARN] dashboard ingress tls secret not found or mismatch (actual=$dashboard_tls_secret)"

kiali_tls_secret="$(kubectl -n istio-system get ingress kiali -o jsonpath='{.spec.tls[0].secretName}' 2>/dev/null || true)"
[ "$kiali_tls_secret" = "kiali-tls" ] || \
  echo "[WARN] kiali ingress tls secret not found or mismatch (actual=$kiali_tls_secret)"

echo "[PASS] ingress/TLS contract checks passed"
