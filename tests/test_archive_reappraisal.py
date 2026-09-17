#!/usr/bin/env python3
"""ADR-0040 reappraisal: the assessment contract, table, and citation rule."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import archive_dispositions as dispositions  # noqa: E402
from document_contracts import load_registry, validate_registry  # noqa: E402


REGISTRY = load_registry(ROOT)
RAW = json.loads((ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8"))

PACKAGE = "docs/98.archive/completed/03.specs/0080-adr-0032-retention-pilot"
DOCUMENT = (
    "docs/98.archive/superseded/02.architecture/decisions/"
    "0035-common-agents-authority-and-native-skill-routing.md"
)
DECISION = (
    "docs/03.specs/0085-archive-reappraisal-and-document-standards/tasks/tsk-0003-x.md"
)
OWNER = (
    "docs/02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md"
)
HOLD = "docs/05.operations/policies/0001-x.md"
PROFILES = {
    DECISION: "sdlc/task",
    OWNER: "sdlc/architecture-decision",
    HOLD: "operation/policy",
}
CATALOG_ROWS = {
    PurePosixPath(PACKAGE): None,
    PurePosixPath(DOCUMENT): None,
}


def link(path: str | None) -> str:
    if path is None:
        return "none"
    return f"[x](../{path.removeprefix('docs/')})"


def row(
    record: str = PACKAGE,
    assessment: str = "invalidated",
    availability: str = "retained",
    *,
    owner: str | None = None,
    decision: str | None = DECISION,
    assessed: str = "2026-09-17",
    hold: str | None = None,
) -> str:
    relative = record.removeprefix("docs/98.archive/")
    cells = (
        f"`{relative}`",
        assessment,
        availability,
        link(owner),
        link(decision),
        assessed,
        link(hold),
    )
    return "| " + " | ".join(cells) + " |"


def table(*rows: str) -> str:
    contract = REGISTRY.archive_assessment
    header = "| " + " | ".join(contract.columns) + " |"
    separator = "| " + " | ".join("---" for _ in contract.columns) + " |"
    return "\n".join(
        ["# Archive", "", f"### {contract.heading}", "", header, separator, *rows, ""]
    )


def diagnose(*rows: str, present: frozenset[str] = frozenset({PACKAGE, DOCUMENT})):
    parsed, errors = dispositions.parse_assessment(REGISTRY, table(*rows))
    codes = {code for code, _ in errors}
    codes.update(
        code
        for code, _ in dispositions.assessment_diagnostics(
            REGISTRY,
            parsed,
            CATALOG_ROWS,
            present=lambda path: path.as_posix() in present,
            profile_of=lambda path: PROFILES.get(path.as_posix()),
        )
    )
    return parsed, codes


def rule_ids(raw: dict) -> set[str]:
    try:
        validate_registry(ROOT, raw)
    except Exception as error:  # noqa: BLE001 - the registry error carries diagnostics
        return {item.rule_id for item in getattr(error, "diagnostics", ())} or {
            type(error).__name__
        }
    return set()


class AssessmentContractTests(unittest.TestCase):
    def test_registry_declares_the_assessment_vocabulary(self) -> None:
        contract = REGISTRY.archive_assessment
        self.assertEqual(contract.heading, "Retention Assessment")
        self.assertEqual(
            contract.columns,
            (
                "Disposition Record",
                "Assessment",
                "Availability",
                "Current Owner",
                "Decision",
                "Assessed",
                "Hold",
            ),
        )
        self.assertEqual(
            contract.assessments,
            ("unreviewed", "usable", "superseded", "withdrawn", "invalidated"),
        )
        self.assertEqual(
            contract.availabilities, ("retained", "git-history-only", "purged")
        )
        self.assertEqual(
            (contract.default_assessment, contract.default_availability),
            ("unreviewed", "retained"),
        )
        self.assertEqual(contract.owner_required_assessments, frozenset({"superseded"}))
        self.assertEqual(contract.reserved_availabilities, frozenset({"purged"}))
        self.assertEqual(
            contract.removed_availabilities, frozenset({"git-history-only"})
        )
        self.assertEqual(
            contract.decision_profile_ids,
            frozenset({"sdlc/task", "sdlc/spec", "sdlc/architecture-decision"}),
        )
        self.assertEqual(contract.default_branch, "main")

    def test_a_default_outside_the_vocabulary_is_rejected(self) -> None:
        raw = copy.deepcopy(RAW)
        raw["archive_assessment"]["default_assessment"] = "usable-by-default"
        self.assertTrue(rule_ids(raw))

    def test_a_decision_profile_the_registry_lacks_is_rejected(self) -> None:
        raw = copy.deepcopy(RAW)
        raw["archive_assessment"]["decision_profile_ids"].append("sdlc/forgotten")
        self.assertIn("REGISTRY_ARCHIVE_ASSESSMENT", rule_ids(raw))


class AssessmentTableTests(unittest.TestCase):
    def test_an_absent_table_means_every_unit_is_unreviewed_and_retained(self) -> None:
        rows, errors = dispositions.parse_assessment(REGISTRY, "# Archive\n")
        self.assertEqual((rows, errors), ({}, ()))
        self.assertEqual(
            dispositions.assessment_of(REGISTRY, rows, PurePosixPath(PACKAGE)),
            ("unreviewed", "retained"),
        )

    def test_an_empty_table_is_valid(self) -> None:
        self.assertEqual(diagnose(), ({}, set()))

    def test_prose_may_precede_the_table(self) -> None:
        contract = REGISTRY.archive_assessment
        text = table(row()).replace(
            f"### {contract.heading}\n", f"### {contract.heading}\n\nJudgment prose.\n"
        )
        rows, errors = dispositions.parse_assessment(REGISTRY, text)
        self.assertEqual(errors, ())
        self.assertIn(PurePosixPath(PACKAGE), rows)

    def test_a_heading_without_a_table_is_malformed(self) -> None:
        contract = REGISTRY.archive_assessment
        text = f"### {contract.heading}\n\nNo table.\n\n## Next\n\n| a | b |\n"
        self.assertEqual(
            dispositions.parse_assessment(REGISTRY, text)[1],
            (("ARCHIVE-ASSESSMENT-STRUCTURE", "docs/98.archive/README.md"),),
        )

    def test_a_reappraisal_row_is_read(self) -> None:
        rows, codes = diagnose(row())
        self.assertEqual(codes, set())
        parsed = rows[PurePosixPath(PACKAGE)]
        self.assertEqual(
            (parsed.assessment, parsed.availability, parsed.decision),
            ("invalidated", "retained", PurePosixPath(DECISION)),
        )

    def test_a_member_resolves_to_its_unit_row(self) -> None:
        rows, _ = diagnose(row())
        self.assertEqual(
            dispositions.assessment_of(
                REGISTRY, rows, PurePosixPath(f"{PACKAGE}/tasks/tsk-0001.md")
            ),
            ("invalidated", "retained"),
        )

    def test_a_row_must_name_a_catalog_record(self) -> None:
        other = "docs/98.archive/completed/03.specs/0066-validation-tooling-ownership"
        self.assertIn("ARCHIVE-ASSESSMENT-RECORD", diagnose(row(other))[1])

    def test_a_record_has_one_row(self) -> None:
        self.assertIn("ARCHIVE-ASSESSMENT-STRUCTURE", diagnose(row(), row())[1])

    def test_a_malformed_row_is_rejected(self) -> None:
        self.assertIn("ARCHIVE-ASSESSMENT-STRUCTURE", diagnose("| `x` | usable |")[1])

    def test_an_unknown_value_is_rejected(self) -> None:
        self.assertIn("ARCHIVE-ASSESSMENT-VALUE", diagnose(row(assessment="fine"))[1])
        self.assertIn(
            "ARCHIVE-ASSESSMENT-VALUE", diagnose(row(availability="elsewhere"))[1]
        )

    def test_a_row_that_changes_nothing_is_rejected(self) -> None:
        self.assertIn(
            "ARCHIVE-ASSESSMENT-NOOP",
            diagnose(row(assessment="unreviewed", availability="retained"))[1],
        )

    def test_usable_is_a_judgment_that_needs_a_decision(self) -> None:
        self.assertEqual(diagnose(row(assessment="usable"))[1], set())
        self.assertIn(
            "ARCHIVE-ASSESSMENT-DECISION",
            diagnose(row(assessment="usable", decision=None))[1],
        )

    def test_a_decision_must_be_a_current_task_spec_or_decision(self) -> None:
        self.assertIn("ARCHIVE-ASSESSMENT-DECISION", diagnose(row(decision=HOLD))[1])
        self.assertIn(
            "ARCHIVE-ASSESSMENT-DECISION",
            diagnose(row(decision="docs/03.specs/9999-missing/spec.md"))[1],
        )
        self.assertIn(
            "ARCHIVE-ASSESSMENT-DECISION", diagnose(row(decision=DOCUMENT))[1]
        )

    def test_superseded_needs_a_current_owner(self) -> None:
        self.assertIn(
            "ARCHIVE-ASSESSMENT-OWNER", diagnose(row(assessment="superseded"))[1]
        )
        self.assertEqual(diagnose(row(assessment="superseded", owner=OWNER))[1], set())
        self.assertIn(
            "ARCHIVE-ASSESSMENT-OWNER",
            diagnose(row(assessment="superseded", owner=DOCUMENT))[1],
        )

    def test_the_assessed_date_is_a_calendar_date(self) -> None:
        for value in ("2026-02-30", "17-09-2026", "", "2026-09-17T00:00:00Z"):
            with self.subTest(value=value):
                self.assertIn(
                    "ARCHIVE-ASSESSMENT-DATE", diagnose(row(assessed=value))[1]
                )

    def test_purged_is_reserved(self) -> None:
        self.assertIn(
            "ARCHIVE-ASSESSMENT-RESERVED",
            diagnose(row(availability="purged"), present=frozenset({DOCUMENT}))[1],
        )

    def test_removal_needs_the_unit_gone_and_no_hold(self) -> None:
        removed = row(assessment="withdrawn", availability="git-history-only")
        self.assertEqual(diagnose(removed, present=frozenset({DOCUMENT}))[1], set())
        self.assertIn("ARCHIVE-ASSESSMENT-AVAILABILITY", diagnose(removed)[1])
        held = row(assessment="withdrawn", availability="git-history-only", hold=HOLD)
        self.assertIn(
            "ARCHIVE-ASSESSMENT-HOLD", diagnose(held, present=frozenset({DOCUMENT}))[1]
        )

    def test_a_retained_unit_must_be_present(self) -> None:
        self.assertIn(
            "ARCHIVE-ASSESSMENT-AVAILABILITY",
            diagnose(row(), present=frozenset({DOCUMENT}))[1],
        )


class RemovedRecordsTests(unittest.TestCase):
    """Every consumer of `removed_records` trusts only a row that could pass."""

    def removed(self, *rows: str) -> frozenset[PurePosixPath]:
        relative = PACKAGE.removeprefix("docs/98.archive/")
        catalog = (
            f"{dispositions.CATALOG_HEADER}\n{dispositions.CATALOG_SEPARATOR}\n"
            f"| [`{relative}`](./{relative}) | "
            f"`{'a' * 40}:docs/03.specs/0080-adr-0032-retention-pilot` |\n\n"
        )
        return dispositions.removed_records(REGISTRY, catalog + table(*rows))

    def test_a_valid_removal_row_is_removed(self) -> None:
        self.assertEqual(
            self.removed(row(assessment="withdrawn", availability="git-history-only")),
            frozenset({PurePosixPath(PACKAGE)}),
        )

    def test_a_row_without_a_decision_or_with_a_hold_is_not_removed(self) -> None:
        for bad in (
            row(assessment="withdrawn", availability="git-history-only", decision=None),
            row(assessment="withdrawn", availability="git-history-only", hold=HOLD),
            row(
                assessment="withdrawn",
                availability="git-history-only",
                assessed="2026-02-30",
            ),
            row(
                assessment="withdrawn",
                availability="git-history-only",
                decision=DOCUMENT,
            ),
        ):
            with self.subTest(row=bad):
                self.assertEqual(self.removed(bad), frozenset())

    def test_a_malformed_table_removes_nothing(self) -> None:
        self.assertEqual(
            self.removed(
                row(assessment="withdrawn", availability="git-history-only"),
                "| `x` | usable |",
            ),
            frozenset(),
        )

    def test_parity_still_reports_a_row_that_cannot_justify_removal(self) -> None:
        text = table(
            row(assessment="withdrawn", availability="git-history-only", decision=None)
        )
        index = (
            "| Disposition Record | Retention Envelope |\n| --- | --- |\n"
            f"| [`{PACKAGE.removeprefix('docs/98.archive/')}`]"
            f"(./{PACKAGE.removeprefix('docs/98.archive/')}) | "
            f"`{'a' * 40}:docs/03.specs/0080-adr-0032-retention-pilot` |\n\n"
        ) + text
        codes = {
            code
            for code, _ in dispositions.catalog_parity_diagnostics(REGISTRY, index, {})
        }
        self.assertIn("ARCHIVE-CATALOG-PARITY", codes)


class CitationAvailabilityTests(unittest.TestCase):
    SOURCE = (PurePosixPath("docs/03.specs/0001-x/spec.md"), "sdlc/spec")
    INCIDENT = (
        PurePosixPath("docs/05.operations/incidents/2026/inc-0002-y/incident.md"),
        "operation/incident",
    )
    TARGET = PurePosixPath(f"{PACKAGE}/spec.md")

    def decide(self, source, assessment: str, availability: str):
        rows, _ = diagnose(row(assessment=assessment, availability=availability))
        return dispositions.citation_decision(
            REGISTRY, source[0], source[1], self.TARGET, assessments=rows
        )

    def test_withdrawn_invalidated_and_removed_units_are_not_cited(self) -> None:
        for assessment, availability in (
            ("withdrawn", "retained"),
            ("invalidated", "retained"),
            ("usable", "git-history-only"),
        ):
            for source in (self.SOURCE, self.INCIDENT):
                with self.subTest(
                    assessment=assessment, availability=availability, source=source
                ):
                    self.assertFalse(
                        self.decide(source, assessment, availability).admitted
                    )

    def test_superseded_and_usable_units_stay_citable(self) -> None:
        for assessment in ("superseded", "usable"):
            with self.subTest(assessment=assessment):
                self.assertTrue(
                    self.decide(self.SOURCE, assessment, "retained").admitted
                )

    def test_a_stage98_source_is_never_rejudged(self) -> None:
        rows, _ = diagnose(row(assessment="invalidated"))
        decision = dispositions.citation_decision(
            REGISTRY,
            PurePosixPath(DOCUMENT),
            "sdlc/architecture-decision",
            self.TARGET,
            assessments=rows,
        )
        self.assertEqual((decision.admitted, decision.rule), (True, 1))

    def test_the_index_stays_citable(self) -> None:
        rows, _ = diagnose(row(assessment="invalidated"))
        decision = dispositions.citation_decision(
            REGISTRY,
            *self.SOURCE,
            PurePosixPath("docs/98.archive/README.md"),
            assessments=rows,
        )
        self.assertTrue(decision.admitted)


if __name__ == "__main__":
    unittest.main()
