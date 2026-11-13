"""SPEC-0183: the one YAML 1.2 frontmatter loader and its five call sites."""

from __future__ import annotations

import ast
import importlib.util
import re
import sys
import tempfile
import types
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import document_contracts as CONTRACTS  # noqa: E402
import document_lifecycle as LIFECYCLE  # noqa: E402
from frontmatter_yaml import FrontmatterError, load_frontmatter  # noqa: E402


def _load_script(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


MARKDOWN = _load_script("frontmatter_yaml_markdown", "validate-markdown-profiles.py")
AGENT_GOVERNANCE = _load_script(
    "frontmatter_yaml_agent_governance", "validate-agent-governance.py"
)
LINKS = _load_script("frontmatter_yaml_links", "validate-links-and-owners.py")

SPEC_PATH = PurePosixPath("docs/03.specs/0999-example/spec.md")


class LoaderRefusalTests(unittest.TestCase):
    def refusal(self, text: str) -> FrontmatterError:
        with self.assertRaises(FrontmatterError) as caught:
            load_frontmatter(text)
        return caught.exception

    def test_a_duplicate_key_is_refused_with_its_key(self) -> None:
        error = self.refusal("a: 1\nb: 2\na: 3\n")
        self.assertEqual((error.reason, error.key), ("duplicate-key", "a"))
        nested = self.refusal("outer:\n  k: 1\n  k: 2\n")
        self.assertEqual((nested.reason, nested.key), ("duplicate-key", "k"))

    def test_each_stated_refusal_has_its_reason_code(self) -> None:
        cases = {
            "directive": ("%YAML 1.1\n---\na: 1\n", "%FOO bar\n---\na: 1\n"),
            "anchor": ("a: &x 1\n", "a: &x [1]\n"),
            "alias": ("a: *x\n", "a: [*x]\n"),
            "non-scalar-key": ("? [a]\n: 1\n", "{a: 1}: 2\n"),
            "tag": ("a: !!str 1\n", "a: !custom 1\n", "a: ! 1\n", "!!map {a: 1}\n"),
            "merge-key": ("<<: {a: 1}\n", "base: {a: 1}\nb:\n  <<: {c: 2}\n"),
            "multi-document": ("a: 1\n---\nb: 2\n",),
            "invalid-yaml": ("a: [\n", "a: b: c\n"),
        }
        for reason, texts in cases.items():
            for text in texts:
                with self.subTest(reason=reason, text=text):
                    self.assertEqual(self.refusal(text).reason, reason)

    def test_nesting_that_overflows_the_stack_is_refused(self) -> None:
        self.assertEqual(self.refusal("a: " + "[" * 5000 + "\n").reason, "too-deep")

    def test_a_quoted_merge_marker_is_an_ordinary_key(self) -> None:
        self.assertEqual(load_frontmatter('"<<": 1\n'), {"<<": 1})

    def test_the_error_is_one_type_with_a_readable_message(self) -> None:
        self.assertIsInstance(self.refusal("a: *x\n"), ValueError)
        self.assertEqual(str(self.refusal("a: 1\na: 2\n")), "duplicate-key: a")


class LoaderValueTests(unittest.TestCase):
    def test_timestamps_stay_text(self) -> None:
        loaded = load_frontmatter(
            'date: 2026-11-13\nstamp: 2026-11-13T10:00:00Z\nquoted: "2026-11-13"\n'
        )
        self.assertEqual(
            loaded,
            {
                "date": "2026-11-13",
                "stamp": "2026-11-13T10:00:00Z",
                "quoted": "2026-11-13",
            },
        )

    def test_yaml_1_1_only_forms_are_strings(self) -> None:
        loaded = load_frontmatter("a: yes\nb: no\nc: on\nd: off\ne: 1:30\nf: y\n")
        self.assertEqual(
            loaded,
            {"a": "yes", "b": "no", "c": "on", "d": "off", "e": "1:30", "f": "y"},
        )
        self.assertEqual(
            load_frontmatter("a: true\nb: false\n"), {"a": True, "b": False}
        )

    def test_octal_forms_follow_yaml_1_2(self) -> None:
        loaded = load_frontmatter("a: 010\nb: 0o10\nc: 0x1F\n")
        self.assertEqual(loaded, {"a": 10, "b": 8, "c": 31})

    def test_the_numeric_extensions_are_accepted_deviations(self) -> None:
        self.assertEqual(load_frontmatter("a: 1_000\nb: 0b11\n"), {"a": 1000, "b": 3})

    def test_values_are_plain_python_and_empty_is_none(self) -> None:
        loaded = load_frontmatter("a: [1, two]\nb:\n  c: null\n")
        self.assertIs(type(loaded), dict)
        self.assertIs(type(loaded["a"]), list)
        self.assertIs(type(loaded["b"]), dict)
        self.assertIsNone(load_frontmatter(""))

    def test_key_order_is_kept(self) -> None:
        self.assertEqual(list(load_frontmatter("z: 1\na: 2\nm: 3\n")), ["z", "a", "m"])


class MissingLibraryTests(unittest.TestCase):
    def test_a_missing_library_names_the_lock_and_the_install_command(self) -> None:
        spec = importlib.util.spec_from_file_location(
            "frontmatter_yaml_missing", ROOT / "scripts/frontmatter_yaml.py"
        )
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        with mock.patch.dict(sys.modules, {"ruamel": None, "ruamel.yaml": None}):
            with self.assertRaises(ImportError) as caught:
                spec.loader.exec_module(module)
        message = str(caught.exception)
        self.assertIn(".github/requirements/ci-validation.txt", message)
        self.assertIn(".agents/governance/git.md", message)
        policy = (ROOT / ".agents/governance/git.md").read_text("utf-8")
        install = "--require-hashes -r .github/requirements/ci-validation.txt"
        self.assertIn(install, message)
        self.assertIn(install, policy)


class CallSiteDiagnosticTests(unittest.TestCase):
    @staticmethod
    def document(body: str) -> str:
        return f"---\n{body}---\n# Body\n"

    def test_profile_check_keeps_its_duplicate_key_diagnostic(self) -> None:
        with self.assertRaises(MARKDOWN.ContractError) as caught:
            MARKDOWN.extract_frontmatter(self.document("title: a\ntitle: b\n"))
        self.assertEqual(
            (caught.exception.rule_id, caught.exception.detail),
            ("FM-DUPLICATE-KEY", "title"),
        )

    def test_profile_check_reports_other_refusals_as_invalid_yaml(self) -> None:
        for body in ("a: &x 1\n", "a: !!str 1\n", "<<: {a: 1}\n", "? [a]\n: 1\n"):
            with self.subTest(body=body):
                with self.assertRaises(MARKDOWN.ContractError) as caught:
                    MARKDOWN.extract_frontmatter(self.document(body))
                self.assertEqual(
                    (caught.exception.rule_id, caught.exception.detail),
                    ("FM-KEYSET", "frontmatter YAML is invalid"),
                )

    def test_profile_check_keeps_timestamps_as_text_and_its_mapping_rule(self) -> None:
        keys, data, _ = MARKDOWN.extract_frontmatter(
            self.document("updated: 2026-11-13\n")
        )
        self.assertEqual((keys, data), (["updated"], {"updated": "2026-11-13"}))
        with self.assertRaises(MARKDOWN.ContractError) as caught:
            MARKDOWN.extract_frontmatter(self.document("- a\n"))
        self.assertEqual(caught.exception.rule_id, "FM-KEYSET")

    def lifecycle_state(self, body: str):
        registry = CONTRACTS.load_registry(ROOT)
        return LIFECYCLE.document_from_text(registry, SPEC_PATH, self.document(body))

    def test_lifecycle_treats_a_refusal_as_not_a_unique_key_mapping(self) -> None:
        for body in ("type: a\ntype: b\n", "a: &x 1\n", "a: !!str 1\n", "<<: {a: 1}\n"):
            with self.subTest(body=body):
                found = self.lifecycle_state(body)
                self.assertIsNone(found.status)
                self.assertEqual(
                    found.state_issue, "frontmatter is not a unique-key mapping"
                )

    def test_lifecycle_still_reads_a_valid_status(self) -> None:
        found = self.lifecycle_state(
            'title: "Example"\nversion: "1.0.0"\ntype: "sdlc/spec"\n'
            'status: "draft"\nowner: "platform"\nupdated: 2026-11-13\n'
        )
        self.assertEqual(found.status, "draft")
        self.assertIsNone(found.state_issue)

    def test_agent_governance_keeps_its_native_metadata_code(self) -> None:
        for body in ("name: a\nname: b\n", "name: &x a\n", "name: !!str a\n"):
            with self.subTest(body=body):
                with self.assertRaises(AGENT_GOVERNANCE.HarnessError) as caught:
                    AGENT_GOVERNANCE._frontmatter(self.document(body))
                self.assertEqual(caught.exception.code, "AGENT-NATIVE-METADATA")
        metadata, body = AGENT_GOVERNANCE._frontmatter(self.document('name: "a"\n'))
        self.assertEqual(metadata["name"], "a")
        self.assertEqual(body, "# Body\n")

    def test_agent_governance_keeps_the_codex_policy_loader_on_pyyaml(self) -> None:
        self.assertTrue(
            issubclass(
                AGENT_GOVERNANCE.UniqueMetadataLoader, AGENT_GOVERNANCE.yaml.SafeLoader
            )
        )

    def test_links_check_treats_a_refusal_as_no_frontmatter(self) -> None:
        for body in ("a: 1\na: 2\n", "a: &x 1\n", "a: !!str 1\n", "a: [\n"):
            with self.subTest(body=body):
                self.assertEqual(LINKS.frontmatter_mapping(self.document(body)), {})
        self.assertEqual(
            LINKS.frontmatter_mapping(self.document("updated: 2026-11-13\n")),
            {"updated": "2026-11-13"},
        )
        self.assertEqual(LINKS.frontmatter_mapping("no frontmatter\n"), {})


class HookifyFrontmatterTests(unittest.TestCase):
    """quality.py runs on import, so lift its Hookify local-rule loop alone."""

    @staticmethod
    def failures(rule_text: str) -> list[str]:
        source = (ROOT / "scripts/validation/repository/quality.py").read_text("utf-8")
        loop = next(
            node
            for node in ast.parse(source).body
            if isinstance(node, ast.For)
            and ast.unparse(node.target) == "local_rule_path"
        )
        failures: list[str] = []
        with tempfile.TemporaryDirectory() as directory:
            rule = Path(directory) / "hookify.example.local.md"
            rule.write_text(rule_text, "utf-8")
            namespace = {
                "claude_local_rule_paths": [rule],
                "rel": lambda path: path.name,
                "read_text": lambda path: path.read_text("utf-8"),
                "fail": failures.append,
                "re": re,
                "subprocess": types.SimpleNamespace(
                    run=lambda *args, **kwargs: types.SimpleNamespace(returncode=0)
                ),
                "root": Path(directory),
                "FrontmatterError": FrontmatterError,
                "load_frontmatter": load_frontmatter,
            }
            exec(  # noqa: S102 - one vetted loop of a tracked repository script
                compile(ast.Module(body=[loop], type_ignores=[]), "quality.py", "exec"),
                namespace,
            )
        return failures

    def test_a_valid_hookify_rule_passes(self) -> None:
        rule = "---\nname: a\nenabled: true\nevent: bash\npattern: x\n---\nbody\n"
        self.assertEqual(self.failures(rule), [])

    def test_a_refusal_reports_the_reason_code_not_library_text(self) -> None:
        duplicate = "---\nname: a\nname: b\nenabled: true\nevent: bash\n---\nbody\n"
        self.assertEqual(
            self.failures(duplicate),
            [
                "hookify.example.local.md Hookify frontmatter parse failed: duplicate-key: name"
            ],
        )
        anchored = "---\nname: &x a\n---\nbody\n"
        self.assertEqual(
            self.failures(anchored),
            ["hookify.example.local.md Hookify frontmatter parse failed: anchor"],
        )

    def test_a_missing_field_is_still_reported(self) -> None:
        rule = "---\nname: a\nevent: bash\npattern: x\n---\nbody\n"
        self.assertEqual(
            self.failures(rule),
            ["hookify.example.local.md missing Hookify frontmatter field: enabled"],
        )


if __name__ == "__main__":
    unittest.main()
