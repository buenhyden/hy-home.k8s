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
REQUIRED_CASE_NAMES = frozenset({
    "valid", "missing-role", "provider-mismatch", "stale-count", "bad-owner",
})
STALE_COUNT_VARIANTS = (
    "8 local agents",
    "Eight local provider adapters",
    "eight shared roles",
    "8 role stems",
)
VALID_ROSTER_PHRASE = "Ten shared local role stems / thirty provider adapters"
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+[^)]*)?\)")


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
        (label.strip().removeprefix("`").removesuffix("`"), target)
        for label, target in MARKDOWN_LINK_RE.findall(catalog_text)
    }
    for label, target in REQUIRED_OWNER_LINKS.items():
        if (label, target) not in catalog_links:
            errors.append(
                f"harness catalog missing canonical owner link: {label} -> {target}"
            )
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
    base_catalog = VALID_ROSTER_PHRASE + "\n" + "\n".join(
        f"[`{label}`]({target})" for label, target in REQUIRED_OWNER_LINKS.items()
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
