"""Bounded Stage 99 document-authority and lifecycle primitives."""

from __future__ import annotations

import argparse
import json
import os
import re
import selectors
import stat
import subprocess
import sys
import time
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence


REGISTRY_PATH = PurePosixPath("docs/99.templates/registry.json")
REGISTRY_MAX_BYTES = 4 * 1024 * 1024
GIT_TIMEOUT_SECONDS = 10
TOP_LEVEL_KEYS = frozenset(
    {
        "$schema",
        "$id",
        "schemaVersion",
        "profiles",
        "programLineage",
        "referenceCurrentPacks",
        "standaloneExecutions",
    }
)
PROFILE_KEYS = frozenset(
    {
        "id",
        "pathPattern",
        "artifactIdPattern",
        "template",
        "requiredFrontmatter",
        "requiredSections",
        "lifecycle",
        "relationships",
    }
)
ROUTER_PROFILE_KEYS = PROFILE_KEYS - {"artifactIdPattern", "lifecycle"}
AGENT_MACHINE_FIELDS = frozenset(
    {
        "agentRoster",
        "agents",
        "agent",
        "role",
        "roles",
        "permission",
        "permissions",
        "provider",
        "providers",
        "skill",
        "skills",
    }
)
TRANSITION_SUPPORT_PROFILE_IDS = frozenset(
    {"governance/template-support", "template/governance/template-support"}
)
EXPECTED_LIFECYCLE_TRANSITIONS = {
    "requirement-architecture": {
        ("draft", "active"), ("draft", "withdrawn"),
        ("active", "superseded"), ("active", "retired"),
    },
    "adr": {
        ("proposed", "accepted"), ("proposed", "rejected"),
        ("accepted", "superseded"),
    },
    "spec-plan": {
        ("draft", "active"), ("active", "done"),
        ("active", "superseded"), ("active", "withdrawn"),
    },
    "task": {
        ("queued", "in-progress"), ("in-progress", "done"),
        ("in-progress", "cancelled"), ("in-progress", "blocked"),
        ("blocked", "in-progress"),
    },
    "governance-guide-policy-runbook": {
        ("draft", "active"), ("active", "superseded"),
        ("active", "retired"),
    },
    "incident": {
        ("open", "mitigated"), ("mitigated", "resolved"),
        ("resolved", "closed"),
    },
    "postmortem": {("draft", "published"), ("published", "superseded")},
    "research": {
        ("draft", "published"), ("published", "superseded"),
        ("published", "retired"),
    },
    "audit": {("draft", "completed"), ("completed", "invalidated")},
    "data": {
        ("draft", "active"), ("active", "stale"),
        ("stale", "superseded"), ("stale", "retired"),
    },
    "migration-tombstone": {("draft", "sealed")},
    "template-profile": {
        ("draft", "active"), ("active", "superseded"),
        ("active", "retired"),
    },
}


class AuthorityError(ValueError):
    """A deterministic authority, lifecycle, or input-boundary failure."""


def read_bounded_utf8(path: Path, *, max_bytes: int = REGISTRY_MAX_BYTES) -> str:
    """Read one regular non-symlink text file within a reviewed byte bound."""

    if max_bytes <= 0:
        raise AuthorityError("AUTHORITY_SIZE: max_bytes must be positive")
    try:
        mode = path.lstat().st_mode
    except OSError as exc:
        raise AuthorityError(f"AUTHORITY_READ: {path}") from exc
    if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
        raise AuthorityError(f"AUTHORITY_TYPE: {path}")
    try:
        with path.open("rb") as handle:
            raw = handle.read(max_bytes + 1)
    except OSError as exc:
        raise AuthorityError(f"AUTHORITY_READ: {path}") from exc
    if len(raw) > max_bytes:
        raise AuthorityError(f"AUTHORITY_SIZE: {path}")
    try:
        return raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise AuthorityError(f"AUTHORITY_UTF8: {path}") from exc


def load_bounded_json(path: Path, *, max_bytes: int = REGISTRY_MAX_BYTES) -> Any:
    """Load bounded strict UTF-8 JSON while rejecting duplicate object keys."""

    def unique_object(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise AuthorityError(f"AUTHORITY_JSON_DUPLICATE: {key}")
            result[key] = value
        return result

    try:
        return json.loads(
            read_bounded_utf8(path, max_bytes=max_bytes),
            object_pairs_hook=unique_object,
        )
    except json.JSONDecodeError as exc:
        raise AuthorityError(f"AUTHORITY_JSON: {path}") from exc


def _forbidden_agent_field(value: Any) -> str | None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if key in AGENT_MACHINE_FIELDS:
                return str(key)
            found = _forbidden_agent_field(nested)
            if found is not None:
                return found
    elif isinstance(value, list):
        for nested in value:
            found = _forbidden_agent_field(nested)
            if found is not None:
                return found
    return None


def validate_registry_authority(registry: Mapping[str, Any]) -> None:
    """Validate the non-delegable Stage 99 registry authority boundary."""

    actual_keys = frozenset(registry)
    if actual_keys != TOP_LEVEL_KEYS:
        raise AuthorityError(
            "REGISTRY_TOP_LEVEL: expected only " + ", ".join(sorted(TOP_LEVEL_KEYS))
        )
    forbidden = _forbidden_agent_field(registry)
    if forbidden is not None:
        raise AuthorityError(f"STAGE99_AGENT_FIELD: {forbidden}")
    profiles = registry.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        raise AuthorityError("REGISTRY_PROFILES: expected a non-empty list")
    seen: set[str] = set()
    for profile in profiles:
        if not isinstance(profile, Mapping):
            raise AuthorityError("REGISTRY_PROFILE: expected an object")
        profile_id = profile.get("id")
        if not isinstance(profile_id, str) or not profile_id or profile_id in seen:
            raise AuthorityError("REGISTRY_PROFILE_ID: IDs must be unique strings")
        seen.add(profile_id)
        required_keys = (
            ROUTER_PROFILE_KEYS if profile.get("class") == "readme" else PROFILE_KEYS
        )
        if not required_keys.issubset(profile):
            missing = sorted(required_keys - set(profile))
            raise AuthorityError(f"REGISTRY_PROFILE_FIELDS: {profile_id}: {missing}")
        if profile.get("class") == "readme" and (
            "artifactIdPattern" in profile or "lifecycle" in profile
        ):
            raise AuthorityError(f"REGISTRY_ROUTER_FIELDS: {profile_id}")
        path_pattern = profile.get("pathPattern")
        if not isinstance(path_pattern, str):
            raise AuthorityError(f"REGISTRY_PATH_PATTERN: {profile_id}")
        if (
            path_pattern.startswith("^docs/99\\.templates/support/")
            and profile_id not in TRANSITION_SUPPORT_PROFILE_IDS
        ):
            raise AuthorityError(f"STAGE99_SUPPORT_OWNER: {profile_id}")
    lineage = registry.get("programLineage")
    if isinstance(lineage, Mapping):
        domains = lineage.get("lifecycleDomains")
        if not isinstance(domains, list):
            raise AuthorityError("LIFECYCLE_DOMAIN: expected a list")
        actual: dict[str, set[tuple[str, str]]] = {}
        for domain in domains:
            if not isinstance(domain, Mapping) or not isinstance(
                domain.get("family"), str
            ):
                raise AuthorityError("LIFECYCLE_DOMAIN: invalid family")
            states = domain.get("states")
            transitions = domain.get("transitions")
            if not isinstance(states, Mapping) or not isinstance(transitions, list):
                raise AuthorityError("LIFECYCLE_DOMAIN: invalid states or transitions")
            if any(value not in {"mutable", "current", "terminal"} for value in states.values()):
                raise AuthorityError("LIFECYCLE_CLASS: invalid validation class")
            edges = {
                tuple(edge)
                for edge in transitions
                if isinstance(edge, list) and len(edge) == 2
            }
            if len(edges) != len(transitions) or any(
                source not in states or target not in states for source, target in edges
            ):
                raise AuthorityError("LIFECYCLE_TRANSITION: invalid edge")
            actual[domain["family"]] = edges
        if actual != EXPECTED_LIFECYCLE_TRANSITIONS:
            raise AuthorityError("LIFECYCLE_TRANSITION: terminal domains differ")


def validate_template_profile_reference(
    template_text: str,
    registry: Mapping[str, Any],
    *,
    allow_router_without_profile: bool = False,
) -> str:
    """Return a template's profile ID and reject destination-path ownership."""

    if re.search(r"(?im)^\s*<!--\s*(?:destination|target-path)\s*:", template_text):
        raise AuthorityError("TEMPLATE_DESTINATION: use a registry profile ID")
    match = re.search(r"(?m)^type:\s*[\"']?([^\"'\s]+)", template_text)
    if match is None:
        if allow_router_without_profile:
            return ""
        raise AuthorityError("TEMPLATE_PROFILE: missing type/profile ID")
    profile_id = match.group(1)
    profile_ids = {
        item.get("id")
        for item in registry.get("profiles", [])
        if isinstance(item, Mapping)
    }
    if profile_id not in profile_ids:
        raise AuthorityError(f"TEMPLATE_PROFILE: unknown profile {profile_id}")
    return profile_id


def is_lifecycle_transition_allowed(
    lifecycle: Mapping[str, Any], from_state: str, to_state: str
) -> bool:
    """Return whether one registry-declared directed lifecycle edge exists."""

    states = lifecycle.get("states")
    transitions = lifecycle.get("transitions")
    if not isinstance(states, Mapping) or not isinstance(transitions, list):
        return False
    if from_state not in states or to_state not in states:
        return False
    return [from_state, to_state] in transitions


def run_bounded_process(
    arguments: Sequence[str],
    *,
    cwd: Path,
    timeout_seconds: float,
    max_stdout_bytes: int,
    max_stderr_bytes: int = 64 * 1024,
    check: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    """Run one process while draining both pipes incrementally within caps."""

    if timeout_seconds <= 0:
        raise AuthorityError("AUTHORITY_TIMEOUT: timeout must be positive")
    if max_stdout_bytes < 0 or max_stderr_bytes < 0:
        raise AuthorityError("AUTHORITY_SIZE: subprocess limits must be non-negative")
    try:
        process = subprocess.Popen(
            list(arguments),
            cwd=cwd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        raise AuthorityError("AUTHORITY_PROCESS: process could not start") from exc
    assert process.stdout is not None and process.stderr is not None
    streams = selectors.DefaultSelector()
    streams.register(process.stdout, selectors.EVENT_READ, ("stdout", max_stdout_bytes))
    streams.register(process.stderr, selectors.EVENT_READ, ("stderr", max_stderr_bytes))
    chunks: dict[str, list[bytes]] = {"stdout": [], "stderr": []}
    sizes = {"stdout": 0, "stderr": 0}
    deadline = time.monotonic() + timeout_seconds
    try:
        while streams.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise AuthorityError("AUTHORITY_TIMEOUT: subprocess exceeded deadline")
            events = streams.select(remaining)
            if not events:
                raise AuthorityError("AUTHORITY_TIMEOUT: subprocess exceeded deadline")
            for key, _ in events:
                name, limit = key.data
                chunk = os.read(key.fileobj.fileno(), min(64 * 1024, limit - sizes[name] + 1))
                if not chunk:
                    streams.unregister(key.fileobj)
                    continue
                sizes[name] += len(chunk)
                if sizes[name] > limit:
                    raise AuthorityError(f"AUTHORITY_SIZE: subprocess {name} exceeded limit")
                chunks[name].append(chunk)
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise AuthorityError("AUTHORITY_TIMEOUT: subprocess exceeded deadline")
        returncode = process.wait(timeout=remaining)
    except (AuthorityError, subprocess.TimeoutExpired):
        process.kill()
        process.wait()
        if isinstance(sys.exc_info()[1], subprocess.TimeoutExpired):
            raise AuthorityError("AUTHORITY_TIMEOUT: subprocess exceeded deadline")
        raise
    finally:
        streams.close()
        process.stdout.close()
        process.stderr.close()
    stdout = b"".join(chunks["stdout"])
    stderr = b"".join(chunks["stderr"])
    completed = subprocess.CompletedProcess(list(arguments), returncode, stdout, stderr)
    if check and returncode != 0:
        raise subprocess.CalledProcessError(
            returncode, completed.args, output=stdout, stderr=stderr
        )
    return completed


def require_reciprocal_supersession(
    *,
    source: str,
    successor: str,
    source_links: Mapping[str, str],
    successor_links: Mapping[str, str],
) -> None:
    """Require both ends of a mutable-current supersession relation."""

    if (
        source_links.get("superseded_by") != successor
        or successor_links.get("supersedes") != source
    ):
        raise AuthorityError("SUPERSESSION_RECIPROCAL: both links are required")


def staged_authority_bytes(
    root: Path,
    path: PurePosixPath,
    *,
    timeout_seconds: float = GIT_TIMEOUT_SECONDS,
    max_bytes: int = REGISTRY_MAX_BYTES,
) -> bytes:
    """Read one stage-zero authority blob with finite subprocess and byte limits."""

    try:
        completed = run_bounded_process(
            ["git", "show", f":{path.as_posix()}"],
            cwd=root,
            check=True,
            timeout_seconds=timeout_seconds,
            max_stdout_bytes=max_bytes,
        )
    except AuthorityError:
        raise
    except (subprocess.SubprocessError, OSError) as exc:
        raise AuthorityError(f"AUTHORITY_INDEX: {path}") from exc
    try:
        completed.stdout.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise AuthorityError(f"AUTHORITY_UTF8: {path}") from exc
    return completed.stdout


def assert_staged_authority_matches_worktree(
    root: Path,
    path: PurePosixPath = REGISTRY_PATH,
    *,
    timeout_seconds: float = GIT_TIMEOUT_SECONDS,
) -> None:
    """Reject material authority drift between stage zero and the worktree."""

    staged = staged_authority_bytes(
        root, path, timeout_seconds=timeout_seconds, max_bytes=REGISTRY_MAX_BYTES
    )
    worktree = read_bounded_utf8(
        root / path, max_bytes=REGISTRY_MAX_BYTES
    ).encode("utf-8")
    if staged != worktree:
        raise AuthorityError(f"AUTHORITY_DRIFT: {path}")


def main(argv: Sequence[str] | None = None) -> int:
    """Validate the current Stage 99 document authority."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    arguments = parser.parse_args(argv)
    root = Path(arguments.root)
    try:
        registry = load_bounded_json(root / REGISTRY_PATH)
        if not isinstance(registry, Mapping):
            raise AuthorityError("REGISTRY_ROOT: expected an object")
        validate_registry_authority(registry)
        seen_templates: set[str] = set()
        for profile in registry["profiles"]:
            template = profile.get("template")
            if not isinstance(template, str) or template in seen_templates:
                continue
            seen_templates.add(template)
            template_text = read_bounded_utf8(
                root / PurePosixPath(template), max_bytes=1024 * 1024
            )
            validate_template_profile_reference(
                template_text,
                registry,
                allow_router_without_profile=(
                    profile.get("class") == "readme"
                    or profile.get("mode") != "authored"
                ),
            )
    except AuthorityError as exc:
        print(f"FAIL document authority: {exc}", file=sys.stderr)
        return 1
    print("PASS document authority")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
