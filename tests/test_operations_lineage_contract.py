"""Owner-key lineage follows the registered relationship section."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from dataclasses import replace
from pathlib import Path, PurePosixPath
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import document_contracts as contracts  # noqa: E402


def load_links_validator():
    specification = importlib.util.spec_from_file_location(
        "operations_lineage_links", ROOT / "scripts/validate-links-and-owners.py"
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


links = load_links_validator()
REGISTRY = json.loads((ROOT / "docs/99.templates/registry.json").read_text())
GUIDE = next(
    profile for profile in REGISTRY["profiles"] if profile["id"] == "operation/guide"
)


class OperationsLineageContractTests(unittest.TestCase):
    def test_duplicate_owner_uses_registered_relationship_section(self) -> None:
        raw = copy.deepcopy(GUIDE)
        profile = contracts._profile_from_mapping(raw, lifecycle_domain=None)
        profile = replace(
            profile,
            body_contract=replace(profile.body_contract, section="Related Documents"),
        )
        first = PurePosixPath("docs/05.operations/guides/0001-example-guide.md")
        second = PurePosixPath("docs/05.operations/guides/0002-example-guide.md")
        view = links.ProfileView(
            profile.profile_id, profile.profile_class, profile.mode
        )
        context = SimpleNamespace(
            root=ROOT,
            paths=(first, second),
            profiles={first: view, second: view},
            metadata={
                first: {"title": "Shared example", "type": "guide", "status": "active"},
                second: {
                    "title": "Shared example",
                    "type": "guide",
                    "status": "active",
                },
            },
            texts={
                first: self._body("0001-unrelated", "0003-shared"),
                second: self._body("0002-unrelated", "0003-shared"),
            },
            document_registry=SimpleNamespace(profiles=(profile,)),
        )

        keys, diagnostics = links._owner_state(context)

        self.assertEqual(keys[first], keys[second])
        self.assertEqual([item.rule_id for item in diagnostics], ["OWNER-DUPLICATE"])

    @staticmethod
    def _body(unrelated: str, shared: str) -> str:
        return (
            "# Example\n\n"
            "## Traceability\n"
            f"[unrelated](../../01.requirements/{unrelated}.md)\n\n"
            "## Related Documents\n"
            f"[shared](../../01.requirements/{shared}.md)\n"
        )


if __name__ == "__main__":
    unittest.main()
