"""Session capture contract (W08-CAPTURE): pointers and structured events only."""

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


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


MEMORY = _load("workspace_memory", "scripts/workspace_memory.py")
CAPTURE = _load("session_capture", "scripts/session_capture.py")
PRIVATE_TEXT = "prompt text that must never be stored"


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


class SessionCaptureTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="session-capture-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        git(self.root, "init", "-q")
        MEMORY.Store.init(self.root)
        self.claude_home = self.base / "claude-home"
        self.codex_home = self.base / "codex-home"
        environment = mock.patch.dict(
            os.environ,
            {
                "CLAUDE_CONFIG_DIR": str(self.claude_home),
                "CODEX_HOME": str(self.codex_home),
            },
        )
        environment.start()
        self.addCleanup(environment.stop)
        self.capture = CAPTURE.Capture.open(self.root)
        self.transcript = self.claude_file("s-1.jsonl")

    def claude_file(self, name: str) -> Path:
        path = self.claude_home / "projects" / "repo" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")
        return path

    def codex_file(self, name: str) -> Path:
        path = self.codex_home / "sessions" / "2026" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")
        return path

    def hook(self, event: str, provider: str = "claude", **fields):
        payload = {
            "hook_event_name": event,
            "session_id": "s-1",
            "transcript_path": str(self.transcript),
            "cwd": str(self.root),
        } | fields
        return self.capture.hook(provider, payload)

    def append(self, *records: dict, path: Path | None = None, tail: str = "") -> None:
        with (path or self.transcript).open("a", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record) + "\n")
            handle.write(tail)

    def stored_bytes(self) -> bytes:
        return self.capture.path.read_bytes()

    def test_hook_keeps_only_allowed_fields_and_deduplicates(self) -> None:
        for _ in range(2):
            self.hook(
                "Stop",
                prompt=PRIVATE_TEXT,
                last_assistant_message=PRIVATE_TEXT,
                tool_input={"command": PRIVATE_TEXT},
            )
        events = self.capture.status("claude", "s-1")["events"]
        self.assertEqual([e["event"] for e in events], ["Stop"])
        self.assertNotIn(PRIVATE_TEXT.encode(), self.stored_bytes())

    def test_hook_from_another_workspace_is_ignored(self) -> None:
        other = self.base / "other"
        other.mkdir()
        git(other, "init", "-q")
        MEMORY.Store.init(other)
        payload = {"hook_event_name": "Stop", "session_id": "s-2", "cwd": str(other)}
        result = CAPTURE.run_hook("claude", json.dumps(payload), root=self.root)
        self.assertEqual(result["outcome"], "ignored")
        self.assertEqual(self.capture.sessions(), [])
        self.assertEqual(CAPTURE.Capture.open(other).sessions(), [])

    def test_hook_failure_never_raises(self) -> None:
        self.capture.path.write_bytes(b"not a database")
        payload = {
            "hook_event_name": "Stop",
            "session_id": "s-1",
            "cwd": str(self.root),
        }
        result = CAPTURE.run_hook("claude", json.dumps(payload), root=self.root)
        self.assertEqual(result["outcome"], "failed")

    def test_transcript_outside_the_provider_session_directory_is_never_read(
        self,
    ) -> None:
        outside = self.base / "credentials.json"
        outside.write_text(json.dumps({"type": "service_account"}) + "\n")
        linked = self.claude_home / "projects" / "repo" / "linked.jsonl"
        linked.symlink_to(outside)
        for path in (outside, linked, self.codex_file("rollout.jsonl")):
            with self.subTest(path=path.name):
                self.hook("SessionStart", session_id="s-x", transcript_path=str(path))
                self.capture.scan()
                status = self.capture.status("claude", "s-x")
                self.assertEqual(
                    (status["transcript_path"], status["completeness"]),
                    (None, "unavailable"),
                )
        self.assertNotIn(b"service_account", self.stored_bytes())

    def test_line_fields_that_are_not_identifiers_are_never_stored(self) -> None:
        self.hook("SessionStart", source="startup")
        self.append(
            {
                "type": PRIVATE_TEXT,
                "timestamp": "password=hunter2",
                "message": {"content": [{"type": "tool_use", "name": PRIVATE_TEXT}]},
            },
            {"type": "user", "timestamp": "2026-11-18T09:40:18.123Z"},
        )
        self.capture.scan()
        records = self.capture.status("claude", "s-1")["records"]
        self.assertEqual(
            [(r["kind"], r["occurred_at"], r["tool"]) for r in records],
            [("other", None, "other"), ("user", "2026-11-18T09:40:18.123Z", None)],
        )
        for text in (PRIVATE_TEXT.encode(), b"hunter2"):
            self.assertNotIn(text, self.stored_bytes())

    def test_scan_records_structure_not_text(self) -> None:
        self.hook("SessionStart", source="startup")
        self.append(
            {"type": "user", "message": {"content": PRIVATE_TEXT}},
            {
                "type": "assistant",
                "message": {"content": [{"type": "tool_use", "name": "Bash"}]},
            },
        )
        self.capture.scan()
        records = self.capture.status("claude", "s-1")["records"]
        self.assertEqual(
            [(r["kind"], r["tool"]) for r in records],
            [("user", None), ("assistant", "Bash")],
        )
        self.assertNotIn(PRIVATE_TEXT.encode(), self.stored_bytes())

    def test_partial_tail_waits_and_rescan_never_duplicates(self) -> None:
        self.hook("SessionStart", source="startup")
        self.append({"type": "user"}, tail='{"type": "assist')
        self.capture.scan()
        status = self.capture.status("claude", "s-1")
        self.assertEqual(
            (len(status["records"]), status["completeness"]), (1, "partial")
        )
        with self.transcript.open("a", encoding="utf-8") as handle:
            handle.write('ant"}\r\n')
        self.capture.scan()
        self.capture.scan()
        self.assertEqual(len(self.capture.status("claude", "s-1")["records"]), 2)

    def test_scan_commits_in_bounded_batches(self) -> None:
        self.hook("SessionStart", source="startup")
        self.append(*({"type": "user"} for _ in range(5)))
        with mock.patch.object(CAPTURE, "SCAN_CHUNK_LIMIT", 20):
            self.capture.scan()
        self.assertEqual(len(self.capture.status("claude", "s-1")["records"]), 5)

    def test_a_line_longer_than_one_batch_is_reported_not_skipped(self) -> None:
        self.hook("SessionStart", source="startup")
        self.append({"type": "user", "pad": "x" * 100})
        self.hook("SessionEnd", reason="exit")
        with mock.patch.object(CAPTURE, "SCAN_CHUNK_LIMIT", 20):
            self.capture.scan()
        status = self.capture.status("claude", "s-1")
        self.assertEqual((status["records"], status["completeness"]), ([], "partial"))
        self.assertTrue(status["oversized_line"])

    def test_session_end_alone_is_not_complete_and_resume_reopens(self) -> None:
        self.hook("SessionStart", source="startup")
        self.append({"type": "user"})
        self.hook("SessionEnd", reason="exit")
        self.assertEqual(
            self.capture.status("claude", "s-1")["completeness"], "partial"
        )
        self.capture.scan()
        self.assertEqual(
            self.capture.status("claude", "s-1")["completeness"], "complete"
        )
        self.append({"type": "assistant"})
        self.assertEqual(
            self.capture.status("claude", "s-1")["completeness"], "partial"
        )
        self.capture.scan()
        self.hook("SessionStart", source="resume")
        self.assertEqual(
            self.capture.status("claude", "s-1")["completeness"], "partial"
        )

    def test_replaced_file_of_equal_size_is_not_complete(self) -> None:
        self.hook("SessionStart", source="startup")
        self.append({"type": "user"})
        self.hook("SessionEnd", reason="exit")
        self.capture.scan()
        replacement = self.transcript.with_suffix(".new")
        replacement.write_bytes(self.transcript.read_bytes())
        replacement.replace(self.transcript)
        self.assertEqual(
            self.capture.status("claude", "s-1")["completeness"], "partial"
        )

    def test_crash_before_cursor_advance_replays_without_duplicates(self) -> None:
        self.hook("SessionStart", source="startup")
        self.append({"type": "user"}, {"type": "user"})
        self.capture.scan()
        with self.capture._connect() as connection:
            connection.execute("update cursor set offset = 0, last_line_sha256 = null")
        self.capture.scan()
        status = self.capture.status("claude", "s-1")
        self.assertEqual((len(status["records"]), status["modified"]), (2, False))

    def test_rewritten_transcript_is_marked_modified(self) -> None:
        self.hook("SessionStart", source="startup")
        self.append({"type": "user"})
        self.capture.scan()
        self.transcript.write_text(
            json.dumps({"type": "other"}) + "\n", encoding="utf-8"
        )
        self.capture.scan()
        status = self.capture.status("claude", "s-1")
        self.assertTrue(status["modified"])
        self.assertEqual(status["completeness"], "partial")

    def test_codex_ordinal_gap_is_reported(self) -> None:
        rollout = self.codex_file("rollout.jsonl")
        self.hook("SessionStart", provider="codex", transcript_path=str(rollout))
        self.append(
            {"type": "session_meta", "ordinal": 1, "payload": {}},
            {
                "type": "response_item",
                "ordinal": 3,
                "payload": {
                    "type": "function_call",
                    "name": "shell",
                    "arguments": PRIVATE_TEXT,
                },
            },
            path=rollout,
        )
        self.hook("SessionEnd", provider="codex", transcript_path=str(rollout))
        self.capture.scan()
        status = self.capture.status("codex", "s-1")
        self.assertEqual(status["ordinal_gaps"], 1)
        self.assertEqual(status["completeness"], "partial")
        self.assertEqual(status["records"][1]["kind"], "response_item/function_call")
        self.assertEqual(status["records"][1]["tool"], "shell")
        self.assertNotIn(PRIVATE_TEXT.encode(), self.stored_bytes())

    def test_missing_transcript_is_unavailable(self) -> None:
        self.hook("SessionStart", transcript_path=None)
        self.capture.scan()
        self.assertEqual(
            self.capture.status("claude", "s-1")["completeness"], "unavailable"
        )

    def test_forgotten_session_is_never_captured_again(self) -> None:
        self.hook("SessionStart", source="startup")
        self.append({"type": "user"})
        self.capture.scan()
        moved = self.claude_file("s-1-moved.jsonl")
        self.append({"type": "user"}, path=moved)
        self.hook("Stop", transcript_path=str(moved))
        self.capture.scan()
        with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_SCHEMA"):
            self.capture.forget("claude", "s-1", owner="platform", approval_ref=" ")
        self.capture.forget("claude", "s-1", owner="platform", approval_ref="user")
        self.assertEqual(self.hook("Stop")["outcome"], "ignored")
        self.capture.scan()
        self.assertEqual(self.capture.sessions(), [])
        with self.capture._connect() as connection:
            for table in ("record", "cursor", "event"):
                self.assertEqual(
                    connection.execute(f"select count(*) from {table}").fetchone()[0], 0
                )

    def test_scan_after_forget_writes_nothing(self) -> None:
        self.hook("SessionStart", source="startup")
        self.append({"type": "user"})
        self.capture.forget("claude", "s-1", owner="platform", approval_ref="user")
        self.assertEqual(
            self.capture._scan_file("claude", "s-1", str(self.transcript)), "forgotten"
        )
        with self.capture._connect() as connection:
            self.assertEqual(
                connection.execute("select count(*) from record").fetchone()[0], 0
            )

    def test_forgetting_one_session_keeps_another_on_the_same_file(self) -> None:
        self.hook("SessionStart", source="startup")
        self.hook("SessionStart", session_id="s-2", source="startup")
        self.append({"type": "user"})
        self.capture.scan()
        self.capture.forget("claude", "s-1", owner="platform", approval_ref="user")
        self.assertEqual(len(self.capture.status("claude", "s-2")["records"]), 1)
        self.capture.forget("claude", "S-2", owner="platform", approval_ref="user")
        self.assertEqual(len(self.capture.status("claude", "s-2")["records"]), 1)

    def test_subagent_transcript_is_its_own_cursor_and_can_be_forgotten(self) -> None:
        agent = self.claude_file("agent.jsonl")
        self.append({"type": "assistant"}, path=agent)
        self.hook("SessionStart", source="startup")
        self.hook("SubagentStop", agent_id="a-1", agent_transcript_path=str(agent))
        self.capture.scan()
        sessions = {(s["provider"], s["session_id"]) for s in self.capture.sessions()}
        self.assertEqual(sessions, {("claude", "s-1"), ("claude", "s-1/agent/a-1")})
        child = "s-1/agent/a-1"
        self.assertEqual(len(self.capture.status("claude", child)["records"]), 1)
        self.capture.forget("claude", child, owner="platform", approval_ref="user")
        self.hook("SubagentStop", agent_id="a-1", agent_transcript_path=str(agent))
        self.assertEqual({s["session_id"] for s in self.capture.sessions()}, {"s-1"})

    def test_cli_hook_reads_stdin_and_prints_nothing(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/session_capture.py"),
                "--root",
                str(self.root),
                "hook",
                "--provider",
                "claude",
            ],
            input=json.dumps(
                {"hook_event_name": "Stop", "session_id": "s-9", "cwd": str(self.root)}
            ),
            capture_output=True,
            text=True,
            cwd=self.root,
            timeout=30,
        )
        self.assertEqual((result.returncode, result.stdout), (0, ""))
        self.assertEqual([s["session_id"] for s in self.capture.sessions()], ["s-9"])


if __name__ == "__main__":
    unittest.main()
