"""Typed document-profile registry loading and deterministic path routing."""

from __future__ import annotations

import json
import re
import stat
import subprocess
from dataclasses import dataclass
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path, PurePosixPath
from typing import Any, Literal, Mapping, NoReturn, Sequence

import yaml
from jsonschema import Draft202012Validator


BASELINE_SHA = "8e1b00b4dfb84b8431ba4d3d31b4ad0445a0019d"  # pragma: allowlist secret
BASELINE_COUNT = 433
_LS_TREE_MODE_TYPES = {
    b"040000": b"tree",
    b"100644": b"blob",
    b"100755": b"blob",
    b"120000": b"blob",
    b"160000": b"commit",
}
_LS_FILES_MODES = {b"100644", b"100755", b"120000", b"160000"}
ROOT_FILES = ("AGENTS.md", "CLAUDE.md", "GEMINI.md", "README.md")
TARGET_ROOTS = (
    "_workspace",
    ".agents",
    ".claude",
    ".codex",
    ".github",
    "docs",
    "examples",
    "gitops",
    "infrastructure",
    "policy",
    "scripts",
    "secrets",
    "tests",
    "traefik",
)
REGISTRY_PATH = PurePosixPath("docs/99.templates/support/document-profiles.json")
SCHEMA_PATH = PurePosixPath("docs/99.templates/support/document-profiles.schema.json")
_EVIDENCE_PREDICATE_SEMANTICS = {
    "archive-source-removal": (
        "source-removed-and-mirror-created",
        ("archive-envelope", "same-diff", "source-removal"),
    ),
    "activate-self-body": ("self-status-and-body", ("same-diff",)),
    "activate-heading-profile": (
        "self-status-and-body",
        ("rendered-link", "same-diff"),
    ),
    "activate-execution-pair": (
        "pair-created-or-status-changed",
        ("rendered-link", "reciprocal-link", "same-diff"),
    ),
    "complete-product-program": (
        "target-and-last-relation-changed",
        ("program-lineage-closed", "same-diff"),
    ),
    "accept-architecture": (
        "target-and-evidence-status-body-changed",
        ("rendered-link", "reciprocal-link", "same-diff"),
    ),
    "accept-decision-self": (
        "self-status-and-body",
        ("rendered-link", "same-diff"),
    ),
    "complete-specification": (
        "target-plan-task-status-changed",
        ("rendered-link", "reciprocal-link", "same-diff"),
    ),
    "complete-execution-pair": (
        "pair-status-changed",
        (
            "rendered-link",
            "reciprocal-link",
            "task-terminal-evidence",
            "same-diff",
        ),
    ),
    "accept-operated-document": (
        "target-plan-task-status-changed",
        ("rendered-link", "same-diff"),
    ),
    "terminate-reviewed-reference": (
        "target-plan-task-status-changed",
        ("rendered-link", "same-diff"),
    ),
}


@dataclass(frozen=True)
class Route:
    kind: Literal["exact", "regex"]
    value: str


@dataclass(frozen=True)
class Diagnostic:
    rule_id: str
    path: PurePosixPath
    profile: str
    expected: str
    actual: str
    owner: str


@dataclass(frozen=True)
class FrontmatterContract:
    mode: Literal["required", "forbidden", "not-applicable"]
    required: tuple[str, ...]
    allowed: tuple[str, ...]
    order: tuple[str, ...]


@dataclass(frozen=True)
class HeadingContract:
    required: tuple[str, ...]
    allowed: tuple[str, ...]


@dataclass(frozen=True)
class AppendContract:
    parent_profile_id: str
    parent_h2: str
    entry_heading_level: Literal[3]
    section_heading_level: Literal[4]
    required_sections: tuple[str, ...]


@dataclass(frozen=True)
class IdentifierColumn:
    column: str
    kind: Literal["requirement", "criterion", "work-item"]


@dataclass(frozen=True)
class BodyContract:
    section: str
    table_heading: str
    enforced_statuses: tuple[str, ...]
    required_columns: tuple[str, ...]
    identifier_columns: tuple[IdentifierColumn, ...]
    source_link_column: str | None
    target_link_column: str | None
    allowed_source_profile_ids: tuple[str, ...]
    allowed_target_profile_ids: tuple[str, ...]
    reciprocal_evidence: bool
    allow_explicit_exclusion: bool


@dataclass(frozen=True)
class ConstantConstraint:
    source: Literal["literal", "profile-id"]
    value: str | int | float | bool | None


@dataclass(frozen=True)
class EnumConstraint:
    source: Literal["literal", "status-domain"]
    values: tuple[str | int | float | bool | None, ...]


@dataclass(frozen=True)
class ConditionalConstraint:
    key: str
    operator: Literal["equals", "not-equals"]
    value: str | int | float | bool | None
    effect: Literal["required", "forbidden"]


@dataclass(frozen=True)
class KeyValueContract:
    key: str
    kind: Literal["string", "date", "integer", "number", "boolean"]
    nullable: bool
    constant: ConstantConstraint | None
    enum: EnumConstraint | None
    pattern: str | None
    conditional: ConditionalConstraint | None


@dataclass(frozen=True)
class ValueContract:
    contract_id: str
    profile_ids: tuple[str, ...]
    keys: tuple[KeyValueContract, ...]


@dataclass(frozen=True)
class RoleDecision:
    role: str
    source_profile_id: str | None
    relationship_section: str | None
    body_requirement: Literal["body-contract", "heading-set", "none"]


@dataclass(frozen=True)
class CreateAdmission:
    mode: Literal["states", "paired", "archive-envelope", "snapshot-only"]
    states: tuple[str, ...]
    evidence_predicate_id: str | None


@dataclass(frozen=True)
class AdmissionPolicy:
    policy_id: str
    profile_ids: tuple[str, ...]
    create: CreateAdmission
    delete: Literal["deny"]
    rename: Literal["deny"]
    profile_change: Literal["deny"]
    baseline_paths: tuple[PurePosixPath, ...]


@dataclass(frozen=True)
class LifecycleEdge:
    from_state: str
    to_state: str
    predicate_id: str


@dataclass(frozen=True)
class LifecycleContract:
    contract_id: str
    profile_ids: tuple[str, ...]
    terminal_states: tuple[str, ...]
    edges: tuple[LifecycleEdge, ...]


@dataclass(frozen=True)
class ProfileEdge:
    profile_id: str
    from_state: str
    to_state: str


@dataclass(frozen=True)
class EvidenceRequirement:
    profile_ids: tuple[str, ...]
    states: tuple[str, ...]
    minimum: int
    maximum: int | None


@dataclass(frozen=True)
class EvidencePredicate:
    predicate_id: str
    profile_edges: tuple[ProfileEdge, ...]
    evidence: tuple[EvidenceRequirement, ...]
    relationship: Literal[
        "self", "role-decision", "pair", "program-lineage", "archive-source"
    ]
    minimum: int
    maximum: int | None
    same_diff: Literal[
        "self-status-and-body",
        "pair-created-or-status-changed",
        "target-and-last-relation-changed",
        "target-and-evidence-status-body-changed",
        "target-plan-task-status-changed",
        "pair-status-changed",
        "source-removed-and-mirror-created",
    ]
    body_requirement: Literal["body-contract", "heading-set", "none"]
    capabilities: tuple[str, ...]


@dataclass(frozen=True)
class DocumentProfile:
    profile_id: str
    profile_class: Literal["sdlc", "common", "governance", "readme", "exception"]
    routes: tuple[Route, ...]
    frontmatter: FrontmatterContract
    status_domain: tuple[str, ...]
    headings: HeadingContract
    template: PurePosixPath | None
    mode: Literal[
        "authored",
        "template",
        "frontmatter-free",
        "classification-only",
        "generated",
        "non-target",
    ]
    source_profile_ids: tuple[str, ...]
    placeholder_policy: Literal["forbidden", "template-only"]
    append_contract: AppendContract | None
    body_contract: BodyContract | None
    value_contract: ValueContract
    role_decision: RoleDecision
    admission: AdmissionPolicy
    lifecycle: LifecycleContract


@dataclass(frozen=True)
class GovernanceCurrentOwners:
    profile_id: str
    allowed_states: tuple[str, ...]
    paths: tuple[PurePosixPath, ...]


@dataclass(frozen=True)
class ReferenceCurrentPack:
    id: str
    allowed_states: tuple[str, ...]
    members: tuple[str, ...]

    @property
    def collection_readme(self) -> PurePosixPath:
        collection = self.id.split("/", 1)[0]
        return PurePosixPath(f"docs/90.references/{collection}/README.md")

    @property
    def pack_readme(self) -> PurePosixPath:
        return PurePosixPath(f"docs/90.references/{self.id}/README.md")

    @property
    def member_paths(self) -> tuple[PurePosixPath, ...]:
        return tuple(
            PurePosixPath(f"docs/90.references/{self.id}/{member}")
            for member in self.members
        )


@dataclass(frozen=True)
class ReferenceCurrentPacks:
    profile_id: str
    packs: tuple[ReferenceCurrentPack, ...]


@dataclass(frozen=True)
class ProgramRelation:
    spec_id: str
    order: int
    state: str
    reason: str
    decision_id: str


@dataclass(frozen=True)
class ProgramFollowUp(ProgramRelation):
    evidence_mode: Literal["reciprocal-body", "successor-record"]


@dataclass(frozen=True)
class ProgramLineage:
    prd_id: str
    ard_id: str
    tranches: tuple[ProgramRelation, ...]
    follow_ups: tuple[ProgramFollowUp, ...]


@dataclass(frozen=True)
class Registry:
    schema_version: int
    baseline_sha: str
    baseline_count: int
    profiles: tuple[DocumentProfile, ...]
    governance_current_owners: GovernanceCurrentOwners
    reference_current_packs: ReferenceCurrentPacks
    program_lineage: tuple[ProgramLineage, ...]
    evidence_predicates: tuple[EvidencePredicate, ...]


@dataclass(frozen=True)
class TargetInventory:
    baseline_paths: tuple[PurePosixPath, ...]
    current_paths: tuple[PurePosixPath, ...]
    new_paths: tuple[PurePosixPath, ...]
    baseline_symlink_paths: tuple[PurePosixPath, ...]
    current_symlink_paths: tuple[PurePosixPath, ...]


@dataclass(frozen=True)
class _GitEntry:
    mode: str
    path: PurePosixPath
    stage: int | None = None


class DocumentContractError(ValueError):
    """A deterministic registry or classification failure."""

    def __init__(self, diagnostics: Sequence[Diagnostic]):
        self.diagnostics = tuple(diagnostics)
        super().__init__("; ".join(item.rule_id for item in self.diagnostics))


class _DuplicateJSONKeyError(ValueError):
    """Internal marker for a duplicate JSON mapping key at any depth."""


class _UniqueKeySafeLoader(yaml.SafeLoader):
    """YAML SafeLoader variant that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: _UniqueKeySafeLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeySafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _diagnostic(
    rule_id: str,
    *,
    path: PurePosixPath = REGISTRY_PATH,
    profile: str = "",
    expected: str,
    actual: str,
) -> Diagnostic:
    return Diagnostic(
        rule_id=rule_id,
        path=path,
        profile=profile,
        expected=expected,
        actual=actual,
        owner="document-contract-registry",
    )


def _fail(rule_id: str, *, expected: str, actual: str) -> NoReturn:
    raise DocumentContractError(
        (_diagnostic(rule_id, expected=expected, actual=actual),)
    )


def load_json_file(
    path: Path, *, diagnostic_path: PurePosixPath = REGISTRY_PATH
) -> Any:
    """Load JSON once with duplicate mapping keys rejected at every depth."""

    def reject_duplicate_keys(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise _DuplicateJSONKeyError("duplicate JSON object key")
            result[key] = value
        return result

    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle, object_pairs_hook=reject_duplicate_keys)
    except (_DuplicateJSONKeyError, json.JSONDecodeError) as exc:
        raise DocumentContractError(
            (
                _diagnostic(
                    "REGISTRY_SCHEMA",
                    path=diagnostic_path,
                    expected="valid JSON with unique mapping keys at every depth",
                    actual="JSON decoding or duplicate-key failure",
                ),
            )
        ) from exc


def _normalize_relative_path(value: str | PurePosixPath) -> PurePosixPath:
    raw = str(value)
    if not raw or raw == ".":
        raise ValueError("path must not be empty")
    if raw.startswith("./"):
        raise ValueError("path must not start with './'")
    if "\\" in raw:
        raise ValueError("path must use POSIX separators")
    if any(ord(character) < 32 or ord(character) == 127 for character in raw):
        raise ValueError("path must not contain control characters")
    path = PurePosixPath(raw)
    if path.is_absolute():
        raise ValueError("path must be repository-relative")
    if ".." in path.parts:
        raise ValueError("path must not contain '..'")
    return path


def _decode_git_path(raw: bytes) -> PurePosixPath:
    try:
        return _normalize_relative_path(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise ValueError("git returned an invalid repository-relative path") from exc


def _validate_git_object_id(raw_object: bytes, command: str) -> None:
    if len(raw_object) not in {40, 64}:
        raise ValueError(f"{command} object id must be exactly 40 or 64 characters")
    if re.fullmatch(rb"[0-9a-f]+", raw_object) is None:
        raise ValueError(f"{command} object id must be lowercase hexadecimal")


def _parse_ls_tree_z(raw: bytes) -> tuple[_GitEntry, ...]:
    """Parse ``git ls-tree -z`` output without interpreting path contents."""

    entries: list[_GitEntry] = []
    records = raw.split(b"\0")
    if records[-1] != b"":
        raise ValueError("git ls-tree output is not NUL terminated")
    for record in records[:-1]:
        try:
            header, raw_path = record.split(b"\t", 1)
            raw_mode, raw_type, raw_object = header.split(b" ", 2)
        except ValueError as exc:
            raise ValueError("malformed git ls-tree record") from exc
        if raw_type not in {b"blob", b"tree", b"commit"}:
            raise ValueError("unsupported git ls-tree object type")
        if raw_mode not in _LS_TREE_MODE_TYPES:
            raise ValueError("noncanonical git ls-tree mode")
        if _LS_TREE_MODE_TYPES[raw_mode] != raw_type:
            raise ValueError("impossible git ls-tree mode/type pair")
        _validate_git_object_id(raw_object, "git ls-tree")
        entries.append(
            _GitEntry(mode=raw_mode.decode("ascii"), path=_decode_git_path(raw_path))
        )
    return tuple(entries)


def _parse_ls_files_stage_z(raw: bytes) -> tuple[_GitEntry, ...]:
    """Parse ``git ls-files --stage -z`` output, retaining mode and stage."""

    entries: list[_GitEntry] = []
    records = raw.split(b"\0")
    if records[-1] != b"":
        raise ValueError("git ls-files output is not NUL terminated")
    for record in records[:-1]:
        try:
            header, raw_path = record.split(b"\t", 1)
            raw_mode, raw_object, raw_stage = header.split(b" ", 2)
        except ValueError as exc:
            raise ValueError("malformed git ls-files record") from exc
        if raw_mode not in _LS_FILES_MODES:
            raise ValueError("noncanonical git ls-files mode")
        _validate_git_object_id(raw_object, "git ls-files")
        if raw_stage not in {b"0", b"1", b"2", b"3"}:
            raise ValueError("invalid git ls-files stage")
        entries.append(
            _GitEntry(
                mode=raw_mode.decode("ascii"),
                path=_decode_git_path(raw_path),
                stage=int(raw_stage),
            )
        )
    return tuple(entries)


def _run_git(root: Path, arguments: Sequence[str]) -> bytes:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout


def _within_target_scope(path: PurePosixPath) -> bool:
    if path.as_posix() == "RTK.md":
        return False
    if not path.parts:
        return False
    if path.parts[0] in {"graphify-out", ".worktrees"}:
        return False
    return path.as_posix() in ROOT_FILES or path.parts[0] in TARGET_ROOTS


def _is_target_markdown(path: PurePosixPath) -> bool:
    return path.suffix == ".md" and _within_target_scope(path)


def _sorted_paths(paths: set[PurePosixPath]) -> tuple[PurePosixPath, ...]:
    return tuple(sorted(paths, key=lambda item: item.as_posix()))


def _is_ignored(root: Path, path: PurePosixPath) -> bool:
    completed = subprocess.run(
        ["git", "check-ignore", "--quiet", "--", path.as_posix()],
        cwd=root,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    if completed.returncode == 0:
        return True
    if completed.returncode == 1:
        return False
    raise subprocess.CalledProcessError(
        completed.returncode, completed.args, stderr=completed.stderr
    )


def _lstat_named_path(root: Path, path: PurePosixPath) -> int:
    current = root
    for part in path.parts:
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError as exc:
            raise ValueError(
                f"included path does not exist: {path.as_posix()}"
            ) from exc
        if stat.S_ISLNK(mode):
            raise ValueError(
                f"included path crosses or names a symlink: {path.as_posix()}"
            )
    return mode


def read_repository_text(root: Path, path: PurePosixPath) -> str:
    """Read one normalized regular file without following path symlinks."""

    normalized = _normalize_relative_path(path)
    mode = _lstat_named_path(root.absolute(), normalized)
    if not stat.S_ISREG(mode):
        raise ValueError(f"repository path is not a regular file: {normalized}")
    return (root.absolute() / normalized).read_text(encoding="utf-8")


def is_ignored_repository_path(root: Path, path: PurePosixPath) -> bool:
    """Return Git's ignore decision for one normalized repository path."""

    return _is_ignored(root.absolute(), _normalize_relative_path(path))


def diagnostic_sort_key(diagnostic: Diagnostic) -> tuple[str, str, str, str]:
    """Return the stable cross-validator diagnostic ordering contract."""

    return (
        diagnostic.path.as_posix(),
        diagnostic.rule_id,
        diagnostic.expected,
        diagnostic.actual,
    )


def enumerate_target_markdown(
    root: Path,
    *,
    include_paths: tuple[PurePosixPath, ...] = (),
) -> TargetInventory:
    root = root.absolute()
    baseline_entries = _parse_ls_tree_z(
        _run_git(root, ("ls-tree", "-rz", "--full-tree", BASELINE_SHA))
    )
    current_entries = _parse_ls_files_stage_z(
        _run_git(root, ("ls-files", "--stage", "-z"))
    )

    baseline_paths = {
        entry.path
        for entry in baseline_entries
        if entry.mode.startswith("100") and _is_target_markdown(entry.path)
    }
    if len(baseline_paths) != BASELINE_COUNT:
        raise ValueError(
            "baseline Markdown inventory count mismatch: "
            f"expected {BASELINE_COUNT}, actual {len(baseline_paths)}"
        )
    current_paths: set[PurePosixPath] = set()
    for entry in current_entries:
        if not entry.mode.startswith("100") or not _is_target_markdown(entry.path):
            continue
        try:
            mode = _lstat_named_path(root, entry.path)
        except ValueError:
            continue
        if stat.S_ISREG(mode):
            current_paths.add(entry.path)
    baseline_symlinks = {
        entry.path
        for entry in baseline_entries
        if entry.mode == "120000" and _within_target_scope(entry.path)
    }
    current_symlinks = {
        entry.path
        for entry in current_entries
        if entry.mode == "120000" and _within_target_scope(entry.path)
    }
    current_paths.difference_update(current_symlinks)

    for requested_path in include_paths:
        try:
            path = _normalize_relative_path(requested_path)
        except ValueError as exc:
            raise ValueError(f"invalid included path: {requested_path}") from exc
        if _is_ignored(root, path):
            raise ValueError(f"included path is ignored: {path.as_posix()}")
        mode = _lstat_named_path(root, path)
        if not stat.S_ISREG(mode):
            raise ValueError(f"included path is not a regular file: {path.as_posix()}")
        if path in current_symlinks:
            raise ValueError(
                f"included path is indexed as a symlink: {path.as_posix()}"
            )
        if not _is_target_markdown(path):
            raise ValueError(
                f"included path is not approved Markdown: {path.as_posix()}"
            )
        current_paths.add(path)

    return TargetInventory(
        baseline_paths=_sorted_paths(baseline_paths),
        current_paths=_sorted_paths(current_paths),
        new_paths=_sorted_paths(current_paths - baseline_paths),
        baseline_symlink_paths=_sorted_paths(baseline_symlinks),
        current_symlink_paths=_sorted_paths(current_symlinks),
    )


def enumerate_tracked_regular_paths(
    root: Path,
    *,
    pathspecs: Sequence[str],
) -> tuple[PurePosixPath, ...]:
    """Return one closed Git-index inventory for the supplied pathspecs.

    The caller owns the semantic path selection. This helper retains only
    stage-zero regular blobs and fails closed on conflicts, symlinks,
    submodules, or duplicate index entries in the selected surface.
    """

    if not pathspecs or any(
        not isinstance(item, str) or not item for item in pathspecs
    ):
        raise ValueError("tracked regular inventory requires non-empty pathspecs")
    entries = _parse_ls_files_stage_z(
        _run_git(root.absolute(), ("ls-files", "--stage", "-z", "--", *pathspecs))
    )
    grouped: dict[PurePosixPath, list[_GitEntry]] = {}
    for entry in entries:
        grouped.setdefault(entry.path, []).append(entry)
    paths: set[PurePosixPath] = set()
    for path, selected in grouped.items():
        if (
            len(selected) != 1
            or selected[0].stage != 0
            or not selected[0].mode.startswith("100")
        ):
            raise ValueError(
                "tracked native surface is not one stage-zero regular blob: "
                f"{path.as_posix()}"
            )
        paths.add(path)
    return _sorted_paths(paths)


@lru_cache(maxsize=None)
def _compile_route(value: str) -> re.Pattern[str]:
    return re.compile(value)


def _schema_rule_id(error: Any) -> str:
    path = tuple(error.absolute_path)
    nested_errors = [error]
    for nested_error in nested_errors:
        nested_errors.extend(nested_error.context)
    nested_paths = [tuple(item.absolute_path) for item in nested_errors]
    if path and path[0] == "documentContracts":
        messages = " ".join(item.message for item in nested_errors)
        if "valueContracts" in path or "valueContracts" in messages:
            return "REGISTRY_VALUE_CONTRACT"
        if "roleDecisions" in path or "roleDecisions" in messages:
            return "REGISTRY_ROLE_DECISION"
        if "admissionPolicies" in path or "admissionPolicies" in messages:
            return "REGISTRY_ADMISSION"
        if "lifecycleContracts" in path or "lifecycleContracts" in messages:
            return "REGISTRY_LIFECYCLE"
        if "evidencePredicates" in path or "evidencePredicates" in messages:
            return "REGISTRY_EVIDENCE_PREDICATE"
        return "REGISTRY_SCHEMA"
    if any("bodyContract" in nested_path for nested_path in nested_paths) or (
        error.validator == "required" and "bodyContract" in error.message
    ):
        if error.validator == "required" and "bodyContract" in error.message:
            return "REGISTRY_BODY_REQUIRED"
        if any(item.validator == "additionalProperties" for item in nested_errors):
            return "REGISTRY_BODY_FIELD"
        if any("requiredColumns" in nested_path for nested_path in nested_paths):
            return "REGISTRY_BODY_COLUMNS"
        if any("identifierColumns" in nested_path for nested_path in nested_paths):
            return "REGISTRY_BODY_IDENTIFIER_COLUMN"
        return "REGISTRY_BODY_SCHEMA"
    if error.validator == "required" and "referenceCurrentPacks" in error.message:
        return "REGISTRY_REFERENCE_CURRENT_PACK_DECLARATION"
    if path and path[0] == "referenceCurrentPacks":
        if len(path) >= 3 and path[1] == "packs" and error.validator == "required":
            if "allowedStates" in error.message:
                return "REGISTRY_REFERENCE_CURRENT_PACK_STATE"
            if "members" in error.message:
                return "REGISTRY_REFERENCE_CURRENT_PACK_PATH"
            if "id" in error.message:
                return "REGISTRY_REFERENCE_CURRENT_PACK_ID"
        if len(path) >= 4 and path[1] == "packs":
            field = path[3]
            if field == "id":
                return "REGISTRY_REFERENCE_CURRENT_PACK_ID"
            if field == "allowedStates":
                return "REGISTRY_REFERENCE_CURRENT_PACK_STATE"
            if field == "members":
                if error.validator == "uniqueItems":
                    return "REGISTRY_REFERENCE_CURRENT_PACK_DUPLICATE"
                return "REGISTRY_REFERENCE_CURRENT_PACK_PATH"
        return "REGISTRY_REFERENCE_CURRENT_PACK_DECLARATION"
    if path and path[0] == "governanceCurrentOwners":
        if error.validator == "required" and "allowedStates" in error.message:
            return "REGISTRY_GOVERNANCE_CURRENT_OWNER_STATE"
        if error.validator == "required" and "paths" in error.message:
            return "REGISTRY_GOVERNANCE_CURRENT_OWNER_PATH"
        if len(path) >= 2 and path[1] == "allowedStates":
            return "REGISTRY_GOVERNANCE_CURRENT_OWNER_STATE"
        if len(path) >= 2 and path[1] == "paths":
            if error.validator == "uniqueItems":
                return "REGISTRY_GOVERNANCE_CURRENT_OWNER_DUPLICATE"
            return "REGISTRY_GOVERNANCE_CURRENT_OWNER_PATH"
    if path and path[0] == "programLineage":
        messages = " ".join(item.message for item in nested_errors)
        if "evidenceMode" in path or "evidenceMode" in messages:
            return "REGISTRY_PROGRAM_EVIDENCE_MODE"
        if "decision" in path or "decision" in messages:
            return "REGISTRY_PROGRAM_DECISION"
        if "state" in path or "state" in messages:
            return "REGISTRY_PROGRAM_STATE"
        return "REGISTRY_SCHEMA"
    if len(path) >= 4 and path[-1] == "kind" and "routes" in path:
        return "REGISTRY_ROUTE_KIND"
    return "REGISTRY_SCHEMA"


def _append_contract(raw: Mapping[str, Any] | None) -> AppendContract | None:
    if raw is None:
        return None
    return AppendContract(
        parent_profile_id=raw["parentProfileId"],
        parent_h2=raw["parentH2"],
        entry_heading_level=raw["entryHeadingLevel"],
        section_heading_level=raw["sectionHeadingLevel"],
        required_sections=tuple(raw["requiredSections"]),
    )


def _body_contract(raw: Mapping[str, Any] | None) -> BodyContract | None:
    if raw is None:
        return None
    return BodyContract(
        section=raw["section"],
        table_heading=raw["tableHeading"],
        enforced_statuses=tuple(raw["enforcedStatuses"]),
        required_columns=tuple(raw["requiredColumns"]),
        identifier_columns=tuple(
            IdentifierColumn(column=item["column"], kind=item["kind"])
            for item in raw["identifierColumns"]
        ),
        source_link_column=raw["sourceLinkColumn"],
        target_link_column=raw["targetLinkColumn"],
        allowed_source_profile_ids=tuple(raw["allowedSourceProfileIds"]),
        allowed_target_profile_ids=tuple(raw["allowedTargetProfileIds"]),
        reciprocal_evidence=raw["reciprocalEvidence"],
        allow_explicit_exclusion=raw["allowExplicitExclusion"],
    )


def _constant_constraint(raw: Mapping[str, Any] | None) -> ConstantConstraint | None:
    if raw is None:
        return None
    return ConstantConstraint(source=raw["source"], value=raw["value"])


def _enum_constraint(raw: Mapping[str, Any] | None) -> EnumConstraint | None:
    if raw is None:
        return None
    return EnumConstraint(source=raw["source"], values=tuple(raw["values"]))


def _conditional_constraint(
    raw: Mapping[str, Any] | None,
) -> ConditionalConstraint | None:
    if raw is None:
        return None
    return ConditionalConstraint(
        key=raw["key"],
        operator=raw["operator"],
        value=raw["value"],
        effect=raw["effect"],
    )


def _value_contract(raw: Mapping[str, Any]) -> ValueContract:
    return ValueContract(
        contract_id=raw["id"],
        profile_ids=tuple(raw["profileIds"]),
        keys=tuple(
            KeyValueContract(
                key=item["key"],
                kind=item["kind"],
                nullable=item["nullable"],
                constant=_constant_constraint(item["constant"]),
                enum=_enum_constraint(item["enum"]),
                pattern=item["pattern"],
                conditional=_conditional_constraint(item["conditional"]),
            )
            for item in raw["keys"]
        ),
    )


def _role_decision(
    raw: Mapping[str, Any], *, source_profile_id: str | None = None
) -> RoleDecision:
    return RoleDecision(
        role=raw["role"],
        source_profile_id=(
            source_profile_id
            if source_profile_id is not None
            else raw["sourceProfileId"]
        ),
        relationship_section=raw["relationshipSection"],
        body_requirement=raw["bodyRequirement"],
    )


def _admission_policy(raw: Mapping[str, Any]) -> AdmissionPolicy:
    return AdmissionPolicy(
        policy_id=raw["id"],
        profile_ids=tuple(raw["profileIds"]),
        create=CreateAdmission(
            mode=raw["create"]["mode"],
            states=tuple(raw["create"]["states"]),
            evidence_predicate_id=raw["create"]["evidencePredicateId"],
        ),
        delete=raw["delete"],
        rename=raw["rename"],
        profile_change=raw["profileChange"],
        baseline_paths=tuple(PurePosixPath(path) for path in raw["baselinePaths"]),
    )


def _lifecycle_contract(raw: Mapping[str, Any]) -> LifecycleContract:
    return LifecycleContract(
        contract_id=raw["id"],
        profile_ids=tuple(raw["profileIds"]),
        terminal_states=tuple(raw["terminalStates"]),
        edges=tuple(
            LifecycleEdge(
                from_state=edge["from"],
                to_state=edge["to"],
                predicate_id=edge["predicateId"],
            )
            for edge in raw["edges"]
        ),
    )


def _evidence_predicate(raw: Mapping[str, Any]) -> EvidencePredicate:
    return EvidencePredicate(
        predicate_id=raw["id"],
        profile_edges=tuple(
            ProfileEdge(
                profile_id=edge["profileId"],
                from_state=edge["from"],
                to_state=edge["to"],
            )
            for edge in raw["profileEdges"]
        ),
        evidence=tuple(
            EvidenceRequirement(
                profile_ids=tuple(item["profileIds"]),
                states=tuple(item["states"]),
                minimum=item["minimum"],
                maximum=item["maximum"],
            )
            for item in raw["evidence"]
        ),
        relationship=raw["relationship"],
        minimum=raw["cardinality"]["minimum"],
        maximum=raw["cardinality"]["maximum"],
        same_diff=raw["sameDiff"],
        body_requirement=raw["bodyRequirement"],
        capabilities=tuple(raw["capabilities"]),
    )


def _profile_from_mapping(
    raw: Mapping[str, Any],
    *,
    value_contract: ValueContract,
    role_decision: RoleDecision,
    admission: AdmissionPolicy,
    lifecycle: LifecycleContract,
) -> DocumentProfile:
    template = raw["template"]
    routes = tuple(
        Route(
            kind=route["kind"],
            value=(
                _normalize_relative_path(route["value"]).as_posix()
                if route["kind"] == "exact"
                else route["value"]
            ),
        )
        for route in raw["routes"]
    )
    return DocumentProfile(
        profile_id=raw["id"],
        profile_class=raw["class"],
        routes=routes,
        frontmatter=FrontmatterContract(
            mode=raw["frontmatter"]["mode"],
            required=tuple(raw["frontmatter"]["required"]),
            allowed=tuple(raw["frontmatter"]["allowed"]),
            order=tuple(raw["frontmatter"]["order"]),
        ),
        status_domain=tuple(raw["statusDomain"]),
        headings=HeadingContract(
            required=tuple(raw["headings"]["required"]),
            allowed=tuple(raw["headings"]["allowed"]),
        ),
        template=_normalize_relative_path(template) if template is not None else None,
        mode=raw["mode"],
        source_profile_ids=tuple(raw["sourceProfileIds"]),
        placeholder_policy=raw["placeholderPolicy"],
        append_contract=_append_contract(raw["appendContract"]),
        body_contract=_body_contract(raw["bodyContract"]),
        value_contract=value_contract,
        role_decision=role_decision,
        admission=admission,
        lifecycle=lifecycle,
    )


def _reference_pack_from_mapping(raw: Mapping[str, Any]) -> ReferenceCurrentPack:
    return ReferenceCurrentPack(
        id=raw["id"],
        allowed_states=tuple(raw["allowedStates"]),
        members=tuple(raw["members"]),
    )


def _program_relation_from_mapping(raw: Mapping[str, Any]) -> ProgramRelation:
    return ProgramRelation(
        spec_id=raw["spec"],
        order=raw["order"],
        state=raw["state"],
        reason=raw["reason"],
        decision_id=raw["decision"],
    )


def _program_follow_up_from_mapping(raw: Mapping[str, Any]) -> ProgramFollowUp:
    return ProgramFollowUp(
        spec_id=raw["spec"],
        order=raw["order"],
        state=raw["state"],
        reason=raw["reason"],
        decision_id=raw["decision"],
        evidence_mode=raw["evidenceMode"],
    )


def _program_lineage_from_mapping(raw: Mapping[str, Any]) -> ProgramLineage:
    return ProgramLineage(
        prd_id=raw["prd"],
        ard_id=raw["ard"],
        tranches=tuple(
            _program_relation_from_mapping(item) for item in raw["tranches"]
        ),
        follow_ups=tuple(
            _program_follow_up_from_mapping(item) for item in raw["followUps"]
        ),
    )


def _program_structure_diagnostics(
    raw_programs: Sequence[Mapping[str, Any]],
) -> tuple[Diagnostic, ...]:
    diagnostics: list[Diagnostic] = []
    prd_ids = [program["prd"] for program in raw_programs]
    ard_ids = [program["ard"] for program in raw_programs]
    if len(prd_ids) != len(set(prd_ids)) or len(ard_ids) != len(set(ard_ids)):
        diagnostics.append(
            _diagnostic(
                "REGISTRY_PROGRAM_DUPLICATE",
                expected="unique PRD and ARD program owners",
                actual="a PRD or ARD is declared by multiple programs",
            )
        )
    if prd_ids != sorted(prd_ids, key=int):
        diagnostics.append(
            _diagnostic(
                "REGISTRY_PROGRAM_RELATION_ORDER",
                expected="programs sorted by numeric PRD identifier",
                actual=repr(prd_ids),
            )
        )

    global_members: set[str] = set()
    for program in raw_programs:
        tranches = program["tranches"]
        follow_ups = program["followUps"]
        tranche_ids = [item["spec"] for item in tranches]
        follow_up_ids = [item["spec"] for item in follow_ups]
        if len(tranche_ids) != len(set(tranche_ids)) or len(follow_up_ids) != len(
            set(follow_up_ids)
        ):
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_PROGRAM_MEMBER_DUPLICATE",
                    expected="unique Spec members within each relation collection",
                    actual=f"PRD-{program['prd']} contains a duplicate member",
                )
            )
        overlap = set(tranche_ids) & set(follow_up_ids)
        if overlap:
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_PROGRAM_MEMBER_OVERLAP",
                    expected="disjoint original tranche and follow-up sets",
                    actual=f"PRD-{program['prd']} overlap {sorted(overlap)!r}",
                )
            )
        program_members = set(tranche_ids) | set(follow_up_ids)
        repeated_members = global_members & program_members
        if repeated_members:
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_PROGRAM_MEMBER_DUPLICATE",
                    expected="each Spec belongs to at most one program",
                    actual=f"cross-program members {sorted(repeated_members)!r}",
                )
            )
        global_members.update(program_members)

        for relation_name, relations in (
            ("tranches", tranches),
            ("followUps", follow_ups),
        ):
            orders = [item["order"] for item in relations]
            if orders != list(range(1, len(relations) + 1)):
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_PROGRAM_RELATION_ORDER",
                        expected=f"contiguous one-based {relation_name} order",
                        actual=f"PRD-{program['prd']} {orders!r}",
                    )
                )

        for follow_up in follow_ups:
            historical_exception = (
                program["prd"] == "005"
                and follow_up["spec"] == "033"
                and follow_up["decision"] == "0017"
            )
            expected_mode = (
                "successor-record" if historical_exception else "reciprocal-body"
            )
            if follow_up["evidenceMode"] != expected_mode:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_PROGRAM_EVIDENCE_MODE",
                        expected=f"{expected_mode} for PRD-{program['prd']} Spec-{follow_up['spec']}",
                        actual=follow_up["evidenceMode"],
                    )
                )
    return tuple(diagnostics)


_PROGRAM_OWNER_CONTRACTS = {
    "prd": (
        PurePosixPath("docs/01.requirements"),
        re.compile(r"^docs/01\.requirements/(?P<id>[0-9]{3})-[^/]+\.md$"),
        "sdlc/prd",
    ),
    "ard": (
        PurePosixPath("docs/02.architecture/requirements"),
        re.compile(r"^docs/02\.architecture/requirements/(?P<id>[0-9]{4})-[^/]+\.md$"),
        "sdlc/ard",
    ),
    "adr": (
        PurePosixPath("docs/02.architecture/decisions"),
        re.compile(r"^docs/02\.architecture/decisions/(?P<id>[0-9]{4})-[^/]+\.md$"),
        "sdlc/adr",
    ),
    "spec": (
        PurePosixPath("docs/03.specs"),
        re.compile(r"^docs/03\.specs/(?P<id>[0-9]{3})-[^/]+/spec\.md$"),
        "sdlc/spec",
    ),
}


def _frontmatter_metadata(root: Path, path: PurePosixPath) -> Mapping[str, Any]:
    text = (root / path).read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    closing = text.find("\n---\n", 4)
    if closing < 0:
        raise ValueError("unterminated YAML frontmatter")
    metadata = yaml.load(text[4:closing], Loader=_UniqueKeySafeLoader)
    if not isinstance(metadata, dict) or not all(
        isinstance(key, str) for key in metadata
    ):
        raise ValueError("frontmatter must be a string-keyed mapping")
    return metadata


def _resolve_program_owner(
    root: Path,
    registry: Registry,
    owner_kind: Literal["prd", "ard", "adr", "spec"],
    numeric_id: str,
) -> tuple[PurePosixPath | None, tuple[Diagnostic, ...]]:
    directory, pattern, expected_profile = _PROGRAM_OWNER_CONTRACTS[owner_kind]
    entries = _parse_ls_files_stage_z(
        _run_git(
            root,
            ("ls-files", "--stage", "-z", "--", directory.as_posix()),
        )
    )
    candidates = [
        entry
        for entry in entries
        if (match := pattern.fullmatch(entry.path.as_posix())) is not None
        and match.group("id") == numeric_id
    ]
    valid_candidates: list[_GitEntry] = []
    for entry in candidates:
        try:
            file_mode = _lstat_named_path(root, entry.path)
        except ValueError:
            continue
        if (
            entry.stage == 0
            and entry.mode.startswith("100")
            and stat.S_ISREG(file_mode)
        ):
            valid_candidates.append(entry)
    if len(valid_candidates) != 1:
        return None, (
            _diagnostic(
                "REGISTRY_PROGRAM_PATH",
                expected=f"one tracked regular {expected_profile} owner for {numeric_id}",
                actual=f"found {len(valid_candidates)} owners",
            ),
        )

    path = valid_candidates[0].path
    try:
        actual_profile = classify_path(registry, path)
    except DocumentContractError:
        actual_profile = None
    if actual_profile is None or actual_profile.profile_id != expected_profile:
        return None, (
            _diagnostic(
                "REGISTRY_PROGRAM_PATH",
                path=path,
                profile=(actual_profile.profile_id if actual_profile else ""),
                expected=expected_profile,
                actual=(
                    actual_profile.profile_id if actual_profile else "unclassified"
                ),
            ),
        )
    return path, ()


def _program_repository_diagnostics(
    root: Path, registry: Registry
) -> tuple[Diagnostic, ...]:
    diagnostics: list[Diagnostic] = []
    owner_cache: dict[
        tuple[str, str], tuple[PurePosixPath | None, tuple[Diagnostic, ...]]
    ] = {}
    metadata_cache: dict[PurePosixPath, Mapping[str, Any] | ValueError] = {}
    decision_keys: dict[str, tuple[date, int] | None] = {}

    def owner(
        kind: Literal["prd", "ard", "adr", "spec"], numeric_id: str
    ) -> PurePosixPath | None:
        cache_key = (kind, numeric_id)
        if cache_key not in owner_cache:
            owner_cache[cache_key] = _resolve_program_owner(
                root, registry, kind, numeric_id
            )
            diagnostics.extend(owner_cache[cache_key][1])
        path, _ = owner_cache[cache_key]
        return path

    def metadata(path: PurePosixPath) -> Mapping[str, Any] | None:
        if path not in metadata_cache:
            try:
                metadata_cache[path] = _frontmatter_metadata(root, path)
            except (OSError, UnicodeError, yaml.YAMLError, ValueError) as exc:
                metadata_cache[path] = ValueError(str(exc))
        result = metadata_cache[path]
        return None if isinstance(result, ValueError) else result

    def decision_key(decision_id: str) -> tuple[date, int] | None:
        if decision_id in decision_keys:
            return decision_keys[decision_id]
        path = owner("adr", decision_id)
        if path is None:
            decision_keys[decision_id] = None
            return None
        decision_metadata = metadata(path)
        if decision_metadata is None or decision_metadata.get("status") != "accepted":
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_PROGRAM_DECISION",
                    path=path,
                    profile="sdlc/adr",
                    expected="an accepted governing ADR",
                    actual=(
                        "unreadable frontmatter"
                        if decision_metadata is None
                        else repr(decision_metadata.get("status"))
                    ),
                )
            )
            decision_keys[decision_id] = None
            return None
        raw_updated = decision_metadata.get("updated")
        try:
            if isinstance(raw_updated, datetime):
                raise ValueError("timestamps are not immutable admission dates")
            if isinstance(raw_updated, date):
                updated = raw_updated
            elif isinstance(raw_updated, str):
                updated = date.fromisoformat(raw_updated)
            else:
                raise TypeError("updated is not an ISO date scalar")
        except (TypeError, ValueError):
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_PROGRAM_DECISION",
                    path=path,
                    profile="sdlc/adr",
                    expected="accepted ADR updated as an ISO date",
                    actual=repr(raw_updated),
                )
            )
            decision_keys[decision_id] = None
            return None
        key = (updated, int(decision_id))
        decision_keys[decision_id] = key
        return key

    for program in registry.program_lineage:
        owner("prd", program.prd_id)
        owner("ard", program.ard_id)
        tranche_keys: list[tuple[date, int]] = []
        follow_up_keys: list[tuple[ProgramFollowUp, tuple[date, int] | None]] = []
        for relation in (*program.tranches, *program.follow_ups):
            spec_path = owner("spec", relation.spec_id)
            if spec_path is not None:
                spec_metadata = metadata(spec_path)
                actual_state = (
                    spec_metadata.get("status") if spec_metadata is not None else None
                )
                if actual_state != relation.state:
                    diagnostics.append(
                        _diagnostic(
                            "REGISTRY_PROGRAM_STATE",
                            path=spec_path,
                            profile="sdlc/spec",
                            expected=relation.state,
                            actual=repr(actual_state),
                        )
                    )
            key = decision_key(relation.decision_id)
            if isinstance(relation, ProgramFollowUp):
                follow_up_keys.append((relation, key))
            elif key is not None:
                tranche_keys.append(key)
        if tranche_keys:
            latest_tranche_key = max(tranche_keys)
            for follow_up, key in follow_up_keys:
                if key is not None and key <= latest_tranche_key:
                    diagnostics.append(
                        _diagnostic(
                            "REGISTRY_PROGRAM_CHRONOLOGY",
                            expected=(
                                "follow-up ADR key later than every original-tranche "
                                "ADR key"
                            ),
                            actual=(
                                f"PRD-{program.prd_id} Spec-{follow_up.spec_id} "
                                f"key={key!r} latest-tranche={latest_tranche_key!r}"
                            ),
                        )
                    )
        for (previous_follow_up, previous_key), (follow_up, key) in zip(
            follow_up_keys, follow_up_keys[1:]
        ):
            if previous_key is not None and key is not None and key <= previous_key:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_PROGRAM_CHRONOLOGY",
                        expected=(
                            "each declared follow-up ADR key later than the "
                            "immediately preceding follow-up ADR key"
                        ),
                        actual=(
                            f"PRD-{program.prd_id} Spec-{follow_up.spec_id} "
                            f"key={key!r} does not follow Spec-"
                            f"{previous_follow_up.spec_id} key={previous_key!r}"
                        ),
                    )
                )
    return tuple(diagnostics)


def _document_contract_projection(
    root: Path,
    raw_profiles: Sequence[Mapping[str, Any]],
    raw_contracts: Mapping[str, Any],
) -> tuple[
    tuple[Diagnostic, ...],
    dict[str, ValueContract],
    dict[str, RoleDecision],
    dict[str, AdmissionPolicy],
    dict[str, LifecycleContract],
    tuple[EvidencePredicate, ...],
]:
    """Validate closed v8 declarations and resolve one immutable contract per profile."""

    diagnostics: list[Diagnostic] = []
    profiles_by_id = {profile["id"]: profile for profile in raw_profiles}
    profile_ids = set(profiles_by_id)

    def assign_groups(
        groups: Sequence[Mapping[str, Any]], rule_id: str
    ) -> dict[str, Mapping[str, Any]]:
        assigned: dict[str, Mapping[str, Any]] = {}
        for group in groups:
            for profile_id in group["profileIds"]:
                if profile_id not in profile_ids:
                    diagnostics.append(
                        _diagnostic(
                            rule_id,
                            profile=profile_id,
                            expected="a declared profile ID",
                            actual="unknown profile assignment",
                        )
                    )
                if profile_id in assigned:
                    diagnostics.append(
                        _diagnostic(
                            rule_id,
                            profile=profile_id,
                            expected="exactly one direct contract assignment",
                            actual="duplicate contract assignment",
                        )
                    )
                else:
                    assigned[profile_id] = group
        return assigned

    value_groups = raw_contracts["valueContracts"]
    value_ids = [item["id"] for item in value_groups]
    if len(value_ids) != len(set(value_ids)):
        diagnostics.append(
            _diagnostic(
                "REGISTRY_VALUE_CONTRACT",
                expected="unique value contract IDs",
                actual="duplicate value contract ID",
            )
        )
    raw_values = assign_groups(value_groups, "REGISTRY_VALUE_CONTRACT")

    role_groups = raw_contracts["roleDecisions"]
    role_labels = [item["role"] for item in role_groups]
    if len(role_labels) != len(set(role_labels)):
        diagnostics.append(
            _diagnostic(
                "REGISTRY_ROLE_DECISION",
                expected="one distinct role label per canonical decision row",
                actual="role label copied across canonical decision rows",
            )
        )
    for role_group in role_groups:
        assigned_profiles = [
            profiles_by_id[profile_id]
            for profile_id in role_group["profileIds"]
            if profile_id in profiles_by_id
        ]
        if any(profile["mode"] == "template" for profile in assigned_profiles):
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_ROLE_DECISION",
                    expected=(
                        "templates inherit the role decision from their sole "
                        "canonical source profile"
                    ),
                    actual="template has a direct role-decision assignment",
                )
            )
    raw_roles = assign_groups(role_groups, "REGISTRY_ROLE_DECISION")
    for role in role_groups:
        if role["sourceProfileId"] is not None:
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_ROLE_DECISION",
                    expected="canonical decisions with null sourceProfileId; forms inherit",
                    actual=repr(role["sourceProfileId"]),
                )
            )

    admission_groups = raw_contracts["admissionPolicies"]
    admission_ids = [item["id"] for item in admission_groups]
    if len(admission_ids) != len(set(admission_ids)):
        diagnostics.append(
            _diagnostic(
                "REGISTRY_ADMISSION",
                expected="unique admission policy IDs",
                actual="duplicate admission policy ID",
            )
        )
    archive_admission_matches = [
        item for item in admission_groups if "content/archive" in item["profileIds"]
    ]
    if "content/archive" in profile_ids and len(archive_admission_matches) != 1:
        diagnostics.append(
            _diagnostic(
                "REGISTRY_ADMISSION",
                profile="content/archive",
                expected="exactly one admission policy membership",
                actual=f"{len(archive_admission_matches)} matching policies",
            )
        )
    raw_admissions = assign_groups(admission_groups, "REGISTRY_ADMISSION")

    lifecycle_groups = raw_contracts["lifecycleContracts"]
    lifecycle_ids = [item["id"] for item in lifecycle_groups]
    if len(lifecycle_ids) != len(set(lifecycle_ids)):
        diagnostics.append(
            _diagnostic(
                "REGISTRY_LIFECYCLE",
                expected="unique lifecycle contract IDs",
                actual="duplicate lifecycle contract ID",
            )
        )
    raw_lifecycles = assign_groups(lifecycle_groups, "REGISTRY_LIFECYCLE")

    def inherited_group(
        profile_id: str,
        assignments: Mapping[str, Mapping[str, Any]],
        rule_id: str,
    ) -> tuple[Mapping[str, Any] | None, str | None]:
        direct = assignments.get(profile_id)
        if direct is not None:
            return direct, None
        profile = profiles_by_id[profile_id]
        source_ids = profile["sourceProfileIds"]
        if profile["mode"] == "template" and len(source_ids) == 1:
            source_id = source_ids[0]
            source = assignments.get(source_id)
            if source is not None:
                return source, source_id
        diagnostics.append(
            _diagnostic(
                rule_id,
                profile=profile_id,
                expected="one direct contract or one canonical template source",
                actual="missing contract assignment",
            )
        )
        return None, None

    typed_values: dict[str, ValueContract] = {}
    typed_roles: dict[str, RoleDecision] = {}
    typed_admissions: dict[str, AdmissionPolicy] = {}
    typed_lifecycles: dict[str, LifecycleContract] = {}
    for profile_id, profile in profiles_by_id.items():
        value_raw, _ = inherited_group(
            profile_id, raw_values, "REGISTRY_VALUE_CONTRACT"
        )
        role_raw, role_source = inherited_group(
            profile_id, raw_roles, "REGISTRY_ROLE_DECISION"
        )
        admission_raw = raw_admissions.get(profile_id)
        lifecycle_raw = raw_lifecycles.get(profile_id)
        if admission_raw is None:
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_ADMISSION",
                    profile=profile_id,
                    expected="exactly one direct admission policy",
                    actual="missing admission assignment",
                )
            )
        if lifecycle_raw is None:
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_LIFECYCLE",
                    profile=profile_id,
                    expected="exactly one direct lifecycle contract",
                    actual="missing lifecycle assignment",
                )
            )
        if value_raw is not None:
            value = _value_contract(value_raw)
            typed_values[profile_id] = value
            key_names = [item.key for item in value.keys]
            expected_keys = profile["frontmatter"]["order"]
            if key_names != expected_keys:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_VALUE_CONTRACT",
                        profile=profile_id,
                        expected=f"value keys in frontmatter order {expected_keys!r}",
                        actual=repr(key_names),
                    )
                )
            if len(key_names) != len(set(key_names)):
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_VALUE_CONTRACT",
                        profile=profile_id,
                        expected="unique value-contract keys",
                        actual="duplicate key",
                    )
                )
            key_set = set(key_names)
            for item in value.keys:
                if item.constant is not None and item.enum is not None:
                    diagnostics.append(
                        _diagnostic(
                            "REGISTRY_VALUE_CONTRACT",
                            profile=profile_id,
                            expected="constant or enum, not both",
                            actual=item.key,
                        )
                    )
                if item.constant is not None:
                    if item.constant.source == "profile-id" and (
                        item.key != "type" or item.constant.value is not None
                    ):
                        diagnostics.append(
                            _diagnostic(
                                "REGISTRY_VALUE_CONTRACT",
                                profile=profile_id,
                                expected="type constant sourced from profile ID with null literal",
                                actual=item.key,
                            )
                        )
                if item.enum is not None:
                    if item.enum.source == "status-domain" and (
                        item.key != "status" or item.enum.values
                    ):
                        diagnostics.append(
                            _diagnostic(
                                "REGISTRY_VALUE_CONTRACT",
                                profile=profile_id,
                                expected="status enum sourced from statusDomain with no literals",
                                actual=item.key,
                            )
                        )
                    if item.enum.source == "literal" and not item.enum.values:
                        diagnostics.append(
                            _diagnostic(
                                "REGISTRY_VALUE_CONTRACT",
                                profile=profile_id,
                                expected="a non-empty literal enum",
                                actual=item.key,
                            )
                        )
                if item.pattern is not None:
                    try:
                        re.compile(item.pattern)
                    except re.error as exc:
                        diagnostics.append(
                            _diagnostic(
                                "REGISTRY_VALUE_CONTRACT",
                                profile=profile_id,
                                expected="a compilable value pattern",
                                actual=str(exc),
                            )
                        )
                if item.conditional is not None and (
                    item.conditional.key not in key_set
                    or item.conditional.key == item.key
                ):
                    diagnostics.append(
                        _diagnostic(
                            "REGISTRY_VALUE_CONTRACT",
                            profile=profile_id,
                            expected="a condition referencing another declared key",
                            actual=item.conditional.key,
                        )
                    )
        if role_raw is not None:
            role = _role_decision(role_raw, source_profile_id=role_source)
            typed_roles[profile_id] = role
            body_contract = profile["bodyContract"]
            headings = profile["headings"]["required"]
            valid_role = (
                (
                    role.body_requirement == "body-contract"
                    and body_contract is not None
                    and (
                        body_contract["section"] not in headings
                        or role.relationship_section == body_contract["section"]
                    )
                )
                or (
                    role.body_requirement == "heading-set"
                    and body_contract is None
                    and role.relationship_section in headings
                )
                or (
                    role.body_requirement == "none"
                    and body_contract is None
                    and role.relationship_section is None
                )
            )
            if not valid_role:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_ROLE_DECISION",
                        profile=profile_id,
                        expected="relationshipSection and bodyRequirement aligned to the selected profile",
                        actual=(
                            f"section={role.relationship_section!r} "
                            f"body={role.body_requirement!r}"
                        ),
                    )
                )
        if admission_raw is not None:
            admission = _admission_policy(admission_raw)
            typed_admissions[profile_id] = admission
            invalid_create_states = set(admission.create.states) - set(
                profile["statusDomain"]
            )
            if invalid_create_states:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_ADMISSION",
                        profile=profile_id,
                        expected="create states within statusDomain",
                        actual=repr(sorted(invalid_create_states)),
                    )
                )
            if admission.create.mode == "states" and admission.create.states != (
                "draft",
            ):
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_ADMISSION",
                        profile=profile_id,
                        expected="draft-only authored creation",
                        actual=repr(admission.create.states),
                    )
                )
            if admission.create.mode == "snapshot-only" and (admission.create.states):
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_ADMISSION",
                        profile=profile_id,
                        expected="no admitted creation states",
                        actual=repr(admission.create.states),
                    )
                )
            admission_profiles = set(admission.profile_ids)
            admission_shape_valid = (
                (
                    admission.create.mode == "states"
                    and profile["mode"] == "authored"
                    and profile_id not in {"sdlc/plan", "sdlc/task", "content/archive"}
                    and admission.create.evidence_predicate_id is None
                    and not admission.baseline_paths
                )
                or (
                    admission.create.mode == "paired"
                    and admission_profiles == {"sdlc/plan", "sdlc/task"}
                    and admission.create.states == ("draft", "active")
                    and admission.create.evidence_predicate_id is None
                    and not admission.baseline_paths
                )
                or (
                    admission.create.mode == "archive-envelope"
                    and admission_profiles == {"content/archive"}
                    and profile_id == "content/archive"
                    and admission.create.states == ("archived",)
                    and admission.create.evidence_predicate_id
                    == "archive-source-removal"
                    and not admission.baseline_paths
                )
                or (
                    admission.create.mode == "snapshot-only"
                    and profile["mode"] != "authored"
                    and admission.create.evidence_predicate_id is None
                    and not admission.baseline_paths
                )
            )
            if not admission_shape_valid:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_ADMISSION",
                        profile=profile_id,
                        expected="the closed family-specific creation and baseline shape",
                        actual=admission.create.mode,
                    )
                )
        if lifecycle_raw is not None:
            lifecycle = _lifecycle_contract(lifecycle_raw)
            typed_lifecycles[profile_id] = lifecycle
            status_domain = set(profile["statusDomain"])
            if not set(lifecycle.terminal_states).issubset(status_domain):
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_LIFECYCLE",
                        profile=profile_id,
                        expected="terminal states within statusDomain",
                        actual=repr(lifecycle.terminal_states),
                    )
                )
            seen_edges: set[tuple[str, str]] = set()
            for edge in lifecycle.edges:
                key = (edge.from_state, edge.to_state)
                if key in seen_edges:
                    diagnostics.append(
                        _diagnostic(
                            "REGISTRY_LIFECYCLE",
                            profile=profile_id,
                            expected="unique from/to lifecycle edges",
                            actual=repr(key),
                        )
                    )
                seen_edges.add(key)
                if (
                    edge.from_state not in status_domain
                    or edge.to_state not in status_domain
                    or edge.from_state == edge.to_state
                ):
                    diagnostics.append(
                        _diagnostic(
                            "REGISTRY_LIFECYCLE",
                            profile=profile_id,
                            expected="distinct edge states within statusDomain",
                            actual=repr(key),
                        )
                    )
                if "archived" in key:
                    diagnostics.append(
                        _diagnostic(
                            "REGISTRY_LIFECYCLE",
                            profile=profile_id,
                            expected="no archive edge before Spec 036",
                            actual=repr(key),
                        )
                    )
                if edge.from_state in lifecycle.terminal_states:
                    diagnostics.append(
                        _diagnostic(
                            "REGISTRY_LIFECYCLE",
                            profile=profile_id,
                            expected="no outgoing edge from a terminal state",
                            actual=repr(key),
                        )
                    )
            if lifecycle.edges:
                from_states = {edge.from_state for edge in lifecycle.edges}
                sink_states = {
                    edge.to_state
                    for edge in lifecycle.edges
                    if edge.to_state not in from_states
                }
                if set(lifecycle.terminal_states) != sink_states:
                    diagnostics.append(
                        _diagnostic(
                            "REGISTRY_LIFECYCLE",
                            profile=profile_id,
                            expected=f"terminal sink states {sorted(sink_states)!r}",
                            actual=repr(lifecycle.terminal_states),
                        )
                    )
            if (
                "archived" in lifecycle.terminal_states
                and profile_id != "content/archive"
            ):
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_LIFECYCLE",
                        profile=profile_id,
                        expected="archived terminal only for immutable archive records",
                        actual=repr(lifecycle.terminal_states),
                    )
                )

    predicate_raw = raw_contracts["evidencePredicates"]
    predicate_ids = [item["id"] for item in predicate_raw]
    if len(predicate_ids) != len(set(predicate_ids)):
        diagnostics.append(
            _diagnostic(
                "REGISTRY_EVIDENCE_PREDICATE",
                expected="unique evidence predicate IDs",
                actual="duplicate predicate ID",
            )
        )
    typed_predicates = tuple(_evidence_predicate(item) for item in predicate_raw)
    expected_edges: dict[str, set[tuple[str, str, str]]] = {}
    for profile_id, lifecycle in typed_lifecycles.items():
        for edge in lifecycle.edges:
            expected_edges.setdefault(edge.predicate_id, set()).add(
                (profile_id, edge.from_state, edge.to_state)
            )
    actual_edges: dict[str, set[tuple[str, str, str]]] = {}
    for predicate in typed_predicates:
        expected_semantics = _EVIDENCE_PREDICATE_SEMANTICS.get(predicate.predicate_id)
        if expected_semantics != (predicate.same_diff, predicate.capabilities):
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_EVIDENCE_PREDICATE",
                    expected="the closed predicate sameDiff/capability tuple",
                    actual=predicate.predicate_id,
                )
            )
        raw_edge_count = len(predicate.profile_edges)
        predicate_edges = {
            (edge.profile_id, edge.from_state, edge.to_state)
            for edge in predicate.profile_edges
        }
        if len(predicate_edges) != raw_edge_count:
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_EVIDENCE_PREDICATE",
                    expected="unique production edge cases per predicate",
                    actual=predicate.predicate_id,
                )
            )
        actual_edges[predicate.predicate_id] = predicate_edges
        if predicate.maximum is not None and predicate.maximum < predicate.minimum:
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_EVIDENCE_PREDICATE",
                    expected="maximum cardinality greater than or equal to minimum",
                    actual=predicate.predicate_id,
                )
            )
        source_profiles = {
            edge.profile_id
            for edge in predicate.profile_edges
            if edge.profile_id in profile_ids
        }
        for edge in predicate.profile_edges:
            profile = profiles_by_id.get(edge.profile_id)
            if profile is None or not {edge.from_state, edge.to_state}.issubset(
                set(profile["statusDomain"]) if profile is not None else set()
            ):
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_EVIDENCE_PREDICATE",
                        profile=edge.profile_id,
                        expected="a known profile edge with declared states",
                        actual=f"{edge.from_state}->{edge.to_state}",
                    )
                )
        for item in predicate.evidence:
            if item.maximum is not None and item.maximum < item.minimum:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_EVIDENCE_PREDICATE",
                        expected="evidence maximum greater than or equal to minimum",
                        actual=predicate.predicate_id,
                    )
                )
            for evidence_profile_id in item.profile_ids:
                if evidence_profile_id == "$self":
                    domains = [
                        set(profiles_by_id[source]["statusDomain"])
                        for source in source_profiles
                    ]
                    if not domains or any(
                        not set(item.states).issubset(domain) for domain in domains
                    ):
                        diagnostics.append(
                            _diagnostic(
                                "REGISTRY_EVIDENCE_PREDICATE",
                                expected="$self states valid for every exact source edge",
                                actual=predicate.predicate_id,
                            )
                        )
                    continue
                evidence_profile = profiles_by_id.get(evidence_profile_id)
                if evidence_profile is None:
                    diagnostics.append(
                        _diagnostic(
                            "REGISTRY_EVIDENCE_PREDICATE",
                            profile=evidence_profile_id,
                            expected="a known evidence profile",
                            actual=predicate.predicate_id,
                        )
                    )
                elif not set(item.states).issubset(
                    set(evidence_profile["statusDomain"])
                ):
                    diagnostics.append(
                        _diagnostic(
                            "REGISTRY_EVIDENCE_PREDICATE",
                            profile=evidence_profile_id,
                            expected="evidence states within profile statusDomain",
                            actual=repr(item.states),
                        )
                    )
        if any(
            typed_roles.get(profile_id) is not None
            and typed_roles[profile_id].body_requirement != predicate.body_requirement
            for profile_id in source_profiles
        ):
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_EVIDENCE_PREDICATE",
                    expected="predicate body requirement aligned to every exact edge profile",
                    actual=predicate.predicate_id,
                )
            )

    all_predicate_ids = set(expected_edges) | set(actual_edges)
    for predicate_id in sorted(all_predicate_ids):
        if expected_edges.get(predicate_id, set()) != actual_edges.get(
            predicate_id, set()
        ):
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_EVIDENCE_PREDICATE",
                    expected=(
                        f"exact lifecycle edge set {sorted(expected_edges.get(predicate_id, set()))!r}"
                    ),
                    actual=repr(sorted(actual_edges.get(predicate_id, set()))),
                )
            )

    archive_admission = typed_admissions.get("content/archive")
    archive_predicates = tuple(
        predicate
        for predicate in typed_predicates
        if predicate.predicate_id == "archive-source-removal"
    )
    if archive_admission is not None and (
        archive_admission.create.mode != "archive-envelope"
        or archive_admission.create.states != ("archived",)
        or archive_admission.create.evidence_predicate_id != "archive-source-removal"
        or archive_admission.baseline_paths
    ):
        diagnostics.append(
            _diagnostic(
                "REGISTRY_ADMISSION",
                profile="content/archive",
                expected="archive-envelope creation in archived state without compatibility baselines",
                actual=archive_admission.create.mode,
            )
        )
    if "content/archive" not in profile_ids:
        pass
    elif len(archive_predicates) != 1:
        diagnostics.append(
            _diagnostic(
                "REGISTRY_EVIDENCE_PREDICATE",
                profile="content/archive",
                expected="one archive-source-removal creation predicate",
                actual=str(len(archive_predicates)),
            )
        )
    else:
        archive_predicate = archive_predicates[0]
        if (
            archive_predicate.profile_edges
            or archive_predicate.evidence
            or archive_predicate.relationship != "archive-source"
            or archive_predicate.minimum != 1
            or archive_predicate.maximum != 1
            or archive_predicate.body_requirement != "none"
        ):
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_EVIDENCE_PREDICATE",
                    profile="content/archive",
                    expected="the closed archive source-removal predicate shape",
                    actual=archive_predicate.predicate_id,
                )
            )

    return (
        tuple(diagnostics),
        typed_values,
        typed_roles,
        typed_admissions,
        typed_lifecycles,
        typed_predicates,
    )


def validate_registry(root: Path, raw_registry: Mapping[str, Any]) -> Registry:
    """Validate a decoded registry and return its immutable typed form."""

    root = root.absolute()
    schema = load_json_file(root / SCHEMA_PATH, diagnostic_path=SCHEMA_PATH)
    if not isinstance(schema, dict):
        _fail(
            "REGISTRY_SCHEMA",
            expected="a JSON Schema object",
            actual=type(schema).__name__,
        )

    schema_errors = sorted(
        Draft202012Validator(schema).iter_errors(raw_registry),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    if schema_errors:
        diagnostics = tuple(
            _diagnostic(
                _schema_rule_id(error),
                expected=error.message,
                actual="schema validation failed",
            )
            for error in schema_errors
        )
        raise DocumentContractError(diagnostics)

    diagnostics: list[Diagnostic] = []
    baseline = raw_registry["baseline"]
    if baseline["sha"] != BASELINE_SHA:
        diagnostics.append(
            _diagnostic(
                "REGISTRY_BASELINE_SHA",
                expected=BASELINE_SHA,
                actual=baseline["sha"],
            )
        )
    if baseline["count"] != BASELINE_COUNT:
        diagnostics.append(
            _diagnostic(
                "REGISTRY_BASELINE_COUNT",
                expected=str(BASELINE_COUNT),
                actual=str(baseline["count"]),
            )
        )

    raw_profiles = raw_registry["profiles"]
    profile_ids = [profile["id"] for profile in raw_profiles]
    duplicate_ids = sorted(
        {profile_id for profile_id in profile_ids if profile_ids.count(profile_id) > 1}
    )
    for profile_id in duplicate_ids:
        diagnostics.append(
            _diagnostic(
                "REGISTRY_PROFILE_ID",
                profile=profile_id,
                expected="a unique profile ID",
                actual="duplicate profile ID",
            )
        )

    raw_profiles_by_id = {profile["id"]: profile for profile in raw_profiles}
    for raw_profile in raw_profiles:
        profile_id = raw_profile["id"]
        body_contract = raw_profile["bodyContract"]
        if body_contract is not None:
            required_headings = raw_profile["headings"]["required"]
            if body_contract["section"] not in required_headings:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_BODY_SECTION",
                        profile=profile_id,
                        expected="bodyContract.section in headings.required",
                        actual=body_contract["section"],
                    )
                )

            invalid_statuses = sorted(
                set(body_contract["enforcedStatuses"])
                - set(raw_profile["statusDomain"])
            )
            if invalid_statuses:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_BODY_STATUS",
                        profile=profile_id,
                        expected="enforcedStatuses within statusDomain",
                        actual=repr(invalid_statuses),
                    )
                )

            required_columns = body_contract["requiredColumns"]
            identifier_columns = body_contract["identifierColumns"]
            identifier_names = [item["column"] for item in identifier_columns]
            if len(identifier_names) != len(set(identifier_names)) or any(
                column not in required_columns for column in identifier_names
            ):
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_BODY_IDENTIFIER_COLUMN",
                        profile=profile_id,
                        expected="unique identifier columns selected from requiredColumns",
                        actual=repr(identifier_names),
                    )
                )

            for direction in ("source", "target"):
                link_key = f"{direction}LinkColumn"
                allowed_key = f"allowed{direction.title()}ProfileIds"
                link_column = body_contract[link_key]
                allowed_ids = body_contract[allowed_key]
                rule_id = f"REGISTRY_BODY_{direction.upper()}_PROFILE"
                invalid_profiles = sorted(
                    profile_id_value
                    for profile_id_value in allowed_ids
                    if profile_id_value not in raw_profiles_by_id
                )
                link_contract_valid = (link_column is None and not allowed_ids) or (
                    link_column in required_columns and bool(allowed_ids)
                )
                if invalid_profiles or not link_contract_valid:
                    diagnostics.append(
                        _diagnostic(
                            rule_id,
                            profile=profile_id,
                            expected=(
                                f"{link_key} selected from requiredColumns with known "
                                f"{allowed_key}, or both unset"
                            ),
                            actual=(
                                f"column={link_column!r} unknown={invalid_profiles!r} "
                                f"allowed={allowed_ids!r}"
                            ),
                        )
                    )

            if body_contract["reciprocalEvidence"] and not (
                body_contract["sourceLinkColumn"] or body_contract["targetLinkColumn"]
            ):
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_BODY_RECIPROCAL",
                        profile=profile_id,
                        expected="at least one linked column for reciprocal evidence",
                        actual="no source or target link column",
                    )
                )

        for source_profile_id in raw_profile["sourceProfileIds"]:
            if source_profile_id not in raw_profiles_by_id:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_SOURCE_PROFILE",
                        profile=profile_id,
                        expected="a declared source profile ID",
                        actual=source_profile_id,
                    )
                )

        if raw_profile["mode"] == "template" and raw_profile["appendContract"] is None:
            source_ids = raw_profile["sourceProfileIds"]
            if len(source_ids) != 1 or source_ids[0] not in raw_profiles_by_id:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_BODY_SOURCE_DRIFT",
                        profile=profile_id,
                        expected="one declared source profile for a canonical form",
                        actual=repr(source_ids),
                    )
                )
            elif body_contract != raw_profiles_by_id[source_ids[0]]["bodyContract"]:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_BODY_SOURCE_DRIFT",
                        profile=profile_id,
                        expected=f"bodyContract equal to {source_ids[0]}",
                        actual="template bodyContract differs",
                    )
                )

        for raw_route in raw_profile["routes"]:
            if raw_route["kind"] == "exact":
                try:
                    _normalize_relative_path(raw_route["value"])
                except ValueError:
                    diagnostics.append(
                        _diagnostic(
                            "REGISTRY_ROUTE_PATH",
                            profile=profile_id,
                            expected="a normalized POSIX repository-relative path",
                            actual=raw_route["value"],
                        )
                    )
            else:
                value = raw_route["value"]
                if not (value.startswith("^") and value.endswith("$")):
                    diagnostics.append(
                        _diagnostic(
                            "REGISTRY_ROUTE_ANCHOR",
                            profile=profile_id,
                            expected="a regex beginning with ^ and ending with $",
                            actual=value,
                        )
                    )
                    continue
                try:
                    _compile_route(value)
                except re.error as exc:
                    diagnostics.append(
                        _diagnostic(
                            "REGISTRY_ROUTE_REGEX",
                            profile=profile_id,
                            expected="a compilable regular expression",
                            actual=str(exc),
                        )
                    )

        template = raw_profile["template"]
        if template is not None:
            try:
                template_path = _normalize_relative_path(template)
                _lstat_named_path(root, template_path)
            except ValueError as exc:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_TEMPLATE",
                        profile=profile_id,
                        expected="an existing normalized path under the repository root",
                        actual=str(exc),
                    )
                )

    raw_current_owners = raw_registry["governanceCurrentOwners"]
    raw_current_paths = raw_current_owners["paths"]
    normalized_current_paths: list[PurePosixPath] = []
    for raw_path in raw_current_paths:
        try:
            normalized_path = _normalize_relative_path(raw_path)
            normalized_current_paths.append(normalized_path)
            if normalized_path.as_posix() != raw_path:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_GOVERNANCE_CURRENT_OWNER_PATH",
                        expected="a canonical POSIX repository-relative path",
                        actual="declared path is not canonical",
                    )
                )
        except ValueError as exc:
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_GOVERNANCE_CURRENT_OWNER_PATH",
                    expected="a normalized POSIX repository-relative path",
                    actual=str(exc),
                )
            )

    normalized_values = [path.as_posix() for path in normalized_current_paths]
    if len(normalized_values) != len(set(normalized_values)):
        diagnostics.append(
            _diagnostic(
                "REGISTRY_GOVERNANCE_CURRENT_OWNER_DUPLICATE",
                expected="unique canonical repository-relative paths",
                actual="normalized paths contain a duplicate",
            )
        )
    if normalized_values != sorted(normalized_values):
        diagnostics.append(
            _diagnostic(
                "REGISTRY_GOVERNANCE_CURRENT_OWNER_ORDER",
                expected="unique paths in ascending repository-relative order",
                actual="paths are not sorted",
            )
        )

    raw_reference_packs = raw_registry["referenceCurrentPacks"]
    raw_packs = raw_reference_packs["packs"]
    raw_pack_ids = [pack["id"] for pack in raw_packs]
    normalized_pack_ids: list[str] = []
    normalized_pack_members: list[list[str]] = []
    derived_member_paths: list[str] = []
    for raw_pack in raw_packs:
        raw_id = raw_pack["id"]
        try:
            normalized_id = _normalize_relative_path(raw_id).as_posix()
            normalized_pack_ids.append(normalized_id)
            if normalized_id != raw_id or len(PurePosixPath(raw_id).parts) != 2:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_REFERENCE_CURRENT_PACK_PATH",
                        expected="a canonical collection/date-key pack ID",
                        actual="pack ID is not canonical",
                    )
                )
        except ValueError as exc:
            normalized_pack_ids.append(raw_id)
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_REFERENCE_CURRENT_PACK_PATH",
                    expected="a canonical collection/date-key pack ID",
                    actual=str(exc),
                )
            )

        members: list[str] = []
        for raw_member in raw_pack["members"]:
            try:
                normalized_member = _normalize_relative_path(raw_member).as_posix()
                members.append(normalized_member)
                if (
                    normalized_member != raw_member
                    or len(PurePosixPath(raw_member).parts) != 1
                    or raw_member == "README.md"
                    or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*\.md", raw_member)
                    is None
                ):
                    diagnostics.append(
                        _diagnostic(
                            "REGISTRY_REFERENCE_CURRENT_PACK_PATH",
                            expected="a canonical direct-child Markdown basename",
                            actual="member path is not canonical",
                        )
                    )
            except ValueError as exc:
                members.append(raw_member)
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_REFERENCE_CURRENT_PACK_PATH",
                        expected="a canonical direct-child Markdown basename",
                        actual=str(exc),
                    )
                )
        normalized_pack_members.append(members)
        if len(members) != len(set(members)):
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_REFERENCE_CURRENT_PACK_DUPLICATE",
                    expected="unique canonical member basenames",
                    actual="normalized members contain a duplicate",
                )
            )
        if members != sorted(members):
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_REFERENCE_CURRENT_PACK_ORDER",
                    expected="member basenames in ascending order",
                    actual="members are not sorted",
                )
            )
        derived_member_paths.extend(
            f"docs/90.references/{normalized_pack_ids[-1]}/{member}"
            for member in members
        )

    if len(raw_pack_ids) != len(set(normalized_pack_ids)):
        diagnostics.append(
            _diagnostic(
                "REGISTRY_REFERENCE_CURRENT_PACK_ID",
                expected="one unique audits pack and one unique research pack",
                actual="pack IDs contain a duplicate",
            )
        )
    collections = [pack_id.split("/", 1)[0] for pack_id in normalized_pack_ids]
    if collections != ["audits", "research"]:
        diagnostics.append(
            _diagnostic(
                "REGISTRY_REFERENCE_CURRENT_PACK_ID",
                expected="exactly one audits pack followed by one research pack",
                actual="pack collections differ",
            )
        )
    if normalized_pack_ids != sorted(normalized_pack_ids):
        diagnostics.append(
            _diagnostic(
                "REGISTRY_REFERENCE_CURRENT_PACK_ORDER",
                expected="pack IDs in ascending order",
                actual="pack IDs are not sorted",
            )
        )
    if len(derived_member_paths) != len(set(derived_member_paths)):
        diagnostics.append(
            _diagnostic(
                "REGISTRY_REFERENCE_CURRENT_PACK_DUPLICATE",
                expected="unique derived member paths",
                actual="derived paths contain a duplicate",
            )
        )

    profiles_by_id = {profile["id"]: profile for profile in raw_profiles}
    reference_profile = profiles_by_id.get(raw_reference_packs["profileId"])
    status_domain = (
        set(reference_profile["statusDomain"]) if reference_profile else set()
    )
    for raw_pack in raw_packs:
        collection = raw_pack["id"].split("/", 1)[0]
        expected_states = ["done"] if collection == "audits" else ["active", "accepted"]
        if raw_pack["allowedStates"] != expected_states or not set(
            raw_pack["allowedStates"]
        ).issubset(status_domain):
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_REFERENCE_CURRENT_PACK_STATE",
                    expected=f"{collection} allowed states {expected_states!r} within content/reference",
                    actual="allowed-state contract differs",
                )
            )

    raw_programs = raw_registry["programLineage"]["programs"]
    diagnostics.extend(_program_structure_diagnostics(raw_programs))
    (
        contract_diagnostics,
        value_contracts_by_profile,
        roles_by_profile,
        admissions_by_profile,
        lifecycles_by_profile,
        evidence_predicates,
    ) = _document_contract_projection(
        root, raw_profiles, raw_registry["documentContracts"]
    )
    diagnostics.extend(contract_diagnostics)

    if diagnostics:
        raise DocumentContractError(diagnostics)

    registry = Registry(
        schema_version=raw_registry["schemaVersion"],
        baseline_sha=baseline["sha"],
        baseline_count=baseline["count"],
        profiles=tuple(
            _profile_from_mapping(
                profile,
                value_contract=value_contracts_by_profile[profile["id"]],
                role_decision=roles_by_profile[profile["id"]],
                admission=admissions_by_profile[profile["id"]],
                lifecycle=lifecycles_by_profile[profile["id"]],
            )
            for profile in raw_profiles
        ),
        governance_current_owners=GovernanceCurrentOwners(
            profile_id=raw_current_owners["profileId"],
            allowed_states=tuple(raw_current_owners["allowedStates"]),
            paths=tuple(normalized_current_paths),
        ),
        reference_current_packs=ReferenceCurrentPacks(
            profile_id=raw_reference_packs["profileId"],
            packs=tuple(_reference_pack_from_mapping(pack) for pack in raw_packs),
        ),
        program_lineage=tuple(
            _program_lineage_from_mapping(program) for program in raw_programs
        ),
        evidence_predicates=evidence_predicates,
    )

    current_owner_diagnostics: list[Diagnostic] = []
    tracked_current_owner_entries: dict[PurePosixPath, list[_GitEntry]] = {}
    for entry in _parse_ls_files_stage_z(
        _run_git(
            root,
            (
                "ls-files",
                "--stage",
                "-z",
                "--",
                *(path.as_posix() for path in registry.governance_current_owners.paths),
            ),
        )
    ):
        tracked_current_owner_entries.setdefault(entry.path, []).append(entry)
    for path in registry.governance_current_owners.paths:
        try:
            mode = _lstat_named_path(root, path)
        except ValueError:
            current_owner_diagnostics.append(
                _diagnostic(
                    "REGISTRY_GOVERNANCE_CURRENT_OWNER_MISSING",
                    path=path,
                    profile=registry.governance_current_owners.profile_id,
                    expected="an existing regular repository file",
                    actual="declared path is missing",
                )
            )
            continue
        if not stat.S_ISREG(mode):
            current_owner_diagnostics.append(
                _diagnostic(
                    "REGISTRY_GOVERNANCE_CURRENT_OWNER_MISSING",
                    path=path,
                    profile=registry.governance_current_owners.profile_id,
                    expected="an existing regular repository file",
                    actual="declared path is not a regular file",
                )
            )
            continue
        tracked_entries = tracked_current_owner_entries.get(path, [])
        if (
            len(tracked_entries) != 1
            or tracked_entries[0].path != path
            or tracked_entries[0].stage != 0
            or not tracked_entries[0].mode.startswith("100")
        ):
            current_owner_diagnostics.append(
                _diagnostic(
                    "REGISTRY_GOVERNANCE_CURRENT_OWNER_MISSING",
                    path=path,
                    profile=registry.governance_current_owners.profile_id,
                    expected="one tracked regular repository Markdown file",
                    actual="declared path is not a tracked regular file",
                )
            )
            continue
        try:
            actual_profile = classify_path(registry, path)
        except DocumentContractError as exc:
            current_owner_diagnostics.extend(exc.diagnostics)
            continue
        if (
            actual_profile.profile_id != registry.governance_current_owners.profile_id
            or actual_profile.mode != "authored"
        ):
            current_owner_diagnostics.append(
                _diagnostic(
                    "REGISTRY_GOVERNANCE_CURRENT_OWNER_PROFILE",
                    path=path,
                    profile=actual_profile.profile_id,
                    expected=(
                        "authored " + registry.governance_current_owners.profile_id
                    ),
                    actual=f"{actual_profile.mode} {actual_profile.profile_id}",
                )
            )
    if current_owner_diagnostics:
        raise DocumentContractError(current_owner_diagnostics)

    reference_diagnostics: list[Diagnostic] = []
    expected_paths: dict[PurePosixPath, tuple[str, str]] = {}
    for pack in registry.reference_current_packs.packs:
        expected_paths[pack.collection_readme] = (
            "readme/collection-index",
            "frontmatter-free",
        )
        expected_paths[pack.pack_readme] = (
            "readme/snapshot-pack",
            "frontmatter-free",
        )
        for member_path in pack.member_paths:
            expected_paths[member_path] = (
                registry.reference_current_packs.profile_id,
                "authored",
            )
    tracked_reference_entries: dict[PurePosixPath, list[_GitEntry]] = {}
    for entry in _parse_ls_files_stage_z(
        _run_git(
            root,
            (
                "ls-files",
                "--stage",
                "-z",
                "--",
                *(path.as_posix() for path in sorted(expected_paths, key=str)),
            ),
        )
    ):
        tracked_reference_entries.setdefault(entry.path, []).append(entry)
    for path, (expected_profile, expected_mode) in expected_paths.items():
        try:
            file_mode = _lstat_named_path(root, path)
        except ValueError:
            file_mode = 0
        entries = tracked_reference_entries.get(path, [])
        if (
            not stat.S_ISREG(file_mode)
            or len(entries) != 1
            or entries[0].stage != 0
            or not entries[0].mode.startswith("100")
        ):
            reference_diagnostics.append(
                _diagnostic(
                    "REGISTRY_REFERENCE_CURRENT_PACK_MISSING",
                    path=path,
                    profile=expected_profile,
                    expected="one tracked stage-0 regular file",
                    actual="declared path is missing, untracked, or non-regular",
                )
            )
            continue
        try:
            actual_profile = classify_path(registry, path)
        except DocumentContractError as exc:
            reference_diagnostics.extend(exc.diagnostics)
            continue
        if (
            actual_profile.profile_id != expected_profile
            or actual_profile.mode != expected_mode
        ):
            reference_diagnostics.append(
                _diagnostic(
                    "REGISTRY_REFERENCE_CURRENT_PACK_PROFILE",
                    path=path,
                    profile=actual_profile.profile_id,
                    expected=f"{expected_mode} {expected_profile}",
                    actual=f"{actual_profile.mode} {actual_profile.profile_id}",
                )
            )
    if reference_diagnostics:
        raise DocumentContractError(reference_diagnostics)
    program_diagnostics = _program_repository_diagnostics(root, registry)
    if program_diagnostics:
        raise DocumentContractError(program_diagnostics)
    return registry


def load_registry(root: Path) -> Registry:
    root = root.absolute()
    raw_registry = load_json_file(root / REGISTRY_PATH)
    if not isinstance(raw_registry, dict):
        _fail(
            "REGISTRY_SCHEMA",
            expected="a JSON object",
            actual=type(raw_registry).__name__,
        )
    if (
        raw_registry.get("schemaVersion") != 8
        or raw_registry.get("$id")
        != "https://hy-home.k8s/schemas/document-profiles-8.schema.json"
    ):
        _fail(
            "REGISTRY_SCHEMA",
            expected="closed production registry schema v8",
            actual=(
                f"schemaVersion={raw_registry.get('schemaVersion')!r} "
                f"$id={raw_registry.get('$id')!r}"
            ),
        )
    return validate_registry(root, raw_registry)


def _route_matches(route: Route, path: PurePosixPath) -> bool:
    value = path.as_posix()
    if route.kind == "exact":
        return value == route.value
    return _compile_route(route.value).fullmatch(value) is not None


def classify_path(registry: Registry, path: PurePosixPath) -> DocumentProfile:
    try:
        normalized = _normalize_relative_path(path)
    except ValueError as exc:
        raise DocumentContractError(
            (
                _diagnostic(
                    "REGISTRY_ROUTE_PATH",
                    path=PurePosixPath(str(path)),
                    expected="a normalized POSIX repository-relative path",
                    actual=str(exc),
                ),
            )
        ) from exc

    matches = tuple(
        (profile, route)
        for profile in registry.profiles
        for route in profile.routes
        if _route_matches(route, normalized)
    )
    if not matches:
        raise DocumentContractError(
            (
                _diagnostic(
                    "REGISTRY_ROUTE_UNCOVERED",
                    path=normalized,
                    expected="exactly one matching profile",
                    actual="no matching profile",
                ),
            )
        )
    if len(matches) != 1:
        raise DocumentContractError(
            (
                _diagnostic(
                    "REGISTRY_ROUTE_AMBIGUOUS",
                    path=normalized,
                    expected="exactly one matching profile",
                    actual=", ".join(
                        f"{profile.profile_id}:{route.kind}:{route.value}"
                        for profile, route in matches
                    ),
                ),
            )
        )
    return matches[0][0]


def classify_paths(
    registry: Registry, paths: Sequence[PurePosixPath]
) -> tuple[Diagnostic, ...]:
    diagnostics: list[Diagnostic] = []
    for path in sorted(paths, key=lambda item: item.as_posix()):
        try:
            classify_path(registry, path)
        except DocumentContractError as exc:
            diagnostics.extend(exc.diagnostics)
    return tuple(diagnostics)
