#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "$script_dir/verify-cluster.sh"
bash "$script_dir/verify-gitops.sh"
bash "$script_dir/verify-secrets.sh"
bash "$script_dir/verify-external-services.sh"
bash "$script_dir/verify-network-policies.sh"
bash "$script_dir/verify-ingress-tls.sh"

echo "[PASS] all verification scripts completed"
