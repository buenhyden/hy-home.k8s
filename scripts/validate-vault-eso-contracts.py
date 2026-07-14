"""Validate the Vault External Secrets Operator store contract."""

from __future__ import annotations

import argparse
import copy
import json
import os
import stat
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

import yaml


EXPECTED_KIND = "ClusterSecretStore"
ENVIRONMENT_SCOPE_ANNOTATION = "platform.hyhome.io/environment-scope"
TRANSPORT_BOUNDARY_ANNOTATION = "platform.hyhome.io/transport-boundary"
LOCAL_ONLY = "local-only"
LOCAL_ONLY_HTTP = "local-only-http"
EXPECTED_VAULT_ROLE = "eso-read-platform"
EXPECTED_SERVICE_ACCOUNT = "external-secrets"
EXPECTED_AUDIENCES = ["vault"]

VAULT_STORE_PATH = Path("gitops/platform/eso/vault-secret-store.yaml")
TOKEN_REVIEWER_PATH = Path(
    "gitops/platform/eso/vault-token-reviewer-binding.yaml"
)
VAULT_EXTERNAL_PATH = Path(
    "gitops/platform/external-services/vault-external.yaml"
)
VAULT_POLICY_PATH = Path("infrastructure/vault/policies/eso-read.hcl")
BOOTSTRAP_PATH = Path("infrastructure/bootstrap-local.sh")

HTTP_ANNOTATION_ERROR = "HTTP Vault transport requires local-only annotations"
AUDIENCES_ERROR = "Vault serviceAccountRef audiences must equal ['vault']"
IDENTITY_ERROR = "Vault identity must be external-secrets/external-secrets"
EXTERNAL_CONTRACT_ERROR = (
    "Vault external manifest must contain exactly one Service and one "
    "EndpointSlice with exact local-only annotations"
)
YAML_PARSE_ERROR = "YAML must parse without duplicate keys"

EXPECTED_POLICY_PATHS = (
    "secret/data/platform/argocd",
    "secret/metadata/platform/argocd",
    "secret/data/platform/postgres-app",
    "secret/metadata/platform/postgres-app",
    "secret/data/platform/notifications",
    "secret/metadata/platform/notifications",
)


class _UniqueKeyLoader(yaml.SafeLoader):
    """Load YAML mappings while rejecting duplicate keys."""


def _construct_unique_mapping(
    loader: _UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as error:
            raise yaml.constructor.ConstructorError(
                None, None, "invalid key", key_node.start_mark
            ) from error
        if duplicate:
            raise yaml.constructor.ConstructorError(
                None, None, "duplicate key", key_node.start_mark
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def validate_vault_store(data: dict) -> list[str]:
    """Return stable diagnostics for violations of the Vault store contract."""
    diagnostics: list[str] = []

    if not isinstance(data, dict):
        return ["Vault store document must be a mapping"]

    if data.get("kind") != EXPECTED_KIND:
        diagnostics.append("Vault store kind must be ClusterSecretStore")

    metadata = data.get("metadata")
    if isinstance(metadata, dict):
        annotations = metadata.get("annotations")
    else:
        diagnostics.append("Vault store metadata must be a mapping")
        annotations = None

    if annotations is not None and not isinstance(annotations, dict):
        diagnostics.append("Vault store annotations must be a mapping")
        annotations = None

    spec = data.get("spec")
    if not isinstance(spec, dict):
        diagnostics.append("Vault store spec must be a mapping")
        return diagnostics

    provider = spec.get("provider")
    if not isinstance(provider, dict):
        diagnostics.append("Vault store provider must be a mapping")
        return diagnostics

    vault = provider.get("vault")
    if not isinstance(vault, dict):
        diagnostics.append("Vault provider configuration must be a mapping")
        return diagnostics

    server = vault.get("server")
    if not isinstance(server, str) or not server:
        diagnostics.append("Vault server must be a non-empty string")
    elif server.startswith("http://"):
        if (
            not isinstance(annotations, dict)
            or annotations.get(ENVIRONMENT_SCOPE_ANNOTATION) != LOCAL_ONLY
            or annotations.get(TRANSPORT_BOUNDARY_ANNOTATION) != LOCAL_ONLY_HTTP
        ):
            diagnostics.append(HTTP_ANNOTATION_ERROR)
    elif server.startswith("https://"):
        if (
            isinstance(annotations, dict)
            and annotations.get(TRANSPORT_BOUNDARY_ANNOTATION) == LOCAL_ONLY_HTTP
        ):
            diagnostics.append(
                "HTTPS Vault transport must not use local-only-http annotation"
            )
    else:
        diagnostics.append("Vault server must use http:// or https://")

    auth = vault.get("auth")
    if not isinstance(auth, dict):
        diagnostics.append("Vault auth must be a mapping")
        return diagnostics

    kubernetes = auth.get("kubernetes")
    if not isinstance(kubernetes, dict):
        diagnostics.append("Vault kubernetes auth must be a mapping")
        return diagnostics

    if kubernetes.get("role") != EXPECTED_VAULT_ROLE:
        diagnostics.append("Vault kubernetes auth role must be eso-read-platform")

    service_account_ref = kubernetes.get("serviceAccountRef")
    if not isinstance(service_account_ref, dict):
        diagnostics.append("Vault serviceAccountRef must be a mapping")
        return diagnostics

    if (
        service_account_ref.get("name") != EXPECTED_SERVICE_ACCOUNT
        or service_account_ref.get("namespace") != EXPECTED_SERVICE_ACCOUNT
    ):
        diagnostics.append(IDENTITY_ERROR)

    if service_account_ref.get("audiences") != EXPECTED_AUDIENCES:
        diagnostics.append(AUDIENCES_ERROR)

    return diagnostics


def validate_token_reviewer(data: dict) -> list[str]:
    """Return stable diagnostics for TokenReview RBAC contract violations."""
    diagnostics: list[str] = []

    if not isinstance(data, dict):
        return ["TokenReview binding document must be a mapping"]

    if data.get("kind") != "ClusterRoleBinding":
        diagnostics.append("TokenReview binding kind must be ClusterRoleBinding")

    expected_role_ref = {
        "apiGroup": "rbac.authorization.k8s.io",
        "kind": "ClusterRole",
        "name": "system:auth-delegator",
    }
    if data.get("roleRef") != expected_role_ref:
        diagnostics.append("TokenReview binding roleRef must be system:auth-delegator")

    subjects = data.get("subjects")
    if not isinstance(subjects, list):
        diagnostics.append("TokenReview binding subjects must be a list")
    elif len(subjects) != 1:
        diagnostics.append("TokenReview binding must contain exactly one subject")
    elif not isinstance(subjects[0], dict):
        diagnostics.append("TokenReview binding subject must be a mapping")
    elif subjects[0] != {
        "kind": "ServiceAccount",
        "name": "external-secrets",
        "namespace": "external-secrets",
    }:
        diagnostics.append(
            "TokenReview binding subject must be the external-secrets ServiceAccount"
        )

    return diagnostics


def validate_vault_external(documents: list[Any]) -> list[str]:
    """Validate the exact local-only Service and EndpointSlice document pair."""
    expected_annotations = {
        ENVIRONMENT_SCOPE_ANNOTATION: LOCAL_ONLY,
        TRANSPORT_BOUNDARY_ANNOTATION: LOCAL_ONLY_HTTP,
    }
    if not isinstance(documents, list) or len(documents) != 2:
        return [EXTERNAL_CONTRACT_ERROR]

    kinds: list[str] = []
    for document in documents:
        if not isinstance(document, dict):
            return [EXTERNAL_CONTRACT_ERROR]
        kind = document.get("kind")
        metadata = document.get("metadata")
        if (
            kind not in {"Service", "EndpointSlice"}
            or not isinstance(metadata, dict)
            or metadata.get("annotations") != expected_annotations
        ):
            return [EXTERNAL_CONTRACT_ERROR]
        kinds.append(kind)

    if sorted(kinds) != ["EndpointSlice", "Service"]:
        return [EXTERNAL_CONTRACT_ERROR]
    return []


def validate_vault_policy(text: str) -> list[str]:
    """Return stable diagnostics for the exact ESO Vault policy allowlist."""
    expected_paths = set(EXPECTED_POLICY_PATHS)
    syntax_error = "Vault policy must contain only valid path stanzas"

    if not isinstance(text, str):
        return ["Vault policy document must be text"]

    length = len(text)
    position = 0

    def skip_ignored(offset: int) -> int:
        while offset < length:
            if text[offset].isspace():
                offset += 1
                continue
            if text.startswith("#", offset) or text.startswith("//", offset):
                newline = text.find("\n", offset)
                if newline == -1:
                    return length
                offset = newline + 1
                continue
            if text.startswith("/*", offset):
                comment_end = text.find("*/", offset + 2)
                if comment_end == -1:
                    raise ValueError
                offset = comment_end + 2
                continue
            break
        return offset

    def consume_literal(offset: int, literal: str) -> int:
        if not text.startswith(literal, offset):
            raise ValueError
        end = offset + len(literal)
        if end < length and (text[end].isalnum() or text[end] in "_-"):
            raise ValueError
        return end

    def consume_character(offset: int, character: str) -> int:
        offset = skip_ignored(offset)
        if offset >= length or text[offset] != character:
            raise ValueError
        return offset + 1

    def consume_string(offset: int) -> tuple[str, int]:
        offset = skip_ignored(offset)
        if offset >= length or text[offset] != '"':
            raise ValueError

        end = offset + 1
        while end < length:
            character = text[end]
            if character == "\\":
                end += 2
                continue
            if character == '"':
                token = text[offset : end + 1]
                try:
                    value = json.loads(token)
                except (json.JSONDecodeError, TypeError) as error:
                    raise ValueError from error
                if not isinstance(value, str):
                    raise ValueError
                return value, end + 1
            if character in "\r\n":
                raise ValueError
            end += 1
        raise ValueError

    parsed_stanzas: list[tuple[str, list[str]]] = []
    try:
        position = skip_ignored(position)
        while position < length:
            position = consume_literal(position, "path")
            path, position = consume_string(position)
            position = consume_character(position, "{")
            position = skip_ignored(position)
            position = consume_literal(position, "capabilities")
            position = consume_character(position, "=")
            position = consume_character(position, "[")

            capabilities: list[str] = []
            position = skip_ignored(position)
            if position >= length or text[position] == "]":
                raise ValueError
            while True:
                capability, position = consume_string(position)
                capabilities.append(capability)
                position = skip_ignored(position)
                if position < length and text[position] == "]":
                    position += 1
                    break
                position = consume_character(position, ",")
                position = skip_ignored(position)
                if position < length and text[position] == "]":
                    position += 1
                    break

            position = consume_character(position, "}")
            parsed_stanzas.append((path, capabilities))
            position = skip_ignored(position)
    except ValueError:
        return [syntax_error]

    parsed_paths = [path for path, _ in parsed_stanzas]
    diagnostics: list[str] = []
    has_wildcard = any("*" in path or "+" in path for path in parsed_paths)
    if has_wildcard:
        diagnostics.append("Vault policy must not contain wildcard platform paths")

    if len(parsed_paths) != len(set(parsed_paths)):
        diagnostics.append("Vault policy must not contain duplicate path stanzas")

    parsed_path_set = set(parsed_paths)
    if not has_wildcard:
        if expected_paths - parsed_path_set:
            diagnostics.append("Vault policy is missing required platform paths")
        if parsed_path_set - expected_paths:
            diagnostics.append("Vault policy must not contain additional platform paths")

    if any(
        len(capabilities) != 2 or set(capabilities) != {"read", "list"}
        for _, capabilities in parsed_stanzas
    ):
        diagnostics.append("Vault policy capabilities must equal read and list")

    return diagnostics


def validate_bootstrap(text: str) -> list[str]:
    """Return stable diagnostics for the secure Vault bootstrap shell contract."""
    import re

    if not isinstance(text, str):
        return ["bootstrap document must be text"]

    active_lines = [
        line for line in text.splitlines() if not re.match(r"^\s*#", line)
    ]
    active_text = "\n".join(active_lines)
    command_text = re.sub(r"\\\s*\n", " ", active_text)
    pipeline_text = re.sub(r"\|\s*\n\s*", "| ", command_text)
    diagnostics: list[str] = []

    vault_curl_function = re.search(
        r'''(?ms)^\s*vault_curl\(\)\s*\{\s*$\n'''
        r'''(?P<body>.*?)^\s*\}\s*$''',
        active_text,
    )
    vault_curl_body_raw = (
        vault_curl_function.group("body") if vault_curl_function else ""
    )
    vault_curl_body = re.sub(r"\\\s*\n", " ", vault_curl_body_raw)

    dependency_discovery_block = '''for cmd in k3d kubectl helm docker curl jq openssl rg; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    fail "required command not found: $cmd"
  fi
done'''
    dependency_loop_neutral_text = active_text
    if active_text.count(dependency_discovery_block) == 1:
        dependency_loop_neutral_text = active_text.replace(
            dependency_discovery_block, "", 1
        )
    curl_token_count = len(
        re.findall(r"\bcurl\b", dependency_loop_neutral_text)
    )
    wrapper_curl_token_count = len(re.findall(r"\bcurl\b", vault_curl_body_raw))
    curl_structure_valid = (
        curl_token_count == 1 and wrapper_curl_token_count == 1
    )

    vault_call_positions = [
        match.start()
        for match in re.finditer(r"\bvault_curl\b(?!\s*\(\))", active_text)
    ]
    first_vault_call = min(vault_call_positions, default=len(active_text))

    xtrace_guard = re.search(r"(?m)^\s*set\s+\+x\s*$", active_text)
    initial_xtrace_guard = re.search(
        r"\A[ \t]*set[ \t]+-euo[ \t]+pipefail[ \t]*\n"
        r"[ \t]*set[ \t]+\+x[ \t]*(?:\n|$)",
        active_text,
    )
    xtrace_reenable = re.search(
        r"(?m)^\s*(?:(?:builtin|command)\s+)?set\s+"
        r"(?:-[A-Za-z]*x[A-Za-z]*"
        r"|-o\s+xtrace)(?=[\s;&|]|$)",
        active_text,
    )
    sensitive_positions = [
        match.start()
        for match in re.finditer(r"\b(?:vault_token|VALKEY_PASSWORD)\b", active_text)
    ]
    first_sensitive_use = min(sensitive_positions, default=len(active_text))
    if (
        xtrace_guard is None
        or initial_xtrace_guard is None
        or xtrace_guard.start() >= min(first_sensitive_use, first_vault_call)
        or xtrace_reenable is not None
    ):
        diagnostics.append(
            "bootstrap must disable shell xtrace before sensitive operations"
        )

    insecure_curl = re.search(
        r"(?m)\bcurl\b[^\n]*(?<!\S)"
        r"(?:-[A-Za-z]*k[A-Za-z]*|--insecure(?:=[^\s]+)?)(?=\s|$)",
        command_text,
    )
    if re.search(r"\bVAULT_SKIP_VERIFY\b", active_text) or insecure_curl:
        diagnostics.append("bootstrap must not disable Vault TLS verification")

    token_in_argv = re.search(
        r'''(?m)\b(?:curl|vault_curl)\b[^\n]*(?:-H|--header)(?:=|\s+)'''
        r'''["']?X-Vault-Token\s*:[^\n"']*'''
        r'''(?:\$(?:vault_token|VAULT_TOKEN)|\$\{(?:vault_token|VAULT_TOKEN)\})''',
        command_text,
    )
    if not curl_structure_valid and not token_in_argv:
        diagnostics.append(
            "bootstrap must contain only the guarded vault_curl command"
        )

    if token_in_argv:
        diagnostics.append("bootstrap must not place Vault token in argv")

    explicit_curl_config = re.search(
        r"(?m)\b(?:curl|vault_curl)\b[^\n]*(?<!\S)"
        r"(?:--conf(?:i(?:g)?)?(?:=|\s)|-[A-Za-z]*K[^\s]*)",
        command_text,
    )
    if explicit_curl_config:
        diagnostics.append("bootstrap curl must not load explicit configuration")

    vault_token_environment_input = re.search(r"\bVAULT_TOKEN\b", active_text)
    if vault_token_environment_input:
        diagnostics.append(
            "bootstrap must not accept or export Vault token environment input"
        )

    secret_in_kubectl_argv = re.search(
        r"(?m)\bkubectl\b[^\n]*--from-literal=redis-password="
        r'''[^\n]*(?:\$VALKEY_PASSWORD|\$\{VALKEY_PASSWORD\})''',
        command_text,
    )
    if secret_in_kubectl_argv:
        diagnostics.append(
            "bootstrap must not place generated secret values in kubectl argv"
        )

    https_guard = re.search(
        r'''(?m)^\s*case\s+"\$VAULT_ADDR"\s+in\s*$\n'''
        r'''^\s*https://\*\)\s*;;\s*$\n'''
        r'''^\s*\*\)\s*fail\b[^\n]*;;\s*$\n'''
        r'''^\s*esac\s*$''',
        active_text,
    )
    if https_guard is None or https_guard.start() > first_vault_call:
        diagnostics.append("bootstrap must require an HTTPS Vault address")

    ca_assignment = re.search(
        r'''(?m)^\s*VAULT_CA_FILE="\$\{VAULT_CA_FILE:-\$ROOT_CA_FILE\}"\s*$''',
        active_text,
    )
    ca_requirement = re.search(
        r'''(?m)^\s*require_file\s+"\$VAULT_CA_FILE"\s*$''', active_text
    )
    require_file_function = re.search(
        r'''(?ms)^\s*require_file\(\)\s*\{\s*$\n'''
        r'''(?P<body>.*?)^\s*\}\s*$''',
        active_text,
    )
    require_file_body = (
        require_file_function.group("body") if require_file_function else ""
    )
    if (
        ca_assignment is None
        or ca_requirement is None
        or require_file_function is None
        or require_file_function.start() > ca_requirement.start()
        or ca_assignment.start() > first_vault_call
        or ca_requirement.start() > first_vault_call
        or not re.search(r'''-r\s+"\$(?:path|1)"''', require_file_body)
    ):
        diagnostics.append("bootstrap must require VAULT_CA_FILE")

    tty_read = re.search(
        r'''(?m)^\s*IFS=\s+read\s+-r\s+-s\s+-p\s+'''
        r'''["'][^"']*["']\s+vault_token\s*</dev/tty\s*$''',
        active_text,
    )
    nonempty_token_guard = re.search(
        r'''(?m)^\s*\[\[\s+-n\s+"\$vault_token"\s+\]\]\s+\|\|\s+fail\b''',
        active_text,
    )
    tty_readability_guard = re.search(
        r'''(?m)^\s*if\s+\[\[\s+!\s+-r\s+/dev/tty\s+\]\];\s+then\s*$''',
        active_text,
    )
    has_silent_tty_read = bool(
        tty_read
        and nonempty_token_guard
        and tty_readability_guard
        and max(
            tty_read.start(),
            nonempty_token_guard.start(),
            tty_readability_guard.start(),
        )
        < first_vault_call
    )
    if not has_silent_tty_read:
        diagnostics.append("bootstrap must read the Vault token silently from /dev/tty")

    cleanup_function = re.search(
        r'''(?ms)^\s*cleanup_sensitive\(\)\s*\{\s*$\n'''
        r'''(?P<body>.*?)^\s*\}\s*$''',
        active_text,
    )
    cleanup_body = cleanup_function.group("body") if cleanup_function else ""
    trap_matches = list(re.finditer(r"(?m)^\s*trap\s+[^\n]+$", active_text))
    trap_lines = [match.group(0) for match in trap_matches]
    has_full_cleanup_trap = any(
        "cleanup_sensitive" in match.group(0)
        and all(
            signal in match.group(0).split()
            for signal in ("EXIT", "HUP", "INT", "TERM")
        )
        and match.start() < first_vault_call
        for match in trap_matches
    )
    exit_traps_preserve_cleanup = all(
        "cleanup_sensitive" in line
        for line in trap_lines
        if re.search(r"(?:^|\s)(?:EXIT|0)(?:\s|$)", line)
    )
    has_cleanup_contract = bool(
        cleanup_function is not None
        and re.search(r"\bunset\b[^\n]*\bvault_token\b", cleanup_body)
        and re.search(r"\bunset\b[^\n]*\bVALKEY_PASSWORD\b", cleanup_body)
        and has_full_cleanup_trap
        and exit_traps_preserve_cleanup
    )
    if not has_cleanup_contract:
        diagnostics.append("bootstrap must install a cleanup trap")

    if not insecure_curl and not re.search(
        r'''\bcurl\s+--disable(?:\s|$)''', vault_curl_body
    ):
        diagnostics.append("bootstrap curl must disable default configuration")
    if not re.search(
        r'''\bcurl\b[^\n]*--cacert\s+"\$VAULT_CA_FILE"''',
        vault_curl_body,
    ):
        diagnostics.append("bootstrap curl must use --cacert")

    has_header_pipe = bool(
        re.search(
            r'''printf\s+['"]X-Vault-Token:\s*%s\\n['"]\s+'''
            r'''"\$vault_token"\s*\|\s*curl\b''',
            vault_curl_body,
        )
        and re.search(r'''\bcurl\b[^\n]*--header\s+@-''', vault_curl_body)
        and '"$@"' in vault_curl_body
        and not re.search(
            r'''\bvault_curl\b(?!\s*\(\))[^\n]*(?:-H|--header)''',
            command_text,
        )
    )
    if not has_header_pipe:
        diagnostics.append("bootstrap curl must read headers from stdin")

    has_direct_secret_extraction = bool(
        "vault_secret_json" not in active_text
        and re.search(
            r'''VALKEY_PASSWORD="\$\(\s*vault_curl\s+'''
            r'''"\$VAULT_ADDR/v1/secret/data/platform/argocd"\s*\|\s*'''
            r'''jq\s+-er\s+['"]\.data\.data\.valkey_password['"]\s*\)"''',
            command_text,
        )
    )
    has_kubectl_stdin_pipe = bool(
        re.search(
            r'''printf\s+['"]%s['"]\s+"\$VALKEY_PASSWORD"\s*\|\s*'''
            r'''kubectl\b[\s\S]*?--from-file=redis-password=/dev/stdin''',
            command_text,
        )
    )
    if not has_direct_secret_extraction or not has_kubectl_stdin_pipe:
        diagnostics.append("bootstrap must provide redis-password to kubectl via stdin")

    sensitive_allowlist_patterns = (
        r'''(?m)^\s*IFS=\s+read\s+-r\s+-s\s+-p\s+'''
        r'''["'][^"']*["']\s+vault_token\s*</dev/tty\s*$''',
        r'''(?m)^\s*\[\[\s+-n\s+"\$vault_token"\s+\]\]\s+'''
        r'''\|\|\s+fail\b[^\n]*$''',
        r'''(?m)^\s*unset\s+vault_token\s+VALKEY_PASSWORD\s*$''',
        r'''(?m)^\s*printf\s+['"]X-Vault-Token:\s*%s\\n['"]\s+'''
        r'''"\$vault_token"\s*\|\s*curl\b[^\n]*'''
        r'''--header\s+@-\s+"\$@"\s*$''',
        r'''(?m)^\s*VALKEY_PASSWORD="\$\(\s*vault_curl\s+'''
        r'''"\$VAULT_ADDR/v1/secret/data/platform/argocd"\s*\|\s*'''
        r'''jq\s+-er\s+['"]\.data\.data\.valkey_password['"]\s*\)"\s*$''',
        r'''(?m)^\s*printf\s+['"]%s['"]\s+"\$VALKEY_PASSWORD"\s*\|\s*'''
        r'''kubectl\b[^\n]*--from-file=redis-password=/dev/stdin[^\n]*'''
        r'''\|\s*kubectl\s+apply\s+-f\s+-\s*$''',
        r'''(?m)^\s*unset\s+VALKEY_PASSWORD\s*$''',
    )
    sensitive_remainder = pipeline_text
    for allowed_pattern in sensitive_allowlist_patterns:
        allowed_matches = list(re.finditer(allowed_pattern, sensitive_remainder))
        if len(allowed_matches) != 1:
            continue
        allowed_match = allowed_matches[0]
        sensitive_remainder = (
            sensitive_remainder[: allowed_match.start()]
            + sensitive_remainder[allowed_match.end() :]
        )

    unapproved_sensitive_use = re.search(
        r"(?i)\b(?:vault_token|valkey_password)\b", sensitive_remainder
    )
    focused_sensitive_error_present = bool(
        token_in_argv
        or vault_token_environment_input
        or secret_in_kubectl_argv
        or not has_silent_tty_read
        or not has_cleanup_contract
        or not has_header_pipe
        or not has_direct_secret_extraction
        or not has_kubectl_stdin_pipe
    )
    if unapproved_sensitive_use and not focused_sensitive_error_present:
        diagnostics.append(
            "bootstrap sensitive identifiers must use only approved operations"
        )

    return diagnostics


class SelfTestError(Exception):
    """A deterministic fixture or self-test contract failure."""


def _valid_contracts() -> dict[str, Any]:
    vault_store = {
        "apiVersion": "external-secrets.io/v1",
        "kind": "ClusterSecretStore",
        "metadata": {
            "name": "vault",
            "annotations": {
                ENVIRONMENT_SCOPE_ANNOTATION: LOCAL_ONLY,
                TRANSPORT_BOUNDARY_ANNOTATION: LOCAL_ONLY_HTTP,
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
                            "role": EXPECTED_VAULT_ROLE,
                            "serviceAccountRef": {
                                "name": EXPECTED_SERVICE_ACCOUNT,
                                "namespace": EXPECTED_SERVICE_ACCOUNT,
                                "audiences": copy.deepcopy(EXPECTED_AUDIENCES),
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
                "name": EXPECTED_SERVICE_ACCOUNT,
                "namespace": EXPECTED_SERVICE_ACCOUNT,
            }
        ],
    }
    vault_policy = "\n\n".join(
        f'path "{path}" {{\n  capabilities = ["read", "list"]\n}}'
        for path in EXPECTED_POLICY_PATHS
    )
    bootstrap = r'''#!/usr/bin/env bash
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
'''
    return {
        "vault_store": vault_store,
        "token_reviewer": token_reviewer,
        "vault_policy": vault_policy,
        "bootstrap": bootstrap,
    }


def _apply_fixture_mutation(contracts: dict[str, Any], mutation: str) -> None:
    if mutation == "none":
        return
    if mutation == "remove-local-only-annotations":
        contracts["vault_store"]["metadata"].pop("annotations")
        return
    if mutation == "remove-vault-audience":
        service_account_ref = contracts["vault_store"]["spec"]["provider"][
            "vault"
        ]["auth"]["kubernetes"]["serviceAccountRef"]
        service_account_ref.pop("audiences")
        return
    if mutation == "change-service-account":
        service_account_ref = contracts["vault_store"]["spec"]["provider"][
            "vault"
        ]["auth"]["kubernetes"]["serviceAccountRef"]
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
            'https://vault.example.invalid/v1/sys/health\n'
        )
        return
    if mutation == "add-exported-token":
        contracts["bootstrap"] += '\nexport VAULT_TOKEN="$vault_token"\n'
        return
    if mutation == "add-from-literal-password":
        contracts["bootstrap"] += (
            "\nkubectl -n argocd create secret generic unsafe "
            '--from-literal=redis-pass'
            'word="$VALKEY_PASSWORD"\n'
        )
        return
    raise SelfTestError(f"unknown mutation {mutation!r}")


def _contract_diagnostics(contracts: dict[str, Any]) -> list[str]:
    return [
        *validate_vault_store(contracts["vault_store"]),
        *validate_token_reviewer(contracts["token_reviewer"]),
        *validate_vault_policy(contracts["vault_policy"]),
        *validate_bootstrap(contracts["bootstrap"]),
    ]


def _reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for key, value in pairs:
        if key in data:
            raise ValueError(f"duplicate JSON key {key!r}")
        data[key] = value
    return data


def _load_fixture_cases(path: Path) -> list[dict[str, Any]]:
    try:
        fixture = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_json_keys,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise SelfTestError("fixture could not be loaded") from error

    if not isinstance(fixture, dict) or set(fixture) != {"cases"}:
        raise SelfTestError("fixture must contain exactly one cases array")
    cases = fixture["cases"]
    if not isinstance(cases, list) or len(cases) != 10:
        raise SelfTestError("fixture must contain exactly 10 cases")

    supported_mutations = {
        "none",
        "remove-local-only-annotations",
        "remove-vault-audience",
        "change-service-account",
        "add-token-reviewer-subject",
        "add-platform-wildcard",
        "add-curl-insecure",
        "add-token-header-argument",
        "add-exported-token",
        "add-from-literal-password",
    }
    names: set[str] = set()
    mutations: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict) or set(case) != {
            "name",
            "mutation",
            "expected",
        }:
            raise SelfTestError(f"case {index + 1} has an invalid object shape")
        name = case["name"]
        mutation = case["mutation"]
        expected = case["expected"]
        if not isinstance(name, str) or not name:
            raise SelfTestError(f"case {index + 1} has an invalid name")
        if name in names:
            raise SelfTestError(f"duplicate case name {name!r}")
        if not isinstance(mutation, str) or mutation not in supported_mutations:
            raise SelfTestError(f"case {name!r} has an unsupported mutation")
        if mutation in mutations:
            raise SelfTestError(f"duplicate fixture mutation {mutation!r}")
        if not isinstance(expected, list) or not all(
            isinstance(diagnostic, str) for diagnostic in expected
        ):
            raise SelfTestError(f"case {name!r} has invalid expected diagnostics")
        names.add(name)
        mutations.add(mutation)

    if mutations != supported_mutations:
        raise SelfTestError("fixture mutation cardinality does not match the contract")
    return cases


def _run_internal_boundaries() -> None:
    malformed_checks: tuple[
        tuple[Callable[[Any], list[str]], Any, list[str]], ...
    ] = (
        (
            validate_vault_store,
            [],
            ["Vault store document must be a mapping"],
        ),
        (
            validate_token_reviewer,
            "not-a-mapping",
            ["TokenReview binding document must be a mapping"],
        ),
        (
            validate_vault_policy,
            {},
            ["Vault policy document must be text"],
        ),
        (
            validate_bootstrap,
            [],
            ["bootstrap document must be text"],
        ),
    )
    for validator, malformed, expected in malformed_checks:
        actual = validator(malformed)
        if actual != expected:
            raise SelfTestError(
                f"malformed type boundary failed for {validator.__name__}"
            )

    try:
        yaml.load("kind: Service\nkind: Secret\n", Loader=_UniqueKeyLoader)
    except yaml.constructor.ConstructorError as error:
        if "duplicate key" not in str(error):
            raise SelfTestError("duplicate YAML key raised an unstable error") from error
    else:
        raise SelfTestError("duplicate YAML key was accepted")

    secure_bootstrap = _valid_contracts()["bootstrap"]
    require_file_block = '''require_file() {
  local path="$1"
  [[ -f "$path" && -r "$path" ]] || fail "required file is missing"
}'''
    require_file_after_use = secure_bootstrap.replace(
        require_file_block + "\n\n", "", 1
    ).replace(
        'require_file "$VAULT_CA_FILE"',
        'require_file "$VAULT_CA_FILE"\n\n' + require_file_block,
        1,
    )
    indirect_dependency_loop = '''for cmd in k3d kubectl helm docker curl jq openssl rg; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    fail "required command not found: $cmd"
  fi
  case "$cmd" in
    c*) "$cmd" --disable --cacert "$VAULT_CA_FILE" "$VAULT_ADDR/v1/sys/health" ;;
  esac
done'''
    focused_bootstrap_checks = (
        (
            "curl must disable its default configuration",
            secure_bootstrap.replace("curl --disable ", "curl ", 1),
            ["bootstrap curl must disable default configuration"],
        ),
        (
            "curl default-config guard must be its first option",
            secure_bootstrap.replace(
                "curl --disable --fail-with-body",
                "curl --fail-with-body --disable",
                1,
            ),
            ["bootstrap curl must disable default configuration"],
        ),
        (
            "xtrace guard must precede sensitive operations",
            secure_bootstrap.replace("set +x\n", "", 1),
            ["bootstrap must disable shell xtrace before sensitive operations"],
        ),
        (
            "set -x must not re-enable shell tracing",
            secure_bootstrap + "\nset -x\n",
            ["bootstrap must disable shell xtrace before sensitive operations"],
        ),
        (
            "semicolon set -x must not re-enable shell tracing",
            secure_bootstrap + "\nset -x; :\n",
            ["bootstrap must disable shell xtrace before sensitive operations"],
        ),
        (
            "builtin set -x must not re-enable shell tracing",
            secure_bootstrap + "\nbuiltin set -x\n",
            ["bootstrap must disable shell xtrace before sensitive operations"],
        ),
        (
            "command set -x must not re-enable shell tracing",
            secure_bootstrap + "\ncommand set -x\n",
            ["bootstrap must disable shell xtrace before sensitive operations"],
        ),
        (
            "set -o xtrace must not re-enable shell tracing",
            secure_bootstrap + "\nset -o xtrace\n",
            ["bootstrap must disable shell xtrace before sensitive operations"],
        ),
        (
            "combined shell options must not enable tracing",
            secure_bootstrap.replace(
                "set -euo pipefail", "set -euxo pipefail", 1
            ),
            ["bootstrap must disable shell xtrace before sensitive operations"],
        ),
        (
            "raw Vault curl must not bypass the guarded wrapper",
            secure_bootstrap.replace(
                'case "$VAULT_ADDR" in',
                '''curl --disable --fail-with-body --cacert "$VAULT_CA_FILE" \\
  "$VAULT_ADDR/v1/sys/health"

case "$VAULT_ADDR" in''',
                1,
            ),
            ["bootstrap must contain only the guarded vault_curl command"],
        ),
        (
            "dependency discovery must not execute a discovered command",
            secure_bootstrap.replace(
                'VAULT_CA_FILE="${VAULT_CA_FILE:-$ROOT_CA_FILE}"',
                indirect_dependency_loop
                + '\n\nVAULT_CA_FILE="${VAULT_CA_FILE:-$ROOT_CA_FILE}"',
                1,
            ),
            ["bootstrap must contain only the guarded vault_curl command"],
        ),
        (
            "aliased raw curl must not bypass the guarded wrapper",
            secure_bootstrap.replace(
                'case "$VAULT_ADDR" in',
                '''endpoint="$VAULT_ADDR/v1/sys/health"
curl --disable --fail-with-body --cacert "$VAULT_CA_FILE" "$endpoint"

case "$VAULT_ADDR" in''',
                1,
            ),
            ["bootstrap must contain only the guarded vault_curl command"],
        ),
        (
            "combined short curl options must not disable TLS verification",
            secure_bootstrap.replace(
                "curl --disable --fail-with-body",
                "curl --disable -sk --fail-with-body",
                1,
            ),
            ["bootstrap must not disable Vault TLS verification"],
        ),
        (
            "assigned long curl option must not disable TLS verification",
            secure_bootstrap.replace(
                "curl --disable --fail-with-body",
                "curl --disable --insecure=true --fail-with-body",
                1,
            ),
            ["bootstrap must not disable Vault TLS verification"],
        ),
        (
            "sensitive printf must be limited to approved stdin pipes",
            secure_bootstrap + '\nprintf \'%s\\n\' "$vault_token"\n',
            ["bootstrap sensitive identifiers must use only approved operations"],
        ),
        (
            "lowercase sensitive variables must not be exported",
            secure_bootstrap + '\nexport vault_token="$vault_token"\n',
            ["bootstrap sensitive identifiers must use only approved operations"],
        ),
        (
            "logger must not consume a sensitive value",
            secure_bootstrap + '\nlogger "$vault_token"\n',
            ["bootstrap sensitive identifiers must use only approved operations"],
        ),
        (
            "declare export attributes must not consume a sensitive identifier",
            secure_bootstrap + "\ndeclare -x vault_token\n",
            ["bootstrap sensitive identifiers must use only approved operations"],
        ),
        (
            "env assignments must not consume a sensitive value",
            secure_bootstrap
            + "\nenv TO"
            + 'KEN="$vault_token" true\n',
            ["bootstrap sensitive identifiers must use only approved operations"],
        ),
        (
            "curl must not load an explicit configuration",
            secure_bootstrap.replace(
                "curl --disable --fail-with-body",
                "curl --disable --config /tmp/operator.curlrc --fail-with-body",
                1,
            ),
            ["bootstrap curl must not load explicit configuration"],
        ),
        (
            "curl abbreviated option must not load an explicit configuration",
            secure_bootstrap.replace(
                "curl --disable --fail-with-body",
                "curl --disable --conf /tmp/operator.curlrc --fail-with-body",
                1,
            ),
            ["bootstrap curl must not load explicit configuration"],
        ),
        (
            "curl partial option must not load an explicit configuration",
            secure_bootstrap.replace(
                "curl --disable --fail-with-body",
                "curl --disable --confi=/tmp/operator.curlrc --fail-with-body",
                1,
            ),
            ["bootstrap curl must not load explicit configuration"],
        ),
        (
            "curl must not load an assigned explicit configuration",
            secure_bootstrap.replace(
                "curl --disable --fail-with-body",
                "curl --disable --config=/tmp/operator.curlrc --fail-with-body",
                1,
            ),
            ["bootstrap curl must not load explicit configuration"],
        ),
        (
            "curl must not load a short-option explicit configuration",
            secure_bootstrap.replace(
                "curl --disable --fail-with-body",
                "curl --disable -K /tmp/operator.curlrc --fail-with-body",
                1,
            ),
            ["bootstrap curl must not load explicit configuration"],
        ),
        (
            "curl must not load a combined attached explicit configuration",
            secure_bootstrap.replace(
                "curl --disable --fail-with-body",
                "curl --disable -sK/tmp/operator.curlrc --fail-with-body",
                1,
            ),
            ["bootstrap curl must not load explicit configuration"],
        ),
        (
            "require_file must be defined before it is used",
            require_file_after_use,
            ["bootstrap must require VAULT_CA_FILE"],
        ),
        (
            "HTTPS guard must be tied to VAULT_ADDR",
            secure_bootstrap.replace(
                '''case "$VAULT_ADDR" in
  https://*) ;;
  *) fail "VAULT_ADDR must use https:// for secret-bearing bootstrap" ;;
esac''',
                '''if [[ -n "$ROOT_CA_FILE" ]]; then
  : "unrelated https:// marker"
fi''',
                1,
            ),
            ["bootstrap must require an HTTPS Vault address"],
        ),
        (
            "Vault header must have a direct stdin producer",
            secure_bootstrap.replace(
                "  printf 'X-Vault-Token: %s",
                "  printf 'Removed-Vault-header: %s",
                1,
            ),
            ["bootstrap curl must read headers from stdin"],
        ),
        (
            "VAULT_CA_FILE must be checked for readability",
            secure_bootstrap.replace('&& -r "$path"', "", 1),
            ["bootstrap must require VAULT_CA_FILE"],
        ),
        (
            "later EXIT traps must preserve sensitive cleanup",
            secure_bootstrap + "\ntrap 'rm -f /tmp/bootstrap.tmp' EXIT\n",
            ["bootstrap must install a cleanup trap"],
        ),
        (
            "Vault secret extraction must use jq -er directly",
            secure_bootstrap.replace("jq -er", "jq -r", 1),
            ["bootstrap must provide redis-password to kubectl via stdin"],
        ),
        (
            "kubectl secret input must have a direct stdin producer",
            secure_bootstrap.replace(
                "printf '%s' \"$VALKEY_PASSWORD\" |\n  kubectl",
                "kubectl",
                1,
            ),
            ["bootstrap must provide redis-password to kubectl via stdin"],
        ),
    )
    for label, candidate, expected in focused_bootstrap_checks:
        actual = validate_bootstrap(candidate)
        if actual != expected:
            raise SelfTestError(
                f"{label}: expected {expected!r}, got {actual!r}"
            )


def _run_self_test() -> int:
    fixture_path = (
        Path(__file__).resolve().parents[1]
        / "tests"
        / "fixtures"
        / "vault-eso-contracts.json"
    )
    cases = _load_fixture_cases(fixture_path)
    baseline = _valid_contracts()
    for case in cases:
        contracts = copy.deepcopy(baseline)
        _apply_fixture_mutation(contracts, case["mutation"])
        actual = _contract_diagnostics(contracts)
        if actual != case["expected"]:
            raise SelfTestError(
                f"case {case['name']!r}: expected {case['expected']!r}, got {actual!r}"
            )
    _run_internal_boundaries()
    print(f"PASS vault-eso-contracts self-test: {len(cases)} cases")
    return 0


def _open_repository_root(root: Path) -> tuple[int | None, list[str]]:
    try:
        root_stat = root.lstat()
    except FileNotFoundError:
        return None, ["repository root is missing"]
    except OSError:
        return None, ["repository root could not be inspected safely"]

    if stat.S_ISLNK(root_stat.st_mode):
        return None, ["repository root must not be a symlink"]
    if not stat.S_ISDIR(root_stat.st_mode):
        return None, ["repository root must be a directory"]

    try:
        root_fd = os.open(
            root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        )
        opened_stat = os.fstat(root_fd)
    except OSError:
        return None, ["repository root could not be opened safely"]

    if (
        not stat.S_ISDIR(opened_stat.st_mode)
        or (opened_stat.st_dev, opened_stat.st_ino)
        != (root_stat.st_dev, root_stat.st_ino)
    ):
        os.close(root_fd)
        return None, ["repository root changed during validation"]
    return root_fd, []


def _read_exact_text(root_fd: int, relative_path: Path) -> tuple[str | None, list[str]]:
    """Read one fixed input without following any repository-internal symlink."""
    try:
        directory_fd = os.dup(root_fd)
    except OSError:
        return None, ["input could not be opened safely"]

    try:
        for component in relative_path.parts[:-1]:
            try:
                component_stat = os.lstat(component, dir_fd=directory_fd)
            except FileNotFoundError:
                return None, ["input is missing"]
            except OSError:
                return None, ["input path could not be inspected safely"]
            if stat.S_ISLNK(component_stat.st_mode):
                return None, ["input path must not traverse symlinks"]
            if not stat.S_ISDIR(component_stat.st_mode):
                return None, ["input parent must be a directory"]

            try:
                next_fd = os.open(
                    component,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=directory_fd,
                )
            except OSError:
                return None, ["input path could not be opened safely"]
            os.close(directory_fd)
            directory_fd = next_fd

        filename = relative_path.name
        try:
            input_stat = os.lstat(filename, dir_fd=directory_fd)
        except FileNotFoundError:
            return None, ["input is missing"]
        except OSError:
            return None, ["input could not be inspected safely"]
        if stat.S_ISLNK(input_stat.st_mode):
            return None, ["input must not be a symlink"]
        if not stat.S_ISREG(input_stat.st_mode):
            return None, ["input must be a regular file"]

        try:
            input_fd = os.open(
                filename, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory_fd
            )
            opened_stat = os.fstat(input_fd)
        except OSError:
            return None, ["input could not be opened safely"]
        if (
            not stat.S_ISREG(opened_stat.st_mode)
            or (opened_stat.st_dev, opened_stat.st_ino)
            != (input_stat.st_dev, input_stat.st_ino)
        ):
            os.close(input_fd)
            return None, ["input changed during validation"]

        try:
            with os.fdopen(input_fd, "r", encoding="utf-8") as stream:
                return stream.read(), []
        except (OSError, UnicodeError):
            return None, ["input could not be read as UTF-8 text"]
    finally:
        os.close(directory_fd)


def _load_yaml_documents(text: str) -> tuple[list[Any] | None, list[str]]:
    try:
        return list(yaml.load_all(text, Loader=_UniqueKeyLoader)), []
    except yaml.YAMLError:
        return None, [YAML_PARSE_ERROR]


def _validate_single_yaml(
    text: str,
    validator: Callable[[Any], list[str]],
    cardinality_error: str,
) -> list[str]:
    documents, diagnostics = _load_yaml_documents(text)
    if documents is None:
        return diagnostics
    if len(documents) != 1:
        return [cardinality_error]
    return validator(documents[0])


def _run_repository(root: Path) -> int:
    root_fd, root_diagnostics = _open_repository_root(root)
    if root_fd is None:
        for diagnostic in root_diagnostics:
            print(f"FAIL .: {diagnostic}")
        return 1

    findings: list[tuple[str, str]] = []

    def inspect(
        relative_path: Path, validate: Callable[[str], list[str]]
    ) -> None:
        text, diagnostics = _read_exact_text(root_fd, relative_path)
        if text is not None:
            diagnostics.extend(validate(text))
        findings.extend(
            (relative_path.as_posix(), diagnostic) for diagnostic in diagnostics
        )

    try:
        inspect(
            VAULT_STORE_PATH,
            lambda text: _validate_single_yaml(
                text,
                validate_vault_store,
                "Vault store input must contain exactly one YAML document",
            ),
        )
        inspect(
            TOKEN_REVIEWER_PATH,
            lambda text: _validate_single_yaml(
                text,
                validate_token_reviewer,
                "TokenReview binding input must contain exactly one YAML document",
            ),
        )

        def validate_external(text: str) -> list[str]:
            documents, diagnostics = _load_yaml_documents(text)
            if documents is None:
                return diagnostics
            return validate_vault_external(documents)

        inspect(VAULT_EXTERNAL_PATH, validate_external)
        inspect(VAULT_POLICY_PATH, validate_vault_policy)
        inspect(BOOTSTRAP_PATH, validate_bootstrap)
    finally:
        os.close(root_fd)

    stable_findings = sorted(set(findings))
    if stable_findings:
        for relative_path, diagnostic in stable_findings:
            print(f"FAIL {relative_path}: {diagnostic}")
        return 1

    print("PASS vault-eso-contracts repository validation")
    return 0


def _parse_args(arguments: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--root", type=Path, metavar="REPOSITORY")
    return parser.parse_args(arguments)


def main(arguments: Sequence[str] | None = None) -> int:
    args = _parse_args(arguments)
    if args.self_test:
        try:
            return _run_self_test()
        except SelfTestError as error:
            print(f"FAIL vault-eso-contracts self-test: {error}", file=sys.stderr)
            return 1

    return _run_repository(args.root)


if __name__ == "__main__":
    raise SystemExit(main())
