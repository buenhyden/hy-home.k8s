"""Core Task rows from compact fixture rows written with the SPEC-0203 names.

The rule tests keep their fixtures short: a fixture row names its cells as a
SPEC-0203 Task did (`ID`, `Consumer`, `Current owner`, `yes` and `no`). This
builder renames them to the core names the rules read. Production code reads
only the core header (SPEC-0223 WORK-003).
"""

from __future__ import annotations

from collections.abc import Mapping

_CORE_NAMES = {"ID": "Item", "Consumer": "Criteria", "Current owner": "Current Owner"}
_REQUIRED = {"yes": "true", "no": "false"}


def core_row(kind: str, row: Mapping[str, str]) -> dict[str, str]:
    """One fixture row under the core names; a work item ID is also its Work Unit."""

    read = {_CORE_NAMES.get(key, key): value for key, value in row.items()}
    if kind == "traceability" and "Item" in read:
        read["Work Unit"] = read["Item"]
    if kind == "evidence" and "Required" in read:
        value = read["Required"].strip()
        read["Required"] = _REQUIRED.get(value, read["Required"])
    return read
