"""Synthetic affected-surface mutations owned by the independent test suite."""

from __future__ import annotations

import copy
from typing import Any


def apply_mutation(contract: dict[str, Any], mutation: dict[str, Any]) -> None:
    kind = mutation["kind"]
    if kind == "append-route":
        surface = next(
            row for row in contract["surfaces"] if row["id"] == mutation["surfaceId"]
        )
        surface["routes"].append(copy.deepcopy(mutation["route"]))
        return
    if kind in {
        "replace-argv",
        "replace-validator-lanes",
        "remove-validator-path-input",
        "add-validator-path-input",
        "replace-fallback-status",
        "replace-evidence-lane",
    }:
        validator = next(
            row
            for row in contract["validators"]
            if row["id"] == mutation["validatorId"]
        )
        if kind == "replace-argv":
            validator["argv"] = list(mutation["argv"])
        elif kind == "replace-validator-lanes":
            validator["lanes"] = list(mutation["lanes"])
        elif kind == "remove-validator-path-input":
            validator.pop("pathInput", None)
        elif kind == "add-validator-path-input":
            validator["pathInput"] = "include-existing-markdown"
        elif kind == "replace-fallback-status":
            validator["fallback"]["status"] = mutation["status"]
        else:
            validator["evidenceLane"] = mutation["evidenceLane"]
        return
    if kind in {
        "append-validator-reference",
        "remove-validator-reference",
        "replace-protected-level",
        "replace-surface-fallback-status",
    }:
        surface = next(
            row for row in contract["surfaces"] if row["id"] == mutation["surfaceId"]
        )
        if kind == "append-validator-reference":
            surface["validators"].append(mutation["validatorId"])
        elif kind == "remove-validator-reference":
            surface["validators"].remove(mutation["validatorId"])
        elif kind == "replace-protected-level":
            surface["protectedLevel"] = mutation["protectedLevel"]
        else:
            surface["fallback"]["status"] = mutation["status"]
        return
    raise AssertionError(f"unknown affected-surface mutation: {kind!r}")
