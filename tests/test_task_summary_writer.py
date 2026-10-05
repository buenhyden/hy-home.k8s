"""Opt-in Task summary authoring preserves bytes and fails closed."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
import document_contracts as contracts  # noqa: E402

TASK = "docs/03.specs/0106-stage99-lifecycle-normalization/tasks/tsk-0001-example.md"
CRITERION = "[VAL-P02-002](../spec.md#success-criteria--verification-plan)"


def load_writer():
    spec = importlib.util.spec_from_file_location(
        "task_summary_writer", SCRIPTS / "sync-task-status.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def row(
    identifier="WORK-001",
    status="ready",
    result="NOT_RUN",
    acceptance="pending",
    evidence="Focused execution pending",
):
    return f"| {identifier} | {CRITERION} | Check summary | platform | {status} | {result} | {acceptance} | {evidence} |"


def task_text(status="ready", rows=None):
    items = rows if rows is not None else [row(), row("WORK-002", "in-progress")]
    return "\n".join(
        [
            "---",
            'title: "Task summary example"',
            'version: "0.1.0"',
            'type: "sdlc/task"',
            f'status: "{status}"',
            'owner: "platform"',
            'updated: "2026-10-05"',
            'layer: "specs"',
            'artifact_id: "SPEC-0106-TSK-0001"',
            'parent_ids: ["SPEC-0106-PLAN-0001"]',
            "---",
            "",
            "# Task: Task summary example",
            "",
            "## Overview",
            "",
            "Bounded synthetic authoring check.",
            "",
            "## Inputs",
            "",
            "[Spec](../spec.md) and [Plan](../plan.md).",
            "",
            "## Task Table",
            "",
            "### Lifecycle Traceability",
            "",
            "| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
            *items,
            "",
            "## Task Evidence",
            "",
            "| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
            f"| EVD-001 | {CRITERION} | WORK-001 | Focused fixture | Synthetic task | NOT_RUN | Pending | pending |",
            "",
            "## Approval and Safety Boundaries",
            "",
            "Local synthetic fixture only.",
            "",
            "## Verification Summary",
            "",
            "Observed execution remains pending.",
            "",
        ]
    )


class TaskSummaryDerivationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registry = contracts.load_registry(ROOT)
        cls.binding = next(
            p for p in registry.profiles if p.profile_id == "sdlc/task"
        ).body_contract.task_execution

    def derive(self, states, binding=None):
        helper = getattr(contracts, "derive_task_summary", None)
        self.assertTrue(
            callable(helper), "shared derive_task_summary helper is required"
        )
        return helper(states, binding or self.binding)

    def test_current_aggregation_priority_and_terminal_mixtures(self):
        cases = [
            (["draft"], "draft"),
            (["ready"], "ready"),
            (["ready", "draft"], "ready"),
            (["completed", "draft"], "in-progress"),
            (["completed", "ready"], "in-progress"),
            (["in-progress", "cancelled"], "in-progress"),
            (["blocked", "completed"], "blocked"),
            (["completed", "completed"], "completed"),
            (["completed", "cancelled"], "cancelled"),
            (["cancelled", "draft"], "draft"),
        ]
        for states, expected in cases:
            with self.subTest(states=states):
                original = tuple(states)
                self.assertEqual(self.derive(states), expected)
                self.assertEqual(tuple(states), original)

    def test_historical_queued_summary_is_preserved(self):
        binding = replace(
            self.binding,
            summary_rule="task-items-v1",
            result_states={
                "draft": ("NOT_RUN",),
                "queued": ("NOT_RUN",),
                "in-progress": ("PASS",),
                "blocked": ("DEFER",),
                "completed": ("PASS",),
                "cancelled": ("NOT_RUN",),
            },
        )
        for states, expected in [
            (["queued", "draft"], "queued"),
            (["completed", "queued"], "in-progress"),
            (["blocked", "queued"], "blocked"),
            (["cancelled", "completed"], "cancelled"),
        ]:
            with self.subTest(states=states):
                self.assertEqual(self.derive(states, binding), expected)

    def test_empty_and_unknown_states_fail(self):
        for states in ([], ["invented"], ["frontmatter"]):
            with self.subTest(states=states):
                with self.assertRaises(ValueError):
                    self.derive(states)


class TaskSummaryWriterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.writer = load_writer()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="task-summary-writer-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repo"
        shutil.copytree(ROOT / "docs/99.templates", self.root / "docs/99.templates")
        self.target = self.root / TASK
        self.target.parent.mkdir(parents=True)
        self.original = task_text().encode()
        self.target.write_bytes(self.original)

    def invoke(self, write=False, path=TASK, root=None):
        args = ["--root", str(root or self.root), "--path", path]
        if write:
            args.append("--write")
        output, errors = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            result = self.writer.main(args)
        return result, output.getvalue(), errors.getvalue()

    def assert_refused(self, expected="SYNC-TASK-INVALID", path=TASK):
        before = self.target.read_bytes()
        result, output, errors = self.invoke(write=True, path=path)
        self.assertEqual(result, 2, (output, errors))
        self.assertIn(expected, errors)
        self.assertIn(path, errors)
        self.assertNotIn("Traceback", errors)
        self.assertEqual(self.target.read_bytes(), before)

    def test_preview_reports_current_expected_without_writing(self):
        before = self.target.stat()
        result, output, errors = self.invoke()
        self.assertEqual((result, errors), (0, ""))
        self.assertIn("current=ready", output)
        self.assertIn("expected=in-progress", output)
        self.assertEqual(self.target.read_bytes(), self.original)
        self.assertEqual(self.target.stat().st_mtime_ns, before.st_mtime_ns)

    def test_explicit_write_preserves_all_other_bytes_and_file_mode(self):
        self.target.chmod(0o640)
        result, output, errors = self.invoke(write=True)
        self.assertEqual((result, errors), (0, ""))
        self.assertIn("changed", output)
        self.assertEqual(
            self.target.read_bytes(),
            self.original.replace(b'status: "ready"', b'status: "in-progress"', 1),
        )
        self.assertEqual(stat.S_IMODE(self.target.stat().st_mode), 0o640)
        self.assertEqual(list(self.target.parent.glob(".task-status-*")), [])

    def test_crlf_comments_whitespace_and_body_status_are_preserved(self):
        original = task_text().replace('status: "ready"', 'status:  "ready"   ', 1)
        original = original.replace(
            'owner: "platform"', '# Keep metadata comment\nowner: "platform"', 1
        )
        original += '\nBody literal status: "ready" stays unchanged.\n'
        raw = original.replace("\n", "\r\n").encode()
        self.target.write_bytes(raw)
        result, _, errors = self.invoke(write=True)
        self.assertEqual((result, errors), (0, ""))
        self.assertEqual(
            self.target.read_bytes(),
            raw.replace(b'status:  "ready"', b'status:  "in-progress"', 1),
        )

    def test_one_row_frontmatter_marker_and_matching_multirow_are_noops(self):
        for text in [
            task_text(rows=[row(status="frontmatter")]),
            task_text("in-progress"),
        ]:
            with self.subTest(text=text):
                self.target.write_text(text)
                before = self.target.stat()
                with mock.patch.object(
                    self.writer.os,
                    "replace",
                    side_effect=AssertionError("no-op must not replace"),
                ):
                    result, output, errors = self.invoke(write=True)
                self.assertEqual((result, errors), (0, ""))
                self.assertIn("unchanged", output)
                self.assertEqual(self.target.read_text(), text)
                self.assertEqual(self.target.stat().st_ino, before.st_ino)
                self.assertEqual(self.target.stat().st_mtime_ns, before.st_mtime_ns)

    def test_comment_and_fence_decoys_do_not_change_parser_selection(self):
        decoy = (
            "## Task Table\n### Lifecycle Traceability\n| Invalid |\n| --- |\n| row |\n"
        )
        text = task_text().replace(
            "## Task Table",
            f"<!--\n{decoy}-->\n\n```markdown\n{decoy}```\n\n## Task Table",
            1,
        )
        self.target.write_text(text)
        result, _, errors = self.invoke(write=True)
        self.assertEqual((result, errors), (0, ""))
        self.assertEqual(
            self.target.read_text(),
            text.replace('status: "ready"', 'status: "in-progress"', 1),
        )

    def test_valid_completed_and_blocked_candidates_follow_legal_edges(self):
        rows = [
            row(
                status="completed",
                result="PASS",
                acceptance="accepted",
                evidence="Focused fixture PASS",
            ),
            row("WORK-002", "completed", "PASS", "accepted", "Second fixture PASS"),
        ]
        for target, items in [
            ("completed", rows),
            (
                "blocked",
                [
                    row(
                        status="blocked",
                        result="DEFER",
                        evidence="Reason: missing runner; Next owner: operator",
                    ),
                    row("WORK-002", "ready"),
                ],
            ),
        ]:
            with self.subTest(target=target):
                self.target.write_text(task_text("in-progress", items))
                result, output, errors = self.invoke(write=True)
                self.assertEqual((result, errors), (0, ""))
                self.assertIn(f"expected={target}", output)

    def test_invalid_source_rows_and_attachment_are_never_repaired(self):
        examples = [
            task_text(rows=[row(), row()]),
            task_text(rows=[row(status="invented"), row("WORK-002")]),
            task_text(rows=[row(result="INVENTED"), row("WORK-002")]),
            task_text(rows=[row(acceptance="invented"), row("WORK-002")]),
            task_text(
                rows=[
                    row(
                        status="completed",
                        result="PASS",
                        acceptance="accepted",
                        evidence="Pending",
                    ),
                    row("WORK-002"),
                ]
            ),
            task_text(
                rows=[row(status="blocked", evidence="Waiting"), row("WORK-002")]
            ),
            task_text().replace("| EVD-001 |", "| BAD |"),
            task_text().replace(
                "| NOT_RUN | Pending | pending |", "| NOT_RUN | Pending | accepted |"
            ),
            task_text().replace("## Task Table", "## Missing Table"),
            task_text().replace(
                "### Lifecycle Traceability",
                "### Lifecycle Traceability\n\n### Lifecycle Traceability",
            ),
            task_text().replace(
                'status: "ready"', 'status: "ready"\nstatus: "ready"', 1
            ),
            task_text().replace('status: "ready"', "status: 'ready'", 1),
            task_text().replace("| Check summary |", "| Check summary | extra |", 1),
        ]
        for text in examples:
            with self.subTest(text=text):
                self.target.write_text(text)
                self.assert_refused()

    def test_illegal_transition_and_invalid_candidate_are_refused_in_preview(self):
        for text, identifier in [
            (task_text("draft"), "SYNC-TASK-TRANSITION"),
            (task_text("completed", [row(), row("WORK-002")]), "SYNC-TASK-TRANSITION"),
            (
                task_text(
                    "in-progress",
                    [
                        row(status="cancelled", evidence="Reason: scope ended"),
                        row("WORK-002", "cancelled", evidence="Reason: scope ended"),
                    ],
                ),
                "SYNC-TASK-CANDIDATE",
            ),
        ]:
            with self.subTest(identifier=identifier):
                self.target.write_text(text)
                result, _, errors = self.invoke()
                self.assertEqual(result, 2)
                self.assertIn(identifier, errors)
                self.assertEqual(self.target.read_text(), text)

    def test_malformed_yaml_mapping_key_has_stable_error_and_no_write(self):
        malformed = task_text().replace(
            'title: "Task summary example"',
            'title: "Task summary example"\n? [a, b]\n: "value"',
            1,
        )
        self.target.write_text(malformed)
        for write in (False, True):
            with self.subTest(write=write):
                result, _, errors = self.invoke(write=write)
                self.assertEqual(result, 2)
                self.assertIn("SYNC-TASK-INVALID", errors)
                self.assertIn(TASK, errors)
                self.assertNotIn("Traceback", errors)
                self.assertEqual(self.target.read_text(), malformed)
        command = [
            sys.executable,
            str(SCRIPTS / "sync-task-status.py"),
            "--root",
            str(self.root),
            "--path",
            TASK,
        ]
        for extra in ([], ["--write"]):
            with self.subTest(extra=extra):
                result = subprocess.run(
                    command + extra, capture_output=True, text=True, timeout=15
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("SYNC-TASK-INVALID", result.stderr)
                self.assertIn(TASK, result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(self.target.read_text(), malformed)

    def test_deep_yaml_nesting_has_stable_error_and_no_write(self):
        nested = "[" * 1000 + "value" + "]" * 1000
        malformed = task_text().replace(
            'title: "Task summary example"', "title: " + nested, 1
        )
        self.target.write_text(malformed)
        for write in (False, True):
            with self.subTest(write=write):
                result, _, errors = self.invoke(write=write)
                self.assertEqual(result, 2)
                self.assertIn("SYNC-TASK-INVALID", errors)
                self.assertIn(TASK, errors)
                self.assertNotIn("Traceback", errors)
                self.assertEqual(self.target.read_text(), malformed)

    def test_frontmatter_schema_must_be_an_object(self):
        for contents in ("null", "[]"):
            with self.subTest(contents=contents):
                schema = (
                    self.root / "docs/99.templates/contracts/frontmatter.schema.json"
                )
                schema.write_text(contents)
                self.assert_refused()

    def test_outside_archive_template_and_native_paths_are_refused(self):
        for path in [
            "../outside.md",
            str(self.root.parent / "outside.md"),
            "docs/98.archive/completed/example.md",
            "docs/99.templates/templates/specs/task.template.md",
            ".codex/agents/worker.toml",
        ]:
            with self.subTest(path=path):
                self.assert_refused("SYNC-TASK-PATH", path)

    def test_symlink_file_parent_and_root_are_refused(self):
        outside = self.root.parent / "outside.md"
        outside.write_bytes(self.original)
        self.target.unlink()
        self.target.symlink_to(outside)
        result, _, errors = self.invoke(write=True)
        self.assertEqual(result, 2)
        self.assertIn("SYNC-TASK-PATH", errors)
        self.assertEqual(outside.read_bytes(), self.original)
        self.target.unlink()
        parent = self.target.parent
        relocated = parent.with_name("relocated")
        parent.rename(relocated)
        (relocated / self.target.name).write_bytes(self.original)
        parent.symlink_to(relocated, target_is_directory=True)
        result, _, errors = self.invoke(write=True)
        self.assertEqual(result, 2)
        self.assertIn("SYNC-TASK-PATH", errors)
        alias = self.root.parent / "alias"
        alias.symlink_to(self.root, target_is_directory=True)
        result, _, errors = self.invoke(write=True, root=alias)
        self.assertEqual(result, 2)
        self.assertIn("SYNC-TASK-PATH", errors)

    def test_missing_nonregular_and_invalid_utf8_are_refused(self):
        self.target.write_bytes(b"\xff")
        self.assert_refused()
        self.target.unlink()
        for create in [
            lambda: None,
            lambda: self.target.mkdir(),
            lambda: os.mkfifo(self.target),
        ]:
            create()
            result, _, errors = self.invoke(write=True)
            self.assertEqual(result, 2)
            self.assertIn("SYNC-TASK-PATH", errors)
            if self.target.is_dir():
                self.target.rmdir()
            elif self.target.exists():
                self.target.unlink()

    def test_source_changed_after_read_preserves_new_source(self):
        changed = self.original + b"\nConcurrent author edit.\n"
        real_fsync = self.writer.os.fsync

        def change_source(fd):
            self.target.write_bytes(changed)
            real_fsync(fd)

        with mock.patch.object(self.writer.os, "fsync", side_effect=change_source):
            result, _, errors = self.invoke(write=True)
        self.assertEqual(result, 2)
        self.assertIn("SYNC-TASK-SOURCE-CHANGED", errors)
        self.assertEqual(self.target.read_bytes(), changed)
        self.assertEqual(list(self.target.parent.glob(".task-status-*")), [])

    def test_same_bytes_replaced_inode_and_changed_parent_are_refused(self):
        real_fsync = self.writer.os.fsync

        def replace_source(fd):
            replacement = self.target.with_name("other-source")
            replacement.write_bytes(self.original)
            replacement.replace(self.target)
            real_fsync(fd)

        with mock.patch.object(self.writer.os, "fsync", side_effect=replace_source):
            result, _, errors = self.invoke(write=True)
        self.assertEqual(result, 2)
        self.assertIn("SYNC-TASK-SOURCE-CHANGED", errors)
        self.assertEqual(self.target.read_bytes(), self.original)
        relocated = self.target.parent.with_name("concurrently-moved")

        def move_parent(fd):
            self.target.parent.rename(relocated)
            self.target.parent.symlink_to(relocated, target_is_directory=True)
            real_fsync(fd)

        with mock.patch.object(self.writer.os, "fsync", side_effect=move_parent):
            result, _, errors = self.invoke(write=True)
        self.assertEqual(result, 2)
        self.assertIn("SYNC-TASK-SOURCE-CHANGED", errors)
        self.assertEqual(self.target.read_bytes(), self.original)
        self.assertEqual(list(relocated.glob(".task-status-*")), [])

    def test_short_writes_are_finished_before_replacement(self):
        original_write = self.writer.os.write
        with mock.patch.object(
            self.writer.os,
            "write",
            side_effect=lambda fd, data: original_write(fd, data[:19]),
        ):
            result, _, errors = self.invoke(write=True)
        self.assertEqual((result, errors), (0, ""))
        self.assertEqual(
            self.target.read_bytes(),
            self.original.replace(b'status: "ready"', b'status: "in-progress"', 1),
        )

    def test_failed_replace_and_temp_write_preserve_original(self):
        for operation in ("replace", "write", "fsync"):
            with self.subTest(operation=operation):
                with mock.patch.object(
                    self.writer.os, operation, side_effect=OSError("synthetic failure")
                ):
                    result, _, errors = self.invoke(write=True)
                self.assertEqual(result, 2)
                self.assertIn("SYNC-TASK-WRITE", errors)
                self.assertEqual(self.target.read_bytes(), self.original)
                self.assertEqual(list(self.target.parent.glob(".task-status-*")), [])

    def test_code_is_loaded_from_trusted_sibling_not_target_root(self):
        evil = self.root / "scripts"
        evil.mkdir()
        (evil / "validate-markdown-profiles.py").write_text(
            "raise RuntimeError('untrusted code executed')\n"
        )
        result, output, errors = self.invoke()
        self.assertEqual((result, errors), (0, ""))
        self.assertIn("expected=in-progress", output)

    def test_real_cli_exit_codes_and_no_traceback(self):
        command = [
            sys.executable,
            str(SCRIPTS / "sync-task-status.py"),
            "--root",
            str(self.root),
            "--path",
            TASK,
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("current=ready expected=in-progress", result.stdout)
        self.target.write_text(
            task_text(rows=[row(result="INVENTED"), row("WORK-002")])
        )
        result = subprocess.run(command, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 2)
        self.assertIn("SYNC-TASK-INVALID", result.stderr)
        self.assertIn(TASK, result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
