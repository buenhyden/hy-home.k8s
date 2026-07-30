#!/usr/bin/env python3
"""Focused regressions for the repository CI Python contract."""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts/validate-ci-python-contract.py"
SPEC = importlib.util.spec_from_file_location("validate_ci_python_contract", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load validator: {VALIDATOR_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


REQUIREMENTS = """\
jsonschema==4.26.0
pre-commit==4.6.1
PyYAML==6.0.3
"""

GITLEAKS_SHA256 = (
    "79a3ab579b53f71efd634f3aaf7e04a0fa0cf206b7ed434638d1547a2470a66e"  # pragma: allowlist secret
)

INVENTORY = f"""\
# Version inventory

### Version Contracts

```yaml
github_actions:
  'actions/checkout': '0000000000000000000000000000000000000000'
ci_python: '3.12'
ci_python_dependencies:
  jsonschema: '4.26.0'
  pre-commit: '4.6.1'
  PyYAML: '6.0.3'
ci_gitleaks:
  version: '8.30.0'
  asset: 'gitleaks_8.30.0_linux_x64.tar.gz'
  sha256: '{GITLEAKS_SHA256}' # pragma: allowlist secret
  install_path: '/usr/local/bin/gitleaks'
```
"""

GITLEAKS_INSTALL = f"""\
set -euo pipefail
curl --fail --location --silent --show-error \\
  https://github.com/gitleaks/gitleaks/releases/download/v8.30.0/gitleaks_8.30.0_linux_x64.tar.gz \\
  --output "$RUNNER_TEMP/gitleaks_8.30.0_linux_x64.tar.gz"
gitleaks_sha256='{GITLEAKS_SHA256}' # pragma: allowlist secret
printf '%s  %s\\n' "$gitleaks_sha256" "$RUNNER_TEMP/gitleaks_8.30.0_linux_x64.tar.gz" | sha256sum --check --strict
tar -xzf "$RUNNER_TEMP/gitleaks_8.30.0_linux_x64.tar.gz" -C "$RUNNER_TEMP" gitleaks
sudo install -o root -g root -m 0755 "$RUNNER_TEMP/gitleaks" /usr/local/bin/gitleaks"""

GOVERNED_TEXT_OWNERS = (
    (
        "requirements",
        Path(".github/requirements/ci-validation.txt"),
        "CI-PYTHON-PIN",
    ),
    (
        "workflow",
        Path(".github/workflows/ci.yml"),
        "CI-PYTHON-WORKFLOW",
    ),
    (
        "inventory",
        Path("docs/90.references/data/tech-stack-version-inventory.md"),
        "CI-PYTHON-INVENTORY",
    ),
)

EXPECTED_STABLE_RULE_IDS = (
    "CI-PYTHON-INPUT",
    "CI-PYTHON-PIN",
    "CI-PYTHON-INVENTORY",
    "CI-PYTHON-WORKFLOW",
    "CI-PYTHON-VERSION",
    "CI-PRECOMMIT-ACTION",
    "CI-PRECOMMIT-ALL-FILES",
    "CI-PRECOMMIT-HISTORY",
    "CI-GITLEAKS-TOOL",
    "CI-REPOSITORY-HISTORY",
    "CI-AGENT-GOVERNANCE-CHECKOUT",
)

WORKFLOW = f"""\
name: CI
jobs:
  pre-commit:
    steps:
      - uses: actions/checkout@0000000000000000000000000000000000000000
        with:
          fetch-depth: 0
      - uses: actions/setup-python@0000000000000000000000000000000000000000
        with:
          python-version: '3.12'
      - name: Install repository validation dependencies
        run: |
          python -m pip install --disable-pip-version-check --requirement .github/requirements/ci-validation.txt
      - name: Install Gitleaks
        run: |
          set -euo pipefail
          curl --fail --location --silent --show-error \\
            https://github.com/gitleaks/gitleaks/releases/download/v8.30.0/gitleaks_8.30.0_linux_x64.tar.gz \\
            --output "$RUNNER_TEMP/gitleaks_8.30.0_linux_x64.tar.gz"
          gitleaks_sha256='{GITLEAKS_SHA256}' # pragma: allowlist secret
          printf '%s  %s\\n' "$gitleaks_sha256" "$RUNNER_TEMP/gitleaks_8.30.0_linux_x64.tar.gz" | sha256sum --check --strict
          tar -xzf "$RUNNER_TEMP/gitleaks_8.30.0_linux_x64.tar.gz" -C "$RUNNER_TEMP" gitleaks
          sudo install -o root -g root -m 0755 "$RUNNER_TEMP/gitleaks" /usr/local/bin/gitleaks
      - name: Run all pre-commit hooks
        run: |
          pre-commit run --all-files --show-diff-on-failure
  repo-quality-static:
    steps:
      - uses: actions/checkout@0000000000000000000000000000000000000000
        with:
          fetch-depth: 0
      - uses: actions/setup-python@0000000000000000000000000000000000000000
        with:
          python-version: '3.12'
      - name: Install repository validation dependencies
        run: |
          python -m pip install --disable-pip-version-check --requirement .github/requirements/ci-validation.txt
      - name: Install Gitleaks
        run: |
          set -euo pipefail
          curl --fail --location --silent --show-error \\
            https://github.com/gitleaks/gitleaks/releases/download/v8.30.0/gitleaks_8.30.0_linux_x64.tar.gz \\
            --output "$RUNNER_TEMP/gitleaks_8.30.0_linux_x64.tar.gz"
          gitleaks_sha256='{GITLEAKS_SHA256}' # pragma: allowlist secret
          printf '%s  %s\\n' "$gitleaks_sha256" "$RUNNER_TEMP/gitleaks_8.30.0_linux_x64.tar.gz" | sha256sum --check --strict
          tar -xzf "$RUNNER_TEMP/gitleaks_8.30.0_linux_x64.tar.gz" -C "$RUNNER_TEMP" gitleaks
          sudo install -o root -g root -m 0755 "$RUNNER_TEMP/gitleaks" /usr/local/bin/gitleaks
      - run: bash scripts/validate-repo-quality-gates.sh .
  agent-governance-static:
    steps:
      - uses: actions/checkout@0000000000000000000000000000000000000000
        with:
          persist-credentials: false
          fetch-depth: 0
      - uses: actions/setup-python@0000000000000000000000000000000000000000
        with:
          python-version: '3.12'
      - name: Install repository validation dependencies
        run: |
          python -m pip install --disable-pip-version-check --requirement .github/requirements/ci-validation.txt
      - run: python3 scripts/validate-agent-harness-contract.py --root .
  manifest-static:
    steps:
      - uses: actions/checkout@0000000000000000000000000000000000000000
        with:
          fetch-depth: 0
      - uses: actions/setup-python@0000000000000000000000000000000000000000
        with:
          python-version: '3.12'
      - name: Install repository validation dependencies
        run: |
          python -m pip install --disable-pip-version-check --requirement .github/requirements/ci-validation.txt
      - run: bash scripts/validate-gitops-structure.sh
"""


class CiPythonContractTests(unittest.TestCase):
    def make_valid_root(self) -> Path:
        directory = tempfile.TemporaryDirectory(prefix="ci-python-contract-")
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        (root / ".github/requirements").mkdir(parents=True)
        (root / ".github/workflows").mkdir(parents=True)
        (root / "docs/90.references/data").mkdir(parents=True)
        (root / ".github/requirements/ci-validation.txt").write_text(
            REQUIREMENTS,
            encoding="utf-8",
        )
        (root / ".github/workflows/ci.yml").write_text(WORKFLOW, encoding="utf-8")
        (
            root / "docs/90.references/data/tech-stack-version-inventory.md"
        ).write_text(INVENTORY, encoding="utf-8")
        return root

    def assert_rule(self, root: Path, rule_id: str) -> None:
        with self.assertRaises(VALIDATOR.ContractError) as raised:
            VALIDATOR.validate_repository(root)
        self.assertEqual(raised.exception.rule_id, rule_id)

    def assert_value_free_rule(
        self,
        root: Path,
        rule_id: str,
        forbidden_value: str,
    ) -> None:
        with self.assertRaises(VALIDATOR.ContractError) as raised:
            VALIDATOR.validate_repository(root)
        self.assertEqual(raised.exception.rule_id, rule_id)
        self.assertNotIn(forbidden_value, raised.exception.detail)

    def test_valid_temporary_repository_passes(self) -> None:
        self.assertEqual(VALIDATOR.validate_repository(self.make_valid_root()), 4)

    def test_cli_accepts_valid_temporary_repository(self) -> None:
        root = self.make_valid_root()
        result = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), "--root", str(root)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("[PASS] CI Python contract validation passed", result.stdout)

    def test_stable_rule_inventory_is_exact_and_duplicate_free(self) -> None:
        self.assertEqual(
            VALIDATOR.STABLE_RULE_IDS,
            EXPECTED_STABLE_RULE_IDS,
        )
        self.assertEqual(
            len(VALIDATOR.STABLE_RULE_IDS),
            len(set(VALIDATOR.STABLE_RULE_IDS)),
        )

    def test_self_test_reports_the_derived_stable_rule_count(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR_PATH),
                "--root",
                str(REPO_ROOT),
                "--self-test",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "[PASS] CI Python contract self-test passed: "
            f"rules={len(EXPECTED_STABLE_RULE_IDS)} cases=14",
            result.stdout,
        )

    def test_symlink_repository_root_fails_closed_without_target_disclosure(
        self,
    ) -> None:
        root = self.make_valid_root()
        link = root.parent / f"{root.name}-link"
        link.symlink_to(root, target_is_directory=True)
        self.addCleanup(link.unlink)
        self.assert_value_free_rule(
            link,
            "CI-PYTHON-INPUT",
            str(root),
        )

    def test_lexical_parent_escape_repository_root_fails_closed(self) -> None:
        root = self.make_valid_root()
        escaped_root = root / "nested" / ".."
        self.assert_rule(escaped_root, "CI-PYTHON-INPUT")

    def test_each_governed_owner_rejects_a_symlink_parent(self) -> None:
        for owner, relative, rule_id in GOVERNED_TEXT_OWNERS:
            with self.subTest(owner=owner):
                root = self.make_valid_root()
                parent = root / relative.parent
                outside = root.parent / f"{root.name}-{owner}-outside-parent"
                parent.rename(outside)
                self.addCleanup(shutil.rmtree, outside, True)
                parent.symlink_to(outside, target_is_directory=True)
                self.assert_value_free_rule(root, rule_id, str(outside))

    def test_parent_directory_identity_swap_fails_closed(self) -> None:
        root = self.make_valid_root()
        parent = root / ".github/requirements"
        displaced = root / ".github/requirements-before-swap"
        original_open = VALIDATOR.os.open
        triggered = False

        def swapping_open(path, flags, mode=0o777, *, dir_fd=None):
            nonlocal triggered
            if (
                not triggered
                and os.fspath(path) == "requirements"
                and dir_fd is not None
            ):
                parent.rename(displaced)
                parent.mkdir()
                triggered = True
            return original_open(path, flags, mode, dir_fd=dir_fd)

        with mock.patch.object(
            VALIDATOR.os,
            "open",
            side_effect=swapping_open,
        ):
            self.assert_rule(root, "CI-PYTHON-PIN")
        self.assertTrue(triggered)

    def test_final_regular_file_identity_swap_fails_closed(self) -> None:
        root = self.make_valid_root()
        governed = root / ".github/requirements/ci-validation.txt"
        displaced = governed.with_name(f"{governed.name}.before-swap")
        original_open = VALIDATOR.os.open
        trigger_paths = {str(governed), governed.name}
        triggered = False

        def swapping_open(path, flags, mode=0o777, *, dir_fd=None):
            nonlocal triggered
            if not triggered and os.fspath(path) in trigger_paths:
                governed.rename(displaced)
                shutil.copyfile(displaced, governed)
                triggered = True
            return original_open(path, flags, mode, dir_fd=dir_fd)

        with mock.patch.object(
            VALIDATOR.os,
            "open",
            side_effect=swapping_open,
        ):
            self.assert_rule(root, "CI-PYTHON-PIN")
        self.assertTrue(triggered)

    def test_each_governed_owner_rejects_a_final_symlink(self) -> None:
        for owner, relative, rule_id in GOVERNED_TEXT_OWNERS:
            with self.subTest(owner=owner):
                root = self.make_valid_root()
                governed = root / relative
                outside = root.parent / f"{root.name}-{owner}-outside-file"
                shutil.copyfile(governed, outside)
                self.addCleanup(outside.unlink)
                governed.unlink()
                governed.symlink_to(outside)
                self.assert_value_free_rule(root, rule_id, str(outside))

    def test_each_governed_owner_rejects_a_final_directory(self) -> None:
        for owner, relative, rule_id in GOVERNED_TEXT_OWNERS:
            with self.subTest(owner=owner):
                root = self.make_valid_root()
                governed = root / relative
                governed.unlink()
                governed.mkdir()
                self.assert_rule(root, rule_id)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO nodes require os.mkfifo")
    def test_each_governed_owner_rejects_a_final_fifo(self) -> None:
        for owner, relative, rule_id in GOVERNED_TEXT_OWNERS:
            with self.subTest(owner=owner):
                root = self.make_valid_root()
                governed = root / relative
                governed.unlink()
                os.mkfifo(governed)
                self.assert_rule(root, rule_id)

    def test_requirement_must_be_exact(self) -> None:
        root = self.make_valid_root()
        requirements = root / ".github/requirements/ci-validation.txt"
        requirements.write_text(
            "jsonschema>=4.26.0\npre-commit==4.6.1\nPyYAML==6.0.3\n",
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-PIN")

    def test_inventory_must_mirror_exact_versions(self) -> None:
        root = self.make_valid_root()
        inventory = root / "docs/90.references/data/tech-stack-version-inventory.md"
        inventory.write_text(
            inventory.read_text(encoding="utf-8").replace(
                "jsonschema: '4.26.0'",
                "jsonschema: '4.25.1'",
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-INVENTORY")

    def test_validation_job_must_pin_python_312(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        workflow.write_text(
            workflow.read_text(encoding="utf-8").replace(
                "python-version: '3.12'",
                "python-version: '3.x'",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-VERSION")

    def test_validation_job_must_use_shared_install(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        workflow.write_text(
            workflow.read_text(encoding="utf-8").replace(
                "python -m pip install --disable-pip-version-check --requirement "
                ".github/requirements/ci-validation.txt",
                "python -m pip install --disable-pip-version-check pyyaml jsonschema",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_agent_governance_job_must_pin_python_312(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        text = workflow.read_text(encoding="utf-8")
        start = text.index("  agent-governance-static:")
        version = text.index("python-version: '3.12'", start)
        workflow.write_text(
            text[:version]
            + text[version:].replace(
                "python-version: '3.12'",
                "python-version: '3.x'",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-VERSION")

    def test_agent_governance_job_must_use_shared_install(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        text = workflow.read_text(encoding="utf-8")
        start = text.index("  agent-governance-static:")
        install = text.index(
            "python -m pip install --disable-pip-version-check --requirement "
            ".github/requirements/ci-validation.txt",
            start,
        )
        workflow.write_text(
            text[:install]
            + text[install:].replace(
                "python -m pip install --disable-pip-version-check --requirement "
                ".github/requirements/ci-validation.txt",
                "python -m pip install pyyaml",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_agent_governance_checkout_must_be_credential_free_with_history(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        text = workflow.read_text(encoding="utf-8")
        start = text.index("  agent-governance-static:")
        persist_credentials = text.index("          persist-credentials: false\n", start)
        workflow.write_text(
            text[:persist_credentials]
            + text[
                persist_credentials + len("          persist-credentials: false\n") :
            ],
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-AGENT-GOVERNANCE-CHECKOUT")

    def test_agent_governance_job_must_not_install_gitleaks(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        text = workflow.read_text(encoding="utf-8")
        start = text.index("  agent-governance-static:")
        harness_step = text.index(
            "      - run: python3 scripts/validate-agent-harness-contract.py --root .\n",
            start,
        )
        injected = (
            "      - name: Install Gitleaks\n"
            "        run: |\n"
            + "".join(f"          {line}\n" for line in GITLEAKS_INSTALL.splitlines())
        )
        workflow.write_text(
            text[:harness_step] + injected + text[harness_step:],
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-GITLEAKS-TOOL")

    def test_unexpected_job_must_not_own_python_validation_setup(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        workflow.write_text(
            workflow.read_text(encoding="utf-8")
            + """\
  unexpected-python:
    steps:
      - uses: actions/setup-python@0000000000000000000000000000000000000000
        with:
          python-version: '3.x'
      - run: python -m pip install pyyaml jsonschema
""",
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_pre_commit_action_is_rejected(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        workflow.write_text(
            workflow.read_text(encoding="utf-8")
            + "\n# pre-commit/action@2c7b3805fd2a0fd8c1884dcaebf91fc102a13ecd\n",
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PRECOMMIT-ACTION")

    def test_pre_commit_command_must_be_exact(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        workflow.write_text(
            workflow.read_text(encoding="utf-8").replace(
                "pre-commit run --all-files --show-diff-on-failure",
                "pre-commit run --all-files",
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PRECOMMIT-ALL-FILES")

    def test_pre_commit_command_must_run_in_pre_commit_job(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        text = workflow.read_text(encoding="utf-8")
        text = text.replace(
            "      - name: Run all pre-commit hooks\n"
            "        run: |\n"
            "          pre-commit run --all-files --show-diff-on-failure\n",
            "",
            1,
        )
        text = text.replace(
            "      - run: bash scripts/validate-repo-quality-gates.sh .\n",
            "      - run: pre-commit run --all-files --show-diff-on-failure\n"
            "      - run: bash scripts/validate-repo-quality-gates.sh .\n",
            1,
        )
        workflow.write_text(text, encoding="utf-8")
        self.assert_rule(root, "CI-PRECOMMIT-ALL-FILES")

    def test_pre_commit_checkout_must_have_full_history(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        workflow.write_text(
            workflow.read_text(encoding="utf-8").replace(
                "          fetch-depth: 0\n",
                "",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PRECOMMIT-HISTORY")

    def test_both_repository_quality_jobs_require_exact_verified_gitleaks(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        text = workflow.read_text(encoding="utf-8")
        workflow.write_text(
            text.replace(
                GITLEAKS_SHA256,
                "0" * 64,
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-GITLEAKS-TOOL")

        workflow.write_text(
            text.replace(
                "      - name: Install Gitleaks\n"
                "        run: |\n"
                + "".join(f"          {line}\n" for line in GITLEAKS_INSTALL.splitlines()),
                "",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-GITLEAKS-TOOL")

    def test_repo_quality_checkout_must_have_full_history(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        text = workflow.read_text(encoding="utf-8")
        second_history = text.find("          fetch-depth: 0\n", text.find("repo-quality-static:"))
        self.assertNotEqual(second_history, -1)
        workflow.write_text(
            text[:second_history] + text[second_history + len("          fetch-depth: 0\n"):],
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-REPOSITORY-HISTORY")

    def test_python_requirements_remain_exactly_three_lines(self) -> None:
        root = self.make_valid_root()
        requirements = root / ".github/requirements/ci-validation.txt"
        self.assertEqual(requirements.read_text(encoding="utf-8"), REQUIREMENTS)


@unittest.skipUnless(
    (REPO_ROOT / ".github/requirements/ci-validation.txt").is_file(),
    "repository contract owners are intentionally added after temporary-root GREEN",
)
class CiPythonProductionRootTests(unittest.TestCase):
    def test_repository_root_passes(self) -> None:
        self.assertEqual(VALIDATOR.validate_repository(REPO_ROOT), 4)


if __name__ == "__main__":
    unittest.main()
