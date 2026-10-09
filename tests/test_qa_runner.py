"""QA profiles execute once over isolated final-tree or exact-index bytes."""

from __future__ import annotations

import builtins
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load_qa():
    path = ROOT / "scripts/qa.py"
    spec = importlib.util.spec_from_file_location("qa_test_owner", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PublicEntryTests(unittest.TestCase):
    def test_public_profiles_are_only_selected_working_tree_and_index(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/qa.py"), "--list"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            [line.split(":", 1)[0] for line in result.stdout.splitlines()],
            ["quick", "staged"],
        )
        for retired in ("full", "ci"):
            with self.subTest(retired=retired):
                denied = subprocess.run(
                    [sys.executable, str(ROOT / "scripts/qa.py"), retired],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(denied.returncode, 2)
                self.assertIn("invalid choice", denied.stderr)


class QaTests(unittest.TestCase):
    def setUp(self):
        self.qa = load_qa()
        self.temporary = tempfile.TemporaryDirectory(prefix="qa-tests-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "source"
        self.root.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "QA Fixture")
        self.git("config", "user.email", "qa@example.invalid")
        (self.root / "file.txt").write_text("original\n")
        (self.root / "gone.txt").write_text("delete\n")
        (self.root / ".gitignore").write_text("ignored-secret\n")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")

    def git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=self.root, check=True, capture_output=True
        ).stdout

    def test_git_diff_reads_without_refreshing_the_private_index(self):
        target = self.root / "file.txt"
        metadata = target.stat()
        os.utime(
            target,
            ns=(metadata.st_atime_ns, metadata.st_mtime_ns + 2_000_000_000),
        )
        baseline = (self.root / ".git/index").read_bytes()
        self.assertEqual(self.qa.git(self.root, "diff", "--name-only", "-z"), b"")
        self.assertEqual((self.root / ".git/index").read_bytes(), baseline)
        target.write_text("changed\n")
        self.assertIn(b"file.txt", self.qa.git(self.root, "diff", "--name-only", "-z"))
        self.assertEqual((self.root / ".git/index").read_bytes(), baseline)

    def test_final_tree_and_index_are_distinct_and_source_is_unchanged(self):
        (self.root / "file.txt").write_text("staged invalid\n")
        self.git("mv", "gone.txt", "renamed space.txt")
        self.git("add", "file.txt")
        (self.root / "file.txt").write_text("unstaged repaired\n")
        (self.root / "new space.txt").write_text("new\n")
        (self.root / "ignored-secret").write_text("excluded\n")
        (self.root / "link").symlink_to("file.txt")
        before = (self.root / ".git/index").read_bytes()
        for staged, expected in [
            (False, "unstaged repaired\n"),
            (True, "staged invalid\n"),
        ]:
            with self.qa.repository_snapshot(self.root, staged=staged) as snapshot:
                self.assertEqual((snapshot / "file.txt").read_text(), expected)
                self.assertTrue((snapshot / "renamed space.txt").is_file())
                self.assertFalse((snapshot / "gone.txt").exists())
                self.assertFalse((snapshot / "ignored-secret").exists())
                self.assertEqual((snapshot / "new space.txt").exists(), not staged)
                self.assertEqual((snapshot / "link").is_symlink(), not staged)
                self.assertEqual(
                    self.qa.git(snapshot, "rev-parse", "HEAD"),
                    self.git("rev-parse", "HEAD"),
                )
                self.assertEqual(self.qa.git(snapshot, "diff", "--name-only"), b"")
        self.assertEqual((self.root / ".git/index").read_bytes(), before)
        self.assertEqual((self.root / "file.txt").read_text(), "unstaged repaired\n")

    def test_staged_source_index_mutation_cannot_enter_pass_cache(self):
        (self.root / "file.txt").write_text("candidate\n")
        self.git("add", "file.txt")
        contract = {
            "profiles": {"staged": ["document-lifecycle"]},
            "validators": [{"id": "document-lifecycle"}],
        }

        def alter_source(*_args, **kwargs):
            kwargs["completed_passes"]["document-lifecycle"] = "PASS"
            (self.root / "file.txt").write_text("raced candidate\n")
            self.git("add", "file.txt")
            return 0

        with (
            mock.patch.object(
                sys, "argv", ["qa.py", "staged", "--root", str(self.root)]
            ),
            mock.patch.object(
                self.qa.contract_module, "validate_contract", return_value=contract
            ),
            mock.patch.object(
                self.qa.contract_module,
                "select_paths",
                return_value={"validators": ["document-lifecycle"]},
            ),
            mock.patch.object(self.qa.runner, "run_selected", side_effect=alter_source),
            mock.patch.object(self.qa.LocalEvidenceStore, "record_pass") as record,
        ):
            self.assertEqual(self.qa.main(), 1)
        record.assert_not_called()

    def test_private_skip_worktree_mutation_is_not_a_pass(self):
        with self.qa.repository_snapshot(self.root, staged=True) as snapshot:
            self.qa.git(snapshot, "update-index", "--skip-worktree", "file.txt")
            head_before = self.qa.git(snapshot, "rev-parse", "HEAD")
            raw_index_before = self.qa.read_bounded_bytes(
                self.qa.index_file(snapshot), max_bytes=self.qa.GIT_INDEX_LIMIT_BYTES
            )
            tree_before = self.qa.tree_identity(snapshot)
            (snapshot / "file.txt").write_text("hidden mutation\n")
            self.assertEqual(self.qa.git(snapshot, "diff", "--name-only", "-z"), b"")
            with self.assertRaisesRegex(
                ValueError, "private snapshot changed: file-bytes"
            ):
                self.qa.require_unchanged_private_snapshot(
                    snapshot,
                    head_before=head_before,
                    raw_index_before=raw_index_before,
                    tree_before=tree_before,
                )

    def test_private_index_only_mutation_reports_index_without_file_data(self):
        with self.qa.repository_snapshot(self.root, staged=True) as snapshot:
            head_before = self.qa.git(snapshot, "rev-parse", "HEAD")
            raw_index_before = self.qa.read_bounded_bytes(
                self.qa.index_file(snapshot), max_bytes=self.qa.GIT_INDEX_LIMIT_BYTES
            )
            tree_before = self.qa.tree_identity(snapshot)
            self.qa.git(snapshot, "update-index", "--assume-unchanged", "file.txt")
            with self.assertRaisesRegex(ValueError, "changed: raw-index$"):
                self.qa.require_unchanged_private_snapshot(
                    snapshot,
                    head_before=head_before,
                    raw_index_before=raw_index_before,
                    tree_before=tree_before,
                )

    def test_private_untracked_file_creation_is_not_a_pass(self):
        with self.qa.repository_snapshot(self.root, staged=True) as snapshot:
            head_before = self.qa.git(snapshot, "rev-parse", "HEAD")
            raw_index_before = self.qa.read_bounded_bytes(
                self.qa.index_file(snapshot), max_bytes=self.qa.GIT_INDEX_LIMIT_BYTES
            )
            tree_before = self.qa.tree_identity(snapshot)
            (snapshot / "new.txt").write_text("formatter output\n")
            with self.assertRaisesRegex(ValueError, "changed: file-bytes$"):
                self.qa.require_unchanged_private_snapshot(
                    snapshot,
                    head_before=head_before,
                    raw_index_before=raw_index_before,
                    tree_before=tree_before,
                )

    def test_snapshot_keeps_a_default_branch_that_exists_only_as_remote_tracking(self):
        # CI checks out a named branch that is not `main`; `main` exists only as
        # `origin/main`, and archive envelopes resolve against it.
        head = self.git("rev-parse", "HEAD").strip()
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        self.git("switch", "-q", "-c", "ci-validated-checkout")
        self.git("branch", "-q", "-D", "master")
        for staged in (False, True):
            with self.qa.repository_snapshot(self.root, staged=staged) as snapshot:
                self.assertEqual(
                    self.qa.git(
                        snapshot, "rev-parse", "refs/remotes/origin/main"
                    ).strip(),
                    head,
                )

    def test_snapshot_supports_worktree_gitfile(self):
        linked = Path(self.temporary.name) / "linked"
        self.git("worktree", "add", "--detach", str(linked))
        with self.qa.repository_snapshot(linked, staged=True) as snapshot:
            self.assertEqual((snapshot / "file.txt").read_text(), "original\n")

    def test_snapshot_preserves_in_progress_merge_parent(self):
        primary = self.git("symbolic-ref", "--short", "HEAD").decode().strip()
        self.git("switch", "-q", "-c", "side")
        (self.root / "side.txt").write_text("side\n")
        self.git("add", "side.txt")
        self.git("commit", "-qm", "side")
        side = self.git("rev-parse", "HEAD").strip()
        self.git("switch", "-q", primary)
        (self.root / "main.txt").write_text("main\n")
        self.git("add", "main.txt")
        self.git("commit", "-qm", "main")
        self.git("merge", "--no-commit", "--no-ff", "side")

        for staged in (False, True):
            with self.subTest(staged=staged):
                with self.qa.repository_snapshot(self.root, staged=staged) as snapshot:
                    merge_head = self.qa.git(
                        snapshot,
                        "rev-parse",
                        "--path-format=absolute",
                        "--git-path",
                        "MERGE_HEAD",
                    ).strip()
                    self.assertEqual(
                        Path(merge_head.decode()).read_bytes(), side + b"\n"
                    )

    def test_full_snapshot_handles_indexed_leaf_replaced_by_directory(self):
        adapter = self.root / ".claude/skills"
        adapter.parent.mkdir()
        adapter.symlink_to("../file.txt")
        self.git("add", ".claude/skills")
        index_before = (self.root / ".git/index").read_bytes()
        adapter.unlink()
        adapter.mkdir()
        child = adapter / "example"
        child.symlink_to("../../file.txt")
        regular = self.root / "gone.txt"
        regular.unlink()
        regular.mkdir()
        (regular / "child.txt").write_text("replacement\n")

        with self.qa.repository_snapshot(self.root) as snapshot:
            self.assertTrue((snapshot / ".claude/skills").is_dir())
            self.assertEqual(
                os.readlink(snapshot / ".claude/skills/example"), "../../file.txt"
            )
            self.assertEqual(
                (snapshot / "gone.txt/child.txt").read_text(), "replacement\n"
            )
            indexed = self.qa.paths_from(self.qa.git(snapshot, "ls-files", "-z"))
            self.assertIn(".claude/skills/example", indexed)
            self.assertNotIn(".claude/skills", indexed)
            self.assertNotIn("gone.txt", indexed)
        self.assertEqual((self.root / ".git/index").read_bytes(), index_before)

    def test_quick_routes_indexed_leaf_directory_transition_through_selected_children(
        self,
    ):
        adapter = self.root / ".claude/skills"
        adapter.parent.mkdir()
        adapter.symlink_to("../file.txt")
        self.git("add", ".claude/skills")
        self.git("commit", "-qm", "old adapter")
        adapter.unlink()
        adapter.mkdir()
        skill = self.root / ".agents/skills/example/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("# Example\n")
        registry = self.root / ".agents/roles/registry.json"
        registry.parent.mkdir(parents=True)
        registry.write_text(
            json.dumps(
                {
                    "skills": [
                        {"id": "example", "path": ".agents/skills/example/SKILL.md"}
                    ]
                }
            )
        )
        (adapter / "example").symlink_to("../../.agents/skills/example")
        contract = self.qa.contract_module.validate_contract(ROOT)
        for staged in (False, True):
            with self.subTest(staged=staged):
                if staged:
                    self.git("add", ".claude/skills", ".agents")
                before = (self.root / ".git/index").read_bytes()
                paths = self.qa.changed_paths(self.root, staged=False)
                self.assertNotIn(".claude/skills", paths)
                self.assertIn(".claude/skills/example", paths)
                with (
                    mock.patch.object(
                        sys, "argv", ["qa.py", "quick", "--root", str(self.root)]
                    ),
                    mock.patch.object(
                        self.qa.contract_module,
                        "validate_contract",
                        return_value=contract,
                    ),
                    mock.patch.object(
                        self.qa.runner, "run_selected", return_value=0
                    ) as run,
                ):
                    self.assertEqual(self.qa.main(), 0)
                run.assert_called_once()
                self.assertEqual(run.call_args.args[2], paths)
                self.assertEqual((self.root / ".git/index").read_bytes(), before)
                if not staged:
                    self.assertEqual(self.qa.changed_paths(self.root, staged=True), [])

    def test_quick_keeps_deletions_rename_inputs_and_directory_without_selected_children(
        self,
    ):
        self.git("mv", "file.txt", "renamed.txt")
        (self.root / "gone.txt").unlink()
        (self.root / "gone.txt").mkdir()
        self.assertEqual(
            self.qa.changed_paths(self.root, staged=False),
            ["file.txt", "gone.txt", "renamed.txt"],
        )

    def test_staged_directory_transition_uses_index_despite_unstaged_replacement(self):
        adapter = self.root / ".claude/skills"
        adapter.parent.mkdir()
        adapter.symlink_to("../file.txt")
        self.git("add", ".claude/skills")
        self.git("commit", "-qm", "old adapter")
        adapter.unlink()
        adapter.mkdir()
        skill_path = ".agents/skills/risk-report/SKILL.md"
        skill = self.root / skill_path
        skill.parent.mkdir(parents=True)
        skill.write_text("# Synthetic skill\n")
        registry_path = ".agents/roles/registry.json"
        registry = self.root / registry_path
        registry.parent.mkdir(parents=True)
        registry.write_text(
            json.dumps({"skills": [{"id": "risk-report", "path": skill_path}]})
        )
        child = adapter / "risk-report"
        child.symlink_to("../../.agents/skills/risk-report")
        self.git("add", ".claude/skills", skill_path, registry_path)
        before = (self.root / ".git/index").read_bytes()
        child.unlink()
        adapter.rmdir()
        adapter.symlink_to("../../outside")

        expected = [registry_path, skill_path, ".claude/skills/risk-report"]
        self.assertEqual(self.qa.changed_paths(self.root, staged=True), expected)
        with self.qa.repository_snapshot(self.root, staged=True) as snapshot:
            paths = self.qa.changed_paths(snapshot, staged=True)
            self.assertEqual(paths, expected)
            self.assertEqual(
                os.readlink(snapshot / ".claude/skills/risk-report"),
                "../../.agents/skills/risk-report",
            )
            contract = self.qa.contract_module.validate_contract(ROOT)
            self.qa.contract_module.select_paths(contract, paths, "staged", snapshot)
        self.assertEqual((self.root / ".git/index").read_bytes(), before)

    def test_staged_transition_preserves_unknown_children_and_plain_deletions(self):
        self.git("rm", "gone.txt")
        target = self.root / "file.txt"
        target.unlink()
        target.mkdir()
        (target / "unknown child.txt").write_text("invalid route\n")
        self.git("add", "file.txt")
        with self.qa.repository_snapshot(self.root, staged=True) as snapshot:
            paths = self.qa.changed_paths(snapshot, staged=True)
            self.assertEqual(paths, ["file.txt/unknown child.txt", "gone.txt"])
            contract = self.qa.contract_module.validate_contract(ROOT)
            with self.assertRaises(self.qa.contract_module.ContractError):
                self.qa.contract_module.select_paths(
                    contract, paths, "staged", snapshot
                )

    def test_quick_does_not_hide_unknown_child_or_escaping_link(self):
        (self.root / "file.txt").unlink()
        (self.root / "file.txt").mkdir()
        (self.root / "file.txt/unknown.txt").write_text("unknown\n")
        paths = self.qa.changed_paths(self.root, staged=False)
        self.assertIn("file.txt/unknown.txt", paths)
        with self.assertRaises(self.qa.contract_module.ContractError):
            self.qa.contract_module.select_paths(
                self.qa.contract_module.validate_contract(ROOT),
                paths,
                "affected",
                self.root,
            )
        (self.root / "gone.txt").unlink()
        (self.root / "gone.txt").symlink_to("../../outside")
        self.assertIn("gone.txt", self.qa.changed_paths(self.root, staged=False))
        with self.assertRaisesRegex(ValueError, "symlink"):
            with self.qa.repository_snapshot(self.root):
                pass

    def test_snapshot_directory_exception_rejects_untracked_and_gitlink_nodes(self):
        directory = self.root / "directory"
        directory.mkdir()
        with self.assertRaisesRegex(ValueError, "regular files and symlinks"):
            self.qa.file_identity(self.root, "directory")
        commit = self.git("rev-parse", "HEAD").decode().strip()
        self.git("update-index", "--add", "--cacheinfo", f"160000,{commit},directory")
        with self.assertRaisesRegex(ValueError, "regular files and symlinks"):
            with self.qa.repository_snapshot(self.root):
                pass

    def test_public_document_terms_do_not_exempt_other_secret_matches(self):
        import json

        executable = self.qa.runner.secure_gitleaks_executable(ROOT)
        self.assertIsNotNone(executable, "Gitleaks is a required validation tool")
        (self.root / ".gitleaks.toml").write_bytes(
            (ROOT / ".gitleaks.toml").read_bytes()
        )
        products = "/".join(("Prometheus", "Grafana"))
        control = "=".join(("GH_PROMPT_DISABLED", "1"))
        documents = {
            "docs/98.archive/completed/03.specs/0024-observability-and-network-review-agents/spec.md": f"live cluster scraping, {products} query execution,\n",
            "docs/98.archive/completed/03.specs/0062-workspace-research-full-corpus-reverification/plan.md": f"non-secret controls:\n`{control}`\n",
        }
        for name, content in documents.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        with tempfile.TemporaryDirectory(prefix="qa-public-term-report-") as tmp:
            report = Path(tmp) / "findings.json"

            def scan():
                return subprocess.run(
                    [
                        executable,
                        "dir",
                        "--redact",
                        "--config=.gitleaks.toml",
                        ".",
                        "--report-format=json",
                        "--report-path=" + str(report),
                    ],
                    cwd=self.root,
                    env=self.qa.runner.closed_subprocess_environment(),
                    capture_output=True,
                    timeout=20,
                )

            self.assertEqual(scan().returncode, 0)
            # Construct harmless negative data rather than store a token fixture.
            value = "".join(f"{chr(97 + n)}{chr(65 + n)}{n % 10}" for n in range(12))
            canary = 'api_key = "' + value + '"\n'
            for name, content in documents.items():
                (self.root / name).write_text(content + canary)
            outside_paths = set()
            for number, content in enumerate(documents.values()):
                name = f"elsewhere-{number}.md"
                outside_paths.add(name)
                (self.root / name).write_text(content)
            self.assertEqual(scan().returncode, 1)
            rows = json.loads(report.read_text())
            self.assertEqual(
                {row["File"] for row in rows}, set(documents) | outside_paths
            )
            self.assertEqual({row["RuleID"] for row in rows}, {"generic-api-key"})

    def test_snapshot_rejects_escaping_symlinks(self):
        (self.root / "escape").symlink_to("../../outside")
        with self.assertRaisesRegex(ValueError, "symlink"):
            with self.qa.repository_snapshot(self.root):
                pass

    def test_identity_and_copy_reject_leaf_and_parent_swaps_before_outside_open(self):
        for operation in ("identity", "copy"):
            for node in ("leaf", "parent"):
                with self.subTest(operation=operation, node=node):
                    directory = self.root / f"swap-{operation}-{node}"
                    directory.mkdir()
                    target = directory / "swap-input.txt"
                    target.write_bytes(b"inside fixture")
                    outside = Path(self.temporary.name) / f"outside-{operation}-{node}"
                    outside.mkdir()
                    sentinel = outside / target.name
                    sentinel.write_bytes(b"harmless outside fixture")
                    outside_inode = sentinel.stat().st_ino
                    armed = operation == "identity"
                    attacked = False
                    outside_opened = []
                    path_open = Path.open
                    builtin_open = builtins.open
                    descriptor_open = os.open
                    tree_identity = self.qa.tree_identity

                    def attack(path):
                        nonlocal attacked
                        if not armed or attacked or isinstance(path, int):
                            return
                        if Path(path) not in (target, Path(target.name)):
                            return
                        attacked = True
                        moved = target if node == "leaf" else directory
                        moved.rename(moved.with_name(moved.name + "-original"))
                        moved.symlink_to(sentinel if node == "leaf" else outside)

                    def observe(descriptor):
                        if os.fstat(descriptor).st_ino == outside_inode:
                            outside_opened.append(descriptor)

                    def open_path(path, mode="r", *args, **kwargs):
                        if "r" in mode:
                            attack(path)
                        result = path_open(path, mode, *args, **kwargs)
                        if "r" in mode:
                            observe(result.fileno())
                        return result

                    def open_builtin(path, mode="r", *args, **kwargs):
                        if "r" in mode:
                            attack(path)
                        result = builtin_open(path, mode, *args, **kwargs)
                        if "r" in mode:
                            observe(result.fileno())
                        return result

                    def open_descriptor(path, flags, *args, **kwargs):
                        if (
                            not flags & os.O_DIRECTORY
                            and flags & os.O_ACCMODE == os.O_RDONLY
                        ):
                            attack(path)
                        result = descriptor_open(path, flags, *args, **kwargs)
                        observe(result)
                        return result

                    def identify(root):
                        nonlocal armed
                        result = tree_identity(root)
                        if root == self.root:
                            armed = True
                        return result

                    try:
                        with (
                            mock.patch.object(Path, "open", open_path),
                            mock.patch.object(builtins, "open", open_builtin),
                            mock.patch.object(os, "open", open_descriptor),
                            mock.patch.object(
                                self.qa, "tree_identity", side_effect=identify
                            ),
                        ):
                            with self.assertRaises((ValueError, OSError)):
                                if operation == "identity":
                                    self.qa.file_identity(
                                        self.root,
                                        target.relative_to(self.root).as_posix(),
                                    )
                                else:
                                    with self.qa.repository_snapshot(self.root):
                                        pass
                    finally:
                        if attacked:
                            moved = target if node == "leaf" else directory
                            moved.unlink()
                            moved.with_name(moved.name + "-original").rename(moved)
                    self.assertTrue(attacked)
                    self.assertEqual(outside_opened, [])

    def test_snapshot_file_and_index_reads_have_separate_finite_limits(self):
        with mock.patch.object(self.qa, "SNAPSHOT_FILE_LIMIT_BYTES", 4):
            with self.assertRaisesRegex(ValueError, "byte budget"):
                self.qa.file_identity(self.root, "file.txt")
        before = (self.root / ".git/index").read_bytes()
        with mock.patch.object(self.qa, "GIT_INDEX_LIMIT_BYTES", 4):
            with self.assertRaisesRegex(ValueError, "byte budget"):
                with self.qa.repository_snapshot(self.root):
                    pass
        self.assertEqual((self.root / ".git/index").read_bytes(), before)

    def test_quick_baseline_uses_head_without_main_and_explicit_empty(self):
        initial = self.git("rev-parse", "HEAD").decode().strip()
        self.assertEqual(self.qa.base_revision(self.root, "quick", ""), initial)
        self.assertEqual(self.qa.base_revision(self.root, "quick", "0" * 40), "EMPTY")
        (self.root / "file.txt").write_text("next\n")
        self.git("commit", "-qam", "next")
        next_head = self.git("rev-parse", "HEAD").decode().strip()
        self.assertEqual(self.qa.base_revision(self.root, "quick", ""), next_head)

    def test_gate_failure_diagnostics_are_bounded_and_redacted(self):
        row = {
            "id": "fixture",
            "argv": ["python3", "check.py"],
            "optional": False,
            "fallback": {"reason": "required"},
            "evidenceLane": "repo-static",
        }
        (self.root / "check.py").write_text(
            "import sys; print('validation failed token=abc123\\n' + 'x'*10000, file=sys.stderr); sys.exit(7)"
        )
        import io
        from contextlib import redirect_stdout

        output = io.StringIO()
        with redirect_stdout(output):
            rc = self.qa.runner.run_selected(
                self.root,
                "affected",
                ["file.txt"],
                {"validators": [row]},
                mock.Mock(),
                validator_ids=["fixture"],
            )
        self.assertEqual(rc, 1)
        self.assertIn("rc=7", output.getvalue())
        self.assertIn("validation failed", output.getvalue())
        self.assertNotIn("abc123", output.getvalue())
        self.assertLess(len(output.getvalue()), 5000)

    def test_python_preserves_invoking_venv_and_refuses_path_shadow(self):
        selected = "/opt/test-venv/bin/python3"
        with mock.patch.object(self.qa.runner.sys, "executable", selected):
            with mock.patch.dict(
                os.environ, {"PATH": str(self.root), "PYTHONPATH": str(self.root)}
            ):
                self.assertEqual(
                    self.qa.runner.resolve_tool("python3", self.root), selected
                )
                self.assertNotIn(
                    str(self.root),
                    self.qa.runner.closed_subprocess_environment()["PATH"],
                )
                self.assertNotIn(
                    "PYTHONPATH", self.qa.runner.closed_subprocess_environment()
                )
                self.assertEqual(
                    self.qa.runner.closed_subprocess_environment()[
                        "GIT_OPTIONAL_LOCKS"
                    ],
                    "0",
                )

    def test_required_missing_tool_fails(self):
        import io
        from contextlib import redirect_stdout

        row = {
            "id": "missing",
            "argv": ["python3", "check.py"],
            "optional": False,
            "fallback": {"reason": "required"},
            "evidenceLane": "repo-static",
        }
        with (
            mock.patch.object(self.qa.runner, "resolve_tool", return_value=None),
            redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(
                self.qa.runner.run_selected(
                    self.root,
                    "affected",
                    ["file.txt"],
                    {"validators": [row]},
                    mock.Mock(),
                    validator_ids=["missing"],
                ),
                1,
            )

    def test_formatter_mutation_fails_without_changing_source(self):
        with self.qa.repository_snapshot(self.root) as snapshot:
            head_before = self.qa.git(snapshot, "rev-parse", "HEAD")
            raw_index_before = self.qa.read_bounded_bytes(
                self.qa.index_file(snapshot), max_bytes=self.qa.GIT_INDEX_LIMIT_BYTES
            )
            tree_before = self.qa.tree_identity(snapshot)
            (snapshot / "file.txt").write_text("formatted\n")
            with self.assertRaisesRegex(
                ValueError, "private snapshot changed: file-bytes"
            ):
                self.qa.require_unchanged_private_snapshot(
                    snapshot,
                    head_before=head_before,
                    raw_index_before=raw_index_before,
                    tree_before=tree_before,
                )
        self.assertEqual((self.root / "file.txt").read_text(), "original\n")

    def test_gate_staged_mutation_fails_without_changing_source_or_index(self):
        import io
        from contextlib import redirect_stderr

        source_index_before = (self.root / ".git/index").read_bytes()

        def stage_mutation(snapshot, *_args, **_kwargs):
            (snapshot / "file.txt").write_text("formatted and staged\n")
            self.qa.git(snapshot, "add", "--", "file.txt")
            return 0

        contract = self.qa.contract_module.validate_contract(ROOT)
        errors = io.StringIO()
        with (
            mock.patch.object(
                sys, "argv", ["qa.py", "quick", "--root", str(self.root)]
            ),
            mock.patch.object(
                self.qa.contract_module, "validate_contract", return_value=contract
            ),
            mock.patch.object(
                self.qa.runner, "run_selected", side_effect=stage_mutation
            ),
            redirect_stderr(errors),
        ):
            self.assertEqual(self.qa.main(), 1)
        self.assertIn(
            "QA private snapshot changed: raw-index,file-bytes", errors.getvalue()
        )
        self.assertEqual((self.root / "file.txt").read_text(), "original\n")
        self.assertEqual((self.root / ".git/index").read_bytes(), source_index_before)


if __name__ == "__main__":
    unittest.main()


class LocalEvidenceTests(unittest.TestCase):
    setUp = QaTests.setUp
    git = QaTests.git

    def test_captured_private_tree_keeps_identity_without_rescanning(self):
        gate = {
            "id": "fixture-change-scoped",
            "argv": ["python3", "check.py"],
            "reuse": {"mode": "change-scoped"},
        }
        arguments = {
            "lane": "staged",
            "paths": ("file.txt",),
            "base_ref": "fixed-base",
            "environment": {"LANG": "C.UTF-8"},
        }
        expected = self.qa.gate_input_identity(self.root, gate, **arguments)
        captured = self.qa.tree_identity(self.root)
        with mock.patch.object(
            self.qa, "tree_identity", side_effect=AssertionError("duplicate tree scan")
        ):
            actual = self.qa.gate_input_identity(
                self.root, gate, **arguments, captured_tree=captured
            )
        self.assertEqual(actual, expected)

    def test_exact_input_identity_changes_for_bytes_mode_paths_base_and_argv(self):
        gate = {
            "id": "fixture-change-scoped",
            "argv": ["python3", "check.py"],
            "reuse": {"mode": "change-scoped"},
        }
        env = {"PATH": "/usr/bin", "LANG": "C.UTF-8"}

        def identity(lane="affected", paths=("file.txt",), base="base-a"):
            return self.qa.gate_input_identity(
                self.root, gate, lane=lane, paths=paths, base_ref=base, environment=env
            )

        initial = identity()
        self.assertEqual(initial, identity())
        self.assertEqual(initial, identity(lane="staged"))
        env["LANG"] = "C"
        self.assertNotEqual(initial, identity())
        env["LANG"] = "C.UTF-8"
        self.assertNotEqual(initial, identity(paths=("gone.txt",)))
        self.assertNotEqual(initial, identity(base="base-b"))
        with self.assertRaisesRegex(ValueError, "lane"):
            identity(lane="all-files")
        gate["argv"] = ["python3", "changed.py"]
        self.assertNotEqual(initial, identity())
        gate["argv"] = ["python3", "check.py"]
        (self.root / "file.txt").write_text("changed\n")
        self.assertNotEqual(initial, identity())
        (self.root / "file.txt").write_text("original\n")
        (self.root / "file.txt").chmod(0o755)
        self.assertNotEqual(initial, identity())
        (self.root / "file.txt").chmod(0o644)
        (self.root / "new.txt").write_text("new\n")
        self.assertNotEqual(initial, identity())

    def test_quick_repeat_and_exact_quick_to_staged_run_once(self):
        (self.root / "check.py").write_text("print('gate passed')\n")
        contract = {
            "validators": [
                {
                    "id": "fixture-change-scoped",
                    "argv": ["python3", "check.py"],
                    "lanes": ["affected", "staged"],
                    "optional": False,
                    "fallback": {"status": "FAIL", "reason": "required"},
                    "evidenceLane": "repo-static",
                    "reuse": {"mode": "change-scoped"},
                }
            ]
        }
        with (
            mock.patch.object(
                self.qa.contract_module, "validate_contract", return_value=contract
            ),
            mock.patch.object(
                self.qa.contract_module,
                "select_paths",
                return_value={"validators": ["fixture-change-scoped"]},
            ),
            mock.patch.object(
                self.qa.contract_module,
                "profile_gate_ids",
                return_value=["fixture-change-scoped"],
            ),
            mock.patch.object(self.qa, "base_revision", return_value="fixed-base"),
            mock.patch.object(
                self.qa.runner,
                "run_bounded_command",
                wraps=self.qa.runner.run_bounded_command,
            ) as child,
            mock.patch.object(
                sys, "argv", ["qa.py", "quick", "--root", str(self.root)]
            ),
        ):
            # Count only the gate command; Git snapshot commands also use the bounded runner.
            import io
            from contextlib import redirect_stdout

            results = []
            for profile in ("quick", "quick", "staged"):
                if profile == "staged":
                    self.git("add", "check.py")
                sys.argv[1] = profile
                with redirect_stdout(io.StringIO()) as output:
                    results.append((self.qa.main(), output.getvalue()))
            gate_calls = [
                call
                for call in child.call_args_list
                if call.args and any("check.py" == arg for arg in call.args[0])
            ]
        self.assertEqual([result for result, _ in results], [0, 0, 0])
        self.assertEqual(len(gate_calls), 1)
        self.assertIn("[REUSED] fixture-change-scoped", results[1][1])
        self.assertIn("[REUSED] fixture-change-scoped", results[2][1])

        # The same selected path must execute again when its staged bytes change.
        (self.root / "check.py").write_text("print('changed gate')\n")
        self.git("add", "check.py")
        with (
            mock.patch.object(
                self.qa.contract_module, "validate_contract", return_value=contract
            ),
            mock.patch.object(
                self.qa.contract_module,
                "select_paths",
                return_value={"validators": ["fixture-change-scoped"]},
            ),
            mock.patch.object(
                self.qa.contract_module,
                "profile_gate_ids",
                return_value=["fixture-change-scoped"],
            ),
            mock.patch.object(self.qa, "base_revision", return_value="fixed-base"),
            mock.patch.object(
                self.qa.runner,
                "run_bounded_command",
                wraps=self.qa.runner.run_bounded_command,
            ) as changed_child,
            mock.patch.object(
                sys, "argv", ["qa.py", "staged", "--root", str(self.root)]
            ),
        ):
            with redirect_stdout(io.StringIO()) as changed_output:
                self.assertEqual(self.qa.main(), 0)
            (self.root / "check.py").chmod(0o755)
            self.git("add", "check.py")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(self.qa.main(), 0)
            (self.root / "new.txt").write_text("new path\n")
            sys.argv[1] = "quick"
            with redirect_stdout(io.StringIO()):
                self.assertEqual(self.qa.main(), 0)
            gate_calls = [
                call
                for call in changed_child.call_args_list
                if call.args and "check.py" in call.args[0]
            ]
        self.assertEqual(len(gate_calls), 3)
        self.assertIn("[PASS] fixture-change-scoped", changed_output.getvalue())

    def test_changed_tool_config_and_argv_execute_again(self):
        (self.root / "check.py").write_text("print('gate passed')\n")
        (self.root / "config.json").write_text('{"rule":1}\n')
        self.git("add", "check.py", "config.json")
        contract = {
            "validators": [
                {
                    "id": "fixture-change-scoped",
                    "argv": ["python3", "check.py"],
                    "lanes": ["affected", "staged"],
                    "optional": False,
                    "fallback": {"status": "FAIL", "reason": "required"},
                    "evidenceLane": "repo-static",
                    "reuse": {"mode": "change-scoped"},
                }
            ]
        }
        import io
        from contextlib import redirect_stdout

        baseline = ["fixed-base"]
        with (
            mock.patch.object(
                self.qa.contract_module, "validate_contract", return_value=contract
            ),
            mock.patch.object(
                self.qa.contract_module,
                "select_paths",
                return_value={"validators": ["fixture-change-scoped"]},
            ),
            mock.patch.object(
                self.qa.contract_module,
                "profile_gate_ids",
                return_value=["fixture-change-scoped"],
            ),
            mock.patch.object(
                self.qa, "base_revision", side_effect=lambda *_: baseline[0]
            ),
            mock.patch.object(
                sys, "argv", ["qa.py", "staged", "--root", str(self.root)]
            ),
            mock.patch.object(
                self.qa.runner,
                "run_bounded_command",
                wraps=self.qa.runner.run_bounded_command,
            ) as child,
        ):
            for step in range(5):
                if step == 1:
                    (self.root / "config.json").write_text('{"rule":2}\n')
                    self.git("add", "config.json")
                if step == 2:
                    contract["validators"][0]["argv"].append("--flag")
                if step == 3:
                    baseline[0] = "changed-base"
                if step == 4:
                    alternate = Path(self.temporary.name) / "python3"
                    alternate.symlink_to(sys.executable)
                    original_resolve = self.qa.runner.resolve_tool
                    with mock.patch.object(
                        self.qa.runner,
                        "resolve_tool",
                        side_effect=lambda token, root: (
                            str(alternate)
                            if token == "python3"
                            else original_resolve(token, root)
                        ),
                    ):
                        with redirect_stdout(io.StringIO()):
                            self.assertEqual(self.qa.main(), 0)
                    continue
                with redirect_stdout(io.StringIO()):
                    self.assertEqual(self.qa.main(), 0)
            gate_calls = [
                call
                for call in child.call_args_list
                if call.args and "check.py" in call.args[0]
            ]
        self.assertEqual(len(gate_calls), 5)

    def test_formatter_rewrite_cannot_record_pass(self):
        (self.root / "check.py").write_text("print('gate passed')\n")
        contract = {
            "validators": [
                {
                    "id": "fixture-change-scoped",
                    "argv": ["python3", "check.py"],
                    "lanes": ["affected", "staged"],
                    "optional": False,
                    "fallback": {"status": "FAIL", "reason": "required"},
                    "evidenceLane": "repo-static",
                    "reuse": {"mode": "change-scoped"},
                }
            ]
        }

        def mutating_run(snapshot, *_args, **kwargs):
            kwargs["completed_passes"]["fixture-change-scoped"] = "PASS"
            (snapshot / "check.py").write_text("formatter rewrite\n")
            return 0

        with (
            mock.patch.object(
                self.qa.contract_module, "validate_contract", return_value=contract
            ),
            mock.patch.object(
                self.qa.contract_module,
                "select_paths",
                return_value={"validators": ["fixture-change-scoped"]},
            ),
            mock.patch.object(
                self.qa.contract_module,
                "profile_gate_ids",
                return_value=["fixture-change-scoped"],
            ),
            mock.patch.object(self.qa, "base_revision", return_value="fixed-base"),
            mock.patch.object(self.qa.runner, "run_selected", side_effect=mutating_run),
            mock.patch.object(
                sys, "argv", ["qa.py", "quick", "--root", str(self.root)]
            ),
        ):
            import io
            from contextlib import redirect_stderr

            with redirect_stderr(io.StringIO()):
                self.assertEqual(self.qa.main(), 1)
        self.assertEqual(self.qa.LocalEvidenceStore(self.root)._passes(), {})

    def test_pr_merge_identity_never_replaces_main_history_or_named_refs(self):
        gate = {
            "id": "fixture-change-scoped",
            "argv": ["python3", "check.py"],
            "reuse": {"mode": "change-scoped"},
        }
        base = self.git("rev-parse", "HEAD").decode().strip()
        tree = self.git("rev-parse", "HEAD^{tree}").decode().strip()

        def commit(label, parents):
            return (
                self.git(
                    "commit-tree",
                    tree,
                    *[arg for parent in parents for arg in ("-p", parent)],
                    "-m",
                    label,
                )
                .decode()
                .strip()
            )

        first = commit("feature one", [base])
        head = commit("feature two", [first])
        tested = commit("synthetic PR merge", [base, head])
        self.git("checkout", "--detach", tested)

        def identity():
            return self.qa.gate_input_identity(
                self.root,
                gate,
                lane="affected",
                paths=("file.txt",),
                base_ref=base,
                environment={"LANG": "C.UTF-8"},
            )

        with mock.patch.object(
            self.qa.importlib.metadata, "distributions", return_value=[]
        ):
            original = identity()
            advanced = commit("advanced main", [base])
            for label, parents in (
                ("merge", [base, head]),
                ("squash", [base]),
                ("multi-commit rebase", [first]),
                ("advanced main merge", [advanced, head]),
            ):
                integrated = commit(label, parents)
                self.git("checkout", "--detach", integrated)
                self.assertEqual(
                    self.git("rev-parse", "HEAD^{tree}").decode().strip(), tree
                )
                self.assertNotEqual(original, identity(), label)
            self.git("checkout", "--detach", tested)
            self.assertEqual(original, identity())
            self.git("update-ref", "refs/remotes/origin/main", advanced)
            self.assertNotEqual(original, identity(), "named ref changed")
            self.git("checkout", "--detach", head)
            self.assertEqual(self.qa.base_revision(self.root, "quick", base), base)
            expected = self.git("merge-base", "HEAD", "origin/main").decode().strip()
            self.assertEqual(self.qa.base_revision(self.root, "quick", None), expected)

    def test_record_is_private_and_rejects_forged_or_unreadable_data(self):
        store = self.qa.LocalEvidenceStore(self.root)
        identity = "a" * 64
        self.assertFalse(store.matching_pass("gate", identity))
        store.record_pass("gate", identity)
        self.assertTrue(store.matching_pass("gate", identity))
        self.assertEqual(stat.S_IMODE(store.path.stat().st_mode), 0o600)
        store.path.write_text(
            '{"version":1,"passes":{"gate":"' + identity + '"},"evil":true}'
        )
        self.assertFalse(store.matching_pass("gate", identity))
        store.path.write_text("[]")
        self.assertFalse(store.matching_pass("gate", identity))
        store.path.chmod(0)
        self.assertFalse(store.matching_pass("gate", identity))
