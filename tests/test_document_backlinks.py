from __future__ import annotations

import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = REPOSITORY_ROOT / "scripts" / "document-backlinks.py"


def load_tool():
    spec = importlib.util.spec_from_file_location(
        "document_backlinks_test_target", TOOL_PATH
    )
    if spec is None or spec.loader is None:
        raise AssertionError("document-backlinks.py could not be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class DocumentBacklinksTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tool = load_tool()
        directory = tempfile.TemporaryDirectory(prefix="backlinks-")
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        files = {
            "docs/parent.md": "# Parent\n",
            "docs/child.md": "See [the parent](parent.md).\n",
            "docs/anchor.md": "See [a section](parent.md#scope).\n",
            "docs/fenced.md": "```text\n[parent](parent.md)\n```\n",
            "docs/commented.md": "<!-- [parent](parent.md) -->\n",
            "docs/other.md": "See [the child](child.md).\n",
        }
        for name, text in files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)

    def run_tool(self, *argv: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = self.tool.main(["--root", str(self.root), *argv])
        return code, out.getvalue(), err.getvalue()

    def test_derives_forward_and_anchor_links_only(self) -> None:
        code, out, _ = self.run_tool("docs/parent.md")
        self.assertEqual(code, 0)
        self.assertEqual(out.splitlines(), ["docs/anchor.md", "docs/child.md"])

    def test_fenced_and_commented_links_do_not_count(self) -> None:
        _, out, _ = self.run_tool("docs/parent.md")
        self.assertNotIn("docs/fenced.md", out)
        self.assertNotIn("docs/commented.md", out)

    def test_absent_target_fails(self) -> None:
        code, _, err = self.run_tool("docs/missing.md")
        self.assertEqual(code, 2)
        self.assertIn("does not exist", err)

    def test_target_outside_root_fails(self) -> None:
        code, _, err = self.run_tool("../outside.md")
        self.assertEqual(code, 2)
        self.assertIn("outside the repository root", err)


if __name__ == "__main__":
    unittest.main()
