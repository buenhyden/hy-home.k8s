"""Validate the Vault External Secrets Operator store contract."""

from __future__ import annotations

import argparse
import json
import os
import stat
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
TOKEN_REVIEWER_PATH = Path("gitops/platform/eso/vault-token-reviewer-binding.yaml")
VAULT_EXTERNAL_PATH = Path("gitops/platform/external-services/vault-external.yaml")
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
            diagnostics.append(
                "Vault policy must not contain additional platform paths"
            )

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

    active_lines = [line for line in text.splitlines() if not re.match(r"^\s*#", line)]
    active_text = "\n".join(active_lines)
    command_text = re.sub(r"\\\s*\n", " ", active_text)
    pipeline_text = re.sub(r"\|\s*\n\s*", "| ", command_text)
    diagnostics: list[str] = []

    vault_curl_function = re.search(
        r"""(?ms)^\s*vault_curl\(\)\s*\{\s*$\n"""
        r"""(?P<body>.*?)^\s*\}\s*$""",
        active_text,
    )
    vault_curl_body_raw = (
        vault_curl_function.group("body") if vault_curl_function else ""
    )
    vault_curl_body = re.sub(r"\\\s*\n", " ", vault_curl_body_raw)

    dependency_discovery_block = """for cmd in k3d kubectl helm docker curl jq openssl rg; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    fail "required command not found: $cmd"
  fi
done"""
    dependency_loop_neutral_text = active_text
    if active_text.count(dependency_discovery_block) == 1:
        dependency_loop_neutral_text = active_text.replace(
            dependency_discovery_block, "", 1
        )
    curl_token_count = len(re.findall(r"\bcurl\b", dependency_loop_neutral_text))
    wrapper_curl_token_count = len(re.findall(r"\bcurl\b", vault_curl_body_raw))
    curl_structure_valid = curl_token_count == 1 and wrapper_curl_token_count == 1

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
        r"""(?m)\b(?:curl|vault_curl)\b[^\n]*(?:-H|--header)(?:=|\s+)"""
        r"""["']?X-Vault-Token\s*:[^\n"']*"""
        r"""(?:\$(?:vault_token|VAULT_TOKEN)|\$\{(?:vault_token|VAULT_TOKEN)\})""",
        command_text,
    )
    if not curl_structure_valid and not token_in_argv:
        diagnostics.append("bootstrap must contain only the guarded vault_curl command")

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
        r"""[^\n]*(?:\$VALKEY_PASSWORD|\$\{VALKEY_PASSWORD\})""",
        command_text,
    )
    if secret_in_kubectl_argv:
        diagnostics.append(
            "bootstrap must not place generated secret values in kubectl argv"
        )

    https_guard = re.search(
        r"""(?m)^\s*case\s+"\$VAULT_ADDR"\s+in\s*$\n"""
        r"""^\s*https://\*\)\s*;;\s*$\n"""
        r"""^\s*\*\)\s*fail\b[^\n]*;;\s*$\n"""
        r"""^\s*esac\s*$""",
        active_text,
    )
    if https_guard is None or https_guard.start() > first_vault_call:
        diagnostics.append("bootstrap must require an HTTPS Vault address")

    ca_assignment = re.search(
        r"""(?m)^\s*VAULT_CA_FILE="\$\{VAULT_CA_FILE:-\$ROOT_CA_FILE\}"\s*$""",
        active_text,
    )
    ca_requirement = re.search(
        r"""(?m)^\s*require_file\s+"\$VAULT_CA_FILE"\s*$""", active_text
    )
    require_file_function = re.search(
        r"""(?ms)^\s*require_file\(\)\s*\{\s*$\n"""
        r"""(?P<body>.*?)^\s*\}\s*$""",
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
        r"""(?m)^\s*IFS=\s+read\s+-r\s+-s\s+-p\s+"""
        r"""["'][^"']*["']\s+vault_token\s*</dev/tty\s*$""",
        active_text,
    )
    nonempty_token_guard = re.search(
        r"""(?m)^\s*\[\[\s+-n\s+"\$vault_token"\s+\]\]\s+\|\|\s+fail\b""",
        active_text,
    )
    tty_readability_guard = re.search(
        r"""(?m)^\s*if\s+\[\[\s+!\s+-r\s+/dev/tty\s+\]\];\s+then\s*$""",
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
        r"""(?ms)^\s*cleanup_sensitive\(\)\s*\{\s*$\n"""
        r"""(?P<body>.*?)^\s*\}\s*$""",
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
        r"""\bcurl\s+--disable(?:\s|$)""", vault_curl_body
    ):
        diagnostics.append("bootstrap curl must disable default configuration")
    if not re.search(
        r'''\bcurl\b[^\n]*--cacert\s+"\$VAULT_CA_FILE"''',
        vault_curl_body,
    ):
        diagnostics.append("bootstrap curl must use --cacert")

    has_header_pipe = bool(
        re.search(
            r"""printf\s+['"]X-Vault-Token:\s*%s\\n['"]\s+"""
            r""""\$vault_token"\s*\|\s*curl\b""",
            vault_curl_body,
        )
        and re.search(r"""\bcurl\b[^\n]*--header\s+@-""", vault_curl_body)
        and '"$@"' in vault_curl_body
        and not re.search(
            r"""\bvault_curl\b(?!\s*\(\))[^\n]*(?:-H|--header)""",
            command_text,
        )
    )
    if not has_header_pipe:
        diagnostics.append("bootstrap curl must read headers from stdin")

    has_direct_secret_extraction = bool(
        "vault_secret_json" not in active_text
        and re.search(
            r"""VALKEY_PASSWORD="\$\(\s*vault_curl\s+"""
            r""""\$VAULT_ADDR/v1/secret/data/platform/argocd"\s*\|\s*"""
            r'''jq\s+-er\s+['"]\.data\.data\.valkey_password['"]\s*\)"''',
            command_text,
        )
    )
    has_kubectl_stdin_pipe = bool(
        re.search(
            r"""printf\s+['"]%s['"]\s+"\$VALKEY_PASSWORD"\s*\|\s*"""
            r"""kubectl\b[\s\S]*?--from-file=redis-password=/dev/stdin""",
            command_text,
        )
    )
    if not has_direct_secret_extraction or not has_kubectl_stdin_pipe:
        diagnostics.append("bootstrap must provide redis-password to kubectl via stdin")

    sensitive_allowlist_patterns = (
        r"""(?m)^\s*IFS=\s+read\s+-r\s+-s\s+-p\s+"""
        r"""["'][^"']*["']\s+vault_token\s*</dev/tty\s*$""",
        r"""(?m)^\s*\[\[\s+-n\s+"\$vault_token"\s+\]\]\s+"""
        r"""\|\|\s+fail\b[^\n]*$""",
        r"""(?m)^\s*unset\s+vault_token\s+VALKEY_PASSWORD\s*$""",
        r"""(?m)^\s*printf\s+['"]X-Vault-Token:\s*%s\\n['"]\s+"""
        r""""\$vault_token"\s*\|\s*curl\b[^\n]*"""
        r"""--header\s+@-\s+"\$@"\s*$""",
        r"""(?m)^\s*VALKEY_PASSWORD="\$\(\s*vault_curl\s+"""
        r""""\$VAULT_ADDR/v1/secret/data/platform/argocd"\s*\|\s*"""
        r"""jq\s+-er\s+['"]\.data\.data\.valkey_password['"]\s*\)"\s*$""",
        r"""(?m)^\s*printf\s+['"]%s['"]\s+"\$VALKEY_PASSWORD"\s*\|\s*"""
        r"""kubectl\b[^\n]*--from-file=redis-password=/dev/stdin[^\n]*"""
        r"""\|\s*kubectl\s+apply\s+-f\s+-\s*$""",
        r"""(?m)^\s*unset\s+VALKEY_PASSWORD\s*$""",
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
        root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        opened_stat = os.fstat(root_fd)
    except OSError:
        return None, ["repository root could not be opened safely"]

    if not stat.S_ISDIR(opened_stat.st_mode) or (
        opened_stat.st_dev,
        opened_stat.st_ino,
    ) != (root_stat.st_dev, root_stat.st_ino):
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
        if not stat.S_ISREG(opened_stat.st_mode) or (
            opened_stat.st_dev,
            opened_stat.st_ino,
        ) != (input_stat.st_dev, input_stat.st_ino):
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

    def inspect(relative_path: Path, validate: Callable[[str], list[str]]) -> None:
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
    parser.add_argument("--root", type=Path, required=True, metavar="REPOSITORY")
    return parser.parse_args(arguments)


def main(arguments: Sequence[str] | None = None) -> int:
    args = _parse_args(arguments)
    return _run_repository(args.root)


if __name__ == "__main__":
    raise SystemExit(main())
