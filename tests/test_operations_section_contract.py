"""Focused content boundaries for authored operation role sections."""

from __future__ import annotations

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
SCHEMA = json.loads(
    (ROOT / "docs/99.templates/contracts/document-profile.schema.json").read_text()
)
GUIDE_PATH = PurePosixPath("docs/05.operations/guides/9999-section-example.md")


RETAINED_STATUS = "accepted"


def retained_extension(**lists):
    """A registered retained form whose H2 lists are the one place a list survives."""

    return {
        "id": "example-retained-form",
        "kind": "retained_form",
        "condition": "an example",
        "owner": "platform",
        "verification": "this test",
        "review": "never",
        "removal": "never",
        "statuses": [RETAINED_STATUS],
        "retained_sections": {
            "required": ["Purpose"],
            "optional": [],
            "forbidden": [],
            **lists,
        },
    }


def guide_profile(*, substantive_body: bool, **lists):
    """The guide profile with a retained form (SPEC-0205): a profile list branch is
    reachable only through a retained form, so the list rules are checked there."""

    profile = contracts.load_registry(ROOT).profiles
    profile = next(item for item in profile if item.profile_id == "operation/guide")
    extension = contracts._common_form_from_mapping(
        {
            "form_id": "guide",
            "title": "guide form",
            "h1": "{{document_title}}",
            "language_rule": "English body",
            "extension_policy": "Register every local heading.",
            "sections": [],
            "extensions": [
                retained_extension(substantive_body=substantive_body, **lists)
            ],
        }
    ).extensions
    return dataclasses.replace(
        profile,
        form=dataclasses.replace(
            profile.form, extensions=(*profile.form.extensions, *extension)
        ),
    )


def rules(body: str, *, substantive_body: bool = True) -> list[str]:
    profile = guide_profile(substantive_body=substantive_body)
    diagnostics = markdown._body_diagnostics(
        GUIDE_PATH, profile, f"# Example\n\n## Purpose\n{body}\n", RETAINED_STATUS
    )
    return [item.rule_id for item in diagnostics]


class OperationsSectionContractTests(unittest.TestCase):
    def test_schema_and_loader_accept_only_boolean_opt_in(self) -> None:
        lists_schema = {"$ref": "#/$defs/heading_lists", "$defs": SCHEMA["$defs"]}
        extension = retained_extension(substantive_body=True, ordered=True)
        self.assertFalse(
            list(
                Draft202012Validator(lists_schema).iter_errors(
                    extension["retained_sections"]
                )
            )
        )
        retained = guide_profile(substantive_body=True, ordered=True).form.extensions[
            -1
        ]
        self.assertTrue(retained.retained.substantive_body)
        self.assertTrue(retained.retained.ordered)

        extension["retained_sections"]["substantive_body"] = "true"
        self.assertTrue(
            list(
                Draft202012Validator(lists_schema).iter_errors(
                    extension["retained_sections"]
                )
            )
        )

        extension["retained_sections"].pop("substantive_body")
        extension["retained_sections"].pop("ordered")
        loaded = contracts._common_form_from_mapping(
            {
                "form_id": "guide",
                "title": "guide form",
                "h1": "{{document_title}}",
                "language_rule": "English body",
                "extension_policy": "Register every local heading.",
                "sections": [],
                "extensions": [extension],
            }
        ).extensions[0]
        self.assertFalse(loaded.retained.substantive_body)
        self.assertFalse(loaded.retained.ordered)

    def test_opted_in_required_h2_follows_declared_relative_order(self) -> None:
        profile = guide_profile(
            substantive_body=False,
            required=["Purpose", "Evidence"],
            ordered=True,
        )
        source = "# Example\n\n## Evidence\nActual evidence.\n\n## Purpose\nActual purpose.\n"
        diagnostics = markdown._body_diagnostics(
            GUIDE_PATH, profile, source, RETAINED_STATUS
        )
        self.assertIn("BODY-H2-ORDER", [item.rule_id for item in diagnostics])

        reordered = source.replace(
            "## Evidence\nActual evidence.\n\n## Purpose\nActual purpose.",
            "## Purpose\nActual purpose.\n\n## Evidence\nActual evidence.",
        )
        diagnostics = markdown._body_diagnostics(
            GUIDE_PATH, profile, reordered, RETAINED_STATUS
        )
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

    def test_link_only_body_does_not_fill_an_instruction_section(self) -> None:
        for body in (
            "[RUN-0001](../runbooks/0001-example.md)\n",
            "- [RUN-0001](../runbooks/0001-example.md)\n- [POL-0001](./0001-x.md)\n",
            "<https://example.invalid/runbook>\n",
        ):
            with self.subTest(body=body):
                self.assertIn("BODY-HEADING-EMPTY", rules(body))
        self.assertNotIn(
            "BODY-HEADING-EMPTY",
            rules("Restart the controller as [RUN-0001](./0001-x.md) step 3 says.\n"),
        )

    def test_navigation_section_may_hold_links_only(self) -> None:
        content = markdown._scan_required_h2_content(
            "# Example\n\n## Related Documents\n- [RUN-0001](./0001-x.md)\n",
            ("Related Documents",),
            substantive_body=True,
        )
        self.assertEqual(content.empty, ())

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
