"""SPEC-0168: the common form model, its registry checks and heading-tree checks."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import document_authority as AUTHORITY  # noqa: E402
import document_contracts as CONTRACTS  # noqa: E402


def _load_script(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


REGISTRY_CHECK = _load_script(
    "common_form_registry_check", "validate-document-contract-registry.py"
)
MARKDOWN = _load_script("common_form_markdown", "validate-markdown-profiles.py")

ROLE_IDS = (
    "requirement",
    "architecture",
    "adr",
    "spec",
    "plan",
    "task",
    "guide",
    "runbook",
    "policy",
    "incident",
    "postmortem",
    "root-readme",
    "stage-readme",
    "service-readme",
    "agents",
    "skill",
)
# The profiles whose common role is clear; every other profile carries none.
ROLE_BINDINGS = {
    "sdlc/requirement": "requirement",
    "sdlc/architecture-description": "architecture",
    "sdlc/architecture-decision": "adr",
    "sdlc/spec": "spec",
    "sdlc/plan": "plan",
    "sdlc/task": "task",
    "operation/guide": "guide",
    "operation/runbook": "runbook",
    "operation/incident": "incident",
    "operation/postmortem": "postmortem",
    "governance/rule": "policy",
    "operation/policy": "policy",
    "common/readme-repository": "root-readme",
    "common/readme-stage-index": "stage-readme",
}
GUIDE = ("operation/guide", "common/template-operation-guide")
ADR = ("sdlc/architecture-decision", "common/template-sdlc-architecture-decision")


def load_raw() -> dict:
    return json.loads((ROOT / "docs/99.templates/registry.json").read_text("utf-8"))


def section(
    section_id: str,
    title: str,
    level: int,
    parent: str | None,
    order: int,
    *,
    requiredness: str = "required",
    condition: str = "always",
    link_only: bool | None = None,
    children: tuple[dict, ...] = (),
) -> dict:
    item = {
        "section_id": section_id,
        "level": level,
        "parent_id": parent,
        "title": title,
        "order": order,
        "requiredness": requiredness,
        "condition": condition,
        "content": f"{title} content",
        "required_content": [f"State the {title}."],
        "prohibited_content": [f"Never leave {title} empty."],
        "empty_policy": (
            "omit_when_condition_false"
            if requiredness == "conditional"
            else "explain_none_or_not_applicable"
        ),
        "validation_ids": ["FORM-STRUCTURE"],
        "children": list(children),
    }
    if link_only is not None:
        item["link_only"] = link_only
    return item


def guide_sections() -> list[dict]:
    return [
        section(
            "g-overview",
            "Overview",
            2,
            None,
            1,
            children=(
                section("g-purpose", "Purpose", 3, "g-overview", 1),
                section("g-context", "Context", 3, "g-overview", 2),
            ),
        ),
        section(
            "g-procedure",
            "Procedure",
            2,
            None,
            2,
            children=(
                section("g-steps", "Steps", 3, "g-procedure", 1),
                section(
                    "g-rollback",
                    "Rollback",
                    3,
                    "g-procedure",
                    2,
                    requiredness="conditional",
                    condition="the procedure changes state",
                ),
            ),
        ),
        section("g-related", "Related Documents", 2, None, 3, link_only=True),
    ]


def extension(**fields: object) -> dict:
    item = {
        "id": "g-ext",
        "kind": "local_h3",
        "condition": "the guide covers a cluster-specific step",
        "owner": "platform",
        "verification": "tests/test_common_form_tree.py",
        "review": "each release",
        "removal": "when no guide needs it",
        "parent_id": "g-procedure",
        "title": "Cluster Notes",
    }
    item.update(fields)
    return item


def definition(**fields: object) -> dict:
    item = {
        "purpose": "Give authors the guide form.",
        "responsibility": "One guide per procedure.",
        "non_goals": ["Runbook steps"],
        "policy_refs": [".agents/governance/document-authoring.md"],
        "vocabulary_refs": ["docs/99.templates/registry.json"],
        "applicability": "Stage 05 guides",
        "consumer_paths": ["scripts/validate-markdown-profiles.py"],
        "validation": {
            "positive": ["tests/test_common_form_tree.py"],
            "negative": ["tests/test_common_form_tree.py"],
            "regression": ["tests/test_common_form_tree.py"],
        },
        "migration": {
            "meaning_map": "H2 headings map to form sections",
            "retained_history": "completed documents keep their headings",
            "rollback": "revert the change",
        },
    }
    item.update(fields)
    return item


def form(role: str, sections: list[dict], extensions: list[dict] | None = None) -> dict:
    return {
        "form_id": role,
        "title": f"{role} form",
        "h1": "{{document_title}}",
        "language_rule": "English body",
        "extension_policy": "Register every local heading.",
        "sections": sections,
        "extensions": extensions or [],
    }


def with_form(
    raw: dict,
    role: str,
    profile_ids: tuple[str, ...],
    sections: list[dict],
    *,
    extensions: list[dict] | None = None,
    definitions: bool = True,
) -> dict:
    """A temporary registry that gives one role a form and moves its profiles to it."""

    candidate = copy.deepcopy(raw)
    for profile in candidate["profiles"]:
        if profile["id"] in profile_ids:
            profile["document_role"] = role
            profile["sections"].update(required=[], optional=[], forbidden=[])
            profile["relationships"]["body_contract"] = None
            if profile["mode"] == "template" and definitions:
                profile["template_definition"] = definition()
    candidate["common_forms"]["forms"] = [form(role, sections, extensions)]
    return candidate


def rules_of(raw: dict) -> set[str]:
    try:
        CONTRACTS.validate_registry(ROOT, raw)
    except CONTRACTS.DocumentContractError as error:
        return {item.rule_id for item in error.diagnostics}
    return set()


class RepositoryRegistryTests(unittest.TestCase):
    def test_repository_registry_binds_clear_roles_and_carries_no_form(self) -> None:
        raw = load_raw()
        self.assertEqual(raw["schema_version"], 10)
        self.assertEqual(
            raw["common_forms"],
            {"contract_id": "COMMON-DOC-FORM-1", "version": "1.0.0", "forms": []},
        )
        by_id = {profile["id"]: profile for profile in raw["profiles"]}
        for profile_id, profile in by_id.items():
            sources = profile["relationships"]["source_profile_ids"]
            expected = ROLE_BINDINGS.get(
                profile_id, ROLE_BINDINGS.get(sources[0]) if sources else None
            )
            with self.subTest(profile=profile_id):
                self.assertEqual(profile.get("document_role"), expected)
                self.assertNotIn("template_definition", profile)
        self.assertEqual(
            {
                by_id[i]["document_role"]
                for i in (
                    "governance/rule",
                    "operation/policy",
                    "common/template-governance-rule",
                    "common/template-operation-policy",
                )
            },
            {"policy"},
        )

    def test_repository_registry_loads_without_a_form(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        self.assertEqual(registry.common_forms, ())
        for profile in registry.profiles:
            self.assertIsNone(profile.form)
        by_id = {profile.profile_id: profile for profile in registry.profiles}
        self.assertEqual(by_id["governance/rule"].document_role, "policy")
        self.assertIsNone(by_id["governance/role"].document_role)

    def test_schema_role_and_form_enums_are_the_sixteen_common_roles(self) -> None:
        schema = json.loads(
            (
                ROOT / "docs/99.templates/contracts/document-profile.schema.json"
            ).read_text("utf-8")
        )
        profile_role = schema["properties"]["profiles"]["items"]["properties"][
            "document_role"
        ]["enum"]
        form_id = schema["$defs"]["common_form"]["properties"]["form_id"]["enum"]
        self.assertEqual(tuple(profile_role), ROLE_IDS)
        self.assertEqual(tuple(form_id), ROLE_IDS)
        self.assertEqual(
            schema["$defs"]["section"]["properties"]["level"]["enum"], [2, 3]
        )
        self.assertIn("link_only", schema["$defs"]["section"]["properties"])


class FormRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.raw = load_raw()

    def candidate(self, sections: list[dict] | None = None, **extra) -> dict:
        return with_form(
            self.raw, "guide", GUIDE, sections or guide_sections(), **extra
        )

    def test_valid_form_binds_to_every_profile_of_its_role(self) -> None:
        registry = CONTRACTS.validate_registry(ROOT, self.candidate())
        self.assertEqual([item.form_id for item in registry.common_forms], ["guide"])
        loaded = registry.common_forms[0]
        self.assertEqual(
            [item.title for item in loaded.sections],
            ["Overview", "Procedure", "Related Documents"],
        )
        self.assertEqual(
            [child.title for child in loaded.sections[0].children],
            ["Purpose", "Context"],
        )
        self.assertTrue(loaded.sections[2].link_only)
        self.assertFalse(loaded.sections[0].link_only)
        by_id = {profile.profile_id: profile for profile in registry.profiles}
        for profile_id in GUIDE:
            self.assertIs(by_id[profile_id].form, loaded)
        self.assertIsNone(by_id["operation/runbook"].form)

    def test_valid_extensions_are_typed(self) -> None:
        retained = {
            "id": "g-legacy",
            "kind": "retained_form",
            "condition": "terminal documents keep their H2 headings",
            "owner": "platform",
            "verification": "tests/test_common_form_tree.py",
            "review": "each release",
            "removal": "when no terminal guide remains",
            "statuses": ["retired"],
            "retained_sections": {
                "required": ["Overview"],
                "optional": [],
                "forbidden": [],
            },
        }
        registry = CONTRACTS.validate_registry(
            ROOT, self.candidate(extensions=[extension(), retained])
        )
        local, kept = registry.common_forms[0].extensions
        self.assertEqual(
            (local.kind, local.parent_id, local.title),
            ("local_h3", "g-procedure", "Cluster Notes"),
        )
        self.assertEqual(local.owner, "platform")
        self.assertEqual((kept.kind, kept.statuses), ("retained_form", ("retired",)))
        self.assertEqual(kept.retained.required, ("Overview",))

    def test_bad_parent_is_refused(self) -> None:
        sections = guide_sections()
        sections[0]["children"][1]["parent_id"] = "g-procedure"
        self.assertIn("REGISTRY_FORM_PARENT", rules_of(self.candidate(sections)))

    def test_wrong_level_is_refused(self) -> None:
        sections = guide_sections()
        sections[0]["children"][0]["level"] = 2
        self.assertIn("REGISTRY_FORM_LEVEL", rules_of(self.candidate(sections)))
        sections = guide_sections()
        sections[1]["level"] = 3
        self.assertIn("REGISTRY_FORM_LEVEL", rules_of(self.candidate(sections)))

    def test_duplicate_or_unsorted_sibling_order_is_refused(self) -> None:
        sections = guide_sections()
        sections[0]["children"][1]["order"] = 1
        self.assertIn("REGISTRY_FORM_ORDER", rules_of(self.candidate(sections)))
        sections = guide_sections()
        sections[1]["order"] = 1
        self.assertIn("REGISTRY_FORM_ORDER", rules_of(self.candidate(sections)))
        sections = guide_sections()
        sections[0]["children"].reverse()
        self.assertIn("REGISTRY_FORM_ORDER", rules_of(self.candidate(sections)))

    def test_conditional_section_cannot_be_always(self) -> None:
        sections = guide_sections()
        sections[1]["children"][1]["condition"] = "always"
        self.assertIn("REGISTRY_FORM_CONDITION", rules_of(self.candidate(sections)))

    def test_duplicate_section_ids_and_sibling_titles_are_refused(self) -> None:
        sections = guide_sections()
        sections[1]["children"][0]["section_id"] = "g-purpose"
        self.assertIn("REGISTRY_FORM_SECTION", rules_of(self.candidate(sections)))
        sections = guide_sections()
        sections[0]["children"][1]["title"] = "Purpose"
        self.assertIn("REGISTRY_FORM_SECTION", rules_of(self.candidate(sections)))

    def test_legacy_h2_lists_beside_a_form_are_refused(self) -> None:
        raw = self.candidate()
        profile = next(item for item in raw["profiles"] if item["id"] == GUIDE[0])
        profile["sections"]["required"] = ["Overview"]
        self.assertIn("REGISTRY_FORM_LEGACY_LISTS", rules_of(raw))
        raw = self.candidate()
        profile = next(item for item in raw["profiles"] if item["id"] == GUIDE[1])
        profile["sections"]["forbidden"] = ["Scratch"]
        self.assertIn("REGISTRY_FORM_LEGACY_LISTS", rules_of(raw))

    def test_duplicate_form_ids_are_refused(self) -> None:
        raw = self.candidate()
        raw["common_forms"]["forms"].append(
            copy.deepcopy(raw["common_forms"]["forms"][0])
        )
        self.assertIn("REGISTRY_FORM_DUPLICATE", rules_of(raw))

    def test_extension_without_an_owner_is_refused(self) -> None:
        for key in ("owner", "condition", "verification", "review", "removal"):
            item = extension()
            del item[key]
            with self.subTest(missing=key):
                self.assertIn(
                    "REGISTRY_SCHEMA", rules_of(self.candidate(extensions=[item]))
                )

    def test_extension_shape_and_parent_are_checked(self) -> None:
        for bad in (
            extension(parent_id="g-missing"),
            extension(parent_id="g-steps"),
            extension(title="Steps"),
        ):
            with self.subTest(extension=bad):
                self.assertIn(
                    "REGISTRY_FORM_EXTENSION",
                    rules_of(self.candidate(extensions=[bad])),
                )
        item = extension()
        del item["parent_id"]
        self.assertIn("REGISTRY_SCHEMA", rules_of(self.candidate(extensions=[item])))
        retained = extension(kind="retained_form")
        self.assertIn(
            "REGISTRY_SCHEMA", rules_of(self.candidate(extensions=[retained]))
        )
        twice = [extension(), extension(title="Other Notes")]
        self.assertIn(
            "REGISTRY_FORM_EXTENSION", rules_of(self.candidate(extensions=twice))
        )

    def test_unknown_roles_are_refused_by_the_schema(self) -> None:
        raw = self.candidate()
        raw["common_forms"]["forms"][0]["form_id"] = "release"
        self.assertIn("REGISTRY_SCHEMA", rules_of(raw))
        raw = load_raw()
        next(item for item in raw["profiles"] if item["id"] == GUIDE[0])[
            "document_role"
        ] = "release"
        self.assertIn("REGISTRY_SCHEMA", rules_of(raw))

    def test_agent_fields_stay_forbidden_everywhere(self) -> None:
        raw = load_raw()
        next(item for item in raw["profiles"] if item["id"] == GUIDE[0])["role"] = (
            "guide"
        )
        with self.assertRaisesRegex(AUTHORITY.AuthorityError, "STAGE99_AGENT_FIELD"):
            AUTHORITY.validate_registry_authority(raw)
        self.assertIn("REGISTRY_SCHEMA", rules_of(raw))
        raw = self.candidate()
        raw["common_forms"]["forms"][0]["skill"] = "docs"
        with self.assertRaisesRegex(AUTHORITY.AuthorityError, "STAGE99_AGENT_FIELD"):
            AUTHORITY.validate_registry_authority(raw)
        raw = self.candidate()
        raw["common_forms"]["forms"][0]["sections"][0]["roles"] = ["guide"]
        with self.assertRaisesRegex(AUTHORITY.AuthorityError, "STAGE99_AGENT_FIELD"):
            AUTHORITY.validate_registry_authority(raw)

    def test_authority_admits_exactly_the_three_new_optional_keys(self) -> None:
        raw = self.candidate()
        AUTHORITY.validate_registry_authority(raw)
        profile = next(item for item in raw["profiles"] if item["id"] == GUIDE[1])
        profile["template_definition"] = {}
        AUTHORITY.validate_registry_authority(raw)
        profile["document_roles"] = "guide"
        with self.assertRaisesRegex(
            AUTHORITY.AuthorityError, "REGISTRY_PROFILE_FIELDS"
        ):
            AUTHORITY.validate_registry_authority(raw)
        raw = load_raw()
        raw["common_form"] = {}
        with self.assertRaisesRegex(AUTHORITY.AuthorityError, "REGISTRY_TOP_LEVEL"):
            AUTHORITY.validate_registry_authority(raw)
        del raw["common_form"], raw["common_forms"]
        AUTHORITY.validate_registry_authority(raw)

    def test_policy_roles_cannot_differ(self) -> None:
        for mutate in (
            lambda by_id: by_id["operation/policy"].update(document_role="guide"),
            lambda by_id: by_id["governance/rule"].pop("document_role"),
            lambda by_id: by_id["common/template-operation-policy"].update(
                document_role="runbook"
            ),
        ):
            raw = load_raw()
            mutate({profile["id"]: profile for profile in raw["profiles"]})
            self.assertIn("REGISTRY_POLICY_ROLE", rules_of(raw))
        raw = load_raw()
        for profile in raw["profiles"]:
            profile.pop("document_role", None)
        self.assertEqual(rules_of(raw), set())

    def test_template_twin_must_share_its_sources_role(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        REGISTRY_CHECK._assert_template_source_parity(registry)
        raw = load_raw()
        next(item for item in raw["profiles"] if item["id"] == GUIDE[1])[
            "document_role"
        ] = "runbook"
        loaded = CONTRACTS.validate_registry(ROOT, raw)
        with self.assertRaisesRegex(AssertionError, "template/source contract differs"):
            REGISTRY_CHECK._assert_template_source_parity(loaded)
        raw = load_raw()
        next(item for item in raw["profiles"] if item["id"] == GUIDE[1]).pop(
            "document_role"
        )
        loaded = CONTRACTS.validate_registry(ROOT, raw)
        with self.assertRaisesRegex(AssertionError, "template/source contract differs"):
            REGISTRY_CHECK._assert_template_source_parity(loaded)

    def test_twin_with_the_same_role_shares_the_form(self) -> None:
        loaded = CONTRACTS.validate_registry(ROOT, self.candidate())
        REGISTRY_CHECK._assert_template_source_parity(loaded)


class TemplateDefinitionTests(unittest.TestCase):
    def candidate(self, given: dict | None, *, on: str = GUIDE[1]) -> dict:
        raw = with_form(load_raw(), "guide", GUIDE, guide_sections(), definitions=False)
        if given is not None:
            next(item for item in raw["profiles"] if item["id"] == on)[
                "template_definition"
            ] = given
        return raw

    def test_complete_definition_on_a_template_profile_is_accepted(self) -> None:
        raw = self.candidate(definition())
        self.assertEqual(rules_of(raw), set())
        profile = {
            item.profile_id: item
            for item in CONTRACTS.validate_registry(ROOT, raw).profiles
        }[GUIDE[1]]
        self.assertEqual(
            profile.template_definition["purpose"], "Give authors the guide form."
        )

    def test_form_role_requires_a_definition_on_its_template_twin(self) -> None:
        self.assertIn("REGISTRY_TEMPLATE_DEFINITION", rules_of(self.candidate(None)))

    def test_definition_is_refused_off_template_profiles_or_without_a_role(
        self,
    ) -> None:
        self.assertIn(
            "REGISTRY_TEMPLATE_DEFINITION",
            rules_of(self.candidate(definition(), on=GUIDE[0])),
        )
        raw = load_raw()
        twin = next(
            item
            for item in raw["profiles"]
            if item["id"] == "common/template-governance-role"
        )
        twin["template_definition"] = definition()
        self.assertIn("REGISTRY_TEMPLATE_DEFINITION", rules_of(raw))

    def test_named_paths_must_exist(self) -> None:
        raw = self.candidate(definition(consumer_paths=["scripts/missing.py"]))
        self.assertIn("REGISTRY_TEMPLATE_DEFINITION", rules_of(raw))

    def test_incomplete_definition_fails_the_schema(self) -> None:
        for key in ("purpose", "consumer_paths", "migration", "validation"):
            incomplete = definition()
            del incomplete[key]
            with self.subTest(missing=key):
                self.assertIn("REGISTRY_SCHEMA", rules_of(self.candidate(incomplete)))
        self.assertIn(
            "REGISTRY_SCHEMA",
            rules_of(self.candidate(definition(role="Release"))),
        )


H1 = "# Guide title"
OVERVIEW = (
    "## Overview",
    "### Purpose",
    "Explain why the guide exists.",
    "### Context",
    "Name where the guide applies.",
)
PROCEDURE = ("## Procedure", "### Steps", "Run the command and read the output.")
RELATED = ("## Related Documents", "- [Specification](spec.md)")
GUIDE_PATH = PurePosixPath("docs/05.operations/guides/0001-temporary-guide.md")


def md(*blocks: str) -> str:
    return "\n\n".join(blocks) + "\n"


VALID = md(H1, *OVERVIEW, *PROCEDURE, *RELATED)


def typed_profiles(raw: dict) -> dict:
    registry = CONTRACTS.validate_registry(ROOT, raw)
    return {profile.profile_id: profile for profile in registry.profiles}


class HeadingScanBodyTests(unittest.TestCase):
    def test_bodies_follow_headings_and_flag_fenced_lines(self) -> None:
        scan = MARKDOWN.scan_headings(
            md(
                "# T",
                "## A",
                "text\n```\n### x\n```\n<!-- ### y -->\n> ### z",
                "### B",
                "body",
            )
        )
        self.assertEqual(scan.headings, ((1, "T"), (2, "A"), (3, "B")))
        self.assertEqual(len(scan.bodies), 3)
        self.assertEqual(
            scan.bodies[1],
            (
                ("", False),
                ("text", False),
                ("### x", True),
                ("", False),
                ("> ### z", False),
                ("", False),
            ),
        )
        self.assertEqual(scan.bodies[2], (("", False), ("body", False)))
        self.assertFalse(scan.unclosed_fence)


class HeadingTreeTests(unittest.TestCase):
    """SPEC-0168 QA-C02: the heading-tree checks on one temporary guide form."""

    @classmethod
    def setUpClass(cls) -> None:
        raw = with_form(
            load_raw(), "guide", GUIDE, guide_sections(), extensions=[extension()]
        )
        profiles = typed_profiles(raw)
        cls.profile = profiles[GUIDE[0]]
        cls.template = profiles[GUIDE[1]]

    def found(self, text: str, *, profile=None, status: str = "active") -> list[str]:
        diagnostics = MARKDOWN._body_diagnostics(
            GUIDE_PATH, profile or self.profile, text, status
        )
        return sorted(item.rule_id for item in diagnostics)

    def test_a_complete_document_passes(self) -> None:
        self.assertEqual(self.found(VALID), [])

    def test_a_missing_conditional_h3_passes_and_a_present_one_needs_content(
        self,
    ) -> None:
        self.assertNotIn("Rollback", VALID)
        with_rollback = VALID.replace(
            "## Related Documents",
            "### Rollback\n\nRestore the previous value.\n\n## Related Documents",
        )
        self.assertEqual(self.found(with_rollback), [])
        empty = VALID.replace(
            "## Related Documents", "### Rollback\n\n## Related Documents"
        )
        self.assertEqual(self.found(empty), ["BODY-SECTION-EMPTY"])

    def test_wrong_parent(self) -> None:
        text = md(
            H1,
            "## Overview",
            "### Purpose\n\nWhy.",
            "### Context\n\nWhere.",
            "### Steps\n\nRun it.",
            "## Procedure",
            "Do things.",
            *RELATED,
        )
        self.assertEqual(self.found(text), ["BODY-H3-PARENT", "BODY-H3-REQUIRED"])

    def test_an_h3_without_an_h2_above_has_no_parent(self) -> None:
        self.assertEqual(
            self.found(md(H1, "### Stray\n\nText.", *OVERVIEW, *PROCEDURE, *RELATED)),
            ["BODY-H3-PARENT"],
        )

    def test_unknown_h3(self) -> None:
        text = VALID.replace("## Procedure", "### Mystery\n\nText.\n\n## Procedure")
        self.assertEqual(self.found(text), ["BODY-H3-UNSUPPORTED"])

    def test_duplicate_h3(self) -> None:
        text = VALID.replace("## Procedure", "### Purpose\n\nAgain.\n\n## Procedure")
        self.assertEqual(self.found(text), ["BODY-H3-DUPLICATE"])

    def test_reordered_h3_siblings(self) -> None:
        text = md(
            H1,
            "## Overview",
            "### Context\n\nWhere.",
            "### Purpose\n\nWhy.",
            *PROCEDURE,
            *RELATED,
        )
        self.assertEqual(self.found(text), ["BODY-H3-ORDER"])

    def test_missing_required_h3_under_a_present_h2(self) -> None:
        text = md(H1, "## Overview", "### Purpose\n\nWhy.", *PROCEDURE, *RELATED)
        self.assertEqual(self.found(text), ["BODY-H3-REQUIRED"])

    def test_a_missing_h2_reports_only_the_h2(self) -> None:
        self.assertEqual(
            self.found(md(H1, *PROCEDURE, *RELATED)), ["BODY-HEADING-REQUIRED"]
        )

    def test_h2_level_checks_use_the_registry_tree(self) -> None:
        self.assertEqual(
            self.found(VALID + "\n## Extras\n\nText.\n"), ["BODY-HEADING-UNSUPPORTED"]
        )
        self.assertEqual(
            self.found(md(H1, *PROCEDURE, *OVERVIEW, *RELATED)), ["BODY-H2-ORDER"]
        )
        self.assertEqual(
            self.found(VALID + "\n" + md(*PROCEDURE)), ["BODY-H2-DUPLICATE"]
        )

    def test_empty_and_bare_placeholder_sections_fail(self) -> None:
        for body in ("", "N/A", "N/A.", "TBD", "pending"):
            text = VALID.replace("Name where the guide applies.", body)
            with self.subTest(body=body):
                self.assertEqual(self.found(text), ["BODY-SECTION-EMPTY"])

    def test_not_applicable_with_a_reason_passes(self) -> None:
        text = VALID.replace(
            "Name where the guide applies.", "N/A: the guide has no wider context."
        )
        self.assertEqual(self.found(text), [])

    def test_table_and_code_content_count(self) -> None:
        table = VALID.replace(
            "Name where the guide applies.", "| Key | Value |\n| --- | --- |\n| a | b |"
        )
        self.assertEqual(self.found(table), [])
        code = VALID.replace(
            "Name where the guide applies.", "```text\nkubectl get pods\n```"
        )
        self.assertEqual(self.found(code), [])

    def test_link_only_sections_may_consist_of_links_alone(self) -> None:
        self.assertEqual(self.found(VALID), [])
        plain = VALID.replace(
            "Explain why the guide exists.", "- [Specification](spec.md)"
        )
        self.assertEqual(self.found(plain), ["BODY-SECTION-EMPTY"])
        bare = VALID.replace("- [Specification](spec.md)", "")
        self.assertEqual(self.found(bare), ["BODY-SECTION-EMPTY"])

    def test_headings_in_fences_comments_and_quotes_are_not_headings(self) -> None:
        for fake in (
            "```markdown\n### Bogus\n```",
            "<!-- ### Bogus -->",
            "> ### Bogus",
            "~~~\n## Extras\n~~~",
        ):
            text = VALID.replace(
                "Run the command and read the output.", fake + "\n\nRun it."
            )
            with self.subTest(fake=fake):
                self.assertEqual(self.found(text), [])
        fenced_required = md(
            H1, *OVERVIEW, "## Procedure", "```markdown\n### Steps\n```", *RELATED
        )
        self.assertEqual(self.found(fenced_required), ["BODY-H3-REQUIRED"])

    def test_deeper_headings_belong_to_their_h3(self) -> None:
        text = VALID.replace(
            "Run the command and read the output.",
            "#### Detail\n\nRun the command.",
        )
        self.assertEqual(self.found(text), [])

    def test_registered_extension_h3_needs_its_parent(self) -> None:
        notes = "### Cluster Notes\n\nThis step differs on this cluster."
        under_procedure = VALID.replace(
            "## Related Documents", notes + "\n\n## Related Documents"
        )
        self.assertEqual(self.found(under_procedure), [])
        under_overview = VALID.replace("## Procedure", notes + "\n\n## Procedure")
        self.assertEqual(self.found(under_overview), ["BODY-H3-PARENT"])
        empty = VALID.replace(
            "## Related Documents", "### Cluster Notes\n\n## Related Documents"
        )
        self.assertEqual(self.found(empty), ["BODY-SECTION-EMPTY"])

    def test_a_template_form_keeps_structure_checks_but_not_the_empty_rule(
        self,
    ) -> None:
        placeholders = md(
            "# {{DOCUMENT_TITLE}}",
            "## Overview",
            "### Purpose\n\n[Describe the purpose.]",
            "### Context\n\n",
            *PROCEDURE,
            *RELATED,
        )
        self.assertEqual(self.found(placeholders, profile=self.template), [])
        broken = placeholders.replace(
            "### Steps\n\nRun the command and read the output.", ""
        )
        self.assertEqual(
            self.found(broken, profile=self.template), ["BODY-H3-REQUIRED"]
        )

    def test_the_h1_and_author_prompt_checks_still_apply(self) -> None:
        self.assertEqual(self.found(VALID.replace(H1 + "\n\n", "")), ["BODY-H1"])
        self.assertEqual(
            self.found(VALID.replace(H1, H1 + "\n\n# Second")), ["BODY-H1"]
        )
        prompt = VALID.replace(H1, H1 + "\n\n<!-- Author prompt: fill this in -->")
        self.assertEqual(self.found(prompt), ["BODY-AUTHOR-PROMPT"])
        self.assertEqual(self.found(VALID + "\n```\n"), ["BODY-FENCE-UNCLOSED"])

    def test_an_end_to_end_document_in_a_temporary_root(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / GUIDE_PATH
            path.parent.mkdir(parents=True)
            path.write_text(VALID, encoding="utf-8")
            clean = MARKDOWN.validate_document(
                Path(root), GUIDE_PATH, self.profile, "strict"
            )
            path.write_text(
                VALID.replace("## Procedure", "### Mystery\n\nText.\n\n## Procedure"),
                encoding="utf-8",
            )
            broken = MARKDOWN.validate_document(
                Path(root), GUIDE_PATH, self.profile, "strict"
            )
        self.assertEqual(
            [i.rule_id for i in clean if i.rule_id.startswith("BODY-")], []
        )
        self.assertIn("BODY-H3-UNSUPPORTED", [i.rule_id for i in broken])


class RetainedFormTests(unittest.TestCase):
    """W03-D02: an ADR keeps its H2 lists for the statuses a retained form names."""

    ADR_PATH = PurePosixPath("docs/02.architecture/decisions/0099-temporary.md")
    LEGACY = md(
        "# Decision title",
        "## Context\n\nWhy we decide.",
        "## Decision\n\nWe decide.",
        "## Consequences\n\nWhat follows.",
    )
    TREE = md("# Decision title", "## Decision", "### Decision Statement\n\nWe decide.")

    @classmethod
    def setUpClass(cls) -> None:
        sections = [
            section(
                "a-decision",
                "Decision",
                2,
                None,
                1,
                children=(
                    section("a-statement", "Decision Statement", 3, "a-decision", 1),
                ),
            )
        ]
        retained = {
            "id": "a-legacy",
            "kind": "retained_form",
            "condition": "accepted decisions keep their H2 headings",
            "owner": "platform",
            "verification": "tests/test_common_form_tree.py",
            "review": "each release",
            "removal": "when no accepted ADR keeps the old headings",
            "statuses": ["accepted"],
            "retained_sections": {
                "required": ["Context", "Decision", "Consequences"],
                "optional": [],
                "forbidden": [],
            },
        }
        raw = with_form(load_raw(), "adr", ADR, sections, extensions=[retained])
        cls.profile = typed_profiles(raw)[ADR[0]]

    def found(self, text: str, status: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._body_diagnostics(
                self.ADR_PATH, self.profile, text, status
            )
        )

    def test_retained_form_applies_to_its_statuses_only(self) -> None:
        self.assertEqual(self.found(self.LEGACY, "accepted"), [])
        self.assertEqual(
            self.found(self.LEGACY, "proposed"),
            [
                "BODY-H3-REQUIRED",
                "BODY-HEADING-UNSUPPORTED",
                "BODY-HEADING-UNSUPPORTED",
            ],
        )

    def test_the_tree_applies_to_every_other_status(self) -> None:
        self.assertEqual(self.found(self.TREE, "proposed"), [])
        self.assertEqual(self.found(self.TREE, "rejected"), [])
        self.assertEqual(
            self.found(self.TREE, "accepted"),
            ["BODY-HEADING-REQUIRED", "BODY-HEADING-REQUIRED"],
        )

    def test_an_unknown_status_uses_the_tree(self) -> None:
        self.assertEqual(self.found(self.TREE, ""), [])

    def test_status_reaches_the_check_from_the_frontmatter(self) -> None:
        def document(status: str, body: str) -> str:
            return (
                "---\n"
                'title: "Decision title"\nversion: "1.0.0"\n'
                'type: "sdlc/architecture-decision"\n'
                f'status: "{status}"\nowner: "platform"\nupdated: "2026-11-12"\n'
                'layer: "architecture"\nartifact_id: "ADR-0099"\n---\n\n' + body
            )

        def body_rules(status: str, body: str) -> list[str]:
            with tempfile.TemporaryDirectory() as root:
                path = Path(root) / self.ADR_PATH
                path.parent.mkdir(parents=True)
                path.write_text(document(status, body), encoding="utf-8")
                found = MARKDOWN.validate_document(
                    Path(root), self.ADR_PATH, self.profile, "strict"
                )
            return sorted(i.rule_id for i in found if i.rule_id.startswith("BODY-"))

        self.assertEqual(body_rules("accepted", self.LEGACY), [])
        self.assertEqual(
            body_rules("proposed", self.LEGACY),
            [
                "BODY-H3-REQUIRED",
                "BODY-HEADING-UNSUPPORTED",
                "BODY-HEADING-UNSUPPORTED",
            ],
        )
        self.assertEqual(body_rules("proposed", self.TREE), [])


class CurrentRegistryUnchangedTests(unittest.TestCase):
    def test_no_current_profile_uses_the_tree(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        self.assertEqual(registry.common_forms, ())
        self.assertTrue(all(profile.form is None for profile in registry.profiles))


if __name__ == "__main__":
    unittest.main()
