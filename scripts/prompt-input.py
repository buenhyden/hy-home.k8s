#!/usr/bin/env python3
"""Assemble a prompt request from a declared contract without calling a model."""

from __future__ import annotations

import argparse
import re
import shlex
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path, PurePosixPath


PROMPT_ROOT = ".agents/prompts"
INPUTS_HEADING = "## Inputs"
COMMAND_TIMEOUT_SECONDS = 30
MAX_CONTRACT_BYTES = 256 * 1024
MAX_INPUT_CHARACTERS = 200_000
IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
TABLE_ROW = re.compile(r"^\s*\|(?P<cells>.+)\|\s*$")
TABLE_DIVIDER = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
HEADING = re.compile(r"^##\s")
INLINE_CODE = re.compile(r"`([^`\n]+)`")
SUBJECT = re.compile(r"The subject input is `([^`\n]+)`")
FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)

# Every command a contract may declare. The builder runs nothing else, so a
# contract cannot widen the builder's reach by declaring a new command; adding
# one is a reviewed change here.
ALLOWED_COMMANDS = frozenset(
    {
        ("git", "diff"),
        ("git", "diff", "--cached"),
        ("git", "diff", "--cached", "--name-only"),
        ("git", "diff", "--check"),
        ("git", "log", "--oneline", "main..HEAD"),
        ("git", "ls-files", "docs/**/README.md", ".agents/**/*.md"),
        ("git", "rev-parse", "HEAD"),
        ("git", "rev-parse", "--abbrev-ref", "HEAD"),
        ("git", "status", "--porcelain"),
    }
)

EXIT_OK = 0
EXIT_CONTRACT = 2
EXIT_REFUSED = 3


class PromptInputError(Exception):
    """Raised when a request cannot be assembled within the declared contract."""

    def __init__(self, code: str, detail: str, status: int = EXIT_CONTRACT) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail
        self.status = status


def contract_path(root: Path, identifier: str) -> Path:
    if not IDENTIFIER.match(identifier):
        raise PromptInputError("PROMPT-IDENTIFIER", f"{identifier!r} is not a contract identifier")
    candidate = root / PROMPT_ROOT / f"{identifier}.md"
    if not candidate.is_file():
        raise PromptInputError("PROMPT-UNKNOWN", f"no contract at {PROMPT_ROOT}/{identifier}.md")
    return candidate


def read_contract(path: Path) -> str:
    if path.stat().st_size > MAX_CONTRACT_BYTES:
        raise PromptInputError("PROMPT-CONTRACT-SIZE", f"{path.name} exceeds the bounded read size")
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise PromptInputError("PROMPT-CONTRACT-READ", str(exc)) from exc


def body(text: str) -> str:
    return FRONTMATTER.sub("", text, count=1)


def section(text: str, heading: str) -> list[str]:
    collected: list[str] = []
    inside = False
    for line in text.split("\n"):
        if line.strip() == heading:
            inside = True
            continue
        if inside and HEADING.match(line):
            break
        if inside:
            collected.append(line)
    return collected


def declared_inputs(text: str) -> list[tuple[str, tuple[str, ...]]]:
    rows: list[list[str]] = []
    for line in section(text, INPUTS_HEADING):
        if TABLE_DIVIDER.match(line):
            continue
        match = TABLE_ROW.match(line)
        if match:
            rows.append([cell.strip() for cell in match.group("cells").split("|")])
    if len(rows) < 2:
        raise PromptInputError("PROMPT-INPUTS-EMPTY", "the contract declares no input row")

    inputs: list[tuple[str, tuple[str, ...]]] = []
    for cells in rows[1:]:
        if len(cells) < 2:
            raise PromptInputError("PROMPT-INPUT-ROW", f"malformed input row {cells!r}")
        name = cells[0]
        codes = INLINE_CODE.findall(cells[1])
        if len(codes) != 1:
            raise PromptInputError("PROMPT-INPUT-COMMAND", f"{name} must declare exactly one command")
        try:
            argv = tuple(shlex.split(codes[0]))
        except ValueError as exc:
            raise PromptInputError("PROMPT-INPUT-COMMAND", f"{name}: {exc}") from exc
        if argv not in ALLOWED_COMMANDS:
            raise PromptInputError(
                "PROMPT-INPUT-FORBIDDEN",
                f"{name} declares {codes[0]!r}, which is not an allowed read-only command",
            )
        inputs.append((name, argv))
    return inputs


def subject_name(text: str) -> str:
    match = SUBJECT.search(text)
    if match is None:
        raise PromptInputError("PROMPT-SUBJECT", "the contract names no subject input")
    return match.group(1)


def run_input(root: Path, name: str, argv: Sequence[str]) -> str:
    try:
        completed = subprocess.run(
            argv,
            cwd=root,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise PromptInputError("PROMPT-INPUT-FAILED", f"{name}: {exc}") from exc
    if completed.returncode != 0:
        raise PromptInputError(
            "PROMPT-INPUT-FAILED",
            f"{name}: `{' '.join(argv)}` exited {completed.returncode}",
        )
    output = completed.stdout
    if len(output) > MAX_INPUT_CHARACTERS:
        output = output[:MAX_INPUT_CHARACTERS] + "\n[truncated at the builder's bounded read size]\n"
    return output


def assemble(root: Path, identifier: str) -> str:
    """Return the assembled request, or raise when the contract refuses."""

    contract_text = body(read_contract(contract_path(root, identifier)))
    inputs = declared_inputs(contract_text)
    subject = subject_name(contract_text)
    names = [name for name, _ in inputs]
    if subject not in names:
        raise PromptInputError(
            "PROMPT-SUBJECT", f"the subject {subject!r} is not one of the declared inputs"
        )

    collected: list[tuple[str, tuple[str, ...], str]] = []
    for name, argv in inputs:
        output = run_input(root, name, argv)
        if name == subject and not output.strip():
            raise PromptInputError(
                "PROMPT-REFUSED",
                f"the subject input {name!r} is empty, so the contract produces no draft",
                EXIT_REFUSED,
            )
        collected.append((name, argv, output))

    parts = [f"# Prompt request: {identifier}", "", "## Contract", "", contract_text.strip(), "", "## Collected inputs", ""]
    for name, argv, output in collected:
        parts += [f"### {name}", "", f"Command: `{' '.join(argv)}`", "", "```", output.rstrip("\n"), "```", ""]
    return "\n".join(parts).rstrip("\n") + "\n"


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assemble a declared prompt request on standard output. Makes no model call."
    )
    parser.add_argument("identifier", help="contract identifier, equal to its file stem")
    parser.add_argument("--root", default=".")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parse_args(sys.argv[1:] if argv is None else argv)
    root = Path(arguments.root).resolve()
    try:
        sys.stdout.write(assemble(root, arguments.identifier))
    except PromptInputError as exc:
        print(f"[FAIL] {exc.code}: {exc.detail}", file=sys.stderr)
        return exc.status
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
