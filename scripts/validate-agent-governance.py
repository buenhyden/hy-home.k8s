#!/usr/bin/env python3
"""Validate the terminal provider-neutral agent registry.

Machine authority lives only in ``docs/00.agent-governance/roles/registry.json`` and its schema.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import tomllib

import yaml
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn, Sequence

from json_schema_validation import SchemaEvaluationError, schema_errors


REGISTRY_PATH = PurePosixPath("docs/00.agent-governance/roles/registry.json")
REGISTRY_SCHEMA_PATH = PurePosixPath(
    "docs/00.agent-governance/roles/registry.schema.json"
)
REGISTRY_PROVIDER_IDS = ("claude", "codex")
REGISTRY_PROJECTION_ROOTS = {
    "neutral": PurePosixPath("docs/00.agent-governance/roles"),
    "claude": PurePosixPath(".claude/agents"),
    "codex": PurePosixPath(".codex/agents"),
}
REGISTRY_PROJECTION_SUFFIXES = {
    "neutral": ".md",
    "claude": ".md",
    "codex": ".toml",
}
REGISTRY_PERMISSION_BEHAVIOR = {
    "read-only-evidence": (False, False),
    "scoped-authoring": (True, False),
    "orchestration": (False, True),
}
CLAUDE_ALLOWED_PERMISSIONS = (
    "Bash(git status --short)",
    "Bash(git diff --check)",
    "Bash(git diff --cached --check)",
    "Bash(git diff --name-only)",
    "Bash(git diff --cached --name-only)",
    "Bash(git rev-parse HEAD)",
    "Bash(git ls-files)",
)
CLAUDE_FORBIDDEN_ALLOW_PERMISSIONS = (
    "Bash(ls:*)",
    "Bash(grep:*)",
    "Bash(cat:*)",
    "Bash(git:*)",
    "Bash(kubectl get:*)",
    "Bash(kubectl describe:*)",
    "Bash(kubectl logs:*)",
)
CLAUDE_REQUIRED_DENY_PERMISSIONS = (
    "Read(./.env)",
    "Read(./.env.*)",
    "Read(./**/.env)",
    "Read(./**/.env.*)",
    "Bash(cat .env:*)",
    "Bash(cat .env.*:*)",
    "Bash(env:*)",
    "Bash(printenv:*)",
    "Bash(vault kv get:*)",
    "Bash(vault read:*)",
    "Bash(vault token lookup:*)",
    "Bash(kubectl get secret:*)",
    "Bash(kubectl get secrets:*)",
    "Bash(kubectl describe secret:*)",
    "Bash(kubectl describe secrets:*)",
    "Bash(git push:*)",
    "Bash(git merge:*)",
    "Bash(gh pr create:*)",
    "Bash(gh pr merge:*)",
    "Bash(gh release create:*)",
    "Bash(gh workflow run:*)",
    "Bash(kubectl delete:*)",
    "Bash(kubectl apply:*)",
    "Bash(kubectl create:*)",
    "Bash(kubectl replace:*)",
    "Bash(kubectl exec:*)",
    "Bash(kubectl patch:*)",
    "Bash(kubectl edit:*)",
    "Bash(kubectl label:*)",
    "Bash(kubectl annotate:*)",
    "Bash(kubectl set:*)",
    "Bash(kubectl scale:*)",
    "Bash(kubectl rollout restart:*)",
    "Bash(kubectl rollout undo:*)",
    "Bash(kubectl port-forward:*)",
    "Bash(kubectl drain:*)",
    "Bash(kubectl cordon:*)",
    "Bash(kubectl uncordon:*)",
    "Bash(kubectl taint:*)",
    "Bash(argocd app sync:*)",
    "Bash(argocd app set:*)",
    "Bash(argocd app patch:*)",
    "Bash(argocd app delete:*)",
    "Bash(argocd app create:*)",
    "Bash(argocd app unset:*)",
    "Bash(argocd app terminate-op:*)",
    "Bash(vault kv put:*)",
    "Bash(vault kv patch:*)",
    "Bash(vault write:*)",
    "Bash(git reset --hard:*)",
    "Bash(git checkout --:*)",
    "Bash(git restore:*)",
    "Bash(git clean:*)",
    "Bash(git rebase:*)",
    "Bash(git commit --amend:*)",
    "Bash(git branch -D:*)",
    "Bash(git push --force:*)",
    "Bash(git push -f:*)",
    "Bash(git push --delete:*)",
    "Bash(git push --mirror:*)",
    "Bash(rm -rf:*)",
    "Bash(k3d cluster delete:*)",
)


MAX_JSON_BYTES = 1_048_576
READ_CHUNK_BYTES = 65_536

REPOSITORY_STATIC_RUNTIME_CLAIMS = (
    re.compile(r"\bauthenticated\s+provider\s+execution\b", re.IGNORECASE),
    re.compile(r"\bprovider\s+(?:runtime\s+)?discovered\b", re.IGNORECASE),
    re.compile(
        r"\bhosted\s+ci\s+(?:passed|verified|authenticated)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:deployment|live\s+runtime)\s+(?:passed|verified|active)\b",
        re.IGNORECASE,
    ),
)
SENSITIVE_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}", re.IGNORECASE),
    re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,})"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{12,}", re.IGNORECASE),
    re.compile(
        r"\b(?:password|passwd|api[_-]?key|client[_-]?secret|"
        r"access[_-]?token|token|secret|aws[_-]?secret[_-]?access[_-]?key)"
        r"\s*[:=]\s*[\"']?[A-Za-z0-9._~+/=-]{12,}",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:raw|full)\s+(?:provider\s+)?(?:prompt|transcript)"
        r"\s*[:=]\s*\S+",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:observed\s+)?(?:"
        r"auth[_ -]?file(?:[_ -]?(?:content|path|payload))?|"
        r"shell[_ -]?history(?:[_ -]?(?:content|payload|entry))?|"
        r"private[_ -]?diagnostic(?:[_ -]?(?:content|payload|dump))?|"
        r"(?:environment|env)[_ -]?dump|"
        r"user[_ -]?(?:configuration|config)"
        r"(?:[_ -]?(?:content|payload|dump))?)"
        r"\s*[:=]\s*\S.{7,}",
        re.IGNORECASE,
    ),
)


class DuplicateKeyError(ValueError):
    """Raised when a JSON object repeats a key."""


class HarnessError(ValueError):
    """Stable registry validation failure."""

    def __init__(self, code: str, detail: str, *, exit_code: int = 1):
        self.code = code
        self.detail = detail
        self.exit_code = exit_code
        super().__init__(f"{code}: {detail}")


def fail(code: str, detail: str, *, exit_code: int = 1) -> NoReturn:
    safe_detail = (
        "input exceeds size limit"
        if "input exceeds" in detail
        else "agent registry validation failed"
    )
    raise HarnessError(code, safe_detail, exit_code=exit_code)


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateKeyError(f"duplicate JSON key {key!r}")
        value[key] = item
    return value


def decode_json_text(text: str, source: str = "<memory>") -> Any:
    """Decode JSON while rejecting duplicate object keys at every depth."""

    try:
        return json.loads(text, object_pairs_hook=_reject_duplicate_pairs)
    except DuplicateKeyError as exc:
        fail("AGENT-REGISTRY-INPUT", f"{source}: {exc}", exit_code=2)
    except json.JSONDecodeError as exc:
        fail("AGENT-REGISTRY-INPUT", f"{source}: {exc}", exit_code=2)


def _strict_root(root: Path, *, code: str = "AGENT-REGISTRY-INPUT") -> Path:
    try:
        absolute = root.absolute()
        metadata = os.lstat(absolute)
    except OSError as exc:
        fail(code, f"repository root is unavailable: {exc}", exit_code=2)
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        fail(
            code,
            "repository root must be a real non-symlink directory",
            exit_code=2,
        )
    try:
        return absolute.resolve(strict=True)
    except OSError as exc:
        fail(code, f"repository root is unavailable: {exc}", exit_code=2)


def _normalized_relative(relative: PurePosixPath | str, *, code: str) -> PurePosixPath:
    raw = relative.as_posix() if isinstance(relative, PurePosixPath) else relative
    path = PurePosixPath(raw)
    if (
        not raw
        or "\x00" in raw
        or path.is_absolute()
        # PurePosixPath has already collapsed empty and dot components.
        or any(part in {"", ".", ".."} for part in raw.split("/"))
    ):
        fail(code, f"{raw!r} is not a normalized repository-relative path")
    return path


def _read_regular_file(
    root: Path,
    relative: PurePosixPath | str,
    *,
    code: str,
    max_bytes: int = MAX_JSON_BYTES,
) -> bytes:
    """Read a bounded regular file without following any path component."""

    strict_root = _strict_root(root, code=code)
    normalized = _normalized_relative(relative, code=code)
    descriptors: list[int] = []
    try:
        directory_flags = (
            os.O_RDONLY
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        parent = os.open(strict_root, directory_flags)
        descriptors.append(parent)
        for segment in normalized.parts[:-1]:
            parent = os.open(segment, directory_flags, dir_fd=parent)
            descriptors.append(parent)
            if not stat.S_ISDIR(os.fstat(parent).st_mode):
                fail(code, f"{normalized}: parent component is not a directory")

        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        if hasattr(os, "O_NONBLOCK"):
            flags |= os.O_NONBLOCK
        descriptor = os.open(normalized.parts[-1], flags, dir_fd=parent)
        descriptors.append(descriptor)
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            fail(code, f"{normalized}: expected a regular non-symlink file")
        if metadata.st_size > max_bytes:
            fail(code, f"{normalized}: input exceeds {max_bytes} bytes")

        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(
                descriptor,
                min(READ_CHUNK_BYTES, max_bytes + 1 - total),
            )
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                fail(code, f"{normalized}: input exceeds {max_bytes} bytes")
            chunks.append(chunk)
        return b"".join(chunks)
    except HarnessError:
        raise
    except OSError as exc:
        fail(code, f"{normalized}: {exc}")
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def load_json(
    root: Path,
    relative: PurePosixPath | str,
    *,
    code: str = "AGENT-REGISTRY-INPUT",
) -> Any:
    try:
        text = _read_regular_file(root, relative, code=code).decode("utf-8")
    except UnicodeError as exc:
        fail(code, f"{relative}: input is not UTF-8: {exc}", exit_code=2)
    return decode_json_text(text, str(relative))


def _validate_registry_schema(root: Path, registry: Any) -> dict[str, Any]:
    if not isinstance(registry, dict):
        fail("AGENT-REGISTRY-SCHEMA", "registry root must be an object")
    schema = load_json(root, REGISTRY_SCHEMA_PATH)
    if not isinstance(schema, dict):
        fail("AGENT-REGISTRY-SCHEMA", "registry schema root must be an object")
    try:
        errors = schema_errors(schema, registry)
    except SchemaEvaluationError:
        fail("AGENT-REGISTRY-SCHEMA", "invalid registry schema")
    if errors:
        error = errors[0]
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        fail("AGENT-REGISTRY-SCHEMA", f"{location}: {error.message}")
    return registry


def _identities(items: list[dict[str, Any]], collection: str) -> list[str]:
    values = [item["id"] for item in items]
    if len(values) != len(set(values)):
        fail(
            f"AGENT-REGISTRY-{collection}",
            f"{collection.lower()} identities must be unique",
        )
    return values


def _registry_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [text for item in value for text in _registry_strings(item)]
    if isinstance(value, dict):
        return [text for item in value.values() for text in _registry_strings(item)]
    return []


def _projection_files(root: Path, relative: PurePosixPath, suffix: str) -> set[str]:
    strict_root = _strict_root(root, code="AGENT-REGISTRY-PROJECTION")
    normalized = _normalized_relative(relative, code="AGENT-REGISTRY-PROJECTION")
    directory = strict_root
    descriptors = []
    try:
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        descriptor = os.open(strict_root, flags)
        descriptors.append(descriptor)
        for part in normalized.parts:
            descriptor = os.open(part, flags, dir_fd=descriptor)
            descriptors.append(descriptor)
        directory = descriptor
        metadata = os.fstat(descriptor)
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            fail("AGENT-REGISTRY-PROJECTION", f"{relative}: invalid projection root")
        actual: set[str] = set()
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_symlink():
                    fail(
                        "AGENT-REGISTRY-PROJECTION",
                        f"{relative}/{entry.name}: symlink projection is forbidden",
                    )
                if entry.name.endswith(suffix) and not (
                    relative == REGISTRY_PROJECTION_ROOTS["neutral"]
                    and entry.name
                    in {
                        "README.md",
                        "architecture.md",
                        "documentation.md",
                        "infrastructure.md",
                        "operations.md",
                        "quality.md",
                        "security.md",
                        "supervision.md",
                    }
                ):
                    if not entry.is_file(follow_symlinks=False):
                        fail(
                            "AGENT-REGISTRY-PROJECTION",
                            f"{relative}/{entry.name}: projection is not a regular file",
                        )
                    actual.add(f"{relative.as_posix()}/{entry.name}")
        return actual
    except HarnessError:
        raise
    except OSError as exc:
        fail("AGENT-REGISTRY-PROJECTION", f"{relative}: {exc}")
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def _require_regular_file(
    root: Path, relative: PurePosixPath | str, *, code: str
) -> None:
    _read_regular_file(root, relative, code=code)


def validate_registry(
    root: Path,
    registry: dict[str, Any] | None = None,
    *,
    check_files: bool = True,
) -> dict[str, int]:
    """Validate the sole Codex/Claude provider-neutral registry authority."""

    if check_files:
        validate_absent_surfaces(root)
    if registry is None:
        registry = load_json(root, REGISTRY_PATH)
    registry = _validate_registry_schema(root, registry)

    providers = registry["providers"]
    provider_ids = _identities(providers, "PROVIDER")
    if tuple(provider_ids) != REGISTRY_PROVIDER_IDS:
        fail(
            "AGENT-REGISTRY-PROVIDER",
            "supported providers must be exactly claude and codex",
        )

    permission_classes = registry["permission_classes"]
    permission_ids = _identities(permission_classes, "PERMISSION")
    if set(permission_ids) != set(REGISTRY_PERMISSION_BEHAVIOR):
        fail(
            "AGENT-REGISTRY-PERMISSION",
            "permission classes differ from the closed authority set",
        )
    for item in permission_classes:
        observed = (item["allows_mutation"], item["allows_delegation"])
        if observed != REGISTRY_PERMISSION_BEHAVIOR[item["id"]]:
            fail(
                "AGENT-REGISTRY-PERMISSION",
                f"{item['id']} behavior differs from its authority boundary",
            )

    skills = registry["skills"]
    skill_ids = _identities(skills, "SKILL")
    roles = registry["roles"]
    role_ids = _identities(roles, "ROLE")
    role_set = set(role_ids)
    skill_set = set(skill_ids)
    declared: dict[str, set[str]] = {
        surface: set() for surface in REGISTRY_PROJECTION_ROOTS
    }
    handoff_count = 0
    projection_count = 0

    for role in roles:
        role_id = role["id"]
        if role["permission_class"] not in permission_ids:
            fail(
                "AGENT-REGISTRY-PERMISSION",
                f"{role_id} references an unknown permission class",
            )
        if tuple(role["supported_providers"]) != REGISTRY_PROVIDER_IDS:
            fail(
                "AGENT-REGISTRY-PROVIDER",
                f"{role_id} must support exactly claude and codex",
            )
        if not set(role["skill_refs"]).issubset(skill_set):
            fail("AGENT-REGISTRY-SKILL", f"{role_id} references an unknown skill")
        handoffs = role["handoff_to"]
        if role_id in handoffs or not set(handoffs).issubset(role_set):
            fail("AGENT-REGISTRY-HANDOFF", f"{role_id} has an invalid handoff edge")
        handoff_count += len(handoffs)

        for surface, path_text in role["projections"].items():
            expected = (
                REGISTRY_PROJECTION_ROOTS[surface]
                / f"{role_id}{REGISTRY_PROJECTION_SUFFIXES[surface]}"
            ).as_posix()
            if path_text != expected or path_text in declared[surface]:
                fail(
                    "AGENT-REGISTRY-PROJECTION",
                    f"{role_id}/{surface} must uniquely project to {expected}",
                )
            declared[surface].add(path_text)
            projection_count += 1

    registry_text = "\n".join(_registry_strings(registry))
    if any(
        pattern.search(registry_text) for pattern in REPOSITORY_STATIC_RUNTIME_CLAIMS
    ):
        fail(
            "AGENT-REGISTRY-EVIDENCE",
            "registry contains a provider-runtime or live-state claim",
        )
    if any(pattern.search(registry_text) for pattern in SENSITIVE_PATTERNS):
        fail("AGENT-REGISTRY-EVIDENCE", "registry contains secret-bearing evidence")

    for role in roles:
        policy, fragment = role["capability_tier_ref"].split("#", 1)
        text = _read_regular_file(root, policy, code="AGENT-REGISTRY-TIER").decode(
            "utf-8"
        )
        headings = {
            match.lower() for match in re.findall(r"(?m)^#{1,6} ([A-Za-z]+)\s*$", text)
        }
        if fragment not in headings:
            fail("AGENT-REGISTRY-TIER", "missing policy heading")
    if check_files:
        for skill in skills:
            _require_regular_file(
                root,
                skill["path"],
                code="AGENT-REGISTRY-SKILL",
            )
        validate_native_assets(root, registry)
        for surface, expected_paths in declared.items():
            actual_paths = _projection_files(
                root,
                REGISTRY_PROJECTION_ROOTS[surface],
                REGISTRY_PROJECTION_SUFFIXES[surface],
            )
            if actual_paths != expected_paths:
                fail(
                    "AGENT-REGISTRY-PROJECTION",
                    f"{surface} projection set differs: "
                    f"expected={sorted(expected_paths)!r} actual={sorted(actual_paths)!r}",
                )
        for provider in providers:
            _require_regular_file(
                root,
                PurePosixPath(provider["gateway"]),
                code="AGENT-REGISTRY-PROVIDER",
            )

    return {
        "providers": len(providers),
        "roles": len(roles),
        "permissionClasses": len(permission_classes),
        "skills": len(skills),
        "handoffs": handoff_count,
        "projections": projection_count,
    }


class UniqueMetadataLoader(yaml.SafeLoader):
    """Reject duplicate native metadata keys before applying permissions."""


def _metadata_mapping(loader: UniqueMetadataLoader, node: yaml.MappingNode):
    pairs = [
        (loader.construct_object(key), loader.construct_object(value))
        for key, value in node.value
    ]
    return _reject_duplicate_pairs(pairs)


UniqueMetadataLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _metadata_mapping
)


def _read_text(root: Path, path: str, code: str) -> str:
    try:
        return _read_regular_file(root, path, code=code).decode("utf-8")
    except UnicodeError:
        fail(code, "input is not UTF-8")


def _frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = re.fullmatch(r"---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not match:
        fail("AGENT-NATIVE-METADATA", "missing native frontmatter")
    raw, body = match.groups()
    try:
        metadata = yaml.load(raw, Loader=UniqueMetadataLoader)
    except (ValueError, yaml.YAMLError):
        fail("AGENT-NATIVE-METADATA", "invalid native metadata")
    if not isinstance(metadata, dict):
        fail("AGENT-NATIVE-METADATA", "metadata must be an object")
    # Native metadata is deliberately scalar and canonical: hidden comments,
    # aliases, tags, or extra policy cannot ride along with provider keys.
    if raw != "\n".join(
        f"{key}: {json.dumps(value, ensure_ascii=False)}"
        for key, value in metadata.items()
    ):
        fail("AGENT-NATIVE-METADATA", "noncanonical native metadata")
    return metadata, body


def validate_absent_surfaces(root: Path) -> None:
    root = _strict_root(root)
    for path in (
        ".agents",
        ".codex/skills",
        ".codex/hooks",
        ".codex/hooks.json",
        ".gemini",
        "GEMINI.md",
    ):
        if os.path.lexists(root / path):
            fail("AGENT-GOVERNANCE-RETIRED", "retired surface was recreated")


def validate_current_sources(root: Path) -> None:
    """Current common guidance cannot import the retired control-plane root.

    Historical Spec/Task/archive records and negative tests are deliberately
    outside this scan; their evidence belongs to the historical consumer owner.
    """
    governance = root / "docs/00.agent-governance"
    if governance.is_dir():
        for parent, directories, files in os.walk(governance, followlinks=False):
            for name in directories:
                if (Path(parent) / name).is_symlink():
                    fail(
                        "AGENT-GOVERNANCE-CONSUMER",
                        "shared owner has a symlink directory",
                    )
            for name in files:
                if not name.endswith((".md", ".json", ".sh")):
                    continue
                path = (Path(parent) / name).relative_to(root).as_posix()
                text = _read_text(root, path, "AGENT-GOVERNANCE-CONSUMER")
                if ".agents/" in text:
                    fail(
                        "AGENT-GOVERNANCE-CONSUMER",
                        "current common guidance references retired root",
                    )


def validate_native_assets(root: Path, registry: dict[str, Any]) -> None:
    """Validate direct canonical reads and native configuration, never discovery."""
    skills = {skill["id"]: skill["path"] for skill in registry["skills"]}
    for skill_id, path in skills.items():
        if path != f"docs/00.agent-governance/skills/{skill_id}/SKILL.md":
            fail("AGENT-REGISTRY-SKILL", "skill identity differs from package path")
        metadata, body = _frontmatter(_read_text(root, path, "AGENT-REGISTRY-SKILL"))
        if (
            set(metadata) != {"name", "description"}
            or metadata["name"] != skill_id
            or not isinstance(metadata["description"], str)
            or not metadata["description"].strip()
            or not body.strip()
        ):
            fail("AGENT-REGISTRY-SKILL", "invalid skill identity or metadata")
    for role in registry["roles"]:
        canonical = role["projections"]["neutral"]
        _read_text(root, canonical, "AGENT-REGISTRY-PROJECTION")
        expected_refs = {
            canonical,
            REGISTRY_PATH.as_posix(),
            "docs/00.agent-governance/skills/work-lifecycle.md",
            *(skills[skill] for skill in role["skill_refs"]),
        }
        for provider in REGISTRY_PROVIDER_IDS:
            text = _read_text(
                root, role["projections"][provider], "AGENT-NATIVE-METADATA"
            )
            if provider == "claude":
                metadata, body = _frontmatter(text)
                allowed = {"name", "description", "model", "tools"}
                model = metadata.get("model")
                if model not in {
                    "claude-sonnet-4-6",
                    "claude-opus-4-8",
                    "claude-sonnet-5",
                }:
                    fail("AGENT-NATIVE-METADATA", "unsupported model identifier")
                tools = {"Read", "Grep", "Glob"}
                if role["permission_class"] == "scoped-authoring":
                    tools |= {"Write", "Edit", "Bash"}
                elif role["permission_class"] == "orchestration":
                    tools |= {"Task"}
                elif role["id"] == "docs-researcher":
                    tools |= {"WebFetch", "WebSearch"}
                else:
                    tools |= {"Bash"}
                raw_tools = metadata.get("tools", "")
                observed = raw_tools.split(", ") if isinstance(raw_tools, str) else []
                if set(observed) != tools or len(observed) != len(tools):
                    fail(
                        "AGENT-NATIVE-PERMISSION",
                        "native tools differ from least authority",
                    )
            else:
                try:
                    metadata = tomllib.loads(text)
                except ValueError:
                    fail("AGENT-NATIVE-METADATA", "invalid native TOML")
                allowed = {
                    "name",
                    "description",
                    "model",
                    "model_reasoning_effort",
                    "developer_instructions",
                }
                body = metadata.get("developer_instructions", "")
                if (
                    not isinstance(metadata.get("model"), str)
                    or not re.fullmatch(r"[a-z0-9][a-z0-9.-]{0,159}", metadata["model"])
                    or not isinstance(metadata.get("model_reasoning_effort"), str)
                    or metadata.get("model_reasoning_effort")
                    not in {"none", "minimal", "low", "medium", "high", "xhigh"}
                ):
                    fail(
                        "AGENT-NATIVE-METADATA", "invalid model or reasoning identifier"
                    )
                if text != "".join(
                    f"{key} = {json.dumps(value)}\n" for key, value in metadata.items()
                ):
                    fail("AGENT-NATIVE-METADATA", "noncanonical native metadata")
            if (
                set(metadata) != allowed
                or metadata.get("name") != role["id"]
                or metadata.get("description") != role["responsibility"]
            ):
                fail("AGENT-NATIVE-METADATA", "native identity or keys differ")
            if not isinstance(body, str):
                fail("AGENT-NATIVE-REFERENCE", "instructions must be text")
            lines = body.strip().splitlines()
            refs = []
            for line in lines[1:-2]:
                match = re.fullmatch(r"- `([^`]+)`", line)
                if not match:
                    fail(
                        "AGENT-NATIVE-REFERENCE",
                        "unexpected shared prose or hidden instructions",
                    )
                refs.append(match.group(1))
            if (
                not lines
                or lines[0] != "Read the following repository files before acting:"
                or lines[-2:]
                != [
                    "",
                    "Apply the role, permission, procedure, and handoff boundaries in those files.",
                ]
                or set(refs) != expected_refs
                or len(refs) != len(expected_refs)
            ):
                fail("AGENT-NATIVE-REFERENCE", "canonical reads differ")
            for ref in refs:
                _read_regular_file(root, ref, code="AGENT-NATIVE-REFERENCE")
    link = root / ".claude/skills"
    if (
        not link.is_symlink()
        or os.readlink(link) != "../docs/00.agent-governance/skills"
    ):
        fail("AGENT-NATIVE-REFERENCE", "Claude skill adapter differs")
    for provider in REGISTRY_PROVIDER_IDS:
        path = f".{provider}/{provider.upper()}.md"
        baseline = _read_text(root, path, "AGENT-NATIVE-REFERENCE")
        expected = {
            f"docs/00.agent-governance/providers/{provider}.md",
            REGISTRY_PATH.as_posix(),
            "docs/00.agent-governance/policies/agent-execution.md",
            "docs/00.agent-governance/policies/approval-and-safety.md",
            "docs/00.agent-governance/skills/work-lifecycle.md",
            "docs/00.agent-governance/policies/quality.md",
            "RTK.md",
        }
        lines = baseline.strip().splitlines()
        refs = [
            match.group(1)
            for line in lines[1:-3]
            if (match := re.fullmatch(r"- `([^`]+)`", line))
        ]
        if (
            len(lines) != len(expected) + 4
            or set(refs) != expected
            or len(refs) != len(expected)
            or lines[0] != "Read the following repository files before acting:"
            or lines[-3:]
            != [
                "",
                "Read the selected canonical role and every skill procedure it requires.",
                "Tracked configuration does not establish native discovery or runtime enforcement.",
            ]
        ):
            fail(
                "AGENT-NATIVE-REFERENCE",
                "baseline must contain only current owner reads",
            )
        for ref in refs:
            _read_regular_file(root, ref, code="AGENT-NATIVE-REFERENCE")
    settings = load_json(root, ".claude/settings.json")
    if not isinstance(settings, dict) or set(settings) != {"permissions", "hooks"}:
        fail("AGENT-NATIVE-METADATA", "unsupported native settings")
    if settings["permissions"] != {
        "allow": list(CLAUDE_ALLOWED_PERMISSIONS),
        "deny": list(CLAUDE_REQUIRED_DENY_PERMISSIONS),
    }:
        fail("AGENT-NATIVE-PERMISSION", "permission settings widened or lost denial")
    expected_hook = {
        "PreToolUse": [
            {
                "matcher": "Write|Edit|MultiEdit",
                "hooks": [
                    {
                        "type": "command",
                        "command": 'HY_HOME_K8S_HOOK_PROVIDER=claude bash "$CLAUDE_PROJECT_DIR/.claude/hooks/k8s-pre-edit.sh"',
                        "timeout": 10,
                    }
                ],
            }
        ]
    }
    if settings["hooks"] != expected_hook:
        fail("AGENT-NATIVE-HOOK", "native pre-action guard differs")
    _read_regular_file(root, ".claude/hooks/k8s-pre-edit.sh", code="AGENT-NATIVE-HOOK")
    for provider in registry["providers"]:
        gateway = _read_text(root, provider["gateway"], "AGENT-NATIVE-REFERENCE")
        required = [
            REGISTRY_PATH.as_posix(),
            "docs/00.agent-governance/skills/work-lifecycle.md",
            f"docs/00.agent-governance/providers/{provider['id']}.md",
            f".{provider['id']}/{provider['id'].upper()}.md",
            "RTK.md",
        ]
        if (
            len(gateway.splitlines()) > 30
            or any(ref not in gateway for ref in required)
            or any(
                heading in gateway
                for heading in ("Agent Catalog", "Role Separation", "Runtime Roster")
            )
        ):
            fail(
                "AGENT-NATIVE-REFERENCE",
                "root gateway must remain a thin current router",
            )
        if ".agents/" in gateway:
            fail("AGENT-GOVERNANCE-CONSUMER", "gateway depends on retired root")


def _resolve_root(value: Path) -> Path:
    return _strict_root(value)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the terminal provider-neutral agent registry."
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    try:
        root = _resolve_root(args.root)
        counts = validate_registry(root)
        validate_current_sources(root)
        import agent_governance_consumers

        try:
            agent_governance_consumers.validate_repository(root)
        except agent_governance_consumers.ContractError:
            fail(
                "AGENT-GOVERNANCE-CONSUMER", "historical/current consumer proof failed"
            )
        print(
            "[PASS] agent registry validation passed: "
            + " ".join(
                f"{key}={counts[key]}"
                for key in (
                    "providers",
                    "roles",
                    "permissionClasses",
                    "skills",
                    "handoffs",
                    "projections",
                )
            )
        )
        return 0
    except HarnessError as exc:
        print(f"ERR {exc.code} {exc.detail}", file=sys.stderr)
        return exc.exit_code
    except (KeyError, TypeError, ValueError):
        print("ERR AGENT-REGISTRY-INPUT invalid input", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
