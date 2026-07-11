#!/usr/bin/env python3
"""Validate the document-profile registry and its deterministic routing."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

from document_contracts import (
    REGISTRY_PATH,
    DocumentContractError,
    classify_path,
    classify_paths,
    enumerate_target_markdown,
    load_registry,
    _parse_ls_files_stage_z,
    _parse_ls_tree_z,
    validate_registry,
)


SAMPLE_PATH = PurePosixPath("tests/fixtures/document-contracts/sample.md")
FIXTURE_PATH = PurePosixPath("tests/fixtures/document-contracts/registry-cases.json")
EXPECTED_CASES = (
    ("valid-minimal", "none", ()),
    ("duplicate-profile-id", "duplicate-profile-id", ("REGISTRY_PROFILE_ID",)),
    ("unsupported-route-kind", "route-kind-glob", ("REGISTRY_ROUTE_KIND",)),
    ("unanchored-regex", "drop-regex-end-anchor", ("REGISTRY_ROUTE_ANCHOR",)),
    ("overlapping-route", "add-overlapping-exact-route", ("REGISTRY_ROUTE_AMBIGUOUS",)),
    ("uncovered-route", "remove-sample-route", ("REGISTRY_ROUTE_UNCOVERED",)),
    ("missing-template", "point-to-missing-template", ("REGISTRY_TEMPLATE",)),
    ("wrong-baseline-sha", "change-baseline-sha", ("REGISTRY_BASELINE_SHA",)),
    ("wrong-baseline-count", "change-baseline-count", ("REGISTRY_BASELINE_COUNT",)),
)


def _include_path_argument(raw: str) -> PurePosixPath:
    if raw.startswith("./"):
        raise argparse.ArgumentTypeError("include path must not start with './'")
    return PurePosixPath(raw)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--mode", choices=("compatibility", "strict"), default="compatibility"
    )
    parser.add_argument("--profile")
    parser.add_argument(
        "--include-path",
        action="append",
        default=[],
        metavar="REPOSITORY_PATH",
        type=_include_path_argument,
    )
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _mutate(raw_registry: dict[str, Any], mutation: str) -> None:
    profile = next(
        profile
        for profile in raw_registry["profiles"]
        if any(
            route.get("kind") == "exact"
            and route.get("value") == SAMPLE_PATH.as_posix()
            for route in profile["routes"]
        )
    )
    route = next(
        route
        for route in profile["routes"]
        if route.get("kind") == "exact"
        and route.get("value") == SAMPLE_PATH.as_posix()
    )
    if mutation == "none":
        return
    if mutation == "duplicate-profile-id":
        raw_registry["profiles"].append(copy.deepcopy(profile))
        return
    if mutation == "route-kind-glob":
        route["kind"] = "glob"
        return
    if mutation == "drop-regex-end-anchor":
        regex_route = next(
            candidate
            for candidate in profile["routes"]
            if candidate.get("kind") == "regex"
        )
        regex_route["value"] = regex_route["value"].removesuffix("$")
        return
    if mutation == "add-overlapping-exact-route":
        profile["routes"].append({"kind": "exact", "value": SAMPLE_PATH.as_posix()})
        return
    if mutation == "remove-sample-route":
        profile["routes"].remove(route)
        return
    if mutation == "point-to-missing-template":
        profile["template"] = "docs/99.templates/templates/missing-document.md"
        return
    if mutation == "change-baseline-sha":
        raw_registry["baseline"]["sha"] = "0" * 40
        return
    if mutation == "change-baseline-count":
        raw_registry["baseline"]["count"] += 1
        return
    raise ValueError(f"unsupported fixture mutation: {mutation}")


def _ordered_rule_ids(diagnostics: Any) -> tuple[str, ...]:
    return tuple(dict.fromkeys(item.rule_id for item in diagnostics))


def _assert_inventory_safety(root: Path) -> None:
    fixture_dir = root / "tests/fixtures/document-contracts"
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix="document-contract-",
        suffix=".md",
        dir=fixture_dir,
        delete=False,
    ) as handle:
        handle.write("# Explicit include self-test\n")
        candidate = Path(handle.name)

    try:
        relative = PurePosixPath(candidate.relative_to(root).as_posix())
        inventory = enumerate_target_markdown(root, include_paths=(relative,))
        if relative not in inventory.current_paths:
            raise AssertionError("explicit untracked Markdown include was not inventoried")
    finally:
        candidate.unlink(missing_ok=True)

    rejected = (
        (PurePosixPath("_workspace/document-contract-ignored.md"), "ignored"),
        (PurePosixPath(".codex/skills"), "symlink"),
    )
    for path, expected_fragment in rejected:
        try:
            enumerate_target_markdown(root, include_paths=(path,))
        except ValueError as exc:
            if expected_fragment not in str(exc):
                raise AssertionError(
                    f"{path}: expected {expected_fragment!r} rejection, got {exc!r}"
                ) from exc
        else:
            raise AssertionError(f"unsafe explicit include was accepted: {path}")


def _assert_parser_safety() -> None:
    oid = b"0" * 40
    negative_cases = (
        (
            _parse_ls_tree_z,
            b"100600 blob " + oid + b"\tdocs/a.md\0",
            "noncanonical git ls-tree mode",
        ),
        (
            _parse_ls_tree_z,
            b"100644 tree " + oid + b"\tdocs/a.md\0",
            "impossible git ls-tree mode/type pair",
        ),
        (
            _parse_ls_tree_z,
            b"100644 blob " + (b"g" * 40) + b"\tdocs/a.md\0",
            "lowercase hexadecimal",
        ),
        (
            _parse_ls_tree_z,
            b"100644 blob " + (b"0" * 41) + b"\tdocs/a.md\0",
            "exactly 40 or 64",
        ),
        (
            _parse_ls_files_stage_z,
            b"040000 " + oid + b" 0\tdocs\0",
            "noncanonical git ls-files mode",
        ),
        (
            _parse_ls_files_stage_z,
            b"100644 " + (b"G" * 40) + b" 0\tdocs/a.md\0",
            "lowercase hexadecimal",
        ),
        (
            _parse_ls_files_stage_z,
            b"100644 " + (b"0" * 63) + b" 0\tdocs/a.md\0",
            "exactly 40 or 64",
        ),
    )
    for parser, raw, expected_fragment in negative_cases:
        try:
            parser(raw)
        except ValueError as exc:
            if expected_fragment not in str(exc):
                raise AssertionError(
                    f"expected {expected_fragment!r}, got {str(exc)!r}"
                ) from exc
        else:
            raise AssertionError(
                f"parser accepted invalid record requiring {expected_fragment!r}"
            )


def _tracked_template_paths(root: Path) -> tuple[PurePosixPath, ...]:
    completed = subprocess.run(
        [
            "git",
            "ls-files",
            "-z",
            "--",
            "docs/99.templates/templates/**/*.template.md",
        ],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    records = completed.stdout.split(b"\0")
    if records[-1] != b"":
        raise AssertionError("git ls-files template inventory is not NUL terminated")
    try:
        return tuple(
            sorted(
                (PurePosixPath(record.decode("utf-8")) for record in records[:-1]),
                key=lambda path: path.as_posix(),
            )
        )
    except UnicodeDecodeError as exc:
        raise AssertionError("git returned a non-UTF-8 template path") from exc


def _assert_positive_coverage(
    root: Path, raw_registry: dict[str, Any], fixture: dict[str, Any]
) -> tuple[int, int]:
    registry = validate_registry(root, raw_registry)
    profiles = {profile.profile_id: profile for profile in registry.profiles}

    coverage = fixture.get("profileCoverage")
    if not isinstance(coverage, list):
        raise AssertionError("profileCoverage must be an array")
    coverage_ids = [row.get("profile") for row in coverage if isinstance(row, dict)]
    if len(coverage_ids) != len(coverage):
        raise AssertionError("profileCoverage rows must be objects")
    if len(coverage_ids) != len(set(coverage_ids)):
        raise AssertionError("profileCoverage must contain each profile exactly once")
    if set(coverage_ids) != set(profiles):
        missing = sorted(set(profiles) - set(coverage_ids))
        extra = sorted(set(coverage_ids) - set(profiles))
        raise AssertionError(
            f"profileCoverage profile set mismatch: missing={missing!r} extra={extra!r}"
        )
    for row in coverage:
        if set(row) != {"path", "profile"} or not all(
            isinstance(row[key], str) and row[key] for key in ("path", "profile")
        ):
            raise AssertionError(f"invalid profileCoverage row: {row!r}")
        actual = classify_path(registry, PurePosixPath(row["path"])).profile_id
        if actual != row["profile"]:
            raise AssertionError(
                f"{row['path']}: expected profile {row['profile']!r}, got {actual!r}"
            )

    template_coverage = fixture.get("templateCoverage")
    if not isinstance(template_coverage, list):
        raise AssertionError("templateCoverage must be an array")
    if any(
        not isinstance(row, dict)
        or set(row) != {"path", "profile"}
        or not all(
            isinstance(row[key], str) and row[key]
            for key in ("path", "profile")
        )
        for row in template_coverage
    ):
        raise AssertionError("templateCoverage rows must contain only path and profile")
    fixture_template_paths = tuple(
        sorted(
            (PurePosixPath(row["path"]) for row in template_coverage),
            key=lambda path: path.as_posix(),
        )
    )
    if len(fixture_template_paths) != len(set(fixture_template_paths)):
        raise AssertionError("templateCoverage paths must be unique")
    tracked_template_paths = _tracked_template_paths(root)
    if fixture_template_paths != tracked_template_paths:
        raise AssertionError(
            "templateCoverage path set must equal tracked *.template.md inventory"
        )

    covered_template_profiles: set[str] = set()
    append_profiles: set[str] = set()
    for row in template_coverage:
        path = PurePosixPath(row["path"])
        profile = classify_path(registry, path)
        if profile.profile_id != row["profile"]:
            raise AssertionError(
                f"{path}: expected template profile {row['profile']!r}, "
                f"got {profile.profile_id!r}"
            )
        if profile.mode != "template":
            raise AssertionError(f"{profile.profile_id}: expected template mode")
        if profile.placeholder_policy != "template-only":
            raise AssertionError(
                f"{profile.profile_id}: expected template-only placeholder policy"
            )
        if len(profile.routes) != 1 or (
            profile.routes[0].kind != "exact"
            or profile.routes[0].value != path.as_posix()
        ):
            raise AssertionError(
                f"{profile.profile_id}: expected one exact route to {path.as_posix()}"
            )
        if profile.template != path:
            raise AssertionError(
                f"{profile.profile_id}: template must equal its exact route"
            )
        covered_template_profiles.add(profile.profile_id)
        if profile.append_contract is not None:
            append_profiles.add(profile.profile_id)
            if profile.profile_id != "governance/progress-entry":
                raise AssertionError(
                    f"{profile.profile_id}: unexpected append contract"
                )
            append_contract = profile.append_contract
            if (
                profile.source_profile_ids != ("governance/progress-ledger",)
                or append_contract.parent_profile_id
                != "governance/progress-ledger"
                or append_contract.parent_h2 != "Work Entries"
                or append_contract.entry_heading_level != 3
                or append_contract.section_heading_level != 4
                or append_contract.required_sections
                != ("Metadata", "Progress", "Memory", "Evidence", "Handoff")
            ):
                raise AssertionError(
                    "governance/progress-entry append contract does not match "
                    "the ledger H3/H4 contract"
                )
            continue
        if not profile.source_profile_ids:
            raise AssertionError(
                f"{profile.profile_id}: ordinary template must declare a source profile"
            )
        for source_id in profile.source_profile_ids:
            source = profiles.get(source_id)
            if source is None:
                raise AssertionError(
                    f"{profile.profile_id}: unknown source profile {source_id!r}"
                )
            inherited = (
                profile.profile_class,
                profile.frontmatter,
                profile.status_domain,
                profile.headings,
            )
            expected = (
                source.profile_class,
                source.frontmatter,
                source.status_domain,
                source.headings,
            )
            if inherited != expected:
                raise AssertionError(
                    f"{profile.profile_id}: inherited contract differs from {source_id}"
                )

        if profile.profile_id == "template/readme/common":
            readme_profile_ids = {
                candidate.profile_id
                for candidate in registry.profiles
                if candidate.profile_class == "readme"
                and candidate.mode == "frontmatter-free"
            }
            if set(profile.source_profile_ids) != readme_profile_ids:
                raise AssertionError(
                    "template/readme/common must source all six README profiles"
                )

    declared_template_profiles = {
        profile.profile_id for profile in registry.profiles if profile.mode == "template"
    }
    if covered_template_profiles != declared_template_profiles:
        raise AssertionError(
            "templateCoverage profile set must equal declared template profiles"
        )
    if append_profiles != {"governance/progress-entry"}:
        raise AssertionError(
            "governance/progress-entry must be the sole append-contract template"
        )
    return len(coverage), len(template_coverage)


def _self_test(root: Path) -> int:
    raw_registry = _load_json(root / REGISTRY_PATH)
    fixture = _load_json(root / FIXTURE_PATH)
    actual_contract = tuple(
        (case.get("name"), case.get("mutation"), tuple(case.get("expected", ())))
        for case in fixture.get("cases", ())
    )
    if fixture.get("schemaVersion") != 1 or actual_contract != EXPECTED_CASES:
        print("FAIL document contract registry self-test: fixture contract mismatch")
        return 1

    for name, mutation, expected in EXPECTED_CASES:
        mutated = copy.deepcopy(raw_registry)
        _mutate(mutated, mutation)
        diagnostics = ()
        try:
            registry = validate_registry(root, mutated)
        except DocumentContractError as exc:
            diagnostics = exc.diagnostics
        else:
            diagnostics = classify_paths(registry, (SAMPLE_PATH,))
        actual = _ordered_rule_ids(diagnostics)
        if actual != expected:
            print(
                f"FAIL document contract registry self-test: {name}: "
                f"expected {list(expected)!r}, got {list(actual)!r}"
            )
            return 1

    try:
        _assert_parser_safety()
        _assert_inventory_safety(root)
        profile_count, template_count = _assert_positive_coverage(
            root, raw_registry, fixture
        )
    except (AssertionError, OSError, subprocess.SubprocessError) as exc:
        print(f"FAIL document contract registry self-test: {exc}")
        return 1

    print(
        "PASS document contract registry self-test: "
        f"9 cases, {profile_count} profiles, {template_count} templates"
    )
    return 0


def _print_diagnostic(diagnostic: Any) -> None:
    print(
        f"FAIL {diagnostic.rule_id} {diagnostic.path.as_posix()}: "
        f"expected {diagnostic.expected}; actual {diagnostic.actual}"
    )


def main() -> int:
    args = _parse_args()
    root = args.root.absolute()
    if args.self_test:
        return _self_test(root)

    try:
        registry = load_registry(root)
        if args.profile and args.profile not in {
            profile.profile_id for profile in registry.profiles
        }:
            raise ValueError(f"unknown profile: {args.profile}")
        inventory = enumerate_target_markdown(
            root, include_paths=tuple(args.include_path)
        )
    except DocumentContractError as exc:
        for diagnostic in exc.diagnostics:
            _print_diagnostic(diagnostic)
        return 1
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"FAIL document contract registry: {exc}")
        return 1

    diagnostics = classify_paths(registry, inventory.current_paths)
    uncovered_count = sum(
        diagnostic.rule_id == "REGISTRY_ROUTE_UNCOVERED"
        for diagnostic in diagnostics
    )
    ambiguous_count = sum(
        diagnostic.rule_id == "REGISTRY_ROUTE_AMBIGUOUS"
        for diagnostic in diagnostics
    )
    if diagnostics:
        for diagnostic in diagnostics:
            _print_diagnostic(diagnostic)
    print(
        f"baseline={len(inventory.baseline_paths)} "
        f"new={len(inventory.new_paths)} "
        f"uncovered={uncovered_count} ambiguous={ambiguous_count}"
    )
    if diagnostics:
        return 1

    selected_count = len(inventory.current_paths)
    if args.profile:
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
