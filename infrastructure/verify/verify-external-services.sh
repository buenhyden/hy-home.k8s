#!/usr/bin/env bash
set -euo pipefail

fail() {
  echo "[FAIL] $*" >&2
  exit 1
}

TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/verify-external-services.XXXXXXXX")" ||
  fail "cannot create private temporary directory"
PLATFORM_SERVICES_OUTPUT="$TEMP_DIR/platform-services.json"

cleanup() {
  local status=$?
  trap - EXIT INT TERM
  if ! rm -rf -- "$TEMP_DIR"; then
    echo "[FAIL] cannot remove private temporary directory" >&2
    [ "$status" -ne 0 ] || status=1
  fi
  exit "$status"
}

trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

echo "[INFO] Checking external service contracts"

kubectl version --request-timeout=5s >/dev/null 2>&1 ||
  fail "kubectl cannot reach cluster (check kubeconfig/context)"
command -v python3 >/dev/null 2>&1 || fail "python3 is required for service contract validation"

kubectl -n platform get svc,endpointslice -o json >"$PLATFORM_SERVICES_OUTPUT" ||
  fail "cannot list platform external services"

python3 - "$PLATFORM_SERVICES_OUTPUT" <<'PY' || exit 1
import json
import sys


def check(items):
    # Frontend, backend, name and protocol are separate route contracts.
    expected = {
        "valkey-external": {("tcp-valkey", 6379, 26379, "TCP")},
        "loki-external": {("http", 3100, 3100, "TCP")},
        "tempo-external": {("http", 3200, 3200, "TCP")},
        "alloy-external": {
            ("grpc-otlp", 4317, 4317, "TCP"),
            ("http-otlp", 4318, 4318, "TCP"),
        },
    }
    services = {}
    slices = {name: [] for name in expected}
    for item in items:
        kind = item["kind"]
        metadata = item["metadata"]
        if kind == "Service" and metadata["name"] in expected:
            name = metadata["name"]
            if name in services:
                raise ValueError(f"duplicate {name} Service")
            services[name] = item["spec"]
        elif kind == "EndpointSlice":
            name = metadata.get("labels", {}).get("kubernetes.io/service-name")
            if name in slices:
                slices[name].append(item)

    for name, routes in expected.items():
        if name not in services:
            raise ValueError(f"missing {name}")
        service = services[name]
        if service.get("type", "ClusterIP") != "ClusterIP":
            raise ValueError(f"{name} Service type mismatch")
        if service.get("clusterIP") == "None":
            raise ValueError(f"{name} headless Service cannot provide the declared ClusterIP route")
        if service.get("selector"):
            raise ValueError(f"{name} Service must be selectorless")
        ports = service["ports"]
        actual = {
            (port.get("name"), port["port"], port.get("targetPort", port["port"]), port.get("protocol", "TCP"))
            for port in ports
        }
        if len(actual) != len(ports) or actual != routes:
            if name == "valkey-external" and any(port[2] != 26379 for port in actual):
                raise ValueError("valkey Service targetPort mismatch")
            raise ValueError(f"{name} Service port contract mismatch")
        if not slices[name]:
            raise ValueError(f"missing {name} EndpointSlice")
        backends = {(port, backend, protocol) for port, _, backend, protocol in routes}
        covered = set()
        for slice_item in slices[name]:
            if slice_item.get("addressType") != "IPv4":
                raise ValueError(f"{name} EndpointSlice address type mismatch")
            slice_ports = slice_item.get("ports", [])
            actual_ports = {
                (port.get("name"), port["port"], port.get("protocol", "TCP"))
                for port in slice_ports
            }
            if not actual_ports or len(actual_ports) != len(slice_ports) or not actual_ports <= backends:
                raise ValueError(f"{name} EndpointSlice port mismatch")
            endpoints = slice_item.get("endpoints", [])
            if not endpoints or any(
                not endpoint.get("addresses")
                or any(address != "192.168.0.13" for address in endpoint["addresses"])
                or (endpoint.get("conditions") or {}).get("ready") is False
                for endpoint in endpoints
            ):
                raise ValueError(f"{name} EndpointSlice address or readiness mismatch")
            covered.update(actual_ports)
        if covered != backends:
            raise ValueError(f"{name} EndpointSlice backend coverage mismatch")


try:
    with open(sys.argv[1], encoding="utf-8") as stream:
        check(json.load(stream)["items"])
except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
    message = str(error) if isinstance(error, ValueError) else "invalid platform service list"
    print(f"[FAIL] {message}", file=sys.stderr)
    sys.exit(1)
PY

echo "[PASS] external service contract checks passed"
