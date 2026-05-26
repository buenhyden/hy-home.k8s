#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
POLICY_DIR="$ROOT_DIR/policy/conftest"

if [[ ! -d "$POLICY_DIR" ]]; then
  echo "ERR policy directory missing: $POLICY_DIR" >&2
  exit 1
fi

mapfile -d '' POLICY_TARGETS < <(
  find \
    "$ROOT_DIR/gitops" \
    "$ROOT_DIR/infrastructure" \
    "$ROOT_DIR/examples" \
    "$ROOT_DIR/traefik" \
    -type f \( -name '*.yaml' -o -name '*.yml' \) -print0
)

if ((${#POLICY_TARGETS[@]} == 0)); then
  echo "ERR no policy target YAML files found" >&2
  exit 1
fi

if command -v conftest >/dev/null 2>&1; then
  conftest test --policy "$POLICY_DIR" "${POLICY_TARGETS[@]}"
else
  echo "SKIP optional conftest not installed — running built-in policy fallback"
fi

python3 - "$ROOT_DIR" "${POLICY_TARGETS[@]}" <<'PY'
import pathlib
import sys

import yaml

root = pathlib.Path(sys.argv[1]).resolve()
paths = [pathlib.Path(value) for value in sys.argv[2:]]
failures = []


def rel(path: pathlib.Path) -> str:
    return str(path.resolve().relative_to(root))


def sync_options(document: dict, application_set: bool = False) -> list[str]:
    if application_set:
        spec = (((document.get("spec") or {}).get("template") or {}).get("spec")) or {}
    else:
        spec = document.get("spec") or {}
    options = ((spec.get("syncPolicy") or {}).get("syncOptions")) or []
    return [value for value in options if isinstance(value, str)]


def walk_containers(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"containers", "initContainers"} and isinstance(child, list):
                for item in child:
                    if isinstance(item, dict) and isinstance(item.get("image"), str):
                        yield item["image"]
            else:
                yield from walk_containers(child)
    elif isinstance(value, list):
        for item in value:
            yield from walk_containers(item)


for path in paths:
    with path.open(encoding="utf-8") as fh:
        documents = list(yaml.safe_load_all(fh))
    for index, document in enumerate(documents, start=1):
        if not isinstance(document, dict):
            continue
        kind = document.get("kind")
        name = ((document.get("metadata") or {}).get("name")) or "<unknown>"
        location = f"{rel(path)}#{index}"

        if document.get("apiVersion") == "v1" and kind == "Secret":
            failures.append(f"{location}: plaintext Kubernetes Secret manifest is not allowed: {name}")

        if kind == "Application" and "CreateNamespace=true" in sync_options(document):
            failures.append(f"{location}: Application must not use CreateNamespace=true: {name}")

        if kind == "ApplicationSet" and "CreateNamespace=true" in sync_options(document, application_set=True):
            failures.append(f"{location}: ApplicationSet must not use CreateNamespace=true: {name}")

        if kind == "AppProject":
            spec = document.get("spec") or {}
            for surface in ["clusterResourceWhitelist", "namespaceResourceWhitelist"]:
                for item in spec.get(surface, []) or []:
                    if not isinstance(item, dict):
                        continue
                    if item.get("group") == "*" or item.get("kind") == "*":
                        failures.append(f"{location}: AppProject wildcard {surface} is not allowed: {name}")

        for image in walk_containers(document):
            if image.endswith(":latest"):
                failures.append(f"{location}: container image must not use latest tag: {name} uses {image}")

if failures:
    print("[FAIL] policy gate violations:")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("[PASS] built-in policy fallback passed")
PY
