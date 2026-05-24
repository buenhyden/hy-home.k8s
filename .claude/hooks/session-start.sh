#!/usr/bin/env bash
# session-start.sh - optional k3d state + unhealthy pods + ArgoCD health check
# Runs at SessionStart. Exits 0 always (non-blocking informational output).
set -euo pipefail

echo "=== hy-home.k8s session start ==="

if [[ "${HY_HOME_K8S_ENABLE_SESSION_LIVE_PROBES:-0}" != "1" ]]; then
  echo "(live session probes skipped; set HY_HOME_K8S_ENABLE_SESSION_LIVE_PROBES=1 for read-only k3d/kubectl checks)"
  echo "==================================="
  exit 0
fi

# k3d cluster list
if command -v k3d &>/dev/null; then
  echo "--- k3d clusters ---"
  k3d cluster list 2>/dev/null || echo "(k3d not reachable)"
else
  echo "(k3d not installed)"
fi

# unhealthy pods
if command -v kubectl &>/dev/null; then
  echo "--- unhealthy pods ---"
  kubectl get pods -A --field-selector='status.phase!=Running,status.phase!=Succeeded' \
    --no-headers 2>/dev/null | grep -v "^$" || echo "(none)"

  # ArgoCD app health
  echo "--- ArgoCD app health ---"
  kubectl get applications -n argocd \
    -o custom-columns='NAME:.metadata.name,HEALTH:.status.health.status,SYNC:.status.sync.status' \
    --no-headers 2>/dev/null || echo "(ArgoCD not reachable)"
else
  echo "(kubectl not installed)"
fi

echo "==================================="
exit 0
