#!/usr/bin/env python3
"""Validate the terminal document-profile registry and deterministic routing."""

from __future__ import annotations

import argparse
import hashlib
import re
import stat
import subprocess
from dataclasses import replace
from pathlib import Path, PurePosixPath
from typing import Any

from document_authority import AuthorityError, run_bounded_process
from document_contracts import (
    DocumentContractError,
    FrontmatterContract,
    Registry,
    TargetInventory,
    classify_path,
    classify_paths,
    enumerate_target_markdown,
    load_registry,
)
from validation.repository.bounded_io import BoundedInputError, read_bytes


DOCUMENT_REGISTRY_ROOT_ERROR = (
    "REGISTRY_ROOT_BOUNDARY: repository root must be an existing non-symlink directory"
)
RETIRED_CLOUD_SDLC_SURFACE_RULE = "REGISTRY_RETIRED_CLOUD_SDLC_SURFACE"
RETIRED_CLOUD_SDLC_SURFACE_ERROR = (
    f"{RETIRED_CLOUD_SDLC_SURFACE_RULE}: retired cloud documentation surface "
    "must remain absent from the Git index"
)
TERMINAL_TEMPLATE_GROUPS = frozenset(
    {
        "architecture",
        "archive",
        "common",
        "governance",
        "operations",
        "references",
        "requirements",
        "runtime",
        "specs",
    }
)
GIT_TIMEOUT_SECONDS = 10
GIT_INVENTORY_MAX_BYTES = 16 * 1024
REFERENCE_PACK_MAX_ENTRIES = 4096
REFERENCE_PACK_GIT_MAX_BYTES = 4 * 1024 * 1024
REFERENCE_PACK_FILE_MAX_BYTES = 8 * 1024 * 1024
REFERENCE_PACK_TOTAL_MAX_BYTES = 64 * 1024 * 1024
REFERENCE_PACK_PATTERN = re.compile(
    r"(?P<number>[0-9]{4})-[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z"
)
REFERENCE_PACK_CATEGORIES = (
    ("audits", "audit"),
    ("data", "data"),
    ("research", "research"),
)


def _include_path_argument(raw: str) -> PurePosixPath:
    path = PurePosixPath(raw)
    if (
        not raw
        or raw.startswith("./")
        or raw != path.as_posix()
        or path.is_absolute()
        or ".." in path.parts
        or "\\" in raw
    ):
        raise argparse.ArgumentTypeError(
            "include path must be normalized and repository-relative"
        )
    return path


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--mode", choices=("strict",), default="strict")
    parser.add_argument(
        "--route-state",
        choices=("legacy", "transition", "terminal"),
        help="parse-only compatibility argument; the registry is terminal",
    )
    parser.add_argument("--profile")
    parser.add_argument(
        "--include-path",
        action="append",
        default=[],
        metavar="REPOSITORY_PATH",
        type=_include_path_argument,
    )
    return parser.parse_args()


def _assert_repository_root_directory(
    root: Path,
    *,
    error: str = DOCUMENT_REGISTRY_ROOT_ERROR,
) -> Path:
    absolute_root = root.absolute()
    try:
        mode = absolute_root.lstat().st_mode
    except OSError as exc:
        raise AssertionError(error) from exc
    if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
        raise AssertionError(error)
    try:
        return absolute_root.resolve(strict=True)
    except OSError as exc:
        raise AssertionError(error) from exc


def _assert_retired_cloud_sdlc_surfaces_absent(root: Path) -> None:
    try:
        completed = run_bounded_process(
            [
                "git",
                "ls-files",
                "-z",
                "--",
                "examples/aws/docs",
                "examples/azure/docs",
            ],
            cwd=root,
            check=True,
            timeout_seconds=GIT_TIMEOUT_SECONDS,
            max_stdout_bytes=GIT_INVENTORY_MAX_BYTES,
        )
    except AuthorityError as exc:
        raise AssertionError(f"{RETIRED_CLOUD_SDLC_SURFACE_RULE}: {exc}") from exc
    if completed.stdout and not completed.stdout.endswith(b"\0"):
        raise AssertionError(
            f"{RETIRED_CLOUD_SDLC_SURFACE_RULE}: Git index inventory must be NUL terminated"
        )
    if completed.stdout:
        raise AssertionError(RETIRED_CLOUD_SDLC_SURFACE_ERROR)


def _bounded_directory_entries(path: Path) -> tuple[Path, ...]:
    """List one held topology level without following a directory symlink."""

    try:
        mode = path.lstat().st_mode
    except OSError as exc:
        raise AssertionError(
            f"REFERENCE_PACK_DIRECTORY: {path.as_posix()} is unavailable"
        ) from exc
    if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
        raise AssertionError(
            f"REFERENCE_PACK_DIRECTORY: {path.as_posix()} must be a regular directory"
        )
    entries: list[Path] = []
    try:
        for entry in path.iterdir():
            entries.append(entry)
            if len(entries) > REFERENCE_PACK_MAX_ENTRIES:
                raise AssertionError(
                    f"REFERENCE_PACK_LIMIT: {path.as_posix()} exceeds the entry budget"
                )
    except OSError as exc:
        raise AssertionError(
            f"REFERENCE_PACK_DIRECTORY: {path.as_posix()} cannot be enumerated"
        ) from exc
    return tuple(sorted(entries, key=lambda entry: entry.name))


def _staged_reference_files(root: Path) -> dict[PurePosixPath, str]:
    """Return canonical stage-zero regular files below the Stage 90 boundary."""

    try:
        completed = run_bounded_process(
            [
                "git",
                "ls-files",
                "--stage",
                "-z",
                "--",
                "docs/90.references",
            ],
            cwd=root,
            check=True,
            timeout_seconds=GIT_TIMEOUT_SECONDS,
            max_stdout_bytes=REFERENCE_PACK_GIT_MAX_BYTES,
        )
    except (AuthorityError, subprocess.SubprocessError) as exc:
        raise AssertionError(
            f"REFERENCE_PACK_INDEX: stage-zero inventory is unavailable: {exc}"
        ) from exc
    if completed.stdout and not completed.stdout.endswith(b"\0"):
        raise AssertionError(
            "REFERENCE_PACK_INDEX: stage-zero inventory is not NUL terminated"
        )
    records = completed.stdout.split(b"\0")
    inventory: dict[PurePosixPath, str] = {}
    try:
        for record in records[:-1]:
            header, raw_path = record.split(b"\t", 1)
            mode, raw_object_id, stage = header.split(b" ", 2)
            object_id = raw_object_id.decode("ascii", errors="strict")
            decoded = raw_path.decode("utf-8", errors="strict")
            path = PurePosixPath(decoded)
            if (
                mode not in {b"100644", b"100755"}
                or re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", object_id)
                is None
                or stage != b"0"
                or path.as_posix() != decoded
                or path.is_absolute()
                or ".." in path.parts
                or path.parts[:2] != ("docs", "90.references")
                or path in inventory
            ):
                raise ValueError
            inventory[path] = object_id
            if len(inventory) > REFERENCE_PACK_MAX_ENTRIES:
                raise AssertionError(
                    "REFERENCE_PACK_LIMIT: Stage 90 index exceeds the entry budget"
                )
    except (UnicodeDecodeError, ValueError) as exc:
        raise AssertionError(
            "REFERENCE_PACK_INDEX: stage-zero inventory is malformed"
        ) from exc
    return inventory


def _assert_reference_pack_topology(root: Path, registry: Registry) -> None:
    """Enforce the only current Stage 90 pack routes and their Stage 99 forms."""

    stage_root = root / "docs/90.references"
    staged_inventory = _staged_reference_files(root)
    staged_files = frozenset(staged_inventory)
    worktree_files: set[PurePosixPath] = set()
    errors: list[str] = []
    root_entries = _bounded_directory_entries(stage_root)
    allowed_root_entries = {"README.md", *(item[0] for item in REFERENCE_PACK_CATEGORIES)}
    for entry in root_entries:
        try:
            mode = entry.lstat().st_mode
        except OSError:
            errors.append(f"REFERENCE_PACK_ROOT_ENTRY: {entry.name} is unavailable")
            continue
        if entry.name == "README.md":
            if not stat.S_ISREG(mode):
                errors.append("REFERENCE_PACK_ROOT_ENTRY: README.md must be regular")
            else:
                worktree_files.add(
                    PurePosixPath(entry.relative_to(root).as_posix())
                )
            continue
        if stat.S_ISREG(mode):
            worktree_files.add(PurePosixPath(entry.relative_to(root).as_posix()))
        if entry.name not in allowed_root_entries or not stat.S_ISDIR(mode):
            errors.append(
                f"REFERENCE_PACK_ROOT_ENTRY: {entry.name} is outside audits/data/research"
            )

    for category, singular in REFERENCE_PACK_CATEGORIES:
        category_root = stage_root / category
        if not category_root.exists() and not category_root.is_symlink():
            continue
        entries = _bounded_directory_entries(category_root)
        router = category_root / "README.md"
        try:
            router_mode = router.lstat().st_mode
        except OSError:
            errors.append(f"REFERENCE_PACK_CATEGORY_README: {category}/README.md is missing")
        else:
            if not stat.S_ISREG(router_mode):
                errors.append(
                    f"REFERENCE_PACK_CATEGORY_README: {category}/README.md must be regular"
                )
            else:
                worktree_files.add(
                    PurePosixPath(router.relative_to(root).as_posix())
                )

        numbers: dict[str, str] = {}
        for entry in entries:
            if entry.name == "README.md":
                continue
            try:
                mode = entry.lstat().st_mode
            except OSError:
                errors.append(
                    f"REFERENCE_PACK_ENTRY: {category}/{entry.name} is unavailable"
                )
                continue
            match = REFERENCE_PACK_PATTERN.fullmatch(entry.name)
            if match is None or stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
                if stat.S_ISREG(mode):
                    worktree_files.add(
                        PurePosixPath(entry.relative_to(root).as_posix())
                    )
                errors.append(
                    f"REFERENCE_PACK_ENTRY: {category}/{entry.name} must be ####-<slug>/"
                )
                continue
            number = match.group("number")
            if number in numbers:
                errors.append(
                    f"REFERENCE_PACK_NUMBER: {category}/{entry.name} duplicates "
                    f"{numbers[number]}"
                )
            numbers[number] = entry.name

            readme = entry / "README.md"
            try:
                readme_mode = readme.lstat().st_mode
            except OSError:
                errors.append(
                    f"REFERENCE_PACK_README: {category}/{entry.name}/README.md is missing"
                )
            else:
                if not stat.S_ISREG(readme_mode):
                    errors.append(
                        f"REFERENCE_PACK_README: {category}/{entry.name}/README.md "
                        "must be regular"
                    )
                else:
                    worktree_files.add(
                        PurePosixPath(readme.relative_to(root).as_posix())
                    )
                    profile = classify_path(
                        registry,
                        PurePosixPath(
                            f"docs/90.references/{category}/{entry.name}/README.md"
                        ),
                    )
                    expected_template = PurePosixPath(
                        "docs/99.templates/templates/references/"
                        f"{singular}-pack.template.md"
                    )
                    if (
                        profile.profile_id != f"readme/{singular}-pack"
                        or profile.template != expected_template
                    ):
                        errors.append(
                            f"REFERENCE_PACK_TEMPLATE: {category}/{entry.name}/README.md "
                            f"must use {expected_template.as_posix()}"
                        )

            for member in _bounded_directory_entries(entry):
                try:
                    member_mode = member.lstat().st_mode
                except OSError:
                    errors.append(
                        f"REFERENCE_PACK_MEMBER: {category}/{entry.name}/{member.name} "
                        "is unavailable"
                    )
                    continue
                if not stat.S_ISREG(member_mode):
                    errors.append(
                        f"REFERENCE_PACK_MEMBER: {category}/{entry.name}/{member.name} "
                        "must be regular"
                    )
                else:
                    worktree_files.add(
                        PurePosixPath(member.relative_to(root).as_posix())
                    )

    if staged_files != worktree_files:
        index_only = ",".join(
            path.as_posix() for path in sorted(staged_files - worktree_files)[:3]
        )
        worktree_only = ",".join(
            path.as_posix() for path in sorted(worktree_files - staged_files)[:3]
        )
        errors.append(
            "REFERENCE_PACK_INDEX_DRIFT: stage-zero and worktree regular-file "
            f"sets differ; index_only={index_only or '-'}; "
            f"worktree_only={worktree_only or '-'}"
        )
    else:
        total_bytes = 0
        for path in sorted(staged_inventory):
            try:
                content = read_bytes(
                    root.joinpath(*path.parts),
                    max_bytes=REFERENCE_PACK_FILE_MAX_BYTES,
                )
            except BoundedInputError as exc:
                errors.append(
                    f"REFERENCE_PACK_INDEX_DRIFT: {path.as_posix()} cannot be "
                    f"compared safely: {exc}"
                )
                continue
            total_bytes += len(content)
            if total_bytes > REFERENCE_PACK_TOTAL_MAX_BYTES:
                errors.append(
                    "REFERENCE_PACK_LIMIT: Stage 90 worktree bytes exceed the "
                    "aggregate budget"
                )
                break
            object_id = staged_inventory[path]
            algorithm = "sha1" if len(object_id) == 40 else "sha256"
            hasher = hashlib.new(algorithm, usedforsecurity=False)
            hasher.update(f"blob {len(content)}\0".encode("ascii"))
            hasher.update(content)
            if hasher.hexdigest() != object_id:
                errors.append(
                    f"REFERENCE_PACK_INDEX_DRIFT: {path.as_posix()} differs "
                    "between stage zero and worktree"
                )

    if errors:
        raise AssertionError("\n".join(errors))


# A form declares only what its author must write into the copy. A Stage 99 file
# is not the document it produces, so it carries neither the document's identity
# nor the layer that document will live in.
TEMPLATE_OMITTED_KEYS = ("artifact_id", "layer")


def _without_key(contract: FrontmatterContract, key: str) -> FrontmatterContract:
    return replace(
        contract,
        required=tuple(name for name in contract.required if name != key),
        allowed=tuple(name for name in contract.allowed if name != key),
        order=tuple(name for name in contract.order if name != key),
    )


def _assert_template_source_parity(registry: Registry) -> None:
    """Require every terminal form to inherit exactly one source profile."""

    profiles = {profile.profile_id: profile for profile in registry.profiles}
    declared_templates = {
        profile.profile_id
        for profile in registry.profiles
        if profile.mode == "template"
    }
    checked: set[str] = set()
    for profile_id in sorted(declared_templates):
        profile = profiles[profile_id]
        if profile.template is None or len(profile.routes) != 1:
            raise AssertionError(f"{profile_id}: template route is not exact")
        route = profile.routes[0]
        if route.kind != "exact" or route.value != profile.template.as_posix():
            raise AssertionError(f"{profile_id}: template route differs from owner")
        parts = profile.template.parts
        if (
            len(parts) < 4
            or parts[:3] != ("docs", "99.templates", "templates")
            or parts[3] not in TERMINAL_TEMPLATE_GROUPS
        ):
            raise AssertionError(f"{profile_id}: template path is not terminal")
        if len(profile.source_profile_ids) != 1:
            raise AssertionError(f"{profile_id}: template needs one source profile")
        source_id = profile.source_profile_ids[0]
        source = profiles.get(source_id)
        if source is None:
            raise AssertionError(f"{profile_id}: unknown source profile {source_id}")
        source_frontmatter = source.frontmatter
        for omitted in TEMPLATE_OMITTED_KEYS:
            if (
                omitted in source_frontmatter.allowed
                and omitted not in profile.frontmatter.allowed
            ):
                source_frontmatter = _without_key(source_frontmatter, omitted)
        inherited = (
            profile.profile_class,
            profile.frontmatter,
            profile.headings,
            profile.body_contract,
        )
        expected = (
            source.profile_class,
            source_frontmatter,
            source.headings,
            source.body_contract,
        )
        if inherited != expected:
            raise AssertionError(
                f"{profile_id}: template/source contract differs from {source_id}"
            )
        checked.add(profile_id)
    if checked != declared_templates:
        raise AssertionError("template/source parity did not cover every template")


def _readme_family_counts(
    registry: Registry,
    inventory: TargetInventory,
) -> tuple[int, int, int]:
    readme_profile_ids = {
        profile.profile_id
        for profile in registry.profiles
        if profile.profile_class == "readme"
    }
    current = tuple(
        path
        for path in inventory.current_paths
        if classify_path(registry, path).profile_id in readme_profile_ids
    )
    new = tuple(path for path in current if path in set(inventory.new_paths))
    baseline = tuple(
        path for path in inventory.baseline_paths if path.name == "README.md"
    )
    return len(baseline), len(current), len(new)


def _print_diagnostic(diagnostic: Any) -> None:
    print(
        f"FAIL {diagnostic.rule_id} {diagnostic.path.as_posix()}: "
        f"expected {diagnostic.expected}; actual {diagnostic.actual}"
    )


def main() -> int:
    args = _parse_args()
    try:
        root = _assert_repository_root_directory(args.root)
        registry = load_registry(root)
        _assert_template_source_parity(registry)
        _assert_reference_pack_topology(root, registry)
        _assert_retired_cloud_sdlc_surfaces_absent(root)
        profile_ids = {profile.profile_id for profile in registry.profiles}
        readme_family = args.profile == "readme"
        if args.profile and not readme_family and args.profile not in profile_ids:
            raise ValueError(f"unknown profile: {args.profile}")
        inventory = enumerate_target_markdown(
            root,
            include_paths=tuple(args.include_path),
        )
    except DocumentContractError as exc:
        for diagnostic in exc.diagnostics:
            _print_diagnostic(diagnostic)
        return 1
    except (AssertionError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"FAIL document contract registry: {exc}")
        return 1

    diagnostics = classify_paths(registry, inventory.current_paths)
    uncovered_count = sum(
        diagnostic.rule_id == "REGISTRY_ROUTE_UNCOVERED" for diagnostic in diagnostics
    )
    ambiguous_count = sum(
        diagnostic.rule_id == "REGISTRY_ROUTE_AMBIGUOUS" for diagnostic in diagnostics
    )
    for diagnostic in diagnostics:
        _print_diagnostic(diagnostic)
    print(
        f"baseline={len(inventory.baseline_paths)} "
        f"new={len(inventory.new_paths)} "
        f"programs={len(registry.program_lineage)} "
        f"uncovered={uncovered_count} ambiguous={ambiguous_count}"
    )
    if diagnostics:
        return 1

    selected_count = len(inventory.current_paths)
    if args.profile:
        if readme_family:
            baseline_count, selected_count, new_count = _readme_family_counts(
                registry, inventory
            )
            print(
                f"README baseline={baseline_count} current={selected_count} "
                f"new={new_count} authority=root-registry uncovered=0 ambiguous=0"
            )
        else:
            selected_count = sum(
                classify_path(registry, path).profile_id == args.profile
                for path in inventory.current_paths
            )
    print(
        f"PASS document contract registry: {selected_count} paths "
        f"({args.mode}, tracked-only plus explicit includes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
