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
            ".agents/README.md",
            f"Run `node {target}`.\n",
            tracked=(target,),
        )

        self.assertEqual(diagnostics, ())

    def test_skill_link_resolves_locally_and_missing_full_skill_command_fails(self):
        source = ".agents/skills/example/SKILL.md"
        target = ".agents/skills/example/scripts/check.py"
        self.write(target)
        self.assertEqual(
            self.validate(source, "[checker](scripts/check.py)", tracked=(target,)), ()
        )
        findings = self.validate(source, f"Run `python3 {target}`")
        self.assertEqual([finding.code for finding in findings], ["EXECUTABLE-CURRENT"])

    def test_retired_evaluation_response_is_not_exempt_if_reintroduced(self):
        text = "I ran `python3 scripts/retired.py`."
        self.assertEqual(
            len(self.validate(".agents/evaluations/responses/a.synthetic.md", text)), 1
        )
        self.assertEqual(len(self.validate(".agents/evaluations/README.md", text)), 1)

    def test_current_owner_command_must_exist(self):
        target = "scripts/qa.py"
        findings = self.validate(".agents/README.md", f"Run `python3 {target}`")
        self.assertEqual([finding.code for finding in findings], ["EXECUTABLE-CURRENT"])
        self.write(target)
        self.assertEqual(
            self.validate(
                ".agents/README.md", f"Run `python3 {target}`", tracked=(target,)
            ),
            (),
        )

    def test_missing_current_reference_is_not_waived_by_git_history(self) -> None:
        target = "scripts/validation/document/check-contract.py"
        recovered: list[PurePosixPath] = []

        diagnostics = self.validate(
            ".agents/README.md",
            f"Run `python3 {target}`.\n",
            historical_path_exists=lambda path: recovered.append(path) or True,
        )

        self.assertEqual([item.code for item in diagnostics], ["EXECUTABLE-CURRENT"])
        self.assertEqual(recovered, [])

    def test_changelog_reference_uses_git_first_recovery(self) -> None:
        target = PurePosixPath("scripts/validate-retired-gates.sh")
        recovered: list[PurePosixPath] = []
        text = f"# Changelog\n\n## [0.1.0] - 2026-10-28\n\n- Add {target} checks.\n"

        diagnostics = self.validate(
            "CHANGELOG.md",
            text,
            historical_path_exists=lambda path: recovered.append(path) or True,
        )
        self.assertEqual(diagnostics, ())
        self.assertEqual(recovered, [target])

        lost = self.validate("CHANGELOG.md", text)
        self.assertEqual([item.code for item in lost], ["EXECUTABLE-HISTORY"])

    def test_completed_task_reference_uses_git_first_recovery(self) -> None:
        target = PurePosixPath("scripts/retired/deep/check-contract.py")
        recovered: list[PurePosixPath] = []
        diagnostics = self.validate(
            "docs/03.specs/0001-example/tasks/tsk-0001-example.md",
            f"---\nstatus: completed\n---\n\nHistorical command: `python3 {target}`.\n",
            historical_path_exists=lambda path: recovered.append(path) or True,
        )
        self.assertEqual(diagnostics, ())
        self.assertEqual(recovered, [target])

    def test_draft_spec_proposal_does_not_claim_a_current_executable(self) -> None:
        invoked: list[PurePosixPath] = []
        diagnostics = self.validate(
            "docs/03.specs/0001-example/spec.md",
            "---\nstatus: draft\n---\n\n"
            "Proposed: `scripts/future/deep/check-contract.py`.\n",
            historical_path_exists=lambda path: invoked.append(path) or True,
        )

        self.assertEqual(diagnostics, ())
        self.assertEqual(invoked, [])

    def test_unrecoverable_terminal_reference_fails_closed(self) -> None:
        target = "scripts/retired/deep/check-contract.sh"
        diagnostics = self.validate(
            "docs/03.specs/0001-example/plan.md",
            f"---\nstatus: cancelled\n---\n\nHistorical: `{target}`.\n",
        )

        self.assertEqual([item.code for item in diagnostics], ["EXECUTABLE-HISTORY"])

    def test_terminal_statuses_are_the_registry_terminal_states_and_accepted(
        self,
    ) -> None:
        registry = json.loads(
            (ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8")
        )
        terminal = {
            state
            for domain in registry["lifecycle_domains"]
            for state, kind in domain["states"].items()
            if kind == "terminal"
        }
        self.assertEqual(references._TERMINAL_STATUSES, terminal | {"accepted"})

    def test_rejected_superseded_and_retired_references_use_git_first_recovery(
        self,
    ) -> None:
        target = PurePosixPath("scripts/retired/deep/check-contract.py")
        for source, status in (
            ("docs/02.architecture/decisions/0001-example.md", "rejected"),
            (".agents/governance/example.md", "superseded"),
            ("docs/05.operations/guides/example.md", "retired"),
        ):
            with self.subTest(status=status):
                recovered: list[PurePosixPath] = []
                diagnostics = self.validate(
                    source,
                    f"---\nstatus: {status}\n---\n\nHistorical: `{target}`.\n",
                    historical_path_exists=lambda path: recovered.append(path) or True,
                )
                self.assertEqual(diagnostics, ())
                self.assertEqual(recovered, [target])

    def test_archive_reference_is_not_checked(self) -> None:
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

    def test_repository_aggregate_delegates_instead_of_reimplementing_rule(
        self,
    ) -> None:
        aggregate = (ROOT / "scripts/qa.py").read_text(encoding="utf-8")
        owner = (ROOT / "scripts/validation/repository/quality.py").read_text(
            encoding="utf-8"
        )
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
