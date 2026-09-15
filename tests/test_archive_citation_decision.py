#!/usr/bin/env python3
"""ADR-0039 citation decisions read from the registry's ordered table."""

from __future__ import annotations

import dataclasses
import sys
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import archive_dispositions as dispositions  # noqa: E402
from document_contracts import load_registry  # noqa: E402


REGISTRY = load_registry(ROOT)

INDEX = "docs/98.archive/README.md"
COMPLETED = (
    "docs/98.archive/completed/03.specs/0066-validation-tooling-ownership/spec.md"
)
RESOLVED = (
    "docs/98.archive/resolved/05.operations/incidents/2026/inc-0001-x/incident.md"
)
SUPERSEDED = (
    "docs/98.archive/superseded/02.architecture/decisions/"
    "0032-completed-and-terminal-document-retention.md"
)
RETIRED = "docs/98.archive/retired/05.operations/runbooks/0009-x.md"
SEALED = "docs/98.archive/superseded/01.requirements/0001-wsl-k3d-argocd-platform.md"
LEDGER = "docs/98.archive/migrations/0004-document-authority-convergence.md"
TOMBSTONE = "docs/98.archive/tombstones/0001-old-route.md"
SCOPE_MIGRATION = "docs/98.archive/migrations/0024-scope-move.md"
UNCLASSIFIED = "docs/98.archive/unknown/x.md"
OUTSIDE = "docs/02.architecture/README.md"

ORDINARY_SOURCES = (
    ("AGENTS.md", "common/root-provider-shim"),
    ("scripts/README.md", "common/readme-implementation"),
    (".agents/governance/document-lifecycle.md", "governance/rule"),
    ("docs/README.md", "common/readme-stage-index"),
    ("docs/99.templates/README.md", "common/readme-stage-index"),
    ("docs/03.specs/0082-unit-archive-retention-contract/spec.md", "sdlc/spec"),
    ("docs/05.operations/runbooks/0001-x.md", "operation/runbook"),
)
INCIDENT_SOURCES = (
    ("docs/05.operations/incidents/2026/inc-0002-y/incident.md", "operation/incident"),
    (
        "docs/05.operations/incidents/2026/inc-0002-y/postmortem.md",
        "operation/postmortem",
    ),
)
ARCHIVE_SOURCE = (LEDGER, "archive/migration")

# target -> (ordinary source, incident or postmortem source), each (admitted, rule)
EXPECTED = {
    INDEX: ((True, 2), (True, 2)),
    COMPLETED: ((True, 6), (True, 5)),
    RESOLVED: ((True, 6), (True, 5)),
    SUPERSEDED: ((False, None), (True, 5)),
    RETIRED: ((False, None), (True, 5)),
    SEALED: ((False, 4), (False, 4)),
    LEDGER: ((False, 3), (False, 3)),
    TOMBSTONE: ((False, 3), (False, 3)),
    SCOPE_MIGRATION: ((False, 3), (False, 3)),
    UNCLASSIFIED: ((False, None), (False, None)),
}


def decide(source: str, profile_id: str, target: str):
    return dispositions.citation_decision(
        REGISTRY, PurePosixPath(source), profile_id, PurePosixPath(target)
    )


class ArchiveTargetKindTests(unittest.TestCase):
    def test_targets_are_classified_by_registry_profile(self) -> None:
        for target, expected in (
            (INDEX, ("index", None)),
            (COMPLETED, ("retained-body", "completed")),
            (RESOLVED, ("retained-body", "resolved")),
            (SUPERSEDED, ("retained-body", "superseded")),
            (RETIRED, ("retained-body", "retired")),
            (SEALED, ("sealed-record", None)),
            (LEDGER, ("route-record", None)),
            (TOMBSTONE, ("route-record", None)),
            (SCOPE_MIGRATION, ("route-record", None)),
            (UNCLASSIFIED, ("unclassified", None)),
        ):
            with self.subTest(target=target):
                self.assertEqual(
                    dispositions.archive_target_kind(REGISTRY, PurePosixPath(target)),
                    expected,
                )

    def test_a_target_outside_stage98_has_no_kind(self) -> None:
        self.assertIsNone(
            dispositions.archive_target_kind(REGISTRY, PurePosixPath(OUTSIDE))
        )


class CitationDecisionTests(unittest.TestCase):
    def assertDecision(self, decision, expected) -> None:
        assert decision is not None
        self.assertEqual((decision.admitted, decision.rule), expected)

    def test_ordinary_sources_reach_only_the_index_completed_and_resolved(
        self,
    ) -> None:
        for source, profile_id in ORDINARY_SOURCES:
            for target, (ordinary, _incident) in EXPECTED.items():
                with self.subTest(source=source, target=target):
                    self.assertDecision(decide(source, profile_id, target), ordinary)

    def test_incident_accounts_cite_retained_bodies_but_not_records(self) -> None:
        for source, profile_id in INCIDENT_SOURCES:
            for target, (_ordinary, incident) in EXPECTED.items():
                with self.subTest(source=source, target=target):
                    self.assertDecision(decide(source, profile_id, target), incident)

    def test_a_runbook_beside_an_incident_does_not_inherit_its_exemption(
        self,
    ) -> None:
        source = "docs/05.operations/incidents/2026/inc-0002-y/incident.md"
        self.assertDecision(
            decide(source, "operation/runbook", SUPERSEDED), (False, None)
        )

    def test_archive_sources_keep_their_historical_links(self) -> None:
        source, profile_id = ARCHIVE_SOURCE
        for target in EXPECTED:
            with self.subTest(target=target):
                self.assertDecision(decide(source, profile_id, target), (True, 1))

    def test_a_target_outside_stage98_is_not_a_citation_decision(self) -> None:
        for source, profile_id in (
            *ORDINARY_SOURCES,
            *INCIDENT_SOURCES,
            ARCHIVE_SOURCE,
        ):
            with self.subTest(source=source):
                self.assertIsNone(decide(source, profile_id, OUTSIDE))

    def test_a_registry_without_a_citation_table_decides_nothing(self) -> None:
        registry = dataclasses.replace(REGISTRY, archive_citation=None)
        with self.assertRaises(dispositions.DispositionError):
            dispositions.citation_decision(
                registry,
                PurePosixPath("docs/README.md"),
                "common/readme-stage-index",
                PurePosixPath(COMPLETED),
            )


class CurrentArchiveAuthorityConsumerTests(unittest.TestCase):
    """The archive validator reads the same decision the link validator reads."""

    def direct_link_reported(
        self, path: str, profile: str, status: str, target: str
    ) -> bool:
        import posixpath

        from archive_validation import (
            CurrentMarkdownDocument,
            validate_current_archive_authority,
        )

        relative = posixpath.relpath(target, posixpath.dirname(path))
        document = CurrentMarkdownDocument(
            path, f"[evidence]({relative})\n", profile, status
        )
        report = validate_current_archive_authority(
            (document,), individual_archive_paths=frozenset({SEALED}), registry=REGISTRY
        )
        return "ARCHIVE-DIRECT-CURRENT-LINK" in {
            item.code for item in report.diagnostics
        }

    def test_a_current_incident_cites_a_retained_body_but_not_a_record(self) -> None:
        incident = "docs/05.operations/incidents/2026/inc-0002-y/incident.md"
        self.assertFalse(
            self.direct_link_reported(
                incident, "operation/incident", "open", SUPERSEDED
            )
        )
        self.assertTrue(
            self.direct_link_reported(incident, "operation/incident", "open", LEDGER)
        )

    def test_an_active_spec_cites_only_completed_and_resolved_bodies(self) -> None:
        spec = "docs/03.specs/0082-unit-archive-retention-contract/spec.md"
        self.assertTrue(
            self.direct_link_reported(spec, "sdlc/spec", "active", SUPERSEDED)
        )
        self.assertFalse(
            self.direct_link_reported(spec, "sdlc/spec", "active", RESOLVED)
        )


if __name__ == "__main__":  # pragma: no cover - module entry guard
    unittest.main()
