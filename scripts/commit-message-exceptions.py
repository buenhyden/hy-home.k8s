#!/usr/bin/env python3
"""Narrow Commitizen prefix exceptions using the canonical .cz.toml shapes."""

from __future__ import annotations

import re
import stat
import sys
import tomllib
from pathlib import Path


def native_message_text(message: str) -> str:
    """Apply Commitizen 4.15.1's commit-file comments and scissor filtering."""
    lines: list[str] = []
    for line in message.split("\n"):
        if "# ------------------------ >8 ------------------------" in line:
            break
        if not line.startswith("#"):
            lines.append(line)
    return "\n".join(lines)


def check_message(message: str, path: Path = Path(".cz.toml")) -> bool:
    """Leave ordinary validation to Commitizen; narrow its prefix bypasses."""
    try:
        if not stat.S_ISREG(path.lstat().st_mode):
            raise ValueError("canonical Commitizen config must be a regular file")
        settings = tomllib.loads(path.read_text(encoding="utf-8"))["tool"]["commitizen"]
        customize = settings["customize"]
        prefixes = settings["allowed_prefixes"]
        if not isinstance(prefixes, list) or not all(
            isinstance(prefix, str) and prefix for prefix in prefixes
        ):
            raise ValueError("allowed_prefixes must contain nonempty strings")
        patterns = {
            name: re.compile(customize[name])
            for name in (
                "schema_pattern",
                "commit_parser",
                "generated_merge_pattern",
                "generated_revert_pattern",
            )
        }
    except (
        OSError,
        UnicodeError,
        KeyError,
        TypeError,
        re.error,
        tomllib.TOMLDecodeError,
    ) as error:
        raise ValueError(
            f"canonical Commitizen grammar is unavailable: {error}"
        ) from error
    candidate = native_message_text(message).strip()
    first_line = candidate.splitlines()[0] if candidate else ""
    matching = tuple(prefix for prefix in prefixes if first_line.startswith(prefix))
    if not matching:
        return True
    if patterns["schema_pattern"].fullmatch(candidate) and patterns[
        "commit_parser"
    ].fullmatch(candidate):
        return True
    return bool(
        (
            "Merge" in matching
            and patterns["generated_merge_pattern"].fullmatch(candidate)
        )
        or (
            "Revert" in matching
            and patterns["generated_revert_pattern"].fullmatch(candidate)
        )
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            "COMMIT-EXCEPTION-INPUT: expected one UTF-8 message file", file=sys.stderr
        )
        return 2
    try:
        if check_message(Path(argv[1]).read_text(encoding="utf-8")):
            return 0
    except (OSError, UnicodeError, ValueError) as error:
        print(f"COMMIT-EXCEPTION-CONTRACT: check .cz.toml: {error}", file=sys.stderr)
        return 2
    print(
        "COMMIT-EXCEPTION-SHAPE: message is not a generated Git Merge/Revert; use the .cz.toml authored grammar",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
