#!/usr/bin/env python3
"""Validate the exact network-free CI Python and pre-commit contract."""

from __future__ import annotations

import argparse
import os
import re
import shlex
import stat
from pathlib import Path
from typing import Any, NoReturn

import yaml


DIRECT_REQUIREMENTS_PATH = Path(".github/requirements/ci-validation.in")
LOCK_PATH = Path(".github/requirements/ci-validation.txt")
WORKFLOW_PATH = Path(".github/workflows/ci.yml")
PRE_COMMIT_CONFIG_PATH = Path(".pre-commit-config.yaml")
CANDIDATE_SHA_REF = "${{ github.sha }}"
EXPECTED_REQUIREMENT_LINES = (
    "jsonschema==4.26.0",
    "pre-commit==4.6.1",
    "PyYAML==6.0.3",
)
EXPECTED_PINS = {
    "jsonschema": "4.26.0",
    "pre-commit": "4.6.1",
    "pyyaml": "6.0.3",
}
EXPECTED_RESOLVED_PINS = {
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
EXPECTED_PRE_COMMIT_REVISIONS = {
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
EXPECTED_PRE_COMMIT_SOURCE_TAGS = {
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
GITLEAKS_SHA256 = "79a3ab579b53f71efd634f3aaf7e04a0fa0cf206b7ed434638d1547a2470a66e"  # pragma: allowlist secret
EXPECTED_GITLEAKS_TOOL = {
    "version": "8.30.0",
    "asset": "gitleaks_8.30.0_linux_x64.tar.gz",
    "sha256": GITLEAKS_SHA256,
    "install_path": "/usr/local/bin/gitleaks",
}
EXPECTED_PYTHON = "3.12"
VALIDATION_JOBS = ("qa",)
INSTALL_COMMAND = (
    "python -m pip install --disable-pip-version-check "
    "--only-binary :all: --require-hashes "
    "--requirement .github/requirements/ci-validation.txt"
)
QA_COMMAND = 'python3 scripts/qa.py ci --base-ref "$BASE_SHA"'
GITLEAKS_JOBS = ("qa",)
GITLEAKS_INSTALL_COMMAND = f"""\
set -euo pipefail
curl --fail --location --silent --show-error \\
  https://github.com/gitleaks/gitleaks/releases/download/v8.30.0/gitleaks_8.30.0_linux_x64.tar.gz \\
  --output "$RUNNER_TEMP/gitleaks_8.30.0_linux_x64.tar.gz"
gitleaks_sha256='{GITLEAKS_SHA256}' # pragma: allowlist secret
printf '%s  %s\\n' "$gitleaks_sha256" "$RUNNER_TEMP/gitleaks_8.30.0_linux_x64.tar.gz" | sha256sum --check --strict
tar -xzf "$RUNNER_TEMP/gitleaks_8.30.0_linux_x64.tar.gz" -C "$RUNNER_TEMP" gitleaks
sudo install -o root -g root -m 0755 "$RUNNER_TEMP/gitleaks" /usr/local/bin/gitleaks"""
PIN_PATTERN = re.compile(
    r"^(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)"
    r"==(?P<version>[A-Za-z0-9][A-Za-z0-9.+_-]*)$"
)
HASH_PATTERN = re.compile(r"^--hash=sha256:(?P<digest>[0-9a-f]{64})$")
FULL_COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
MAX_SHELL_COMMAND_CHARS = 65536
MAX_SHELL_RECURSION = 6
SHELL_RESERVED_PREFIXES = frozenset(
    {
        "case",
        "do",
        "done",
        "elif",
        "else",
        "esac",
        "fi",
        "for",
        "if",
        "in",
        "select",
        "then",
        "until",
        "while",
        "{",
        "}",
    }
)
SHELL_WRAPPERS = frozenset(
    {"command", "env", "exec", "nohup", "sudo", "time", "nice", "setsid", "timeout"}
)
SHELL_INTERPRETERS = frozenset({"bash", "dash", "ksh", "sh", "zsh"})
SHELL_UNSUPPORTED_EXECUTABLES = frozenset(
    {".", "alias", "builtin", "coproc", "eval", "function", "source"}
)
SHELL_EXPLICIT_SAFE_COMMANDS = frozenset(
    {
        "[",
        "[[",
        "curl",
        "echo",
        "exit",
        "false",
        "grep",
        "install",
        "mypython",
        "pipx",
        "pre-commit",
        "printf",
        "set",
        "sha256sum",
        "tar",
        "test",
        "true",
    }
)
TAR_EXECUTION_LONG_OPTIONS = frozenset(
    {
        "--checkpoint-action",
        "--compress-program",
        "--filter",
        "--info-script",
        "--new-volume-script",
        "--rmt-command",
        "--rsh-command",
        "--to-command",
        "--use-compress-program",
    }
)
GIT_EXECUTION_LONG_OPTIONS_BY_SUBCOMMAND = {
    "cat-file": {
        "--filters": "--fi",
        "--textconv": "--t",
    },
    "diff": {
        "--ext-diff": "--ext",
        "--textconv": "--textc",
    },
}
GIT_EXACT_SAFE_LONG_OPTIONS_BY_SUBCOMMAND = {
    "diff": frozenset({"--text"}),
}
INSTALL_EXECUTION_LONG_OPTIONS = frozenset({"--strip", "--strip-program"})
PIP_GLOBAL_OPTIONS_WITH_VALUE = frozenset(
    {
        "--cache-dir",
        "--cert",
        "--client-cert",
        "--default-timeout",
        "--exists-action",
        "--keyring-provider",
        "--local-log",
        "--log",
        "--log-file",
        "--proxy",
        "--python",
        "--resume-retries",
        "--retries",
        "--timeout",
        "--trusted-host",
        "--use-deprecated",
        "--use-feature",
    }
)
PIP_GLOBAL_FLAG_OPTIONS = frozenset(
    {
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
    }
)
PIP_GLOBAL_SHORT_FLAG_CHARACTERS = frozenset("hqvV")
WRAPPER_OPTIONS_WITH_VALUE = {
    "env": frozenset({"-C", "--chdir", "-u", "--unset"}),
    "exec": frozenset({"-a"}),
    "sudo": frozenset(
        {
            "-C",
            "-D",
            "-R",
            "-T",
            "-U",
            "-g",
            "-h",
            "-p",
            "-r",
            "-t",
            "-u",
            "--chdir",
            "--close-from",
            "--group",
            "--host",
            "--other-user",
            "--prompt",
            "--role",
            "--type",
            "--user",
        }
    ),
    "time": frozenset({"-f", "-o", "--format", "--output"}),
    "nice": frozenset({"-n", "--adjustment"}),
    "timeout": frozenset({"-k", "--kill-after"}),
}


class ContractError(ValueError):
    """A stable CI Python contract finding."""

    def __init__(self, rule_id: str, detail: str):
        self.rule_id = rule_id
        self.detail = detail
        super().__init__(f"{rule_id}: {detail}")


def fail(rule_id: str, detail: str) -> NoReturn:
    raise ContractError(rule_id, detail)


class ShellGuardError(ValueError):
    """A bounded shell command could not be classified safely."""


def _shell_guard_error() -> NoReturn:
    raise ShellGuardError("shell command is outside the bounded grammar")


def _is_shell_comment_start(text: str, index: int) -> bool:
    return index == 0 or text[index - 1].isspace() or text[index - 1] in ";&|()"


def _find_command_substitution_end(text: str, start: int) -> int:
    depth = 1
    quote: str | None = None
    index = start + 2
    while index < len(text):
        character = text[index]
        if quote == "'":
            if character == "'":
                quote = None
            index += 1
            continue
        if character == '"':
            quote = None if quote == '"' else '"'
            index += 1
            continue
        if character == "'" and quote is None:
            quote = "'"
            index += 1
            continue
        if character == "\\":
            index += 2
            continue
        if (
            quote is None
            and character == "#"
            and _is_shell_comment_start(
                text,
                index,
            )
        ):
            newline = text.find("\n", index)
            if newline < 0:
                _shell_guard_error()
            index = newline + 1
            continue
        if character == "$" and index + 1 < len(text) and text[index + 1] == "(":
            depth += 1
            index += 2
            continue
        if quote is None and character == "(":
            depth += 1
        elif quote is None and character == ")":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    _shell_guard_error()


def _mask_and_check_command_substitutions(
    text: str,
    recursion: int,
) -> tuple[str, bool]:
    output: list[str] = []
    quote: str | None = None
    index = 0
    while index < len(text):
        character = text[index]
        if quote == "'":
            output.append(character)
            if character == "'":
                quote = None
            index += 1
            continue
        if character == "\\":
            output.append(character)
            if index + 1 < len(text):
                output.append(text[index + 1])
            index += 2
            continue
        if character == "'" and quote is None:
            quote = "'"
            output.append(character)
            index += 1
            continue
        if character == '"':
            quote = None if quote == '"' else '"'
            output.append(character)
            index += 1
            continue
        if (
            quote is None
            and character == "#"
            and _is_shell_comment_start(
                text,
                index,
            )
        ):
            newline = text.find("\n", index)
            if newline < 0:
                output.append(text[index:])
                break
            output.append(text[index:newline])
            output.append("\n")
            index = newline + 1
            continue
        if character == "$" and index + 1 < len(text) and text[index + 1] == "(":
            end = _find_command_substitution_end(text, index)
            payload = text[index + 2 : end]
            if _shell_contains_pip_install(payload, recursion + 1):
                return "", True
            output.append("__command_substitution__")
            index = end + 1
            continue
        if character == "`":
            end = index + 1
            while end < len(text):
                if text[end] == "\\":
                    end += 2
                    continue
                if text[end] == "`":
                    break
                end += 1
            if end >= len(text):
                _shell_guard_error()
            if _shell_contains_pip_install(text[index + 1 : end], recursion + 1):
                return "", True
            output.append("__command_substitution__")
            index = end + 1
            continue
        output.append(character)
        index += 1
    return "".join(output), False


def _is_shell_control_token(token: str) -> bool:
    return bool(token) and all(character in ";&|()!" for character in token)


def _mask_shell_quoted_text(text: str) -> str:
    output: list[str] = []
    quote: str | None = None
    index = 0
    while index < len(text):
        character = text[index]
        if character == "\\" and quote != "'":
            output.append(" ")
            if index + 1 < len(text):
                output.append(" ")
            index += 2
            continue
        if (
            quote is None
            and character == "#"
            and _is_shell_comment_start(
                text,
                index,
            )
        ):
            newline = text.find("\n", index)
            if newline < 0:
                output.extend(" " for _ in text[index:])
                return "".join(output)
            output.extend(" " for _ in text[index:newline])
            output.append("\n")
            index = newline + 1
            continue
        if character in {"'", '"'}:
            if quote == character:
                quote = None
            elif quote is None:
                quote = character
            output.append(" ")
        elif character == "\n" and quote is not None:
            _shell_guard_error()
        elif quote is None:
            output.append(character)
        else:
            output.append(" ")
        index += 1
    return "".join(output)


def _shell_simple_commands(text: str) -> list[list[str]]:
    unsupported = (
        r"(?:^|[;|&()\n])[ \t]*(?:function|coproc|alias|source|builtin|eval)[ \t]",
        r"(?:^|[;|&()\n])[ \t]*\.[ \t]",
        r"(?:^|[;|&()\n])[A-Za-z_][A-Za-z0-9_]*[ \t]*=\s*\(",
        r"(?:^|[;|&()\n])[A-Za-z_][A-Za-z0-9_]*\s*\(\)\s*\{",
        r"(?:<<|<\(|>\()",
        r"\|[ \t]*(?:sh|bash|dash|ksh|zsh)(?:[ \t]|$)",
    )
    syntax_text = _mask_shell_quoted_text(text)
    if any(re.search(pattern, syntax_text) for pattern in unsupported):
        _shell_guard_error()
    commands: list[list[str]] = []
    case_pattern_expected: list[bool] = []
    for line in text.splitlines() or [""]:
        stripped_line = line.strip()
        if re.fullmatch(r"case\b.*\bin", stripped_line):
            case_pattern_expected.append(True)
            continue
        if stripped_line == "esac":
            if not case_pattern_expected:
                _shell_guard_error()
            case_pattern_expected.pop()
            continue
        if case_pattern_expected and case_pattern_expected[-1]:
            if not re.fullmatch(
                r"[A-Za-z0-9_.*?:-]+(?:\|[A-Za-z0-9_.*?:-]+)*\)",
                stripped_line,
            ):
                _shell_guard_error()
            case_pattern_expected[-1] = False
            continue
        if case_pattern_expected and stripped_line == ";;":
            case_pattern_expected[-1] = True
            continue
        lexer = shlex.shlex(
            line,
            posix=True,
            punctuation_chars=";&|()",
        )
        lexer.commenters = "#"
        lexer.whitespace_split = True
        try:
            tokens = list(lexer)
        except ValueError:
            _shell_guard_error()
        current: list[str] = []
        case_header = False
        redirection_target = False
        for token in tokens:
            if redirection_target:
                current.append(token)
                redirection_target = False
                continue
            if token == "case" and not current:
                case_header = True
                continue
            if case_header:
                if token == "in":
                    case_header = False
                continue
            if _is_shell_control_token(token):
                if (
                    token == "&"
                    and current
                    and current[-1]
                    in {
                        "<",
                        "<<",
                        ">",
                        ">>",
                    }
                ):
                    current.append(token)
                    redirection_target = True
                    continue
                if current:
                    commands.append(current)
                    current = []
                continue
            if not current and token in SHELL_RESERVED_PREFIXES:
                continue
            current.append(token)
        if current:
            commands.append(current)
    if case_pattern_expected:
        _shell_guard_error()
    return commands


def _shell_basename(token: str) -> str:
    return token.rsplit("/", 1)[-1]


def _is_shell_assignment(token: str) -> bool:
    name, separator, _ = token.partition("=")
    return bool(
        separator
        and name
        and (name[0].isalpha() or name[0] == "_")
        and all(character.isalnum() or character == "_" for character in name)
    )


def _is_versioned_launcher(name: str, prefix: str) -> bool:
    if name == prefix:
        return True
    if not name.startswith(prefix):
        return False
    suffix = name[len(prefix) :]
    components = suffix.split(".")
    return (
        bool(suffix)
        and len(components) <= 2
        and all(component.isdecimal() and component for component in components)
    )


def _is_dynamic_shell_word(token: str) -> bool:
    return "$" in token or "`" in token or "__command_substitution__" in token


def _pip_subcommand(arguments: list[str]) -> str:
    """Return the bounded effective pip subcommand after supported globals."""
    index = 0
    while index < len(arguments):
        token = arguments[index]
        if _is_dynamic_shell_word(token):
            _shell_guard_error()
        if not token.startswith("-"):
            return token

        if token.startswith("--"):
            name, separator, inline_value = token.partition("=")
            if name in PIP_GLOBAL_OPTIONS_WITH_VALUE:
                if separator:
                    if not inline_value or _is_dynamic_shell_word(inline_value):
                        _shell_guard_error()
                    index += 1
                    continue
                if index + 1 >= len(arguments):
                    _shell_guard_error()
                value = arguments[index + 1]
                if not value or _is_dynamic_shell_word(value):
                    _shell_guard_error()
                index += 2
                continue
            if name in PIP_GLOBAL_FLAG_OPTIONS and not separator:
                index += 1
                continue
            _shell_guard_error()

        short_flags = token[1:]
        if not short_flags or any(
            flag not in PIP_GLOBAL_SHORT_FLAG_CHARACTERS for flag in short_flags
        ):
            _shell_guard_error()
        index += 1

    _shell_guard_error()


def _wrapper_target_index(
    words: list[str],
    start: int,
    wrapper: str,
    recursion: int,
) -> tuple[int, bool]:
    index = start + 1
    while index < len(words):
        token = words[index]
        option_name = token.split("=", 1)[0]
        if wrapper == "sudo" and (
            option_name in {"--login", "--shell"}
            or (
                token.startswith("-")
                and not token.startswith("--")
                and any(option in token[1:] for option in "is")
            )
        ):
            _shell_guard_error()
        if token == "--":
            return index + 1, False
        if wrapper == "command" and token in {"-v", "-V"}:
            return len(words), False
        if wrapper == "env" and token in {"-S", "--split-string"}:
            if index + 1 >= len(words):
                _shell_guard_error()
            return len(words), _shell_contains_pip_install(
                words[index + 1],
                recursion + 1,
            )
        if wrapper == "env" and token.startswith("--split-string="):
            return len(words), _shell_contains_pip_install(
                token.split("=", 1)[1],
                recursion + 1,
            )
        if _is_shell_assignment(token):
            index += 1
            continue
        if token.startswith("-") and token != "-":
            if (
                option_name
                in WRAPPER_OPTIONS_WITH_VALUE.get(
                    wrapper,
                    frozenset(),
                )
                and "=" not in token
            ):
                if index + 1 >= len(words):
                    _shell_guard_error()
                index += 2
            else:
                index += 1
            continue
        if wrapper == "timeout":
            if index + 1 >= len(words):
                _shell_guard_error()
            return index + 1, False
        return index, False
    return index, False


def _tar_has_execution_option(arguments: list[str]) -> bool:
    for argument in arguments:
        option_name = argument.split("=", 1)[0]
        if any(
            dangerous.startswith(option_name)
            for dangerous in TAR_EXECUTION_LONG_OPTIONS
            if len(option_name) > 3
        ):
            return True
        if argument.startswith("-") and not argument.startswith("--"):
            if "I" in argument[1:] or "F" in argument[1:]:
                return True
    if arguments and re.fullmatch(r"[A-Za-z]+", arguments[0]):
        if "I" in arguments[0] or "F" in arguments[0]:
            return True
    return False


def _arguments_have_long_option(
    arguments: list[str],
    forbidden: frozenset[str],
) -> bool:
    return any(argument.split("=", 1)[0] in forbidden for argument in arguments)


def _git_has_execution_option(
    subcommand: str,
    arguments: list[str],
) -> bool:
    forbidden = GIT_EXECUTION_LONG_OPTIONS_BY_SUBCOMMAND.get(
        subcommand,
        {},
    )
    exact_safe = GIT_EXACT_SAFE_LONG_OPTIONS_BY_SUBCOMMAND.get(
        subcommand,
        frozenset(),
    )
    for argument in arguments:
        if argument == "--":
            break
        option_name = argument.split("=", 1)[0]
        if option_name in exact_safe:
            continue
        if any(
            len(option_name) >= len(minimum_prefix)
            and dangerous.startswith(option_name)
            for dangerous, minimum_prefix in forbidden.items()
        ):
            return True
    return False


def _simple_command_is_allowed(executable: str, arguments: list[str]) -> bool:
    if executable not in SHELL_EXPLICIT_SAFE_COMMANDS:
        return False
    if executable == "tar" and _tar_has_execution_option(arguments):
        _shell_guard_error()
    if executable == "install" and (
        _arguments_have_long_option(arguments, INSTALL_EXECUTION_LONG_OPTIONS)
        or any(
            argument.startswith("-")
            and not argument.startswith("--")
            and "s" in argument[1:]
            for argument in arguments
        )
    ):
        _shell_guard_error()
    if executable == "set" and arguments != ["-euo", "pipefail"]:
        _shell_guard_error()
    if executable == "pre-commit" and arguments != [
        "run",
        "--all-files",
        "--show-diff-on-failure",
    ]:
        _shell_guard_error()
    if executable == "exit" and (len(arguments) != 1 or not arguments[0].isdecimal()):
        _shell_guard_error()
    return True


def _simple_command_contains_pip_install(
    words: list[str],
    recursion: int,
) -> bool:
    index = 0
    while index < len(words) and _is_shell_assignment(words[index]):
        index += 1

    wrapper_count = 0
    while index < len(words):
        executable = _shell_basename(words[index])
        if executable not in SHELL_WRAPPERS:
            break
        wrapper_count += 1
        if wrapper_count > len(words):
            _shell_guard_error()
        index, nested_install = _wrapper_target_index(
            words,
            index,
            executable,
            recursion,
        )
        if nested_install:
            return True
        while index < len(words) and _is_shell_assignment(words[index]):
            index += 1

    if index >= len(words):
        return False

    executable = _shell_basename(words[index])
    arguments = words[index + 1 :]
    if executable in SHELL_UNSUPPORTED_EXECUTABLES:
        _shell_guard_error()
    if executable in SHELL_INTERPRETERS:
        for option_index, option in enumerate(arguments):
            has_command_payload = option in {"-c", "--command"} or (
                option.startswith("-")
                and not option.startswith("--")
                and "c" in option[1:]
            )
            if not has_command_payload:
                continue
            if option_index + 1 >= len(arguments):
                _shell_guard_error()
            if _is_dynamic_shell_word(arguments[option_index + 1]):
                _shell_guard_error()
            return _shell_contains_pip_install(
                arguments[option_index + 1],
                recursion + 1,
            )
        if not arguments:
            _shell_guard_error()
        script_index = 1 if arguments[0] == "--" else 0
        if script_index >= len(arguments):
            _shell_guard_error()
        script = arguments[script_index]
        if (
            script == "-"
            or script.startswith("-")
            or script.startswith("<")
            or _is_dynamic_shell_word(script)
        ):
            _shell_guard_error()
        return False

    if _is_dynamic_shell_word(words[index]):
        _shell_guard_error()

    if _is_versioned_launcher(executable, "pip"):
        return _pip_subcommand(arguments) == "install"

    if not _is_versioned_launcher(executable, "python"):
        if _simple_command_is_allowed(executable, arguments):
            return False
        if (
            executable == "git"
            and arguments
            and arguments[0]
            in {
                "cat-file",
                "diff",
                "ls-tree",
            }
        ):
            if _git_has_execution_option(arguments[0], arguments[1:]):
                _shell_guard_error()
            return False
        _shell_guard_error()
    if any(
        argument in {"-c", "--command"}
        or (
            argument.startswith("-")
            and not argument.startswith("--")
            and "c" in argument[1:]
        )
        for argument in arguments
    ):
        _shell_guard_error()
    for module_index, argument in enumerate(arguments):
        if argument != "-m" or module_index + 1 >= len(arguments):
            continue
        module = arguments[module_index + 1]
        remaining = arguments[module_index + 2 :]
        if _is_dynamic_shell_word(module):
            _shell_guard_error()
        if module == "pip" or module.startswith("pip."):
            return _pip_subcommand(remaining) == "install"
        return False
    if not arguments:
        _shell_guard_error()
    if _is_dynamic_shell_word(arguments[0]) or arguments[0] == "-":
        _shell_guard_error()
    return False


def _shell_contains_pip_install(text: str, recursion: int = 0) -> bool:
    if recursion > MAX_SHELL_RECURSION:
        _shell_guard_error()
    if len(text) > MAX_SHELL_COMMAND_CHARS or "\0" in text:
        _shell_guard_error()
    normalized = text.replace("\\\r\n", "").replace("\\\n", "")
    masked, nested_install = _mask_and_check_command_substitutions(
        normalized,
        recursion,
    )
    if nested_install:
        return True
    return any(
        _simple_command_contains_pip_install(command, recursion)
        for command in _shell_simple_commands(masked)
    )


def shell_contains_pip_install(text: str) -> bool:
    """Return whether a bounded shell command owns a Python package install."""

    return _shell_contains_pip_install(text)


def _guarded_pip_install(command: str) -> bool:
    try:
        return shell_contains_pip_install(command)
    except ShellGuardError:
        fail(
            "CI-PYTHON-WORKFLOW",
            "workflow shell command is outside the bounded install grammar",
        )


def canonical_package_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


class DuplicateKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects every duplicate mapping key."""


def _construct_mapping_without_duplicates(
    loader: DuplicateKeyLoader,
    node: yaml.MappingNode,
    deep: bool = False,
) -> dict[Any, Any]:
    seen: set[Any] = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in seen
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                None,
                None,
                "unhashable YAML mapping key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise yaml.constructor.ConstructorError(
                None,
                None,
                f"duplicate YAML mapping key: {key!r}",
                key_node.start_mark,
            )
        seen.add(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


DuplicateKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping_without_duplicates,
)


DIRECTORY_OPEN_FLAGS = (
    os.O_RDONLY
    | getattr(os, "O_CLOEXEC", 0)
    | getattr(os, "O_DIRECTORY", 0)
    | getattr(os, "O_NOFOLLOW", 0)
)
REGULAR_FILE_OPEN_FLAGS = (
    os.O_RDONLY
    | getattr(os, "O_CLOEXEC", 0)
    | getattr(os, "O_NOFOLLOW", 0)
    | getattr(os, "O_NONBLOCK", 0)
)


def _close_descriptor(descriptor: int) -> None:
    if descriptor < 0:
        return
    try:
        os.close(descriptor)
    except OSError:
        pass


def _same_identity(checked: os.stat_result, opened: os.stat_result) -> bool:
    return (checked.st_dev, checked.st_ino) == (
        opened.st_dev,
        opened.st_ino,
    )


def _open_repository_root(root: Path) -> tuple[Path, int]:
    raw_root = Path(root)
    if any(part == ".." for part in raw_root.parts):
        fail("CI-PYTHON-INPUT", "repository root is invalid")
    try:
        absolute_root = Path(os.path.abspath(os.fspath(raw_root)))
    except (OSError, TypeError, ValueError):
        fail("CI-PYTHON-INPUT", "repository root is unavailable")

    root_descriptor = -1
    next_descriptor = -1
    try:
        anchor = Path(absolute_root.anchor)
        try:
            checked = os.lstat(anchor)
        except OSError:
            fail("CI-PYTHON-INPUT", "repository root is unavailable")
        if stat.S_ISLNK(checked.st_mode) or not stat.S_ISDIR(checked.st_mode):
            fail("CI-PYTHON-INPUT", "repository root is not a real directory")
        try:
            root_descriptor = os.open(anchor, DIRECTORY_OPEN_FLAGS)
            opened = os.fstat(root_descriptor)
        except OSError:
            fail("CI-PYTHON-INPUT", "repository root is unavailable")
        if not stat.S_ISDIR(opened.st_mode) or not _same_identity(
            checked,
            opened,
        ):
            fail("CI-PYTHON-INPUT", "repository root identity changed")

        for part in absolute_root.parts[1:]:
            try:
                checked = os.lstat(part, dir_fd=root_descriptor)
            except OSError:
                fail("CI-PYTHON-INPUT", "repository root is unavailable")
            if stat.S_ISLNK(checked.st_mode):
                fail(
                    "CI-PYTHON-INPUT",
                    "repository root path contains a symlink",
                )
            if not stat.S_ISDIR(checked.st_mode):
                fail(
                    "CI-PYTHON-INPUT",
                    "repository root is not a real directory",
                )
            try:
                next_descriptor = os.open(
                    part,
                    DIRECTORY_OPEN_FLAGS,
                    dir_fd=root_descriptor,
                )
                opened = os.fstat(next_descriptor)
            except OSError:
                fail("CI-PYTHON-INPUT", "repository root is unavailable")
            if not stat.S_ISDIR(opened.st_mode) or not _same_identity(
                checked,
                opened,
            ):
                fail("CI-PYTHON-INPUT", "repository root identity changed")
            _close_descriptor(root_descriptor)
            root_descriptor = next_descriptor
            next_descriptor = -1

        try:
            real_root = Path(os.path.realpath(absolute_root, strict=True))
        except (OSError, TypeError, ValueError):
            fail("CI-PYTHON-INPUT", "repository root is unavailable")
        if real_root != absolute_root:
            fail("CI-PYTHON-INPUT", "repository root path is not real")
        result_descriptor = root_descriptor
        root_descriptor = -1
        return absolute_root, result_descriptor
    finally:
        _close_descriptor(next_descriptor)
        _close_descriptor(root_descriptor)


def _resolve_repository_root(root: Path) -> Path:
    absolute_root, descriptor = _open_repository_root(root)
    _close_descriptor(descriptor)
    return absolute_root


def _canonical_relative_path(relative: Path, rule_id: str) -> Path:
    raw = os.fspath(relative)
    normalized = Path(raw)
    if (
        not raw
        or normalized.is_absolute()
        or raw != normalized.as_posix()
        or "\\" in raw
        or not normalized.parts
        or any(part in {"", ".", ".."} for part in normalized.parts)
    ):
        fail(rule_id, "governed input path is invalid")
    return normalized


def _open_regular_file(root: Path, relative: Path, rule_id: str) -> int:
    canonical = _canonical_relative_path(relative, rule_id)
    _, parent_descriptor = _open_repository_root(root)
    next_descriptor = -1
    final_descriptor = -1
    try:
        for index, part in enumerate(canonical.parts):
            final_component = index == len(canonical.parts) - 1
            try:
                checked = os.lstat(part, dir_fd=parent_descriptor)
            except OSError:
                fail(rule_id, "governed input is unavailable")
            if not final_component:
                if stat.S_ISLNK(checked.st_mode) or not stat.S_ISDIR(checked.st_mode):
                    fail(
                        rule_id,
                        "governed input parent is not a real directory",
                    )
                try:
                    next_descriptor = os.open(
                        part,
                        DIRECTORY_OPEN_FLAGS,
                        dir_fd=parent_descriptor,
                    )
                    opened = os.fstat(next_descriptor)
                except OSError:
                    fail(rule_id, "governed input is unavailable")
                if not stat.S_ISDIR(opened.st_mode) or not _same_identity(
                    checked,
                    opened,
                ):
                    fail(rule_id, "governed input parent identity changed")
                _close_descriptor(parent_descriptor)
                parent_descriptor = next_descriptor
                next_descriptor = -1
                continue
            if stat.S_ISLNK(checked.st_mode) or not stat.S_ISREG(checked.st_mode):
                fail(
                    rule_id,
                    "governed input must be a regular non-symlink file",
                )
            try:
                final_descriptor = os.open(
                    part,
                    REGULAR_FILE_OPEN_FLAGS,
                    dir_fd=parent_descriptor,
                )
                opened = os.fstat(final_descriptor)
            except OSError:
                fail(rule_id, "governed input is unavailable")
            if not stat.S_ISREG(opened.st_mode) or not _same_identity(
                checked,
                opened,
            ):
                fail(rule_id, "governed input final identity changed")
            result_descriptor = final_descriptor
            final_descriptor = -1
            return result_descriptor
    finally:
        _close_descriptor(final_descriptor)
        _close_descriptor(next_descriptor)
        _close_descriptor(parent_descriptor)
    fail(rule_id, "governed input path is invalid")


def _read_regular_text(root: Path, relative: Path, rule_id: str) -> str:
    descriptor = _open_regular_file(root, relative, rule_id)
    try:
        with os.fdopen(descriptor, "r", encoding="utf-8") as stream:
            descriptor = -1
            return stream.read()
    except ContractError:
        raise
    except (OSError, UnicodeError):
        fail(rule_id, "governed input cannot be read as UTF-8")
    finally:
        _close_descriptor(descriptor)


def _load_yaml(text: str, rule_id: str, source: Path) -> dict[str, Any]:
    try:
        value = yaml.load(text, Loader=DuplicateKeyLoader)
    except yaml.YAMLError as exc:
        fail(rule_id, f"{source.as_posix()} YAML is invalid: {exc}")
    if not isinstance(value, dict):
        fail(rule_id, f"{source.as_posix()} YAML root must be a mapping")
    return value


def _validate_direct_requirements(text: str) -> None:
    expected_text = "\n".join(EXPECTED_REQUIREMENT_LINES) + "\n"
    if text != expected_text:
        fail(
            "CI-PYTHON-PIN",
            f"{DIRECT_REQUIREMENTS_PATH.as_posix()} must contain exactly the three ordered pins",
        )

    observed: dict[str, str] = {}
    for line in text.splitlines():
        match = PIN_PATTERN.fullmatch(line)
        if match is None:
            fail("CI-PYTHON-PIN", "every dependency must use one exact == pin")
        package = canonical_package_name(match.group("name"))
        if package in observed:
            fail("CI-PYTHON-PIN", f"duplicate dependency name: {package}")
        observed[package] = match.group("version")
    if observed != EXPECTED_PINS:
        fail("CI-PYTHON-PIN", "dependency names or versions differ")


def _lock_entries(text: str) -> tuple[dict[str, str], int]:
    entries: list[str] = []
    current: list[str] = []
    binary_directive_count = 0
    expecting_hash = False
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "--only-binary :all:":
            if current:
                fail(
                    "CI-PYTHON-LOCK",
                    "binary-only directive must precede every requirement",
                )
            binary_directive_count += 1
            continue
        if stripped.startswith("--") and not raw_line[:1].isspace():
            fail("CI-PYTHON-LOCK", "unexpected global lock directive")
        if raw_line[:1].isspace():
            if not current or not expecting_hash:
                fail("CI-PYTHON-LOCK", "orphaned lock continuation")
            has_continuation = stripped.endswith("\\")
            current.append(stripped[:-1].rstrip() if has_continuation else stripped)
            expecting_hash = has_continuation
            continue
        elif current:
            if expecting_hash:
                fail("CI-PYTHON-LOCK", "locked requirement has a dangling continuation")
            entries.append(" ".join(current))
            current = []
        if not raw_line.rstrip().endswith(" " + "\\"):
            fail("CI-PYTHON-LOCK", "locked requirement must continue to its hash")
        current.append(stripped[:-1].rstrip())
        expecting_hash = True
    if current:
        if expecting_hash:
            fail("CI-PYTHON-LOCK", "locked requirement has a dangling continuation")
        entries.append(" ".join(current))

    if binary_directive_count != 1:
        fail(
            "CI-PYTHON-LOCK",
            "lock must contain exactly one --only-binary :all: directive",
        )

    observed: dict[str, str] = {}
    for entry in entries:
        parts = entry.split()
        if len(parts) < 2:
            fail(
                "CI-PYTHON-LOCK",
                "every locked dependency must carry a SHA-256 hash",
            )
        pin = PIN_PATTERN.fullmatch(parts[0])
        if pin is None:
            fail("CI-PYTHON-LOCK", "every locked dependency must use one exact == pin")
        package = canonical_package_name(pin.group("name"))
        if package in observed:
            fail("CI-PYTHON-LOCK", f"duplicate locked dependency name: {package}")
        hashes = parts[1:]
        if any(HASH_PATTERN.fullmatch(value) is None for value in hashes):
            fail(
                "CI-PYTHON-LOCK",
                "every lock hash must be an exact lowercase SHA-256 digest",
            )
        if len(hashes) != len(set(hashes)):
            fail("CI-PYTHON-LOCK", "duplicate hashes are not allowed")
        observed[package] = pin.group("version")

    if observed != EXPECTED_RESOLVED_PINS:
        fail(
            "CI-PYTHON-LOCK",
            "resolved dependency names or versions differ from the CPython 3.12 lock",
        )
    return observed, binary_directive_count


def _validate_lock(text: str) -> dict[str, str]:
    resolved, _ = _lock_entries(text)
    return resolved


def _validate_pre_commit_revisions(
    text: str,
    config: dict[str, Any],
) -> None:
    repositories = config.get("repos")
    if not isinstance(repositories, list) or any(
        not isinstance(repository, dict) for repository in repositories
    ):
        fail("CI-PRECOMMIT-REV", "pre-commit repos must be a mapping list")

    observed: dict[str, str] = {}
    local_count = 0
    for repository in repositories:
        repo = repository.get("repo")
        if not isinstance(repo, str):
            fail("CI-PRECOMMIT-REV", "every pre-commit repository needs a string repo")
        if repo == "local":
            local_count += 1
            if "rev" in repository:
                fail(
                    "CI-PRECOMMIT-REV", "local pre-commit repository must not have rev"
                )
            continue
        if repo in observed:
            fail("CI-PRECOMMIT-REV", f"duplicate pre-commit repository: {repo}")
        revision = repository.get("rev")
        if (
            not isinstance(revision, str)
            or FULL_COMMIT_PATTERN.fullmatch(revision) is None
        ):
            fail(
                "CI-PRECOMMIT-REV",
                "every non-local pre-commit rev must be a full lowercase commit",
            )
        observed[repo] = revision

    if local_count > 1:
        fail(
            "CI-PRECOMMIT-REV",
            "pre-commit config must not duplicate the local repository",
        )
    if observed != EXPECTED_PRE_COMMIT_REVISIONS:
        fail(
            "CI-PRECOMMIT-REV",
            "pre-commit repository revisions differ from the exact frozen mapping",
        )
    try:
        root_node = yaml.compose(text, Loader=DuplicateKeyLoader)
    except yaml.YAMLError:
        fail("CI-PRECOMMIT-REV", "pre-commit provenance source is invalid")
    if not isinstance(root_node, yaml.MappingNode):
        fail("CI-PRECOMMIT-REV", "pre-commit provenance source must be a mapping")
    repo_nodes: dict[str, yaml.ScalarNode] = {}
    for key, value in root_node.value:
        if not isinstance(key, yaml.ScalarNode) or key.value != "repos":
            continue
        if not isinstance(value, yaml.SequenceNode):
            fail("CI-PRECOMMIT-REV", "pre-commit repos provenance must be a sequence")
        for item in value.value:
            if not isinstance(item, yaml.MappingNode):
                continue
            fields = {
                pair_key.value: pair_value
                for pair_key, pair_value in item.value
                if isinstance(pair_key, yaml.ScalarNode)
            }
            repo_node, rev_node = fields.get("repo"), fields.get("rev")
            if isinstance(repo_node, yaml.ScalarNode) and isinstance(
                rev_node, yaml.ScalarNode
            ):
                repo_nodes[repo_node.value] = rev_node
    lines = text.splitlines()
    for repo, revision in EXPECTED_PRE_COMMIT_REVISIONS.items():
        rev_node = repo_nodes.get(repo)
        if rev_node is None or rev_node.start_mark.line >= len(lines):
            fail(
                "CI-PRECOMMIT-REV",
                "every frozen repository must retain its semantic rev node",
            )
        source_tag = EXPECTED_PRE_COMMIT_SOURCE_TAGS[repo]
        frozen_line = f"    rev: {revision} # frozen: {source_tag}"
        if lines[rev_node.start_mark.line] != frozen_line:
            fail(
                "CI-PRECOMMIT-REV",
                "every frozen repo rev node must retain its exact source-tag line",
            )


def _steps_for_job(workflow: dict[str, Any], job_id: str) -> list[dict[str, Any]]:
    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict):
        fail("CI-PYTHON-WORKFLOW", "workflow jobs must be a mapping")
    job = jobs.get(job_id)
    if not isinstance(job, dict):
        fail("CI-PYTHON-WORKFLOW", f"validation job is missing: {job_id}")
    steps = job.get("steps")
    if not isinstance(steps, list) or any(not isinstance(step, dict) for step in steps):
        fail("CI-PYTHON-WORKFLOW", f"{job_id} steps must be a mapping list")
    return steps


def _run_text(step: dict[str, Any]) -> str:
    value = step.get("run")
    return value.strip() if isinstance(value, str) else ""


def _validate_python_versions(
    job_steps: dict[str, list[dict[str, Any]]],
) -> None:
    for job_id, steps in job_steps.items():
        setup_steps = [
            step
            for step in steps
            if isinstance(step.get("uses"), str)
            and step["uses"].startswith("actions/setup-python@")
        ]
        if len(setup_steps) != 1:
            fail(
                "CI-PYTHON-VERSION",
                f"{job_id} must contain exactly one actions/setup-python step",
            )
        setup_with = setup_steps[0].get("with")
        if (
            not isinstance(setup_with, dict)
            or setup_with.get("python-version") != EXPECTED_PYTHON
        ):
            fail("CI-PYTHON-VERSION", f"{job_id} must select Python 3.12")


def _validate_shared_installs(
    job_steps: dict[str, list[dict[str, Any]]],
) -> None:
    for job_id, steps in job_steps.items():
        run_commands = [_run_text(step) for step in steps]
        if run_commands.count(INSTALL_COMMAND) != 1:
            fail(
                "CI-PYTHON-WORKFLOW",
                f"{job_id} must contain exactly one shared requirements install",
            )
        install_commands = [
            command for command in run_commands if _guarded_pip_install(command)
        ]
        if install_commands != [INSTALL_COMMAND]:
            fail(
                "CI-PYTHON-WORKFLOW",
                f"{job_id} must not install loose inline Python packages",
            )


def _validate_no_outside_python_validation(workflow: dict[str, Any]) -> None:
    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict):
        fail("CI-PYTHON-WORKFLOW", "workflow jobs must be a mapping")
    for job_id, job in jobs.items():
        if job_id in VALIDATION_JOBS or not isinstance(job, dict):
            continue
        steps = job.get("steps")
        if not isinstance(steps, list):
            continue
        for step in steps:
            if not isinstance(step, dict):
                continue
            uses = step.get("uses")
            if isinstance(uses, str) and uses.startswith("actions/setup-python@"):
                fail(
                    "CI-PYTHON-WORKFLOW",
                    f"non-validation job must not own setup-python: {job_id}",
                )
            if _guarded_pip_install(_run_text(step)):
                fail(
                    "CI-PYTHON-WORKFLOW",
                    f"non-validation job must not own a pip install: {job_id}",
                )


def _validate_shell_boundaries(workflow: dict[str, Any]) -> None:
    """Admit only the reviewed default Actions shell for every run step."""

    defaults = workflow.get("defaults")
    if isinstance(defaults, dict) and "run" in defaults:
        fail(
            "CI-PYTHON-WORKFLOW",
            "workflow defaults.run shell overrides are unsupported",
        )
    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict):
        fail("CI-PYTHON-WORKFLOW", "workflow jobs must be a mapping")
    for job_id, job in jobs.items():
        if not isinstance(job, dict):
            continue
        job_defaults = job.get("defaults")
        if isinstance(job_defaults, dict) and "run" in job_defaults:
            fail(
                "CI-PYTHON-WORKFLOW",
                f"job defaults.run shell overrides are unsupported: {job_id}",
            )
        steps = job.get("steps")
        if not isinstance(steps, list):
            continue
        for step in steps:
            if isinstance(step, dict) and "run" in step and "shell" in step:
                fail("CI-PYTHON-WORKFLOW", "step shell overrides are unsupported")


def _validate_qa_execution(
    workflow: dict[str, Any],
    job_steps: dict[str, list[dict[str, Any]]],
) -> None:
    commands = [
        _run_text(step)
        for job in workflow["jobs"].values()
        if isinstance(job, dict)
        for step in job.get("steps", [])
        if isinstance(step, dict)
    ]
    qa_commands = [command for command in commands if "scripts/qa.py" in command]
    if qa_commands != [QA_COMMAND] or any(
        "pre-commit run" in command
        or "unittest discover" in command
        or "validate-repo-quality-gates.sh" in command
        for command in commands
    ):
        fail("CI-QA-EXECUTION", "CI must execute the shared QA profile exactly once")
    if [_run_text(step) for step in job_steps["qa"]].count(QA_COMMAND) != 1:
        fail("CI-QA-EXECUTION", "the shared QA profile must run in qa")


def _validate_gitleaks_tool(
    workflow: dict[str, Any],
    job_steps: dict[str, list[dict[str, Any]]],
) -> None:
    for job_id in GITLEAKS_JOBS:
        commands = [_run_text(step) for step in job_steps[job_id]]
        if commands.count(GITLEAKS_INSTALL_COMMAND) != 1:
            fail(
                "CI-GITLEAKS-TOOL",
                f"{job_id} must install the exact verified Gitleaks release",
            )

    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict):
        fail("CI-GITLEAKS-TOOL", "workflow jobs must be a mapping")
    for job_id, job in jobs.items():
        if job_id in GITLEAKS_JOBS or not isinstance(job, dict):
            continue
        steps = job.get("steps")
        if not isinstance(steps, list):
            continue
        if any(
            "gitleaks/releases/download" in _run_text(step)
            or "/usr/local/bin/gitleaks" in _run_text(step)
            for step in steps
            if isinstance(step, dict)
        ):
            fail(
                "CI-GITLEAKS-TOOL",
                f"non-owning job must not install Gitleaks: {job_id}",
            )


def _validate_repository_history(
    job_steps: dict[str, list[dict[str, Any]]],
) -> None:
    checkout_steps = [
        step
        for step in job_steps["qa"]
        if isinstance(step.get("uses"), str)
        and step["uses"].startswith("actions/checkout@")
    ]
    if len(checkout_steps) != 1 or checkout_steps[0].get("with") != {
        "ref": CANDIDATE_SHA_REF,
        "persist-credentials": False,
        "fetch-depth": 0,
    }:
        fail(
            "CI-REPOSITORY-HISTORY",
            "qa checkout requires immutable event SHA, full history, and disabled credentials",
        )


def validate_dependencies(root: Path) -> int:
    root = _resolve_repository_root(root)
    direct_requirements_text = _read_regular_text(
        root,
        DIRECT_REQUIREMENTS_PATH,
        "CI-PYTHON-PIN",
    )
    lock_text = _read_regular_text(
        root,
        LOCK_PATH,
        "CI-PYTHON-LOCK",
    )
    workflow_text = _read_regular_text(
        root,
        WORKFLOW_PATH,
        "CI-PYTHON-WORKFLOW",
    )
    pre_commit_text = _read_regular_text(
        root,
        PRE_COMMIT_CONFIG_PATH,
        "CI-PRECOMMIT-REV",
    )

    _validate_direct_requirements(direct_requirements_text)
    _validate_lock(lock_text)
    workflow = _load_yaml(workflow_text, "CI-PYTHON-WORKFLOW", WORKFLOW_PATH)
    pre_commit = _load_yaml(
        pre_commit_text,
        "CI-PRECOMMIT-REV",
        PRE_COMMIT_CONFIG_PATH,
    )
    _validate_pre_commit_revisions(pre_commit_text, pre_commit)

    if "pre-commit/action" in workflow_text.lower():
        fail(
            "CI-PRECOMMIT-ACTION",
            "pre-commit/action must be absent from the workflow",
        )

    job_steps = {job_id: _steps_for_job(workflow, job_id) for job_id in VALIDATION_JOBS}
    _validate_shell_boundaries(workflow)
    _validate_qa_execution(workflow, job_steps)
    _validate_gitleaks_tool(workflow, job_steps)
    _validate_no_outside_python_validation(workflow)
    _validate_python_versions(job_steps)
    _validate_shared_installs(job_steps)
    _validate_repository_history(job_steps)
    return len(job_steps)


def validate_workflow(workflow: dict[str, Any]) -> None:
    """Own CI topology; dependency grammar and QA gate selection have other owners."""
    events = workflow.get("on", workflow.get(True))
    if not isinstance(events, dict) or set(events) != {
        "push",
        "pull_request",
        "workflow_dispatch",
    }:
        fail("CI-TOPOLOGY", "CI requires push, pull_request, and manual entrypoints")
    for event in ("push", "pull_request"):
        if events[event] != {"branches": ["main"]}:
            fail("CI-TOPOLOGY", "required CI must target main without path filters")
    if workflow.get("permissions") != {"contents": "read"}:
        fail("CI-TOPOLOGY", "CI permissions must remain contents: read")
    jobs = workflow.get("jobs", {})
    if set(jobs) != {"branch-policy", "qa", "ci-summary"}:
        fail("CI-TOPOLOGY", "CI has one QA job, branch policy, and required summary")
    qa, branch, summary = (jobs[key] for key in ("qa", "branch-policy", "ci-summary"))
    if "if" in qa or qa.get("needs"):
        fail("CI-TOPOLOGY", "QA cannot be conditionally skipped")
    if branch.get("if") != "github.event_name == 'pull_request'":
        fail("CI-TOPOLOGY", "branch policy applies only to pull requests")
    if summary.get("if") != "always()" or summary.get("needs") != [
        "branch-policy",
        "qa",
    ]:
        fail("CI-TOPOLOGY", "ci-summary must always inspect both predecessor results")
    for job in jobs.values():
        if job.get("permissions") or job.get("continue-on-error"):
            fail("CI-TOPOLOGY", "jobs cannot widen permissions or suppress failures")
        for step in job.get("steps", []):
            if step.get("continue-on-error"):
                fail("CI-TOPOLOGY", "steps cannot suppress required failures")
            if "SKIP" in step.get("env", {}):
                fail("CI-TOPOLOGY", "CI cannot bypass registered QA checks")
    qa_steps = [step for step in qa["steps"] if _run_text(step) == QA_COMMAND]
    if len(qa_steps) != 1 or qa_steps[0].get("env") != {
        "BASE_SHA": "${{ github.event.pull_request.base.sha || github.event.before || '' }}"
    }:
        fail("CI-TOPOLOGY", "QA must receive the event comparison base")
    steps = summary.get("steps", [])
    if len(steps) != 1 or steps[0].get("env") != {
        "EVENT_NAME": "${{ github.event_name }}",
        "BRANCH_POLICY_RESULT": "${{ needs.branch-policy.result }}",
        "QA_RESULT": "${{ needs.qa.result }}",
    }:
        fail("CI-TOPOLOGY", "summary must consume actual event and predecessor results")
    summary_text = _run_text(steps[0])
    for fragment in (
        'case "$EVENT_NAME:$BRANCH_POLICY_RESULT" in',
        "pull_request:success)",
        "push:skipped|workflow_dispatch:skipped)",
        "branch_verdict=FAIL",
        'case "$QA_RESULT" in',
        "qa_verdict=PASS",
        "qa_verdict=FAIL",
        'if [ "$failed" -ne 0 ]; then',
        "exit 1",
        "exit 0",
    ):
        if fragment not in summary_text:
            fail(
                "CI-TOPOLOGY",
                "summary must fail closed for missing, skipped, failed or cancelled QA",
            )


def validate_repository(root: Path) -> int:
    count = validate_dependencies(root)
    text = _read_regular_text(root, WORKFLOW_PATH, "CI-PYTHON-WORKFLOW")
    validate_workflow(_load_yaml(text, "CI-PYTHON-WORKFLOW", WORKFLOW_PATH))
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        job_count = validate_repository(args.root)
        print(
            "[PASS] CI Python contract validation passed: "
            f"jobs={job_count} pins={len(EXPECTED_PINS)}"
        )
        return 0
    except ContractError as exc:
        print(f"[FAIL] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
