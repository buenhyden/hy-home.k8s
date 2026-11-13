"""SPEC-0168: the common form model, its registry checks and heading-tree checks."""

from __future__ import annotations

import copy
import dataclasses
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
    "common/readme-collection-index": "stage-readme",
    "common/readme-implementation": "service-readme",
    "common/readme-runtime-governance": "service-readme",
}
GUIDE = ("operation/guide", "common/template-operation-guide")
ADR = ("sdlc/architecture-decision", "common/template-sdlc-architecture-decision")
GUIDE_TREE = (
    ("Purpose", ("Outcome", "Boundaries")),
    ("Prerequisites", ("Environment", "Permissions")),
    ("Procedure", ("Actions", "Exceptions")),
    ("Verification", ("Expected Result", "Troubleshooting")),
)
RUNBOOK = ("operation/runbook", "common/template-operation-runbook")
RUNBOOK_TREE = (
    ("Purpose", ("Trigger and Outcome", "Scope")),
    ("Preconditions", ("Authority and Access", "Safety Checks")),
    ("Steps", ("Actions", "Stop Conditions")),
    ("Validation", ("Service Checks", "Evidence")),
    ("Recovery", ("Rollback", "Escalation")),
)
RUNBOOK_EXTENSIONS = [
    {
        "id": "runbook-recovery-procedures",
        "kind": "local_h3",
        "condition": (
            "a runbook holds recovery or remediation procedures that are not an "
            "undo of its steps"
        ),
        "owner": "platform",
        "verification": "the form tree check",
        "review": "when the Runbook form version changes",
        "removal": (
            "when the common Runbook form gains an H3 for non-rollback recovery"
        ),
        "parent_id": "runbook-recovery",
        "title": "Recovery Procedures",
    },
    {
        "id": "runbook-lifecycle-traceability",
        "kind": "local_h3",
        "condition": (
            "a runbook in a status the body contract enforces (draft, in-review, "
            "active, deprecated) states its promoted owner or an N/A reason"
        ),
        "owner": "platform",
        "verification": "the body-contract check",
        "review": "when the Runbook form version changes",
        "removal": "when runbook lineage has another registered owner",
        "parent_id": "runbook-validation",
        "title": "Lifecycle Traceability",
    },
]
RUNBOOK_TABLE_KEYS = {
    "Triggers": (
        "runbook-steps-actions",
        ("Trigger", "Action", "Rollback"),
        0,
        "Trigger",
    ),
    "Lifecycle Traceability": (
        "runbook-lifecycle-traceability",
        ("Promoted owner", "Trigger or control", "Evidence or recovery owner"),
        1,
        "Promoted owner",
    ),
}
INCIDENT = ("operation/incident", "common/template-operation-incident")
INCIDENT_TREE = (
    ("Summary", ("Event", "Current Status")),
    ("Impact", ("Affected Users", "Severity and Duration")),
    ("Timeline", ("Events", "Decisions")),
    ("Resolution", ("Mitigation", "Recovery Verification")),
    ("Evidence", ("Evidence Sources", "Follow-up Owners")),
)
POSTMORTEM = ("operation/postmortem", "common/template-operation-postmortem")
POSTMORTEM_TREE = (
    ("Summary", ("Incident Reference", "Review Scope")),
    ("Root Cause", ("Causal Analysis", "Contributing Factors")),
    ("Impact", ("Observed Impact", "Detection and Response")),
    ("Corrective Actions", ("Actions", "Verification")),
    ("Evidence", ("Source Records", "Review Decision")),
)
ROOT_FORM = ("common/readme-repository", "common/template-readme-repository")
ROOT_FORM_TREE = (
    ("Purpose", ("Project Role", "Boundaries")),
    ("Repository Map", ("Directories", "Canonical Entry Points")),
    ("Getting Started", ("Prerequisites", "First Verified Path")),
    ("References", ("Current Documentation", "Support and Ownership")),
)
ROOT_TABLE_KEYS = {
    "Directory Index": (
        "root-readme-repository-map-directories",
        ("Path", "Purpose", "Owner"),
        0,
        "Path",
    ),
}
STAGE_FORM = (
    "common/readme-stage-index",
    "common/template-readme-stage-index",
    "common/readme-collection-index",
    "common/template-readme-collection-index",
)
STAGE_FORM_TREE = (
    ("Stage Responsibility", ("Purpose and Readers", "Inputs and Outputs")),
    ("Contents", ("Current Items", "Classification")),
    ("Workflow", ("Create and Review", "Transition and Exit")),
    ("Related Documents", ("Upstream and Downstream", "Policy and Templates")),
)
STAGE_TABLE_KEYS = {
    "Index": (
        "stage-readme-contents-current-items",
        ("Path", "Purpose", "Owner"),
        0,
        "Path",
    ),
}
SERVICE_FORM = (
    "common/readme-implementation",
    "common/template-readme-implementation",
    "common/readme-runtime-governance",
    "common/template-readme-runtime-governance",
)
SERVICE_FORM_TREE = (
    ("Purpose", ("Service Role", "Supported Environment")),
    ("Interfaces", ("Inputs and Outputs", "Security Boundary")),
    ("Development", ("Local Workflow", "Checks")),
    ("Operations", ("Runbook Links", "Observability and Recovery")),
)
SERVICE_TABLE_KEYS = {
    "Commands": (
        "service-readme-development-checks",
        ("Command", "Output"),
        0,
        "Command",
    ),
}
POLICY_GOVERNANCE = ("governance/rule", "common/template-governance-rule")
POLICY_OPERATIONS = ("operation/policy", "common/template-operation-policy")
POLICY_TREE = (
    ("Purpose", ("Objective", "Authority")),
    ("Scope", ("Applies To", "Exclusions")),
    ("Rules", ("Requirements", "Enforcement")),
    ("Exceptions", ("Exception Conditions", "Approval and Review")),
    ("Ownership", ("Responsibilities", "Change and Adoption")),
)
POLICY_EXTENSION = {
    "id": "policy-lifecycle-traceability",
    "kind": "local_h3",
    "condition": (
        "a policy in a status the body contract enforces (draft, in-review, "
        "active, deprecated) states its promoted owner or an N/A reason"
    ),
    "owner": "platform",
    "verification": "the body-contract check",
    "review": "when the Policy form version changes",
    "removal": "when policy lineage has another registered owner",
    "parent_id": "policy-ownership",
    "title": "Lifecycle Traceability",
}
POLICY_RULES_TABLE = (
    "policy-rules-requirements",
    ("Rule", "Condition", "Evidence"),
    0,
    "Rule",
)
POLICY_GOVERNANCE_TABLE_KEYS = {"Rules": POLICY_RULES_TABLE}
POLICY_OPERATIONS_TABLE_KEYS = {
    "Rules": POLICY_RULES_TABLE,
    "Lifecycle Traceability": (
        "policy-lifecycle-traceability",
        ("Promoted owner", "Control owner", "Enforcement surface"),
        1,
        "Promoted owner",
    ),
}
# The eight roles that carry a form; every other profile keeps its H2 lists.
FORM_PROFILES = (
    GUIDE
    + RUNBOOK
    + INCIDENT
    + POSTMORTEM
    + ROOT_FORM
    + STAGE_FORM
    + SERVICE_FORM
    + POLICY_GOVERNANCE
    + POLICY_OPERATIONS
)
FORM_TEMPLATES = (
    GUIDE[1],
    RUNBOOK[1],
    INCIDENT[1],
    POSTMORTEM[1],
    ROOT_FORM[1],
    STAGE_FORM[1],
    STAGE_FORM[3],
    SERVICE_FORM[1],
    SERVICE_FORM[3],
    POLICY_GOVERNANCE[1],
    POLICY_OPERATIONS[1],
)
EIGHT_FORMS = [
    "guide",
    "runbook",
    "incident",
    "postmortem",
    "root-readme",
    "stage-readme",
    "service-readme",
    "policy",
]
LIFECYCLE_CONDITION = (
    "a document in a status the body contract enforces states its follow-up "
    "Task or an N/A reason"
)
INCIDENT_EXTENSIONS = [
    {
        "id": "incident-lifecycle-traceability",
        "kind": "local_h3",
        "condition": LIFECYCLE_CONDITION,
        "owner": "platform",
        "verification": "the body-contract check",
        "review": "when the form version changes",
        "removal": "when incident lineage has another registered owner",
        "parent_id": "incident-evidence",
        "title": "Lifecycle Traceability",
    }
]
POSTMORTEM_EXTENSIONS = [
    {
        "id": "postmortem-lifecycle-traceability",
        "kind": "local_h3",
        "condition": LIFECYCLE_CONDITION,
        "owner": "platform",
        "verification": "the body-contract check",
        "review": "when the form version changes",
        "removal": "when incident lineage has another registered owner",
        "parent_id": "postmortem-corrective-actions",
        "title": "Lifecycle Traceability",
    },
    {
        "id": "postmortem-what-went-well",
        "kind": "local_h3",
        "condition": (
            "a postmortem records controls or response actions that reduced impact"
        ),
        "owner": "platform",
        "verification": "the form tree check",
        "review": "when the Postmortem form version changes",
        "removal": "when the common Postmortem form gains a What Went Well H3",
        "parent_id": "postmortem-impact",
        "title": "What Went Well",
    },
]
INCIDENT_TABLE_KEYS = {
    "Events": (
        "incident-timeline-events",
        ("Timestamp", "Event", "Actor"),
        0,
        "Timestamp",
    ),
    "Lifecycle Traceability": (
        "incident-lifecycle-traceability",
        ("Timeline or action", "Evidence", "Follow-up Task"),
        1,
        "Timeline or action",
    ),
}
POSTMORTEM_TABLE_KEYS = {
    "Actions": (
        "postmortem-corrective-actions-actions",
        ("Action", "Owner", "Verification"),
        0,
        "Action",
    ),
    "Lifecycle Traceability": (
        "postmortem-lifecycle-traceability",
        (
            "Root cause or action",
            "Owner and due state",
            "Follow-up Task",
            "Feedback target",
        ),
        1,
        "Root cause or action",
    ),
}
GUIDE_EXTENSION = {
    "id": "guide-lifecycle-traceability",
    "kind": "local_h3",
    "condition": (
        "a guide in a status the body contract enforces (draft, in-review, "
        "active, deprecated) states its promoted owner or an N/A reason"
    ),
    "owner": "platform",
    "verification": "the body-contract check",
    "review": "when the Guide form version changes",
    "removal": "when guide lineage has another registered owner",
    "parent_id": "guide-verification",
    "title": "Lifecycle Traceability",
}
GUIDE_TABLE_KEYS = {
    "Steps": ("guide-procedure-actions", ("Step", "Action", "Check"), 0, "Step"),
    "Lifecycle Traceability": (
        "guide-lifecycle-traceability",
        ("Promoted owner", "Audience outcome", "Operating surface"),
        1,
        "Promoted owner",
    ),
}


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
        "tables": [],
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
            if profile["mode"] == "template":
                profile.pop("template_definition", None)
                if definitions:
                    profile["template_definition"] = definition()
    forms = candidate["common_forms"]["forms"]
    replacement = form(role, sections, extensions)
    # Keep the registry order: swap the role's form in place, else append it.
    if any(item["form_id"] == role for item in forms):
        candidate["common_forms"]["forms"] = [
            replacement if item["form_id"] == role else item for item in forms
        ]
    else:
        forms.append(replacement)
    return candidate


def rules_of(raw: dict) -> set[str]:
    try:
        CONTRACTS.validate_registry(ROOT, raw)
    except CONTRACTS.DocumentContractError as error:
        return {item.rule_id for item in error.diagnostics}
    return set()


class RepositoryRegistryTests(unittest.TestCase):
    def test_repository_registry_binds_clear_roles_and_carries_exactly_the_eight_forms(
        self,
    ) -> None:
        raw = load_raw()
        self.assertEqual(raw["schema_version"], 10)
        common = raw["common_forms"]
        self.assertEqual(common["contract_id"], "COMMON-DOC-FORM-1")
        self.assertEqual(common["version"], "1.0.0")
        self.assertEqual(
            [(item["form_id"], item["title"]) for item in common["forms"]],
            [
                ("guide", "Guide"),
                ("runbook", "Runbook"),
                ("incident", "Incident"),
                ("postmortem", "Postmortem"),
                ("root-readme", "Root README"),
                ("stage-readme", "Stage README"),
                ("service-readme", "Service README"),
                ("policy", "Policy"),
            ],
        )
        by_id = {profile["id"]: profile for profile in raw["profiles"]}
        for form_id, tree, extensions, tables, profiles, body_section in (
            (
                "guide",
                GUIDE_TREE,
                [GUIDE_EXTENSION],
                GUIDE_TABLE_KEYS,
                GUIDE,
                "Verification",
            ),
            (
                "runbook",
                RUNBOOK_TREE,
                RUNBOOK_EXTENSIONS,
                RUNBOOK_TABLE_KEYS,
                RUNBOOK,
                "Validation",
            ),
            (
                "incident",
                INCIDENT_TREE,
                INCIDENT_EXTENSIONS,
                INCIDENT_TABLE_KEYS,
                INCIDENT,
                "Evidence",
            ),
            (
                "postmortem",
                POSTMORTEM_TREE,
                POSTMORTEM_EXTENSIONS,
                POSTMORTEM_TABLE_KEYS,
                POSTMORTEM,
                "Corrective Actions",
            ),
            (
                "root-readme",
                ROOT_FORM_TREE,
                [],
                ROOT_TABLE_KEYS,
                ROOT_FORM,
                None,
            ),
            (
                "stage-readme",
                STAGE_FORM_TREE,
                [],
                STAGE_TABLE_KEYS,
                STAGE_FORM,
                None,
            ),
            (
                "service-readme",
                SERVICE_FORM_TREE,
                [],
                SERVICE_TABLE_KEYS,
                SERVICE_FORM,
                None,
            ),
            (
                "policy",
                POLICY_TREE,
                [POLICY_EXTENSION],
                POLICY_GOVERNANCE_TABLE_KEYS,
                POLICY_GOVERNANCE,
                None,
            ),
            (
                "policy",
                POLICY_TREE,
                [POLICY_EXTENSION],
                POLICY_OPERATIONS_TABLE_KEYS,
                POLICY_OPERATIONS,
                "Ownership",
            ),
        ):
            loaded = next(f for f in common["forms"] if f["form_id"] == form_id)
            self.assertEqual(loaded["h1"], "{{document_title}}")
            self.assertEqual(
                [
                    (
                        item["section_id"],
                        item["title"],
                        item["order"],
                        [
                            (child["section_id"], child["title"], child["order"])
                            for child in item["children"]
                        ],
                    )
                    for item in loaded["sections"]
                ],
                [
                    (
                        f"{form_id}-{title.lower().replace(' ', '-')}",
                        title,
                        position,
                        [
                            (
                                f"{form_id}-{title.lower().replace(' ', '-')}-"
                                f"{child.lower().replace(' ', '-')}",
                                child,
                                n,
                            )
                            for n, child in enumerate(children, start=1)
                        ],
                    )
                    for position, (title, children) in enumerate(tree, start=1)
                ],
            )
            every = [
                node
                for item in loaded["sections"]
                for node in (item, *item["children"])
            ]
            conditional = {
                node["section_id"]
                for node in every
                if node["requiredness"] != "required"
            }
            self.assertEqual(
                conditional,
                {"runbook-recovery-rollback"} if form_id == "runbook" else set(),
            )
            self.assertEqual({node.get("link_only") for node in every}, {False})
            self.assertEqual(loaded["extensions"], extensions)
            for profile_id in profiles:
                profile = by_id[profile_id]
                self.assertEqual(
                    profile["sections"]["required"]
                    + profile["sections"]["optional"]
                    + profile["sections"]["forbidden"],
                    [],
                )
                contract = profile["relationships"]["body_contract"]
                self.assertEqual(contract and contract["section"], body_section)
                self.assertNotIn("substantive_body", profile["sections"])
                self.assertNotIn("ordered", profile["sections"])
            for twin in (p for p in profiles if by_id[p]["mode"] == "template"):
                self.assertEqual(
                    {
                        table["name"]: (
                            table["section"],
                            tuple(column["key"] for column in table["columns"]),
                            table["minimum_rows"],
                            table["row_identity"],
                        )
                        for table in by_id[twin]["template_definition"]["tables"]
                    },
                    tables,
                )
                for table in by_id[twin]["template_definition"]["tables"]:
                    for column in table["columns"]:
                        self.assertTrue(column["meaning"])
                        self.assertEqual(column["data_type"], "string")
                        self.assertIs(
                            column["required"],
                            not (
                                form_id in ("root-readme", "stage-readme")
                                and column["key"] == "Owner"
                            ),
                        )
        for profile_id, profile in by_id.items():
            sources = profile["relationships"]["source_profile_ids"]
            expected = ROLE_BINDINGS.get(
                profile_id, ROLE_BINDINGS.get(sources[0]) if sources else None
            )
            with self.subTest(profile=profile_id):
                self.assertEqual(profile.get("document_role"), expected)
                if profile_id in FORM_TEMPLATES:
                    self.assertIn("template_definition", profile)
                else:
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

    def test_repository_registry_loads_with_exactly_the_eight_forms(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        self.assertEqual(
            [item.form_id for item in registry.common_forms],
            EIGHT_FORMS,
        )
        forms = {item.form_id: item for item in registry.common_forms}
        tables = {
            "guide": ["Steps", "Lifecycle Traceability"],
            "runbook": ["Triggers", "Lifecycle Traceability"],
            "incident": ["Events", "Lifecycle Traceability"],
            "postmortem": ["Actions", "Lifecycle Traceability"],
            "root-readme": ["Directory Index"],
            "stage-readme": ["Index"],
            "service-readme": ["Commands"],
            "policy": ["Rules", "Lifecycle Traceability"],
        }
        governance_tables = ["Rules"]
        for profile in registry.profiles:
            with self.subTest(profile=profile.profile_id):
                role = next(
                    (
                        form_id
                        for form_id, ids in (
                            ("guide", GUIDE),
                            ("runbook", RUNBOOK),
                            ("incident", INCIDENT),
                            ("postmortem", POSTMORTEM),
                            ("root-readme", ROOT_FORM),
                            ("stage-readme", STAGE_FORM),
                            ("service-readme", SERVICE_FORM),
                            ("policy", POLICY_GOVERNANCE + POLICY_OPERATIONS),
                        )
                        if profile.profile_id in ids
                    ),
                    None,
                )
                if role:
                    self.assertIs(profile.form, forms[role])
                    self.assertEqual(
                        [t.name for t in profile.tables],
                        governance_tables
                        if profile.profile_id in POLICY_GOVERNANCE
                        else tables[role],
                    )
                else:
                    self.assertIsNone(profile.form)
                    self.assertEqual(profile.tables, ())
                if profile.profile_id in FORM_TEMPLATES:
                    self.assertIsNotNone(profile.template_definition)
                else:
                    self.assertIsNone(profile.template_definition)
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
        self.assertEqual(
            [item.form_id for item in registry.common_forms],
            EIGHT_FORMS,
        )
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
        self.assertIsNone(by_id["governance/role"].form)

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
            if profile["id"] not in FORM_PROFILES:
                profile.pop("document_role", None)
        self.assertEqual(rules_of(raw), set())

    def test_template_twin_must_share_its_sources_role(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        REGISTRY_CHECK._assert_template_source_parity(registry)
        raw = self.candidate()
        profile_of(raw, GUIDE[1])["document_role"] = "runbook"
        loaded = CONTRACTS.validate_registry(ROOT, raw)
        with self.assertRaisesRegex(AssertionError, "template/source contract differs"):
            REGISTRY_CHECK._assert_template_source_parity(loaded)
        raw = self.candidate()
        twin = profile_of(raw, GUIDE[1])
        twin.pop("document_role")
        twin.pop("template_definition")
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
        for key in (
            "purpose",
            "consumer_paths",
            "migration",
            "validation",
            "tables",
        ):
            incomplete = definition()
            del incomplete[key]
            with self.subTest(missing=key):
                self.assertIn("REGISTRY_SCHEMA", rules_of(self.candidate(incomplete)))
        self.assertIn(
            "REGISTRY_SCHEMA",
            rules_of(self.candidate(definition(role="Release"))),
        )


def profile_of(raw: dict, profile_id: str) -> dict:
    return next(item for item in raw["profiles"] if item["id"] == profile_id)


def guide_tables(raw: dict) -> list[dict]:
    return profile_of(raw, GUIDE[1])["template_definition"]["tables"]


class GuideFormRegistryTests(unittest.TestCase):
    """SPEC-0169 VAL-GUIDEFORM-001: the Guide form, its tables and their checks."""

    def test_the_repository_registry_is_valid(self) -> None:
        self.assertEqual(rules_of(load_raw()), set())

    def test_loaded_guide_heading_lists_equal_the_form_h2_titles(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        titles = tuple(title for title, _ in GUIDE_TREE)
        self.assertEqual(
            tuple(item.title for item in registry.common_forms[0].sections), titles
        )
        by_id = {profile.profile_id: profile for profile in registry.profiles}
        for profile_id in GUIDE:
            with self.subTest(profile=profile_id):
                headings = by_id[profile_id].headings
                self.assertEqual(headings.required, titles)
                self.assertEqual(headings.allowed, titles)
                self.assertFalse(headings.substantive_body)
                self.assertFalse(headings.ordered)

    def test_derived_required_list_skips_a_conditional_h2(self) -> None:
        sections = guide_sections()
        sections[1]["requiredness"] = "conditional"
        sections[1]["condition"] = "the guide has steps"
        profile = typed_profiles(with_form(load_raw(), "guide", GUIDE, sections))[
            GUIDE[0]
        ]
        self.assertEqual(profile.headings.required, ("Overview", "Related Documents"))
        self.assertEqual(
            profile.headings.allowed, ("Overview", "Procedure", "Related Documents")
        )

    def test_the_loader_types_the_tables_and_copies_them_to_the_source(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        by_id = {profile.profile_id: profile for profile in registry.profiles}
        twin, source = by_id[GUIDE[1]], by_id[GUIDE[0]]
        self.assertEqual(source.tables, twin.tables)
        steps, lifecycle = twin.tables
        self.assertEqual(
            (steps.name, steps.section, steps.minimum_rows, steps.row_identity),
            ("Steps", "guide-procedure-actions", 0, "Step"),
        )
        self.assertEqual(
            [column.key for column in lifecycle.columns],
            list(GUIDE_TABLE_KEYS["Lifecycle Traceability"][1]),
        )
        self.assertTrue(all(column.required for column in steps.columns))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            steps.name = "Other"  # type: ignore[misc]

    def test_body_section_must_be_a_required_h2_of_the_form(self) -> None:
        for bad in ("Related Documents", "Lifecycle Traceability", "Actions"):
            for profile_id in GUIDE:
                raw = load_raw()
                profile_of(raw, profile_id)["relationships"]["body_contract"][
                    "section"
                ] = bad
                with self.subTest(section=bad, profile=profile_id):
                    self.assertIn("REGISTRY_BODY_SECTION", rules_of(raw))

    def test_a_guide_profile_with_h2_lists_is_refused(self) -> None:
        for key in ("required", "optional", "forbidden"):
            for profile_id in GUIDE:
                raw = load_raw()
                profile_of(raw, profile_id)["sections"][key] = ["Verification"]
                with self.subTest(list=key, profile=profile_id):
                    self.assertIn("REGISTRY_FORM_LEGACY_LISTS", rules_of(raw))

    def test_a_table_section_must_be_a_form_section_or_extension(self) -> None:
        raw = load_raw()
        guide_tables(raw)[0]["section"] = "guide-missing"
        self.assertIn("REGISTRY_TABLE_SECTION", rules_of(raw))
        raw = load_raw()
        guide_tables(raw)[0]["section"] = "Actions"
        self.assertIn("REGISTRY_TABLE_SECTION", rules_of(raw))
        for accepted in ("guide-purpose", "guide-verification-troubleshooting"):
            raw = load_raw()
            guide_tables(raw)[0]["section"] = accepted
            with self.subTest(section=accepted):
                self.assertEqual(rules_of(raw), set())

    def test_a_table_needs_a_form_to_name_a_section(self) -> None:
        raw = load_raw()
        raw["common_forms"]["forms"] = []
        for profile_id in GUIDE:
            profile_of(raw, profile_id)["sections"]["required"] = ["Verification"]
        self.assertIn("REGISTRY_TABLE_SECTION", rules_of(raw))

    def test_column_keys_must_be_unique_and_name_the_row_identity(self) -> None:
        raw = load_raw()
        columns = guide_tables(raw)[0]["columns"]
        columns[2]["key"] = "Action"
        self.assertIn("REGISTRY_TABLE_COLUMNS", rules_of(raw))
        raw = load_raw()
        guide_tables(raw)[0]["row_identity"] = "Number"
        self.assertIn("REGISTRY_TABLE_COLUMNS", rules_of(raw))

    def test_the_body_contract_table_keeps_the_body_contract_columns(self) -> None:
        for mutate in (
            lambda keys: keys.reverse(),
            lambda keys: keys.__setitem__(2, "Surface"),
            lambda keys: keys.pop(),
            lambda keys: keys.append("Notes"),
        ):
            raw = load_raw()
            table = guide_tables(raw)[1]
            keys = [column["key"] for column in table["columns"]]
            mutate(keys)
            table["columns"] = [
                {"key": key, "meaning": "m", "data_type": "string", "required": True}
                for key in keys
            ]
            with self.subTest(keys=keys):
                self.assertIn("REGISTRY_TABLE_BODY_CONTRACT", rules_of(raw))

    def test_a_definition_without_tables_fails_the_schema(self) -> None:
        raw = load_raw()
        del profile_of(raw, GUIDE[1])["template_definition"]["tables"]
        self.assertIn("REGISTRY_SCHEMA", rules_of(raw))

    def test_the_table_schema_is_closed(self) -> None:
        def broken(change) -> dict:
            raw = load_raw()
            change(guide_tables(raw)[0])
            return raw

        for label, change in (
            ("extra table key", lambda t: t.update(extra=1)),
            ("extra column key", lambda t: t["columns"][0].update(extra=1)),
            ("column without required", lambda t: t["columns"][0].pop("required")),
            ("column without meaning", lambda t: t["columns"][0].pop("meaning")),
            ("no columns", lambda t: t.update(columns=[])),
            ("negative minimum", lambda t: t.update(minimum_rows=-1)),
            ("no row identity", lambda t: t.pop("row_identity")),
            ("no minimum rows", lambda t: t.pop("minimum_rows")),
        ):
            with self.subTest(label):
                self.assertIn("REGISTRY_SCHEMA", rules_of(broken(change)))


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


STEPS = "| Step | Action | Check |\n| --- | --- | --- |\n| 1 | Run | Read |"
OTHER = "| Name | Value |\n| --- | --- |\n| a | b |"
LIFECYCLE = (
    "| Promoted owner | Audience outcome | Operating surface |\n"
    "| --- | --- | --- |\n| N/A | Readers | Surface |"
)


def guide_body(actions: str, verification: str = "") -> str:
    return md(
        "# Guide",
        "## Procedure",
        "### Actions",
        actions,
        "### Exceptions",
        "None.",
        "## Verification",
        verification or "### Expected Result\n\nPass.",
    )


class TableCheckTests(unittest.TestCase):
    """SPEC-0169 VAL-GUIDEFORM-002: the document table check in isolation."""

    @classmethod
    def setUpClass(cls) -> None:
        raw = load_raw()
        cls.profile = typed_profiles(raw)[GUIDE[0]]
        guide_tables(raw)[0]["minimum_rows"] = 2
        profiles = typed_profiles(raw)
        cls.strict = profiles[GUIDE[0]]
        cls.template = profiles[GUIDE[1]]

    def found(self, body: str, profile=None) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._table_diagnostics(
                GUIDE_PATH, profile or self.profile, body
            )
        )

    def test_a_matching_table_passes(self) -> None:
        self.assertEqual(self.found(guide_body(STEPS)), [])

    def test_a_missing_optional_table_or_section_passes(self) -> None:
        self.assertEqual(self.found(guide_body("Run the command.")), [])
        self.assertEqual(self.found(md("# Guide", "## Procedure")), [])
        self.assertEqual(self.found(md("# Guide", "## Purpose")), [])

    def test_other_tables_in_the_section_are_ignored(self) -> None:
        self.assertEqual(self.found(guide_body(OTHER + "\n\n" + STEPS)), [])
        self.assertEqual(self.found(guide_body(OTHER)), [])
        # An ignored table never counts towards the minimum.
        self.assertEqual(
            self.found(guide_body(OTHER), self.strict), ["BODY-TABLE-ROWS"]
        )

    def test_a_reordered_missing_or_extra_column_fails(self) -> None:
        for header in (
            "| Step | Check | Action |",
            "| Step | Action |",
            "| Step | Action | Check | Note |",
            "| Step | Action | Check | Check |",
        ):
            cells = header.count("|") - 1
            body = f"{header}\n" + "| --- " * cells + "|\n" + "| 1 " * cells + "|"
            with self.subTest(header=header):
                self.assertEqual(self.found(guide_body(body)), ["BODY-TABLE-COLUMNS"])

    def test_every_identified_table_is_checked(self) -> None:
        wrong = "| Step | Action |\n| --- | --- |\n| 1 | Run |"
        body = STEPS + "\n\n" + wrong
        self.assertEqual(self.found(guide_body(body)), ["BODY-TABLE-COLUMNS"])

    def test_the_minimum_rows_count_every_identified_table_in_the_section(
        self,
    ) -> None:
        header_only = "| Step | Action | Check |\n| --- | --- | --- |"
        self.assertEqual(
            self.found(guide_body(header_only), self.strict), ["BODY-TABLE-ROWS"]
        )
        self.assertEqual(
            self.found(guide_body(STEPS), self.strict), ["BODY-TABLE-ROWS"]
        )
        self.assertEqual(
            self.found(guide_body(STEPS + "\n| 2 | Run | Read |"), self.strict),
            [],
        )
        split = guide_body(STEPS + "\n\n#### Detail\n\n" + STEPS)
        self.assertEqual(self.found(split, self.strict), [])

    def test_a_table_in_another_section_is_not_looked_at(self) -> None:
        body = md(
            "# Guide",
            "## Procedure",
            "### Actions",
            "Run it.",
            "### Exceptions",
            "| Step | Action |\n| --- | --- |\n| 1 | Run |",
        )
        self.assertEqual(self.found(body), [])
        self.assertEqual(self.found(body, self.strict), ["BODY-TABLE-ROWS"])

    def test_a_non_unique_section_heading_is_left_to_the_tree_check(self) -> None:
        body = guide_body(STEPS) + "\n### Actions\n\n" + OTHER + "\n"
        self.assertEqual(self.found(body, self.strict), [])

    def test_the_body_contract_table_is_not_checked_twice(self) -> None:
        wrong = LIFECYCLE.replace("Operating surface", "Surface")
        body = guide_body(STEPS, "### Lifecycle Traceability\n\n" + wrong)
        self.assertEqual(self.found(body), [])
        self.assertEqual(
            sorted(
                item.rule_id
                for item in MARKDOWN._body_contract_diagnostics(
                    GUIDE_PATH, self.profile, body, "active", "registry"
                )
            ),
            ["BODY-CONTRACT-COLUMNS"],
        )

    def test_a_profile_without_tables_is_not_checked(self) -> None:
        role = typed_profiles(load_raw())["governance/role"]
        self.assertEqual(role.tables, ())
        self.assertEqual(self.found(guide_body(STEPS), role), [])

    def test_the_check_runs_for_authored_documents_only(self) -> None:
        wrong = "| Step | Action |\n| --- | --- |\n| 1 | Run |"
        text = (
            "---\n"
            'title: "Guide"\nversion: "1.0.0"\ntype: "operation/guide"\n'
            'status: "active"\nowner: "platform"\nupdated: "2026-11-12"\n'
            'layer: "operations"\nartifact_id: "GDE-0001"\n---\n\n' + guide_body(wrong)
        )

        def rules(profile) -> list[str]:
            return [
                item.rule_id
                for item in MARKDOWN.validate_document_text(
                    text, GUIDE_PATH, profile, "strict"
                )
                if item.rule_id.startswith("BODY-TABLE-")
            ]

        self.assertEqual(rules(self.profile), ["BODY-TABLE-COLUMNS"])
        self.assertEqual(rules(self.template), [])
        self.assertEqual(rules(self.strict), ["BODY-TABLE-COLUMNS", "BODY-TABLE-ROWS"])


class OptionalTrailingColumnTests(unittest.TestCase):
    """SPEC-0172: optional columns may only trail the required ones."""

    @classmethod
    def raw_with_note(cls, required: bool = False) -> dict:
        raw = load_raw()
        columns = guide_tables(raw)[0]["columns"]
        columns.append(
            {"key": "Note", "meaning": "m", "data_type": "string", "required": required}
        )
        return raw

    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = typed_profiles(cls.raw_with_note())[GUIDE[0]]

    def found(self, header: tuple[str, ...]) -> list[str]:
        cells = len(header)
        body = (
            "| "
            + " | ".join(header)
            + " |\n"
            + "| --- " * cells
            + "|\n"
            + "| x " * cells
            + "|"
        )
        return sorted(
            item.rule_id
            for item in MARKDOWN._table_diagnostics(
                GUIDE_PATH, self.profile, guide_body(body)
            )
        )

    def test_an_omitted_optional_trailing_column_passes(self) -> None:
        self.assertEqual(self.found(("Step", "Action", "Check")), [])

    def test_a_present_optional_trailing_column_passes(self) -> None:
        self.assertEqual(self.found(("Step", "Action", "Check", "Note")), [])

    def test_a_missing_required_column_fails(self) -> None:
        for header in (("Step", "Action"), ("Step",)):
            with self.subTest(header=header):
                self.assertEqual(self.found(header), ["BODY-TABLE-COLUMNS"])

    def test_a_reordered_or_extra_column_still_fails(self) -> None:
        for header in (
            ("Step", "Action", "Note"),
            ("Step", "Action", "Note", "Check"),
            ("Step", "Action", "Check", "Note", "Extra"),
        ):
            with self.subTest(header=header):
                self.assertEqual(self.found(header), ["BODY-TABLE-COLUMNS"])

    def test_a_required_column_after_an_optional_one_is_refused(self) -> None:
        self.assertEqual(rules_of(self.raw_with_note()), set())
        raw = self.raw_with_note()
        columns = guide_tables(raw)[0]["columns"]
        columns[1]["required"] = False
        self.assertIn("REGISTRY_TABLE_COLUMNS", rules_of(raw))
        raw = self.raw_with_note(required=True)
        guide_tables(raw)[0]["columns"][2]["required"] = False
        self.assertIn("REGISTRY_TABLE_COLUMNS", rules_of(raw))


class RootReadmeFormTests(unittest.TestCase):
    """SPEC-0172: the Root README form and its table in the repository registry."""

    BODY = md(
        "# Project",
        *(
            f"{'## ' + title}\n\n" + "\n\n".join(f"### {h3}\n\nText." for h3 in h3s)
            for title, h3s in ROOT_FORM_TREE
        ),
    )

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = CONTRACTS.load_registry(ROOT)
        cls.profile = {p.profile_id: p for p in cls.registry.profiles}[ROOT_FORM[0]]

    def tree(self, text: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._body_diagnostics(
                PurePosixPath("README.md"), self.profile, text
            )
        )

    def test_the_heading_lists_equal_the_form_h2_titles(self) -> None:
        titles = tuple(title for title, _ in ROOT_FORM_TREE)
        self.assertEqual(self.profile.headings.required, titles)
        self.assertEqual(self.profile.headings.allowed, titles)

    def test_a_complete_body_passes_the_tree_and_an_h4_is_allowed(self) -> None:
        self.assertEqual(self.tree(self.BODY), [])
        deeper = self.BODY.replace(
            "### Boundaries\n\nText.",
            "### Boundaries\n\nText.\n\n#### In Scope\n\nText.",
        )
        self.assertEqual(self.tree(deeper), [])

    def test_a_missing_h3_or_an_old_h2_fails_the_tree(self) -> None:
        self.assertIn(
            "BODY-H3-REQUIRED",
            self.tree(self.BODY.replace("### Directories", "#### Directories")),
        )
        self.assertNotEqual(self.tree(self.BODY + "\n## Structure\n\nText.\n"), [])

    def test_the_navigation_section_is_the_directories_h3(self) -> None:
        navigation = self.registry.readme_navigation.profiles[ROOT_FORM[0]]
        self.assertEqual(
            (navigation.section, navigation.complete), ("Directories", False)
        )


class StageReadmeFormTests(unittest.TestCase):
    """SPEC-0173: the Stage README form, its Index table and its navigation."""

    HOME = "### Current Items\n\nText."
    HEADER = ("Path", "Purpose", "Owner")
    BODY = md(
        "# Stage",
        *(
            f"{'## ' + title}\n\n" + "\n\n".join(f"### {h3}\n\nText." for h3 in h3s)
            for title, h3s in STAGE_FORM_TREE
        ),
    )

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = CONTRACTS.load_registry(ROOT)
        cls.by_id = {p.profile_id: p for p in cls.registry.profiles}

    def tree(self, profile_id: str, text: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._body_diagnostics(
                PurePosixPath("docs/README.md"), self.by_id[profile_id], text
            )
        )

    def tables(self, profile_id: str, text: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._table_diagnostics(
                PurePosixPath("docs/README.md"), self.by_id[profile_id], text
            )
        )

    def with_table(self, *lines: str, home: str | None = None) -> str:
        home = home or self.HOME
        return self.BODY.replace(home, home + "\n\n" + "\n".join(lines), 1)

    def test_the_heading_lists_equal_the_form_h2_titles(self) -> None:
        titles = tuple(title for title, _ in STAGE_FORM_TREE)
        for profile_id in STAGE_FORM:
            with self.subTest(profile=profile_id):
                headings = self.by_id[profile_id].headings
                self.assertEqual(headings.required, titles)
                self.assertEqual(headings.allowed, titles)

    def test_a_complete_body_passes_and_an_old_h2_fails_the_tree(self) -> None:
        for profile_id in STAGE_FORM[::2]:
            with self.subTest(profile=profile_id):
                self.assertEqual(self.tree(profile_id, self.BODY), [])
                deeper = self.BODY.replace(
                    "### Classification\n\nText.",
                    "### Classification\n\nText.\n\n#### Matrix\n\nText.",
                )
                self.assertEqual(self.tree(profile_id, deeper), [])
                self.assertNotEqual(
                    self.tree(profile_id, self.BODY + "\n## Structure\n\nText.\n"), []
                )
                self.assertIn(
                    "BODY-H3-REQUIRED",
                    self.tree(
                        profile_id,
                        self.BODY.replace("### Current Items", "#### Current Items"),
                    ),
                )

    def test_the_index_table_accepts_its_registered_columns(self) -> None:
        for profile_id in STAGE_FORM[::2]:
            for header in (self.HEADER[:2], self.HEADER):
                row = tuple("x" for _ in header)
                text = self.with_table(
                    "| " + " | ".join(header) + " |",
                    "| " + " | ".join("---" for _ in header) + " |",
                    "| " + " | ".join(row) + " |",
                )
                with self.subTest(profile=profile_id, header=header):
                    self.assertEqual(self.tables(profile_id, text), [])
            header_only = self.with_table("| Path | Purpose |", "| --- | --- |")
            with self.subTest(profile=profile_id, header="header only"):
                self.assertEqual(self.tables(profile_id, header_only), [])

    def test_a_reordered_missing_or_extra_column_fails(self) -> None:
        for profile_id in STAGE_FORM[::2]:
            for header in (
                ("Path",),
                ("Path", "Owner", "Purpose"),
                (*self.HEADER, "Note"),
            ):
                text = self.with_table(
                    "| " + " | ".join(header) + " |",
                    "| " + " | ".join("---" for _ in header) + " |",
                    "| " + " | ".join("x" for _ in header) + " |",
                )
                with self.subTest(profile=profile_id, header=header):
                    self.assertEqual(
                        self.tables(profile_id, text), ["BODY-TABLE-COLUMNS"]
                    )

    def test_the_table_is_not_looked_at_outside_its_section(self) -> None:
        wrong = self.with_table(
            "| Path |", "| --- |", "| a |", home="### Classification"
        )
        for profile_id in STAGE_FORM[::2]:
            with self.subTest(profile=profile_id):
                self.assertEqual(self.tables(profile_id, wrong), [])

    def test_the_navigation_section_is_the_current_items_h3(self) -> None:
        for profile_id in STAGE_FORM[::2]:
            navigation = self.registry.readme_navigation.profiles[profile_id]
            with self.subTest(profile=profile_id):
                self.assertEqual(
                    (navigation.section, navigation.complete), ("Current Items", True)
                )


class ServiceReadmeFormTests(unittest.TestCase):
    """SPEC-0174: the Service README form, its Commands table and navigation."""

    HOME = "### Checks\n\nText."
    HEADER = ("Command", "Output")
    BODY = md(
        "# Service",
        *(
            f"{'## ' + title}\n\n" + "\n\n".join(f"### {h3}\n\nText." for h3 in h3s)
            for title, h3s in SERVICE_FORM_TREE
        ),
    )

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = CONTRACTS.load_registry(ROOT)
        cls.by_id = {p.profile_id: p for p in cls.registry.profiles}

    def tree(self, profile_id: str, text: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._body_diagnostics(
                PurePosixPath("gitops/README.md"), self.by_id[profile_id], text
            )
        )

    def tables(self, profile_id: str, text: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._table_diagnostics(
                PurePosixPath("gitops/README.md"), self.by_id[profile_id], text
            )
        )

    def with_table(self, *lines: str, home: str | None = None) -> str:
        home = home or self.HOME
        return self.BODY.replace(home, home + "\n\n" + "\n".join(lines), 1)

    def test_the_heading_lists_equal_the_form_h2_titles(self) -> None:
        titles = tuple(title for title, _ in SERVICE_FORM_TREE)
        for profile_id in SERVICE_FORM:
            with self.subTest(profile=profile_id):
                headings = self.by_id[profile_id].headings
                self.assertEqual(headings.required, titles)
                self.assertEqual(headings.allowed, titles)

    def test_a_complete_body_passes_and_an_old_h2_fails_the_tree(self) -> None:
        for profile_id in SERVICE_FORM[::2]:
            with self.subTest(profile=profile_id):
                self.assertEqual(self.tree(profile_id, self.BODY), [])
                deeper = self.BODY.replace(
                    "### Service Role\n\nText.",
                    "### Service Role\n\nText.\n\n#### Matrix\n\nText.",
                )
                self.assertEqual(self.tree(profile_id, deeper), [])
                self.assertNotEqual(
                    self.tree(profile_id, self.BODY + "\n## Structure\n\nText.\n"), []
                )
                self.assertIn(
                    "BODY-H3-REQUIRED",
                    self.tree(
                        profile_id,
                        self.BODY.replace("### Checks", "#### Checks"),
                    ),
                )

    def test_the_commands_table_accepts_its_registered_columns(self) -> None:
        for profile_id in SERVICE_FORM[::2]:
            text = self.with_table(
                "| Command | Output |", "| --- | --- |", "| make test | ok |"
            )
            with self.subTest(profile=profile_id):
                self.assertEqual(self.tables(profile_id, text), [])
            header_only = self.with_table("| Command | Output |", "| --- | --- |")
            with self.subTest(profile=profile_id, header="header only"):
                self.assertEqual(self.tables(profile_id, header_only), [])

    def test_a_reordered_missing_or_extra_column_fails(self) -> None:
        for profile_id in SERVICE_FORM[::2]:
            for header in (
                ("Command",),
                ("Command", "Note", "Output"),
                (*self.HEADER, "Note"),
            ):
                text = self.with_table(
                    "| " + " | ".join(header) + " |",
                    "| " + " | ".join("---" for _ in header) + " |",
                    "| " + " | ".join("x" for _ in header) + " |",
                )
                with self.subTest(profile=profile_id, header=header):
                    self.assertEqual(
                        self.tables(profile_id, text), ["BODY-TABLE-COLUMNS"]
                    )

    def test_the_table_is_not_looked_at_outside_its_section(self) -> None:
        wrong = self.with_table(
            "| Command |", "| --- |", "| a |", home="### Local Workflow"
        )
        for profile_id in SERVICE_FORM[::2]:
            with self.subTest(profile=profile_id):
                self.assertEqual(self.tables(profile_id, wrong), [])

    def test_the_navigation_section_is_the_service_role_h3(self) -> None:
        navigation = self.registry.readme_navigation.profiles[SERVICE_FORM[0]]
        self.assertEqual(
            (navigation.section, navigation.complete), ("Service Role", False)
        )
        self.assertNotIn(SERVICE_FORM[2], self.registry.readme_navigation.profiles)


class TableIteratorTests(unittest.TestCase):
    def test_every_table_is_yielded_in_order(self) -> None:
        text = md(
            "| A | B |\n| --- | --- |\n| 1 | 2 |\n| 3 | 4 |",
            "text",
            "```\n| X | Y |\n| - | - |\n```",
            "| C |\n| :---: |",
        )
        self.assertEqual(
            list(MARKDOWN._visible_tables(text)),
            [(["A", "B"], [["1", "2"], ["3", "4"]]), (["C"], [])],
        )
        self.assertEqual(
            MARKDOWN._first_visible_table(text),
            (["A", "B"], [["1", "2"], ["3", "4"]]),
        )
        self.assertIsNone(MARKDOWN._first_visible_table("no table here"))


RUNBOOK_PATH = PurePosixPath("docs/05.operations/runbooks/0001-temporary-runbook.md")
TRIGGERS = (
    "| Trigger | Action | Rollback |\n| --- | --- | --- |\n| Alert | Restart | Undo |"
)
RUNBOOK_BODY = md(
    "# Runbook title",
    "## Purpose",
    "### Trigger and Outcome\n\nAn alert starts it.",
    "### Scope\n\nOne service.",
    "## Preconditions",
    "### Authority and Access\n\nOwner approval.",
    "### Safety Checks\n\nBackup exists.",
    "## Steps",
    "### Actions\n\nRun it.",
    "### Stop Conditions\n\nStop on error.",
    "## Validation",
    "### Service Checks\n\nRead the status.",
    "### Evidence\n\nNone recorded.",
    "## Recovery",
    "### Escalation\n\nCall the owner.",
)


class RunbookFormTests(unittest.TestCase):
    """SPEC-0170 VAL-RUNBOOKFORM-001: the Runbook form, its tables and extensions."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = typed_profiles(load_raw())[RUNBOOK[0]]

    def tree(self, text: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._body_diagnostics(
                RUNBOOK_PATH, self.profile, text, "active"
            )
        )

    def tables(self, text: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._table_diagnostics(RUNBOOK_PATH, self.profile, text)
        )

    def under(self, heading: str, block: str) -> str:
        """Insert an H3 block just before the given H2 (or at the end)."""

        if not heading:
            return RUNBOOK_BODY + "\n" + block + "\n"
        return RUNBOOK_BODY.replace(heading, block + "\n\n" + heading)

    def test_the_loaded_runbook_heading_lists_equal_the_form_h2_titles(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        titles = tuple(title for title, _ in RUNBOOK_TREE)
        loaded = next(f for f in registry.common_forms if f.form_id == "runbook")
        self.assertEqual(tuple(item.title for item in loaded.sections), titles)
        by_id = {profile.profile_id: profile for profile in registry.profiles}
        for profile_id in RUNBOOK:
            with self.subTest(profile=profile_id):
                headings = by_id[profile_id].headings
                self.assertEqual(headings.required, titles)
                self.assertEqual(headings.allowed, titles)
                self.assertFalse(headings.substantive_body)
                self.assertFalse(headings.ordered)

    def test_the_loader_copies_the_runbook_tables_to_the_source_profile(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        by_id = {profile.profile_id: profile for profile in registry.profiles}
        twin, source = by_id[RUNBOOK[1]], by_id[RUNBOOK[0]]
        self.assertEqual(source.tables, twin.tables)
        triggers, lifecycle = twin.tables
        self.assertEqual(
            (
                triggers.name,
                triggers.section,
                triggers.minimum_rows,
                triggers.row_identity,
            ),
            ("Triggers", "runbook-steps-actions", 0, "Trigger"),
        )
        self.assertEqual(
            [column.key for column in lifecycle.columns],
            list(RUNBOOK_TABLE_KEYS["Lifecycle Traceability"][1]),
        )
        self.assertTrue(all(column.required for column in triggers.columns))

    def test_the_repository_runbook_registry_is_valid_and_its_twin_matches(
        self,
    ) -> None:
        self.assertEqual(rules_of(load_raw()), set())
        REGISTRY_CHECK._assert_template_source_parity(CONTRACTS.load_registry(ROOT))

    def test_a_complete_runbook_passes_the_tree(self) -> None:
        self.assertEqual(self.tree(RUNBOOK_BODY), [])

    def test_a_triggers_table_passes_when_it_keeps_the_registered_columns(
        self,
    ) -> None:
        body = RUNBOOK_BODY.replace("Run it.", "Run it.\n\n" + TRIGGERS)
        self.assertEqual(self.tables(body), [])

    def test_a_header_only_triggers_table_passes_because_the_minimum_is_zero(
        self,
    ) -> None:
        header_only = "| Trigger | Action | Rollback |\n| --- | --- | --- |"
        self.assertEqual(self.tables(RUNBOOK_BODY.replace("Run it.", header_only)), [])
        self.assertEqual(self.tables(RUNBOOK_BODY), [])

    def test_a_reordered_or_missing_triggers_column_fails(self) -> None:
        for header in (
            "| Trigger | Rollback | Action |",
            "| Trigger | Action |",
            "| Trigger | Action | Rollback | Note |",
        ):
            cells = header.count("|") - 1
            table = f"{header}\n" + "| --- " * cells + "|\n" + "| a " * cells + "|"
            with self.subTest(header=header):
                self.assertEqual(
                    self.tables(RUNBOOK_BODY.replace("Run it.", table)),
                    ["BODY-TABLE-COLUMNS"],
                )

    def test_the_four_column_step_table_is_not_identified(self) -> None:
        step = (
            "| Step | Action | Expected result | Stop / escalate when |\n"
            "| --- | --- | --- | --- |\n| 1 | Run | Pass | Error |"
        )
        self.assertEqual(self.tables(RUNBOOK_BODY.replace("Run it.", step)), [])

    def test_a_triggers_table_outside_actions_is_not_looked_at(self) -> None:
        wrong = "| Trigger | Action |\n| --- | --- |\n| a | b |"
        body = RUNBOOK_BODY.replace("Stop on error.", wrong)
        self.assertEqual(self.tables(body), [])

    def test_recovery_procedures_is_accepted_under_recovery(self) -> None:
        block = "### Recovery Procedures\n\nRestore the replica from the snapshot."
        self.assertEqual(self.tree(self.under("", block)), [])
        before_rollback = RUNBOOK_BODY.replace(
            "### Escalation",
            block + "\n\n### Rollback\n\nUndo step 1.\n\n### Escalation",
        )
        self.assertEqual(self.tree(before_rollback), [])

    def test_recovery_procedures_under_another_h2_is_refused(self) -> None:
        block = "### Recovery Procedures\n\nRestore the replica."
        self.assertEqual(
            self.tree(self.under("## Validation", block)), ["BODY-H3-PARENT"]
        )

    def test_an_absent_recovery_procedures_passes_and_an_empty_one_fails(self) -> None:
        self.assertNotIn("Recovery Procedures", RUNBOOK_BODY)
        self.assertEqual(self.tree(RUNBOOK_BODY), [])
        self.assertEqual(
            self.tree(self.under("", "### Recovery Procedures\n")),
            ["BODY-SECTION-EMPTY"],
        )

    def test_lifecycle_traceability_belongs_under_validation(self) -> None:
        block = (
            "### Lifecycle Traceability\n\n"
            "| Promoted owner | Trigger or control | Evidence or recovery owner |\n"
            "| --- | --- | --- |\n| N/A | None | None |"
        )
        self.assertEqual(self.tree(self.under("## Recovery", block)), [])
        self.assertEqual(self.tree(self.under("## Steps", block)), ["BODY-H3-PARENT"])


INCIDENT_PATH = PurePosixPath(
    "docs/05.operations/incidents/2026/inc-0001-example/incident.md"
)
INCIDENT_BODY = md(
    "# Incident title",
    "## Summary",
    "### Event\n\n| Field | Value |\n| --- | --- |\n| Severity | SEV-2 |",
    "### Current Status\n\nInvestigating.",
    "## Impact",
    "### Affected Users\n\nOne team.",
    "### Severity and Duration\n\nSEV-2 for one hour.",
    "## Timeline",
    "### Events\n\nThe alert fired.",
    "### Decisions\n\nThe commander chose rollback.",
    "## Resolution",
    "### Mitigation\n\nRolled back.",
    "### Recovery Verification\n\nChecks pass.",
    "## Evidence",
    "### Evidence Sources\n\nA log link.",
    "### Follow-up Owners\n\nA Task owner.",
)
POSTMORTEM_PATH = PurePosixPath(
    "docs/05.operations/incidents/2026/inc-0001-example/postmortem.md"
)
POSTMORTEM_BODY = md(
    "# Postmortem title",
    "## Summary",
    "### Incident Reference\n\nIncident INC-0001 as recorded in the incident folder.",
    "### Review Scope\n\nThe whole event.",
    "## Root Cause",
    "### Causal Analysis\n\nA bad rollout.",
    "### Contributing Factors\n\nNo canary.",
    "## Impact",
    "### Observed Impact\n\nOne team.",
    "### Detection and Response\n\nAn alert fired.",
    "## Corrective Actions",
    "### Actions\n\nAdd a canary.",
    "### Verification\n\nThe canary catches it.",
    "## Evidence",
    "### Source Records\n\nA log link.",
    "### Review Decision\n\nApproved.",
)


class RoleFormBody(unittest.TestCase):
    """Shared checks for a role form; each subclass names its form and body."""

    PATH: PurePosixPath
    PROFILES: tuple[str, str]
    FORM_ID: str
    TREE: tuple
    TABLE_KEYS: dict
    BODY: str
    HEADER: tuple[str, ...]  # its registered columns
    HOME: str  # the H3 line its table belongs under

    @classmethod
    def setUpClass(cls) -> None:
        if cls is RoleFormBody:
            raise unittest.SkipTest("shared base; its subclasses run the checks")
        cls.profile = typed_profiles(load_raw())[cls.PROFILES[0]]

    def tree(self, text: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._body_diagnostics(
                self.PATH, self.profile, text, "active"
            )
        )

    def tables(self, text: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._table_diagnostics(self.PATH, self.profile, text)
        )

    def under(self, heading: str, block: str) -> str:
        """Insert an H3 block just before the given H2 (or at the end)."""

        if not heading:
            return self.BODY + "\n" + block + "\n"
        return self.BODY.replace("\n" + heading, "\n" + block + "\n\n" + heading, 1)

    def table(self, header: tuple[str, ...], *rows: tuple[str, ...]) -> str:
        lines = [
            "| " + " | ".join(header) + " |",
            "| " + " | ".join("---" for _ in header) + " |",
        ]
        lines += ["| " + " | ".join(row) + " |" for row in rows]
        return "\n".join(lines)

    def with_table(self, table: str, *, home: str | None = None) -> str:
        home = home or self.HOME
        return self.BODY.replace(home, home + "\n\n" + table, 1)

    def test_the_loaded_heading_lists_equal_the_form_h2_titles(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        titles = tuple(title for title, _ in self.TREE)
        loaded = next(f for f in registry.common_forms if f.form_id == self.FORM_ID)
        self.assertEqual(tuple(item.title for item in loaded.sections), titles)
        by_id = {profile.profile_id: profile for profile in registry.profiles}
        for profile_id in self.PROFILES:
            with self.subTest(profile=profile_id):
                headings = by_id[profile_id].headings
                self.assertEqual(headings.required, titles)
                self.assertEqual(headings.allowed, titles)
                self.assertFalse(headings.substantive_body)
                self.assertFalse(headings.ordered)

    def test_the_loader_copies_the_tables_to_the_source_profile(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        by_id = {profile.profile_id: profile for profile in registry.profiles}
        twin, source = by_id[self.PROFILES[1]], by_id[self.PROFILES[0]]
        self.assertEqual(source.tables, twin.tables)
        self.assertEqual(
            {
                t.name: (
                    t.section,
                    tuple(c.key for c in t.columns),
                    t.minimum_rows,
                    t.row_identity,
                )
                for t in twin.tables
            },
            self.TABLE_KEYS,
        )
        self.assertTrue(all(c.required for t in twin.tables for c in t.columns))

    def test_the_repository_registry_is_valid_and_its_twin_matches(self) -> None:
        self.assertEqual(rules_of(load_raw()), set())
        REGISTRY_CHECK._assert_template_source_parity(CONTRACTS.load_registry(ROOT))

    def test_a_complete_document_passes_the_tree(self) -> None:
        self.assertEqual(self.tree(self.BODY), [])
        self.assertEqual(self.tables(self.BODY), [])

    def test_the_optional_table_passes_with_the_registered_columns(self) -> None:
        row = tuple("x" for _ in self.HEADER)
        body = self.with_table(self.table(self.HEADER, row))
        self.assertEqual(self.tables(body), [])
        self.assertEqual(self.tree(body), [])

    def test_a_header_only_table_passes_because_the_minimum_is_zero(self) -> None:
        self.assertEqual(self.tables(self.with_table(self.table(self.HEADER))), [])

    def test_a_reordered_missing_or_extra_column_fails(self) -> None:
        first, second, third = self.HEADER
        for header in (
            (first, third, second),
            (first, second),
            (*self.HEADER, "Note"),
        ):
            table = self.table(header, tuple("x" for _ in header))
            with self.subTest(header=header):
                self.assertEqual(
                    self.tables(self.with_table(table)), ["BODY-TABLE-COLUMNS"]
                )

    def test_the_table_is_not_looked_at_outside_its_section(self) -> None:
        wrong = self.table(self.HEADER[:2], ("a", "b"))
        body = self.with_table(wrong, home="### Source Records")
        self.assertEqual(self.tables(body), [])


class IncidentFormTests(RoleFormBody):
    """SPEC-0171 VAL-INCIDENTFORM-001: the Incident form, its tables and extension."""

    PATH = INCIDENT_PATH
    PROFILES = INCIDENT
    FORM_ID = "incident"
    TREE = INCIDENT_TREE
    TABLE_KEYS = INCIDENT_TABLE_KEYS
    BODY = INCIDENT_BODY
    HEADER = ("Timestamp", "Event", "Actor")
    HOME = "The alert fired."

    def test_the_table_is_not_looked_at_outside_its_section(self) -> None:
        wrong = self.table(("Timestamp", "Event"), ("a", "b"))
        body = INCIDENT_BODY.replace("Checks pass.", wrong)
        self.assertEqual(self.tables(body), [])

    def test_the_metadata_table_is_not_a_contract_table(self) -> None:
        self.assertIn("| Field | Value |", INCIDENT_BODY)
        self.assertEqual(self.tables(INCIDENT_BODY), [])
        wrong = self.table(("Field",), ("Severity",))
        self.assertEqual(self.tables(self.with_table(wrong, home="Investigating.")), [])

    def test_lifecycle_traceability_belongs_under_evidence(self) -> None:
        block = (
            "### Lifecycle Traceability\n\n"
            "| Timeline or action | Evidence | Follow-up Task |\n"
            "| --- | --- | --- |\n| Alert | A log | N/A |"
        )
        self.assertEqual(self.tree(self.under("", block)), [])
        self.assertEqual(
            self.tree(self.under("## Evidence", block)), ["BODY-H3-PARENT"]
        )


class PostmortemFormTests(RoleFormBody):
    """SPEC-0171 VAL-INCIDENTFORM-001: the Postmortem form, tables and extensions."""

    PATH = POSTMORTEM_PATH
    PROFILES = POSTMORTEM
    FORM_ID = "postmortem"
    TREE = POSTMORTEM_TREE
    TABLE_KEYS = POSTMORTEM_TABLE_KEYS
    BODY = POSTMORTEM_BODY
    HEADER = ("Action", "Owner", "Verification")
    HOME = "Add a canary."

    WELL = "### What Went Well\n\nThe alert fired within a minute."

    def test_what_went_well_is_accepted_under_impact(self) -> None:
        self.assertEqual(self.tree(self.under("## Corrective Actions", self.WELL)), [])
        after_detection = POSTMORTEM_BODY.replace(
            "## Corrective Actions", self.WELL + "\n\n## Corrective Actions"
        )
        self.assertLess(
            after_detection.index("### Detection and Response"),
            after_detection.index("### What Went Well"),
        )

    def test_what_went_well_under_another_h2_is_refused(self) -> None:
        for heading in ("## Root Cause", "## Evidence"):
            with self.subTest(before=heading):
                self.assertEqual(
                    self.tree(self.under(heading, self.WELL)), ["BODY-H3-PARENT"]
                )
        self.assertEqual(self.tree(self.under("", self.WELL)), ["BODY-H3-PARENT"])

    def test_an_absent_what_went_well_passes_and_an_empty_one_fails(self) -> None:
        self.assertNotIn("What Went Well", POSTMORTEM_BODY)
        self.assertEqual(self.tree(POSTMORTEM_BODY), [])
        empty = self.under("## Corrective Actions", "### What Went Well\n")
        self.assertEqual(self.tree(empty), ["BODY-SECTION-EMPTY"])

    def test_what_went_wrong_is_an_h4_under_contributing_factors(self) -> None:
        body = POSTMORTEM_BODY.replace(
            "No canary.", "No canary.\n\n#### What Went Wrong\n\nA wrong assumption."
        )
        self.assertEqual(self.tree(body), [])

    def test_lifecycle_traceability_belongs_under_corrective_actions(self) -> None:
        block = (
            "### Lifecycle Traceability\n\n"
            "| Root cause or action | Owner and due state | Follow-up Task "
            "| Feedback target |\n| --- | --- | --- | --- |\n"
            "| Cause | Platform | N/A | Spec |"
        )
        self.assertEqual(self.tree(self.under("## Evidence", block)), [])
        self.assertEqual(self.tree(self.under("", block)), ["BODY-H3-PARENT"])


GOVERNANCE_POLICY_PATH = PurePosixPath(".agents/governance/agent-execution.md")
OPERATIONS_POLICY_PATH = PurePosixPath(
    "docs/05.operations/policies/0001-k8s-gitops-operations-policy.md"
)


def policy_body() -> str:
    return md(
        "# Policy title",
        "## Purpose",
        "### Objective\n\nKeep changes reviewable.",
        "### Authority\n\nPlatform owns this policy.",
        "## Scope",
        "### Applies To\n\nEvery change.",
        "### Exclusions\n\nNone: nothing is excluded.",
        "## Rules",
        "### Requirements\n\nReview every change.",
        "### Enforcement\n\nCI checks it.",
        "## Exceptions",
        "### Exception Conditions\n\nNone: no exception exists.",
        "### Approval and Review\n\nThe owner approves.",
        "## Ownership",
        "### Responsibilities\n\nPlatform.",
        "### Change and Adoption\n\nChanges follow the Spec.",
    )


class GovernancePolicyFormTests(RoleFormBody):
    """SPEC-0175 VAL-POLICY-001: the Policy form on governance rules."""

    PATH = GOVERNANCE_POLICY_PATH
    PROFILES = POLICY_GOVERNANCE
    FORM_ID = "policy"
    TREE = POLICY_TREE
    TABLE_KEYS = POLICY_GOVERNANCE_TABLE_KEYS
    BODY = policy_body()
    HEADER = ("Rule", "Condition", "Evidence")
    HOME = "Review every change."

    def test_the_loader_copies_the_tables_to_the_source_profile(self) -> None:
        super().test_the_loader_copies_the_tables_to_the_source_profile()
        self.assertIsNone(typed_profiles(load_raw())[self.PROFILES[0]].body_contract)

    def test_the_table_is_not_looked_at_outside_its_section(self) -> None:
        wrong = self.table(self.HEADER[:2], ("a", "b"))
        body = self.with_table(wrong, home="Platform owns this policy.")
        self.assertEqual(self.tables(body), [])


class OperationsPolicyFormTests(RoleFormBody):
    """SPEC-0175 VAL-POLICY-001: the Policy form on operations policies."""

    PATH = OPERATIONS_POLICY_PATH
    PROFILES = POLICY_OPERATIONS
    FORM_ID = "policy"
    TREE = POLICY_TREE
    TABLE_KEYS = POLICY_OPERATIONS_TABLE_KEYS
    BODY = policy_body()
    HEADER = ("Rule", "Condition", "Evidence")
    HOME = "Review every change."

    BLOCK = (
        "### Lifecycle Traceability\n\n"
        "| Promoted owner | Control owner | Enforcement surface |\n"
        "| --- | --- | --- |\n| N/A | Platform | CI |"
    )

    def test_the_table_is_not_looked_at_outside_its_section(self) -> None:
        wrong = self.table(self.HEADER[:2], ("a", "b"))
        body = self.with_table(wrong, home="Platform owns this policy.")
        self.assertEqual(self.tables(body), [])

    def test_the_loader_copies_the_tables_to_the_source_profile(self) -> None:
        super().test_the_loader_copies_the_tables_to_the_source_profile()
        contract = typed_profiles(load_raw())[self.PROFILES[0]].body_contract
        self.assertEqual(contract.section, "Ownership")
        self.assertEqual(contract.table_heading, "Lifecycle Traceability")

    def test_lifecycle_traceability_is_accepted_after_change_and_adoption(
        self,
    ) -> None:
        body = self.under("", self.BLOCK)
        self.assertLess(
            body.index("### Change and Adoption"),
            body.index("### Lifecycle Traceability"),
        )
        self.assertEqual(self.tree(body), [])
        self.assertEqual(self.tables(body), [])

    def test_lifecycle_traceability_under_another_h2_is_refused(self) -> None:
        for heading in ("## Rules", "## Exceptions", "## Ownership"):
            with self.subTest(before=heading):
                self.assertEqual(
                    self.tree(self.under(heading, self.BLOCK)), ["BODY-H3-PARENT"]
                )

    def test_an_absent_lifecycle_traceability_passes_and_an_empty_one_fails(
        self,
    ) -> None:
        self.assertNotIn("Lifecycle Traceability", self.BODY)
        empty = self.under("", "### Lifecycle Traceability\n")
        self.assertEqual(self.tree(empty), ["BODY-SECTION-EMPTY"])


class TemplateTwinTableTests(unittest.TestCase):
    """SPEC-0175 W03-H10: two tabled twins may not name one source profile."""

    def second_twin(self, raw: dict, *, tables: bool) -> dict:
        twin = copy.deepcopy(profile_of(raw, GUIDE[1]))
        twin["id"] = "common/template-operation-guide-second"
        twin["path_pattern"] = (
            "^docs/99\\.templates/templates/operations/guide\\.second$"
        )
        if not tables:
            twin["template_definition"]["tables"] = []
        raw["profiles"].append(twin)
        return raw

    def test_the_repository_registry_names_each_source_once(self) -> None:
        self.assertNotIn("REGISTRY_TABLE_TWIN", rules_of(load_raw()))

    def test_a_source_named_by_two_tabled_twins_is_refused(self) -> None:
        raw = self.second_twin(load_raw(), tables=True)
        self.assertIn("REGISTRY_TABLE_TWIN", rules_of(raw))

    def test_a_second_twin_without_tables_is_not_refused(self) -> None:
        raw = self.second_twin(load_raw(), tables=False)
        self.assertEqual(rules_of(raw), set())


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


class CurrentRegistryEightFormsOnlyTests(unittest.TestCase):
    def test_only_the_eight_form_profiles_use_the_tree(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        self.assertEqual(
            [item.form_id for item in registry.common_forms],
            EIGHT_FORMS,
        )
        self.assertEqual(
            sorted(p.profile_id for p in registry.profiles if p.form is not None),
            sorted(FORM_PROFILES),
        )
        self.assertEqual(
            sorted(p.profile_id for p in registry.profiles if p.template_definition),
            sorted(FORM_TEMPLATES),
        )


if __name__ == "__main__":
    unittest.main()
