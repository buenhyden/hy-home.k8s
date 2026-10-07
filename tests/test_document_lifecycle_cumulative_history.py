"""Bounded first-parent admission for committed intermediate lifecycle states."""

from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path, PurePosixPath
from unittest import mock

from tests.git_fixture import GitFixture


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location(
    "validate_document_lifecycle_cumulative_history_tested",
    SCRIPTS / "validate-document-lifecycle.py",
)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import boundary
    raise RuntimeError("cannot load document lifecycle validator")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)

from document_contracts import load_registry  # noqa: E402
from document_lifecycle import LifecycleDiagnostic  # noqa: E402


class CumulativeLifecycleHistoryTest(unittest.TestCase):
    path = ".agents/governance/cumulative-history.md"

    @classmethod
    def setUpClass(cls) -> None:
        cls.seed_temporary = tempfile.TemporaryDirectory(
            prefix="lifecycle-history-seed-"
        )
        cls.addClassCleanup(cls.seed_temporary.cleanup)
        cls.seed_root = Path(cls.seed_temporary.name) / "repository"
        cls.seed_root.mkdir()
        registry_path = Path("docs/99.templates/registry.json")
        raw_registry = json.loads((ROOT / registry_path).read_text())
        selected = {
            "governance/contract",
            "sdlc/architecture-description",
            "sdlc/spec",
            "sdlc/plan",
            "archive/tombstone",
        }
        for domain in raw_registry["lifecycle_domains"]:
            selected.add(
                "archive/migration"
                if "archive/migration" in domain["profile_ids"]
                else domain["profile_ids"][0]
            )
            domain["profile_ids"] = [
                profile_id
                for profile_id in domain["profile_ids"]
                if profile_id in selected
            ]
        # README navigation names profiles this selection drops.
        raw_registry.pop("readme_navigation", None)
        # The language contract names profiles this selection drops.
        raw_registry.pop("document_language", None)
        raw_registry["profiles"] = [
            profile for profile in raw_registry["profiles"] if profile["id"] in selected
        ]
        # These synthetic lifecycle documents exercise transitions, not the
        # production contract owner's closed path inventory.
        for profile in raw_registry["profiles"]:
            if profile["id"] == "governance/contract":
                profile["path_pattern"] = (
                    r"^\.agents/governance/(?:cumulative-history|"
                    r"cumulative-history-second|source|other|repeated)\.md$"
                )
        target_registry = cls.seed_root / registry_path
        target_registry.parent.mkdir(parents=True)
        target_registry.write_text(json.dumps(raw_registry))
        templates = {
            profile["template_source"]
            for profile in raw_registry["profiles"]
            if profile["template_source"] is not None
        }
        for relative in {
            "docs/99.templates/contracts/document-profile.schema.json",
            *templates,
        }:
            target = cls.seed_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / relative).read_bytes())
        seed_git = GitFixture(cls.seed_root)
        seed_git.run("add", "--", "docs/99.templates")
        seed_git.run("commit", "--quiet", "-m", "registry")

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="lifecycle-history-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repository"
        subprocess.run(
            ["git", "clone", "--quiet", str(self.seed_root), str(self.root)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.git = GitFixture(self.root)
        self.base = self.oid("HEAD")
        self.primary_branch = (
            self.git.run("symbolic-ref", "--short", "HEAD").decode("ascii").strip()
        )
        self._registry = None

    @property
    def registry(self):
        if self._registry is None:
            self._registry = load_registry(self.root)
        return self._registry

    def oid(self, ref: str) -> str:
        return self.git.run("rev-parse", ref).decode("ascii").strip()

    def document(self, status: str, body: str | None = None) -> bytes:
        if body is None:
            body = "unique cumulative history content " + "z" * 4_096
        sections = "".join(
            f"## {heading}\n\n{body}\n\n"
            for heading in (
                "Overview",
                "Authority Boundary",
                "Governance Context",
                "Current Contract",
                "Validation and Refresh",
                "Related Documents",
            )
        )
        return (
            "---\n"
            'title: "Cumulative history"\n'
            'version: "0.1.0"\n'
            'type: "governance/contract"\n'
            f'status: "{status}"\n'
            'owner: "platform"\n'
            'updated: "2026-08-31"\n'
            "---\n\n# Cumulative history\n\n"
            f"{sections}"
        ).encode()

    def commit(self, status: str, body: str | None = None) -> str:
        self.git.commit(self.path, self.document(status, body))
        return self.oid("HEAD")

    def commit_path(
        self,
        path: str,
        status: str,
        body: str | None = None,
    ) -> str:
        self.git.commit(path, self.document(status, body))
        return self.oid("HEAD")

    def invoke(self, mode: str, **refs: str) -> tuple[int, str]:
        arguments = ["--root", str(self.root), "--mode", mode]
        for name, value in refs.items():
            arguments.extend(["--" + name.replace("_", "-"), value])
        output = io.StringIO()
        with redirect_stdout(output), redirect_stderr(output):
            result = VALIDATOR.main(arguments)
        return result, output.getvalue()

    def commit_reviewed_activation(self, path: str | None = None) -> str:
        """Record the real current review edge for an intended legal activation."""
        target = self.path if path is None else path
        self.commit_path(target, "in-review")
        return self.commit_path(target, "active")

    def explicit(self, start: str, end: str) -> tuple[int, str]:
        return self.invoke("explicit-ref", from_ref=start, to_ref=end)

    def proved(self, start: str, end: str) -> bool:
        return VALIDATOR._history_proves_cumulative_create(
            self.root,
            self.registry,
            PurePosixPath(self.path),
            start,
            end,
        )

    def registered_task_document(self, status: str = "draft") -> bytes:
        """Render the actual registered form, retaining its real Git provenance."""
        template = next(
            profile.template
            for profile in self.registry.profiles
            if profile.profile_id == "sdlc/task"
        )
        text = (self.root / template).read_text()
        substitutions = {
            "{{TITLE}}": "Registered template history",
            "{{OWNER}}": "platform",
            "{{UPDATED}}": "2026-10-05",
            "{{ARTIFACT_ID}}": "SPEC-9999-TSK-0001",
            "{{PARENT_ID}}": "SPEC-9999-PLAN-0001",
            "{{SPEC_RELATIVE_PATH}}": "../spec.md",
        }
        for placeholder, value in substitutions.items():
            text = text.replace(placeholder, value)
        self.assertNotIn("{{", text)
        text = text.replace("VAL-FEATURE-001", "VAL-P02-004")
        text = text.replace("WORK-001", "WORK-004")
        if status == "completed":
            text = text.replace(
                "| NOT_RUN | pending | Pending named repository evidence |",
                "| PASS | accepted | [Synthetic fixture result](#verification-summary) |",
            ).replace(
                "| NOT_RUN | Pending | pending |",
                "| PASS | [Synthetic fixture result](#verification-summary) | accepted |",
            )
        return text.replace('status: "draft"', f'status: "{status}"', 1).encode()

    def registered_task_history(self) -> tuple[PurePosixPath, str]:
        """Create template-derived owner documents and every legal Task transition."""
        package = "docs/03.specs/9999-template-history"
        for name, profile_id, artifact_id in (
            ("spec.md", "sdlc/spec", "SPEC-9999"),
            ("plan.md", "sdlc/plan", "SPEC-9999-PLAN-0001"),
        ):
            template = next(
                profile.template
                for profile in self.registry.profiles
                if profile.profile_id == profile_id
            )
            text = (self.root / template).read_text()
            for placeholder, value in {
                "{{TITLE}}": "Registered template history",
                "{{OWNER}}": "platform",
                "{{UPDATED}}": "2026-10-05",
                "{{ARTIFACT_ID}}": artifact_id,
                "{{PARENT_ID}}": "SPEC-9999",
                "{{SPEC_RELATIVE_PATH}}": "spec.md",
                "{{TASK_RELATIVE_PATH}}": "tasks/tsk-0001-copy.md",
            }.items():
                text = text.replace(placeholder, value)
            self.assertNotIn("{{", text)
            self.git.commit(
                f"{package}/{name}",
                text.encode(),
            )
        self.base = self.oid("HEAD")
        target = PurePosixPath(f"{package}/tasks/tsk-0001-copy.md")
        for status in ("draft", "ready", "in-progress", "completed"):
            self.git.commit(target.as_posix(), self.registered_task_document(status))
        return target, self.oid("HEAD")

    def test_real_registered_task_template_first_draft_copy_is_admitted(self) -> None:
        target = PurePosixPath(
            "docs/03.specs/9999-template-history/tasks/tsk-0001-copy.md"
        )
        self.git.commit(target.as_posix(), self.registered_task_document())
        created = self.oid("HEAD")
        records = self.git.run(
            "diff",
            "--name-status",
            "-z",
            "--find-copies=1%",
            "--find-copies-harder",
            "-l0",
            self.base,
            created,
            "--",
        ).split(b"\0")
        destination = records.index(target.as_posix().encode())
        self.assertTrue(records[destination - 2].startswith(b"C"))
        self.assertEqual(
            records[destination - 1],
            b"docs/99.templates/templates/specs/task.template.md",
        )
        cache = VALIDATOR._CumulativeHistoryCache(self.root, self.registry)
        document = cache._snapshot(created)[0][target]
        self.assertIsNone(document.state_issue)
        self.assertFalse(
            VALIDATOR._history_rename_or_copy_into_path(
                self.root,
                self.base,
                created,
                target,
                target_document=document,
                cache=cache,
            )
        )

    def test_registered_task_history_is_admitted_by_ci_and_explicit_ref(self) -> None:
        target, completed = self.registered_task_history()
        for mode in ("ci", "explicit-ref"):
            with self.subTest(mode=mode):
                result, output = (
                    self.invoke(mode, base_ref=self.base, to_ref=completed)
                    if mode == "ci"
                    else self.explicit(self.base, completed)
                )
                self.assertEqual(result, 0, output)
        self.assertTrue(
            VALIDATOR._history_proves_cumulative_create(
                self.root,
                self.registry,
                target,
                self.base,
                completed,
            )
        )

    def test_registered_task_history_is_admitted_by_real_staged_merge(self) -> None:
        self.git.run("checkout", "--quiet", "-b", "side", self.base)
        _, completed = self.registered_task_history()
        common = self.base
        self.git.run("checkout", "--quiet", self.primary_branch)
        self.git.run("merge", "--quiet", "--ff-only", common)
        self.git.commit(".agents/governance/other.md", self.document("draft"))
        self.git.run("merge", "--no-commit", "--no-ff", completed)
        result, output = self.invoke("staged")
        self.assertEqual(result, 0, output)

    def registered_task_boundary_parent(self, mutation, target, source, data):
        if mutation == "state":
            return self.registered_task_document("ready")
        if mutation == "identity":
            return data.replace(b"SPEC-9999-TSK-0001", b"SPEC-9999-TSK-0002")
        if mutation == "reused":
            self.git.commit(
                "docs/03.specs/9999-template-history/tasks/tsk-0002-other.md",
                data,
            )
        elif mutation == "existing-target":
            self.git.commit(target.as_posix(), data)
            return data + b"\nA later body maintenance event.\n"
        elif mutation == "missing-source":
            self.git.run("rm", "--", source.as_posix())
            self.git.run("commit", "--quiet", "-m", "missing template")
        elif mutation == "nonregular-source":
            (self.root / source).unlink()
            (self.root / source).symlink_to("plan.template.md")
            self.git.run("add", "--", source.as_posix())
            self.git.run("commit", "--quiet", "-m", "nonregular template")
        return data

    def registered_task_boundary_event(self, mutation, source, original, data):
        if mutation == "changed-source":
            (self.root / source).write_bytes(original + b"\nChanged form.\n")
            self.git.run("add", "--", source.as_posix())
        elif mutation == "binding":
            path = self.root / "docs/99.templates/registry.json"
            raw = json.loads(path.read_text())
            next(p for p in raw["profiles"] if p["id"] == "sdlc/task")[
                "template_source"
            ] = "docs/99.templates/templates/specs/plan.template.md"
            path.write_text(json.dumps(raw))
            self.git.run("add", "--", "docs/99.templates/registry.json")
        elif mutation == "proposed-duplicate":
            relative = "docs/03.specs/9999-template-history/tasks/tsk-0002-other.md"
            (self.root / relative).parent.mkdir(parents=True, exist_ok=True)
            (self.root / relative).write_bytes(data)
            self.git.run("add", "--", relative)

    def test_registered_task_template_boundary_rejects_invalid_inputs(self) -> None:
        target = PurePosixPath(
            "docs/03.specs/9999-template-history/tasks/tsk-0001-copy.md"
        )
        source = PurePosixPath("docs/99.templates/templates/specs/task.template.md")
        for mutation in (
            "state",
            "identity",
            "reused",
            "changed-source",
            "other-form",
            "binding",
            "missing-source",
            "nonregular-source",
            "existing-target",
            "proposed-duplicate",
        ):
            with self.subTest(mutation=mutation):
                self.setUp()
                registry = self.registry
                data = self.registered_task_document()
                original = (self.root / source).read_bytes()
                data = self.registered_task_boundary_parent(
                    mutation, target, source, data
                )
                self.base = self.oid("HEAD")
                self.registered_task_boundary_event(mutation, source, original, data)
                self.git.commit(target.as_posix(), data)
                created = self.oid("HEAD")
                cache = VALIDATOR._CumulativeHistoryCache(self.root, registry)
                before = cache._snapshot(self.base)[0]
                after = cache._snapshot(created)[0]
                candidate_source = (
                    PurePosixPath("docs/99.templates/templates/specs/plan.template.md")
                    if mutation == "other-form"
                    else source
                )
                arguments = (
                    self.root,
                    self.base,
                    created,
                    candidate_source,
                    target,
                    after[target],
                    cache,
                    before,
                    after,
                )
                if mutation == "nonregular-source":
                    with self.assertRaises(VALIDATOR.InvocationError):
                        VALIDATOR._history_registered_task_template_copy(*arguments)
                else:
                    self.assertFalse(
                        VALIDATOR._history_registered_task_template_copy(*arguments)
                    )

    def test_ordinary_canonical_task_copy_remains_rejected_by_ci(self) -> None:
        source = PurePosixPath("docs/03.specs/9998-source/tasks/tsk-0001-source.md")
        target = PurePosixPath(
            "docs/03.specs/9999-template-history/tasks/tsk-0001-copy.md"
        )
        data = self.registered_task_document()
        self.git.commit(source.as_posix(), data.replace(b"SPEC-9999", b"SPEC-9998"))
        self.base = self.oid("HEAD")
        self.git.commit(target.as_posix(), data)
        created = self.oid("HEAD")
        records = self.git.run(
            "diff",
            "--name-status",
            "-z",
            "--find-copies=1%",
            "--find-copies-harder",
            "-l0",
            self.base,
            created,
            "--",
        ).split(b"\0")
        destination = records.index(target.as_posix().encode())
        self.assertTrue(records[destination - 2].startswith(b"C"))
        self.assertEqual(records[destination - 1], source.as_posix().encode())
        self.git.commit(target.as_posix(), self.registered_task_document("ready"))
        ready = self.oid("HEAD")
        self.assertFalse(
            VALIDATOR._history_proves_cumulative_create(
                self.root,
                self.registry,
                target,
                self.base,
                ready,
            )
        )
        result, output = self.invoke("ci", base_ref=self.base, to_ref=ready)
        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

    def assert_registered_task_later_refusal(self, target, invalid_tip, invalid):
        if invalid == "edge":
            self.assertFalse(
                VALIDATOR._history_proves_cumulative_create(
                    self.root,
                    self.registry,
                    target,
                    self.base,
                    invalid_tip,
                )
            )
        else:
            result, output = self.invoke("ci", base_ref=self.base, to_ref=invalid_tip)
            self.assertNotEqual(result, 0, output)
            self.assertIn("TASK-TERMINAL-EVIDENCE", output)
            self.assertNotIn("LIFECYCLE-CREATE", output)

    def test_registered_template_admission_preserves_later_task_checks(self) -> None:
        for invalid in ("edge", "result"):
            with self.subTest(invalid=invalid):
                self.setUp()
                target, valid_tip = self.registered_task_history()
                valid_result, valid_output = self.invoke(
                    "ci",
                    base_ref=self.base,
                    to_ref=valid_tip,
                )
                self.assertEqual(valid_result, 0, valid_output)
                self.git.run("checkout", "--quiet", "-b", "illegal", self.base)
                for status in ("draft", "ready"):
                    self.git.commit(
                        target.as_posix(), self.registered_task_document(status)
                    )
                ready = self.oid("HEAD")
                self.assertTrue(
                    VALIDATOR._history_proves_cumulative_create(
                        self.root,
                        self.registry,
                        target,
                        self.base,
                        ready,
                    )
                )
                completed = self.registered_task_document("completed")
                if invalid == "result":
                    self.git.commit(
                        target.as_posix(),
                        self.registered_task_document("in-progress"),
                    )
                    invalid_result = completed.replace(
                        b"| PASS | accepted |", b"| NOT_RUN | pending |"
                    )
                    self.assertNotEqual(invalid_result, completed)
                    completed = invalid_result
                self.git.commit(target.as_posix(), completed)
                invalid_tip = self.oid("HEAD")
                self.assert_registered_task_later_refusal(target, invalid_tip, invalid)

    def test_explicit_ref_admits_absent_draft_active_chain(self) -> None:
        self.commit("draft")
        active = self.commit_reviewed_activation()

        result, output = self.explicit(self.base, active)

        self.assertEqual(result, 0, output)

    def test_ci_admits_same_chain_from_merge_base(self) -> None:
        self.commit("draft")
        active = self.commit_reviewed_activation()

        result, output = self.invoke("ci", base_ref=self.base, to_ref=active)

        self.assertEqual(result, 0, output)

    def test_same_status_body_change_is_a_valid_intermediate_event(self) -> None:
        self.commit("draft")
        self.commit("draft", "Reviewed policy with an intermediate revision.")
        active = self.commit_reviewed_activation()

        result, output = self.explicit(self.base, active)

        self.assertEqual(result, 0, output)

    def test_committed_ref_blobs_ignore_dirty_checkout_and_index(self) -> None:
        self.commit("draft")
        active = self.commit_reviewed_activation()
        target = self.root / self.path
        target.write_bytes(self.document("retired"))
        self.git.run("add", "--", self.path)

        result, output = self.explicit(self.base, active)

        self.assertEqual(result, 0, output)

    def test_only_create_diagnostic_is_removed_for_a_proved_path(self) -> None:
        self.commit("draft")
        active = self.commit_reviewed_activation()
        path = PurePosixPath(self.path)
        create = LifecycleDiagnostic(
            "FAIL",
            "LIFECYCLE-CREATE",
            path,
            "governance/contract",
            "draft",
            "active",
            "explicit-ref",
            "",
        )
        duplicate = LifecycleDiagnostic(
            "FAIL",
            "LIFECYCLE-CREATE",
            path,
            "governance/contract",
            "draft",
            "active",
            "explicit-ref",
            "duplicate",
        )
        other = LifecycleDiagnostic(
            "FAIL",
            "LIFECYCLE-EVIDENCE",
            path,
            "governance/contract",
            "evidence",
            "missing",
            "explicit-ref",
            "missing",
        )

        actual = VALIDATOR._admit_cumulative_create_diagnostics(
            (create, duplicate, other),
            root=self.root,
            registry=self.registry,
            mode="explicit-ref",
            base_commit=self.base,
            proposed_commit=active,
            base_blobs={},
            proposed_blobs={path: VALIDATOR._tree_blob_oid(self.root, active, path)},
        )

        self.assertEqual(actual, (duplicate, other))

    def test_direct_active_creation_remains_rejected(self) -> None:
        active = self.commit("active")

        result, output = self.explicit(self.base, active)

        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

    def test_invalid_intermediate_edges_are_not_admitted(self) -> None:
        draft = self.commit("draft")
        retired = self.commit("retired")
        self.assertFalse(self.proved(self.base, retired))
        result, output = self.explicit(self.base, retired)
        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

        self.git.run("reset", "--hard", draft)
        self.commit_reviewed_activation()
        draft_again = self.commit("draft")
        self.assertFalse(self.proved(self.base, draft_again))

    def test_draft_to_active_without_review_remains_rejected(self) -> None:
        self.commit("draft")
        active = self.commit("active")

        result, output = self.explicit(self.base, active)

        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

    def test_deletion_recreation_and_exact_rename_are_not_admitted(self) -> None:
        self.commit("draft")
        self.git.run("rm", "--quiet", "--", self.path)
        self.git.run("commit", "--quiet", "-m", "delete")
        recreated = self.commit("active")
        self.assertFalse(self.proved(self.base, recreated))
        result, output = self.explicit(self.base, recreated)
        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

        self.git.run("reset", "--hard", self.base)
        source = ".agents/governance/source.md"
        self.git.commit(source, self.document("draft"))
        self.git.run("mv", source, self.path)
        self.git.run("commit", "--quiet", "-m", "rename")
        renamed = self.commit("active")
        self.assertFalse(self.proved(self.base, renamed))
        result, output = self.explicit(self.base, renamed)
        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

    def test_side_branch_merge_and_non_ancestral_refs_are_not_admitted(self) -> None:
        self.git.run("checkout", "--quiet", "-b", "side", self.base)
        self.commit("draft")
        side = self.oid("HEAD")
        self.git.run("checkout", "--quiet", self.primary_branch)
        self.git.commit(".agents/governance/other.md", self.document("draft"))
        self.git.run("merge", "--no-ff", "--no-edit", "side")
        merged = self.commit("active")
        self.assertFalse(self.proved(self.base, merged))
        self.assertFalse(self.proved(side, self.base))
        result, output = self.explicit(self.base, merged)
        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

    def test_malformed_missing_and_bounded_history_evidence_fails_closed(self) -> None:
        self.commit("draft")
        active = self.commit_reviewed_activation()
        with mock.patch.object(
            VALIDATOR, "_first_parent_history", return_value=("bad",)
        ):
            self.assertFalse(self.proved(self.base, active))
        with mock.patch.object(VALIDATOR, "CUMULATIVE_HISTORY_MAX_COMMITS", 1):
            self.assertFalse(self.proved(self.base, active))

    def test_staged_direct_active_creation_remains_rejected(self) -> None:
        self.git.commit(self.path, self.document("active"))
        self.git.run("reset", "--soft", "HEAD~1")

        result, output = self.invoke("staged")

        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

    def test_staged_merge_admits_only_exact_legal_side_parent_create(self) -> None:
        self.git.run("checkout", "--quiet", "-b", "side", self.base)
        self.commit("draft")
        self.commit_reviewed_activation()
        self.git.run("checkout", "--quiet", self.primary_branch)
        self.git.commit(".agents/governance/other.md", self.document("draft"))
        self.git.run("merge", "--no-commit", "--no-ff", "side")

        result, output = self.invoke("staged")
        self.assertEqual(result, 0, output)

        (self.root / self.path).write_bytes(self.document("active", "tampered"))
        self.git.run("add", "--", self.path)
        result, output = self.invoke("staged")
        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

    def test_staged_merge_admits_one_committed_merge_boundary(self) -> None:
        self.git.run("checkout", "--quiet", "-b", "side", self.base)
        self.commit("draft")
        self.commit_reviewed_activation()
        self.git.run("checkout", "--quiet", self.primary_branch)
        self.git.commit("notes/main.txt", b"unrelated main history")
        self.git.run("merge", "--no-ff", "--no-edit", "side")
        self.git.run("checkout", "--quiet", "-b", "feature", self.base)
        self.git.commit("notes/feature.txt", b"unrelated feature history")
        self.git.run("merge", "--no-commit", "--no-ff", self.primary_branch)

        result, output = self.invoke("staged")

        self.assertEqual(result, 0, output)

    def test_staged_merge_rejects_copied_document_without_distinct_identity(
        self,
    ) -> None:
        source = ".agents/governance/source.md"
        self.git.commit(source, self.document("draft"))
        self.base = self.oid("HEAD")
        self.git.run("checkout", "--quiet", "-b", "side", self.base)
        self.commit("draft")
        self.commit_reviewed_activation()
        self.git.run("checkout", "--quiet", self.primary_branch)
        self.git.commit("notes/feature.txt", b"unrelated feature history")
        self.git.run("merge", "--no-commit", "--no-ff", "side")

        result, output = self.invoke("staged")

        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

    def test_staged_merge_rejects_missing_malformed_and_fake_parent(self) -> None:
        self.git.run("checkout", "--quiet", "-b", "fake", self.base)
        fake = self.commit("active")
        self.git.run("checkout", "--quiet", "-b", "side", self.base)
        self.commit("draft")
        self.commit_reviewed_activation()
        self.git.run("checkout", "--quiet", self.primary_branch)
        self.git.commit(".agents/governance/other.md", self.document("draft"))
        self.git.run("merge", "--no-commit", "--no-ff", "side")
        merge_path = Path(
            self.git.run(
                "rev-parse", "--path-format=absolute", "--git-path", "MERGE_HEAD"
            )
            .decode()
            .strip()
        )
        actual = merge_path.read_bytes()
        for payload in (b"bad\n", actual + actual, fake.encode() + b"\n"):
            with self.subTest(payload=payload):
                merge_path.write_bytes(payload)
                result, output = self.invoke("staged")
                self.assertNotEqual(result, 0, output)
                self.assertIn("LIFECYCLE-CREATE", output)
        merge_path.unlink()
        result, output = self.invoke("staged")
        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

    def test_staged_merge_rejects_illegal_or_unavailable_side_history(self) -> None:
        self.git.run("checkout", "--quiet", "-b", "side", self.base)
        self.commit("draft")
        self.commit("retired")
        self.git.run("checkout", "--quiet", self.primary_branch)
        self.git.commit(".agents/governance/other.md", self.document("draft"))
        self.git.run("merge", "--no-commit", "--no-ff", "side")

        result, output = self.invoke("staged")
        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)
        with mock.patch.object(
            VALIDATOR,
            "_first_parent_history",
            side_effect=VALIDATOR.InvocationError("no history"),
        ):
            result, output = self.invoke("staged")
        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

    def test_staged_copy_signal_requires_distinct_canonical_unique_identity(
        self,
    ) -> None:
        source = PurePosixPath("docs/03.specs/0095-closed-package-retention/plan.md")
        target = PurePosixPath(
            "docs/03.specs/0099-workspace-engineering-research-refresh/plan.md"
        )
        source_document = VALIDATOR.LifecycleDocument(
            source, "sdlc/plan", "draft", artifact_id="SPEC-0095-PLAN-0001"
        )
        target_document = VALIDATOR.LifecycleDocument(
            target, "sdlc/plan", "draft", artifact_id="SPEC-0099-PLAN-0001"
        )
        raw = (
            b"C007\0"
            + source.as_posix().encode()
            + b"\0"
            + target.as_posix().encode()
            + b"\0"
        )
        cache = mock.Mock()
        cache.registry = self.registry
        cache._snapshot.side_effect = [
            ({source: source_document}, {}),
            ({target: target_document}, {}),
        ]
        with (
            mock.patch.object(VALIDATOR, "_run_git", return_value=raw),
            mock.patch.object(VALIDATOR, "_tree_blob_oid", return_value="a" * 40),
        ):
            self.assertFalse(
                VALIDATOR._history_rename_or_copy_into_path(
                    self.root,
                    self.base,
                    self.base,
                    target,
                    target_document=target_document,
                    cache=cache,
                )
            )
            for source_id, proposed in (
                (None, {target: target_document}),
                (target_document.artifact_id, {target: target_document}),
                (
                    source_document.artifact_id,
                    {target: target_document, source: target_document},
                ),
            ):
                with self.subTest(source_id=source_id, proposed=len(proposed)):
                    candidate = VALIDATOR.LifecycleDocument(
                        source, "sdlc/plan", "draft", artifact_id=source_id
                    )
                    cache._snapshot.side_effect = [
                        ({source: candidate}, {}),
                        (proposed, {}),
                    ]
                    self.assertTrue(
                        VALIDATOR._history_rename_or_copy_into_path(
                            self.root,
                            self.base,
                            self.base,
                            target,
                            target_document=target_document,
                            cache=cache,
                        )
                    )
            duplicate_source = PurePosixPath(
                "docs/03.specs/0095-closed-package-retention/spec.md"
            )
            wrong_profile = VALIDATOR.LifecycleDocument(
                source, "sdlc/spec", "draft", artifact_id=source_document.artifact_id
            )
            for base_documents in (
                {source: source_document, duplicate_source: source_document},
                {source: wrong_profile},
            ):
                cache._snapshot.side_effect = [
                    (base_documents, {}),
                    ({target: target_document}, {}),
                ]
                self.assertTrue(
                    VALIDATOR._history_rename_or_copy_into_path(
                        self.root,
                        self.base,
                        self.base,
                        target,
                        target_document=target_document,
                        cache=cache,
                    )
                )
            cache._snapshot.side_effect = [
                ({source: source_document}, {}),
                ({target: target_document}, {}),
            ]
            with mock.patch.object(
                VALIDATOR, "_run_git", return_value=raw.replace(b"C007", b"R007")
            ):
                self.assertTrue(
                    VALIDATOR._history_rename_or_copy_into_path(
                        self.root,
                        self.base,
                        self.base,
                        target,
                        target_document=target_document,
                        cache=cache,
                    )
                )

    def test_staged_seed_reuses_exact_blob_and_reparses_changed_or_legacy_blobs(
        self,
    ) -> None:
        draft = self.commit("draft")
        blobs = VALIDATOR._tree_blob_map(self.root, draft)
        documents, texts = VALIDATOR._snapshot_projection(
            self.root,
            self.registry,
            blobs,
            historical=True,
            legacy_completion=VALIDATOR._legacy_completion_generation(self.root, draft),
        )
        seed = dict(
            seed_blobs=blobs,
            seed_documents=documents,
            seed_texts=texts,
            seed_legacy_completion=VALIDATOR._legacy_completion_generation(
                self.root, draft
            ),
        )
        cache = VALIDATOR._CumulativeHistoryCache(self.root, self.registry, **seed)
        with mock.patch.object(
            VALIDATOR, "_snapshot_projection", wraps=VALIDATOR._snapshot_projection
        ) as project:
            self.assertEqual(
                cache._snapshot(draft)[0][PurePosixPath(self.path)].status, "draft"
            )
            self.assertEqual(len(project.call_args.args[2]), 0)
            active = self.commit_reviewed_activation()
            self.assertEqual(
                cache._snapshot(active)[0][PurePosixPath(self.path)].status, "active"
            )
            self.assertEqual(len(project.call_args.args[2]), 1)
        wrong_legacy = VALIDATOR._CumulativeHistoryCache(
            self.root,
            self.registry,
            **{**seed, "seed_legacy_completion": not seed["seed_legacy_completion"]},
        )
        with mock.patch.object(
            VALIDATOR, "_snapshot_projection", wraps=VALIDATOR._snapshot_projection
        ) as project:
            wrong_legacy._snapshot(draft)
            self.assertEqual(len(project.call_args.args[2]), len(blobs))

    def test_rename_rewrite_and_copy_into_target_remain_rejected(self) -> None:
        source = "notes/source.txt"
        self.git.commit(source, b"x" * 20_000)
        (self.root / self.path).parent.mkdir(parents=True, exist_ok=True)
        self.git.run("mv", source, self.path)
        self.git.commit(self.path, self.document("draft", "y" * 300))
        renamed = self.commit_reviewed_activation()
        result, output = self.explicit(self.base, renamed)
        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

        self.git.run("reset", "--hard", self.base)
        source = ".agents/governance/source.md"
        source_body = "\n".join(f"source-{index}" for index in range(100))
        target_body = "\n".join(
            f"source-{index}" if index < 40 else f"target-{index}"
            for index in range(100)
        )
        source_commit = self.commit_path(source, "draft", source_body)
        (self.root / self.path).write_bytes((self.root / source).read_bytes())
        (self.root / self.path).write_bytes(self.document("draft", target_body))
        self.git.run("add", "--", self.path)
        self.git.run("commit", "--quiet", "-m", "copy")
        copy_commit = self.oid("HEAD")
        self.assertIn(
            b"C",
            self.git.run(
                "diff",
                "--find-copies=1%",
                "--find-copies-harder",
                "--name-status",
                "-z",
                source_commit,
                copy_commit,
            ),
        )
        self.assertTrue(
            VALIDATOR._history_rename_or_copy_into_path(
                self.root, source_commit, copy_commit, PurePosixPath(self.path)
            )
        )
        copied = self.commit_reviewed_activation()
        self.assertFalse(self.proved(self.base, copied))
        result, output = self.explicit(self.base, copied)
        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

        self.git.run("reset", "--hard", self.base)
        self.git.commit("notes/unchanged-source.bin", b"\0" * 20_000)
        self.commit("draft")
        independent = self.commit_reviewed_activation()
        result, output = self.explicit(self.base, independent)
        self.assertEqual(result, 0, output)

    def test_missing_evidence_type_change_and_profile_change_retain_create(
        self,
    ) -> None:
        self.commit("draft")
        active = self.commit_reviewed_activation()
        missing = LifecycleDiagnostic(
            "FAIL",
            "LIFECYCLE-EVIDENCE",
            PurePosixPath(self.path),
            "governance/contract",
            "evidence",
            "missing",
            "explicit-ref",
            "missing",
        )
        with mock.patch.object(
            VALIDATOR, "_history_event_diagnostics", return_value=(missing,)
        ):
            result, output = self.explicit(self.base, active)
        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

        self.git.run("reset", "--hard", self.base)
        self.commit("draft")
        target = self.root / self.path
        target.unlink()
        target.symlink_to("non-regular-history-target")
        self.git.run("add", "--", self.path)
        self.git.run("commit", "--quiet", "-m", "type change")
        target.unlink()
        typed = self.commit("active")
        result, output = self.explicit(self.base, typed)
        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

        self.git.run("reset", "--hard", self.base)
        self.commit("draft")
        mismatched = self.document("draft").replace(
            b'type: "governance/contract"',
            b'type: "sdlc/architecture-description"',
        )
        self.git.commit(self.path, mismatched)
        active = self.commit_reviewed_activation()
        result, output = self.explicit(self.base, active)
        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

    def test_aggregate_candidate_budget_fails_closed_before_proof_work(self) -> None:
        second = ".agents/governance/cumulative-history-second.md"
        self.commit_path(self.path, "draft")
        self.commit_path(second, "draft")
        self.commit_reviewed_activation(self.path)
        active = self.commit_reviewed_activation(second)
        candidates = (
            LifecycleDiagnostic(
                "FAIL",
                "LIFECYCLE-CREATE",
                PurePosixPath(self.path),
                "governance/contract",
                "draft",
                "active",
                "explicit-ref",
                "",
            ),
            LifecycleDiagnostic(
                "FAIL",
                "LIFECYCLE-CREATE",
                PurePosixPath(second),
                "governance/contract",
                "draft",
                "active",
                "explicit-ref",
                "",
            ),
        )
        blobs = {
            PurePosixPath(self.path): VALIDATOR._tree_blob_oid(
                self.root, active, PurePosixPath(self.path)
            ),
            PurePosixPath(second): VALIDATOR._tree_blob_oid(
                self.root, active, PurePosixPath(second)
            ),
        }
        with (
            mock.patch.object(VALIDATOR, "CUMULATIVE_HISTORY_MAX_CANDIDATES", 1),
            mock.patch.object(
                VALIDATOR, "_first_parent_history", side_effect=AssertionError
            ) as history,
            mock.patch.object(
                VALIDATOR,
                "_history_proves_cumulative_create",
                side_effect=AssertionError,
            ) as proof,
        ):
            actual = VALIDATOR._admit_cumulative_create_diagnostics(
                candidates,
                root=self.root,
                registry=self.registry,
                mode="explicit-ref",
                base_commit=self.base,
                proposed_commit=active,
                base_blobs={},
                proposed_blobs=blobs,
            )
        self.assertEqual(actual, candidates)
        history.assert_not_called()
        proof.assert_not_called()

        with (
            mock.patch.object(VALIDATOR, "CUMULATIVE_HISTORY_MAX_CANDIDATES", 2),
            mock.patch.object(VALIDATOR, "CUMULATIVE_HISTORY_MAX_CANDIDATE_EVENTS", 1),
            mock.patch.object(
                VALIDATOR,
                "_first_parent_history",
                wraps=VALIDATOR._first_parent_history,
            ) as history,
            mock.patch.object(
                VALIDATOR, "_tree_blob_map", wraps=VALIDATOR._tree_blob_map
            ) as snapshots,
            mock.patch.object(
                VALIDATOR,
                "_history_proves_cumulative_create",
                side_effect=AssertionError,
            ) as proof,
        ):
            actual = VALIDATOR._admit_cumulative_create_diagnostics(
                candidates,
                root=self.root,
                registry=self.registry,
                mode="explicit-ref",
                base_commit=self.base,
                proposed_commit=active,
                base_blobs={},
                proposed_blobs=blobs,
            )
        self.assertEqual(actual, candidates)
        history.assert_called_once_with(self.root, self.base, active)
        snapshots.assert_not_called()
        proof.assert_not_called()

        cache = VALIDATOR._CumulativeHistoryCache(self.root, self.registry)
        with mock.patch.object(VALIDATOR, "CUMULATIVE_HISTORY_CACHE_MAX_SNAPSHOTS", 1):
            cache._snapshot(self.base)
            cache._snapshot(active)
        self.assertEqual(len(cache.snapshots), 1)

        with (
            mock.patch.object(
                VALIDATOR, "CUMULATIVE_HISTORY_MAX_SNAPSHOT_WORK_BYTES", 1
            ),
            mock.patch.object(
                VALIDATOR, "_snapshot_projection", side_effect=AssertionError
            ) as projection,
        ):
            actual = VALIDATOR._admit_cumulative_create_diagnostics(
                candidates,
                root=self.root,
                registry=self.registry,
                mode="explicit-ref",
                base_commit=self.base,
                proposed_commit=active,
                base_blobs={},
                proposed_blobs=blobs,
            )
        self.assertEqual(actual, candidates)
        projection.assert_not_called()

        repeated = {
            PurePosixPath(self.path): blobs[PurePosixPath(self.path)],
            PurePosixPath(".agents/governance/repeated.md"): blobs[
                PurePosixPath(self.path)
            ],
        }
        cache = VALIDATOR._CumulativeHistoryCache(self.root, self.registry)
        with (
            mock.patch.object(VALIDATOR, "CUMULATIVE_HISTORY_MAX_SNAPSHOT_PATHS", 1),
            mock.patch.object(VALIDATOR, "_tree_blob_map", return_value=repeated),
            mock.patch.object(
                VALIDATOR, "_run_git", side_effect=AssertionError
            ) as batch,
            mock.patch.object(
                VALIDATOR, "_snapshot_projection", side_effect=AssertionError
            ) as projection,
            self.assertRaises(VALIDATOR._CumulativeHistoryBudgetExceeded),
        ):
            cache._snapshot(self.base)
        batch.assert_not_called()
        projection.assert_not_called()

        with (
            mock.patch.object(VALIDATOR, "CUMULATIVE_HISTORY_MAX_SNAPSHOT_PATHS", 1),
            mock.patch.object(
                VALIDATOR, "_snapshot_projection", side_effect=AssertionError
            ) as projection,
        ):
            actual = VALIDATOR._admit_cumulative_create_diagnostics(
                candidates,
                root=self.root,
                registry=self.registry,
                mode="explicit-ref",
                base_commit=self.base,
                proposed_commit=active,
                base_blobs={},
                proposed_blobs=blobs,
            )
        self.assertEqual(actual, candidates)
        projection.assert_not_called()

        with (
            mock.patch.object(VALIDATOR, "_run_git", return_value=b"malformed\n"),
            self.assertRaises(VALIDATOR._CumulativeHistoryBudgetExceeded),
        ):
            VALIDATOR._snapshot_blob_size(
                self.root,
                {PurePosixPath(self.path): blobs[PurePosixPath(self.path)]},
            )

        with mock.patch.object(
            VALIDATOR,
            "_history_proves_cumulative_create",
            side_effect=(True, VALIDATOR._CumulativeHistoryBudgetExceeded()),
        ):
            actual = VALIDATOR._admit_cumulative_create_diagnostics(
                candidates,
                root=self.root,
                registry=self.registry,
                mode="explicit-ref",
                base_commit=self.base,
                proposed_commit=active,
                base_blobs={},
                proposed_blobs=blobs,
            )
        self.assertEqual(actual, candidates)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
