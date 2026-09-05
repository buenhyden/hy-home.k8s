"""Common agent authority keeps strict document routing and native metadata."""

from __future__ import annotations

import ast
import importlib.util
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import document_contracts as contracts  # noqa: E402

SPEC = importlib.util.spec_from_file_location(
    "common_agents_markdown_profiles", ROOT / "scripts/validate-markdown-profiles.py"
)
assert SPEC is not None and SPEC.loader is not None
MARKDOWN = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MARKDOWN
SPEC.loader.exec_module(MARKDOWN)


class CommonAgentsDocumentRoutesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = contracts.load_registry(ROOT)

    def test_common_authorities_select_existing_semantic_profiles(self) -> None:
        routes = {
            ".agents/README.md": "common/readme-implementation",
            ".agents/governance/sdlc.md": "governance/contract",
            ".agents/governance/quality.md": "governance/rule",
            ".agents/roles/README.md": "common/readme-collection-index",
            ".agents/roles/doc-writer.md": "governance/role",
            ".agents/workflows/work-lifecycle.md": "governance/skill",
            ".agents/workflows/delegated-development.md": "governance/skill",
            ".agents/skills/docs-stage-routing/SKILL.md": "common/native-skill-package",
            ".claude/provider.md": "governance/provider",
            ".codex/provider.md": "governance/provider",
        }
        for path, expected in routes.items():
            with self.subTest(path=path):
                profile = contracts.classify_path(self.registry, PurePosixPath(path))
                self.assertEqual(profile.profile_id, expected)
                if expected.startswith("governance/"):
                    self.assertEqual(
                        profile.status_domain,
                        ("draft", "active", "superseded", "retired"),
                    )
                    self.assertIsNotNone(profile.lifecycle_domain)

    def test_unowned_and_retired_routes_are_not_catch_all_native_exceptions(
        self,
    ) -> None:
        for path in (
            "docs/00.agent-governance/policies/quality.md",
            "docs/00.agent-governance/skills/docs-stage-routing/SKILL.md",
            ".agents/memory/progress.md",
            ".agents/providers/codex.md",
            ".agents/governance/README.md",
            ".agents/governance/contracts/duplicate.md",
            ".agents/skills/README.md",
            ".agents/skills/routing.md",
            ".agents/skills/routing/nested/SKILL.md",
            ".agents/workflows/unregistered.md",
            ".claude/provider/extra.md",
            ".codex/provider-extra.md",
        ):
            with (
                self.subTest(path=path),
                self.assertRaisesRegex(
                    contracts.DocumentContractError, "REGISTRY_ROUTE_UNCOVERED"
                ),
            ):
                contracts.classify_path(self.registry, PurePosixPath(path))

    def test_tracked_hidden_markdown_is_in_full_document_inventory(self) -> None:
        path = PurePosixPath(".agents/governance/quality.md")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / path
            target.parent.mkdir(parents=True)
            target.write_text("# Current policy\n", encoding="utf-8")
            record = f"100644 {'1' * 40} 0\t{path}\0".encode()
            with mock.patch.object(contracts, "_run_git", return_value=record):
                inventory = contracts.enumerate_target_markdown(root)
            self.assertIn(path, inventory.current_paths)

    def test_native_skill_metadata_preserves_explicit_typed_invocation_control(
        self,
    ) -> None:
        path = PurePosixPath(".agents/skills/docs-stage-routing/SKILL.md")
        profile = contracts.classify_path(self.registry, path)
        valid = (
            '---\nname: "docs-stage-routing"\n'
            'description: "Route authored documents."\n'
            "disable-model-invocation: true\n---\n\n# Routing\n"
        )
        schema = MARKDOWN.load_frontmatter_schema(ROOT)
        self.assertEqual(
            MARKDOWN.validate_document_text(
                valid, path, profile, "strict", frontmatter_schema=schema
            ),
            [],
        )
        for replacement in ('"true"', "false", "1", "yes", "null"):
            with self.subTest(value=replacement):
                invalid = valid.replace(
                    "disable-model-invocation: true",
                    f"disable-model-invocation: {replacement}",
                )
                self.assertTrue(
                    MARKDOWN.validate_document_text(invalid, path, profile, "strict")
                )
        for invalid in (
            valid.replace("disable-model-invocation: true\n", ""),
            valid.replace("---\n\n#", "tools: Bash\n---\n\n#"),
            valid.replace("---\n\n#", "disable-model-invocation: true\n---\n\n#"),
        ):
            with self.subTest(invalid=invalid):
                self.assertTrue(
                    MARKDOWN.validate_document_text(invalid, path, profile, "strict")
                )

    def test_retired_governance_root_rejects_even_a_dangling_link(self) -> None:
        source = (ROOT / "scripts/validation/repository/quality.py").read_text(
            encoding="utf-8"
        )
        candidates = [
            node
            for node in ast.parse(source).body
            if isinstance(node, ast.If) and "os.path.lexists" in ast.unparse(node.test)
        ]
        code = compile(ast.Module(body=candidates, type_ignores=[]), "quality", "exec")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".agents").mkdir()
            failures: list[str] = []
            context = {"root": root, "os": os, "fail": failures.append}
            exec(code, context)
            self.assertEqual(failures, [])
            old = root / "docs/00.agent-governance"
            old.parent.mkdir()
            old.symlink_to("missing-governance")
            exec(code, context)
            self.assertTrue(failures)
            old.unlink()
            failures.clear()
            (root / ".agents/memory").mkdir()
            exec(code, context)
            self.assertTrue(failures)

    def test_common_agent_documents_and_native_sidecars_stay_english_only(self) -> None:
        source = (ROOT / "scripts/validation/repository/quality.py").read_text(
            encoding="utf-8"
        )
        nodes = ast.parse(source).body
        start = next(
            index
            for index, node in enumerate(nodes)
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "tracked_language_roots"
                for target in node.targets
            )
        )
        code = compile(
            ast.Module(body=nodes[start : start + 2], type_ignores=[]),
            "quality",
            "exec",
        )
        paths = (
            ".agents/README.md",
            ".agents/governance/quality.md",
            ".agents/skills/routing/SKILL.md",
            ".agents/skills/routing/agents/openai.yaml",
            ".claude/provider.md",
            ".codex/provider.md",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for path in paths:
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(
                    "English policy.\n한국어 실행 계약\n", encoding="utf-8"
                )
            failures: list[str] = []
            exec(
                code,
                {
                    "root": root,
                    "re": re,
                    "tracked": set(paths),
                    "read_text": lambda path: path.read_text(encoding="utf-8"),
                    "fail": failures.append,
                },
            )
            self.assertEqual(len(failures), len(paths))


if __name__ == "__main__":
    unittest.main()
