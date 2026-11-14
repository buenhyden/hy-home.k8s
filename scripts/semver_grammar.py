"""The one SemVer 2.0.0 grammar for repository version values."""

from __future__ import annotations

import re

# Unanchored, no `v` prefix; groups: major, minor, patch, prerelease, build.
_IDENTIFIER = r"(?:0|[1-9][0-9]*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*)"
SEMVER_PATTERN = (
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    rf"(?:-({_IDENTIFIER}(?:\.{_IDENTIFIER})*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
)
_COMPILED = re.compile(SEMVER_PATTERN)


def is_semver(value: str) -> bool:
    return _COMPILED.fullmatch(value) is not None


def precedence(value: str) -> tuple[object, ...]:
    """The SemVer 2.0.0 precedence key of a bare version; build metadata is ignored.

    Raises ValueError for a value outside the grammar, such as a `v` tag label.
    """

    match = _COMPILED.fullmatch(value)
    if match is None:
        raise ValueError("not a SemVer 2.0.0 version")
    major, minor, patch, prerelease, _ = match.groups()
    pre = tuple(
        (0, int(part)) if part.isdecimal() else (1, part)
        for part in (prerelease.split(".") if prerelease else ())
    )
    return (int(major), int(minor), int(patch), 0 if pre else 1, pre)
