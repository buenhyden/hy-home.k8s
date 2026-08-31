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

from tests.test_archive_recovery import GitFixture


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
from document_lifecycle import LifecycleDiagnostic, LifecycleDocument  # noqa: E402


class CumulativeLifecycleHistoryTest(unittest.TestCase):
    path = "docs/00.agent-governance/cumulative-history.md"

    @classmethod
    def setUpClass(cls) -> None:
        cls.seed_temporary = tempfile.TemporaryDirectory(prefix="lifecycle-history-seed-")
        cls.addClassCleanup(cls.seed_temporary.cleanup)
        cls.seed_root = Path(cls.seed_temporary.name) / "repository"
        cls.seed_root.mkdir()
        registry_path = Path("docs/99.templates/registry.json")
        raw_registry = json.loads((ROOT / registry_path).read_text())
        selected = {
            "governance/reference",
            "sdlc/ad",
            "sdlc/data-model",
            "sdlc/plan",
            "content/archive",
        }
        for domain in raw_registry["programLineage"]["lifecycleDomains"]:
            selected.add(
                "content/archive-migration"
                if "content/archive-migration" in domain["profileIds"]
                else domain["profileIds"][0]
            )
            domain["profileIds"] = [
                profile_id for profile_id in domain["profileIds"] if profile_id in selected
            ]
        raw_registry["profiles"] = [
            profile for profile in raw_registry["profiles"] if profile["id"] in selected
        ]
        raw_registry["programLineage"]["programs"] = raw_registry["programLineage"][
            "programs"
        ][:1]
        raw_registry["standaloneExecutions"] = []
        target_registry = cls.seed_root / registry_path
        target_registry.parent.mkdir(parents=True)
        target_registry.write_text(json.dumps(raw_registry))
        templates = {
            profile["template"]
            for profile in raw_registry["profiles"]
            if profile["template"] is not None
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
        self.primary_branch = self.git.run(
            "symbolic-ref", "--short", "HEAD"
        ).decode("ascii").strip()
        self._registry = None

    @property
    def registry(self):
        if self._registry is None:
            self._registry = load_registry(self.root)
        return self._registry

    def oid(self, ref: str) -> str:
        return self.git.run("rev-parse", ref).decode("ascii").strip()

    def document(self, status: str, body: str = "Reviewed policy.") -> bytes:
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
            "title: 'Cumulative history'\n"
            "type: governance/reference\n"
            f"status: {status}\n"
            "owner: platform\n"
            "updated: 2026-08-31\n"
            "---\n\n# Cumulative history\n\n"
            f"{sections}"
        ).encode()

    def commit(self, status: str, body: str = "Reviewed policy.") -> str:
        self.git.commit(self.path, self.document(status, body))
        return self.oid("HEAD")

    def commit_path(
        self,
        path: str,
        status: str,
        body: str = "Reviewed policy.",
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

    def test_explicit_ref_admits_absent_draft_active_chain(self) -> None:
        self.commit("draft")
        active = self.commit("active")

        result, output = self.explicit(self.base, active)

        self.assertEqual(result, 0, output)

    def test_ci_admits_same_chain_from_merge_base(self) -> None:
        self.commit("draft")
        active = self.commit("active")

        result, output = self.invoke("ci", base_ref=self.base, to_ref=active)

        self.assertEqual(result, 0, output)

    def test_same_status_body_change_is_a_valid_intermediate_event(self) -> None:
        self.commit("draft")
        self.commit("draft", "Reviewed policy with an intermediate revision.")
        active = self.commit("active")

        result, output = self.explicit(self.base, active)

        self.assertEqual(result, 0, output)

    def test_committed_ref_blobs_ignore_dirty_checkout_and_index(self) -> None:
        self.commit("draft")
        active = self.commit("active")
        target = self.root / self.path
        target.write_bytes(self.document("retired"))
        self.git.run("add", "--", self.path)

        result, output = self.explicit(self.base, active)

        self.assertEqual(result, 0, output)

    def test_only_create_diagnostic_is_removed_for_a_proved_path(self) -> None:
        self.commit("draft")
        active = self.commit("active")
        path = PurePosixPath(self.path)
        create = LifecycleDiagnostic(
            "FAIL", "LIFECYCLE-CREATE", path, "governance/reference", "draft", "active", "explicit-ref", ""
        )
        duplicate = LifecycleDiagnostic(
            "FAIL", "LIFECYCLE-CREATE", path, "governance/reference", "draft", "active", "explicit-ref", "duplicate"
        )
        other = LifecycleDiagnostic(
            "FAIL", "LIFECYCLE-EVIDENCE", path, "governance/reference", "evidence", "missing", "explicit-ref", "missing"
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
        self.commit("active")
        draft_again = self.commit("draft")
        self.assertFalse(self.proved(self.base, draft_again))

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
        source = "docs/00.agent-governance/source.md"
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
        self.git.commit("docs/00.agent-governance/other.md", self.document("draft"))
        self.git.run("merge", "--no-ff", "--no-edit", "side")
        merged = self.commit("active")
        self.assertFalse(self.proved(self.base, merged))
        self.assertFalse(self.proved(side, self.base))
        result, output = self.explicit(self.base, merged)
        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

    def test_malformed_missing_and_bounded_history_evidence_fails_closed(self) -> None:
        self.commit("draft")
        active = self.commit("active")
        with mock.patch.object(VALIDATOR, "_first_parent_history", return_value=("bad",)):
            self.assertFalse(self.proved(self.base, active))
        with mock.patch.object(VALIDATOR, "CUMULATIVE_HISTORY_MAX_COMMITS", 1):
            self.assertFalse(self.proved(self.base, active))

    def test_staged_direct_active_creation_remains_rejected(self) -> None:
        self.git.commit(self.path, self.document("active"))
        self.git.run("reset", "--soft", "HEAD~1")

        result, output = self.invoke("staged")

        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

    def test_rename_rewrite_and_copy_into_target_remain_rejected(self) -> None:
        source = "docs/00.agent-governance/source.md"
        self.commit_path(source, "draft", "x" * 300)
        self.git.run("mv", source, self.path)
        self.git.commit(self.path, self.document("draft", "y" * 300))
        renamed = self.commit("active")
        result, output = self.explicit(self.base, renamed)
        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

        self.git.run("reset", "--hard", self.base)
        self.commit_path(source, "draft")
        (self.root / self.path).write_bytes((self.root / source).read_bytes())
        self.git.run("add", "--", self.path)
        self.git.run("commit", "--quiet", "-m", "copy")
        copied = self.commit("active")
        result, output = self.explicit(self.base, copied)
        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

    def test_missing_evidence_type_change_and_profile_change_retain_create(self) -> None:
        self.commit("draft")
        active = self.commit("active")
        missing = LifecycleDiagnostic(
            "FAIL", "LIFECYCLE-EVIDENCE", PurePosixPath(self.path), "governance/reference", "evidence", "missing", "explicit-ref", "missing"
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
        active = self.commit("active")
        original = VALIDATOR._history_document

        def changed_profile(*args):
            document = original(*args)
            if args[3] == VALIDATOR._tree_blob_oid(
                self.root, active, PurePosixPath(self.path)
            ):
                return LifecycleDocument(
                    document.path, "sdlc/ad", document.status, document.state_issue
                )
            return document

        with mock.patch.object(VALIDATOR, "_history_document", side_effect=changed_profile):
            result, output = self.explicit(self.base, active)
        self.assertNotEqual(result, 0, output)
        self.assertIn("LIFECYCLE-CREATE", output)

    def test_aggregate_candidate_budget_fails_closed_before_proof_work(self) -> None:
        second = "docs/00.agent-governance/cumulative-history-second.md"
        self.commit_path(self.path, "draft")
        self.commit_path(second, "draft")
        self.commit_path(self.path, "active")
        active = self.commit_path(second, "active")
        candidates = (
            LifecycleDiagnostic(
                "FAIL", "LIFECYCLE-CREATE", PurePosixPath(self.path), "governance/reference", "draft", "active", "explicit-ref", ""
            ),
            LifecycleDiagnostic(
                "FAIL", "LIFECYCLE-CREATE", PurePosixPath(second), "governance/reference", "draft", "active", "explicit-ref", ""
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
                VALIDATOR, "_history_proves_cumulative_create", side_effect=AssertionError
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
            mock.patch.object(VALIDATOR, "_tree_blob_map", wraps=VALIDATOR._tree_blob_map) as snapshots,
            mock.patch.object(
                VALIDATOR, "_history_proves_cumulative_create", side_effect=AssertionError
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


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
