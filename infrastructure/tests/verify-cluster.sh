#!/usr/bin/env bash
set -euo pipefail

fail() {
  echo "[FAIL] $*" >&2
  exit 1
}

echo "[INFO] Checking cluster node topology (1 master + 3 workers baseline)"

kubectl_version_output="$(kubectl version --request-timeout=5s 2>&1 >/dev/null)" || {
  if [[ "$kubectl_version_output" == *"x509: certificate signed by unknown authority"* ]]; then
    fail "kubectl cannot reach cluster: kubeconfig TLS trust failed (x509: certificate signed by unknown authority)"
  fi
  kubectl_version_first_line="${kubectl_version_output%%$'\n'*}"
  fail "kubectl cannot reach cluster (check kubeconfig/context): ${kubectl_version_first_line:-no kubectl error output}"
}

node_count="$(kubectl get nodes --no-headers | wc -l | tr -d ' ')"
[ -n "$node_count" ] || fail "failed to get node count"

if [ "$node_count" -lt 4 ]; then
  fail "expected at least 4 nodes, got $node_count"
fi

ready_count="$(kubectl get nodes --no-headers 2>/dev/null | awk '$2 ~ /Ready/ {c++} END {print c+0}')"
if [ "$ready_count" -lt 4 ]; then
  fail "expected at least 4 Ready nodes, got $ready_count"
fi

echo "[PASS] cluster topology check passed (nodes=$node_count, ready=$ready_count)"

echo "[INFO] Checking MetalLB readiness"
metallb_ready="$(kubectl -n metallb-system get deploy metallb-controller \
  -o jsonpath='{.status.readyReplicas}' 2>/dev/null || true)"
if [ "${metallb_ready:-0}" -lt 1 ]; then
  metallb_ready="$(kubectl -n metallb-system get deploy controller \
    -o jsonpath='{.status.readyReplicas}' 2>/dev/null || true)"
fi
[ "${metallb_ready:-0}" -ge 1 ] || \
  fail "metallb controller is not ready (readyReplicas=${metallb_ready:-0})"

ip_pool="$(kubectl get ipaddresspool -n metallb-system local-services \
  -o jsonpath='{.spec.addresses[0]}' 2>/dev/null || true)"
[ -n "$ip_pool" ] || fail "MetalLB IPAddressPool 'local-services' not found"

echo "[PASS] MetalLB ready (pool=$ip_pool)"
