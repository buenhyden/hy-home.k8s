"""The approved completed spelling preserves frozen and historical evidence."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from archive_validation import (  # noqa: E402
    CurrentMarkdownDocument,
    validate_current_archive_authority,
)
from document_contracts import load_registry  # noqa: E402
from tests.git_fixture import GitFixture  # noqa: E402
from tests.test_document_lifecycle_archive_cutover import VALIDATOR  # noqa: E402
from document_lifecycle import compare_lifecycle, document_from_text  # noqa: E402


class CompletedStateMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_registry(ROOT)

    def document(self, path: str, profile: str, status: str, **kwargs):
        return document_from_text(
            self.registry,
            PurePosixPath(path),
            f"---\ntype: {profile}\nstatus: {status}\n---\n\n# Fixture\n",
            **kwargs,
        )

    def test_current_contract_admits_completed_and_rejects_done(self) -> None:
        cases = (
            ("sdlc/spec", "docs/03.specs/9999-example/spec.md"),
            ("sdlc/plan", "docs/03.specs/9999-example/plan.md"),
            (
                "sdlc/task",
                "docs/03.specs/9999-example/tasks/tsk-0001-example.md",
            ),
        )
        for profile, path in cases:
            with self.subTest(profile=profile):
                completed = self.document(path, profile, "completed")
                done = self.document(path, profile, "done")
                self.assertEqual(
                    compare_lifecycle(
                        self.registry,
                        {
                            completed.path: self.document(
                                path,
                                profile,
                                "active" if profile != "sdlc/task" else "in-progress",
                            )
                        },
                        {completed.path: completed},
                        base_mode="staged",
                    ),
                    (),
                )
                self.assertEqual(
                    [
                        item.rule_id
                        for item in compare_lifecycle(
                            self.registry, {}, {done.path: done}, base_mode="staged"
                        )
                    ],
                    ["LIFECYCLE-STATE"],
                )
                self.assertEqual(
                    [
                        item.rule_id
                        for item in compare_lifecycle(
                            self.registry,
                            {},
                            {completed.path: completed},
                            base_mode="staged",
                        )
                    ],
                    ["LIFECYCLE-CREATE"],
                )

    def test_historical_done_normalizes_only_for_approved_profiles(self) -> None:
        path = "docs/03.specs/9999-example/spec.md"
        old = self.document(path, "sdlc/spec", "done", legacy_completion=True)
        current = self.document(path, "sdlc/spec", "completed")
        self.assertEqual(old.status, "completed")
        self.assertEqual(
            compare_lifecycle(
                self.registry,
                {old.path: old},
                {current.path: current},
                base_mode="staged",
            ),
            (),
        )
        self.assertEqual(self.document(path, "sdlc/spec", "done").status, "done")
        incident = self.document(
            "docs/05.operations/incidents/2026/inc-9999-example/incident.md",
            "operation/incident",
            "done",
            legacy_completion=True,
        )
        self.assertEqual(incident.status, "done")

    def test_frozen_retained_done_is_readable_without_rewriting(self) -> None:
        frozen = self.document(
            "docs/98.archive/completed/03.specs/9999-example/spec.md",
            "sdlc/spec",
            "done",
        )
        self.assertEqual(frozen.status, "completed")

    def test_archive_authority_accepts_frozen_done_but_rejects_live_done(self) -> None:
        frozen = "docs/98.archive/completed/03.specs/9999-example/spec.md"
        live = "docs/03.specs/9999-example/spec.md"
        for path, expected in ((frozen, False), (live, True)):
            with self.subTest(path=path):
                report = validate_current_archive_authority(
                    [CurrentMarkdownDocument(path, "# Fixture\n", "sdlc/spec", "done")],
                    individual_archive_paths=frozenset(),
                    registry=self.registry,
                )
                codes = {item.code for item in report.diagnostics}
                self.assertEqual("ARCHIVE-CURRENT-STATUS-INVALID" in codes, expected)

    def test_terminal_cannot_reopen_or_masquerade_as_unrelated_edge(self) -> None:
        path = "docs/03.specs/9999-example/spec.md"
        old = self.document(path, "sdlc/spec", "done", legacy_completion=True)
        for target, rule in (("draft", "LIFECYCLE-EDGE"), ("done", "LIFECYCLE-STATE")):
            with self.subTest(target=target):
                proposed = self.document(path, "sdlc/spec", target)
                self.assertEqual(
                    [
                        item.rule_id
                        for item in compare_lifecycle(
                            self.registry,
                            {old.path: old},
                            {proposed.path: proposed},
                            base_mode="staged",
                        )
                    ],
                    [rule],
                )

    def test_cumulative_replay_uses_each_commits_registry_generation(self) -> None:
        registry_path = "docs/99.templates/registry.json"
        current_bytes = (ROOT / registry_path).read_bytes()
        old = json.loads(current_bytes)
        for profile in old["profiles"]:
            if profile["id"] in {"sdlc/spec", "sdlc/plan", "sdlc/task"}:
                states = profile["lifecycle"]["status_domain"]
                states[states.index("completed")] = "done"
        for domain in old["lifecycle_domains"]:
            if domain["family"] in {"spec-plan", "task"}:
                domain["states"]["done"] = domain["states"].pop("completed")
                domain["transitions"] = [
                    ["done" if state == "completed" else state for state in edge]
                    for edge in domain["transitions"]
                ]
        with tempfile.TemporaryDirectory(prefix="completed-generation-") as raw:
            root = Path(raw)
            git = GitFixture(root)
            base, _ = git.commit(registry_path, json.dumps(old).encode())
            path = "docs/03.specs/9999-example/spec.md"

            def body(status: str) -> bytes:
                return f"---\ntype: sdlc/spec\nstatus: {status}\n---\n\n# Fixture\n".encode()

            for status in ("draft", "active", "done"):
                git.commit(path, body(status))
            migrated, _ = git.commit_many(
                {registry_path: current_bytes, path: body("completed")}
            )
            self.assertTrue(
                VALIDATOR._history_proves_cumulative_create(
                    root, self.registry, PurePosixPath(path), base, migrated
                )
            )
            future = "docs/03.specs/9998-future/spec.md"
            for status in ("draft", "active", "done"):
                illegal, _ = git.commit(future, body(status))
            self.assertFalse(
                VALIDATOR._history_proves_cumulative_create(
                    root, self.registry, PurePosixPath(future), migrated, illegal
                )
            )


if __name__ == "__main__":
    unittest.main()
