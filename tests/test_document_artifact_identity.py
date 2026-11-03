"""Focused path, uniqueness, and retired artifact identity regressions."""

from __future__ import annotations

import contextlib
import dataclasses
import datetime as dt
import importlib.util
import io
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
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
                "docs/03.specs/0072-example/spec.md",
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
            "reference/audit-pack": (
                "docs/90.references/audits/0072-example/README.md",
                "AUD-0072",
            ),
            "reference/research": (
                "docs/90.references/research/0072-example/m0002-example.md",
                "RES-0072-m0002",
            ),
            "reference/research-pack": (
                "docs/90.references/research/0072-example/README.md",
                "RES-0072",
            ),
            "reference/data": (
                "docs/90.references/data/0072-example/m0002-example.md",
                "DATA-0072-m0002",
            ),
            "reference/data-pack": (
                "docs/90.references/data/0072-example/README.md",
                "DATA-0072",
            ),
        }

        cls.pattern_owned = frozenset(
            {
                "reference/audit-pack",
                "reference/research-pack",
                "reference/data-pack",
            }
        )

    def test_registered_numbered_profiles_have_declared_identity_contracts(
        self,
    ) -> None:
        authored = {
            profile.profile_id
            for profile in self.registry.profiles
            if profile.mode == "authored" and profile.artifact_id_pattern is not None
        }
        self.assertEqual(set(self.cases), authored)
        for profile_id, (raw_path, expected) in self.cases.items():
            with self.subTest(profile=profile_id):
                profile = self.profiles[profile_id]
                path = PurePosixPath(raw_path)
                self.assertEqual(MARKDOWN.classify_path(self.registry, path), profile)
                derived = None if profile_id in self.pattern_owned else expected
                self.assertEqual(MARKDOWN.expected_artifact_id(path, profile), derived)
                self.assertRegex(expected, profile.artifact_id_pattern)

    @staticmethod
    def _pattern_diagnostics(path, profile, artifact_id):
        text = (ROOT / profile.template).read_text(encoding="utf-8")
        for placeholder, value in {
            "ARTIFACT_ID": artifact_id,
            "OWNER": "platform",
            "UPDATED": "2026-10-05",
            "RETIRED_ROUTE": "docs/legacy.md",
        }.items():
            text = text.replace("{{" + placeholder + "}}", value)
        text = re.sub(r"\{\{[A-Z_]+\}\}", "Fixture", text)
        return [
            diagnostic
            for diagnostic in MARKDOWN.validate_document_text(
                text, path, profile, "strict"
            )
            if diagnostic.expected.startswith("artifact_id matches ")
        ]

    def test_wrong_but_pattern_valid_ids_fail_for_each_numbered_profile(self) -> None:
        for profile_id, (raw_path, expected) in self.cases.items():
            with self.subTest(profile=profile_id):
                profile = self.profiles[profile_id]
                wrong = expected.replace("0072", "0073", 1)
                diagnostics = MARKDOWN.artifact_identity_diagnostics(
                    PurePosixPath(raw_path), profile, {"artifact_id": wrong}
                )
                if profile_id in self.pattern_owned:
                    # These owners declare an identity pattern, without a
                    # path-derived identity. Exercise the normal value guard.
                    self.assertEqual(diagnostics, [])
                    self.assertEqual(
                        self._pattern_diagnostics(
                            PurePosixPath(raw_path), profile, wrong
                        ),
                        [],
                    )
                    malformed = self._pattern_diagnostics(
                        PurePosixPath(raw_path), profile, "INVALID"
                    )
                    self.assertEqual(
                        [item.rule_id for item in malformed], ["FM-VALUE-PATTERN"]
                    )
                    continue
                expected_rule = (
                    "REQUIREMENT-PACKAGE-IDENTITY"
                    if profile_id == "sdlc/requirement"
                    else "ARTIFACT-IDENTITY"
                )
                self.assertEqual(
                    [item.rule_id for item in diagnostics], [expected_rule]
                )
                self.assertIn(expected, diagnostics[0].expected)

    def test_template_placeholders_are_not_current_ids(self) -> None:
        template_profile = self.profiles["common/template-sdlc-spec"]
        template_path = template_profile.template
        self.assertIsNotNone(template_path)
        template_text = (ROOT / template_path).read_text(encoding="utf-8")
        identities = MARKDOWN.current_artifact_identities(
            (
                (template_path, template_profile, template_text),
                (template_path, template_profile, template_text),
            )
        )
        self.assertEqual(identities, ())

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
    @staticmethod
    def document(path: str, artifact_id: str | None):
        return LIFECYCLE.LifecycleDocument(
            path=PurePosixPath(path),
            profile_id="sdlc/architecture-decision",
            status="accepted",
            artifact_id=artifact_id,
        )

    def test_unrelated_new_path_cannot_reuse_base_identity(self) -> None:
        old = self.document("docs/02.architecture/decisions/0072-old.md", "ADR-0072")
        new = self.document("docs/02.architecture/decisions/0072-new.md", "ADR-0072")
        diagnostics = LIFECYCLE.artifact_identity_reuse_diagnostics(
            {old.path: old}, {new.path: new}, base_mode="staged"
        )
        self.assertEqual(
            [item.rule_id for item in diagnostics], ["LIFECYCLE-IDENTITY-REUSE"]
        )


class ScopedDocumentMetadataTests(unittest.TestCase):
    def test_scoped_cli_keeps_global_duplicate_identity_and_pending_census(self):
        unrelated = PurePosixPath("docs/03.specs/0140-archive-check-removal/plan.md")
        selected = (
            "docs/03.specs/0140-archive-check-removal/tasks/"
            "tsk-0001-archive-check-removal.md"
        )
        source_registry = MARKDOWN.load_registry(ROOT)
        language = dataclasses.replace(
            source_registry.document_language,
            pending_paths=frozenset({unrelated}),
        )
        registry = dataclasses.replace(source_registry, document_language=language)
        original_read = MARKDOWN.read_repository_text

        def duplicate_identity(root, path):
            text = original_read(root, path)
            if path == unrelated:
                return text.replace(
                    'artifact_id: "SPEC-0140-PLAN-0001"', 'artifact_id: "SPEC-0140"', 1
                )
            return text

        output = io.StringIO()
        with (
            mock.patch.object(MARKDOWN, "load_registry", return_value=registry),
            mock.patch.object(
                MARKDOWN, "read_repository_text", side_effect=duplicate_identity
            ),
            contextlib.redirect_stdout(output),
        ):
            code = MARKDOWN.main(
                (
                    "--root",
                    str(ROOT),
                    "--format",
                    "json",
                    "--change-scope",
                    f"--changed-path={selected}",
                )
            )
        self.assertEqual(code, 1)
        self.assertIn("ARTIFACT-IDENTITY-DUPLICATE", output.getvalue())
        self.assertIn("LANG-PENDING", output.getvalue())

    def test_change_scope_cli_rejects_zero_malformed_and_explicit_audit(self):
        for options in (
            ("--change-scope",),
            ("--changed-path=docs/README.md",),
            ("--change-scope", "--changed-path=docs//README.md"),
            (
                "--change-scope",
                "--changed-path=docs/README.md",
                "--body-contracts=audit",
            ),
        ):
            with (
                self.subTest(options=options),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                self.assertEqual(MARKDOWN.main(options), 2)

    def test_unselected_body_is_skipped_but_malformed_frontmatter_still_fails(self):
        path = PurePosixPath(
            "docs/03.specs/0140-archive-check-removal/tasks/tsk-0001-archive-check-removal.md"
        )
        registry = MARKDOWN.load_registry(ROOT)
        profile = MARKDOWN.classify_path(registry, path)
        source = (ROOT / path).read_text(encoding="utf-8")
        self.assertIn("## Task Evidence", source)
        broken = source.replace("## Task Evidence", "## Missing Evidence", 1)
        broken = broken.replace('owner: "platform"', "owner: 3", 1)
        full = MARKDOWN.validate_document_text(
            broken, path, profile, "strict", today=dt.date(2026, 10, 9)
        )
        metadata_only = MARKDOWN.validate_document_text(
            broken,
            path,
            profile,
            "strict",
            today=dt.date(2026, 10, 9),
            include_body=False,
        )
        self.assertIn("TASK-EVIDENCE-COLUMNS", {item.rule_id for item in full})
        self.assertIn("FM-OWNER", {item.rule_id for item in metadata_only})
        self.assertNotIn(
            "TASK-EVIDENCE-COLUMNS", {item.rule_id for item in metadata_only}
        )


if __name__ == "__main__":
    unittest.main()
