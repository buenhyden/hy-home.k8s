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
SPEC = importlib.util.spec_from_file_location(
    "validate_ci_python_contract", VALIDATOR_PATH
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load validator: {VALIDATOR_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


DIRECT_INPUT = """\
jsonschema==4.26.0
pre-commit==4.6.1
PyYAML==6.0.3
"""

RESOLVED_PINS = {
    "attrs": "26.1.0",
    "cfgv": "3.5.0",
    "distlib": "0.4.3",
    "filelock": "3.32.2",
    "identify": "2.6.19",
    "jsonschema": "4.26.0",
    "jsonschema-specifications": "2025.9.1",
    "nodeenv": "1.10.0",
    "platformdirs": "4.11.0",
    "pre-commit": "4.6.1",
    "python-discovery": "1.5.0",
    "pyyaml": "6.0.3",
    "referencing": "0.37.0",
    "rpds-py": "2026.6.3",
    "typing-extensions": "4.16.0",
    "virtualenv": "21.7.0",
}

PRE_COMMIT_REVISIONS = {
    "https://github.com/commitizen-tools/commitizen": (
        "efb1a7dc7a81934ff473100ae3a5a716f3022534"  # pragma: allowlist secret
    ),
    "https://github.com/pre-commit/pre-commit-hooks": (
        "3e8a8703264a2f4a69428a0aa4dcb512790b2c8c"  # pragma: allowlist secret
    ),
    "https://github.com/gitleaks/gitleaks": (
        "6eaad039603a4de39fddd1cf5f727391efe9974e"  # pragma: allowlist secret
    ),
    "https://github.com/Yelp/detect-secrets": (
        "01886c8a910c64595c47f186ca1ffc0b77fa5458"  # pragma: allowlist secret
    ),
    "https://github.com/DavidAnson/markdownlint-cli2": (
        "996abf60411a8d954288ac9856aae7602b80cbda"  # pragma: allowlist secret
    ),
    "https://github.com/python-jsonschema/check-jsonschema": (
        "f805888065fdb6162e1f800e50bb9460cbd223d6"  # pragma: allowlist secret
    ),
    "https://github.com/shellcheck-py/shellcheck-py": (
        "745eface02aef23e168a8afb6b5737818efbea95"  # pragma: allowlist secret
    ),
    "https://github.com/scop/pre-commit-shfmt": (
        "05c1426671b9237fb5e1444dd63aa5731bec0dfb"  # pragma: allowlist secret
    ),
    "https://github.com/astral-sh/ruff-pre-commit": (
        "1f1e8bf348ff38fc88619a38d3ca4d9c56abea49"  # pragma: allowlist secret
    ),
    "https://github.com/zizmorcore/zizmor-pre-commit": (
        "a4727cbbcd26d7098e96b9cb738169b59711ae51"  # pragma: allowlist secret
    ),
    "https://github.com/hadolint/hadolint": (
        "57e1618d78fd469a92c1e584e8c9313024656623"  # pragma: allowlist secret
    ),
    "https://github.com/rhysd/actionlint": (
        "914e7df21a07ef503a81201c76d2b11c789d3fca"  # pragma: allowlist secret
    ),
    "https://github.com/stackrox/kube-linter": (
        "10ae003038c81855aca8489df5e35da150f4dc2e"  # pragma: allowlist secret
    ),
}

PRE_COMMIT_SOURCE_TAGS = {
    "https://github.com/commitizen-tools/commitizen": "v4.15.1",
    "https://github.com/pre-commit/pre-commit-hooks": "v6.0.0",
    "https://github.com/gitleaks/gitleaks": "v8.30.0",
    "https://github.com/Yelp/detect-secrets": "v1.5.0",  # pragma: allowlist secret
    "https://github.com/DavidAnson/markdownlint-cli2": "v0.22.1",
    "https://github.com/python-jsonschema/check-jsonschema": "0.37.2",
    "https://github.com/shellcheck-py/shellcheck-py": "v0.11.0.1",
    "https://github.com/scop/pre-commit-shfmt": "v3.13.1-1",
    "https://github.com/astral-sh/ruff-pre-commit": "v0.16.5",
    "https://github.com/zizmorcore/zizmor-pre-commit": "v1.24.1",
    "https://github.com/hadolint/hadolint": "v2.14.0",
    "https://github.com/rhysd/actionlint": "v1.7.12",
    "https://github.com/stackrox/kube-linter": "v0.8.3",
}


def make_lock(pins: dict[str, str] | None = None) -> str:
    if pins is None:
        return (REPO_ROOT / ".github/requirements/ci-validation.txt").read_text(
            encoding="utf-8"
        )
    resolved = RESOLVED_PINS if pins is None else pins
    lines = [
        "# Generated for the Linux CPython 3.12 CI lane.",
        "--only-binary :all:",
        "",
    ]
    for index, (name, version) in enumerate(resolved.items(), start=1):
        lines.extend(
            (
                f"{name}=={version} \\",
                f"    --hash=sha256:{index:064x}",
            )
        )
    return "\n".join(lines) + "\n"


def make_pre_commit_config() -> str:
    lines = ["repos:"]
    for repo, revision in PRE_COMMIT_REVISIONS.items():
        lines.extend(
            (
                f"  - repo: {repo}",
                f"    rev: {revision} # frozen: {PRE_COMMIT_SOURCE_TAGS[repo]}",
                "    hooks:",
                "      - id: example",
            )
        )
    lines.extend(
        (
            "  - repo: local",
            "    hooks:",
            "      - id: local-example",
            "        name: local example",
            "        entry: true",
            "        language: system",
        )
    )
    return "\n".join(lines) + "\n"


GITLEAKS_SHA256 = "79a3ab579b53f71efd634f3aaf7e04a0fa0cf206b7ed434638d1547a2470a66e"  # pragma: allowlist secret


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
        "direct input",
        Path(".github/requirements/ci-validation.in"),
        "CI-PYTHON-PIN",
    ),
    (
        "resolved lock",
        Path(".github/requirements/ci-validation.txt"),
        "CI-PYTHON-LOCK",
    ),
    (
        "workflow",
        Path(".github/workflows/ci.yml"),
        "CI-PYTHON-WORKFLOW",
    ),
    (
        "pre-commit config",
        Path(".pre-commit-config.yaml"),
        "CI-PRECOMMIT-REV",
    ),
)

EXPECTED_STABLE_RULE_IDS = (
    "CI-PYTHON-INPUT",
    "CI-PYTHON-PIN",
    "CI-PYTHON-LOCK",
    "CI-PYTHON-WORKFLOW",
    "CI-PYTHON-VERSION",
    "CI-PRECOMMIT-ACTION",
    "CI-PRECOMMIT-REV",
    "CI-PRECOMMIT-ALL-FILES",
    "CI-PRECOMMIT-HISTORY",
    "CI-GITLEAKS-TOOL",
    "CI-REPOSITORY-HISTORY",
    "CI-AGENT-GOVERNANCE-CHECKOUT",
)
CANDIDATE_REF = "${{ github.event.pull_request.head.sha || github.sha }}"

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
          python -m pip install --disable-pip-version-check --only-binary :all: --require-hashes --requirement .github/requirements/ci-validation.txt
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
          ref: {CANDIDATE_REF}
          fetch-depth: 0
      - uses: actions/setup-python@0000000000000000000000000000000000000000
        with:
          python-version: '3.12'
      - name: Install repository validation dependencies
        run: |
          python -m pip install --disable-pip-version-check --only-binary :all: --require-hashes --requirement .github/requirements/ci-validation.txt
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
          ref: {CANDIDATE_REF}
          persist-credentials: false
          fetch-depth: 0
      - uses: actions/setup-python@0000000000000000000000000000000000000000
        with:
          python-version: '3.12'
      - name: Install repository validation dependencies
        run: |
          python -m pip install --disable-pip-version-check --only-binary :all: --require-hashes --requirement .github/requirements/ci-validation.txt
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
          python -m pip install --disable-pip-version-check --only-binary :all: --require-hashes --requirement .github/requirements/ci-validation.txt
      - run: bash scripts/validate-gitops-structure.sh
"""

PIP_INSTALL_BYPASS_COMMANDS = (
    "sudo pip install rogue==1",
    "command python -m pip install rogue==1",
    '"/usr/bin/python3" -m pip install rogue==1',
    "if python -m pip install rogue==1; then true; fi",
    "echo $(python -m pip install rogue==1)",
    "! python -m pip install rogue==1",
    "time python -m pip install rogue==1",
    "python \\\n-m \\\npip \\\ninstall rogue==1",
    "bash -c 'python -m pip install rogue==1'",
    "sh -c '/usr/bin/pip3 install rogue==1'",
    "eval 'python3.12 -m pip install rogue==1'",
    "env MODE=ci /usr/bin/python3 -m pip install rogue==1",
    "./venv/bin/python12.4 -m pip install rogue==1",
    "../venv/bin/pip3.12 install rogue==1",
    "$PIP install rogue==1",
    "env PIP=pip $PIP install rogue==1",
    "bash -c '$PIP install rogue==1'",
    "eval '$INSTALLER install rogue==1'",
    "bash -c 'python -m pip install rogue==1",
    'verb=install; pip "$verb" rogue==1',
    'verb=install; python -m pip "$verb" rogue==1',
    "cmd='pip install rogue==1'; eval \"$cmd\"",
    "cmd='pip install rogue==1'; bash -c \"$cmd\"",
    "timeout 30 pip install rogue==1",
    "nice pip install rogue==1",
    'set -- pip install rogue==1; "$@"',
    "eval \"$(printf 'pip install %s' rogue==1)\"",
    "printf 'pip install rogue==1\\n' | sh",
    "python -m pip.__main__ install rogue==1",
    'python -c \'from pip._internal.cli.main import main; main(["install","rogue==1"])\'',
    "pip --disable-pip-version-check install rogue==1",
    "python -m pip --disable-pip-version-check install rogue==1",
    'verb=install; pip --disable-pip-version-check "$verb" rogue==1',
    'verb=install; python -m pip --disable-pip-version-check "$verb" rogue==1',
    "stdbuf -oL pip install rogue==1",
    "xargs pip install rogue==1",
    "xargs sh -c 'pip install rogue==1'",
    'xargs "$PIP" install rogue==1',
    "xargs sh",
    "xargs install rogue==1",
)

PIP_INSTALL_SAFE_COMMANDS = (
    "# python -m pip install rogue==1",
    "echo 'python -m pip install rogue==1'",
    'printf "%s\\n" "python -m pip install rogue==1"',
    "mypython -m pip install rogue==1",
    "pipx install rogue==1",
    "python -m pipx install rogue==1",
    "python -m pip show pip",
    "pip download rogue==1",
    "pip show install",
    "python -m pip download install",
    "grep -q pip install",
    "true && echo /usr/bin/pip3 install rogue==1",
    'echo "$PIP install rogue==1"',
    'printf "%s\\n" "$PIP install rogue==1"',
    'grep -q "$PIP" install',
    "echo 'cat <<EOF'",
    "printf '%s\\n' '<(echo safe)'",
    "grep -q 'source \"$SCRIPT\"' file",
)

PIP_GLOBAL_VALUE_OPTIONS = (
    "--python",
    "--log",
    "--log-file",
    "--local-log",
    "--keyring-provider",
    "--proxy",
    "--retries",
    "--resume-retries",
    "--timeout",
    "--default-timeout",
    "--exists-action",
    "--trusted-host",
    "--cert",
    "--client-cert",
    "--cache-dir",
    "--use-feature",
    "--use-deprecated",
)

PIP_GLOBAL_FLAG_OPTIONS = (
    "--debug",
    "--disable-pip-version-check",
    "--help",
    "--isolated",
    "--no-cache-dir",
    "--no-color",
    "--no-input",
    "--no-python-version-warning",
    "--quiet",
    "--require-venv",
    "--require-virtualenv",
    "--verbose",
    "--version",
)

PIP_LAUNCHERS = ("pip", "python -m pip")

UNSUPPORTED_EXECUTION_COMMANDS = (
    "function runner { echo safe; }; runner",
    "runner() { echo safe; }; runner",
    'source "$SCRIPT"',
    '. "$SCRIPT"',
    "alias runner='echo safe'; runner",
    "coproc echo safe",
    "builtin echo safe",
    "eval 'echo safe'",
    "cat <<'PAYLOAD'\necho safe\nPAYLOAD",
    "cat <(echo safe)",
    "printf '%s\\n' safe | sh",
    "sh",
    "sh < input.sh",
    "sudo -s",
    "sudo --shell",
    "sudo -i",
    "values=(one two); printf '%s\\n' \"${values[0]}\"",
    "printf '%s\\n' \"first\nsecond\"",
    'xargs "$RUNNER" argument',
)

NORMALIZED_EXECUTION_DELEGATORS = (
    "\"eval\" 'pip install rogue==1'",
    "command eval 'pip install rogue==1'",
    '"source" ./script.sh',
    "command source ./script.sh",
    '"." ./script.sh',
    "command . ./script.sh",
    "builtin eval 'pip install rogue==1'",
    "\"builtin\" eval 'pip install rogue==1'",
    "command builtin eval 'pip install rogue==1'",
    '"alias" runner=echo',
    '"coproc" echo safe',
    'case "$MODE" in\nsafe)\n  ( "eval" \'pip install rogue==1\' )\n  ;;\nesac',
)

XARGS_DELEGATION_COMMANDS = (
    "xargs",
    "printf x | xargs",
    "printf x | xargs awk 'BEGIN { system(\"pip install rogue==1\") }'",
    "xargs awk 'BEGIN { system(\"pip install rogue==1\") }'",
    'xargs "$RUNNER" argument',
    'xargs "awk \'BEGIN { system(\\"pip install rogue==1\\") }\'"',
)

UNKNOWN_EXECUTABLE_COMMANDS = (
    "future-tool",
    "future-tool harmless",
    "future-tool --version",
)

SAFE_COMMAND_EXECUTION_OPTIONS = (
    "tar --to-command='pip install rogue==1' -xf archive.tar",
    "tar --to-command 'pip install rogue==1' -xf archive.tar",
    "tar --use-compress-program=sh -xf archive.tar",
    "tar --use-compress-program sh -xf archive.tar",
    "tar -I sh -xf archive.tar",
    "tar -Ish -xf archive.tar",
    "tar --checkpoint-action=exec='pip install rogue==1' -cf archive.tar .",
    "tar --rsh-command=sh -cf archive.tar .",
    "tar --new-volume-script=./runner -cf archive.tar .",
    "tar --info-script ./runner -cf archive.tar .",
    "tar -F ./runner -cf archive.tar .",
    "tar xI sh archive.tar",
    "install --strip-program=sh source target",
    "install -s --strip-program sh source target",
    "sudo install --strip-program=sh source target",
)

GIT_EXECUTION_OPTIONS_BY_SUBCOMMAND = {
    "cat-file": {
        "--filters": "--fi",
        "--textconv": "--t",
    },
    "diff": {
        "--ext-diff": "--ext",
        "--textconv": "--textc",
    },
}

GIT_SAFE_COMMANDS = (
    'git cat-file -e "$BEFORE_SHA^{commit}"',
    'git diff --no-renames --name-only -z "$BEFORE_SHA" "$HEAD_SHA"',
    'git ls-tree -r --name-only -z "$HEAD_SHA"',
    "git diff --no-ext-diff --no-textconv HEAD^ HEAD",
)

GIT_REVIEWED_WRAPPER_PREFIXES = (
    "command",
    "env MODE=ci",
    "exec",
    "nohup",
    "sudo",
    "time",
    "nice",
    "setsid",
    "timeout 30",
)

GIT_SAFE_OPTION_GRAMMAR_COMMANDS = (
    "git cat-file --f HEAD:path",
    "git diff --e HEAD^ HEAD",
    "git diff --ex HEAD^ HEAD",
    "git diff --t HEAD^ HEAD",
    "git diff --te HEAD^ HEAD",
    "git diff --tex HEAD^ HEAD",
    "git diff --text HEAD^ HEAD",
    "git diff --no-ext-diff --no-textconv HEAD^ HEAD",
    "git cat-file -e -- --filters",
    "git cat-file -e -- --textconv=value",
    "git diff HEAD^ HEAD -- --ext-diff",
    "git diff HEAD^ HEAD -- --textconv=value",
)


class CiPythonContractTests(unittest.TestCase):
    def make_valid_root(self) -> Path:
        directory = tempfile.TemporaryDirectory(prefix="ci-python-contract-")
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        (root / ".github/requirements").mkdir(parents=True)
        (root / ".github/workflows").mkdir(parents=True)
        lock = make_lock()
        (root / ".github/requirements/ci-validation.in").write_text(
            DIRECT_INPUT,
            encoding="utf-8",
        )
        (root / ".github/requirements/ci-validation.txt").write_text(
            lock,
            encoding="utf-8",
        )
        (root / ".github/workflows/ci.yml").write_text(WORKFLOW, encoding="utf-8")
        (root / ".pre-commit-config.yaml").write_text(
            make_pre_commit_config(),
            encoding="utf-8",
        )
        return root

    def assert_rule(self, root: Path, rule_id: str) -> None:
        with self.assertRaises(VALIDATOR.ContractError) as raised:
            VALIDATOR.validate_repository(root)
        self.assertEqual(raised.exception.rule_id, rule_id)

    def test_reference_inventory_is_not_a_ci_contract_input(self) -> None:
        root = self.make_valid_root()

        self.assertEqual(VALIDATOR.validate_repository(root), 4)

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

    def inject_validation_step(self, root: Path, command: str) -> None:
        workflow = root / ".github/workflows/ci.yml"
        text = workflow.read_text(encoding="utf-8")
        marker = "      - name: Install Gitleaks\n"
        indented = command.replace("\n", "\n          ")
        workflow.write_text(
            text.replace(
                marker,
                f"      - run: |\n          {indented}\n" + marker,
                1,
            ),
            encoding="utf-8",
        )

    def inject_non_validation_job(self, root: Path, command: str) -> None:
        workflow = root / ".github/workflows/ci.yml"
        indented = command.replace("\n", "\n          ")
        workflow.write_text(
            workflow.read_text(encoding="utf-8")
            + (
                "  unexpected-python:\n"
                "    steps:\n"
                "      - run: |\n"
                f"          {indented}\n"
            ),
            encoding="utf-8",
        )

    def assert_command_rejected_in_all_job_classes(self, command: str) -> None:
        root = self.make_valid_root()
        self.inject_validation_step(root, command)
        self.assert_rule(root, "CI-PYTHON-WORKFLOW")
        root = self.make_valid_root()
        self.inject_non_validation_job(root, command)
        self.assert_rule(root, "CI-PYTHON-WORKFLOW")

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
                if relative.parent == Path("."):
                    continue
                root = self.make_valid_root()
                parent = root / relative.parent
                outside = root.parent / f"{root.name}-{owner}-outside-parent"
                parent.rename(outside)
                self.addCleanup(shutil.rmtree, outside, True)
                parent.symlink_to(outside, target_is_directory=True)
                expected_rule = (
                    "CI-PYTHON-PIN"
                    if relative == Path(".github/requirements/ci-validation.txt")
                    else rule_id
                )
                self.assert_value_free_rule(root, expected_rule, str(outside))

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
        governed = root / ".github/requirements/ci-validation.in"
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

    def test_direct_input_rejects_a_range(self) -> None:
        root = self.make_valid_root()
        direct_input = root / ".github/requirements/ci-validation.in"
        direct_input.write_text(
            "jsonschema>=4.26.0\npre-commit==4.6.1\nPyYAML==6.0.3\n",
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-PIN")

    def test_direct_input_rejects_a_duplicate(self) -> None:
        root = self.make_valid_root()
        direct_input = root / ".github/requirements/ci-validation.in"
        direct_input.write_text(
            DIRECT_INPUT + "jsonschema==4.26.0\n",
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-PIN")

    def test_direct_input_rejects_a_dropped_direct_dependency(self) -> None:
        root = self.make_valid_root()
        direct_input = root / ".github/requirements/ci-validation.in"
        direct_input.write_text(
            DIRECT_INPUT.replace("PyYAML==6.0.3\n", ""),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-PIN")

    def test_lock_rejects_an_unhashed_transitive_dependency(self) -> None:
        root = self.make_valid_root()
        lock = root / ".github/requirements/ci-validation.txt"
        lock.write_text(
            lock.read_text(encoding="utf-8").replace(
                "attrs==26.1.0 \\\n"
                "    --hash=sha256:c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309\n",
                "attrs==26.1.0\n",
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-LOCK")

    def test_lock_rejects_a_missing_transitive_dependency(self) -> None:
        root = self.make_valid_root()
        lock = root / ".github/requirements/ci-validation.txt"
        lock.write_text(
            lock.read_text(encoding="utf-8").replace(
                "cfgv==3.5.0 \\\n"
                "    --hash=sha256:a8dc6b26ad22ff227d2634a65cb388215ce6cc96bbcc5cfde7641ae87e8dacc0\n",
                "",
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-LOCK")

    def test_lock_rejects_a_non_sha256_hash(self) -> None:
        root = self.make_valid_root()
        lock = root / ".github/requirements/ci-validation.txt"
        lock.write_text(
            lock.read_text(encoding="utf-8").replace(
                "--hash=sha256:",
                "--hash=sha512:",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-LOCK")

    def test_lock_rejects_a_ranged_dependency(self) -> None:
        root = self.make_valid_root()
        lock = root / ".github/requirements/ci-validation.txt"
        lock.write_text(
            lock.read_text(encoding="utf-8").replace(
                "attrs==26.1.0",
                "attrs>=26.1.0",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-LOCK")

    def test_lock_rejects_a_duplicate_dependency(self) -> None:
        root = self.make_valid_root()
        lock = root / ".github/requirements/ci-validation.txt"
        lock.write_text(
            lock.read_text(encoding="utf-8")
            + "attrs==26.1.0 \\\n"
            + "    --hash=sha256:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\n",
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-LOCK")

    def test_lock_rejects_a_dropped_direct_dependency(self) -> None:
        root = self.make_valid_root()
        lock = root / ".github/requirements/ci-validation.txt"
        lock.write_text(
            lock.read_text(encoding="utf-8").replace(
                "jsonschema==4.26.0 \\\n"
                "    --hash=sha256:d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce\n",
                "",
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-LOCK")

    def test_structurally_valid_lock_hash_update_is_not_source_pinned(self) -> None:
        root = self.make_valid_root()
        lock = root / ".github/requirements/ci-validation.txt"
        lock.write_text(
            lock.read_text(encoding="utf-8").replace(
                "c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309",  # pragma: allowlist secret
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                1,
            ),
            encoding="utf-8",
        )
        VALIDATOR.validate_repository(root)

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
                "python -m pip install --disable-pip-version-check "
                "--only-binary :all: --require-hashes --requirement "
                ".github/requirements/ci-validation.txt",
                "python -m pip install --disable-pip-version-check pyyaml jsonschema",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_validation_job_install_requires_hash_mode(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        workflow.write_text(
            workflow.read_text(encoding="utf-8").replace(
                " --require-hashes",
                "",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_validation_job_install_disallows_source_distributions(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        workflow.write_text(
            workflow.read_text(encoding="utf-8").replace(
                " --only-binary :all:",
                "",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_validation_job_rejects_absolute_python_path_pip_install(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        text = workflow.read_text(encoding="utf-8")
        marker = "      - name: Install Gitleaks\n"
        workflow.write_text(
            text.replace(
                marker,
                "      - run: /usr/bin/python3 -m pip install rogue==1\n" + marker,
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_validation_job_rejects_versioned_python_pip_install(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        text = workflow.read_text(encoding="utf-8")
        marker = "      - name: Install Gitleaks\n"
        workflow.write_text(
            text.replace(
                marker,
                "      - run: python3.12 -m pip install rogue==1\n" + marker,
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_validation_job_rejects_absolute_direct_pip_path_install(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        text = workflow.read_text(encoding="utf-8")
        marker = "      - name: Install Gitleaks\n"
        workflow.write_text(
            text.replace(
                marker,
                "      - run: /usr/bin/pip3 install rogue==1\n" + marker,
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_validation_job_rejects_env_prefixed_python_path_install(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        text = workflow.read_text(encoding="utf-8")
        marker = "      - name: Install Gitleaks\n"
        workflow.write_text(
            text.replace(
                marker,
                "      - run: env /usr/bin/python3 -m pip install rogue==1\n" + marker,
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
            "python -m pip install --disable-pip-version-check "
            "--only-binary :all: --require-hashes --requirement "
            ".github/requirements/ci-validation.txt",
            start,
        )
        workflow.write_text(
            text[:install]
            + text[install:].replace(
                "python -m pip install --disable-pip-version-check "
                "--only-binary :all: --require-hashes --requirement "
                ".github/requirements/ci-validation.txt",
                "python -m pip install pyyaml",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_agent_governance_checkout_must_be_credential_free_with_history(
        self,
    ) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        text = workflow.read_text(encoding="utf-8")
        start = text.index("  agent-governance-static:")
        persist_credentials = text.index(
            "          persist-credentials: false\n", start
        )
        workflow.write_text(
            text[:persist_credentials]
            + text[
                persist_credentials + len("          persist-credentials: false\n") :
            ],
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-AGENT-GOVERNANCE-CHECKOUT")

    def test_agent_governance_checkout_must_select_candidate_head(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        text = workflow.read_text(encoding="utf-8")
        start = text.index("  agent-governance-static:")
        candidate_ref = text.index(f"          ref: {CANDIDATE_REF}\n", start)
        workflow.write_text(
            text[:candidate_ref]
            + text[candidate_ref + len(f"          ref: {CANDIDATE_REF}\n") :],
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
        injected = "      - name: Install Gitleaks\n        run: |\n" + "".join(
            f"          {line}\n" for line in GITLEAKS_INSTALL.splitlines()
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

    def test_unexpected_job_rejects_relative_versioned_python_path_install(
        self,
    ) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        workflow.write_text(
            workflow.read_text(encoding="utf-8")
            + """\
  unexpected-python:
    steps:
      - run: ./venv/bin/python3.12 -m pip install rogue==1
""",
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_validation_jobs_reject_the_closed_pip_bypass_matrix(self) -> None:
        for command in PIP_INSTALL_BYPASS_COMMANDS:
            with self.subTest(command=command):
                root = self.make_valid_root()
                self.inject_validation_step(root, command)
                self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_non_validation_jobs_reject_the_closed_pip_bypass_matrix(
        self,
    ) -> None:
        for command in PIP_INSTALL_BYPASS_COMMANDS:
            with self.subTest(command=command):
                root = self.make_valid_root()
                self.inject_non_validation_job(root, command)
                self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_validation_jobs_accept_safe_shell_controls(self) -> None:
        for command in PIP_INSTALL_SAFE_COMMANDS:
            with self.subTest(command=command):
                root = self.make_valid_root()
                self.inject_validation_step(root, command)
                self.assertEqual(VALIDATOR.validate_repository(root), 4)

    def test_non_validation_jobs_accept_safe_shell_controls(self) -> None:
        for command in PIP_INSTALL_SAFE_COMMANDS:
            with self.subTest(command=command):
                root = self.make_valid_root()
                self.inject_non_validation_job(root, command)
                self.assertEqual(VALIDATOR.validate_repository(root), 4)

    def test_valued_pip_globals_with_separate_values_reject_install(self) -> None:
        for launcher in PIP_LAUNCHERS:
            for option in PIP_GLOBAL_VALUE_OPTIONS:
                command = f"{launcher} {option} option-value install rogue==1"
                with self.subTest(launcher=launcher, option=option):
                    root = self.make_valid_root()
                    self.inject_validation_step(root, command)
                    self.assert_rule(root, "CI-PYTHON-WORKFLOW")
                    root = self.make_valid_root()
                    self.inject_non_validation_job(root, command)
                    self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_valueless_and_short_pip_globals_use_the_effective_subcommand(
        self,
    ) -> None:
        spellings = PIP_GLOBAL_FLAG_OPTIONS + ("-h", "-V", "-vvq")
        self.assertEqual(
            VALIDATOR.PIP_GLOBAL_FLAG_OPTIONS,
            frozenset(PIP_GLOBAL_FLAG_OPTIONS),
        )
        for launcher in PIP_LAUNCHERS:
            for spelling in spellings:
                with self.subTest(launcher=launcher, spelling=spelling):
                    unsafe = f"{launcher} {spelling} install rogue==1"
                    root = self.make_valid_root()
                    self.inject_validation_step(root, unsafe)
                    self.assert_rule(root, "CI-PYTHON-WORKFLOW")
                    root = self.make_valid_root()
                    self.inject_non_validation_job(root, unsafe)
                    self.assert_rule(root, "CI-PYTHON-WORKFLOW")

                    safe = f"{launcher} {spelling} show install"
                    root = self.make_valid_root()
                    self.inject_validation_step(root, safe)
                    self.assertEqual(VALIDATOR.validate_repository(root), 4)
                    root = self.make_valid_root()
                    self.inject_non_validation_job(root, safe)
                    self.assertEqual(VALIDATOR.validate_repository(root), 4)

    def test_valued_pip_global_inventory_is_exact(self) -> None:
        self.assertEqual(
            VALIDATOR.PIP_GLOBAL_OPTIONS_WITH_VALUE,
            frozenset(PIP_GLOBAL_VALUE_OPTIONS),
        )

    def test_valued_pip_globals_with_equals_values_reject_install(self) -> None:
        for launcher in PIP_LAUNCHERS:
            for option in PIP_GLOBAL_VALUE_OPTIONS:
                command = f"{launcher} {option}=option-value install rogue==1"
                with self.subTest(launcher=launcher, option=option):
                    root = self.make_valid_root()
                    self.inject_validation_step(root, command)
                    self.assert_rule(root, "CI-PYTHON-WORKFLOW")
                    root = self.make_valid_root()
                    self.inject_non_validation_job(root, command)
                    self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_literal_install_as_a_pip_global_value_is_not_a_subcommand(self) -> None:
        for launcher in PIP_LAUNCHERS:
            for option in PIP_GLOBAL_VALUE_OPTIONS:
                for spelling in (f"{option} install", f"{option}=install"):
                    command = f"{launcher} {spelling} show rogue==1"
                    with self.subTest(launcher=launcher, spelling=spelling):
                        root = self.make_valid_root()
                        self.inject_validation_step(root, command)
                        self.assertEqual(VALIDATOR.validate_repository(root), 4)
                        root = self.make_valid_root()
                        self.inject_non_validation_job(root, command)
                        self.assertEqual(VALIDATOR.validate_repository(root), 4)

    def test_dynamic_pip_global_values_fail_closed(self) -> None:
        for launcher in PIP_LAUNCHERS:
            for option in PIP_GLOBAL_VALUE_OPTIONS:
                for spelling in (f'{option} "$VALUE"', f'{option}="$VALUE"'):
                    command = f"{launcher} {spelling} install rogue==1"
                    with self.subTest(launcher=launcher, spelling=spelling):
                        root = self.make_valid_root()
                        self.inject_validation_step(root, command)
                        self.assert_rule(root, "CI-PYTHON-WORKFLOW")
                        root = self.make_valid_root()
                        self.inject_non_validation_job(root, command)
                        self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_unknown_pip_globals_fail_closed_for_both_launchers(self) -> None:
        spellings = (
            "--future-global",
            "--future-global=value",
            "--future-global option-value",
            "-Z",
            "-Zvalue",
        )
        for launcher in PIP_LAUNCHERS:
            for spelling in spellings:
                command = f"{launcher} {spelling} show install"
                with self.subTest(launcher=launcher, spelling=spelling):
                    root = self.make_valid_root()
                    self.inject_validation_step(root, command)
                    self.assert_rule(root, "CI-PYTHON-WORKFLOW")
                    root = self.make_valid_root()
                    self.inject_non_validation_job(root, command)
                    self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_validation_jobs_reject_unsupported_execution_grammar(self) -> None:
        for command in UNSUPPORTED_EXECUTION_COMMANDS:
            with self.subTest(command=command):
                root = self.make_valid_root()
                self.inject_validation_step(root, command)
                self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_non_validation_jobs_reject_unsupported_execution_grammar(
        self,
    ) -> None:
        for command in UNSUPPORTED_EXECUTION_COMMANDS:
            with self.subTest(command=command):
                root = self.make_valid_root()
                self.inject_non_validation_job(root, command)
                self.assert_rule(root, "CI-PYTHON-WORKFLOW")

    def test_normalized_execution_delegators_fail_closed_in_all_jobs(self) -> None:
        for command in NORMALIZED_EXECUTION_DELEGATORS:
            with self.subTest(command=command):
                self.assert_command_rejected_in_all_job_classes(command)

    def test_xargs_delegation_fails_closed_in_all_forms_and_jobs(self) -> None:
        for command in XARGS_DELEGATION_COMMANDS:
            with self.subTest(command=command):
                self.assert_command_rejected_in_all_job_classes(command)

    def test_unknown_executables_fail_closed_in_all_jobs(self) -> None:
        for command in UNKNOWN_EXECUTABLE_COMMANDS:
            with self.subTest(command=command):
                self.assert_command_rejected_in_all_job_classes(command)

    def test_safe_command_execution_options_fail_closed_in_all_jobs(self) -> None:
        for command in SAFE_COMMAND_EXECUTION_OPTIONS:
            with self.subTest(command=command):
                self.assert_command_rejected_in_all_job_classes(command)

    def test_git_execution_long_option_prefixes_fail_closed_in_all_jobs(
        self,
    ) -> None:
        for subcommand, options in GIT_EXECUTION_OPTIONS_BY_SUBCOMMAND.items():
            operand = "HEAD:path" if subcommand == "cat-file" else "HEAD^ HEAD"
            for option, minimum_prefix in options.items():
                for length in range(len(minimum_prefix), len(option) + 1):
                    prefix = option[:length]
                    for spelling in (prefix, f"{prefix}=value"):
                        command = f"git {subcommand} {spelling} {operand}"
                        with self.subTest(
                            subcommand=subcommand,
                            option=option,
                            spelling=spelling,
                        ):
                            self.assert_command_rejected_in_all_job_classes(command)

    def test_git_option_grammar_preserves_safe_controls_in_all_jobs(self) -> None:
        for command in GIT_SAFE_OPTION_GRAMMAR_COMMANDS:
            with self.subTest(command=command):
                root = self.make_valid_root()
                self.inject_validation_step(root, command)
                self.assertEqual(VALIDATOR.validate_repository(root), 4)
                root = self.make_valid_root()
                self.inject_non_validation_job(root, command)
                self.assertEqual(VALIDATOR.validate_repository(root), 4)

    def test_git_execution_options_resist_normalized_obfuscation(self) -> None:
        commands = [
            '"git" "cat-file" "--textc" HEAD:path',
            "GIT_EXTERNAL_DIFF=sh git diff --ext-d HEAD^ HEAD",
            (
                "GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=diff.demo.textconv "
                "GIT_CONFIG_VALUE_0=sh git cat-file --textc HEAD:path"
            ),
            (
                "env GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=filter.demo.smudge "
                "GIT_CONFIG_VALUE_0=sh git cat-file --filt HEAD:path"
            ),
        ]
        commands.extend(
            f"{wrapper} git diff --ext-d HEAD^ HEAD"
            for wrapper in GIT_REVIEWED_WRAPPER_PREFIXES
        )
        for command in commands:
            with self.subTest(command=command):
                self.assert_command_rejected_in_all_job_classes(command)

        for command in GIT_SAFE_COMMANDS:
            with self.subTest(safe_command=command):
                root = self.make_valid_root()
                self.inject_validation_step(root, command)
                self.assertEqual(VALIDATOR.validate_repository(root), 4)
                root = self.make_valid_root()
                self.inject_non_validation_job(root, command)
                self.assertEqual(VALIDATOR.validate_repository(root), 4)

    def test_ci_summary_preserves_pass_skip_fail_missing_and_cancelled(self) -> None:
        workflow = VALIDATOR.yaml.safe_load(
            (REPO_ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        )
        script = workflow["jobs"]["ci-summary"]["steps"][0]["run"]
        base_env = {
            "EVENT_NAME": "pull_request",
            "BRANCH_POLICY_RESULT": "success",
            "CHANGES_RESULT": "success",
            "PRE_COMMIT_SELECTED": "true",
            "PRE_COMMIT_RESULT": "success",
            "REPO_QUALITY_STATIC_SELECTED": "false",
            "REPO_QUALITY_STATIC_RESULT": "skipped",
            "AGENT_GOVERNANCE_STATIC_SELECTED": "true",
            "AGENT_GOVERNANCE_STATIC_RESULT": "success",
            "MANIFEST_STATIC_SELECTED": "false",
            "MANIFEST_STATIC_RESULT": "skipped",
        }

        success = subprocess.run(
            ["/bin/bash", "-c", script],
            cwd=REPO_ROOT,
            env=base_env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(success.returncode, 0, success.stdout + success.stderr)
        self.assertIn(
            "branch-policy selected=true result=success verdict=PASS",
            success.stdout,
        )
        self.assertIn(
            "repo-quality-static selected=false result=skipped verdict=SKIP",
            success.stdout,
        )
        self.assertIn(
            "changes selected=true result=success verdict=PASS",
            success.stdout,
        )

        push_env = base_env | {
            "EVENT_NAME": "push",
            "BRANCH_POLICY_RESULT": "skipped",
        }
        push = subprocess.run(
            ["/bin/bash", "-c", script],
            cwd=REPO_ROOT,
            env=push_env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(push.returncode, 0, push.stdout + push.stderr)
        self.assertIn(
            "branch-policy selected=false result=skipped verdict=SKIP",
            push.stdout,
        )

        for label, updates in (
            ("required-failure", {"CHANGES_RESULT": "failure"}),
            (
                "cancelled",
                {
                    "AGENT_GOVERNANCE_STATIC_SELECTED": "true",
                    "AGENT_GOVERNANCE_STATIC_RESULT": "cancelled",
                },
            ),
            (
                "missing-selection",
                {
                    "MANIFEST_STATIC_SELECTED": "",
                    "MANIFEST_STATIC_RESULT": "skipped",
                },
            ),
        ):
            with self.subTest(label=label):
                result = subprocess.run(
                    ["/bin/bash", "-c", script],
                    cwd=REPO_ROOT,
                    env=base_env | updates,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("verdict=FAIL", result.stdout)
                self.assertIn(
                    "one or more required CI gates failed closed",
                    result.stdout,
                )

    def test_rejects_step_job_and_workflow_shell_overrides(self) -> None:
        mutations = (
            (
                "step",
                "      - run: |\n          python -m pip install rogue==1\n        shell: python\n",
            ),
            ("job", "    defaults:\n      run:\n        shell: python\n"),
            ("workflow", "defaults:\n  run:\n    shell: python\n"),
        )
        for label, mutation in mutations:
            with self.subTest(level=label):
                root = self.make_valid_root()
                workflow = root / ".github/workflows/ci.yml"
                text = workflow.read_text(encoding="utf-8")
                if label == "step":
                    text = text.replace(
                        "      - name: Install Gitleaks\n",
                        mutation + "      - name: Install Gitleaks\n",
                        1,
                    )
                elif label == "job":
                    text = text.replace(
                        "  pre-commit:\n", "  pre-commit:\n" + mutation, 1
                    )
                else:
                    text = mutation + text
                workflow.write_text(text, encoding="utf-8")
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

    def test_pre_commit_tag_revision_is_rejected(self) -> None:
        root = self.make_valid_root()
        config = root / ".pre-commit-config.yaml"
        revision = next(iter(PRE_COMMIT_REVISIONS.values()))
        config.write_text(
            config.read_text(encoding="utf-8").replace(
                revision,
                "v4.15.1",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PRECOMMIT-REV")

    def test_pre_commit_branch_revision_is_rejected(self) -> None:
        root = self.make_valid_root()
        config = root / ".pre-commit-config.yaml"
        revision = next(iter(PRE_COMMIT_REVISIONS.values()))
        config.write_text(
            config.read_text(encoding="utf-8").replace(
                revision,
                "main",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PRECOMMIT-REV")

    def test_pre_commit_abbreviated_revision_is_rejected(self) -> None:
        root = self.make_valid_root()
        config = root / ".pre-commit-config.yaml"
        revision = next(iter(PRE_COMMIT_REVISIONS.values()))
        config.write_text(
            config.read_text(encoding="utf-8").replace(
                revision,
                revision[:12],
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PRECOMMIT-REV")

    def test_pre_commit_wrong_full_sha_revision_is_rejected(self) -> None:
        root = self.make_valid_root()
        config = root / ".pre-commit-config.yaml"
        revision = next(iter(PRE_COMMIT_REVISIONS.values()))
        config.write_text(
            config.read_text(encoding="utf-8").replace(
                revision,
                "f" * 40,
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PRECOMMIT-REV")

    def test_pre_commit_missing_revision_is_rejected(self) -> None:
        root = self.make_valid_root()
        config = root / ".pre-commit-config.yaml"
        revision = next(iter(PRE_COMMIT_REVISIONS.values()))
        config.write_text(
            config.read_text(encoding="utf-8").replace(
                f"    rev: {revision} # frozen: v4.15.1\n",
                "",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PRECOMMIT-REV")

    def test_pre_commit_frozen_tag_moved_to_unrelated_comment_is_rejected(
        self,
    ) -> None:
        root = self.make_valid_root()
        config = root / ".pre-commit-config.yaml"
        repo, revision = next(iter(PRE_COMMIT_REVISIONS.items()))
        expected_line = f"    rev: {revision} # frozen: {PRE_COMMIT_SOURCE_TAGS[repo]}"
        mutated = config.read_text(encoding="utf-8").replace(
            expected_line,
            f"    rev: {revision} # frozen: wrong-source-tag",
            1,
        )
        config.write_text(
            mutated + f"\n# {expected_line}\n",
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PRECOMMIT-REV")

    def test_pre_commit_duplicate_repository_is_rejected(self) -> None:
        root = self.make_valid_root()
        config = root / ".pre-commit-config.yaml"
        repo, revision = next(iter(PRE_COMMIT_REVISIONS.items()))
        duplicate = (
            f"  - repo: {repo}\n"
            f"    rev: {revision} # frozen: {PRE_COMMIT_SOURCE_TAGS[repo]}\n"
            "    hooks:\n"
            "      - id: duplicate\n"
        )
        config.write_text(
            config.read_text(encoding="utf-8").replace(
                "  - repo: local\n",
                duplicate + "  - repo: local\n",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PRECOMMIT-REV")

    def test_pre_commit_local_repository_must_not_have_a_revision(self) -> None:
        root = self.make_valid_root()
        config = root / ".pre-commit-config.yaml"
        config.write_text(
            config.read_text(encoding="utf-8").replace(
                "  - repo: local\n",
                "  - repo: local\n    rev: 0000000000000000000000000000000000000000\n",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PRECOMMIT-REV")

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
                + "".join(
                    f"          {line}\n" for line in GITLEAKS_INSTALL.splitlines()
                ),
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
        second_history = text.find(
            "          fetch-depth: 0\n", text.find("repo-quality-static:")
        )
        self.assertNotEqual(second_history, -1)
        workflow.write_text(
            text[:second_history]
            + text[second_history + len("          fetch-depth: 0\n") :],
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-REPOSITORY-HISTORY")

    def test_repo_quality_checkout_must_select_candidate_head(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        text = workflow.read_text(encoding="utf-8")
        start = text.index("  repo-quality-static:")
        candidate_ref = text.index(f"          ref: {CANDIDATE_REF}\n", start)
        workflow.write_text(
            text[:candidate_ref]
            + text[candidate_ref + len(f"          ref: {CANDIDATE_REF}\n") :],
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-REPOSITORY-HISTORY")

    def test_python_direct_input_remains_exactly_three_lines(self) -> None:
        root = self.make_valid_root()
        direct_input = root / ".github/requirements/ci-validation.in"
        self.assertEqual(direct_input.read_text(encoding="utf-8"), DIRECT_INPUT)


@unittest.skipUnless(
    (REPO_ROOT / ".github/requirements/ci-validation.in").is_file(),
    "repository contract owners are intentionally added after temporary-root GREEN",
)
class CiPythonProductionRootTests(unittest.TestCase):
    def test_repository_root_passes(self) -> None:
        self.assertEqual(VALIDATOR.validate_repository(REPO_ROOT), 4)


if __name__ == "__main__":
    unittest.main()
