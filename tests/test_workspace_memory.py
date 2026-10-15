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

    def test_store_path_symlink_is_unavailable(self) -> None:
        external = self.root.parent / "moved.sqlite3"
        self.store.path.rename(external)
        self.store.path.symlink_to(external)
        with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_UNAVAILABLE"):
            MEMORY.Store.open(self.root)
        with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_UNAVAILABLE"):
            self.store.query()

    def test_linked_worktree_resolves_the_same_database(self) -> None:
        linked = self.root.parent / "linked"
        git(self.root, "worktree", "add", "-q", "--detach", str(linked))
        memory = self.write()
        opened = MEMORY.Store.open(linked)
        self.assertEqual(opened.path, self.store.path)
        self.assertEqual(opened.get(memory["memory_id"])["body"], SHORT)
        self.assertEqual(opened.workspace_id, self.store.workspace_id)

    def test_git_timeout_reports_the_store_unavailable(self) -> None:
        expired = subprocess.TimeoutExpired(["git"], MEMORY.GIT_TIMEOUT_SECONDS)
        with mock.patch.object(MEMORY.subprocess, "run", side_effect=expired):
            with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_UNAVAILABLE"):
                MEMORY.representative_root(Path("."))

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

    def test_idempotency_key_binds_the_complete_request(self) -> None:
        first = self.write(idempotency_key="bound")
        for changes in (
            {"body": SHORT | {"narrative": "different"}},
            {"source_refs": ["policy.md"]},
            {"owner": "another-owner"},
            {"memory_id": first["memory_id"], "expected_revision": 1},
        ):
            with self.subTest(changes=changes):
                with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_CONFLICT"):
                    self.write(idempotency_key="bound", **changes)
        self.assertEqual(self.store.usage()["tiers"]["short-term"]["revisions"], 1)

    def test_conflict_retry_replays_result_without_storing_or_charging_twice(
        self,
    ) -> None:
        first = self.write()
        self.write(memory_id=first["memory_id"], expected_revision=1)
        request = {
            "memory_id": first["memory_id"],
            "expected_revision": 1,
            "body": SHORT | {"narrative": "stale"},
            "idempotency_key": "stale-retry",
        }
        conflict = self.write(**request)
        used = self.store.usage()["tiers"]["short-term"]["bytes"]
        self.assertEqual(self.write(**request), conflict)
        self.assertEqual(len(self.store.history(first["memory_id"])["conflicts"]), 1)
        self.assertEqual(self.store.usage()["tiers"]["short-term"]["bytes"], used)
        for changes in ({"expected_revision": 0}, {"body": SHORT}):
            with self.subTest(changes=changes):
                with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_CONFLICT"):
                    self.write(**(request | changes))

    def test_conflict_history_retains_source_provenance(self) -> None:
        first = self.write()
        conflict = self.write(
            memory_id=first["memory_id"],
            expected_revision=0,
            source_refs=["policy.md"],
        )
        self.assertTrue(conflict["stored"])
        source_refs = self.store.history(first["memory_id"])["conflicts"][0][
            "source_refs"
        ]
        self.assertEqual([ref["path"] for ref in source_refs], ["policy.md"])
        self.assertEqual(len(source_refs[0]["sha256"]), 64)

    def test_legacy_unbound_idempotency_key_fails_closed_without_loss(self) -> None:
        first = self.write()
        with sqlite3.connect(self.store.path) as connection:
            connection.execute("drop table idempotency")
            connection.execute(
                "create table idempotency (key text primary key, result text not null)"
            )
            connection.execute(
                "insert into idempotency values (?, ?)",
                ("old-key", json.dumps(first)),
            )
        with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_CONFLICT"):
            self.write(idempotency_key="old-key")
        self.assertEqual(self.store.get(first["memory_id"])["body"], SHORT)
        self.assertEqual(self.write(idempotency_key="new-key")["revision"], 1)

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
                idempotency_key="capacity-conflict",
            )
            self.assertEqual(
                self.write(
                    memory_id=kept["memory_id"],
                    expected_revision=0,
                    body=SHORT | {"narrative": "y" * 100},
                    idempotency_key="capacity-conflict",
                ),
                refused,
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

    def test_source_symlinks_outside_repository_are_never_read(self) -> None:
        external = self.root.parent / "outside.txt"
        external.write_text("private fixture\n", encoding="utf-8")
        (self.root / "outside-link").symlink_to(external)
        with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_SCHEMA"):
            self.write(source_refs=["outside-link"])
        (self.root / "linked-dir").symlink_to(
            self.root.parent, target_is_directory=True
        )
        with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_SCHEMA"):
            self.write(source_refs=["linked-dir/outside.txt"])
        os.mkfifo(self.root / "pipe")
        with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_SCHEMA"):
            self.write(source_refs=["pipe"])
        fresh = self.write(source_refs=["policy.md"])
        self.store.set_eligibility(fresh["memory_id"], "current", expected_revision=1)
        (self.root / "policy.md").unlink()
        (self.root / "policy.md").symlink_to(external)
        self.assertEqual(self.store.query(), [])
        self.assertEqual(
            self.store.get(fresh["memory_id"])["stale_sources"], ["policy.md"]
        )

    def test_malformed_source_refs_have_a_stable_schema_error(self) -> None:
        for raw in ("./", None):
            with self.subTest(raw=raw):
                with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_SCHEMA"):
                    self.write(source_refs=[raw])

    def test_source_freshness_uses_the_callers_worktree(self) -> None:
        linked = self.root.parent / "linked-source"
        git(self.root, "worktree", "add", "-q", "--detach", str(linked))
        (linked / "policy.md").write_text("linked version\n", encoding="utf-8")
        linked_store = MEMORY.Store.open(linked)
        item = linked_store.write(
            tier="short-term", body=SHORT, owner="platform", source_refs=["policy.md"]
        )
        linked_store.set_eligibility(item["memory_id"], "current", expected_revision=1)
        self.assertEqual(len(linked_store.query()), 1)
        self.assertEqual(self.store.query(), [])

    def test_reconnected_database_retains_its_page_limit(self) -> None:
        with self.store._connect() as connection:
            page_size = connection.execute("pragma page_size").fetchone()[0]
            self.assertEqual(
                connection.execute("pragma max_page_count").fetchone()[0],
                MEMORY.DATABASE_LIMIT // page_size,
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

    def test_backup_rejects_existing_target_symlink(self) -> None:
        external = self.root.parent / "external-backup"
        external.write_text("untouched", encoding="utf-8")
        target = self.store.path.parent / MEMORY.BACKUP_NAME
        target.symlink_to(external)
        with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_BACKUP_FAILED"):
            self.store.backup()
        self.assertTrue(target.is_symlink())
        self.assertEqual(external.read_text(encoding="utf-8"), "untouched")

    def test_backup_preserves_previous_copy_if_store_identity_changes(self) -> None:
        self.write()
        backup = self.store.backup()["path"]
        foreign_root = self.root.parent / "foreign"
        foreign_root.mkdir()
        git(foreign_root, "init", "-q")
        foreign_store = MEMORY.Store.init(foreign_root)
        self.store.path.rename(self.root.parent / "original.sqlite3")
        foreign_store.path.rename(self.store.path)
        with self.assertRaisesRegex(MEMORY.MemoryError_, "MEMORY_BACKUP_FAILED"):
            self.store.backup()
        with sqlite3.connect(backup) as copy:
            self.assertEqual(
                copy.execute(
                    "select value from meta where key='workspace_id'"
                ).fetchone()[0],
                self.store.workspace_id,
            )

    def test_backup_uses_a_new_temporary_file_and_preserves_conflicts(self) -> None:
        external = self.root.parent / "external-temp"
        external.write_text("untouched", encoding="utf-8")
        (self.store.path.parent / (MEMORY.BACKUP_NAME + ".tmp")).symlink_to(external)
        first = self.write()
        self.write(memory_id=first["memory_id"], expected_revision=0)
        result = self.store.backup()
        with sqlite3.connect(result["path"]) as copy:
            self.assertEqual(
                copy.execute("select count(*) from conflict").fetchone()[0], 1
            )
            self.assertEqual(
                copy.execute(
                    "select value from meta where key='workspace_id'"
                ).fetchone()[0],
                self.store.workspace_id,
            )
        self.assertEqual(external.read_text(encoding="utf-8"), "untouched")

    def test_parallel_backups_produce_a_valid_container(self) -> None:
        self.write()
        script = ROOT / "scripts/workspace_memory.py"
        command = [sys.executable, str(script), "--root", str(self.root), "backup"]
        racers = [
            subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            for _ in range(4)
        ]
        results = [racer.communicate() for racer in racers]
        self.assertEqual([racer.returncode for racer in racers], [0] * 4, results)
        with sqlite3.connect(self.store.path.parent / MEMORY.BACKUP_NAME) as copy:
            self.assertEqual(copy.execute("pragma integrity_check").fetchone()[0], "ok")
            self.assertEqual(
                copy.execute("select count(*) from revision").fetchone()[0], 1
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
