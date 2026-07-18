"""Provider-entry isolation regressions for the production post-validate hook."""

from __future__ import annotations

import json
import re
import shlex
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK_PATH = ROOT / "docs/00.agent-governance/hooks/post-validate.sh"
QUALITY_MARKER = "[PASS] repository quality gates passed"
HOOK_RELATIVE_PATH = "docs/00.agent-governance/hooks/post-validate.sh"

PROVIDERS = {
    "claude": (ROOT / ".claude/settings.json", "CLAUDE_PROJECT_DIR"),
    "codex": (ROOT / ".codex/hooks.json", "CODEX_PROJECT_DIR"),
    "gemini": (ROOT / ".agents/hooks.json", "GEMINI_PROJECT_DIR"),
}

EXPECTED_VALIDATORS = {
    "docs": {
        "document-contract-registry",
        "links-and-owners",
        "markdown-profiles",
        "repository-quality",
    },
    "manifest": {
        "gitops-change-set",
        "gitops-structure",
        "infrastructure-contracts",
        "k8s-manifests",
        "policy-gates",
        "repository-quality",
        "secret-handling",
    },
}


def post_validate_command(config_path: Path) -> str:
    data = json.loads(config_path.read_text(encoding="utf-8"))
    for entry in data["hooks"]["PostToolUse"]:
        if entry.get("matcher") != "Write|Edit|MultiEdit":
            continue
        for hook in entry.get("hooks", []):
            command = str(hook.get("command") or "")
            if HOOK_RELATIVE_PATH in command:
                return command
    raise AssertionError(f"missing PostToolUse hook in {config_path}")


def expected_command(provider: str, project_variable: str) -> str:
    provider_assignments = (
        f'{project_variable}="${project_variable}" '
        if provider == "claude"
        else (
            f'{project_variable}="${project_variable}" '
            f'CLAUDE_PROJECT_DIR="${project_variable}" '
        )
    )
    return (
        '/usr/bin/env -i HOME="$HOME" LANG=C.UTF-8 LC_ALL=C.UTF-8 '
        "PATH=/usr/bin:/bin "
        f"{provider_assignments}"
        f"HY_HOME_K8S_HOOK_PROVIDER={provider} "
        "/usr/bin/bash --noprofile --norc "
        f'"${project_variable}/{HOOK_RELATIVE_PATH}"'
    )


class ProviderPostValidateEntryTest(unittest.TestCase):
    def test_provider_commands_are_exact_closed_absolute_entries(self):
        for provider, (config_path, project_variable) in PROVIDERS.items():
            with self.subTest(provider=provider):
                command = post_validate_command(config_path)
                self.assertEqual(command, expected_command(provider, project_variable))
                self.assertNotIn("$(", command)
                self.assertNotRegex(command, r"\b(?:git|pwd)\b")

    def test_every_production_python_entry_is_isolated(self):
        hook_text = HOOK_PATH.read_text(encoding="utf-8")

        self.assertNotRegex(hook_text, r"(?m)^\s*(?:if ! )?python3\b")
        self.assertEqual(hook_text.count("/usr/bin/python3 -I"), 4)
        self.assertGreaterEqual(hook_text.count("/usr/bin/env -i"), 4)
        self.assertNotIn("git rev-parse", hook_text)

    def test_actual_provider_commands_fail_closed_and_preserve_selection(self):
        with tempfile.TemporaryDirectory(prefix="provider-post-validate-") as raw_temp:
            temp = Path(raw_temp)
            fixture_root = temp / "fixture"
            self._build_fixture(fixture_root)
            hostile_environment, markers = self._hostile_environment(temp, fixture_root)

            payloads = {
                "docs": {
                    "tool_input": {"file_path": "docs/03.specs/provider-hook-probe.md"}
                },
                "manifest": {
                    "tool_input": {
                        "file_path": ("gitops/platform/headlamp/headlamp-ingress.yaml")
                    }
                },
            }
            for provider, (config_path, _project_variable) in PROVIDERS.items():
                command = post_validate_command(config_path)
                for payload_name, payload in payloads.items():
                    with self.subTest(provider=provider, payload=payload_name):
                        completed = self._run_command(
                            command,
                            fixture_root,
                            hostile_environment,
                            json.dumps(payload),
                        )
                        output = completed.stdout + completed.stderr
                        self.assertEqual(completed.returncode, 0, output)
                        self.assertTrue(output.strip())
                        statuses = set(
                            re.findall(r"^\[PASS\] ([^ ]+) ", output, re.MULTILINE)
                        )
                        self.assertEqual(statuses, EXPECTED_VALIDATORS[payload_name])
                        self.assertIn('scope="affected:paths=1"', output)
                        if payload_name == "docs":
                            self.assertGreaterEqual(
                                output.count("docs/03.specs/provider-hook-probe.md"),
                                3,
                            )

                with self.subTest(provider=provider, payload="malformed"):
                    completed = self._run_command(
                        command,
                        fixture_root,
                        hostile_environment,
                        '{"tool_input":',
                    )
                    output = completed.stdout + completed.stderr
                    self.assertEqual(completed.returncode, 2, output)
                    self.assertTrue(output.strip())
                    self.assertIn("[FAIL] HOOK-PAYLOAD-JSON", output)

            for marker in markers:
                self.assertFalse(marker.exists(), f"hostile startup executed: {marker}")

    @staticmethod
    def _run_command(
        command: str,
        fixture_root: Path,
        environment: dict[str, str],
        payload: str,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["/bin/sh", "-c", command],
            cwd=fixture_root,
            input=payload,
            text=True,
            capture_output=True,
            env=environment,
            timeout=60,
            check=False,
        )

    @staticmethod
    def _build_fixture(fixture_root: Path) -> None:
        fixture_files = (
            "docs/00.agent-governance/hooks/post-validate.sh",
            "docs/00.agent-governance/hooks/post-validate-runner-result.py",
            "docs/00.agent-governance/contracts/validation-surfaces.schema.json",
            "docs/00.agent-governance/contracts/validation-surfaces.json",
            "scripts/run-validation-lane.py",
            "scripts/select-affected-surfaces.py",
            "scripts/validate-affected-surfaces.py",
        )
        for relative_path in fixture_files:
            source = ROOT / relative_path
            target = fixture_root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

        contract_path = (
            fixture_root / "docs/00.agent-governance/contracts/validation-surfaces.json"
        )
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        for validator in contract["validators"]:
            validator["argv"] = [
                "bash",
                "scripts/provider-hook-validator-probe.sh",
                validator["id"],
            ]
        contract_path.write_text(
            json.dumps(contract, indent=2) + "\n",
            encoding="utf-8",
        )

        probe = fixture_root / "scripts/provider-hook-validator-probe.sh"
        probe.write_text(
            "#!/usr/bin/bash\n"
            "set -euo pipefail\n"
            'if [[ "$1" == repository-quality ]]; then\n'
            f"  printf '%s\\n' {shlex.quote(QUALITY_MARKER)}\n"
            "fi\n",
            encoding="utf-8",
        )
        probe.chmod(0o755)

        targets = {
            "docs/03.specs/provider-hook-probe.md": "# Provider hook probe\n",
            "gitops/platform/headlamp/headlamp-ingress.yaml": (
                "apiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: probe\n"
            ),
        }
        for relative_path, content in targets.items():
            target = fixture_root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

    @staticmethod
    def _hostile_environment(
        temp: Path, fixture_root: Path
    ) -> tuple[dict[str, str], tuple[Path, ...]]:
        shadow = temp / "shadow"
        shadow.mkdir()
        fake_bash_marker = temp / "fake-bash-ran"
        fake_python_marker = temp / "fake-python-ran"
        startup_marker = temp / "bash-env-ran"
        for name, marker in (
            ("bash", fake_bash_marker),
            ("python3", fake_python_marker),
        ):
            executable = shadow / name
            executable.write_text(
                f"#!/bin/sh\n: > {shlex.quote(str(marker))}\nexit 0\n",
                encoding="utf-8",
            )
            executable.chmod(0o755)
        bash_env = temp / "hostile-bash-env.sh"
        bash_env.write_text(
            f": > {shlex.quote(str(startup_marker))}\nexit 0\n",
            encoding="utf-8",
        )

        home = temp / "home"
        home.mkdir()
        environment = {
            "HOME": str(home),
            "LANG": "C.UTF-8",
            "PATH": f"{shadow}:/usr/bin:/bin",
            "BASH_ENV": str(bash_env),
            "ENV": str(bash_env),
            "PYTHONPATH": str(temp / "python-shadow"),
            "NODE_OPTIONS": "--require=/tmp/provider-hook-sentinel",
            "CLAUDE_PROJECT_DIR": str(fixture_root),
            "CODEX_PROJECT_DIR": str(fixture_root),
            "GEMINI_PROJECT_DIR": str(fixture_root),
        }
        return environment, (fake_bash_marker, fake_python_marker, startup_marker)


if __name__ == "__main__":
    unittest.main()
