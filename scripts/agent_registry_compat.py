#!/usr/bin/env python3
"""Shared compatibility adapter for registry-derived legacy agent gates."""

from __future__ import annotations

import copy
import importlib.util
import os
import stat
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


TERMINAL_VALIDATOR = Path(__file__).with_name("validate-agent-harness-contract.py")
SUPPORTED_MODES = frozenset(
    {"admission", "currentness", "model-fitness", "evaluations", "closure"}
)


class CompatibilityError(ValueError):
    """Stable failure raised by a compatibility CLI."""

    def __init__(self, code: str, detail: str, *, exit_code: int = 1) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail
        self.exit_code = exit_code


def resolve_root(value: Path) -> Path:
    """Resolve a real repository directory without following a root symlink."""

    try:
        mode = os.lstat(value).st_mode
    except OSError as exc:
        raise CompatibilityError(
            "AGENT-COMPAT-INPUT", "repository root is unavailable", exit_code=2
        ) from exc
    if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
        raise CompatibilityError(
            "AGENT-COMPAT-INPUT",
            "repository root must be a real directory",
            exit_code=2,
        )
    try:
        return value.resolve(strict=True)
    except OSError as exc:
        raise CompatibilityError(
            "AGENT-COMPAT-INPUT", "repository root is unavailable", exit_code=2
        ) from exc


def load_terminal_validator() -> ModuleType:
    """Load the terminal registry gate without creating a second authority."""

    specification = importlib.util.spec_from_file_location(
        "agent_registry_terminal_validator", TERMINAL_VALIDATOR
    )
    if specification is None or specification.loader is None:
        raise CompatibilityError(
            "AGENT-COMPAT-IMPORT",
            "terminal registry validator is unavailable",
            exit_code=2,
        )
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def validate(root: Path, mode: str) -> dict[str, int]:
    """Delegate one legacy gate to the terminal registry authority."""

    if mode not in SUPPORTED_MODES:
        raise CompatibilityError(
            "AGENT-COMPAT-MODE", f"unsupported compatibility mode: {mode}", exit_code=2
        )
    terminal = load_terminal_validator()
    return terminal.validate_registry(resolve_root(root), check_files=True)


def _apply_bounded_mutation(registry: dict[str, Any], mode: str) -> str:
    if mode == "admission":
        registry["roles"][0]["permission_class"] = "unbounded-write"
        return "AGENT-REGISTRY-PERMISSION"
    if mode == "currentness":
        registry["roles"][0]["projections"]["neutral"] = ".agents/agents/wrong-role.md"
        return "AGENT-REGISTRY-PROJECTION"
    if mode == "model-fitness":
        registry["roles"][0]["capability_tier_ref"] = "unbounded-model-tier"
        return "AGENT-REGISTRY-SCHEMA"
    if mode in {"evaluations", "closure"}:
        registry["roles"][0]["responsibility"] = (
            "Authenticated provider execution was discovered and verified."
        )
        return "AGENT-REGISTRY-EVIDENCE"
    raise CompatibilityError(
        "AGENT-COMPAT-MODE", f"unsupported compatibility mode: {mode}", exit_code=2
    )


def run_self_test(root: Path, mode: str) -> dict[str, int]:
    """Exercise one bounded failure owned by the selected compatibility gate."""

    terminal = load_terminal_validator()
    resolved_root = resolve_root(root)
    registry = terminal.load_json(resolved_root, terminal.REGISTRY_PATH)
    counts = terminal.validate_registry(resolved_root, registry, check_files=True)
    mutated = copy.deepcopy(registry)
    expected_code = _apply_bounded_mutation(mutated, mode)
    try:
        terminal.validate_registry(resolved_root, mutated, check_files=False)
    except terminal.HarnessError as exc:
        if exc.code != expected_code:
            raise CompatibilityError(
                "AGENT-COMPAT-SELF-TEST",
                f"{mode} expected {expected_code}, got {exc.code}",
            ) from exc
    else:
        raise CompatibilityError(
            "AGENT-COMPAT-SELF-TEST", f"{mode} mutation unexpectedly passed"
        )
    return counts


def format_counts(counts: dict[str, int]) -> str:
    """Return a stable summary whose cardinalities come only from the registry."""

    return " ".join(
        f"{key}={counts[key]}"
        for key in (
            "providers",
            "roles",
            "permissionClasses",
            "skills",
            "handoffs",
            "projections",
        )
    )
