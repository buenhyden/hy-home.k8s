"""QA profiles execute once over isolated final-tree or exact-index bytes."""

from __future__ import annotations

import copy
import builtins
import importlib.util
import json
import os
from pathlib import Path
import pwd
import stat
import subprocess
import sys
import tempfile
from types import SimpleNamespace
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
    def test_list_is_a_working_public_entry(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/qa.py"), "--list"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("full", result.stdout)
        self.assertIn("staged", result.stdout)


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

    def test_snapshot_supports_worktree_gitfile(self):
        linked = Path(self.temporary.name) / "linked"
        self.git("worktree", "add", "--detach", str(linked))
        with self.qa.repository_snapshot(linked, staged=True) as snapshot:
            self.assertEqual((snapshot / "file.txt").read_text(), "original\n")

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

    def test_full_pre_commit_receives_untracked_hidden_skill_in_temporary_index(self):
        self.git("mv", "file.txt", "README.md")
        self.git("rm", "gone.txt")
        hidden = ".agents/skills/example/SKILL.md"
        target = self.root / hidden
        target.parent.mkdir(parents=True)
        target.write_text("# New skill\n")
        index_before = (self.root / ".git/index").read_bytes()
        head_before = self.git("rev-parse", "HEAD")
        contract = self.qa.contract_module.load_json(
            ROOT / "scripts/validation/registry.json"
        )
        contract["profiles"]["full"] = ["pre-commit"]
        real_run = self.qa.runner.run_bounded_command
        observed = []

        def run_command(argv, *, cwd, env, **kwargs):
            if argv[0] != "/trusted/pre-commit":
                return real_run(argv, cwd=cwd, env=env, **kwargs)
            self.assertNotEqual(cwd, self.root)
            self.assertEqual(argv, ["/trusted/pre-commit", "run", "--all-files"])
            self.assertEqual((cwd / hidden).read_text(), "# New skill\n")
            self.assertIn(
                hidden, self.qa.paths_from(self.qa.git(cwd, "ls-files", "-z"))
            )
            self.assertEqual((self.root / ".git/index").read_bytes(), index_before)
            observed.append(hidden)
            return real_run([sys.executable, "-c", "pass"], cwd=cwd, env=env)

        with (
            mock.patch.object(sys, "argv", ["qa.py", "full", "--root", str(self.root)]),
            mock.patch.object(
                self.qa.contract_module, "validate_contract", return_value=contract
            ),
            mock.patch.object(
                self.qa.runner, "resolve_tool", return_value="/trusted/pre-commit"
            ),
            mock.patch.object(
                self.qa.runner, "run_bounded_command", side_effect=run_command
            ),
        ):
            self.assertEqual(self.qa.main(), 0)
        self.assertEqual(observed, [hidden])
        self.assertEqual((self.root / ".git/index").read_bytes(), index_before)
        self.assertEqual(self.git("rev-parse", "HEAD"), head_before)
        self.assertNotIn(hidden, self.qa.paths_from(self.git("ls-files", "-z")))

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

    def test_ci_baseline_is_parent_or_empty_never_self(self):
        self.assertEqual(self.qa.base_revision(self.root, "ci", ""), "EMPTY")
        self.assertEqual(self.qa.base_revision(self.root, "ci", "0" * 40), "EMPTY")
        parent = self.git("rev-parse", "HEAD").decode().strip()
        (self.root / "file.txt").write_text("next\n")
        self.git("commit", "-qam", "next")
        self.assertEqual(self.qa.base_revision(self.root, "ci", ""), parent)

    def test_profiles_are_complete_equal_and_deduplicated(self):
        contract = self.qa.contract_module.validate_contract(ROOT)
        self.assertEqual(contract["profiles"]["full"], contract["profiles"]["ci"])
        ids = contract["profiles"]["full"]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), {r["id"] for r in contract["validators"]})
        self.assertEqual(ids.count("unit-tests"), 1)
        self.assertEqual(ids.count("pre-commit"), 1)
        for mutation in ("duplicate", "unknown", "missing"):
            bad = copy.deepcopy(contract)
            if mutation == "duplicate":
                bad["profiles"]["full"].append(ids[0])
            elif mutation == "unknown":
                bad["profiles"]["full"][0] = "no-such-gate"
            else:
                bad["profiles"]["full"].pop()
            with self.assertRaises(self.qa.contract_module.ContractError):
                self.qa.contract_module.validate_contract(ROOT, bad)

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
                "all-files",
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

    def test_required_missing_tool_fails(self):
        import io
        from contextlib import redirect_stdout

        row = {
            "id": "missing",
            "argv": ["pre-commit", "run", "--all-files"],
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
                    "all-files",
                    ["file.txt"],
                    {"validators": [row]},
                    mock.Mock(),
                    validator_ids=["missing"],
                ),
                1,
            )

    def test_formatter_mutation_fails_without_changing_source(self):
        with self.qa.repository_snapshot(self.root) as snapshot:
            (snapshot / "file.txt").write_text("formatted\n")
            with self.assertRaisesRegex(ValueError, "modified"):
                self.qa.require_unchanged_snapshot(snapshot)
        self.assertEqual((self.root / "file.txt").read_text(), "original\n")


class FailureSnippetTests(unittest.TestCase):
    def setUp(self):
        self.runner = load_qa().runner

    def snippet(self, *, stdout=b"", stderr=b""):
        result = SimpleNamespace(
            stdout=SimpleNamespace(retained=stdout),
            stderr=SimpleNamespace(retained=stderr),
        )
        return self.runner.failure_snippet(result)

    def test_unittest_error_headers_survive_progress_noise(self):
        result = self.snippet(
            stderr=b"." * 4096
            + b"\nERROR: test_import (tests.Example.test_import)\nprivate traceback body\nFAIL: test_value (tests.Example.test_value)\nFAILED (failures=1, errors=1)\n"
        )
        self.assertIn("ERROR: test_import", result)
        self.assertIn("FAIL: test_value", result)
        self.assertIn("FAILED (failures=1, errors=1)", result)
        self.assertNotIn("private traceback body", result)

    def test_pre_commit_failed_hook_and_exit_survive_passes_and_stderr_warning(self):
        result = self.snippet(
            stdout=b"passing hook........................Passed\n" * 80
            + b"ruff-check........................Failed\n- hook id: ruff-check\n- exit code: 1\nprivate child body\n",
            stderr=b"harmless warning\n",
        )
        self.assertIn("ruff-check", result)
        self.assertIn("- hook id: ruff-check", result)
        self.assertIn("- exit code: 1", result)
        self.assertNotIn("passing hook", result)
        self.assertNotIn("private child body", result)

    def test_prioritized_diagnostics_remain_redacted_escaped_and_bounded(self):
        # Construct a synthetic PEM envelope; no encoded key material is used.
        key_label = b"PRIVATE KEY"
        envelope = b"-----BEGIN %s-----\nERROR: hidden-key-body\n-----END %s-----\n"
        payload = (
            envelope % (key_label, key_label)
            + b"ERROR: test_sample token=do-not-expose \x1b[31m\n" * 200
        )
        result = self.snippet(stderr=payload)
        self.assertNotIn("hidden-key-body", result)
        self.assertNotIn("do-not-expose", result)
        self.assertNotIn("\x1b", result)
        self.assertLessEqual(len(json.loads(result)), 1024)

    def test_generic_failure_keeps_the_existing_bounded_fallback(self):
        result = self.snippet(stderr=b"validation failed token=hidden\n" + b"x" * 2048)
        self.assertIn("validation failed", result)
        self.assertNotIn("hidden", result)
        self.assertLessEqual(len(json.loads(result)), 1024)


class PreCommitResolutionTests(unittest.TestCase):
    def setUp(self):
        self.runner = load_qa().runner
        self.home = Path("/home/qa-fixture")
        self.candidate = self.home / ".local/bin/pre-commit"
        self.target = self.home / ".local/share/uv/tools/pre-commit/bin/pre-commit"
        self.metadata = {
            path: SimpleNamespace(st_mode=stat.S_IFDIR | 0o755, st_uid=1000)
            for path in (*self.candidate.parents, *self.target.parents)
        }
        # Namespace-mapped platform ancestors are outside the passwd-home anchor.
        for path in self.home.parents:
            self.metadata[path].st_uid = 65534
        self.metadata[self.candidate] = SimpleNamespace(
            st_mode=stat.S_IFLNK | 0o777, st_uid=1000
        )
        self.metadata[self.target] = SimpleNamespace(
            st_mode=stat.S_IFREG | 0o755, st_uid=1000
        )
        account = pwd.struct_passwd(
            ("qa-fixture", "x", 1000, 1000, "", str(self.home), "/bin/sh")
        )
        for patcher in (
            mock.patch.object(self.runner.pwd, "getpwuid", return_value=account),
            mock.patch.object(self.runner.sys, "executable", "/usr/bin/python3"),
            mock.patch.object(self.runner.shutil, "which", return_value=None),
            mock.patch.object(Path, "lstat", autospec=True, side_effect=self.lstat),
            mock.patch.object(
                self.runner.os, "readlink", return_value=str(self.target)
            ),
            mock.patch.object(self.runner.os, "access", return_value=True),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def lstat(self, path):
        try:
            return self.metadata[Path(path)]
        except KeyError as exc:
            raise FileNotFoundError(path) from exc

    def test_exact_account_owned_uv_entrypoint_resolves_without_ambient_path(self):
        with mock.patch.dict(
            os.environ, {"PATH": "/tmp/shadow", "HOME": "/tmp/hostile"}
        ):
            self.assertEqual(
                self.runner.resolve_tool("pre-commit", ROOT), str(self.target)
            )
        self.assertNotIn(
            "/tmp/shadow", self.runner.shutil.which.call_args.kwargs["path"]
        )

    def test_regular_account_entrypoint_remains_supported(self):
        self.metadata[self.candidate].st_mode = stat.S_IFREG | 0o755
        self.assertEqual(
            self.runner.resolve_tool("pre-commit", ROOT), str(self.candidate)
        )

    def test_entrypoint_rejects_untrusted_ownership_modes_and_symlink_parents(self):
        mutations = (
            (self.candidate, "st_uid", 1001),
            (self.target, "st_uid", 1001),
            (self.target, "st_mode", stat.S_IFREG | 0o775),
            (self.target, "st_mode", stat.S_IFLNK | 0o777),
            (self.target.parent, "st_mode", stat.S_IFDIR | 0o777),
            (self.target.parent, "st_mode", stat.S_IFLNK | 0o777),
            (self.home, "st_mode", stat.S_IFLNK | 0o777),
            (self.home / ".local", "st_uid", 65534),
        )
        for path, field, value in mutations:
            with self.subTest(path=path, field=field, value=value):
                old = getattr(self.metadata[path], field)
                setattr(self.metadata[path], field, value)
                self.assertIsNone(self.runner.resolve_tool("pre-commit", ROOT))
                setattr(self.metadata[path], field, old)

    def test_entrypoint_rejects_escape_and_arbitrary_install_targets(self):
        for target in (
            "/tmp/pre-commit",
            str(ROOT / "pre-commit"),
            str(self.home / "other/pre-commit"),
        ):
            with (
                self.subTest(target=target),
                mock.patch.object(self.runner.os, "readlink", return_value=target),
            ):
                self.assertIsNone(self.runner.resolve_tool("pre-commit", ROOT))
        self.assertIsNone(self.runner.resolve_tool("pre-commit", self.home))

    def test_entrypoint_must_be_executable(self):
        with mock.patch.object(self.runner.os, "access", return_value=False):
            self.assertIsNone(self.runner.resolve_tool("pre-commit", ROOT))


if __name__ == "__main__":
    unittest.main()
