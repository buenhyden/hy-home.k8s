"""Closed RIA-001 contract loading and validation."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tempfile
from typing import Mapping

from jsonschema import Draft202012Validator


DEFAULT_CONTRACT_PATH = Path(
    "docs/90.references/data/reference-information-architecture.json"
)
CANONICAL_SCHEMA_PATH = Path(
    "docs/90.references/data/reference-information-architecture.schema.json"
)
ALLOWED_PATH_ROOTS = frozenset({"docs", "scripts", "tests"})
GIT_SHA1_PATTERN = re.compile(r"^git-sha1:([0-9a-f]{40})$")
PACK_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*(?:/[a-z0-9][a-z0-9-]*)*$")
RIA_RULE_IDS = frozenset(
    {
        "RIA-CONTRACT",
        "RIA-BOUNDARY",
        "RIA-SNAPSHOT",
        "RIA-OVERLAY",
        "RIA-SOURCE",
        "RIA-GENERATOR",
        "RIA-DUPLICATE",
    }
)


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
        raise ContractError(
            "RIA-BOUNDARY", field, "path is outside repository root"
        ) from error
    return parse_repository_path(relative.as_posix(), field=field)


def _read_regular_file(root: Path, relative: Path, *, field: str) -> bytes:
    """Read a bounded regular file without following any path symlink."""

    try:
        root_stat = root.lstat()
    except OSError as error:
        raise ContractError(
            "RIA-BOUNDARY", field, "repository root is unavailable"
        ) from error
    if not stat.S_ISDIR(root_stat.st_mode) or stat.S_ISLNK(root_stat.st_mode):
        raise ContractError("RIA-BOUNDARY", field, "repository root is not a directory")
    try:
        directory_fd = os.open(
            root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
        )
    except OSError as error:
        raise ContractError(
            "RIA-BOUNDARY", field, "repository root cannot be opened"
        ) from error
    try:
        for component in relative.parts[:-1]:
            component_stat = os.lstat(component, dir_fd=directory_fd)
            if not stat.S_ISDIR(component_stat.st_mode) or stat.S_ISLNK(
                component_stat.st_mode
            ):
                raise ContractError(
                    "RIA-BOUNDARY", field, "path contains a non-directory"
                )
            next_fd = os.open(
                component,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=directory_fd,
            )
            os.close(directory_fd)
            directory_fd = next_fd
        filename = relative.parts[-1]
        file_stat = os.lstat(filename, dir_fd=directory_fd)
        if not stat.S_ISREG(file_stat.st_mode) or stat.S_ISLNK(file_stat.st_mode):
            raise ContractError("RIA-BOUNDARY", field, "path is not a regular file")
        file_fd = os.open(
            filename,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC,
            dir_fd=directory_fd,
        )
        try:
            if not stat.S_ISREG(os.fstat(file_fd).st_mode):
                raise ContractError("RIA-BOUNDARY", field, "opened path is not regular")
            chunks: list[bytes] = []
            remaining = 2_000_000
            while chunk := os.read(file_fd, min(65_536, remaining + 1)):
                chunks.append(chunk)
                remaining -= len(chunk)
                if remaining < 0:
                    raise ContractError(
                        "RIA-CONTRACT", field, "file exceeds input limit"
                    )
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
        decoded = _read_regular_file(root, relative, field=field).decode(
            "utf-8", "strict"
        )
        loaded = json.loads(decoded, object_pairs_hook=_reject_duplicate_keys)
    except ContractError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ContractError(
            "RIA-CONTRACT", field, "JSON must be valid and unique-keyed"
        ) from error
    if not isinstance(loaded, dict):
        raise ContractError("RIA-CONTRACT", field, "JSON root must be an object")
    return loaded


def parse_git_sha1(value: object) -> str:
    """Return only a fully validated SHA-1 payload for later fixed Git argv use."""

    if not isinstance(value, str):
        raise ContractError(
            "RIA-SNAPSHOT", "snapshotGuard.sourceCommit", "must be encoded SHA-1"
        )
    match = GIT_SHA1_PATTERN.fullmatch(value)
    if match is None:
        raise ContractError(
            "RIA-SNAPSHOT",
            "snapshotGuard.sourceCommit",
            "must be git-sha1:<40 lowercase hex>",
        )
    oid = match.group(1)
    if re.fullmatch(r"[0-9a-f]{40}", oid) is None:
        raise ContractError(
            "RIA-SNAPSHOT", "snapshotGuard.sourceCommit", "SHA-1 payload is invalid"
        )
    return oid


def _validate_schema(
    root: Path, contract: dict[str, object], contract_path: Path
) -> None:
    if contract.get("$schema") != "./reference-information-architecture.schema.json":
        raise ContractError(
            "RIA-CONTRACT", "$schema", "schema reference is not canonical"
        )
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
        raise ContractError(
            "RIA-CONTRACT", location, "contract does not match closed schema"
        )


def _unique_strings(value: object, *, field: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ContractError("RIA-CONTRACT", field, "must be an array of strings")
    if len(set(value)) != len(value):
        raise ContractError("RIA-CONTRACT", field, "contains duplicate values")
    return value


def _validate_path_fields(contract: Mapping[str, object]) -> None:
    """Apply path semantics before schema validation to every path-bearing field."""

    parse_repository_path(
        contract.get("currentPackRegistry"), field="currentPackRegistry"
    )
    projections = contract.get("mutableIndexProjections")
    if isinstance(projections, list):
        for index, projection in enumerate(projections):
            if not isinstance(projection, Mapping):
                continue
            parse_repository_path(
                projection.get("path"), field=f"mutableIndexProjections[{index}].path"
            )
            replacement = projection.get("navigationReplacement")
            if isinstance(replacement, Mapping):
                parse_repository_path(
                    replacement.get("destination"),
                    field=f"mutableIndexProjections[{index}].navigationReplacement.destination",
                )
    data_assets = contract.get("dataAssets")
    if isinstance(data_assets, list):
        for index, asset in enumerate(data_assets):
            if not isinstance(asset, Mapping) or not isinstance(
                asset.get("repositoryEvidence"), list
            ):
                continue
            for evidence_index, path in enumerate(asset["repositoryEvidence"]):
                parse_repository_path(
                    path,
                    field=f"dataAssets[{index}].repositoryEvidence[{evidence_index}]",
                )
    generated_assets = contract.get("generatedAssets")
    if isinstance(generated_assets, list):
        for index, asset in enumerate(generated_assets):
            if not isinstance(asset, Mapping):
                continue
            for key in ("generatorPath", "outputPath", "canonicalOwnerPath"):
                if key in asset:
                    parse_repository_path(
                        asset.get(key), field=f"generatedAssets[{index}].{key}"
                    )
            input_roots = asset.get("inputRoots")
            if isinstance(input_roots, list):
                for root_index, path in enumerate(input_roots):
                    parse_repository_path(
                        path, field=f"generatedAssets[{index}].inputRoots[{root_index}]"
                    )
    duplicate_rules = contract.get("duplicateRules")
    if not isinstance(duplicate_rules, Mapping):
        return
    roots = duplicate_rules.get("canonicalOwnerRoots")
    if isinstance(roots, list):
        for index, path in enumerate(roots):
            parse_repository_path(
                path, field=f"duplicateRules.canonicalOwnerRoots[{index}]"
            )
    exceptions = duplicate_rules.get("structuralExceptions")
    if isinstance(exceptions, list):
        for index, exception in enumerate(exceptions):
            if not isinstance(exception, Mapping):
                continue
            for key in ("canonicalOwnerPath", "referencePath"):
                if key in exception:
                    parse_repository_path(
                        exception.get(key),
                        field=f"duplicateRules.structuralExceptions[{index}].{key}",
                    )


def _validate_contract_boundaries(contract: dict[str, object]) -> None:
    registry_path = parse_repository_path(
        contract.get("currentPackRegistry"), field="currentPackRegistry"
    )
    if registry_path != Path("docs/99.templates/support/document-profiles.json"):
        raise ContractError(
            "RIA-BOUNDARY", "currentPackRegistry", "registry path is fixed"
        )
    guard = contract.get("snapshotGuard")
    if not isinstance(guard, dict):
        raise ContractError("RIA-CONTRACT", "snapshotGuard", "must be an object")
    historical_pack_ids = _unique_strings(
        guard.get("historicalPackIds"), field="snapshotGuard.historicalPackIds"
    )
    current_pack_ids = _unique_strings(
        guard.get("currentPackIds"), field="snapshotGuard.currentPackIds"
    )
    if set(historical_pack_ids) & set(current_pack_ids):
        raise ContractError(
            "RIA-CONTRACT", "snapshotGuard", "historical and Current pack IDs overlap"
        )
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
                raise ContractError(
                    "RIA-CONTRACT", f"{field}[{index}]", "must be an object"
                )
            path = parse_repository_path(
                value.get(key), field=f"{field}[{index}].{key}"
            )
            if path in paths:
                raise ContractError("RIA-CONTRACT", field, "contains duplicate paths")
            paths.add(path)


def load_contract(root: Path, contract_path: Path) -> dict[str, object]:
    """Load one closed contract through no-follow regular-file boundaries."""

    root = root.absolute()
    relative_contract_path = _path_under_root(root, contract_path, field="contract")
    contract = _load_json(root, relative_contract_path, field="contract")
    _validate_path_fields(contract)
    snapshot_guard = contract.get("snapshotGuard")
    if isinstance(snapshot_guard, dict):
        parse_git_sha1(snapshot_guard.get("sourceCommit"))
    _validate_schema(root, contract, relative_contract_path)
    _validate_contract_boundaries(contract)
    return contract


def validate_reference_architecture(
    root: Path, contract: Mapping[str, object]
) -> list[Finding]:
    """Validate the RIA-001 registry references without reading the corpus."""

    registry_path = parse_repository_path(
        contract.get("currentPackRegistry"), field="currentPackRegistry"
    )
    registry = _load_json(root.absolute(), registry_path, field="currentPackRegistry")
    packs_root = registry.get("referenceCurrentPacks")
    if not isinstance(packs_root, dict) or not isinstance(
        packs_root.get("packs"), list
    ):
        raise ContractError(
            "RIA-CONTRACT", "currentPackRegistry", "Current pack registry is malformed"
        )
    registry_ids: set[str] = set()
    for index, pack in enumerate(packs_root["packs"]):
        if not isinstance(pack, dict):
            raise ContractError(
                "RIA-CONTRACT",
                f"currentPackRegistry.packs[{index}]",
                "pack must be an object",
            )
        pack_id = pack.get("id")
        if not isinstance(pack_id, str) or PACK_ID_PATTERN.fullmatch(pack_id) is None:
            raise ContractError(
                "RIA-CONTRACT",
                f"currentPackRegistry.packs[{index}].id",
                "pack ID is invalid",
            )
        if pack_id in registry_ids:
            raise ContractError(
                "RIA-CONTRACT",
                "currentPackRegistry.packs",
                "contains duplicate pack IDs",
            )
        registry_ids.add(pack_id)
    guard = contract.get("snapshotGuard")
    if not isinstance(guard, Mapping):
        raise ContractError("RIA-CONTRACT", "snapshotGuard", "must be an object")
    current_pack_ids = _unique_strings(
        guard.get("currentPackIds"), field="snapshotGuard.currentPackIds"
    )
    if set(current_pack_ids) != registry_ids:
        return [
            Finding(
                "RIA-CONTRACT",
                "snapshotGuard.currentPackIds",
                "Current pack IDs must exactly equal the registry set",
            )
        ]
    return []


def _canonical_schema_bytes() -> bytes:
    """Read the canonical schema through the same no-follow boundary as contracts."""

    repository_root = Path(__file__).resolve().parents[1]
    return _read_regular_file(
        repository_root, CANONICAL_SCHEMA_PATH, field="self-test.schema"
    )


def _self_test_asset() -> dict[str, object]:
    return {
        "id": "asset",
        "repositoryEvidence": ["docs/90.references/data/README.md"],
        "refreshTrigger": "contract change",
        "sources": [
            {
                "url": "https://example.invalid/source",
                "checkedOn": "2026-07-22",
                "adoptedScope": ["contract"],
                "rejectedScope": ["runtime"],
            }
        ],
    }


def _self_test_generated(output_path: str) -> dict[str, object]:
    return {
        "id": "generated",
        "generatorPath": "scripts/generate.py",
        "inputRoots": ["docs/90.references"],
        "outputPath": output_path,
        "checkCommand": "bash scripts/generate.py --check",
        "canonicalOwnerPath": "docs/90.references/README.md",
    }


def _self_test_exception() -> dict[str, object]:
    return {
        "canonicalOwnerPath": "docs/00.agent-governance/README.md",
        "referencePath": "docs/90.references/README.md",
        "paragraphSha256": "a" * 64,
        "structuralRole": "navigation",
        "reason": "bounded structural copy",
    }


def run_self_test() -> None:
    """Exercise the production loader/validator in an isolated repository."""

    accepted = "git-sha1:8fb9821497aaa93d9ed5fc1a69b60c628b047b47"
    bare_oid = accepted.removeprefix("git-sha1:")
    rejected = (
        bare_oid,
        "git-sha1:",
        "git-sha1:git-sha1:8fb9821497aaa93d9ed5fc1a69b60c628b047b47",
        "git-sha1:8FB9821497AAA93D9ED5FC1A69B60C628B047B47",
        "git-sha1:zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz",
        "git-sha1:" + "a" * 64,
        accepted + " trailing",
        " " + accepted,
        accepted + " ",
    )
    if parse_git_sha1(accepted) != accepted.removeprefix("git-sha1:"):
        raise AssertionError("accepted SHA-1 was rejected")
    if bare_oid == accepted:
        raise AssertionError("bare SHA-1 fixture retained its required prefix")
    for value in rejected:
        try:
            parse_git_sha1(value)
        except ContractError:
            continue
        raise AssertionError("malformed SHA-1 was accepted")

    with tempfile.TemporaryDirectory() as temporary_directory:
        root = Path(temporary_directory)
        contract_path = root / DEFAULT_CONTRACT_PATH
        schema_path = contract_path.with_name(
            "reference-information-architecture.schema.json"
        )
        registry_path = root / "docs/99.templates/support/document-profiles.json"
        contract_path.parent.mkdir(parents=True)
        registry_path.parent.mkdir(parents=True)
        schema_path.write_bytes(_canonical_schema_bytes())

        contract: dict[str, object] = {
            "$schema": "./reference-information-architecture.schema.json",
            "schemaVersion": 1,
            "evidenceCutoff": "2026-07-22",
            "currentPackRegistry": "docs/99.templates/support/document-profiles.json",
            "snapshotGuard": {
                "sourceCommit": accepted,
                "historicalPackIds": [],
                "currentPackIds": ["audits/a", "research/b"],
            },
            "mutableIndexProjections": [],
            "dataAssets": [],
            "generatedAssets": [],
            "duplicateRules": {
                "canonicalOwnerRoots": ["docs/00.agent-governance"],
                "minimumParagraphCharacters": 1,
                "structuralExceptions": [],
            },
        }

        def write_registry(packs: object) -> None:
            registry_path.write_text(
                json.dumps({"referenceCurrentPacks": {"packs": packs}}),
                encoding="utf-8",
            )

        def write_contract(value: object) -> None:
            contract_path.write_text(json.dumps(value), encoding="utf-8")

        def expect_error(value: object, *, validate: bool = False) -> None:
            write_contract(value)
            try:
                loaded = load_contract(root, contract_path)
                if validate and validate_reference_architecture(root, loaded):
                    return
            except ContractError:
                return
            raise AssertionError("invalid isolated probe was accepted")

        write_registry([{"id": "audits/a"}, {"id": "research/b"}])
        write_contract(contract)
        if validate_reference_architecture(root, load_contract(root, contract_path)):
            raise AssertionError("accepted isolated contract produced findings")

        contract_path.write_text(
            '{"schemaVersion":1,"schemaVersion":1}', encoding="utf-8"
        )
        try:
            load_contract(root, contract_path)
        except ContractError:
            pass
        else:
            raise AssertionError("duplicate key was accepted")

        nested_guard = dict(contract["snapshotGuard"])
        nested_guard["unknown"] = True
        incomplete = dict(contract)
        incomplete.pop("evidenceCutoff")
        cardinality = dict(contract)
        cardinality["duplicateRules"] = {
            **contract["duplicateRules"],
            "canonicalOwnerRoots": [],
        }
        for mutation in (
            {**contract, "unknown": True},
            {**contract, "schemaVersion": 2},
            {**contract, "snapshotGuard": nested_guard},
            incomplete,
            cardinality,
            {**contract, "currentPackRegistry": "docs/../unsafe.json"},
            {
                **contract,
                "mutableIndexProjections": [{"path": "docs/../mutable.md"}],
            },
            {
                **contract,
                "mutableIndexProjections": [
                    {
                        "path": "docs/90.references/README.md",
                        "navigationReplacement": {
                            "visibleText": "Current",
                            "destination": "docs/../target.md",
                        },
                    }
                ],
            },
            {
                **contract,
                "dataAssets": [
                    {
                        **_self_test_asset(),
                        "repositoryEvidence": ["docs/../evidence.md"],
                    }
                ],
            },
            {
                **contract,
                "generatedAssets": [
                    {
                        **_self_test_generated("docs/90.references/data/output.md"),
                        "generatorPath": "scripts/../generator.py",
                    }
                ],
            },
            {
                **contract,
                "generatedAssets": [
                    {
                        **_self_test_generated("docs/90.references/data/output.md"),
                        "inputRoots": ["docs/../inputs"],
                    }
                ],
            },
            {
                **contract,
                "generatedAssets": [_self_test_generated("docs/../output.md")],
            },
            {
                **contract,
                "generatedAssets": [
                    _self_test_generated("docs/90.references/data/output.md"),
                    {
                        **_self_test_generated("docs/90.references/data/output.md"),
                        "id": "generated-second",
                    },
                ],
            },
            {
                **contract,
                "generatedAssets": [
                    {
                        **_self_test_generated("docs/90.references/data/output.md"),
                        "canonicalOwnerPath": "docs/../owner.md",
                    }
                ],
            },
            {
                **contract,
                "duplicateRules": {
                    **contract["duplicateRules"],
                    "canonicalOwnerRoots": ["docs/../owner"],
                },
            },
            {
                **contract,
                "duplicateRules": {
                    **contract["duplicateRules"],
                    "structuralExceptions": [
                        {
                            **_self_test_exception(),
                            "referencePath": "docs/../reference.md",
                        }
                    ],
                },
            },
            {
                **contract,
                "snapshotGuard": {
                    **contract["snapshotGuard"],
                    "currentPackIds": ["audits/a"],
                },
            },
        ):
            expect_error(mutation, validate=True)

        for packs in ([{}], [{"id": "audits/a"}, {"id": "audits/a"}]):
            write_registry(packs)
            write_contract(contract)
            try:
                validate_reference_architecture(
                    root, load_contract(root, contract_path)
                )
            except ContractError:
                pass
            else:
                raise AssertionError("malformed registry was accepted")

        write_registry([{"id": "audits/a"}, {"id": "research/b"}])
        registry_path.unlink()
        registry_path.mkdir()
        expect_error(contract, validate=True)
        registry_path.rmdir()
        write_registry([{"id": "audits/a"}, {"id": "research/b"}])
        link_path = contract_path.with_name("contract-link.json")
        link_path.symlink_to(contract_path)
        try:
            load_contract(root, link_path)
        except ContractError:
            return
        raise AssertionError("symlink contract was accepted")
