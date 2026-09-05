"""QA profiles execute once over isolated final-tree or exact-index bytes."""
from __future__ import annotations

import copy
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load_qa():
    path = ROOT / "scripts/qa.py"
    spec = importlib.util.spec_from_file_location("qa_test_owner", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PublicEntryTests(unittest.TestCase):
    def test_list_is_a_working_public_entry(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/qa.py"), "--list"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("full", result.stdout)
        self.assertIn("staged", result.stdout)


class QaTests(unittest.TestCase):
    def setUp(self):
        self.qa = load_qa()
        self.temporary = tempfile.TemporaryDirectory(prefix="qa-tests-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "source"
        self.root.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "QA Fixture")
        self.git("config", "user.email", "qa@example.invalid")
        (self.root / "file.txt").write_text("original\n")
        (self.root / "gone.txt").write_text("delete\n")
        (self.root / ".gitignore").write_text("ignored-secret\n")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True).stdout

    def test_final_tree_and_index_are_distinct_and_source_is_unchanged(self):
        (self.root / "file.txt").write_text("staged invalid\n")
        self.git("mv", "gone.txt", "renamed space.txt")
        self.git("add", "file.txt")
        (self.root / "file.txt").write_text("unstaged repaired\n")
        (self.root / "new space.txt").write_text("new\n")
        (self.root / "ignored-secret").write_text("excluded\n")
        (self.root / "link").symlink_to("file.txt")
        before = (self.root / ".git/index").read_bytes()
        for staged, expected in [(False, "unstaged repaired\n"), (True, "staged invalid\n")]:
            with self.qa.repository_snapshot(self.root, staged=staged) as snapshot:
                self.assertEqual((snapshot / "file.txt").read_text(), expected)
                self.assertTrue((snapshot / "renamed space.txt").is_file())
                self.assertFalse((snapshot / "gone.txt").exists())
                self.assertFalse((snapshot / "ignored-secret").exists())
                self.assertEqual((snapshot / "new space.txt").exists(), not staged)
                self.assertEqual((snapshot / "link").is_symlink(), not staged)
                self.assertEqual(self.qa.git(snapshot, "rev-parse", "HEAD"), self.git("rev-parse", "HEAD"))
                self.assertEqual(self.qa.git(snapshot, "diff", "--name-only"), b"")
        self.assertEqual((self.root / ".git/index").read_bytes(), before)
        self.assertEqual((self.root / "file.txt").read_text(), "unstaged repaired\n")

    def test_snapshot_supports_worktree_gitfile(self):
        linked = Path(self.temporary.name) / "linked"
        self.git("worktree", "add", "--detach", str(linked))
        with self.qa.repository_snapshot(linked, staged=True) as snapshot:
            self.assertEqual((snapshot / "file.txt").read_text(), "original\n")

    def test_snapshot_rejects_escaping_symlinks(self):
        (self.root / "escape").symlink_to("../../outside")
        with self.assertRaisesRegex(ValueError, "symlink"):
            with self.qa.repository_snapshot(self.root):
                pass

    def test_ci_baseline_is_parent_or_empty_never_self(self):
        self.assertEqual(self.qa.base_revision(self.root, "ci", ""), "EMPTY")
        self.assertEqual(self.qa.base_revision(self.root, "ci", "0" * 40), "EMPTY")
        parent = self.git("rev-parse", "HEAD").decode().strip()
        (self.root / "file.txt").write_text("next\n")
        self.git("commit", "-qam", "next")
        self.assertEqual(self.qa.base_revision(self.root, "ci", ""), parent)

    def test_profiles_are_complete_equal_and_deduplicated(self):
        contract = self.qa.contract_module.validate_contract(ROOT)
        self.assertEqual(contract["profiles"]["full"], contract["profiles"]["ci"])
        ids = contract["profiles"]["full"]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), {r["id"] for r in contract["validators"]})
        self.assertEqual(ids.count("unit-tests"), 1)
        self.assertEqual(ids.count("pre-commit"), 1)
        for mutation in ("duplicate", "unknown", "missing"):
            bad = copy.deepcopy(contract)
            if mutation == "duplicate":
                bad["profiles"]["full"].append(ids[0])
            elif mutation == "unknown":
                bad["profiles"]["full"][0] = "no-such-gate"
            else:
                bad["profiles"]["full"].pop()
            with self.assertRaises(self.qa.contract_module.ContractError):
                self.qa.contract_module.validate_contract(ROOT, bad)

    def test_gate_failure_diagnostics_are_bounded_and_redacted(self):
        row = {"id": "fixture", "argv": ["python3", "check.py"], "optional": False, "fallback": {"reason": "required"}, "evidenceLane": "repo-static"}
        (self.root / "check.py").write_text("import sys; print('validation failed token=abc123\\n' + 'x'*10000, file=sys.stderr); sys.exit(7)")
        import io
        from contextlib import redirect_stdout
        output = io.StringIO()
        with redirect_stdout(output):
            rc = self.qa.runner.run_selected(self.root, "all-files", ["file.txt"], {"validators": [row]}, mock.Mock(), validator_ids=["fixture"])
        self.assertEqual(rc, 1)
        self.assertIn("rc=7", output.getvalue())
        self.assertIn("validation failed", output.getvalue())
        self.assertNotIn("abc123", output.getvalue())
        self.assertLess(len(output.getvalue()), 5000)

    def test_python_preserves_invoking_venv_and_refuses_path_shadow(self):
        selected = "/opt/test-venv/bin/python3"
        with mock.patch.object(self.qa.runner.sys, "executable", selected):
            with mock.patch.dict(os.environ, {"PATH": str(self.root), "PYTHONPATH": str(self.root)}):
                self.assertEqual(self.qa.runner.resolve_tool("python3", self.root), selected)
                self.assertNotIn(str(self.root), self.qa.runner.closed_subprocess_environment()["PATH"])
                self.assertNotIn("PYTHONPATH", self.qa.runner.closed_subprocess_environment())

    def test_required_missing_tool_fails(self):
        import io
        from contextlib import redirect_stdout
        row = {"id": "missing", "argv": ["pre-commit", "run", "--all-files"], "optional": False, "fallback": {"reason": "required"}, "evidenceLane": "repo-static"}
        with mock.patch.object(self.qa.runner, "resolve_tool", return_value=None), redirect_stdout(io.StringIO()):
            self.assertEqual(self.qa.runner.run_selected(self.root, "all-files", ["file.txt"], {"validators": [row]}, mock.Mock(), validator_ids=["missing"]), 1)

    def test_formatter_mutation_fails_without_changing_source(self):
        with self.qa.repository_snapshot(self.root) as snapshot:
            (snapshot / "file.txt").write_text("formatted\n")
            with self.assertRaisesRegex(ValueError, "modified"):
                self.qa.require_unchanged_snapshot(snapshot)
        self.assertEqual((self.root / "file.txt").read_text(), "original\n")


if __name__ == "__main__":
    unittest.main()
