"""Request intake, brief record and first-change admission (SPEC-0231)."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/request_brief.py"
spec = importlib.util.spec_from_file_location("request_brief", SCRIPT)
brief_module = importlib.util.module_from_spec(spec)
sys.modules["request_brief"] = brief_module
spec.loader.exec_module(brief_module)

BRIEF = {
    "goal": "Fix the link",
    "scope": ["docs/a.md"],
    "keep": [],
    "change": ["one link"],
    "questions": [],
    "checks": ["links"],
}


def _git(root: Path, *arguments: str) -> None:
    subprocess.run(
        ["git", "-C", str(root), *arguments], check=True, capture_output=True
    )


class RequestBriefTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        base = Path(self.temporary.name)
        self.root = base / "repo"
        self.root.mkdir()
        _git(self.root, "init", "-q", "-b", "main")
        (self.root / "AGENTS.md").write_text("policy\n")
        _git(self.root, "add", "AGENTS.md")
        _git(
            self.root,
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@example.invalid",
            "commit",
            "-qm",
            "init",
        )
        self.other = base / "other"
        self.other.mkdir()
        _git(self.other, "init", "-q")
        self.root_text = str(self.root.resolve())
        environment = {
            key: value
            for key, value in os.environ.items()
            if key != brief_module.STATE_ENV
        }
        self.environment = mock.patch.dict(os.environ, environment, clear=True)
        self.environment.start()

    def tearDown(self):
        self.environment.stop()
        self.temporary.cleanup()

    def intake(self, prompt="fix it", session="s1", turn=None):
        payload = {"session_id": session, "prompt": prompt}
        if turn:
            payload["turn_id"] = turn
        return brief_module.intake(payload, "claude", self.root_text)

    def refused(self, code, call, *arguments):
        with self.assertRaises(brief_module.Refusal) as caught:
            call(*arguments)
        self.assertEqual(caught.exception.code, code)

    def test_read_only_intake_then_shown_brief_admits_the_first_change(self):
        receipt = self.intake()
        stored = brief_module.state_dir(self.root_text)
        text = "".join(path.read_text() for path in stored.glob("*.json"))
        self.assertNotIn("fix it", text, "the prompt text is never kept")
        self.refused(
            "BRIEF-NOT-SHOWN",
            brief_module.admit,
            {"session_id": "s1"},
            "claude",
            self.root_text,
        )
        brief_module.record(receipt["request_id"], BRIEF, self.root_text)
        shown = brief_module.admit({"session_id": "s1"}, "claude", self.root_text)
        self.assertIn(receipt["request_id"], shown)
        self.assertIn("Fix the link", shown)
        self.assertIsNone(
            brief_module.admit({"session_id": "s1"}, "claude", self.root_text),
            "later changes of the same request pass without a second display",
        )

    def test_missing_receipt_or_session_is_refused(self):
        self.refused(
            "BRIEF-MISSING",
            brief_module.admit,
            {"session_id": "s1"},
            "claude",
            self.root_text,
        )
        self.refused("BRIEF-MISSING", brief_module.admit, {}, "claude", self.root_text)

    def test_a_new_request_makes_the_earlier_brief_stale(self):
        first = self.intake("first")
        brief_module.record(first["request_id"], BRIEF, self.root_text)
        brief_module.admit({"session_id": "s1"}, "claude", self.root_text)
        second = self.intake("changed request")
        self.assertEqual(second["generation"], 2)
        self.refused(
            "BRIEF-NOT-SHOWN",
            brief_module.admit,
            {"session_id": "s1"},
            "claude",
            self.root_text,
        )
        self.refused(
            "BRIEF-STALE",
            brief_module.record,
            first["request_id"],
            BRIEF,
            self.root_text,
        )

    def test_policy_or_branch_change_before_the_first_change_is_stale(self):
        receipt = self.intake()
        brief_module.record(receipt["request_id"], BRIEF, self.root_text)
        (self.root / "AGENTS.md").write_text("changed policy\n")
        self.refused(
            "BRIEF-STALE",
            brief_module.admit,
            {"session_id": "s1"},
            "claude",
            self.root_text,
        )
        receipt = self.intake()
        _git(self.root, "switch", "-qc", "other")
        self.refused(
            "BRIEF-STALE",
            brief_module.record,
            receipt["request_id"],
            BRIEF,
            self.root_text,
        )

    def test_dispatch_needs_the_current_recorded_brief(self):
        receipt = self.intake()
        request = receipt["request_id"]
        self.refused("BRIEF-NOT-SHOWN", brief_module.current, request, self.root_text)
        brief_module.record(request, BRIEF, self.root_text)
        self.assertEqual(
            brief_module.current(request, self.root_text)["request_id"], request
        )
        brief_module.admit({"session_id": "s1"}, "claude", self.root_text)
        _git(self.root, "switch", "-qc", "work")
        self.assertEqual(
            brief_module.current(request, self.root_text)["state"],
            "admitted",
            "an admitted request may move to its work branch",
        )
        (self.root / "AGENTS.md").write_text("changed policy\n")
        self.refused("BRIEF-STALE", brief_module.current, request, self.root_text)
        (self.root / "AGENTS.md").write_text("policy\n")
        self.intake("next request")
        self.refused("BRIEF-STALE", brief_module.current, request, self.root_text)
        self.refused(
            "BRIEF-STALE",
            brief_module.current,
            request,
            str(self.other.resolve()),
        )

    def test_another_workspace_or_turn_is_refused(self):
        receipt = self.intake(turn="t1")
        brief_module.record(receipt["request_id"], BRIEF, self.root_text)
        with mock.patch.dict(
            os.environ,
            {brief_module.STATE_ENV: str(brief_module.state_dir(self.root_text))},
        ):
            self.refused(
                "BRIEF-WORKSPACE",
                brief_module.admit,
                {"session_id": "s1"},
                "claude",
                str(self.other.resolve()),
            )
        self.refused(
            "BRIEF-STALE",
            brief_module.admit,
            {"session_id": "s1", "turn_id": "t2"},
            "claude",
            self.root_text,
        )
        self.assertIsNotNone(
            brief_module.admit(
                {"session_id": "s1", "turn_id": "t1"}, "claude", self.root_text
            )
        )

    def test_an_incomplete_brief_is_refused(self):
        receipt = self.intake()
        for broken in (
            {**BRIEF, "goal": " "},
            {**BRIEF, "change": []},
            {key: value for key, value in BRIEF.items() if key != "checks"},
            {**BRIEF, "scope": [3]},
        ):
            self.refused(
                "BRIEF-SHAPE",
                brief_module.record,
                receipt["request_id"],
                broken,
                self.root_text,
            )

    def test_hook_intake_never_blocks_and_tells_the_model(self):
        environment = {**os.environ, "CLAUDE_PROJECT_DIR": self.root_text}
        run = subprocess.run(
            [sys.executable, str(SCRIPT), "intake", "--provider", "claude"],
            input=json.dumps({"session_id": "s9", "prompt": "do it"}),
            capture_output=True,
            text=True,
            env=environment,
            timeout=30,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        context = json.loads(run.stdout)["hookSpecificOutput"]
        self.assertEqual(context["hookEventName"], "UserPromptSubmit")
        self.assertIn("record --request", context["additionalContext"])
        broken = subprocess.run(
            [sys.executable, str(SCRIPT), "intake", "--provider", "claude"],
            input="{not json",
            capture_output=True,
            text=True,
            env=environment,
            timeout=30,
        )
        self.assertEqual((broken.returncode, broken.stdout), (0, ""))


if __name__ == "__main__":
    unittest.main()
