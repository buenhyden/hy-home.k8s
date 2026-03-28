#!/usr/bin/env bash
set -euo pipefail

fail() {
  echo "[FAIL] $*" >&2
  exit 1
}

echo "[INFO] Checking external service contracts"

kubectl version --request-timeout=5s >/dev/null 2>&1 || \
  fail "kubectl cannot reach cluster (check kubeconfig/context)"

kubectl -n platform get svc,endpointslice > /tmp/platform-services.txt

rg -q 'postgres-write-external' /tmp/platform-services.txt || fail "missing postgres-write-external"
rg -q 'postgres-read-external' /tmp/platform-services.txt || fail "missing postgres-read-external"
rg -q 'vault-external' /tmp/platform-services.txt || fail "missing vault-external"

rw_port="$(kubectl -n platform get svc postgres-write-external -o jsonpath='{.spec.ports[0].port}' 2>/dev/null || true)"
[ "$rw_port" = "15432" ] || fail "postgres-write-external port mismatch (actual=$rw_port)"

ro_port="$(kubectl -n platform get svc postgres-read-external -o jsonpath='{.spec.ports[0].port}' 2>/dev/null || true)"
[ "$ro_port" = "15433" ] || fail "postgres-read-external port mismatch (actual=$ro_port)"

vault_port="$(kubectl -n platform get svc vault-external -o jsonpath='{.spec.ports[0].port}' 2>/dev/null || true)"
[ "$vault_port" = "8200" ] || fail "vault-external port mismatch (actual=$vault_port)"

valkey_host="$(kubectl -n platform get svc valkey-external -o jsonpath='{.spec.externalName}' 2>/dev/null || true)"
[ "$valkey_host" = "host.k3d.internal" ] || fail "valkey externalName mismatch (actual=$valkey_host)"

valkey_port="$(kubectl -n platform get svc valkey-external -o jsonpath='{.spec.ports[0].port}' 2>/dev/null || true)"
[ "$valkey_port" = "26379" ] || fail "valkey-external port mismatch (actual=$valkey_port)"

echo "[PASS] external service contract checks passed"
