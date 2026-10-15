"""Synthetic contract tests for the local Git hook dispatcher."""

from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


DISPATCHER = Path(__file__).resolve().parents[1] / "scripts/githooks/chained-hook.sh"


class ChainedGitHooksTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="chained-hook-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo with 한글"
        self.repo.mkdir()
        self.global_dir = self.root / "global hooks"
        self.global_dir.mkdir()
        self.config = self.root / "synthetic-global.gitconfig"
        self.log = self.root / "hook-log"
        self.env = {
            "PATH": os.environ["PATH"],
            "HOME": str(self.root),
            "GIT_CONFIG_GLOBAL": str(self.config),
            "GIT_CONFIG_NOSYSTEM": "1",
            "HOOK_TEST_LOG": str(self.log),
        }
        subprocess.run(
            ("git", "init", "--quiet", str(self.repo)),
            env=self.env,
            check=True,
            capture_output=True,
        )
        self.workspace_dir = self.repo / ".git/hooks"

    def set_global_path(self, path: Path) -> None:
        self.config.write_text(f"[core]\n\thooksPath = {path}\n", encoding="utf-8")

    def make_hook(self, path: Path, label: str, *, status: int = 0) -> None:
        path.write_text(
            "#!/usr/bin/env python3\n"
            "import json, os, pathlib, sys\n"
            "pathlib.Path(os.environ['HOOK_TEST_LOG']).open('a', encoding='utf-8').write("
            f"json.dumps({{'label': {label!r}, 'args': sys.argv[1:], "
            "'cwd': os.getcwd(), 'index': os.environ.get('GIT_INDEX_FILE'), "
            "'stdin': sys.stdin.read()}, ensure_ascii=False) + '\\n')\n"
            f"sys.exit({status})\n",
            encoding="utf-8",
        )
        path.chmod(0o755)

    def run_chain(
        self, hook: str, *args: str, input_text: str = ""
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ("bash", str(DISPATCHER), hook, *args),
            cwd=self.repo,
            env={**self.env, "GIT_INDEX_FILE": str(self.root / "synthetic-index")},
            input=input_text,
            capture_output=True,
            text=True,
            timeout=5,
        )

    def records(self) -> list[dict]:
        if not self.log.exists():
            return []
        return [
            json.loads(line)
            for line in self.log.read_text(encoding="utf-8").splitlines()
        ]

    def test_missing_selected_workspace_hook_fails(self) -> None:
        for hook in ("pre-commit", "commit-msg"):
            with self.subTest(hook=hook):
                result = self.run_chain(hook)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(hook, result.stderr)
                self.assertIn("workspace", result.stderr)

    def test_pre_push_absence_is_optional(self) -> None:
        result = self.run_chain(
            "pre-push", input_text="refs/heads/main aaa refs/heads/main bbb\n"
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unset_global_path_runs_workspace_hook(self) -> None:
        self.make_hook(self.workspace_dir / "pre-commit", "workspace")
        result = self.run_chain("pre-commit")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([record["label"] for record in self.records()], ["workspace"])

    def test_global_config_read_error_is_not_treated_as_unset(self) -> None:
        self.make_hook(self.workspace_dir / "pre-commit", "workspace")
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        git = bin_dir / "git"
        git.write_text(
            "#!/bin/sh\n"
            'if [ "$1" = config ] && [ "$2" = --global ]; then\n'
            "  echo 'synthetic config failure' >&2\n"
            "  exit 7\n"
            "fi\n"
            f'exec {shlex.quote(shutil.which("git") or "/usr/bin/git")} "$@"\n',
            encoding="utf-8",
        )
        git.chmod(0o755)
        self.env["PATH"] = str(bin_dir) + os.pathsep + self.env["PATH"]
        result = self.run_chain("pre-commit")
        self.assertEqual(result.returncode, 7, result.stderr)
        self.assertIn("HOOK-CONFIG", result.stderr)
        self.assertEqual(self.records(), [])

    def test_malformed_global_config_fails_without_skipping_workspace(self) -> None:
        self.make_hook(self.workspace_dir / "pre-commit", "workspace")
        self.config.write_text("[core\n", encoding="utf-8")
        result = self.run_chain("pre-commit")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("global", result.stderr)
        self.assertEqual(self.records(), [])

    def test_configured_global_dir_missing_fails(self) -> None:
        self.make_hook(self.workspace_dir / "pre-commit", "workspace")
        self.set_global_path(self.root / "missing-global-dir")
        result = self.run_chain("pre-commit")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.records(), [])

    def test_existing_nonexecutable_or_broken_global_hook_fails(self) -> None:
        self.make_hook(self.workspace_dir / "pre-commit", "workspace")
        self.set_global_path(self.global_dir)
        hook = self.global_dir / "pre-commit"
        for setup in ("nonexec", "broken-link"):
            with self.subTest(setup=setup):
                if hook.exists() or hook.is_symlink():
                    hook.unlink()
                if setup == "nonexec":
                    hook.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
                else:
                    hook.symlink_to(self.root / "missing-target")
                result = self.run_chain("pre-commit")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("global", result.stderr)
                self.assertEqual(self.records(), [])

    def test_canonical_duplicate_executes_once(self) -> None:
        self.make_hook(self.workspace_dir / "pre-commit", "workspace")
        self.global_dir.rmdir()
        self.global_dir.symlink_to(self.workspace_dir, target_is_directory=True)
        self.set_global_path(self.global_dir)
        result = self.run_chain("pre-commit")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([record["label"] for record in self.records()], ["workspace"])

    def test_recursive_adapter_fails_without_running_workspace_hook(self) -> None:
        self.set_global_path(self.global_dir)
        self.make_hook(self.workspace_dir / "pre-commit", "workspace")
        adapter = self.global_dir / "pre-commit"
        adapter.write_text(
            f'#!/bin/sh\nexec bash {DISPATCHER} pre-commit "$@"\n',
            encoding="utf-8",
        )
        adapter.chmod(0o755)
        result = self.run_chain("pre-commit")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("recurs", result.stderr.lower())
        self.assertEqual(self.records(), [])

    def test_push_payload_context_order_and_first_failure(self) -> None:
        self.set_global_path(self.global_dir)
        self.make_hook(self.global_dir / "pre-push", "global")
        self.make_hook(self.workspace_dir / "pre-push", "workspace")
        refs = (
            "refs/heads/main aaa refs/heads/main bbb\n"
            "refs/heads/new ccc refs/heads/new 000000\n"
            "(delete) 000000 refs/heads/old ddd\n"
        )
        result = self.run_chain(
            "pre-push", "origin", "file:///synthetic", input_text=refs
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        records = self.records()
        self.assertEqual(
            [record["label"] for record in records], ["global", "workspace"]
        )
        for record in records:
            self.assertEqual(record["args"], ["origin", "file:///synthetic"])
            self.assertEqual(record["cwd"], str(self.repo))
            self.assertEqual(record["index"], str(self.root / "synthetic-index"))
            self.assertEqual(record["stdin"], refs)

        self.log.unlink()
        self.make_hook(self.global_dir / "pre-push", "global", status=17)
        result = self.run_chain("pre-push", input_text=refs)
        self.assertEqual(result.returncode, 17, result.stderr)
        self.assertEqual([record["label"] for record in self.records()], ["global"])


if __name__ == "__main__":
    unittest.main()
