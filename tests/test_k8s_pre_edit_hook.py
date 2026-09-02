"""Path-resolution and trust-boundary regressions for the pre-edit guard.

The guard runs at PreToolUse for Write|Edit|MultiEdit. It must accept any path
inside this repository, including any of its linked worktrees, reject every
path outside it, and never run an executable selected by tool input.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK_PATH = ROOT / "docs/00.agent-governance/hooks/k8s-pre-edit.sh"
SELECTOR_RELATIVE_PATH = "scripts/select-affected-surfaces.py"
SAMPLE_DOCUMENT = "docs/01.requirements/README.md"


def run_hook(payload: str, project_dir: Path, environment: dict | None = None):
    """Invoke the production hook with one raw JSON payload on stdin."""
    env = dict(os.environ)
    env["CLAUDE_PROJECT_DIR"] = str(project_dir)
    if environment:
        env.update(environment)
    return subprocess.run(
        ("bash", str(HOOK_PATH)),
        input=payload,
        capture_output=True,
        text=True,
        env=env,
        timeout=300,
    )


def scalar_payload(path: str) -> str:
    return '{"tool_input":{"file_path":%s}}' % _json_string(path)


def collection_payload(paths: tuple[str, ...]) -> str:
    joined = ",".join(_json_string(path) for path in paths)
    return '{"tool_input":{"files":[%s]}}' % joined


def _json_string(value: str) -> str:
    import json

    return json.dumps(value)


def repository_worktrees() -> tuple[Path, ...]:
    """Return every linked worktree of this repository, excluding the main one."""
    completed = subprocess.run(
        ("git", "-C", str(ROOT), "worktree", "list", "--porcelain"),
        capture_output=True,
        text=True,
        check=True,
    )
    roots = [
        Path(line.split(" ", 1)[1])
        for line in completed.stdout.splitlines()
        if line.startswith("worktree ")
    ]
    main_root = roots[0] if roots else ROOT
    return tuple(root for root in roots[1:] if root != main_root)


def main_checkout() -> Path:
    completed = subprocess.run(
        ("git", "-C", str(ROOT), "worktree", "list", "--porcelain"),
        capture_output=True,
        text=True,
        check=True,
    )
    for line in completed.stdout.splitlines():
        if line.startswith("worktree "):
            return Path(line.split(" ", 1)[1])
    return ROOT


class PreEditAcceptanceTest(unittest.TestCase):
    """Paths inside this repository are accepted and resolved to their own root."""

    def test_repository_relative_path_is_accepted(self):
        result = run_hook(scalar_payload(SAMPLE_DOCUMENT), ROOT)

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_absolute_path_in_project_dir_is_accepted(self):
        result = run_hook(scalar_payload(str(ROOT / SAMPLE_DOCUMENT)), ROOT)

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_path_in_a_linked_worktree_is_accepted(self):
        worktrees = repository_worktrees()
        if not worktrees:
            self.skipTest("repository has no linked worktree to exercise")
        worktree = worktrees[0]

        result = run_hook(
            scalar_payload(str(worktree / SAMPLE_DOCUMENT)), main_checkout()
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_worktree_path_resolves_against_its_own_root(self):
        """A worktree path must not survive as `.worktrees/<name>/...`.

        Linked worktrees may live under the main checkout, so a plain prefix
        strip yields a path relative to the wrong tree.
        """
        worktrees = repository_worktrees()
        if not worktrees:
            self.skipTest("repository has no linked worktree to exercise")
        worktree = worktrees[0]

        result = run_hook(
            scalar_payload(str(worktree / SAMPLE_DOCUMENT)), main_checkout()
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"`{SAMPLE_DOCUMENT}`", result.stdout)
        self.assertNotIn(".worktrees/", result.stdout)

    def test_not_yet_existing_deep_path_is_accepted(self):
        """`Write` creates files, so resolution cannot require the path to exist."""
        target = ROOT / "docs/03.specs/9999-not-created-yet/spec.md"
        self.assertFalse(target.exists())

        result = run_hook(scalar_payload(str(target)), ROOT)

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_terminal_requirement_route_is_selected_from_registry(self):
        target = "docs/01.requirements/9999-example-feature.md"

        result = run_hook(scalar_payload(target), ROOT)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("`sdlc/requirement`", result.stdout)
        self.assertIn(
            "`docs/99.templates/templates/requirements/requirement-package.template.md`",
            result.stdout,
        )

    def test_terminal_spec_task_route_is_selected_from_registry(self):
        target = "docs/03.specs/9999-example-feature/tasks/tsk-0001-implement.md"

        result = run_hook(scalar_payload(target), ROOT)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("`sdlc/task`", result.stdout)
        self.assertIn(
            "`docs/99.templates/templates/specs/task.template.md`",
            result.stdout,
        )


class PreEditRejectionTest(unittest.TestCase):
    """Every path outside this repository fails closed with its own code."""

    def assert_rejected(self, payload: str, code: str, project_dir: Path = ROOT):
        result = run_hook(payload, project_dir)

        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn(code, result.stderr)

    def test_system_path_outside_the_repository_is_rejected(self):
        self.assert_rejected(scalar_payload("/etc/passwd"), "HOOK-PATH-ROOT")

    def test_temporary_path_outside_the_repository_is_rejected(self):
        self.assert_rejected(scalar_payload("/tmp/evil.md"), "HOOK-PATH-ROOT")

    def test_credential_path_outside_the_repository_is_rejected(self):
        home = Path(os.path.expanduser("~"))
        self.assert_rejected(
            scalar_payload(str(home / ".ssh/config")), "HOOK-PATH-ROOT"
        )

    def test_sibling_directory_of_another_repository_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            other = Path(directory) / "other-repository"
            other.mkdir()
            subprocess.run(
                ("git", "-C", str(other), "init", "--quiet"),
                check=True,
                capture_output=True,
            )
            target = other / "docs/x.md"

            self.assert_rejected(scalar_payload(str(target)), "HOOK-PATH-ROOT")

    def test_traversal_payload_is_rejected(self):
        self.assert_rejected(
            scalar_payload(f"{ROOT}/docs/../../../etc/passwd"),
            "HOOK-PATH-NORMALIZATION",
        )

    def test_symlinked_component_is_rejected(self):
        symlinked = ROOT / ".claude/skills"
        if not symlinked.is_symlink():
            self.skipTest("no symlinked component available to exercise")

        self.assert_rejected(
            scalar_payload(str(symlinked / "probe.md")), "HOOK-PATH-SYMLINK"
        )

    def test_payload_mixing_two_repository_roots_is_rejected(self):
        worktrees = repository_worktrees()
        if not worktrees:
            self.skipTest("repository has no linked worktree to exercise")

        payload = collection_payload(
            (
                str(worktrees[0] / SAMPLE_DOCUMENT),
                str(main_checkout() / SAMPLE_DOCUMENT),
            )
        )

        self.assert_rejected(payload, "HOOK-PATH-ROOT", project_dir=main_checkout())

    def test_every_retired_standalone_form_is_rejected_with_terminal_owner(self):
        cases = (
            ("docs/01.requirements/prd-example-feature.md", "sdlc/requirement"),
            ("docs/01.requirements/srs-example-feature.md", "sdlc/requirement"),
            ("docs/01.requirements/ifc-example-feature.md", "sdlc/requirement"),
            (
                "docs/01.requirements/interface-example-feature.md",
                "sdlc/requirement",
            ),
            ("docs/03.specs/9999-example-feature/design.md", "sdlc/spec"),
            ("docs/03.specs/9999-example-feature/tests.md", "sdlc/spec"),
            ("docs/03.specs/9999-example-feature/agent-design.md", "sdlc/spec"),
            ("docs/03.specs/9999-example-feature/tasks.md", "sdlc/task"),
        )
        for path, owner in cases:
            with self.subTest(path=path):
                result = run_hook(scalar_payload(path), ROOT)
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertIn("HOOK-DOC-RETIRED", result.stderr)
                self.assertIn(owner, result.stderr)

    def test_registry_template_parent_symlink_is_rejected(self):
        import json

        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "repository"
            outside = Path(directory) / "outside"
            registry_dir = project / "docs/99.templates"
            outside.mkdir()
            registry_dir.mkdir(parents=True)
            (outside / "requirement-package.template.md").write_text(
                "# escaped\n", encoding="utf-8"
            )
            (registry_dir / "templates").symlink_to(outside, target_is_directory=True)
            (registry_dir / "registry.json").write_text(
                json.dumps(
                    {
                        "profiles": [
                            {
                                "id": "sdlc/requirement",
                                "pathPattern": (
                                    r"^docs/01\.requirements/[0-9]{4}-[a-z-]+\.md$"
                                ),
                                "template": (
                                    "docs/99.templates/templates/"
                                    "requirement-package.template.md"
                                ),
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            result = run_hook(
                scalar_payload("docs/01.requirements/9999-example-feature.md"),
                project,
            )

        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("HOOK-DOC-TEMPLATE", result.stderr)
        self.assertIn("symlink component", result.stderr)

    def test_registry_parent_symlink_is_rejected(self):
        import json

        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "repository"
            outside = Path(directory) / "outside"
            (project / "docs").mkdir(parents=True)
            outside.mkdir()
            (outside / "registry.json").write_text(
                json.dumps({"profiles": []}), encoding="utf-8"
            )
            (project / "docs/99.templates").symlink_to(
                outside, target_is_directory=True
            )

            result = run_hook(
                scalar_payload("docs/01.requirements/9999-example-feature.md"),
                project,
            )

        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("HOOK-DOC-REGISTRY", result.stderr)
        self.assertIn("symlink component", result.stderr)


class PreEditGitDegradationTest(unittest.TestCase):
    """A failed, missing, or hung git falls back to the fail-closed prefix rule."""

    def failing_git_environment(self, directory: str) -> dict:
        shim = Path(directory) / "git"
        shim.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        shim.chmod(0o755)
        return {"PATH": f"{directory}{os.pathsep}{os.environ['PATH']}"}

    def test_outside_path_is_still_rejected_when_git_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            result = run_hook(
                scalar_payload("/etc/passwd"),
                ROOT,
                self.failing_git_environment(directory),
            )

        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("HOOK-PATH-ROOT", result.stderr)

    def test_project_dir_path_still_resolves_when_git_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            result = run_hook(
                scalar_payload(str(ROOT / SAMPLE_DOCUMENT)),
                ROOT,
                self.failing_git_environment(directory),
            )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_git_probes_are_bounded_by_an_explicit_timeout(self):
        hook_text = HOOK_PATH.read_text(encoding="utf-8")

        self.assertIn("GIT_TIMEOUT_SECONDS", hook_text)
        self.assertIn("timeout=GIT_TIMEOUT_SECONDS", hook_text)

    def test_git_results_are_memoized(self):
        hook_text = HOOK_PATH.read_text(encoding="utf-8")

        self.assertIn("_git_cache", hook_text)


class PreEditTrustBoundaryTest(unittest.TestCase):
    """A root derived from tool input selects data only, never an executable."""

    def test_selector_executable_is_pinned_to_project_dir(self):
        hook_text = HOOK_PATH.read_text(encoding="utf-8")

        self.assertIn(f'python3 "$PROJECT_DIR/{SELECTOR_RELATIVE_PATH}"', hook_text)
        self.assertNotIn(f'"$RESOLVED_ROOT/{SELECTOR_RELATIVE_PATH}"', hook_text)

    def test_no_executable_is_selected_by_the_resolved_root(self):
        for line in HOOK_PATH.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or "$RESOLVED_ROOT" not in stripped:
                continue
            self.assertNotIn(
                "$RESOLVED_ROOT/",
                stripped.replace('--root "$RESOLVED_ROOT"', ""),
                f"tool-derived root selects a program: {stripped}",
            )

    def test_resolved_root_reaches_the_selector_as_data(self):
        hook_text = HOOK_PATH.read_text(encoding="utf-8")

        self.assertIn('--root "$RESOLVED_ROOT"', hook_text)

    def test_worktree_edit_does_not_run_that_worktrees_selector(self):
        """Substituting the worktree's selector must not change the outcome."""
        worktrees = repository_worktrees()
        if not worktrees:
            self.skipTest("repository has no linked worktree to exercise")
        worktree = worktrees[0]
        selector = worktree / SELECTOR_RELATIVE_PATH
        if not selector.is_file():
            self.skipTest("worktree has no selector copy to substitute")

        original = selector.read_bytes()
        try:
            selector.write_text(
                "#!/usr/bin/env python3\nimport sys\nsys.exit(3)\n", encoding="utf-8"
            )
            result = run_hook(
                scalar_payload(str(worktree / SAMPLE_DOCUMENT)), main_checkout()
            )
        finally:
            selector.write_bytes(original)

        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
