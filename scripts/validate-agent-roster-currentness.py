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
REQUIRED_OWNER_POINTERS = (
    "docs/00.agent-governance/rules/bootstrap.md",
    "docs/00.agent-governance/rules/persona.md",
    "docs/00.agent-governance/rules/stage-authoring-matrix.md",
    "docs/04.execution/tasks/2026-07-06-observability-and-network-review-agents.md",
    "docs/04.execution/tasks/2026-07-11-governance-owner-and-roster-currentness.md",
    "docs/99.templates/support/documentation-contract.md",
    "docs/99.templates/support/template-routing.md",
)


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
    if re.search(r"\b(?:Eight|eight) (?:local )?(?:provider adapters|agents)\b", catalog_text):
        errors.append("harness catalog contains stale eight-role currentness prose")
    for pointer in REQUIRED_OWNER_POINTERS:
        if pointer not in catalog_text:
            errors.append(f"harness catalog missing canonical owner pointer: {pointer}")
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
    base_catalog = "Ten local provider adapters\n" + "\n".join(
        REQUIRED_OWNER_POINTERS
    )
    for case in data["cases"]:
        providers = {name: set(EXPECTED_STEMS) for name in ("claude", "codex", "gemini")}
        catalog = base_catalog
        mutation = case["mutation"]
        if mutation == "remove-network-from-claude":
            providers["claude"].remove("network-reviewer")
        elif mutation == "add-extra-to-codex":
            providers["codex"].add("extra-reviewer")
        elif mutation == "replace-ten-with-eight":
            catalog = catalog.replace("Ten local", "Eight local", 1)
        elif mutation == "remove-bootstrap-owner":
            catalog = catalog.replace(
                "docs/00.agent-governance/rules/bootstrap.md", "", 1
            )
        elif mutation != "none":
            failures.append(f"{case['name']}: unknown mutation {mutation}")
            continue
        errors = validate_contract(providers, catalog)
        expected = case["expected_error"]
        if expected is None and errors:
            failures.append(f"{case['name']}: expected no errors, got {errors}")
        elif expected is not None and expected not in errors:
            failures.append(f"{case['name']}: missing expected error {expected!r}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        errors = run_self_test(
            args.repo_root / "tests/fixtures/agent-roster-currentness.json"
        )
    else:
        providers, catalog = repository_inputs(args.repo_root)
        errors = validate_contract(providers, catalog)
    if errors:
        for error in errors:
            print(f"ERR {error}", file=sys.stderr)
        return 1
    print("[PASS] agent roster currentness validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
