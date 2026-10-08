"""Focused content boundaries for authored operation role sections."""

from __future__ import annotations

import copy
import dataclasses
import importlib.util
import json
import sys
import unittest
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import document_contracts as contracts  # noqa: E402


def load_markdown_validator():
    specification = importlib.util.spec_from_file_location(
        "operations_section_markdown", ROOT / "scripts/validate-markdown-profiles.py"
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


markdown = load_markdown_validator()
REGISTRY = json.loads((ROOT / "docs/99.templates/registry.json").read_text())
SCHEMA = json.loads(
    (ROOT / "docs/99.templates/contracts/document-profile.schema.json").read_text()
)
GUIDE = next(
    profile for profile in REGISTRY["profiles"] if profile["id"] == "operation/guide"
)
GUIDE_PATH = PurePosixPath("docs/05.operations/guides/9999-section-example.md")


def guide_profile(*, substantive_body: bool):
    raw = copy.deepcopy(GUIDE)
    raw["sections"] = {
        "required": ["Purpose"],
        "optional": [],
        "forbidden": [],
        "substantive_body": substantive_body,
    }
    return contracts._profile_from_mapping(raw, lifecycle_domain=None)


def rules(body: str, *, substantive_body: bool = True) -> list[str]:
    profile = guide_profile(substantive_body=substantive_body)
    diagnostics = markdown._body_diagnostics(
        GUIDE_PATH, profile, f"# Example\n\n## Purpose\n{body}\n"
    )
    return [item.rule_id for item in diagnostics]


class OperationsSectionContractTests(unittest.TestCase):
    def test_schema_and_loader_accept_only_boolean_opt_in(self) -> None:
        profile_schema = SCHEMA["properties"]["profiles"]["items"]
        profile = copy.deepcopy(GUIDE)
        profile["sections"]["substantive_body"] = True
        profile["sections"]["ordered"] = True
        self.assertFalse(
            list(Draft202012Validator(profile_schema).iter_errors(profile))
        )
        self.assertTrue(
            contracts._profile_from_mapping(
                profile, lifecycle_domain=None
            ).headings.substantive_body
        )
        self.assertTrue(
            contracts._profile_from_mapping(
                profile, lifecycle_domain=None
            ).headings.ordered
        )

        profile["sections"]["substantive_body"] = "true"
        self.assertTrue(list(Draft202012Validator(profile_schema).iter_errors(profile)))

        profile["sections"].pop("substantive_body")
        profile["sections"].pop("ordered")
        self.assertFalse(
            contracts._profile_from_mapping(
                profile, lifecycle_domain=None
            ).headings.substantive_body
        )
        self.assertFalse(
            contracts._profile_from_mapping(
                profile, lifecycle_domain=None
            ).headings.ordered
        )

    def test_opted_in_required_h2_follows_declared_relative_order(self) -> None:
        profile = guide_profile(substantive_body=False)
        profile = dataclasses.replace(
            profile,
            headings=dataclasses.replace(
                profile.headings,
                required=("Purpose", "Evidence"),
                allowed=("Purpose", "Evidence"),
                ordered=True,
            ),
        )
        source = "# Example\n\n## Evidence\nActual evidence.\n\n## Purpose\nActual purpose.\n"
        diagnostics = markdown._body_diagnostics(GUIDE_PATH, profile, source)
        self.assertIn("BODY-H2-ORDER", [item.rule_id for item in diagnostics])

        reordered = source.replace(
            "## Evidence\nActual evidence.\n\n## Purpose\nActual purpose.",
            "## Purpose\nActual purpose.\n\n## Evidence\nActual evidence.",
        )
        diagnostics = markdown._body_diagnostics(GUIDE_PATH, profile, reordered)
        self.assertNotIn("BODY-H2-ORDER", [item.rule_id for item in diagnostics])

    def test_subheadings_placeholders_and_table_header_do_not_fill_required_section(
        self,
    ) -> None:
        bodies = (
            "### Detail\n",
            "TBD\n",
            "TODO\n",
            "N/A\n",
            "NA\n",
            "pending\n",
            "| Item | Detail |\n| --- | --- |\n",
            "Item | Detail\n--- | ---\n",
            "| Item | Detail |\n| --- | --- |\n| TODO | N/A |\n",
            "```text\n```\n",
            "```text\nTODO\n```\n",
            "```text\nN/A\n```\n",
            "<!-- explanation pending -->\n",
            "- [ ] TODO\n",
            "- [x] TODO\n",
            "- [ ]\n",
            '<a id="noop"></a>\n',
            '<a id="noop"></a> TODO\n',
        )
        for body in bodies:
            with self.subTest(body=body):
                self.assertIn("BODY-HEADING-EMPTY", rules(body))

    def test_real_prose_table_row_code_and_contextual_na_fill_section(self) -> None:
        bodies = (
            "This guide covers initial platform setup.\n",
            "### Detail\nThe operator checks the outcome here.\n",
            "| Item | Detail |\n| --- | --- |\n| Owner | platform |\n",
            "Item | Detail\n--- | ---\nOwner | platform\n",
            "```sh\nkubectl get pods\n```\n",
            "```sh\necho TODO\n```\n",
            "N/A: this step applies only when service mesh is installed.\n",
            "- [ ] Confirm the operator has a current change record.\n",
            "- [x] Verified the current platform bootstrap sequence.\n",
            '<a id="purpose">This heading explains when to use the guide.</a>\n',
            '<a id="purpose"></a> This guide names the current owner.\n',
        )
        for body in bodies:
            with self.subTest(body=body):
                self.assertNotIn("BODY-HEADING-EMPTY", rules(body))

    def test_nested_role_heading_is_rejected_even_when_prose_exists(self) -> None:
        self.assertIn(
            "BODY-HEADING-NESTED-ROLE",
            rules("A real introductory sentence.\n\n### Purpose\nA second sentence.\n"),
        )
        self.assertNotIn(
            "BODY-HEADING-NESTED-ROLE",
            rules("A real sentence.\n\n```md\n### Purpose\n```\n"),
        )
        self.assertIn(
            "BODY-HEADING-NESTED-ROLE",
            rules("Actual purpose.\n\n## Extra\n### Purpose\n"),
        )

    def test_unflagged_legacy_profile_keeps_existing_empty_rule(self) -> None:
        self.assertNotIn(
            "BODY-HEADING-EMPTY", rules("### Detail\n", substantive_body=False)
        )
        self.assertNotIn(
            "BODY-HEADING-NESTED-ROLE",
            rules("### Purpose\n", substantive_body=False),
        )


if __name__ == "__main__":
    unittest.main()
