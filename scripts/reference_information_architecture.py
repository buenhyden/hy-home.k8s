"""Closed RIA-001 contract loading and validation."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
from typing import Mapping

from jsonschema import Draft202012Validator


DEFAULT_CONTRACT_PATH = Path("docs/90.references/data/reference-information-architecture.json")
ALLOWED_PATH_ROOTS = frozenset({"docs", "scripts", "tests"})
GIT_SHA1_PATTERN = re.compile(r"^git-sha1:([0-9a-f]{40})$")


@dataclass(frozen=True, order=True)
class Finding:
    rule_id: str
    path: str
    message: str


class ContractError(ValueError):
    """A malformed or unsafe contract/configuration boundary."""

    def __init__(self, rule_id: str, path: str, message: str) -> None:
        self.finding = Finding(rule_id, path, message)
        super().__init__(f"{rule_id} {path}: {message}")


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def parse_repository_path(value: object, *, field: str) -> Path:
    """Return a canonical allowlisted repository-relative POSIX path."""

    if not isinstance(value, str) or not value:
        raise ContractError("RIA-BOUNDARY", field, "path must be a non-empty string")
    if "\\" in value or value.startswith("/"):
        raise ContractError("RIA-BOUNDARY", field, "path must be relative POSIX")
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ContractError("RIA-BOUNDARY", field, "path contains a forbidden segment")
    parsed = PurePosixPath(value)
    if parsed.is_absolute() or parsed.parts[0] not in ALLOWED_PATH_ROOTS:
        raise ContractError("RIA-BOUNDARY", field, "path is outside declared roots")
    if str(parsed) != value:
        raise ContractError("RIA-BOUNDARY", field, "path is not canonical")
    return Path(*parsed.parts)


def _path_under_root(root: Path, candidate: Path, *, field: str) -> Path:
    try:
        relative = candidate.relative_to(root) if candidate.is_absolute() else candidate
    except ValueError as error:
        raise ContractError("RIA-BOUNDARY", field, "path is outside repository root") from error
    return parse_repository_path(relative.as_posix(), field=field)


def _read_regular_file(root: Path, relative: Path, *, field: str) -> bytes:
    """Read a bounded regular file without following any path symlink."""

    try:
        root_stat = root.lstat()
    except OSError as error:
        raise ContractError("RIA-BOUNDARY", field, "repository root is unavailable") from error
    if not stat.S_ISDIR(root_stat.st_mode) or stat.S_ISLNK(root_stat.st_mode):
        raise ContractError("RIA-BOUNDARY", field, "repository root is not a directory")
    try:
        directory_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError as error:
        raise ContractError("RIA-BOUNDARY", field, "repository root cannot be opened") from error
    try:
        for component in relative.parts[:-1]:
            component_stat = os.lstat(component, dir_fd=directory_fd)
            if not stat.S_ISDIR(component_stat.st_mode) or stat.S_ISLNK(component_stat.st_mode):
                raise ContractError("RIA-BOUNDARY", field, "path contains a non-directory")
            next_fd = os.open(
                component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory_fd
            )
            os.close(directory_fd)
            directory_fd = next_fd
        filename = relative.parts[-1]
        file_stat = os.lstat(filename, dir_fd=directory_fd)
        if not stat.S_ISREG(file_stat.st_mode) or stat.S_ISLNK(file_stat.st_mode):
            raise ContractError("RIA-BOUNDARY", field, "path is not a regular file")
        file_fd = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory_fd)
        try:
            if not stat.S_ISREG(os.fstat(file_fd).st_mode):
                raise ContractError("RIA-BOUNDARY", field, "opened path is not regular")
            chunks: list[bytes] = []
            remaining = 2_000_000
            while chunk := os.read(file_fd, min(65_536, remaining + 1)):
                chunks.append(chunk)
                remaining -= len(chunk)
                if remaining < 0:
                    raise ContractError("RIA-CONTRACT", field, "file exceeds input limit")
            return b"".join(chunks)
        finally:
            os.close(file_fd)
    except ContractError:
        raise
    except OSError as error:
        raise ContractError("RIA-BOUNDARY", field, "safe file read failed") from error
    finally:
        os.close(directory_fd)


def _load_json(root: Path, relative: Path, *, field: str) -> dict[str, object]:
    try:
        decoded = _read_regular_file(root, relative, field=field).decode("utf-8", "strict")
        loaded = json.loads(decoded, object_pairs_hook=_reject_duplicate_keys)
    except ContractError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ContractError("RIA-CONTRACT", field, "JSON must be valid and unique-keyed") from error
    if not isinstance(loaded, dict):
        raise ContractError("RIA-CONTRACT", field, "JSON root must be an object")
    return loaded


def parse_git_sha1(value: object) -> str:
    """Return only a fully validated SHA-1 payload for later fixed Git argv use."""

    if not isinstance(value, str):
        raise ContractError("RIA-SNAPSHOT", "snapshotGuard.sourceCommit", "must be encoded SHA-1")
    match = GIT_SHA1_PATTERN.fullmatch(value)
    if match is None:
        raise ContractError("RIA-SNAPSHOT", "snapshotGuard.sourceCommit", "must be git-sha1:<40 lowercase hex>")
    oid = match.group(1)
    if re.fullmatch(r"[0-9a-f]{40}", oid) is None:
        raise ContractError("RIA-SNAPSHOT", "snapshotGuard.sourceCommit", "SHA-1 payload is invalid")
    return oid


def _validate_schema(root: Path, contract: dict[str, object], contract_path: Path) -> None:
    if contract.get("$schema") != "./reference-information-architecture.schema.json":
        raise ContractError("RIA-CONTRACT", "$schema", "schema reference is not canonical")
    schema = _load_json(
        root,
        contract_path.with_name("reference-information-architecture.schema.json"),
        field="$schema",
    )
    try:
        Draft202012Validator.check_schema(schema)
        errors = sorted(
            Draft202012Validator(schema).iter_errors(contract),
            key=lambda error: list(error.absolute_path),
        )
    except Exception as error:
        raise ContractError("RIA-CONTRACT", "$schema", "schema is invalid") from error
    if errors:
        location = ".".join(str(part) for part in errors[0].absolute_path) or "$"
        raise ContractError("RIA-CONTRACT", location, "contract does not match closed schema")


def _unique_strings(value: object, *, field: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ContractError("RIA-CONTRACT", field, "must be an array of strings")
    if len(set(value)) != len(value):
        raise ContractError("RIA-CONTRACT", field, "contains duplicate values")
    return value


def _validate_contract_boundaries(contract: dict[str, object]) -> None:
    registry_path = parse_repository_path(contract.get("currentPackRegistry"), field="currentPackRegistry")
    if registry_path != Path("docs/99.templates/support/document-profiles.json"):
        raise ContractError("RIA-BOUNDARY", "currentPackRegistry", "registry path is fixed")
    guard = contract.get("snapshotGuard")
    if not isinstance(guard, dict):
        raise ContractError("RIA-CONTRACT", "snapshotGuard", "must be an object")
    _unique_strings(guard.get("historicalPackIds"), field="snapshotGuard.historicalPackIds")
    _unique_strings(guard.get("currentPackIds"), field="snapshotGuard.currentPackIds")
    parse_git_sha1(guard.get("sourceCommit"))
    projections = contract.get("mutableIndexProjections")
    generated_assets = contract.get("generatedAssets")
    for field, values, key in (
        ("mutableIndexProjections", projections, "path"),
        ("generatedAssets", generated_assets, "outputPath"),
    ):
        if not isinstance(values, list):
            raise ContractError("RIA-CONTRACT", field, "must be an array")
        paths: set[Path] = set()
        for index, value in enumerate(values):
            if not isinstance(value, dict):
                raise ContractError("RIA-CONTRACT", f"{field}[{index}]", "must be an object")
            path = parse_repository_path(value.get(key), field=f"{field}[{index}].{key}")
            if path in paths:
                raise ContractError("RIA-CONTRACT", field, "contains duplicate paths")
            paths.add(path)


def load_contract(root: Path, contract_path: Path) -> dict[str, object]:
    """Load one closed contract through no-follow regular-file boundaries."""

    root = root.absolute()
    relative_contract_path = _path_under_root(root, contract_path, field="contract")
    contract = _load_json(root, relative_contract_path, field="contract")
    parse_repository_path(contract.get("currentPackRegistry"), field="currentPackRegistry")
    snapshot_guard = contract.get("snapshotGuard")
    if isinstance(snapshot_guard, dict):
        parse_git_sha1(snapshot_guard.get("sourceCommit"))
    _validate_schema(root, contract, relative_contract_path)
    _validate_contract_boundaries(contract)
    return contract


def validate_reference_architecture(root: Path, contract: Mapping[str, object]) -> list[Finding]:
    """Validate the RIA-001 registry references without reading the corpus."""

    registry_path = parse_repository_path(contract.get("currentPackRegistry"), field="currentPackRegistry")
    registry = _load_json(root.absolute(), registry_path, field="currentPackRegistry")
    packs_root = registry.get("referenceCurrentPacks")
    if not isinstance(packs_root, dict) or not isinstance(packs_root.get("packs"), list):
        raise ContractError("RIA-CONTRACT", "currentPackRegistry", "Current pack registry is malformed")
    registry_ids = {
        pack.get("id") for pack in packs_root["packs"] if isinstance(pack, dict) and isinstance(pack.get("id"), str)
    }
    guard = contract.get("snapshotGuard")
    if not isinstance(guard, Mapping):
        raise ContractError("RIA-CONTRACT", "snapshotGuard", "must be an object")
    current_pack_ids = _unique_strings(guard.get("currentPackIds"), field="snapshotGuard.currentPackIds")
    findings = [
        Finding("RIA-CONTRACT", f"snapshotGuard.currentPackIds[{index}]", "referenced Current pack is absent from the registry")
        for index, pack_id in enumerate(current_pack_ids)
        if pack_id not in registry_ids
    ]
    return sorted(findings)
