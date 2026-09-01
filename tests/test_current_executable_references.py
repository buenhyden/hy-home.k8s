#!/usr/bin/env python3
"""Focused behavior tests for current and historical script references."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path, PurePosixPath

from scripts.validation import current_executable_references as references


ROOT = Path(__file__).resolve().parents[1]


class CurrentExecutableReferenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(
            prefix="current-executable-references-"
        )
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, relative: str, content: str = "#!/usr/bin/env python3\n") -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def validate(
        self,
        source: str,
        text: str,
        *,
        tracked: tuple[str, ...] = (),
        historical_path_exists=lambda _path: False,
    ) -> tuple[references.ExecutableReferenceDiagnostic, ...]:
        source_path = PurePosixPath(source)
        tracked_paths = frozenset(
            {source_path, *(PurePosixPath(path) for path in tracked)}
        )
        return references.validate_current_executable_references(
            self.root,
            tracked_paths=tracked_paths,
            source_texts={source_path: text},
            executable_suffixes=frozenset({".py", ".sh", ".mjs"}),
            historical_path_exists=historical_path_exists,
        )

    def test_present_reference_is_extension_neutral_and_depth_aware(self) -> None:
        target = "scripts/validation/document/check-contract.mjs"
        self.write(target, "#!/usr/bin/env node\n")

        diagnostics = self.validate(
            "docs/00.agent-governance/README.md",
            f"Run `node {target}`.\n",
            tracked=(target,),
        )

        self.assertEqual(diagnostics, ())

    def test_missing_current_reference_is_not_waived_by_git_history(self) -> None:
        target = "scripts/validation/document/check-contract.py"
        recovered: list[PurePosixPath] = []

        diagnostics = self.validate(
            "docs/00.agent-governance/README.md",
            f"Run `python3 {target}`.\n",
            historical_path_exists=lambda path: recovered.append(path) or True,
        )

        self.assertEqual([item.code for item in diagnostics], ["EXECUTABLE-CURRENT"])
        self.assertEqual(recovered, [])

    def test_terminal_reference_uses_git_first_recovery(self) -> None:
        target = PurePosixPath("scripts/retired/deep/check-contract.py")
        recovered: list[PurePosixPath] = []
        text = (
            "---\nstatus: done\n---\n\n"
            f"Historical command: `python3 {target}`.\n"
        )

        diagnostics = self.validate(
            "docs/03.specs/0001-example/spec.md",
            text,
            historical_path_exists=lambda path: recovered.append(path) or True,
        )

        self.assertEqual(diagnostics, ())
        self.assertEqual(recovered, [target])

    def test_active_spec_proposal_does_not_claim_a_current_executable(self) -> None:
        invoked: list[PurePosixPath] = []
        diagnostics = self.validate(
            "docs/03.specs/0001-example/spec.md",
            "---\nstatus: active\n---\n\n"
            "Proposed: `scripts/future/deep/check-contract.py`.\n",
            historical_path_exists=lambda path: invoked.append(path) or True,
        )

        self.assertEqual(diagnostics, ())
        self.assertEqual(invoked, [])

    def test_unrecoverable_terminal_reference_fails_closed(self) -> None:
        target = "scripts/retired/deep/check-contract.sh"
        diagnostics = self.validate(
            "docs/03.specs/0001-example/plan.md",
            f"---\nstatus: done\n---\n\nHistorical: `{target}`.\n",
        )

        self.assertEqual([item.code for item in diagnostics], ["EXECUTABLE-HISTORY"])

    def test_sealed_archive_reference_is_delegated_to_archive_validation(self) -> None:
        invoked: list[PurePosixPath] = []
        diagnostics = self.validate(
            "docs/98.archive/records/0001-example.md",
            "Historical: `scripts/retired/deep/check-contract.py`.\n",
            historical_path_exists=lambda path: invoked.append(path) or False,
        )

        self.assertEqual(diagnostics, ())
        self.assertEqual(invoked, [])

    def test_registry_argv_derives_extensions_instead_of_hardcoding_shell(self) -> None:
        registry = {
            "validators": [
                {"argv": ["python3", "scripts/check.py"]},
                {"argv": ["bash", "scripts/deep/check.sh"]},
                {"argv": ["node", "scripts/deeper/check.mjs"]},
            ]
        }

        self.assertEqual(
            references.executable_suffixes_from_registry(registry),
            frozenset({".mjs", ".py", ".sh"}),
        )

    def test_repository_aggregate_delegates_instead_of_reimplementing_rule(self) -> None:
        aggregate = (ROOT / "scripts/validate-repo-quality-gates.sh").read_text(
            encoding="utf-8"
        )
        owner = (
            ROOT / "scripts/validation/repository/quality.py"
        ).read_text(encoding="utf-8")
        registry = json.loads(
            (ROOT / "scripts/validation/registry.json").read_text(encoding="utf-8")
        )
        repository_quality = next(
            row for row in registry["validators"] if row["id"] == "repository-quality"
        )

        self.assertNotIn("script_ref_pattern =", aggregate)
        self.assertNotIn("validate_current_executable_references(", aggregate)
        self.assertNotIn("scripts/validation/repository/quality.py", aggregate)
        self.assertEqual(
            repository_quality["argv"],
            [
                "python3",
                "scripts/validation/repository/quality.py",
                "--root",
                ".",
            ],
        )
        self.assertIn("validate_current_executable_references(", owner)


if __name__ == "__main__":
    unittest.main()
