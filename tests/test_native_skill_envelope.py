"""Native Skill metadata retains provider controls while exposing document meaning."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path, PurePosixPath

from tests.test_task_execution_contract import MARKDOWN


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location(
    "native_skill_envelope", ROOT / "scripts/validate-agent-governance.py"
)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)
from document_contracts import load_registry  # noqa: E402
from document_lifecycle import document_from_text  # noqa: E402


class NativeSkillEnvelopeTests(unittest.TestCase):
    def test_canonical_nested_metadata_is_read_without_losing_native_control(
        self,
    ) -> None:
        skill = (
            "---\n"
            'name: "example"\n'
            'description: "Example procedure."\n'
            "metadata:\n"
            '  title: "Example"\n'
            '  version: "1.0.0"\n'
            '  type: "governance/skill"\n'
            '  status: "active"\n'
            '  owner: "platform"\n'
            '  updated: "2026-10-05"\n'
            "disable-model-invocation: true\n"
            "---\n\n# Example\n"
        )
        metadata, body = VALIDATOR._frontmatter(skill)
        self.assertEqual(metadata["metadata"]["type"], "governance/skill")
        self.assertIs(metadata["disable-model-invocation"], True)
        self.assertEqual(body.strip(), "# Example")

    def test_actual_skill_metadata_drives_markdown_and_lifecycle(self) -> None:
        registry = load_registry(ROOT)
        path = PurePosixPath(".agents/skills/k8s-validate/SKILL.md")
        profile = MARKDOWN.classify_path(registry, path)
        text = (ROOT / path).read_text()
        schema = MARKDOWN.load_frontmatter_schema(ROOT)
        self.assertEqual(
            MARKDOWN.validate_document_text(
                text, path, profile, "strict", frontmatter_schema=schema
            ),
            [],
        )
        self.assertEqual(document_from_text(registry, path, text).status, "active")
        for changed in (
            text.replace('  owner: "platform"\n', ""),
            text.replace('  type: "governance/skill"', '  type: "MYSTERY"'),
            text.replace('  type: "governance/skill"', '  type: "operation/incident"'),
        ):
            self.assertIn(
                "FM-SCHEMA",
                {
                    item.rule_id
                    for item in MARKDOWN.validate_document_text(
                        changed, path, profile, "strict", frontmatter_schema=schema
                    )
                },
            )
        changed = text.replace("  title:", '  owner: "platform"\n  title:').replace(
            '  owner: "platform"\n  updated:', "  updated:"
        )
        with self.assertRaises(VALIDATOR.HarnessError):
            VALIDATOR._frontmatter(changed)

    def test_resolved_incident_requires_real_zoned_time_and_evidence(self) -> None:
        registry = load_registry(ROOT)
        path = PurePosixPath(
            "docs/05.operations/incidents/2026/inc-0001-example/incident.md"
        )
        profile = next(
            p for p in registry.profiles if p.profile_id == "operation/incident"
        )
        source = (ROOT / profile.template).read_text()
        source = source.replace('status: "detected"', 'status: "resolved"').replace(
            'updated: "{{UPDATED}}"', 'updated: "2026-10-05"'
        )
        for value in (
            "2026-99-99T99:99:99Z",
            "2026-10-05T10:20:30",
            "2026-10-05T10:20:30+99:99",
        ):
            changed = source.replace("layer:", f'resolved_at: "{value}"\nlayer:')
            self.assertIn(
                "INCIDENT-RESOLVED-AT",
                {
                    d.rule_id
                    for d in MARKDOWN.validate_document_text(
                        changed, path, profile, "strict"
                    )
                },
            )
        changed = source.replace(
            "layer:", 'resolved_at: "2026-10-05T10:20:30+09:00"\nlayer:'
        )
        self.assertIn(
            "INCIDENT-RESOLUTION-EVIDENCE",
            {
                d.rule_id
                for d in MARKDOWN.validate_document_text(
                    changed, path, profile, "strict"
                )
            },
        )
        changed = changed.replace(
            "## Closure\n",
            "## Closure\n\n[Resolved check](incident.md#evidence) confirms recovery.\n",
        )
        self.assertNotIn(
            "INCIDENT-RESOLVED-AT",
            {
                d.rule_id
                for d in MARKDOWN.validate_document_text(
                    changed, path, profile, "strict"
                )
            },
        )


if __name__ == "__main__":
    unittest.main()
