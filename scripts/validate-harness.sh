#!/usr/bin/env bash
# validate-harness.sh — repo-static harness validation wrapper.
# Bundles the existing repo-static gates that guard harness surfaces. It adds no
# new validation logic and runs no live-cluster checks. Live k3d / ArgoCD / Vault
# verification stays in approved operations runbooks, not in this wrapper.
# Usage: bash scripts/validate-harness.sh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "==> Repository quality gates"
bash scripts/validate-repo-quality-gates.sh .

echo "==> GitOps object identity and deletion set"
python3 scripts/validate-gitops-change-set.py --root . --base-ref HEAD

echo "==> GitOps structure"
bash scripts/validate-gitops-structure.sh

echo "==> Kubernetes manifests"
bash scripts/validate-k8s-manifests.sh .

echo "==> Secret handling"
bash scripts/check-secret-handling.sh .

echo "==> Policy gates"
bash scripts/validate-policy-gates.sh .

echo "==> Static infrastructure contracts"
bash infrastructure/tests/verify-contracts-static.sh

echo "==> Diff hygiene"
git diff --check

echo "PASS harness repo-static validation"
