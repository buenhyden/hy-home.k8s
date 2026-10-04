"""Independent synthetic cases for production repository-quality rules."""

import ast
import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import document_contracts as contracts  # noqa: E402


class RepositoryQualityRuleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / "scripts/validation/repository/quality.py"
        tree = ast.parse(path.read_text())
        names = {
            "strip_multiline_html_comments",
            "visible_markdown_lines",
            "parse_markdown_table_after_heading",
            "profiled_readme_table_headings",
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

    def test_readme_tables_retain_visible_headings_and_unique_diagnostics(self):
        titles = (
            "Probe Index",
            "Example Role Matrix",
            "Service Coverage Matrix",
            "Platform Coverage Matrix",
            "External Service Contract Matrix",
            "Secret Management Responsibility Matrix",
            "Workload Coverage Matrix",
            "AppProject Allow-list Rationale Matrix",
            "Workload Image and Kind Policy Matrix",
            "Namespace Ownership Matrix",
            "Infrastructure Coverage Matrix",
            "Host Runtime Prerequisite Matrix",
            "Bootstrap Boundary Matrix",
            "Infrastructure Test Inventory",
        )
        table = "\n| Name | Value |\n| --- | --- |\n| alpha | one |\n"
        parse = self.rules["parse_markdown_table_after_heading"]
        for title in titles:
            headings = self.rules["profiled_readme_table_headings"](title)
            hidden_table = table.replace("alpha | one", "hidden | ignored")
            backtick = f"```markdown\n## {title}{hidden_table}```\n"
            tilde = f"~~~markdown\n### {title}{hidden_table}~~~\n"
            comment = f"<!--\n## {title}{hidden_table}-->\n"
            for heading in headings:
                for hidden in (
                    "",
                    backtick,
                    tilde,
                    comment,
                    backtick + tilde,
                    backtick + comment,
                ):
                    with self.subTest(title=title, heading=heading, hidden=hidden):
                        self.assertEqual(
                            parse(hidden + heading + table, headings),
                            ([["Name", "Value"], ["alpha", "one"]], None),
                        )
            self.assertEqual(
                parse("\n".join(headings) + table, headings),
                ([], f"ambiguous visible markdown table headings: {list(headings)!r}"),
            )
            self.assertEqual(
                parse(f"```markdown\n## {title}{table}```\n", headings),
                ([], f"missing visible markdown heading: one of {headings!r}"),
            )

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
