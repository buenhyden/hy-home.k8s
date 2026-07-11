#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


EXPECTED_STEMS = frozenset({
    "code-reviewer", "doc-writer", "gitops-reviewer", "incident-responder",
    "k8s-implementer", "network-reviewer", "observability-reviewer",
    "security-auditor", "supervisor", "wiki-curator",
})
REQUIRED_OWNER_LINKS = {
    "docs/00.agent-governance/rules/bootstrap.md": "rules/bootstrap.md",
    "docs/00.agent-governance/rules/persona.md": "rules/persona.md",
    "docs/00.agent-governance/rules/stage-authoring-matrix.md": "rules/stage-authoring-matrix.md",
    "docs/04.execution/tasks/2026-07-06-observability-and-network-review-agents.md": "../04.execution/tasks/2026-07-06-observability-and-network-review-agents.md",
    "docs/04.execution/tasks/2026-07-11-governance-owner-and-roster-currentness.md": "../04.execution/tasks/2026-07-11-governance-owner-and-roster-currentness.md",
    "docs/99.templates/support/documentation-contract.md": "../99.templates/support/documentation-contract.md",
    "docs/99.templates/support/template-routing.md": "../99.templates/support/template-routing.md",
}
STALE_COUNT_VARIANTS = (
    "8 local agents",
    "Eight local provider adapters",
    "eight shared roles",
    "8 role stems",
)
VALID_ROSTER_PHRASE = "Ten shared local role stems / thirty provider adapters"
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)(?:\s+[^)]*)?\)")


def missing_owner_link_error(label: str, target: str) -> str:
    return f"harness catalog missing canonical owner link: {label} -> {target}"


FIXTURE_CASE_SCHEMA = {
    "valid": {
        "mutation": "none",
        "expected_errors": frozenset(),
        "catalog_variants": None,
    },
    "missing-role": {
        "mutation": "remove-network-from-claude",
        "expected_errors": frozenset({
            "claude roster missing expected stems: network-reviewer",
            "provider adapter inventory must contain exactly 30 files",
        }),
        "catalog_variants": None,
    },
    "provider-mismatch": {
        "mutation": "add-extra-to-codex",
        "expected_errors": frozenset({
            "codex roster has unexpected stems: extra-reviewer",
            "provider adapter inventory must contain exactly 30 files",
        }),
        "catalog_variants": None,
    },
    "stale-count": {
        "mutation": "check-stale-count-variants",
        "expected_errors": frozenset({
            "harness catalog contains stale eight-role currentness prose",
        }),
        "catalog_variants": STALE_COUNT_VARIANTS,
    },
    "bad-owner": {
        "mutation": "misdirect-bootstrap-owner",
        "expected_errors": frozenset({
            missing_owner_link_error(
                "docs/00.agent-governance/rules/bootstrap.md",
                "rules/bootstrap.md",
            ),
        }),
        "catalog_variants": None,
    },
}
REQUIRED_CASE_NAMES = frozenset(FIXTURE_CASE_SCHEMA)


def normalize_markdown_label(label: str) -> str:
    stripped = label.strip()
    code_label = re.fullmatch(r"`([^`]*)`", stripped)
    return code_label.group(1) if code_label else stripped


def validate_contract(
    provider_stems: dict[str, set[str]], catalog_text: str
) -> list[str]:
    errors: list[str] = []
    for provider in ("claude", "codex", "gemini"):
        stems = provider_stems[provider]
        missing = sorted(EXPECTED_STEMS - stems)
        extra = sorted(stems - EXPECTED_STEMS)
        if missing:
            errors.append(f"{provider} roster missing expected stems: {', '.join(missing)}")
        if extra:
            errors.append(f"{provider} roster has unexpected stems: {', '.join(extra)}")
    if sum(len(stems) for stems in provider_stems.values()) != 30:
        errors.append("provider adapter inventory must contain exactly 30 files")
    if re.search(
        r"\b(?:8|eight)\s+(?:local\s+|shared\s+)?"
        r"(?:provider adapters|agents|roles|role stems)\b",
        catalog_text,
        re.IGNORECASE,
    ):
        errors.append("harness catalog contains stale eight-role currentness prose")
    catalog_links = {
        (normalize_markdown_label(label), target)
        for label, target in MARKDOWN_LINK_RE.findall(catalog_text)
    }
    for label, target in REQUIRED_OWNER_LINKS.items():
        if (label, target) not in catalog_links:
            errors.append(missing_owner_link_error(label, target))
    return errors


def repository_inputs(root: Path) -> tuple[dict[str, set[str]], str]:
    providers = {
        "claude": {path.stem for path in (root / ".claude/agents").glob("*.md")},
        "codex": {path.stem for path in (root / ".codex/agents").glob("*.toml")},
        "gemini": {path.stem for path in (root / ".agents/agents").glob("*.md")},
    }
    catalog = (root / "docs/00.agent-governance/harness-catalog.md").read_text(
        encoding="utf-8"
    )
    return providers, catalog


def run_self_test(fixture_path: Path) -> list[str]:
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    failures: list[str] = []
    if frozenset(data["expected_stems"]) != EXPECTED_STEMS:
        failures.append("fixture expected_stems does not match EXPECTED_STEMS")
    cases = data["cases"]
    case_names = [case["name"] for case in cases]
    if len(case_names) != len(REQUIRED_CASE_NAMES) or set(case_names) != REQUIRED_CASE_NAMES:
        failures.append(
            "fixture case names must be exactly: "
            + ", ".join(sorted(REQUIRED_CASE_NAMES))
        )
        return failures
    for case in cases:
        case_name = case["name"]
        schema = FIXTURE_CASE_SCHEMA[case_name]
        schema_errors: list[str] = []
        if case.get("mutation") != schema["mutation"]:
            schema_errors.append(
                f"mutation must be {schema['mutation']!r}, got "
                f"{case.get('mutation')!r}"
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
    base_catalog = VALID_ROSTER_PHRASE + "\n" + "\n".join(
        f"[`{label}`]({target})" for label, target in REQUIRED_OWNER_LINKS.items()
    )
    probe_providers = {
        name: set(EXPECTED_STEMS) for name in ("claude", "codex", "gemini")
    }
    image_catalog = VALID_ROSTER_PHRASE + "\n" + "\n".join(
        f"![`{label}`]({target})" for label, target in REQUIRED_OWNER_LINKS.items()
    )
    image_errors = set(validate_contract(probe_providers, image_catalog))
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
        probe_errors = set(validate_contract(probe_providers, probe_catalog))
        if probe_errors != expected_bootstrap_error:
            failures.append(
                f"bootstrap owner-link {probe_name} probe: expected exact errors "
                f"{sorted(expected_bootstrap_error)!r}, got {sorted(probe_errors)!r}"
            )
    for case in cases:
        providers = {name: set(EXPECTED_STEMS) for name in ("claude", "codex", "gemini")}
        catalog = base_catalog
        mutation = case["mutation"]
        if mutation == "remove-network-from-claude":
            providers["claude"].remove("network-reviewer")
        elif mutation == "add-extra-to-codex":
            providers["codex"].add("extra-reviewer")
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
                    providers,
                    catalog.replace(VALID_ROSTER_PHRASE, variant, 1),
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
        elif mutation != "none":
            failures.append(f"{case['name']}: unknown mutation {mutation}")
            continue
        errors = validate_contract(providers, catalog)
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
        if args.self_test:
            errors = run_self_test(
                args.repo_root / "tests/fixtures/agent-roster-currentness.json"
            )
        else:
            providers, catalog = repository_inputs(args.repo_root)
            errors = validate_contract(providers, catalog)
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
