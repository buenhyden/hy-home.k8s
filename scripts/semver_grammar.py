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
