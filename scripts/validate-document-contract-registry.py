#!/usr/bin/env python3
"""Validate the terminal document-profile registry and deterministic routing."""

from __future__ import annotations

import argparse
import stat
import subprocess
from dataclasses import replace
from pathlib import Path, PurePosixPath
from typing import Any

from document_authority import AuthorityError, load_bounded_json, run_bounded_process
from document_contracts import (
    DocumentContractError,
    FrontmatterContract,
    Registry,
    TargetInventory,
    classify_path,
    classify_paths,
    enumerate_target_markdown,
    load_json_file,
    load_registry,
)


GEMINI_NATIVE_CURRENT_SURFACE_RULE = "REGISTRY_GEMINI_NATIVE_CURRENT_SURFACE"
GEMINI_NATIVE_CURRENT_SURFACE_ERROR = (
    f"{GEMINI_NATIVE_CURRENT_SURFACE_RULE}: Gemini CLI native surface must be "
    "a closed repository-static current projection"
)
DOCUMENT_REGISTRY_ROOT_ERROR = (
    "REGISTRY_ROOT_BOUNDARY: repository root must be an existing non-symlink directory"
)
GEMINI_SETTINGS_SCHEMA_URL = (
    "https://raw.githubusercontent.com/google-gemini/gemini-cli/main/"
    "schemas/settings.schema.json"
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
        "specs",
    }
)
GEMINI_SETTINGS_MAX_BYTES = 16 * 1024
GIT_TIMEOUT_SECONDS = 10
GIT_INVENTORY_MAX_BYTES = 16 * 1024


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


def _repo_path_without_symlinks(
    root: Path,
    relative: PurePosixPath,
    *,
    final_kind: str,
) -> Path:
    if relative.is_absolute() or any(
        part in {"", ".", ".."} for part in relative.parts
    ):
        raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)
    strict_root = _assert_repository_root_directory(
        root,
        error=GEMINI_NATIVE_CURRENT_SURFACE_ERROR,
    )
    candidate = strict_root
    for index, part in enumerate(relative.parts):
        candidate = candidate / part
        try:
            mode = candidate.lstat().st_mode
        except OSError as exc:
            raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR) from exc
        if stat.S_ISLNK(mode):
            raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)
        final = index == len(relative.parts) - 1
        if not final and not stat.S_ISDIR(mode):
            raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)
        if final and final_kind == "directory" and not stat.S_ISDIR(mode):
            raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)
        if final and final_kind == "file" and not stat.S_ISREG(mode):
            raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)
    try:
        candidate.resolve(strict=True).relative_to(strict_root)
    except (OSError, ValueError) as exc:
        raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR) from exc
    return candidate


def _load_gemini_settings_json(path: Path) -> dict[str, Any]:
    try:
        payload = load_bounded_json(path, max_bytes=GEMINI_SETTINGS_MAX_BYTES)
    except AuthorityError as exc:
        raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR) from exc
    if not isinstance(payload, dict):
        raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)
    return payload


def _expected_gemini_settings_json() -> dict[str, Any]:
    return {"$schema": GEMINI_SETTINGS_SCHEMA_URL, "agents": {"overrides": {}}}


def _harness_current_role_ids(root: Path) -> tuple[str, ...]:
    harness = load_json_file(
        root / "docs/00.agent-governance/contracts/harness-contract.json"
    )
    try:
        inventory = harness["currentInventory"]
        role_ids = tuple(inventory["roleIds"])
    except (KeyError, TypeError) as exc:
        raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR) from exc
    if (
        inventory.get("state") != "current"
        or inventory.get("expectedRoleCount") != 12
        or inventory.get("expectedSurfaceCount") != 4
        or inventory.get("expectedProjectionCount") != 48
        or len(role_ids) != 12
        or len(role_ids) != len(set(role_ids))
        or any(not isinstance(role_id, str) or not role_id for role_id in role_ids)
    ):
        raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)
    return role_ids


def _assert_gemini_native_current_surface(root: Path) -> None:
    """Preserve the provider surface until its owning WP-003 cutover."""

    strict_root = _assert_repository_root_directory(
        root,
        error=GEMINI_NATIVE_CURRENT_SURFACE_ERROR,
    )
    role_ids = _harness_current_role_ids(strict_root)
    agents_dir = _repo_path_without_symlinks(
        strict_root,
        PurePosixPath(".gemini/agents"),
        final_kind="directory",
    )
    settings_path = _repo_path_without_symlinks(
        strict_root,
        PurePosixPath(".gemini/settings.json"),
        final_kind="file",
    )
    expected_names = {f"{role_id}.md" for role_id in role_ids}
    try:
        entries = tuple(agents_dir.iterdir())
    except OSError as exc:
        raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR) from exc
    actual_names: set[str] = set()
    for entry in entries:
        try:
            mode = entry.lstat().st_mode
        except OSError as exc:
            raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR) from exc
        if stat.S_ISLNK(mode) or not stat.S_ISREG(mode) or entry.suffix != ".md":
            raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)
        actual_names.add(entry.name)
    if actual_names != expected_names:
        raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)
    if _load_gemini_settings_json(settings_path) != _expected_gemini_settings_json():
        raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)


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


def _without_artifact_id(contract: FrontmatterContract) -> FrontmatterContract:
    return replace(
        contract,
        required=tuple(key for key in contract.required if key != "artifact_id"),
        allowed=tuple(key for key in contract.allowed if key != "artifact_id"),
        order=tuple(key for key in contract.order if key != "artifact_id"),
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
    append_profiles: set[str] = set()
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
        if profile.append_contract is not None:
            append_profiles.add(profile_id)
            contract = profile.append_contract
            if (
                profile_id != "governance/progress-entry"
                or source_id != "governance/progress-ledger"
                or contract.parent_profile_id != "governance/progress-ledger"
                or contract.parent_h2 != "Work Entries"
                or contract.entry_heading_level != 3
                or contract.section_heading_level != 4
                or contract.required_sections
                != ("Metadata", "Progress", "Memory", "Evidence", "Handoff")
            ):
                raise AssertionError(
                    "governance/progress-entry append contract differs"
                )
            checked.add(profile_id)
            continue
        source_frontmatter = source.frontmatter
        if (
            "artifact_id" in source_frontmatter.required
            and "artifact_id" not in profile.frontmatter.required
        ):
            source_frontmatter = _without_artifact_id(source_frontmatter)
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
    if append_profiles != {"governance/progress-entry"}:
        raise AssertionError(
            "governance/progress-entry must be the sole append template"
        )


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
        _assert_gemini_native_current_surface(root)
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
