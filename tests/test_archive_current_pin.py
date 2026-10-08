"""Current WORK-107 ledger admission stays separate from historical recovery."""

from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import archive_recovery, archive_validation
from scripts.archive_recovery import ArchiveContractError


ROOT = Path(__file__).resolve().parents[1]


class CurrentWork107PinTests(unittest.TestCase):
    def setUp(self) -> None:
        self.content = (ROOT / archive_recovery.WORK107_MIGRATION_PATH).read_bytes()

    def test_current_reader_accepts_exact_bytes_and_rejects_canonical_subset(
        self,
    ) -> None:
        rows = archive_recovery.parse_pinned_work107_migration_document(self.content)
        self.assertEqual(
            hashlib.sha256(self.content).hexdigest(),
            archive_recovery.WORK107_MIGRATION_DOCUMENT_SHA256,
        )
        self.assertEqual(
            rows, archive_recovery.parse_work107_migration_document(self.content)
        )
        earlier_shape = archive_recovery.render_work107_migration_document(rows[:1])
        with self.assertRaises(ArchiveContractError):
            archive_recovery.parse_pinned_work107_migration_document(earlier_shape)
        with self.assertRaises(ArchiveContractError):
            archive_recovery.parse_pinned_work107_migration_document(
                self.content + b"\n"
            )

    def test_current_archive_reader_requires_ledger_presence(self) -> None:
        with tempfile.TemporaryDirectory(prefix="archive-current-ledger-") as temporary:
            with self.assertRaisesRegex(RuntimeError, "stable ledger is unavailable"):
                archive_validation._work107_stable_rows(Path(temporary))  # noqa: SLF001

            with (
                mock.patch.object(
                    archive_validation,
                    "_repository_archive_records",
                    return_value=({}, [], None),
                ),
                mock.patch.object(
                    archive_validation, "repository_registry", return_value=None
                ),
                mock.patch.object(
                    archive_validation, "_read_repository_index", return_value=""
                ),
            ):
                report = archive_validation.validate_repository_archive(temporary, {})
            self.assertIn(
                "ARCHIVE-MIGRATION-LEDGER", {item.code for item in report.diagnostics}
            )

    def test_link_reader_uses_supplied_bytes_without_git_rebuild(self) -> None:
        links = archive_validation._load_canonical_link_module()  # noqa: SLF001
        links._validated_work107_stable_archive_rows.cache_clear()  # noqa: SLF001
        rows = links._validated_work107_stable_archive_rows(self.content)  # noqa: SLF001
        self.assertTrue(rows)
        rejected = links._validated_work107_stable_archive_rows(  # noqa: SLF001
            self.content + b"\n"
        )
        self.assertEqual(rejected, ())

    def test_historical_source_recovery_still_requires_its_git_object(self) -> None:
        row = archive_recovery.parse_work107_migration_document(self.content)[0]
        recovered = archive_recovery.recover_work107_legacy_envelope(ROOT, row)
        self.assertEqual(recovered.metadata["source_blob"], row["source_blob"])
        missing = dict(row)
        missing["legacy_archive_commit"] = "0" * 40
        with self.assertRaises(ArchiveContractError):
            archive_recovery.recover_work107_legacy_envelope(ROOT, missing)


if __name__ == "__main__":
    unittest.main()
