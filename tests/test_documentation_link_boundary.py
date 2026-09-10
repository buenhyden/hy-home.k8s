#!/usr/bin/env python3
"""Focused contract tests for the outside-docs stage link boundary."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate-links-and-owners.py"
SCRIPTS = str(SCRIPT.parent)
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

SPEC = importlib.util.spec_from_file_location("stage_boundary_validator", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("link validator is unavailable")
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


CONSUMER = PurePosixPath("scripts/README.md")
PROFILE = "common/readme-implementation"
HUB = PurePosixPath("docs/README.md")


def _report(source: PurePosixPath, target: str):
    return validator._stage_boundary_diagnostic(source, PROFILE, PurePosixPath(target))


def _archive(source: PurePosixPath, target: str, *, profile: str = PROFILE):
    return validator._archive_boundary_diagnostic(
        source, profile, PurePosixPath(target)
    )


class ArchiveLinkBoundaryTests(unittest.TestCase):
    def test_reports_every_archive_internal_target(self) -> None:
        for target in (
            "docs/98.archive/migrations/0004-document-authority-convergence.md",
            "docs/98.archive/superseded/01.requirements/0001-wsl-k3d-argocd-platform.md",
            "docs/98.archive/tombstones/03.specs/0002-legacy.md",
        ):
            with self.subTest(target=target):
                diagnostic = _archive(CONSUMER, target)

                self.assertIsNotNone(diagnostic)
                assert diagnostic is not None
                self.assertEqual(diagnostic.rule_id, "LINK-ARCHIVE-BYPASS")
                self.assertEqual(diagnostic.path, CONSUMER)

    def test_admits_the_two_declared_routes_into_the_archive(self) -> None:
        """The index routes to a record; a retention class holds the document."""

        self.assertIsNone(_archive(CONSUMER, "docs/98.archive/README.md"))
        self.assertIsNone(
            _archive(
                CONSUMER,
                "docs/98.archive/completed/03.specs/0066-validation-tooling-ownership/spec.md",
            )
        )

    def test_only_an_incident_account_may_cite_an_archive_path(self) -> None:
        """An incident and its postmortem rest on the archived record itself.

        Every other profile keeps the claim and drops the path, so the exemption
        is bound to what a document is rather than to what state it is in."""

        target = "docs/98.archive/migrations/0004-document-authority-convergence.md"
        source = PurePosixPath(
            "docs/05.operations/incidents/2026/inc-0001-x/incident.md"
        )
        for profile in ("operation/incident", "operation/postmortem"):
            with self.subTest(profile=profile):
                self.assertIsNone(_archive(source, target, profile=profile))
        for profile in ("sdlc/task", "sdlc/architecture-decision", "operation/runbook"):
            with self.subTest(profile=profile):
                self.assertIsNotNone(_archive(source, target, profile=profile))

    def test_leaves_the_archive_own_cross_references_alone(self) -> None:
        self.assertIsNone(
            _archive(
                PurePosixPath("docs/98.archive/migrations/0004-x.md"),
                "docs/98.archive/superseded/01.requirements/0001-y.md",
            )
        )

    def test_leaves_targets_outside_the_archive_alone(self) -> None:
        self.assertIsNone(_archive(CONSUMER, "docs/02.architecture/README.md"))


class StageLinkBoundaryTests(unittest.TestCase):
    def test_reports_every_numbered_stage_target_written_outside_docs(self) -> None:
        for target in (
            "docs/01.requirements/README.md",
            "docs/02.architecture/decisions/0031-validation-ownership.md",
            "docs/03.specs/0008-current-local-gitops-platform/spec.md",
            "docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md",
            "docs/90.references/README.md",
            "docs/98.archive/README.md",
            "docs/99.templates/registry.json",
        ):
            with self.subTest(target=target):
                diagnostic = _report(CONSUMER, target)

                self.assertIsNotNone(diagnostic)
                assert diagnostic is not None
                self.assertEqual(diagnostic.rule_id, "LINK-STAGE-BOUNDARY")
                self.assertEqual(diagnostic.path, CONSUMER)
                self.assertEqual(diagnostic.actual, target)

    def test_leaves_the_documentation_hub_reachable_from_outside(self) -> None:
        self.assertIsNone(_report(CONSUMER, "docs/README.md"))

    def test_leaves_links_between_documents_inside_docs_alone(self) -> None:
        self.assertIsNone(
            validator._stage_boundary_diagnostic(
                HUB, PROFILE, PurePosixPath("docs/02.architecture/README.md")
            )
        )
        self.assertIsNone(
            validator._stage_boundary_diagnostic(
                PurePosixPath("docs/02.architecture/README.md"),
                PROFILE,
                PurePosixPath("docs/99.templates/README.md"),
            )
        )

    def test_leaves_targets_outside_the_numbered_stage_tree_alone(self) -> None:
        for target in (
            "scripts/README.md",
            ".agents/governance/quality.md",
            "docs-extra/notes.md",
        ):
            with self.subTest(target=target):
                self.assertIsNone(_report(CONSUMER, target))


if __name__ == "__main__":  # pragma: no cover - module entry guard
    unittest.main()
