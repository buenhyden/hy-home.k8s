"""Numeric document versions and SemVer 2.0.0 product versions."""

from __future__ import annotations

import re
from decimal import Decimal

NUMERIC_VERSION_PATTERN = r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
_NUMERIC = re.compile(NUMERIC_VERSION_PATTERN)

# Unanchored, no `v` prefix; groups: major, minor, patch, prerelease, build.
_IDENTIFIER = r"(?:0|[1-9][0-9]*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*)"
SEMVER_PATTERN = (
    rf"{NUMERIC_VERSION_PATTERN}(?:-({_IDENTIFIER}(?:\.{_IDENTIFIER})*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
)
_COMPILED = re.compile(SEMVER_PATTERN)


def is_numeric_version(value: object) -> bool:
    return isinstance(value, str) and _NUMERIC.fullmatch(value) is not None


def numeric_version_order(value: object) -> tuple[Decimal, Decimal, Decimal] | None:
    """Return exact numeric components without the int string length limit."""

    match = _NUMERIC.fullmatch(value) if isinstance(value, str) else None
    if match is None:
        return None
    major, minor, patch = match.groups()
    return Decimal(major), Decimal(minor), Decimal(patch)


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
