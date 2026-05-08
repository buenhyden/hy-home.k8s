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
rg -q 'valkey-external' /tmp/platform-services.txt || fail "missing valkey-external"

rw_port="$(kubectl -n platform get svc postgres-write-external -o jsonpath='{.spec.ports[0].port}' 2>/dev/null || true)"
[ "$rw_port" = "15432" ] || fail "postgres-write-external port mismatch (actual=$rw_port)"

ro_port="$(kubectl -n platform get svc postgres-read-external -o jsonpath='{.spec.ports[0].port}' 2>/dev/null || true)"
[ "$ro_port" = "15433" ] || fail "postgres-read-external port mismatch (actual=$ro_port)"

vault_port="$(kubectl -n platform get svc vault-external -o jsonpath='{.spec.ports[0].port}' 2>/dev/null || true)"
[ "$vault_port" = "8200" ] || fail "vault-external port mismatch (actual=$vault_port)"

valkey_port="$(kubectl -n platform get svc valkey-external -o jsonpath='{.spec.ports[0].port}' 2>/dev/null || true)"
[ "$valkey_port" = "6379" ] || fail "valkey-external port mismatch (actual=$valkey_port)"

valkey_ep_port="$(kubectl -n platform get endpointslice valkey-external-1 -o jsonpath='{.ports[0].port}' 2>/dev/null || true)"
[ "$valkey_ep_port" = "6379" ] || fail "valkey EndpointSlice port mismatch (actual=$valkey_ep_port)"

valkey_ep_addr="$(kubectl -n platform get endpointslice valkey-external-1 -o jsonpath='{.endpoints[0].addresses[0]}' 2>/dev/null || true)"
[ "$valkey_ep_addr" = "172.18.0.9" ] || fail "valkey EndpointSlice address mismatch (actual=$valkey_ep_addr)"

echo "[INFO] Checking observability external service contracts"

kubectl -n platform get svc,endpointslice > /tmp/platform-services.txt 2>/dev/null || true

for svc in prometheus-external loki-external tempo-external alloy-external grafana-external; do
  rg -q "$svc" /tmp/platform-services.txt || fail "missing $svc in platform namespace"
done

check_obs_port() {
  local svc="$1"
  local expected_port="$2"
  local actual
  actual="$(kubectl -n platform get svc "$svc" -o jsonpath='{.spec.ports[0].port}' 2>/dev/null || true)"
  [ "$actual" = "$expected_port" ] || fail "${svc} port mismatch (expected=${expected_port}, actual=${actual})"
}

check_obs_port "prometheus-external" "9090"
check_obs_port "loki-external" "3100"
check_obs_port "tempo-external" "3200"
check_obs_port "alloy-external" "4317"
check_obs_port "grafana-external" "3000"

check_obs_ep() {
  local slice="$1"
  local expected_addr="$2"
  local actual
  actual="$(kubectl -n platform get endpointslice "${slice}-1" -o jsonpath='{.endpoints[0].addresses[0]}' 2>/dev/null || true)"
  [ "$actual" = "$expected_addr" ] || fail "${slice}-1 address mismatch (expected=${expected_addr}, actual=${actual})"
}

check_obs_ep "prometheus-external" "172.18.0.10"
check_obs_ep "loki-external" "172.18.0.13"
check_obs_ep "tempo-external" "172.18.0.12"
check_obs_ep "alloy-external" "172.18.0.11"
check_obs_ep "grafana-external" "172.18.0.14"

echo "[PASS] external service contract checks passed"
