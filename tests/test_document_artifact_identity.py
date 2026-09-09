"""Focused path, uniqueness, and retired artifact identity regressions."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def load_module(name: str, path: Path):
    scripts = str(SCRIPTS)
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


MARKDOWN = load_module(
    "artifact_identity_markdown", SCRIPTS / "validate-markdown-profiles.py"
)
LIFECYCLE = importlib.import_module("document_lifecycle")
LIFECYCLE_VALIDATOR = load_module(
    "artifact_identity_lifecycle_validator",
    SCRIPTS / "validate-document-lifecycle.py",
)


class PathArtifactIdentityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = MARKDOWN.load_registry(ROOT)
        cls.profiles = {
            profile.profile_id: profile for profile in cls.registry.profiles
        }
        cls.cases = {
            "sdlc/requirement": (
                "docs/01.requirements/0072-example.md",
                "REQ-0072",
            ),
            "sdlc/architecture-description": (
                "docs/02.architecture/descriptions/0072-example.md",
                "AD-0072",
            ),
            "sdlc/architecture-decision": (
                "docs/02.architecture/decisions/0072-example.md",
                "ADR-0072",
            ),
            "sdlc/spec": (
                "docs/98.archive/completed/03.specs/0072-example/spec.md",
                "SPEC-0072",
            ),
            "sdlc/plan": (
                "docs/03.specs/0072-example/plan.md",
                "SPEC-0072-PLAN-0001",
            ),
            "sdlc/task": (
                "docs/03.specs/0072-example/tasks/tsk-0002-example.md",
                "SPEC-0072-TSK-0002",
            ),
            "operation/guide": (
                "docs/05.operations/guides/0072-example.md",
                "GDE-0072",
            ),
            "operation/policy": (
                "docs/05.operations/policies/0072-example.md",
                "POL-0072",
            ),
            "operation/runbook": (
                "docs/05.operations/runbooks/0072-example.md",
                "RUN-0072",
            ),
            "operation/incident": (
                "docs/05.operations/incidents/2026/inc-0072-example/incident.md",
                "inc-2026-0072",
            ),
            "operation/postmortem": (
                "docs/05.operations/incidents/2026/inc-0072-example/postmortem.md",
                "inc-2026-0072-PM",
            ),
            "reference/audit": (
                "docs/90.references/audits/0072-example/m0002-example.md",
                "AUD-0072-m0002",
            ),
            "reference/research": (
                "docs/90.references/research/0072-example/m0002-example.md",
                "RES-0072-m0002",
            ),
            "reference/data": (
                "docs/90.references/data/0072-example/m0002-example.md",
                "DATA-0072-m0002",
            ),
            "archive/migration": (
                "docs/98.archive/migrations/0072-example.md",
                "MIG-0072",
            ),
        }

    def test_every_registered_numbered_authored_profile_is_path_bound(self) -> None:
        authored = {
            profile.profile_id
            for profile in self.registry.profiles
            if profile.mode == "authored" and profile.artifact_id_pattern is not None
        }
        self.assertEqual(set(self.cases) - {"archive/migration"}, authored)
        for profile_id, (raw_path, expected) in self.cases.items():
            with self.subTest(profile=profile_id):
                profile = self.profiles[profile_id]
                path = PurePosixPath(raw_path)
                self.assertEqual(MARKDOWN.classify_path(self.registry, path), profile)
                self.assertEqual(MARKDOWN.expected_artifact_id(path, profile), expected)

    def test_wrong_but_pattern_valid_ids_fail_for_each_numbered_profile(self) -> None:
        for profile_id, (raw_path, expected) in self.cases.items():
            with self.subTest(profile=profile_id):
                profile = self.profiles[profile_id]
                wrong = expected.replace("0072", "0073", 1)
                diagnostics = MARKDOWN.artifact_identity_diagnostics(
                    PurePosixPath(raw_path), profile, {"artifact_id": wrong}
                )
                expected_rule = (
                    "REQUIREMENT-PACKAGE-IDENTITY"
                    if profile_id == "sdlc/requirement"
                    else "ARTIFACT-IDENTITY"
                )
                self.assertEqual(
                    [item.rule_id for item in diagnostics], [expected_rule]
                )
                self.assertIn(expected, diagnostics[0].expected)

    def test_template_placeholders_and_tombstone_payload_ids_are_not_current_ids(
        self,
    ) -> None:
        template_profile = self.profiles["common/template-sdlc-spec"]
        template_path = template_profile.template
        self.assertIsNotNone(template_path)
        template_text = (ROOT / template_path).read_text(encoding="utf-8")
        tombstone_path = PurePosixPath(
            "docs/98.archive/superseded/01.requirements/"
            "0007-repository-delivery-and-platform-assurance.md"
        )
        tombstone_profile = MARKDOWN.classify_path(self.registry, tombstone_path)
        tombstone_text = (ROOT / tombstone_path).read_text(encoding="utf-8")
        identities = MARKDOWN.current_artifact_identities(
            (
                (template_path, template_profile, template_text),
                (template_path, template_profile, template_text),
                (tombstone_path, tombstone_profile, tombstone_text),
            )
        )
        self.assertEqual(
            identities,
            ((tombstone_path, "tomb-REQ-0007"),),
        )

    def test_partial_include_still_detects_duplicate_current_id(self) -> None:
        with tempfile.TemporaryDirectory(prefix="artifact-identity-") as temporary:
            root = Path(temporary)
            shutil.copytree(ROOT / "docs/99.templates", root / "docs/99.templates")
            source = (
                ROOT / "docs/02.architecture/descriptions/"
                "0004-argo-rollouts-progressive-delivery.md"
            ).read_text(encoding="utf-8")
            paths = (
                "docs/02.architecture/descriptions/0004-alpha.md",
                "docs/02.architecture/descriptions/0004-beta.md",
            )
            for path in paths:
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(source, encoding="utf-8")
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            subprocess.run(["git", "add", "--", *paths], cwd=root, check=True)
            stdout, stderr = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                result = MARKDOWN.main(
                    ["--root", str(root), "--include-path", paths[0]]
                )
            self.assertEqual(result, 1, stderr.getvalue() or stdout.getvalue())
            self.assertEqual(stdout.getvalue().count("ARTIFACT-IDENTITY-DUPLICATE"), 2)


class RetiredArtifactIdentityTest(unittest.TestCase):
    def document(
        self,
        path: str,
        artifact_id: str | None,
        *,
        profile: str = "sdlc/architecture-decision",
        original_artifact_id: str | None = None,
        original_path: str | None = None,
        replacement: str | None = None,
    ):
        return LIFECYCLE.LifecycleDocument(
            path=PurePosixPath(path),
            profile_id=profile,
            status=(
                "archived"
                if profile == "archive/tombstone"
                else "sealed"
                if profile == "archive/migration"
                else "accepted"
            ),
            artifact_id=artifact_id,
            original_artifact_id=original_artifact_id,
            original_path=None
            if original_path is None
            else PurePosixPath(original_path),
            replacement=None if replacement is None else PurePosixPath(replacement),
        )

    def diagnostics(self, base, proposed, lineages=()):
        return LIFECYCLE.artifact_identity_reuse_diagnostics(
            base,
            proposed,
            identity_lineages=frozenset(lineages),
            base_mode="staged",
        )

    def test_unrelated_new_path_cannot_reuse_base_identity(self) -> None:
        old = self.document("docs/02.architecture/decisions/0072-old.md", "ADR-0072")
        new = self.document("docs/02.architecture/decisions/0072-new.md", "ADR-0072")
        diagnostics = self.diagnostics({old.path: old}, {new.path: new})
        self.assertEqual(
            [item.rule_id for item in diagnostics], ["LIFECYCLE-IDENTITY-REUSE"]
        )

    def test_verified_move_preserves_same_document_identity(self) -> None:
        old = self.document("docs/02.architecture/decisions/0072-old.md", "ADR-0072")
        new = self.document("docs/02.architecture/decisions/0072-new.md", "ADR-0072")
        lineage = LIFECYCLE.ArtifactIdentityLineage("ADR-0072", old.path, new.path)
        self.assertEqual(
            self.diagnostics({old.path: old}, {new.path: new}, (lineage,)), ()
        )

    def test_tombstone_original_id_is_reserved_but_outer_id_is_distinct(self) -> None:
        source = "docs/02.architecture/decisions/0072-old.md"
        target = "docs/02.architecture/decisions/0072-replacement.md"
        tombstone = self.document(
            "docs/98.archive/superseded/02.architecture/decisions/0072-old.md",
            "tomb-ADR-0072",
            profile="archive/tombstone",
            original_artifact_id="ADR-0072",
            original_path=source,
            replacement=target,
        )
        unrelated = self.document(
            "docs/02.architecture/decisions/0072-unrelated.md", "ADR-0072"
        )
        replacement = self.document(target, "ADR-0072")
        self.assertEqual(
            [
                item.rule_id
                for item in self.diagnostics(
                    {},
                    {
                        tombstone.path: tombstone,
                        unrelated.path: unrelated,
                    },
                )
            ],
            ["LIFECYCLE-IDENTITY-REUSE"],
        )
        self.assertEqual(
            self.diagnostics(
                {}, {tombstone.path: tombstone, replacement.path: replacement}
            ),
            (),
        )

    def test_verified_sealed_rows_reserve_sources_and_only_allow_exact_targets(
        self,
    ) -> None:
        migration_path = PurePosixPath(
            "docs/98.archive/migrations/0004-document-authority-convergence.md"
        )
        migration_text = (ROOT / migration_path).read_text(encoding="utf-8")
        migration = self.document(
            migration_path.as_posix(),
            "MIG-0004",
            profile="archive/migration",
        )
        events, diagnostics = LIFECYCLE_VALIDATOR._migration_lifecycle_events(
            ROOT,
            MARKDOWN.load_registry(ROOT),
            {},
            {},
            {},
            {migration_path: migration},
            {migration_path: migration_text},
            proposed_commit=None,
            mode="staged",
        )
        self.assertEqual(diagnostics, ())
        rows = LIFECYCLE_VALIDATOR.parse_pinned_migration_control(
            migration_path.as_posix(), migration_text.encode("utf-8")
        )
        expected_lineages = {
            LIFECYCLE.ArtifactIdentityLineage(
                str(row["artifact_id"]),
                PurePosixPath(str(row["legacy_path"])),
                PurePosixPath(str(row["stable_path"])),
            )
            for row in rows
            if row["action"] == "moved" and row["artifact_id"] is not None
        }
        self.assertTrue(any(row["artifact_id"] is None for row in rows))
        self.assertEqual(events.identity_lineages, expected_lineages)

        lineage = min(events.identity_lineages)
        exact_target = self.document(
            lineage.target_path.as_posix(), lineage.artifact_id
        )
        unrelated_target = self.document(
            "docs/02.architecture/decisions/9999-unrelated.md",
            lineage.artifact_id,
        )
        self.assertEqual(
            self.diagnostics(
                {}, {exact_target.path: exact_target}, events.identity_lineages
            ),
            (),
        )
        self.assertEqual(
            [
                item.rule_id
                for item in self.diagnostics(
                    {},
                    {unrelated_target.path: unrelated_target},
                    events.identity_lineages,
                )
            ],
            ["LIFECYCLE-IDENTITY-REUSE"],
        )


if __name__ == "__main__":
    unittest.main()
