"""Typed document-profile registry loading and deterministic path routing."""

from __future__ import annotations

import json
import re
import stat
import subprocess
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path, PurePosixPath
from typing import Any, Literal, Mapping, NoReturn, Sequence

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
SCHEMA_PATH = PurePosixPath(
    "docs/99.templates/support/document-profiles.schema.json"
)


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
class DocumentProfile:
    profile_id: str
    profile_class: Literal["sdlc", "common", "governance", "readme", "exception"]
    routes: tuple[Route, ...]
    frontmatter: FrontmatterContract
    status_domain: tuple[str, ...]
    headings: HeadingContract
    template: PurePosixPath | None
    mode: Literal[
        "authored", "template", "frontmatter-free", "classification-only", "generated", "non-target"
    ]
    source_profile_ids: tuple[str, ...]
    placeholder_policy: Literal["forbidden", "template-only"]
    append_contract: AppendContract | None


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
class Registry:
    schema_version: int
    baseline_sha: str
    baseline_count: int
    profiles: tuple[DocumentProfile, ...]
    governance_current_owners: GovernanceCurrentOwners
    reference_current_packs: ReferenceCurrentPacks


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
            raise ValueError(f"included path does not exist: {path.as_posix()}") from exc
        if stat.S_ISLNK(mode):
            raise ValueError(f"included path crosses or names a symlink: {path.as_posix()}")
    return mode


def read_repository_text(root: Path, path: PurePosixPath) -> str:
    """Read one normalized regular file without following path symlinks."""

    normalized = _normalize_relative_path(path)
    mode = _lstat_named_path(root.absolute(), normalized)
    if not stat.S_ISREG(mode):
        raise ValueError(f"repository path is not a regular file: {normalized}")
    return (root.absolute() / normalized).read_text(encoding="utf-8")


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
    current_paths = {
        entry.path
        for entry in current_entries
        if entry.mode.startswith("100") and _is_target_markdown(entry.path)
    }
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
            raise ValueError(f"included path is indexed as a symlink: {path.as_posix()}")
        if not _is_target_markdown(path):
            raise ValueError(f"included path is not approved Markdown: {path.as_posix()}")
        current_paths.add(path)

    return TargetInventory(
        baseline_paths=_sorted_paths(baseline_paths),
        current_paths=_sorted_paths(current_paths),
        new_paths=_sorted_paths(current_paths - baseline_paths),
        baseline_symlink_paths=_sorted_paths(baseline_symlinks),
        current_symlink_paths=_sorted_paths(current_symlinks),
    )


@lru_cache(maxsize=None)
def _compile_route(value: str) -> re.Pattern[str]:
    return re.compile(value)


def _schema_rule_id(error: Any) -> str:
    path = tuple(error.absolute_path)
    if (
        error.validator == "required"
        and "referenceCurrentPacks" in error.message
    ):
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


def _profile_from_mapping(raw: Mapping[str, Any]) -> DocumentProfile:
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
    )


def _reference_pack_from_mapping(raw: Mapping[str, Any]) -> ReferenceCurrentPack:
    return ReferenceCurrentPack(
        id=raw["id"],
        allowed_states=tuple(raw["allowedStates"]),
        members=tuple(raw["members"]),
    )


def validate_registry(root: Path, raw_registry: Mapping[str, Any]) -> Registry:
    """Validate a decoded registry and return its immutable typed form."""

    root = root.absolute()
    with (root / SCHEMA_PATH).open("r", encoding="utf-8") as handle:
        schema = json.load(handle)

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

    for raw_profile in raw_profiles:
        profile_id = raw_profile["id"]
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
    status_domain = set(reference_profile["statusDomain"]) if reference_profile else set()
    for raw_pack in raw_packs:
        collection = raw_pack["id"].split("/", 1)[0]
        expected_states = ["done"] if collection == "audits" else ["active", "accepted"]
        if (
            raw_pack["allowedStates"] != expected_states
            or not set(raw_pack["allowedStates"]).issubset(status_domain)
        ):
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_REFERENCE_CURRENT_PACK_STATE",
                    expected=f"{collection} allowed states {expected_states!r} within content/reference",
                    actual="allowed-state contract differs",
                )
            )

    if diagnostics:
        raise DocumentContractError(diagnostics)

    registry = Registry(
        schema_version=raw_registry["schemaVersion"],
        baseline_sha=baseline["sha"],
        baseline_count=baseline["count"],
        profiles=tuple(_profile_from_mapping(profile) for profile in raw_profiles),
        governance_current_owners=GovernanceCurrentOwners(
            profile_id=raw_current_owners["profileId"],
            allowed_states=tuple(raw_current_owners["allowedStates"]),
            paths=tuple(normalized_current_paths),
        ),
        reference_current_packs=ReferenceCurrentPacks(
            profile_id=raw_reference_packs["profileId"],
            packs=tuple(_reference_pack_from_mapping(pack) for pack in raw_packs),
        ),
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
                *(
                    path.as_posix()
                    for path in registry.governance_current_owners.paths
                ),
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
            actual_profile.profile_id
            != registry.governance_current_owners.profile_id
            or actual_profile.mode != "authored"
        ):
            current_owner_diagnostics.append(
                _diagnostic(
                    "REGISTRY_GOVERNANCE_CURRENT_OWNER_PROFILE",
                    path=path,
                    profile=actual_profile.profile_id,
                    expected=(
                        "authored "
                        + registry.governance_current_owners.profile_id
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
    return registry


def load_registry(root: Path) -> Registry:
    root = root.absolute()
    with (root / REGISTRY_PATH).open("r", encoding="utf-8") as handle:
        raw_registry = json.load(handle)
    if not isinstance(raw_registry, dict):
        _fail(
            "REGISTRY_SCHEMA",
            expected="a JSON object",
            actual=type(raw_registry).__name__,
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
