#!/usr/bin/env python3
"""Validate the repository-static AGQC-003 legacy consumer cutover."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import stat
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn

from jsonschema import Draft202012Validator


CONTRACT_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-legacy-cutover.json"
)
SCHEMA_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-legacy-cutover.schema.json"
)
FIXTURE_PATH = PurePosixPath("tests/fixtures/agent-legacy-cutover.json")
FIXTURE_SHA256 = (
    "98a1ed58b552bfb8b6158a571161b617c6ca0573ba7c480f3a8ac1e229ab3af1"  # pragma: allowlist secret
)

SCHEMA_VERSION = 1
CONTRACT_VERSION = "1.0.0"
OWNER_SPEC = "docs/03.specs/045-agent-governance-ci-qa-cutover/spec.md"
RIA_SNAPSHOT_SOURCE_COMMIT = (
    "8fb9821497aaa93d9ed5fc1a69b60c628b047b47"  # pragma: allowlist secret
)
RESULT_VOCABULARY = ("PASS", "FAIL")
EVIDENCE_VOCABULARY = ("repo-static",)
RETIRED_SURFACES = (
    "docs/00.agent-governance/contracts/agent-role-semantics.json",
    "docs/00.agent-governance/contracts/agent-role-semantics.schema.json",
    "scripts/validate-agent-role-semantics.py",
    "tests/fixtures/agent-role-semantics.json",
    ".github/ABOUT.md",
)
REPLACEMENT_SURFACES = (
    "docs/00.agent-governance/contracts/harness-contract.json",
    "docs/00.agent-governance/contracts/harness-contract.schema.json",
    "scripts/validate-agent-harness-semantics.py",
    "tests/fixtures/agent-harness-semantics.json",
    ".github/README.md",
)
HARNESS_CUTOVER = {
    "contractPath": REPLACEMENT_SURFACES[0],
    "schemaPath": REPLACEMENT_SURFACES[1],
    "consumersKey": "consumers",
    "selectedConsumer": {
        "id": "harness-semantics-validator",
        "path": REPLACEMENT_SURFACES[2],
    },
    "retiredConsumerIds": ["role-semantics-validator"],
    "forbiddenTopLevelKeys": ["compatibility"],
}
CURRENT_AUTHORITY_MIGRATIONS = (
    {
        "path": (
            "docs/90.references/research/2026-07-07-wer/"
            "automation-pipeline-workflow-qa.md"
        ),
        "from": RETIRED_SURFACES[4],
        "to": REPLACEMENT_SURFACES[4],
        "count": 3,
    },
    {
        "path": (
            "docs/90.references/research/2026-07-07-wer/"
            "document-migration-evidence-ledger.md"
        ),
        "from": RETIRED_SURFACES[4],
        "to": REPLACEMENT_SURFACES[4],
        "count": 3,
    },
    {
        "path": (
            "docs/90.references/research/2026-07-07-wer/"
            "kubernetes-infrastructure-security.md"
        ),
        "from": RETIRED_SURFACES[4],
        "to": REPLACEMENT_SURFACES[4],
        "count": 1,
    },
    {
        "path": (
            "docs/90.references/research/2026-07-07-wer/"
            "workspace-governance-baseline.md"
        ),
        "from": RETIRED_SURFACES[4],
        "to": REPLACEMENT_SURFACES[4],
        "count": 2,
    },
)
PACKAGE_REFERENCES = (
    CONTRACT_PATH.as_posix(),
    SCHEMA_PATH.as_posix(),
    "scripts/validate-agent-legacy-cutover.py",
    "scripts/validate-links-and-owners.py",
    FIXTURE_PATH.as_posix(),
    "tests/test_validate_agent_legacy_cutover.py",
    "docs/90.references/data/reference-information-architecture.json",
    "docs/90.references/data/reference-information-architecture.schema.json",
    "scripts/reference_information_architecture.py",
    "tests/test_reference_information_architecture.py",
)
MIGRATION_REFERENCES = (
    OWNER_SPEC,
    "docs/00.agent-governance/memory/progress.md",
)
ALLOWED_REFERENCE_COUNTS = (
    (CONTRACT_PATH.as_posix(), (1, 1, 1, 2, 9)),
    (SCHEMA_PATH.as_posix(), (0, 0, 0, 0, 0)),
    ("scripts/validate-agent-legacy-cutover.py", (1, 1, 1, 1, 1)),
    ("scripts/validate-links-and-owners.py", (1, 1, 1, 1, 4)),
    (FIXTURE_PATH.as_posix(), (1, 0, 0, 1, 1)),
    ("tests/test_validate_agent_legacy_cutover.py", (1, 0, 1, 0, 0)),
    (
        "docs/90.references/data/reference-information-architecture.json",
        (0, 0, 0, 0, 0),
    ),
    (
        "docs/90.references/data/reference-information-architecture.schema.json",
        (0, 0, 0, 0, 0),
    ),
    ("scripts/reference_information_architecture.py", (0, 0, 0, 0, 1)),
    ("tests/test_reference_information_architecture.py", (0, 0, 0, 0, 4)),
    (OWNER_SPEC, (1, 0, 1, 1, 4)),
    ("docs/00.agent-governance/memory/progress.md", (0, 0, 0, 0, 9)),
)
PROTECTED_EVIDENCE_FILES = (
    {
        "path": "docs/90.references/data/active-corpus-retention-census.json",
        "sha256": "d7052fac94af246d5254052935bc49e4a9070b06cb99160902a7e83dc7aad3e3",  # pragma: allowlist secret
        "evidenceKind": "pinned-activation-snapshot",
        "lifecycleStatus": "superseded",
        "observedAt": "2026-07-18",
        "sourceCommit": "9e2ec37f483145b322cf68a2f6e697dcf4fb80e1",  # pragma: allowlist secret
        "retiredReference": RETIRED_SURFACES[3],
        "supersededBy": REPLACEMENT_SURFACES[3],
        "count": 1,
    },
    {
        "path": (
            "docs/90.references/audits/2026-07-05-wea/"
            "sdlc-ci-qa-formatting-automation.md"
        ),
        "sha256": "c81e25e2346241c4ffcb83fb073ba2d7c147541dbfeadd0bdeb21bc13e004bb8",  # pragma: allowlist secret
        "evidenceKind": "pinned-ria-snapshot",
        "lifecycleStatus": "superseded",
        "observedAt": "2026-07-05",
        "sourceCommit": RIA_SNAPSHOT_SOURCE_COMMIT,
        "retiredReference": RETIRED_SURFACES[4],
        "supersededBy": REPLACEMENT_SURFACES[4],
        "count": 12,
    },
    {
        "path": (
            "docs/90.references/audits/2026-07-03-wdgh/"
            "workspace-document-governance-hardening-audit.md"
        ),
        "sha256": "16ebdfce8fcb4f2e82cfd47e76962b0509385c30823b3d4ece23c1b130994b4f",  # pragma: allowlist secret
        "evidenceKind": "pinned-ria-snapshot",
        "lifecycleStatus": "superseded",
        "observedAt": "2026-07-04",
        "sourceCommit": RIA_SNAPSHOT_SOURCE_COMMIT,
        "retiredReference": RETIRED_SURFACES[4],
        "supersededBy": REPLACEMENT_SURFACES[4],
        "count": 2,
    },
    {
        "path": (
            "docs/90.references/research/2026-07-04-wer/"
            "automation-pipeline-workflow-qa.md"
        ),
        "sha256": "9e4b828aae5e631ff5cf3daf6bc88223ecdb17ce377914b5e9b2f1a2af2601ab",  # pragma: allowlist secret
        "evidenceKind": "pinned-ria-snapshot",
        "lifecycleStatus": "superseded",
        "observedAt": "2026-07-05",
        "sourceCommit": RIA_SNAPSHOT_SOURCE_COMMIT,
        "retiredReference": RETIRED_SURFACES[4],
        "supersededBy": REPLACEMENT_SURFACES[4],
        "count": 6,
    },
    {
        "path": (
            "docs/90.references/audits/2026-07-04-wdcn/"
            "workspace-document-contract-normalization-audit.md"
        ),
        "sha256": "bfa40f0f7e918df9dfaf0c44e5098e581a38969b7417bed2ab7fdabbdad80913",  # pragma: allowlist secret
        "evidenceKind": "pinned-ria-snapshot",
        "lifecycleStatus": "superseded",
        "observedAt": "2026-07-04",
        "sourceCommit": RIA_SNAPSHOT_SOURCE_COMMIT,
        "retiredReference": RETIRED_SURFACES[4],
        "supersededBy": REPLACEMENT_SURFACES[4],
        "count": 3,
    },
)
TERMINAL_STATUSES = (
    "archived",
    "cancelled",
    "closed",
    "complete",
    "completed",
    "done",
    "rejected",
    "retired",
    "superseded",
)
EXCLUDED_ROOTS = (
    ".agent-work",
    ".git",
    ".pytest_cache",
    ".superpowers",
    ".venv",
    ".worktrees",
    "__pycache__",
    "node_modules",
)
ALWAYS_ACTIVE_PREFIXES = (
    ".agents/",
    ".claude/",
    ".codex/",
    ".gemini/",
    ".github/",
    "docs/00.agent-governance/",
    "scripts/",
    "tests/",
)
ALWAYS_ACTIVE_FILES = (
    ".pre-commit-config.yaml",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "README.md",
    "pyproject.toml",
)
ALLOWED_INTERNAL_SYMLINKS = (
    (".claude/output-styles", "../.agents/output-styles"),
    (".claude/skills", "../.agents/skills"),
    (".claude/workflows", "../.agents/workflows"),
    (".codex/output-styles", "../.agents/output-styles"),
    (".codex/skills", "../.agents/skills"),
    (".codex/workflows", "../.agents/workflows"),
)
COMMANDS = {
    "selfTest": (
        "python3 scripts/validate-agent-legacy-cutover.py "
        "--root . --self-test"
    ),
    "production": "python3 scripts/validate-agent-legacy-cutover.py --root .",
}
EXIT_CODES = (
    {"code": 0, "result": "PASS"},
    {"code": 1, "result": "FAIL"},
    {"code": 2, "result": "FAIL"},
)
EXPECTED_POSITIVE_CASES = (
    ("clean-cutover", "none"),
    ("terminal-reference-is-evidence", "add-terminal-reference"),
    ("protected-reference-is-evidence", "verify-protected-evidence"),
)
EXPECTED_MUTATION_CASES = (
    ("retained-role-contract", "filesystem", "add-retired-path", "AGQC-LEGACY-RETIRED"),
    ("retained-old-github-hub", "filesystem", "add-retired-path", "AGQC-LEGACY-RETIRED"),
    ("missing-replacement", "filesystem", "remove-replacement", "AGQC-LEGACY-REPLACEMENT"),
    ("stale-active-consumer", "filesystem", "add-active-reference", "AGQC-LEGACY-CONSUMER"),
    ("old-harness-consumer", "filesystem", "select-retired-consumer", "AGQC-LEGACY-HARNESS"),
    ("old-harness-compatibility", "filesystem", "add-harness-compatibility", "AGQC-LEGACY-HARNESS"),
    ("replacement-symlink", "filesystem", "symlink-replacement", "AGQC-LEGACY-INPUT"),
    ("malformed-harness-json", "filesystem", "malform-harness-json", "AGQC-LEGACY-JSON"),
    ("duplicate-harness-json-key", "filesystem", "duplicate-harness-json-key", "AGQC-LEGACY-JSON"),
    ("migration-allowlist-growth", "contract", "add-migration-reference", "AGQC-LEGACY-SCHEMA"),
    ("replacement-path-escape", "contract", "replace-replacement-path", "AGQC-LEGACY-SCHEMA"),
    ("protected-evidence-allowlist-growth", "contract", "add-protected-evidence", "AGQC-LEGACY-SCHEMA"),
    ("active-research-reference", "filesystem", "add-active-reference", "AGQC-LEGACY-CONSUMER"),
    ("accepted-reference-pack-reference", "filesystem", "add-active-reference", "AGQC-LEGACY-CONSUMER"),
    ("protected-data-drift", "filesystem", "mutate-protected-evidence", "AGQC-LEGACY-CONSUMER"),
    ("protected-evidence-missing", "filesystem", "remove-protected-evidence", "AGQC-LEGACY-CONSUMER"),
    ("protected-reference-removal", "filesystem", "replace-protected-reference", "AGQC-LEGACY-CONSUMER"),
    ("digest-pinned-draft-reference", "contract", "replace-protected-evidence", "AGQC-LEGACY-SCHEMA"),
    ("extensionless-active-reference", "filesystem", "add-active-reference", "AGQC-LEGACY-CONSUMER"),
    ("invalid-utf8-reference", "filesystem", "add-invalid-utf8-reference", "AGQC-LEGACY-INPUT"),
    ("allowed-reference-count-drift", "filesystem", "mutate-allowed-reference", "AGQC-LEGACY-CONSUMER"),
    ("current-authority-migration-drift", "contract", "change-current-authority-migration", "AGQC-LEGACY-CONTRACT"),
)
STATUS_LINE = re.compile(r"^status\s*:\s*(.*?)\s*$", re.IGNORECASE)
UPDATED_LINE = re.compile(r"^updated\s*:\s*(.*?)\s*$", re.IGNORECASE)


class ContractError(ValueError):
    """One stable cutover contract finding."""

    def __init__(self, rule_id: str, detail: str):
        self.rule_id = rule_id
        self.detail = detail
        super().__init__(f"{rule_id}: {detail}")


class DuplicateKeyError(ValueError):
    """Raised when a JSON object repeats a key."""


def fail(rule_id: str, detail: str) -> NoReturn:
    raise ContractError(rule_id, detail)


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, child in pairs:
        if key in value:
            raise DuplicateKeyError(f"duplicate JSON key {key!r}")
        value[key] = child
    return value


def _parse_json(text: str, source: str) -> Any:
    try:
        return json.loads(text, object_pairs_hook=_reject_duplicate_pairs)
    except (json.JSONDecodeError, DuplicateKeyError) as exc:
        fail("AGQC-LEGACY-JSON", f"{source}: {exc}")


def _absolute_root(root: Path) -> Path:
    absolute = Path(os.path.abspath(os.fspath(root)))
    try:
        mode = absolute.lstat().st_mode
    except OSError as exc:
        fail(
            "AGQC-LEGACY-INPUT",
            f"repository root is unavailable: {exc.strerror}",
        )
    if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
        fail(
            "AGQC-LEGACY-INPUT",
            "repository root must be a non-symlink directory",
        )
    return absolute


def _relative_path(value: str) -> PurePosixPath:
    if (
        not value
        or value == "."
        or value.startswith("/")
        or "\\" in value
        or any(part in ("", ".", "..") for part in value.split("/"))
    ):
        fail("AGQC-LEGACY-INPUT", f"unsafe repository path: {value!r}")
    return PurePosixPath(value)


def _walk_parents(root: Path, relative: PurePosixPath) -> Path:
    current = root
    for part in relative.parts[:-1]:
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            return root / relative
        except OSError as exc:
            fail(
                "AGQC-LEGACY-INPUT",
                f"{relative.as_posix()} parent is unavailable: {exc.strerror}",
            )
        if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
            fail(
                "AGQC-LEGACY-INPUT",
                f"{relative.as_posix()} has a non-directory or symlink parent",
            )
    return root / relative


def _path_state(root: Path, value: str) -> tuple[Path, int | None]:
    relative = _relative_path(value)
    path = _walk_parents(root, relative)
    try:
        return path, path.lstat().st_mode
    except FileNotFoundError:
        return path, None
    except OSError as exc:
        fail(
            "AGQC-LEGACY-INPUT",
            f"{value} is unavailable: {exc.strerror}",
        )


def _read_regular_text(
    root: Path,
    value: str,
    *,
    missing_rule: str = "AGQC-LEGACY-INPUT",
) -> str:
    path, mode = _path_state(root, value)
    if mode is None:
        fail(missing_rule, f"{value} is missing")
    if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
        fail(
            "AGQC-LEGACY-INPUT",
            f"{value} must be a regular non-symlink file",
        )
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail("AGQC-LEGACY-INPUT", f"{value} is not readable UTF-8: {exc}")


def _load_json_regular(
    root: Path,
    value: str,
    *,
    missing_rule: str = "AGQC-LEGACY-INPUT",
) -> Any:
    return _parse_json(
        _read_regular_text(root, value, missing_rule=missing_rule),
        value,
    )


def load_contract_documents(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load the contract and schema from regular contained files."""

    absolute = _absolute_root(root)
    contract = _load_json_regular(absolute, CONTRACT_PATH.as_posix())
    schema = _load_json_regular(absolute, SCHEMA_PATH.as_posix())
    if not isinstance(contract, dict) or not isinstance(schema, dict):
        fail("AGQC-LEGACY-JSON", "contract and schema roots must be objects")
    return contract, schema


def _schema_error_detail(error: Any) -> str:
    location = "/".join(str(part) for part in error.absolute_path) or "<root>"
    return f"{location}: {error.message}"


def validate_contract_data(
    contract: dict[str, Any],
    schema: dict[str, Any],
) -> dict[str, Any]:
    """Validate closed syntax and exact no-growth cutover semantics."""

    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema exposes multiple schema exceptions
        fail("AGQC-LEGACY-SCHEMA", f"schema definition is invalid: {exc}")
    errors = sorted(
        Draft202012Validator(schema).iter_errors(contract),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    if errors:
        fail("AGQC-LEGACY-SCHEMA", _schema_error_detail(errors[0]))

    if (
        contract["schemaVersion"] != SCHEMA_VERSION
        or contract["contractVersion"] != CONTRACT_VERSION
        or contract["currentOwnerSpec"] != OWNER_SPEC
    ):
        fail("AGQC-LEGACY-CONTRACT", "version or current owner differs")
    if tuple(contract["resultVocabulary"]) != RESULT_VOCABULARY:
        fail("AGQC-LEGACY-CONTRACT", "result vocabulary or order differs")
    if tuple(contract["evidenceVocabulary"]) != EVIDENCE_VOCABULARY:
        fail("AGQC-LEGACY-CONTRACT", "evidence vocabulary differs")
    if tuple(contract["retiredSurfaces"]) != RETIRED_SURFACES:
        fail("AGQC-LEGACY-CONTRACT", "retired surface set or order differs")
    if tuple(contract["replacementSurfaces"]) != REPLACEMENT_SURFACES:
        fail(
            "AGQC-LEGACY-CONTRACT",
            "replacement surface set or order differs",
        )
    if contract["harnessCutover"] != HARNESS_CUTOVER:
        fail("AGQC-LEGACY-CONTRACT", "harness cutover selector differs")
    if contract["currentAuthorityMigrations"] != list(
        CURRENT_AUTHORITY_MIGRATIONS
    ):
        fail(
            "AGQC-LEGACY-CONTRACT",
            "current authority migration set grew, shrank, or changed",
        )

    references = contract["referencePolicy"]
    expected_references = {
        "packageReferences": list(PACKAGE_REFERENCES),
        "migrationReferences": list(MIGRATION_REFERENCES),
        "allowedReferenceCounts": [
            {"path": path, "counts": list(counts)}
            for path, counts in ALLOWED_REFERENCE_COUNTS
        ],
        "protectedEvidenceFiles": copy.deepcopy(
            list(PROTECTED_EVIDENCE_FILES)
        ),
        "terminalStatuses": list(TERMINAL_STATUSES),
    }
    if references != expected_references:
        fail(
            "AGQC-LEGACY-CONTRACT",
            "reference allowlist grew, shrank, or changed order",
        )

    scan = contract["scanPolicy"]
    expected_scan = {
        "root": ".",
        "excludedRoots": list(EXCLUDED_ROOTS),
        "scanAllRegularFiles": True,
        "alwaysActivePrefixes": list(ALWAYS_ACTIVE_PREFIXES),
        "alwaysActiveFiles": list(ALWAYS_ACTIVE_FILES),
        "allowedInternalSymlinks": [
            {"path": path, "target": target}
            for path, target in ALLOWED_INTERNAL_SYMLINKS
        ],
    }
    if scan != expected_scan:
        fail("AGQC-LEGACY-CONTRACT", "scan policy or symlink set differs")
    if contract["commands"] != COMMANDS:
        fail("AGQC-LEGACY-CONTRACT", "command ownership differs")
    if tuple(contract["exitCodes"]) != EXIT_CODES:
        fail("AGQC-LEGACY-CONTRACT", "stable exit-code mapping differs")
    return contract


def _validate_replacements(root: Path) -> None:
    for value in RETIRED_SURFACES:
        _path, mode = _path_state(root, value)
        if mode is not None:
            fail("AGQC-LEGACY-RETIRED", f"retired surface remains: {value}")
    for value in REPLACEMENT_SURFACES:
        _read_regular_text(
            root,
            value,
            missing_rule="AGQC-LEGACY-REPLACEMENT",
        )
    for value in (
        REPLACEMENT_SURFACES[0],
        REPLACEMENT_SURFACES[1],
        REPLACEMENT_SURFACES[3],
    ):
        _load_json_regular(
            root,
            value,
            missing_rule="AGQC-LEGACY-REPLACEMENT",
        )


def _all_strings(value: Any) -> list[str]:
    values: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            values.append(str(key))
            values.extend(_all_strings(child))
    elif isinstance(value, list):
        for child in value:
            values.extend(_all_strings(child))
    elif isinstance(value, str):
        values.append(value)
    return values


def _validate_harness(root: Path) -> None:
    harness = _load_json_regular(
        root,
        REPLACEMENT_SURFACES[0],
        missing_rule="AGQC-LEGACY-REPLACEMENT",
    )
    if not isinstance(harness, dict):
        fail("AGQC-LEGACY-HARNESS", "harness contract root must be an object")
    for key in HARNESS_CUTOVER["forbiddenTopLevelKeys"]:
        if key in harness:
            fail(
                "AGQC-LEGACY-HARNESS",
                f"retired harness compatibility owner remains: {key}",
            )
    consumers = harness.get(HARNESS_CUTOVER["consumersKey"])
    if not isinstance(consumers, list) or any(
        not isinstance(row, dict) for row in consumers
    ):
        fail("AGQC-LEGACY-HARNESS", "harness consumers must be an object list")
    expected = HARNESS_CUTOVER["selectedConsumer"]
    selected = [
        row
        for row in consumers
        if row.get("id") == expected["id"]
        and row.get("path") == expected["path"]
    ]
    if len(selected) != 1:
        fail(
            "AGQC-LEGACY-HARNESS",
            "new harness semantics consumer is not selected exactly once",
        )
    retired_ids = set(HARNESS_CUTOVER["retiredConsumerIds"])
    if any(row.get("id") in retired_ids for row in consumers):
        fail("AGQC-LEGACY-HARNESS", "retired harness consumer remains")
    flattened = _all_strings(harness)
    stale = next(
        (
            token
            for token in RETIRED_SURFACES
            if any(token in value for value in flattened)
        ),
        None,
    )
    if stale is not None:
        fail(
            "AGQC-LEGACY-HARNESS",
            f"harness contract retains retired token: {stale}",
        )


def _under_prefix(value: str, prefix: str) -> bool:
    return value == prefix or value.startswith(prefix + "/")


def _is_terminal_document(text: str) -> bool:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return False
    try:
        end = next(
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == "---"
        )
    except StopIteration:
        return False
    statuses: list[str] = []
    for line in lines[1:end]:
        match = STATUS_LINE.fullmatch(line)
        if match is not None:
            value = match.group(1).split("#", 1)[0].strip().strip("'\"")
            statuses.append(value.casefold())
    return len(statuses) == 1 and statuses[0] in TERMINAL_STATUSES


def _is_verified_protected_evidence(
    raw: bytes,
    text: str,
    record: dict[str, Any],
) -> bool:
    """Accept only a closed superseding relation, never a digest alone."""

    if hashlib.sha256(raw).hexdigest() != record["sha256"]:
        return False
    if (
        record["lifecycleStatus"] != "superseded"
        or record["supersededBy"] not in REPLACEMENT_SURFACES
    ):
        return False
    if record["evidenceKind"] == "pinned-activation-snapshot":
        try:
            snapshot = _parse_json(text, record["path"])
        except ContractError:
            return False
        if not isinstance(snapshot, dict):
            return False
        activation = snapshot.get("activation")
        if not isinstance(activation, dict):
            return False
        if (
            snapshot.get("observedAt") != record["observedAt"]
            or activation.get("activationCommit") != record["sourceCommit"]
        ):
            return False
    elif record["evidenceKind"] == "pinned-ria-snapshot":
        if record["sourceCommit"] != RIA_SNAPSHOT_SOURCE_COMMIT:
            return False
        updated_values = [
            match.group(1).split("#", 1)[0].strip().strip("'\"")
            for line in text.splitlines()
            if (match := UPDATED_LINE.fullmatch(line)) is not None
        ]
        if updated_values != [record["observedAt"]]:
            return False
    else:
        return False
    retired_reference = record["retiredReference"].encode("utf-8")
    if raw.count(retired_reference) != record["count"]:
        return False
    if any(
        token != record["retiredReference"]
        and token.encode("utf-8") in raw
        for token in RETIRED_SURFACES
    ):
        return False
    if record["supersededBy"].encode("utf-8") in raw:
        return False
    return True


def _validate_protected_evidence_files(
    root: Path,
    protected_files: dict[str, dict[str, Any]],
) -> None:
    for relative, record in protected_files.items():
        path, mode = _path_state(root, relative)
        if mode is None or stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
            fail(
                "AGQC-LEGACY-CONSUMER",
                f"protected evidence is missing or not regular: {relative}",
            )
        try:
            raw = path.read_bytes()
            text = raw.decode("utf-8")
        except (OSError, UnicodeError) as exc:
            fail(
                "AGQC-LEGACY-INPUT",
                f"protected evidence is unreadable UTF-8 {relative}: {exc}",
            )
        if not _is_verified_protected_evidence(raw, text, record):
            fail(
                "AGQC-LEGACY-CONSUMER",
                f"protected evidence relation differs: {relative}",
            )


def _validate_allowed_symlink(root: Path, relative: str, target: str) -> None:
    expected = dict(ALLOWED_INTERNAL_SYMLINKS).get(relative)
    if expected is None or target != expected:
        fail(
            "AGQC-LEGACY-INPUT",
            f"undeclared or changed symlink: {relative} -> {target}",
        )
    lexical_target = Path(
        os.path.abspath(os.fspath(root / PurePosixPath(relative).parent / target))
    )
    try:
        common = os.path.commonpath((os.fspath(root), os.fspath(lexical_target)))
    except ValueError:
        common = ""
    if common != os.fspath(root):
        fail(
            "AGQC-LEGACY-INPUT",
            f"allowed symlink escapes repository: {relative}",
        )


def _scan_consumers(root: Path) -> tuple[int, int, list[str]]:
    allowed_counts = dict(ALLOWED_REFERENCE_COUNTS)
    protected_files = {
        record["path"]: record for record in PROTECTED_EVIDENCE_FILES
    }
    _validate_protected_evidence_files(root, protected_files)
    excluded_roots = set(EXCLUDED_ROOTS)
    scanned = 0
    evidence = 0
    consumers: list[str] = []

    for relative in allowed_counts:
        _read_regular_text(root, relative)

    for current, directory_names, file_names in os.walk(
        root,
        topdown=True,
        followlinks=False,
    ):
        current_path = Path(current)
        current_relative = current_path.relative_to(root).as_posix()
        if current_relative == ".":
            current_relative = ""

        retained_directories: list[str] = []
        for name in sorted(directory_names):
            path = current_path / name
            relative = (
                f"{current_relative}/{name}" if current_relative else name
            )
            if name in excluded_roots or any(
                _under_prefix(relative, value) for value in excluded_roots
            ):
                continue
            if path.is_symlink():
                try:
                    target = os.readlink(path)
                except OSError as exc:
                    fail(
                        "AGQC-LEGACY-INPUT",
                        f"cannot inspect symlink {relative}: {exc}",
                    )
                _validate_allowed_symlink(root, relative, target)
                continue
            retained_directories.append(name)
        directory_names[:] = retained_directories

        for name in sorted(file_names):
            path = current_path / name
            relative = (
                f"{current_relative}/{name}" if current_relative else name
            )
            if any(_under_prefix(relative, value) for value in excluded_roots):
                continue
            if path.is_symlink():
                fail(
                    "AGQC-LEGACY-INPUT",
                    f"undeclared symlink file in scan surface: {relative}",
                )
            try:
                mode = path.lstat().st_mode
            except OSError as exc:
                fail(
                    "AGQC-LEGACY-INPUT",
                    f"scan input unavailable {relative}: {exc.strerror}",
                )
            if not stat.S_ISREG(mode):
                fail(
                    "AGQC-LEGACY-INPUT",
                    f"scan input is not regular: {relative}",
                )
            try:
                raw = path.read_bytes()
            except OSError as exc:
                fail(
                    "AGQC-LEGACY-INPUT",
                    f"scan input unreadable {relative}: {exc}",
                )
            scanned += 1
            retired = [
                token
                for token in RETIRED_SURFACES
                if token.encode("utf-8") in raw
            ]
            if not retired:
                continue
            try:
                text = raw.decode("utf-8")
            except UnicodeError as exc:
                fail(
                    "AGQC-LEGACY-INPUT",
                    f"candidate consumer is not UTF-8 {relative}: {exc}",
                )
            expected_counts = allowed_counts.get(relative)
            if expected_counts is not None:
                observed_counts = tuple(
                    raw.count(token.encode("utf-8"))
                    for token in RETIRED_SURFACES
                )
                if observed_counts == expected_counts:
                    evidence += 1
                else:
                    consumers.append(
                        f"{relative}:allowed-reference-count-drift"
                    )
                continue
            protected_record = protected_files.get(relative)
            if protected_record is not None and _is_verified_protected_evidence(
                raw,
                text,
                protected_record,
            ):
                evidence += 1
                continue
            always_active = (
                relative in ALWAYS_ACTIVE_FILES
                or any(
                    relative.startswith(prefix)
                    for prefix in ALWAYS_ACTIVE_PREFIXES
                )
            )
            if not always_active and _is_terminal_document(text):
                evidence += 1
                continue
            consumers.append(f"{relative}:{retired[0]}")
    return scanned, evidence, consumers


def validate_repository(root: Path) -> dict[str, int]:
    """Validate a completed cutover using repository-static evidence only."""

    absolute = _absolute_root(root)
    contract, schema = load_contract_documents(absolute)
    validate_contract_data(contract, schema)
    _validate_replacements(absolute)
    _validate_harness(absolute)
    scanned, evidence, consumers = _scan_consumers(absolute)
    if consumers:
        fail(
            "AGQC-LEGACY-CONSUMER",
            "active consumer retains a retired token: " + consumers[0],
        )
    return {
        "retiredSurfaces": len(RETIRED_SURFACES),
        "replacementSurfaces": len(REPLACEMENT_SURFACES),
        "activeConsumers": len(consumers),
        "scannedFiles": scanned,
        "evidenceReferences": evidence,
    }


def _fixture_target(root: Path, relative: str) -> Path:
    safe = _relative_path(relative)
    current = root
    for part in safe.parts[:-1]:
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            current.mkdir()
            continue
        except OSError as exc:
            fail(
                "AGQC-LEGACY-FIXTURE",
                f"fixture parent is unavailable {relative}: {exc}",
            )
        if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
            fail(
                "AGQC-LEGACY-FIXTURE",
                f"fixture parent must be a non-symlink directory: {relative}",
            )
    return current / safe.name


def _write_text(root: Path, relative: str, text: str) -> Path:
    path = _fixture_target(root, relative)
    path.write_text(text, encoding="utf-8")
    return path


def _write_bytes(root: Path, relative: str, payload: bytes) -> Path:
    path = _fixture_target(root, relative)
    path.write_bytes(payload)
    return path


def _fixture_regular_file(root: Path, relative: str) -> Path:
    path, mode = _path_state(root, relative)
    if mode is None or stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
        fail(
            "AGQC-LEGACY-FIXTURE",
            f"fixture target must be a regular non-symlink file: {relative}",
        )
    return path


def _create_baseline(source_root: Path, target_root: Path) -> None:
    for relative in dict.fromkeys(PACKAGE_REFERENCES + MIGRATION_REFERENCES):
        source = source_root / PurePosixPath(relative)
        target = target_root / PurePosixPath(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    for record in PROTECTED_EVIDENCE_FILES:
        relative = record["path"]
        source = source_root / PurePosixPath(relative)
        target = target_root / PurePosixPath(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    _write_text(
        target_root,
        REPLACEMENT_SURFACES[0],
        json.dumps(
            {
                "consumers": [
                    {
                        "id": HARNESS_CUTOVER["selectedConsumer"]["id"],
                        "path": HARNESS_CUTOVER["selectedConsumer"]["path"],
                    }
                ]
            },
            indent=2,
        )
        + "\n",
    )
    _write_text(target_root, REPLACEMENT_SURFACES[1], "{}\n")
    _write_text(target_root, REPLACEMENT_SURFACES[2], "replacement\n")
    _write_text(target_root, REPLACEMENT_SURFACES[3], "{}\n")
    _write_text(target_root, REPLACEMENT_SURFACES[4], "replacement hub\n")


def _load_fixture(root: Path) -> dict[str, Any]:
    path, mode = _path_state(root, FIXTURE_PATH.as_posix())
    if mode is None or stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
        fail(
            "AGQC-LEGACY-FIXTURE",
            "fixture must be a regular non-symlink file",
        )
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        fail("AGQC-LEGACY-FIXTURE", f"fixture is unreadable: {exc}")
    if hashlib.sha256(raw).hexdigest() != FIXTURE_SHA256:
        fail("AGQC-LEGACY-FIXTURE", "fixture bytes differ from the closed set")
    fixture = _parse_json(text, FIXTURE_PATH.as_posix())
    if not isinstance(fixture, dict):
        fail("AGQC-LEGACY-FIXTURE", "fixture root must be an object")
    expected_keys = {"fixtureVersion", "positiveCases", "mutationCases"}
    if set(fixture) != expected_keys or fixture["fixtureVersion"] != 1:
        fail("AGQC-LEGACY-FIXTURE", "fixture keys or version differ")
    positives = tuple(
        (case.get("name"), case.get("mutation", {}).get("kind"))
        for case in fixture["positiveCases"]
        if isinstance(case, dict) and isinstance(case.get("mutation"), dict)
    )
    mutations = tuple(
        (
            case.get("name"),
            case.get("target"),
            case.get("mutation", {}).get("kind"),
            case.get("expectedRule"),
        )
        for case in fixture["mutationCases"]
        if isinstance(case, dict) and isinstance(case.get("mutation"), dict)
    )
    if positives != EXPECTED_POSITIVE_CASES or mutations != EXPECTED_MUTATION_CASES:
        fail("AGQC-LEGACY-FIXTURE", "fixture case set or order differs")
    return fixture


def _apply_positive(root: Path, kind: str) -> None:
    if kind == "none":
        return
    if kind == "add-terminal-reference":
        _write_text(
            root,
            "docs/04.execution/plans/terminal-evidence.md",
            "---\nstatus: Done\n---\n"
            f"historical: {RETIRED_SURFACES[0]}\n",
        )
        return
    if kind == "verify-protected-evidence":
        if not all(
            (root / PurePosixPath(record["path"])).is_file()
            for record in PROTECTED_EVIDENCE_FILES
        ):
            fail(
                "AGQC-LEGACY-FIXTURE",
                "protected evidence baseline is incomplete",
            )
        return
    fail("AGQC-LEGACY-FIXTURE", f"unknown positive mutation: {kind}")


def _mutate_contract(contract: dict[str, Any], mutation: dict[str, Any]) -> None:
    kind = mutation["kind"]
    if kind == "add-migration-reference":
        contract["referencePolicy"]["migrationReferences"].append(
            mutation["path"]
        )
    elif kind == "replace-replacement-path":
        contract["replacementSurfaces"][mutation["index"]] = mutation["path"]
    elif kind == "add-protected-evidence":
        contract["referencePolicy"]["protectedEvidenceFiles"].append(
            {
                "path": mutation["path"],
                "sha256": mutation["sha256"],
            }
        )
    elif kind == "replace-protected-evidence":
        contract["referencePolicy"]["protectedEvidenceFiles"][0] = {
            "path": mutation["path"],
            "sha256": mutation["sha256"],
            "evidenceKind": "authored-document",
            "lifecycleStatus": mutation["lifecycleStatus"],
            "observedAt": mutation["observedAt"],
            "sourceCommit": mutation["sourceCommit"],
            "retiredReference": mutation["retiredReference"],
            "supersededBy": mutation["supersededBy"],
            "count": mutation["count"],
        }
    elif kind == "change-current-authority-migration":
        contract["currentAuthorityMigrations"][mutation["index"]][
            mutation["field"]
        ] = mutation["value"]
    else:
        fail("AGQC-LEGACY-FIXTURE", f"unknown contract mutation: {kind}")


def _mutate_filesystem(root: Path, mutation: dict[str, Any]) -> None:
    kind = mutation["kind"]
    harness_path = root / PurePosixPath(REPLACEMENT_SURFACES[0])
    if kind == "add-retired-path":
        _write_text(root, mutation["path"], "{}\n")
    elif kind == "remove-replacement":
        _fixture_regular_file(root, mutation["path"]).unlink()
    elif kind == "add-active-reference":
        _write_text(
            root,
            mutation["path"],
            (
                "---\n"
                "title: 'Stale reference fixture'\n"
                "type: content/reference\n"
                f"status: {mutation.get('status', 'active')}\n"
                "owner: platform\n"
                "updated: 2026-07-30\n"
                "---\n\n"
                f"use {RETIRED_SURFACES[0]}\n"
            ),
        )
    elif kind == "mutate-protected-evidence":
        path = _fixture_regular_file(root, mutation["path"])
        path.write_bytes(path.read_bytes() + b"\nprotected evidence drift\n")
    elif kind == "remove-protected-evidence":
        _fixture_regular_file(root, mutation["path"]).unlink()
    elif kind == "replace-protected-reference":
        path = _fixture_regular_file(root, mutation["path"])
        raw = path.read_bytes()
        retired = RETIRED_SURFACES[3].encode("utf-8")
        replacement = REPLACEMENT_SURFACES[3].encode("utf-8")
        if raw.count(retired) != 1:
            fail(
                "AGQC-LEGACY-FIXTURE",
                "protected reference fixture count differs",
            )
        path.write_bytes(raw.replace(retired, replacement))
    elif kind == "add-invalid-utf8-reference":
        _write_bytes(
            root,
            mutation["path"],
            RETIRED_SURFACES[0].encode("utf-8") + b"\xff\n",
        )
    elif kind == "mutate-allowed-reference":
        path = _fixture_regular_file(root, mutation["path"])
        path.write_bytes(
            path.read_bytes()
            + b"\n"
            + RETIRED_SURFACES[0].encode("utf-8")
            + b"\n"
        )
    elif kind == "select-retired-consumer":
        _write_text(
            root,
            REPLACEMENT_SURFACES[0],
            json.dumps(
                {
                    "consumers": [
                        {
                            "id": "role-semantics-validator",
                            "path": RETIRED_SURFACES[2],
                        }
                    ]
                },
                indent=2,
            )
            + "\n",
        )
    elif kind == "add-harness-compatibility":
        value = _parse_json(
            harness_path.read_text(encoding="utf-8"),
            REPLACEMENT_SURFACES[0],
        )
        value["compatibility"] = {"removalOwnerSpec": OWNER_SPEC}
        harness_path.write_text(
            json.dumps(value, indent=2) + "\n",
            encoding="utf-8",
        )
    elif kind == "symlink-replacement":
        path = _fixture_regular_file(root, mutation["path"])
        copy_path = path.with_name("replacement-copy" + path.suffix)
        shutil.copyfile(path, copy_path)
        path.unlink()
        path.symlink_to(copy_path.name)
    elif kind == "malform-harness-json":
        harness_path.write_text('{"consumers": [', encoding="utf-8")
    elif kind == "duplicate-harness-json-key":
        harness_path.write_text(
            '{"consumers": [], "consumers": []}\n',
            encoding="utf-8",
        )
    else:
        fail("AGQC-LEGACY-FIXTURE", f"unknown filesystem mutation: {kind}")


def run_self_test(root: Path) -> tuple[int, int]:
    """Execute deterministic fixtures in temporary repositories only."""

    absolute = _absolute_root(root)
    contract, schema = load_contract_documents(absolute)
    validate_contract_data(contract, schema)
    fixture = _load_fixture(absolute)

    for case in fixture["positiveCases"]:
        with tempfile.TemporaryDirectory(
            prefix="agent-legacy-cutover-positive-"
        ) as directory:
            target = Path(directory)
            _create_baseline(absolute, target)
            _apply_positive(target, case["mutation"]["kind"])
            validate_repository(target)

    for case in fixture["mutationCases"]:
        expected = case["expectedRule"]
        try:
            if case["target"] == "contract":
                mutated = copy.deepcopy(contract)
                _mutate_contract(mutated, case["mutation"])
                validate_contract_data(mutated, schema)
            elif case["target"] == "filesystem":
                with tempfile.TemporaryDirectory(
                    prefix="agent-legacy-cutover-negative-"
                ) as directory:
                    target = Path(directory)
                    _create_baseline(absolute, target)
                    _mutate_filesystem(target, case["mutation"])
                    validate_repository(target)
            else:
                fail(
                    "AGQC-LEGACY-FIXTURE",
                    f"unknown mutation target: {case['target']}",
                )
        except ContractError as exc:
            if exc.rule_id != expected:
                fail(
                    "AGQC-LEGACY-FIXTURE",
                    f"{case['name']}: expected {expected}, got {exc.rule_id}",
                )
        else:
            fail(
                "AGQC-LEGACY-FIXTURE",
                f"{case['name']}: mutation was accepted",
            )
    return len(fixture["positiveCases"]), len(fixture["mutationCases"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            positive_count, mutation_count = run_self_test(args.root)
            print(
                "[PASS] agent legacy cutover self-test passed: "
                f"positive_cases={positive_count} "
                f"mutation_cases={mutation_count}"
            )
            return 0
        counts = validate_repository(args.root)
        print(
            "[PASS] agent legacy cutover validation passed: "
            f"retired_surfaces={counts['retiredSurfaces']} "
            f"replacement_surfaces={counts['replacementSurfaces']} "
            f"active_consumers={counts['activeConsumers']} "
            f"scanned_files={counts['scannedFiles']} "
            f"evidence_references={counts['evidenceReferences']}"
        )
        return 0
    except ContractError as exc:
        print(f"[FAIL] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
