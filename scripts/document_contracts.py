"""Typed document-profile registry loading and deterministic path routing."""

from __future__ import annotations

import copy
import re
import stat
import subprocess
from dataclasses import dataclass, replace
from functools import lru_cache
from pathlib import Path, PurePosixPath
from typing import Any, Literal, Mapping, NoReturn, Sequence

import yaml

from document_authority import (
    AuthorityError,
    REGISTRY_MAX_BYTES,
    load_bounded_json,
    read_bounded_utf8,
    run_bounded_process,
    validate_registry_authority,
)
from json_schema_validation import SchemaEvaluationError, schema_errors


GIT_TIMEOUT_SECONDS = 10
DOCUMENT_TEXT_MAX_BYTES = 16 * 1024 * 1024
_LS_TREE_MODE_TYPES = {
    b"040000": b"tree",
    b"100644": b"blob",
    b"100755": b"blob",
    b"120000": b"blob",
    b"160000": b"commit",
}
_LS_FILES_MODES = {b"100644", b"100755", b"120000", b"160000"}
ROOT_FILES = ("AGENTS.md", "CLAUDE.md", "README.md")
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
REGISTRY_PATH = PurePosixPath("docs/99.templates/registry.json")
PROFILE_SCHEMA_PATH = PurePosixPath(
    "docs/99.templates/contracts/document-profile.schema.json"
)
# Compatibility name for direct callers of ``validate_registry``.  The only
# schema it may load is the root-registry profile schema.
SCHEMA_PATH = PROFILE_SCHEMA_PATH
_UNSET = object()


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
class LifecycleDomain:
    family: str
    profile_ids: tuple[str, ...]
    states: tuple[tuple[str, Literal["mutable", "current", "terminal"]], ...]
    transitions: frozenset[tuple[str, str]]

    def validation_class(
        self, state: str
    ) -> Literal["mutable", "current", "terminal"] | None:
        return dict(self.states).get(state)

    def allows(self, from_state: str, to_state: str) -> bool:
        return (from_state, to_state) in self.transitions

    @property
    def requires_reciprocal_supersession(self) -> bool:
        return any(target == "superseded" for _, target in self.transitions)


@dataclass(frozen=True)
class DocumentProfile:
    profile_id: str
    profile_class: Literal[
        "sdlc",
        "operation",
        "reference",
        "archive",
        "governance",
        "readme",
        "exception",
    ]
    path_pattern: str
    routes: tuple[Route, ...]
    artifact_id_pattern: str | None
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
    body_contract: BodyContract | None
    lifecycle_domain: LifecycleDomain | None


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
    ad_id: str
    tranches: tuple[ProgramRelation, ...]
    follow_ups: tuple[ProgramFollowUp, ...]


@dataclass(frozen=True)
class StandaloneExecution:
    spec_id: str
    plan_path: PurePosixPath
    task_path: PurePosixPath
    state: str
    reason: str
    decision_id: str
    approval_mode: Literal["spec-body-record"]


@dataclass(frozen=True)
class Registry:
    schema_version: int
    profiles: tuple[DocumentProfile, ...]
    program_lineage: tuple[ProgramLineage, ...]
    standalone_executions: tuple[StandaloneExecution, ...]
    lifecycle_domains: tuple[LifecycleDomain, ...]


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
    try:
        return load_bounded_json(path, max_bytes=REGISTRY_MAX_BYTES)
    except AuthorityError as exc:
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


def _run_git(
    root: Path,
    arguments: Sequence[str],
    *,
    timeout_seconds: float = GIT_TIMEOUT_SECONDS,
    max_stdout_bytes: int = DOCUMENT_TEXT_MAX_BYTES,
) -> bytes:
    completed = run_bounded_process(
        ["git", *arguments],
        cwd=root,
        check=True,
        timeout_seconds=timeout_seconds,
        max_stdout_bytes=max_stdout_bytes,
    )
    return completed.stdout


def _within_target_scope(path: PurePosixPath) -> bool:
    if path.as_posix() == "RTK.md":
        return False
    if not path.parts:
        return False
    if path.parts[0] == ".worktrees":
        return False
    return path.as_posix() in ROOT_FILES or path.parts[0] in TARGET_ROOTS


def _is_target_markdown(path: PurePosixPath) -> bool:
    return path.suffix == ".md" and _within_target_scope(path)


def _sorted_paths(paths: set[PurePosixPath]) -> tuple[PurePosixPath, ...]:
    return tuple(sorted(paths, key=lambda item: item.as_posix()))


def _is_ignored(
    root: Path,
    path: PurePosixPath,
    *,
    timeout_seconds: float = GIT_TIMEOUT_SECONDS,
) -> bool:
    completed = run_bounded_process(
        ["git", "check-ignore", "--quiet", "--", path.as_posix()],
        cwd=root,
        check=False,
        timeout_seconds=timeout_seconds,
        max_stdout_bytes=0,
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
    mode: int | None = None
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
    if mode is None:
        raise ValueError("included path must not be empty")
    return mode


def read_repository_text(root: Path, path: PurePosixPath) -> str:
    """Read one normalized regular file without following path symlinks."""

    normalized = _normalize_relative_path(path)
    mode = _lstat_named_path(root.absolute(), normalized)
    if not stat.S_ISREG(mode):
        raise ValueError(f"repository path is not a regular file: {normalized}")
    try:
        return read_bounded_utf8(
            root.absolute() / normalized,
            max_bytes=DOCUMENT_TEXT_MAX_BYTES,
        )
    except AuthorityError as exc:
        raise ValueError(str(exc)) from exc


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
    current_entries = _parse_ls_files_stage_z(
        _run_git(root, ("ls-files", "--stage", "-z"))
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
        baseline_paths=(),
        current_paths=_sorted_paths(current_paths),
        new_paths=_sorted_paths(current_paths),
        baseline_symlink_paths=(),
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
    if path and path[0] == "programLineage":
        messages = " ".join(item.message for item in nested_errors)
        if "evidenceMode" in path or "evidenceMode" in messages:
            return "REGISTRY_PROGRAM_EVIDENCE_MODE"
        if "decision" in path or "decision" in messages:
            return "REGISTRY_PROGRAM_DECISION"
        if "state" in path or "state" in messages:
            return "REGISTRY_PROGRAM_STATE"
        return "REGISTRY_SCHEMA"
    if path and path[0] == "standaloneExecutions":
        messages = " ".join(item.message for item in nested_errors)
        if "approvalMode" in path or "approvalMode" in messages:
            return "REGISTRY_STANDALONE_APPROVAL_MODE"
        if "decision" in path or "decision" in messages:
            return "REGISTRY_STANDALONE_DECISION"
        if "state" in path or "state" in messages:
            return "REGISTRY_STANDALONE_STATE"
        if "plan" in path or "task" in path or "plan" in messages or "task" in messages:
            return "REGISTRY_STANDALONE_PATH"
        return "REGISTRY_SCHEMA"
    if len(path) >= 4 and path[-1] == "kind" and "routes" in path:
        return "REGISTRY_ROUTE_KIND"
    return "REGISTRY_SCHEMA"


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


def _profile_from_mapping(
    raw: Mapping[str, Any],
    *,
    path_pattern: str,
    lifecycle_domain: LifecycleDomain | None,
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
        path_pattern=path_pattern,
        routes=routes,
        artifact_id_pattern=raw["artifactIdPattern"],
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
        body_contract=_body_contract(raw["bodyContract"]),
        lifecycle_domain=lifecycle_domain,
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
        ad_id=raw["ad"],
        tranches=tuple(
            _program_relation_from_mapping(item) for item in raw["tranches"]
        ),
        follow_ups=tuple(
            _program_follow_up_from_mapping(item) for item in raw["followUps"]
        ),
    )


def _standalone_execution_from_mapping(
    raw: Mapping[str, Any],
) -> StandaloneExecution:
    return StandaloneExecution(
        spec_id=raw["spec"],
        plan_path=_normalize_relative_path(raw["plan"]),
        task_path=_normalize_relative_path(raw["task"]),
        state=raw["state"],
        reason=raw["reason"],
        decision_id=raw["decision"],
        approval_mode=raw["approvalMode"],
    )


def _program_structure_diagnostics(
    raw_programs: Sequence[Mapping[str, Any]],
) -> tuple[Diagnostic, ...]:
    diagnostics: list[Diagnostic] = []
    prd_ids = [program["prd"] for program in raw_programs]
    ad_ids = [program["ad"] for program in raw_programs]
    if len(prd_ids) != len(set(prd_ids)) or len(ad_ids) != len(set(ad_ids)):
        diagnostics.append(
            _diagnostic(
                "REGISTRY_PROGRAM_DUPLICATE",
                expected="unique PRD and AD program owners",
                actual="a PRD or AD is declared by multiple programs",
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
    return tuple(diagnostics)


def _standalone_structure_diagnostics(
    raw_standalones: Sequence[Mapping[str, Any]],
    raw_programs: Sequence[Mapping[str, Any]],
) -> tuple[Diagnostic, ...]:
    diagnostics: list[Diagnostic] = []
    spec_ids = [item["spec"] for item in raw_standalones]
    plan_paths = [item["plan"] for item in raw_standalones]
    task_paths = [item["task"] for item in raw_standalones]
    if spec_ids != sorted(spec_ids, key=int):
        diagnostics.append(
            _diagnostic(
                "REGISTRY_STANDALONE_ORDER",
                expected="standalone relations sorted by numeric Spec identifier",
                actual=repr(spec_ids),
            )
        )
    if any(
        len(values) != len(set(values)) for values in (spec_ids, plan_paths, task_paths)
    ):
        diagnostics.append(
            _diagnostic(
                "REGISTRY_STANDALONE_DUPLICATE",
                expected="unique standalone Spec, Plan, and Task identities",
                actual="a standalone identity is declared more than once",
            )
        )
    for item in raw_standalones:
        for key in ("plan", "task"):
            try:
                normalized = _normalize_relative_path(item[key]).as_posix()
                if normalized != item[key]:
                    raise ValueError("path is not canonical")
            except ValueError as exc:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_STANDALONE_PATH",
                        expected="a normalized POSIX repository-relative path",
                        actual=f"{key}={item[key]!r}: {exc}",
                    )
                )
    program_specs = {
        relation["spec"]
        for program in raw_programs
        for section in ("tranches", "followUps")
        for relation in program[section]
    }
    overlap = program_specs & set(spec_ids)
    if overlap:
        diagnostics.append(
            _diagnostic(
                "REGISTRY_STANDALONE_OVERLAP",
                expected="standalone Specs disjoint from program relations",
                actual=repr(sorted(overlap)),
            )
        )
    return tuple(diagnostics)


def _terminal_semantic_diagnostics(
    root: Path,
    raw_registry: Mapping[str, Any],
    *,
    template_regular_paths: frozenset[PurePosixPath] | None = None,
) -> tuple[Diagnostic, ...]:
    """Validate relationships not expressible in the terminal JSON Schema."""

    diagnostics: list[Diagnostic] = []
    raw_profiles = raw_registry["profiles"]
    profiles_by_id = {profile["id"]: profile for profile in raw_profiles}
    for raw_profile in raw_profiles:
        profile_id = raw_profile["id"]
        for field, rule_id in (
            ("pathPattern", "REGISTRY_ROUTE_REGEX"),
            ("artifactIdPattern", "REGISTRY_ARTIFACT_ID_PATTERN"),
        ):
            pattern = raw_profile.get(field)
            if pattern is None:
                continue
            try:
                if not (pattern.startswith("^") and pattern.endswith("$")):
                    raise re.error("pattern is not anchored")
                _compile_route(pattern)
            except re.error as exc:
                diagnostics.append(
                    _diagnostic(
                        rule_id,
                        profile=profile_id,
                        expected="an anchored compilable regular expression",
                        actual=str(exc),
                    )
                )
        relationships = raw_profile["relationships"]
        for source_profile_id in relationships["sourceProfileIds"]:
            if source_profile_id not in profiles_by_id:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_SOURCE_PROFILE",
                        profile=profile_id,
                        expected="a declared source profile ID",
                        actual=source_profile_id,
                    )
                )

        lifecycle = raw_profile.get("lifecycle")
        body_contract = relationships["bodyContract"]
        if body_contract is not None:
            required_headings = raw_profile["requiredSections"]["required"]
            if body_contract["section"] not in required_headings:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_BODY_SECTION",
                        profile=profile_id,
                        expected="body section in required sections",
                        actual=body_contract["section"],
                    )
                )
            status_domain = (
                lifecycle["statusDomain"]
                if lifecycle and raw_profile["mode"] != "template"
                else body_contract["enforcedStatuses"]
            )
            invalid_statuses = sorted(
                set(body_contract["enforcedStatuses"]) - set(status_domain)
            )
            if invalid_statuses:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_BODY_STATUS",
                        profile=profile_id,
                        expected="enforced statuses within the profile status domain",
                        actual=repr(invalid_statuses),
                    )
                )
            required_columns = body_contract["requiredColumns"]
            identifier_names = [
                item["column"] for item in body_contract["identifierColumns"]
            ]
            if len(identifier_names) != len(set(identifier_names)) or any(
                column not in required_columns for column in identifier_names
            ):
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_BODY_IDENTIFIER_COLUMN",
                        profile=profile_id,
                        expected=(
                            "unique identifier columns selected from required columns"
                        ),
                        actual=repr(identifier_names),
                    )
                )
            for direction in ("source", "target"):
                link_key = f"{direction}LinkColumn"
                allowed_key = f"allowed{direction.title()}ProfileIds"
                link_column = body_contract[link_key]
                allowed_ids = body_contract[allowed_key]
                unknown = sorted(
                    value for value in allowed_ids if value not in profiles_by_id
                )
                valid_pair = (link_column is None and not allowed_ids) or (
                    link_column in required_columns and bool(allowed_ids)
                )
                if unknown or not valid_pair:
                    diagnostics.append(
                        _diagnostic(
                            f"REGISTRY_BODY_{direction.upper()}_PROFILE",
                            profile=profile_id,
                            expected=(
                                f"{link_key} selected from required columns with "
                                f"known {allowed_key}, or both unset"
                            ),
                            actual=(
                                f"column={link_column!r} unknown={unknown!r} "
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

        template = raw_profile["template"]
        if template is not None:
            try:
                template_path = _normalize_relative_path(template)
                if template_path.as_posix() != template:
                    raise ValueError("path is not canonical")
                regular = (
                    stat.S_ISREG(_lstat_named_path(root, template_path))
                    if template_regular_paths is None
                    else template_path in template_regular_paths
                )
                if not regular:
                    raise ValueError("template is not a regular file")
            except ValueError as exc:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_TEMPLATE",
                        profile=profile_id,
                        expected=(
                            "an existing normalized regular non-symlink file "
                            "under the repository root"
                        ),
                        actual=str(exc),
                    )
                )

    assigned_profiles: set[str] = set()
    domains_by_profile: dict[str, Mapping[str, Any]] = {}
    families: set[str] = set()
    for domain in raw_registry["programLineage"]["lifecycleDomains"]:
        family = domain["family"]
        if family in families:
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_LIFECYCLE_DOMAIN",
                    expected="one lifecycle domain per family",
                    actual=f"duplicate family {family}",
                )
            )
        families.add(family)
        if not domain["profileIds"]:
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_LIFECYCLE_DOMAIN",
                    expected="at least one lifecycle profile ID per family",
                    actual=f"empty lifecycle domain {family}",
                )
            )
        for profile_id in domain["profileIds"]:
            if profile_id not in profiles_by_id:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_LIFECYCLE_DOMAIN",
                        profile=profile_id,
                        expected="a declared lifecycle profile ID",
                        actual="unknown profile",
                    )
                )
            elif profile_id in assigned_profiles:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_LIFECYCLE_DOMAIN",
                        profile=profile_id,
                        expected="at most one lifecycle domain per profile",
                        actual="duplicate lifecycle domain assignment",
                    )
                )
            assigned_profiles.add(profile_id)
            domains_by_profile[profile_id] = domain

    for profile_id, profile in profiles_by_id.items():
        if profile["mode"] != "authored":
            continue
        lifecycle = profile["lifecycle"]
        domain = domains_by_profile.get(profile_id)
        if lifecycle is None or domain is None:
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_LIFECYCLE_DOMAIN",
                    profile=profile_id,
                    expected="one lifecycle domain for each authored profile",
                    actual="missing lifecycle domain assignment",
                )
            )
            continue
        status_domain = set(lifecycle["statusDomain"])
        classified_states = set(domain["states"])
        if status_domain != classified_states:
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_LIFECYCLE_DOMAIN",
                    profile=profile_id,
                    expected="profile statuses exactly match lifecycle state classes",
                    actual=(
                        f"profile={sorted(status_domain)!r} "
                        f"domain={sorted(classified_states)!r}"
                    ),
                )
            )

    raw_programs = raw_registry["programLineage"]["programs"]
    raw_standalones = raw_registry.get("standaloneExecutions", [])
    diagnostics.extend(_program_structure_diagnostics(raw_programs))
    diagnostics.extend(_standalone_structure_diagnostics(raw_standalones, raw_programs))
    return tuple(diagnostics)


def _typed_registry_from_mapping(raw: Mapping[str, Any]) -> Registry:
    domains = tuple(
        LifecycleDomain(
            family=item["family"],
            profile_ids=tuple(item["profileIds"]),
            states=tuple(item["states"].items()),
            transitions=frozenset(tuple(edge) for edge in item["transitions"]),
        )
        for item in raw["programLineage"]["lifecycleDomains"]
    )
    domains_by_profile = {
        profile_id: domain for domain in domains for profile_id in domain.profile_ids
    }

    def typed_profile(profile: Mapping[str, Any]) -> DocumentProfile:
        internal = _internal_profile_form(profile)
        return _profile_from_mapping(
            internal,
            path_pattern=profile["pathPattern"],
            lifecycle_domain=domains_by_profile.get(profile["id"]),
        )

    profiles = tuple(typed_profile(profile) for profile in raw["profiles"])
    profiles_by_id = {profile.profile_id: profile for profile in profiles}
    profiles = tuple(
        replace(
            profile,
            status_domain=profiles_by_id[profile.source_profile_ids[0]].status_domain,
        )
        if profile.mode == "template" and profile.source_profile_ids
        else profile
        for profile in profiles
    )
    return Registry(
        schema_version=raw["schemaVersion"],
        profiles=profiles,
        program_lineage=tuple(
            _program_lineage_from_mapping(item)
            for item in raw["programLineage"]["programs"]
        ),
        standalone_executions=tuple(
            _standalone_execution_from_mapping(item)
            for item in raw.get("standaloneExecutions", [])
        ),
        lifecycle_domains=domains,
    )


def validate_registry(
    root: Path,
    raw_registry: Mapping[str, Any],
    *,
    template_regular_paths: frozenset[PurePosixPath] | None = None,
    trusted_registry: Registry | None = None,
    raw_schema: object = _UNSET,
) -> Registry:
    """Validate a payload with filesystem or caller-proved Git template regularity.

    Supplied paths replace only template existence/type lookup, never schema,
    path normalization, profile, relationship, or lifecycle validation.
    A supplied trusted registry binds every profile's literal executable patterns
    before proposed pattern compilation, projection, or classification.
    """

    root = root.absolute()
    if raw_schema is not _UNSET and (
        not isinstance(template_regular_paths, frozenset)
        or any(not isinstance(path, PurePosixPath) for path in template_regular_paths)
    ):
        _fail(
            "REGISTRY_SCHEMA",
            expected="complete supplied schema and template regularity facts",
            actual="template facts are unavailable",
        )
    schema = (
        load_json_file(root / SCHEMA_PATH, diagnostic_path=SCHEMA_PATH)
        if raw_schema is _UNSET
        else raw_schema
    )
    if not isinstance(schema, dict):
        _fail(
            "REGISTRY_SCHEMA",
            expected="a JSON Schema object",
            actual=type(schema).__name__,
        )
    try:
        errors = schema_errors(schema, raw_registry)
    except SchemaEvaluationError:
        _fail(
            "REGISTRY_SCHEMA",
            expected="a valid local JSON Schema",
            actual="schema configuration or evaluation failed",
        )
    if errors:
        raise DocumentContractError(
            tuple(
                _diagnostic(
                    _schema_rule_id(error),
                    expected=error.message,
                    actual="schema validation failed",
                )
                for error in errors
            )
        )
    if trusted_registry is not None:
        proposed_profiles = raw_registry["profiles"]
        proposed_ids = tuple(profile["id"] for profile in proposed_profiles)
        trusted_ids = tuple(profile.profile_id for profile in trusted_registry.profiles)
        matches = len(set(proposed_ids)) == len(proposed_ids) and set(
            proposed_ids
        ) == set(trusted_ids)
        if matches:
            trusted_profiles = {
                profile.profile_id: profile for profile in trusted_registry.profiles
            }
            matches = all(
                profile["pathPattern"] == trusted_profiles[profile["id"]].path_pattern
                and profile.get("artifactIdPattern")
                == trusted_profiles[profile["id"]].artifact_id_pattern
                for profile in proposed_profiles
            )
        if not matches:
            _fail(
                "REGISTRY_EXECUTABLE_POLICY",
                expected="the trusted profile identities and literal patterns",
                actual="proposed executable policy differs",
            )
    try:
        validate_registry_authority(raw_registry)
    except AuthorityError as exc:
        _fail(
            "REGISTRY_AUTHORITY",
            expected="the sole bounded Stage 99 document-profile authority",
            actual=str(exc),
        )
    semantic_diagnostics = _terminal_semantic_diagnostics(
        root, raw_registry, template_regular_paths=template_regular_paths
    )
    if semantic_diagnostics:
        raise DocumentContractError(semantic_diagnostics)
    return _typed_registry_from_mapping(raw_registry)


def _load_published_contract(
    root: Path,
    path: PurePosixPath,
    schema_path: PurePosixPath,
    *,
    raw_payload: object = _UNSET,
    raw_schema: object = _UNSET,
) -> dict[str, Any]:
    """Decode one published contract and validate it against its own schema.

    Identity is checked before the schema is read so that a payload from a
    retired schema generation is rejected as REGISTRY_SCHEMA rather than
    reaching a schema this repository no longer ships.
    """

    if (raw_payload is _UNSET) != (raw_schema is _UNSET):
        _fail(
            "REGISTRY_SCHEMA",
            expected="complete supplied registry and schema inputs",
            actual="a supplied input is unavailable",
        )
    payload = (
        load_json_file(root / path, diagnostic_path=path)
        if raw_payload is _UNSET
        else raw_payload
    )
    if not isinstance(payload, dict):
        _fail(
            "REGISTRY_SCHEMA",
            expected=f"a JSON object at {path.as_posix()}",
            actual=type(payload).__name__,
        )
    expected_id = f"https://hy-home.k8s/{path.as_posix()}"
    if payload.get("schemaVersion") != 8 or payload.get("$id") != expected_id:
        _fail(
            "REGISTRY_SCHEMA",
            expected=f"schemaVersion=8 $id={expected_id!r}",
            actual=(
                f"schemaVersion={payload.get('schemaVersion')!r} "
                f"$id={payload.get('$id')!r}"
            ),
        )
    schema = (
        load_json_file(root / schema_path, diagnostic_path=schema_path)
        if raw_schema is _UNSET
        else raw_schema
    )
    if not isinstance(schema, dict):
        _fail(
            "REGISTRY_SCHEMA",
            expected=f"a JSON Schema object at {schema_path.as_posix()}",
            actual=type(schema).__name__,
        )
    try:
        errors = schema_errors(schema, payload)
    except SchemaEvaluationError:
        _fail(
            "REGISTRY_SCHEMA",
            expected="a valid local JSON Schema",
            actual="schema configuration or evaluation failed",
        )
    if errors:
        raise DocumentContractError(
            tuple(
                _diagnostic(
                    _schema_rule_id(error),
                    path=path,
                    expected=error.message,
                    actual="schema validation failed",
                )
                for error in errors
            )
        )
    return dict(payload)


def _split_top_level_alternation(body: str) -> list[str]:
    """Split one alternation, ignoring bars inside groups, classes, or escapes."""

    parts: list[str] = []
    buffer: list[str] = []
    depth = 0
    in_class = False
    index = 0
    while index < len(body):
        char = body[index]
        if char == "\\":
            buffer.append(body[index : index + 2])
            index += 2
            continue
        if in_class:
            if char == "]":
                in_class = False
        elif char == "[":
            in_class = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "|" and depth == 0:
            parts.append("".join(buffer))
            buffer = []
            index += 1
            continue
        buffer.append(char)
        index += 1
    parts.append("".join(buffer))
    return parts


def _internal_routes(pattern: str) -> list[dict[str, str]]:
    """Recover the internal route list a published ``pathPattern`` encodes.

    The published form states one anchored expression per profile, with an
    alternation when the profile owns several routes. Recovering the branches
    matters beyond matching: self-tests select a route by ``kind``, so a
    projection that flattened every branch to one regex would silently retarget
    them. A branch whose escaping round-trips is an exact route; anything else
    stays a regex.
    """

    if not (pattern.startswith("^") and pattern.endswith("$")):
        _fail(
            "REGISTRY_SCHEMA",
            expected="an anchored pathPattern",
            actual=pattern,
        )
    inner = pattern[1:-1]
    branches = (
        _split_top_level_alternation(inner[3:-1])
        if inner.startswith("(?:") and inner.endswith(")")
        else [inner]
    )
    routes: list[dict[str, str]] = []
    for branch in branches:
        literal = re.sub(r"\\(.)", r"\1", branch)
        if re.escape(literal) == branch:
            routes.append({"kind": "exact", "value": literal})
        else:
            routes.append({"kind": "regex", "value": f"^{branch}$"})
    return routes


def _internal_profile_form(profile: Mapping[str, Any]) -> dict[str, Any]:
    """Project one published profile into the typed consumer input shape."""

    return {
        "id": profile["id"],
        "class": profile["class"],
        "mode": profile["mode"],
        "routes": _internal_routes(profile["pathPattern"]),
        "artifactIdPattern": profile.get("artifactIdPattern"),
        "frontmatter": profile["requiredFrontmatter"],
        "statusDomain": profile.get("lifecycle", {}).get("statusDomain", []),
        "headings": profile["requiredSections"],
        "template": profile["template"],
        "sourceProfileIds": profile["relationships"]["sourceProfileIds"],
        "placeholderPolicy": profile["placeholderPolicy"],
        "bodyContract": profile["relationships"]["bodyContract"],
    }


def load_internal_payload(
    root: Path,
    *,
    raw_registry: object = _UNSET,
    raw_schema: object = _UNSET,
    template_regular_paths: frozenset[PurePosixPath] | None = None,
) -> dict[str, Any]:
    """Return a defensive copy of the sole published Stage 99 registry.

    The terminal topology deliberately has no flat-registry or route-contract
    projection. Consumers mutate only this private copy in tests; production
    authority remains the root registry and its profile schema.
    """

    root = root.absolute()
    if (
        raw_registry is not _UNSET
        or raw_schema is not _UNSET
        or template_regular_paths is not None
    ) and (
        raw_registry is _UNSET
        or raw_schema is _UNSET
        or not isinstance(template_regular_paths, frozenset)
        or any(not isinstance(path, PurePosixPath) for path in template_regular_paths)
    ):
        _fail(
            "REGISTRY_SCHEMA",
            expected="complete supplied registry, schema and template regularity facts",
            actual="a supplied input is unavailable or malformed",
        )
    registry = _load_published_contract(
        root,
        REGISTRY_PATH,
        PROFILE_SCHEMA_PATH,
        raw_payload=raw_registry,
        raw_schema=raw_schema,
    )
    try:
        validate_registry_authority(registry)
    except AuthorityError as exc:
        _fail(
            "REGISTRY_AUTHORITY",
            expected="the sole bounded Stage 99 document-profile authority",
            actual=str(exc),
        )
    semantic_diagnostics = _terminal_semantic_diagnostics(
        root, registry, template_regular_paths=template_regular_paths
    )
    if semantic_diagnostics:
        raise DocumentContractError(semantic_diagnostics)
    return copy.deepcopy(registry)


def load_registry(
    root: Path,
    *,
    raw_registry: object = _UNSET,
    raw_schema: object = _UNSET,
    template_regular_paths: frozenset[PurePosixPath] | None = None,
) -> Registry:
    """Build the typed view directly from the root registry authority."""

    return _typed_registry_from_mapping(
        load_internal_payload(
            root,
            raw_registry=raw_registry,
            raw_schema=raw_schema,
            template_regular_paths=template_regular_paths,
        )
    )


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
