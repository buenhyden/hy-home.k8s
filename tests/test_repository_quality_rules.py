"""Independent synthetic cases for production repository-quality rules."""

import ast
import importlib.util
import pathlib
import re
import sys
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import document_contracts as contracts  # noqa: E402
from validation import document_content as content  # noqa: E402


class RepositoryQualityRuleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / "scripts/validation/repository/quality.py"
        tree = ast.parse(path.read_text())
        names = {
            "strip_multiline_html_comments",
            "visible_markdown_lines",
            "canonical_markdown_owns_generic_residue",
            "generic_template_residue_lines",
            "has_nearby_marker",
            "is_inert_prohibition",
            "is_bare_or_main_push",
            "is_unmarked_command",
            "rel",
        }
        nodes = [
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name in names
        ]
        if {node.name for node in nodes} != names:
            raise AssertionError("production rule extraction is incomplete")
        residue = next(
            node
            for node in tree.body
            if isinstance(node, ast.Assign)
            and any(
                isinstance(t, ast.Name) and t.id == "authored_template_residue"
                for t in node.targets
            )
        )
        boundary = next(
            node
            for node in tree.body
            if isinstance(node, ast.Assign)
            and any(
                isinstance(t, ast.Name) and t.id == "command_boundary_rules"
                for t in node.targets
            )
        )
        push_pattern = next(
            node
            for node in tree.body
            if isinstance(node, ast.Assign)
            and any(
                isinstance(t, ast.Name) and t.id == "git_push_pattern"
                for t in node.targets
            )
        )
        cls.rules = {
            "re": re,
            "pathlib": pathlib,
            "root": ROOT,
            "document_registry": contracts.load_registry(ROOT),
            "classify_path": contracts.classify_path,
            "DocumentContractError": contracts.DocumentContractError,
        }
        exec(
            compile(
                ast.Module(
                    body=[residue, boundary, push_pattern, *nodes], type_ignores=[]
                ),
                str(path),
                "exec",
            ),
            cls.rules,
        )
        source = ROOT / "scripts/validate-markdown-profiles.py"
        spec = importlib.util.spec_from_file_location("selected_document_rules", source)
        cls.document_validator = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = cls.document_validator
        spec.loader.exec_module(cls.document_validator)
        cls.document_registry = cls.document_validator.load_registry(ROOT)

    def test_current_collection_index_header_uses_shared_navigation_contract(self):
        validator = self.document_validator
        path = pathlib.PurePosixPath("docs/05.operations/guides/README.md")
        text = (ROOT / path).read_text(encoding="utf-8")
        profile = validator.classify_path(self.document_registry, path)
        self.assertEqual(
            validator.document_content_diagnostics(ROOT, path, profile, text), []
        )
        changed = text.replace("| Path |", "| 문서 |", 1)
        self.assertNotEqual(text, changed)
        issues = validator.document_content_diagnostics(ROOT, path, profile, changed)
        self.assertIn("DOC-INDEX-HEADER", {issue.rule_id for issue in issues})

    def test_selected_document_gate_keeps_live_matrix_relationships(self):
        validator = self.document_validator
        registry = self.document_registry

        def findings(relative, mutate=None):
            path = pathlib.PurePosixPath(relative)
            text = (ROOT / path).read_text(encoding="utf-8")
            if mutate is not None:
                changed = mutate(text)
                self.assertNotEqual(text, changed)
                text = changed
            profile = validator.classify_path(registry, path)
            return validator.document_content_diagnostics(ROOT, path, profile, text)

        for path in (
            "examples/README.md",
            ".github/repository-surface.md",
            "infrastructure/verify/README.md",
        ):
            with self.subTest(path=path):
                self.assertEqual(findings(path), [])

        mutations = (
            (
                "examples/README.md",
                lambda text: re.sub(
                    r"(?m)^#{2,3} Example Role Matrix$",
                    "## Missing Example Role Matrix",
                    text,
                    count=1,
                ),
            ),
            (
                "examples/README.md",
                lambda text: text.replace("| `sample-app/` |", "| `missing-app/` |", 1),
            ),
            (
                ".github/repository-surface.md",
                lambda text: text.replace("No deploy CD", "Deploy CD", 1),
            ),
            (
                "infrastructure/verify/README.md",
                lambda text: re.sub(
                    r"(?m)^\| .*`verify-gitops\.sh`.*\n", "", text, count=1
                ),
            ),
        )
        for path, mutate in mutations:
            with self.subTest(path=path, mutation=mutate):
                self.assertTrue(findings(path, mutate))

    def test_incident_state_tracks_each_record_kind_independently(self):
        validator = self.document_validator
        path = pathlib.PurePosixPath("docs/05.operations/incidents/README.md")
        text = (ROOT / path).read_text(encoding="utf-8")
        profile = validator.classify_path(self.document_registry, path)
        self.assertEqual(
            validator.document_content_diagnostics(ROOT, path, profile, text), []
        )
        for filename in ("incident.md", "postmortem.md"):
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as temp:
                sample = (
                    pathlib.Path(temp)
                    / "docs/05.operations/incidents/2026/inc-0001-example"
                    / filename
                )
                sample.parent.mkdir(parents=True)
                sample.write_text("record", encoding="utf-8")
                findings = validator.document_content_diagnostics(
                    pathlib.Path(temp),
                    path,
                    profile,
                    text,
                    registry=self.document_registry,
                )
                self.assertIn("DOC-INCIDENT-STATE", {item.rule_id for item in findings})

    def test_document_inventory_rejects_unsafe_or_incomplete_scans(self):
        validator = self.document_validator
        registry = self.document_registry
        guide = pathlib.PurePosixPath("docs/05.operations/guides/README.md")
        guide_profile = validator.classify_path(registry, guide)
        empty_index = "### 문서 인덱스\n\n| Path | Purpose |\n| --- | --- |\n"
        with (
            tempfile.TemporaryDirectory() as temp,
            tempfile.TemporaryDirectory() as outside,
        ):
            root = pathlib.Path(temp)
            guide_parent = root / "docs/05.operations"
            guide_parent.mkdir(parents=True)
            (guide_parent / "guides").symlink_to(outside, target_is_directory=True)
            issues = validator.document_content_diagnostics(
                root, guide, guide_profile, empty_index, registry=registry
            )
            self.assertIn("DOC-INDEX-INPUT", {item.rule_id for item in issues})

        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            guides = root / "docs/05.operations/guides"
            guides.mkdir(parents=True)
            (guides / "linked.md").symlink_to(ROOT / guide)
            with self.assertRaises(content.BoundedInputError):
                content._children(root, "docs/05.operations/guides", "file")
            with mock.patch.object(content.os, "scandir", side_effect=PermissionError):
                with self.assertRaises(content.BoundedInputError):
                    content._children(root, "docs/05.operations/guides", "file")

        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            examples = root / "examples"
            examples.mkdir()
            for index in range(content.MAX_DIRECTORY_ENTRIES + 1):
                (examples / f"example-{index}").mkdir()
            with self.assertRaises(content.BoundedInputError):
                content._children(root, "examples", "dir")

        with (
            tempfile.TemporaryDirectory() as temp,
            tempfile.TemporaryDirectory() as outside,
        ):
            root = pathlib.Path(temp)
            incident = pathlib.PurePosixPath("docs/05.operations/incidents/README.md")
            incident_profile = validator.classify_path(registry, incident)
            incident_parent = root / "docs/05.operations"
            incident_parent.mkdir(parents=True)
            (incident_parent / "incidents").symlink_to(
                outside, target_is_directory=True
            )
            text = (ROOT / incident).read_text(encoding="utf-8")
            issues = validator.document_content_diagnostics(
                root, incident, incident_profile, text, registry=registry
            )
            self.assertIn("DOC-INCIDENT-INPUT", {item.rule_id for item in issues})

    def test_incident_inventory_reports_noncanonical_depth(self):
        validator = self.document_validator
        registry = self.document_registry
        path = pathlib.PurePosixPath("docs/05.operations/incidents/README.md")
        profile = validator.classify_path(registry, path)
        text = (ROOT / path).read_text(encoding="utf-8")
        for parts in (
            ("2026", "incident.md"),
            ("2026", "inc-0001-example", "deeper", "incident.md"),
        ):
            with self.subTest(parts=parts), tempfile.TemporaryDirectory() as temp:
                root = pathlib.Path(temp)
                misplaced = root / "docs/05.operations/incidents" / pathlib.Path(*parts)
                misplaced.parent.mkdir(parents=True)
                misplaced.write_text("record", encoding="utf-8")
                issues = validator.document_content_diagnostics(
                    root, path, profile, text, registry=registry
                )
                self.assertIn("DOC-INCIDENT-PATH", {item.rule_id for item in issues})

    def test_readme_tables_retain_visible_headings_and_unique_diagnostics(self):
        title = "Probe Index"
        table = "\n| Name | Value |\n| --- | --- |\n| alpha | one |\n"
        parse = self.document_validator._document_content_table
        hidden_table = table.replace("alpha | one", "hidden | ignored")
        for hidden in (
            "",
            f"```markdown\n## {title}{hidden_table}```\n",
            f"~~~markdown\n### {title}{hidden_table}~~~\n",
            f"<!--\n## {title}{hidden_table}-->\n",
        ):
            with self.subTest(hidden=hidden):
                self.assertEqual(
                    parse(hidden + f"### {title}" + table, title),
                    (["Name", "Value"], [["alpha", "one"]]),
                )
        self.assertIsNone(parse(f"## {title}\n### {title}" + table, title))
        self.assertIsNone(parse(f"```markdown\n## {title}{table}```\n", title))

    def test_generic_residue_retains_lines_and_delegates_structural_markdown(self):
        residue = self.rules["generic_template_residue_lines"]
        self.assertEqual(residue("route: Use this " + "template"), [1])
        self.assertEqual(residue("Target: " + "docs/example.md"), [1])
        self.assertEqual(residue("valid configuration\n"), [])
        self.assertEqual(
            residue("valid\nTarget: " + "docs/example.md\nUse this " + "template"),
            [2, 3],
        )
        owns = self.rules["canonical_markdown_owns_generic_residue"]
        self.assertTrue(owns(ROOT / "docs/01.requirements/9999-projection.md"))
        self.assertFalse(owns(ROOT / "AGENTS.md"))

    def test_secret_value_output_is_detected_with_or_without_namespace_flag(self):
        rule = next(
            pattern
            for label, pattern, _markers in self.rules["command_boundary_rules"]
            if label == "kubectl get secret yaml/json"
        )
        for command in (
            "kubectl get secret app -o yaml",
            'kubectl get secret app -o yaml""',
            "kubectl get secret app -o=json",
            "kubectl get secret app -oyaml",
            "kubectl -n argocd get secret argocd-external-valkey -o yaml",
            "kubectl --namespace apps get secrets -o json",
            "kubectl get secret app --output yaml",
            "kubectl get secret app --output=yaml",
            "kubectl get secret app --output=json''",
            "kubectl -n apps get secrets --output=json",
        ):
            with self.subTest(command=command):
                self.assertIsNotNone(rule.search(command))
        for option in ("-o ", "-o=", "--output ", "--output="):
            for value in ("yaml", "json"):
                for quote in ("'", '"'):
                    command = f"kubectl get secret app {option}{quote}{value}{quote}"
                    with self.subTest(command=command):
                        self.assertIsNotNone(rule.search(command))
        for command in (
            "kubectl -n argocd get secret argocd-local-tls -o jsonpath='{.type}'",
            "kubectl -n apps get secret app --output=jsonpath='{.type}'",
            "kubectl -n apps get secret app --output='jsonpath={.type}'",
            "kubectl get secret app -o 'json'path='{.type}'",
            "kubectl get secret app --output='json'path='{.type}'",
            "kubectl -n argocd get externalsecret argocd-external-valkey -o yaml",
            "kubectl -n headlamp get secret headlamp-tls",
            "kubectl get secret app -o 'yaml\"",
            "kubectl get secret app -o=\"json'",
            "kubectl get secret app --output='yaml\"",
        ):
            with self.subTest(command=command):
                self.assertIsNone(rule.search(command))

    def test_raw_secret_output_rejects_nearby_safety_claims(self):
        label, pattern, markers = next(
            row
            for row in self.rules["command_boundary_rules"]
            if row[0] == "kubectl get secret yaml/json"
        )
        decide = self.rules["is_unmarked_command"]
        raw = "kubectl -n apps get secret app -o yaml"
        for lines in (
            ["metadata-only redacted status-only jsonpath no secret value", raw],
            [raw + " # redacted metadata-only"],
            ["# prohibited-example: `kubectl get secret app -o yaml`", raw],
            ["redacted", "kubectl get secret app --output=yaml"],
            ["redacted", "kubectl get secret app -o 'yaml'"],
            ["redacted", 'kubectl get secret app --output="json"'],
            ["redacted", 'kubectl get secret app -o yaml""'],
            ["redacted", "kubectl get secret app --output=json''"],
        ):
            with self.subTest(lines=lines):
                self.assertTrue(
                    decide(lines, len(lines) - 1, label, pattern, markers, False)
                )
        self.assertFalse(
            decide(
                ["prohibited-example: `kubectl get secret app -o yaml`"],
                0,
                label,
                pattern,
                markers,
                True,
            )
        )
        self.assertFalse(
            decide(
                ["- do-not-run: `kubectl get secret app -o json`"],
                0,
                label,
                pattern,
                markers,
                True,
            )
        )
        self.assertFalse(
            decide(
                ['do-not-run: `kubectl get secret app --output="json"`'],
                0,
                label,
                pattern,
                markers,
                True,
            )
        )
        self.assertFalse(
            decide(
                ["kubectl get secret app --output='json'path='{.type}'"],
                0,
                label,
                pattern,
                markers,
                False,
            )
        )
        fenced = "```sh\n# do-not-run: `kubectl get secret app -o 'yaml'`\n```\n"
        visible = {index for index, _ in self.rules["visible_markdown_lines"](fenced)}
        self.assertNotIn(1, visible)
        self.assertTrue(
            decide(fenced.splitlines(), 1, label, pattern, markers, 1 in visible)
        )
        self.assertTrue(
            decide(
                ["prohibited-example: `kubectl get secret app -o yaml`"],
                0,
                label,
                pattern,
                markers,
                False,
            )
        )
        self.assertTrue(
            decide(
                ["# prohibited-example: `kubectl get secret app -o yaml`"],
                0,
                label,
                pattern,
                markers,
                True,
            )
        )
        self.assertTrue(
            decide(
                ["    prohibited-example: `kubectl get secret app -o yaml`"],
                0,
                label,
                pattern,
                markers,
                True,
            )
        )
        self.assertTrue(
            decide(
                ["> do-not-run: `kubectl get secret app -o yaml`"],
                0,
                label,
                pattern,
                markers,
                True,
            )
        )
        self.assertFalse(
            decide(
                ["kubectl -n apps get secret app -o jsonpath='{.type}'"],
                0,
                label,
                pattern,
                markers,
                False,
            )
        )

    def test_prohibited_prose_does_not_hide_other_live_commands(self):
        decide = self.rules["is_unmarked_command"]
        label, pattern, markers = self.rules["command_boundary_rules"][0]
        fenced = "```sh\ndo-not-run: `kubectl apply -f app.yaml`\n```\n"
        visible = {index for index, _ in self.rules["visible_markdown_lines"](fenced)}
        self.assertNotIn(1, visible)
        self.assertTrue(
            decide(
                fenced.splitlines(),
                1,
                label,
                pattern,
                markers,
                1 in visible,
            )
        )
        self.assertFalse(
            decide(
                ["do-not-run: `kubectl apply -f app.yaml`"],
                0,
                label,
                pattern,
                markers,
                True,
            )
        )
        self.assertTrue(
            decide(
                ["do-not-run: `kubectl apply -f app.yaml`"],
                0,
                label,
                pattern,
                markers,
                False,
            )
        )
        self.assertTrue(
            decide(
                [
                    "do-not-run: `kubectl apply -f app.yaml`; kubectl apply -f other.yaml"
                ],
                0,
                label,
                pattern,
                markers,
                True,
            )
        )
        self.assertTrue(
            decide(
                ["kubectl apply -f app.yaml"],
                0,
                label,
                pattern,
                markers,
                True,
            )
        )
        push = self.rules["is_bare_or_main_push"]
        self.assertFalse(push("prohibited-example: `git push origin main`", True))
        self.assertTrue(push("prohibited-example: `git push origin main`", False))
        self.assertTrue(
            push("git push origin main # do-not-run: `git push origin main`", True)
        )


if __name__ == "__main__":
    unittest.main()
