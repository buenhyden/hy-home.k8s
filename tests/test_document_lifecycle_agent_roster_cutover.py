"""Regressions for the terminal agent-registry lifecycle boundary."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

SPEC = importlib.util.spec_from_file_location(
    "validate_document_lifecycle_agent_registry_tested",
    SCRIPTS / "validate-document-lifecycle.py",
)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import boundary
    raise RuntimeError("cannot import document lifecycle validator")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)

from document_contracts import classify_path, load_registry  # noqa: E402


class TerminalAgentRegistryLifecycleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document_registry = load_registry(ROOT)
        cls.agent_registry = json.loads(
            (ROOT / "docs/00.agent-governance/roles/registry.json").read_text(
                encoding="utf-8"
            )
        )

    def test_terminal_registry_has_only_codex_and_claude_providers(self) -> None:
        self.assertEqual(
            [provider["id"] for provider in self.agent_registry["providers"]],
            ["claude", "codex"],
        )
        for role in self.agent_registry["roles"]:
            self.assertEqual(role["supported_providers"], ["claude", "codex"])
            self.assertEqual(set(role["projections"]), {"neutral", "claude", "codex"})

    def test_agent_markdown_uses_neutral_and_claude_document_profiles(self) -> None:
        self.assertEqual(
            classify_path(
                self.document_registry,
                PurePosixPath("docs/00.agent-governance/roles/docs-researcher.md"),
            ).profile_id,
            "governance/role",
        )
        self.assertEqual(
            classify_path(
                self.document_registry,
                PurePosixPath(".claude/agents/docs-researcher.md"),
            ).profile_id,
            "common/provider-native-metadata",
        )

    def test_retired_finite_roster_gate_is_not_a_lifecycle_authority(self) -> None:
        retired_names = (
            "AGENT_ROSTER_ADMISSION_BASE_COMMIT",
            "AGENT_ROSTER_SURFACE_IDS",
            "finite_agent_roster_cutover_paths",
            "_agent_contracts_from_blob_maps",
        )
        for name in retired_names:
            with self.subTest(name=name):
                self.assertFalse(hasattr(VALIDATOR, name))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
