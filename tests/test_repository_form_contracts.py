"""Negative boundaries for the repository's canonical form rules."""

import pathlib
import sys
import unittest
from types import SimpleNamespace

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validation.repository.form_contracts import (  # noqa: E402
    canonical_form_content_errors,
    canonical_form_contract_errors,
)
from validation.repository.sample_app_contract import (  # noqa: E402
    sample_app_copyset_errors,
    sample_app_yaml_filenames,
)


class CanonicalFormContractTests(unittest.TestCase):
    def test_ownership_rejects_missing_unowned_duplicate_and_noncanonical_forms(self):
        form = pathlib.PurePosixPath(
            "docs/99.templates/templates/common/example.template.md"
        )
        other = pathlib.PurePosixPath(
            "docs/99.templates/templates/common/extra.template.md"
        )
        bad_name = pathlib.PurePosixPath(
            "docs/99.templates/templates/common/openapi.yaml"
        )
        references = [("common/example", form)]
        owners = [("common/example", form)]
        self.assertEqual(canonical_form_contract_errors({form}, references, owners), [])
        cases = (
            (set(), owners, "registry-owned forms are missing"),
            ({form, other}, owners, "physical forms have no registry owner"),
            ({form}, owners + [("common/second", form)], "exactly one profile owner"),
            ({form, bad_name}, owners, "physical form filenames must match"),
        )
        for physical, changed_owners, expected in cases:
            with self.subTest(expected=expected):
                findings = canonical_form_contract_errors(
                    physical, references, changed_owners
                )
                self.assertTrue(any(expected in item for item in findings))

    def test_content_rejects_prompt_table_and_comment_drift(self):
        form = pathlib.PurePosixPath(
            "docs/99.templates/templates/common/example.template.md"
        )
        profile = SimpleNamespace(
            headings=SimpleNamespace(required=("Overview",)),
            body_contract=SimpleNamespace(
                table_heading="Lifecycle Traceability",
                required_columns=("ID", "Status"),
            ),
        )
        source = (
            "## Overview\n\n<!-- Author prompt: Explain the current owner. -->\n\n"
            "### Lifecycle Traceability\n\n| ID | Status |\n"
        )
        owners = [("common/example", form)]
        profiles = {"common/example": profile}

        def check(value):
            return canonical_form_content_errors({form: value}, owners, profiles)

        self.assertEqual(check(source), [])
        mutations = (
            (
                source.replace("Author prompt", "Generic prompt"),
                "non-author form comment",
            ),
            (
                source.replace("Lifecycle Traceability", "Other Traceability"),
                "lifecycle table",
            ),
            (
                source.replace(
                    "<!-- Author prompt: Explain the current owner. -->", ""
                ),
                "useful Author prompt",
            ),
            (source + "<!-- Target: docs/example.md -->\n", "retired form residue"),
            (source + "<!-- unclosed", "unbalanced HTML comment"),
        )
        for changed, expected in mutations:
            with self.subTest(expected=expected):
                self.assertTrue(any(expected in item for item in check(changed)))
        self.assertEqual(canonical_form_content_errors({}, owners, profiles), [])

    def test_archive_comment_markers_are_exact_allowlist(self):
        form = pathlib.PurePosixPath(
            "docs/99.templates/templates/archive/example.template.md"
        )
        envelope = (
            "<!-- archive-envelope:v1 payload=rest-of-file encoding=git-blob-bytes -->"
        )
        migration = "<!-- archive-migration-ledger:v1 format=json -->"
        source = f"{envelope}\n{migration}\n"
        self.assertEqual(canonical_form_content_errors({form: source}, [], {}), [])
        for marker in (envelope, migration):
            with self.subTest(marker=marker):
                changed = (
                    source.replace(":v1", ":v2", 1)
                    if marker == envelope
                    else source.replace(
                        "archive-migration-ledger:v1", "archive-migration-ledger:v2"
                    )
                )
                self.assertTrue(
                    any(
                        "non-author form comment" in item
                        for item in canonical_form_content_errors(
                            {form: changed}, [], {}
                        )
                    )
                )


class SampleAppCopysetTests(unittest.TestCase):
    def test_resources_and_commented_optional_file_define_yaml_copyset(self):
        source = (
            "resources:\n  - rollout.yaml\n  - service.yaml\n"
            "  # - external-secret.yaml\n"
        )
        parsed = {"resources": ["rollout.yaml", "service.yaml"]}
        expected = {
            "kustomization.yaml",
            "rollout.yaml",
            "service.yaml",
            "external-secret.yaml",
        }
        self.assertEqual(sample_app_yaml_filenames(parsed, source), expected)
        self.assertEqual(sample_app_copyset_errors(expected, parsed, source), [])
        self.assertTrue(
            sample_app_copyset_errors(expected | {"surprise.yaml"}, parsed, source)
        )
        self.assertTrue(
            sample_app_copyset_errors(
                expected - {"external-secret.yaml"}, parsed, source
            )
        )

    def test_resource_paths_and_optional_declarations_are_bounded(self):
        source = "resources:\n  - rollout.yaml\n  # - external-secret.yaml\n"
        for invalid in (
            "../outside.yaml",
            "nested/file.yaml",
            "/outside.yaml",
            "other.yml",
        ):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    sample_app_yaml_filenames({"resources": [invalid]}, source)
        with self.assertRaises(ValueError):
            sample_app_yaml_filenames(
                {"resources": ["rollout.yaml", "rollout.yaml"]}, source
            )
