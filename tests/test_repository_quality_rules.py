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
                ast.Module(body=[residue, *nodes], type_ignores=[]), str(path), "exec"
            ),
            cls.rules,
        )

    def test_readme_tables_retain_visible_headings_and_unique_diagnostics(self):
        titles = (
            "Probe Index",
            "Example Role Matrix",
            "Service Coverage Matrix",
            "External Service Contract Matrix",
            "Secret Management Responsibility Matrix",
            "Workload Coverage Matrix",
            "AppProject Allow-list Rationale Matrix",
            "Workload Image and Kind Policy Matrix",
            "Namespace Ownership Matrix",
            "Infrastructure Coverage Matrix",
            "WSL2 Runtime Prerequisite Matrix",
            "Bootstrap Boundary Matrix",
            "Infrastructure Test Inventory",
            "Traefik Route Inventory",
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


if __name__ == "__main__":
    unittest.main()
