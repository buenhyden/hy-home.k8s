"""SPEC-0168: the common form model, its registry checks and heading-tree checks."""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import importlib.util
import json
import re
import sys
import tempfile
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
    "reference-report",
)
# W03-D20, W03-D26, W03-D33: one Stage 99 local role has no form
# (provider-native keeps none; reference-report gets one in W03-D36).
LOCAL_ROLE_IDS = ("provider-native",)
# The schema role order: the 18 first roles, reference-report, the governance
# document and governance role, the six small local roles, then provider-native.
ROLE_IDS = (
    FORM_IDS[:18] + FORM_IDS[26:] + FORM_IDS[24:26] + FORM_IDS[18:24] + LOCAL_ROLE_IDS
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
    "reference/audit": "reference-report",
    "reference/research": "reference-report",
    "reference/data": "reference-report",
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
# SPEC-0194 (W03-D65): four common columns and the one optional Status extension.
POLICY_RULES_COLUMNS = ("Rule ID", "Condition", "Level", "Evidence")
POLICY_RULES_OPTIONAL = ("Status",)
POLICY_RULES_TABLE = (
    "policy-rules-requirements",
    (*POLICY_RULES_COLUMNS, *POLICY_RULES_OPTIONAL),
    0,
    "Rule ID",
)
AGENTS = ("common/folder-agents-guide", "common/template-agents-guide")
AGENTS_TREE = (
    ("Scope", ("Allowed Surface", "Non-goals")),
    ("Required Policies", ("Canonical Sources", "Local Obligations")),
    ("Workflow", ("Inspect and Change", "Handoff")),
    ("Verification", ("Required Checks", "Evidence and Limits")),
    ("Safety", ("Protected Actions", "Stop and Escalate")),
)
AGENTS_TABLE_KEYS = {
    "Tool Rules": (
        "agents-required-policies-local-obligations",
        ("Rule", "Trigger", "Effect"),
        0,
        "Rule",
    )
}
SKILL_GOVERNANCE = ("governance/skill", "common/template-governance-skill")
SKILL_NATIVE = ("common/native-skill-package", "common/template-native-skill")
SKILL_TREE = (
    ("Purpose and Trigger", ("When to Use", "When Not to Use")),
    ("Procedure", ("Steps", "Failure Handling")),
    ("Inputs and Outputs", ("Inputs", "Outputs")),
    ("Verification", ("Checks", "Completion and Handoff")),
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
    "parent_id": "skill-purpose-and-trigger",
    "title": "Authority Boundary",
}
SKILL_TABLE_KEYS = {
    "Steps": ("skill-procedure-steps", ("Step", "Input", "Output"), 0, "Step")
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
        "parent_id": "reference-pack-readme-pack-contract",
        "title": "Separate Evidence Axes",
    },
]
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
# SPEC-0195 (W03-D03, W03-D08, W03-D55): the Requirement form, its two local H3
# extensions and its three tables (the requirement id, statement, rationale and
# acceptance of the common contract, then the optional trailing Priority).
REQUIREMENT = ("sdlc/requirement", "common/template-sdlc-requirement")
REQUIREMENT_TREE = (
    ("Overview", ("Problem and Outcome", "Stakeholders")),
    ("Scope", ("In Scope", "Constraints and Exclusions")),
    ("Requirements", ("Functional Requirements", "Quality Requirements")),
    ("Acceptance Criteria", ("Acceptance Conditions", "Verification Method")),
    ("Traceability", ("Source and Constraints", "Downstream Links")),
)
REQUIREMENT_EXTENSIONS = [
    {
        "id": "requirement-lifecycle-traceability",
        "kind": "local_h3",
        "condition": (
            "a requirement in a status the body contract enforces (draft, "
            "in-review, approved) maps each member to its acceptance criterion "
            "and downstream owner"
        ),
        "owner": "platform",
        "verification": "the body-contract check",
        "review": "when the Requirement form version changes",
        "removal": "when requirement lineage has another registered owner",
        "parent_id": "requirement-traceability",
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
        "parent_id": "requirement-traceability",
        "title": "Archived Lineage",
    },
]
REQUIREMENT_COLUMNS = ("Requirement ID", "Statement", "Rationale", "Acceptance")
REQUIREMENT_OPTIONAL = ("Priority",)
REQUIREMENT_TABLE_KEYS = {
    "Functional Requirements": (
        "requirement-requirements-functional-requirements",
        (*REQUIREMENT_COLUMNS, *REQUIREMENT_OPTIONAL),
        1,
        "Requirement ID",
    ),
    "Quality Requirements": (
        "requirement-requirements-quality-requirements",
        (*REQUIREMENT_COLUMNS, *REQUIREMENT_OPTIONAL),
        0,
        "Requirement ID",
    ),
    "Lifecycle Traceability": (
        "requirement-lifecycle-traceability",
        ("Requirement ID", "Acceptance criterion", "Downstream owner"),
        1,
        "Requirement ID",
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
# SPEC-0189: the one reference-report form of the audit, research and data reports.
REFERENCE_FORM = (
    "reference/audit",
    "common/template-reference-audit",
    "reference/research",
    "common/template-reference-research",
    "reference/data",
    "common/template-reference-data",
)
REFERENCE_H2 = (
    "Overview",
    "Reference Type",
    "Authority Boundary",
    "Scope",
    "Definitions / Facts",
    "Sources",
    "Review and Freshness",
    "Related Documents",
)
# The 31 conditional H3 titles per H2 in form order: each report kind's template
# titles and the 15 historical titles that two or more research reports share.
REFERENCE_H3 = {
    "Overview": ("Historical overview and observation boundary",),
    "Reference Type": ("Historical reference classification",),
    "Authority Boundary": ("Historical authority statement",),
    "Scope": (
        "Criteria and Inspected Surface",
        "Historical scope",
        "Research Questions",
        "Method",
    ),
    "Definitions / Facts": (
        "Observed Evidence",
        "Findings and Gaps",
        "Historical observations and corrections \u2014 2026-08-08 to 2026-09-05",
        "Current external analysis",
        "Historical analysis and dated observations",
        "Current external research",
        "Follow-up workspace questions",
        "Claim-Source Matrix",
        "Findings",
        "Schema",
        "Repository Facts",
    ),
    "Sources": (
        "Historical source provenance",
        "Current primary sources",
        "Historical sources",
        "Provenance",
    ),
    "Review and Freshness": (
        "Remediation",
        "Verification State",
        "Current review boundary",
        "Historical refresh record",
        "Dated history retained from 2026-08-08 through 2026-09-14",
        "Limitations",
        "Recommendations",
        "Generation and Refresh",
        "Staleness Boundaries",
    ),
    "Related Documents": (),
}
REFERENCE_TREE = tuple((title, REFERENCE_H3[title]) for title in REFERENCE_H2)
REFERENCE_FORMS = (
    (
        "reference-report",
        "Reference Report",
        REFERENCE_FORM,
        REFERENCE_TREE,
        [],
        "Related Documents",
    ),
)
# The nine tables of the three twins, each named by its form section id (SPEC-0179
# moved them to heading lines; SPEC-0189 gives the role a form).
REFERENCE_TABLES = {
    "common/template-reference-audit": [
        (
            "Criterion",
            "reference-report-scope-criteria-and-inspected-surface",
            ("Criterion", "In-scope surface"),
            0,
            "Criterion",
        ),
        (
            "Observation",
            "reference-report-definitions-facts-observed-evidence",
            ("Observation", "Source and input", "Result"),
            0,
            "Observation",
        ),
        (
            "ID",
            "reference-report-definitions-facts-findings-and-gaps",
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
        (
            "Remediation",
            "reference-report-review-and-freshness-remediation",
            ("Remediation", "Owner", "Due or decision date"),
            0,
            "Remediation",
        ),
    ],
    "common/template-reference-research": [
        (
            "Claim",
            "reference-report-definitions-facts-claim-source-matrix",
            ("Claim", "Source", "Verification state"),
            0,
            "Claim",
        ),
        (
            "Source",
            "reference-report-sources",
            ("Source", "Grade", "Retrieved", "Relevance"),
            0,
            "Source",
        ),
    ],
    "common/template-reference-data": [
        (
            "Field",
            "reference-report-definitions-facts-schema",
            ("Field", "Meaning and unit", "Producer"),
            0,
            "Field",
        ),
        (
            "Source",
            "reference-report-sources-provenance",
            ("Source", "Revision or observation", "Derivation"),
            0,
            "Source",
        ),
        (
            "Generation command",
            "reference-report-review-and-freshness-generation-and-refresh",
            ("Generation command", "Refresh trigger", "Owner"),
            0,
            "Generation command",
        ),
    ],
}
# The source profile of each twin inherits the twin's tables.
REFERENCE_PROFILE_TABLES = {
    **REFERENCE_TABLES,
    "reference/audit": REFERENCE_TABLES["common/template-reference-audit"],
    "reference/research": REFERENCE_TABLES["common/template-reference-research"],
    "reference/data": REFERENCE_TABLES["common/template-reference-data"],
}
# Every local form in registry order: the six small forms, SPEC-0188's two, then
# SPEC-0189's reference-report.
LOCAL_FORMS = SMALL_FORMS + GOVERNANCE_FORMS + REFERENCE_FORMS


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
# The reference-report form also keeps its Sources section link-only (W03-D36).
LOCAL_LINK_ONLY["reference-report"].add("reference-report-sources")
# The twenty-two roles that carry a form; every other profile keeps its H2 lists.
FORM_PROFILES = (
    REQUIREMENT
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
    + REFERENCE_FORM
)
FORM_TEMPLATES = (
    REQUIREMENT[1],
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
    REFERENCE_FORM[1],
    REFERENCE_FORM[3],
    REFERENCE_FORM[5],
)
TWENTY_TWO_FORMS = [
    "guide",
    "runbook",
    "incident",
    "postmortem",
    "root-readme",
    "stage-readme",
    "service-readme",
    "policy",
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
    "reference-report",
    "requirement",
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
        "contract_version": "COMMON-DOC-FORM-1/1.0.0",
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
    def test_repository_registry_binds_clear_roles_and_carries_exactly_the_twenty_two_forms(
        self,
    ) -> None:
        raw = load_raw()
        self.assertIsInstance(raw["schema_version"], str)
        self.assertEqual(
            int(raw["schema_version"].split(".")[0]), AUTHORITY.REGISTRY_MAJOR
        )
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
                ("agents", "AGENTS"),
                ("skill", "Skill"),
                ("workspace-readme", "Workspace README"),
                ("reference-pack-readme", "Reference Pack README"),
                *((form_id, title) for form_id, title, *_ in LOCAL_FORMS),
                ("requirement", "Requirement"),
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
                        f"{form_id}-{slug(title)}",
                        title,
                        position,
                        [
                            (
                                f"{form_id}-{slug(title)}-{slug(child)}",
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
                    "runbook": {"runbook-recovery-rollback"},
                    "reference-pack-readme": {
                        f"reference-pack-readme-{title.lower().replace(' ', '-')}"
                        for title in PACK_NOT_REQUIRED
                    },
                    "requirement": {"requirement-requirements-quality-requirements"},
                    "reference-report": {
                        f"reference-report-{slug(h2)}-{slug(h3)}"
                        for h2, titles in REFERENCE_H3.items()
                        for h3 in titles
                    },
                }.get(form_id, set()),
            )
            self.assertTrue(all(isinstance(n.get("link_only"), bool) for n in every))
            self.assertEqual(
                {node["section_id"] for node in every if node.get("link_only")},
                LOCAL_LINK_ONLY.get(form_id, set()),
            )
            if form_id != "reference-report":
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
                        REFERENCE_TABLES[twin]
                        if form_id == "reference-report"
                        else [(name, *spec) for name, spec in tables.items()]
                        if isinstance(tables, dict)
                        else tables
                    ),
                )
                for table in by_id[twin]["template_definition"]["tables"]:
                    for column in table["columns"]:
                        self.assertTrue(column["meaning"])
                        # The research Sources table dates its retrieval (W03-D21).
                        self.assertEqual(
                            column["data_type"],
                            "date" if column["key"] == "Retrieved" else "string",
                        )
                        self.assertIs(
                            column["required"],
                            not (
                                form_id in ("root-readme", "stage-readme")
                                and column["key"] == "Owner"
                                or form_id == "policy"
                                and column["key"] in POLICY_RULES_OPTIONAL
                                or form_id == "requirement"
                                and column["key"] in REQUIREMENT_OPTIONAL
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

    def test_repository_registry_loads_with_exactly_the_twenty_two_forms(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        self.assertEqual(
            [item.form_id for item in registry.common_forms],
            TWENTY_TWO_FORMS,
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
            "agents": ["Tool Rules"],
            "skill": ["Steps"],
            "workspace-readme": [],
            "reference-pack-readme": [],
            "requirement": [
                "Functional Requirements",
                "Quality Requirements",
                "Lifecycle Traceability",
            ],
            **{
                form_id: [name for name, *_ in tables]
                for form_id, _, _, _, tables, _ in LOCAL_FORMS
            },
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
                            ("agents", AGENTS),
                            ("skill", SKILL_GOVERNANCE + SKILL_NATIVE),
                            ("workspace-readme", WORKSPACE_FORM),
                            ("reference-pack-readme", PACK_FORM),
                            ("requirement", REQUIREMENT),
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
                        else [
                            n for n, *_ in REFERENCE_PROFILE_TABLES[profile.profile_id]
                        ]
                        if role == "reference-report"
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

    def test_schema_role_enum_is_twenty_eight_and_form_enum_is_twenty_seven(
        self,
    ) -> None:
        schema = json.loads(
            (
                ROOT / "docs/99.templates/contracts/document-profile.schema.json"
            ).read_text("utf-8")
        )
        profile_role = schema["properties"]["profiles"]["items"]["properties"][
            "document_role"
        ]["enum"]
        form_id = schema["$defs"]["common_form"]["properties"]["form_id"]["enum"]
        self.assertEqual(len(ROLE_IDS), 28)
        self.assertEqual(tuple(profile_role), ROLE_IDS)
        self.assertEqual(tuple(form_id), FORM_IDS)
        self.assertEqual(len(form_id), 27)
        self.assertEqual(
            [item.form_id for item in CONTRACTS.load_registry(ROOT).common_forms],
            TWENTY_TWO_FORMS,
        )
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
            TWENTY_TWO_FORMS,
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
    HEADER: tuple[str, ...]  # its required columns, in order
    OPTIONAL: tuple[str, ...] = ()  # its optional trailing columns, in order
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
        self.assertEqual(
            tuple(c.key for t in twin.tables for c in t.columns if not c.required),
            self.OPTIONAL,
        )

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
    HEADER = POLICY_RULES_COLUMNS
    OPTIONAL = POLICY_RULES_OPTIONAL
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
    HEADER = POLICY_RULES_COLUMNS
    OPTIONAL = POLICY_RULES_OPTIONAL
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


AGENTS_PATH = PurePosixPath("scripts/AGENTS.md")


def agents_body() -> str:
    return md(
        "# AGENTS.md",
        "Agent instructions for `scripts/`.",
        "## Scope",
        "### Allowed Surface\n\nValidators only.",
        "### Non-goals\n\nThis folder adds no non-goal beyond the parent `AGENTS.md`; "
        "if work here must be excluded, state it here.",
        "## Required Policies",
        "### Canonical Sources\n\nThe quality policy.",
        "### Local Obligations\n\n1. Keep the change small.",
        "## Workflow",
        "### Inspect and Change\n\nFollow the rules above.",
        "### Handoff\n\nThis folder hands off through the work lifecycle's Completion "
        "steps with no extra field; if it needs one, state it here.",
        "## Verification",
        "### Required Checks\n\nRun the suite.",
        "### Evidence and Limits\n\nRepository-static only.",
        "## Safety",
        "### Protected Actions\n\nNone beyond the policy.",
        "### Stop and Escalate\n\nStop on a failed check.",
    )


class AgentsFormTests(RoleFormBody):
    """SPEC-0176 VAL-AGENTS-001: the AGENTS form on every AGENTS.md."""

    PATH = AGENTS_PATH
    PROFILES = AGENTS
    FORM_ID = "agents"
    TREE = AGENTS_TREE
    TABLE_KEYS = AGENTS_TABLE_KEYS
    BODY = agents_body()
    HEADER = ("Rule", "Trigger", "Effect")
    HOME = "1. Keep the change small."

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
                self.assertEqual(
                    raw["sections"], {"required": [], "optional": [], "forbidden": []}
                )
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
            self.tree(self.BODY.replace("### Handoff", "### Handover")),
            ["BODY-H3-REQUIRED", "BODY-H3-UNSUPPORTED"],
        )
        self.assertEqual(
            self.tree(self.BODY.replace("### Handoff\n", "### Handoff\n\n#### Deep\n")),
            [],
        )
        self.assertEqual(
            self.tree(self.under("## Safety", "### Stray\n\nText.")),
            ["BODY-H3-UNSUPPORTED"],
        )

    def test_the_table_is_not_looked_at_outside_its_section(self) -> None:
        wrong = self.table(self.HEADER[:2], ("a", "b"))
        body = self.with_table(wrong, home="The quality policy.")
        self.assertEqual(self.tables(body), [])


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

    def with_line(self, line: str, heading: str = "### Handoff") -> str:
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
        "## Purpose and Trigger",
        "### When to Use\n\nUse it when a change needs review.",
        "### When Not to Use\n\nNot for a one-line fix.",
        "## Procedure",
        "### Steps\n\n1. Run the check.",
        "### Failure Handling\n\nStop on a failed check.",
        "## Inputs and Outputs",
        "### Inputs\n\nThe request.",
        "### Outputs\n\nA report.",
        "## Verification",
        "### Checks\n\nRun the suite.",
        "### Completion and Handoff\n\nRecord the result.",
    )
    return md(*((preface,) if preface else ()), *blocks)


# TestCase is named again so the static collector sees a runnable base.
class SkillFormBody(RoleFormBody, unittest.TestCase):
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
        self.assertEqual(table["section"], "skill-procedure-steps")
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
        for heading in ("## Inputs and Outputs", "## Verification"):
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
        self.assertEqual(
            profile_of(load_raw(), self.PROFILES[0])["sections"],
            {"required": [], "optional": [], "forbidden": []},
        )

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
                self.assertEqual(
                    raw["sections"], {"required": [], "optional": [], "forbidden": []}
                )
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


def pack_body(*extra: tuple[str, str]) -> str:
    """A pack README; `extra` is (H2 title, body) of the optional sections."""

    later = dict(extra)
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
                self.assertEqual(
                    profile["sections"],
                    {"required": [], "optional": [], "forbidden": []},
                )
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

    def test_related_documents_may_be_a_link_list_and_no_other_section(self) -> None:
        self.assertEqual(self.tree(self.BODY), [])
        plain = re.sub(r"(## Structure\n\n)[^\n]*", r"\1- [a](a.md)", self.BODY)
        self.assertEqual(self.tree(plain), ["BODY-SECTION-EMPTY"])
        bare = re.sub(r"(## Related Documents\n\n)[^\n]*", r"\1", self.BODY)
        self.assertEqual(self.tree(bare), ["BODY-SECTION-EMPTY"])

    def test_the_form_has_the_two_registered_local_h3s(self) -> None:
        self.assertEqual(self.raw_form()["extensions"], PACK_EXTENSIONS)

    def test_the_three_closure_sections_and_method_are_not_required(self) -> None:
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
        required = tuple(t for t in every if t not in PACK_NOT_REQUIRED)
        by_id = {profile.profile_id: profile for profile in registry.profiles}
        for profile_id in PACK_FORM:
            with self.subTest(profile=profile_id):
                headings = by_id[profile_id].headings
                self.assertEqual(headings.required, required)
                self.assertEqual(headings.allowed, every)

    def test_each_conditional_section_may_be_absent_or_present(self) -> None:
        self.assertEqual(self.tree(self.BODY), [])
        for title in PACK_NOT_REQUIRED:
            with self.subTest(section=title):
                body = pack_body((title, "The pack states it."))
                self.assertEqual(self.tree(body), [])
                empty = pack_body((title, ""))
                self.assertEqual(self.tree(empty), ["BODY-SECTION-EMPTY"])

    def test_every_closure_section_is_accepted_at_once_in_form_order(self) -> None:
        body = pack_body(*((title, "Stated.") for title in PACK_NOT_REQUIRED))
        self.assertEqual(self.tree(body), [])
        early = body.replace(
            "## Usage", "## Review and Closure\n\nEarly.\n\n## Usage", 1
        )
        early = early.replace("## Review and Closure\n\nStated.\n\n", "", 1)
        self.assertEqual(self.tree(early), ["BODY-H2-ORDER"])

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
                    self.assertEqual(
                        raw["sections"],
                        {"required": [], "optional": [], "forbidden": []},
                    )
                    self.assertEqual(self.profiles[profile_id].form.form_id, form_id)
        self.assertEqual(
            profile_of(self.raw, "evaluation/raw-output")["sections"],
            {"required": [], "optional": [], "forbidden": []},
        )
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
                    profile_of(raw, profile_id)["sections"]["required"] = ["Overview"]
                    self.assertIn("REGISTRY_FORM_LEGACY_LISTS", rules_of(raw))


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
        self.assertEqual(len(forms), 22)
        self.assertEqual(list(forms)[-4:-2], ["governance-document", "governance-role"])
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
                    self.assertEqual(
                        raw["sections"],
                        {"required": [], "optional": [], "forbidden": []},
                    )
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
                    profile_of(raw, profile_id)["sections"]["required"] = ["Overview"]
                    self.assertIn("REGISTRY_FORM_LEGACY_LISTS", rules_of(raw))

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


class ReferenceReportFormTests(unittest.TestCase):
    """SPEC-0189 VAL-REFFORM-001: the reference-report form of the three report kinds."""

    AUDIT_H3 = {
        "Scope": ("Criteria and Inspected Surface",),
        "Definitions / Facts": ("Observed Evidence", "Findings and Gaps"),
        "Review and Freshness": ("Remediation", "Verification State"),
    }
    RESEARCH_H3 = {
        "Scope": ("Research Questions", "Method"),
        "Definitions / Facts": ("Claim-Source Matrix", "Findings"),
        "Review and Freshness": ("Limitations", "Recommendations"),
    }
    DATA_H3 = {
        "Definitions / Facts": ("Schema", "Repository Facts"),
        "Sources": ("Provenance",),
        "Review and Freshness": ("Generation and Refresh", "Staleness Boundaries"),
    }
    KINDS = {
        "reference/audit": ("audits", AUDIT_H3),
        "reference/research": ("research", RESEARCH_H3),
        "reference/data": ("data", DATA_H3),
    }
    # (H2, count of conditional H3) and (parent H2, count of local_h3 extensions).
    CONDITIONAL_BY_H2 = {
        "Overview": 1,
        "Reference Type": 1,
        "Authority Boundary": 1,
        "Scope": 4,
        "Definitions / Facts": 11,
        "Sources": 4,
        "Review and Freshness": 9,
        "Related Documents": 0,
    }
    EXTENSIONS_BY_H2 = {
        "Definitions / Facts": 33,
        "Sources": 3,
        "Review and Freshness": 3,
    }
    LINK = "- [Source](https://example.com/a), grade A, retrieved 2026-11-13."

    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = load_raw()
        cls.profiles = typed_profiles(cls.raw)
        cls.form = next(
            f
            for f in cls.raw["common_forms"]["forms"]
            if f["form_id"] == "reference-report"
        )

    @staticmethod
    def body(h3: dict, *, sources: str | None = None) -> str:
        blocks = ["# Reference: Sample"]
        for h2 in REFERENCE_H2:
            children = h3.get(h2, ())
            if h2 == "Related Documents":
                blocks.append(f"## {h2}\n\n- [Owner](owner.md)")
            elif children:
                blocks.append(f"## {h2}")
                blocks += [f"### {c}\n\nThe {c} text." for c in children]
            elif h2 == "Sources":
                blocks.append(f"## {h2}\n\n{sources or ReferenceReportFormTests.LINK}")
            else:
                blocks.append(f"## {h2}\n\nThe {h2} text.")
        return md(*blocks)

    def rules(self, profile_id: str, text: str) -> list[str]:
        folder, _ = self.KINDS[profile_id]
        path = PurePosixPath(f"docs/90.references/{folder}/0001-sample/m0001-sample.md")
        return sorted(
            item.rule_id
            for item in MARKDOWN._body_diagnostics(
                path, self.profiles[profile_id], text, "published"
            )
        )

    def research(self, text: str) -> list[str]:
        return self.rules("reference/research", text)

    def test_the_form_is_a_stage_99_local_form_with_eight_required_h2(self) -> None:
        stage = next(
            f
            for f in self.raw["common_forms"]["forms"]
            if f["form_id"] == "stage-readme"
        )
        form = self.form
        self.assertEqual(form["title"], "Reference Report")
        self.assertEqual(form["h1"], "{{document_title}}")
        self.assertEqual(form["language_rule"], stage["language_rule"])
        for needle in (
            "Stage 99",
            "W03-D20",
            "W03-D26",
            "W03-D35",
            "W03-D36",
            "COMMON-DOC-FORM-1",
        ):
            self.assertIn(needle, form["extension_policy"])
        self.assertNotEqual(form["extension_policy"], stage["extension_policy"])
        self.assertEqual([s["title"] for s in form["sections"]], list(REFERENCE_H2))
        self.assertEqual(self.raw["common_forms"]["contract_id"], "COMMON-DOC-FORM-1")
        for node in form["sections"]:
            with self.subTest(section=node["title"]):
                self.assertEqual(node["requiredness"], "required")
                self.assertEqual(node["condition"], "always")
                self.assertEqual(node["empty_policy"], "explain_none_or_not_applicable")
                self.assertIs(
                    node["link_only"], node["title"] in ("Sources", "Related Documents")
                )

    def test_every_section_carries_the_form_fields_and_a_slug_id(self) -> None:
        nodes = [n for s in self.form["sections"] for n in (s, *s["children"])]
        self.assertEqual(len(nodes), 39)
        for node in nodes:
            with self.subTest(section=node["section_id"]):
                self.assertTrue(node["content"])
                self.assertTrue(node["required_content"])
                self.assertTrue(node["prohibited_content"])
                self.assertEqual(
                    node["validation_ids"], ["FORM-STRUCTURE", "FORM-CONTENT-REVIEW"]
                )
                self.assertIsInstance(node["link_only"], bool)
                prefix = "reference-report-"
                if node["level"] == 2:
                    self.assertEqual(node["section_id"], prefix + slug(node["title"]))
                else:
                    self.assertEqual(
                        node["section_id"],
                        f"{node['parent_id']}-{slug(node['title'])}",
                    )

    def test_sources_asks_for_link_grade_and_iso_retrieval_date(self) -> None:
        sources = self.form["sections"][5]
        self.assertEqual(sources["title"], "Sources")
        text = " ".join(sources["required_content"])
        for needle in ("링크", "등급", "ISO"):
            self.assertIn(needle, text)

    def test_the_form_holds_thirty_one_conditional_h3_in_registered_order(self) -> None:
        counts = {}
        for node in self.form["sections"]:
            counts[node["title"]] = len(node["children"])
            self.assertEqual(
                [c["title"] for c in node["children"]],
                list(REFERENCE_H3[node["title"]]),
            )
            for child in node["children"]:
                with self.subTest(h3=child["section_id"]):
                    self.assertEqual(child["level"], 3)
                    self.assertEqual(child["requiredness"], "conditional")
                    self.assertNotEqual(child["condition"], "always")
                    self.assertEqual(child["empty_policy"], "omit_when_condition_false")
                    self.assertIs(child["link_only"], False)
        self.assertEqual(counts, self.CONDITIONAL_BY_H2)
        self.assertEqual(sum(counts.values()), 31)

    def test_each_conditional_h3_names_its_own_report_kind_or_history(self) -> None:
        conditions = [
            (c["title"], c["condition"])
            for s in self.form["sections"]
            for c in s["children"]
        ]
        self.assertEqual(len({text for _, text in conditions}), 31)
        for title, text in conditions:
            with self.subTest(h3=title):
                if title in {
                    t
                    for kind in (self.AUDIT_H3, self.DATA_H3)
                    for v in kind.values()
                    for t in v
                }:
                    self.assertTrue("audit" in text or "data" in text, text)
                else:
                    self.assertIn("research", text)

    def test_the_thirty_nine_local_h3_extensions_are_one_document_titles(self) -> None:
        extensions = self.form["extensions"]
        self.assertEqual(len(extensions), 39)
        self.assertEqual(len({e["id"] for e in extensions}), 39)
        by_id = {s["section_id"]: s for s in self.form["sections"]}
        counts: dict[str, int] = {}
        for item in extensions:
            with self.subTest(extension=item["id"]):
                self.assertEqual(item["kind"], "local_h3")
                self.assertEqual(item["owner"], "platform")
                self.assertEqual(item["verification"], "the form tree check")
                for field in ("condition", "review", "removal", "title"):
                    self.assertTrue(item[field])
                parent = by_id[item["parent_id"]]
                counts[parent["title"]] = counts.get(parent["title"], 0) + 1
                self.assertNotIn(
                    item["title"], [c["title"] for c in parent["children"]]
                )
        self.assertEqual(counts, self.EXTENSIONS_BY_H2)
        under_sources = sorted(
            e["title"]
            for e in extensions
            if e["parent_id"] == "reference-report-sources"
        )
        self.assertEqual(under_sources, ["Findings", "Limitations", "Recommendations"])
        titles = [e["title"] for e in extensions]
        self.assertTrue(
            any("\u2014" in title and "2026-" in title for title in titles),
            "a dated title keeps its em dash and date",
        )

    def test_the_six_profiles_hold_no_h2_list_and_the_pack_profiles_do_not_change(
        self,
    ) -> None:
        for profile_id in REFERENCE_FORM:
            with self.subTest(profile=profile_id):
                raw = profile_of(self.raw, profile_id)
                self.assertEqual(raw["document_role"], "reference-report")
                self.assertEqual(
                    raw["sections"], {"required": [], "optional": [], "forbidden": []}
                )
                typed = self.profiles[profile_id]
                self.assertEqual(typed.form.form_id, "reference-report")
                self.assertEqual(typed.headings.required, REFERENCE_H2)
        for profile_id in PACK_FORM:
            self.assertEqual(
                profile_of(self.raw, profile_id)["document_role"],
                "reference-pack-readme",
            )
        bound = sorted(
            p["id"]
            for p in self.raw["profiles"]
            if p.get("document_role") == "reference-report"
        )
        self.assertEqual(bound, sorted(REFERENCE_FORM))

    def test_the_nine_tables_use_form_section_ids(self) -> None:
        ids = {
            n["section_id"] for s in self.form["sections"] for n in (s, *s["children"])
        }
        for twin, expected in REFERENCE_TABLES.items():
            with self.subTest(twin=twin):
                tables = profile_of(self.raw, twin)["template_definition"]["tables"]
                self.assertEqual(
                    [
                        (
                            t["name"],
                            t["section"],
                            tuple(c["key"] for c in t["columns"]),
                            t["minimum_rows"],
                            t["row_identity"],
                        )
                        for t in tables
                    ],
                    expected,
                )
                for table in tables:
                    self.assertIn(table["section"], ids)
                    self.assertFalse(table["section"].startswith("#"))
        self.assertEqual(sum(len(v) for v in REFERENCE_TABLES.values()), 9)

    def test_a_table_section_must_be_a_form_section_id(self) -> None:
        twin = "common/template-reference-research"
        for section_text in (
            "### Claim-Source Matrix",
            "## Sources",
            "reference-report-nope",
        ):
            raw = load_raw()
            profile_of(raw, twin)["template_definition"]["tables"][0]["section"] = (
                section_text
            )
            with self.subTest(section=section_text):
                self.assertIn("REGISTRY_TABLE_SECTION", rules_of(raw))
        self.assertEqual(rules_of(load_raw()), set())

    def test_the_twin_definitions_say_the_role_has_its_own_form(self) -> None:
        for twin in REFERENCE_TABLES:
            definition_ = profile_of(self.raw, twin)["template_definition"]
            with self.subTest(twin=twin):
                first, second = definition_["non_goals"][:2]
                self.assertNotIn("has no form", first)
                self.assertIn("own local form", first)
                for needle in ("W03-D20", "W03-D26", "W03-D35", "W03-D36"):
                    self.assertIn(needle, first)
                self.assertIn("COMMON-DOC-FORM-1", first)
                self.assertIn("owned by the form", second)
                for path in (
                    "scripts/validate-document-contract-registry.py",
                    "scripts/validation/repository/form_contracts.py",
                    "scripts/validation/repository/quality.py",
                ):
                    self.assertIn(path, definition_["consumer_paths"])
                    self.assertTrue((ROOT / path).is_file())
                self.assertEqual(
                    len(definition_["consumer_paths"]),
                    len(set(definition_["consumer_paths"])),
                )
                text = json.dumps(definition_["validation"])
                self.assertIn("form tree check", text)
                self.assertNotIn("heading line", text)
                self.assertIn("SPEC-0189", definition_["migration"]["meaning_map"])
        research = profile_of(self.raw, "common/template-reference-research")
        self.assertIn(
            "W03-D21", research["template_definition"]["migration"]["meaning_map"]
        )

    def test_the_three_templates_pass_the_form_tree(self) -> None:
        for template in ("audit", "research", "data"):
            twin = self.profiles[f"common/template-reference-{template}"]
            with self.subTest(template=template):
                path = PurePosixPath(twin.template)
                text = (ROOT / path).read_text(encoding="utf-8")
                found = MARKDOWN.validate_document_text(text, path, twin, "strict")
                self.assertEqual([item.rule_id for item in found], [])

    def test_a_report_of_each_kind_passes_the_tree(self) -> None:
        for profile_id, (_, h3) in self.KINDS.items():
            with self.subTest(profile=profile_id):
                self.assertEqual(self.rules(profile_id, self.body(h3)), [])

    def test_a_report_with_no_h3_passes_and_a_missing_conditional_h3_passes(
        self,
    ) -> None:
        self.assertEqual(self.research(self.body({})), [])
        partial = {**self.RESEARCH_H3, "Scope": ("Research Questions",)}
        self.assertEqual(self.research(self.body(partial)), [])

    def test_a_missing_or_renamed_required_h2_fails(self) -> None:
        text = self.body(self.RESEARCH_H3)
        missing = text.replace("## Related Documents\n\n- [Owner](owner.md)\n", "")
        self.assertEqual(self.research(missing), ["BODY-HEADING-REQUIRED"])
        renamed = text.replace("## Reference Type", "## Kind")
        self.assertEqual(
            self.research(renamed),
            ["BODY-HEADING-REQUIRED", "BODY-HEADING-UNSUPPORTED"],
        )

    def test_a_reordered_h2_fails(self) -> None:
        text = self.body({})
        swapped = (
            text.replace("## Scope", "## @@")
            .replace("## Overview", "## Scope")
            .replace("## @@", "## Overview")
        )
        self.assertEqual(self.research(swapped), ["BODY-H2-ORDER"])

    def test_a_reordered_conditional_h3_fails(self) -> None:
        swapped = {**self.RESEARCH_H3, "Scope": ("Method", "Research Questions")}
        self.assertEqual(self.research(self.body(swapped)), ["BODY-H3-ORDER"])

    def test_an_unregistered_h3_is_refused(self) -> None:
        stray = {**self.RESEARCH_H3, "Scope": ("Research Questions", "Stray")}
        self.assertEqual(self.research(self.body(stray)), ["BODY-H3-UNSUPPORTED"])

    def test_an_h3_under_the_wrong_h2_is_refused(self) -> None:
        wrong = {**self.RESEARCH_H3, "Sources": ("Method",)}
        self.assertEqual(self.research(self.body(wrong)), ["BODY-H3-PARENT"])

    def test_a_duplicate_h3_is_refused(self) -> None:
        twice = {**self.RESEARCH_H3, "Scope": ("Method", "Method")}
        self.assertIn("BODY-H3-DUPLICATE", self.research(self.body(twice)))

    def test_a_registered_extension_is_accepted_only_under_its_h2(self) -> None:
        item = next(
            e for e in self.form["extensions"] if e["parent_id"].endswith("-sources")
        )
        under_sources = {**self.RESEARCH_H3, "Sources": (item["title"],)}
        self.assertEqual(self.research(self.body(under_sources)), [])
        under_scope = {**self.RESEARCH_H3, "Scope": (item["title"],)}
        self.assertEqual(self.research(self.body(under_scope)), ["BODY-H3-PARENT"])

    def test_a_bare_or_empty_section_fails(self) -> None:
        text = self.body(self.RESEARCH_H3)
        empty = text.replace("The Overview text.", "")
        self.assertEqual(self.research(empty), ["BODY-SECTION-EMPTY"])
        hollow = text.replace("The Method text.", "")
        self.assertEqual(self.research(hollow), ["BODY-SECTION-EMPTY"])

    def test_only_sources_and_related_documents_accept_a_list_of_links(self) -> None:
        text = self.body(self.RESEARCH_H3)
        self.assertEqual(self.research(text), [])
        plain = text.replace("The Overview text.", "- [a](a.md)")
        self.assertEqual(self.research(plain), ["BODY-SECTION-EMPTY"])
        listed = self.body({}, sources="- [a](https://example.com/a)\n- [b](b.md)")
        self.assertEqual(self.research(listed), [])

    def test_the_old_h2_lists_are_refused_on_a_profile_with_a_form(self) -> None:
        raw = load_raw()
        profile_of(raw, "reference/research")["sections"]["required"] = list(
            REFERENCE_H2
        )
        self.assertIn("REGISTRY_FORM_LEGACY_LISTS", rules_of(raw))


REQUIREMENT_PATH = PurePosixPath(
    "docs/01.requirements/0001-argo-rollouts-progressive-delivery.md"
)
REQUIREMENT_HEADER = (*REQUIREMENT_COLUMNS, *REQUIREMENT_OPTIONAL)
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
            "Priority": "Must",
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
        "## Acceptance Criteria",
        "### Acceptance Conditions\n\nThe controller is available.",
        "### Verification Method\n\nEach Acceptance cell names its evidence.",
        "## Traceability",
        "### Source and Constraints\n\nNo upstream requirement exists.",
        "### Downstream Links\n\n- **AD**: [AD 0004](../02.architecture/x.md)",
        "### Lifecycle Traceability\n\n"
        "| Requirement ID | Acceptance criterion | Downstream owner |\n"
        "| --- | --- | --- |\n"
        "| REQ-0001-FR-0001 | The controller is available. | AD 0004 |",
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

    def test_the_form_has_five_h2_ten_h3_and_one_conditional_section(self) -> None:
        form = next(f for f in self.registry.common_forms if f.form_id == "requirement")
        self.assertEqual(form.title, "Requirement")
        self.assertEqual(
            [(s.title, tuple(c.title for c in s.children)) for s in form.sections],
            list(REQUIREMENT_TREE),
        )
        every = [n for s in form.sections for n in (s, *s.children)]
        self.assertEqual(
            [n.title for n in every if n.requiredness != "required"],
            ["Quality Requirements"],
        )
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
                self.assertEqual(
                    raw["sections"],
                    {"required": [], "optional": [], "forbidden": []},
                )
                self.assertEqual(raw["document_role"], "requirement")
                headings = self.profiles[profile_id].headings
                self.assertEqual(headings.required, titles)
                self.assertEqual(headings.allowed, titles)
                contract = raw["relationships"]["body_contract"]
                self.assertEqual(contract["section"], "Traceability")
                self.assertEqual(contract["table_heading"], "Lifecycle Traceability")
                self.assertEqual(
                    contract["required_columns"],
                    ["Requirement ID", "Acceptance criterion", "Downstream owner"],
                )
                self.assertEqual(
                    contract["enforced_statuses"], ["draft", "in-review", "approved"]
                )
                self.assertEqual(
                    contract["allowed_target_profile_ids"],
                    ["sdlc/architecture-description", "sdlc/spec"],
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
        self.assertEqual(
            [(t.name, c.key) for t in twin.tables for c in t.columns if not c.required],
            [
                ("Functional Requirements", "Priority"),
                ("Quality Requirements", "Priority"),
            ],
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

    def test_a_complete_document_passes_with_and_without_quality_requirements(
        self,
    ) -> None:
        for quality in (True, False):
            with self.subTest(quality=quality):
                body = requirement_body(quality=quality)
                self.assertEqual(self.tree(body), [])
                self.assertEqual(self.tables(body), [])
        self.assertNotIn("Quality Requirements", requirement_body(quality=False))

    def test_a_removed_h2_or_a_missing_h3_fails_the_tree(self) -> None:
        old = requirement_body().replace("## Scope", "## Scope and Non-goals")
        found = set(self.tree(old))
        self.assertLessEqual(
            {"BODY-HEADING-REQUIRED", "BODY-HEADING-UNSUPPORTED"}, found
        )
        lost = requirement_body().replace(
            "### Verification Method\n\nEach Acceptance cell names its evidence.\n\n",
            "",
        )
        self.assertEqual(self.tree(lost), ["BODY-H3-REQUIRED"])

    def test_an_h3_under_the_wrong_h2_is_refused(self) -> None:
        body = requirement_body()
        quality = "### Quality Requirements\n\n" + requirement_table(kind="NFR")
        moved = body.replace(quality + "\n\n", "").replace(
            "## Traceability", quality + "\n\n## Traceability"
        )
        self.assertEqual(self.tree(moved), ["BODY-H3-PARENT"])

    def test_archived_lineage_and_lifecycle_traceability_belong_under_traceability(
        self,
    ) -> None:
        body = requirement_body()
        lineage = "### Archived Lineage\n\nSPEC-0004 left the tree.\n"
        for heading in ("## Overview", "## Scope", "## Acceptance Criteria"):
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
        for header in (REQUIREMENT_HEADER, REQUIREMENT_COLUMNS):
            with self.subTest(header=header):
                body = requirement_body().replace(
                    requirement_table(), requirement_table(header)
                )
                self.assertEqual(self.tables(body), [])
        for header in (
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
        body = requirement_body()
        empty_quality = body.replace(
            requirement_table(kind="NFR"), requirement_table(kind="NFR", rows=0)
        )
        self.assertEqual(self.tables(empty_quality), [])
        empty_functional = body.replace(requirement_table(), requirement_table(rows=0))
        self.assertEqual(self.tables(empty_functional), ["BODY-TABLE-ROWS"])

    def test_the_body_contract_table_is_not_read_as_a_requirement_table(self) -> None:
        body = requirement_body()
        self.assertIn(
            "| Requirement ID | Acceptance criterion | Downstream owner |", body
        )
        self.assertEqual(self.tables(body), [])

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
                'artifact_id: "ADR-0099"\n---\n\n' + body
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


# SPEC-0196 (W03-D56, W03-D65): the full TemplateDefinition record.
SCHEMA_COPY = ROOT / "docs/99.templates/contracts/template-definition.schema.json"
# The package schema TEMPLATE-DEFINITION.schema.json of the v14.7 revision; any
# byte change is a deliberate change of this digest and of the file.
SCHEMA_COPY_SHA256 = "e490cf402419bd1e8204d665b5774f8c9869f28e31879d1b4f3ea39d550364ff"
COMMON_RECORD_ROLES = frozenset(FORM_IDS[:16])
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


def schema_copy() -> dict:
    return json.loads(SCHEMA_COPY.read_text("utf-8"))


def record_errors(record: dict) -> list:
    return schema_errors(schema_copy(), record)


def form_headings(item: dict) -> dict:
    """The form section as a package heading: every field but the local flag."""

    return {
        **{
            key: value
            for key, value in item.items()
            if key not in {"link_only", "children"}
        },
        "children": [form_headings(child) for child in item["children"]],
    }


class TemplateRecordTests(unittest.TestCase):
    """VAL-TDREC-001: one 19-field record per template, derived from its owners."""

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

    def test_the_schema_copy_digest_is_pinned(self) -> None:
        self.assertEqual(
            hashlib.sha256(SCHEMA_COPY.read_bytes()).hexdigest(), SCHEMA_COPY_SHA256
        )

    def test_the_record_fields_follow_the_required_list_of_the_schema_copy(
        self,
    ) -> None:
        self.assertEqual(
            list(CONTRACTS.TEMPLATE_RECORD_FIELDS), schema_copy()["required"]
        )
        self.assertEqual(len(CONTRACTS.TEMPLATE_RECORD_FIELDS), 19)

    def test_every_template_with_a_definition_has_the_nineteen_key_record(
        self,
    ) -> None:
        self.assertTrue(self.templates)
        for profile in self.templates:
            with self.subTest(template=profile["id"]):
                record = self.records[profile["id"]]
                self.assertEqual(list(record), schema_copy()["required"])
                self.assertEqual(self.tolerated(profile, record_errors(record)), [])

    def test_the_record_is_derived_from_the_profile_and_form(self) -> None:
        for profile in self.templates:
            with self.subTest(template=profile["id"]):
                record = self.records[profile["id"]]
                definition = profile["template_definition"]
                self.assertEqual(record["template_id"], profile["id"])
                self.assertEqual(record["role"], profile["document_role"])
                self.assertEqual(
                    record["contract_version"], definition["contract_version"]
                )
                for key in (
                    "purpose",
                    "responsibility",
                    "non_goals",
                    "policy_refs",
                    "vocabulary_refs",
                    "applicability",
                    "tables",
                    "consumer_paths",
                    "validation",
                    "migration",
                ):
                    self.assertEqual(record[key], definition[key])
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
            for key in ("headings", "extensions", "contract_version"):
                with self.subTest(role=role, key=key):
                    self.assertEqual(
                        len(
                            {json.dumps(item[key], sort_keys=True) for item in records}
                        ),
                        1,
                    )

    def test_the_contract_version_names_the_contract_of_its_role(self) -> None:
        common = self.raw["common_forms"]
        for profile in self.templates:
            role = profile["document_role"]
            expected = (
                f"{common['contract_id']}/{common['version']}"
                if role in COMMON_RECORD_ROLES
                else "STAGE99-LOCAL-FORM-1/1.0.0"
            )
            with self.subTest(template=profile["id"]):
                self.assertEqual(
                    profile["template_definition"]["contract_version"], expected
                )

    def test_the_templates_without_a_definition_are_the_sdlc_templates(self) -> None:
        without = [
            item
            for item in self.raw["profiles"]
            if item["mode"] == "template" and "template_definition" not in item
        ]
        self.assertTrue(without)
        for profile in without:
            with self.subTest(template=profile["id"]):
                self.assertIn(profile["document_role"], SDLC_ROLES)
                with self.assertRaises(ValueError):
                    CONTRACTS.template_definition_record(self.raw, profile["id"])
        for profile in self.templates:
            self.assertNotIn(profile["document_role"], SDLC_ROLES - {"requirement"})

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

    def test_a_common_value_that_differs_from_the_common_form_version_fails(
        self,
    ) -> None:
        raw = load_raw()
        self.definition(raw, GUIDE[1])["contract_version"] = "COMMON-DOC-FORM-1/9.9.9"
        self.assertIn("REGISTRY_TEMPLATE_RECORD", current_rules(raw))

    def test_a_common_value_on_a_role_without_a_form_fails(self) -> None:
        raw = load_raw()
        for profile_id in self.NATIVES:
            self.definition(raw, profile_id)["contract_version"] = (
                "COMMON-DOC-FORM-1/1.0.0"
            )
        self.assertIn("REGISTRY_TEMPLATE_RECORD", current_rules(raw))

    def test_a_value_outside_the_grammar_fails(self) -> None:
        for value in (
            "COMMON-DOC-FORM-1",
            "COMMON-DOC-FORM-1/",
            "COMMON-DOC-FORM-1/1.0",
            "COMMON-DOC-FORM-1/v1.0.0",
            "common-doc-form-1/1.0.0",
            "STAGE99-LOCAL-FORM-1/01.0.0",
            "/1.0.0",
            " STAGE99-LOCAL-FORM-1/1.0.0",
        ):
            raw = load_raw()
            self.definition(raw, "common/template-governance-prompt")[
                "contract_version"
            ] = value
            with self.subTest(value=value):
                self.assertIn("REGISTRY_TEMPLATE_RECORD", current_rules(raw))

    def test_two_values_on_one_role_fail(self) -> None:
        raw = load_raw()
        self.definition(raw, "common/template-readme-stage-index")[
            "contract_version"
        ] = "STAGE99-LOCAL-FORM-1/1.0.0"
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


class CurrentRegistryTenFormsOnlyTests(unittest.TestCase):
    def test_only_the_twenty_two_form_profiles_use_the_tree(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        self.assertEqual(
            [item.form_id for item in registry.common_forms],
            TWENTY_TWO_FORMS,
        )
        self.assertEqual(
            sorted(p.profile_id for p in registry.profiles if p.form is not None),
            sorted(FORM_PROFILES),
        )
        self.assertEqual(
            sorted(p.profile_id for p in registry.profiles if p.template_definition),
            sorted(FORM_TEMPLATES + LOCAL_TEMPLATES),
        )


if __name__ == "__main__":
    unittest.main()
