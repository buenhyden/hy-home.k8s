#!/usr/bin/env python3
"""Validate closed, secret-free provider runtime/config evidence."""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import stat
import sys
from datetime import date, datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn, Sequence

from jsonschema import Draft202012Validator


CONTRACT_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/provider-runtime-evidence.json"
)
SCHEMA_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/provider-runtime-evidence.schema.json"
)
FIXTURE_PATH = PurePosixPath(
    "tests/fixtures/agent-provider-runtime-evidence.json"
)
HARNESS_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/harness-contract.json"
)
ROUTING_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/validation-surfaces.json"
)

CUTOFF_UTC = datetime(2026, 7, 10, 1, 0, 0, tzinfo=timezone.utc)
CUTOFF_UTC_DATE = CUTOFF_UTC.date()
PROVIDER_IDS = ("local", "claude", "codex", "gemini")
SOURCE_PROVIDERS = ("claude", "codex", "gemini", "agency-agents")
SOURCE_IDS = (
    "claude-code-changelog-2-1-206",
    "claude-code-changelog-2-1-154",
    "claude-code-subagents-current",
    "codex-release-0-144-1",
    "codex-release-0-145-0-alpha-2",
    "codex-config-reference-current",
    "gemini-cli-release-0-50-0",
    "gemini-cli-release-0-51-preview-0",
    "gemini-cli-subagents-current",
    "agency-agents-pin-9f3e401c",
)
EVIDENCE_CLASSES = (
    "repo-static",
    "native-discovery",
    "authenticated-run",
)
VERDICTS = ("PASS", "FAIL", "BLOCKED", "ABSENT", "DEFER")
MCP_IDS = (
    "context7",
    "exa",
    "github",
    "memory",
    "playwright",
    "sequential-thinking",
    "supabase",
)
MODEL_GATE_IDS = ("configParse", "runtimeResolution", "spec044Fitness")
ROUTED_SURFACES = (
    "provider-gateways",
    "agent-shared",
    "agent-claude",
    "agent-codex",
    "agent-gemini",
    "governance-documents",
    "scripts",
    "tests",
)
FOCUSED_VALIDATORS = (
    (
        "python3",
        "scripts/validate-agent-provider-config.py",
        "--root",
        ".",
    ),
    (
        "python3",
        "scripts/validate-agent-provider-canaries.py",
        "--root",
        ".",
    ),
)
REQUIRED_PROHIBITED_CONTENT = {
    "api-keys",
    "tokens",
    "account-identifiers",
    "auth-cache-paths",
    "auth-cache-content",
    "private-endpoints",
    "prompt-transcripts",
    "provider-response-bodies",
    "secret-bearing-diagnostics",
    "environment-dumps",
    "shell-history",
    "user-configuration",
}
FORBIDDEN_KEY_NAMES = {
    "apikey",
    "token",
    "accesstoken",
    "refreshtoken",
    "secretvalue",
    "credentialvalue",
    "accountidentifier",
    "accountname",
    "authcachepath",
    "authfilepath",
    "prompttext",
    "prompttranscript",
    "providerresponse",
    "providerresponsebody",
    "environmentdump",
    "shellhistory",
    "privateendpoint",
}
FORBIDDEN_VALUE_FRAGMENTS = (
    "sk-",
    "bearer ",
    "ghp_",
    "aiza",
    "-----begin private key",
)


class ProviderConfigError(ValueError):
    """Typed provider-config contract failure."""

    def __init__(self, code: str, detail: str, *, exit_code: int = 1) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail
        self.exit_code = exit_code


def fail(code: str, detail: str, *, exit_code: int = 1) -> NoReturn:
    raise ProviderConfigError(code, detail, exit_code=exit_code)


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: set[str] = set()
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in seen:
            fail(
                "PNME-DUPLICATE-KEY",
                f"duplicate JSON key {key!r}",
                exit_code=2,
            )
        seen.add(key)
        result[key] = value
    return result


def decode_json_text(text: str, source: str) -> Any:
    try:
        return json.loads(text, object_pairs_hook=no_duplicate_pairs)
    except json.JSONDecodeError as exc:
        fail("PNME-JSON", f"{source}: {exc}", exit_code=2)


DIRECTORY_OPEN_FLAGS = (
    os.O_RDONLY
    | getattr(os, "O_CLOEXEC", 0)
    | getattr(os, "O_DIRECTORY", 0)
    | getattr(os, "O_NOFOLLOW", 0)
)
REGULAR_FILE_OPEN_FLAGS = (
    os.O_RDONLY
    | getattr(os, "O_CLOEXEC", 0)
    | getattr(os, "O_NOFOLLOW", 0)
    | getattr(os, "O_NONBLOCK", 0)
)


def _close_descriptor(descriptor: int) -> None:
    if descriptor < 0:
        return
    try:
        os.close(descriptor)
    except OSError:
        pass


def _same_identity(checked: os.stat_result, opened: os.stat_result) -> bool:
    return (checked.st_dev, checked.st_ino) == (
        opened.st_dev,
        opened.st_ino,
    )


def _open_repository_root(root: Path) -> tuple[Path, int]:
    raw_root = Path(root)
    if any(part == ".." for part in raw_root.parts):
        fail("PNME-INPUT", "repository root is invalid", exit_code=2)
    try:
        absolute_root = Path(os.path.abspath(os.fspath(raw_root)))
    except (OSError, TypeError, ValueError):
        fail("PNME-INPUT", "repository root is unavailable", exit_code=2)

    root_descriptor = -1
    next_descriptor = -1
    try:
        anchor = Path(absolute_root.anchor)
        try:
            checked = os.lstat(anchor)
        except OSError:
            fail("PNME-INPUT", "repository root is unavailable", exit_code=2)
        if stat.S_ISLNK(checked.st_mode) or not stat.S_ISDIR(checked.st_mode):
            fail(
                "PNME-INPUT",
                "repository root is not a real directory",
                exit_code=2,
            )
        try:
            root_descriptor = os.open(anchor, DIRECTORY_OPEN_FLAGS)
            opened = os.fstat(root_descriptor)
        except OSError:
            fail("PNME-INPUT", "repository root is unavailable", exit_code=2)
        if not stat.S_ISDIR(opened.st_mode) or not _same_identity(
            checked,
            opened,
        ):
            fail(
                "PNME-INPUT",
                "repository root identity changed",
                exit_code=2,
            )

        for part in absolute_root.parts[1:]:
            try:
                checked = os.lstat(part, dir_fd=root_descriptor)
            except OSError:
                fail(
                    "PNME-INPUT",
                    "repository root is unavailable",
                    exit_code=2,
                )
            if stat.S_ISLNK(checked.st_mode):
                fail(
                    "PNME-INPUT",
                    "repository root path contains a symlink",
                    exit_code=2,
                )
            if not stat.S_ISDIR(checked.st_mode):
                fail(
                    "PNME-INPUT",
                    "repository root is not a real directory",
                    exit_code=2,
                )
            try:
                next_descriptor = os.open(
                    part,
                    DIRECTORY_OPEN_FLAGS,
                    dir_fd=root_descriptor,
                )
                opened = os.fstat(next_descriptor)
            except OSError:
                fail(
                    "PNME-INPUT",
                    "repository root is unavailable",
                    exit_code=2,
                )
            if not stat.S_ISDIR(opened.st_mode) or not _same_identity(
                checked,
                opened,
            ):
                fail(
                    "PNME-INPUT",
                    "repository root identity changed",
                    exit_code=2,
                )
            _close_descriptor(root_descriptor)
            root_descriptor = next_descriptor
            next_descriptor = -1

        try:
            real_root = Path(os.path.realpath(absolute_root, strict=True))
        except (OSError, TypeError, ValueError):
            fail("PNME-INPUT", "repository root is unavailable", exit_code=2)
        if real_root != absolute_root:
            fail(
                "PNME-INPUT",
                "repository root path is not real",
                exit_code=2,
            )
        result_descriptor = root_descriptor
        root_descriptor = -1
        return absolute_root, result_descriptor
    finally:
        _close_descriptor(next_descriptor)
        _close_descriptor(root_descriptor)


def _resolve_repository_root(root: Path) -> Path:
    absolute_root, descriptor = _open_repository_root(root)
    _close_descriptor(descriptor)
    return absolute_root


def _canonical_relative_path(
    relative: PurePosixPath | str,
) -> PurePosixPath:
    raw = os.fspath(relative)
    path = PurePosixPath(raw)
    if (
        not raw
        or path.is_absolute()
        or raw != path.as_posix()
        or "\\" in raw
        or not path.parts
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        fail("PNME-INPUT", "governed input path is invalid", exit_code=2)
    return path


def _open_governed_node(
    root: Path,
    relative: PurePosixPath | str,
    *,
    expected_kind: str,
) -> int | None:
    if expected_kind not in {"file", "directory", "absent"}:
        fail("PNME-INPUT", "governed input kind is invalid", exit_code=2)
    canonical = _canonical_relative_path(relative)
    _, parent_descriptor = _open_repository_root(root)
    next_descriptor = -1
    final_descriptor = -1
    try:
        for index, part in enumerate(canonical.parts):
            final_component = index == len(canonical.parts) - 1
            try:
                checked = os.lstat(part, dir_fd=parent_descriptor)
            except FileNotFoundError:
                if expected_kind == "absent":
                    return None
                fail(
                    "PNME-INPUT",
                    "governed input is unavailable",
                    exit_code=2,
                )
            except OSError:
                fail(
                    "PNME-INPUT",
                    "governed input is unavailable",
                    exit_code=2,
                )

            if not final_component:
                if stat.S_ISLNK(checked.st_mode) or not stat.S_ISDIR(
                    checked.st_mode
                ):
                    fail(
                        "PNME-INPUT",
                        "governed input parent is not a real directory",
                        exit_code=2,
                    )
                try:
                    next_descriptor = os.open(
                        part,
                        DIRECTORY_OPEN_FLAGS,
                        dir_fd=parent_descriptor,
                    )
                    opened = os.fstat(next_descriptor)
                except FileNotFoundError:
                    if expected_kind == "absent":
                        return None
                    fail(
                        "PNME-INPUT",
                        "governed input is unavailable",
                        exit_code=2,
                    )
                except OSError:
                    fail(
                        "PNME-INPUT",
                        "governed input is unavailable",
                        exit_code=2,
                    )
                if not stat.S_ISDIR(opened.st_mode) or not _same_identity(
                    checked,
                    opened,
                ):
                    fail(
                        "PNME-INPUT",
                        "governed input parent identity changed",
                        exit_code=2,
                    )
                _close_descriptor(parent_descriptor)
                parent_descriptor = next_descriptor
                next_descriptor = -1
                continue

            if expected_kind == "absent":
                fail(
                    "PNME-INPUT",
                    "declared-absent input has an existing final node",
                    exit_code=2,
                )
            if stat.S_ISLNK(checked.st_mode):
                fail(
                    "PNME-INPUT",
                    "governed input final node is a symlink",
                    exit_code=2,
                )
            if expected_kind == "file" and not stat.S_ISREG(checked.st_mode):
                fail(
                    "PNME-INPUT",
                    "governed input final node is not a regular file",
                    exit_code=2,
                )
            if expected_kind == "directory" and not stat.S_ISDIR(
                checked.st_mode
            ):
                fail(
                    "PNME-INPUT",
                    "governed input final node is not a real directory",
                    exit_code=2,
                )
            flags = (
                REGULAR_FILE_OPEN_FLAGS
                if expected_kind == "file"
                else DIRECTORY_OPEN_FLAGS
            )
            try:
                final_descriptor = os.open(
                    part,
                    flags,
                    dir_fd=parent_descriptor,
                )
                opened = os.fstat(final_descriptor)
            except OSError:
                fail(
                    "PNME-INPUT",
                    "governed input is unavailable",
                    exit_code=2,
                )
            expected_mode = (
                stat.S_ISREG(opened.st_mode)
                if expected_kind == "file"
                else stat.S_ISDIR(opened.st_mode)
            )
            if not expected_mode or not _same_identity(checked, opened):
                fail(
                    "PNME-INPUT",
                    "governed input final identity changed",
                    exit_code=2,
                )
            result_descriptor = final_descriptor
            final_descriptor = -1
            return result_descriptor
    finally:
        _close_descriptor(final_descriptor)
        _close_descriptor(next_descriptor)
        _close_descriptor(parent_descriptor)

    fail("PNME-INPUT", "governed input path is invalid", exit_code=2)


def _inspect_governed_node(
    root: Path,
    relative: PurePosixPath | str,
    *,
    expected_kind: str,
) -> None:
    descriptor = _open_governed_node(
        root,
        relative,
        expected_kind=expected_kind,
    )
    if descriptor is not None:
        _close_descriptor(descriptor)


def _read_regular_text(root: Path, relative: PurePosixPath | str) -> str:
    descriptor = _open_governed_node(root, relative, expected_kind="file")
    if descriptor is None:
        fail("PNME-INPUT", "governed input is unavailable", exit_code=2)
    try:
        with os.fdopen(descriptor, "r", encoding="utf-8") as stream:
            descriptor = -1
            return stream.read()
    except ProviderConfigError:
        raise
    except (OSError, UnicodeError):
        fail(
            "PNME-INPUT",
            "governed input cannot be read as UTF-8",
            exit_code=2,
        )
    finally:
        _close_descriptor(descriptor)


def load_json(root: Path, relative: PurePosixPath) -> Any:
    return decode_json_text(_read_regular_text(root, relative), str(relative))


def schema_errors(contract: Any, schema: Any) -> list[str]:
    validator = Draft202012Validator(schema)
    return [
        f"{'/'.join(str(part) for part in error.path) or '<root>'}: "
        f"{error.message}"
        for error in sorted(validator.iter_errors(contract), key=str)
    ]


def validate_schema(root: Path, contract: dict[str, Any]) -> None:
    schema = load_json(root, SCHEMA_PATH)
    errors = schema_errors(contract, schema)
    if errors:
        fail("PNME-SCHEMA", "; ".join(errors[:8]))


def _normalized_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", key.lower())


def validate_sensitive_content(value: Any, path: str = "<root>") -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            if _normalized_key(key) in FORBIDDEN_KEY_NAMES:
                fail(
                    "PNME-SENSITIVE-CONTENT",
                    f"forbidden durable key at {path}/{key}",
                )
            validate_sensitive_content(nested, f"{path}/{key}")
        return
    if isinstance(value, list):
        for index, nested in enumerate(value):
            validate_sensitive_content(nested, f"{path}/{index}")
        return
    if isinstance(value, str):
        lowered = value.lower()
        for fragment in FORBIDDEN_VALUE_FRAGMENTS:
            if fragment in lowered:
                fail(
                    "PNME-SENSITIVE-CONTENT",
                    f"secret-like value at {path}",
                )


def validate_sources(contract: dict[str, Any]) -> None:
    ledger = contract["sourceLedger"]
    source_ids = [source["id"] for source in ledger]
    if len(source_ids) != len(set(source_ids)):
        fail("PNME-SOURCE-DUPLICATE", "source ledger IDs must be unique")
    if tuple(source_ids) != SOURCE_IDS:
        fail(
            "PNME-SOURCE-SET",
            f"expected fixed source ledger {SOURCE_IDS}, got {tuple(source_ids)}",
        )

    observed_providers = {source["provider"] for source in ledger}
    missing = set(SOURCE_PROVIDERS).difference(observed_providers)
    if missing:
        fail(
            "PNME-SOURCE-COVERAGE",
            f"missing official/comparison providers: {sorted(missing)}",
    )

    for source in ledger:
        try:
            source_date = date.fromisoformat(source["sourceDate"])
        except ValueError:
            fail(
                "PNME-SOURCE-CUTOFF",
                f"{source['id']} has invalid source date",
            )
        published_at_raw = source["publishedAtUtc"]
        published_at: datetime | None = None
        if published_at_raw is not None:
            try:
                published_at = datetime.strptime(
                    published_at_raw, "%Y-%m-%dT%H:%M:%SZ"
                ).replace(tzinfo=timezone.utc)
            except ValueError:
                fail(
                    "PNME-SOURCE-CUTOFF",
                    f"{source['id']} has invalid UTC publication timestamp",
                )
            if published_at.date() != source_date:
                fail(
                    "PNME-SOURCE-CUTOFF",
                    f"{source['id']} publication timestamp/date disagree",
                )
        classification = source["cutoffApplicability"]
        confidence = source["confidence"]
        basis = source["dateBasis"]
        if classification == "cutoff-applicable":
            if published_at is not None and published_at > CUTOFF_UTC:
                fail(
                    "PNME-SOURCE-CUTOFF",
                    f"{source['id']} is after cutoff but classified applicable",
                )
            if published_at is None and source_date >= CUTOFF_UTC_DATE:
                fail(
                    "PNME-SOURCE-CUTOFF",
                    f"{source['id']} needs exact UTC time on the cutoff date",
                )
            if confidence != "dated-primary" or basis == "observed":
                fail(
                    "PNME-SOURCE-CUTOFF",
                    f"{source['id']} lacks dated release/commit confidence",
                )
        elif classification == "current-only":
            if confidence != "current-primary" or basis != "observed":
                fail(
                    "PNME-SOURCE-CUTOFF",
                    f"{source['id']} current-only confidence/date basis drifted",
                )
        elif classification == "post-cutoff":
            if published_at is not None and published_at <= CUTOFF_UTC:
                fail(
                    "PNME-SOURCE-CUTOFF",
                    f"{source['id']} is not after the cutoff",
                )
            if published_at is None and source_date <= CUTOFF_UTC_DATE:
                fail(
                    "PNME-SOURCE-CUTOFF",
                    f"{source['id']} needs exact UTC time on the cutoff date",
                )


def provider_map(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    observed = [provider["id"] for provider in contract["providers"]]
    if observed != list(PROVIDER_IDS):
        fail(
            "PNME-PROVIDER-ORDER",
            f"expected {PROVIDER_IDS}, got {observed}",
        )
    return {
        provider["id"]: provider
        for provider in contract["providers"]
    }


def validate_repo_path(raw_path: str, field: str) -> PurePosixPath:
    path = PurePosixPath(raw_path)
    if (
        path.is_absolute()
        or raw_path != path.as_posix()
        or any(part in {"", ".", ".."} for part in path.parts)
        or "\\" in raw_path
    ):
        fail("PNME-PATH", f"{field} must be a canonical repo-relative path")
    return path


def validate_observations(providers: dict[str, dict[str, Any]], contract: dict[str, Any]) -> None:
    expected_current = {
        "claude": ("present", "2.1.220 (Claude Code)"),
        "codex": ("present", "codex-cli 0.140.0"),
        "gemini": ("absent", None),
    }
    for provider_id, (installation, version) in expected_current.items():
        observation = providers[provider_id]["localObservation"]
        if (
            observation["installation"],
            observation["version"],
            observation["observedAt"],
            observation["userReported"],
            observation["readinessClaim"],
        ) != (installation, version, "2026-07-28", False, False):
            fail(
                "PNME-LOCAL-OBSERVATION",
                f"{provider_id} current local observation drifted",
            )

    prior = contract["observationHistory"]
    matching = [
        item
        for item in prior
        if item["observationClass"] == "prior-user-report"
        and item["providers"]["codex"]["version"]
        == "codex-cli 0.145.0-alpha.27"
        and item["providers"]["claude"]["installation"] == "absent"
        and item["providers"]["gemini"]["installation"] == "absent"
        and item["readinessClaim"] is False
    ]
    if len(matching) != 1:
        fail(
            "PNME-LOCAL-OBSERVATION",
            "prior user-reported Codex alpha/Claude absent state must be preserved once",
        )


def validate_surface_parity(
    root: Path,
    providers: dict[str, dict[str, Any]],
    *,
    check_paths: bool,
) -> dict[str, Any]:
    harness = load_json(root, HARNESS_PATH)
    harness_surfaces = {
        surface["id"]: surface
        for surface in harness["surfaces"]
    }
    if tuple(harness_surfaces) != PROVIDER_IDS:
        fail(
            "PNME-HARNESS-PARITY",
            f"harness surfaces drifted: {tuple(harness_surfaces)}",
        )

    for provider_id in PROVIDER_IDS:
        provider = providers[provider_id]
        surface = provider["trackedSurface"]
        surface_path_root = validate_repo_path(
            surface["pathRoot"], f"{provider_id}.trackedSurface.pathRoot"
        )
        harness_surface = harness_surfaces[provider_id]
        expected = (
            harness_surface["pathRoot"],
            harness_surface["admissionState"],
            harness_surface["evidenceClass"],
        )
        actual = (
            surface["pathRoot"],
            surface["state"],
            surface["evidenceClass"],
        )
        if actual != expected:
            fail(
                "PNME-SURFACE-PARITY",
                f"{provider_id} expected {expected}, got {actual}",
            )
        if surface["state"] == "current" and surface["presence"] != "present":
            fail(
                "PNME-SURFACE-PARITY",
                f"{provider_id} current surface must be declared present",
            )

        project_paths = [
            (
                item,
                validate_repo_path(
                    item["path"], f"{provider_id}.projectPaths.path"
                ),
            )
            for item in provider["projectPaths"]
        ]
        if len({path for _, path in project_paths}) != len(project_paths):
            fail(
                "PNME-PATH",
                f"{provider_id}.projectPaths contains duplicate paths",
            )

        if check_paths:
            _inspect_governed_node(
                root,
                surface_path_root,
                expected_kind=(
                    "directory"
                    if surface["presence"] == "present"
                    else "absent"
                ),
            )

            for item, relative_item_path in project_paths:
                expected_kind = "absent"
                if item["state"] == "current":
                    expected_kind = (
                        "directory"
                        if item["kind"] == "role-directory"
                        else "file"
                    )
                _inspect_governed_node(
                    root,
                    relative_item_path,
                    expected_kind=expected_kind,
                )

    if providers["local"]["trackedSurface"]["pathRoot"] != ".agents/agents":
        fail(
            "PNME-SURFACE-PARITY",
            ".agents must remain the local projection",
        )
    if providers["gemini"]["trackedSurface"]["pathRoot"] != ".gemini/agents":
        fail(
            "PNME-SURFACE-PARITY",
            "Gemini native projection must remain under .gemini",
        )
    if (
        check_paths
        and providers["gemini"]["trackedSurface"]["state"] != "current"
    ):
        _inspect_governed_node(
            root,
            PurePosixPath(".gemini"),
            expected_kind="absent",
        )
    return harness


def validate_evidence_lanes(providers: dict[str, dict[str, Any]]) -> None:
    runtime_keys = {
        "repo-static": "repoStatic",
        "native-discovery": "nativeDiscovery",
        "authenticated-run": "authenticatedRun",
    }
    for provider_id, provider in providers.items():
        lanes = provider["evidenceLanes"]
        observed = [lane["id"] for lane in lanes]
        if observed != list(EVIDENCE_CLASSES):
            fail(
                "PNME-EVIDENCE-LANE",
                f"{provider_id} lane order/coverage drifted: {observed}",
            )
        for lane in lanes:
            if lane["verdict"] not in VERDICTS:
                fail(
                    "PNME-EVIDENCE-LANE",
                    f"{provider_id}/{lane['id']} has invalid verdict",
                )
            if lane["crossLanePromotion"] is not False:
                fail(
                    "PNME-EVIDENCE-LANE",
                    f"{provider_id}/{lane['id']} permits cross-lane promotion",
                )
            if (
                provider["runtimeVerdicts"][runtime_keys[lane["id"]]]
                != lane["verdict"]
            ):
                fail(
                    "PNME-EVIDENCE-LANE",
                    f"{provider_id}/{lane['id']} compatibility verdict drifted",
                )
            if lane["verdict"] != "PASS" and (
                not lane["owner"]
                or not lane["limitation"]
                or not lane["retryTrigger"]
            ):
                fail(
                    "PNME-EVIDENCE-LANE",
                    f"{provider_id}/{lane['id']} limitation is not actionable",
                )

        by_id = {lane["id"]: lane["verdict"] for lane in lanes}
        if (
            by_id["authenticated-run"] == "PASS"
            and by_id["native-discovery"] != "PASS"
        ):
            fail(
                "PNME-EVIDENCE-LANE",
                f"{provider_id} authenticated PASS lacks discovery PASS",
            )
        if (
            by_id["native-discovery"] == "PASS"
            and by_id["repo-static"] != "PASS"
        ):
            fail(
                "PNME-EVIDENCE-LANE",
                f"{provider_id} discovery PASS lacks repo-static PASS",
            )


def validate_models(contract: dict[str, Any], providers: dict[str, dict[str, Any]]) -> None:
    source_ids = {source["id"] for source in contract["sourceLedger"]}
    for provider_id, provider in providers.items():
        candidates = provider["modelCandidates"]
        if [item["roleClass"] for item in candidates] != [
            "planning-supervisor",
            "worker-subagent",
        ]:
            fail(
                "PNME-MODEL-GATE",
                f"{provider_id} role-class candidate coverage drifted",
            )
        for candidate in candidates:
            missing_sources = set(candidate["sourceIds"]).difference(source_ids)
            if missing_sources:
                fail(
                    "PNME-MODEL-GATE",
                    f"{provider_id} references unknown sources {sorted(missing_sources)}",
                )
            if candidate["promotionState"] != "candidate-only":
                fail(
                    "PNME-MODEL-GATE",
                    f"{provider_id} candidate was promoted",
                )
            if candidate["fallback"]["silentFallbackAllowed"]:
                fail(
                    "PNME-MODEL-GATE",
                    f"{provider_id} candidate permits silent fallback",
                )
            if set(candidate["gates"]) != set(MODEL_GATE_IDS):
                fail(
                    "PNME-MODEL-GATE",
                    f"{provider_id} model gates are incomplete",
                )
            if candidate["idResolution"] == "configured-only" and (
                candidate["configuredId"] is None
                or candidate["observedId"] is not None
            ):
                fail(
                    "PNME-MODEL-GATE",
                    f"{provider_id} configured-only ID boundary drifted",
                )
            if candidate["idResolution"] == "unresolved" and (
                candidate["observedId"] is not None
            ):
                fail(
                    "PNME-MODEL-GATE",
                    f"{provider_id} unresolved candidate has observed ID",
                )
            if candidate["idResolution"] == "resolved" and (
                candidate["configuredId"] is None
                or candidate["observedId"] is None
                or candidate["gates"]["runtimeResolution"] != "PASS"
            ):
                fail(
                    "PNME-MODEL-GATE",
                    f"{provider_id} resolved candidate lacks exact runtime evidence",
                )
            if candidate["fallback"]["observedId"] is not None:
                fail(
                    "PNME-MODEL-GATE",
                    f"{provider_id} candidate records unapproved fallback",
                )


def validate_mcp_inventory(
    contract: dict[str, Any],
    harness: dict[str, Any],
) -> None:
    inventory = contract["mcpInventory"]
    ids = [server["id"] for server in inventory]
    if tuple(ids) != MCP_IDS or len(ids) != len(set(ids)):
        fail(
            "PNME-MCP-BOUNDARY",
            f"expected MCP inventory {MCP_IDS}, got {ids}",
        )
    allowed_roles = set(harness["targetInventory"]["roleIds"])
    for server in inventory:
        unknown = set(server["allowedRoles"]).difference(allowed_roles)
        if unknown:
            fail(
                "PNME-MCP-BOUNDARY",
                f"{server['id']} allows unknown roles {sorted(unknown)}",
            )
        if server["credentialClass"] not in {
            "none",
            "environment-reference",
            "provider-managed-auth",
        }:
            fail(
                "PNME-MCP-BOUNDARY",
                f"{server['id']} credential class is not declarative",
            )
        if server["runtimeState"] == "PASS":
            fail(
                "PNME-MCP-BOUNDARY",
                f"{server['id']} cannot claim runtime PASS without a canary",
            )


def validate_canary_policy(contract: dict[str, Any]) -> None:
    policy = contract["canaryRecordContract"]
    if tuple(policy["allowedVerdicts"]) != VERDICTS:
        fail("PNME-CANARY-POLICY", "allowed verdicts drifted")
    if tuple(policy["requiredEvidenceClasses"]) != EVIDENCE_CLASSES:
        fail("PNME-CANARY-POLICY", "required evidence classes drifted")
    if (
        policy["redactionRequired"] is not True
        or policy["syntheticTaskRequired"] is not True
        or policy["mutationMode"] != "no-mutation"
        or policy["crossLanePromotionAllowed"] is not False
    ):
        fail("PNME-CANARY-POLICY", "safe canary policy drifted")
    missing = REQUIRED_PROHIBITED_CONTENT.difference(
        policy["prohibitedDurableContent"]
    )
    if missing:
        fail(
            "PNME-CANARY-POLICY",
            f"missing prohibited content classes {sorted(missing)}",
        )


def validate_routing(root: Path, contract: dict[str, Any]) -> None:
    route = contract["routeIntegration"]
    if tuple(tuple(argv) for argv in route["focusedValidators"]) != FOCUSED_VALIDATORS:
        fail("PNME-ROUTING", "focused validator commands drifted")
    if tuple(route["surfaces"]) != ROUTED_SURFACES:
        fail("PNME-ROUTING", "provider evidence surfaces drifted")
    if not {"infrastructure", "gitops", "vault", "remote-live"}.issubset(
        route["excludedSurfaces"]
    ):
        fail("PNME-ROUTING", "protected/live exclusions are incomplete")

    routing = load_json(root, ROUTING_PATH)
    registrations = [
        item
        for item in routing["validators"]
        if item["id"] == route["validatorId"]
    ]
    if len(registrations) != 1:
        fail("PNME-ROUTING", "agent-provider-evidence route must be unique")
    if registrations[0]["argv"] != route["argv"]:
        fail("PNME-ROUTING", "registered provider evidence argv drifted")
    routed = tuple(
        surface["id"]
        for surface in routing["surfaces"]
        if route["validatorId"] in surface["validators"]
    )
    if routed != ROUTED_SURFACES:
        fail("PNME-ROUTING", f"registered surfaces drifted: {routed}")


def validate_contract(
    root: Path,
    contract: dict[str, Any] | None = None,
    *,
    check_paths: bool = True,
) -> dict[str, int]:
    root = _resolve_repository_root(root)
    if contract is None:
        contract = load_json(root, CONTRACT_PATH)
    validate_schema(root, contract)
    validate_sensitive_content(contract)
    validate_sources(contract)
    providers = provider_map(contract)
    validate_observations(providers, contract)
    harness = validate_surface_parity(
        root,
        providers,
        check_paths=check_paths,
    )
    validate_evidence_lanes(providers)
    validate_models(contract, providers)
    validate_mcp_inventory(contract, harness)
    validate_canary_policy(contract)
    if check_paths:
        validate_routing(root, contract)
    return {
        "providers": len(providers),
        "sources": len(contract["sourceLedger"]),
        "modelCandidates": sum(
            len(provider["modelCandidates"])
            for provider in providers.values()
        ),
        "mcpServers": len(contract["mcpInventory"]),
    }


def apply_mutation(contract: dict[str, Any], name: str) -> None:
    if name == "unknown-top-level-key":
        contract["unexpected"] = True
    elif name == "cutoff-source-after-cutoff":
        contract["sourceLedger"][0]["sourceDate"] = "2026-07-11"
    elif name == "cutoff-source-same-day-after-cutoff":
        contract["sourceLedger"][0]["sourceDate"] = "2026-07-10"
        contract["sourceLedger"][0][
            "publishedAtUtc"
        ] = "2026-07-10T01:00:01Z"
    elif name == "source-id-substitution":
        contract["sourceLedger"][0]["id"] = "replacement-source-id"
    elif name == "extra-source-new-id":
        extra = copy.deepcopy(contract["sourceLedger"][0])
        extra["id"] = "extra-source-new-id"
        contract["sourceLedger"].append(extra)
    elif name == "absolute-project-path":
        contract["providers"][1]["projectPaths"][0]["path"] = "/etc/passwd"
    elif name == "invalid-calendar-source-date":
        contract["sourceLedger"][0]["sourceDate"] = "2026-02-30"
    elif name == "gemini-current-while-absent":
        contract["providers"][3]["trackedSurface"]["presence"] = "absent"
    elif name == "agents-relabeled-as-gemini":
        contract["providers"][0]["trackedSurface"]["pathRoot"] = ".gemini/agents"
    elif name == "model-silent-fallback-enabled":
        contract["providers"][2]["modelCandidates"][0]["fallback"][
            "silentFallbackAllowed"
        ] = True
    elif name == "model-fitness-promoted-without-gates":
        contract["providers"][2]["modelCandidates"][0][
            "promotionState"
        ] = "current-assignment"
    elif name == "mcp-role-outside-harness":
        contract["mcpInventory"][0]["allowedRoles"].append("unowned-agent")
    elif name == "secret-like-contract-value":
        contract["sourceLedger"][0]["claim"] = "sk-test-not-a-real-secret"
    else:
        fail("PNME-FIXTURE", f"unknown config mutation {name}")


def validate_fixture(root: Path) -> int:
    contract = load_json(root, CONTRACT_PATH)
    fixture = load_json(root, FIXTURE_PATH)
    cases = fixture["configMutations"]
    for case in cases:
        mutated = copy.deepcopy(contract)
        apply_mutation(mutated, case["name"])
        try:
            validate_contract(root, mutated, check_paths=True)
        except ProviderConfigError as exc:
            if exc.code != case["expectedRule"]:
                fail(
                    "PNME-FIXTURE",
                    f"{case['name']} expected {case['expectedRule']} got {exc.code}",
                )
        else:
            fail("PNME-FIXTURE", f"{case['name']} unexpectedly passed")
    return len(cases)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate provider runtime/config evidence."
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.root)
    try:
        cases = validate_fixture(root) if args.self_test else 0
        counts = validate_contract(root)
        if args.self_test:
            print(
                "[PASS] agent provider config self-test passed: "
                f"cases={cases} providers={counts['providers']} "
                f"sources={counts['sources']} "
                f"models={counts['modelCandidates']} "
                f"mcp={counts['mcpServers']}"
            )
        else:
            print(
                "[PASS] agent provider config validation passed: "
                f"providers={counts['providers']} "
                f"sources={counts['sources']} "
                f"models={counts['modelCandidates']} "
                f"mcp={counts['mcpServers']}"
            )
        return 0
    except ProviderConfigError as exc:
        print(f"{exc.code}: {exc.detail}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
