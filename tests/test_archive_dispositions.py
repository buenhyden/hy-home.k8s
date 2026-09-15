#!/usr/bin/env python3
"""ADR-0038 six-disposition Stage 98 owner contracts."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import archive_dispositions as dispositions  # noqa: E402
from document_contracts import DocumentContractError, classify_path, load_registry  # noqa: E402


REGISTRY = load_registry(ROOT)
COMMIT = "a" * 40
FROZEN_RECORD = (
    "docs/98.archive/superseded/01.requirements/0001-wsl-k3d-argocd-platform.md"
)


def catalog(*rows: str) -> str:
    return "\n".join(
        (
            "# Archive",
            "",
            "## Retention Catalog",
            "",
            dispositions.CATALOG_HEADER,
            dispositions.CATALOG_SEPARATOR,
            *rows,
            "",
        )
    )


def row(record: str, envelope: str) -> str:
    relative = record.removeprefix("docs/98.archive/")
    return f"| [`{relative}`](./{relative}) | `{envelope}` |"


class RegistryGenerationTests(unittest.TestCase):
    def test_frozen_records_and_ledgers_keep_their_generation(self) -> None:
        self.assertEqual(
            classify_path(REGISTRY, PurePosixPath(FROZEN_RECORD)).profile_id,
            "archive/tombstone",
        )
        self.assertEqual(
            classify_path(
                REGISTRY,
                PurePosixPath(
                    "docs/98.archive/migrations/0013-completed-stage03-package-retention.md"
                ),
            ).profile_id,
            "archive/migration",
        )

    def test_no_new_record_or_path_ledger_is_routable(self) -> None:
        for path in (
            "docs/98.archive/superseded/03.specs/0900-fixture.md",
            "docs/98.archive/migrations/0005-policy-convergence.md",
        ):
            with self.subTest(path=path):
                with self.assertRaises(DocumentContractError):
                    classify_path(REGISTRY, PurePosixPath(path))

    def test_retained_bodies_keep_their_original_profile(self) -> None:
        for path, profile in (
            (
                "docs/98.archive/superseded/01.requirements/0009-next.md",
                "sdlc/requirement",
            ),
            (
                "docs/98.archive/superseded/02.architecture/decisions/0032-x.md",
                "sdlc/architecture-decision",
            ),
            (
                "docs/98.archive/retired/05.operations/runbooks/0009-x.md",
                "operation/runbook",
            ),
            (
                "docs/98.archive/resolved/05.operations/incidents/2026/inc-0001-x/incident.md",
                "operation/incident",
            ),
            ("docs/98.archive/completed/03.specs/0079-x/spec.md", "sdlc/spec"),
        ):
            with self.subTest(path=path):
                self.assertEqual(
                    classify_path(REGISTRY, PurePosixPath(path)).profile_id, profile
                )

    def test_route_dispositions_have_body_less_profiles(self) -> None:
        self.assertEqual(
            classify_path(
                REGISTRY, PurePosixPath("docs/98.archive/tombstones/0001-old-route.md")
            ).profile_id,
            "archive/route-tombstone",
        )
        self.assertEqual(
            classify_path(
                REGISTRY, PurePosixPath("docs/98.archive/migrations/0024-scope-move.md")
            ).profile_id,
            "archive/scope-migration",
        )

    def test_registry_binds_each_class_to_its_source_states(self) -> None:
        bound = {item.name: item for item in REGISTRY.retention_classes}
        self.assertEqual(set(bound), {"completed", "superseded", "retired", "resolved"})
        self.assertIn("done", bound["completed"].admitted_states)
        self.assertEqual(bound["superseded"].admitted_states, frozenset({"superseded"}))
        self.assertIn("withdrawn", bound["retired"].admitted_states)
        self.assertEqual(
            bound["resolved"].admitted_states, frozenset({"closed", "published"})
        )


class RetentionPathTests(unittest.TestCase):
    def test_retention_class_is_read_from_the_mirror_path(self) -> None:
        path = PurePosixPath(
            "docs/98.archive/superseded/02.architecture/decisions/0032-x.md"
        )
        retention = dispositions.retention_class_of(REGISTRY, path)
        assert retention is not None
        self.assertEqual(retention.name, "superseded")
        self.assertEqual(
            dispositions.retention_source_path(path),
            PurePosixPath("docs/02.architecture/decisions/0032-x.md"),
        )

    def test_frozen_record_and_route_records_are_not_retained_bodies(self) -> None:
        for path in (
            FROZEN_RECORD,
            "docs/98.archive/tombstones/0001-old-route.md",
            "docs/98.archive/migrations/0024-scope-move.md",
            "docs/98.archive/README.md",
            "docs/02.architecture/decisions/0032-x.md",
        ):
            with self.subTest(path=path):
                self.assertIsNone(
                    dispositions.retention_class_of(REGISTRY, PurePosixPath(path))
                )


class RetentionEnvelopeTests(unittest.TestCase):
    def test_envelope_names_one_commit_and_original_path(self) -> None:
        envelope = dispositions.parse_retention_envelope(
            f"{COMMIT}:docs/02.architecture/decisions/0032-x.md"
        )
        self.assertEqual(envelope.commit, COMMIT)
        self.assertEqual(
            envelope.original_path,
            PurePosixPath("docs/02.architecture/decisions/0032-x.md"),
        )

    def test_envelope_rejects_a_second_recovery_identity(self) -> None:
        for value in (
            f"{COMMIT}",
            f"{COMMIT[:12]}:docs/a.md",
            f"{COMMIT}:docs/a.md:{'b' * 40}",
            f"{COMMIT}:/docs/a.md",
            f"{COMMIT}:docs/../a.md",
            f"{COMMIT}:docs/a.md sha256={'c' * 64}",
            f"{COMMIT.upper()}:docs/a.md",
        ):
            with self.subTest(value=value):
                with self.assertRaises(dispositions.DispositionError):
                    dispositions.parse_retention_envelope(value)


class CatalogTests(unittest.TestCase):
    record = "docs/98.archive/superseded/02.architecture/decisions/0032-x.md"
    original = "docs/02.architecture/decisions/0032-x.md"

    def test_absent_catalog_has_no_rows(self) -> None:
        self.assertEqual(dispositions.parse_catalog("# Archive\n"), ({}, ()))

    def test_catalog_row_names_record_and_envelope(self) -> None:
        rows, errors = dispositions.parse_catalog(
            catalog(row(self.record, f"{COMMIT}:{self.original}"))
        )
        self.assertEqual(errors, ())
        entry = rows[PurePosixPath(self.record)]
        self.assertEqual(entry.envelope.original_path, PurePosixPath(self.original))

    def test_catalog_rejects_duplicates_bad_links_and_extra_columns(self) -> None:
        for text in (
            catalog(
                row(self.record, f"{COMMIT}:{self.original}"),
                row(self.record, f"{COMMIT}:{self.original}"),
            ),
            catalog(f"| [`x`](./y) | `{COMMIT}:{self.original}` |"),
            catalog(
                row(self.record, f"{COMMIT}:{self.original}")[:-1] + f" `{'d' * 40}` |"
            ),
            catalog(),
            catalog(row(self.record, f"{COMMIT}:{self.original}"))
            + dispositions.CATALOG_HEADER
            + "\n",
        ):
            with self.subTest(text=text[-120:]):
                _rows, errors = dispositions.parse_catalog(text)
                self.assertTrue(errors)

    def test_catalog_span_lets_the_frozen_index_parser_skip_it(self) -> None:
        text = catalog(row(self.record, f"{COMMIT}:{self.original}"))
        lines = text.splitlines()
        span = dispositions.catalog_line_span(lines)
        assert span is not None
        start, end = span
        self.assertEqual(lines[start], dispositions.CATALOG_HEADER)
        self.assertTrue(all(line.startswith("|") for line in lines[start:end]))
        self.assertFalse(end < len(lines) and lines[end].startswith("|"))


class LinkRebaseTests(unittest.TestCase):
    source = PurePosixPath("docs/02.architecture/decisions/0032-x.md")
    record = PurePosixPath(
        "docs/98.archive/superseded/02.architecture/decisions/0032-x.md"
    )
    text = (
        "See [next](./0038-y.md), [registry](../../99.templates/registry.json#top),\n"
        "[site](https://example.com/a), [here](#local).\n\n[ref]: ../README.md\n"
    )

    def test_rebased_copy_names_the_same_targets(self) -> None:
        rebased = dispositions.rebase_relative_links(
            self.text, self.source, self.record
        )
        self.assertIn("../../../../02.architecture/decisions/0038-y.md", rebased)
        self.assertIn("https://example.com/a", rebased)
        self.assertIn("(#local)", rebased)
        self.assertEqual(
            dispositions.link_resolved_text(self.text, self.source),
            dispositions.link_resolved_text(rebased, self.record),
        )

    def test_unrebased_or_rewritten_copy_differs(self) -> None:
        self.assertNotEqual(
            dispositions.link_resolved_text(self.text, self.source),
            dispositions.link_resolved_text(self.text, self.record),
        )
        rebased = dispositions.rebase_relative_links(
            self.text, self.source, self.record
        )
        self.assertNotEqual(
            dispositions.link_resolved_text(self.text, self.source),
            dispositions.link_resolved_text(rebased + "Added.\n", self.record),
        )

    def test_links_to_documents_moving_together_follow_the_move(self) -> None:
        moves = {
            PurePosixPath("docs/02.architecture/decisions/0038-y.md"): PurePosixPath(
                "docs/98.archive/superseded/02.architecture/decisions/0038-y.md"
            )
        }
        rebased = dispositions.rebase_relative_links(
            self.text, self.source, self.record, moves
        )
        self.assertIn("(./0038-y.md)", rebased)
        self.assertEqual(
            dispositions.link_resolved_text(self.text, self.source, moves),
            dispositions.link_resolved_text(rebased, self.record),
        )


class CatalogParityTests(unittest.TestCase):
    record = PurePosixPath(
        "docs/98.archive/superseded/02.architecture/decisions/0032-x.md"
    )
    original = "docs/02.architecture/decisions/0032-x.md"
    body = '---\ntype: "sdlc/architecture-decision"\nsuperseded_by: "ADR-0038"\n---\n'

    def parity(self, index_text, texts, frozen=frozenset()):
        return dispositions.catalog_parity_diagnostics(
            REGISTRY, index_text, texts, frozen_retained=frozen
        )

    def test_every_current_generation_file_has_exactly_one_row(self) -> None:
        text = catalog(row(self.record.as_posix(), f"{COMMIT}:{self.original}"))
        self.assertEqual(self.parity(text, {self.record: self.body}), ())
        self.assertIn(
            ("ARCHIVE-CATALOG-PARITY", self.record.as_posix()),
            self.parity("# Archive\n", {self.record: self.body}),
        )
        self.assertIn(
            ("ARCHIVE-CATALOG-PARITY", self.record.as_posix()),
            self.parity(text, {}),
        )

    def test_frozen_retained_bodies_keep_their_ledger_generation(self) -> None:
        completed = PurePosixPath("docs/98.archive/completed/03.specs/0067-x/spec.md")
        self.assertEqual(
            self.parity(
                "# Archive\n", {completed: "---\n---\n"}, frozenset({completed})
            ),
            (),
        )

    def test_row_must_name_the_mirrored_source(self) -> None:
        text = catalog(
            row(
                self.record.as_posix(),
                f"{COMMIT}:docs/02.architecture/decisions/0031-y.md",
            )
        )
        self.assertIn(
            ("ARCHIVE-CATALOG-ENVELOPE", self.record.as_posix()),
            self.parity(text, {self.record: self.body}),
        )

    def test_superseded_body_must_name_its_successor(self) -> None:
        text = catalog(row(self.record.as_posix(), f"{COMMIT}:{self.original}"))
        self.assertIn(
            ("ARCHIVE-DISPOSITION-NAMING", self.record.as_posix()),
            self.parity(
                text, {self.record: '---\ntype: "sdlc/architecture-decision"\n---\n'}
            ),
        )

    def test_route_record_envelope_names_its_route(self) -> None:
        tomb = PurePosixPath("docs/98.archive/tombstones/0001-old-route.md")
        body = '---\nretired_route: "docs/05.operations/guides/0009-old.md"\n---\n'
        good = catalog(
            row(tomb.as_posix(), f"{COMMIT}:docs/05.operations/guides/0009-old.md")
        )
        bad = catalog(
            row(tomb.as_posix(), f"{COMMIT}:docs/05.operations/guides/0008-other.md")
        )
        self.assertEqual(self.parity(good, {tomb: body}), ())
        self.assertIn(
            ("ARCHIVE-CATALOG-ENVELOPE", tomb.as_posix()),
            self.parity(bad, {tomb: body}),
        )


class FrozenIndexParserTests(unittest.TestCase):
    def test_both_frozen_index_parsers_skip_the_catalog_table(self) -> None:
        import archive_cutover
        import archive_validation

        index = (ROOT / "docs/98.archive/README.md").read_text(encoding="utf-8")
        if dispositions.CATALOG_HEADER not in index:
            index += "\n" + catalog(
                row(
                    "docs/98.archive/superseded/02.architecture/decisions/0032-x.md",
                    f"{COMMIT}:docs/02.architecture/decisions/0032-x.md",
                )
            )
        catalog_rows, catalog_errors = dispositions.parse_catalog(index)
        self.assertTrue(catalog_rows)
        self.assertEqual(catalog_errors, ())
        rows, _links, diagnostics = archive_validation._parse_repository_index(index)
        self.assertEqual(len(rows), 25)
        self.assertEqual(diagnostics, [])
        cutover_rows, structure_failure = archive_cutover._parse_archive_index(index)
        self.assertEqual(len(cutover_rows), 25)
        self.assertFalse(structure_failure)


if __name__ == "__main__":  # pragma: no cover - module entry guard
    unittest.main()
