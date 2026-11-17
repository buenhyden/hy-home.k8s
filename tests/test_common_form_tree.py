"""SPEC-0168: the common form model, its registry checks and heading-tree checks."""

from __future__ import annotations

import copy
import dataclasses
import importlib.util
import json
import re
import sys
import tempfile
import types
import unittest
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import document_authority as AUTHORITY  # noqa: E402
import document_contracts as CONTRACTS  # noqa: E402
from json_schema_validation import schema_errors  # noqa: E402


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
LINKS = _load_script("common_form_links", "validate-links-and-owners.py")

FORM_IDS = (
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
    "workspace-readme",
    "reference-pack-readme",
    "knowledge-map",
    "vocabulary",
    "prompt",
    "evaluation-task",
    "evaluation-score",
    "evaluation-results",
    "governance-document",
    "governance-role",
    "research",
    "audit",
    "data-reference",
)
# The profiles bound to a role: the clear common roles, then the local roles on
# their source profiles; every other profile carries none.
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
    "common/folder-agents-guide": "agents",
    "governance/skill": "skill",
    "common/native-skill-package": "skill",
    "common/readme-workspace-staging": "workspace-readme",
    "reference/research-pack": "reference-pack-readme",
    "reference/audit-pack": "reference-pack-readme",
    "reference/data-pack": "reference-pack-readme",
    "common/readme-repository": "root-readme",
    "common/readme-stage-index": "stage-readme",
    "common/readme-collection-index": "stage-readme",
    "common/readme-implementation": "service-readme",
    "common/readme-runtime-governance": "service-readme",
    "reference/audit": "audit",
    "reference/research": "research",
    "reference/data": "data-reference",
    "governance/provider": "governance-document",
    "governance/role": "governance-role",
    "governance/knowledge": "knowledge-map",
    "governance/vocabulary": "vocabulary",
    "governance/prompt": "prompt",
    "evaluation/task": "evaluation-task",
    "evaluation/score": "evaluation-score",
    "evaluation/results": "evaluation-results",
    "common/provider-native-metadata": "provider-native",
    "common/provider-native-command": "provider-native",
    "common/codex-agent-binding": "provider-native",
}
# The three templates of the role without a form carry a definition and no table.
LOCAL_TABLES = {
    "common/template-exception-provider-native-metadata": [],
    "common/template-exception-provider-native-command": [],
    "common/template-exception-provider-native-codex": [],
}
LOCAL_TEMPLATES = tuple(LOCAL_TABLES)
# A source profile inherits the tables of the template that names it.
LOCAL_SOURCES = {
    "common/template-exception-provider-native-metadata": "common/provider-native-metadata",
    "common/template-exception-provider-native-command": "common/provider-native-command",
    "common/template-exception-provider-native-codex": "common/codex-agent-binding",
}
LOCAL_PROFILE_TABLES = {
    **LOCAL_TABLES,
    **{source: LOCAL_TABLES[twin] for twin, source in LOCAL_SOURCES.items()},
}
GUIDE = ("operation/guide", "common/template-operation-guide")
ADR = ("sdlc/architecture-decision", "common/template-sdlc-architecture-decision")
GUIDE_TREE = (
    ("Purpose", ("Audience", "Outcome")),
    ("Prerequisites", ("Environment", "Authority")),
    ("Procedure", ("Steps", "Expected Results")),
    ("Troubleshooting", ("Symptoms", "Next Action")),
)
RUNBOOK = ("operation/runbook", "common/template-operation-runbook")
RUNBOOK_TREE = (
    ("Trigger and Scope", ("Trigger", "Targets")),
    ("Preflight", ("Authority", "Environment")),
    ("Procedure", ("Steps", "Stop Conditions")),
    ("Verification", ("Expected Results", "Unverified Conditions")),
    ("Escalation", ("Next Owner", "Recovery or Forward Repair")),
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
        "authority_ref": "ADR-0059",
        "parent_id": "runbook.escalation",
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
        "authority_ref": "ADR-0059",
        "parent_id": "runbook.verification",
        "title": "Lifecycle Traceability",
    },
]
# SPEC-0222: the core step table of the runbook, guide and their operations peers.
CORE_STEP_COLUMNS = ("Step", "Action", "Expected Result", "On Failure")
CORE_ACTION_COLUMNS = ("Action", "Owner", "Condition", "Evidence")
RUNBOOK_TABLE_KEYS = {
    "Steps": ("runbook.procedure", CORE_STEP_COLUMNS, 0, "Step"),
    "Lifecycle Traceability": (
        "runbook-lifecycle-traceability",
        ("Promoted owner", "Trigger or control", "Evidence or recovery owner"),
        1,
        "Promoted owner",
    ),
}
INCIDENT = ("operation/incident", "common/template-operation-incident")
INCIDENT_TREE = (
    ("Impact", ("Affected Users", "Observed Scope")),
    ("Response", ("Timeline", "Actions")),
    ("Resolution", ("Verified State", "Remaining Work")),
)
POSTMORTEM = ("operation/postmortem", "common/template-operation-postmortem")
POSTMORTEM_TREE = (
    ("Facts", ("Timeline", "Impact")),
    ("Causes", ("Contributing Factors", "Uncertainty")),
    ("Actions", ("Prevention", "Owners and Checks")),
)
ROOT_FORM = ("common/readme-repository", "common/template-readme-repository")
ROOT_FORM_TREE = (
    ("Purpose", ("Audience", "Outcome")),
    ("Getting Started", ("Prerequisites", "First Use")),
    ("Repository Map", ("Current Paths", "Owners")),
    ("Support", ("Help", "Related Documentation")),
)
# SPEC-0222: the index tables are the core paths tables of their H2.
ROOT_TABLE_KEYS = {
    "Directory Index": (
        "root-readme.map",
        ("Path", "Purpose"),
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
    ("Responsibility", ("Purpose", "Excluded Responsibilities")),
    ("Current Contents", ("Paths", "Owners")),
    ("Usage", ("Entry Points", "Checks")),
)
STAGE_TABLE_KEYS = {
    "Index": (
        "stage-readme.contents",
        ("Path", "Purpose"),
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
    ("Service", ("Purpose", "Interfaces")),
    ("Usage", ("Prerequisites", "Selected Start")),
    ("Checks", ("Readiness", "Failure Handling")),
)
SERVICE_TABLE_KEYS = {
    "External Interfaces": (
        "service-readme.service",
        ("Interface", "Producer", "Consumer", "Contract", "Failure"),
        0,
        "Interface",
    ),
    "Commands": (
        "service-readme.checks.1",
        ("Command", "Output"),
        0,
        "Command",
    ),
}
POLICY_GOVERNANCE = ("governance/rule", "common/template-governance-rule")
POLICY_OPERATIONS = ("operation/policy", "common/template-operation-policy")
POLICY_TREE = (
    ("Purpose and Scope", ("Objective", "Applies To")),
    ("Rules", ("Requirements", "Exceptions")),
    ("Enforcement", ("Mechanisms", "Limits")),
    ("Ownership", ("Owner", "Review Triggers")),
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
    "authority_ref": "ADR-0059",
    "parent_id": "policy.ownership",
    "title": "Lifecycle Traceability",
}
# SPEC-0222: the core Rules table and the local Rule Levels table keyed by Rule ID,
# whose Status stays the one optional extension (SPEC-0194, W03-D65).
POLICY_RULES_COLUMNS = (
    "Rule ID",
    "Condition",
    "Requirement",
    "Enforcement",
    "Evidence",
)
POLICY_RULES_OPTIONAL = ("Status",)
POLICY_RULES_TABLE = ("policy.rules", POLICY_RULES_COLUMNS, 0, "Rule ID")
POLICY_LEVELS_TABLE = (
    "policy.rules.1",
    ("Rule ID", "Level", *POLICY_RULES_OPTIONAL),
    0,
    "Rule ID",
)
AGENTS = ("common/folder-agents-guide", "common/template-agents-guide")
# SPEC-0222 WORK-007: the agent-instructions core tree; the core has no table.
AGENTS_TREE = (
    ("Scope", ("Allowed Scope", "Instruction Precedence")),
    ("Workflow", ("Intake", "Execution")),
    ("Boundaries", ("Authority", "Secrets and External Effects")),
    ("Verification", ("Checks", "Reporting")),
)
AGENTS_TABLE_KEYS: dict = {}
SKILL_GOVERNANCE = ("governance/skill", "common/template-governance-skill")
SKILL_NATIVE = ("common/native-skill-package", "common/template-native-skill")
SKILL_TREE = (
    ("Trigger", ("When to Use", "When Not to Use")),
    ("Procedure", ("Steps", "Failure Handling")),
    ("Outputs", ("Artifacts", "Handoff")),
    ("Verification", ("Checks", "Limits")),
)
SKILL_EXTENSION = {
    "id": "skill-authority-boundary",
    "kind": "local_h3",
    "condition": (
        "a workflow that applies existing policy and states its own authority boundary"
    ),
    "owner": "platform",
    "verification": "the form tree check",
    "review": "when the Skill form version changes",
    "removal": "when the common Skill form gains an authority H3",
    "authority_ref": "ADR-0059",
    "parent_id": "skill.trigger",
    "title": "Authority Boundary",
}
SKILL_TABLE_KEYS = {
    "Steps": ("skill.procedure.1", ("Step", "Input", "Output"), 0, "Step")
}
WORKSPACE_FORM = (
    "common/readme-workspace-staging",
    "common/template-readme-workspace-staging",
)
WORKSPACE_FORM_TREE = (
    ("Overview", ()),
    ("Scope", ("Permitted Artifacts", "Forbidden Local State")),
    ("Structure", ()),
    ("Usage", ("Promotion and Cleanup", "Tracking Rules")),
    ("Related Documents", ()),
)
PACK_FORM = (
    "reference/research-pack",
    "common/template-readme-research-pack",
    "reference/audit-pack",
    "common/template-readme-audit-pack",
    "reference/data-pack",
    "common/template-readme-data-pack",
)
PACK_FORM_TREE = (
    ("Overview", ()),
    ("Scope", ()),
    ("Pack Contract", ()),
    ("Method", ()),
    ("Structure", ()),
    ("Pack Index", ()),
    ("Usage", ()),
    ("Refresh and Succession", ()),
    ("Review and Closure", ()),
    ("Refresh and Retention", ()),
    ("Evidence Boundary", ()),
    ("Related Documents", ()),
)
PACK_NOT_REQUIRED = (
    "Method",
    "Refresh and Succession",
    "Review and Closure",
    "Refresh and Retention",
)
PACK_CLOSURES = dict(zip(PACK_FORM[::2], PACK_NOT_REQUIRED[1:]))
PACK_EXTENSIONS = [
    {
        "id": "pack-external-finding-vocabulary",
        "kind": "local_h3",
        "condition": (
            "a research pack that fixes the external finding vocabulary its reports use"
        ),
        "owner": "platform",
        "verification": "the form tree check",
        "review": "when the Reference Pack README form changes",
        "removal": ("when the Reference Pack README form gains a matching section"),
        "authority_ref": "ADR-0059",
        "parent_id": "reference-pack-readme-pack-contract",
        "title": "External Finding Vocabulary",
    },
    {
        "id": "pack-separate-evidence-axes",
        "kind": "local_h3",
        "condition": (
            "a research pack that keeps its evidence axes apart in its reports"
        ),
        "owner": "platform",
        "verification": "the form tree check",
        "review": "when the Reference Pack README form changes",
        "removal": ("when the Reference Pack README form gains a matching section"),
        "authority_ref": "ADR-0059",
        "parent_id": "reference-pack-readme-pack-contract",
        "title": "Separate Evidence Axes",
    },
]
POLICY_GOVERNANCE_TABLE_KEYS = {
    "Rules": POLICY_RULES_TABLE,
    "Rule Levels": POLICY_LEVELS_TABLE,
}
POLICY_OPERATIONS_TABLE_KEYS = {
    "Rules": POLICY_RULES_TABLE,
    "Rule Levels": POLICY_LEVELS_TABLE,
    "Lifecycle Traceability": (
        "policy-lifecycle-traceability",
        ("Promoted owner", "Control owner", "Enforcement surface"),
        1,
        "Promoted owner",
    ),
}
# SPEC-0195 (W03-D03, W03-D08, W03-D55): the Requirement form, its two local H3
# extensions and its tables. SPEC-0222 WORK-003: the Functional and Quality
# Requirements tables are instances of the core requirement.requirements table
# (Priority required, in the core's lower case), the core requirement.quality
# table is defined and not rendered, and Lifecycle Traceability stays a local
# table of its own.
REQUIREMENT = ("sdlc/requirement", "common/template-sdlc-requirement")
REQUIREMENT_TREE = (
    ("Overview", ("Problem and Outcome", "Stakeholders")),
    ("Scope", ("In Scope", "Constraints and Exclusions")),
    ("Requirements", ("Functional Requirements", "Quality Requirements")),
    ("Traceability", ("Sources", "Verification Links")),
)
REQUIREMENT_EXTENSIONS = [
    {
        "id": "requirement-lifecycle-traceability",
        "kind": "local_h3",
        "condition": (
            "a requirement in a status the body contract enforces (draft, "
            "in-review, approved) maps each member to its acceptance criterion"
        ),
        "owner": "platform",
        "verification": "the body-contract check",
        "review": "when the Requirement form version changes",
        "removal": "when requirement lineage has another registered owner",
        "authority_ref": "ADR-0059",
        "parent_id": "requirement.relations",
        "title": "Lifecycle Traceability",
    },
    {
        "id": "requirement-archived-lineage",
        "kind": "local_h3",
        "condition": (
            "a requirement summarizes the deleted or archived documents whose "
            "current meaning it owns, so that Git history recovers each of them"
        ),
        "owner": "platform",
        "verification": ("the package-exit check and the retired-identity reservation"),
        "review": "when the Requirement form version changes",
        "removal": "when requirement lineage has another registered owner",
        "authority_ref": "ADR-0059",
        "parent_id": "requirement.relations",
        "title": "Archived Lineage",
    },
]
REQUIREMENT_COLUMNS = (
    "Requirement ID",
    "Statement",
    "Rationale",
    "Acceptance",
    "Priority",
)
REQUIREMENT_QUALITY_COLUMNS = (
    "Requirement ID",
    "Attribute",
    "Measure",
    "Unit",
    "Environment",
    "Criterion",
)
REQUIREMENT_TABLE_KEYS = {
    "Requirements": (
        "requirement.requirements",
        REQUIREMENT_COLUMNS,
        1,
        "Requirement ID",
    ),
    "Quality Measures": (
        "requirement.requirements",
        REQUIREMENT_QUALITY_COLUMNS,
        0,
        "Requirement ID",
    ),
    "Lifecycle Traceability": (
        "requirement-lifecycle-traceability",
        ("Requirement ID", "Acceptance criterion"),
        1,
        "Requirement ID",
    ),
}
# SPEC-0197 (W03-D03, W03-D08, W03-D57): the Architecture form, its two local H3
# extensions and its three tables; the description profiles keep their body
# contract and carry no H2 list.
ARCHITECTURE = (
    "sdlc/architecture-description",
    "common/template-sdlc-architecture-description",
)
ARCHITECTURE_TREE = (
    ("Context and Boundaries", ("System Boundary", "Constraints")),
    ("Structure", ("Building Blocks", "Interfaces")),
    ("Runtime Behavior", ("Normal Flow", "Failure and Recovery")),
    ("Quality Scenarios", ("Scenarios", "Trade-offs")),
    ("Decisions and Adoption", ("Decisions", "Adoption Boundaries")),
)
ARCHITECTURE_EXTENSIONS = [
    {
        "id": "architecture-lifecycle-traceability",
        "kind": "local_h3",
        "condition": (
            "an architecture description in a status the body contract enforces "
            "(draft, in-review, active) maps each cited requirement to its "
            "quality attribute or boundary and its ADR or Spec"
        ),
        "owner": "platform",
        "verification": "the body-contract check",
        "review": "when the Architecture form version changes",
        "removal": "when architecture lineage has another registered owner",
        "authority_ref": "ADR-0059",
        "parent_id": "architecture.decisions",
        "title": "Lifecycle Traceability",
    },
    {
        "id": "architecture-archived-lineage",
        "kind": "local_h3",
        "condition": (
            "an architecture description summarizes the deleted or archived "
            "documents whose current meaning it owns, so that Git history "
            "recovers each of them"
        ),
        "owner": "platform",
        "verification": "the retired-identity reservation",
        "review": "when the Architecture form version changes",
        "removal": "when architecture lineage has another registered owner",
        "authority_ref": "ADR-0059",
        "parent_id": "architecture.decisions",
        "title": "Archived Lineage",
    },
]
ARCHITECTURE_INTERFACE_COLUMNS = (
    "Interface",
    "Producer",
    "Consumer",
    "Contract",
    "Failure",
)
ARCHITECTURE_TABLE_KEYS = {
    "External Interfaces": (
        "architecture.structure",
        ARCHITECTURE_INTERFACE_COLUMNS,
        0,
        "Interface",
    ),
    "Constraints": (
        "architecture.context.2",
        ("Architecture ID", "Constraint", "Affected Components"),
        0,
        "Architecture ID",
    ),
    "Quality Scenarios": (
        "architecture.quality.1",
        ("Quality attribute", "Stimulus", "Environment", "Response", "Measure"),
        0,
        "Quality attribute",
    ),
    "Lifecycle Traceability": (
        "architecture-lifecycle-traceability",
        ("Upstream requirement", "Quality attribute or boundary", "ADR / Spec"),
        1,
        "Upstream requirement",
    ),
}
# SPEC-0198 (W03-D02, W03-D03, W03-D08, W03-D52, W03-D57, W03-D69): the ADR
# form, its local H3 extension, its retained form for ADR-0001 to ADR-0061 and
# its two tables; the decision profiles keep their body contract and carry no
# H2 list. SPEC-0222 WORK-006 binds the form to the core `decision` role.
ADR_TREE = (
    ("Context", ("Problem and Drivers", "Decision Scope")),
    ("Options", ("Considered Options", "Trade-offs")),
    ("Decision", ("Chosen Option", "Authority and Effect")),
    ("Consequences", ("Impacts", "Follow-up")),
)
# The closed range ADR-0001 to ADR-0061 and nothing else.
ADR_BOUND = "^ADR-(?:000[1-9]|00[1-5][0-9]|006[01])$"
ADR_RETAINED_LISTS = {
    "required": [
        "Overview",
        "Context",
        "Decision",
        "Explicit Non-goals",
        "Consequences",
        "Alternatives",
        "Traceability",
    ],
    "optional": [],
    "forbidden": [],
}
ADR_EXTENSIONS = [
    {
        "id": "adr-lifecycle-traceability",
        "kind": "local_h3",
        "condition": (
            "a decision in a status the body contract enforces (proposed) maps "
            "its lineage, its replacement relation and its affected Spec"
        ),
        "owner": "platform",
        "verification": "the body-contract check",
        "review": "when the ADR form version changes",
        "removal": "when decision lineage has another registered owner",
        "authority_ref": "ADR-0059",
        "parent_id": "decision.decision",
        "title": "Lifecycle Traceability",
    },
    {
        "id": "adr-accepted-retained-form",
        "kind": "retained_form",
        "condition": (
            "an accepted ADR from ADR-0001 to ADR-0061 keeps the seven H2 it was "
            "accepted with; an ADR outside that range takes the form tree in every "
            "status"
        ),
        "owner": "platform",
        "verification": "tests/test_common_form_tree.py",
        "review": "when an ADR in the range is replaced by a successor",
        "removal": (
            "when no ADR in the range remains in the tree, each having been "
            "replaced by a successor; the bound is never widened"
        ),
        "authority_ref": "ADR-0059",
        "statuses": ["accepted"],
        "identity_bound": ADR_BOUND,
        "retained_sections": ADR_RETAINED_LISTS,
        "body_contract": {
            "section": "Traceability",
            "table_heading": "Lifecycle Traceability",
        },
    },
]
ADR_TABLE_KEYS = {
    "Options": (
        "decision.options",
        ("Option", "Benefit", "Cost and Risk", "Reason"),
        0,
        "Option",
    ),
    # SPEC-0222: the former Alternatives table stays as a local table of its
    # own after the core table, so a recorded row whose Benefit has no source
    # fact keeps every fact (ADR-0062).
    "Alternatives": (
        "decision.options.2",
        ("Alternative", "Trade-off"),
        0,
        "Alternative",
    ),
    "Lifecycle Traceability": (
        "adr-lifecycle-traceability",
        ("Decision lineage", "Replacement relation", "Affected Spec"),
        1,
        "Decision lineage",
    ),
}
# SPEC-0186: the six small local roles, each (source, twin), its H2 tree with no
# H3, and its tables as (name, section id, column keys, minimum rows, identity).
KNOWLEDGE_FORM = (
    "governance/knowledge",
    "common/template-governance-knowledge",
)
KNOWLEDGE_FORM_TREE = (
    ("Overview", ()),
    ("Authority Boundary", ()),
    ("Pointer Index", ()),
    ("Validation and Refresh", ()),
    ("Related Documents", ()),
)
VOCABULARY_FORM = (
    "governance/vocabulary",
    "common/template-governance-vocabulary",
)
VOCABULARY_FORM_TREE = (
    ("Purpose", ()),
    ("Scope", ()),
    ("Normative Language", ()),
    ("Repository Vocabulary", ()),
    ("Local Extensions", ()),
    ("Maintenance", ()),
    ("References", ()),
)
VOCABULARY_TABLES = [
    (
        "Term ID",
        "vocabulary-repository-vocabulary",
        (
            "Term ID",
            "Term",
            "Korean",
            "Definition",
            "Not to Confuse",
            "Policy Owner",
            "Contract Version",
        ),
        0,
        "Term ID",
    )
]
PROMPT_FORM = ("governance/prompt", "common/template-governance-prompt")
PROMPT_FORM_TREE = (
    ("Overview", ()),
    ("Authority Boundary", ()),
    ("Inputs", ()),
    ("Output", ()),
    ("Validation", ()),
    ("Refusal Conditions", ()),
    ("Related Documents", ()),
)
TASK_FORM = ("evaluation/task", "common/template-evaluation-task")
TASK_FORM_TREE = (
    ("Overview", ()),
    ("Declared Trials", ()),
    ("Signals and Criteria", ()),
    ("Human Calibration", ()),
    ("Related Documents", ()),
)
TASK_TABLES = [
    (
        "Field",
        "evaluation-task-overview",
        ("Field", "Declared value"),
        0,
        "Field",
    ),
    (
        "Trial ID",
        "evaluation-task-declared-trials",
        (
            "Trial ID",
            "Baseline output",
            "With-skill output",
            "Pair status",
            "Partial reason",
        ),
        0,
        "Trial ID",
    ),
    (
        "Criterion ID",
        "evaluation-task-signals-and-criteria",
        ("Criterion ID", "Observable signal", "Scoring rule", "Scorer ID"),
        0,
        "Criterion ID",
    ),
]
SCORE_FORM = ("evaluation/score", "common/template-evaluation-score")
SCORE_FORM_TREE = (
    ("Overview", ()),
    ("Trial Evidence", ()),
    ("Criterion Scores", ()),
    ("Human Calibration", ()),
    ("Related Documents", ()),
)
SCORE_TABLES = [
    (
        "Field",
        "evaluation-score-overview",
        ("Field", "Observed value"),
        0,
        "Field",
    ),
    (
        "Trial ID",
        "evaluation-score-trial-evidence",
        (
            "Trial ID",
            "Baseline output and hash",
            "With-skill output and hash",
            "Session references",
            "Evidence status",
        ),
        0,
        "Trial ID",
    ),
    (
        "Trial ID",
        "evaluation-score-criterion-scores",
        (
            "Trial ID",
            "Criterion ID",
            "Baseline observed signal and raw locator",
            "With-skill observed signal and raw locator",
            "Baseline score",
            "With-skill score",
        ),
        0,
        "Criterion ID",
    ),
]
RESULTS_FORM = ("evaluation/results", "common/template-evaluation-results")
RESULTS_FORM_TREE = (
    ("Overview", ()),
    ("Pair Coverage", ()),
    ("Aggregate", ()),
    ("Limitations", ()),
    ("Related Documents", ()),
)
RESULTS_TABLES = [
    (
        "Cycle ID",
        "evaluation-results-pair-coverage",
        (
            "Cycle ID",
            "Trial ID",
            "Declared pairs",
            "Complete pairs",
            "Task",
            "Score",
            "Partial reason",
        ),
        0,
        "Cycle ID",
    ),
    (
        "Scope",
        "evaluation-results-aggregate",
        (
            "Scope",
            "Actual pairs",
            "Criterion ID",
            "Baseline summary",
            "With-skill summary",
            "Calibration reference",
        ),
        0,
        "Criterion ID",
    ),
]
# (form id, title, (source, twin), tree, tables, link-only section title)
SMALL_FORMS = (
    (
        "knowledge-map",
        "Knowledge Map",
        KNOWLEDGE_FORM,
        KNOWLEDGE_FORM_TREE,
        [],
        "Related Documents",
    ),
    (
        "vocabulary",
        "Vocabulary",
        VOCABULARY_FORM,
        VOCABULARY_FORM_TREE,
        VOCABULARY_TABLES,
        "References",
    ),
    ("prompt", "Prompt", PROMPT_FORM, PROMPT_FORM_TREE, [], "Related Documents"),
    (
        "evaluation-task",
        "Evaluation Task",
        TASK_FORM,
        TASK_FORM_TREE,
        TASK_TABLES,
        "Related Documents",
    ),
    (
        "evaluation-score",
        "Evaluation Score",
        SCORE_FORM,
        SCORE_FORM_TREE,
        SCORE_TABLES,
        "Related Documents",
    ),
    (
        "evaluation-results",
        "Evaluation Results",
        RESULTS_FORM,
        RESULTS_FORM_TREE,
        RESULTS_TABLES,
        "Related Documents",
    ),
)
# SPEC-0188: the governance document (provider note) and governance role forms.
# The role tree holds the eight H3 of the Current Contract; the provider tree none.
GOVERNANCE_ROLE_H3 = (
    "Role",
    "When to Use",
    "Inputs",
    "Outputs",
    "Guardrails",
    "Capability and Evidence",
    "Handoff / Escalation",
    "Postflight",
)
GOVERNANCE_DOCUMENT_FORM = (
    "governance/provider",
    "common/template-governance-provider",
)
GOVERNANCE_ROLE_FORM = ("governance/role", "common/template-governance-role")
GOVERNANCE_DOCUMENT_TREE = (
    ("Overview", ()),
    ("Authority Boundary", ()),
    ("Governance Context", ()),
    ("Current Contract", ()),
    ("Validation and Refresh", ()),
    ("Related Documents", ()),
)
GOVERNANCE_ROLE_TREE = (
    ("Overview", ()),
    ("Authority Boundary", ()),
    ("Governance Context", ()),
    ("Current Contract", GOVERNANCE_ROLE_H3),
    ("Validation and Refresh", ()),
    ("Related Documents", ()),
)
GOVERNANCE_FORMS = (
    (
        "governance-document",
        "Governance Document",
        GOVERNANCE_DOCUMENT_FORM,
        GOVERNANCE_DOCUMENT_TREE,
        [],
        "Related Documents",
    ),
    (
        "governance-role",
        "Governance Role",
        GOVERNANCE_ROLE_FORM,
        GOVERNANCE_ROLE_TREE,
        [],
        "Related Documents",
    ),
)
# SPEC-0222: the research and audit reports bind their core roles. The thirteen
# published members keep the eight H2 of the former reference-report form through
# an identity-bound retained form until Q07-CUTOVER disposes of them.
FORMER_REFERENCE_H2 = (
    "Overview",
    "Reference Type",
    "Authority Boundary",
    "Scope",
    "Definitions / Facts",
    "Sources",
    "Review and Freshness",
    "Related Documents",
)
RESEARCH = ("reference/research", "common/template-reference-research")
RESEARCH_TREE = (
    ("Question and Scope", ("Question", "Scope")),
    ("Sources", ("Primary Sources", "Versions and Dates")),
    ("Analysis", ("Findings", "Alternatives")),
    ("Application and Limits", ("Design Implications", "Unverified Conditions")),
)
RESEARCH_SOURCES = (
    ("Source ID", "source_id", "identifier"),
    ("Source", "url", "reference"),
    ("Version", "version", "string-or-none"),
    ("Checked At", "checked", "timestamp"),
    ("Finding", "finding", "string"),
    ("Application", "application", "string"),
    ("Limits", "limits", "string"),
)
RESEARCH_TABLE_KEYS = {
    "Source ID": (
        "research.sources",
        tuple(label for label, _, _ in RESEARCH_SOURCES),
        0,
        "Source ID",
    ),
    "Claim": (
        "research-claim-source-matrix",
        ("Claim", "Source", "Verification state"),
        0,
        "Claim",
    ),
    "Source": (
        "research.sources.1",
        ("Source", "Grade", "Retrieved", "Relevance"),
        0,
        "Source",
    ),
}
RETAINED_REMOVAL = (
    "when Q07-CUTOVER disposes of the bound members after their successors are "
    "accepted; the bound is never widened"
)
RESEARCH_EXTENSIONS = [
    {
        "id": "research-claim-source-matrix",
        "kind": "local_h3",
        "condition": (
            "a research report that records each claim against its sources in a "
            "Claim-Source Matrix table"
        ),
        "owner": "platform",
        "verification": "the form tree check and the Claim table check",
        "review": "when the Research form changes",
        "removal": (
            "when research.sources carries every claim's source facts and no report "
            "keeps the matrix"
        ),
        "parent_id": "research.analysis",
        "title": "Claim-Source Matrix",
        "authority_ref": "SPEC-0222",
    },
    {
        "id": "research-published-retained-form",
        "kind": "retained_form",
        "condition": (
            "a published research member RES-0001-m0001 to RES-0001-m0012 keeps the "
            "eight H2 it was published with; every other research member takes the "
            "form tree"
        ),
        "owner": "platform",
        "verification": "tests/test_common_form_tree.py",
        "review": "when a bound member's successor is published",
        "removal": RETAINED_REMOVAL,
        "statuses": ["published"],
        "identity_bound": "^RES-0001-m00(?:0[1-9]|1[0-2])$",
        "retained_sections": {
            "required": list(FORMER_REFERENCE_H2),
            "optional": [],
            "forbidden": [],
        },
        "authority_ref": "SPEC-0222",
    },
]
AUDIT = ("reference/audit", "common/template-reference-audit")
AUDIT_TREE = (
    ("Scope", ("Subject", "Read Coverage")),
    ("Findings", ("Evidence", "Conflicts and Gaps")),
    ("Actions", ("Owners", "Acceptance Conditions")),
)
AUDIT_FINDINGS = (
    ("Finding ID", "finding_id", "identifier"),
    ("Requirement", "requirement", "reference"),
    ("Evidence", "evidence", "reference-list"),
    ("Classification", "classification", "enum"),
    ("Action", "action", "string"),
    ("Owner", "owner", "string"),
    ("Acceptance", "acceptance", "string"),
)
AUDIT_TABLE_KEYS = {
    "Finding ID": (
        "audit.findings",
        tuple(label for label, _, _ in AUDIT_FINDINGS),
        0,
        "Finding ID",
    ),
    "Criterion": ("audit.scope.2", ("Criterion", "In-scope surface"), 0, "Criterion"),
    "Observation": (
        "audit.findings.1",
        ("Observation", "Source and input", "Result"),
        0,
        "Observation",
    ),
    "ID": (
        "audit.findings.2",
        (
            "ID",
            "Finding or gap",
            "Requirement",
            "Fact or hypothesis",
            "Severity",
            "Evidence",
            "Action",
            "Acceptance",
        ),
        0,
        "ID",
    ),
    "Remediation": (
        "audit.actions.1",
        ("Remediation", "Owner", "Due or decision date"),
        0,
        "Remediation",
    ),
}
AUDIT_EXTENSIONS = [
    {
        "id": "audit-published-retained-form",
        "kind": "retained_form",
        "condition": (
            "the published audit member AUD-0001-m0001 keeps the eight H2 it was "
            "published with; every other audit member takes the form tree"
        ),
        "owner": "platform",
        "verification": "tests/test_common_form_tree.py",
        "review": "when the bound member's successor is published",
        "removal": RETAINED_REMOVAL,
        "statuses": ["published"],
        "identity_bound": "^AUD-0001-m0001$",
        "retained_sections": {
            "required": list(FORMER_REFERENCE_H2),
            "optional": [],
            "forbidden": [],
        },
        "authority_ref": "SPEC-0222",
    },
]
# SPEC-0222: the data reports bind the data-reference core role. Its template
# carries the core schema table and keeps the former data tables as local tables:
# the producer of a field keyed by Field, the provenance and the generation.
DATA_REFERENCE = ("reference/data", "common/template-reference-data")
DATA_REFERENCE_TREE = (
    ("Purpose", ("Consumers", "Boundaries")),
    ("Provenance", ("Collection", "Versions and Dates")),
    ("Interpretation", ("Schema and Units", "Limits")),
)
DATA_REFERENCE_SCHEMA = (
    ("Field", "field", "identifier"),
    ("Type", "type", "string"),
    ("Unit", "unit", "string-or-none"),
    ("Meaning", "meaning", "string"),
    ("Limits", "limitations", "string"),
)
DATA_REFERENCE_TABLE_KEYS = {
    "Field": (
        "data-reference.interpretation",
        tuple(label for label, _, _ in DATA_REFERENCE_SCHEMA),
        0,
        "Field",
    ),
    "Producer": ("data-reference.provenance.1", ("Field", "Producer"), 0, "Field"),
    "Source": (
        "data-reference.provenance.1",
        ("Source", "Revision or observation", "Derivation"),
        0,
        "Source",
    ),
    "Generation command": (
        "data-reference.provenance.1",
        ("Generation command", "Refresh trigger", "Owner"),
        0,
        "Generation command",
    ),
}
# Every local form in registry order: the six small forms, then SPEC-0188's two.
LOCAL_FORMS = SMALL_FORMS + GOVERNANCE_FORMS


def slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


LOCAL_LINK_ONLY = {
    "workspace-readme": {"workspace-readme-related-documents"},
    "reference-pack-readme": {"reference-pack-readme-related-documents"},
    **{
        form_id: {f"{form_id}-{slug(link)}"}
        for form_id, _, _, _, _, link in LOCAL_FORMS
    },
}
# The research form keeps Primary Sources link-only, as the former reference
# report kept its Sources section (W03-D36).
LOCAL_LINK_ONLY["research"] = {"research.sources.1"}
# SPEC-0200 (W03-D03, W03-D04, W03-D08, W03-D65): the Spec and Plan forms, the
# Spec's local H3 extension and the four tables; the profiles carry no H2 list.
SPEC_FORM = ("sdlc/spec", "common/template-sdlc-spec")
SPEC_FORM_TREE = (
    ("Overview", ("Goal", "Consumers")),
    ("Scope", ("In Scope", "Out of Scope")),
    ("Behavior Contract", ("Inputs and Outputs", "Failure Behavior")),
    ("Acceptance Criteria", ("Criteria", "Verification Strategy")),
)
# SPEC-0221: the approved and frozen Specs and Plans keep the tree they were
# approved with, bound to their four identities.
SPEC_RETAINED_TREE = (
    ("Overview", ("Intent", "Owning Requirements")),
    ("Scope", ("In Scope", "Non-goals")),
    ("Behavior Contract", ("Normal Behavior", "Failure and Edge Cases")),
    ("Acceptance Criteria", ("Criteria", "Evidence Requirements")),
    ("References", ("Normative and Evidence", "Historical and Navigation")),
)
PLAN_RETAINED_TREE = (
    ("Overview", ("Goal and Boundary", "Assumptions")),
    ("Dependencies", ("Prerequisites", "Dependency Order")),
    ("Implementation Strategy", ("Work Breakdown", "Change and Rollback")),
    ("Verification Plan", ("Verification Matrix", "Stage Placement")),
    ("Risks", ("Risks and Mitigations", "Escalation")),
    ("Promotion Map", ("Durable Meaning", "Owner and Receipt")),
)
SPEC_RETAINED_BOUND = "^SPEC-0(?:161|221)$"
PLAN_RETAINED_BOUND = "^SPEC-0(?:161|221)-PLAN-0001$"
SPEC_FORM_EXTENSIONS = [
    {
        "id": "spec-lifecycle-traceability",
        "kind": "local_h3",
        "condition": (
            "a Spec in a status the body contract enforces (draft, in-review, "
            "approved, in-progress, blocked) maps each requirement member to its "
            "Spec criterion, its architecture or an explicit exclusion, and its "
            "verification method"
        ),
        "owner": "platform",
        "verification": "the body-contract check",
        "review": "when the Spec form version changes",
        "removal": "when Spec traceability has another registered owner",
        "authority_ref": "ADR-0059",
        "parent_id": "spec.acceptance",
        "title": "Lifecycle Traceability",
    },
    {
        "id": "spec-approved-retained-form",
        "kind": "retained_form",
        "condition": (
            "an approved Spec of SPEC-0161 or SPEC-0221 keeps the five H2 it was "
            "approved with and its Lifecycle Traceability table under References; "
            "every other Spec takes the form tree"
        ),
        "owner": "platform",
        "verification": "tests/test_common_form_tree.py",
        "review": "when SPEC-0161 or SPEC-0221 leaves the tree",
        "removal": "when neither package remains in the tree; the bound is never widened",
        "authority_ref": "ADR-0059",
        "statuses": ["approved"],
        "identity_bound": SPEC_RETAINED_BOUND,
        "retained_sections": {
            "required": [h2 for h2, _ in SPEC_RETAINED_TREE],
            "optional": [],
            "forbidden": [],
        },
        "body_contract": {
            "section": "References",
            "table_heading": "Lifecycle Traceability",
        },
    },
]
PLAN_FORM_EXTENSIONS = [
    {
        "id": "plan-approved-retained-form",
        "kind": "retained_form",
        "condition": (
            "an approved Plan of SPEC-0161 or SPEC-0221 keeps the six H2 it was "
            "approved with and its Work Breakdown table under Implementation "
            "Strategy; every other Plan takes the form tree"
        ),
        "owner": "platform",
        "verification": "tests/test_common_form_tree.py",
        "review": "when SPEC-0161 or SPEC-0221 leaves the tree",
        "removal": "when neither package remains in the tree; the bound is never widened",
        "authority_ref": "ADR-0059",
        "statuses": ["approved"],
        "identity_bound": PLAN_RETAINED_BOUND,
        "retained_sections": {
            "required": [h2 for h2, _ in PLAN_RETAINED_TREE],
            "optional": [],
            "forbidden": [],
        },
        "body_contract": {
            "section": "Implementation Strategy",
            "table_heading": "Work Breakdown",
        },
        "section_titles": {
            "plan.intent.2": "Goal and Boundary",
            "plan.work.1": "Work Breakdown",
            "plan.promotion.1": "Owner and Receipt",
        },
    },
]
CORE_CHECK_COLUMNS = (
    "Check ID",
    "Guarantee",
    "Input",
    "Trust Boundary",
    "Required When",
    "Evidence",
)
CORE_WORK_UNIT_COLUMNS = (
    "Work Unit",
    "Outcome",
    "Depends On",
    "Owner",
    "Write Scope",
    "Acceptance",
    "Checks",
)
SPEC_FORM_TABLE_KEYS = {
    "Checks": ("spec.acceptance", CORE_CHECK_COLUMNS, 0, "Check ID"),
    "Criteria": (
        "spec.acceptance.1",
        ("Criterion ID", "Expected Result"),
        1,
        "Criterion ID",
    ),
    "Lifecycle Traceability": (
        "spec-lifecycle-traceability",
        ("Requirement ID", "Spec criterion", "Architecture", "Verification method"),
        1,
        "Spec criterion",
    ),
}
PLAN_FORM = ("sdlc/plan", "common/template-sdlc-plan")
PLAN_FORM_TREE = (
    ("Overview", ("Outcome", "Constraints")),
    ("Dependencies", ("Prerequisites", "Shared Resources")),
    ("Work Breakdown", ("Work Units", "Dependency Edges")),
    ("Verification Plan", ("Selected Checks", "Evidence Plan")),
    ("Promotion Map", ("Durable Owners", "Consumer Updates")),
)
PLAN_FORM_TABLE_KEYS = {
    "Units": ("plan.work", CORE_WORK_UNIT_COLUMNS, 0, "Work Unit"),
    "Checks": ("plan.verification", CORE_CHECK_COLUMNS, 0, "Check ID"),
    "Work Breakdown": (
        "plan.work.1",
        ("Work Unit", "Criteria", "Work", "Dependencies", "Task", "Verification"),
        1,
        "Work Unit",
    ),
    "Promotion": (
        "plan.promotion.1",
        ("Promotion ID", "Target Owner", "Acceptance", "Evidence"),
        1,
        "Promotion ID",
    ),
}
# SPEC-0221: an adopted form takes the target section IDs, <role>.<group> for
# an H2 and <role>.<group>.<n> for an H3; every other form keeps the slug IDs.
TARGET_GROUPS = {
    "guide": ("purpose", "prerequisites", "steps", "troubleshoot"),
    "runbook": ("trigger", "preflight", "procedure", "verification", "escalation"),
    "policy": ("purpose", "rules", "enforcement", "ownership"),
    "incident": ("impact", "response", "resolution"),
    "postmortem": ("facts", "causes", "actions"),
    "requirement": ("intent", "scope", "requirements", "relations"),
    "architecture": ("context", "structure", "behavior", "quality", "decisions"),
    "spec": ("intent", "scope", "behavior", "acceptance"),
    "plan": ("intent", "dependencies", "work", "verification", "promotion"),
    "root-readme": ("purpose", "start", "map", "support"),
    "stage-readme": ("scope", "contents", "use"),
    "service-readme": ("service", "use", "checks"),
    "skill": ("trigger", "procedure", "output", "verification"),
    # SPEC-0222: the Task form takes the core section IDs.
    "task": ("scope", "work", "evidence", "acceptance", "handoff"),
    "adr": ("context", "options", "decision", "consequences"),
    "agents": ("scope", "workflow", "limits", "verification"),
    "research": ("question", "sources", "analysis", "application"),
    "audit": ("scope", "findings", "actions"),
    "data-reference": ("purpose", "provenance", "interpretation"),
}
# SPEC-0222: a form whose ID differs from its core role takes the role's prefix.
CORE_PREFIX = {"adr": "decision", "agents": "agent-instructions"}


def section_id_of(
    form_id: str,
    position: int,
    title: str,
    n: int | None = None,
    child: str | None = None,
) -> str:
    groups = TARGET_GROUPS.get(form_id)
    if groups is not None:
        h2 = f"{CORE_PREFIX.get(form_id, form_id)}.{groups[position - 1]}"
        return h2 if n is None else f"{h2}.{n}"
    h2 = f"{form_id}-{slug(title)}"
    return h2 if child is None else f"{h2}-{slug(child)}"


SDLC_TASK_FORM = ("sdlc/task", "common/template-sdlc-task")
SDLC_TASK_FORM_TREE = (
    ("Scope", ("Objective and Parent", "Inputs and Authority")),
    ("Execution Log", ("Work Performed", "Blockers and Decisions")),
    ("Verification Evidence", ("Results", "Resolution Links")),
    ("Acceptance Decision", ("Criterion Decisions", "Remaining Conditions")),
    ("Handoff", ("Promotion Receipt", "Next Owner")),
)
SDLC_TASK_FORM_EXTENSIONS = [
    {
        "id": "task-lifecycle-traceability",
        "kind": "local_h3",
        "condition": (
            "a Task in a status the body contract enforces (draft, ready, "
            "in-progress, blocked) keeps, for each work item, its upstream Spec "
            "criterion, its result and its evidence, keyed by the Item of the core "
            "task.work_items row"
        ),
        "owner": "platform",
        "verification": "the body-contract check",
        "review": "when the Task form version changes",
        "removal": "when Task work items have another registered owner",
        "authority_ref": "ADR-0059",
        "parent_id": "task.work",
        "title": "Lifecycle Traceability",
    },
    {
        "id": "task-residue-handoff",
        "kind": "local_h3",
        "condition": (
            "a Task that records residue (an open handoff, conflict, adoption or "
            "survey item) keeps it in one table of this name, after the evidence "
            "table, with a matching entry in the work residue ledger"
        ),
        "owner": "platform",
        "verification": "the work residue ledger check of scripts/validate-work-residue-ledger.py",
        "review": "when the work residue ledger design changes or the Task form version changes",
        "removal": "when the work residue ledger has another registered host for residue",
        "authority_ref": "ADR-0059",
        "parent_id": "task.evidence",
        "title": "Residue Handoff",
    },
]
# SPEC-0222: the three core tables and the local Lifecycle Traceability table.
SDLC_TASK_FORM_TABLE_KEYS = {
    "Work Items": (
        "task.work",
        ("Item", "Work Unit", "Owner", "Status", "Blocker"),
        0,
        "Item",
    ),
    "Lifecycle Traceability": (
        "task-lifecycle-traceability",
        ("Item", "Upstream criterion", "Result", "Evidence"),
        1,
        "Item",
    ),
    "Results": (
        "task.evidence",
        (
            "Evidence ID",
            "Criteria",
            "Work Unit",
            "Method",
            "Input",
            "Tool and Config",
            "Command",
            "Exit",
            "Result",
            "Location",
            "Required",
            "Resolves",
        ),
        1,
        "Evidence ID",
    ),
    "Criterion Decisions": (
        "task.acceptance",
        (
            "Criterion",
            "Intent",
            "Acceptance",
            "Evidence",
            "Decision",
            "Accepted By",
            "Current Owner",
            "Reassigned To",
        ),
        1,
        "Criterion",
    ),
}
# The twenty-seven roles that carry a form; every other profile keeps its H2 lists.
FORM_PROFILES = (
    REQUIREMENT
    + ARCHITECTURE
    + ADR
    + SPEC_FORM
    + PLAN_FORM
    + SDLC_TASK_FORM
    + GUIDE
    + RUNBOOK
    + INCIDENT
    + POSTMORTEM
    + ROOT_FORM
    + STAGE_FORM
    + SERVICE_FORM
    + POLICY_GOVERNANCE
    + POLICY_OPERATIONS
    + AGENTS
    + SKILL_GOVERNANCE
    + SKILL_NATIVE
    + WORKSPACE_FORM
    + PACK_FORM
    + KNOWLEDGE_FORM
    + VOCABULARY_FORM
    + PROMPT_FORM
    + TASK_FORM
    + SCORE_FORM
    + RESULTS_FORM
    + GOVERNANCE_DOCUMENT_FORM
    + GOVERNANCE_ROLE_FORM
    + RESEARCH
    + AUDIT
    + DATA_REFERENCE
)
FORM_TEMPLATES = (
    REQUIREMENT[1],
    ARCHITECTURE[1],
    ADR[1],
    SPEC_FORM[1],
    PLAN_FORM[1],
    SDLC_TASK_FORM[1],
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
    AGENTS[1],
    SKILL_GOVERNANCE[1],
    SKILL_NATIVE[1],
    WORKSPACE_FORM[1],
    PACK_FORM[1],
    PACK_FORM[3],
    PACK_FORM[5],
    KNOWLEDGE_FORM[1],
    VOCABULARY_FORM[1],
    PROMPT_FORM[1],
    TASK_FORM[1],
    SCORE_FORM[1],
    RESULTS_FORM[1],
    GOVERNANCE_DOCUMENT_FORM[1],
    GOVERNANCE_ROLE_FORM[1],
    RESEARCH[1],
    AUDIT[1],
    DATA_REFERENCE[1],
)
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
        "authority_ref": "ADR-0059",
        "parent_id": "incident.resolution",
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
        "authority_ref": "ADR-0059",
        "parent_id": "postmortem.actions",
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
        "authority_ref": "ADR-0059",
        "parent_id": "postmortem.facts",
        "title": "What Went Well",
    },
]
INCIDENT_TABLE_KEYS = {
    "Events": (
        "incident.response.1",
        ("Timestamp", "Event", "Actor"),
        0,
        "Timestamp",
    ),
    "Actions": ("incident.response", CORE_ACTION_COLUMNS, 0, "Action"),
    "Lifecycle Traceability": (
        "incident-lifecycle-traceability",
        ("Timeline or action", "Evidence", "Follow-up Task"),
        1,
        "Timeline or action",
    ),
}
POSTMORTEM_TABLE_KEYS = {
    "Actions": ("postmortem.actions", CORE_ACTION_COLUMNS, 0, "Action"),
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
    "authority_ref": "ADR-0059",
    "parent_id": "guide.troubleshoot",
    "title": "Lifecycle Traceability",
}
GUIDE_TABLE_KEYS = {
    "Steps": ("guide.steps", CORE_STEP_COLUMNS, 0, "Step"),
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
        "authority_ref": "ADR-0059",
        "parent_id": "g-procedure",
        "title": "Cluster Notes",
    }
    item.update(fields)
    return item


def definition(**fields: object) -> dict:
    item = {
        "contract_id": "COMMON-DOC-FORM-1",
        "contract_version": "2.0.0",
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


def lists_of(**lists: list[str]) -> dict:
    """A `sections` value as a registry of an earlier MAJOR carried it."""

    return {"required": [], "optional": [], "forbidden": [], **lists}


def semantic_rules_of(raw: dict) -> set[str]:
    """The rules of the semantic registry check, which runs past the schema: the
    schema refuses a `sections` key first, so its own rule is read directly."""

    return {
        item.rule_id for item in CONTRACTS._terminal_semantic_diagnostics(ROOT, raw)
    }


class RepositoryRegistryTests(unittest.TestCase):
    def test_repository_registry_binds_clear_roles(self) -> None:
        raw = load_raw()
        self.assertIsInstance(raw["schema_version"], str)
        self.assertEqual(
            int(raw["schema_version"].split(".")[0]), AUTHORITY.REGISTRY_MAJOR
        )
        common = raw["common_forms"]
        self.assertEqual(common["contract_id"], "COMMON-DOC-FORM-1")
        self.assertEqual(common["version"], "2.0.0")
        by_id = {profile["id"]: profile for profile in raw["profiles"]}
        for form_id, tree, extensions, tables, profiles, body_section in (
            (
                "guide",
                GUIDE_TREE,
                [GUIDE_EXTENSION],
                GUIDE_TABLE_KEYS,
                GUIDE,
                "Troubleshooting",
            ),
            (
                "runbook",
                RUNBOOK_TREE,
                RUNBOOK_EXTENSIONS,
                RUNBOOK_TABLE_KEYS,
                RUNBOOK,
                "Verification",
            ),
            (
                "incident",
                INCIDENT_TREE,
                INCIDENT_EXTENSIONS,
                INCIDENT_TABLE_KEYS,
                INCIDENT,
                "Resolution",
            ),
            (
                "postmortem",
                POSTMORTEM_TREE,
                POSTMORTEM_EXTENSIONS,
                POSTMORTEM_TABLE_KEYS,
                POSTMORTEM,
                "Actions",
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
            ("agents", AGENTS_TREE, [], AGENTS_TABLE_KEYS, AGENTS, None),
            (
                "skill",
                SKILL_TREE,
                [SKILL_EXTENSION],
                SKILL_TABLE_KEYS,
                SKILL_GOVERNANCE,
                None,
            ),
            (
                "skill",
                SKILL_TREE,
                [SKILL_EXTENSION],
                SKILL_TABLE_KEYS,
                SKILL_NATIVE,
                None,
            ),
            (
                "workspace-readme",
                WORKSPACE_FORM_TREE,
                [],
                {},
                WORKSPACE_FORM,
                None,
            ),
            (
                "reference-pack-readme",
                PACK_FORM_TREE,
                PACK_EXTENSIONS,
                {},
                PACK_FORM,
                None,
            ),
            *(
                (form_id, tree, [], tables, profiles, None)
                for form_id, _, profiles, tree, tables, _ in LOCAL_FORMS
            ),
            (
                "requirement",
                REQUIREMENT_TREE,
                REQUIREMENT_EXTENSIONS,
                REQUIREMENT_TABLE_KEYS,
                REQUIREMENT,
                "Traceability",
            ),
            (
                "architecture",
                ARCHITECTURE_TREE,
                ARCHITECTURE_EXTENSIONS,
                ARCHITECTURE_TABLE_KEYS,
                ARCHITECTURE,
                "Decisions and Adoption",
            ),
            (
                "adr",
                ADR_TREE,
                ADR_EXTENSIONS,
                ADR_TABLE_KEYS,
                ADR,
                "Decision",
            ),
            (
                "spec",
                SPEC_FORM_TREE,
                SPEC_FORM_EXTENSIONS,
                SPEC_FORM_TABLE_KEYS,
                SPEC_FORM,
                "Acceptance Criteria",
            ),
            (
                "plan",
                PLAN_FORM_TREE,
                PLAN_FORM_EXTENSIONS,
                PLAN_FORM_TABLE_KEYS,
                PLAN_FORM,
                "Work Breakdown",
            ),
            (
                "task",
                SDLC_TASK_FORM_TREE,
                SDLC_TASK_FORM_EXTENSIONS,
                SDLC_TASK_FORM_TABLE_KEYS,
                SDLC_TASK_FORM,
                "Execution Log",
            ),
            (
                "research",
                RESEARCH_TREE,
                RESEARCH_EXTENSIONS,
                RESEARCH_TABLE_KEYS,
                RESEARCH,
                None,
            ),
            (
                "audit",
                AUDIT_TREE,
                AUDIT_EXTENSIONS,
                AUDIT_TABLE_KEYS,
                AUDIT,
                None,
            ),
            (
                "data-reference",
                DATA_REFERENCE_TREE,
                [],
                DATA_REFERENCE_TABLE_KEYS,
                DATA_REFERENCE,
                None,
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
                        section_id_of(form_id, position, title),
                        title,
                        position,
                        [
                            (
                                section_id_of(form_id, position, title, n, child),
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
                {
                    "reference-pack-readme": {
                        f"reference-pack-readme-{title.lower().replace(' ', '-')}"
                        for title in PACK_NOT_REQUIRED
                    },
                }.get(form_id, set()),
            )
            self.assertTrue(all(isinstance(n.get("link_only"), bool) for n in every))
            self.assertEqual(
                {node["section_id"] for node in every if node.get("link_only")},
                LOCAL_LINK_ONLY.get(form_id, set()),
            )
            self.assertEqual(loaded["extensions"], extensions)
            for profile_id in profiles:
                profile = by_id[profile_id]
                # SPEC-0205: no profile carries an H2 list.
                self.assertNotIn("sections", profile)
                contract = profile["relationships"]["body_contract"]
                self.assertEqual(contract and contract["section"], body_section)
            for twin in (p for p in profiles if by_id[p]["mode"] == "template"):
                self.assertEqual(
                    sorted(
                        (
                            table["name"],
                            table["section"],
                            tuple(column["key"] for column in table["columns"]),
                            table["minimum_rows"],
                            table["row_identity"],
                        )
                        for table in by_id[twin]["template_definition"]["tables"]
                    ),
                    sorted(
                        [(name, *spec) for name, spec in tables.items()]
                        if isinstance(tables, dict)
                        else tables
                    ),
                )
                core_types = {
                    (t["table_id"], c["label"]): c["value_type"]
                    for t in loaded.get("core", {}).get("tables", ())
                    for c in t["columns"]
                }
                for table in by_id[twin]["template_definition"]["tables"]:
                    if "table_id" in table:
                        # A core table keeps the core value types; the strict
                        # registry check compares it (REGISTRY_CORE_TABLE).
                        continue
                    for column in table["columns"]:
                        self.assertTrue(column["meaning"])
                        # The research Sources table dates its retrieval (W03-D21);
                        # a core table takes the core value type (SPEC-0222).
                        self.assertEqual(
                            column["data_type"],
                            core_types.get(
                                (table.get("table_id"), column["key"]),
                                "date" if column["key"] == "Retrieved" else "string",
                            ),
                        )
                        self.assertIs(
                            column["required"],
                            not (
                                form_id == "policy"
                                and column["key"] in POLICY_RULES_OPTIONAL
                            ),
                        )
        for profile_id, profile in by_id.items():
            sources = profile["relationships"]["source_profile_ids"]
            expected = ROLE_BINDINGS.get(
                profile_id, ROLE_BINDINGS.get(sources[0]) if sources else None
            )
            with self.subTest(profile=profile_id):
                self.assertEqual(profile.get("document_role"), expected)
                if profile_id in FORM_TEMPLATES + LOCAL_TEMPLATES:
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

    def test_repository_registry_loads_role_forms_and_tables(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        forms = {item.form_id: item for item in registry.common_forms}
        tables = {
            "guide": ["Steps", "Lifecycle Traceability"],
            "runbook": ["Steps", "Lifecycle Traceability"],
            "incident": ["Events", "Actions", "Lifecycle Traceability"],
            "postmortem": ["Actions", "Lifecycle Traceability"],
            "root-readme": ["Directory Index"],
            "stage-readme": ["Index"],
            "service-readme": ["External Interfaces", "Commands"],
            "policy": ["Rules", "Rule Levels", "Lifecycle Traceability"],
            "agents": [],
            "skill": ["Steps"],
            "workspace-readme": [],
            "reference-pack-readme": [],
            "requirement": [
                "Requirements",
                "Quality Measures",
                "Lifecycle Traceability",
            ],
            "architecture": [
                "External Interfaces",
                "Constraints",
                "Quality Scenarios",
                "Lifecycle Traceability",
            ],
            "adr": ["Options", "Alternatives", "Lifecycle Traceability"],
            "spec": ["Checks", "Criteria", "Lifecycle Traceability"],
            "plan": ["Units", "Checks", "Work Breakdown", "Promotion"],
            "task": [
                "Work Items",
                "Lifecycle Traceability",
                "Results",
                "Criterion Decisions",
            ],
            "research": list(RESEARCH_TABLE_KEYS),
            "audit": list(AUDIT_TABLE_KEYS),
            "data-reference": list(DATA_REFERENCE_TABLE_KEYS),
            **{
                form_id: [name for name, *_ in tables]
                for form_id, _, _, _, tables, _ in LOCAL_FORMS
            },
        }
        governance_tables = ["Rules", "Rule Levels"]
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
                            ("agents", AGENTS),
                            ("skill", SKILL_GOVERNANCE + SKILL_NATIVE),
                            ("workspace-readme", WORKSPACE_FORM),
                            ("reference-pack-readme", PACK_FORM),
                            ("requirement", REQUIREMENT),
                            ("architecture", ARCHITECTURE),
                            ("adr", ADR),
                            ("spec", SPEC_FORM),
                            ("plan", PLAN_FORM),
                            ("task", SDLC_TASK_FORM),
                            ("research", RESEARCH),
                            ("audit", AUDIT),
                            ("data-reference", DATA_REFERENCE),
                            *(
                                (form_id, profiles)
                                for form_id, _, profiles, _, _, _ in LOCAL_FORMS
                            ),
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
                    # A role without a form: provider-native or no role.
                    self.assertIsNone(profile.form)
                    self.assertEqual(
                        [(t.name, t.section) for t in profile.tables],
                        LOCAL_PROFILE_TABLES.get(profile.profile_id, []),
                    )
                if profile.profile_id in FORM_TEMPLATES + LOCAL_TEMPLATES:
                    self.assertIsNotNone(profile.template_definition)
                else:
                    self.assertIsNone(profile.template_definition)
        by_id = {profile.profile_id: profile for profile in registry.profiles}
        self.assertEqual(by_id["governance/rule"].document_role, "policy")
        self.assertEqual(by_id["governance/role"].document_role, "governance-role")
        self.assertEqual(
            by_id["governance/provider"].document_role, "governance-document"
        )

    def test_registered_forms_are_bound_to_profiles_and_admitted_by_schema(
        self,
    ) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        forms = [form.form_id for form in registry.common_forms]
        self.assertCountEqual(
            forms,
            {profile.form.form_id for profile in registry.profiles if profile.form},
        )
        schema = json.loads(
            (
                ROOT / "docs/99.templates/contracts/document-profile.schema.json"
            ).read_text("utf-8")
        )
        allowed = schema["$defs"]["common_form"]["properties"]["form_id"]["enum"]
        self.assertLessEqual(set(forms), set(allowed))
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
        loaded = next(form for form in registry.common_forms if form.form_id == "guide")
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
        self.assertIsNone(by_id["common/provider-native-command"].form)

    def test_valid_extensions_are_typed(self) -> None:
        retained = {
            "id": "g-legacy",
            "kind": "retained_form",
            "condition": "terminal documents keep their H2 headings",
            "owner": "platform",
            "verification": "tests/test_common_form_tree.py",
            "review": "each release",
            "removal": "when no terminal guide remains",
            "authority_ref": "ADR-0059",
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
        profile["sections"] = lists_of(required=["Overview"])
        self.assertIn("REGISTRY_FORM_LEGACY_LISTS", semantic_rules_of(raw))
        self.assertEqual(rules_of(raw), {"REGISTRY_SCHEMA"})
        raw = self.candidate()
        profile = next(item for item in raw["profiles"] if item["id"] == GUIDE[1])
        profile["sections"] = lists_of(forbidden=["Scratch"])
        self.assertIn("REGISTRY_FORM_LEGACY_LISTS", semantic_rules_of(raw))

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
        # SPEC-0181: the key descriptions and the dialect are admitted top-level
        # sections, each alone and both absent, as in a comparison-base registry.
        # SPEC-0194 admits the policy rule ID section the same way.
        for section in ("frontmatter_keys", "frontmatter_dialect", "policy_rule_ids"):
            candidate = {**load_raw(), section: {}}
            AUTHORITY.validate_registry_authority(candidate)
            del candidate[section]
            AUTHORITY.validate_registry_authority(candidate)
        raw = {**load_raw(), "frontmatter_key": {}}
        with self.assertRaisesRegex(AUTHORITY.AuthorityError, "REGISTRY_TOP_LEVEL"):
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
                # A local role's template holds a definition, which needs a role.
                profile.pop("document_role", None)
                profile.pop("template_definition", None)
        # SPEC-0205: only the new rule fires; an authored, router or template profile
        # without a role has no form.
        self.assertEqual(rules_of(raw), {"REGISTRY_FORM_REQUIRED"})

    def test_template_twin_must_share_its_sources_role(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        REGISTRY_CHECK._assert_template_source_parity(registry)
        raw = self.candidate()
        profile_of(raw, GUIDE[1])["document_role"] = "runbook"
        # SPEC-0222: the moved template also lacks the runbook core table.
        self.assertEqual(rules_of(raw), {"REGISTRY_CORE_TABLE"})
        loaded = CONTRACTS._typed_registry_from_mapping(raw)
        with self.assertRaisesRegex(AssertionError, "template/source contract differs"):
            REGISTRY_CHECK._assert_template_source_parity(loaded)
        raw = self.candidate()
        twin = profile_of(raw, GUIDE[1])
        twin.pop("document_role")
        twin.pop("template_definition")
        self.assertEqual(rules_of(raw), {"REGISTRY_FORM_REQUIRED"})
        loaded = CONTRACTS._typed_registry_from_mapping(raw)
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
        # The template holds its definition; without a role it is refused.
        self.assertEqual(twin["document_role"], "governance-role")
        self.assertEqual(rules_of(raw), set())
        del twin["document_role"]
        self.assertIn("REGISTRY_TEMPLATE_DEFINITION", rules_of(raw))

    def test_named_paths_must_exist(self) -> None:
        raw = self.candidate(definition(consumer_paths=["scripts/missing.py"]))
        self.assertIn("REGISTRY_TEMPLATE_DEFINITION", rules_of(raw))

    def test_incomplete_definition_fails_the_schema(self) -> None:
        for key in (
            "contract_id",
            "contract_version",
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
                headings = CONTRACTS.heading_contract(by_id[profile_id])
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
        self.assertEqual(
            CONTRACTS.heading_contract(profile).required,
            ("Overview", "Related Documents"),
        )
        self.assertEqual(
            CONTRACTS.heading_contract(profile).allowed,
            ("Overview", "Procedure", "Related Documents"),
        )

    def test_the_loader_types_the_tables_and_copies_them_to_the_source(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        by_id = {profile.profile_id: profile for profile in registry.profiles}
        twin, source = by_id[GUIDE[1]], by_id[GUIDE[0]]
        self.assertEqual(source.tables, twin.tables)
        steps, lifecycle = twin.tables
        self.assertEqual(
            (steps.name, steps.section, steps.minimum_rows, steps.row_identity),
            ("Steps", "guide.steps", 0, "Step"),
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
                profile_of(raw, profile_id)["sections"] = lists_of(
                    **{key: ["Verification"]}
                )
                with self.subTest(list=key, profile=profile_id):
                    self.assertIn("REGISTRY_FORM_LEGACY_LISTS", semantic_rules_of(raw))

    def test_a_table_section_must_be_a_form_section_or_extension(self) -> None:
        raw = load_raw()
        guide_tables(raw)[0]["section"] = "guide-missing"
        self.assertIn("REGISTRY_TABLE_SECTION", rules_of(raw))
        raw = load_raw()
        guide_tables(raw)[0]["section"] = "Actions"
        self.assertIn("REGISTRY_TABLE_SECTION", rules_of(raw))
        for accepted in ("guide.purpose", "guide.troubleshoot.1"):
            raw = unbind_guide(load_raw())
            guide_tables(raw)[0]["section"] = accepted
            with self.subTest(section=accepted):
                self.assertEqual(rules_of(raw), set())

    def test_a_table_needs_a_form_to_name_a_section(self) -> None:
        raw = load_raw()
        raw["common_forms"]["forms"] = []
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

    def test_a_bare_childless_h2_fails_and_an_explained_one_passes(self) -> None:
        bare = VALID.replace(
            "- [Specification](spec.md)", "None is stated in this document."
        )
        self.assertEqual(self.found(bare), ["BODY-SECTION-BARE"])
        explained = VALID.replace(
            "- [Specification](spec.md)",
            "This guide has no related document; link one here when it exists.",
        )
        self.assertEqual(self.found(explained), [])
        self.assertEqual(self.found(bare, profile=self.template), [])

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
        for body in (
            "",
            "N/A",
            "N/A.",
            "TBD",
            "pending",
            "&nbsp;",
            "**&#160;**",
            "| Key | Value |\n| --- | --- |\n| &nbsp; | &#160; |",
        ):
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
        for code in (
            "```text\nkubectl get pods\n```",
            "```text\n&nbsp;\n```",
            "`&nbsp;`",
        ):
            with self.subTest(code=code):
                text = VALID.replace("Name where the guide applies.", code)
                self.assertEqual(self.found(text), [])

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


STEPS = (
    "| Step | Action | Expected Result | On Failure |\n"
    "| --- | --- | --- | --- |\n| 1 | Run | Read | Stop |"
)
OTHER = "| Name | Value |\n| --- | --- |\n| a | b |"
LIFECYCLE = (
    "| Promoted owner | Audience outcome | Operating surface |\n"
    "| --- | --- | --- |\n| N/A | Readers | Surface |"
)


def guide_body(actions: str, verification: str = "") -> str:
    return md(
        "# Guide",
        "## Procedure",
        "### Steps",
        actions,
        "### Expected Results",
        "Pass.",
        "## Troubleshooting",
        "### Next Action",
        "None.",
        *((verification,) if verification else ()),
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
            "| Step | Expected Result | Action | On Failure |",
            "| Action | Step | Expected Result | On Failure |",
            "| Step | Action | Expected Result |",
            "| Step | Action | Expected Result | On Failure | Note |",
            "| Step | Action | Check | On Failure |",
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
        header_only = "| Step | Action | Expected Result | On Failure |\n| --- | --- | --- | --- |"
        self.assertEqual(
            self.found(guide_body(header_only), self.strict), ["BODY-TABLE-ROWS"]
        )
        self.assertEqual(
            self.found(guide_body(STEPS), self.strict), ["BODY-TABLE-ROWS"]
        )
        self.assertEqual(
            self.found(guide_body(STEPS + "\n| 2 | Run | Read | Stop |"), self.strict),
            [],
        )
        split = guide_body(STEPS + "\n\n#### Detail\n\n" + STEPS)
        self.assertEqual(self.found(split, self.strict), [])

    def test_a_table_in_another_section_is_not_looked_at(self) -> None:
        body = md(
            "# Guide",
            "## Procedure",
            "### Steps",
            "Run it.",
            "## Troubleshooting",
            "### Next Action",
            "| Step | Action |\n| --- | --- |\n| 1 | Run |",
        )
        self.assertEqual(self.found(body), [])
        self.assertEqual(self.found(body, self.strict), ["BODY-TABLE-ROWS"])

    def test_a_non_unique_section_heading_is_left_to_the_tree_check(self) -> None:
        # SPEC-0222: the core table belongs to the Procedure H2.
        body = guide_body(STEPS) + "\n## Procedure\n\n" + OTHER + "\n"
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

    def test_template_columns_are_checked_without_authored_row_minima(self) -> None:
        wrong = "| Step | Action |\n| --- | --- |\n| 1 | Run |"
        text = (
            "---\n"
            'title: "Guide"\nversion: "1.0.0"\ntype: "operation/guide"\n'
            'status: "active"\nowner: "platform"\nupdated: "2026-11-12"\n'
            'artifact_id: "GDE-0001"\n---\n\n' + guide_body(wrong)
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
        self.assertEqual(rules(self.template), ["BODY-TABLE-COLUMNS"])
        self.assertEqual(rules(self.strict), ["BODY-TABLE-COLUMNS", "BODY-TABLE-ROWS"])
        self.assertEqual(
            rules(dataclasses.replace(self.strict, mode="template")),
            ["BODY-TABLE-COLUMNS"],
        )


class OptionalTrailingColumnTests(unittest.TestCase):
    """SPEC-0172: optional columns may only trail the required ones."""

    @classmethod
    def raw_with_note(cls, required: bool = False) -> dict:
        # A core table refuses an appended column; the trailing-column rule is
        # a local table rule, read here on the unbound guide table.
        raw = unbind_guide(load_raw())
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
        self.assertEqual(self.found(CORE_STEP_COLUMNS), [])

    def test_a_present_optional_trailing_column_passes(self) -> None:
        self.assertEqual(self.found((*CORE_STEP_COLUMNS, "Note")), [])

    def test_a_missing_required_column_fails(self) -> None:
        for header in (("Step", "Action", "Expected Result"), ("Step",)):
            with self.subTest(header=header):
                self.assertEqual(self.found(header), ["BODY-TABLE-COLUMNS"])

    def test_a_reordered_or_extra_column_still_fails(self) -> None:
        for header in (
            ("Step", "Action", "Expected Result", "Note"),
            ("Step", "Action", "Expected Result", "Note", "On Failure"),
            (*CORE_STEP_COLUMNS, "Note", "Extra"),
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
        headings = CONTRACTS.heading_contract(self.profile)
        self.assertEqual(headings.required, titles)
        self.assertEqual(headings.allowed, titles)

    def test_a_complete_body_passes_the_tree_and_an_h4_is_allowed(self) -> None:
        self.assertEqual(self.tree(self.BODY), [])
        deeper = self.BODY.replace(
            "### Outcome\n\nText.",
            "### Outcome\n\nText.\n\n#### In Scope\n\nText.",
        )
        self.assertEqual(self.tree(deeper), [])

    def test_a_missing_h3_or_an_old_h2_fails_the_tree(self) -> None:
        self.assertIn(
            "BODY-H3-REQUIRED",
            self.tree(self.BODY.replace("### Current Paths", "#### Current Paths")),
        )
        self.assertNotEqual(self.tree(self.BODY + "\n## Structure\n\nText.\n"), [])

    def test_the_paths_table_is_read_anywhere_in_repository_map(self) -> None:
        def tables(home: str, header: str) -> list[str]:
            row = "| " + " | ".join("x" for _ in header.split("|")[1:-1]) + " |"
            delimiter = "|" + " --- |" * len(header.split("|")[1:-1])
            text = self.BODY.replace(home, f"{home}\n\n{header}\n{delimiter}\n{row}", 1)
            return sorted(
                item.rule_id
                for item in MARKDOWN._table_diagnostics(
                    PurePosixPath("README.md"), self.profile, text
                )
            )

        for home in ("### Current Paths\n\nText.", "### Owners\n\nText."):
            with self.subTest(home=home):
                self.assertEqual(tables(home, "| Path | Purpose |"), [])
                self.assertEqual(
                    tables(home, "| Path | Purpose | Owner |"), ["BODY-TABLE-COLUMNS"]
                )
        self.assertEqual(tables("### Help\n\nText.", "| Path | Purpose | Owner |"), [])

    def test_the_navigation_section_is_the_current_paths_h3(self) -> None:
        navigation = self.registry.readme_navigation.profiles[ROOT_FORM[0]]
        self.assertEqual(
            (navigation.section, navigation.complete), ("Current Paths", False)
        )


class StageReadmeFormTests(unittest.TestCase):
    """SPEC-0173: the Stage README form, its Index table and its navigation."""

    HOME = "### Paths\n\nText."
    HEADER = ("Path", "Purpose")
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
                headings = CONTRACTS.heading_contract(self.by_id[profile_id])
                self.assertEqual(headings.required, titles)
                self.assertEqual(headings.allowed, titles)

    def test_a_complete_body_passes_and_an_old_h2_fails_the_tree(self) -> None:
        for profile_id in STAGE_FORM[::2]:
            with self.subTest(profile=profile_id):
                self.assertEqual(self.tree(profile_id, self.BODY), [])
                deeper = self.BODY.replace(
                    "### Owners\n\nText.",
                    "### Owners\n\nText.\n\n#### Matrix\n\nText.",
                )
                self.assertEqual(self.tree(profile_id, deeper), [])
                self.assertNotEqual(
                    self.tree(profile_id, self.BODY + "\n## Structure\n\nText.\n"), []
                )
                self.assertIn(
                    "BODY-H3-REQUIRED",
                    self.tree(
                        profile_id,
                        self.BODY.replace("### Paths", "#### Paths"),
                    ),
                )

    def test_the_index_table_accepts_its_registered_columns(self) -> None:
        for profile_id in STAGE_FORM[::2]:
            for header in (self.HEADER,):
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
                ("Purpose", "Path"),
                (*self.HEADER, "Owner"),
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

    def test_the_table_is_read_in_its_core_h2_and_not_outside(self) -> None:
        # SPEC-0222: the core table belongs to Current Contents, so an Owners
        # table is read and a Usage table is not.
        inside = self.with_table("| Path |", "| --- |", "| a |", home="### Owners")
        wrong = self.with_table("| Path |", "| --- |", "| a |", home="### Entry Points")
        for profile_id in STAGE_FORM[::2]:
            with self.subTest(profile=profile_id):
                self.assertEqual(
                    self.tables(profile_id, inside), ["BODY-TABLE-COLUMNS"]
                )
                self.assertEqual(self.tables(profile_id, wrong), [])

    def test_the_navigation_section_is_the_paths_h3(self) -> None:
        for profile_id in STAGE_FORM[::2]:
            navigation = self.registry.readme_navigation.profiles[profile_id]
            with self.subTest(profile=profile_id):
                self.assertEqual(
                    (navigation.section, navigation.complete), ("Paths", True)
                )


class ServiceReadmeFormTests(unittest.TestCase):
    """SPEC-0174: the Service README form, its Commands table and navigation."""

    HOME = "### Readiness\n\nText."
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
                headings = CONTRACTS.heading_contract(self.by_id[profile_id])
                self.assertEqual(headings.required, titles)
                self.assertEqual(headings.allowed, titles)

    def test_a_complete_body_passes_and_an_old_h2_fails_the_tree(self) -> None:
        for profile_id in SERVICE_FORM[::2]:
            with self.subTest(profile=profile_id):
                self.assertEqual(self.tree(profile_id, self.BODY), [])
                deeper = self.BODY.replace(
                    "### Purpose\n\nText.",
                    "### Purpose\n\nText.\n\n#### Matrix\n\nText.",
                )
                self.assertEqual(self.tree(profile_id, deeper), [])
                self.assertNotEqual(
                    self.tree(profile_id, self.BODY + "\n## Structure\n\nText.\n"), []
                )
                self.assertIn(
                    "BODY-H3-REQUIRED",
                    self.tree(
                        profile_id,
                        self.BODY.replace("### Readiness", "#### Readiness"),
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
            "| Command |", "| --- |", "| a |", home="### Selected Start"
        )
        for profile_id in SERVICE_FORM[::2]:
            with self.subTest(profile=profile_id):
                self.assertEqual(self.tables(profile_id, wrong), [])

    def test_the_interface_table_is_read_in_the_service_h2(self) -> None:
        header = "| Interface | Producer | Consumer | Contract | Failure |"
        delimiter = "| --- | --- | --- | --- | --- |"
        row = "| `api` | p | c | [contract](c.md) | f |"
        for profile_id in SERVICE_FORM[::2]:
            for home in ("### Interfaces\n\nText.", "### Purpose\n\nText."):
                with self.subTest(profile=profile_id, home=home):
                    ok = self.with_table(header, delimiter, row, home=home)
                    self.assertEqual(self.tables(profile_id, ok), [])
                    relabeled = self.with_table(
                        header.replace("Failure", "Failure mode"),
                        delimiter,
                        row,
                        home=home,
                    )
                    self.assertEqual(
                        self.tables(profile_id, relabeled), ["BODY-TABLE-COLUMNS"]
                    )
            # A document without an external interface renders no table.
            self.assertEqual(self.tables(profile_id, self.BODY), [])

    def test_the_navigation_section_is_the_purpose_h3(self) -> None:
        navigation = self.registry.readme_navigation.profiles[SERVICE_FORM[0]]
        self.assertEqual((navigation.section, navigation.complete), ("Purpose", False))
        self.assertNotIn(SERVICE_FORM[2], self.registry.readme_navigation.profiles)


class TableIteratorTests(unittest.TestCase):
    def test_only_root_rendered_tables_can_supply_form_evidence(self) -> None:
        hidden = "| Example |\n| --- |\n| Opaque |"
        visible = "| Outcome |\n| --- |\n| Observed |"
        for example in (
            f"<pre>\n{hidden}\n</pre>",
            f"<![CDATA[\n```\n{hidden}\n]]>",
            "\n".join("> " + line for line in hidden.splitlines()),
            "- Example\n\n" + "\n".join("  " + line for line in hidden.splitlines()),
        ):
            with self.subTest(example=example):
                text = example + "\n\n" + visible
                expected = (["Outcome"], [["Observed"]])
                self.assertEqual(list(MARKDOWN._visible_tables(text)), [expected])
                self.assertEqual(LINKS._first_visible_table(text), expected)

    def test_the_link_reader_uses_the_rendered_root_heading(self) -> None:
        text = "<pre>\n## Scope\nFake.\n</pre>\n\n## Scope\n\nActual.\n"
        expected = "\nActual."
        self.assertEqual(MARKDOWN._exact_heading_section(text, "## Scope"), expected)
        self.assertEqual(LINKS._exact_heading_section(text, "## Scope"), expected)

    def test_opaque_markup_does_not_hide_subsequent_author_prompts(self) -> None:
        text = "<pre>\n```\n</pre>\n\n<!-- Author prompt: fill this in -->\n"
        self.assertIn(
            "<!-- Author prompt: fill this in -->",
            MARKDOWN.text_outside_fenced_code(text),
        )

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
RUNBOOK_STEPS = (
    "| Step | Action | Expected Result | On Failure |\n"
    "| --- | --- | --- | --- |\n| 1 | Restart | Ready | Stop and call the owner |"
)
RUNBOOK_BODY = md(
    "# Runbook title",
    "## Trigger and Scope",
    "### Trigger\n\nAn alert starts it.",
    "### Targets\n\nOne service.",
    "## Preflight",
    "### Authority\n\nOwner approval.",
    "### Environment\n\nBackup exists.",
    "## Procedure",
    "### Steps\n\nRun it.",
    "### Stop Conditions\n\nStop on error.",
    "## Verification",
    "### Expected Results\n\nRead the status.",
    "### Unverified Conditions\n\nNone recorded.",
    "## Escalation",
    "### Next Owner\n\nCall the owner.",
    "### Recovery or Forward Repair\n\nUndo step 1.",
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
                headings = CONTRACTS.heading_contract(by_id[profile_id])
                self.assertEqual(headings.required, titles)
                self.assertEqual(headings.allowed, titles)
                self.assertFalse(headings.substantive_body)
                self.assertFalse(headings.ordered)

    def test_the_loader_copies_the_runbook_tables_to_the_source_profile(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        by_id = {profile.profile_id: profile for profile in registry.profiles}
        twin, source = by_id[RUNBOOK[1]], by_id[RUNBOOK[0]]
        self.assertEqual(source.tables, twin.tables)
        steps, lifecycle = twin.tables
        self.assertEqual(
            (steps.name, steps.section, steps.minimum_rows, steps.row_identity),
            ("Steps", "runbook.procedure", 0, "Step"),
        )
        self.assertEqual(
            [column.key for column in steps.columns], list(CORE_STEP_COLUMNS)
        )
        self.assertEqual(
            [column.key for column in lifecycle.columns],
            list(RUNBOOK_TABLE_KEYS["Lifecycle Traceability"][1]),
        )
        self.assertTrue(all(column.required for column in steps.columns))

    def test_the_repository_runbook_registry_is_valid_and_its_twin_matches(
        self,
    ) -> None:
        self.assertEqual(rules_of(load_raw()), set())
        REGISTRY_CHECK._assert_template_source_parity(CONTRACTS.load_registry(ROOT))

    def test_a_complete_runbook_passes_the_tree(self) -> None:
        self.assertEqual(self.tree(RUNBOOK_BODY), [])

    def test_recovery_or_forward_repair_is_required_as_the_core_states(self) -> None:
        without = RUNBOOK_BODY.replace(
            "\n\n### Recovery or Forward Repair\n\nUndo step 1.", ""
        )
        self.assertNotIn("Recovery or Forward Repair", without)
        self.assertNotEqual(self.tree(without), [])

    def test_a_steps_table_passes_when_it_keeps_the_core_columns(
        self,
    ) -> None:
        body = RUNBOOK_BODY.replace("Run it.", "Run it.\n\n" + RUNBOOK_STEPS)
        self.assertEqual(self.tables(body), [])

    def test_a_header_only_steps_table_passes_because_the_minimum_is_zero(
        self,
    ) -> None:
        header_only = "| Step | Action | Expected Result | On Failure |\n| --- | --- | --- | --- |"
        self.assertEqual(self.tables(RUNBOOK_BODY.replace("Run it.", header_only)), [])
        self.assertEqual(self.tables(RUNBOOK_BODY), [])

    def test_a_reordered_relabeled_or_missing_steps_column_fails(self) -> None:
        for header in (
            "| Step | Expected Result | Action | On Failure |",
            "| Step | Action | Expected Result |",
            "| Step | Action | Expected Result | On Failure | Note |",
            "| Step | Action | Expected result | Stop / escalate when |",
        ):
            cells = header.count("|") - 1
            table = f"{header}\n" + "| --- " * cells + "|\n" + "| a " * cells + "|"
            with self.subTest(header=header):
                self.assertEqual(
                    self.tables(RUNBOOK_BODY.replace("Run it.", table)),
                    ["BODY-TABLE-COLUMNS"],
                )

    def test_a_steps_table_outside_procedure_is_not_looked_at(self) -> None:
        wrong = "| Step | Action |\n| --- | --- |\n| a | b |"
        self.assertEqual(
            self.tables(RUNBOOK_BODY.replace("Read the status.", wrong)), []
        )
        inside = RUNBOOK_BODY.replace("Stop on error.", wrong)
        self.assertEqual(self.tables(inside), ["BODY-TABLE-COLUMNS"])

    def test_recovery_procedures_is_accepted_under_recovery(self) -> None:
        block = "### Recovery Procedures\n\nRestore the replica from the snapshot."
        self.assertEqual(self.tree(self.under("", block)), [])
        before_rollback = RUNBOOK_BODY.replace(
            "### Next Owner\n\nCall the owner.",
            "### Next Owner\n\nCall the owner.\n\n" + block,
        )
        self.assertLess(
            before_rollback.index("### Recovery Procedures"),
            before_rollback.index("### Recovery or Forward Repair"),
        )
        self.assertEqual(self.tree(before_rollback), [])

    def test_recovery_procedures_under_another_h2_is_refused(self) -> None:
        block = "### Recovery Procedures\n\nRestore the replica."
        self.assertEqual(
            self.tree(self.under("## Verification", block)), ["BODY-H3-PARENT"]
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
        self.assertEqual(self.tree(self.under("## Escalation", block)), [])
        self.assertEqual(
            self.tree(self.under("## Procedure", block)), ["BODY-H3-PARENT"]
        )


INCIDENT_PATH = PurePosixPath(
    "docs/05.operations/incidents/2026/inc-0001-example/incident.md"
)
INCIDENT_BODY = md(
    "# Incident title",
    "## Impact",
    "### Affected Users\n\nOne team.",
    "### Observed Scope\n\nSEV-2 for one hour.",
    "#### Event\n\n| Field | Value |\n| --- | --- |\n| Severity | SEV-2 |",
    "#### Current Status\n\nInvestigating.",
    "## Response",
    "### Timeline\n\nThe alert fired.",
    "#### Decisions\n\nThe commander chose rollback.",
    "### Actions\n\nRolled back.",
    "## Resolution",
    "### Verified State\n\nChecks pass.",
    "### Remaining Work\n\nA Task owner.",
    "#### Evidence Sources\n\nA log link.",
)
POSTMORTEM_PATH = PurePosixPath(
    "docs/05.operations/incidents/2026/inc-0001-example/postmortem.md"
)
POSTMORTEM_BODY = md(
    "# Postmortem title",
    "## Facts",
    "### Timeline\n\nIncident INC-0001 as recorded in the incident folder.",
    "#### Review Scope\n\nThe whole event.",
    "### Impact\n\nOne team.",
    "#### Detection and Response\n\nAn alert fired.",
    "## Causes",
    "### Contributing Factors\n\nNo canary.",
    "#### Causal Analysis\n\nA bad rollout.",
    "### Uncertainty\n\nNone: no open question remains.",
    "## Actions",
    "### Prevention\n\nAdd a canary.",
    "### Owners and Checks\n\nThe canary catches it.",
    "#### Source Records\n\nA log link.",
    "#### Review Decision\n\nApproved.",
)


class RoleFormBody(unittest.TestCase):
    """Shared checks for a role form; each subclass names its form and body."""

    PATH: PurePosixPath
    PROFILES: tuple[str, str]
    FORM_ID: str
    TREE: tuple
    TABLE_KEYS: dict
    BODY: str
    HEADER: tuple[str, ...]  # its required columns, in order
    OPTIONAL: tuple[str, ...] = ()  # its optional trailing columns, in order
    ALL_OPTIONAL: tuple[str, ...] | None = None  # every table's, when it differs
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
                headings = CONTRACTS.heading_contract(by_id[profile_id])
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
        self.assertEqual(
            tuple(c.key for t in twin.tables for c in t.columns if not c.required),
            self.OPTIONAL if self.ALL_OPTIONAL is None else self.ALL_OPTIONAL,
        )

    def test_the_repository_registry_is_valid_and_its_twin_matches(self) -> None:
        self.assertEqual(rules_of(load_raw()), set())
        REGISTRY_CHECK._assert_template_source_parity(CONTRACTS.load_registry(ROOT))

    def test_a_complete_document_passes_the_tree(self) -> None:
        self.assertEqual(self.tree(self.BODY), [])
        self.assertEqual(self.tables(self.BODY), [])


class RoleFormTableBody(RoleFormBody):
    """Shared checks for a role form that carries a table."""

    @classmethod
    def setUpClass(cls) -> None:
        if cls is RoleFormTableBody:
            raise unittest.SkipTest("shared base; its subclasses run the checks")
        super().setUpClass()

    def test_the_optional_table_passes_with_the_registered_columns(self) -> None:
        row = tuple("x" for _ in self.HEADER)
        body = self.with_table(self.table(self.HEADER, row))
        self.assertEqual(self.tables(body), [])
        self.assertEqual(self.tree(body), [])

    def test_a_header_only_table_passes_because_the_minimum_is_zero(self) -> None:
        self.assertEqual(self.tables(self.with_table(self.table(self.HEADER))), [])

    def test_a_reordered_missing_or_extra_column_fails(self) -> None:
        first, second, third, *rest = self.HEADER
        for header in (
            (first, third, second, *rest),
            self.HEADER[:-1],
            (*self.HEADER, *self.OPTIONAL, "Note"),
        ):
            table = self.table(header, tuple("x" for _ in header))
            with self.subTest(header=header):
                self.assertEqual(
                    self.tables(self.with_table(table)), ["BODY-TABLE-COLUMNS"]
                )

    def test_the_optional_trailing_columns_may_be_present_or_omitted(self) -> None:
        full = (*self.HEADER, *self.OPTIONAL)
        for header in {self.HEADER, full}:
            table = self.table(header, tuple("x" for _ in header))
            with self.subTest(header=header):
                self.assertEqual(self.tables(self.with_table(table)), [])
        if self.OPTIONAL:
            wrong = (self.HEADER[0], *self.OPTIONAL, *self.HEADER[1:])
            table = self.table(wrong, tuple("x" for _ in wrong))
            self.assertEqual(
                self.tables(self.with_table(table)), ["BODY-TABLE-COLUMNS"]
            )

    def test_the_table_is_not_looked_at_outside_its_section(self) -> None:
        wrong = self.table(self.HEADER[:2], ("a", "b"))
        body = self.with_table(wrong, home="#### Source Records")
        self.assertEqual(self.tables(body), [])


class IncidentFormTests(RoleFormTableBody):
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

    def test_the_core_actions_table_belongs_to_the_response_section(self) -> None:
        # SPEC-0222: incident.actions sits under Response > Actions.
        core = self.table(CORE_ACTION_COLUMNS, ("Roll back", "Ops", "Alert", "none"))
        body = self.with_table(core, home="Rolled back.")
        self.assertEqual(self.tables(body), [])
        self.assertEqual(self.tree(body), [])
        old = self.table(("Action", "Owner", "Verification"), ("a", "b", "c"))
        self.assertEqual(
            self.tables(self.with_table(old, home="Rolled back.")),
            ["BODY-TABLE-COLUMNS"],
        )
        self.assertEqual(self.tables(self.with_table(old, home="Checks pass.")), [])

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
            self.tree(self.under("## Resolution", block)), ["BODY-H3-PARENT"]
        )


class PostmortemFormTests(RoleFormTableBody):
    """SPEC-0171 VAL-INCIDENTFORM-001: the Postmortem form, tables and extensions."""

    PATH = POSTMORTEM_PATH
    PROFILES = POSTMORTEM
    FORM_ID = "postmortem"
    TREE = POSTMORTEM_TREE
    TABLE_KEYS = POSTMORTEM_TABLE_KEYS
    BODY = POSTMORTEM_BODY
    HEADER = CORE_ACTION_COLUMNS
    HOME = "Add a canary."

    def test_the_table_is_not_looked_at_outside_its_section(self) -> None:
        # SPEC-0222: the core table belongs to the whole Actions H2.
        wrong = self.table(self.HEADER[:2], ("a", "b"))
        self.assertEqual(self.tables(self.with_table(wrong, home="No canary.")), [])
        inside = self.with_table(wrong, home="#### Source Records")
        self.assertEqual(self.tables(inside), ["BODY-TABLE-COLUMNS"])

    WELL = "### What Went Well\n\nThe alert fired within a minute."

    def test_what_went_well_is_accepted_under_impact(self) -> None:
        self.assertEqual(self.tree(self.under("## Causes", self.WELL)), [])
        after_detection = POSTMORTEM_BODY.replace(
            "## Causes", self.WELL + "\n\n## Causes"
        )
        self.assertLess(
            after_detection.index("### Detection and Response"),
            after_detection.index("### What Went Well"),
        )

    def test_what_went_well_under_another_h2_is_refused(self) -> None:
        for heading in ("## Actions", "### Owners and Checks"):
            with self.subTest(before=heading):
                self.assertEqual(
                    self.tree(self.under(heading, self.WELL)), ["BODY-H3-PARENT"]
                )
        self.assertEqual(self.tree(self.under("", self.WELL)), ["BODY-H3-PARENT"])

    def test_an_absent_what_went_well_passes_and_an_empty_one_fails(self) -> None:
        self.assertNotIn("What Went Well", POSTMORTEM_BODY)
        self.assertEqual(self.tree(POSTMORTEM_BODY), [])
        empty = self.under("## Causes", "### What Went Well\n")
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
        self.assertEqual(self.tree(self.under("", block)), [])
        self.assertEqual(self.tree(self.under("## Actions", block)), ["BODY-H3-PARENT"])


GOVERNANCE_POLICY_PATH = PurePosixPath(".agents/governance/agent-execution.md")
OPERATIONS_POLICY_PATH = PurePosixPath(
    "docs/05.operations/policies/0001-k8s-gitops-operations-policy.md"
)


def policy_body() -> str:
    return md(
        "# Policy title",
        "## Purpose and Scope",
        "### Objective\n\nKeep changes reviewable.",
        "### Applies To\n\nEvery change.",
        "#### Exclusions\n\nNone: nothing is excluded.",
        "## Rules",
        "### Requirements\n\nReview every change.",
        "### Exceptions\n\nNone: no exception exists.",
        "#### Approval and Review\n\nThe owner approves.",
        "## Enforcement",
        "### Mechanisms\n\nCI checks it.",
        "### Limits\n\nCI cannot see a manual change.",
        "## Ownership",
        "### Owner\n\nPlatform owns this policy.",
        "#### Responsibilities\n\nPlatform.",
        "### Review Triggers\n\nChanges follow the Spec.",
    )


class GovernancePolicyFormTests(RoleFormTableBody):
    """SPEC-0175 VAL-POLICY-001: the Policy form on governance rules."""

    PATH = GOVERNANCE_POLICY_PATH
    PROFILES = POLICY_GOVERNANCE
    FORM_ID = "policy"
    TREE = POLICY_TREE
    TABLE_KEYS = POLICY_GOVERNANCE_TABLE_KEYS
    BODY = policy_body()
    HEADER = POLICY_RULES_COLUMNS
    ALL_OPTIONAL = POLICY_RULES_OPTIONAL
    HOME = "Review every change."

    def tables(self, text: str) -> list[str]:
        # SPEC-0222: the rule check owns both rule tables of an authored policy, so
        # the generic table check is read on the template twin.
        twin = typed_profiles(load_raw())[self.PROFILES[1]]
        return sorted(
            item.rule_id for item in MARKDOWN._table_diagnostics(self.PATH, twin, text)
        )

    def test_the_loader_copies_the_tables_to_the_source_profile(self) -> None:
        super().test_the_loader_copies_the_tables_to_the_source_profile()
        self.assertIsNone(typed_profiles(load_raw())[self.PROFILES[0]].body_contract)

    def test_the_table_is_not_looked_at_outside_its_section(self) -> None:
        wrong = self.table(self.HEADER[:2], ("a", "b"))
        body = self.with_table(wrong, home="Platform owns this policy.")
        self.assertEqual(self.tables(body), [])


class OperationsPolicyFormTests(RoleFormTableBody):
    """SPEC-0175 VAL-POLICY-001: the Policy form on operations policies."""

    PATH = OPERATIONS_POLICY_PATH
    PROFILES = POLICY_OPERATIONS
    FORM_ID = "policy"
    TREE = POLICY_TREE
    TABLE_KEYS = POLICY_OPERATIONS_TABLE_KEYS
    BODY = policy_body()
    HEADER = POLICY_RULES_COLUMNS
    ALL_OPTIONAL = POLICY_RULES_OPTIONAL
    HOME = "Review every change."

    def tables(self, text: str) -> list[str]:
        # SPEC-0222: the rule check owns both rule tables of an authored policy, so
        # the generic table check is read on the template twin.
        twin = typed_profiles(load_raw())[self.PROFILES[1]]
        return sorted(
            item.rule_id for item in MARKDOWN._table_diagnostics(self.PATH, twin, text)
        )

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
            body.index("### Review Triggers"),
            body.index("### Lifecycle Traceability"),
        )
        self.assertEqual(self.tree(body), [])
        self.assertEqual(self.tables(body), [])

    def test_lifecycle_traceability_under_another_h2_is_refused(self) -> None:
        for heading in ("## Rules", "## Enforcement", "## Ownership"):
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


AGENTS_PATH = PurePosixPath("scripts/AGENTS.md")


def agents_body() -> str:
    return md(
        "# AGENTS.md",
        "Agent instructions for `scripts/`.",
        "## Scope",
        "### Allowed Scope\n\nValidators only.",
        "#### Non-goals\n\nThis folder adds no non-goal beyond the parent "
        "`AGENTS.md`; if work here must be excluded, state it here.",
        "### Instruction Precedence",
        "#### Canonical Sources\n\nThe quality policy.",
        "## Workflow",
        "### Intake",
        "#### Local Obligations\n\n1. Keep the change small.",
        "### Execution\n\nFollow the rules above.",
        "## Boundaries",
        "### Authority",
        "#### Stop and Escalate\n\nStop on a failed check.",
        "### Secrets and External Effects",
        "#### Protected Actions\n\nNone beyond the policy.",
        "## Verification",
        "### Checks\n\nRun the suite.",
        "### Reporting",
        "#### Evidence and Limits\n\nRepository-static only.",
        "#### Handoff\n\nThis folder hands off through the work lifecycle's "
        "Completion steps with no extra field; if it needs one, state it here.",
    )


# SPEC-0222 WORK-007: the agent-instructions core members the form carries.
AGENTS_CORE_IDS = (
    "agent-instructions.scope",
    "agent-instructions.scope.1",
    "agent-instructions.scope.2",
    "agent-instructions.workflow",
    "agent-instructions.workflow.1",
    "agent-instructions.workflow.2",
    "agent-instructions.limits",
    "agent-instructions.limits.1",
    "agent-instructions.limits.2",
    "agent-instructions.verification",
    "agent-instructions.verification.1",
    "agent-instructions.verification.2",
)
AGENTS_CORE_H2 = {
    "agent-instructions.scope": ("실행 범위", "작업 경로·우선권·허용 행동"),
    "agent-instructions.workflow": ("절차", "필요 정책·계획·브리핑"),
    "agent-instructions.limits": ("제한", "권한·실패·중단"),
    "agent-instructions.verification": ("완료", "관련 검사와 보고"),
}


class AgentsFormTests(RoleFormBody):
    """SPEC-0176 VAL-AGENTS-001: the AGENTS form on every AGENTS.md; SPEC-0222
    WORK-007 binds it to the agent-instructions core tree."""

    PATH = AGENTS_PATH
    PROFILES = AGENTS
    FORM_ID = "agents"
    TREE = AGENTS_TREE
    TABLE_KEYS = AGENTS_TABLE_KEYS
    BODY = agents_body()

    def test_the_form_binds_the_agent_instructions_core(self) -> None:
        form = next(
            f for f in load_raw()["common_forms"]["forms"] if f["form_id"] == "agents"
        )
        self.assertEqual(form["core_role"], "agent-instructions")
        core = form["core"]
        self.assertEqual(core["purpose"], "허용 범위의 도구 독립 실행 규칙")
        self.assertEqual(core["non_goals"], "다른 역할의 상태·정책 정본 대체")
        self.assertEqual(core["tables"], [])
        self.assertEqual(core["status"], "DESIGN_PROPOSAL_NOT_ADOPTED")
        self.assertEqual(core["metadata_policy"]["envelope"], "native")
        self.assertEqual(
            core["rules"],
            [
                "single-meaning-owner",
                "no-synthetic-evidence",
                "no-release-document-role",
                "no-package-path-runtime-dependency",
            ],
        )
        nodes = [n for s in form["sections"] for n in (s, *s["children"])]
        self.assertEqual(tuple(n["section_id"] for n in nodes), AGENTS_CORE_IDS)
        for node in nodes:
            with self.subTest(section=node["section_id"]):
                self.assertEqual(node["condition"], "always")
                self.assertEqual(node["core"]["required_when"], "always")
                if node["level"] == 2:
                    self.assertEqual(
                        (node["core"]["title_ko"], node["core"]["content_rule"]),
                        AGENTS_CORE_H2[node["section_id"]],
                    )
                else:
                    self.assertEqual(node["core"]["title_ko"], node["title"])
                    self.assertIn(node["title"], node["core"]["content_rule"])

    def test_the_template_carries_no_table(self) -> None:
        twin = profile_of(load_raw(), self.PROFILES[1])
        self.assertEqual(twin["template_definition"]["tables"], [])
        template = (ROOT / twin["template_source"]).read_text(encoding="utf-8")
        self.assertNotIn("|", template)

    def test_the_loaded_heading_lists_equal_the_form_h2_titles(self) -> None:
        # The AGENTS profiles stay native: they carry no H2 lists, so an empty
        # section is a review matter, not a BODY-SECTION-EMPTY diagnostic.
        registry = CONTRACTS.load_registry(ROOT)
        loaded = next(f for f in registry.common_forms if f.form_id == self.FORM_ID)
        self.assertEqual(
            tuple(item.title for item in loaded.sections),
            tuple(title for title, _ in self.TREE),
        )
        by_id = {profile.profile_id: profile for profile in registry.profiles}
        for profile_id in self.PROFILES:
            with self.subTest(profile=profile_id):
                raw = profile_of(load_raw(), profile_id)
                self.assertNotIn("sections", raw)
                self.assertIs(by_id[profile_id].form, loaded)

    def test_the_profiles_are_native_and_the_template_is_exact(self) -> None:
        raw = load_raw()
        folder, twin = (profile_of(raw, profile_id) for profile_id in self.PROFILES)
        self.assertEqual(folder["mode"], "native")
        self.assertEqual(folder["frontmatter"]["mode"], "absent")
        self.assertEqual(
            folder["template_source"],
            "docs/99.templates/templates/common/agents.template.md",
        )
        self.assertEqual(twin["mode"], "template")
        self.assertEqual(twin["frontmatter"]["mode"], "absent")
        self.assertEqual(twin["placeholder_policy"], "template-only")
        self.assertEqual(
            twin["relationships"]["source_profile_ids"], [self.PROFILES[0]]
        )
        self.assertEqual(
            twin["path_pattern"],
            "^docs/99\\.templates/templates/common/agents\\.template\\.md$",
        )

    def test_the_form_has_no_extension_and_no_body_section(self) -> None:
        form = next(
            f for f in load_raw()["common_forms"]["forms"] if f["form_id"] == "agents"
        )
        self.assertEqual(form["extensions"], [])
        for profile_id in self.PROFILES:
            self.assertIsNone(
                profile_of(load_raw(), profile_id)["relationships"]["body_contract"]
            )

    def test_the_root_and_every_folder_file_resolve_to_the_agents_profile(
        self,
    ) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        for path in (
            "AGENTS.md",
            "scripts/AGENTS.md",
            "docs/03.specs/AGENTS.md",
            "examples/azure/AGENTS.md",
        ):
            with self.subTest(path=path):
                profile = CONTRACTS.classify_path(registry, PurePosixPath(path))
                self.assertEqual(profile.profile_id, AGENTS[0])
                self.assertEqual(profile.document_role, "agents")
        self.assertEqual(
            CONTRACTS.classify_path(registry, PurePosixPath("CLAUDE.md")).profile_id,
            "common/root-provider-shim",
        )
        self.assertIsNone(
            CONTRACTS.classify_path(registry, PurePosixPath("CLAUDE.md")).document_role
        )
        self.assertEqual(
            CONTRACTS.classify_path(
                registry, PurePosixPath("scripts/CLAUDE.md")
            ).profile_id,
            "common/folder-claude-import",
        )

    def test_the_archive_has_no_agents_profile(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        try:
            profile = CONTRACTS.classify_path(
                registry, PurePosixPath("docs/98.archive/AGENTS.md")
            )
        except CONTRACTS.DocumentContractError:
            return
        self.assertNotEqual(profile.profile_id, AGENTS[0])

    def test_a_missing_or_renamed_form_heading_fails_the_tree(self) -> None:
        self.assertEqual(
            self.tree(self.BODY.replace("### Reporting", "### Report")),
            ["BODY-H3-REQUIRED", "BODY-H3-UNSUPPORTED"],
        )
        self.assertEqual(
            self.tree(self.BODY.replace("### Checks\n", "### Checks\n\n#### Deep\n")),
            [],
        )
        self.assertEqual(
            self.tree(self.under("## Verification", "### Stray\n\nText.")),
            ["BODY-H3-UNSUPPORTED"],
        )

    def test_a_former_form_heading_is_refused_as_an_h3(self) -> None:
        for old, new in (
            ("### Allowed Scope", "### Allowed Surface"),
            ("#### Local Obligations", "### Local Obligations"),
            ("## Boundaries", "## Safety"),
        ):
            with self.subTest(heading=new):
                self.assertNotEqual(self.tree(self.BODY.replace(old, new)), [])


GOVERNANCE_SKILL_PATH = PurePosixPath(".agents/workflows/work-lifecycle.md")
NATIVE_SKILL_PATH = PurePosixPath(".agents/skills/example/SKILL.md")
SKILL_AUTHORITY = "### Authority Boundary\n\nThis procedure applies existing policy."


class BareSectionTests(unittest.TestCase):
    """SPEC-0182 VAL-EMPTY-001: BODY-SECTION-BARE refuses a bare statement."""

    NONE = "None is stated in this document."
    KOREAN = "이 README에는 분류 표가 없다."

    @classmethod
    def setUpClass(cls) -> None:
        profiles = typed_profiles(load_raw())
        cls.native = profiles[AGENTS[0]]
        cls.template = profiles[AGENTS[1]]
        cls.no_form = profiles["common/native-changelog"]

    def found(self, text: str, profile=None) -> list[str]:
        profile = profile or self.native
        return sorted(
            item.rule_id
            for item in MARKDOWN._body_diagnostics(AGENTS_PATH, profile, text, "active")
        )

    def with_line(self, line: str, heading: str = "### Execution") -> str:
        body = agents_body()
        start = body.index(heading) + len(heading)
        end = body.index("\n\n##", start)
        return body[:start] + "\n\n" + line + body[end:]

    def test_each_bare_shape_fails(self) -> None:
        for line in (
            self.NONE,
            "This file states no separate handoff rule.",
            "This policy marks no subject as excluded from its scope.",
            "This skill states no failure branch of its own.",
            self.KOREAN,
            "이 문서에는 runbook이나 링크가 없다.",
            "이 정책에는 예외 조건, 승인 단계가 없다.",
        ):
            with self.subTest(line=line):
                self.assertEqual(
                    self.found(self.with_line(line)), ["BODY-SECTION-BARE"]
                )

    def test_an_explained_none_passes(self) -> None:
        for line in (
            "This folder hands off through the work lifecycle's Completion steps "
            "with no extra field; if it needs one, state it here.",
            "This file states no separate handoff rule; it is a provider gateway.",
            "이 문서는 분류 표를 따로 두지 않는다. 분류 표를 두게 되면 여기에 둔다.",
            "이 디렉터리는 라우터이며 로컬 작업 절차가 없다.",
            "이 정책은 예외가 없으므로 별도 승인이 없다.",
        ):
            with self.subTest(line=line):
                self.assertEqual(self.found(self.with_line(line)), [])

    def test_a_pointer_passes(self) -> None:
        line = "Handoff is stated in rules 3 and 5 under Local Obligations."
        self.assertEqual(self.found(self.with_line(line)), [])

    def test_a_reworded_bare_statement_passes_which_is_the_stated_limit(self) -> None:
        line = "Nothing is stated here."
        self.assertEqual(self.found(self.with_line(line)), [])

    def test_a_statement_with_more_than_one_line_or_in_code_passes(self) -> None:
        self.assertEqual(self.found(self.with_line(self.NONE + "\n\nMore.")), [])
        self.assertEqual(self.found(self.with_line("```\n" + self.NONE + "\n```")), [])

    def test_a_template_and_a_role_without_a_form_are_not_checked(self) -> None:
        body = self.with_line(self.NONE)
        self.assertEqual(self.found(body, self.template), [])
        self.assertEqual(self.found(self.NONE, self.no_form), [])

    def test_the_agents_fixture_carries_only_explained_lines(self) -> None:
        self.assertEqual(self.found(agents_body()), [])


def skill_body(*, preface: str = "") -> str:
    blocks = (
        "# Skill title",
        "## Trigger",
        "### When to Use\n\nUse it when a change needs review.",
        "### When Not to Use\n\nNot for a one-line fix.",
        "## Procedure",
        "### Steps\n\n1. Run the check.",
        "### Failure Handling\n\nStop on a failed check.",
        "## Outputs",
        "### Artifacts\n\nA report.",
        "### Handoff\n\nRecord the result.",
        "## Verification",
        "### Checks\n\nRun the suite.",
        "### Limits\n\nThe suite does not prove live state.",
    )
    return md(*((preface,) if preface else ()), *blocks)


# TestCase is named again so the static collector sees a runnable base.
class SkillFormBody(RoleFormTableBody, unittest.TestCase):
    """Shared Skill checks; the two Skill profile pairs share one form."""

    FORM_ID = "skill"
    TREE = SKILL_TREE
    TABLE_KEYS = SKILL_TABLE_KEYS
    BODY = skill_body()
    HEADER = ("Step", "Input", "Output")
    HOME = "1. Run the check."

    @classmethod
    def setUpClass(cls) -> None:
        if cls is SkillFormBody:
            raise unittest.SkipTest("shared base; its subclasses run the checks")
        super().setUpClass()

    def test_the_table_is_not_looked_at_outside_its_section(self) -> None:
        wrong = self.table(self.HEADER[:2], ("a", "b"))
        body = self.with_table(wrong, home="A report.")
        self.assertEqual(self.tables(body), [])

    def test_the_table_keys_are_the_step_input_output_columns(self) -> None:
        raw = profile_of(load_raw(), self.PROFILES[1])
        (table,) = raw["template_definition"]["tables"]
        self.assertEqual(table["section"], "skill.procedure.1")
        self.assertEqual(table["row_identity"], "Step")
        self.assertEqual(table["minimum_rows"], 0)
        self.assertEqual(
            [(c["key"], c["required"]) for c in table["columns"]],
            [("Step", True), ("Input", True), ("Output", True)],
        )

    def test_the_form_has_one_local_extension_and_no_body_section(self) -> None:
        form = next(
            f for f in load_raw()["common_forms"]["forms"] if f["form_id"] == "skill"
        )
        self.assertEqual(form["extensions"], [SKILL_EXTENSION])
        for profile_id in self.PROFILES:
            self.assertIsNone(
                profile_of(load_raw(), profile_id)["relationships"]["body_contract"]
            )

    def test_the_template_twin_names_every_real_consumer(self) -> None:
        twin = profile_of(load_raw(), self.PROFILES[1])
        paths = twin["template_definition"]["consumer_paths"]
        self.assertEqual(len(paths), len(set(paths)))
        for path in paths:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file())
        self.assertIn(twin["template_source"], paths)

    def test_a_missing_or_renamed_form_heading_fails_the_tree(self) -> None:
        self.assertEqual(
            self.tree(self.BODY.replace("### Checks", "### Tests")),
            ["BODY-H3-REQUIRED", "BODY-H3-UNSUPPORTED"],
        )
        self.assertEqual(
            self.tree(self.BODY.replace("## Procedure", "## Workflow Steps")),
            [
                "BODY-H3-PARENT",
                "BODY-H3-PARENT",
                "BODY-HEADING-REQUIRED",
                "BODY-HEADING-UNSUPPORTED",
            ],
        )
        self.assertEqual(
            self.tree(self.under("## Verification", "### Stray\n\nText.")),
            ["BODY-H3-UNSUPPORTED"],
        )

    def test_deeper_headings_stay_inside_their_form_h3(self) -> None:
        body = self.BODY.replace(
            "Stop on a failed check.", "Stop.\n\n#### Deep\n\nDetail.\n\n##### Deeper"
        )
        self.assertEqual(self.tree(body), [])

    def test_authority_boundary_is_accepted_after_when_not_to_use(self) -> None:
        body = self.under("## Procedure", SKILL_AUTHORITY)
        self.assertLess(
            body.index("### When Not to Use"), body.index("### Authority Boundary")
        )
        self.assertEqual(self.tree(body), [])

    def test_authority_boundary_under_another_h2_is_refused(self) -> None:
        for heading in ("## Outputs", "## Verification"):
            with self.subTest(before=heading):
                self.assertEqual(
                    self.tree(self.under(heading, SKILL_AUTHORITY)),
                    ["BODY-H3-PARENT"],
                )
        self.assertEqual(self.tree(self.under("", SKILL_AUTHORITY)), ["BODY-H3-PARENT"])

    def test_the_steps_table_passes_and_a_wrong_table_there_fails(self) -> None:
        good = self.table(self.HEADER, ("1", "A request", "A report"))
        self.assertEqual(self.tables(self.with_table(good)), [])
        old = self.table(("Step", "Action", "Check"), ("1", "a", "b"))
        self.assertEqual(self.tables(self.with_table(old)), ["BODY-TABLE-COLUMNS"])


class GovernanceSkillFormTests(SkillFormBody):
    """SPEC-0177 VAL-SKILL-001: the Skill form on the common workflows."""

    PATH = GOVERNANCE_SKILL_PATH
    PROFILES = SKILL_GOVERNANCE

    def test_the_authored_profile_keeps_a_form_and_empty_h2_lists(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        by_id = {profile.profile_id: profile for profile in registry.profiles}
        self.assertEqual(by_id[self.PROFILES[0]].mode, "authored")
        self.assertNotIn("sections", profile_of(load_raw(), self.PROFILES[0]))

    def test_an_absent_authority_boundary_passes_and_an_empty_one_fails(self) -> None:
        self.assertNotIn("Authority Boundary", self.BODY)
        self.assertEqual(self.tree(self.BODY), [])
        empty = self.under("## Procedure", "### Authority Boundary\n")
        self.assertEqual(self.tree(empty), ["BODY-SECTION-EMPTY"])

    def test_both_workflows_resolve_to_the_skill_profile(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        for path in (
            ".agents/workflows/work-lifecycle.md",
            ".agents/workflows/delegated-development.md",
        ):
            with self.subTest(path=path):
                profile = CONTRACTS.classify_path(registry, PurePosixPath(path))
                self.assertEqual(profile.profile_id, SKILL_GOVERNANCE[0])
                self.assertEqual(profile.document_role, "skill")


class NativeSkillFormTests(SkillFormBody):
    """SPEC-0177 VAL-SKILL-001: the Skill form on native SKILL.md packages."""

    PATH = NATIVE_SKILL_PATH
    PROFILES = SKILL_NATIVE

    def test_the_loaded_heading_lists_equal_the_form_h2_titles(self) -> None:
        # The native Skill profiles carry no H2 lists, like the AGENTS ones.
        registry = CONTRACTS.load_registry(ROOT)
        loaded = next(f for f in registry.common_forms if f.form_id == self.FORM_ID)
        self.assertEqual(
            tuple(item.title for item in loaded.sections),
            tuple(title for title, _ in self.TREE),
        )
        by_id = {profile.profile_id: profile for profile in registry.profiles}
        for profile_id in self.PROFILES:
            with self.subTest(profile=profile_id):
                raw = profile_of(load_raw(), profile_id)
                self.assertNotIn("sections", raw)
                self.assertIs(by_id[profile_id].form, loaded)

    def test_the_package_is_native_and_its_template_is_the_exact_twin(self) -> None:
        raw = load_raw()
        package, twin = (profile_of(raw, profile_id) for profile_id in self.PROFILES)
        self.assertEqual(package["mode"], "native")
        self.assertEqual(
            package["template_source"],
            "docs/99.templates/templates/common/native-skill.template.md",
        )
        self.assertEqual(twin["mode"], "template")
        self.assertEqual(twin["placeholder_policy"], "template-only")
        self.assertEqual(twin["frontmatter"], package["frontmatter"])
        self.assertEqual(
            twin["frontmatter"]["constants"], {"disable-model-invocation": True}
        )
        self.assertEqual(
            twin["relationships"]["source_profile_ids"], [self.PROFILES[0]]
        )
        self.assertEqual(
            twin["path_pattern"],
            "^docs/99\\.templates/templates/common/native\\-skill\\.template\\.md$",
        )

    def test_the_authority_sentence_before_the_h1_does_not_disturb_the_tree(
        self,
    ) -> None:
        body = skill_body(preface="Read the policy before using this procedure.")
        self.assertEqual(self.tree(body), [])
        self.assertEqual(self.tables(body), [])

    def test_reference_files_and_assets_keep_no_role(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        by_id = {profile.profile_id: profile for profile in registry.profiles}
        for profile_id in (
            "common/native-skill-reference",
            "common/native-skill-asset",
        ):
            with self.subTest(profile=profile_id):
                self.assertIsNone(by_id[profile_id].document_role)
                self.assertIsNone(by_id[profile_id].form)


WORKSPACE_PATH = PurePosixPath("_workspace/diagnostics/README.md")
PACK_PATH = PurePosixPath("docs/90.references/research/0001-example/README.md")
LOCAL_FORM_CONSUMERS = (
    "docs/99.templates/registry.json",
    "docs/99.templates/contracts/document-profile.schema.json",
    "docs/99.templates/README.md",
    "scripts/document_contracts.py",
    "scripts/validate-markdown-profiles.py",
    "scripts/validate-document-contract-registry.py",
    "scripts/validate-links-and-owners.py",
    "scripts/validation/repository/form_contracts.py",
    "scripts/validation/repository/quality.py",
    "tests/test_common_form_tree.py",
)


def workspace_body() -> str:
    return md(
        "# Workspace area",
        "## Overview\n\nA local staging area.",
        "## Scope",
        "### Permitted Artifacts\n\nAnalysis output.",
        "### Forbidden Local State\n\nNo secrets.",
        "## Structure\n\nOne folder per kind.",
        "## Usage",
        "### Promotion and Cleanup\n\nPromote, then delete.",
        "### Tracking Rules\n\nIgnored by Git.",
        "## Related Documents\n\n- [Root](../README.md)",
    )


def pack_body(
    *extra: tuple[str, str], closure: str | None = PACK_CLOSURES[PACK_FORM[0]]
) -> str:
    """A pack README with its closure section and any supplied overrides."""

    later = {closure: "The pack records its review boundary."} if closure else {}
    later.update(extra)
    blocks = ["# Research pack"]
    for title, _ in PACK_FORM_TREE:
        if title == "Related Documents":
            blocks.append("## Related Documents\n\n- [Stage](../README.md)")
        elif title in PACK_NOT_REQUIRED:
            if title in later:
                blocks.append(f"## {title}\n\n{later[title]}")
        else:
            blocks.append(f"## {title}\n\nThe {title} of the pack.")
    return md(*blocks)


# TestCase is named again so the static collector sees a runnable base.
class LocalReadmeForm(unittest.TestCase):
    """Shared checks for a Stage 99 local README role (W03-D09, W03-D10)."""

    PATH: PurePosixPath
    PROFILES: tuple[str, ...]  # source, twin, ...
    FORM_ID: str
    FORM_TITLE: str
    TREE: tuple
    BODY: str

    @classmethod
    def setUpClass(cls) -> None:
        if cls is LocalReadmeForm:
            raise unittest.SkipTest("shared base; its subclasses run the checks")
        cls.profile = typed_profiles(load_raw())[cls.PROFILES[0]]

    def tree(self, text: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._body_diagnostics(
                self.PATH, self.profile, text, "active"
            )
        )

    def under(self, heading: str, block: str) -> str:
        """Insert a block just before the given H2 (or at the end)."""

        if not heading:
            return self.BODY + "\n" + block + "\n"
        return self.BODY.replace("\n" + heading, "\n" + block + "\n\n" + heading, 1)

    def raw_form(self) -> dict:
        return next(
            f
            for f in load_raw()["common_forms"]["forms"]
            if f["form_id"] == self.FORM_ID
        )

    def test_the_form_is_a_stage_99_local_role_with_the_readme_language_rule(
        self,
    ) -> None:
        raw = self.raw_form()
        stage = next(
            f
            for f in load_raw()["common_forms"]["forms"]
            if f["form_id"] == "stage-readme"
        )
        self.assertEqual(raw["title"], self.FORM_TITLE)
        self.assertEqual(raw["h1"], "{{document_title}}")
        self.assertEqual(raw["language_rule"], stage["language_rule"])
        policy = raw["extension_policy"]
        for needle in ("Stage 99", "W03-D09", "W03-D10", "COMMON-DOC-FORM-1"):
            self.assertIn(needle, policy)
        self.assertNotEqual(policy, stage["extension_policy"])

    def test_the_form_tree_has_the_registered_titles_and_no_body_section(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        loaded = next(f for f in registry.common_forms if f.form_id == self.FORM_ID)
        self.assertEqual(
            tuple(
                (item.title, tuple(child.title for child in item.children))
                for item in loaded.sections
            ),
            self.TREE,
        )
        for profile_id in self.PROFILES:
            with self.subTest(profile=profile_id):
                profile = profile_of(load_raw(), profile_id)
                self.assertEqual(profile["document_role"], self.FORM_ID)
                self.assertNotIn("sections", profile)
                self.assertIsNone(profile["relationships"]["body_contract"])

    def test_the_repository_registry_is_valid_and_its_twins_match(self) -> None:
        self.assertEqual(rules_of(load_raw()), set())
        REGISTRY_CHECK._assert_template_source_parity(CONTRACTS.load_registry(ROOT))

    def test_every_template_twin_has_a_definition_without_tables(self) -> None:
        for profile_id in self.PROFILES:
            profile = profile_of(load_raw(), profile_id)
            if profile["mode"] != "template":
                continue
            with self.subTest(profile=profile_id):
                definition_ = profile["template_definition"]
                self.assertEqual(definition_["tables"], [])
                self.assertEqual(
                    definition_["policy_refs"],
                    [
                        ".agents/governance/document-authoring.md",
                        ".agents/governance/document-lifecycle.md",
                    ],
                )
                self.assertEqual(
                    definition_["vocabulary_refs"], [".agents/knowledge/glossary.md"]
                )
                paths = definition_["consumer_paths"]
                self.assertEqual(len(paths), len(set(paths)))
                self.assertIn(profile["template_source"], paths)
                for path in (*LOCAL_FORM_CONSUMERS, *paths):
                    self.assertTrue((ROOT / path).is_file(), path)
                for path in LOCAL_FORM_CONSUMERS:
                    self.assertIn(path, paths)

    def test_a_complete_document_passes_the_tree(self) -> None:
        self.assertEqual(self.tree(self.BODY), [])

    def test_a_missing_or_renamed_h2_fails_the_tree(self) -> None:
        self.assertEqual(
            self.tree(self.BODY.replace("## Structure", "## Layout")),
            ["BODY-HEADING-REQUIRED", "BODY-HEADING-UNSUPPORTED"],
        )

    def test_an_unregistered_h3_is_refused(self) -> None:
        self.assertEqual(
            self.tree(self.under("## Related Documents", "### Stray\n\nText.")),
            ["BODY-H3-UNSUPPORTED"],
        )


class WorkspaceReadmeFormTests(LocalReadmeForm):
    """SPEC-0178 VAL-LOCALREADME-001: the Workspace README form."""

    PATH = WORKSPACE_PATH
    PROFILES = WORKSPACE_FORM
    FORM_ID = "workspace-readme"
    FORM_TITLE = "Workspace README"
    TREE = WORKSPACE_FORM_TREE
    BODY = workspace_body()

    def test_the_form_has_no_extension(self) -> None:
        self.assertEqual(self.raw_form()["extensions"], [])

    def test_a_router_profile_leaves_empty_sections_to_review(self) -> None:
        self.assertEqual(self.profile.mode, "router")
        bare = re.sub(r"(## Structure\n\n)[^\n]*", r"\1", self.BODY)
        self.assertEqual(self.tree(bare), [])
        links = re.sub(r"(## Structure\n\n)[^\n]*", r"\1- [a](a.md)", self.BODY)
        self.assertEqual(self.tree(links), [])

    def test_a_missing_or_renamed_form_h3_fails_the_tree(self) -> None:
        self.assertEqual(
            self.tree(self.BODY.replace("### Tracking Rules", "### Tracking")),
            ["BODY-H3-REQUIRED", "BODY-H3-UNSUPPORTED"],
        )
        self.assertEqual(
            self.tree(self.under("## Structure", "### Stray\n\nText.")),
            ["BODY-H3-UNSUPPORTED"],
        )

    def test_the_seven_workspace_readmes_resolve_to_the_profile(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        for path in (
            "_workspace/README.md",
            "_workspace/diagnostics/README.md",
            "_workspace/diagnostics/ci/README.md",
            "_workspace/diagnostics/validation/README.md",
            "_workspace/repo-support/README.md",
            "_workspace/repo-support/analysis/README.md",
            "_workspace/repo-support/previews/README.md",
        ):
            with self.subTest(path=path):
                profile = CONTRACTS.classify_path(registry, PurePosixPath(path))
                self.assertEqual(profile.profile_id, WORKSPACE_FORM[0])
                self.assertEqual(profile.document_role, "workspace-readme")


class ReferencePackFormTests(LocalReadmeForm):
    """SPEC-0178 VAL-LOCALREADME-001: the Reference Pack README form."""

    PATH = PACK_PATH
    PROFILES = PACK_FORM
    FORM_ID = "reference-pack-readme"
    FORM_TITLE = "Reference Pack README"
    TREE = PACK_FORM_TREE
    BODY = pack_body()

    def test_pack_must_include_only_its_own_closure_section(self) -> None:
        self.assertEqual(self.tree(pack_body(closure=None)), ["BODY-HEADING-REQUIRED"])
        research = ("Refresh and Succession", "Review the cited sources.")
        self.assertEqual(self.tree(pack_body(research)), [])
        audit = ("Review and Closure", "Close verified audit items.")
        self.assertEqual(
            self.tree(pack_body(research, audit)), ["BODY-HEADING-INAPPLICABLE"]
        )

    def test_related_documents_may_be_a_link_list_and_no_other_section(self) -> None:
        self.assertEqual(self.tree(self.BODY), [])
        plain = re.sub(r"(## Structure\n\n)[^\n]*", r"\1- [a](a.md)", self.BODY)
        self.assertEqual(self.tree(plain), ["BODY-SECTION-EMPTY"])
        bare = re.sub(r"(## Related Documents\n\n)[^\n]*", r"\1", self.BODY)
        self.assertEqual(self.tree(bare), ["BODY-SECTION-EMPTY"])

    def test_the_form_has_the_two_registered_local_h3s(self) -> None:
        self.assertEqual(self.raw_form()["extensions"], PACK_EXTENSIONS)

    def test_closure_sections_are_conditional_and_method_is_optional(self) -> None:
        sections = {s["title"]: s for s in self.raw_form()["sections"]}
        for title in PACK_NOT_REQUIRED:
            with self.subTest(section=title):
                self.assertNotEqual(sections[title]["requiredness"], "required")
                self.assertNotEqual(sections[title]["condition"], "always")
        self.assertEqual(sections["Method"]["requiredness"], "optional")
        for title in PACK_NOT_REQUIRED[1:]:
            self.assertEqual(sections[title]["requiredness"], "conditional")

    def test_the_profiles_derive_the_required_headings_from_the_form(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        every = tuple(title for title, _ in PACK_FORM_TREE)
        by_id = {profile.profile_id: profile for profile in registry.profiles}
        for profile_id in PACK_FORM:
            with self.subTest(profile=profile_id):
                profile = by_id[profile_id]
                source_id = next(iter(profile.source_profile_ids), profile_id)
                headings = CONTRACTS.heading_contract(profile)
                closure = PACK_CLOSURES[source_id]
                self.assertEqual(
                    headings.required,
                    tuple(
                        t for t in every if t == closure or t not in PACK_NOT_REQUIRED
                    ),
                )
                self.assertEqual(
                    headings.allowed,
                    tuple(
                        t
                        for t in every
                        if t == closure or t not in PACK_CLOSURES.values()
                    ),
                )

    def test_optional_method_may_be_absent_and_present_sections_need_content(
        self,
    ) -> None:
        self.assertEqual(self.tree(self.BODY), [])
        for title in ("Method", PACK_CLOSURES[PACK_FORM[0]]):
            with self.subTest(section=title):
                body = pack_body((title, "The pack states it."))
                self.assertEqual(self.tree(body), [])
                empty = pack_body((title, ""))
                self.assertEqual(self.tree(empty), ["BODY-SECTION-EMPTY"])

    def test_the_applicable_closure_section_keeps_form_order(self) -> None:
        closure = PACK_CLOSURES[PACK_FORM[0]]
        body = pack_body((closure, "Stated."))
        self.assertEqual(self.tree(body), [])
        early = body.replace("## Usage", f"## {closure}\n\nEarly.\n\n## Usage", 1)
        early = early.replace(f"## {closure}\n\nStated.\n\n", "", 1)
        self.assertEqual(self.tree(early), ["BODY-H2-ORDER"])

    def test_applicability_refuses_missing_other_role_and_template_sources(
        self,
    ) -> None:
        for profile_id in (
            "reference/unknown-pack",
            "reference/research",
            "common/template-readme-research-pack",
        ):
            with self.subTest(profile=profile_id):
                raw = load_raw()
                form = next(
                    f
                    for f in raw["common_forms"]["forms"]
                    if f["form_id"] == self.FORM_ID
                )
                section = next(
                    s
                    for s in form["sections"]
                    if s["title"] == PACK_CLOSURES[PACK_FORM[0]]
                )
                section["applicability"]["source_profile_ids"] = [profile_id]
                self.assertIn("REGISTRY_FORM_CONDITION", semantic_rules_of(raw))

    def test_an_old_pack_heading_is_refused(self) -> None:
        for old, new in (
            ("## Pack Contract", "## Research Contract"),
            ("## Pack Index", "## Report Index"),
        ):
            with self.subTest(old=new):
                self.assertEqual(
                    self.tree(self.BODY.replace(old, new)),
                    ["BODY-HEADING-REQUIRED", "BODY-HEADING-UNSUPPORTED"],
                )

    def test_the_local_h3s_are_accepted_under_pack_contract_only(self) -> None:
        for title in ("External Finding Vocabulary", "Separate Evidence Axes"):
            block = f"### {title}\n\nThe pack keeps it."
            with self.subTest(h3=title):
                self.assertEqual(self.tree(self.under("## Structure", block)), [])
                for heading in ("## Pack Contract", "## Usage", "## Related Documents"):
                    self.assertEqual(
                        self.tree(self.under(heading, block)), ["BODY-H3-PARENT"]
                    )
                self.assertEqual(self.tree(self.under("", block)), ["BODY-H3-PARENT"])

    def test_an_empty_local_h3_fails_and_an_absent_one_passes(self) -> None:
        self.assertNotIn("External Finding Vocabulary", self.BODY)
        empty = self.under("## Structure", "### Separate Evidence Axes\n")
        self.assertEqual(self.tree(empty), ["BODY-SECTION-EMPTY"])

    def test_both_local_h3s_are_accepted_together_under_pack_contract(self) -> None:
        both = self.under(
            "## Structure",
            "### External Finding Vocabulary\n\nTerms.\n\n"
            "### Separate Evidence Axes\n\nAxes.",
        )
        self.assertEqual(self.tree(both), [])

    def test_the_three_pack_profiles_read_navigation_from_pack_index(self) -> None:
        navigation = load_raw()["readme_navigation"]["profiles"]
        for profile_id in (
            "reference/audit-pack",
            "reference/data-pack",
            "reference/research-pack",
        ):
            with self.subTest(profile=profile_id):
                self.assertEqual(
                    navigation[profile_id], {"section": "Pack Index", "complete": True}
                )

    def test_the_pack_readmes_resolve_to_the_pack_profiles(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        for path, profile_id in (
            (
                "docs/90.references/research/0001-workspace-engineering/README.md",
                "reference/research-pack",
            ),
            (
                "docs/90.references/audits/0001-sdlc-governance/README.md",
                "reference/audit-pack",
            ),
            ("docs/90.references/data/0001-example/README.md", "reference/data-pack"),
        ):
            with self.subTest(path=path):
                profile = CONTRACTS.classify_path(registry, PurePosixPath(path))
                self.assertEqual(profile.profile_id, profile_id)
                self.assertEqual(profile.document_role, "reference-pack-readme")


class SmallLocalFormTests(unittest.TestCase):
    """SPEC-0186 VAL-SMALLFORMS-001: the six small local forms (W03-D26)."""

    PATHS = {
        "knowledge-map": PurePosixPath(".agents/knowledge/domains.md"),
        "vocabulary": PurePosixPath(".agents/knowledge/glossary.md"),
        "prompt": PurePosixPath(".agents/prompts/doc-update.md"),
        "evaluation-task": PurePosixPath(".agents/evaluations/harnesses/x/task.md"),
        "evaluation-score": PurePosixPath(".agents/evaluations/harnesses/x/score.md"),
        "evaluation-results": PurePosixPath(".agents/evaluations/results.md"),
    }
    NONE = "None is stated in this document."

    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = load_raw()
        cls.profiles = typed_profiles(cls.raw)

    @staticmethod
    def body(tree: tuple, link: str, *, skip: str = "", swap: bool = False) -> str:
        titles = [title for title, _ in tree if title != skip]
        if swap:
            titles[0], titles[1] = titles[1], titles[0]
        blocks = ["# Document title"]
        for title in titles:
            text = "- [Owner](owner.md)" if title == link else f"The {title} text."
            blocks.append(f"## {title}\n\n{text}")
        return md(*blocks)

    def tree_rules(self, form_id: str, source: str, text: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._body_diagnostics(
                self.PATHS[form_id], self.profiles[source], text, "active"
            )
        )

    def test_the_forms_are_stage_99_local_forms_with_only_required_h2_sections(
        self,
    ) -> None:
        forms = {f["form_id"]: f for f in self.raw["common_forms"]["forms"]}
        stage = forms["stage-readme"]
        for form_id, title, _, tree, _, link in SMALL_FORMS:
            with self.subTest(form=form_id):
                form = forms[form_id]
                self.assertEqual(form["title"], title)
                self.assertEqual(form["h1"], "{{document_title}}")
                self.assertEqual(form["language_rule"], stage["language_rule"])
                self.assertEqual(form["extensions"], [])
                for needle in ("Stage 99", "W03-D09", "W03-D20", "W03-D26"):
                    self.assertIn(needle, form["extension_policy"])
                self.assertIn("COMMON-DOC-FORM-1", form["extension_policy"])
                self.assertNotEqual(form["extension_policy"], stage["extension_policy"])
                self.assertEqual(
                    [
                        (s["section_id"], s["title"], s["order"])
                        for s in form["sections"]
                    ],
                    [
                        (f"{form_id}-{name.lower().replace(' ', '-')}", name, n)
                        for n, (name, _) in enumerate(tree, start=1)
                    ],
                )
                for s in form["sections"]:
                    self.assertEqual(s["level"], 2)
                    self.assertEqual(s["requiredness"], "required")
                    self.assertEqual(s["condition"], "always")
                    self.assertEqual(s["children"], [])
                    self.assertEqual(
                        s["empty_policy"], "explain_none_or_not_applicable"
                    )
                    self.assertEqual(
                        s["validation_ids"], ["FORM-STRUCTURE", "FORM-CONTENT-REVIEW"]
                    )
                    self.assertTrue(s["required_content"] and s["prohibited_content"])
                    self.assertIs(s["link_only"], s["title"] == link)
        self.assertEqual(
            sum(
                len(f["sections"])
                for f in forms.values()
                if f["form_id"] in {x[0] for x in SMALL_FORMS}
            ),
            34,
        )

    def test_the_twelve_profiles_use_the_form_and_hold_no_h2_list(self) -> None:
        self.assertEqual(sum(len(x[2]) for x in SMALL_FORMS), 12)
        for form_id, _, profiles, _, _, _ in SMALL_FORMS:
            for profile_id in profiles:
                with self.subTest(profile=profile_id):
                    raw = profile_of(self.raw, profile_id)
                    self.assertEqual(raw["document_role"], form_id)
                    self.assertNotIn("sections", raw)
                    self.assertEqual(self.profiles[profile_id].form.form_id, form_id)
        self.assertNotIn("sections", profile_of(self.raw, "evaluation/raw-output"))
        self.assertIsNone(self.profiles["evaluation/raw-output"].form)

    def test_the_twin_definitions_name_the_form_and_record_section_id_tables(
        self,
    ) -> None:
        for form_id, _, (_, twin), _, tables, _ in SMALL_FORMS:
            with self.subTest(form=form_id):
                definition_ = profile_of(self.raw, twin)["template_definition"]
                self.assertEqual(
                    [
                        (
                            t["name"],
                            t["section"],
                            tuple(c["key"] for c in t["columns"]),
                            t["minimum_rows"],
                            t["row_identity"],
                        )
                        for t in definition_["tables"]
                    ],
                    tables,
                )
                joined = " ".join(definition_["non_goals"])
                self.assertIn("W03-D26", joined)
                self.assertNotIn("has no form", joined)
                self.assertNotIn("stay as the profile records them", joined)
                self.assertIn("owned by the form", joined)
                for path in (
                    "scripts/validate-document-contract-registry.py",
                    "scripts/validation/repository/form_contracts.py",
                    "scripts/validation/repository/quality.py",
                    "tests/test_common_form_tree.py",
                ):
                    self.assertIn(path, definition_["consumer_paths"])
                for path in definition_["consumer_paths"]:
                    self.assertTrue((ROOT / path).is_file(), path)
                checks = " ".join(
                    definition_["validation"]["positive"]
                    + definition_["validation"]["negative"]
                )
                self.assertNotIn("heading line", checks)
                self.assertEqual("REGISTRY_TABLE_SECTION" in checks, bool(tables))
                self.assertEqual("BODY-TABLE-COLUMNS" in checks, bool(tables))
                self.assertEqual("BODY-TABLE-ROWS" in checks, bool(tables))
                self.assertIn("SPEC-0186", definition_["migration"]["meaning_map"])

    def test_the_repository_registry_is_valid_and_its_twins_match(self) -> None:
        self.assertEqual(rules_of(load_raw()), set())
        REGISTRY_CHECK._assert_template_source_parity(CONTRACTS.load_registry(ROOT))

    def test_a_complete_document_passes_the_tree(self) -> None:
        for form_id, _, (source, twin), tree, _, link in SMALL_FORMS:
            with self.subTest(form=form_id):
                text = self.body(tree, link)
                self.assertEqual(self.tree_rules(form_id, source, text), [])
                self.assertEqual(self.tree_rules(form_id, twin, text), [])

    def test_a_missing_h2_fails_the_tree(self) -> None:
        for form_id, _, (source, _), tree, _, link in SMALL_FORMS:
            with self.subTest(form=form_id):
                text = self.body(tree, link, skip=tree[1][0])
                self.assertEqual(
                    self.tree_rules(form_id, source, text), ["BODY-HEADING-REQUIRED"]
                )

    def test_a_reordered_required_h2_fails_the_tree(self) -> None:
        for form_id, _, (source, _), tree, _, link in SMALL_FORMS:
            with self.subTest(form=form_id):
                text = self.body(tree, link, swap=True)
                self.assertEqual(
                    self.tree_rules(form_id, source, text), ["BODY-H2-ORDER"]
                )

    def test_a_stray_h3_is_refused(self) -> None:
        for form_id, _, (source, _), tree, _, link in SMALL_FORMS:
            with self.subTest(form=form_id):
                text = self.body(tree, link).replace(
                    f"## {tree[0][0]}\n\n",
                    f"## {tree[0][0]}\n\n### Stray\n\nText.\n\n",
                    1,
                )
                self.assertEqual(
                    self.tree_rules(form_id, source, text), ["BODY-H3-UNSUPPORTED"]
                )

    def test_a_bare_section_fails_and_a_template_is_not_checked(self) -> None:
        for form_id, _, (source, twin), tree, _, link in SMALL_FORMS:
            with self.subTest(form=form_id):
                name = tree[0][0]
                text = self.body(tree, link).replace(f"The {name} text.", self.NONE)
                self.assertEqual(
                    self.tree_rules(form_id, source, text), ["BODY-SECTION-BARE"]
                )
                self.assertEqual(self.tree_rules(form_id, twin, text), [])

    def test_only_the_link_section_may_hold_links_alone(self) -> None:
        for form_id, _, (source, _), tree, _, link in SMALL_FORMS:
            with self.subTest(form=form_id):
                self.assertIn(
                    f"## {link}\n\n- [Owner](owner.md)", self.body(tree, link)
                )
                other = tree[0][0]
                text = self.body(tree, link).replace(
                    f"The {other} text.", "- [Owner](owner.md)"
                )
                self.assertEqual(
                    self.tree_rules(form_id, source, text), ["BODY-SECTION-EMPTY"]
                )
                self.assertEqual(
                    self.tree_rules(form_id, source, self.body(tree, link)), []
                )

    def test_the_h2_titles_two_scripts_read_by_name_stay_literal(self) -> None:
        titles = {
            form_id: {name for name, _ in tree}
            for form_id, _, _, tree, _, _ in SMALL_FORMS
        }
        self.assertIn("Pointer Index", titles["knowledge-map"])
        self.assertLessEqual(
            {"Repository Vocabulary", "Local Extensions"}, titles["vocabulary"]
        )
        self.assertIn("Inputs", titles["prompt"])

    def test_a_table_is_read_by_its_section_id_and_checked_by_column(self) -> None:
        for form_id, _, (source, _), tree, tables, link in SMALL_FORMS:
            for name, section_id, keys, _, _ in tables:
                with self.subTest(form=form_id, section=section_id):
                    title = next(
                        n
                        for n, _ in tree
                        if f"{form_id}-{n.lower().replace(' ', '-')}" == section_id
                    )
                    # The identity column stays first, so a swap needs three.
                    variants = [(keys, []), (keys[:-1], ["BODY-TABLE-COLUMNS"])]
                    if len(keys) > 2:
                        swapped = (*keys[:-2], keys[-1], keys[-2])
                        variants.append((swapped, ["BODY-TABLE-COLUMNS"]))
                    for header, expected in variants:
                        table = "\n".join(
                            (
                                "| " + " | ".join(header) + " |",
                                "| " + " | ".join("---" for _ in header) + " |",
                                "| " + " | ".join("x" for _ in header) + " |",
                            )
                        )
                        text = self.body(tree, link).replace(
                            f"## {title}\n\n", f"## {title}\n\n{table}\n\n", 1
                        )
                        found = sorted(
                            item.rule_id
                            for item in MARKDOWN._table_diagnostics(
                                self.PATHS[form_id], self.profiles[source], text
                            )
                        )
                        self.assertEqual(found, expected)

    def test_an_unknown_table_section_id_is_refused(self) -> None:
        for form_id, _, (_, twin), _, tables, _ in SMALL_FORMS:
            if not tables:
                continue
            with self.subTest(form=form_id):
                raw = load_raw()
                profile_of(raw, twin)["template_definition"]["tables"][0]["section"] = (
                    f"{form_id}-no-such-section"
                )
                self.assertIn("REGISTRY_TABLE_SECTION", rules_of(raw))
                raw = load_raw()
                profile_of(raw, twin)["template_definition"]["tables"][0]["section"] = (
                    "## Overview"
                )
                self.assertIn("REGISTRY_TABLE_SECTION", rules_of(raw))

    def test_a_profile_of_these_roles_with_an_h2_list_is_refused(self) -> None:
        for form_id, _, (source, twin), _, _, _ in SMALL_FORMS:
            for profile_id in (source, twin):
                with self.subTest(profile=profile_id):
                    raw = load_raw()
                    profile_of(raw, profile_id)["sections"] = lists_of(
                        required=["Overview"]
                    )
                    self.assertIn("REGISTRY_FORM_LEGACY_LISTS", semantic_rules_of(raw))


class GovernanceRoleFormTests(unittest.TestCase):
    """SPEC-0188 VAL-GOVROLE-001: the governance role and document forms."""

    PATHS = {
        "governance-role": PurePosixPath(".agents/roles/quality-engineer.md"),
        "governance-document": PurePosixPath(".claude/provider.md"),
    }
    NONE = "None is stated in this document."

    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = load_raw()
        cls.profiles = typed_profiles(cls.raw)

    @staticmethod
    def body(tree: tuple, *, mutate=None) -> str:
        blocks = ["# Document title"]
        for title, children in tree:
            text = (
                "- [Owner](owner.md)"
                if title == "Related Documents"
                else f"The {title} text."
            )
            blocks.append(f"## {title}\n\n{text}")
            for child in children:
                blocks.append(f"### {child}\n\nThe {child} text.")
        text = md(*blocks)
        return mutate(text) if mutate else text

    def tree_rules(self, form_id: str, text: str) -> list[str]:
        source = {"governance-role": "governance/role"}.get(
            form_id, "governance/provider"
        )
        return sorted(
            item.rule_id
            for item in MARKDOWN._body_diagnostics(
                self.PATHS[form_id], self.profiles[source], text, "active"
            )
        )

    def test_the_forms_hold_twenty_sections_and_no_extension(self) -> None:
        forms = {f["form_id"]: f for f in self.raw["common_forms"]["forms"]}
        stage = forms["stage-readme"]
        counts = {}
        for form_id, title, _, tree, _, link in GOVERNANCE_FORMS:
            with self.subTest(form=form_id):
                form = forms[form_id]
                self.assertEqual(form["title"], title)
                self.assertEqual(form["h1"], "{{document_title}}")
                self.assertEqual(form["language_rule"], stage["language_rule"])
                self.assertEqual(form["extensions"], [])
                for needle in ("Stage 99", "W03-D09", "W03-D20", "W03-D26", "W03-D34"):
                    self.assertIn(needle, form["extension_policy"])
                self.assertIn("COMMON-DOC-FORM-1", form["extension_policy"])
                nodes = [n for s in form["sections"] for n in (s, *s["children"])]
                counts[form_id] = len(nodes)
                for node in nodes:
                    self.assertEqual(node["requiredness"], "required")
                    self.assertEqual(node["condition"], "always")
                    self.assertEqual(
                        node["empty_policy"], "explain_none_or_not_applicable"
                    )
                    self.assertEqual(
                        node["validation_ids"],
                        ["FORM-STRUCTURE", "FORM-CONTENT-REVIEW"],
                    )
                    self.assertTrue(
                        node["required_content"] and node["prohibited_content"]
                    )
                    self.assertIs(node["link_only"], node["title"] == link)
        self.assertEqual(counts, {"governance-document": 6, "governance-role": 14})
        role = forms["governance-role"]["sections"][3]
        self.assertEqual(
            [c["section_id"] for c in role["children"]][4:7],
            [
                "governance-role-current-contract-guardrails",
                "governance-role-current-contract-capability-and-evidence",
                "governance-role-current-contract-handoff-escalation",
            ],
        )
        document = forms["governance-document"]["sections"][3]
        self.assertEqual(document["children"], [])
        self.assertIn("여덟 H3", " ".join(document["prohibited_content"]))

    def test_the_four_profiles_hold_no_h2_list_and_the_role_pair_is_rebound(
        self,
    ) -> None:
        for form_id, _, profiles, _, _, _ in GOVERNANCE_FORMS:
            for profile_id in profiles:
                with self.subTest(profile=profile_id):
                    raw = profile_of(self.raw, profile_id)
                    self.assertEqual(raw["document_role"], form_id)
                    self.assertNotIn("sections", raw)
                    self.assertEqual(self.profiles[profile_id].form.form_id, form_id)
        bound = sorted(
            p["id"]
            for p in self.raw["profiles"]
            if p.get("document_role") == "governance-document"
        )
        self.assertEqual(
            bound, ["common/template-governance-provider", "governance/provider"]
        )

    def test_the_twin_definitions_name_the_forms_and_the_new_consumers(self) -> None:
        for form_id, _, (_, twin), _, _, _ in GOVERNANCE_FORMS:
            with self.subTest(form=form_id):
                definition_ = profile_of(self.raw, twin)["template_definition"]
                self.assertEqual(definition_["tables"], [])
                joined = " ".join(definition_["non_goals"])
                self.assertIn("W03-D26", joined)
                self.assertNotIn("has no form", joined)
                self.assertNotIn("stay as the profile records them", joined)
                self.assertIn("owned by the form", joined)
                self.assertEqual("W03-D34" in joined, form_id == "governance-role")
                for path in (
                    "scripts/validate-document-contract-registry.py",
                    "scripts/validation/repository/form_contracts.py",
                    "scripts/validation/repository/quality.py",
                    "tests/test_common_form_tree.py",
                ):
                    self.assertIn(path, definition_["consumer_paths"])
                for path in definition_["consumer_paths"]:
                    self.assertTrue((ROOT / path).is_file(), path)
                checks = " ".join(
                    definition_["validation"]["positive"]
                    + definition_["validation"]["negative"]
                )
                self.assertNotIn("H2 list the profile records", checks)
                self.assertIn("form tree", checks)
                self.assertIn("SPEC-0188", definition_["migration"]["meaning_map"])
        role = profile_of(self.raw, GOVERNANCE_ROLE_FORM[1])["template_definition"]
        self.assertIn("eight H3", role["migration"]["meaning_map"])

    def test_the_repository_registry_is_valid_and_its_twins_match(self) -> None:
        self.assertEqual(rules_of(load_raw()), set())
        REGISTRY_CHECK._assert_template_source_parity(CONTRACTS.load_registry(ROOT))

    def test_a_complete_document_passes_the_tree(self) -> None:
        for form_id, _, (source, twin), tree, _, _ in GOVERNANCE_FORMS:
            with self.subTest(form=form_id):
                self.assertEqual(self.tree_rules(form_id, self.body(tree)), [])

    def test_a_missing_extra_or_reordered_h3_fails_the_role_tree(self) -> None:
        tree = GOVERNANCE_ROLE_TREE
        for name, mutate, expected in (
            (
                "missing",
                lambda t: t.replace("### Inputs\n\nThe Inputs text.\n\n", ""),
                ["BODY-H3-REQUIRED"],
            ),
            (
                "extra",
                lambda t: t.replace(
                    "### Role\n\n", "### Stray\n\nText.\n\n### Role\n\n", 1
                ),
                ["BODY-H3-UNSUPPORTED"],
            ),
            (
                "reordered",
                lambda t: (
                    t.replace("### Inputs", "### TMP")
                    .replace("### Outputs", "### Inputs")
                    .replace("### TMP", "### Outputs")
                ),
                ["BODY-H3-ORDER"],
            ),
        ):
            with self.subTest(case=name):
                found = self.tree_rules(
                    "governance-role", self.body(tree, mutate=mutate)
                )
                self.assertTrue(found, name)
                self.assertEqual(found, expected)

    def test_a_stray_h3_in_a_governance_document_tree_is_refused(self) -> None:
        text = self.body(GOVERNANCE_DOCUMENT_TREE).replace(
            "## Current Contract\n\n",
            "## Current Contract\n\n### Role\n\nText.\n\n",
            1,
        )
        self.assertEqual(
            self.tree_rules("governance-document", text), ["BODY-H3-UNSUPPORTED"]
        )

    def test_a_bare_section_fails_and_only_related_documents_may_be_links(
        self,
    ) -> None:
        for form_id, _, _, tree, _, _ in GOVERNANCE_FORMS:
            with self.subTest(form=form_id):
                text = self.body(tree).replace("The Overview text.", self.NONE)
                self.assertEqual(self.tree_rules(form_id, text), ["BODY-SECTION-BARE"])
                text = self.body(tree).replace(
                    "The Overview text.", "- [Owner](owner.md)"
                )
                self.assertEqual(self.tree_rules(form_id, text), ["BODY-SECTION-EMPTY"])

    def test_a_profile_of_these_roles_with_an_h2_list_is_refused(self) -> None:
        for _, _, (source, twin), _, _, _ in GOVERNANCE_FORMS:
            for profile_id in (source, twin):
                with self.subTest(profile=profile_id):
                    raw = load_raw()
                    profile_of(raw, profile_id)["sections"] = lists_of(
                        required=["Overview"]
                    )
                    self.assertIn("REGISTRY_FORM_LEGACY_LISTS", semantic_rules_of(raw))

    def test_the_role_template_holds_the_eight_h3_each_with_an_author_prompt(
        self,
    ) -> None:
        text = (
            ROOT / "docs/99.templates/templates/governance/role.template.md"
        ).read_text(encoding="utf-8")
        section = text.split("## Current Contract\n", 1)[1].split("\n## ", 1)[0]
        headings = [x[4:] for x in section.splitlines() if x.startswith("### ")]
        self.assertEqual(tuple(headings), GOVERNANCE_ROLE_H3)
        for part in section.split("\n### ")[1:]:
            self.assertIn("<!-- Author prompt:", part)
        self.assertEqual(
            self.tree_rules("governance-role", self.body(GOVERNANCE_ROLE_TREE)),
            [],
        )


class DataReferenceFormTests(unittest.TestCase):
    """SPEC-0222 WORK-008: the data reports bind the data-reference core role."""

    PATH = PurePosixPath("docs/90.references/data/0001-sample/m0001-sample.md")

    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = load_raw()
        cls.profiles = typed_profiles(cls.raw)
        cls.form = next(
            f
            for f in cls.raw["common_forms"]["forms"]
            if f["form_id"] == "data-reference"
        )

    @staticmethod
    def body(tree=DATA_REFERENCE_TREE) -> str:
        blocks = ["# Reference: Sample"]
        for h2, children in tree:
            blocks.append(f"## {h2}")
            blocks += [f"### {child}\n\nThe {child} text." for child in children]
        return md(*blocks)

    def rules(self, text: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._body_diagnostics(
                self.PATH, self.profiles["reference/data"], text, "published"
            )
        )

    def test_the_form_carries_the_data_reference_core(self) -> None:
        form = self.form
        self.assertEqual(form["core_role"], "data-reference")
        self.assertNotIn("classification", form)
        core = form["core"]
        self.assertEqual(core["purpose"], "생성 자료의 입력·출처·해석")
        self.assertEqual(core["non_goals"], "다른 역할의 상태·정책 정본 대체")
        self.assertEqual(core["status"], "DESIGN_PROPOSAL_NOT_ADOPTED")
        self.assertEqual(
            core["rules"],
            [
                "single-meaning-owner",
                "no-synthetic-evidence",
                "no-release-document-role",
                "no-package-path-runtime-dependency",
            ],
        )
        (table,) = core["tables"]
        self.assertEqual(
            (table["table_id"], table["section_id"], table["required_when"]),
            ("data-reference.schema", "data-reference.interpretation", "always"),
        )
        self.assertEqual(
            [(c["label"], c["key"], c["value_type"]) for c in table["columns"]],
            list(DATA_REFERENCE_SCHEMA),
        )
        self.assertTrue(all(c["required"] for c in table["columns"]))
        for item in form["sections"]:
            for node in (item, *item["children"]):
                with self.subTest(section=node["section_id"]):
                    self.assertEqual(node["condition"], "always")
                    self.assertEqual(node["requiredness"], "required")
                    self.assertEqual(node["core"]["required_when"], "always")
                    self.assertTrue(node["core"]["title_ko"].strip())
                    self.assertTrue(node["core"]["content_rule"].strip())
                    self.assertEqual(
                        "prohibited_content" in node["core"], node["level"] == 2
                    )
        self.assertEqual(form["extensions"], [])
        self.assertEqual(rules_of(self.raw), set())

    def test_the_template_carries_the_core_schema_table_and_local_tables(
        self,
    ) -> None:
        twin = profile_of(self.raw, DATA_REFERENCE[1])
        tables = twin["template_definition"]["tables"]
        (core,) = [t for t in tables if "table_id" in t]
        self.assertEqual(core["table_id"], "data-reference.schema")
        self.assertEqual(
            [(c["key"], c["id"], c["data_type"]) for c in core["columns"]],
            list(DATA_REFERENCE_SCHEMA),
        )
        local = [t["name"] for t in tables if "table_id" not in t]
        self.assertEqual(local, ["Producer", "Source", "Generation command"])
        dropped = load_raw()
        table = next(
            t
            for t in profile_of(dropped, DATA_REFERENCE[1])["template_definition"][
                "tables"
            ]
            if t.get("table_id") == "data-reference.schema"
        )
        table["columns"][2]["data_type"] = "string"
        self.assertIn("REGISTRY_CORE_TABLE", rules_of(dropped))

    def test_the_registry_carries_the_core_table_and_the_record_stays_projected(
        self,
    ) -> None:
        # SPEC-0222 WORK-001: the core table identity stays in the registry.
        tables = profile_of(self.raw, DATA_REFERENCE[1])["template_definition"][
            "tables"
        ]
        (core,) = [t for t in tables if "table_id" in t]
        self.assertEqual(core["table_id"], "data-reference.schema")
        self.assertEqual(
            [c["id"] for c in core["columns"]],
            [key for _, key, _ in DATA_REFERENCE_SCHEMA],
        )
        record = CONTRACTS.template_definition_record(self.raw, DATA_REFERENCE[1])
        self.assertEqual(record_errors(record), [])
        self.assertFalse(any("table_id" in t for t in record["tables"]))

    def test_the_data_profiles_leave_the_reference_report_form(self) -> None:
        for profile_id in DATA_REFERENCE:
            with self.subTest(profile=profile_id):
                self.assertEqual(
                    profile_of(self.raw, profile_id)["document_role"],
                    "data-reference",
                )
        self.assertNotIn(
            "reference-report",
            {f["form_id"] for f in self.raw["common_forms"]["forms"]},
        )

    def test_the_template_passes_the_form_tree(self) -> None:
        twin = self.profiles[DATA_REFERENCE[1]]
        path = PurePosixPath(twin.template)
        text = (ROOT / path).read_text(encoding="utf-8")
        found = MARKDOWN.validate_document_text(text, path, twin, "strict")
        self.assertEqual([item.rule_id for item in found], [])
        self.assertIn("| Field | Type | Unit | Meaning | Limits |", text)

    def test_a_data_report_takes_the_core_tree_and_refuses_the_former_one(
        self,
    ) -> None:
        self.assertEqual(self.rules(self.body()), [])
        former = md(
            "# Reference: Sample",
            *(f"## {h2}\n\nThe {h2} text." for h2 in FORMER_REFERENCE_H2),
        )
        found = self.rules(former)
        self.assertIn("BODY-HEADING-UNSUPPORTED", found)
        self.assertIn("BODY-HEADING-REQUIRED", found)
        missing = (
            ("Purpose", ("Consumers",)),
            *DATA_REFERENCE_TREE[1:],
        )
        self.assertEqual(self.rules(self.body(missing)), ["BODY-H3-REQUIRED"])


class ResearchAuditFormTests(unittest.TestCase):
    """SPEC-0222 WORK-008: the research and audit reports bind their core roles;
    the thirteen published members keep their former H2 until Q07-CUTOVER."""

    RES = "docs/90.references/research/0001-sample/m{:04d}-sample.md"
    AUD = "docs/90.references/audits/0001-sample/m{:04d}-sample.md"

    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = load_raw()
        cls.profiles = typed_profiles(cls.raw)
        cls.forms = {f["form_id"]: f for f in cls.raw["common_forms"]["forms"]}

    @staticmethod
    def body(tree, extra: str = "") -> str:
        blocks = ["# Reference: Sample"]
        for h2, children in tree:
            blocks.append(f"## {h2}")
            blocks += [f"### {child}\n\nThe {child} text." for child in children]
            if h2 == "Analysis" and extra:
                blocks.append(extra)
        return md(*blocks)

    @staticmethod
    def former() -> str:
        return md(
            "# Reference: Sample",
            *(f"## {h2}\n\nThe {h2} text." for h2 in FORMER_REFERENCE_H2),
        )

    def rules(self, profile_id: str, path: str, text: str, status: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._body_diagnostics(
                PurePosixPath(path), self.profiles[profile_id], text, status
            )
        )

    def test_the_forms_carry_their_core_members_and_tables(self) -> None:
        for form_id, purpose, table_id, columns in (
            (
                "research",
                "외부 근거의 적용 가능한 의미",
                "research.sources",
                RESEARCH_SOURCES,
            ),
            ("audit", "주장과 증거 사이 차이", "audit.findings", AUDIT_FINDINGS),
        ):
            form = self.forms[form_id]
            with self.subTest(form=form_id):
                self.assertEqual(form["core_role"], form_id)
                self.assertEqual(form["core"]["purpose"], purpose)
                (table,) = form["core"]["tables"]
                self.assertEqual(
                    (table["table_id"], table["section_id"], table["required_when"]),
                    (table_id, table_id, "always"),
                )
                self.assertEqual(
                    [(c["label"], c["key"], c["value_type"]) for c in table["columns"]],
                    list(columns),
                )
                for item in form["sections"]:
                    for node in (item, *item["children"]):
                        self.assertEqual(node["condition"], "always")
                        self.assertEqual(node["core"]["required_when"], "always")
        classification = self.forms["audit"]["core"]["tables"][0]["columns"][3]
        self.assertEqual(
            classification["allowed_values"],
            ["confirmed", "gap", "conflict", "unverified", "not-applicable"],
        )
        self.assertNotIn("reference-report", self.forms)
        self.assertEqual(rules_of(self.raw), set())

    def test_the_templates_carry_the_core_tables_and_pass_the_tree(self) -> None:
        for twin, header, columns in (
            (RESEARCH[1], "| Source ID | Source | Version |", RESEARCH_SOURCES),
            (AUDIT[1], "| Finding ID | Requirement | Evidence |", AUDIT_FINDINGS),
        ):
            with self.subTest(twin=twin):
                tables = profile_of(self.raw, twin)["template_definition"]["tables"]
                (core,) = [t for t in tables if "table_id" in t]
                self.assertEqual(
                    [(c["key"], c["id"], c["data_type"]) for c in core["columns"]],
                    list(columns),
                )
                typed = self.profiles[twin]
                path = PurePosixPath(typed.template)
                text = (ROOT / path).read_text(encoding="utf-8")
                found = MARKDOWN.validate_document_text(text, path, typed, "strict")
                self.assertEqual([item.rule_id for item in found], [])
                self.assertIn(header, text)

    def test_the_retained_form_binds_only_the_published_members(self) -> None:
        research, audit = "reference/research", "reference/audit"
        self.assertEqual(
            self.rules(research, self.RES.format(1), self.former(), "published"), []
        )
        self.assertEqual(
            self.rules(research, self.RES.format(12), self.former(), "published"), []
        )
        self.assertEqual(
            self.rules(audit, self.AUD.format(1), self.former(), "published"), []
        )
        for profile_id, path, status in (
            (research, self.RES.format(13), "published"),
            (research, self.RES.format(1), "draft"),
            (audit, self.AUD.format(3), "published"),
        ):
            with self.subTest(path=path, status=status):
                self.assertIn(
                    "BODY-HEADING-UNSUPPORTED",
                    self.rules(profile_id, path, self.former(), status),
                )
        self.assertEqual(
            self.rules(
                research, self.RES.format(15), self.body(RESEARCH_TREE), "draft"
            ),
            [],
        )
        self.assertEqual(
            self.rules(audit, self.AUD.format(3), self.body(AUDIT_TREE), "draft"), []
        )

    def test_the_extensions_name_their_authority_and_removal(self) -> None:
        for form_id in ("research", "audit"):
            for extension in self.forms[form_id]["extensions"]:
                with self.subTest(extension=extension["id"]):
                    self.assertEqual(extension["authority_ref"], "SPEC-0222")
                    if extension["kind"] == "retained_form":
                        self.assertIn("Q07-CUTOVER", extension["removal"])
                        self.assertEqual(extension["statuses"], ["published"])

    def test_the_claim_matrix_is_a_local_h3_under_analysis_only(self) -> None:
        research = "reference/research"
        path = self.RES.format(15)
        matrix = "### Claim-Source Matrix\n\nThe matrix text."
        self.assertEqual(
            self.rules(research, path, self.body(RESEARCH_TREE, matrix), "draft"), []
        )
        wrong = self.body(RESEARCH_TREE).replace(
            "### Primary Sources", matrix + "\n\n### Primary Sources"
        )
        self.assertIn("BODY-H3-PARENT", self.rules(research, path, wrong, "draft"))

    def test_artifact_ids_stay_on_the_research_form_only(self) -> None:
        raw = load_raw()
        guide = next(f for f in raw["common_forms"]["forms"] if f["form_id"] == "guide")
        guide["extensions"][0]["artifact_ids"] = ["RES-0001-m0001"]
        self.assertIn("REGISTRY_FORM_EXTENSION", rules_of(raw))


REQUIREMENT_PATH = PurePosixPath(
    "docs/01.requirements/0001-argo-rollouts-progressive-delivery.md"
)
REQUIREMENT_HEADER = REQUIREMENT_COLUMNS
OLD_REQUIREMENT_HEADER = (
    "Requirement ID",
    "Requirement",
    "Priority",
    "Verification intent",
)


def requirement_table(
    header: tuple[str, ...] = REQUIREMENT_HEADER, *, rows: int = 1, kind: str = "FR"
) -> str:
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for number in range(1, rows + 1):
        cells = {
            "Requirement ID": f"REQ-0001-{kind}-{number:04d}",
            "Priority": "must",
        }
        lines.append(
            "| " + " | ".join(cells.get(key, f"A {key} cell.") for key in header) + " |"
        )
    return "\n".join(lines)


def requirement_body(*, quality: bool = True, lineage: bool = True) -> str:
    blocks = [
        "# Requirement title",
        "## Overview",
        "### Problem and Outcome\n\nOperators lack a safe delivery path.",
        "### Stakeholders\n\nPlatform engineers.",
        "## Scope",
        "### In Scope\n\nThe controller.",
        "### Constraints and Exclusions\n\nNo multi-cluster use.",
        "## Requirements",
        "### Functional Requirements\n\n" + requirement_table(),
    ]
    if quality:
        blocks.append("### Quality Requirements\n\n" + requirement_table(kind="NFR"))
    blocks += [
        "## Traceability",
        "### Sources\n\nNo upstream requirement exists.",
        "### Verification Links\n\n- **AD**: [AD 0004](../02.architecture/x.md)"
        "\n\n#### Acceptance Conditions\n\nThe controller is available."
        "\n\n#### Verification Method\n\nEach Acceptance cell names its evidence.",
        "### Lifecycle Traceability\n\n"
        "| Requirement ID | Acceptance criterion |\n"
        "| --- | --- |\n"
        "| REQ-0001-FR-0001 | The controller is available. |",
    ]
    if lineage:
        blocks.append("### Archived Lineage\n\nSPEC-0004 left the tree.")
    return md(*blocks)


class RequirementFormTests(unittest.TestCase):
    """SPEC-0195 VAL-REQFORM-001: the Requirement form, extensions and tables."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = load_raw()
        cls.registry = CONTRACTS.load_registry(ROOT)
        cls.profiles = {p.profile_id: p for p in cls.registry.profiles}
        cls.profile = cls.profiles[REQUIREMENT[0]]

    def tree(self, text: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._body_diagnostics(
                REQUIREMENT_PATH, self.profile, text, "approved"
            )
        )

    def tables(self, text: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._table_diagnostics(
                REQUIREMENT_PATH, self.profile, text
            )
        )

    def test_the_form_has_four_h2_eight_h3_all_required(self) -> None:
        # SPEC-0222 WORK-003: the core requires Quality Requirements always.
        form = next(f for f in self.registry.common_forms if f.form_id == "requirement")
        self.assertEqual(form.title, "Requirement")
        self.assertEqual(
            [(s.title, tuple(c.title for c in s.children)) for s in form.sections],
            list(REQUIREMENT_TREE),
        )
        every = [n for s in form.sections for n in (s, *s.children)]
        self.assertEqual([n.title for n in every if n.requiredness != "required"], [])
        self.assertFalse(any(n.link_only for n in every))
        self.assertEqual(
            [(e.extension_id, e.parent_id, e.title) for e in form.extensions],
            [(e["id"], e["parent_id"], e["title"]) for e in REQUIREMENT_EXTENSIONS],
        )

    def test_the_two_profiles_derive_their_headings_and_keep_the_body_contract(
        self,
    ) -> None:
        titles = tuple(title for title, _ in REQUIREMENT_TREE)
        for profile_id in REQUIREMENT:
            with self.subTest(profile=profile_id):
                raw = next(p for p in self.raw["profiles"] if p["id"] == profile_id)
                self.assertNotIn("sections", raw)
                self.assertEqual(raw["document_role"], "requirement")
                headings = CONTRACTS.heading_contract(self.profiles[profile_id])
                self.assertEqual(headings.required, titles)
                self.assertEqual(headings.allowed, titles)
                contract = raw["relationships"]["body_contract"]
                self.assertEqual(contract["section"], "Traceability")
                self.assertEqual(contract["table_heading"], "Lifecycle Traceability")
                self.assertEqual(
                    contract["required_columns"],
                    ["Requirement ID", "Acceptance criterion"],
                )
                self.assertIsNone(contract["target_link_column"])
                self.assertIsNone(contract["source_link_column"])
                self.assertEqual(
                    contract["enforced_statuses"], ["draft", "in-review", "approved"]
                )
                self.assertEqual(
                    contract["allowed_target_profile_ids"],
                    [],
                )

    def test_the_three_tables_are_recorded_on_the_twin_and_copied_to_the_source(
        self,
    ) -> None:
        twin, source = (self.profiles[i] for i in reversed(REQUIREMENT))
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
            REQUIREMENT_TABLE_KEYS,
        )
        self.assertTrue(all(c.required for t in twin.tables for c in t.columns))
        (priority,) = (c for t in twin.tables for c in t.columns if c.key == "Priority")
        self.assertEqual(
            (priority.data_type, priority.allowed_values),
            ("enum", ("must", "should", "could")),
        )

    def test_the_repository_registry_is_valid_and_its_twin_matches(self) -> None:
        self.assertEqual(rules_of(self.raw), set())
        REGISTRY_CHECK._assert_template_source_parity(self.registry)

    def test_the_twin_definition_names_the_form_and_every_real_consumer(self) -> None:
        definition_ = self.profiles[REQUIREMENT[1]].template_definition
        for path in (
            "docs/99.templates/registry.json",
            "docs/99.templates/contracts/document-profile.schema.json",
            "docs/99.templates/templates/requirements/requirement-package.template.md",
            "docs/01.requirements/0001-argo-rollouts-progressive-delivery.md",
            "docs/01.requirements/0002-argo-notifications-slack.md",
            "docs/01.requirements/0003-workspace-agent-governance-platform.md",
            "docs/01.requirements/0004-current-local-gitops-platform.md",
            "docs/01.requirements/README.md",
            "docs/99.templates/README.md",
            "scripts/document_contracts.py",
            "scripts/document_lifecycle.py",
            "scripts/validate-document-contract-registry.py",
            "scripts/validate-markdown-profiles.py",
            "scripts/validate-links-and-owners.py",
            "scripts/validate-document-lifecycle.py",
            "tests/test_common_form_tree.py",
        ):
            with self.subTest(path=path):
                self.assertIn(path, definition_["consumer_paths"])
        self.assertEqual(
            definition_["policy_refs"],
            [".agents/governance/document-authoring.md", ".agents/governance/sdlc.md"],
        )
        self.assertEqual(
            definition_["vocabulary_refs"], [".agents/knowledge/glossary.md"]
        )

    def test_a_complete_document_passes_and_quality_requirements_is_required(
        self,
    ) -> None:
        body = requirement_body()
        self.assertEqual(self.tree(body), [])
        self.assertEqual(self.tables(body), [])
        without = requirement_body(quality=False)
        self.assertNotIn("Quality Requirements", without)
        self.assertEqual(self.tree(without), ["BODY-H3-REQUIRED"])

    def test_a_priority_outside_the_core_values_is_refused(self) -> None:
        body = requirement_body()
        for value in ("Must", "high", ""):
            with self.subTest(value=value):
                changed = body.replace("| must |", f"| {value} |", 1)
                self.assertNotEqual(changed, body)
                self.assertEqual(self.tables(changed), ["BODY-TABLE-VALUE"])
        # A row of author prompts is the author-prompt check's, not a value.
        prompt_row = (
            "| "
            + " | ".join(
                f"<!-- Author prompt: Name the {key}. -->" for key in REQUIREMENT_HEADER
            )
            + " |"
        )
        prompt = body.replace(
            requirement_table(), requirement_table() + "\n" + prompt_row, 1
        )
        self.assertIn(prompt_row, prompt)
        self.assertEqual(self.tables(prompt), [])

    def test_declared_nfr_needs_its_quality_member(self) -> None:
        frontmatter = (
            '---\ntitle: "Requirement"\nversion: "1.0.0"\ntype: "sdlc/requirement"\n'
            'status: "approved"\nowner: "platform"\nupdated: "2026-11-12"\n'
            'artifact_id: "REQ-0001"\n---\n\n'
        )

        def quality_rules(body):
            return {
                item.rule_id
                for item in MARKDOWN.validate_document_text(
                    frontmatter + body, REQUIREMENT_PATH, self.profile, "strict"
                )
                if item.rule_id.startswith("BODY-QUALITY-")
            }

        trace = "| REQ-0001-FR-0001 | The controller is available. |"
        nfr_trace = "| `REQ-0001-NFR-0001` | The controller is available. |"
        plain = requirement_body(quality=False)
        self.assertEqual(
            quality_rules(plain.replace(trace, nfr_trace)), {"BODY-QUALITY-MEMBER"}
        )
        misplaced = plain.replace(requirement_table(), requirement_table(kind="NFR"))
        self.assertIn("BODY-QUALITY-PLACEMENT", quality_rules(misplaced))
        for kind in ("FR", "IF"):
            with self.subTest(kind=kind):
                misplaced = requirement_body().replace(
                    requirement_table(kind="NFR"), requirement_table(kind=kind)
                )
                self.assertEqual(quality_rules(misplaced), {"BODY-QUALITY-PLACEMENT"})
        correct = requirement_body().replace(trace, trace + "\n" + nfr_trace)
        self.assertEqual(quality_rules(correct), set())
        self.assertEqual(quality_rules(plain + "\nSee REQ-0001-NFR-0001.\n"), set())
        foreign = nfr_trace.replace("REQ-0001-", "REQ-0002-")
        self.assertEqual(quality_rules(plain.replace(trace, foreign)), set())
        hidden = f"<pre>\n| Requirement ID | Acceptance criterion |\n| --- | --- |\n{nfr_trace}\n</pre>"
        self.assertEqual(
            quality_rules(plain.replace(trace, trace + "\n\n" + hidden)), set()
        )

    def test_a_removed_h2_or_a_missing_h3_fails_the_tree(self) -> None:
        old = requirement_body().replace("## Scope", "## Scope and Non-goals")
        found = set(self.tree(old))
        self.assertLessEqual(
            {"BODY-HEADING-REQUIRED", "BODY-HEADING-UNSUPPORTED"}, found
        )
        lost = requirement_body().replace(
            "### Sources\n\nNo upstream requirement exists.\n\n",
            "",
        )
        self.assertEqual(self.tree(lost), ["BODY-H3-REQUIRED"])

    def test_an_h3_under_the_wrong_h2_is_refused(self) -> None:
        body = requirement_body()
        quality = "### Quality Requirements\n\n" + requirement_table(kind="NFR")
        moved = body.replace(quality + "\n\n", "").replace(
            "## Scope", quality + "\n\n## Scope"
        )
        # SPEC-0222 WORK-003: Quality Requirements is required, so moving it
        # also leaves Requirements without it.
        self.assertEqual(self.tree(moved), ["BODY-H3-PARENT", "BODY-H3-REQUIRED"])

    def test_archived_lineage_and_lifecycle_traceability_belong_under_traceability(
        self,
    ) -> None:
        body = requirement_body()
        lineage = "### Archived Lineage\n\nSPEC-0004 left the tree.\n"
        for heading in ("## Overview", "## Scope", "## Requirements"):
            with self.subTest(before=heading):
                moved = body.replace(lineage, "").replace(
                    heading, lineage + "\n" + heading, 1
                )
                self.assertEqual(self.tree(moved), ["BODY-H3-PARENT"])
        self.assertEqual(self.tree(requirement_body(lineage=False)), [])

    def test_the_old_four_column_header_is_refused_and_the_new_one_accepted(
        self,
    ) -> None:
        old = requirement_body().replace(
            requirement_table(), requirement_table(OLD_REQUIREMENT_HEADER)
        )
        self.assertEqual(self.tables(old), ["BODY-TABLE-COLUMNS"])
        body = requirement_body().replace(
            requirement_table(), requirement_table(REQUIREMENT_HEADER)
        )
        self.assertEqual(self.tables(body), [])
        # SPEC-0222 WORK-003: the core requires Priority, so the former
        # four-column header without it no longer passes.
        for header in (
            REQUIREMENT_HEADER[:-1],
            REQUIREMENT_HEADER[:-2],
            (
                REQUIREMENT_HEADER[0],
                REQUIREMENT_HEADER[2],
                REQUIREMENT_HEADER[1],
                *REQUIREMENT_HEADER[3:],
            ),
            (*REQUIREMENT_HEADER, "Note"),
            (REQUIREMENT_HEADER[0], "Priority", *REQUIREMENT_HEADER[1:4]),
        ):
            with self.subTest(header=header):
                body = requirement_body().replace(
                    requirement_table(), requirement_table(header)
                )
                self.assertEqual(self.tables(body), ["BODY-TABLE-COLUMNS"])

    def test_a_header_only_functional_table_fails_and_a_header_only_quality_passes(
        self,
    ) -> None:
        def rules(text: str) -> list[str]:
            # The core table counts rows across both H3; the quality check keeps
            # the functional minimum of one member (SPEC-0222 WORK-003).
            return sorted(
                [
                    *self.tables(text),
                    *(
                        item.rule_id
                        for item in MARKDOWN._requirement_quality_diagnostics(
                            REQUIREMENT_PATH, self.profile, text
                        )
                    ),
                ]
            )

        body = requirement_body()
        empty_quality = body.replace(
            requirement_table(kind="NFR"), requirement_table(kind="NFR", rows=0)
        )
        self.assertEqual(rules(empty_quality), [])
        empty_functional = body.replace(requirement_table(), requirement_table(rows=0))
        self.assertEqual(rules(empty_functional), ["BODY-TABLE-ROWS"])
        both = empty_functional.replace(
            requirement_table(kind="NFR"), requirement_table(kind="NFR", rows=0)
        )
        self.assertEqual(rules(both), ["BODY-TABLE-ROWS", "BODY-TABLE-ROWS"])

    def test_the_body_contract_table_is_not_read_as_a_requirement_table(self) -> None:
        body = requirement_body()
        self.assertIn("| Requirement ID | Acceptance criterion |", body)
        self.assertNotIn("Downstream owner", body)
        self.assertEqual(self.tables(body), [])

    def test_the_old_three_column_body_contract_table_fails_the_column_check(
        self,
    ) -> None:
        old = requirement_body().replace(
            "| Requirement ID | Acceptance criterion |\n| --- | --- |\n"
            "| REQ-0001-FR-0001 | The controller is available. |",
            "| Requirement ID | Acceptance criterion | Downstream owner |\n"
            "| --- | --- | --- |\n"
            "| REQ-0001-FR-0001 | The controller is available. | AD 0004 |",
        )
        self.assertIn("Downstream owner", old)

        def contract(text: str) -> list[str]:
            return sorted(
                item.rule_id
                for item in MARKDOWN._body_contract_diagnostics(
                    REQUIREMENT_PATH, self.profile, text, "approved", "registry"
                )
            )

        self.assertEqual(contract(requirement_body()), [])
        self.assertIn("BODY-CONTRACT-COLUMNS", contract(old))

    def test_the_template_passes_the_form_tree_and_carries_no_archived_lineage(
        self,
    ) -> None:
        twin = self.profiles[REQUIREMENT[1]]
        path = PurePosixPath(twin.template)
        text = (ROOT / path).read_text(encoding="utf-8")
        self.assertEqual(
            [
                item.rule_id
                for item in MARKDOWN.validate_document_text(text, path, twin, "strict")
            ],
            [],
        )
        self.assertNotIn("Archived Lineage", text)
        self.assertNotIn("Verification intent", text)
        self.assertNotIn("| Requirement | Priority |", text)
        for h3 in (h for _, children in REQUIREMENT_TREE for h in children):
            with self.subTest(h3=h3):
                self.assertRegex(
                    text, rf"(?m)^### {re.escape(h3)}\n\n<!-- Author prompt:"
                )


ARCHITECTURE_PATH = PurePosixPath(
    "docs/02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md"
)


def architecture_table(header: tuple[str, ...], *, rows: int = 1) -> str:
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for number in range(rows):
        lines.append("| " + " | ".join(f"{key} {number}" for key in header) + " |")
    return "\n".join(lines)


def architecture_body(
    *,
    constraints: int = 0,
    scenarios: int = 1,
    lineage: bool = True,
    quality_header: tuple[str, ...] = ARCHITECTURE_TABLE_KEYS["Quality Scenarios"][1],
) -> str:
    blocks = ["# Description title"]
    for h2, children in ARCHITECTURE_TREE:
        blocks.append(f"## {h2}")
        for h3 in children:
            text = f"The {h3} of the system."
            if h3 == "Constraints":
                text += "\n\n" + architecture_table(
                    ARCHITECTURE_TABLE_KEYS["Constraints"][1], rows=constraints
                )
            if h3 == "Scenarios":
                text += "\n\n" + architecture_table(quality_header, rows=scenarios)
            blocks.append(f"### {h3}\n\n{text}")
    blocks.append(
        "### Lifecycle Traceability\n\n"
        + architecture_table(ARCHITECTURE_TABLE_KEYS["Lifecycle Traceability"][1])
    )
    if lineage:
        blocks.append("### Archived Lineage\n\nSPEC-0004 left the tree.")
    return md(*blocks)


class ArchitectureFormTests(unittest.TestCase):
    """SPEC-0197 VAL-ADFORM-001: the Architecture form, extensions and tables."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = load_raw()
        cls.registry = CONTRACTS.load_registry(ROOT)
        cls.profiles = {p.profile_id: p for p in cls.registry.profiles}
        cls.profile = cls.profiles[ARCHITECTURE[0]]

    def tree(self, text: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._body_diagnostics(
                ARCHITECTURE_PATH, self.profile, text, "active"
            )
        )

    def tables(self, text: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._table_diagnostics(
                ARCHITECTURE_PATH, self.profile, text
            )
        )

    def test_the_form_has_six_h2_twelve_h3_all_required_and_two_extensions(
        self,
    ) -> None:
        form = next(
            f for f in self.registry.common_forms if f.form_id == "architecture"
        )
        self.assertEqual(form.title, "Architecture")
        self.assertEqual(
            [(s.title, tuple(c.title for c in s.children)) for s in form.sections],
            list(ARCHITECTURE_TREE),
        )
        every = [n for s in form.sections for n in (s, *s.children)]
        self.assertEqual([n.title for n in every if n.requiredness != "required"], [])
        self.assertFalse(any(n.link_only for n in every))
        self.assertEqual(
            [(e.extension_id, e.parent_id, e.title) for e in form.extensions],
            [(e["id"], e["parent_id"], e["title"]) for e in ARCHITECTURE_EXTENSIONS],
        )

    def test_the_two_profiles_derive_their_headings_and_keep_the_body_contract(
        self,
    ) -> None:
        titles = tuple(title for title, _ in ARCHITECTURE_TREE)
        for profile_id in ARCHITECTURE:
            with self.subTest(profile=profile_id):
                raw = next(p for p in self.raw["profiles"] if p["id"] == profile_id)
                self.assertNotIn("sections", raw)
                self.assertEqual(raw["document_role"], "architecture")
                headings = CONTRACTS.heading_contract(self.profiles[profile_id])
                self.assertEqual(headings.required, titles)
                self.assertEqual(headings.allowed, titles)
                contract = raw["relationships"]["body_contract"]
                self.assertEqual(contract["section"], "Decisions and Adoption")
                self.assertEqual(contract["table_heading"], "Lifecycle Traceability")
                self.assertEqual(
                    contract["required_columns"],
                    [
                        "Upstream requirement",
                        "Quality attribute or boundary",
                        "ADR / Spec",
                    ],
                )
                self.assertEqual(contract["source_link_column"], "Upstream requirement")
                self.assertEqual(contract["target_link_column"], "ADR / Spec")
                self.assertEqual(
                    contract["enforced_statuses"], ["draft", "in-review", "active"]
                )

    def test_the_three_tables_are_recorded_on_the_twin_and_copied_to_the_source(
        self,
    ) -> None:
        twin, source = (self.profiles[i] for i in reversed(ARCHITECTURE))
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
            ARCHITECTURE_TABLE_KEYS,
        )
        self.assertTrue(all(c.required for t in twin.tables for c in t.columns))

    def test_the_repository_registry_is_valid_and_its_twin_matches(self) -> None:
        self.assertEqual(rules_of(self.raw), set())
        REGISTRY_CHECK._assert_template_source_parity(self.registry)

    def test_the_twin_definition_names_the_form_version_and_every_real_consumer(
        self,
    ) -> None:
        definition_ = self.profiles[ARCHITECTURE[1]].template_definition
        self.assertEqual(definition_["contract_id"], "COMMON-DOC-FORM-1")
        self.assertEqual(definition_["contract_version"], "2.0.0")
        for path in (
            "docs/99.templates/registry.json",
            "docs/99.templates/contracts/document-profile.schema.json",
            "docs/99.templates/templates/architecture/description.template.md",
            "docs/02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md",
            "docs/02.architecture/descriptions/0005-argo-notifications-slack.md",
            "docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md",
            "docs/02.architecture/descriptions/0007-current-local-gitops-platform.md",
            "docs/02.architecture/README.md",
            "docs/99.templates/README.md",
            "scripts/document_contracts.py",
            "scripts/document_lifecycle.py",
            "scripts/validate-document-contract-registry.py",
            "scripts/validate-markdown-profiles.py",
            "scripts/validate-links-and-owners.py",
            "scripts/validate-document-lifecycle.py",
            "tests/test_common_form_tree.py",
        ):
            with self.subTest(path=path):
                self.assertIn(path, definition_["consumer_paths"])
                self.assertTrue((ROOT / path).is_file())
        self.assertEqual(
            definition_["policy_refs"],
            [".agents/governance/document-authoring.md", ".agents/governance/sdlc.md"],
        )
        self.assertEqual(
            definition_["vocabulary_refs"], [".agents/knowledge/glossary.md"]
        )

    def test_a_complete_document_passes_with_and_without_rows_or_lineage(self) -> None:
        for kwargs in ({}, {"constraints": 2}, {"scenarios": 0}, {"lineage": False}):
            with self.subTest(kwargs=kwargs):
                body = architecture_body(**kwargs)
                self.assertEqual(self.tree(body), [])
                self.assertEqual(self.tables(body), [])

    def test_a_previous_h2_or_a_missing_h3_fails_the_tree(self) -> None:
        old = architecture_body().replace("## Structure", "## Data Architecture")
        self.assertLessEqual(
            {"BODY-HEADING-REQUIRED", "BODY-HEADING-UNSUPPORTED"}, set(self.tree(old))
        )
        lost = architecture_body().replace(
            "### Failure and Recovery\n\nThe Failure and Recovery of the system.\n\n",
            "",
        )
        self.assertEqual(self.tree(lost), ["BODY-H3-REQUIRED"])

    def test_archived_lineage_and_lifecycle_traceability_belong_under_decisions_and_adoption(
        self,
    ) -> None:
        body = architecture_body()
        lineage = "### Archived Lineage\n\nSPEC-0004 left the tree.\n"
        for heading in (
            "## Context and Boundaries",
            "## Structure",
            "## Quality Scenarios",
        ):
            with self.subTest(before=heading):
                moved = body.replace(lineage, "").replace(
                    heading, lineage + "\n" + heading, 1
                )
                self.assertEqual(self.tree(moved), ["BODY-H3-PARENT"])

    def test_a_wrong_quality_scenarios_or_constraints_header_is_refused(self) -> None:
        keys = ARCHITECTURE_TABLE_KEYS["Quality Scenarios"][1]
        for header in (keys[:-1], (*keys, "Note")):
            with self.subTest(header=header):
                body = architecture_body(quality_header=header)
                self.assertEqual(self.tables(body), ["BODY-TABLE-COLUMNS"])
        wrong = architecture_body(constraints=1).replace(
            "| Architecture ID | Constraint | Affected Components |",
            "| Architecture ID | Constraint | Owner |",
        )
        self.assertEqual(self.tables(wrong), ["BODY-TABLE-COLUMNS"])

    def test_the_template_passes_the_form_tree_and_carries_no_archived_lineage(
        self,
    ) -> None:
        twin = self.profiles[ARCHITECTURE[1]]
        path = PurePosixPath(twin.template)
        text = (ROOT / path).read_text(encoding="utf-8")
        self.assertEqual(
            [
                item.rule_id
                for item in MARKDOWN.validate_document_text(text, path, twin, "strict")
            ],
            [],
        )
        self.assertNotIn("Archived Lineage", text)
        for h2 in ("Boundaries & Non-goals", "System Overview & Context"):
            self.assertNotIn(f"## {h2}", text)
        for h3 in (h for _, children in ARCHITECTURE_TREE for h in children):
            with self.subTest(h3=h3):
                self.assertRegex(
                    text, rf"(?m)^### {re.escape(h3)}\n\n<!-- Author prompt:"
                )


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
        # SPEC-0222: the twin rule stays silent; the core rule still asks every
        # guide template for the core guide.steps table.
        self.assertEqual(rules_of(raw), {"REGISTRY_CORE_TABLE"})


class RetainedFormTests(unittest.TestCase):
    """W03-D02, W03-D52: a retained form applies by status and, when bounded, identity."""

    INSIDE = PurePosixPath("docs/02.architecture/decisions/0050-temporary.md")
    OUTSIDE = PurePosixPath("docs/02.architecture/decisions/0062-temporary.md")
    GUIDE_PATH = PurePosixPath("docs/05.operations/guides/0099-temporary.md")
    LEGACY = md(
        "# Decision title",
        "## Context\n\nWhy we decide.",
        "## Decision\n\nWe decide.",
        "## Consequences\n\nWhat follows.",
    )
    TREE = md("# Decision title", "## Decision", "### Decision Statement\n\nWe decide.")

    @staticmethod
    def retained(bound: str | None) -> dict:
        item = {
            "id": "a-legacy",
            "kind": "retained_form",
            "condition": "accepted decisions keep their H2 headings",
            "owner": "platform",
            "verification": "tests/test_common_form_tree.py",
            "review": "each release",
            "removal": "when no accepted ADR keeps the old headings",
            "authority_ref": "ADR-0059",
            "statuses": ["accepted"],
            "retained_sections": {
                "required": ["Context", "Decision", "Consequences"],
                "optional": [],
                "forbidden": [],
            },
        }
        if bound is not None:
            item["identity_bound"] = bound
        return item

    @staticmethod
    def sections() -> list[dict]:
        return [
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

    @classmethod
    def setUpClass(cls) -> None:
        raw = with_form(
            load_raw(),
            "adr",
            ADR,
            cls.sections(),
            extensions=[cls.retained(ADR_BOUND)],
        )
        cls.profile = typed_profiles(raw)[ADR[0]]
        # The kind as SPEC-0168 defined it: no bound, selected by status alone.
        unbounded = with_form(
            load_raw(),
            "guide",
            GUIDE,
            cls.sections(),
            extensions=[cls.retained(None)],
        )
        cls.unbounded = typed_profiles(unbounded)[GUIDE[0]]

    def found(
        self, text: str, status: str, path: PurePosixPath | None = None
    ) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._body_diagnostics(
                path or self.INSIDE, self.profile, text, status
            )
        )

    def test_retained_form_applies_to_its_statuses_inside_the_range(self) -> None:
        self.assertEqual(self.found(self.LEGACY, "accepted"), [])
        self.assertEqual(
            self.found(self.LEGACY, "proposed"),
            [
                "BODY-H3-REQUIRED",
                "BODY-HEADING-UNSUPPORTED",
                "BODY-HEADING-UNSUPPORTED",
            ],
        )

    def test_an_accepted_adr_inside_the_range_passes_the_retained_form_and_fails_the_tree(
        self,
    ) -> None:
        self.assertEqual(self.found(self.LEGACY, "accepted", self.INSIDE), [])
        self.assertEqual(
            self.found(self.TREE, "accepted", self.INSIDE),
            ["BODY-HEADING-REQUIRED", "BODY-HEADING-REQUIRED"],
        )

    def test_an_accepted_adr_outside_the_range_passes_the_tree_and_fails_the_retained_form(
        self,
    ) -> None:
        self.assertEqual(self.found(self.TREE, "accepted", self.OUTSIDE), [])
        self.assertEqual(
            self.found(self.LEGACY, "accepted", self.OUTSIDE),
            [
                "BODY-H3-REQUIRED",
                "BODY-HEADING-UNSUPPORTED",
                "BODY-HEADING-UNSUPPORTED",
            ],
        )

    def test_the_tree_applies_to_every_other_status_whatever_the_identity(self) -> None:
        for path in (self.INSIDE, self.OUTSIDE):
            with self.subTest(path=path.name):
                self.assertEqual(self.found(self.TREE, "proposed", path), [])
                self.assertEqual(self.found(self.TREE, "rejected", path), [])

    def test_an_unknown_status_uses_the_tree(self) -> None:
        self.assertEqual(self.found(self.TREE, ""), [])

    def test_a_template_has_no_identity_and_uses_the_tree(self) -> None:
        template = PurePosixPath(self.profile.template)
        self.assertEqual(
            sorted(
                i.rule_id
                for i in MARKDOWN._body_diagnostics(
                    template, self.profile, self.LEGACY, "accepted"
                )
            ),
            [
                "BODY-H3-REQUIRED",
                "BODY-HEADING-UNSUPPORTED",
                "BODY-HEADING-UNSUPPORTED",
            ],
        )

    def test_a_retained_form_without_a_bound_still_selects_by_status(self) -> None:
        def found(text: str, status: str, path: PurePosixPath) -> list[str]:
            return sorted(
                i.rule_id
                for i in MARKDOWN._body_diagnostics(path, self.unbounded, text, status)
            )

        for path in (self.GUIDE_PATH, self.INSIDE, self.OUTSIDE):
            with self.subTest(path=path.name):
                self.assertEqual(found(self.LEGACY, "accepted", path), [])
                self.assertEqual(
                    found(self.TREE, "accepted", path),
                    ["BODY-HEADING-REQUIRED", "BODY-HEADING-REQUIRED"],
                )
                self.assertEqual(found(self.TREE, "proposed", path), [])

    def test_status_reaches_the_check_from_the_frontmatter(self) -> None:
        def document(status: str, number: str, body: str) -> str:
            return (
                "---\n"
                'title: "Decision title"\nversion: "1.0.0"\n'
                'type: "sdlc/architecture-decision"\n'
                f'status: "{status}"\nowner: "platform"\nupdated: "2026-11-12"\n'
                f'artifact_id: "ADR-{number}"\n---\n\n' + body
            )

        def body_rules(status: str, number: str, body: str) -> list[str]:
            relative = PurePosixPath(
                f"docs/02.architecture/decisions/{number}-temporary.md"
            )
            with tempfile.TemporaryDirectory() as root:
                path = Path(root) / relative
                path.parent.mkdir(parents=True)
                path.write_text(document(status, number, body), encoding="utf-8")
                found = MARKDOWN.validate_document(
                    Path(root), relative, self.profile, "strict"
                )
            return sorted(i.rule_id for i in found if i.rule_id.startswith("BODY-"))

        self.assertEqual(body_rules("accepted", "0050", self.LEGACY), [])
        self.assertEqual(body_rules("accepted", "0062", self.TREE), [])
        self.assertNotEqual(body_rules("accepted", "0062", self.LEGACY), [])
        self.assertEqual(
            body_rules("proposed", "0050", self.LEGACY),
            [
                "BODY-H3-REQUIRED",
                "BODY-HEADING-UNSUPPORTED",
                "BODY-HEADING-UNSUPPORTED",
            ],
        )
        self.assertEqual(body_rules("proposed", "0050", self.TREE), [])


class IdentityBoundTests(unittest.TestCase):
    """SPEC-0198: the bound is an anchored expression; the ADR role's bound is closed."""

    RULE = "REGISTRY_FORM_EXTENSION"

    @staticmethod
    def with_bound(bound: str | None) -> dict:
        raw = load_raw()
        form_ = next(f for f in raw["common_forms"]["forms"] if f["form_id"] == "adr")
        retained = next(e for e in form_["extensions"] if e["kind"] == "retained_form")
        if bound is None:
            retained.pop("identity_bound")
        else:
            retained["identity_bound"] = bound
        return raw

    def test_the_repository_bound_matches_exactly_adr_0001_to_adr_0061(self) -> None:
        raw = load_raw()
        form_ = next(f for f in raw["common_forms"]["forms"] if f["form_id"] == "adr")
        retained = next(e for e in form_["extensions"] if e["kind"] == "retained_form")
        self.assertEqual(retained["identity_bound"], ADR_BOUND)
        matched = [n for n in range(0, 10000) if re.search(ADR_BOUND, f"ADR-{n:04d}")]
        self.assertEqual(matched, list(range(1, 62)))
        self.assertEqual(rules_of(raw), set())

    def test_an_unanchored_or_uncompilable_bound_is_refused(self) -> None:
        for bound in (
            "ADR-00[0-5][0-9]",
            "^ADR-00[0-5][0-9]",
            "ADR-00[0-5][0-9]$",
            "^ADR-(0001$",
        ):
            with self.subTest(bound=bound):
                self.assertIn(self.RULE, rules_of(self.with_bound(bound)))

    def test_a_retained_form_of_the_adr_role_without_a_bound_is_refused(self) -> None:
        self.assertIn(self.RULE, rules_of(self.with_bound(None)))

    def test_a_bound_of_the_adr_role_that_matches_adr_0062_is_refused(self) -> None:
        for bound in (
            "^ADR-[0-9]{4}$",
            "^ADR-006[0-2]$",
            "^ADR-00(?:0[1-9]|[1-6][0-9])$",
        ):
            with self.subTest(bound=bound):
                self.assertIn(self.RULE, rules_of(self.with_bound(bound)))

    def test_a_retained_form_of_another_role_needs_no_bound(self) -> None:
        raw = with_form(
            load_raw(),
            "guide",
            GUIDE,
            RetainedFormTests.sections(),
            extensions=[RetainedFormTests.retained(None)],
        )
        self.assertNotIn(self.RULE, rules_of(raw))

    def test_a_local_h3_extension_cannot_carry_a_bound(self) -> None:
        raw = load_raw()
        form_ = next(f for f in raw["common_forms"]["forms"] if f["form_id"] == "adr")
        local = next(e for e in form_["extensions"] if e["kind"] == "local_h3")
        local["identity_bound"] = ADR_BOUND
        self.assertNotEqual(rules_of(raw), set())


ADR_PATH = PurePosixPath("docs/02.architecture/decisions/0062-example.md")


def adr_body(*, supersession: bool = True) -> str:
    """A form-tree ADR: Sources and the optional Supersession stay as H4 under
    Authority and Effect, and Lifecycle Traceability is the local H3 of Decision."""

    blocks = ["# ADR-0062: Decision title"]
    for h2, children in ADR_TREE:
        blocks.append(f"## {h2}")
        for h3 in children:
            blocks.append(f"### {h3}\n\nThe {h3} of the decision.")
            if h3 == "Trade-offs":
                blocks.append(
                    "| Option | Benefit | Cost and Risk | Reason |\n"
                    "| --- | --- | --- | --- |\n"
                    "| One way | It is simple. | It is slow. | Chosen. |"
                )
            if h3 == "Authority and Effect":
                blocks.append("#### Sources\n\nThe sources of the decision.")
                if supersession:
                    blocks.append("#### Supersession\n\nNo predecessor.")
        if h2 == "Decision":
            blocks.append(
                "### Lifecycle Traceability\n\n"
                "| Decision lineage | Replacement relation | Affected Spec |\n"
                "| --- | --- | --- |\n"
                "| Architecture owner | N/A | N/A |"
            )
    return md(*blocks)


class AdrFormTests(unittest.TestCase):
    """SPEC-0198 VAL-ADRFORM-001 and VAL-ADRFORM-002: the ADR form and its template."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = load_raw()
        cls.registry = CONTRACTS.load_registry(ROOT)
        cls.profiles = {p.profile_id: p for p in cls.registry.profiles}
        cls.profile = cls.profiles[ADR[0]]
        cls.form = next(f for f in cls.registry.common_forms if f.form_id == "adr")

    def test_the_form_has_the_four_core_h2_and_eight_required_h3(self) -> None:
        self.assertEqual(self.form.title, "ADR")
        self.assertEqual(
            [(s.title, tuple(c.title for c in s.children)) for s in self.form.sections],
            list(ADR_TREE),
        )
        every = [n for s in self.form.sections for n in (s, *s.children)]
        self.assertEqual([n.title for n in every if n.requiredness != "required"], [])
        self.assertFalse(any(n.link_only for n in every))

    def test_the_form_registers_one_local_h3_and_one_bounded_retained_form(
        self,
    ) -> None:
        local, retained = self.form.extensions
        self.assertEqual(
            (local.kind, local.parent_id, local.title),
            ("local_h3", "decision.decision", "Lifecycle Traceability"),
        )
        self.assertEqual(
            (retained.kind, retained.statuses, retained.identity_bound),
            ("retained_form", ("accepted",), ADR_BOUND),
        )
        # The retained ADRs keep reading their lifecycle table under Traceability.
        self.assertEqual(
            retained.body_contract, ("Traceability", "Lifecycle Traceability")
        )
        self.assertEqual(
            retained.retained.required, tuple(ADR_RETAINED_LISTS["required"])
        )
        self.assertFalse(retained.retained.ordered)

    def test_the_two_profiles_carry_no_h2_list_and_keep_the_body_contract(self) -> None:
        for profile_id in ADR:
            with self.subTest(profile=profile_id):
                raw = next(p for p in self.raw["profiles"] if p["id"] == profile_id)
                self.assertNotIn("sections", raw)
                self.assertEqual(raw["document_role"], "adr")
                contract = raw["relationships"]["body_contract"]
                self.assertEqual(contract["section"], "Decision")
                self.assertEqual(contract["table_heading"], "Lifecycle Traceability")
                self.assertEqual(
                    contract["required_columns"],
                    ["Decision lineage", "Replacement relation", "Affected Spec"],
                )
                self.assertEqual(contract["enforced_statuses"], ["proposed"])

    def test_the_tables_are_recorded_on_the_twin_and_copied_to_the_source(
        self,
    ) -> None:
        twin, source = (self.profiles[i] for i in reversed(ADR))
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
            ADR_TABLE_KEYS,
        )
        self.assertTrue(all(c.required for t in twin.tables for c in t.columns))

    def test_the_stored_definition_and_derived_record_preserve_the_adr_contract(
        self,
    ) -> None:
        definition_ = profile_of(self.raw, ADR[1])["template_definition"]
        self.assertEqual(
            sorted(definition_),
            sorted(
                [
                    "purpose",
                    "responsibility",
                    "non_goals",
                    "policy_refs",
                    "vocabulary_refs",
                    "applicability",
                    "consumer_paths",
                    "validation",
                    "migration",
                    "tables",
                    "contract_id",
                    "contract_version",
                ]
            ),
        )
        self.assertEqual(definition_["contract_id"], "COMMON-DOC-FORM-1")
        self.assertEqual(definition_["contract_version"], "2.0.0")
        self.assertEqual(
            definition_["policy_refs"],
            [".agents/governance/document-authoring.md", ".agents/governance/sdlc.md"],
        )
        for path in definition_["consumer_paths"]:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file())
        record = CONTRACTS.template_definition_record(self.raw, ADR[1])
        self.assertEqual(
            [e["delta"].split(" ")[:2] for e in record["extensions"]],
            [
                ["local_h3", "adr-lifecycle-traceability"],
                ["retained_form", "adr-accepted-retained-form"],
            ],
        )
        self.assertEqual(rules_of(self.raw), set())

    def test_a_complete_document_passes_in_every_status_with_or_without_supersession(
        self,
    ) -> None:
        for status in ("proposed", "accepted", "rejected"):
            for kwargs in ({}, {"supersession": False}):
                with self.subTest(status=status, kwargs=kwargs):
                    body = adr_body(**kwargs)
                    self.assertEqual(
                        sorted(
                            i.rule_id
                            for i in MARKDOWN._body_diagnostics(
                                ADR_PATH, self.profile, body, status
                            )
                        ),
                        [],
                    )

    def test_an_accepted_adr_after_the_range_fails_the_retained_headings(self) -> None:
        legacy = md(
            "# ADR-0062: Decision title",
            *(f"## {h}\n\nThe {h} text." for h in ADR_RETAINED_LISTS["required"]),
        )
        found = {
            i.rule_id
            for i in MARKDOWN._body_diagnostics(
                ADR_PATH, self.profile, legacy, "accepted"
            )
        }
        self.assertIn("BODY-HEADING-UNSUPPORTED", found)
        inside = PurePosixPath("docs/02.architecture/decisions/0061-example.md")
        self.assertEqual(
            [
                i.rule_id
                for i in MARKDOWN._body_diagnostics(
                    inside, self.profile, legacy, "accepted"
                )
            ],
            [],
        )

    def test_the_36_accepted_adrs_and_the_template_gain_no_diagnostic(self) -> None:
        for path in sorted((ROOT / "docs/02.architecture/decisions").glob("00*.md")):
            relative = PurePosixPath(path.relative_to(ROOT).as_posix())
            with self.subTest(adr=relative.name):
                self.assertEqual(
                    MARKDOWN.validate_document(ROOT, relative, self.profile, "strict"),
                    [],
                )
        twin = self.profiles[ADR[1]]
        path = PurePosixPath(twin.template)
        text = (ROOT / path).read_text(encoding="utf-8")
        self.assertEqual(
            [
                i.rule_id
                for i in MARKDOWN.validate_document_text(text, path, twin, "strict")
            ],
            [],
        )

    def test_the_template_places_an_author_prompt_under_every_h3(self) -> None:
        text = (ROOT / self.profiles[ADR[1]].template).read_text(encoding="utf-8")
        for h2, children in ADR_TREE:
            self.assertRegex(text, rf"(?m)^## {re.escape(h2)}$")
            for h3 in children:
                with self.subTest(h3=h3):
                    self.assertRegex(
                        text, rf"(?m)^### {re.escape(h3)}\n\n<!-- Author prompt:"
                    )
        # SPEC-0222: the former Traceability H3 stay as H4 under Authority and
        # Effect, and the local Lifecycle Traceability H3 closes Decision.
        self.assertRegex(
            text,
            r"(?s)### Authority and Effect\n.*\n#### Sources\n\n<!-- Author prompt:"
            r".*\n#### Supersession\n\n<!-- Author prompt:"
            r".*\n### Lifecycle Traceability\n.*\n## Consequences\n",
        )
        for gone in (
            "## Overview",
            "## Explicit Non-goals",
            "## Alternatives",
            "## Traceability",
        ):
            self.assertNotIn(gone, text)


# SPEC-0196 (W03-D56, W03-D65): the full TemplateDefinition record.
RECORD_SCHEMA = ROOT / "docs/99.templates/contracts/template-definition.schema.json"
# SPEC-0222: the research, audit and data-reference core-role forms outside the
# first sixteen also take the common contract.
COMMON_RECORD_ROLES = frozenset(FORM_IDS[:16]) | {"research", "audit", "data-reference"}
SDLC_ROLES = frozenset(FORM_IDS[:6])
HEADINGS_EXTENSION = {
    "id": "provider-native-empty-headings",
    "condition": "the files are read by a native runtime whose own format fixes their shape",
    "owner": "platform",
    "verification": "REGISTRY_TEMPLATE_EXTENSION",
    "review": "when a provider's native file format changes",
    "removal": "when provider-native receives a form in common_forms",
}


def current_rules(raw: dict) -> set[str]:
    return {item.rule_id for item in CONTRACTS.current_registry_diagnostics(ROOT, raw)}


def record_schema() -> dict:
    return json.loads(RECORD_SCHEMA.read_text("utf-8"))


def record_errors(record: dict) -> list:
    return schema_errors(record_schema(), record)


def form_headings(item: dict) -> dict:
    """The form section as a package heading: every field but the local flag and
    the section core members, which stay in the registry (SPEC-0222)."""

    return {
        **{
            key: value
            for key, value in item.items()
            if key not in {"link_only", "children", "core"}
        },
        "children": [form_headings(child) for child in item["children"]],
    }


class TemplateRecordTests(unittest.TestCase):
    """VAL-TDREC-001: a record per template, derived from its owners."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = load_raw()
        cls.forms = {item["form_id"]: item for item in cls.raw["common_forms"]["forms"]}
        cls.profiles = {item["id"]: item for item in cls.raw["profiles"]}
        cls.templates = [
            item
            for item in cls.raw["profiles"]
            if item["mode"] == "template" and "template_definition" in item
        ]
        cls.records = {
            item["id"]: CONTRACTS.template_definition_record(cls.raw, item["id"])
            for item in cls.templates
        }

    def tolerated(self, profile: dict, errors: list) -> list:
        """The findings left once the one tolerated `headings` finding is dropped."""

        if profile["document_role"] in self.forms:
            return errors
        return [
            error
            for error in errors
            if not (error.validator == "minItems" and list(error.path) == ["headings"])
        ]

    def test_the_record_fields_follow_the_required_list_of_the_schema(
        self,
    ) -> None:
        self.assertEqual(
            list(CONTRACTS.TEMPLATE_RECORD_FIELDS), record_schema()["required"]
        )

    def test_current_registry_exposes_the_normalized_template_record(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        profile_id = "common/template-readme-research-pack"
        profile = next(p for p in registry.profiles if p.profile_id == profile_id)
        self.assertEqual(profile.template_definition, self.records[profile_id])
        closure = next(
            section
            for section in profile.template_definition["headings"]
            if section["title"] == PACK_CLOSURES[PACK_FORM[0]]
        )
        self.assertEqual(
            closure["applicability"],
            {"source_profile_ids": [PACK_FORM[0]], "required": True},
        )

    def test_every_template_with_a_definition_has_a_valid_record(
        self,
    ) -> None:
        self.assertTrue(self.templates)
        for profile in self.templates:
            with self.subTest(template=profile["id"]):
                record = self.records[profile["id"]]
                self.assertEqual(list(record), record_schema()["required"])
                self.assertEqual(self.tolerated(profile, record_errors(record)), [])

    def test_the_record_is_derived_from_the_profile_and_form(self) -> None:
        for profile in self.templates:
            with self.subTest(template=profile["id"]):
                record = self.records[profile["id"]]
                definition = profile["template_definition"]
                self.assertEqual(record["template_id"], profile["id"])
                self.assertEqual(record["role"], profile["document_role"])
                for key in (
                    "contract_id",
                    "contract_version",
                    "purpose",
                    "responsibility",
                    "non_goals",
                    "policy_refs",
                    "vocabulary_refs",
                    "applicability",
                    "consumer_paths",
                    "validation",
                    "migration",
                ):
                    self.assertEqual(record[key], definition[key])
                # SPEC-0222: the record keeps its own table fields; a core table's
                # binding stays in the registry.
                self.assertEqual(
                    record["tables"],
                    [
                        {
                            "name": table["name"],
                            "section": table["section"],
                            "columns": [
                                {
                                    key: column[key]
                                    for key in (
                                        "key",
                                        "meaning",
                                        "data_type",
                                        "required",
                                    )
                                }
                                for column in table["columns"]
                            ],
                            "minimum_rows": table["minimum_rows"],
                            "row_identity": table["row_identity"],
                        }
                        for table in definition["tables"]
                    ],
                )
                form = self.forms.get(profile["document_role"])
                self.assertEqual(
                    record["headings"],
                    []
                    if form is None
                    else [form_headings(item) for item in form["sections"]],
                )
                source = self.profiles[
                    profile["relationships"]["source_profile_ids"][0]
                ]
                lists = source["frontmatter"]
                listed = (
                    []
                    if lists["mode"] == "absent"
                    else [*lists["required"], *lists["optional"], *lists["forbidden"]]
                )
                self.assertEqual([item["name"] for item in record["metadata"]], listed)

    def test_the_templates_of_one_role_share_headings_extensions_and_version(
        self,
    ) -> None:
        by_role: dict[str, list[dict]] = {}
        for profile in self.templates:
            by_role.setdefault(profile["document_role"], []).append(
                self.records[profile["id"]]
            )
        self.assertGreater(len(by_role), 1)
        for role, records in by_role.items():
            for key in ("headings", "extensions", "contract_id", "contract_version"):
                with self.subTest(role=role, key=key):
                    self.assertEqual(
                        len(
                            {json.dumps(item[key], sort_keys=True) for item in records}
                        ),
                        1,
                    )

    def test_the_contract_fields_name_the_contract_of_its_role(self) -> None:
        common = self.raw["common_forms"]
        for profile in self.templates:
            role = profile["document_role"]
            expected = (
                (common["contract_id"], common["version"])
                if role in COMMON_RECORD_ROLES
                else (
                    "STAGE99-LOCAL-FORM-1",
                    "2.0.0" if role == "reference-pack-readme" else "1.0.0",
                )
            )
            definition = profile["template_definition"]
            with self.subTest(template=profile["id"]):
                self.assertEqual(
                    (definition["contract_id"], definition["contract_version"]),
                    expected,
                )

    def test_every_template_carries_a_definition_since_the_task_form(self) -> None:
        # SPEC-0203 gave the last SDLC template (the Task) its definition, so no
        # template is left without one and the record is derived for each.
        without = [
            item
            for item in self.raw["profiles"]
            if item["mode"] == "template" and "template_definition" not in item
        ]
        self.assertEqual(without, [])
        for profile in self.templates:
            with self.subTest(template=profile["id"]):
                self.assertIsInstance(
                    CONTRACTS.template_definition_record(self.raw, profile["id"]),
                    dict,
                )
        self.assertIn(SDLC_TASK_FORM[1], {item["id"] for item in self.templates})

    def test_the_function_refuses_a_profile_that_is_not_a_template(self) -> None:
        for profile_id in ("operation/guide", "no/such-profile"):
            with self.subTest(profile=profile_id):
                with self.assertRaises(ValueError):
                    CONTRACTS.template_definition_record(self.raw, profile_id)

    def test_the_function_reads_the_mapping_only_and_is_repeatable(self) -> None:
        raw = copy.deepcopy(self.raw)
        first = CONTRACTS.template_definition_record(raw, GUIDE[1])
        self.assertEqual(raw, self.raw)
        self.assertEqual(first, CONTRACTS.template_definition_record(raw, GUIDE[1]))

    def test_relationships_hold_one_sentence_per_relation_naming_the_profile(
        self,
    ) -> None:
        contract = self.raw["relationship_contract"]
        for profile in self.templates:
            source = profile["relationships"]["source_profile_ids"][0]
            named = [
                item["id"]
                for item in contract["relations"]
                if {profile["id"], source}
                & {*item["source_profile_ids"], *item["target_profile_ids"]}
            ]
            sentences = self.records[profile["id"]]["relationships"]
            with self.subTest(template=profile["id"]):
                self.assertEqual(len(sentences), len(named))
                for relation in named:
                    self.assertEqual(
                        sum(f"Relation {relation} " in item for item in sentences), 1
                    )
                for relation in ("policy-authority", "consumer-impact"):
                    self.assertIn(relation, named)

    def test_the_lifecycle_sentence_names_the_family_or_says_there_is_none(
        self,
    ) -> None:
        guide = self.records[GUIDE[1]]["lifecycle"]
        self.assertIn("governance-operations", guide)
        self.assertIn("draft", guide)
        readme = self.records["common/template-readme-repository"]["lifecycle"]
        self.assertIn("binds no lifecycle domain", readme)

    def test_the_language_sentence_reads_the_document_language_contract(
        self,
    ) -> None:
        self.assertIn("korean-first", self.records[GUIDE[1]]["language"])
        native = self.records["common/template-exception-provider-native-metadata"]
        self.assertIn("english-only", native["language"])
        self.assertIn(
            self.forms["guide"]["language_rule"], self.records[GUIDE[1]]["language"]
        )

    def test_the_extensions_come_from_the_form_or_the_headings_extension(
        self,
    ) -> None:
        runbook = self.records[RUNBOOK[1]]["extensions"]
        form = self.forms["runbook"]["extensions"]
        self.assertTrue(form)
        self.assertEqual(len(runbook), len(form))
        for item, stored in zip(runbook, form, strict=True):
            self.assertEqual(item["condition"], stored["condition"])
            self.assertEqual(item["owner"], stored["owner"])
            self.assertIn(stored["id"], item["delta"])
            self.assertIn(stored["kind"], item["delta"])
            self.assertEqual(item["validation"], stored["verification"])
            self.assertIn(stored["review"], item["expiry_or_review"])
            self.assertIn(stored["removal"], item["expiry_or_review"])
        for profile in self.templates:
            if profile["document_role"] == "provider-native":
                stored = profile["template_definition"]["headings_extension"]
                (item,) = self.records[profile["id"]]["extensions"]
                self.assertIn("empty_headings", item["delta"])
                self.assertIn(stored["id"], item["delta"])

    def test_the_provider_native_templates_carry_the_complete_extension(self) -> None:
        native = [
            item
            for item in self.templates
            if item["document_role"] == "provider-native"
        ]
        self.assertEqual(len(native), 3)
        for profile in native:
            with self.subTest(template=profile["id"]):
                stored = profile["template_definition"]["headings_extension"]
                self.assertEqual(set(stored), set(HEADINGS_EXTENSION))
                self.assertEqual(stored["id"], HEADINGS_EXTENSION["id"])
                self.assertTrue(all(value.strip() for value in stored.values()))
        for profile in self.templates:
            if profile["document_role"] != "provider-native":
                self.assertNotIn("headings_extension", profile["template_definition"])

    def test_the_repository_registry_passes_both_registry_rules(self) -> None:
        self.assertEqual(current_rules(self.raw), set())
        self.assertEqual(rules_of(self.raw), set())


class TemplateRecordRuleTests(unittest.TestCase):
    """VAL-TDREC-001: REGISTRY_TEMPLATE_RECORD and REGISTRY_TEMPLATE_EXTENSION refuse."""

    NATIVE = "common/template-exception-provider-native-metadata"
    NATIVES = (
        NATIVE,
        "common/template-exception-provider-native-command",
        "common/template-exception-provider-native-codex",
    )

    def definition(self, raw: dict, profile_id: str) -> dict:
        return profile_of(raw, profile_id)["template_definition"]

    def test_a_definition_without_contract_version_fails_the_schema(self) -> None:
        raw = load_raw()
        del self.definition(raw, GUIDE[1])["contract_version"]
        self.assertIn("REGISTRY_SCHEMA", rules_of(raw))

    def test_definition_and_record_require_distinct_contract_fields(self) -> None:
        raw = load_raw()
        stored = self.definition(raw, GUIDE[1])
        self.assertEqual(stored["contract_id"], "COMMON-DOC-FORM-1")
        self.assertEqual(stored["contract_version"], "2.0.0")
        record = CONTRACTS.template_definition_record(raw, GUIDE[1])
        self.assertEqual(record["contract_id"], stored["contract_id"])
        self.assertEqual(record["contract_version"], stored["contract_version"])
        for invalid in (
            "COMMON-DOC-FORM-1/1.0.0",
            "1.0.0-rc.1",
            "1.0.0+local",
            "1.0.0\n",
        ):
            with self.subTest(version=invalid):
                self.assertTrue(record_errors({**record, "contract_version": invalid}))
        del stored["contract_id"]
        self.assertIn("REGISTRY_SCHEMA", rules_of(raw))

    def test_a_common_value_that_differs_from_the_common_form_version_fails(
        self,
    ) -> None:
        raw = load_raw()
        self.definition(raw, GUIDE[1])["contract_version"] = "9.9.9"
        self.assertIn("REGISTRY_TEMPLATE_RECORD", current_rules(raw))

    def test_a_common_value_on_a_role_without_a_form_fails(self) -> None:
        raw = load_raw()
        for profile_id in self.NATIVES:
            self.definition(raw, profile_id)["contract_id"] = "COMMON-DOC-FORM-1"
        self.assertIn("REGISTRY_TEMPLATE_RECORD", current_rules(raw))

    def test_a_value_outside_the_grammar_fails(self) -> None:
        invalid = {
            "contract_id": (
                "common-doc-form-1",
                "COMMON-DOC-FORM-1/1.0.0",
                "STAGE99-LOCAL-FORM-1\n",
            ),
            "contract_version": (
                "1.0",
                "v1.0.0",
                "01.0.0",
                "１.0.0",
                "1.0.0\n",
                "1.0.0-rc.1",
                "1.0.0+build",
            ),
        }
        for field, values in invalid.items():
            for value in values:
                raw = load_raw()
                self.definition(raw, "common/template-governance-prompt")[field] = value
                with self.subTest(field=field, value=value):
                    self.assertIn("REGISTRY_TEMPLATE_RECORD", current_rules(raw))
                    self.assertIn("REGISTRY_SCHEMA", rules_of(raw))

    def test_two_values_on_one_role_fail(self) -> None:
        raw = load_raw()
        self.definition(raw, "common/template-readme-stage-index")["contract_id"] = (
            "STAGE99-LOCAL-FORM-1"
        )
        self.assertIn("REGISTRY_TEMPLATE_RECORD", current_rules(raw))

    def test_a_record_with_a_missing_added_or_wrong_field_fails_the_schema(
        self,
    ) -> None:
        good = CONTRACTS.template_definition_record(load_raw(), GUIDE[1])
        self.assertEqual(record_errors(good), [])

        def h3(record: dict) -> dict:
            return next(
                child for item in record["headings"] for child in item["children"]
            )

        cases = {
            "missing field": lambda r: r.pop("language"),
            "added field": lambda r: r.update(extra="x"),
            "Release role": lambda r: r.update(role="Release"),
            "H3 with children": lambda r: h3(r)["children"].append(
                copy.deepcopy(h3(r))
            ),
            "H2 with a parent": lambda r: r["headings"][0].update(parent_id="x"),
            "empty headings": lambda r: r.update(headings=[]),
        }
        for name, change in cases.items():
            record = copy.deepcopy(good)
            change(record)
            with self.subTest(case=name):
                self.assertTrue(record_errors(record))

    def test_an_empty_headings_list_on_a_role_with_a_form_fails(self) -> None:
        raw = load_raw()
        for item in raw["common_forms"]["forms"]:
            if item["form_id"] == "guide":
                item["sections"] = []
        self.assertIn("REGISTRY_TEMPLATE_RECORD", current_rules(raw))

    def test_a_provider_native_definition_needs_its_complete_extension(self) -> None:
        raw = load_raw()
        del self.definition(raw, self.NATIVE)["headings_extension"]
        found = current_rules(raw)
        self.assertIn("REGISTRY_TEMPLATE_EXTENSION", found)
        self.assertIn("REGISTRY_TEMPLATE_RECORD", found)

    def test_each_malformed_extension_fails(self) -> None:
        cases = {
            "missing field": lambda e: e.pop("review"),
            "empty field": lambda e: e.update(removal=""),
            "whitespace field": lambda e: e.update(condition="   \t"),
            "non-text field": lambda e: e.update(verification=["x"]),
            "extra key": lambda e: e.update(note="x"),
            "wrong id": lambda e: e.update(id="other"),
            "unregistered owner": lambda e: e.update(owner="nobody"),
        }
        for name, change in cases.items():
            raw = load_raw()
            change(self.definition(raw, self.NATIVE)["headings_extension"])
            with self.subTest(case=name):
                self.assertIn("REGISTRY_TEMPLATE_EXTENSION", current_rules(raw))

    def test_the_owner_set_is_read_from_the_registry(self) -> None:
        raw = load_raw()
        self.assertEqual(current_rules(raw), set())
        extension = self.definition(raw, self.NATIVE)["headings_extension"]
        self.assertEqual(extension["owner"], "platform")
        extension["owner"] = raw["shared_contract"]["owner"]
        self.assertEqual(current_rules(raw), set())
        extension["owner"] = "newowner"
        self.assertIn("REGISTRY_TEMPLATE_EXTENSION", current_rules(raw))
        next(
            item for form in raw["common_forms"]["forms"] for item in form["extensions"]
        )["owner"] = "newowner"
        self.assertEqual(current_rules(raw), set())

    def test_a_record_on_a_role_with_a_form_fails(self) -> None:
        raw = load_raw()
        self.definition(raw, GUIDE[1])["headings_extension"] = dict(HEADINGS_EXTENSION)
        self.assertIn("REGISTRY_TEMPLATE_EXTENSION", current_rules(raw))

    def test_a_record_off_the_provider_native_role_fails(self) -> None:
        raw = load_raw()
        raw["common_forms"]["forms"] = [
            item
            for item in raw["common_forms"]["forms"]
            if item["form_id"] != "vocabulary"
        ]
        self.definition(raw, "common/template-governance-vocabulary")[
            "headings_extension"
        ] = dict(HEADINGS_EXTENSION)
        self.assertIn("REGISTRY_TEMPLATE_EXTENSION", current_rules(raw))

    def test_a_complete_record_does_not_hide_another_schema_finding(self) -> None:
        raw = load_raw()
        self.definition(raw, self.NATIVE)["non_goals"] = []
        found = current_rules(raw)
        self.assertIn("REGISTRY_TEMPLATE_RECORD", found)
        self.assertNotIn("REGISTRY_TEMPLATE_EXTENSION", found)


SPEC_PATH = PurePosixPath("docs/03.specs/0900-form-fixture/spec.md")
PLAN_PATH = PurePosixPath("docs/03.specs/0900-form-fixture/plan.md")


def form_table(header: tuple[str, ...], *, rows: int = 1) -> str:
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for number in range(rows):
        lines.append("| " + " | ".join(f"{key} {number}" for key in header) + " |")
    return "\n".join(lines)


def spec_form_body(*, header: tuple[str, ...] | None = None) -> str:
    keys = SPEC_FORM_TABLE_KEYS
    blocks = ["# Spec title"]
    for h2, children in SPEC_FORM_TREE:
        blocks.append(f"## {h2}")
        for h3 in children:
            text = f"The {h3} of the change."
            if h3 == "Criteria":
                text += "\n\n" + form_table(header or keys["Criteria"][1])
            blocks.append(f"### {h3}\n\n{text}")
    blocks.append(
        "### Lifecycle Traceability\n\n" + form_table(keys["Lifecycle Traceability"][1])
    )
    return md(*blocks)


def plan_form_body(*, constraints_first: bool = False) -> str:
    keys = PLAN_FORM_TABLE_KEYS
    blocks = ["# Plan title"]
    for h2, children in PLAN_FORM_TREE:
        blocks.append(f"## {h2}")
        for h3 in children:
            text = f"The {h3} of the work."
            if h3 == "Constraints":
                text += "\n\n#### Global Constraints\n\nKeep the Spec constraints."
            if h3 == "Work Units":
                text += "\n\n" + form_table(keys["Work Breakdown"][1])
            if h3 == "Durable Owners":
                text += "\n\n" + form_table(keys["Promotion"][1])
            blocks.append(f"### {h3}\n\n{text}")
    return md(*blocks)


class SpecPlanFormTests(unittest.TestCase):
    """SPEC-0200 VAL-SPECPLAN-001: the Spec and Plan forms, extension and tables."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = load_raw()
        cls.registry = CONTRACTS.load_registry(ROOT)
        cls.profiles = {p.profile_id: p for p in cls.registry.profiles}

    def tree(self, path: PurePosixPath, profile_id: str, text: str) -> list[str]:
        return sorted(
            item.rule_id
            for item in MARKDOWN._body_diagnostics(
                path, self.profiles[profile_id], text, "active"
            )
        )

    def test_each_form_has_the_common_sections_all_required_and_no_link_only(
        self,
    ) -> None:
        for form_id, tree, extensions in (
            ("spec", SPEC_FORM_TREE, SPEC_FORM_EXTENSIONS),
            ("plan", PLAN_FORM_TREE, PLAN_FORM_EXTENSIONS),
        ):
            with self.subTest(form=form_id):
                form = next(
                    f for f in self.registry.common_forms if f.form_id == form_id
                )
                self.assertEqual(
                    [
                        (s.title, tuple(c.title for c in s.children))
                        for s in form.sections
                    ],
                    list(tree),
                )
                every = [n for s in form.sections for n in (s, *s.children)]
                self.assertEqual(
                    [n.title for n in every if n.requiredness != "required"], []
                )
                self.assertFalse(any(n.link_only for n in every))
                self.assertEqual(
                    [(e.extension_id, e.parent_id, e.title) for e in form.extensions],
                    [(e["id"], e.get("parent_id"), e.get("title")) for e in extensions],
                )
        self.assertEqual(
            self.registry.schema_version.split(".")[0], str(AUTHORITY.REGISTRY_MAJOR)
        )

    def test_the_four_profiles_carry_no_h2_list_and_the_moved_body_contracts(
        self,
    ) -> None:
        for profile_id, section, heading, columns in (
            (
                "sdlc/spec",
                "Acceptance Criteria",
                "Lifecycle Traceability",
                SPEC_FORM_TABLE_KEYS["Lifecycle Traceability"][1],
            ),
            (
                "common/template-sdlc-spec",
                "Acceptance Criteria",
                "Lifecycle Traceability",
                SPEC_FORM_TABLE_KEYS["Lifecycle Traceability"][1],
            ),
            (
                "sdlc/plan",
                "Work Breakdown",
                "Work Units",
                PLAN_FORM_TABLE_KEYS["Work Breakdown"][1],
            ),
            (
                "common/template-sdlc-plan",
                "Work Breakdown",
                "Work Units",
                PLAN_FORM_TABLE_KEYS["Work Breakdown"][1],
            ),
        ):
            with self.subTest(profile=profile_id):
                raw = next(p for p in self.raw["profiles"] if p["id"] == profile_id)
                self.assertNotIn("sections", raw)
                contract = raw["relationships"]["body_contract"]
                self.assertEqual(contract["section"], section)
                self.assertEqual(contract["table_heading"], heading)
                self.assertEqual(contract["required_columns"], list(columns))
        for profile_id in SPEC_FORM:
            contract = next(p for p in self.raw["profiles"] if p["id"] == profile_id)[
                "relationships"
            ]["body_contract"]
            self.assertEqual(contract["target_link_column"], "Architecture")
            self.assertEqual(
                contract["allowed_target_profile_ids"],
                ["sdlc/architecture-description", "sdlc/architecture-decision"],
            )
            self.assertTrue(contract["allow_explicit_exclusion"])

    def test_the_tables_are_recorded_on_the_twin_and_copied_to_the_source(self) -> None:
        for pair, expected in (
            (SPEC_FORM, SPEC_FORM_TABLE_KEYS),
            (PLAN_FORM, PLAN_FORM_TABLE_KEYS),
        ):
            twin, source = (self.profiles[i] for i in reversed(pair))
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
                expected,
            )
            self.assertTrue(all(c.required for t in twin.tables for c in t.columns))

    def test_the_registry_is_valid_and_each_twin_names_the_form_version(self) -> None:
        self.assertEqual(rules_of(self.raw), set())
        REGISTRY_CHECK._assert_template_source_parity(self.registry)
        for twin in (SPEC_FORM[1], PLAN_FORM[1]):
            with self.subTest(twin=twin):
                definition_ = self.profiles[twin].template_definition
                self.assertEqual(definition_["contract_id"], "COMMON-DOC-FORM-1")
                self.assertEqual(definition_["contract_version"], "2.0.0")
                record = CONTRACTS.template_definition_record(self.raw, twin)
                self.assertEqual(record["contract_id"], definition_["contract_id"])
                self.assertEqual(
                    record["contract_version"], definition_["contract_version"]
                )
                for path in definition_["consumer_paths"]:
                    self.assertTrue((ROOT / path).is_file(), path)
                self.assertIn(
                    "tests/test_common_form_tree.py", definition_["consumer_paths"]
                )

    def test_a_complete_document_passes_the_tree_and_a_previous_h2_fails(self) -> None:
        self.assertEqual(self.tree(SPEC_PATH, "sdlc/spec", spec_form_body()), [])
        self.assertEqual(self.tree(PLAN_PATH, "sdlc/plan", plan_form_body()), [])
        old_spec = spec_form_body().replace("## Acceptance Criteria", "## Traceability")
        self.assertLessEqual(
            {"BODY-HEADING-REQUIRED", "BODY-HEADING-UNSUPPORTED"},
            set(self.tree(SPEC_PATH, "sdlc/spec", old_spec)),
        )
        old_plan = plan_form_body().replace("## Promotion Map", "## Promotion")
        self.assertLessEqual(
            {"BODY-HEADING-REQUIRED", "BODY-HEADING-UNSUPPORTED"},
            set(self.tree(PLAN_PATH, "sdlc/plan", old_plan)),
        )

    def test_lifecycle_traceability_belongs_under_acceptance_criteria(self) -> None:
        body = spec_form_body()
        block = "### Lifecycle Traceability\n\n" + form_table(
            SPEC_FORM_TABLE_KEYS["Lifecycle Traceability"][1]
        )
        moved = body.replace(block, "").replace("## Scope", block + "\n\n## Scope", 1)
        self.assertEqual(self.tree(SPEC_PATH, "sdlc/spec", moved), ["BODY-H3-PARENT"])

    def test_the_criteria_and_promotion_headers_take_the_common_names(self) -> None:
        old = spec_form_body(header=("Criterion", "Acceptance evidence"))
        found = sorted(
            item.rule_id
            for item in MARKDOWN._table_diagnostics(
                SPEC_PATH, self.profiles["sdlc/spec"], old
            )
        )
        self.assertTrue(
            found and set(found) <= {"BODY-TABLE-COLUMNS", "BODY-TABLE-ROWS"}
        )
        old_plan = plan_form_body().replace(
            "| Promotion ID | Target Owner | Acceptance | Evidence |",
            "| Durable contract | Promoted to | Where |",
        )
        found = sorted(
            item.rule_id
            for item in MARKDOWN._table_diagnostics(
                PLAN_PATH, self.profiles["sdlc/plan"], old_plan
            )
        )
        self.assertTrue(
            found and set(found) <= {"BODY-TABLE-COLUMNS", "BODY-TABLE-ROWS"}
        )

    def test_the_templates_pass_the_form_tree_and_put_global_constraints_after_text(
        self,
    ) -> None:
        for twin_id, forbidden in (
            (SPEC_FORM[1], r"(?m)^## Success Criteria & Verification Plan"),
            (PLAN_FORM[1], r"(?m)^## Global Constraints"),
        ):
            twin = self.profiles[twin_id]
            path = PurePosixPath(twin.template)
            text = (ROOT / path).read_text(encoding="utf-8")
            with self.subTest(template=twin_id):
                self.assertEqual(
                    [
                        item.rule_id
                        for item in MARKDOWN.validate_document_text(
                            text, path, twin, "strict"
                        )
                    ],
                    [],
                )
                self.assertNotRegex(text, forbidden)
        plan = (ROOT / self.profiles[PLAN_FORM[1]].template).read_text(encoding="utf-8")
        constraints = plan.split("### Constraints", 1)[1].split("## Dependencies", 1)[0]
        before, found, _ = constraints.partition("#### Global Constraints")
        self.assertTrue(found)
        self.assertNotIn("####", before)
        self.assertTrue(before.strip())
        self.assertIn("| Promotion ID | Target Owner | Acceptance | Evidence |", plan)


def retained_spec_text(artifact_id: str, status: str) -> str:
    keys = SPEC_FORM_TABLE_KEYS
    blocks = [
        "---",
        'title: "Retained Spec"',
        'version: "1.0.0"',
        'type: "sdlc/spec"',
        f'status: "{status}"',
        'owner: "platform"',
        'updated: "2026-11-17"',
        f'artifact_id: "{artifact_id}"',
        "---",
        "",
        "# Spec title",
    ]
    for h2, children in SPEC_RETAINED_TREE:
        blocks.append(f"## {h2}")
        for h3 in children:
            text = f"The {h3} of the change."
            if h3 == "Criteria":
                text += "\n\n" + form_table(keys["Criteria"][1])
            blocks.append(f"### {h3}\n\n{text}")
    blocks.append(
        "### Lifecycle Traceability\n\n" + form_table(keys["Lifecycle Traceability"][1])
    )
    return md(*blocks)


def retained_plan_text(artifact_id: str, status: str) -> str:
    keys = PLAN_FORM_TABLE_KEYS
    blocks = [
        "---",
        'title: "Retained Plan"',
        'version: "1.0.0"',
        'type: "sdlc/plan"',
        f'status: "{status}"',
        'owner: "platform"',
        'updated: "2026-11-17"',
        f'artifact_id: "{artifact_id}"',
        f'parent_ids: ["{artifact_id.split("-PLAN")[0]}"]',
        "---",
        "",
        "# Plan title",
    ]
    for h2, children in PLAN_RETAINED_TREE:
        blocks.append(f"## {h2}")
        for h3 in children:
            text = f"The {h3} of the work."
            if h3 == "Goal and Boundary":
                text += "\n\n#### Global Constraints\n\nKeep the Spec constraints."
            if h3 == "Work Breakdown":
                text += "\n\n" + form_table(keys["Work Breakdown"][1])
            if h3 == "Owner and Receipt":
                text += "\n\n" + form_table(keys["Promotion"][1])
            blocks.append(f"### {h3}\n\n{text}")
    return md(*blocks)


class RetainedSpecPlanTests(unittest.TestCase):
    """SPEC-0221 VAL-FORM-003: four approved identities keep their old tree."""

    CASES = (
        ("sdlc/spec", "0161-w00-v14-7-delta-intake", "SPEC-0161", "spec.md"),
        ("sdlc/spec", "0221-w03-form-target-adoption", "SPEC-0221", "spec.md"),
        ("sdlc/plan", "0161-w00-v14-7-delta-intake", "SPEC-0161-PLAN-0001", "plan.md"),
        (
            "sdlc/plan",
            "0221-w03-form-target-adoption",
            "SPEC-0221-PLAN-0001",
            "plan.md",
        ),
    )

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = CONTRACTS.load_registry(ROOT)
        cls.profiles = {p.profile_id: p for p in cls.registry.profiles}

    @staticmethod
    def text(profile_id: str, artifact_id: str, status: str) -> str:
        build = retained_spec_text if profile_id == "sdlc/spec" else retained_plan_text
        return build(artifact_id, status)

    def found(self, profile_id: str, path: PurePosixPath, text: str, status: str):
        profile = self.profiles[profile_id]
        return sorted(
            item.rule_id
            for item in (
                *MARKDOWN._body_diagnostics(path, profile, text, status),
                *MARKDOWN._body_contract_diagnostics(
                    path, profile, text, status, "registry"
                ),
            )
        )

    def test_each_retained_identity_passes_its_approved_tree_and_table(self) -> None:
        for profile_id, package, artifact_id, name in self.CASES:
            with self.subTest(artifact=artifact_id):
                path = PurePosixPath("docs/03.specs", package, name)
                text = self.text(profile_id, artifact_id, "approved")
                profile = self.profiles[profile_id]
                self.assertEqual(
                    [
                        item.rule_id
                        for item in MARKDOWN._body_diagnostics(
                            path, profile, text, "approved"
                        )
                    ],
                    [],
                )
                # The synthetic rows carry no real identifier; only the table's
                # location is under test here.
                self.assertNotIn(
                    "BODY-CONTRACT-HEADING",
                    self.found(profile_id, path, text, "approved"),
                )
                rows = LINKS._body_contract_rows(text, profile)
                self.assertTrue(rows)

    def test_only_a_retained_form_may_carry_a_location_or_titles(self) -> None:
        for key, value in (
            ("body_contract", {"section": "Scope", "table_heading": "In Scope"}),
            ("section_titles", {"spec.scope.1": "In Scope"}),
        ):
            with self.subTest(key=key):
                raw = load_raw()
                form = next(
                    f for f in raw["common_forms"]["forms"] if f["form_id"] == "spec"
                )
                local = next(e for e in form["extensions"] if e["kind"] == "local_h3")
                local[key] = value
                self.assertIn("REGISTRY_SCHEMA", rules_of(raw))
        raw = load_raw()
        form = next(f for f in raw["common_forms"]["forms"] if f["form_id"] == "plan")
        kept = next(e for e in form["extensions"] if e["kind"] == "retained_form")
        kept["section_titles"] = {}
        self.assertIn("REGISTRY_SCHEMA", rules_of(raw))

    def test_a_retained_title_applies_only_to_its_bounded_identity(self) -> None:
        form = self.profiles["sdlc/plan"].form
        self.assertEqual(
            form.section_heading("plan.promotion.1", "approved", "SPEC-0221-PLAN-0001"),
            (3, "Owner and Receipt"),
        )
        for status, identity in (
            ("approved", "SPEC-0162-PLAN-0001"),
            ("draft", "SPEC-0221-PLAN-0001"),
        ):
            with self.subTest(status=status, identity=identity):
                self.assertEqual(
                    form.section_heading("plan.promotion.1", status, identity),
                    (3, "Durable Owners"),
                )

    def test_the_retained_plan_promotion_table_keeps_its_column_check(self) -> None:
        path = PurePosixPath("docs/03.specs/0221-w03-form-target-adoption/plan.md")
        text = (ROOT / path).read_text(encoding="utf-8")
        profile = self.profiles["sdlc/plan"]

        def tables(body: str) -> list[str]:
            return [
                item.rule_id
                for item in MARKDOWN._table_diagnostics(path, profile, body, "approved")
            ]

        self.assertEqual(tables(text), [])
        broken = text.replace(
            "| Promotion ID | Target Owner |", "| Promotion ID | Owner |"
        )
        self.assertIn("BODY-TABLE-COLUMNS", tables(broken))

    def test_another_identity_in_the_old_tree_is_refused(self) -> None:
        for profile_id, artifact_id, name in (
            ("sdlc/spec", "SPEC-0162", "spec.md"),
            ("sdlc/plan", "SPEC-0162-PLAN-0001", "plan.md"),
        ):
            with self.subTest(artifact=artifact_id):
                path = PurePosixPath("docs/03.specs/0162-other", name)
                text = self.text(profile_id, artifact_id, "approved")
                found = self.found(profile_id, path, text, "approved")
                self.assertIn("BODY-HEADING-UNSUPPORTED", found)
                self.assertIn("BODY-CONTRACT-HEADING", found)
                self.assertIsNone(
                    LINKS._body_contract_rows(text, self.profiles[profile_id])
                )

    def test_a_retained_identity_in_another_status_takes_the_tree(self) -> None:
        for profile_id, package, artifact_id, name in self.CASES:
            with self.subTest(artifact=artifact_id):
                path = PurePosixPath("docs/03.specs", package, name)
                text = self.text(profile_id, artifact_id, "draft")
                self.assertIn(
                    "BODY-HEADING-UNSUPPORTED",
                    self.found(profile_id, path, text, "draft"),
                )


class FormlessRoleTableTests(unittest.TestCase):
    """VAL-TDREC-002: a role without a form records no table (SPEC-0196, W03-D56)."""

    NATIVE = "common/template-exception-provider-native-metadata"
    TABLE = {
        "name": "Rows",
        "columns": [
            {
                "key": "Key",
                "meaning": "The key.",
                "data_type": "string",
                "required": True,
            }
        ],
        "minimum_rows": 0,
        "row_identity": "Key",
    }

    def test_a_table_on_a_role_without_a_form_fails(self) -> None:
        for section in ("### Rows", "## Overview", "native-rows"):
            raw = load_raw()
            profile_of(raw, self.NATIVE)["template_definition"]["tables"] = [
                {**self.TABLE, "section": section}
            ]
            with self.subTest(section=section):
                self.assertIn("REGISTRY_TABLE_SECTION", rules_of(raw))

    def test_the_repository_roles_without_a_form_record_no_table(self) -> None:
        raw = load_raw()
        forms = {item["form_id"] for item in raw["common_forms"]["forms"]}
        for profile in raw["profiles"]:
            definition = profile.get("template_definition")
            if definition is not None and profile["document_role"] not in forms:
                self.assertEqual(definition["tables"], [], profile["id"])
        for profile in raw["profiles"]:
            for table in (profile.get("template_definition") or {}).get("tables", ()):
                self.assertFalse(table["section"].startswith("#"), profile["id"])


TASK_PATH = PurePosixPath("docs/03.specs/0900-form-fixture/tasks/tsk-0001-fixture.md")


def task_form_body(*, evidence_header: tuple[str, ...] | None = None) -> str:
    keys = SDLC_TASK_FORM_TABLE_KEYS
    blocks = ["# Task title"]
    for h2, children in SDLC_TASK_FORM_TREE:
        blocks.append(f"## {h2}")
        for h3 in children:
            text = f"The {h3} of the execution."
            if h3 == "Results":
                text += "\n\n" + form_table(evidence_header or keys["Results"][1])
            if h3 == "Criterion Decisions":
                text += "\n\n" + form_table(keys["Criterion Decisions"][1])
            blocks.append(f"### {h3}\n\n{text}")
            if h3 == "Blockers and Decisions":
                blocks.append(
                    "### Lifecycle Traceability\n\n"
                    + form_table(keys["Lifecycle Traceability"][1])
                )
    return md(*blocks)


class TaskFormTests(unittest.TestCase):
    """SPEC-0203 VAL-TASKFORM-001: the Task form, its extensions and its tables."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = load_raw()
        cls.registry = CONTRACTS.load_registry(ROOT)
        cls.profiles = {p.profile_id: p for p in cls.registry.profiles}

    def test_the_form_has_the_common_sections_and_two_registered_extensions(
        self,
    ) -> None:
        form = next(f for f in self.registry.common_forms if f.form_id == "task")
        self.assertEqual(
            [(s.title, tuple(c.title for c in s.children)) for s in form.sections],
            list(SDLC_TASK_FORM_TREE),
        )
        every = [n for s in form.sections for n in (s, *s.children)]
        self.assertEqual([n.title for n in every if n.requiredness != "required"], [])
        self.assertFalse(any(n.link_only for n in every))
        raw_form = next(
            f for f in self.raw["common_forms"]["forms"] if f["form_id"] == "task"
        )
        self.assertEqual(raw_form["extensions"], SDLC_TASK_FORM_EXTENSIONS)
        # SPEC-0222: the core evidence table names Work Unit, Location, Required
        # and Resolves, so no column extension remains.
        self.assertEqual({e.kind for e in form.extensions}, {"local_h3"})

    def test_the_two_profiles_carry_no_h2_list_and_the_moved_contract_and_binding(
        self,
    ) -> None:
        for profile_id in SDLC_TASK_FORM:
            with self.subTest(profile=profile_id):
                raw = next(p for p in self.raw["profiles"] if p["id"] == profile_id)
                self.assertNotIn("sections", raw)
                contract = raw["relationships"]["body_contract"]
                self.assertEqual(contract["section"], "Execution Log")
                self.assertEqual(contract["table_heading"], "Lifecycle Traceability")
                binding = contract["task_execution"]
                self.assertEqual(binding["evidence_section"], "Verification Evidence")
                self.assertEqual(
                    binding["criterion_acceptance_section"], "Acceptance Decision"
                )
                self.assertEqual(
                    binding["evidence_columns"],
                    list(SDLC_TASK_FORM_TABLE_KEYS["Results"][1]),
                )
        self.assertEqual(
            self.raw["work_residue"]["task_table"]["section"], "Verification Evidence"
        )

    def test_the_tables_and_the_definition_are_recorded_on_the_twin(self) -> None:
        twin, source = (self.profiles[i] for i in reversed(SDLC_TASK_FORM))
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
            SDLC_TASK_FORM_TABLE_KEYS,
        )
        self.assertEqual(twin.template_definition["contract_id"], "COMMON-DOC-FORM-1")
        self.assertEqual(twin.template_definition["contract_version"], "2.0.0")
        self.assertEqual(rules_of(self.raw), set())
        record = CONTRACTS.template_definition_record(self.raw, SDLC_TASK_FORM[1])
        self.assertEqual(record["contract_id"], twin.template_definition["contract_id"])
        self.assertEqual(
            record["contract_version"], twin.template_definition["contract_version"]
        )
        for path in twin.template_definition["consumer_paths"]:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_a_complete_task_passes_the_tree_and_a_previous_h2_fails(self) -> None:
        def tree(text: str) -> set[str]:
            return {
                item.rule_id
                for item in MARKDOWN._body_diagnostics(
                    TASK_PATH, self.profiles["sdlc/task"], text, "active"
                )
            }

        self.assertEqual(
            {r for r in tree(task_form_body()) if r.startswith("BODY-HEADING")}, set()
        )
        old = task_form_body().replace("## Verification Evidence", "## Task Evidence")
        self.assertLessEqual(
            {"BODY-HEADING-REQUIRED", "BODY-HEADING-UNSUPPORTED"}, tree(old)
        )

    def test_a_column_extension_is_refused(self) -> None:
        # SPEC-0222: no local table column extends a core table.
        raw = copy.deepcopy(self.raw)
        form = next(f for f in raw["common_forms"]["forms"] if f["form_id"] == "task")
        form["extensions"].append(
            {
                "id": "task-extra-columns",
                "kind": "local_columns",
                "condition": "c",
                "owner": "platform",
                "verification": "v",
                "review": "r",
                "removal": "x",
                "authority_ref": "SPEC-0222",
                "table": "Results",
                "columns": ["Extra"],
            }
        )
        self.assertIn("REGISTRY_SCHEMA", rules_of(raw))
        raw = copy.deepcopy(self.raw)
        form = next(f for f in raw["common_forms"]["forms"] if f["form_id"] == "task")
        next(e for e in form["extensions"] if e["id"] == "task-lifecycle-traceability")[
            "columns"
        ] = ["Extra"]
        self.assertTrue(rules_of(raw))

    def test_the_extension_kinds_are_the_local_h3_and_the_retained_form(self) -> None:
        schema = json.loads(
            (
                ROOT / "docs/99.templates/contracts/document-profile.schema.json"
            ).read_text(encoding="utf-8")
        )
        kinds = schema["$defs"]["form_extension"]["properties"]["kind"]["enum"]
        self.assertEqual(kinds, ["local_h3", "retained_form"])


class HeadingListRemovalTests(unittest.TestCase):
    """SPEC-0205 (W03-D63): no profile carries an H2 list; every reader takes its H2
    from the form of the profile's role through one accessor."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = load_raw()
        cls.registry = CONTRACTS.load_registry(ROOT)
        cls.schema = json.loads(
            (
                ROOT / "docs/99.templates/contracts/document-profile.schema.json"
            ).read_text(encoding="utf-8")
        )

    def test_the_registry_schema_and_guard_carry_no_sections_key(self) -> None:
        for profile in self.raw["profiles"]:
            self.assertNotIn("sections", profile)
        item = self.schema["properties"]["profiles"]["items"]
        self.assertNotIn("sections", item["properties"])
        self.assertNotIn("sections", item["required"])
        self.assertNotIn("sections", AUTHORITY.PROFILE_KEYS)
        # The list definition stays for the retained form of the accepted ADRs.
        self.assertIn("heading_lists", self.schema["$defs"])

    def test_a_sections_key_is_refused_by_the_schema_the_guard_and_the_check(
        self,
    ) -> None:
        for profile_id in ("sdlc/spec", "common/provider-native-metadata"):
            with self.subTest(profile=profile_id):
                raw = load_raw()
                profile_of(raw, profile_id)["sections"] = lists_of()
                self.assertEqual(rules_of(raw), {"REGISTRY_SCHEMA"})
                with self.assertRaises(AUTHORITY.AuthorityError):
                    AUTHORITY.validate_registry_authority(raw)
                self.assertIn("REGISTRY_FORM_LEGACY_LISTS", semantic_rules_of(raw))

    def test_the_accessor_gives_each_form_profile_its_form_titles(self) -> None:
        for profile in self.registry.profiles:
            headings = CONTRACTS.heading_contract(profile)
            with self.subTest(profile=profile.profile_id):
                if profile.form is None:
                    self.assertEqual((headings.required, headings.allowed), ((), ()))
                    continue
                sources = set(profile.source_profile_ids or (profile.profile_id,))
                applicable = [
                    item
                    for item in profile.form.sections
                    if not item.applicable_source_profiles
                    or sources.intersection(item.applicable_source_profiles)
                ]
                self.assertEqual(
                    headings.required,
                    tuple(
                        item.title
                        for item in applicable
                        if item.requiredness == "required"
                        or item.required_if_applicable
                    ),
                )
                self.assertEqual(
                    headings.allowed,
                    tuple(item.title for item in applicable),
                )

    def test_the_old_field_is_gone_so_a_reader_of_it_fails_loudly(self) -> None:
        for profile in self.registry.profiles:
            with self.subTest(profile=profile.profile_id):
                with self.assertRaises(AttributeError):
                    profile.headings
                self.assertIsNone(profile.listed_headings)

    def test_a_registry_of_an_earlier_major_is_read_with_its_lists(self) -> None:
        raw = load_raw()
        earlier = f"{AUTHORITY.REGISTRY_MAJOR - 1}.0.0"
        raw["schema_version"] = earlier
        for profile in raw["profiles"]:
            profile["sections"] = lists_of()
        bare = profile_of(raw, "governance/provider")
        bare["document_role"] = None
        bare.pop("document_role")
        bare["sections"] = lists_of(
            required=["Overview", "Scope"], optional=["Notes"], ordered=True
        )
        # A profile whose role has a form keeps the form's titles over any list.
        profile_of(raw, "sdlc/spec")["sections"] = lists_of(required=["Stale"])
        loaded = CONTRACTS._typed_registry_from_mapping(raw)
        by_id = {profile.profile_id: profile for profile in loaded.profiles}
        listed = CONTRACTS.heading_contract(by_id["governance/provider"])
        self.assertEqual(listed.required, ("Overview", "Scope"))
        self.assertEqual(listed.allowed, ("Overview", "Scope", "Notes"))
        self.assertTrue(listed.ordered)
        spec = CONTRACTS.heading_contract(by_id["sdlc/spec"])
        self.assertNotIn("Stale", spec.required)
        self.assertEqual(loaded.schema_version, earlier)

    def test_a_registry_of_the_current_major_is_read_with_no_list(self) -> None:
        raw = load_raw()
        for profile in raw["profiles"]:
            profile["sections"] = lists_of(required=["Stale"])
            profile.pop("document_role", None)
        loaded = CONTRACTS._typed_registry_from_mapping(raw)
        for profile in loaded.profiles:
            with self.subTest(profile=profile.profile_id):
                self.assertIsNone(profile.listed_headings)
                self.assertEqual(
                    CONTRACTS.heading_contract(profile),
                    CONTRACTS.HeadingContract(required=(), allowed=()),
                )

    def test_every_profile_meets_the_form_requirement(self) -> None:
        by_id = {profile.profile_id: profile for profile in self.registry.profiles}
        self.assertEqual(len(by_id), len(self.raw["profiles"]))
        self.assertEqual(semantic_rules_of(self.raw), set())
        for profile_id, profile in by_id.items():
            with self.subTest(profile=profile_id):
                if profile.form is not None:
                    continue
                self.assertTrue(
                    profile.mode in {"native", "non-target"}
                    or profile.document_role == "provider-native"
                )

    def test_the_form_requirement_refuses_an_authored_profile_without_a_form(
        self,
    ) -> None:
        for profile_id in (
            "sdlc/spec",
            "common/template-sdlc-spec",
            "common/readme-repository",
        ):
            with self.subTest(profile=profile_id):
                raw = load_raw()
                profile_of(raw, profile_id).pop("document_role")
                self.assertIn("REGISTRY_FORM_REQUIRED", semantic_rules_of(raw))
        raw = load_raw()
        for profile in raw["profiles"]:
            if profile.get("document_role") == "provider-native":
                profile.pop("document_role")
                profile["mode"] = "native"
                profile.pop("template_definition", None)
        self.assertNotIn("REGISTRY_FORM_REQUIRED", semantic_rules_of(raw))
        raw = load_raw()
        native = next(p for p in raw["profiles"] if p["mode"] == "native")
        native.pop("document_role", None)
        self.assertNotIn("REGISTRY_FORM_REQUIRED", semantic_rules_of(raw))

    def test_the_provider_native_role_is_admitted_without_a_form(self) -> None:
        roles = {
            profile["id"]: (profile["mode"], profile.get("document_role"))
            for profile in self.raw["profiles"]
            if profile.get("document_role") == "provider-native"
        }
        self.assertEqual(len(roles), 6)
        self.assertIn("template", {mode for mode, _ in roles.values()})
        self.assertNotIn("REGISTRY_FORM_REQUIRED", semantic_rules_of(self.raw))

    def test_a_body_section_must_be_a_required_h2_of_the_form(self) -> None:
        raw = load_raw()
        profile_of(raw, "sdlc/spec")["relationships"]["body_contract"]["section"] = (
            "Nope"
        )
        self.assertIn("REGISTRY_BODY_SECTION", semantic_rules_of(raw))

    def test_the_link_reader_refuses_a_document_without_a_required_h2(self) -> None:
        policy = next(
            p for p in self.registry.profiles if p.profile_id == "governance/rule"
        )
        path = PurePosixPath(".agents/governance/agent-execution.md")
        text = (ROOT / path).read_text(encoding="utf-8")
        mapping = {path: "governance/rule"}
        self.assertTrue(
            LINKS.lifecycle_markdown_evidence(
                path, text, policy, mapping
            ).relationship_section_valid
        )
        required = CONTRACTS.heading_contract(policy).required[0]
        missing = re.sub(
            rf"(?m)^## {re.escape(required)}\s*$", "## Elsewhere", text, count=1
        )
        self.assertNotEqual(missing, text)
        for broken in (missing, text + "\n## Not In The Form\n"):
            self.assertFalse(
                LINKS.lifecycle_markdown_evidence(
                    path, broken, policy, mapping
                ).relationship_section_valid
            )

    def test_the_parity_check_reads_the_form_through_the_accessor(self) -> None:
        by_id = {profile.profile_id: profile for profile in self.registry.profiles}
        twin = by_id["common/template-sdlc-spec"]
        shorter = dataclasses.replace(twin.form, sections=twin.form.sections[:-1])
        profiles = tuple(
            dataclasses.replace(profile, form=shorter) if profile is twin else profile
            for profile in self.registry.profiles
        )
        with self.assertRaisesRegex(AssertionError, "template/source contract differs"):
            REGISTRY_CHECK._assert_template_source_parity(
                dataclasses.replace(self.registry, profiles=profiles)
            )

    def test_the_quality_gate_test_for_a_heading_contract_follows_the_form(
        self,
    ) -> None:
        for profile in self.registry.profiles:
            headings = CONTRACTS.heading_contract(profile)
            with self.subTest(profile=profile.profile_id):
                self.assertEqual(
                    bool(headings.required or headings.allowed),
                    profile.form is not None,
                )

    def test_a_profile_without_a_form_keeps_its_fence_and_frontmatter_checks(
        self,
    ) -> None:
        profile = next(
            p
            for p in self.registry.profiles
            if p.profile_id == "common/provider-native-metadata"
        )
        self.assertIsNone(profile.form)
        path = PurePosixPath(".claude/agents/example.md")
        unclosed = MARKDOWN._body_diagnostics(
            path, profile, "# Example\n\n```text\nopen\n"
        )
        self.assertEqual({item.rule_id for item in unclosed}, {"BODY-FENCE-UNCLOSED"})
        self.assertEqual(
            MARKDOWN._body_diagnostics(path, profile, "# Example\n\nBody text.\n"), []
        )

    def test_an_accepted_adr_in_the_range_keeps_its_retained_lists(self) -> None:
        adr = next(
            p
            for p in self.registry.profiles
            if p.profile_id == "sdlc/architecture-decision"
        )
        path = PurePosixPath(
            "docs/02.architecture/decisions/0002-argocd-helm-and-gitops-model.md"
        )
        body = (ROOT / path).read_text(encoding="utf-8").split("\n---\n", 1)[1]
        self.assertEqual(MARKDOWN._body_diagnostics(path, adr, body, "accepted"), [])
        broken = re.sub(r"(?m)^## Context\s*\n", "", body, count=1)
        rules = {
            item.rule_id
            for item in MARKDOWN._body_diagnostics(path, adr, broken, "accepted")
        }
        self.assertIn("BODY-HEADING-REQUIRED", rules)


class MeaningMapRecoveryPointerTests(unittest.TestCase):
    """SPEC-0209: no meaning map points at a Task that left the tree."""

    @staticmethod
    def meaning_maps(node: object) -> list[str]:
        found: list[str] = []
        if isinstance(node, dict):
            migration = node.get("migration")
            if isinstance(migration, dict) and "meaning_map" in migration:
                found.append(migration["meaning_map"])
            for value in node.values():
                found.extend(MeaningMapRecoveryPointerTests.meaning_maps(value))
        elif isinstance(node, list):
            for value in node:
                found.extend(MeaningMapRecoveryPointerTests.meaning_maps(value))
        return found

    def test_no_meaning_map_ends_with_the_dangling_task_clause(self) -> None:
        maps = self.meaning_maps(load_raw())
        self.assertGreaterEqual(len(maps), 32)
        self.assertEqual([item for item in maps if "the Task records it" in item], [])

    def test_a_recovery_pointer_names_the_package_of_its_own_token(self) -> None:
        pointer = re.compile(
            r"recover the map from the (SPEC-[0-9]{4}) recovery proof "
            r"in the REQ-0003 Archived Lineage\.$"
        )
        # SPEC-0221: a later migration replaces a role's map, so the number of
        # pointers is history, not a contract; every map that names a recovery
        # proof must point to it in the one form and name its own package.
        for text in self.meaning_maps(load_raw()):
            if "recovery proof" not in text:
                continue
            match = pointer.search(text)
            self.assertIsNotNone(match, text)
            self.assertEqual(re.search(r"SPEC-[0-9]{4}", text).group(0), match[1])


def core_bound_guide(raw: dict) -> dict:
    """SPEC-0222: bind the guide form to a small synthetic core whose one table
    the guide template carries exactly; the real core members arrive per unit."""

    form = next(f for f in raw["common_forms"]["forms"] if f["form_id"] == "guide")
    columns = [
        {
            "key": "step",
            "label": "Step",
            "value_type": "integer",
            "meaning": "order",
            "required": True,
        },
        {
            "key": "action",
            "label": "Action",
            "value_type": "enum",
            "meaning": "allowed action",
            "required": True,
            "allowed_values": ["run", "check"],
        },
    ]
    form["core_role"] = "guide"
    form["core"] = {
        "purpose": "p",
        "non_goals": "n",
        "metadata_policy": {},
        "tables": [
            {
                "table_id": "guide.steps",
                "section_id": "guide.steps",
                "required_when": "ordered_procedure",
                "columns": columns,
                "empty_policy": "no invented rows",
            }
        ],
        "language": {},
        "status": "s",
        "relationships": {},
        "lifecycle": {},
        "rules": ["r"],
    }
    stack = list(form["sections"])
    while stack:
        item = stack.pop()
        stack.extend(item["children"])
        item["core"] = {
            "title_ko": "t",
            "required_when": item["condition"],
            "content_rule": "c",
        }
        if item["level"] == 2:
            item["core"].update(prohibited_content="x", empty_policy="e")
    table = next(t for t in guide_tables(raw) if t["name"] == "Steps")
    table.update(
        table_id="guide.steps",
        section="guide.steps",
        required_when="ordered_procedure",
        empty_policy="no invented rows",
        columns=[
            {
                "key": c["label"],
                "id": c["key"],
                "data_type": c["value_type"],
                "meaning": c["meaning"],
                "required": c["required"],
                **(
                    {"allowed_values": c["allowed_values"]}
                    if "allowed_values" in c
                    else {}
                ),
            }
            for c in columns
        ],
    )
    return raw


def unbind_guide(raw: dict) -> dict:
    """SPEC-0222: the guide form without its core binding, so that a test of a
    local table rule can use the guide tables as a plain local fixture."""

    form = next(f for f in raw["common_forms"]["forms"] if f["form_id"] == "guide")
    del form["core_role"], form["core"]
    stack = list(form["sections"])
    while stack:
        item = stack.pop()
        stack.extend(item["children"])
        del item["core"]
    for table in guide_tables(raw):
        for key in ("table_id", "required_when", "empty_policy"):
            table.pop(key, None)
        for column in table["columns"]:
            column.pop("id", None)
    return raw


# SPEC-0222 WORK-005: the README and skill forms bind their core roles; each
# template of a role carries the role's core tables with these columns.
README_CORE_PATHS = (
    ("Path", "path", "path", "정규 위치"),
    ("Purpose", "purpose", "string", "독자가 찾을 내용"),
)
README_CORE_BINDINGS = {
    "root-readme": (
        "사람의 진입·사용·탐색",
        {"root-readme.paths": ("root-readme.map", "always", README_CORE_PATHS)},
    ),
    "stage-readme": (
        "단계의 소유 내용·현재 탐색",
        {"stage-readme.paths": ("stage-readme.contents", "always", README_CORE_PATHS)},
    ),
    "service-readme": (
        "선택 서비스 사용과 경계",
        {
            "service-readme.interface": (
                "service-readme.service",
                "external_interface",
                (
                    ("Interface", "interface", "identifier", "경계"),
                    ("Producer", "producer", "string", "생산자"),
                    ("Consumer", "consumer", "string", "소비자"),
                    ("Contract", "contract", "reference", "입출력 의미"),
                    ("Failure", "failure", "string", "실패 처리"),
                ),
            )
        },
    ),
    "skill": ("반복 가능한 호출형 절차", {}),
}


class ReadmeAndSkillCoreBindingTests(unittest.TestCase):
    """SPEC-0222 VAL-CORE-001: root, stage and service README and skill forms."""

    def test_each_form_binds_its_core_role_and_members(self) -> None:
        raw = load_raw()
        forms = {form["form_id"]: form for form in raw["common_forms"]["forms"]}
        for role, (purpose, tables) in README_CORE_BINDINGS.items():
            with self.subTest(role=role):
                form = forms[role]
                self.assertEqual(form.get("core_role"), role)
                self.assertEqual(form["core"]["purpose"], purpose)
                self.assertEqual(form["core"]["status"], "DESIGN_PROPOSAL_NOT_ADOPTED")
                self.assertEqual(
                    [table["table_id"] for table in form["core"]["tables"]],
                    list(tables),
                )
                for section in form["sections"]:
                    for item in (section, *section["children"]):
                        self.assertEqual(
                            item["core"]["required_when"], item["condition"]
                        )
        self.assertEqual(rules_of(raw), set())

    def test_each_template_carries_its_core_tables_exactly(self) -> None:
        raw = load_raw()
        for role, (_, tables) in README_CORE_BINDINGS.items():
            templates = [
                profile
                for profile in raw["profiles"]
                if profile["mode"] == "template"
                and profile.get("document_role") == role
            ]
            self.assertTrue(templates)
            for profile in templates:
                with self.subTest(profile=profile["id"]):
                    core = [
                        table
                        for table in profile["template_definition"]["tables"]
                        if "table_id" in table
                    ]
                    self.assertEqual(
                        {
                            table["table_id"]: (
                                table["section"],
                                table["required_when"],
                                tuple(
                                    (c["key"], c["id"], c["data_type"], c["meaning"])
                                    for c in table["columns"]
                                ),
                            )
                            for table in core
                        },
                        tables,
                    )
                    for table in core:
                        self.assertTrue(all(c["required"] for c in table["columns"]))


class CoreRoleBindingTests(unittest.TestCase):
    """SPEC-0222 VAL-CORE-001: the registry carries the common core binding."""

    def test_the_repository_records_the_core_identity_and_classifications(
        self,
    ) -> None:
        raw = load_raw()
        self.assertEqual(
            raw["common_forms"]["core"]["contract_id"],
            "workspace-document-role-design",
        )
        self.assertEqual(raw["common_forms"]["core"]["contract_version"], "4.0.0")
        forms = raw["common_forms"]["forms"]
        for form in forms:
            for extension in form["extensions"]:
                with self.subTest(extension=extension["id"]):
                    self.assertTrue(extension["authority_ref"].strip())
            if form.get("core_role") == "domain":
                self.assertTrue(form["classification"]["authority_ref"].strip())
        natives = [
            p
            for p in raw["profiles"]
            if (p.get("template_definition") or {}).get("core_role") == "native"
        ]
        self.assertTrue(natives)
        for profile in natives:
            self.assertEqual(profile["document_role"], "provider-native")
        self.assertEqual(rules_of(raw), set())

    def test_the_schema_refuses_a_misplaced_or_missing_core_member(self) -> None:
        cases = {}
        raw = load_raw()
        domain = next(
            f for f in raw["common_forms"]["forms"] if f.get("core_role") == "domain"
        )
        domain["core"] = {}
        cases["domain with core"] = raw
        raw = load_raw()
        form = next(f for f in raw["common_forms"]["forms"] if f["form_id"] == "guide")
        self.assertEqual(form["core_role"], "guide")
        del form["core"]
        cases["core role without core"] = raw
        raw = load_raw()
        del raw["common_forms"]["forms"][0]["extensions"][0]["authority_ref"]
        cases["extension without authority_ref"] = raw
        raw = load_raw()
        native = next(
            p
            for p in raw["profiles"]
            if (p.get("template_definition") or {}).get("core_role") == "native"
        )
        del native["template_definition"]["classification"]
        cases["native without classification"] = raw
        for name, payload in cases.items():
            with self.subTest(case=name):
                self.assertIn("REGISTRY_SCHEMA", rules_of(payload))

    def test_a_core_bound_form_with_its_exact_table_passes(self) -> None:
        self.assertEqual(rules_of(core_bound_guide(load_raw())), set())

    def test_each_table_drift_is_refused(self) -> None:
        def drift(change) -> set[str]:
            raw = core_bound_guide(load_raw())
            table = next(t for t in guide_tables(raw) if t["name"] == "Steps")
            change(table)
            return rules_of(raw)

        cases = {
            "relabeled column": lambda t: t["columns"][0].update(key="Order"),
            "same label, other type": lambda t: t["columns"][0].update(
                data_type="string"
            ),
            "appended column": lambda t: t["columns"].append(
                {
                    "key": "Note",
                    "id": "note",
                    "data_type": "string",
                    "meaning": "m",
                    "required": False,
                }
            ),
            "reordered columns": lambda t: t["columns"].reverse(),
            "dropped column": lambda t: t["columns"].pop(),
            "same type, other allowed values": lambda t: t["columns"][1].update(
                allowed_values=["run"]
            ),
            "allowed values dropped": lambda t: t["columns"][1].pop("allowed_values"),
            "other condition": lambda t: t.update(required_when="always"),
            "other section": lambda t: t.update(section="guide.purpose"),
        }
        for name, change in cases.items():
            with self.subTest(case=name):
                self.assertIn("REGISTRY_CORE_TABLE", drift(change))

    def test_a_missing_core_table_or_section_member_is_refused(self) -> None:
        raw = core_bound_guide(load_raw())
        table = next(t for t in guide_tables(raw) if t["name"] == "Steps")
        for key in ("table_id", "required_when", "empty_policy"):
            del table[key]
        self.assertEqual(rules_of(raw), {"REGISTRY_CORE_TABLE"})
        raw = core_bound_guide(load_raw())
        form = next(f for f in raw["common_forms"]["forms"] if f["form_id"] == "guide")
        del form["sections"][0]["core"]["empty_policy"]
        self.assertEqual(rules_of(raw), {"REGISTRY_CORE_SECTION"})

    def test_a_core_table_id_outside_a_core_role_form_is_refused(self) -> None:
        raw = unbind_guide(load_raw())
        table = next(t for t in guide_tables(raw) if t["name"] == "Steps")
        table.update(table_id="guide.steps", required_when="w", empty_policy="e")
        self.assertEqual(rules_of(raw), {"REGISTRY_CORE_TABLE"})

    def test_a_repeated_core_table_id_cannot_hide_a_drifted_copy(self) -> None:
        raw = core_bound_guide(load_raw())
        tables = guide_tables(raw)
        exact = next(t for t in tables if t["name"] == "Steps")
        copy = json.loads(json.dumps(exact))
        copy["name"] = "Shadow"
        copy["columns"][0]["data_type"] = "string"
        tables.insert(0, copy)
        self.assertIn("REGISTRY_CORE_TABLE", rules_of(raw))
        raw = core_bound_guide(load_raw())
        form = next(f for f in raw["common_forms"]["forms"] if f["form_id"] == "guide")
        form["core"]["tables"].append(json.loads(json.dumps(form["core"]["tables"][0])))
        self.assertIn("REGISTRY_CORE_TABLE", rules_of(raw))

    def test_an_extra_core_table_id_is_refused(self) -> None:
        raw = core_bound_guide(load_raw())
        table = next(t for t in guide_tables(raw) if t["name"] != "Steps")
        table.update(table_id="guide.other", required_when="w", empty_policy="e")
        self.assertIn("REGISTRY_CORE_TABLE", rules_of(raw))

    def test_the_core_identity_is_required_once_a_form_binds_a_core_role(
        self,
    ) -> None:
        raw = core_bound_guide(load_raw())
        del raw["common_forms"]["core"]
        self.assertEqual(rules_of(raw), {"REGISTRY_CORE_IDENTITY"})

    def test_a_native_core_role_only_on_a_form_less_provider_native_template(
        self,
    ) -> None:
        raw = load_raw()
        profile_of(raw, GUIDE[1])["template_definition"].update(
            core_role="native",
            classification={
                "owner": "platform",
                "reason": "r",
                "review_trigger": "t",
                "authority_ref": "a",
            },
        )
        self.assertEqual(rules_of(raw), {"REGISTRY_CORE_ROLE"})

    def test_section_core_members_follow_the_core(self) -> None:
        cases = {
            "condition differs": lambda f: f["sections"][0].update(condition="x"),
            "missing core": lambda f: f["sections"][0].pop("core"),
            "H2 missing prohibited_content": lambda f: f["sections"][0]["core"].pop(
                "prohibited_content"
            ),
            "H3 carries empty_policy": lambda f: f["sections"][0]["children"][0][
                "core"
            ].update(empty_policy="e"),
        }
        for name, change in cases.items():
            with self.subTest(case=name):
                raw = core_bound_guide(load_raw())
                form = next(
                    f for f in raw["common_forms"]["forms"] if f["form_id"] == "guide"
                )
                change(form)
                self.assertEqual(rules_of(raw), {"REGISTRY_CORE_SECTION"})


OPERATIONS_CORE = {
    "guide": {
        "guide.steps": ("guide.steps", "ordered_procedure", CORE_STEP_COLUMNS),
    },
    "runbook": {
        "runbook.steps": ("runbook.procedure", "always", CORE_STEP_COLUMNS),
    },
    "incident": {
        "incident.actions": ("incident.response", "always", CORE_ACTION_COLUMNS),
    },
    "postmortem": {
        "postmortem.actions": ("postmortem.actions", "always", CORE_ACTION_COLUMNS),
    },
    "policy": {
        "policy.rules": ("policy.rules", "always", POLICY_RULES_COLUMNS),
    },
}
OPERATIONS_TEMPLATES = {
    "guide": GUIDE[1],
    "runbook": RUNBOOK[1],
    "incident": INCIDENT[1],
    "postmortem": POSTMORTEM[1],
    "policy": POLICY_GOVERNANCE[1],
}


class OperationsCoreBindingTests(unittest.TestCase):
    """SPEC-0222 WORK-004: guide, runbook, incident and postmortem bind the core."""

    @staticmethod
    def form(raw: dict, role: str) -> dict:
        return next(f for f in raw["common_forms"]["forms"] if f["form_id"] == role)

    def test_each_form_binds_its_core_role_and_core_tables(self) -> None:
        raw = load_raw()
        for role, expected in OPERATIONS_CORE.items():
            with self.subTest(role=role):
                form = self.form(raw, role)
                self.assertEqual(form["core_role"], role)
                self.assertEqual(
                    {
                        t["table_id"]: (
                            t["section_id"],
                            t["required_when"],
                            tuple(c["label"] for c in t["columns"]),
                        )
                        for t in form["core"]["tables"]
                    },
                    expected,
                )
                stack = list(form["sections"])
                while stack:
                    item = stack.pop()
                    stack.extend(item["children"])
                    self.assertEqual(item["condition"], "always")
                    self.assertEqual(item["core"]["required_when"], "always")
                tables = {
                    t["table_id"]: t
                    for t in profile_of(raw, OPERATIONS_TEMPLATES[role])[
                        "template_definition"
                    ]["tables"]
                    if "table_id" in t
                }
                self.assertEqual(set(tables), set(expected))
                for table_id, (section_id, condition, labels) in expected.items():
                    table = tables[table_id]
                    self.assertEqual(
                        (table["section"], table["required_when"]),
                        (section_id, condition),
                    )
                    self.assertEqual(tuple(c["key"] for c in table["columns"]), labels)
                    self.assertEqual(table["row_identity"], labels[0])
        self.assertEqual(rules_of(raw), set())

    def test_the_core_value_types_reach_the_template_columns(self) -> None:
        raw = load_raw()
        types = {
            role: [
                (c["id"], c["data_type"])
                for t in profile_of(raw, OPERATIONS_TEMPLATES[role])[
                    "template_definition"
                ]["tables"]
                if "table_id" in t
                for c in t["columns"]
            ]
            for role in OPERATIONS_CORE
        }
        steps = [
            ("step", "integer"),
            ("action", "string"),
            ("expected", "string"),
            ("on_failure", "string"),
        ]
        actions = [
            ("action", "string"),
            ("owner", "string"),
            ("condition", "string"),
            ("evidence", "reference-or-none"),
        ]
        policy = [
            ("rule_id", "identifier"),
            ("condition", "condition"),
            ("requirement", "string"),
            ("enforcement", "reference-or-none"),
            ("evidence", "reference-or-none"),
        ]
        self.assertEqual(
            types,
            {
                "guide": steps,
                "runbook": steps,
                "incident": actions,
                "postmortem": actions,
                "policy": policy,
            },
        )
        # Both policy templates carry the same core table.
        twins = [
            next(
                t
                for t in profile_of(raw, template)["template_definition"]["tables"]
                if "table_id" in t
            )
            for template in (POLICY_GOVERNANCE[1], POLICY_OPERATIONS[1])
        ]
        self.assertEqual(twins[0], twins[1])

    def test_a_drifted_operations_core_table_is_refused(self) -> None:
        cases = {
            "relabeled": lambda t: t["columns"][0].update(key="Order"),
            "other type": lambda t: t["columns"][0].update(data_type="text"),
            "appended": lambda t: t["columns"].append(
                {
                    "key": "Note",
                    "id": "note",
                    "data_type": "string",
                    "meaning": "m",
                    "required": False,
                }
            ),
            "other section": lambda t: t.update(section=t["section"] + ".1"),
        }
        for role in OPERATIONS_CORE:
            for name, change in cases.items():
                with self.subTest(role=role, case=name):
                    raw = load_raw()
                    table = next(
                        t
                        for t in profile_of(raw, OPERATIONS_TEMPLATES[role])[
                            "template_definition"
                        ]["tables"]
                        if "table_id" in t
                    )
                    change(table)
                    self.assertIn("REGISTRY_CORE_TABLE", rules_of(raw))

    def test_the_registry_carries_the_core_tables_and_the_record_stays_projected(
        self,
    ) -> None:
        # SPEC-0222 WORK-001: the core binding of a table stays in the registry,
        # which the core check reads; the record keeps its own table fields.
        raw = load_raw()
        for role, template in OPERATIONS_TEMPLATES.items():
            with self.subTest(role=role):
                tables = profile_of(raw, template)["template_definition"]["tables"]
                self.assertEqual(
                    {t["table_id"] for t in tables if "table_id" in t},
                    set(OPERATIONS_CORE[role]),
                )
                record = CONTRACTS.template_definition_record(raw, template)
                self.assertEqual(record_errors(record), [])
                self.assertFalse(any("table_id" in t for t in record["tables"]))

    def test_every_runbook_renders_the_always_core_steps_table(self) -> None:
        # SPEC-0222: runbook.steps is always required; a runbook whose steps lack
        # a stated Expected Result keeps its header-only table (W04-CONTENT).
        profile = typed_profiles(load_raw())[RUNBOOK[0]]
        paths = sorted((ROOT / "docs/05.operations/runbooks").glob("0*.md"))
        self.assertTrue(paths)
        for path in paths:
            text = path.read_text(encoding="utf-8")
            relative = PurePosixPath(path.relative_to(ROOT).as_posix())
            with self.subTest(path=path.name):
                section = MARKDOWN._exact_heading_section(text, "## Procedure")
                headers = [
                    tuple(header)
                    for header, _ in MARKDOWN._visible_tables(section)
                    if header[0] == "Step"
                ]
                self.assertEqual(headers, [CORE_STEP_COLUMNS])
                self.assertEqual(
                    MARKDOWN._table_diagnostics(relative, profile, text), []
                )

    def test_the_converted_runbook_passes_and_its_former_header_fails(self) -> None:
        path = PurePosixPath(
            "docs/05.operations/runbooks/0012-main-release-preparation-runbook.md"
        )
        text = (ROOT / path).read_text(encoding="utf-8")
        profile = typed_profiles(load_raw())[RUNBOOK[0]]
        self.assertIn("| Step | Action | Expected Result | On Failure |", text)
        self.assertEqual(MARKDOWN._table_diagnostics(path, profile, text), [])
        former = text.replace(
            "| Step | Action | Expected Result | On Failure |",
            "| Step | Action | Expected result | Stop / escalate when |",
        )
        self.assertEqual(
            [d.rule_id for d in MARKDOWN._table_diagnostics(path, profile, former)],
            ["BODY-TABLE-COLUMNS"],
        )


DECISION_CORE_TREE = [
    ("decision.context", "문제와 조건", ["decision.context.1", "decision.context.2"]),
    ("decision.options", "대안", ["decision.options.1", "decision.options.2"]),
    ("decision.decision", "결정", ["decision.decision.1", "decision.decision.2"]),
    (
        "decision.consequences",
        "영향",
        ["decision.consequences.1", "decision.consequences.2"],
    ),
]
DECISION_OPTIONS_COLUMNS = [
    ("Option", "option"),
    ("Benefit", "benefit"),
    ("Cost and Risk", "cost"),
    ("Reason", "reason"),
]


class DecisionCoreBindingTests(unittest.TestCase):
    """SPEC-0222 WORK-006: the ADR form binds the core decision role."""

    def test_the_adr_form_carries_the_decision_core_and_its_table(self) -> None:
        raw = load_raw()
        form = next(f for f in raw["common_forms"]["forms"] if f["form_id"] == "adr")
        self.assertEqual(form["core_role"], "decision")
        self.assertEqual(form["core"]["purpose"], "중요 설계 선택의 이유")
        self.assertEqual(
            [
                (
                    s["section_id"],
                    s["core"]["title_ko"],
                    [c["section_id"] for c in s["children"]],
                )
                for s in form["sections"]
            ],
            DECISION_CORE_TREE,
        )
        (core_table,) = form["core"]["tables"]
        self.assertEqual(
            (
                core_table["table_id"],
                core_table["section_id"],
                core_table["required_when"],
                [(c["label"], c["key"]) for c in core_table["columns"]],
            ),
            (
                "decision.options",
                "decision.options",
                "always",
                DECISION_OPTIONS_COLUMNS,
            ),
        )
        table = next(
            t
            for t in profile_of(raw, ADR[1])["template_definition"]["tables"]
            if t.get("table_id") == "decision.options"
        )
        self.assertEqual(
            [(c["key"], c["id"]) for c in table["columns"]], DECISION_OPTIONS_COLUMNS
        )
        # The kept Alternatives table is a local table of its own: no core ID.
        local = next(
            t
            for t in profile_of(raw, ADR[1])["template_definition"]["tables"]
            if t["name"] == "Alternatives"
        )
        self.assertEqual(local["authority_ref"], "SPEC-0222")
        self.assertNotIn("table_id", local)
        self.assertEqual(rules_of(raw), set())
        # The record keeps its own table fields (WORK-001); the core binding stays
        # in the registry, which the core check reads.
        record = CONTRACTS.template_definition_record(raw, ADR[1])
        self.assertEqual(record["tables"][0]["name"], "Options")
        self.assertNotIn("table_id", record["tables"][0])
        self.assertEqual(current_rules(raw), set())

    def test_the_former_alternatives_header_on_the_adr_template_is_refused(
        self,
    ) -> None:
        raw = load_raw()
        table = next(
            t
            for t in profile_of(raw, ADR[1])["template_definition"]["tables"]
            if t.get("table_id") == "decision.options"
        )
        table["columns"][0]["key"] = "Alternative"
        self.assertIn("REGISTRY_CORE_TABLE", rules_of(raw))

    def test_a_core_table_cannot_carry_a_local_authority_ref(self) -> None:
        raw = load_raw()
        table = next(
            t
            for t in profile_of(raw, ADR[1])["template_definition"]["tables"]
            if t.get("table_id") == "decision.options"
        )
        table["authority_ref"] = "SPEC-0222"
        self.assertIn("REGISTRY_SCHEMA", rules_of(raw))

    def test_the_owner_lineage_reads_each_adr_where_its_form_keeps_the_table(
        self,
    ) -> None:
        link = "[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)"
        expected = "docs-01-requirements-0003-workspace-agent-governance-platform-md"
        registry = CONTRACTS.load_registry(ROOT)
        for number, section in (("0064", "Decision"), ("0050", "Traceability")):
            path = PurePosixPath(
                f"docs/02.architecture/decisions/{number}-temporary.md"
            )
            text = (
                '---\ntitle: "Decision title"\nversion: "1.0.0"\n'
                'type: "sdlc/architecture-decision"\nstatus: "accepted"\n'
                'owner: "platform"\nupdated: "2026-11-17"\n'
                f'artifact_id: "ADR-{number}"\n---\n\n# ADR-{number}: Decision title\n\n'
                f"## Context\n\nNo link here.\n\n## {section}\n\nServes {link}.\n"
            )
            context = types.SimpleNamespace(
                root=ROOT,
                texts={path: text},
                current_registry=registry,
                profiles={path: types.SimpleNamespace(profile_id=ADR[0])},
            )
            with self.subTest(section=section):
                self.assertEqual(LINKS._traceability_lineage(context, path), expected)


CORE_CHECK_TYPES = (
    ("Check ID", "check_id", "identifier"),
    ("Guarantee", "guarantee", "string"),
    ("Input", "input", "string"),
    ("Trust Boundary", "trust", "string"),
    ("Required When", "required_when", "condition"),
    ("Evidence", "evidence", "string"),
)
# SPEC-0222 WORK-003: the requirement, architecture, spec and plan forms bind
# their core roles; each existing table without a core counterpart stays a
# registered local table of its own (`authority_ref: ADR-0059`).
SDLC_CORE = {
    "requirement": (
        "필요·목표·검증 가능한 요구",
        REQUIREMENT[1],
        {
            "requirement.requirements": (
                "requirement.requirements",
                "always",
                (
                    ("Requirement ID", "requirement_id", "identifier"),
                    ("Statement", "statement", "string"),
                    ("Rationale", "rationale", "string"),
                    ("Acceptance", "acceptance", "string"),
                    ("Priority", "priority", "enum"),
                ),
            ),
            "requirement.quality": (
                "requirement.requirements",
                "quality_requirement",
                (
                    ("Requirement ID", "requirement_id", "identifier"),
                    ("Attribute", "attribute", "string"),
                    ("Measure", "measure", "string"),
                    ("Unit", "unit", "string"),
                    ("Environment", "environment", "string"),
                    ("Criterion", "criterion", "string"),
                ),
            ),
        },
        ("Lifecycle Traceability",),
    ),
    "architecture": (
        "목표 구조와 현재 적용 상태",
        ARCHITECTURE[1],
        {
            "architecture.interface": (
                "architecture.structure",
                "external_interface",
                (
                    ("Interface", "interface", "identifier"),
                    ("Producer", "producer", "string"),
                    ("Consumer", "consumer", "string"),
                    ("Contract", "contract", "reference"),
                    ("Failure", "failure", "string"),
                ),
            )
        },
        ("Constraints", "Quality Scenarios", "Lifecycle Traceability"),
    ),
    "spec": (
        "범위 있는 변경의 관측 가능한 계약",
        SPEC_FORM[1],
        {"spec.checks": ("spec.acceptance", "always", CORE_CHECK_TYPES)},
        ("Criteria", "Lifecycle Traceability"),
    ),
    "plan": (
        "실행 전략과 의존성",
        PLAN_FORM[1],
        {
            "plan.work_units": (
                "plan.work",
                "always",
                (
                    ("Work Unit", "work_unit", "identifier"),
                    ("Outcome", "outcome", "string"),
                    ("Depends On", "depends_on", "reference-list"),
                    ("Owner", "owner", "string"),
                    ("Write Scope", "write_scope", "path-list"),
                    ("Acceptance", "acceptance", "reference-list"),
                    ("Checks", "checks", "reference-list"),
                ),
            ),
            "plan.checks": ("plan.verification", "always", CORE_CHECK_TYPES),
        },
        ("Work Breakdown", "Promotion"),
    ),
}
# Architecture descriptions that state an external interface render the core
# table; with no stated failure handling per interface it stays header-only and
# the missing facts are residue (W04-CONTENT). AD-0006 leaves external service
# interfaces to their own domains (AD-0007), so it renders none.
AD_INTERFACE_TABLES = {
    "0004-argo-rollouts-progressive-delivery.md": 0,
    "0005-argo-notifications-slack.md": 0,
    "0006-workspace-agent-governance-platform.md": None,
    "0007-current-local-gitops-platform.md": 0,
}


def _frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf'(?m)^{key}: "([^"]*)"$', text.split("\n---", 1)[0])
    return match.group(1) if match else ""


class SdlcCoreBindingTests(unittest.TestCase):
    """SPEC-0222 WORK-003: requirement, architecture, spec and plan bind the core."""

    @staticmethod
    def form(raw: dict, role: str) -> dict:
        return next(f for f in raw["common_forms"]["forms"] if f["form_id"] == role)

    @staticmethod
    def visible_headers(text: str, heading: str) -> list[tuple[str, ...]]:
        section = MARKDOWN._exact_heading_section(text, heading) or ""
        return [tuple(header) for header, _ in MARKDOWN._visible_tables(section)]

    def test_each_form_binds_its_core_role_members_and_section_conditions(
        self,
    ) -> None:
        raw = load_raw()
        for role, (purpose, _, tables, _) in SDLC_CORE.items():
            with self.subTest(role=role):
                form = self.form(raw, role)
                self.assertEqual(form["core_role"], role)
                self.assertEqual(form["core"]["purpose"], purpose)
                self.assertEqual(form["core"]["status"], "DESIGN_PROPOSAL_NOT_ADOPTED")
                self.assertEqual(
                    {
                        t["table_id"]: (
                            t["section_id"],
                            t["required_when"],
                            tuple(
                                (c["label"], c["key"], c["value_type"])
                                for c in t["columns"]
                            ),
                        )
                        for t in form["core"]["tables"]
                    },
                    tables,
                )
                stack = list(form["sections"])
                while stack:
                    item = stack.pop()
                    stack.extend(item["children"])
                    self.assertEqual(item["condition"], "always")
                    self.assertEqual(item["requiredness"], "required")
                    self.assertEqual(item["core"]["required_when"], "always")
        self.assertEqual(rules_of(raw), set())

    def test_each_template_carries_its_core_tables_and_local_tables_of_its_own(
        self,
    ) -> None:
        raw = load_raw()
        for role, (_, template, tables, local) in SDLC_CORE.items():
            with self.subTest(role=role):
                definition_ = profile_of(raw, template)["template_definition"]
                core = {
                    t["table_id"]: t for t in definition_["tables"] if "table_id" in t
                }
                self.assertEqual(
                    {
                        table_id: (
                            t["section"],
                            t["required_when"],
                            tuple(
                                (c["key"], c["id"], c["data_type"])
                                for c in t["columns"]
                            ),
                        )
                        for table_id, t in core.items()
                    },
                    tables,
                )
                for table in core.values():
                    self.assertTrue(all(c["required"] for c in table["columns"]))
                    self.assertEqual(table["row_identity"], table["columns"][0]["key"])
                    self.assertNotIn("authority_ref", table)
                own = [t for t in definition_["tables"] if "table_id" not in t]
                self.assertEqual(sorted(t["name"] for t in own), sorted(local))
                for table in own:
                    self.assertEqual(table["authority_ref"], "ADR-0059")
                # The record keeps its own table fields (WORK-001).
                record = CONTRACTS.template_definition_record(raw, template)
                self.assertEqual(record_errors(record), [])
                self.assertFalse(any("table_id" in t for t in record["tables"]))
        priority = next(
            c
            for t in profile_of(raw, REQUIREMENT[1])["template_definition"]["tables"]
            if t.get("table_id") == "requirement.requirements"
            for c in t["columns"]
            if c["key"] == "Priority"
        )
        self.assertEqual(priority["allowed_values"], ["must", "should", "could"])
        self.assertEqual(rules_of(raw), set())

    def test_a_drifted_sdlc_core_table_is_refused(self) -> None:
        cases = {
            "relabeled": lambda t: t["columns"][0].update(key="Name"),
            "other type": lambda t: t["columns"][0].update(data_type="string"),
            "appended": lambda t: t["columns"].append(
                {
                    "key": "Note",
                    "id": "note",
                    "data_type": "string",
                    "meaning": "m",
                    "required": False,
                }
            ),
            "other section": lambda t: t.update(section=t["section"] + ".1"),
            "dropped": lambda t: t["columns"].pop(),
        }
        for role, (_, template, tables, _) in SDLC_CORE.items():
            for table_id in tables:
                for name, change in cases.items():
                    with self.subTest(role=role, table=table_id, case=name):
                        raw = load_raw()
                        table = next(
                            t
                            for t in profile_of(raw, template)["template_definition"][
                                "tables"
                            ]
                            if t.get("table_id") == table_id
                        )
                        change(table)
                        self.assertIn("REGISTRY_CORE_TABLE", rules_of(raw))
        raw = load_raw()
        self.form(raw, "requirement")["sections"][2]["children"][1].update(
            condition="품질 요구가 적용됨"
        )
        self.assertIn("REGISTRY_CORE_SECTION", rules_of(raw))

    def test_every_requirement_renders_the_core_table_with_core_priorities(
        self,
    ) -> None:
        profile = typed_profiles(load_raw())[REQUIREMENT[0]]
        paths = sorted((ROOT / "docs/01.requirements").glob("0*.md"))
        self.assertTrue(paths)
        for path in paths:
            text = path.read_text(encoding="utf-8")
            relative = PurePosixPath(path.relative_to(ROOT).as_posix())
            with self.subTest(path=path.name):
                section = MARKDOWN._exact_heading_section(text, "## Requirements")
                self.assertIsNotNone(section)
                self.assertIn("### Quality Requirements", section)
                tables = [
                    (header, rows)
                    for header, rows in MARKDOWN._visible_tables(section)
                    if header[0] == "Requirement ID"
                ]
                self.assertTrue(tables)
                for header, rows in tables:
                    self.assertEqual(tuple(header), REQUIREMENT_COLUMNS)
                    for row in rows:
                        self.assertIn(row[-1], {"must", "should", "could"})
                self.assertEqual(
                    MARKDOWN._table_diagnostics(relative, profile, text), []
                )
                self.assertEqual(
                    MARKDOWN._requirement_quality_diagnostics(relative, profile, text),
                    [],
                )

    def test_each_description_renders_the_interface_table_where_it_applies(
        self,
    ) -> None:
        profile = typed_profiles(load_raw())[ARCHITECTURE[0]]
        folder = ROOT / "docs/02.architecture/descriptions"
        self.assertEqual(
            sorted(p.name for p in folder.glob("0*.md")), sorted(AD_INTERFACE_TABLES)
        )
        for name, rows in AD_INTERFACE_TABLES.items():
            text = (folder / name).read_text(encoding="utf-8")
            with self.subTest(path=name):
                section = MARKDOWN._exact_heading_section(text, "### Interfaces") or ""
                found = [
                    len(data)
                    for header, data in MARKDOWN._visible_tables(section)
                    if tuple(header) == ARCHITECTURE_INTERFACE_COLUMNS
                ]
                self.assertEqual(found, [] if rows is None else [rows])
                relative = PurePosixPath((folder / name).relative_to(ROOT).as_posix())
                self.assertEqual(
                    MARKDOWN._table_diagnostics(relative, profile, text), []
                )

    def test_every_current_spec_and_plan_renders_its_core_tables_unless_retained(
        self,
    ) -> None:
        profiles = typed_profiles(load_raw())
        cases = {
            "spec.md": ("sdlc/spec", {"## Acceptance Criteria": [CORE_CHECK_COLUMNS]}),
            "plan.md": (
                "sdlc/plan",
                {
                    "## Work Breakdown": [CORE_WORK_UNIT_COLUMNS],
                    "## Verification Plan": [CORE_CHECK_COLUMNS],
                },
            ),
        }
        retained = []
        for package in sorted((ROOT / "docs/03.specs").glob("0*/")):
            for name, (profile_id, headings) in cases.items():
                path = package / name
                if not path.is_file():
                    continue
                text = path.read_text(encoding="utf-8")
                profile = profiles[profile_id]
                identity = _frontmatter_value(text, "artifact_id")
                status = _frontmatter_value(text, "status")
                relative = PurePosixPath(path.relative_to(ROOT).as_posix())
                with self.subTest(path=str(relative)):
                    core = {CORE_CHECK_COLUMNS, CORE_WORK_UNIT_COLUMNS}
                    if status == "approved" and profile.form.retains_identity(identity):
                        # SPEC-0161 and SPEC-0221 keep their approved bytes.
                        retained.append(identity)
                        self.assertFalse(
                            core
                            & {
                                tuple(header)
                                for header, _ in MARKDOWN._visible_tables(text)
                            }
                        )
                    else:
                        for heading, expected in headings.items():
                            found = [
                                header
                                for header in self.visible_headers(text, heading)
                                if header in core
                            ]
                            self.assertEqual(found, expected)
                    self.assertEqual(
                        MARKDOWN._table_diagnostics(relative, profile, text, status),
                        [],
                    )
        self.assertEqual(
            sorted(retained),
            [
                "SPEC-0161",
                "SPEC-0161-PLAN-0001",
                "SPEC-0221",
                "SPEC-0221-PLAN-0001",
            ],
        )

    def test_the_core_tables_sit_beside_the_local_tables_their_readers_use(
        self,
    ) -> None:
        profiles = typed_profiles(load_raw())
        spec = spec_form_body().replace(
            "### Verification Strategy\n\nThe Verification Strategy of the change.",
            "### Verification Strategy\n\nThe Verification Strategy of the change.\n\n"
            + form_table(CORE_CHECK_COLUMNS),
        )
        plan = (
            plan_form_body()
            .replace(
                form_table(PLAN_FORM_TABLE_KEYS["Work Breakdown"][1]),
                form_table(PLAN_FORM_TABLE_KEYS["Work Breakdown"][1])
                + "\n\n"
                + form_table(CORE_WORK_UNIT_COLUMNS),
            )
            .replace(
                "### Selected Checks\n\nThe Selected Checks of the work.",
                "### Selected Checks\n\nThe Selected Checks of the work.\n\n"
                + form_table(CORE_CHECK_COLUMNS),
            )
        )
        for path, profile_id, text in (
            (SPEC_PATH, "sdlc/spec", spec),
            (PLAN_PATH, "sdlc/plan", plan),
        ):
            with self.subTest(profile=profile_id):
                profile = profiles[profile_id]
                self.assertEqual(MARKDOWN._table_diagnostics(path, profile, text), [])
                rows = LINKS._body_contract_rows(text, profile)
                self.assertTrue(rows)
                self.assertEqual(
                    tuple(rows[0]), tuple(profile.body_contract.required_columns)
                )
                wrong = text.replace(
                    "| Check ID | Guarantee |", "| Check ID | Promise |"
                )
                self.assertEqual(
                    [
                        d.rule_id
                        for d in MARKDOWN._table_diagnostics(path, profile, wrong)
                    ],
                    ["BODY-TABLE-COLUMNS"],
                )
        relabeled = plan.replace("| Depends On |", "| Dependencies |", 1)
        self.assertNotIn("Work Unit | Outcome | Depends On", relabeled)
        self.assertEqual(
            [
                d.rule_id
                for d in MARKDOWN._table_diagnostics(
                    PLAN_PATH, profiles["sdlc/plan"], relabeled
                )
            ],
            ["BODY-TABLE-COLUMNS"],
        )


if __name__ == "__main__":
    unittest.main()
