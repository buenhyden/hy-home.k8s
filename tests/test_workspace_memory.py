"""Shared workspace memory store contract (SPEC-0109 VAL-MEMORY-001)."""

from __future__ import annotations

import importlib.util
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "workspace_memory", ROOT / "scripts/workspace_memory.py"
)
assert SPEC is not None and SPEC.loader is not None
MEMORY = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MEMORY
SPEC.loader.exec_module(MEMORY)

SHORT = {"context": "Task context", "narrative": "why the check failed"}


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


class WorkspaceMemoryTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="workspace-memory-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "repo"
        self.root.mkdir()
        git(self.root, "init", "-q")
        git(self.root, "config", "user.email", "test@example.invalid")
        git(self.root, "config", "user.name", "test")
        (self.root / "policy.md").write_text("v1\n", encoding="utf-8")
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", "fixture")
        self.store = MEMORY.Store.init(self.root)

    def write(self, **changes):
        values = {
            "tier": "short-term",
            "body": SHORT,
            "owner": "platform",
            "source_refs": [],
        } | changes
        return self.store.write(**values)

    def test_store_is_never_created_implicitly(self) -> None:
        other = Path(self.root.parent) / "other"
        other.mkdir()
        git(other, "init", "-q")
        with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_UNAVAILABLE"):
            MEMORY.Store.open(other)
        self.assertFalse((other / MEMORY.STORE_DIR).exists())
        with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_EXISTS"):
            MEMORY.Store.init(self.root)

    def test_linked_worktree_resolves_the_same_database(self) -> None:
        linked = self.root.parent / "linked"
        git(self.root, "worktree", "add", "-q", "--detach", str(linked))
        memory = self.write()
        opened = MEMORY.Store.open(linked)
        self.assertEqual(opened.path, self.store.path)
        self.assertEqual(opened.get(memory["memory_id"])["body"], SHORT)
        self.assertEqual(opened.workspace_id, self.store.workspace_id)

    def test_tier_schema_and_task_state_copies_are_rejected(self) -> None:
        for tier, body in (
            ("short-term", {"context": "x"}),
            ("long-term", {"claim": "x"}),
            ("domain", {"symptom": "x", "cause": "y"}),
            ("short-term", SHORT | {"status": "completed"}),
            ("unknown", SHORT),
        ):
            with self.subTest(tier=tier, body=body):
                with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_SCHEMA"):
                    self.write(tier=tier, body=body)
        with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_SCHEMA"):
            self.write(sensitivity="secret")
        domain = self.write(
            tier="domain",
            domain_id="gitops",
            body={"symptom": "s", "cause": "c", "resolution": "r"},
        )
        self.assertEqual(self.store.get(domain["memory_id"])["domain_id"], "gitops")

    def test_revision_conflict_is_kept_without_last_write_wins(self) -> None:
        first = self.write()
        second = self.write(
            memory_id=first["memory_id"],
            expected_revision=1,
            body=SHORT | {"narrative": "revised"},
        )
        self.assertEqual(second["revision"], 2)
        stale = self.write(
            memory_id=first["memory_id"],
            expected_revision=1,
            body=SHORT | {"narrative": "stale"},
        )
        self.assertEqual(stale["outcome"], "conflict")
        self.assertTrue(stale["stored"])
        self.assertEqual(stale["current_revision"], 2)
        current = self.store.get(first["memory_id"])
        self.assertEqual(current["body"]["narrative"], "revised")
        history = self.store.history(first["memory_id"])
        self.assertEqual([item["revision"] for item in history["revisions"]], [1, 2])
        self.assertEqual(len(history["conflicts"]), 1)

    def test_concurrent_writers_with_one_expected_revision_never_both_win(self) -> None:
        first = self.write()
        body = self.root.parent / "race.json"
        body.write_text(json.dumps(SHORT), encoding="utf-8")
        command = [
            sys.executable,
            str(ROOT / "scripts/workspace_memory.py"),
            "--root",
            str(self.root),
            "write",
            "--tier",
            "short-term",
            "--owner",
            "platform",
            "--body-file",
            str(body),
            "--memory-id",
            first["memory_id"],
            "--expected-revision",
            "1",
        ]
        racers = [
            subprocess.Popen(command, stdout=subprocess.PIPE, text=True)
            for _ in range(4)
        ]
        outcomes = sorted(
            json.loads(racer.communicate()[0])["outcome"] for racer in racers
        )
        self.assertEqual(outcomes, ["conflict", "conflict", "conflict", "written"])
        self.assertEqual(self.store.get(first["memory_id"])["revision"], 2)

    def test_idempotent_retry_returns_the_first_result(self) -> None:
        first = self.write(idempotency_key="retry-1")
        again = self.write(idempotency_key="retry-1")
        self.assertEqual(first["memory_id"], again["memory_id"])
        self.assertEqual(self.store.usage()["tiers"]["short-term"]["revisions"], 1)

    def test_capacity_refusal_keeps_existing_memory(self) -> None:
        kept = self.write()
        before = self.store.usage()["tiers"]["short-term"]["bytes"]
        limits = dict(MEMORY.TIER_LIMITS) | {"short-term": before + 10}
        with mock.patch.object(MEMORY, "TIER_LIMITS", limits):
            with self.assertRaisesRegex(
                MEMORY.MemoryError_, "MEMORY_CAPACITY_EXCEEDED"
            ):
                self.write(body=SHORT | {"narrative": "x" * 100})
            refused = self.write(
                memory_id=kept["memory_id"],
                expected_revision=0,
                body=SHORT | {"narrative": "y" * 100},
            )
        self.assertEqual(refused["outcome"], "conflict")
        self.assertFalse(refused["stored"])
        self.assertEqual(self.store.usage()["tiers"]["short-term"]["bytes"], before)
        self.assertEqual(self.store.get(kept["memory_id"])["body"], SHORT)
        with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_CAPACITY_EXCEEDED"):
            self.write(body={"context": "c", "narrative": "z" * MEMORY.REVISION_LIMIT})

    def test_default_query_excludes_stale_sources_but_history_keeps_them(self) -> None:
        fresh = self.write(source_refs=["policy.md"])
        self.store.set_eligibility(fresh["memory_id"], "current", expected_revision=1)
        candidate = self.write()
        self.assertEqual(
            [item["memory_id"] for item in self.store.query()], [fresh["memory_id"]]
        )
        (self.root / "policy.md").write_text("v2\n", encoding="utf-8")
        self.assertEqual(self.store.query(), [])
        stale = self.store.query(include_stale=True)
        self.assertEqual(stale[0]["stale_sources"], ["policy.md"])
        self.assertEqual(
            self.store.get(candidate["memory_id"])["eligibility"], "candidate"
        )

    def test_no_api_deletes_memory_and_backup_preserves_all_revisions(self) -> None:
        self.assertFalse(
            [name for name in dir(MEMORY.Store) if "delete" in name or "purge" in name]
        )
        first = self.write()
        self.write(memory_id=first["memory_id"], expected_revision=1, body=SHORT)
        result = self.store.backup()
        with sqlite3.connect(result["path"]) as copy:
            self.assertEqual(
                copy.execute("select count(*) from revision").fetchone()[0], 2
            )
        with mock.patch.object(MEMORY.os, "replace", side_effect=OSError("disk full")):
            with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_BACKUP_FAILED"):
                self.store.backup()
        with sqlite3.connect(result["path"]) as copy:
            self.assertEqual(
                copy.execute("select count(*) from revision").fetchone()[0], 2
            )
        self.assertLessEqual(
            len(os.listdir(self.store.path.parent)), MEMORY.RUNTIME_FILE_LIMIT
        )

    def test_rollback_journal_is_used(self) -> None:
        with sqlite3.connect(self.store.path) as connection:
            self.assertEqual(
                connection.execute("pragma journal_mode").fetchone()[0], "delete"
            )

    def test_cli_round_trip(self) -> None:
        body = self.root.parent / "body.json"
        body.write_text(json.dumps(SHORT), encoding="utf-8")
        script = ROOT / "scripts/workspace_memory.py"
        written = json.loads(
            subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--root",
                    str(self.root),
                    "write",
                    "--tier",
                    "short-term",
                    "--owner",
                    "platform",
                    "--body-file",
                    str(body),
                ],
                check=True,
                capture_output=True,
                text=True,
            ).stdout
        )
        read = json.loads(
            subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--root",
                    str(self.root),
                    "get",
                    written["memory_id"],
                ],
                check=True,
                capture_output=True,
                text=True,
            ).stdout
        )
        self.assertEqual(read["body"], SHORT)
        missing = subprocess.run(
            [
                sys.executable,
                str(script),
                "--root",
                str(self.root),
                "get",
                "mem-absent",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(missing.returncode, 2)
        self.assertIn("MEMORY_NOT_FOUND", missing.stderr)


if __name__ == "__main__":
    unittest.main()
