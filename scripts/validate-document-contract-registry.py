#!/usr/bin/env python3
"""Validate the document-profile registry and its deterministic routing."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

from document_contracts import (
    BASELINE_COUNT,
    BASELINE_SHA,
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


SAMPLE_PATH = PurePosixPath(".agents/GEMINI.md")
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

DOCUMENT_PROFILE_CONTRACT_V1 = {
    "name": "DocumentProfileContract.v1",
    "profile_ids": (
        "content/archive-tombstone",
        "content/reference",
        "exception/generated-record",
        "exception/github-native-control",
        "exception/native-contract",
        "exception/program-non-target",
        "exception/provider-native-metadata",
        "exception/root-provider-shim",
        "governance/memory",
        "governance/progress-entry",
        "governance/progress-ledger",
        "governance/reference",
        "governance/template-support",
        "readme/collection-index",
        "readme/implementation",
        "readme/repository",
        "readme/snapshot-pack",
        "readme/stage-index",
        "readme/workspace-staging",
        "sdlc/adr",
        "sdlc/agent-design",
        "sdlc/api-spec",
        "sdlc/ard",
        "sdlc/data-model",
        "sdlc/guide",
        "sdlc/incident",
        "sdlc/plan",
        "sdlc/policy",
        "sdlc/postmortem",
        "sdlc/prd",
        "sdlc/runbook",
        "sdlc/spec",
        "sdlc/task",
        "sdlc/tests",
        "template/content/archive-tombstone",
        "template/content/reference",
        "template/governance/memory",
        "template/readme/common",
        "template/sdlc/adr",
        "template/sdlc/agent-design",
        "template/sdlc/api-spec",
        "template/sdlc/ard",
        "template/sdlc/data-model",
        "template/sdlc/guide",
        "template/sdlc/incident",
        "template/sdlc/plan",
        "template/sdlc/policy",
        "template/sdlc/postmortem",
        "template/sdlc/prd",
        "template/sdlc/runbook",
        "template/sdlc/spec",
        "template/sdlc/task",
        "template/sdlc/task-legacy-harness",
        "template/sdlc/tests",
    ),
    "semantic_sha256": (
        "0d15439c97695d6b833bc1b2f94760b82ae9c95f39fa8e7e30886dc3967d19b2"  # pragma: allowlist secret
    ),
}
DOCUMENT_PROFILE_CONTRACT_V1_FIELDS = (
    "id",
    "class",
    "mode",
    "frontmatter",
    "statusDomain",
    "headings",
    "template",
    "routes",
    "sourceProfileIds",
    "placeholderPolicy",
    "appendContract",
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


def _document_profile_contract_projection(
    raw_registry: dict[str, Any],
) -> list[dict[str, Any]]:
    projection: list[dict[str, Any]] = []
    for profile in sorted(raw_registry["profiles"], key=lambda item: item["id"]):
        row = {
            field: copy.deepcopy(profile[field])
            for field in DOCUMENT_PROFILE_CONTRACT_V1_FIELDS
        }
        row["routes"] = sorted(
            row["routes"], key=lambda route: (route["kind"], route["value"])
        )
        projection.append(row)
    return projection


def _assert_document_profile_contract(raw_registry: dict[str, Any]) -> int:
    expected_ids = DOCUMENT_PROFILE_CONTRACT_V1["profile_ids"]
    actual_ids = tuple(sorted(profile["id"] for profile in raw_registry["profiles"]))
    if actual_ids != expected_ids:
        missing = sorted(set(expected_ids) - set(actual_ids))
        extra = sorted(set(actual_ids) - set(expected_ids))
        raise AssertionError(
            "DocumentProfileContract.v1 ID mismatch: "
            f"missing={missing!r} extra={extra!r}"
        )

    canonical = json.dumps(
        _document_profile_contract_projection(raw_registry),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    actual_digest = hashlib.sha256(canonical).hexdigest()
    expected_digest = DOCUMENT_PROFILE_CONTRACT_V1["semantic_sha256"]
    if actual_digest != expected_digest:
        raise AssertionError(
            "DocumentProfileContract.v1 semantic digest mismatch: "
            f"expected={expected_digest} actual={actual_digest}"
        )
    return len(actual_ids)


def _assert_document_profile_contract_mutation_proof(
    raw_registry: dict[str, Any],
) -> None:
    mutations = (
        ("placeholder policy", "placeholderPolicy", "template-only"),
        (
            "authored template",
            "template",
            "docs/99.templates/templates/sdlc/specs/spec.template.md",
        ),
    )
    for label, field, value in mutations:
        mutated = copy.deepcopy(raw_registry)
        profile = next(
            profile
            for profile in mutated["profiles"]
            if profile["id"] == "sdlc/prd"
        )
        profile[field] = value
        try:
            _assert_document_profile_contract(mutated)
        except AssertionError as exc:
            if "semantic digest mismatch" not in str(exc):
                raise AssertionError(
                    "DocumentProfileContract.v1 "
                    f"{label} mutation proof failed unexpectedly"
                ) from exc
        else:
            raise AssertionError(
                "DocumentProfileContract.v1 accepted a "
                f"{label} semantic mutation"
            )


def _minimal_fixture_registry() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://hy-home.k8s/schemas/document-profiles-1.schema.json",
        "schemaVersion": 1,
        "baseline": {"sha": BASELINE_SHA, "count": BASELINE_COUNT},
        "target": {"roots": [".agents"], "rootFiles": ["README.md"]},
        "profiles": [
            {
                "id": "test/sample",
                "class": "exception",
                "mode": "native",
                "routes": [
                    {"kind": "exact", "value": SAMPLE_PATH.as_posix()},
                    {
                        "kind": "regex",
                        "value": (
                            "^tests/fixtures/document-contracts/"
                            "self-test-.+\\.md$"
                        ),
                    },
                ],
                "frontmatter": {
                    "mode": "not-applicable",
                    "required": [],
                    "allowed": [],
                    "order": [],
                },
                "statusDomain": [],
                "headings": {"required": [], "allowed": []},
                "template": None,
                "sourceProfileIds": [],
                "placeholderPolicy": "forbidden",
                "appendContract": None,
            }
        ],
        "programLineage": {
            "prd": "005",
            "ard": "0008",
            "specs": ["026"],
        },
    }


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


def _assert_role_specific_spec_routes(registry: Any) -> None:
    probes = {
        PurePosixPath("examples/aws/docs/03.specs/contract-probe/spec.md"): "sdlc/spec",
        PurePosixPath(
            "examples/aws/docs/03.specs/contract-probe/api-spec.md"
        ): "sdlc/api-spec",
        PurePosixPath(
            "examples/azure/docs/03.specs/contract-probe/agent-design.md"
        ): "sdlc/agent-design",
        PurePosixPath(
            "examples/azure/docs/03.specs/contract-probe/data-model.md"
        ): "sdlc/data-model",
        PurePosixPath(
            "examples/azure/docs/03.specs/contract-probe/tests.md"
        ): "sdlc/tests",
        PurePosixPath(
            "examples/azure/docs/03.specs/2026-03-31-resource-specs.md"
        ): "sdlc/spec",
    }
    for path, expected_profile in probes.items():
        actual_profile = classify_path(registry, path).profile_id
        if actual_profile != expected_profile:
            raise AssertionError(
                f"{path}: expected role-specific profile {expected_profile!r}, "
                f"got {actual_profile!r}"
            )


def _assert_tracked_negative_fixture_sample(root: Path, registry: Any) -> None:
    completed = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "--", SAMPLE_PATH.as_posix()],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.stdout.strip() != SAMPLE_PATH.as_posix():
        raise AssertionError("negative fixture sample must be one exact tracked path")
    actual_profile = classify_path(registry, SAMPLE_PATH).profile_id
    if actual_profile != "exception/provider-native-metadata":
        raise AssertionError(
            f"{SAMPLE_PATH}: expected provider metadata, got {actual_profile!r}"
        )


def _assert_positive_coverage(
    root: Path, raw_registry: dict[str, Any], fixture: dict[str, Any]
) -> tuple[int, int]:
    registry = validate_registry(root, raw_registry)
    profiles = {profile.profile_id: profile for profile in registry.profiles}
    _assert_role_specific_spec_routes(registry)
    _assert_tracked_negative_fixture_sample(root, registry)

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
    try:
        contract_profile_count = _assert_document_profile_contract(raw_registry)
        _assert_document_profile_contract_mutation_proof(raw_registry)
    except (AssertionError, KeyError, TypeError) as exc:
        print(f"FAIL document contract registry self-test: {exc}")
        return 1

    fixture = _load_json(root / FIXTURE_PATH)
    actual_contract = tuple(
        (case.get("name"), case.get("mutation"), tuple(case.get("expected", ())))
        for case in fixture.get("cases", ())
    )
    if (
        fixture.get("schemaVersion") != 1
        or fixture.get("negativeFixtureSamplePath") != SAMPLE_PATH.as_posix()
        or actual_contract != EXPECTED_CASES
    ):
        print("FAIL document contract registry self-test: fixture contract mismatch")
        return 1

    for name, mutation, expected in EXPECTED_CASES:
        mutated = _minimal_fixture_registry()
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
        if profile_count != contract_profile_count:
            raise AssertionError(
                "profileCoverage count differs from DocumentProfileContract.v1"
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
