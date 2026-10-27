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

RETIRED_HOSTED_QA_COMMAND = 'python3 scripts/qa.py ci --base-ref "$BASE_SHA"'


DIRECT_INPUT = """\
jsonschema==4.26.0
pre-commit==4.6.1
PyYAML==6.0.3
"""

LOCK_PINS = {
    "attrs": "26.1.0",
    "jsonschema": "4.26.0",
    "pre-commit": "4.6.1",
    "pyyaml": "6.0.3",
}

# Any 40-hex revision and any frozen tag are valid: the config owns the values.
PRE_COMMIT_REPOS = {
    "https://github.com/example/one": ("a" * 40, "v1.0.0"),
    "https://github.com/example/two": ("b" * 40, "0.2.3"),
}

CHECKOUT_ACTION = "actions/checkout@" + "c" * 40
SETUP_PYTHON_ACTION = "actions/setup-python@" + "d" * 40
ACTIONS = (CHECKOUT_ACTION, SETUP_PYTHON_ACTION)


def make_lock() -> str:
    lines = [
        "# Generated for the Linux CPython 3.12 CI lane.",
        "--only-binary :all:",
        "",
    ]
    for index, (name, version) in enumerate(LOCK_PINS.items(), start=1):
        lines.extend(
            (
                f"{name}=={version} \\",
                f"    --hash=sha256:{index:064x}",
            )
        )
    return "\n".join(lines) + "\n"


def make_pre_commit_config() -> str:
    lines = ["repos:"]
    for repo, (revision, tag) in PRE_COMMIT_REPOS.items():
        lines.extend(
            (
                f"  - repo: {repo}",
                f"    rev: {revision} # frozen: {tag}",
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

LOCK_STEP = """\
      - name: Validate a changed CI lock
        working-directory: candidate
        run: |
          set -euo pipefail
          if grep -qz '^\\.github/requirements/' "$RUNNER_TEMP/pr-style-paths.z"; then
            python -I ../trusted-base/scripts/validate-ci-python-contract.py --root .
          fi
"""

CANDIDATE_BRANCH_REF = "${{ github.sha }}"
CANDIDATE_SHA_REF = "${{ github.head_ref || github.ref }}"

WORKFLOW = """\
name: CI
jobs:
  branch-policy:
    steps:
      - name: Inspect contract
        run: echo contract
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
            VALIDATOR.validate_dependencies(root)
        self.assertEqual(raised.exception.rule_id, rule_id)

    def assert_value_free_rule(
        self,
        root: Path,
        rule_id: str,
        forbidden_value: str,
    ) -> None:
        with self.assertRaises(VALIDATOR.ContractError) as raised:
            VALIDATOR.validate_dependencies(root)
        self.assertEqual(raised.exception.rule_id, rule_id)
        self.assertNotIn(forbidden_value, raised.exception.detail)

    def inject_validation_step(self, root: Path, command: str) -> None:
        workflow = root / ".github/workflows/ci.yml"
        text = workflow.read_text(encoding="utf-8")
        marker = "      - name: Inspect contract\n"
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

    def test_non_style_jobs_reject_python_setup_and_gitleaks_install(self):
        for step, rule in (
            (
                "      - uses: actions/setup-python@0000000000000000000000000000000000000000\n",
                "CI-PYTHON-WORKFLOW",
            ),
            (
                "      - run: sudo install gitleaks /usr/local/bin/gitleaks\n",
                "CI-GITLEAKS-TOOL",
            ),
        ):
            root = self.make_valid_root()
            workflow = root / ".github/workflows/ci.yml"
            workflow.write_text(workflow.read_text() + step)
            self.assert_rule(root, rule)

    def test_hosted_jobs_reject_full_qa(self):
        root = self.make_valid_root()
        self.inject_validation_step(root, RETIRED_HOSTED_QA_COMMAND)
        self.assert_rule(root, "CI-QA-EXECUTION")

    def test_valid_temporary_repository_passes(self) -> None:
        self.assertEqual(VALIDATOR.validate_dependencies(self.make_valid_root()), 0)

    def make_real_workflow_root(self, *replacements: tuple[str, str]) -> Path:
        root = self.make_valid_root()
        text = (REPO_ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        for old, new in replacements:
            self.assertIn(old, text)
            text = text.replace(old, new)
        (root / ".github/workflows/ci.yml").write_text(text, encoding="utf-8")
        metadata = root / VALIDATOR.PR_METADATA_SCRIPT_PATH
        metadata.parent.mkdir(exist_ok=True)
        metadata.write_bytes(
            (REPO_ROOT / VALIDATOR.PR_METADATA_SCRIPT_PATH).read_bytes()
        )
        return root

    def real_action_refs(self) -> tuple[str, str]:
        workflow = VALIDATOR._load_yaml(
            (REPO_ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8"),
            "CI-PYTHON-WORKFLOW",
            VALIDATOR.WORKFLOW_PATH,
        )
        return VALIDATOR._workflow_action_refs(workflow)

    def test_cli_accepts_valid_temporary_repository(self) -> None:
        root = self.make_real_workflow_root()
        result = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), "--root", str(root)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "[PASS] local Python dependency and scoped CI contract passed",
            result.stdout,
        )
        self.assertIn("hosted-installs=1", result.stdout)

    def test_style_job_requires_the_changed_lock_step(self) -> None:
        root = self.make_real_workflow_root((LOCK_STEP, ""))
        self.assert_rule_in_repository(root, "CI-STYLE-TOPOLOGY")

    def test_changed_lock_step_condition_reads_the_path_list_directly(self) -> None:
        root = self.make_real_workflow_root(
            (
                "if grep -qz '^\\.github/requirements/' \"$RUNNER_TEMP/pr-style-paths.z\"; then",
                "if tr '\\0' '\\n' < \"$RUNNER_TEMP/pr-style-paths.z\" | grep -q '^\\.github/requirements/'; then",
            )
        )
        self.assert_rule_in_repository(root, "CI-STYLE-TOPOLOGY")

    def test_action_sha_bump_passes(self) -> None:
        checkout, setup_python = self.real_action_refs()
        root = self.make_real_workflow_root(
            (checkout, "actions/checkout@" + "1" * 40),
            (setup_python, "actions/setup-python@" + "2" * 40),
        )
        self.assertEqual(VALIDATOR.validate_repository(root), 1)

    def test_action_refs_must_be_full_commits(self) -> None:
        checkout, _ = self.real_action_refs()
        for bad in ("actions/checkout@v7", "actions/checkout@" + "A" * 40):
            with self.subTest(bad=bad):
                root = self.make_real_workflow_root((checkout, bad))
                self.assert_rule_in_repository(root, "CI-PYTHON-WORKFLOW")

    def test_action_refs_must_be_identical_across_uses(self) -> None:
        checkout, _ = self.real_action_refs()
        root = self.make_real_workflow_root()
        workflow = root / ".github/workflows/ci.yml"
        workflow.write_text(
            workflow.read_text(encoding="utf-8").replace(
                checkout, "actions/checkout@" + "1" * 40, 1
            ),
            encoding="utf-8",
        )
        self.assert_rule_in_repository(root, "CI-PYTHON-WORKFLOW")

    def assert_rule_in_repository(self, root: Path, rule_id: str) -> None:
        with self.assertRaises(VALIDATOR.ContractError) as raised:
            VALIDATOR.validate_repository(root)
        self.assertEqual(raised.exception.rule_id, rule_id)

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

    def test_direct_pin_order_does_not_duplicate_package_authority(self) -> None:
        root = self.make_valid_root()
        direct_input = root / ".github/requirements/ci-validation.in"
        direct_input.write_text(
            "\n".join(reversed(DIRECT_INPUT.splitlines())) + "\n",
            encoding="utf-8",
        )
        self.assertEqual(VALIDATOR.validate_dependencies(root), 0)

    def edit(self, root: Path, relative: str, old: str, new: str) -> None:
        path = root / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def edit_lock(self, root: Path, old: str, new: str) -> None:
        self.edit(root, ".github/requirements/ci-validation.txt", old, new)

    def test_consistent_pin_bump_in_input_and_lock_passes(self) -> None:
        root = self.make_valid_root()
        self.edit(root, ".github/requirements/ci-validation.in", "==4.26.0", "==9.9.9")
        self.edit_lock(root, "jsonschema==4.26.0", "jsonschema==9.9.9")
        self.assertEqual(VALIDATOR.validate_dependencies(root), 0)

    def test_direct_input_must_agree_with_the_lock(self) -> None:
        root = self.make_valid_root()
        self.edit(root, ".github/requirements/ci-validation.in", "==4.26.0", "==9.9.9")
        self.assert_rule(root, "CI-PYTHON-LOCK")

    def test_direct_input_rejects_a_dependency_absent_from_the_lock(self) -> None:
        root = self.make_valid_root()
        self.edit(
            root,
            ".github/requirements/ci-validation.in",
            "PyYAML==6.0.3\n",
            "PyYAML==6.0.3\nrogue==1.0.0\n",
        )
        self.assert_rule(root, "CI-PYTHON-LOCK")

    def test_lock_rejects_an_unhashed_transitive_dependency(self) -> None:
        root = self.make_valid_root()
        self.edit_lock(
            root,
            f"attrs==26.1.0 \\\n    --hash=sha256:{1:064x}\n",
            "attrs==26.1.0\n",
        )
        self.assert_rule(root, "CI-PYTHON-LOCK")

    def test_lock_rejects_a_non_sha256_hash(self) -> None:
        root = self.make_valid_root()
        self.edit_lock(root, "--hash=sha256:", "--hash=sha512:")
        self.assert_rule(root, "CI-PYTHON-LOCK")

    def test_lock_rejects_a_ranged_dependency(self) -> None:
        root = self.make_valid_root()
        self.edit_lock(root, "attrs==26.1.0", "attrs>=26.1.0")
        self.assert_rule(root, "CI-PYTHON-LOCK")

    def test_lock_rejects_a_duplicate_dependency(self) -> None:
        root = self.make_valid_root()
        lock = root / ".github/requirements/ci-validation.txt"
        lock.write_text(
            lock.read_text(encoding="utf-8")
            + "attrs==26.1.0 \\\n"
            + f"    --hash=sha256:{99:064x}\n",
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-LOCK")

    def test_lock_rejects_a_dropped_direct_dependency(self) -> None:
        root = self.make_valid_root()
        self.edit_lock(
            root,
            f"jsonschema==4.26.0 \\\n    --hash=sha256:{2:064x}\n",
            "",
        )
        self.assert_rule(root, "CI-PYTHON-LOCK")

    def test_lock_requires_the_binary_only_directive(self) -> None:
        root = self.make_valid_root()
        self.edit_lock(root, "--only-binary :all:\n", "")
        self.assert_rule(root, "CI-PYTHON-LOCK")

    def test_lock_hash_update_is_not_source_pinned(self) -> None:
        root = self.make_valid_root()
        self.edit_lock(root, f"{1:064x}", "a" * 64)
        VALIDATOR.validate_dependencies(root)

    def test_validation_job_rejects_absolute_python_path_pip_install(self) -> None:
        root = self.make_valid_root()
        workflow = root / ".github/workflows/ci.yml"
        text = workflow.read_text(encoding="utf-8")
        marker = "      - name: Inspect contract\n"
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
        marker = "      - name: Inspect contract\n"
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
        marker = "      - name: Inspect contract\n"
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
        marker = "      - name: Inspect contract\n"
        workflow.write_text(
            text.replace(
                marker,
                "      - run: env /usr/bin/python3 -m pip install rogue==1\n" + marker,
                1,
            ),
            encoding="utf-8",
        )
        self.assert_rule(root, "CI-PYTHON-WORKFLOW")

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
                self.assertEqual(VALIDATOR.validate_dependencies(root), 0)

    def test_non_validation_jobs_accept_safe_shell_controls(self) -> None:
        for command in PIP_INSTALL_SAFE_COMMANDS:
            with self.subTest(command=command):
                root = self.make_valid_root()
                self.inject_non_validation_job(root, command)
                self.assertEqual(VALIDATOR.validate_dependencies(root), 0)

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
                    self.assertEqual(VALIDATOR.validate_dependencies(root), 0)
                    root = self.make_valid_root()
                    self.inject_non_validation_job(root, safe)
                    self.assertEqual(VALIDATOR.validate_dependencies(root), 0)

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
                        self.assertEqual(VALIDATOR.validate_dependencies(root), 0)
                        root = self.make_valid_root()
                        self.inject_non_validation_job(root, command)
                        self.assertEqual(VALIDATOR.validate_dependencies(root), 0)

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
                self.assertEqual(VALIDATOR.validate_dependencies(root), 0)
                root = self.make_valid_root()
                self.inject_non_validation_job(root, command)
                self.assertEqual(VALIDATOR.validate_dependencies(root), 0)

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
                self.assertEqual(VALIDATOR.validate_dependencies(root), 0)
                root = self.make_valid_root()
                self.inject_non_validation_job(root, command)
                self.assertEqual(VALIDATOR.validate_dependencies(root), 0)

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
                        "      - name: Inspect contract\n",
                        mutation + "      - name: Inspect contract\n",
                        1,
                    )
                elif label == "job":
                    text = text.replace(
                        "  branch-policy:\n", "  branch-policy:\n" + mutation, 1
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

    def edit_pre_commit(self, root: Path, old: str, new: str) -> None:
        self.edit(root, ".pre-commit-config.yaml", old, new)

    def test_pre_commit_revision_and_tag_bump_passes(self) -> None:
        root = self.make_valid_root()
        revision, tag = PRE_COMMIT_REPOS["https://github.com/example/one"]
        self.edit_pre_commit(
            root,
            f"rev: {revision} # frozen: {tag}",
            f"rev: {'e' * 40} # frozen: v9.9.9",
        )
        self.assertEqual(VALIDATOR.validate_dependencies(root), 0)

    def test_pre_commit_non_commit_revisions_are_rejected(self) -> None:
        revision, _ = PRE_COMMIT_REPOS["https://github.com/example/one"]
        for label, bad in (
            ("tag", "v4.15.1"),
            ("branch", "main"),
            ("abbreviated", revision[:12]),
            ("uppercase", revision.upper()),
        ):
            with self.subTest(label=label):
                root = self.make_valid_root()
                self.edit_pre_commit(root, revision, bad)
                self.assert_rule(root, "CI-PRECOMMIT-REV")

    def test_pre_commit_missing_revision_is_rejected(self) -> None:
        root = self.make_valid_root()
        revision, tag = PRE_COMMIT_REPOS["https://github.com/example/one"]
        self.edit_pre_commit(root, f"    rev: {revision} # frozen: {tag}\n", "")
        self.assert_rule(root, "CI-PRECOMMIT-REV")

    def test_pre_commit_revision_without_frozen_comment_is_rejected(self) -> None:
        revision, tag = PRE_COMMIT_REPOS["https://github.com/example/one"]
        for replacement in (
            f"rev: {revision}",
            f"rev: {revision} # {tag}",
            f"rev: {revision} # frozen:",
            f"rev: {revision} # frozen: {tag} extra",
        ):
            with self.subTest(replacement=replacement):
                root = self.make_valid_root()
                self.edit_pre_commit(
                    root, f"rev: {revision} # frozen: {tag}", replacement
                )
                self.assert_rule(root, "CI-PRECOMMIT-REV")

    def test_pre_commit_frozen_comment_elsewhere_does_not_count(self) -> None:
        root = self.make_valid_root()
        revision, tag = PRE_COMMIT_REPOS["https://github.com/example/one"]
        line = f"    rev: {revision} # frozen: {tag}"
        self.edit_pre_commit(root, line, f"    rev: {revision}")
        config = root / ".pre-commit-config.yaml"
        config.write_text(
            config.read_text(encoding="utf-8") + f"\n# {line}\n", encoding="utf-8"
        )
        self.assert_rule(root, "CI-PRECOMMIT-REV")

    def test_pre_commit_duplicate_repository_is_rejected(self) -> None:
        root = self.make_valid_root()
        repo, (revision, tag) = next(iter(PRE_COMMIT_REPOS.items()))
        duplicate = (
            f"  - repo: {repo}\n"
            f"    rev: {revision} # frozen: {tag}\n"
            "    hooks:\n"
            "      - id: duplicate\n"
        )
        self.edit_pre_commit(root, "  - repo: local\n", duplicate + "  - repo: local\n")
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


class CiPythonShellGitSubcommandTests(unittest.TestCase):
    """Bound the git subcommands a workflow run step may name.

    An exact-SHA checkout detaches HEAD, so the workflow needs to name that
    commit and to read back what it named. The widening stops there: it stays
    an allowlist, and the execution-option guard still applies to it.
    """

    def _allowed(self, command: str) -> bool:
        try:
            VALIDATOR.shell_contains_pip_install(command)
        except VALIDATOR.ShellGuardError:
            return False
        return True

    def test_checkout_binding_subcommands_are_allowed(self):
        for command in (
            "git switch --force-create ci-validated-checkout",
            "git symbolic-ref --quiet HEAD",
            'test "$(git rev-parse HEAD)" = "$(git rev-parse ci-validated-checkout)"',
        ):
            with self.subTest(command=command):
                self.assertTrue(self._allowed(command))

    def test_subcommands_outside_the_allowlist_stay_rejected(self):
        for command in (
            "git push origin main",
            "git config core.hooksPath .githooks",
            "git fetch origin",
            "git commit --allow-empty -m drift",
            "git clean -xdf",
        ):
            with self.subTest(command=command):
                self.assertFalse(self._allowed(command))

    def test_submodule_recursion_is_still_refused_for_the_binding(self):
        """Recursion reaches content outside the validated checkout."""

        for command in (
            "git switch --recurse-submodules --force-create ci-validated-checkout",
            "git switch --recurse-submodules=yes -c ci-validated-checkout",
        ):
            with self.subTest(command=command):
                self.assertFalse(self._allowed(command))


class MetadataAndStyleCiContractTests(unittest.TestCase):
    def workflow(self):
        import copy

        return copy.deepcopy(
            VALIDATOR._load_yaml(
                (REPO_ROOT / ".github/workflows/ci.yml").read_text(),
                "CI-PYTHON-WORKFLOW",
                VALIDATOR.WORKFLOW_PATH,
            )
        )

    def test_workflow_rejects_inherited_execution_environment(self):
        workflow = self.workflow()
        workflow["env"] = {"NODE_OPTIONS": "--require ./candidate/payload.cjs"}
        with self.assertRaisesRegex(VALIDATOR.ContractError, "CI-TOPOLOGY"):
            VALIDATOR.validate_workflow(workflow)

    def test_summary_requires_pr_commit_range_producer(self):
        workflow = self.workflow()
        workflow["jobs"]["ci-summary"]["steps"] = workflow["jobs"]["ci-summary"][
            "steps"
        ][:4]
        with self.assertRaisesRegex(VALIDATOR.ContractError, "CI-TOPOLOGY"):
            VALIDATOR.validate_workflow(workflow)

    def test_summary_requires_present_matching_canonical_metadata_script(self):
        workflow = self.workflow()
        with tempfile.TemporaryDirectory(prefix="pr-metadata-contract-") as directory:
            root = Path(directory)
            source = root / "scripts/validate-pr-metadata.py"
            with self.assertRaisesRegex(VALIDATOR.ContractError, "CI-TOPOLOGY"):
                VALIDATOR.validate_workflow(workflow, root)
            source.parent.mkdir()
            source.write_bytes(
                (REPO_ROOT / VALIDATOR.PR_METADATA_SCRIPT_PATH).read_bytes()
            )
            VALIDATOR.validate_workflow(workflow, root)
            source.write_text(source.read_text() + "\n", encoding="utf-8")
            with self.assertRaisesRegex(VALIDATOR.ContractError, "CI-TOPOLOGY"):
                VALIDATOR.validate_workflow(workflow, root)

    def test_required_pr_metadata_cannot_skip_title_edits(self):
        import copy

        baseline = self.workflow()
        VALIDATOR.validate_workflow(baseline)
        for types in (
            ["opened", "synchronize", "reopened"],
            ["opened", "synchronize", "reopened", "edited", "ready_for_review"],
        ):
            with self.subTest(types=types):
                workflow = copy.deepcopy(baseline)
                events = workflow.get("on", workflow.get(True))
                events["pull_request"]["types"] = types
                with self.assertRaisesRegex(VALIDATOR.ContractError, "CI-TOPOLOGY"):
                    VALIDATOR.validate_workflow(workflow)

    def test_title_metadata_keeps_exact_trusted_base_and_fail_closed_code(self):
        import copy

        baseline = self.workflow()
        VALIDATOR.validate_workflow(baseline)
        variants = []
        workflow = copy.deepcopy(baseline)
        workflow["jobs"]["ci-summary"]["steps"][1]["with"]["ref"] = "${{ github.sha }}"
        variants.append(workflow)
        workflow = copy.deepcopy(baseline)
        workflow["jobs"]["ci-summary"]["steps"][1]["with"]["persist-credentials"] = True
        variants.append(workflow)
        workflow = copy.deepcopy(baseline)
        workflow["jobs"]["ci-summary"]["steps"][2]["with"]["fetch-depth"] = 1
        variants.append(workflow)
        workflow = copy.deepcopy(baseline)
        workflow["jobs"]["ci-summary"]["steps"][3]["uses"] = "actions/setup-python@v7"
        variants.append(workflow)
        workflow = copy.deepcopy(baseline)
        workflow["jobs"]["ci-summary"]["steps"][4]["env"]["PR_TITLE"] = (
            "${{ github.head_ref }}"
        )
        variants.append(workflow)
        workflow = copy.deepcopy(baseline)
        workflow["jobs"]["ci-summary"]["steps"][4]["run"] = "echo title-valid"
        variants.append(workflow)
        workflow = copy.deepcopy(baseline)
        workflow["jobs"]["ci-summary"]["steps"].pop(4)
        variants.append(workflow)
        for workflow in variants:
            with (
                self.subTest(workflow=workflow),
                self.assertRaises(VALIDATOR.ContractError),
            ):
                VALIDATOR.validate_workflow(workflow)

    def test_extra_hosted_jobs_and_qa_execution_are_rejected(self):
        for name in ("qa", "qa-source", "qa-isolated", "branch-policy"):
            workflow = self.workflow()
            workflow["jobs"][name] = {"steps": [{"run": RETIRED_HOSTED_QA_COMMAND}]}
            with self.subTest(job=name), self.assertRaises(VALIDATOR.ContractError):
                VALIDATOR.validate_workflow(workflow)

    def test_summary_rejects_permission_and_execution_drift(self):
        import copy

        baseline = self.workflow()
        variants = []
        workflow = copy.deepcopy(baseline)
        workflow["jobs"]["ci-summary"]["permissions"] = {"contents": "write"}
        variants.append(workflow)
        workflow = copy.deepcopy(baseline)
        workflow["jobs"]["ci-summary"]["steps"][0]["continue-on-error"] = True
        variants.append(workflow)
        workflow = copy.deepcopy(baseline)
        workflow["jobs"]["ci-summary"]["steps"][0]["if"] = "success()"
        variants.append(workflow)
        workflow = copy.deepcopy(baseline)
        workflow["jobs"]["ci-summary"]["steps"].append(
            {"run": RETIRED_HOSTED_QA_COMMAND}
        )
        variants.append(workflow)
        workflow = copy.deepcopy(baseline)
        workflow["jobs"]["ci-summary"]["steps"].append({"uses": "actions/checkout@abc"})
        variants.append(workflow)
        workflow = copy.deepcopy(baseline)
        workflow["jobs"]["ci-summary"]["needs"] = ["qa"]
        variants.append(workflow)
        for workflow in variants:
            with (
                self.subTest(workflow=workflow),
                self.assertRaises(VALIDATOR.ContractError),
            ):
                VALIDATOR.validate_workflow(workflow)

    def test_summary_requires_event_metadata_without_retired_qa_claims(self):
        import copy

        baseline = self.workflow()
        variants = []
        workflow = copy.deepcopy(baseline)
        workflow["jobs"]["ci-summary"]["steps"][0]["env"].pop("HEAD_REF")
        variants.append(workflow)
        for result in ("NOT_RUN", "PASS"):
            workflow = copy.deepcopy(baseline)
            step = workflow["jobs"]["ci-summary"]["steps"][0]
            step["run"] = step["run"].replace(
                'if [ "$branch_verdict" = FAIL ]; then',
                f"printf 'full-qa result={result} verdict={result}\\n'\n"
                'if [ "$branch_verdict" = FAIL ]; then',
                1,
            )
            variants.append(workflow)
        workflow = copy.deepcopy(baseline)
        workflow["jobs"]["ci-summary"]["steps"][0]["run"] = workflow["jobs"][
            "ci-summary"
        ]["steps"][0]["run"].replace("branch_verdict=FAIL", "branch_verdict=PASS")
        variants.append(workflow)
        for workflow in variants:
            with (
                self.subTest(workflow=workflow),
                self.assertRaises(VALIDATOR.ContractError),
            ):
                VALIDATOR.validate_workflow(workflow)

    def test_summary_rejects_early_success_before_branch_verdict(self):
        workflow = self.workflow()
        step = workflow["jobs"]["ci-summary"]["steps"][0]
        original = step["run"]
        for premature in (
            "exit 0\n",
            "exit\n",
            "exec true\n",
            ":; exit 0\n",
            "if true; then exit 0; fi\n",
            "branch_verdict=PASS\n",
        ):
            with self.subTest(premature=premature):
                step["run"] = original.replace(
                    "set -euo pipefail\n", "set -euo pipefail\n" + premature, 1
                )
                with self.assertRaisesRegex(VALIDATOR.ContractError, "CI-TOPOLOGY"):
                    VALIDATOR.validate_workflow(workflow)


class HostedStyleJobBoundaryTests(unittest.TestCase):
    def style_job(self):
        return {
            "if": "github.event_name == 'pull_request'",
            "runs-on": "ubuntu-latest",
            "timeout-minutes": 5,
            "permissions": {"contents": "read"},
            "steps": [
                {
                    "uses": CHECKOUT_ACTION,
                    "with": {
                        "ref": "${{ github.event.pull_request.base.sha }}",
                        "path": "trusted-base",
                        "persist-credentials": False,
                    },
                },
                {
                    "uses": CHECKOUT_ACTION,
                    "with": {
                        "path": "candidate",
                        "fetch-depth": 2,
                        "persist-credentials": False,
                    },
                },
                {
                    "uses": SETUP_PYTHON_ACTION,
                    "with": {"python-version": "3.12"},
                },
                {
                    "working-directory": "candidate",
                    "env": {"BASE_SHA": "${{ github.event.pull_request.base.sha }}"},
                    "run": (
                        "set -euo pipefail\n"
                        "umask 077\n"
                        'test "$(git rev-parse HEAD^1)" = "$BASE_SHA"\n'
                        "git diff --no-ext-diff --no-textconv --no-renames --name-only -z --diff-filter=ACMR "
                        'HEAD^1 HEAD > "$RUNNER_TEMP/pr-style-paths.z"'
                    ),
                },
                {
                    "run": (
                        "python -I -m pip install --disable-pip-version-check --only-binary=:all: "
                        "--require-hashes -r trusted-base/.github/requirements/ci-validation.txt"
                    )
                },
                {
                    "working-directory": "candidate",
                    "env": {"BASE_SHA": "${{ github.event.pull_request.base.sha }}"},
                    "run": (
                        "python -I ../trusted-base/scripts/validate-selected-style.py --root . "
                        "--config ../trusted-base/.pre-commit-config.yaml "
                        "--markdown-config ../trusted-base/.markdownlint-cli2.yaml "
                        "--ruff-config ../trusted-base/.ruff.toml "
                        '--paths-file "$RUNNER_TEMP/pr-style-paths.z" --delimiter nul '
                        '--expected-base-sha "$BASE_SHA"'
                    ),
                },
                {
                    "working-directory": "candidate",
                    "run": (
                        "set -euo pipefail\n"
                        "if grep -qz '^\\.github/requirements/' "
                        '"$RUNNER_TEMP/pr-style-paths.z"; then\n'
                        "  python -I ../trusted-base/scripts/validate-ci-python-contract.py "
                        "--root .\n"
                        "fi"
                    ),
                },
            ],
        }

    def test_style_job_rejects_untrusted_or_mutable_inputs(self):
        import copy

        VALIDATOR._validate_style_pr_job(self.style_job(), ACTIONS)
        cases = (
            (
                6,
                "run",
                "set -euo pipefail\n"
                "if grep -qz '^\\.github/requirements/' "
                '"$RUNNER_TEMP/pr-style-paths.z"; then\n'
                "  python -I scripts/validate-ci-python-contract.py --root .\n"
                "fi",
            ),
            (0, "uses", "actions/checkout@v7"),
            (
                0,
                "with",
                {
                    "ref": "${{ github.head_ref }}",
                    "path": "trusted-base",
                    "persist-credentials": False,
                },
            ),
            (
                1,
                "with",
                {"path": "candidate", "fetch-depth": 2, "persist-credentials": True},
            ),
            (4, "run", "python -m pip install pre-commit"),
            (5, "run", "python scripts/validate-selected-style.py --root . || true"),
            (
                4,
                "run",
                self.style_job()["steps"][4]["run"].replace("python -I", "python", 1),
            ),
            (
                5,
                "run",
                self.style_job()["steps"][5]["run"].replace("python -I", "python", 1),
            ),
        )
        for index, key, value in cases:
            with self.subTest(index=index, key=key, value=value):
                job = copy.deepcopy(self.style_job())
                job["steps"][index][key] = value
                with self.assertRaises(VALIDATOR.ContractError):
                    VALIDATOR._validate_style_pr_job(job, ACTIONS)

    def test_style_job_rejects_permission_and_event_drift(self):
        for key, value in (
            ("if", "always()"),
            ("permissions", {"contents": "write"}),
            ("timeout-minutes", 11),
        ):
            with self.subTest(key=key):
                job = self.style_job()
                job[key] = value
                with self.assertRaises(VALIDATOR.ContractError):
                    VALIDATOR._validate_style_pr_job(job, ACTIONS)


if __name__ == "__main__":
    unittest.main()
