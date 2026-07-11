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
    profile = raw_registry["profiles"][0]
    route = profile["routes"][0]
    if mutation == "none":
        return
    if mutation == "duplicate-profile-id":
        raw_registry["profiles"].append(copy.deepcopy(profile))
        return
    if mutation == "route-kind-glob":
        route["kind"] = "glob"
        return
    if mutation == "drop-regex-end-anchor":
        route["value"] = route["value"].removesuffix("$")
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
    except (AssertionError, OSError, subprocess.SubprocessError) as exc:
        print(f"FAIL document contract registry self-test: inventory safety: {exc}")
        return 1

    print("PASS document contract registry self-test: 9 cases")
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
