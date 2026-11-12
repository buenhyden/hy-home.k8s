"""Synthetic contract tests for the local Git hook dispatcher."""

from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
import sys
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
        self.venv = self.make_venv(self.root / "검증 env")
        self.venv_setting: str | None = str(self.venv)
        self.global_hooks: Path | None = None
        self.write_config()

    def make_venv(self, path: Path) -> Path:
        site = path / "lib/python3/site-packages"
        site.mkdir(parents=True)
        (path / "bin").mkdir()
        (site / "marker.py").write_text("", encoding="utf-8")
        (path / "pyvenv.cfg").write_text("home = /usr/bin\n", encoding="utf-8")
        (path / "bin/python3").symlink_to(sys.executable)
        stub = path / "bin/pre-commit"
        stub.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        stub.chmod(0o755)
        for directory in (path, path / "bin", path / "lib", site.parent, site):
            directory.chmod(0o755)
        for file in (site / "marker.py", path / "pyvenv.cfg"):
            file.chmod(0o644)
        return path

    def write_config(self) -> None:
        lines = []
        if self.global_hooks is not None:
            lines += ["[core]", f"\thooksPath = {self.global_hooks}"]
        if self.venv_setting is not None:
            lines += ["[hyhome]", f"\tvalidationVenv = {self.venv_setting}"]
        self.config.write_text(
            "\n".join(lines) + "\n" if lines else "", encoding="utf-8"
        )

    def set_global_path(self, path: Path) -> None:
        self.global_hooks = path
        self.write_config()

    def shim(self, name: str, body: str) -> None:
        bin_dir = self.root / "shims"
        bin_dir.mkdir(exist_ok=True)
        tool = bin_dir / name
        tool.write_text(body, encoding="utf-8")
        tool.chmod(0o755)
        self.env["PATH"] = str(bin_dir) + os.pathsep + self.env["PATH"]

    def assert_env_refused(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("HOOK-ENV", result.stderr)
        self.assertIn("hyhome.validationVenv", result.stderr)
        self.assertEqual(self.records(), [])

    def make_hook(self, path: Path, label: str, *, status: int = 0) -> None:
        path.write_text(
            "#!/usr/bin/env python3\n"
            "import json, os, pathlib, sys\n"
            "pathlib.Path(os.environ['HOOK_TEST_LOG']).open('a', encoding='utf-8').write("
            f"json.dumps({{'label': {label!r}, 'args': sys.argv[1:], "
            "'cwd': os.getcwd(), 'index': os.environ.get('GIT_INDEX_FILE'), "
            "'path': os.environ.get('PATH'), "
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

    def test_only_the_workspace_hook_gets_the_validation_environment(self) -> None:
        self.set_global_path(self.global_dir)
        for hook in ("pre-commit", "commit-msg"):
            with self.subTest(hook=hook):
                if self.log.exists():
                    self.log.unlink()
                self.make_hook(self.global_dir / hook, "global")
                self.make_hook(self.workspace_dir / hook, "workspace")
                result = self.run_chain(hook)
                self.assertEqual(result.returncode, 0, result.stderr)
                paths = {item["label"]: item["path"] for item in self.records()}
                self.assertEqual(paths["global"], self.env["PATH"])
                self.assertEqual(
                    paths["workspace"],
                    f"{os.path.realpath(self.venv)}/bin{os.pathsep}{self.env['PATH']}",
                )

    def test_unusable_environment_blocks_before_any_hook(self) -> None:
        self.set_global_path(self.global_dir)
        self.make_hook(self.global_dir / "pre-commit", "global")
        self.make_hook(self.workspace_dir / "pre-commit", "workspace")
        cases: dict[str, str | None] = {
            "unset": None,
            "empty": "",
            "relative": "relative/env",
            "missing": str(self.root / "absent"),
            "inside checkout": str(self.make_venv(self.repo / "env")),
        }
        git_env = {
            **self.env,
            "GIT_AUTHOR_NAME": "t",
            "GIT_AUTHOR_EMAIL": "t@example.invalid",
            "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": "t@example.invalid",
        }
        for argv in (
            ("git", "-C", str(self.repo), "commit", "-q", "--allow-empty", "-m", "x"),
            (
                "git",
                "-C",
                str(self.repo),
                "worktree",
                "add",
                "--detach",
                "-q",
                str(self.root / "other tree"),
            ),
        ):
            subprocess.run(argv, env=git_env, check=True, capture_output=True)
        if self.log.exists():  # the setup commit ran the synthetic hooks
            self.log.unlink()
        cases["inside another worktree"] = str(
            self.make_venv(self.root / "other tree/env")
        )

        def broken(name: str, change) -> str:
            path = self.make_venv(self.root / "cases" / name)
            change(path)
            return str(path)

        cases["no python3"] = broken("a", lambda v: (v / "bin/python3").unlink())
        cases["no pre-commit"] = broken("b", lambda v: (v / "bin/pre-commit").unlink())
        cases["group-writable directory"] = broken("c", lambda v: v.chmod(0o775))
        cases["other-writable bin"] = broken("d", lambda v: (v / "bin").chmod(0o757))
        cases["group-writable pre-commit"] = broken(
            "e", lambda v: (v / "bin/pre-commit").chmod(0o775)
        )
        cases["group-writable site-packages file"] = broken(
            "f", lambda v: (v / "lib/python3/site-packages/marker.py").chmod(0o664)
        )

        def umask_002(path: Path) -> None:
            for item in path.rglob("*"):
                if not item.is_symlink():
                    item.chmod(
                        0o775 if item.is_dir() or os.access(item, os.X_OK) else 0o664
                    )
            path.chmod(0o775)

        cases["built under umask 002"] = broken("g", umask_002)
        for name, value in cases.items():
            with self.subTest(case=name):
                self.venv_setting = value
                self.write_config()
                self.assert_env_refused(self.run_chain("pre-commit"))

    def test_foreign_owner_is_refused(self) -> None:
        self.make_hook(self.workspace_dir / "pre-commit", "workspace")
        real = shutil.which("find") or "/usr/bin/find"
        # Report the invoking account as some other uid, so every entry looks foreign.
        self.shim(
            "find",
            '#!/bin/sh\nme=$(id -u)\nfor a in "$@"; do shift; '
            '[ "$a" = "$me" ] && a=99999; set -- "$@" "$a"; done\n'
            f'exec {shlex.quote(real)} "$@"\n',
        )
        self.assert_env_refused(self.run_chain("pre-commit"))

    def test_accepted_environment_spellings(self) -> None:
        self.make_hook(self.workspace_dir / "pre-commit", "workspace")
        sibling = self.make_venv(Path(f"{self.repo}-venv"))
        link = self.root / "env link"
        link.symlink_to(self.venv, target_is_directory=True)
        for name, value, expected in (
            ("sibling sharing the checkout prefix", str(sibling), sibling),
            ("symbolic link", str(link), self.venv),
            ("home expansion", "~/검증 env", self.venv),
        ):
            with self.subTest(case=name):
                if self.log.exists():
                    self.log.unlink()
                self.venv_setting = value
                self.write_config()
                result = self.run_chain("pre-commit")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(
                    self.records()[0]["path"].startswith(
                        f"{os.path.realpath(expected)}/bin{os.pathsep}"
                    )
                )

    def test_environment_read_error_is_not_treated_as_unset(self) -> None:
        self.make_hook(self.workspace_dir / "pre-commit", "workspace")
        self.shim(
            "git",
            "#!/bin/sh\n"
            'case "$*" in *hyhome.validationVenv*) echo boom >&2; exit 7;; esac\n'
            f'exec {shlex.quote(shutil.which("git") or "/usr/bin/git")} "$@"\n',
        )
        result = self.run_chain("pre-commit")
        self.assertEqual(result.returncode, 7, result.stderr)
        self.assertIn("HOOK-CONFIG", result.stderr)
        self.assertEqual(self.records(), [])

    def test_pre_push_without_workspace_hook_needs_no_environment(self) -> None:
        self.venv_setting = None
        self.write_config()
        result = self.run_chain("pre-push", input_text="")
        self.assertEqual(result.returncode, 0, result.stderr)

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
