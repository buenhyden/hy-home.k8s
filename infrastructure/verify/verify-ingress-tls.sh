#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ARGOCD_HOST="${ARGOCD_HOST:-argo.hy-k8s.home.arpa}"
ARGOCD_FALLBACK_PORT_WAS_SET="${ARGOCD_FALLBACK_PORT+x}"
ARGOCD_FALLBACK_PORT="${ARGOCD_FALLBACK_PORT:-443}"
ARGOCD_FALLBACK_IP="${ARGOCD_FALLBACK_IP:-}"
K8S_ROUTER_IP="${K8S_ROUTER_IP:-192.168.0.14}"
CHECK_K8S_ROUTER="${CHECK_K8S_ROUTER:-false}"

fail() {
  echo "[FAIL] $*" >&2
  exit 1
}

TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/verify-ingress-tls.XXXXXXXX")" ||
  fail "cannot create private temporary directory"
TLS_FALLBACK_OUTPUT="$TEMP_DIR/argocd-tls-fallback.txt"
TLS_ROUTER_OUTPUT="$TEMP_DIR/argocd-tls-router443.txt"

cleanup() {
  local status=$?
  trap - EXIT INT TERM
  if ! rm -rf -- "$TEMP_DIR"; then
    echo "[FAIL] cannot remove private temporary directory" >&2
    [ "$status" -ne 0 ] || status=1
  fi
  exit "$status"
}

trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

echo "[INFO] Checking ingress/TLS contracts"

kubectl version --request-timeout=5s >/dev/null 2>&1 ||
  fail "kubectl cannot reach cluster (check kubeconfig/context)"

svc_type="$(kubectl -n ingress-nginx get svc ingress-nginx-controller -o jsonpath='{.spec.type}' 2>/dev/null || true)"
[ "$svc_type" = "LoadBalancer" ] || fail "ingress-nginx-controller type mismatch (actual=$svc_type)"

ingress_lb_ip="$(kubectl -n ingress-nginx get svc ingress-nginx-controller \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || true)"
if [ -z "$ARGOCD_FALLBACK_IP" ]; then
  if [ -z "$ARGOCD_FALLBACK_PORT_WAS_SET" ]; then
    ARGOCD_FALLBACK_IP="$ingress_lb_ip"
  else
    ARGOCD_FALLBACK_IP="127.0.0.1"
  fi
fi
[ -n "$ARGOCD_FALLBACK_IP" ] || fail "ingress-nginx-controller LoadBalancer IP is empty"

ing_host="$(kubectl -n argocd get ingress argocd-server -o jsonpath='{.spec.rules[0].host}' 2>/dev/null || true)"
[ "$ing_host" = "$ARGOCD_HOST" ] || fail "argocd ingress host mismatch (actual=$ing_host)"

tls_host="$(kubectl -n argocd get ingress argocd-server -o jsonpath='{.spec.tls[0].hosts[0]}' 2>/dev/null || true)"
[ "$tls_host" = "$ARGOCD_HOST" ] || fail "argocd ingress tls host mismatch (actual=$tls_host)"

tls_secret="$(kubectl -n argocd get ingress argocd-server -o jsonpath='{.spec.tls[0].secretName}' 2>/dev/null || true)"
[ "$tls_secret" = "argocd-local-tls" ] || fail "argocd ingress tls secret mismatch (actual=$tls_secret)" # pragma: allowlist secret

secret_type="$(kubectl -n argocd get secret argocd-local-tls -o jsonpath='{.type}' 2>/dev/null || true)"
[ "$secret_type" = "kubernetes.io/tls" ] || fail "argocd-local-tls type mismatch (actual=$secret_type)" # pragma: allowlist secret

curl -kIs --max-time 5 \
  --resolve "${ARGOCD_HOST}:${ARGOCD_FALLBACK_PORT}:${ARGOCD_FALLBACK_IP}" \
  "https://${ARGOCD_HOST}:${ARGOCD_FALLBACK_PORT}" >"$TLS_FALLBACK_OUTPUT" 2>/dev/null ||
  fail "https fallback endpoint is not reachable (${ARGOCD_HOST}:${ARGOCD_FALLBACK_PORT} via ${ARGOCD_FALLBACK_IP})"
rg -q '^HTTP/' "$TLS_FALLBACK_OUTPUT" ||
  fail "https fallback endpoint did not return HTTP response"

# k8s router (ADR-0043): the k3d serverlb on K8S_ROUTER_IP:443 must answer for
# the canonical host, and the apex path must redirect to it.
if [ "$CHECK_K8S_ROUTER" = "true" ]; then
  curl -kIs --max-time 5 --resolve "${ARGOCD_HOST}:443:${K8S_ROUTER_IP}" \
    "https://${ARGOCD_HOST}" >"$TLS_ROUTER_OUTPUT" 2>/dev/null ||
    fail "k8s router endpoint is not reachable (${ARGOCD_HOST} via ${K8S_ROUTER_IP}:443)"
  rg -q '^HTTP/' "$TLS_ROUTER_OUTPUT" ||
    fail "k8s router endpoint did not return HTTP response"
  curl -kIs --max-time 5 --resolve "hy-k8s.home.arpa:443:${K8S_ROUTER_IP}" \
    "https://hy-k8s.home.arpa/argo" >"$TLS_ROUTER_OUTPUT" 2>/dev/null ||
    fail "k8s router apex endpoint is not reachable (hy-k8s.home.arpa via ${K8S_ROUTER_IP}:443)"
  rg -qi "^location: https://${ARGOCD_HOST}/" "$TLS_ROUTER_OUTPUT" ||
    fail "hy-k8s.home.arpa/argo does not redirect to https://${ARGOCD_HOST}/"
  echo "[INFO] k8s router check passed"
else
  echo "[INFO] k8s router check skipped (set CHECK_K8S_ROUTER=true to enforce)"
fi

echo "[INFO] Checking least-privilege consistency"

proj_has_allowlist="$(kubectl -n argocd get appproject platform -o jsonpath='{.spec.clusterResourceWhitelist[?(@.kind=="ClusterSecretStore")].kind}' 2>/dev/null || true)"
[ "$proj_has_allowlist" = "ClusterSecretStore" ] ||
  fail "AppProject allow-list mismatch (ClusterSecretStore missing)"

rg -q 'path "secret/data/platform/argocd"' "$ROOT_DIR/infrastructure/vault/policies/eso-read.hcl" ||
  fail "Vault policy missing secret/data/platform/argocd"
rg -q 'path "secret/data/platform/postgres-app"' "$ROOT_DIR/infrastructure/vault/policies/eso-read.hcl" ||
  fail "Vault policy missing secret/data/platform/postgres-app"

echo "[INFO] Checking Headlamp and Kiali ingress TLS"

headlamp_tls_secret="$(kubectl -n headlamp get ingress headlamp -o jsonpath='{.spec.tls[0].secretName}' 2>/dev/null || true)"
[ "$headlamp_tls_secret" = "headlamp-tls" ] || { # pragma: allowlist secret
  echo "[WARN] headlamp ingress tls secret not found or mismatch (actual=$headlamp_tls_secret)"
}

kiali_tls_secret="$(kubectl -n istio-system get ingress kiali -o jsonpath='{.spec.tls[0].secretName}' 2>/dev/null || true)"
[ "$kiali_tls_secret" = "kiali-tls" ] || { # pragma: allowlist secret
  echo "[WARN] kiali ingress tls secret not found or mismatch (actual=$kiali_tls_secret)"
}

echo "[PASS] ingress/TLS contract checks passed"
