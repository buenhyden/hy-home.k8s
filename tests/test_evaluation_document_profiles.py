"""Evaluation evidence paths have explicit, non-grading document contracts."""

from pathlib import Path, PurePosixPath
import importlib.util
import re
import sys
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import document_contracts as contracts  # noqa: E402

SPEC = importlib.util.spec_from_file_location(
    "evaluation_markdown_profiles", ROOT / "scripts/validate-markdown-profiles.py"
)
assert SPEC is not None and SPEC.loader is not None
MARKDOWN = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MARKDOWN
SPEC.loader.exec_module(MARKDOWN)

REGISTRY_SPEC = importlib.util.spec_from_file_location(
    "evaluation_registry_validator",
    ROOT / "scripts/validate-document-contract-registry.py",
)
assert REGISTRY_SPEC is not None and REGISTRY_SPEC.loader is not None
REGISTRY_VALIDATOR = importlib.util.module_from_spec(REGISTRY_SPEC)
sys.modules[REGISTRY_SPEC.name] = REGISTRY_VALIDATOR
REGISTRY_SPEC.loader.exec_module(REGISTRY_VALIDATOR)


class EvaluationDocumentProfilesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = contracts.load_registry(ROOT)

    def test_each_supported_path_has_exactly_one_profile(self) -> None:
        expected = {
            ".agents/evaluations/results.md": "evaluation/results",
            ".agents/evaluations/harnesses/example-pair/task.md": "evaluation/task",
            ".agents/evaluations/harnesses/example-pair/score.md": "evaluation/score",
            ".agents/evaluations/harnesses/example-pair/baseline.md": "evaluation/raw-output",
            ".agents/evaluations/harnesses/example-pair/with-skill.md": "evaluation/raw-output",
        }
        for path, profile_id in expected.items():
            with self.subTest(path=path):
                self.assertEqual(
                    contracts.classify_path(
                        self.registry, PurePosixPath(path)
                    ).profile_id,
                    profile_id,
                )

    def test_unsupported_evaluation_files_have_no_fallback_route(self) -> None:
        for path in (
            ".agents/evaluations/harnesses/example-pair/unknown.md",
            ".agents/evaluations/harnesses/example-pair/nested/task.md",
            ".agents/evaluations/harnesses/BadID/task.md",
        ):
            with (
                self.subTest(path=path),
                self.assertRaises(contracts.DocumentContractError),
            ):
                contracts.classify_path(self.registry, PurePosixPath(path))

    def test_non_markdown_language_inputs_do_not_enter_raw_output_profile(self) -> None:
        self.assertFalse(
            contracts.is_opaque_evaluation_output(
                self.registry, PurePosixPath(".agents/roles/registry.json")
            )
        )
        self.assertFalse(
            contracts.is_opaque_evaluation_output(
                self.registry, PurePosixPath(".agents/evaluations/results.md")
            )
        )

    def test_raw_output_is_bounded_opaque_data_and_never_rewritten(self) -> None:
        path = PurePosixPath(".agents/evaluations/harnesses/example-pair/baseline.md")
        profile = contracts.classify_path(self.registry, path)
        raw = b"---\nstatus: active\n---\n[bogus](missing.md)\xff\t\r\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / path
            target.parent.mkdir(parents=True)
            target.write_bytes(raw)
            self.assertEqual(
                MARKDOWN.validate_document(root, path, profile, "strict"), []
            )
            self.assertEqual(target.read_bytes(), raw)
            target.unlink()
            target.symlink_to(root / "other.md")
            with self.assertRaises(ValueError):
                contracts.verify_opaque_evaluation_output(root, path)

    def test_raw_output_size_cap_applies_without_utf8_decode(self) -> None:
        path = PurePosixPath(".agents/evaluations/harnesses/example-pair/with-skill.md")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / path
            target.parent.mkdir(parents=True)
            with target.open("wb") as stream:
                stream.truncate(contracts.DOCUMENT_TEXT_MAX_BYTES + 1)
            with self.assertRaises(ValueError):
                contracts.verify_opaque_evaluation_output(root, path)

    def test_forms_keep_six_key_envelope_and_required_headings(self) -> None:
        for kind in ("task", "score", "results"):
            path = PurePosixPath(
                f"docs/99.templates/templates/evaluations/evaluation-{kind}.template.md"
            )
            profile = contracts.classify_path(self.registry, path)
            text = (ROOT / path).read_text(encoding="utf-8")
            with self.subTest(kind=kind):
                self.assertEqual(
                    MARKDOWN.validate_document_text(text, path, profile, "strict"), []
                )
                first_heading = profile.headings.required[1]
                malformed = text.replace(
                    f"## {first_heading}", "## Unsupported Heading", 1
                )
                rules = {
                    diagnostic.rule_id
                    for diagnostic in MARKDOWN.validate_document_text(
                        malformed, path, profile, "strict"
                    )
                }
                self.assertIn("BODY-HEADING-REQUIRED", rules)

    def test_evaluation_forms_inherit_one_terminal_source_profile(self) -> None:
        REGISTRY_VALIDATOR._assert_template_source_parity(self.registry)

    def test_format_exclusion_is_limited_to_the_two_raw_output_names(self) -> None:
        hooks = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text())
        precommit = next(
            repo for repo in hooks["repos"] if "pre-commit-hooks" in repo["repo"]
        )
        formatting = {
            hook["id"]: hook
            for hook in precommit["hooks"]
            if hook["id"]
            in {"end-of-file-fixer", "mixed-line-ending", "trailing-whitespace"}
        }
        self.assertEqual(len(formatting), 3)
        raw = ".agents/evaluations/harnesses/example-pair/baseline.md"
        authored = ".agents/evaluations/harnesses/example-pair/task.md"
        unsupported = ".agents/evaluations/harnesses/BadID/baseline.md"
        for hook in formatting.values():
            pattern = re.compile(hook["exclude"])
            self.assertIsNotNone(pattern.fullmatch(raw))
            self.assertIsNone(pattern.fullmatch(authored))
            self.assertIsNone(pattern.fullmatch(unsupported))
        lint = yaml.safe_load((ROOT / ".markdownlint-cli2.yaml").read_text())
        self.assertIn(".agents/evaluations/harnesses/*/baseline.md", lint["ignores"])
        self.assertIn(".agents/evaluations/harnesses/*/with-skill.md", lint["ignores"])


if __name__ == "__main__":
    unittest.main()
