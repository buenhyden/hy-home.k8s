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

    def test_scan_records_structure_and_the_selected_prompt(self) -> None:
        # Q02 (SPEC-0233): the visible prompt is selected content; structure is unchanged.
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
        self.assertEqual(
            [
                (c["role"], c["selection"], c["text"])
                for c in self.capture.contents("claude", "s-1")
            ],
            [("prompt", "selected", PRIVATE_TEXT)],
        )

    def test_tool_failure_is_recorded_as_a_flag_and_selected_evidence(self) -> None:
        self.hook("SessionStart", source="startup")
        self.append(
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "is_error": True,
                            "content": PRIVATE_TEXT,
                        }
                    ]
                },
            },
            {"type": "user", "message": {"content": [{"type": "tool_result"}]}},
            {"type": "assistant"},
        )
        rollout = self.codex_file("rollout-errors.jsonl")
        self.hook(
            "SessionStart",
            provider="codex",
            session_id="c-1",
            transcript_path=str(rollout),
        )
        self.append(
            {
                "type": "event_msg",
                "payload": {"type": "exec_command_end", "exit_code": 2},
            },
            {
                "type": "event_msg",
                "payload": {"type": "exec_command_end", "exit_code": 0},
            },
            path=rollout,
        )
        self.capture.scan()
        claude = [r["error"] for r in self.capture.status("claude", "s-1")["records"]]
        codex = [r["error"] for r in self.capture.status("codex", "c-1")["records"]]
        self.assertEqual((claude, codex), ([1, 0, None], [1, 0]))
        failed = self.capture.contents("claude", "s-1")[0]
        self.assertEqual(
            (failed["failure_class"], failed["selection"], failed["text"]),
            ("command_failed", "selected", PRIVATE_TEXT),
        )

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


class SelectedContentTest(unittest.TestCase):
    """Q02/D10 selected content (SPEC-0233): redacted, abridged, bounded, expiring."""

    setUp = SessionCaptureTest.setUp
    claude_file = SessionCaptureTest.claude_file
    hook = SessionCaptureTest.hook
    append = SessionCaptureTest.append
    stored_bytes = SessionCaptureTest.stored_bytes

    def contents(self):
        return self.capture.contents("claude", "s-1")

    @staticmethod
    def prompt(text, when="2026-11-18T09:00:00Z"):
        return {"type": "user", "timestamp": when, "message": {"content": text}}

    @staticmethod
    def answer(text, when="2026-11-18T09:00:01Z"):
        return {
            "type": "assistant",
            "timestamp": when,
            "message": {"content": [{"type": "text", "text": text}]},
        }

    @staticmethod
    def result(text, call="toolu_1", error=False, when="2026-11-18T09:00:02Z"):
        return {
            "type": "user",
            "timestamp": when,
            "message": {
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": call,
                        "is_error": error,
                        "content": text,
                    }
                ]
            },
        }

    def test_redaction_runs_on_the_whole_value_before_it_is_cut(self) -> None:
        secret = "sk-ant-" + "Q" * 40  # pragma: allowlist secret
        self.hook("SessionStart", source="startup")
        self.append(self.prompt("x" * 16370 + " " + secret + " mail a@b.example"))
        self.capture.scan()
        (row,) = self.contents()
        self.assertEqual((row["role"], row["selection"]), ("prompt", "selected"))
        self.assertLessEqual(len(row["text"].encode()), CAPTURE.SELECTED_LIMIT)
        self.assertTrue(row["truncated"])
        self.assertNotIn(b"sk-ant-", self.stored_bytes())
        self.assertNotIn(b"a@b.example", self.stored_bytes())

    def test_a_turn_keeps_its_final_response_and_abridges_earlier_ones(self) -> None:
        self.hook("SessionStart", source="startup")
        self.append(
            self.prompt("fix the link"),
            self.answer("draft " * 2000),
            self.answer("final answer"),
        )
        self.capture.scan()
        rows = {r["offset"]: r for r in self.contents()}
        first, second = sorted(o for o, r in rows.items() if r["role"] == "response")
        self.assertEqual(rows[first]["selection"], "summary")
        self.assertLessEqual(
            len(rows[first]["text"].encode()), CAPTURE.SUMMARY_TURN_LIMIT
        )
        self.assertEqual(
            (rows[second]["selection"], rows[second]["text"]),
            ("selected", "final answer"),
        )

    def test_tool_results_carry_call_ids_and_failure_classes(self) -> None:
        self.hook("SessionStart", source="startup")
        self.append(
            self.prompt("run it"),
            self.result(
                "Permission to use Bash with command ls has been denied.", "c1", True
            ),
            self.result(
                "PreToolUse:Edit hook error: [FAIL] BRIEF-MISSING: x", "c2", True
            ),
            self.result("Exit code 1\nboom", "c3", True),
            self.result("ok output", "c4", False),
        )
        self.capture.scan()
        results = [r for r in self.contents() if r["role"] == "tool_result"]
        self.assertEqual(
            [(r["call_id"], r["failure_class"], r["selection"]) for r in results],
            [
                ("c1", "permission_denied", "selected"),
                ("c2", "hook_rejected", "selected"),
                ("c3", "command_failed", "selected"),
                ("c4", None, "summary"),
            ],
        )
        records = self.capture.status("claude", "s-1")["records"]
        self.assertIn("permission_denied", [r["failure_class"] for r in records])

    def test_hidden_reasoning_and_tool_arguments_are_never_stored(self) -> None:
        self.hook("SessionStart", source="startup")
        self.append(
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "thinking", "thinking": "hidden-thought-text"},
                        {
                            "type": "tool_use",
                            "name": "Bash",
                            "input": {"command": "argument-text"},
                        },
                    ]
                },
            },
            {
                "type": "user",
                "isMeta": True,
                "message": {"content": "injected-meta-text"},
            },
        )
        self.capture.scan()
        self.assertEqual(self.contents(), [])
        for text in (b"hidden-thought-text", b"argument-text", b"injected-meta-text"):
            self.assertNotIn(text, self.stored_bytes())

    def test_redelivery_stores_each_line_once(self) -> None:
        self.hook("SessionStart", source="startup")
        self.append(self.prompt("same"), self.prompt("same"))
        for _ in range(2):
            self.capture.scan()
        self.assertEqual(len(self.contents()), 2)

    def test_content_expires_at_30_days_and_metadata_at_90(self) -> None:
        self.hook("SessionStart", source="startup")
        self.append(
            self.prompt("old prompt", "2026-08-01T00:00:00Z"),
            self.result("ok output", "c9", False, "2026-08-01T00:00:01Z"),
        )
        self.capture.scan()
        self.capture.expire(
            now=CAPTURE.dt.datetime(2026, 9, 5, tzinfo=CAPTURE.dt.timezone.utc)
        )
        self.assertEqual([r["selection"] for r in self.contents()], ["summary"])
        later = CAPTURE.dt.datetime.now(CAPTURE.dt.timezone.utc) + CAPTURE.dt.timedelta(
            days=91
        )
        self.capture.expire(now=later)
        self.assertEqual(self.capture.sessions(), [])
        self.capture.scan()
        self.assertNotIn(b"old prompt", self.stored_bytes())

    def test_a_full_body_store_records_a_gap_not_the_text(self) -> None:
        self.hook("SessionStart", source="startup")
        self.append(self.prompt("first"), self.prompt("second"))
        with mock.patch.object(CAPTURE, "BODY_STORE_LIMIT", 5):
            self.capture.scan()
        rows = self.contents()
        self.assertEqual(
            [(r["selection"], r["gap"]) for r in rows][-1], ("gap", "capacity")
        )
        self.assertNotIn(b"second", self.stored_bytes())


if __name__ == "__main__":
    unittest.main()
