#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$script_dir/verify-cluster.sh"
"$script_dir/verify-gitops.sh"
"$script_dir/verify-secrets.sh"
"$script_dir/verify-external-services.sh"
"$script_dir/verify-network-policies.sh"

echo "[PASS] all verification scripts completed"
