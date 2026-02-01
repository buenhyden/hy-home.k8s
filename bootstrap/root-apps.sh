#!/bin/bash
set -euo pipefail

echo "=== Deploying Root Applications ==="

# Deploy Apps root application
echo "Deploying Apps root application..."
kubectl apply -f ../clusters/docker-desktop/apps.yaml

# Deploy Infrastructure root application
echo "Deploying Infrastructure root application..."
kubectl apply -f ../clusters/docker-desktop/infrastructure.yaml

echo ""
echo "=== Root Applications Deployed ==="
echo ""
echo "Monitor sync status:"
echo "  kubectl get applications -n argocd"
echo ""
echo "Or access ArgoCD UI:"
echo "  kubectl port-forward svc/argocd-server -n argocd 8080:443"
echo "  Visit: https://localhost:8080"
