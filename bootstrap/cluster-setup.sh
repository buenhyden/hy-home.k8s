#!/bin/bash
set -euo pipefail

echo "=== Creating Kind Cluster ==="

# Check if kind is installed
if ! command -v kind &> /dev/null; then
    echo "Error: kind is not installed"
    echo "Install from: https://kind.sigs.k8s.io/docs/user/quick-start/#installation"
    exit 1
fi

# Cluster name
CLUSTER_NAME="docker-desktop"

# Check if cluster exists
if kind get clusters 2>&1 | grep -q "^${CLUSTER_NAME}$"; then
    echo "Cluster '${CLUSTER_NAME}' already exists"
    read -p "Delete and recreate? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kind delete cluster --name "${CLUSTER_NAME}"
    else
        echo "Using existing cluster"
        exit 0
    fi
fi

# Create kind config
cat > /tmp/kind-config.yaml <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
  - role: worker
EOF

# Create cluster
echo "Creating cluster '${CLUSTER_NAME}'..."
kind create cluster --config /tmp/kind-config.yaml --name "${CLUSTER_NAME}"

# Verify cluster
kubectl cluster-info --context kind-${CLUSTER_NAME}
kubectl get nodes

echo ""
echo "=== Cluster Created Successfully ==="
echo ""
echo "Next steps:"
echo "1. Configure hybrid networking (see bootstrap/README.md)"
echo "2. Run: ./argocd-install.sh"
