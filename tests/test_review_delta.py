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
EVIDENCE_HEADER = (
    "## Verification Evidence\n### Results\n"
    "| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |\n"
    "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
)
EVD_ONE = "| EVD-001 | AC-1 | WORK-001 | automated | fixture | none | Check fixture | 0 | PASS | here | true | none |\n"
EVD_TWO = "| EVD-002 | AC-1 | WORK-001 | automated | fixture | none | Check fixture | 0 | PASS | here | true | none |\n"


def task_text(rows: str = EVD_ONE, *, version: str = "0.1.0") -> str:
    return f'---\nversion: "{version}"\nupdated: "2026-11-20"\n---\n{EVIDENCE_HEADER}{rows}'


class ReviewDeltaTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="review-delta-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.git("init", "--quiet", "--initial-branch=main")
        self.write(TASK, task_text())
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
            TASK,
            task_text(EVD_ONE + EVD_TWO, version="0.1.1").replace(
                'updated: "2026-11-20"', 'updated: "2026-11-21"'
            ),
        )
        self.commit("evidence")
        result = self.classify()
        self.assertEqual(result["verdict"], "EVIDENCE_ONLY")
        self.assertEqual(result["evidence"], [TASK])

    def test_factual_row_before_a_following_section_keeps_the_review(self):
        following = "\n### Residue Handoff\n| ID | State |\n| --- | --- |\n"
        self.write(TASK, task_text() + following)
        self.reviewed = self.commit("reviewed task with following section")
        self.write(TASK, task_text(EVD_ONE + EVD_TWO) + following)
        self.commit("factual result")
        self.assertEqual(self.classify()["evidence"], [TASK])

    def test_factual_evidence_in_other_table_or_prose_needs_review(self):
        for text in (
            task_text() + "New acceptance condition.\n",
            task_text() + "\n## Acceptance Decision\n" + EVD_TWO,
            task_text() + "\n| Requirement | New rule |\n",
        ):
            with self.subTest(text=text[-45:]):
                self.git("reset", "--quiet", "--hard", self.reviewed)
                self.write(TASK, text)
                self.commit("semantic task addition")
                self.assertEqual(self.classify()["rereview"], [TASK])

    def test_authority_receipt_cannot_hide_in_an_evidence_row(self):
        for command in (
            "Scoped execution approval",
            "Spec/Plan first-record approval",
            "Criterion acceptance",
            "Requirement adoption",
            "Authority granted",
        ):
            with self.subTest(command=command):
                self.git("reset", "--quiet", "--hard", self.reviewed)
                self.write(
                    TASK, task_text(EVD_ONE + EVD_TWO.replace("Check fixture", command))
                )
                self.commit("authority receipt")
                self.assertEqual(self.classify()["rereview"], [TASK])

    def test_normative_evidence_payload_needs_review(self):
        self.write(
            TASK,
            task_text(
                EVD_ONE
                + EVD_TWO.replace(
                    "| fixture | none |", "| New requirement grants access | none |"
                )
            ),
        )
        self.commit("semantic evidence payload")
        self.assertEqual(self.classify()["rereview"], [TASK])

    def test_metadata_addition_or_owner_replacement_needs_review(self):
        for text in (
            task_text().replace(
                'updated: "2026-11-20"', 'owner: "other"\nupdated: "2026-11-20"'
            ),
            task_text().replace('updated: "2026-11-20"', 'status: "approved"'),
        ):
            with self.subTest(text=text[:80]):
                self.git("reset", "--quiet", "--hard", self.reviewed)
                self.write(TASK, text)
                self.commit("metadata semantic change")
                self.assertEqual(self.classify()["rereview"], [TASK])

    def test_ledger_new_obligation_needs_review(self):
        self.write(LEDGER, LEDGER_TWO)
        self.commit("new residue obligation")
        self.assertEqual(self.classify()["rereview"], [LEDGER])

    def test_any_other_path_needs_rereview_of_that_path_only(self):
        self.write(TASK, task_text(EVD_ONE + EVD_TWO))
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
            "deleted row": task_text(""),
            "flipped result": task_text(EVD_ONE.replace("PASS", "FAIL")),
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
        self.write("docs/03.specs/0001-x/01.tasks/tsk-0002-y.md", task_text())
        self.commit("new task")
        self.assertEqual(self.classify()["verdict"], "REREVIEW")

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
        self.write(TASK, task_text(EVD_ONE + EVD_TWO))
        self.commit("regular again")
        self.assertEqual(self.classify()["verdict"], "REREVIEW")

    def test_a_commit_that_changes_no_path_needs_nothing(self):
        self.commit("empty")
        result = self.classify()
        self.assertEqual(result["verdict"], "NO_CHANGE")
        self.assertIn("no path changed", result["reason"])

    def test_growth_is_read_from_the_blobs_not_the_diff_text(self):
        body = task_text()
        cases = {
            "removed delimiter": (body.replace("---\n", "", 1), body),
            "removed dash line": (body + "-- keep\n", body + EVD_TWO),
            "version line outside front matter": (
                body + EVD_TWO,
                body + 'version: "9"\n',
            ),
            "binary task": (body + "\0" + EVD_TWO, body),
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
        self.write(TASK, task_text(EVD_ONE + EVD_TWO))
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
