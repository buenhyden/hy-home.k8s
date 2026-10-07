"""Boundaries for the local selected non-style pre-commit projection."""

from __future__ import annotations

import importlib.util
import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate-selected-nonstyle.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("selected_nonstyle", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("selected non-style checker is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SelectedNonstyleContractTests(unittest.TestCase):
    def test_worktree_diff_probe_preserves_private_index_bytes(self) -> None:
        checker = load_checker()
        with tempfile.TemporaryDirectory(prefix="nonstyle-index-probe-") as temporary:
            root = Path(temporary)

            def git(*args: str) -> None:
                subprocess.run(
                    ["git", *args], cwd=root, check=True, capture_output=True
                )

            git("init", "-q")
            git("config", "user.name", "Fixture")
            git("config", "user.email", "fixture@example.invalid")
            target = root / "file.txt"
            target.write_text("same\n", encoding="utf-8")
            git("add", "file.txt")
            git("commit", "-qm", "fixture")
            metadata = target.stat()
            os.utime(
                target,
                ns=(metadata.st_atime_ns, metadata.st_mtime_ns + 2_000_000_000),
            )
            baseline = (root / ".git/index").read_bytes()
            self.assertEqual(checker._worktree_diff(root), b"")
            self.assertEqual((root / ".git/index").read_bytes(), baseline)
            target.write_text("changed\n", encoding="utf-8")
            self.assertIn(b"file.txt", checker._worktree_diff(root))
            self.assertEqual((root / ".git/index").read_bytes(), baseline)

    def test_clean_selected_index_file_passes_without_whole_sweep(self) -> None:
        checker = load_checker()
        with tempfile.TemporaryDirectory(
            prefix="selected-nonstyle-clean-"
        ) as temporary:
            root = Path(temporary)
            env = {
                **os.environ,
                "GIT_AUTHOR_NAME": "Fixture",
                "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                "GIT_COMMITTER_NAME": "Fixture",
                "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
            }

            def git(*args: str) -> None:
                subprocess.run(
                    ["git", *args], cwd=root, env=env, check=True, capture_output=True
                )

            git("init", "-q")
            for name in (
                ".pre-commit-config.yaml",
                ".gitleaks.toml",
                ".secrets.baseline",
                ".kube-linter.yaml",
            ):
                (root / name).write_bytes((ROOT / name).read_bytes())
            (root / "proof.txt").write_text("first\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "fixture")
            (root / "proof.txt").write_text("second\n", encoding="utf-8")
            git("add", "proof.txt")
            metadata = (root / "proof.txt").stat()
            os.utime(
                root / "proof.txt",
                ns=(metadata.st_atime_ns, metadata.st_mtime_ns + 2_000_000_000),
            )
            index_before = (root / ".git/index").read_bytes()
            cache = Path.home() / ".cache/pre-commit"
            if not cache.is_dir():
                self.skipTest("pre-commit cache unavailable")
            previous = os.environ.get("PRE_COMMIT_HOME")
            real_run = checker.run
            hook_environments: list[dict[str, str]] = []

            def observed_run(argv, **kwargs):
                if "pre_commit" in argv:
                    hook_environments.append(kwargs["env"])
                return real_run(argv, **kwargs)

            try:
                os.environ["PRE_COMMIT_HOME"] = str(cache)
                stderr = io.StringIO()
                with (
                    contextlib.redirect_stderr(stderr),
                    patch.object(checker, "run", side_effect=observed_run),
                ):
                    result = checker.main(
                        [
                            "--root",
                            str(root),
                            "--config",
                            str(root / ".pre-commit-config.yaml"),
                            "--include-path",
                            "proof.txt",
                        ]
                    )
            finally:
                if previous is None:
                    os.environ.pop("PRE_COMMIT_HOME", None)
                else:
                    os.environ["PRE_COMMIT_HOME"] = previous
            self.assertEqual(result, 0, stderr.getvalue())
            self.assertEqual((root / ".git/index").read_bytes(), index_before)
            self.assertEqual(len(hook_environments), 1)
            hook_env = hook_environments[0]
            self.assertEqual(hook_env["GIT_OPTIONAL_LOCKS"], "0")
            self.assertEqual(hook_env["PRE_COMMIT_HOME"], str(cache))
            for variable in (
                "CARGO_HOME",
                "GOCACHE",
                "GOPATH",
                "XDG_CACHE_HOME",
                "npm_config_cache",
            ):
                with self.subTest(variable=variable):
                    self.assertTrue(Path(hook_env[variable]).is_relative_to(cache))
                    self.assertTrue(Path(hook_env[variable]).is_dir())

            def alter_disposable_index(argv, **kwargs):
                result = real_run(argv, **kwargs)
                if "pre_commit" in argv:
                    subprocess.run(
                        [
                            "git",
                            "update-index",
                            "--assume-unchanged",
                            "--",
                            "proof.txt",
                        ],
                        cwd=root,
                        env=kwargs["env"],
                        check=True,
                        capture_output=True,
                    )
                return result

            with (
                contextlib.redirect_stderr(stderr := io.StringIO()),
                patch.object(checker, "run", side_effect=alter_disposable_index),
                patch.dict(os.environ, {"PRE_COMMIT_HOME": str(cache)}),
            ):
                self.assertEqual(
                    checker.main(
                        [
                            "--root",
                            str(root),
                            "--config",
                            str(root / ".pre-commit-config.yaml"),
                            "--include-path",
                            "proof.txt",
                        ]
                    ),
                    2,
                )
            self.assertIn("NONSTYLE-MUTATION", stderr.getvalue())
            self.assertEqual((root / ".git/index").read_bytes(), index_before)
            (root / "proof.txt").write_text("unstaged concealment\n", encoding="utf-8")
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                rejected = checker.main(
                    [
                        "--root",
                        str(root),
                        "--config",
                        str(root / ".pre-commit-config.yaml"),
                        "--include-path",
                        "proof.txt",
                    ]
                )
            self.assertEqual(rejected, 2)
            self.assertIn("NONSTYLE-INDEX", stderr.getvalue())

    def test_staged_synthetic_secret_uses_reviewed_head_config(self) -> None:
        checker = load_checker()
        with tempfile.TemporaryDirectory(
            prefix="selected-nonstyle-secret-"
        ) as temporary:
            root = Path(temporary)
            env = {
                **os.environ,
                "GIT_AUTHOR_NAME": "Fixture",
                "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                "GIT_COMMITTER_NAME": "Fixture",
                "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
            }

            def git(*args: str) -> None:
                subprocess.run(
                    ["git", *args], cwd=root, env=env, check=True, capture_output=True
                )

            git("init", "-q")
            for name in (
                ".pre-commit-config.yaml",
                ".secrets.baseline",
                ".kube-linter.yaml",
            ):
                (root / name).write_bytes((ROOT / name).read_bytes())
            (root / ".gitleaks.toml").write_text(
                '[[rules]]\nid = "synthetic-marker"\nregex = "SYNTHETIC_LEAK_MARKER"\n',
                encoding="utf-8",
            )
            git("add", ".")
            git("commit", "-qm", "fixture")
            (root / ".hidden.txt").write_text(
                "SYNTHETIC_LEAK_MARKER\n", encoding="utf-8"
            )
            (root / ".gitleaks.toml").write_text("[allowlist]\n", encoding="utf-8")
            git("add", ".hidden.txt", ".gitleaks.toml")
            cache = Path.home() / ".cache/pre-commit"
            if not cache.is_dir():
                self.skipTest("pre-commit cache unavailable")
            previous = os.environ.get("PRE_COMMIT_HOME")
            try:
                os.environ["PRE_COMMIT_HOME"] = str(cache)
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    result = checker.main(
                        [
                            "--root",
                            str(root),
                            "--config",
                            str(root / ".pre-commit-config.yaml"),
                            "--include-path",
                            ".hidden.txt",
                            "--include-path",
                            ".gitleaks.toml",
                        ]
                    )
            finally:
                if previous is None:
                    os.environ.pop("PRE_COMMIT_HOME", None)
                else:
                    os.environ["PRE_COMMIT_HOME"] = previous
            self.assertEqual(result, 2)
            self.assertIn("NONSTYLE-HOOK-FAIL", stderr.getvalue())

    def test_staged_broken_symlink_is_checked_in_full_index_topology(self) -> None:
        checker = load_checker()
        with tempfile.TemporaryDirectory(prefix="selected-nonstyle-") as temporary:
            root = Path(temporary)

            def git(*args: str) -> None:
                subprocess.run(
                    ["git", *args],
                    cwd=root,
                    check=True,
                    capture_output=True,
                    env={
                        **os.environ,
                        "GIT_AUTHOR_NAME": "Fixture",
                        "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                        "GIT_COMMITTER_NAME": "Fixture",
                        "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
                    },
                )

            git("init", "-q")
            for name in (
                ".pre-commit-config.yaml",
                ".gitleaks.toml",
                ".secrets.baseline",
                ".kube-linter.yaml",
            ):
                (root / name).write_bytes((ROOT / name).read_bytes())
            (root / "existing.txt").write_text("fixture\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "fixture")
            (root / "broken-link").symlink_to("missing-target")
            git("add", "broken-link")
            self.assertEqual(
                checker._selected_index_paths(root, ("broken-link",)),
                ["broken-link"],
            )
            cache = Path.home() / ".cache/pre-commit"
            if not cache.is_dir():
                self.skipTest("pre-commit cache unavailable")
            old = os.environ.get("PRE_COMMIT_HOME")
            try:
                os.environ["PRE_COMMIT_HOME"] = str(cache)
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    result = checker.main(
                        [
                            "--root",
                            str(root),
                            "--config",
                            str(root / ".pre-commit-config.yaml"),
                            "--include-path",
                            "broken-link",
                        ]
                    )
            finally:
                if old is None:
                    os.environ.pop("PRE_COMMIT_HOME", None)
                else:
                    os.environ["PRE_COMMIT_HOME"] = old
            self.assertEqual(result, 2)
            self.assertIn("NONSTYLE-HOOK-FAIL", stderr.getvalue())
            self.assertTrue((root / "broken-link").is_symlink())

    def test_projection_keeps_only_scoped_nonstyle_hooks(self) -> None:
        checker = load_checker()
        config = (ROOT / ".pre-commit-config.yaml").read_bytes()
        projected = checker.project_nonstyle(config)
        hooks = [hook for repo in projected["repos"] for hook in repo["hooks"]]
        self.assertEqual({hook["id"] for hook in hooks}, set(checker.NONSTYLE_IDS))
        self.assertNotIn("--all-files", yaml.safe_dump(projected))
        self.assertEqual(len([h for h in hooks if h["id"] == "gitleaks"]), 1)

    def test_unreviewed_or_whole_tree_hook_fails_closed(self) -> None:
        checker = load_checker()
        config = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text())
        manual_only = {**config, "default_stages": ["manual"]}
        with self.assertRaisesRegex(checker.NonstyleError, "pre-commit default stage"):
            checker.project_nonstyle(yaml.safe_dump(manual_only).encode())
        config["repos"][-1]["hooks"].append({"id": "unreviewed-hook"})
        with self.assertRaises(checker.NonstyleError):
            checker.project_nonstyle(yaml.safe_dump(config).encode())
        config["repos"][-1]["hooks"].pop()
        normal = next(
            h
            for r in config["repos"]
            for h in r["hooks"]
            if h["id"] == "gitleaks" and h.get("alias") is None
        )
        normal["pass_filenames"] = False
        normal["entry"] = "gitleaks dir ."
        with self.assertRaises(checker.NonstyleError):
            checker.project_nonstyle(yaml.safe_dump(config).encode())


if __name__ == "__main__":
    unittest.main()
