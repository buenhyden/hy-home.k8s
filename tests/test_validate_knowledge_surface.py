from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPOSITORY_ROOT / "scripts" / "validate-knowledge-surface.py"
REGISTRY_PATH = REPOSITORY_ROOT / "scripts" / "validation" / "registry.json"

FRONTMATTER = (
    "---\n"
    'title: "Sample Map"\n'
    'version: "0.1.0"\n'
    'type: "governance/knowledge"\n'
    'status: "active"\n'
    'owner: "platform"\n'
    'updated: "2026-09-07"\n'
    "---\n\n"
)

OWNER_TEXT = (
    "# Owner\n\n"
    "The reconciliation boundary keeps declarative desired state under version "
    "control so that every applied change arrives through a reviewed pull "
    "request rather than a direct cluster mutation.\n"
)

README_TEMPLATE = (
    "# Common Knowledge\n\n"
    "## Item Index\n\n"
    "{entries}\n\n"
    "## Related Documents\n\n"
    "- nothing\n"
)


def load_validator():
    specification = importlib.util.spec_from_file_location(
        "knowledge_surface_validator_test_target", VALIDATOR_PATH
    )
    if specification is None or specification.loader is None:
        raise AssertionError("knowledge surface validator could not be loaded")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def document(
    rows: str, prose: str = "This map points at owners and states no policy of its own."
) -> str:
    return (
        FRONTMATTER
        + "# Sample Map\n\n"
        + "## Overview\n\n"
        + prose
        + "\n\n## Authority Boundary\n\nEvery row points; none decides.\n\n"
        + "## Pointer Index\n\n"
        + "| Area | Owner path | Entry path | Stays valid while |\n"
        + "| --- | --- | --- | --- |\n"
        + rows
        + "\n\n## Validation and Refresh\n\nThe validator judges this file.\n\n"
        + "## Related Documents\n\n- none\n"
    )


class KnowledgeSurfaceValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_validator()
        self._directory = tempfile.TemporaryDirectory(prefix="knowledge-surface-")
        self.addCleanup(self._directory.cleanup)
        self.root = Path(self._directory.name)
        surface = self.root / ".agents" / "knowledge"
        surface.mkdir(parents=True)
        (self.root / "owner").mkdir()
        (self.root / "owner" / "README.md").write_text(OWNER_TEXT, encoding="utf-8")
        self.surface = surface

    def write_readme(self, *names: str) -> None:
        entries = "\n".join(f"- [Sample]({name}): a map." for name in names)
        (self.surface / "README.md").write_text(
            README_TEMPLATE.format(entries=entries), encoding="utf-8"
        )

    def codes(self):
        return [
            finding.code
            for finding in self.module.validate_knowledge_surface(self.root)
        ]

    def test_valid_document_passes(self) -> None:
        self.write_readme("map.md")
        (self.surface / "map.md").write_text(
            document(
                "| Owner | `owner/` | `owner/README.md` | The owner keeps its scope |"
            ),
            encoding="utf-8",
        )
        self.assertEqual(self.codes(), [])

    def test_missing_owner_path_fails(self) -> None:
        self.write_readme("map.md")
        (self.surface / "map.md").write_text(
            document(
                "| Owner | `absent/` | `owner/README.md` | The owner keeps its scope |"
            ),
            encoding="utf-8",
        )
        self.assertIn("KNOWLEDGE-PATH-MISSING", self.codes())

    def test_missing_entry_path_fails(self) -> None:
        self.write_readme("map.md")
        (self.surface / "map.md").write_text(
            document(
                "| Owner | `owner/` | `owner/ABSENT.md` | The owner keeps its scope |"
            ),
            encoding="utf-8",
        )
        self.assertIn("KNOWLEDGE-PATH-MISSING", self.codes())

    def test_reproduced_policy_span_fails(self) -> None:
        self.write_readme("map.md")
        borrowed = (
            "The reconciliation boundary keeps declarative desired state under "
            "version control so that every applied change arrives through a "
            "reviewed pull request rather than a direct cluster mutation."
        )
        (self.surface / "map.md").write_text(
            document(
                "| Owner | `owner/` | `owner/README.md` | The owner keeps its scope |",
                prose=borrowed,
            ),
            encoding="utf-8",
        )
        self.assertIn("KNOWLEDGE-DUPLICATED-SPAN", self.codes())

    def test_unindexed_document_fails(self) -> None:
        self.write_readme()
        (self.surface / "map.md").write_text(
            document(
                "| Owner | `owner/` | `owner/README.md` | The owner keeps its scope |"
            ),
            encoding="utf-8",
        )
        self.assertIn("KNOWLEDGE-INDEX-MISSING", self.codes())

    def test_absent_surface_reports_nothing(self) -> None:
        empty = Path(self._directory.name) / "empty"
        empty.mkdir()
        self.assertEqual(self.module.validate_knowledge_surface(empty), [])


class KnowledgeSurfaceRepositoryTests(unittest.TestCase):
    def test_repository_surface_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), "--root", str(REPOSITORY_ROOT)],
            capture_output=True,
            text=True,
            timeout=120,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_validator_is_registered(self) -> None:
        import json

        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        commands = [
            " ".join(str(part) for part in validator.get("argv", []))
            for validator in registry["validators"]
        ]
        self.assertTrue(
            any("validate-knowledge-surface.py" in command for command in commands),
            "the knowledge surface validator is not routed by the validation registry",
        )


if __name__ == "__main__":
    unittest.main()
