"""Regressions for the review delta classifier (W10-REVIEW, D05)."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


DELTA = _load("review_delta", "scripts/review_delta.py")
TASK = "docs/03.specs/0001-x/01.tasks/tsk-0001-x.md"
LEDGER = "docs/03.specs/work-residue-ledger.json"
LEDGER_ONE = '{"entries": [{"id": "A-1", "state": "open"}]}\n'
LEDGER_TWO = (
    '{"entries": [{"id": "A-1", "state": "open"}, {"id": "B-1", "state": "open"}]}\n'
)


class ReviewDeltaTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="review-delta-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.git("init", "--quiet", "--initial-branch=main")
        self.write(TASK, '---\nversion: "0.1.0"\n---\n| EVD-001 | PASS |\n')
        self.write(LEDGER, LEDGER_ONE)
        self.write("scripts/tool.py", "print('a')\n")
        self.reviewed = self.commit("reviewed")

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", "-c", "user.name=F", "-c", "user.email=f@x.invalid", *args],
            cwd=self.root,
            env={"PATH": "/usr/bin:/bin", "GIT_CONFIG_GLOBAL": "/dev/null"},
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout.strip()

    def write(self, path: str, text: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def commit(self, message: str) -> str:
        self.git("add", "-A")
        self.git("commit", "--quiet", "--allow-empty", "-m", message)
        return self.git("rev-parse", "HEAD")

    def classify(self, head: str = "HEAD"):
        return DELTA.classify(self.root, self.reviewed, head)

    def test_the_reviewed_commit_itself_needs_nothing(self):
        self.assertEqual(self.classify()["verdict"], "NO_CHANGE")

    def test_appended_evidence_keeps_the_review(self):
        self.write(
            TASK, '---\nversion: "0.1.1"\n---\n| EVD-001 | PASS |\n| EVD-002 | PASS |\n'
        )
        self.write(LEDGER, LEDGER_TWO)
        self.commit("evidence")
        result = self.classify()
        self.assertEqual(result["verdict"], "EVIDENCE_ONLY")
        self.assertEqual(sorted(result["evidence"]), sorted([LEDGER, TASK]))

    def test_any_other_path_needs_rereview_of_that_path_only(self):
        self.write(
            TASK, '---\nversion: "0.1.0"\n---\n| EVD-001 | PASS |\n| EVD-002 | PASS |\n'
        )
        self.write("scripts/tool.py", "print('b')\n")
        self.commit("code and evidence")
        result = self.classify()
        self.assertEqual(result["verdict"], "REREVIEW")
        self.assertEqual(result["rereview"], ["scripts/tool.py"])

    def test_evidence_paths_cannot_hide_a_behavior_change(self):
        cases = {
            "deleted task": lambda: (self.root / TASK).unlink(),
            "symlinked task": lambda: (
                (self.root / TASK).unlink(),
                os.symlink("../../../../scripts/tool.py", self.root / TASK),
            ),
            "executable task": lambda: os.chmod(self.root / TASK, 0o755),
            "task file outside a tasks folder": lambda: self.write(
                "docs/03.specs/0001-x/spec.md", "changed\n"
            ),
        }
        for name, change in cases.items():
            with self.subTest(name):
                self.git("reset", "--quiet", "--hard", self.reviewed)
                change()
                self.commit(name)
                self.assertEqual(self.classify()["verdict"], "REREVIEW", name)

    def test_evidence_must_only_grow(self):
        cases = {
            "deleted row": '---\nversion: "0.1.0"\n---\n',
            "flipped result": '---\nversion: "0.1.0"\n---\n| EVD-001 | FAIL |\n',
        }
        for name, text in cases.items():
            with self.subTest(name):
                self.git("reset", "--quiet", "--hard", self.reviewed)
                self.write(TASK, text)
                self.commit(name)
                result = self.classify()
                self.assertEqual(result["verdict"], "REREVIEW", name)
                self.assertEqual(result["rereview"], [TASK])
        for name, text in {
            "removed entry": '{"entries": []}\n',
            "changed entry": '{"entries": [{"id": "A-1", "state": "closed"}]}\n',
        }.items():
            with self.subTest(name):
                self.git("reset", "--quiet", "--hard", self.reviewed)
                self.write(LEDGER, text)
                self.commit(name)
                self.assertEqual(self.classify()["rereview"], [LEDGER], name)

    def test_only_task_records_are_evidence(self):
        for name in ("CLAUDE.md", "AGENTS.md", "README.md", ".tsk-0002-x.md"):
            with self.subTest(name):
                self.git("reset", "--quiet", "--hard", self.reviewed)
                self.write(f"docs/03.specs/0001-x/tasks/{name}", "@AGENTS.md\n")
                self.commit(name)
                self.assertEqual(self.classify()["verdict"], "REREVIEW", name)
        self.git("reset", "--quiet", "--hard", self.reviewed)
        self.write(
            "docs/03.specs/0001-x/01.tasks/tsk-0002-y.md", "| EVD-001 | PASS |\n"
        )
        self.commit("new task")
        self.assertEqual(self.classify()["verdict"], "EVIDENCE_ONLY")

    def test_special_entries_are_never_evidence(self):
        task_link = "docs/03.specs/0001-x/01.tasks/tsk-0003-z.md"
        self.git("reset", "--quiet", "--hard", self.reviewed)
        (self.root / task_link).parent.mkdir(parents=True, exist_ok=True)
        os.symlink("../../../../scripts/tool.py", self.root / task_link)
        self.commit("new symlinked task")
        self.assertEqual(self.classify()["verdict"], "REREVIEW")
        self.git("reset", "--quiet", "--hard", self.reviewed)
        self.git(
            "update-index",
            "--add",
            "--cacheinfo",
            f"160000,{self.reviewed},docs/03.specs/0001-x/01.tasks/tsk-0004-g.md",
        )
        self.git("commit", "--quiet", "-m", "gitlink")
        self.assertEqual(self.classify()["verdict"], "REREVIEW")

    def test_a_mode_change_back_to_regular_is_not_evidence(self):
        os.chmod(self.root / TASK, 0o755)
        self.reviewed = self.commit("executable task")
        os.chmod(self.root / TASK, 0o644)
        self.write(TASK, '---\nversion: "0.1.0"\n---\n| EVD-001 | PASS |\n| E2 |\n')
        self.commit("regular again")
        self.assertEqual(self.classify()["verdict"], "REREVIEW")

    def test_a_commit_that_changes_no_path_needs_nothing(self):
        self.commit("empty")
        result = self.classify()
        self.assertEqual(result["verdict"], "NO_CHANGE")
        self.assertIn("no path changed", result["reason"])

    def test_growth_is_read_from_the_blobs_not_the_diff_text(self):
        body = '---\nversion: "0.1.0"\n---\n| EVD-001 | PASS |\n'
        cases = {
            "removed delimiter": ('version: "0.1.0"\n---\n| EVD-001 | PASS |\n', body),
            "removed dash line": (body + "| E2 |\n", body + "-- keep\n"),
            "version line outside front matter": (
                body + "| E2 |\n",
                body + 'version: "9"\n',
            ),
            "binary task": (body + "\0| E2 |\n", body),
        }
        for name, (after, before) in cases.items():
            with self.subTest(name):
                self.git("reset", "--quiet", "--hard", self.reviewed)
                self.write(TASK, before)
                self.reviewed = self.commit(f"{name} before")
                self.write(TASK, after)
                self.commit(name)
                self.assertEqual(self.classify()["verdict"], "REREVIEW", name)
        for name, text in {
            "schema change": '{"schema_version": "2", "entries": [{"id": "A-1", "state": "open"}]}\n',
            "new key": '{"extra": 1, "entries": [{"id": "A-1", "state": "open"}]}\n',
        }.items():
            with self.subTest(name):
                self.git("reset", "--quiet", "--hard", self.reviewed)
                self.write(LEDGER, LEDGER_ONE)
                self.reviewed = self.commit(f"{name} before")
                self.write(LEDGER, text)
                self.commit(name)
                self.assertEqual(self.classify()["verdict"], "REREVIEW", name)

    def test_rewritten_history_needs_a_full_review(self):
        self.write(TASK, "| EVD-001 | PASS |\n| EVD-002 | PASS |\n")
        self.git("add", "-A")
        self.git("commit", "--quiet", "--amend", "-m", "amended")
        result = self.classify()
        self.assertEqual(result["verdict"], "REREVIEW")
        self.assertIn("not an ancestor", result["reason"])

    def test_the_cli_exit_code_follows_the_verdict(self):
        script = str(ROOT / "scripts" / "review_delta.py")
        run = [sys.executable, script, "--root", str(self.root), "--reviewed"]
        self.assertEqual(
            subprocess.run([*run, self.reviewed], capture_output=True).returncode, 0
        )
        self.write("scripts/tool.py", "print('c')\n")
        self.commit("code")
        done = subprocess.run([*run, self.reviewed], capture_output=True, text=True)
        self.assertEqual(done.returncode, 1)
        self.assertIn("REREVIEW", done.stdout)
        bad = subprocess.run([*run, "not-a-commit"], capture_output=True, text=True)
        self.assertEqual(bad.returncode, 2)


if __name__ == "__main__":
    unittest.main()
