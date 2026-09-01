#!/usr/bin/env python3
"""Import the canonical agent-registry validator for composed validators."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


TERMINAL_VALIDATOR = Path(__file__).with_name("validate-agent-harness-contract.py")


def load_terminal_validator() -> ModuleType:
    specification = importlib.util.spec_from_file_location(
        "agent_registry_terminal_validator", TERMINAL_VALIDATOR
    )
    if specification is None or specification.loader is None:
        raise ImportError("canonical agent-registry validator is unavailable")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module
