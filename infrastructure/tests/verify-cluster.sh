#!/usr/bin/env bash
set -euo pipefail

fail() {
  echo "[FAIL] $*" >&2
  exit 1
}

echo "[INFO] Checking cluster node topology (1 master + 3 workers baseline)"

kubectl version --request-timeout=5s >/dev/null 2>&1 || \
  fail "kubectl cannot reach cluster (check kubeconfig/context)"

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
