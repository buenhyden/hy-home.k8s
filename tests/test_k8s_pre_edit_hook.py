"""Path-resolution and trust-boundary regressions for the pre-edit guard.

The guard runs at PreToolUse on both providers: Bash|Write|Edit|MultiEdit on
Claude and Bash|apply_patch on Codex. It must accept any path inside this
repository, including any of its linked worktrees, reject every path outside
it, and never run an executable selected by tool input. Codex supplies no
`CLAUDE_PROJECT_DIR`, so the guard derives the root from Git instead.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK_PATH = ROOT / ".claude/hooks/k8s-pre-edit.sh"
GUARD_PATH = ROOT / "scripts/provider_write_guard.py"
CODEX_ADAPTER_PATH = ROOT / ".codex/hooks/pre-tool-use.sh"
CODEX_REGISTRATION_PATH = ROOT / ".codex/hooks.json"
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


def run_hook_without_project_dir(payload: str, cwd: Path):
    """Invoke the guard the way Codex does: no project variable, Git root only."""
    env = {
        key: value
        for key, value in os.environ.items()
        if key not in ("CLAUDE_PROJECT_DIR", "CLAUDE_TOOL_INPUT_FILE_PATH")
    }
    return subprocess.run(
        ("bash", str(HOOK_PATH)),
        input=payload,
        capture_output=True,
        text=True,
        env=env,
        cwd=str(cwd),
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

    def test_retired_governance_root_is_rejected(self):
        for path in (
            "docs/00.agent-governance/README.md",
            "docs/00.agent-governance/roles/registry.json",
        ):
            with self.subTest(path=path):
                result = run_hook(scalar_payload(path), ROOT)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("HOOK-PATH-RETIRED", result.stderr)
                self.assertIn(".agents/", result.stderr)

    def test_common_governance_path_is_accepted_without_qa(self):
        result = run_hook(scalar_payload(".agents/governance/quality.md"), ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("qa profile=", result.stdout + result.stderr)

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
        symlinked = ROOT / ".claude/skills/risk-report"
        self.assertTrue(symlinked.is_symlink())

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
                        "schema_version": 9,
                        "profiles": [
                            {
                                "id": "sdlc/requirement",
                                "path_pattern": (
                                    r"^docs/01\.requirements/[0-9]{4}-[a-z-]+\.md$"
                                ),
                                "template_source": (
                                    "docs/99.templates/templates/"
                                    "requirement-package.template.md"
                                ),
                            }
                        ],
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
        guard_text = GUARD_PATH.read_text(encoding="utf-8")

        self.assertIn("GIT_TIMEOUT_SECONDS", guard_text)
        self.assertIn("timeout=GIT_TIMEOUT_SECONDS", guard_text)

    def test_git_results_are_memoized(self):
        guard_text = GUARD_PATH.read_text(encoding="utf-8")

        self.assertIn("_git_cache", guard_text)


def patch_payload(body: str, argv_form: bool = False) -> str:
    """One apply_patch payload in either form the client may send."""
    command = ["apply_patch", body] if argv_form else body
    return json.dumps({"tool_name": "apply_patch", "tool_input": {"command": command}})


def envelope(*header_lines: str) -> str:
    return (
        "*** Begin Patch\n"
        + "".join(f"{line}\n" for line in header_lines)
        + "*** End Patch\n"
    )


class PatchEnvelopeTest(unittest.TestCase):
    """A patch write receives the checks a structured write already receives."""

    def assert_manifest_advisory(self, payload: str, path: str):
        result = run_hook(payload, ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Editing Kubernetes manifest", result.stdout)
        self.assertIn(path, result.stdout)

    def test_update_target_is_evaluated_in_the_string_form(self):
        self.assert_manifest_advisory(
            patch_payload(envelope("*** Update File: gitops/test.yaml")),
            "gitops/test.yaml",
        )

    def test_add_target_is_evaluated_in_the_argument_vector_form(self):
        self.assert_manifest_advisory(
            patch_payload(envelope("*** Add File: gitops/new.yaml"), argv_form=True),
            "gitops/new.yaml",
        )

    def test_delete_target_is_evaluated(self):
        self.assert_manifest_advisory(
            patch_payload(envelope("*** Delete File: gitops/old.yaml")),
            "gitops/old.yaml",
        )

    def test_a_move_yields_both_the_source_and_the_destination(self):
        result = run_hook(
            patch_payload(
                envelope(
                    "*** Update File: gitops/from.yaml",
                    "*** Move to: gitops/to.yaml",
                )
            ),
            ROOT,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("gitops/from.yaml", result.stdout)
        self.assertIn("gitops/to.yaml", result.stdout)

    def test_several_files_produce_one_evaluation_each(self):
        result = run_hook(
            patch_payload(
                envelope(
                    "*** Update File: gitops/one.yaml",
                    "*** Add File: gitops/two.yaml",
                )
            ),
            ROOT,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("Editing Kubernetes manifest"), 2)

    def test_an_envelope_naming_no_file_is_quiet_and_successful(self):
        result = run_hook(patch_payload(envelope()), ROOT)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "")

    def test_a_truncated_envelope_is_rejected_as_malformed_transport(self):
        result = run_hook(
            patch_payload("*** Begin Patch\n*** Update File: gitops/test.yaml\n"),
            ROOT,
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("HOOK-PATCH-ENVELOPE", result.stderr)

    def test_an_empty_target_path_is_rejected(self):
        result = run_hook(patch_payload(envelope("*** Add File:   ")), ROOT)

        self.assertEqual(result.returncode, 2)
        self.assertIn("HOOK-PATCH-PATH", result.stderr)

    def test_a_patch_body_resembling_a_command_yields_no_shell_target(self):
        result = run_hook(
            patch_payload(
                envelope("*** Update File: gitops/test.yaml").replace(
                    "*** End Patch", "+echo bad > gitops/injected.yaml\n*** End Patch"
                )
            ),
            ROOT,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("gitops/injected.yaml", result.stdout)
        self.assertNotIn("Shell command writes", result.stdout)

    def test_a_patch_target_outside_the_repository_is_rejected(self):
        result = run_hook(
            patch_payload(envelope("*** Add File: ../outside.yaml")), ROOT
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("HOOK-PATH-NORMALIZATION", result.stderr)

    def test_an_ordinary_shell_command_still_reaches_the_shell_observer(self):
        """Routing by shape must not disable the existing advisory path."""
        result = run_hook(
            json.dumps(
                {
                    "tool_name": "Bash",
                    "tool_input": {"command": "echo x > gitops/shell.yaml"},
                }
            ),
            ROOT,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Shell command writes", result.stdout)


class ProviderAdapterOwnershipTest(unittest.TestCase):
    """Neither provider directory may execute the other's program."""

    def test_the_codex_registration_names_no_claude_path(self):
        registration = json.loads(CODEX_REGISTRATION_PATH.read_text(encoding="utf-8"))
        commands = [
            handler.get("command", "")
            for entry in registration["hooks"]["PreToolUse"]
            for handler in entry["hooks"]
        ]

        self.assertTrue(commands, "the Codex registration must register a handler")
        for command in commands:
            self.assertNotIn(".claude/", command)
            self.assertIn(".codex/hooks/", command)

    def test_the_codex_adapter_exists_and_names_its_provider(self):
        self.assertTrue(
            CODEX_ADAPTER_PATH.is_file(), "the Codex adapter must be a real file"
        )
        adapter = CODEX_ADAPTER_PATH.read_text(encoding="utf-8")

        self.assertIn("--provider codex", adapter)
        self.assertIn("ADAPTER_DIR", adapter)
        self.assertNotIn(".claude/", adapter)

    def test_both_adapters_stay_thin(self):
        """An adapter names a provider and forwards; it holds no shared logic."""
        for adapter_path in (HOOK_PATH, CODEX_ADAPTER_PATH):
            body = [
                line.strip()
                for line in adapter_path.read_text(encoding="utf-8").splitlines()
                if line.strip() and not line.strip().startswith("#")
            ]

            self.assertLessEqual(
                len(body),
                8,
                f"{adapter_path.name} carries logic that belongs in the shared guard",
            )
            self.assertNotIn(
                "registry.json",
                "\n".join(body),
                f"{adapter_path.name} must not route documents itself",
            )


class PreEditTrustBoundaryTest(unittest.TestCase):
    """A root derived from tool input selects data only, never an executable."""

    def test_selector_executable_is_pinned_to_project_dir(self):
        guard_text = GUARD_PATH.read_text(encoding="utf-8")

        self.assertIn("os.path.join(project_dir, SELECTOR_RELATIVE_PATH)", guard_text)
        self.assertNotIn(
            "os.path.join(resolved_root, SELECTOR_RELATIVE_PATH)", guard_text
        )

    def test_no_executable_is_selected_by_the_resolved_root(self):
        """Every line naming the tool-derived root must use it as data."""
        seen = 0
        for line in GUARD_PATH.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or "resolved_root" not in stripped:
                continue
            seen += 1
            self.assertNotIn(
                "os.path.join(resolved_root",
                stripped,
                f"tool-derived root selects a program: {stripped}",
            )
            self.assertNotIn(
                "subprocess",
                stripped,
                f"tool-derived root reaches a process call: {stripped}",
            )
        self.assertGreater(seen, 0, "the guard must name the resolved root")

    def test_resolved_root_never_selects_a_program_in_the_shared_guard(self):
        """The resolved root is data. Only project_dir may name an executable."""
        guard_text = GUARD_PATH.read_text(encoding="utf-8")

        self.assertNotIn("Path(resolved_root) /", guard_text)
        self.assertNotIn('resolved_root, "scripts', guard_text)

    def test_the_adapter_resolves_the_guard_from_its_own_checkout(self):
        """A project directory pointed at another tree supplies data, never the
        program. Resolving the guard through PROJECT_DIR would let the guarded
        tree replace the guard."""
        hook_text = HOOK_PATH.read_text(encoding="utf-8")

        self.assertIn("ADAPTER_DIR", hook_text)
        self.assertNotIn('"$PROJECT_DIR/scripts/provider_write_guard.py"', hook_text)

    def test_resolved_root_reaches_the_selector_as_data(self):
        guard_text = GUARD_PATH.read_text(encoding="utf-8")

        self.assertIn('"--root",\n                resolved_root,', guard_text)

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


def shell_payload(command: str) -> str:
    return '{"tool_name":"Bash","tool_input":{"command":%s}}' % _json_string(command)


class ShellWriteObservationTests(unittest.TestCase):
    """Shell writes are reported, and an unreadable one never blocks the tool."""

    def assert_silent_success(self, command: str) -> None:
        result = run_hook(shell_payload(command), ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "")

    def test_shell_write_to_a_manifest_is_reported(self):
        result = run_hook(
            shell_payload("sed -i s/a/b/ gitops/platform/eso/vault-secret-store.yaml"),
            ROOT,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("gitops/platform/eso/vault-secret-store.yaml", result.stdout)
        self.assertIn("did not see this write", result.stdout)

    def test_shell_redirect_into_an_authored_document_is_reported(self):
        result = run_hook(shell_payload(f"cat > {SAMPLE_DOCUMENT}"), ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(SAMPLE_DOCUMENT, result.stdout)

    def test_shell_tee_target_is_reported(self):
        result = run_hook(shell_payload("printf x | tee traefik/example.yaml"), ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("traefik/example.yaml", result.stdout)

    def test_ordinary_and_unreadable_shell_commands_never_block(self):
        for command in (
            "git status --short",
            "echo hi > /tmp/scratch.txt",
            'echo "unterminated',
            "cat ../outside/file.yaml",
            "rm -rf /",
        ):
            with self.subTest(command=command):
                self.assert_silent_success(command)

    def test_shell_observation_does_not_reach_the_surface_selector(self):
        """An unrouted shell guess must not become a hard selector failure."""
        result = run_hook(shell_payload("echo x > not-a-registered-surface.txt"), ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)


class CodexPayloadTests(unittest.TestCase):
    """The guard judges a Codex PreToolUse payload by the same boundary.

    Codex delivers `tool_name` and `tool_input` like Claude but sets no
    `CLAUDE_PROJECT_DIR`, so these cases prove the Git-derived root carries
    the same accept and reject decisions.
    """

    def test_shell_write_inside_the_repository_is_observed(self):
        import json

        payload = json.dumps(
            {
                "session_id": "synthetic",
                "hook_event_name": "PreToolUse",
                "cwd": str(ROOT),
                "tool_name": "Bash",
                "tool_input": {"command": "echo x >" + " gitops/synthetic.yaml"},
            }
        )
        result = run_hook_without_project_dir(payload, ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("systemMessage", result.stdout)

    def test_apply_patch_on_the_retired_authority_root_fails_closed(self):
        payload = '{"tool_name":"apply_patch",%s}' % (
            '"tool_input":{"file_path":"docs/00.agent-governance/x.md"}'
        )
        result = run_hook_without_project_dir(payload, ROOT)
        self.assertEqual(result.returncode, 2)
        self.assertIn("HOOK-PATH-RETIRED", result.stderr)

    def test_apply_patch_outside_the_repository_fails_closed(self):
        payload = '{"tool_name":"apply_patch","tool_input":{"file_path":"/etc/passwd"}}'
        result = run_hook_without_project_dir(payload, ROOT)
        self.assertEqual(result.returncode, 2)
        self.assertNotEqual(result.stderr.strip(), "")


class ProviderScopedEnvironmentTests(unittest.TestCase):
    """The named provider selects which runtime variables the guard may read."""

    def run_guard(self, provider: str, payload: str, environment: dict):
        env = {
            key: value
            for key, value in os.environ.items()
            if key
            not in (
                "CLAUDE_PROJECT_DIR",
                "CLAUDE_TOOL_INPUT",
                "CLAUDE_TOOL_INPUT_FILE_PATH",
            )
        }
        env.update(environment)
        return subprocess.run(
            (
                "python3",
                str(GUARD_PATH),
                "--provider",
                provider,
                "--project-dir",
                str(ROOT),
            ),
            input=payload,
            capture_output=True,
            text=True,
            env=env,
            cwd=str(ROOT),
            timeout=300,
        )

    def test_claude_payload_variable_is_read_only_for_claude(self):
        retired = (
            '{"tool_input":{"file_path":"docs/00.agent-governance/x.md"}}'
        )

        claude = self.run_guard("claude", "", {"CLAUDE_TOOL_INPUT": retired})
        codex = self.run_guard("codex", "", {"CLAUDE_TOOL_INPUT": retired})

        self.assertEqual(claude.returncode, 2)
        self.assertIn("HOOK-PATH-RETIRED", claude.stderr)
        self.assertEqual(codex.returncode, 0)

    def test_claude_path_variable_is_read_only_for_claude(self):
        outside = {"CLAUDE_TOOL_INPUT_FILE_PATH": "/etc/passwd"}

        claude = self.run_guard("claude", "{}", outside)
        codex = self.run_guard("codex", "{}", outside)

        self.assertEqual(claude.returncode, 2)
        self.assertNotEqual(claude.stderr.strip(), "")
        self.assertEqual(codex.returncode, 0)

    def test_selector_bound_stays_inside_every_registered_hook_timeout(self):
        guard_source = GUARD_PATH.read_text(encoding="utf-8")
        namespace: dict = {}
        for line in guard_source.splitlines():
            if line.startswith("SELECTOR_TIMEOUT_SECONDS ="):
                exec(line, namespace)  # noqa: S102 - one reviewed constant line
        bound = namespace["SELECTOR_TIMEOUT_SECONDS"]

        registrations = []
        claude_settings = json.loads(
            (ROOT / ".claude/settings.json").read_text(encoding="utf-8")
        )
        for matcher in claude_settings["hooks"]["PreToolUse"]:
            registrations.extend(hook["timeout"] for hook in matcher["hooks"])
        codex_registration = json.loads(
            CODEX_REGISTRATION_PATH.read_text(encoding="utf-8")
        )
        for matcher in codex_registration["hooks"]["PreToolUse"]:
            registrations.extend(hook["timeout"] for hook in matcher["hooks"])

        self.assertTrue(registrations)
        for timeout in registrations:
            # A bound above the registration is never reached: the runtime
            # kills the hook first and the controlled rejection is lost.
            self.assertLessEqual(bound, timeout)


if __name__ == "__main__":
    unittest.main()
