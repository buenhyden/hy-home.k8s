#!/usr/bin/env python3
"""Run one named suite of contract regressions as a purpose gate.

Each registered gate runs one suite, so a test module runs when its product or
its own file changes instead of waiting for a blanket unit run that no lane
executes. A suite is a table row here plus one registry validator; the
affected-surface tests require every test module to belong to exactly one gate.
"""

from __future__ import annotations

import argparse
import sys
import unittest
from pathlib import Path


def _modules(*names: str) -> tuple[str, ...]:
    return tuple(f"tests.test_{name}" for name in names)


SUITES = {
    "archive": _modules(
        "archive_registry_contract",
        "archive_citation_decision",
        "archive_dispositions",
        "archive_disposition_lifecycle",
        "archive_catalog_reverification",
        "archive_reappraisal",
        "generic_migration_recovery",
        "archive_current_pin",
        "archive_disposition_routes",
        "archive_generation_fixture",
        "archive_historical_proof",
        "archive_integrity",
        "archive_recovery",
    ),
    # ponytail: about 400 s in one module; split ArchiveTransitionLinkTest out
    # if archive_validation.py edits become frequent.
    "archive-validation": _modules("archive_validation"),
    "document": _modules(
        "completed_state_migration",
        "document_lifecycle_cumulative_history",
        "task_execution_contract",
        "task_acceptance_contract",
        "task_acceptance_boundaries",
        "operations_section_contract",
        "operations_lineage_contract",
        "shared_contract_binding",
        "document_scope_selection",
        "task_summary_derivation",
        "evaluation_document_profiles",
        "readme_navigation",
        "reference_pack_routes",
        "native_skill_envelope",
        "markdown_render_cache",
        "json_schema_validation",
        "common_agents_document_routes",
        "common_agents_archive_routes",
        "document_strict_cutover",
        "document_language",
        "documentation_link_boundary",
    ),
    "document-lifecycle": _modules(
        "document_lifecycle_migration",
        "document_lifecycle_archive_cutover",
        "document_artifact_identity",
    ),
    "validation-routing": _modules(
        "validate_affected_surfaces",
        "validation_profiles",
        "affected_surface_migration",
        "run_validation_lane",
        "validation_tooling_ownership",
        "validation_bounded_io",
        "selected_style",
        "validate_selected_nonstyle",
    ),
    "qa-runner": _modules("qa_runner"),
    "ci-metadata": _modules(
        "validate_ci_python_contract",
        "validate_github_actions_security",
        "ci_branch_metadata",
    ),
    "release": _modules("release", "commit_contracts"),
    "agent-governance": _modules(
        "agent_governance",
        "agent_governance_consumers",
        "validate_agent_registry",
        "validate_agent_harness_contract",
        "validate_agent_core_cutover",
    ),
    "tooling": _modules(
        "independent_review",
        "prompt_input",
        "provider_guard_registry_generation",
        "k8s_pre_edit_hook",
        "repository_quality_rules",
        "repository_form_contracts",
        "current_executable_references",
        "workspace_boundary",
        "validate_knowledge_surface",
    ),
    "cluster-gate": _modules(
        "check_secret_handling",
        "validate_k8s_manifests",
        "validate_gitops_change_set",
        "validate_vault_eso_contracts",
        "platform_assurance",
        "platform_ingress",
        "infrastructure_tempfiles",
        "external_service_contracts",
    ),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--suite", required=True, choices=sorted(SUITES))
    arguments = parser.parse_args()

    root = arguments.root.resolve()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    modules = SUITES[arguments.suite]
    label = f"{arguments.suite} contract regressions"
    try:
        suite = unittest.defaultTestLoader.loadTestsFromNames(modules)
    except Exception as error:  # noqa: BLE001 - any load failure is a gate failure
        print(f"[FAIL] {label} are unavailable: {error}")
        return 1
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(suite)
    if not result.wasSuccessful():
        print(
            f"[FAIL] {label} failed: "
            f"tests={result.testsRun} failures={len(result.failures)} "
            f"errors={len(result.errors)}"
        )
        return 1
    print(f"[PASS] {label} passed: modules={len(modules)} tests={result.testsRun}")
    return 0


if __name__ == "__main__":  # pragma: no cover - module entry guard
    raise SystemExit(main())
