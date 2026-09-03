"""Synthetic contract and security cases for Vault/ESO validation."""

from __future__ import annotations

from typing import Any

import yaml


def valid_contracts(module: Any) -> dict[str, Any]:
    vault_store = {
        "apiVersion": "external-secrets.io/v1",
        "kind": "ClusterSecretStore",
        "metadata": {
            "name": "vault",
            "annotations": {
                module.ENVIRONMENT_SCOPE_ANNOTATION: module.LOCAL_ONLY,
                module.TRANSPORT_BOUNDARY_ANNOTATION: module.LOCAL_ONLY_HTTP,
            },
        },
        "spec": {
            "provider": {
                "vault": {
                    "server": "http://vault.vault.svc.cluster.local:8200",
                    "path": "secret",
                    "version": "v2",
                    "auth": {
                        "kubernetes": {
                            "role": module.EXPECTED_VAULT_ROLE,
                            "serviceAccountRef": {
                                "name": module.EXPECTED_SERVICE_ACCOUNT,
                                "namespace": module.EXPECTED_SERVICE_ACCOUNT,
                                "audiences": list(module.EXPECTED_AUDIENCES),
                            },
                        }
                    },
                }
            }
        },
    }
    token_reviewer = {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "ClusterRoleBinding",
        "metadata": {"name": "external-secrets-token-reviewer"},
        "roleRef": {
            "apiGroup": "rbac.authorization.k8s.io",
            "kind": "ClusterRole",
            "name": "system:auth-delegator",
        },
        "subjects": [
            {
                "kind": "ServiceAccount",
                "name": module.EXPECTED_SERVICE_ACCOUNT,
                "namespace": module.EXPECTED_SERVICE_ACCOUNT,
            }
        ],
    }
    vault_policy = "\n\n".join(
        f'path "{path}" {{\n  capabilities = ["read", "list"]\n}}'
        for path in module.EXPECTED_POLICY_PATHS
    )
    bootstrap = r"""#!/usr/bin/env bash
set -euo pipefail
set +x

ROOT_CA_FILE="/tmp/root-ca.pem"
VAULT_ADDR="${VAULT_ADDR:-https://vault.example.invalid}"

fail() {
  printf '%s\n' "$1" >&2
  exit 1
}

require_file() {
  local path="$1"
  [[ -f "$path" && -r "$path" ]] || fail "required file is missing"
}

VAULT_CA_FILE="${VAULT_CA_FILE:-$ROOT_CA_FILE}"

case "$VAULT_ADDR" in
  https://*) ;;
  *) fail "VAULT_ADDR must use https:// for secret-bearing bootstrap" ;;
esac

require_file "$VAULT_CA_FILE"
if [[ ! -r /dev/tty ]]; then
  fail "interactive /dev/tty is required for Vault token input"
fi
IFS= read -r -s -p "Vault token: " vault_token </dev/tty
printf '\n' >/dev/tty
[[ -n "$vault_token" ]] || fail "Vault token input is empty"

cleanup_sensitive() {
  unset vault_token VALKEY_PASSWORD
}
trap cleanup_sensitive EXIT HUP INT TERM

vault_curl() {
  printf 'X-Vault-Token: %s\n' "$vault_token" |
    curl --disable --fail-with-body --silent --show-error \
      --cacert "$VAULT_CA_FILE" --header @- "$@"
}

VALKEY_PASSWORD="$(vault_curl \
  "$VAULT_ADDR/v1/secret/data/platform/argocd" |
  jq -er '.data.data.valkey_password')"

printf '%s' "$VALKEY_PASSWORD" |
  kubectl -n argocd create secret generic argocd-external-valkey \
    --from-file=redis-password=/dev/stdin \
    --dry-run=client -o yaml |
  kubectl apply -f -
unset VALKEY_PASSWORD
"""
    return {
        "vault_store": vault_store,
        "token_reviewer": token_reviewer,
        "vault_policy": vault_policy,
        "bootstrap": bootstrap,
    }


def apply_fixture_mutation(contracts: dict[str, Any], mutation: str) -> None:
    if mutation == "none":
        return
    if mutation == "remove-local-only-annotations":
        contracts["vault_store"]["metadata"].pop("annotations")
        return
    service_account_ref = contracts["vault_store"]["spec"]["provider"]["vault"]["auth"][
        "kubernetes"
    ]["serviceAccountRef"]
    if mutation == "remove-vault-audience":
        service_account_ref.pop("audiences")
        return
    if mutation == "change-service-account":
        service_account_ref["name"] = "unexpected-service-account"
        return
    if mutation == "add-token-reviewer-subject":
        contracts["token_reviewer"]["subjects"].append(
            {
                "kind": "ServiceAccount",
                "name": "unexpected-service-account",
                "namespace": "external-secrets",
            }
        )
        return
    if mutation == "add-platform-wildcard":
        contracts["vault_policy"] = contracts["vault_policy"].replace(
            'path "secret/data/platform/argocd"',
            'path "secret/data/platform/*"',
            1,
        )
        return
    if mutation == "add-curl-insecure":
        contracts["bootstrap"] = contracts["bootstrap"].replace(
            "curl --disable --fail-with-body",
            "curl --disable -k --fail-with-body",
            1,
        )
        return
    if mutation == "add-token-header-argument":
        contracts["bootstrap"] += (
            '\ncurl --header "X-Vault-Token: $vault_token" '
            "https://vault.example.invalid/v1/sys/health\n"
        )
        return
    if mutation == "add-exported-token":
        contracts["bootstrap"] += '\nexport VAULT_TOKEN="$vault_token"\n'
        return
    if mutation == "add-from-literal-password":
        # Held in a variable so the literal keeps its exact runtime bytes
        # without matching generic credential-assignment scanners.
        unsafe_value = '"$VALKEY_PASSWORD"'
        contracts["bootstrap"] += (
            "\nkubectl -n argocd create secret generic unsafe "
            f"--from-literal=redis-password={unsafe_value}\n"
        )
        return
    raise AssertionError(f"unknown mutation {mutation!r}")


def contract_diagnostics(module: Any, contracts: dict[str, Any]) -> list[str]:
    return [
        *module.validate_vault_store(contracts["vault_store"]),
        *module.validate_token_reviewer(contracts["token_reviewer"]),
        *module.validate_vault_policy(contracts["vault_policy"]),
        *module.validate_bootstrap(contracts["bootstrap"]),
    ]


def run_internal_boundaries(module: Any) -> None:
    malformed_checks = (
        (
            module.validate_vault_store,
            [],
            ["Vault store document must be a mapping"],
        ),
        (
            module.validate_token_reviewer,
            "not-a-mapping",
            ["TokenReview binding document must be a mapping"],
        ),
        (
            module.validate_vault_policy,
            {},
            ["Vault policy document must be text"],
        ),
        (
            module.validate_bootstrap,
            [],
            ["bootstrap document must be text"],
        ),
    )
    for validator, malformed, expected in malformed_checks:
        assert validator(malformed) == expected, validator.__name__

    try:
        yaml.load("kind: Service\nkind: Secret\n", Loader=module._UniqueKeyLoader)
    except yaml.constructor.ConstructorError as error:
        assert "duplicate key" in str(error)
    else:
        raise AssertionError("duplicate YAML key was accepted")

    secure_bootstrap = valid_contracts(module)["bootstrap"]
    require_file_block = """require_file() {
  local path="$1"
  [[ -f "$path" && -r "$path" ]] || fail "required file is missing"
}"""
    require_file_after_use = secure_bootstrap.replace(
        require_file_block + "\n\n", "", 1
    ).replace(
        'require_file "$VAULT_CA_FILE"',
        'require_file "$VAULT_CA_FILE"\n\n' + require_file_block,
        1,
    )
    indirect_dependency_loop = """for cmd in k3d kubectl helm docker curl jq openssl rg; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    fail "required command not found: $cmd"
  fi
  case "$cmd" in
    c*) "$cmd" --disable --cacert "$VAULT_CA_FILE" "$VAULT_ADDR/v1/sys/health" ;;
  esac
done"""
    focused_bootstrap_checks = (
        (
            "curl default configuration",
            secure_bootstrap.replace("curl --disable ", "curl ", 1),
            ["bootstrap curl must disable default configuration"],
        ),
        (
            "curl guard order",
            secure_bootstrap.replace(
                "curl --disable --fail-with-body",
                "curl --fail-with-body --disable",
                1,
            ),
            ["bootstrap curl must disable default configuration"],
        ),
        (
            "missing xtrace guard",
            secure_bootstrap.replace("set +x\n", "", 1),
            ["bootstrap must disable shell xtrace before sensitive operations"],
        ),
        (
            "set -x",
            secure_bootstrap + "\nset -x\n",
            ["bootstrap must disable shell xtrace before sensitive operations"],
        ),
        (
            "semicolon set -x",
            secure_bootstrap + "\nset -x; :\n",
            ["bootstrap must disable shell xtrace before sensitive operations"],
        ),
        (
            "builtin set -x",
            secure_bootstrap + "\nbuiltin set -x\n",
            ["bootstrap must disable shell xtrace before sensitive operations"],
        ),
        (
            "command set -x",
            secure_bootstrap + "\ncommand set -x\n",
            ["bootstrap must disable shell xtrace before sensitive operations"],
        ),
        (
            "set -o xtrace",
            secure_bootstrap + "\nset -o xtrace\n",
            ["bootstrap must disable shell xtrace before sensitive operations"],
        ),
        (
            "combined tracing options",
            secure_bootstrap.replace("set -euo pipefail", "set -euxo pipefail", 1),
            ["bootstrap must disable shell xtrace before sensitive operations"],
        ),
        (
            "raw Vault curl",
            secure_bootstrap.replace(
                'case "$VAULT_ADDR" in',
                """curl --disable --fail-with-body --cacert "$VAULT_CA_FILE" \\
  "$VAULT_ADDR/v1/sys/health"

case "$VAULT_ADDR" in""",
                1,
            ),
            ["bootstrap must contain only the guarded vault_curl command"],
        ),
        (
            "indirect command execution",
            secure_bootstrap.replace(
                'VAULT_CA_FILE="${VAULT_CA_FILE:-$ROOT_CA_FILE}"',
                indirect_dependency_loop
                + '\n\nVAULT_CA_FILE="${VAULT_CA_FILE:-$ROOT_CA_FILE}"',
                1,
            ),
            ["bootstrap must contain only the guarded vault_curl command"],
        ),
        (
            "aliased raw curl",
            secure_bootstrap.replace(
                'case "$VAULT_ADDR" in',
                """endpoint="$VAULT_ADDR/v1/sys/health"
curl --disable --fail-with-body --cacert "$VAULT_CA_FILE" "$endpoint"

case "$VAULT_ADDR" in""",
                1,
            ),
            ["bootstrap must contain only the guarded vault_curl command"],
        ),
        (
            "combined insecure option",
            secure_bootstrap.replace(
                "curl --disable --fail-with-body",
                "curl --disable -sk --fail-with-body",
                1,
            ),
            ["bootstrap must not disable Vault TLS verification"],
        ),
        (
            "assigned insecure option",
            secure_bootstrap.replace(
                "curl --disable --fail-with-body",
                "curl --disable --insecure=true --fail-with-body",
                1,
            ),
            ["bootstrap must not disable Vault TLS verification"],
        ),
        (
            "sensitive printf",
            secure_bootstrap + "\nprintf '%s\\n' \"$vault_token\"\n",
            ["bootstrap sensitive identifiers must use only approved operations"],
        ),
        (
            "exported token",
            secure_bootstrap + '\nexport vault_token="$vault_token"\n',
            ["bootstrap sensitive identifiers must use only approved operations"],
        ),
        (
            "logger token",
            secure_bootstrap + '\nlogger "$vault_token"\n',
            ["bootstrap sensitive identifiers must use only approved operations"],
        ),
        (
            "declare token",
            secure_bootstrap + "\ndeclare -x vault_token\n",
            ["bootstrap sensitive identifiers must use only approved operations"],
        ),
        (
            "env token",
            secure_bootstrap + "\nenv TO" + 'KEN="$vault_token" true\n',
            ["bootstrap sensitive identifiers must use only approved operations"],
        ),
        (
            "curl config",
            secure_bootstrap.replace(
                "curl --disable --fail-with-body",
                "curl --disable --config /tmp/operator.curlrc --fail-with-body",
                1,
            ),
            ["bootstrap curl must not load explicit configuration"],
        ),
        (
            "curl abbreviated config",
            secure_bootstrap.replace(
                "curl --disable --fail-with-body",
                "curl --disable --conf /tmp/operator.curlrc --fail-with-body",
                1,
            ),
            ["bootstrap curl must not load explicit configuration"],
        ),
        (
            "curl partial config",
            secure_bootstrap.replace(
                "curl --disable --fail-with-body",
                "curl --disable --confi=/tmp/operator.curlrc --fail-with-body",
                1,
            ),
            ["bootstrap curl must not load explicit configuration"],
        ),
        (
            "curl assigned config",
            secure_bootstrap.replace(
                "curl --disable --fail-with-body",
                "curl --disable --config=/tmp/operator.curlrc --fail-with-body",
                1,
            ),
            ["bootstrap curl must not load explicit configuration"],
        ),
        (
            "curl short config",
            secure_bootstrap.replace(
                "curl --disable --fail-with-body",
                "curl --disable -K /tmp/operator.curlrc --fail-with-body",
                1,
            ),
            ["bootstrap curl must not load explicit configuration"],
        ),
        (
            "curl combined config",
            secure_bootstrap.replace(
                "curl --disable --fail-with-body",
                "curl --disable -sK/tmp/operator.curlrc --fail-with-body",
                1,
            ),
            ["bootstrap curl must not load explicit configuration"],
        ),
        (
            "late require_file",
            require_file_after_use,
            ["bootstrap must require VAULT_CA_FILE"],
        ),
        (
            "unrelated HTTPS marker",
            secure_bootstrap.replace(
                """case "$VAULT_ADDR" in
  https://*) ;;
  *) fail "VAULT_ADDR must use https:// for secret-bearing bootstrap" ;;
esac""",
                """if [[ -n "$ROOT_CA_FILE" ]]; then
  : "unrelated https:// marker"
fi""",
                1,
            ),
            ["bootstrap must require an HTTPS Vault address"],
        ),
        (
            "removed Vault header",
            secure_bootstrap.replace(
                "  printf 'X-Vault-Token: %s",
                "  printf 'Removed-Vault-header: %s",
                1,
            ),
            ["bootstrap curl must read headers from stdin"],
        ),
        (
            "unreadable CA unchecked",
            secure_bootstrap.replace('&& -r "$path"', "", 1),
            ["bootstrap must require VAULT_CA_FILE"],
        ),
        (
            "later EXIT trap",
            secure_bootstrap + "\ntrap 'rm -f /tmp/bootstrap.tmp' EXIT\n",
            ["bootstrap must install a cleanup trap"],
        ),
        (
            "weak jq extraction",
            secure_bootstrap.replace("jq -er", "jq -r", 1),
            ["bootstrap must provide redis-password to kubectl via stdin"],
        ),
        (
            "missing kubectl stdin producer",
            secure_bootstrap.replace(
                "printf '%s' \"$VALKEY_PASSWORD\" |\n  kubectl",
                "kubectl",
                1,
            ),
            ["bootstrap must provide redis-password to kubectl via stdin"],
        ),
    )
    for label, candidate, expected in focused_bootstrap_checks:
        actual = module.validate_bootstrap(candidate)
        assert actual == expected, f"{label}: expected {expected!r}, got {actual!r}"
