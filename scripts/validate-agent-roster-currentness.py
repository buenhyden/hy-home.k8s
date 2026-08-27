#!/usr/bin/env python3
import argparse
import json
import os
import re
import stat
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any


HARNESS_CONTRACT_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/harness-contract.json"
)
FIXTURE_PATH = PurePosixPath("tests/fixtures/agent-roster-currentness.json")
CONTRACT_VERSION = "1.0.0"
CONSUMER_ID = "roster-currentness-validator"
ALLOWED_EXTENSIONS = frozenset({".md", ".toml"})
REQUIRED_OWNER_LINKS = {
    "docs/00.agent-governance/rules/bootstrap.md": "rules/bootstrap.md",
    "docs/00.agent-governance/rules/persona.md": "rules/persona.md",
    "docs/00.agent-governance/rules/document-authoring.md": "rules/document-authoring.md",
    "docs/03.specs/0024-observability-and-network-review-agents/README.md": "../03.specs/0024-observability-and-network-review-agents/README.md",
    "docs/03.specs/0025-governance-owner-and-roster-currentness/README.md": "../03.specs/0025-governance-owner-and-roster-currentness/README.md",
    "docs/99.templates/README.md": "../99.templates/README.md",
}
STALE_COUNT_VARIANTS = (
    "8 local agents",
    "Eight local role adapters",
    "eight shared roles",
    "8 role stems",
    "10 local agents",
    "Ten local role adapters",
    "ten shared roles",
    "10 role stems",
    "3 surfaces",
    "30 adapters",
)
VALID_ROSTER_PHRASE = (
    "Twelve shared local role stems / forty-eight tracked role adapters"
)
VALID_ROSTER_PHRASE_ERROR = (
    "harness catalog canonical roster phrase must appear exactly once"
)
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)(?:\s+[^)]*)?\)")


@dataclass(frozen=True)
class HarnessRoster:
    role_ids: tuple[str, ...]
    surface_ids: tuple[str, ...]
    locations: dict[str, tuple[PurePosixPath, str]]
    projection_paths: frozenset[PurePosixPath]


def missing_owner_link_error(label: str, target: str) -> str:
    return f"harness catalog missing canonical owner link: {label} -> {target}"


def duplicate_owner_link_error(label: str, target: str) -> str:
    return (
        "harness catalog canonical owner link must appear exactly once: "
        f"{label} -> {target}"
    )


REQUIRED_CASE_NAMES = frozenset(
    {
        "valid",
        "missing-role",
        "surface-mismatch",
        "stale-count",
        "bad-owner",
        "duplicate-owner",
        "missing-current-phrase",
    }
)


def normalize_markdown_label(label: str) -> str:
    stripped = label.strip()
    code_label = re.fullmatch(r"`([^`]*)`", stripped)
    return code_label.group(1) if code_label else stripped


def load_harness_contract(root: Path) -> dict[str, Any]:
    contract_path = safe_repo_path(
        root,
        HARNESS_CONTRACT_PATH,
        final_kind="file",
    )
    value = json.loads(contract_path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("harness contract root must be an object")
    return value


def safe_relative_root(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if (
        not value
        or path.is_absolute()
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise ValueError(f"unsafe surface path root: {value!r}")
    return path


def safe_repo_path(
    root: Path,
    relative: PurePosixPath | str,
    *,
    final_kind: str,
) -> Path:
    raw = relative.as_posix() if isinstance(relative, PurePosixPath) else relative
    candidate_relative = PurePosixPath(raw)
    segments = raw.split("/")
    if (
        candidate_relative.is_absolute()
        or not segments
        or any(segment in {"", ".", ".."} for segment in segments)
    ):
        raise ValueError(f"{raw}: expected a normalized repository-relative path")
    try:
        absolute_root = root.absolute()
        root_mode = os.lstat(absolute_root).st_mode
    except OSError as exc:
        raise ValueError(f"repository root: {exc}") from exc
    if stat.S_ISLNK(root_mode) or not stat.S_ISDIR(root_mode):
        raise ValueError("repository root must be a non-symlink directory")
    strict_root = absolute_root.resolve(strict=True)
    candidate = strict_root
    for index, segment in enumerate(segments):
        candidate = candidate / segment
        try:
            mode = os.lstat(candidate).st_mode
        except OSError as exc:
            raise ValueError(f"{raw}: {exc}") from exc
        if stat.S_ISLNK(mode):
            raise ValueError(f"{raw}: symlink path component {segment!r} is forbidden")
        is_final = index == len(segments) - 1
        if not is_final and not stat.S_ISDIR(mode):
            raise ValueError(f"{raw}: parent component {segment!r} is not a directory")
        if is_final:
            expected = (
                stat.S_ISREG(mode) if final_kind == "file" else stat.S_ISDIR(mode)
            )
            if not expected:
                raise ValueError(f"{raw}: expected a regular non-symlink {final_kind}")
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(strict_root)
    except (OSError, ValueError) as exc:
        raise ValueError(
            f"{raw}: resolved path escapes the repository root: {exc}"
        ) from exc
    return resolved


def select_current_harness(contract: dict[str, Any]) -> HarnessRoster:
    """Select current roster and path layout from harness-contract/1.0.0."""

    if contract.get("contractVersion") != CONTRACT_VERSION:
        raise ValueError("harness contract version differs")
    consumers = contract.get("consumers")
    if not isinstance(consumers, list):
        raise ValueError("harness consumers must be a list")
    selected = [
        consumer
        for consumer in consumers
        if isinstance(consumer, dict) and consumer.get("id") == CONSUMER_ID
    ]
    if len(selected) != 1 or (
        selected[0].get("selectedContract"),
        selected[0].get("selectedVersion"),
        selected[0].get("migrationState"),
    ) != ("harness-contract", CONTRACT_VERSION, "current"):
        raise ValueError("roster validator must select harness-contract/1.0.0/current")

    inventory = contract.get("currentInventory")
    if not isinstance(inventory, dict) or inventory.get("state") != "current":
        raise ValueError("currentInventory must be a current object")
    role_ids = tuple(inventory.get("roleIds", ()))
    surface_ids = tuple(inventory.get("surfaceIds", ()))
    if (
        not role_ids
        or not surface_ids
        or not all(isinstance(item, str) for item in (*role_ids, *surface_ids))
        or len(role_ids) != len(set(role_ids))
        or len(surface_ids) != len(set(surface_ids))
    ):
        raise ValueError("current role and surface identities differ")
    expected_count = len(role_ids) * len(surface_ids)
    if (
        inventory.get("expectedRoleCount"),
        inventory.get("expectedSurfaceCount"),
        inventory.get("expectedProjectionCount"),
    ) != (len(role_ids), len(surface_ids), expected_count):
        raise ValueError("current inventory counts differ")

    surfaces = contract.get("surfaces")
    if not isinstance(surfaces, list):
        raise ValueError("surfaces must be a list")
    surface_by_id = {
        surface.get("id"): surface
        for surface in surfaces
        if isinstance(surface, dict) and isinstance(surface.get("id"), str)
    }
    locations: dict[str, tuple[PurePosixPath, str]] = {}
    for surface_id in surface_ids:
        surface = surface_by_id.get(surface_id)
        if not isinstance(surface, dict) or surface.get("admissionState") != "current":
            raise ValueError(f"{surface_id} is not a current surface")
        path_root = surface.get("pathRoot")
        extension = surface.get("extension")
        if (
            not isinstance(path_root, str)
            or not isinstance(extension, str)
            or extension not in ALLOWED_EXTENSIONS
        ):
            raise ValueError(f"{surface_id} location differs")
        locations[surface_id] = (safe_relative_root(path_root), extension)

    expected_paths = {
        (
            role_id,
            surface_id,
            locations[surface_id][0] / f"{role_id}{locations[surface_id][1]}",
        )
        for role_id in role_ids
        for surface_id in surface_ids
    }
    projections = inventory.get("projections")
    if not isinstance(projections, list):
        raise ValueError("current projections must be a list")
    actual_paths = {
        (
            projection.get("roleId"),
            projection.get("surfaceId"),
            PurePosixPath(projection["path"]),
        )
        for projection in projections
        if isinstance(projection, dict)
        and isinstance(projection.get("path"), str)
        and projection.get("admissionState") == "current"
    }
    if actual_paths != expected_paths or len(projections) != expected_count:
        raise ValueError("current projection layout differs")
    return HarnessRoster(
        role_ids=role_ids,
        surface_ids=surface_ids,
        locations=locations,
        projection_paths=frozenset(path for _role, _surface, path in actual_paths),
    )


def fixture_case_schema(roster: HarnessRoster) -> dict[str, dict[str, Any]]:
    inventory_error = (
        "role adapter inventory must contain exactly "
        f"{len(roster.projection_paths)} files"
    )
    return {
        "valid": {
            "mutation": "none",
            "expected_errors": frozenset(),
            "catalog_variants": None,
        },
        "missing-role": {
            "mutation": "remove-network-from-claude",
            "expected_errors": frozenset(
                {
                    "claude roster missing expected stems: network-reviewer",
                    inventory_error,
                }
            ),
            "catalog_variants": None,
        },
        "surface-mismatch": {
            "mutation": "add-extra-to-codex",
            "expected_errors": frozenset(
                {
                    "codex roster has unexpected stems: extra-reviewer",
                    inventory_error,
                }
            ),
            "catalog_variants": None,
        },
        "stale-count": {
            "mutation": "check-stale-count-variants",
            "expected_errors": frozenset(
                {
                    "harness catalog contains stale pre-12-role currentness prose",
                }
            ),
            "catalog_variants": STALE_COUNT_VARIANTS,
        },
        "bad-owner": {
            "mutation": "misdirect-bootstrap-owner",
            "expected_errors": frozenset(
                {
                    missing_owner_link_error(
                        "docs/00.agent-governance/rules/bootstrap.md",
                        "rules/bootstrap.md",
                    ),
                }
            ),
            "catalog_variants": None,
        },
        "duplicate-owner": {
            "mutation": "duplicate-document-authoring-owner",
            "expected_errors": frozenset(
                {
                    duplicate_owner_link_error(
                        "docs/00.agent-governance/rules/document-authoring.md",
                        "rules/document-authoring.md",
                    ),
                }
            ),
            "catalog_variants": None,
        },
        "missing-current-phrase": {
            "mutation": "remove-current-roster-phrase",
            "expected_errors": frozenset({VALID_ROSTER_PHRASE_ERROR}),
            "catalog_variants": None,
        },
    }


def validate_contract(
    surface_stems: dict[str, set[str]],
    catalog_text: str,
    roster: HarnessRoster,
) -> list[str]:
    errors: list[str] = []
    expected_stems = set(roster.role_ids)
    for surface in roster.surface_ids:
        stems = surface_stems[surface]
        missing = sorted(expected_stems - stems)
        extra = sorted(stems - expected_stems)
        if missing:
            errors.append(
                f"{surface} roster missing expected stems: {', '.join(missing)}"
            )
        if extra:
            errors.append(f"{surface} roster has unexpected stems: {', '.join(extra)}")
    expected_projection_count = len(roster.projection_paths)
    if sum(len(stems) for stems in surface_stems.values()) != expected_projection_count:
        errors.append(
            "role adapter inventory must contain exactly "
            f"{expected_projection_count} files"
        )
    if re.search(
        r"\b(?:(?:8|eight|10|ten)\s+(?:local\s+|shared\s+)?"
        r"(?:provider adapters|role adapters|agents|roles|role stems)"
        r"|3\s+surfaces|30\s+adapters)\b",
        catalog_text,
        re.IGNORECASE,
    ):
        errors.append("harness catalog contains stale pre-12-role currentness prose")
    if catalog_text.count(VALID_ROSTER_PHRASE) != 1:
        errors.append(VALID_ROSTER_PHRASE_ERROR)
    catalog_links = [
        (normalize_markdown_label(label), target)
        for label, target in MARKDOWN_LINK_RE.findall(catalog_text)
    ]
    for label, target in REQUIRED_OWNER_LINKS.items():
        link_count = catalog_links.count((label, target))
        if link_count == 0:
            errors.append(missing_owner_link_error(label, target))
        elif link_count > 1:
            errors.append(duplicate_owner_link_error(label, target))
    return errors


def repository_inputs(
    root: Path, roster: HarnessRoster
) -> tuple[dict[str, set[str]], str]:
    surfaces = {
        surface_id: {
            path.stem
            for path in safe_repo_path(
                root,
                path_root,
                final_kind="directory",
            ).glob(f"*{extension}")
            if not path.is_symlink() and path.is_file()
        }
        for surface_id, (path_root, extension) in roster.locations.items()
    }
    catalog = safe_repo_path(
        root,
        "docs/00.agent-governance/harness-catalog.md",
        final_kind="file",
    ).read_text(encoding="utf-8")
    return surfaces, catalog


def run_self_test(root: Path, roster: HarnessRoster) -> list[str]:
    fixture_path = safe_repo_path(
        root,
        FIXTURE_PATH,
        final_kind="file",
    )
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    failures: list[str] = []
    expected_stems = frozenset(roster.role_ids)
    if frozenset(data["expected_stems"]) != expected_stems:
        failures.append("fixture expected_stems does not match harness current roleIds")
    fixture_owner_links = data.get("expected_owner_links")
    if not isinstance(fixture_owner_links, dict) or not all(
        isinstance(label, str) and isinstance(target, str)
        for label, target in fixture_owner_links.items()
    ):
        failures.append("fixture expected_owner_links must be a string map")
    elif fixture_owner_links != REQUIRED_OWNER_LINKS:
        failures.append(
            "fixture expected_owner_links does not match required canonical owner links"
        )
    cases = data["cases"]
    case_schema = fixture_case_schema(roster)
    case_names = [case["name"] for case in cases]
    if (
        len(case_names) != len(REQUIRED_CASE_NAMES)
        or set(case_names) != REQUIRED_CASE_NAMES
    ):
        failures.append(
            "fixture case names must be exactly: "
            + ", ".join(sorted(REQUIRED_CASE_NAMES))
        )
        return failures
    for case in cases:
        case_name = case["name"]
        schema = case_schema[case_name]
        schema_errors: list[str] = []
        if case.get("mutation") != schema["mutation"]:
            schema_errors.append(
                f"mutation must be {schema['mutation']!r}, got {case.get('mutation')!r}"
            )
        fixture_expected_errors = case.get("expected_errors")
        if not isinstance(fixture_expected_errors, list) or not all(
            isinstance(error, str) for error in fixture_expected_errors
        ):
            fixture_error_set = None
        else:
            fixture_error_set = frozenset(fixture_expected_errors)
        if fixture_error_set != schema["expected_errors"]:
            schema_errors.append(
                "expected_errors must be exactly "
                f"{sorted(schema['expected_errors'])!r}, got "
                f"{fixture_expected_errors!r}"
            )
        fixture_variants = case.get("catalog_variants")
        schema_variants = schema["catalog_variants"]
        expected_variants = list(schema_variants) if schema_variants else None
        if fixture_variants != expected_variants:
            schema_errors.append(
                f"catalog_variants must be {expected_variants!r}, got "
                f"{fixture_variants!r}"
            )
        if schema_errors:
            failures.append(
                f"{case_name}: fixture schema mismatch: " + "; ".join(schema_errors)
            )
    if failures:
        return failures
    base_catalog = (
        VALID_ROSTER_PHRASE
        + "\n"
        + "\n".join(
            f"[`{label}`]({target})" for label, target in REQUIRED_OWNER_LINKS.items()
        )
    )
    probe_surfaces = {name: set(expected_stems) for name in roster.surface_ids}
    image_catalog = (
        VALID_ROSTER_PHRASE
        + "\n"
        + "\n".join(
            f"![`{label}`]({target})" for label, target in REQUIRED_OWNER_LINKS.items()
        )
    )
    image_errors = set(validate_contract(probe_surfaces, image_catalog, roster))
    expected_image_errors = {
        missing_owner_link_error(label, target)
        for label, target in REQUIRED_OWNER_LINKS.items()
    }
    if image_errors != expected_image_errors:
        failures.append(
            "owner-link image syntax probe: expected exact errors "
            f"{sorted(expected_image_errors)!r}, got {sorted(image_errors)!r}"
        )
    bootstrap_label = "docs/00.agent-governance/rules/bootstrap.md"
    bootstrap_target = REQUIRED_OWNER_LINKS[bootstrap_label]
    valid_bootstrap_link = f"[`{bootstrap_label}`]({bootstrap_target})"
    expected_bootstrap_error = {
        missing_owner_link_error(bootstrap_label, bootstrap_target)
    }
    for probe_name, malformed_link in (
        ("leading backtick", f"[`{bootstrap_label}]({bootstrap_target})"),
        ("trailing backtick", f"[{bootstrap_label}`]({bootstrap_target})"),
    ):
        probe_catalog = base_catalog.replace(valid_bootstrap_link, malformed_link, 1)
        probe_errors = set(validate_contract(probe_surfaces, probe_catalog, roster))
        if probe_errors != expected_bootstrap_error:
            failures.append(
                f"bootstrap owner-link {probe_name} probe: expected exact errors "
                f"{sorted(expected_bootstrap_error)!r}, got {sorted(probe_errors)!r}"
            )
    duplicate_phrase_errors = set(
        validate_contract(
            probe_surfaces,
            f"{VALID_ROSTER_PHRASE}\n{base_catalog}",
            roster,
        )
    )
    if duplicate_phrase_errors != {VALID_ROSTER_PHRASE_ERROR}:
        failures.append(
            "duplicate canonical roster phrase probe: expected exact errors "
            f"{[VALID_ROSTER_PHRASE_ERROR]!r}, got "
            f"{sorted(duplicate_phrase_errors)!r}"
        )
    for case in cases:
        surfaces = {name: set(expected_stems) for name in roster.surface_ids}
        catalog = base_catalog
        mutation = case["mutation"]
        if mutation == "remove-network-from-claude":
            surfaces["claude"].remove("network-reviewer")
        elif mutation == "add-extra-to-codex":
            surfaces["codex"].add("extra-reviewer")
        elif mutation == "check-stale-count-variants":
            variants = case["catalog_variants"]
            if variants != list(STALE_COUNT_VARIANTS):
                failures.append(
                    f"{case['name']}: catalog_variants must be exactly "
                    f"{list(STALE_COUNT_VARIANTS)!r}"
                )
            expected = set(case["expected_errors"])
            for variant in variants:
                errors = validate_contract(
                    surfaces,
                    f"{catalog}\n{variant}",
                    roster,
                )
                if set(errors) != expected:
                    failures.append(
                        f"{case['name']} ({variant}): expected exact errors "
                        f"{sorted(expected)!r}, got {sorted(set(errors))!r}"
                    )
            continue
        elif mutation == "misdirect-bootstrap-owner":
            catalog = catalog.replace(
                "[`docs/00.agent-governance/rules/bootstrap.md`](rules/bootstrap.md)",
                "[`docs/00.agent-governance/rules/bootstrap.md`](rules/persona.md)",
                1,
            )
        elif mutation == "duplicate-document-authoring-owner":
            label = "docs/00.agent-governance/rules/document-authoring.md"
            target = "rules/document-authoring.md"
            catalog = f"{catalog}\n[`{label}`]({target})"
        elif mutation == "remove-current-roster-phrase":
            catalog = catalog.replace(
                VALID_ROSTER_PHRASE,
                "Current roster phrase intentionally removed by fixture",
                1,
            )
        elif mutation != "none":
            failures.append(f"{case['name']}: unknown mutation {mutation}")
            continue
        errors = validate_contract(surfaces, catalog, roster)
        expected = set(case["expected_errors"])
        if set(errors) != expected:
            failures.append(
                f"{case['name']}: expected exact errors {sorted(expected)!r}, "
                f"got {sorted(set(errors))!r}"
            )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        roster = select_current_harness(load_harness_contract(args.repo_root))
        if args.self_test:
            errors = run_self_test(args.repo_root, roster)
        else:
            surfaces, catalog = repository_inputs(args.repo_root, roster)
            errors = validate_contract(surfaces, catalog, roster)
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"ERR agent roster currentness input error: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERR {error}", file=sys.stderr)
        return 1
    print("[PASS] agent roster currentness validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
