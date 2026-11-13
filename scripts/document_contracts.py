"""Typed document-profile registry loading and deterministic path routing."""

from __future__ import annotations

import ast
import copy
import json
import re
import stat
import subprocess
from dataclasses import dataclass, field as dataclass_field, replace
from functools import lru_cache
from types import MappingProxyType
from pathlib import Path, PurePosixPath
from typing import Any, Literal, Mapping, NoReturn, Sequence

import yaml

from document_authority import (
    AuthorityError,
    REGISTRY_MAX_BYTES,
    load_bounded_json,
    read_bounded_utf8,
    run_bounded_process,
    validate_registry_authority,
)
from json_schema_validation import SchemaEvaluationError, schema_errors
from validation.repository.bounded_io import (
    BoundedInputError,
    read_bytes as read_bounded_bytes,
)


GIT_TIMEOUT_SECONDS = 10
TASK_FIRST_RECORDING_EXTENSION = (
    "Local candidate Task first-recording of observed draft, ready, in-progress, "
    "or blocked state"
)
SPEC_PLAN_DIRECT_APPROVAL_EXTENSION = (
    "Local candidate Spec/Plan direct draft-to-approved transition "
    "after actual batch review and approval"
)
SPEC_PLAN_FIRST_APPROVED_EXTENSION = (
    "Local candidate Spec/Plan first-recording as approved after actual batch "
    "review and approval"
)
TASK_INITIAL_STATES = ("draft", "ready", "in-progress", "blocked")
# The shared contract's local extensions apply at each of these stages.
SHARED_STAGES = ("candidate", "approved", "adopted")
# SPEC-0168: the one policy role that governance/rule and operation/policy share.
POLICY_ROLE_SOURCES = ("governance/rule", "operation/policy")
MARKDOWN_TEMPLATE_PLACEHOLDER = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}")
DOCUMENT_TEXT_MAX_BYTES = 16 * 1024 * 1024
_LS_FILES_MODES = {b"100644", b"100755", b"120000", b"160000"}
ROOT_FILES = ("AGENTS.md", "CHANGELOG.md", "CLAUDE.md", "README.md")
TARGET_ROOTS = (
    "_workspace",
    ".agents",
    ".claude",
    ".codex",
    ".github",
    "docs",
    "examples",
    "gitops",
    "infrastructure",
    "policy",
    "scripts",
    "secrets",
    "tests",
)
REGISTRY_PATH = PurePosixPath("docs/99.templates/registry.json")
PROFILE_SCHEMA_PATH = PurePosixPath(
    "docs/99.templates/contracts/document-profile.schema.json"
)
# Compatibility name for direct callers of ``validate_registry``.  The only
# schema it may load is the root-registry profile schema.
SCHEMA_PATH = PROFILE_SCHEMA_PATH
_UNSET = object()


@dataclass(frozen=True)
class Route:
    kind: Literal["exact", "regex"]
    value: str


@dataclass(frozen=True)
class Diagnostic:
    rule_id: str
    path: PurePosixPath
    profile: str
    expected: str
    actual: str
    owner: str


@dataclass(frozen=True)
class FrontmatterContract:
    mode: Literal["required", "forbidden"]
    required: tuple[str, ...]
    allowed: tuple[str, ...]
    order: tuple[str, ...]


@dataclass(frozen=True)
class HeadingContract:
    required: tuple[str, ...]
    allowed: tuple[str, ...]
    substantive_body: bool = False
    ordered: bool = False


@dataclass(frozen=True)
class IdentifierColumn:
    column: str
    kind: Literal["requirement", "criterion", "work-item"]


@dataclass(frozen=True)
class TaskExecution:
    single_status_marker: Literal["frontmatter"]
    result_states: Mapping[str, tuple[str, ...]]
    summary_rule: Literal["task-items-v2"]
    criterion_acceptance_section: str
    acceptance_states: tuple[str, ...] = ()
    evidence_section: str | None = None
    evidence_columns: tuple[str, ...] = ()
    evidence_result_states: tuple[str, ...] = ()
    criterion_acceptance_columns: tuple[str, ...] = ()


def direct_parent(
    path: PurePosixPath, profile_id: str
) -> tuple[PurePosixPath, str] | None:
    if path.parts[:2] != ("docs", "03.specs") or profile_id not in {
        "sdlc/plan",
        "sdlc/task",
    }:
        return None
    package = path.parent if profile_id == "sdlc/plan" else path.parent.parent
    spec_id = f"SPEC-{package.name[:4]}"
    return (
        (package / "spec.md", spec_id)
        if profile_id == "sdlc/plan"
        else (package / "plan.md", f"{spec_id}-PLAN-0001")
    )


def task_evidence_issues(
    rows: Sequence[Mapping[str, str]], binding: TaskExecution
) -> tuple[tuple[str, str], ...]:
    issues: list[tuple[str, str]] = []
    seen: set[str] = set()
    for number, row in enumerate(rows, 1):
        identifier = row["Evidence"].strip()
        if (
            re.fullmatch(r"EVD-(?:[A-Z0-9]+-)*[0-9]{3}", identifier) is None
            or identifier in seen
        ):
            issues.append(
                (
                    "TASK-EVIDENCE-ID",
                    f"row {number}: invalid or duplicate {identifier!r}",
                )
            )
        seen.add(identifier)
        if task_criterion_ids(row["Criteria"]) is None:
            issues.append(
                ("TASK-EVIDENCE-CRITERION", f"row {number}: invalid criterion")
            )
        if re.fullmatch(r"WORK-[0-9]{3}", row["Work Unit"].strip()) is None:
            issues.append(("TASK-EVIDENCE-WORK", f"row {number}: invalid work unit"))
        if row.get("Required", "").strip() not in {"yes", "no"}:
            issues.append(("TASK-EVIDENCE-REQUIRED", f"row {number}: expected yes/no"))
        if _task_evidence_ids(row.get("Resolves", "")) is None:
            issues.append(
                ("TASK-EVIDENCE-RESOLUTION", f"row {number}: invalid Resolves IDs")
            )
        result = row["Result"].strip()
        if result not in binding.evidence_result_states:
            issues.append(
                ("TASK-EVIDENCE-RESULT", f"row {number}: invalid result {result!r}")
            )
        placeholder_keys = (
            ("Check", "Input", "Location") if result in {"PASS", "FAIL"} else ()
        )
        if any(not cell.strip() for cell in row.values()) or any(
            _TASK_EVIDENCE_PLACEHOLDER.fullmatch(row[key].strip())
            for key in placeholder_keys
        ):
            issues.append(
                (
                    "TASK-EVIDENCE-LOCATION",
                    f"row {number}: concrete {'/'.join(placeholder_keys) or 'cell'} required",
                )
            )
    return tuple(issues)


_TASK_EVIDENCE_ID = re.compile(r"EVD-(?:[A-Z0-9]+-)*[0-9]{3}")


def _task_evidence_ids(cell: str) -> tuple[str, ...] | None:
    value = cell.strip()
    if value == "none":
        return ()
    identifiers = tuple(value.split(", "))
    if not identifiers or any(
        _TASK_EVIDENCE_ID.fullmatch(item) is None for item in identifiers
    ):
        return None
    return identifiers if len(identifiers) == len(set(identifiers)) else None


def task_contract_issues(
    work_rows: Sequence[Mapping[str, str]],
    evidence_rows: Sequence[Mapping[str, str]],
    acceptance_rows: Sequence[Mapping[str, str]],
    status: str,
    binding: TaskExecution,
) -> tuple[tuple[str, str], ...]:
    """Validate one modern Task's execution, check graph, and sole AC decisions."""

    issues = list(task_execution_issues(work_rows, status, binding))
    issues.extend(task_evidence_issues(evidence_rows, binding))

    work_by_id = {row["ID"].strip().strip("`"): row for row in work_rows}
    required_criteria = {
        criterion
        for row in work_rows
        for criterion in (task_criterion_ids(row["Upstream criterion"]) or ())
    }
    checks: dict[str, tuple[int, Mapping[str, str]]] = {}
    closed: set[str] = set()
    for index, check in enumerate(evidence_rows):
        identifier = check["Evidence"].strip()
        work = work_by_id.get(check["Work Unit"].strip())
        criteria = task_criterion_ids(check["Criteria"])
        work_criteria = (
            task_criterion_ids(work["Upstream criterion"]) if work is not None else None
        )
        if (
            work is None
            or criteria is None
            or work_criteria is None
            or not set(criteria) <= set(work_criteria)
        ):
            issues.append(
                (
                    "TASK-EVIDENCE-WORK",
                    f"row {index + 1}: check does not map to its work criteria",
                )
            )
        resolves = _task_evidence_ids(check.get("Resolves", ""))
        if resolves is None:
            continue
        if resolves and check["Result"].strip() != "PASS":
            issues.append(
                ("TASK-EVIDENCE-RESOLUTION", f"row {index + 1}: only PASS can resolve")
            )
        for target_id in resolves:
            previous = checks.get(target_id)
            if (
                previous is None
                or check["Result"].strip() != "PASS"
                or check["Required"].strip() != "yes"
                or previous[1]["Required"].strip() != "yes"
                or previous[1]["Result"].strip() not in {"FAIL", "DEFER", "NOT_RUN"}
                or any(
                    check[key].strip() != previous[1][key].strip()
                    for key in ("Criteria", "Work Unit", "Check")
                )
            ):
                issues.append(
                    (
                        "TASK-EVIDENCE-RESOLUTION",
                        f"row {index + 1}: invalid predecessor {target_id}",
                    )
                )
            else:
                closed.add(target_id)
        checks[identifier] = (index, check)
    if not evidence_rows:
        issues.append(("TASK-EVIDENCE-COLUMNS", "Task Evidence requires a check row"))

    decisions: set[str] = set()
    accepted: set[str] = set()
    for number, row in enumerate(acceptance_rows, 1):
        criterion_ids = task_criterion_ids(row["Criterion"])
        if criterion_ids is None or len(criterion_ids) != 1:
            issues.append(
                (
                    "TASK-ACCEPTANCE-CRITERION",
                    f"row {number}: one linked criterion required",
                )
            )
            continue
        criterion = criterion_ids[0]
        if criterion in decisions:
            issues.append(
                ("TASK-ACCEPTANCE-DUPLICATE", f"row {number}: duplicate {criterion}")
            )
        decisions.add(criterion)
        if criterion not in required_criteria:
            issues.append(
                ("TASK-ACCEPTANCE-CRITERION", f"row {number}: unassigned {criterion}")
            )
        verdict = row["Acceptance"].strip()
        if verdict not in binding.acceptance_states:
            issues.append(("TASK-ACCEPTANCE-STATE", f"row {number}: invalid {verdict}"))
        if any(
            not row[key].strip()
            or _TASK_EVIDENCE_PLACEHOLDER.fullmatch(row[key].strip())
            for key in ("Disposition", "Current owner")
        ):
            issues.append(
                (
                    "TASK-ACCEPTANCE-DISPOSITION",
                    f"row {number}: concrete disposition and owner required",
                )
            )
        cited = _task_evidence_ids(row["Evidence"])
        if cited is None or any(item not in checks for item in cited):
            issues.append(
                ("TASK-ACCEPTANCE-EVIDENCE", f"row {number}: unknown evidence ID")
            )
            continue
        if any(
            criterion not in (task_criterion_ids(checks[item][1]["Criteria"]) or ())
            for item in cited
        ):
            issues.append(
                ("TASK-ACCEPTANCE-EVIDENCE", f"row {number}: unrelated cited evidence")
            )
        if verdict == "accepted":
            accepted.add(criterion)
            if not cited or not any(
                checks[item][1]["Result"].strip() == "PASS"
                and checks[item][1]["Required"].strip() == "yes"
                and criterion in (task_criterion_ids(checks[item][1]["Criteria"]) or ())
                for item in cited
            ):
                issues.append(
                    (
                        "TASK-ACCEPTANCE-EVIDENCE",
                        f"row {number}: accepted criterion needs relevant PASS",
                    )
                )
        elif verdict == "not-required" and status != "cancelled":
            issues.append(
                (
                    "TASK-ACCEPTANCE-SCOPE",
                    f"row {number}: linked Spec criterion cannot be waived by Task",
                )
            )
    if decisions != required_criteria:
        issues.append(
            (
                "TASK-ACCEPTANCE-COVERAGE",
                "one decision per assigned Spec criterion required",
            )
        )
    if accepted or status == "completed":
        unresolved = [
            identifier
            for identifier, (_, check) in checks.items()
            if check["Required"].strip() == "yes"
            and check["Result"].strip() in {"FAIL", "DEFER", "NOT_RUN"}
            and identifier not in closed
            and (
                status == "completed"
                or any(
                    criterion in accepted
                    for criterion in (task_criterion_ids(check["Criteria"]) or ())
                )
            )
        ]
        if unresolved:
            issues.append(("TASK-EVIDENCE-UNRESOLVED", ", ".join(unresolved)))
    if status == "completed" and accepted != required_criteria:
        issues.append(
            (
                "TASK-ACCEPTANCE-COMPLETED",
                "completed Task requires its sole accepted criteria",
            )
        )
    return tuple(issues)


_TASK_CRITERION_LINK = re.compile(r"\[(VAL-[A-Z0-9-]+-[0-9]{3})\]\(([^()\s]+)\)")
_TASK_EVIDENCE_PLACEHOLDER = re.compile(
    r"(?i)^(?:tbd|todo|n/?a|pending|waiting|not recorded|not executed|"
    r"execution pending|named repository evidence|[-—])$"
)


def task_criterion_ids(cell: str) -> tuple[str, ...] | None:
    """Read one Task cell's individually linked Spec criteria; empty means N/A."""

    value = cell.strip()
    if re.fullmatch(r"N/A — \S(?:.*\S)?", value):
        return ()
    parts = value.split(", ")
    matches = [_TASK_CRITERION_LINK.fullmatch(part) for part in parts]
    if not matches or any(match is None for match in matches):
        return None
    identifiers = tuple(match.group(1) for match in matches if match is not None)
    return identifiers if len(identifiers) == len(set(identifiers)) else None


def derive_task_summary(states: Sequence[str], binding: TaskExecution) -> str:
    """Derive a validated Task row summary without changing the input states."""

    if not states or any(state not in binding.result_states for state in states):
        raise ValueError("Task summary requires nonempty registry-valid states")
    if len(states) == 1:
        expected = states[0]
    elif "blocked" in states:
        expected = "blocked"
    elif "in-progress" in states or (
        "completed" in states and any(state in states for state in ("draft", "ready"))
    ):
        expected = "in-progress"
    elif "ready" in states:
        expected = "ready"
    elif "draft" in states:
        expected = "draft"
    elif all(state == "completed" for state in states):
        expected = "completed"
    else:
        expected = "cancelled"
    return expected


def _task_row_states(text: str, contract: "BodyContract") -> list[str] | None:
    """Status cells of the bound Task table in its current column form only."""

    lines = text.split("\n")
    try:
        start = lines.index(f"## {contract.section}")
        start = lines.index(f"### {contract.table_heading}", start)
    except ValueError:
        return None
    table: list[list[str]] = []
    for line in lines[start + 1 :]:
        if line.startswith("#"):
            break
        if line.startswith("|"):
            cells = re.split(r"(?<!\\)\|", line.strip())[1:-1]
            table.append([cell.strip() for cell in cells])
        elif table:
            break
    # ponytail: plain pipe split; the full validators still check the table shape.
    if len(table) < 3 or tuple(table[0]) != contract.required_columns:
        return None
    column = table[0].index("Status")
    return [row[column] for row in table[2:] if len(row) == len(table[0])]


def task_status(
    metadata: Mapping[str, Any], text: str, profile: "DocumentProfile"
) -> str:
    """Frontmatter status, else the summary a multi-row Task's rows derive, else ''."""

    if "status" in metadata:
        value = metadata["status"]
        return value if isinstance(value, str) else ""
    contract = profile.body_contract
    binding = contract.task_execution if contract else None
    states = _task_row_states(text, contract) if binding else None
    if binding is None or not states or len(states) < 2:
        return ""
    try:
        return derive_task_summary(states, binding)
    except ValueError:
        return ""


def task_execution_issues(
    rows: Sequence[Mapping[str, str]],
    status: str,
    binding: TaskExecution,
    *,
    template: bool = False,
) -> tuple[tuple[str, str], ...]:
    """Check parsed Task rows without parsing Markdown or changing their status."""

    issues: list[tuple[str, str]] = []
    seen_ids: set[str] = set()
    states: list[str] = []
    for number, row in enumerate(rows, start=1):
        work_id = row["ID"].strip().strip("`")
        if work_id in seen_ids:
            issues.append(("TASK-EXECUTION-ID", f"row {number}: duplicate {work_id}"))
        seen_ids.add(work_id)
        criterion_ids = task_criterion_ids(row["Upstream criterion"])
        if criterion_ids is None:
            issues.append(
                ("TASK-EXECUTION-CRITERION", f"row {number}: invalid linked criterion")
            )
        row_status = row["Status"].strip()
        result = row["Result"].strip()
        evidence = row["Evidence"].strip()
        if len(rows) == 1 and row_status != binding.single_status_marker:
            issues.append(
                ("TASK-EXECUTION-STATUS", f"row {number}: expected frontmatter marker")
            )
        effective_status = status if len(rows) == 1 else row_status
        states.append(effective_status)
        allowed = binding.result_states.get(effective_status)
        if allowed is None:
            issues.append(
                ("TASK-EXECUTION-STATUS", f"row {number}: {effective_status!r}")
            )
            continue
        if result not in allowed:
            issues.append(
                ("TASK-EXECUTION-RESULT", f"row {number}: {effective_status}/{result}")
            )
        if criterion_ids and effective_status == "completed" and result != "PASS":
            issues.append(
                (
                    "TASK-EXECUTION-RESULT",
                    f"row {number}: linked completed criterion requires PASS",
                )
            )
        if effective_status == "completed" and (
            not evidence or _TASK_EVIDENCE_PLACEHOLDER.fullmatch(evidence)
        ):
            issues.append(
                (
                    "TASK-EXECUTION-EVIDENCE",
                    f"row {number}: completed evidence placeholder",
                )
            )
        if effective_status == "blocked" and not (
            re.search(r"(?i)\breason:\s*\S", evidence)
            and re.search(r"(?i)\bnext owner:\s*\S", evidence)
        ):
            issues.append(
                (
                    "TASK-EXECUTION-EVIDENCE",
                    f"row {number}: blocked reason and next owner required",
                )
            )
        if effective_status == "cancelled" and not re.search(
            r"(?i)\breason:\s*\S", evidence
        ):
            issues.append(
                (
                    "TASK-EXECUTION-EVIDENCE",
                    f"row {number}: cancellation reason required",
                )
            )
    if (
        template
        or not states
        or any(state not in binding.result_states for state in states)
    ):
        return tuple(issues)
    expected = derive_task_summary(states, binding)
    # Readers pass a derived summary for an omitted multi-row status, so an empty
    # value here means the shared reader could not read the table: fail closed.
    if status != expected:
        issues.append(
            ("TASK-EXECUTION-SUMMARY", f"frontmatter {status!r}, rows {expected!r}")
        )
    return tuple(issues)


@dataclass(frozen=True)
class BodyContract:
    section: str
    table_heading: str
    enforced_statuses: tuple[str, ...]
    required_columns: tuple[str, ...]
    identifier_columns: tuple[IdentifierColumn, ...]
    source_link_column: str | None
    target_link_column: str | None
    allowed_source_profile_ids: tuple[str, ...]
    allowed_target_profile_ids: tuple[str, ...]
    allow_explicit_exclusion: bool
    task_execution: TaskExecution | None = None


@dataclass(frozen=True)
class ConstantConstraint:
    source: Literal["literal", "profile-id"]
    value: str | int | float | bool | None


@dataclass(frozen=True)
class EnumConstraint:
    source: Literal["literal", "status-domain"]
    values: tuple[str | int | float | bool | None, ...]


@dataclass(frozen=True)
class ConditionalConstraint:
    key: str
    operator: Literal["equals", "not-equals"]
    value: str | int | float | bool | None
    effect: Literal["required", "forbidden"]


@dataclass(frozen=True)
class LifecycleDomain:
    family: str
    profile_ids: tuple[str, ...]
    states: tuple[tuple[str, Literal["mutable", "current", "terminal"]], ...]
    transitions: frozenset[tuple[str, str]]
    initial_states: tuple[str, ...] | None = None

    def validation_class(
        self, state: str
    ) -> Literal["mutable", "current", "terminal"] | None:
        return dict(self.states).get(state)

    def allows(self, from_state: str, to_state: str) -> bool:
        return (from_state, to_state) in self.transitions

    @property
    def requires_reciprocal_supersession(self) -> bool:
        return any(target == "superseded" for _, target in self.transitions)


@dataclass(frozen=True)
class ReadmeNavigationProfile:
    """The navigation section a README profile owns and whether it is complete."""

    section: str
    complete: bool


@dataclass(frozen=True)
class ReadmeNavigation:
    """SPEC-0091: what a README may list, owned by the registry alone."""

    placeholders: frozenset[str]
    forbidden_index_columns: frozenset[str]
    max_deep_links_per_child: int
    profiles: Mapping[str, ReadmeNavigationProfile]
    pending_paths: frozenset[PurePosixPath]
    # READMEs the contract never checks: the Stage 98 index carries the machine
    # tables that sealed and frozen proofs read.
    exempt_paths: frozenset[PurePosixPath] = frozenset()
    index_columns: tuple[str, ...] = ()
    optional_index_columns: tuple[str, ...] = ()


@dataclass(frozen=True)
class DocumentLanguage:
    """SPEC-0093: which language each document is written in."""

    english_only_roots: tuple[str, ...]
    korean_allowed_markdown_roots: tuple[str, ...]
    english_only_suffixes: frozenset[str]
    korean_first_profiles: frozenset[str]
    english_sections: frozenset[str]
    min_latin_words: int
    pending_paths: frozenset[PurePosixPath]

    def english_only(self, path: PurePosixPath) -> bool:
        """A non-README file under an English-only root; READMEs follow their profile."""

        return (
            path.as_posix().startswith(self.english_only_roots)
            and path.suffix in self.english_only_suffixes
            and path.name != "README.md"
            and not self.korean_allowed_markdown(path)
        )

    def korean_allowed_markdown(self, path: PurePosixPath) -> bool:
        return (
            path.suffix == ".md"
            and path.name != "README.md"
            and path.as_posix().startswith(self.korean_allowed_markdown_roots)
        )


# The twenty-four form identifiers a form may carry: sixteen COMMON-DOC-FORM-1
# roles and eight Stage 99 local roles (W03-D09, W03-D26).
FormId = Literal[
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
]

# Nine Stage 99 local roles follow (W03-D09, W03-D20); six have a form, and
# reference-report, governance-document and provider-native have none yet.
DocumentRole = Literal[
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
    "reference-report",
    "governance-document",
    "knowledge-map",
    "vocabulary",
    "prompt",
    "evaluation-task",
    "evaluation-score",
    "evaluation-results",
    "provider-native",
]


@dataclass(frozen=True)
class TableColumn:
    """One column of a template table; `key` is the exact header text."""

    key: str
    meaning: str
    data_type: str
    required: bool


@dataclass(frozen=True)
class TableContract:
    """A table a template carries inside one section of its role's form."""

    name: str
    section: str
    columns: tuple[TableColumn, ...]
    minimum_rows: int
    row_identity: str


@dataclass(frozen=True)
class FormSection:
    """One section of a form in the COMMON-DOC-FORM-1 list (which also holds
    Stage 99 local forms); link_only is the one local field."""

    section_id: str
    title: str
    level: Literal[2, 3]
    parent_id: str | None
    order: int
    requiredness: Literal["required", "conditional", "optional"]
    condition: str
    empty_policy: Literal["explain_none_or_not_applicable", "omit_when_condition_false"]
    link_only: bool
    children: tuple["FormSection", ...]


@dataclass(frozen=True)
class FormExtension:
    """A registered departure from a form: a local H3 or a retained H2 list."""

    extension_id: str
    kind: Literal["local_h3", "retained_form"]
    condition: str
    owner: str
    verification: str
    review: str
    removal: str
    parent_id: str | None = None
    title: str | None = None
    statuses: tuple[str, ...] = ()
    retained: HeadingContract | None = None


@dataclass(frozen=True)
class CommonForm:
    """The section tree every profile bound to one document role shares."""

    form_id: FormId
    title: str
    h1: str
    language_rule: str
    extension_policy: str
    sections: tuple[FormSection, ...]
    extensions: tuple[FormExtension, ...]

    def retained_headings(self, status: str) -> HeadingContract | None:
        """The retained H2 lists that replace the tree for this status, if any."""

        for extension in self.extensions:
            if extension.kind == "retained_form" and status in extension.statuses:
                return extension.retained
        return None


@dataclass(frozen=True)
class DocumentProfile:
    profile_id: str
    profile_class: Literal[
        "sdlc",
        "operation",
        "reference",
        "governance",
        "evaluation",
        "readme",
        "exception",
    ]
    path_pattern: str
    routes: tuple[Route, ...]
    artifact_id_pattern: str | None
    frontmatter: FrontmatterContract
    constants: tuple[tuple[str, str | int | float | bool | None], ...]
    status_domain: tuple[str, ...]
    headings: HeadingContract
    template: PurePosixPath | None
    mode: Literal[
        "authored",
        "router",
        "template",
        "native",
        "non-target",
    ]
    source_profile_ids: tuple[str, ...]
    placeholder_policy: Literal["forbidden", "template-only"]
    body_contract: BodyContract | None
    lifecycle_domain: LifecycleDomain | None
    document_role: DocumentRole | None = None
    form: CommonForm | None = None
    template_definition: Mapping[str, Any] | None = dataclass_field(
        default=None, hash=False
    )
    tables: tuple[TableContract, ...] = ()


@dataclass(frozen=True)
class SharedExtension:
    """A local extension of the shared contract; unrecorded facts read unverified."""

    name: str
    condition: str
    owner: str
    verification: str
    review: str
    removal: str


@dataclass(frozen=True)
class SharedContract:
    """Reviewed input identity, never an authenticated approval decision."""

    contract_id: str
    version: str
    stage: Literal["candidate", "approved", "adopted"]
    owner: str
    source: str
    source_revision: str | None
    content_digest: str
    approval_ref: str | None
    local_adapter: str
    extensions: tuple[SharedExtension, ...]
    approved_by: str | None = None
    approved_at: str | None = None
    effective_from: str | None = None
    scope: str | None = None
    migration: str | None = None
    rollback: str | None = None
    consumer_version: str | None = None


def extension_name(extension: Mapping[str, Any] | SharedExtension) -> str:
    """The one reader of a shared-contract extension's name."""

    if isinstance(extension, Mapping):
        return extension["name"]
    return extension.name


def local_extension_names(
    shared: Mapping[str, Any] | SharedContract | None,
) -> frozenset[str]:
    """Names of the local extensions in force; none at an unrecognized stage."""

    if shared is None:
        return frozenset()
    if isinstance(shared, Mapping):
        stage, extensions = shared.get("stage"), shared.get("extensions", ())
    else:
        stage, extensions = shared.stage, shared.extensions
    if stage not in SHARED_STAGES:
        return frozenset()
    return frozenset(extension_name(item) for item in extensions)


@dataclass(frozen=True)
class KeyTestReference:
    """A test module path and a test name."""

    module: str
    test: str


@dataclass(frozen=True)
class FrontmatterKey:
    """SPEC-0181: the one description of a frontmatter key."""

    key: str
    purpose: str
    data_type: str
    condition: str
    authoring_owner: Literal["author", "tool", "derived"]
    derived_from: str
    duplicate_source: str
    consumer_paths: tuple[str, ...]
    lifecycle: str
    migration: str
    positive_test: KeyTestReference
    negative_test: KeyTestReference


@dataclass(frozen=True)
class FrontmatterLoader:
    path: str
    loader: str
    scope: str
    duplicate_keys: Literal["refused", "last-wins"]
    timestamps: Literal["resolved", "kept-as-text"]


@dataclass(frozen=True)
class FrontmatterDialect:
    """SPEC-0181: the YAML and JSON Schema dialect of frontmatter."""

    current_yaml: str
    current_library: str
    loaders: tuple[FrontmatterLoader, ...]
    target_yaml: str
    target_decision: str
    target_asserted_by_check: bool
    schema_dialect: str
    schema_format: str
    date_rule: str
    date_checked_by: str


@dataclass(frozen=True)
class Registry:
    schema_version: int
    profiles: tuple[DocumentProfile, ...]
    lifecycle_domains: tuple[LifecycleDomain, ...]
    readme_navigation: ReadmeNavigation | None = None
    document_language: DocumentLanguage | None = None
    shared_contract: SharedContract | None = None
    common_forms: tuple[CommonForm, ...] = ()
    # A comparison-base registry from before SPEC-0181 has neither section.
    frontmatter_keys: tuple[FrontmatterKey, ...] = ()
    frontmatter_dialect: FrontmatterDialect | None = None


@dataclass(frozen=True)
class TargetInventory:
    baseline_paths: tuple[PurePosixPath, ...]
    current_paths: tuple[PurePosixPath, ...]
    new_paths: tuple[PurePosixPath, ...]
    baseline_symlink_paths: tuple[PurePosixPath, ...]
    current_symlink_paths: tuple[PurePosixPath, ...]


@dataclass(frozen=True)
class _GitEntry:
    mode: str
    path: PurePosixPath
    stage: int | None = None


class DocumentContractError(ValueError):
    """A deterministic registry or classification failure."""

    def __init__(self, diagnostics: Sequence[Diagnostic]):
        self.diagnostics = tuple(diagnostics)
        super().__init__("; ".join(item.rule_id for item in self.diagnostics))


class _UniqueKeySafeLoader(yaml.SafeLoader):
    """YAML SafeLoader variant that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: _UniqueKeySafeLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeySafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _diagnostic(
    rule_id: str,
    *,
    path: PurePosixPath = REGISTRY_PATH,
    profile: str = "",
    expected: str,
    actual: str,
) -> Diagnostic:
    return Diagnostic(
        rule_id=rule_id,
        path=path,
        profile=profile,
        expected=expected,
        actual=actual,
        owner="document-contract-registry",
    )


def _fail(rule_id: str, *, expected: str, actual: str) -> NoReturn:
    raise DocumentContractError(
        (_diagnostic(rule_id, expected=expected, actual=actual),)
    )


def load_json_file(
    path: Path, *, diagnostic_path: PurePosixPath = REGISTRY_PATH
) -> Any:
    """Load JSON once with duplicate mapping keys rejected at every depth."""
    try:
        return load_bounded_json(path, max_bytes=REGISTRY_MAX_BYTES)
    except AuthorityError as exc:
        raise DocumentContractError(
            (
                _diagnostic(
                    "REGISTRY_SCHEMA",
                    path=diagnostic_path,
                    expected="valid JSON with unique mapping keys at every depth",
                    actual="JSON decoding or duplicate-key failure",
                ),
            )
        ) from exc


def _normalize_relative_path(value: str | PurePosixPath) -> PurePosixPath:
    raw = str(value)
    if not raw or raw == ".":
        raise ValueError("path must not be empty")
    if raw.startswith("./"):
        raise ValueError("path must not start with './'")
    if "\\" in raw:
        raise ValueError("path must use POSIX separators")
    if any(ord(character) < 32 or ord(character) == 127 for character in raw):
        raise ValueError("path must not contain control characters")
    path = PurePosixPath(raw)
    if path.is_absolute():
        raise ValueError("path must be repository-relative")
    if ".." in path.parts:
        raise ValueError("path must not contain '..'")
    return path


_DOCUMENT_SCOPE_READERS = frozenset(
    {
        "scripts/document_authority.py",
        "scripts/document_contracts.py",
        "scripts/document_language.py",
        "scripts/document_lifecycle.py",
        "scripts/validation/document_content.py",
        "scripts/validate-document-contract-registry.py",
        "scripts/validate-document-lifecycle.py",
        "scripts/validate-links-and-owners.py",
        "scripts/validate-markdown-profiles.py",
    }
)


def validated_changed_paths(
    changed_paths: Sequence[str | PurePosixPath],
) -> tuple[PurePosixPath, ...]:
    """Preserve each raw old/new Git path while rejecting malformed CLI input."""
    if not changed_paths:
        raise ValueError("change scope requires at least one changed path")
    normalized = tuple(_normalize_relative_path(raw) for raw in changed_paths)
    for raw, path in zip(changed_paths, normalized, strict=True):
        if str(raw) != path.as_posix():
            raise ValueError(f"changed path is not normalized: {raw}")
    return normalized


def scoped_document_content_paths(
    registry: Registry,
    changed_paths: Sequence[str | PurePosixPath],
    current_paths: Sequence[PurePosixPath],
) -> frozenset[PurePosixPath] | None:
    """Select body checks; None means a contract change requires the full corpus.

    Metadata and relationship checks remain global in their respective readers.
    Raw deleted paths are retained so their README matrix owners are checked.
    """

    normalized = validated_changed_paths(changed_paths)
    current = frozenset(current_paths)
    selected: set[PurePosixPath] = set()
    for path in normalized:
        name = path.as_posix()
        if (
            name.startswith("docs/99.templates/")
            or name in _DOCUMENT_SCOPE_READERS
            or name.startswith("scripts/validation/registry.")
            or name
            in {
                "scripts/qa.py",
                "scripts/run-validation-lane.py",
                "scripts/validate-affected-surfaces.py",
            }
        ):
            return None
        if path in current:
            # A changed Markdown document is checked only when it is in the
            # reader's current, already validated inventory.
            classify_path(registry, path)
            selected.add(path)
        owner: str | None = None
        parts = path.parts
        if len(parts) >= 2 and parts[0] == "examples":
            owner = "examples/README.md"
        elif (
            len(parts) == 3
            and parts[:2] == (".github", "workflows")
            and path.suffix == ".yml"
        ):
            owner = ".github/repository-surface.md"
        elif len(parts) >= 3 and parts[:2] in {
            ("gitops", "platform"),
            ("gitops", "workloads"),
        }:
            owner = f"{parts[0]}/{parts[1]}/README.md"
        elif len(parts) >= 3 and parts[:3] in {
            ("gitops", "clusters", "local"),
            ("gitops", "apps", "root"),
        }:
            owner = "gitops/README.md"
        elif (
            len(parts) == 4
            and parts[:2] == ("docs", "05.operations")
            and parts[2] in {"guides", "policies", "runbooks"}
            and path.suffix == ".md"
        ):
            owner = f"docs/05.operations/{parts[2]}/README.md"
        elif len(parts) >= 4 and parts[:3] == (
            "docs",
            "05.operations",
            "incidents",
        ):
            owner = "docs/05.operations/incidents/README.md"
        elif len(parts) >= 2 and parts[0] == "infrastructure":
            owner = "infrastructure/README.md"
            if len(parts) == 3 and parts[1] == "verify" and path.suffix == ".sh":
                selected.add(PurePosixPath("infrastructure/verify/README.md"))
        if owner is not None:
            selected.add(PurePosixPath(owner))
    if missing := selected - current:
        raise ValueError(f"document matrix owner missing: {sorted(missing)[0]}")
    return frozenset(selected)


def _decode_git_path(raw: bytes) -> PurePosixPath:
    try:
        return _normalize_relative_path(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise ValueError("git returned an invalid repository-relative path") from exc


def _validate_git_object_id(raw_object: bytes, command: str) -> None:
    if len(raw_object) not in {40, 64}:
        raise ValueError(f"{command} object id must be exactly 40 or 64 characters")
    if re.fullmatch(rb"[0-9a-f]+", raw_object) is None:
        raise ValueError(f"{command} object id must be lowercase hexadecimal")


def _parse_ls_files_stage_z(raw: bytes) -> tuple[_GitEntry, ...]:
    """Parse ``git ls-files --stage -z`` output, retaining mode and stage."""

    entries: list[_GitEntry] = []
    records = raw.split(b"\0")
    if records[-1] != b"":
        raise ValueError("git ls-files output is not NUL terminated")
    for record in records[:-1]:
        try:
            header, raw_path = record.split(b"\t", 1)
            raw_mode, raw_object, raw_stage = header.split(b" ", 2)
        except ValueError as exc:
            raise ValueError("malformed git ls-files record") from exc
        if raw_mode not in _LS_FILES_MODES:
            raise ValueError("noncanonical git ls-files mode")
        _validate_git_object_id(raw_object, "git ls-files")
        if raw_stage not in {b"0", b"1", b"2", b"3"}:
            raise ValueError("invalid git ls-files stage")
        entries.append(
            _GitEntry(
                mode=raw_mode.decode("ascii"),
                path=_decode_git_path(raw_path),
                stage=int(raw_stage),
            )
        )
    return tuple(entries)


def _run_git(
    root: Path,
    arguments: Sequence[str],
    *,
    timeout_seconds: float = GIT_TIMEOUT_SECONDS,
    max_stdout_bytes: int = DOCUMENT_TEXT_MAX_BYTES,
) -> bytes:
    completed = run_bounded_process(
        ["git", *arguments],
        cwd=root,
        check=True,
        timeout_seconds=timeout_seconds,
        max_stdout_bytes=max_stdout_bytes,
    )
    return completed.stdout


def _within_target_scope(path: PurePosixPath) -> bool:
    if path.as_posix() == "RTK.md":
        return False
    if not path.parts:
        return False
    if path.parts[0] == ".worktrees":
        return False
    if path.parts[:2] == ("docs", "98.archive"):
        # Archive content is unvalidated history, outside the document scope.
        return False
    return path.as_posix() in ROOT_FILES or path.parts[0] in TARGET_ROOTS


def _is_target_markdown(path: PurePosixPath) -> bool:
    return path.suffix == ".md" and _within_target_scope(path)


def _sorted_paths(paths: set[PurePosixPath]) -> tuple[PurePosixPath, ...]:
    return tuple(sorted(paths, key=lambda item: item.as_posix()))


def _is_ignored(
    root: Path,
    path: PurePosixPath,
    *,
    timeout_seconds: float = GIT_TIMEOUT_SECONDS,
) -> bool:
    completed = run_bounded_process(
        ["git", "check-ignore", "--quiet", "--", path.as_posix()],
        cwd=root,
        check=False,
        timeout_seconds=timeout_seconds,
        max_stdout_bytes=0,
    )
    if completed.returncode == 0:
        return True
    if completed.returncode == 1:
        return False
    raise subprocess.CalledProcessError(
        completed.returncode, completed.args, stderr=completed.stderr
    )


def _lstat_named_path(root: Path, path: PurePosixPath) -> int:
    current = root
    mode: int | None = None
    for part in path.parts:
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError as exc:
            raise ValueError(
                f"included path does not exist: {path.as_posix()}"
            ) from exc
        if stat.S_ISLNK(mode):
            raise ValueError(
                f"included path crosses or names a symlink: {path.as_posix()}"
            )
    if mode is None:
        raise ValueError("included path must not be empty")
    return mode


def read_repository_text(root: Path, path: PurePosixPath) -> str:
    """Read one normalized regular file without following path symlinks."""

    normalized = _normalize_relative_path(path)
    mode = _lstat_named_path(root.absolute(), normalized)
    if not stat.S_ISREG(mode):
        raise ValueError(f"repository path is not a regular file: {normalized}")
    try:
        return read_bounded_utf8(
            root.absolute() / normalized,
            max_bytes=DOCUMENT_TEXT_MAX_BYTES,
        )
    except AuthorityError as exc:
        raise ValueError(str(exc)) from exc


def verify_opaque_evaluation_output(root: Path, path: PurePosixPath) -> None:
    """Check raw data's regular-file, symlink and size boundary without decoding it."""

    normalized = _normalize_relative_path(path)
    try:
        read_bounded_bytes(
            root.absolute() / normalized, max_bytes=DOCUMENT_TEXT_MAX_BYTES
        )
    except BoundedInputError as exc:
        raise ValueError(
            f"unsafe or oversized raw evaluation output: {normalized}"
        ) from exc


def is_ignored_repository_path(root: Path, path: PurePosixPath) -> bool:
    """Return Git's ignore decision for one normalized repository path."""

    return _is_ignored(root.absolute(), _normalize_relative_path(path))


def diagnostic_sort_key(diagnostic: Diagnostic) -> tuple[str, str, str, str]:
    """Return the stable cross-validator diagnostic ordering contract."""

    return (
        diagnostic.path.as_posix(),
        diagnostic.rule_id,
        diagnostic.expected,
        diagnostic.actual,
    )


def enumerate_target_markdown(
    root: Path,
    *,
    include_paths: tuple[PurePosixPath, ...] = (),
) -> TargetInventory:
    root = root.absolute()
    current_entries = _parse_ls_files_stage_z(
        _run_git(root, ("ls-files", "--stage", "-z"))
    )

    current_paths: set[PurePosixPath] = set()
    for entry in current_entries:
        if not entry.mode.startswith("100") or not _is_target_markdown(entry.path):
            continue
        try:
            mode = _lstat_named_path(root, entry.path)
        except ValueError:
            continue
        if stat.S_ISREG(mode):
            current_paths.add(entry.path)
    current_symlinks = {
        entry.path
        for entry in current_entries
        if entry.mode == "120000" and _within_target_scope(entry.path)
    }
    current_paths.difference_update(current_symlinks)

    for requested_path in include_paths:
        try:
            path = _normalize_relative_path(requested_path)
        except ValueError as exc:
            raise ValueError(f"invalid included path: {requested_path}") from exc
        if _is_ignored(root, path):
            raise ValueError(f"included path is ignored: {path.as_posix()}")
        mode = _lstat_named_path(root, path)
        if not stat.S_ISREG(mode):
            raise ValueError(f"included path is not a regular file: {path.as_posix()}")
        if path in current_symlinks:
            raise ValueError(
                f"included path is indexed as a symlink: {path.as_posix()}"
            )
        if not _is_target_markdown(path):
            raise ValueError(
                f"included path is not approved Markdown: {path.as_posix()}"
            )
        current_paths.add(path)

    return TargetInventory(
        baseline_paths=(),
        current_paths=_sorted_paths(current_paths),
        new_paths=_sorted_paths(current_paths),
        baseline_symlink_paths=(),
        current_symlink_paths=_sorted_paths(current_symlinks),
    )


def enumerate_tracked_regular_paths(
    root: Path,
    *,
    pathspecs: Sequence[str],
) -> tuple[PurePosixPath, ...]:
    """Return one closed Git-index inventory for the supplied pathspecs.

    The caller owns the semantic path selection. This helper retains only
    stage-zero regular blobs and fails closed on conflicts, symlinks,
    submodules, or duplicate index entries in the selected surface.
    """

    if not pathspecs or any(
        not isinstance(item, str) or not item for item in pathspecs
    ):
        raise ValueError("tracked regular inventory requires non-empty pathspecs")
    entries = _parse_ls_files_stage_z(
        _run_git(root.absolute(), ("ls-files", "--stage", "-z", "--", *pathspecs))
    )
    grouped: dict[PurePosixPath, list[_GitEntry]] = {}
    for entry in entries:
        grouped.setdefault(entry.path, []).append(entry)
    paths: set[PurePosixPath] = set()
    for path, selected in grouped.items():
        if (
            len(selected) != 1
            or selected[0].stage != 0
            or not selected[0].mode.startswith("100")
        ):
            raise ValueError(
                "tracked native surface is not one stage-zero regular blob: "
                f"{path.as_posix()}"
            )
        paths.add(path)
    return _sorted_paths(paths)


SHARED_EDITION_SURFACES = (".agents/", "docs/99.templates/", ".claude/", ".codex/")


def shared_edition_surface_texts(root: Path) -> dict[PurePosixPath, str]:
    """Read the tracked Markdown rule surfaces that may name the shared edition."""

    paths = enumerate_tracked_regular_paths(
        root,
        pathspecs=tuple(
            f":(glob){prefix}**/*.md" for prefix in SHARED_EDITION_SURFACES
        ),
    )
    return {path: read_repository_text(root, path) for path in paths}


def shared_edition_mismatches(
    contract: SharedContract | None,
    texts: Mapping[PurePosixPath, str],
) -> tuple[Diagnostic, ...]:
    """Report rule-surface edition mentions that differ from the adopted one."""

    if contract is None:
        return ()
    pattern = re.compile(
        re.escape(contract.contract_id)
        + r"`?\s*(?:/\s*)?`?(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]*\d[0-9A-Za-z]*)?)"
    )
    found = []
    for path in sorted(texts):
        posix = path.as_posix()
        if not posix.endswith(".md") or not posix.startswith(SHARED_EDITION_SURFACES):
            continue
        text = texts[path]
        for match in pattern.finditer(text):
            if match.group(1) == contract.version:
                continue
            line = text.count("\n", 0, match.start()) + 1
            found.append(
                _diagnostic(
                    "REGISTRY_SHARED_EDITION_MISMATCH",
                    path=path,
                    expected=f"{contract.contract_id} {contract.version}",
                    actual=f"line {line}: {contract.contract_id} {match.group(1)}",
                )
            )
    return tuple(found)


@lru_cache(maxsize=None)
def _compile_route(value: str) -> re.Pattern[str]:
    return re.compile(value)


def _schema_rule_id(error: Any) -> str:
    nested_errors = [error]
    for nested_error in nested_errors:
        nested_errors.extend(nested_error.context)
    nested_paths = [tuple(item.absolute_path) for item in nested_errors]
    body_contract_error = any(
        "body_contract" in nested_path for nested_path in nested_paths
    ) or (error.validator == "required" and "body_contract" in error.message)
    if body_contract_error:
        if error.validator == "required" and "body_contract" in error.message:
            return "REGISTRY_BODY_REQUIRED"
        if any(item.validator == "additionalProperties" for item in nested_errors):
            return "REGISTRY_BODY_FIELD"
        if any("required_columns" in nested_path for nested_path in nested_paths):
            return "REGISTRY_BODY_COLUMNS"
        if any("identifier_columns" in nested_path for nested_path in nested_paths):
            return "REGISTRY_BODY_IDENTIFIER_COLUMN"
        return "REGISTRY_BODY_SCHEMA"
    return "REGISTRY_SCHEMA"


def _body_contract(raw: Mapping[str, Any] | None) -> BodyContract | None:
    if raw is None:
        return None
    execution = raw.get("task_execution")
    return BodyContract(
        section=raw["section"],
        table_heading=raw["table_heading"],
        enforced_statuses=tuple(raw["enforced_statuses"]),
        required_columns=tuple(raw["required_columns"]),
        identifier_columns=tuple(
            IdentifierColumn(column=item["column"], kind=item["kind"])
            for item in raw["identifier_columns"]
        ),
        source_link_column=raw["source_link_column"],
        target_link_column=raw["target_link_column"],
        allowed_source_profile_ids=tuple(raw["allowed_source_profile_ids"]),
        allowed_target_profile_ids=tuple(raw["allowed_target_profile_ids"]),
        allow_explicit_exclusion=raw["allow_explicit_exclusion"],
        task_execution=(
            None
            if execution is None
            else TaskExecution(
                single_status_marker=execution["single_status_marker"],
                result_states=MappingProxyType(
                    {
                        state: tuple(results)
                        for state, results in execution["result_states"].items()
                    }
                ),
                summary_rule=execution["summary_rule"],
                acceptance_states=tuple(execution.get("acceptance_states", ())),
                evidence_section=execution.get("evidence_section"),
                evidence_columns=tuple(execution.get("evidence_columns", ())),
                evidence_result_states=tuple(
                    execution.get("evidence_result_states", ())
                ),
                criterion_acceptance_section=execution["criterion_acceptance_section"],
                criterion_acceptance_columns=tuple(
                    execution.get("criterion_acceptance_columns", ())
                ),
            )
        ),
    )


def _form_headings(form: CommonForm) -> HeadingContract:
    """The H2 lists a form implies: required titles in order, all titles allowed."""

    return HeadingContract(
        required=tuple(
            item.title for item in form.sections if item.requiredness == "required"
        ),
        allowed=tuple(item.title for item in form.sections),
    )


def _tables_from_definition(
    definition: Mapping[str, Any] | None,
) -> tuple[TableContract, ...]:
    return tuple(
        TableContract(
            name=table["name"],
            section=table["section"],
            columns=tuple(
                TableColumn(
                    key=column["key"],
                    meaning=column["meaning"],
                    data_type=column["data_type"],
                    required=column["required"],
                )
                for column in table["columns"]
            ),
            minimum_rows=table["minimum_rows"],
            row_identity=table["row_identity"],
        )
        for table in (definition or {}).get("tables", ())
    )


def _profile_from_mapping(
    raw: Mapping[str, Any],
    *,
    lifecycle_domain: LifecycleDomain | None,
    form: CommonForm | None = None,
) -> DocumentProfile:
    frontmatter = raw["frontmatter"]
    lifecycle = raw["lifecycle"]
    constants = frontmatter["constants"]
    template = raw["template_source"]
    routes = tuple(
        Route(
            kind=route["kind"],
            value=(
                _normalize_relative_path(route["value"]).as_posix()
                if route["kind"] == "exact"
                else route["value"]
            ),
        )
        for route in _internal_routes(raw["path_pattern"])
    )
    status_domain = (
        tuple(lifecycle["status_domain"])
        if lifecycle is not None
        else ((constants["status"],) if "status" in constants else ())
    )
    return DocumentProfile(
        profile_id=raw["id"],
        profile_class=_typed_profile_class(raw),
        path_pattern=raw["path_pattern"],
        routes=routes,
        artifact_id_pattern=raw["artifact_id_pattern"],
        frontmatter=FrontmatterContract(
            mode=("required" if frontmatter["mode"] == "required" else "forbidden"),
            required=tuple(frontmatter["required"]),
            allowed=tuple(frontmatter["required"] + frontmatter["optional"]),
            order=tuple(frontmatter["order"]),
        ),
        constants=tuple(constants.items()),
        status_domain=status_domain,
        headings=(
            _form_headings(form)
            if form is not None
            else HeadingContract(
                required=tuple(raw["sections"]["required"]),
                allowed=tuple(
                    raw["sections"]["required"] + raw["sections"]["optional"]
                ),
                substantive_body=raw["sections"].get("substantive_body", False),
                ordered=raw["sections"].get("ordered", False),
            )
        ),
        template=_normalize_relative_path(template) if template is not None else None,
        mode=raw["mode"],
        source_profile_ids=tuple(raw["relationships"]["source_profile_ids"]),
        placeholder_policy=raw["placeholder_policy"],
        body_contract=_body_contract(raw["relationships"]["body_contract"]),
        lifecycle_domain=lifecycle_domain,
        document_role=raw.get("document_role"),
        form=form,
        template_definition=raw.get("template_definition"),
        tables=_tables_from_definition(raw.get("template_definition")),
    )


def _registry_section_diagnostics(
    raw_registry: Mapping[str, Any],
    profiles_by_id: Mapping[str, Mapping[str, Any]],
) -> list[Diagnostic]:
    """Validate the README navigation and document language sections."""

    return [
        *_readme_navigation_registry_diagnostics(raw_registry, profiles_by_id),
        *_document_language_registry_diagnostics(raw_registry, profiles_by_id),
    ]


def _terminal_semantic_diagnostics(
    root: Path,
    raw_registry: Mapping[str, Any],
    *,
    template_regular_paths: frozenset[PurePosixPath] | None = None,
) -> tuple[Diagnostic, ...]:
    """Validate relationships not expressible in the terminal JSON Schema."""

    diagnostics: list[Diagnostic] = []
    raw_profiles = raw_registry["profiles"]
    profiles_by_id = {profile["id"]: profile for profile in raw_profiles}
    raw_forms = {
        form["form_id"]: form
        for form in (raw_registry.get("common_forms") or {}).get("forms", ())
    }
    for raw_profile in raw_profiles:
        profile_id = raw_profile["id"]
        for field, rule_id in (
            ("path_pattern", "REGISTRY_ROUTE_REGEX"),
            ("artifact_id_pattern", "REGISTRY_ARTIFACT_ID_PATTERN"),
        ):
            pattern = raw_profile.get(field)
            if pattern is None:
                continue
            try:
                if not (pattern.startswith("^") and pattern.endswith("$")):
                    raise re.error("pattern is not anchored")
                _compile_route(pattern)
            except re.error as exc:
                diagnostics.append(
                    _diagnostic(
                        rule_id,
                        profile=profile_id,
                        expected="an anchored compilable regular expression",
                        actual=str(exc),
                    )
                )
        relationships = raw_profile["relationships"]
        for source_profile_id in relationships["source_profile_ids"]:
            if source_profile_id not in profiles_by_id:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_SOURCE_PROFILE",
                        profile=profile_id,
                        expected="a declared source profile ID",
                        actual=source_profile_id,
                    )
                )

        lifecycle = raw_profile.get("lifecycle")
        if raw_profile["mode"] == "template" and (lifecycle or {}).get("status_domain"):
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_FORM_STATUS_DOMAIN",
                    profile=profile_id,
                    expected="a form declares no status domain of its own",
                    actual=repr(lifecycle["status_domain"]),
                )
            )
        body_contract = relationships["body_contract"]
        if body_contract is not None:
            role_form = raw_forms.get(raw_profile.get("document_role"))
            required_headings = (
                [
                    item["title"]
                    for item in role_form["sections"]
                    if item["requiredness"] == "required"
                ]
                if role_form is not None
                else raw_profile["sections"]["required"]
            )
            if body_contract["section"] not in required_headings:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_BODY_SECTION",
                        profile=profile_id,
                        expected="body section in required sections",
                        actual=body_contract["section"],
                    )
                )
            # A form inherits its source profile's domain, so comparing its
            # enforced statuses against its own declaration compared them
            # against themselves and could not fail. The source owns the
            # vocabulary, and that is what the form may enforce a subset of.
            if raw_profile["mode"] == "template":
                source_ids = relationships["source_profile_ids"]
                source = profiles_by_id.get(source_ids[0]) if source_ids else None
                source_lifecycle = source.get("lifecycle") if source else None
                status_domain = (
                    source_lifecycle["status_domain"] if source_lifecycle else []
                )
            else:
                status_domain = lifecycle["status_domain"] if lifecycle else []
            invalid_statuses = sorted(
                set(body_contract["enforced_statuses"]) - set(status_domain)
            )
            if invalid_statuses:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_BODY_STATUS",
                        profile=profile_id,
                        expected="enforced statuses within the profile status domain",
                        actual=repr(invalid_statuses),
                    )
                )
            required_columns = body_contract["required_columns"]
            identifier_names = [
                item["column"] for item in body_contract["identifier_columns"]
            ]
            if len(identifier_names) != len(set(identifier_names)) or any(
                column not in required_columns for column in identifier_names
            ):
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_BODY_IDENTIFIER_COLUMN",
                        profile=profile_id,
                        expected=(
                            "unique identifier columns selected from required columns"
                        ),
                        actual=repr(identifier_names),
                    )
                )
            for direction in ("source", "target"):
                link_key = f"{direction}_link_column"
                allowed_key = f"allowed_{direction}_profile_ids"
                link_column = body_contract[link_key]
                allowed_ids = body_contract[allowed_key]
                unknown = sorted(
                    value for value in allowed_ids if value not in profiles_by_id
                )
                valid_pair = (link_column is None and not allowed_ids) or (
                    link_column in required_columns and bool(allowed_ids)
                )
                if unknown or not valid_pair:
                    diagnostics.append(
                        _diagnostic(
                            f"REGISTRY_BODY_{direction.upper()}_PROFILE",
                            profile=profile_id,
                            expected=(
                                f"{link_key} selected from required columns with "
                                f"known {allowed_key}, or both unset"
                            ),
                            actual=(
                                f"column={link_column!r} unknown={unknown!r} "
                                f"allowed={allowed_ids!r}"
                            ),
                        )
                    )

        template = raw_profile["template_source"]
        if template is not None:
            try:
                template_path = _normalize_relative_path(template)
                if template_path.as_posix() != template:
                    raise ValueError("path is not canonical")
                regular = (
                    stat.S_ISREG(_lstat_named_path(root, template_path))
                    if template_regular_paths is None
                    else template_path in template_regular_paths
                )
                if not regular:
                    raise ValueError("template is not a regular file")
            except ValueError as exc:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_TEMPLATE",
                        profile=profile_id,
                        expected=(
                            "an existing normalized regular non-symlink file "
                            "under the repository root"
                        ),
                        actual=str(exc),
                    )
                )

    assigned_profiles: set[str] = set()
    domains_by_profile: dict[str, Mapping[str, Any]] = {}
    families: set[str] = set()
    local_extensions = local_extension_names(raw_registry.get("shared_contract"))
    local_task_recording = TASK_FIRST_RECORDING_EXTENSION in local_extensions
    local_spec_direct_approval = SPEC_PLAN_DIRECT_APPROVAL_EXTENSION in local_extensions
    for domain in raw_registry["lifecycle_domains"]:
        family = domain["family"]
        initial_states = domain.get("initial_states")
        inbound = {target for _, target in domain["transitions"]}
        if family == "spec-plan" and (
            (["draft", "approved"] in domain["transitions"])
            != local_spec_direct_approval
        ):
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_LIFECYCLE_DOMAIN",
                    expected=(
                        "spec-plan draft-to-approved edge exactly when the local "
                        "extension is declared at a recognized shared stage"
                    ),
                    actual="spec-plan direct approval extension/edge mismatch",
                )
            )
        observed_task_initial = (
            family == "task"
            and local_task_recording
            and initial_states == list(TASK_INITIAL_STATES)
        )
        if initial_states is not None and (
            not initial_states
            or any(
                state not in domain["states"]
                or domain["states"][state] == "terminal"
                or (state in inbound and not observed_task_initial)
                for state in initial_states
            )
        ):
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_LIFECYCLE_DOMAIN",
                    expected="nonempty nonterminal creation states; zero-indegree except the local Task first-recording extension",
                    actual=f"invalid initial_states for {family}: {initial_states!r}",
                )
            )
        expected_initial_states = (
            list(TASK_INITIAL_STATES)
            if family == "task" and local_task_recording
            else ["draft"]
        )
        if (
            family in {"spec-plan", "task"}
            and initial_states != expected_initial_states
        ):
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_LIFECYCLE_DOMAIN",
                    expected=f"modern {family} initial_states={expected_initial_states!r}",
                    actual=repr(initial_states),
                )
            )
        if family in families:
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_LIFECYCLE_DOMAIN",
                    expected="one lifecycle domain per family",
                    actual=f"duplicate family {family}",
                )
            )
        families.add(family)
        if not domain["profile_ids"]:
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_LIFECYCLE_DOMAIN",
                    expected="at least one lifecycle profile ID per family",
                    actual=f"empty lifecycle domain {family}",
                )
            )
        for profile_id in domain["profile_ids"]:
            if profile_id not in profiles_by_id:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_LIFECYCLE_DOMAIN",
                        profile=profile_id,
                        expected="a declared lifecycle profile ID",
                        actual="unknown profile",
                    )
                )
            elif profile_id in assigned_profiles:
                diagnostics.append(
                    _diagnostic(
                        "REGISTRY_LIFECYCLE_DOMAIN",
                        profile=profile_id,
                        expected="at most one lifecycle domain per profile",
                        actual="duplicate lifecycle domain assignment",
                    )
                )
            assigned_profiles.add(profile_id)
            domains_by_profile[profile_id] = domain

    diagnostics.extend(_registry_section_diagnostics(raw_registry, profiles_by_id))
    diagnostics.extend(_shared_extension_diagnostics(raw_registry))
    diagnostics.extend(
        _form_registry_diagnostics(
            root, raw_registry, profiles_by_id, template_regular_paths
        )
    )

    for profile_id, profile in profiles_by_id.items():
        if profile["mode"] != "authored":
            continue
        lifecycle = profile["lifecycle"]
        domain = domains_by_profile.get(profile_id)
        if lifecycle is None or domain is None:
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_LIFECYCLE_DOMAIN",
                    profile=profile_id,
                    expected="one lifecycle domain for each authored profile",
                    actual="missing lifecycle domain assignment",
                )
            )
            continue
        status_domain = set(lifecycle["status_domain"])
        classified_states = set(domain["states"])
        if status_domain != classified_states:
            diagnostics.append(
                _diagnostic(
                    "REGISTRY_LIFECYCLE_DOMAIN",
                    profile=profile_id,
                    expected="profile statuses exactly match lifecycle state classes",
                    actual=(
                        f"profile={sorted(status_domain)!r} "
                        f"domain={sorted(classified_states)!r}"
                    ),
                )
            )

    return tuple(diagnostics)


def _shared_extension_diagnostics(raw_registry: Mapping[str, Any]) -> list[Diagnostic]:
    """Require every shared-contract extension name to appear once."""

    shared = raw_registry.get("shared_contract")
    if not isinstance(shared, Mapping):
        return []
    names = [extension_name(item) for item in shared.get("extensions", ())]
    return [
        _diagnostic(
            "REGISTRY_SHARED_EXTENSION",
            expected="one extension per name",
            actual=f"duplicate extension {name!r}",
        )
        for name in sorted({name for name in names if names.count(name) > 1})
    ]


FRONTMATTER_KEY_FIELDS = (
    "key",
    "purpose",
    "data_type",
    "condition",
    "authoring_owner",
    "derived_from",
    "duplicate_source",
    "consumer_paths",
    "lifecycle",
    "migration",
    "positive_test",
    "negative_test",
)
KEY_TABLE_COLUMNS = (
    "document_type",
    "key",
    "purpose",
    "type",
    "requiredness",
    "allowed_values",
    "authoring_owner",
    "derived_from",
    "duplicate_source",
    "consumer_paths",
    "lifecycle",
    "migration",
    "positive_test",
    "negative_test",
)
_EXTENSION_RECORD_FIELDS = ("condition", "owner", "verification", "review", "removal")


def _used_frontmatter_keys(raw_registry: Mapping[str, Any]) -> list[str]:
    """Every key any profile requires, allows, forbids or orders, first seen first."""

    used: dict[str, None] = {}
    for profile in raw_registry["profiles"]:
        lists = profile["frontmatter"]
        for field in ("required", "optional", "forbidden", "order"):
            used.update(dict.fromkeys(lists[field]))
    return list(used)


@lru_cache(maxsize=64)
def _test_function_sources(
    root: str, module: str, state: tuple[int, int]
) -> dict[str, str]:
    """Source text of every function in one test module, by name.

    ``state`` is the file's (size, mtime) so a changed module is read again.
    """

    text = read_repository_text(Path(root), PurePosixPath(module))
    return {
        node.name: ast.get_source_segment(text, node) or ""
        for node in ast.walk(ast.parse(text))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _test_reference_fault(root: Path, key: str, reference: Mapping[str, Any]) -> str:
    """Name what is wrong with one test reference, or return an empty string.

    It confirms that the module and the test exist and that the test's source
    contains the key; it does not claim the test exercises the key correctly.
    """

    try:
        module = _normalize_relative_path(reference["module"])
        file_state = (root.absolute() / module).lstat()
        sources = _test_function_sources(
            str(root.absolute()),
            module.as_posix(),
            (file_state.st_size, file_state.st_mtime_ns),
        )
    except (OSError, ValueError, SyntaxError):
        return f"module {reference['module']!r} is not a readable test module"
    source = sources.get(reference["test"])
    if source is None:
        return f"{reference['module']} has no test {reference['test']!r}"
    if key not in source:
        return f"{reference['test']} never names the key {key!r}"
    return ""


def current_registry_diagnostics(
    root: Path, raw_registry: Mapping[str, Any]
) -> tuple[Diagnostic, ...]:
    """SPEC-0181 checks of the current registry's key, dialect and extension records.

    These refuse what a comparison-base registry legitimately lacks, so they run
    from the strict registry validator and never on the load path.
    """

    faults: list[tuple[str, str, str, str]] = []
    keys = raw_registry.get("frontmatter_keys")
    if keys is None:
        faults.append(
            ("REGISTRY_FRONTMATTER_KEY", "a frontmatter_keys section", "missing", "")
        )
    else:
        names = [item["key"] for item in keys]
        used = _used_frontmatter_keys(raw_registry)
        for name in sorted({name for name in names if names.count(name) > 1}):
            faults.append(
                (
                    "REGISTRY_FRONTMATTER_KEY",
                    "one entry per key",
                    f"duplicate {name!r}",
                    "",
                )
            )
        for name in used:
            if name not in names:
                faults.append(
                    (
                        "REGISTRY_FRONTMATTER_KEY",
                        "an entry for every key a profile uses",
                        f"no entry for {name!r}",
                        "",
                    )
                )
        for name in sorted(set(names) - set(used)):
            faults.append(
                (
                    "REGISTRY_FRONTMATTER_KEY",
                    "no entry for a key no profile uses",
                    f"stray entry {name!r}",
                    "",
                )
            )
        for item in keys:
            name = item["key"]
            consumers = item["consumer_paths"]
            if not consumers:
                faults.append(
                    (
                        "REGISTRY_KEY_CONSUMER",
                        "at least one consumer path",
                        f"{name}: none",
                        "",
                    )
                )
            for named in consumers:
                try:
                    normalized = _normalize_relative_path(named)
                    if normalized.as_posix() != named:
                        raise ValueError("path is not canonical")
                    if not stat.S_ISREG(_lstat_named_path(root.absolute(), normalized)):
                        raise ValueError("not a regular file")
                except ValueError as exc:
                    faults.append(
                        (
                            "REGISTRY_KEY_CONSUMER",
                            "consumer paths naming existing regular files",
                            f"{name}: {named}: {exc}",
                            "",
                        )
                    )
            for field in ("positive_test", "negative_test"):
                fault = _test_reference_fault(root, name, item[field])
                if fault:
                    faults.append(
                        (
                            "REGISTRY_KEY_TEST",
                            f"a resolvable {field}",
                            f"{name}: {fault}",
                            "",
                        )
                    )
    if raw_registry.get("frontmatter_dialect") is None:
        faults.append(
            (
                "REGISTRY_FRONTMATTER_DIALECT",
                "a frontmatter_dialect section",
                "missing",
                "",
            )
        )
    shared = raw_registry.get("shared_contract")
    for extension in (shared or {}).get("extensions", ()):
        if isinstance(extension, str):
            continue
        for field in _EXTENSION_RECORD_FIELDS:
            if extension[field] == "unverified":
                faults.append(
                    (
                        "REGISTRY_SHARED_EXTENSION",
                        f"a recorded {field} for each extension",
                        f"{extension['name']!r} holds unverified",
                        "",
                    )
                )
    return tuple(
        _diagnostic(rule, profile=profile, expected=expected, actual=actual)
        for rule, expected, actual, profile in faults
    )


def _schema_grammar(prop: Mapping[str, Any], defs: Mapping[str, Any]) -> str:
    """Render one frontmatter schema property as the grammar a value must meet."""

    if "$ref" in prop:
        return _schema_grammar(defs[prop["$ref"].rsplit("/", 1)[-1]], defs)
    if "oneOf" in prop:
        return " or ".join(_schema_grammar(item, defs) for item in prop["oneOf"])
    kind = prop.get("type")
    if kind == "array":
        return f"array of {_schema_grammar(prop['items'], defs)}"
    if kind == "object":
        return "mapping with keys " + ", ".join(
            prop.get("required", prop["properties"])
        )
    if "pattern" in prop:
        return f"{kind} matching {prop['pattern']}"
    return f"non-empty {kind}" if prop.get("minLength") else str(kind)


def frontmatter_key_table(
    raw_registry: Mapping[str, Any],
    frontmatter_schema: Mapping[str, Any],
    claude_bindings: Mapping[str, Any],
) -> tuple[dict[str, Any], ...]:
    """Derive the fourteen-column key table of the W03 task, one row per profile key.

    Nothing here is stored: ``requiredness`` comes from the profile's frontmatter
    lists and the entry's condition, ``allowed_values`` from the profile
    constants and status domain, the frontmatter schema grammar for a shared
    key, the Claude provider binding for ``model``, ``effort`` and ``tools``, and
    provider-owned free text for any other native key; the remaining columns
    come from ``frontmatter_keys``. A profile whose frontmatter mode is
    ``absent`` lists no key and adds no row.
    """

    entries = {item["key"]: item for item in raw_registry["frontmatter_keys"]}
    profiles = {item["id"]: item for item in raw_registry["profiles"]}
    properties = frontmatter_schema["properties"]
    defs = frontmatter_schema["$defs"]
    overrides = claude_bindings["role_overrides"].values()
    bound = {
        "model": {
            *claude_bindings["capability_models"].values(),
            *(item["model"] for item in overrides if "model" in item),
        },
        "effort": {
            *claude_bindings["capability_reasoning"].values(),
            *(
                item["reasoning_effort"]
                for item in overrides
                if "reasoning_effort" in item
            ),
        },
        "tools": {
            tool
            for scope in claude_bindings["permission_scopes"].values()
            for tool in scope
        },
    }

    def status_domain(profile: Mapping[str, Any]) -> list[str]:
        owner = profile
        if not (profile.get("lifecycle") or {}).get("status_domain"):
            sources = profile["relationships"]["source_profile_ids"]
            owner = profiles[sources[0]] if sources else profile
        return list((owner.get("lifecycle") or {}).get("status_domain", ()))

    def allowed(profile: Mapping[str, Any], key: str) -> str:
        constants = profile["frontmatter"]["constants"]
        if key in constants:
            return f"constant {json.dumps(constants[key])}"
        if key == "status" and status_domain(profile):
            return "one of " + ", ".join(status_domain(profile))
        if key in properties:
            return _schema_grammar(properties[key], defs)
        if key in bound:
            return (
                "comma-separated subset of " if key == "tools" else "one of "
            ) + ", ".join(sorted(bound[key]))
        return "provider-owned free text"

    rows: list[dict[str, Any]] = []
    for profile in raw_registry["profiles"]:
        lists = profile["frontmatter"]
        listed = {
            **dict.fromkeys(lists["order"]),
            **dict.fromkeys(
                [*lists["required"], *lists["optional"], *lists["forbidden"]]
            ),
        }
        for key in listed:
            entry = entries[key]
            if key in lists["required"]:
                requiredness = "required"
            elif key in lists["forbidden"]:
                requiredness = "forbidden"
            elif entry["condition"]:
                requiredness = f"conditional: {entry['condition']}"
            else:
                requiredness = "optional"
            rows.append(
                {
                    "document_type": profile["id"],
                    "key": key,
                    "purpose": entry["purpose"],
                    "type": entry["data_type"],
                    "requiredness": requiredness,
                    "allowed_values": allowed(profile, key),
                    "authoring_owner": entry["authoring_owner"],
                    "derived_from": entry["derived_from"],
                    "duplicate_source": entry["duplicate_source"],
                    "consumer_paths": list(entry["consumer_paths"]),
                    "lifecycle": entry["lifecycle"],
                    "migration": entry["migration"],
                    "positive_test": "{module}::{test}".format(
                        **entry["positive_test"]
                    ),
                    "negative_test": "{module}::{test}".format(
                        **entry["negative_test"]
                    ),
                }
            )
    return tuple(rows)


def _form_section_diagnostics(
    form: Mapping[str, Any],
) -> list[tuple[str, str, str]]:
    """Check one form's tree: nesting, levels, order, uniqueness and conditions."""

    faults: list[tuple[str, str, str]] = []
    seen_ids: set[str] = set()

    def walk(
        items: Sequence[Mapping[str, Any]],
        parent: Mapping[str, Any] | None,
        level: int,
    ) -> None:
        orders = [item["order"] for item in items]
        if any(left >= right for left, right in zip(orders, orders[1:])):
            faults.append(
                (
                    "REGISTRY_FORM_ORDER",
                    "sibling sections listed in strictly increasing order",
                    f"{form['form_id']}: {orders!r}",
                )
            )
        titles = [item["title"] for item in items]
        for title in sorted({name for name in titles if titles.count(name) > 1}):
            faults.append(
                (
                    "REGISTRY_FORM_SECTION",
                    "unique sibling titles",
                    f"{form['form_id']}: duplicate title {title!r}",
                )
            )
        for item in items:
            where = f"{form['form_id']}: {item['section_id']}"
            if item["section_id"] in seen_ids:
                faults.append(
                    (
                        "REGISTRY_FORM_SECTION",
                        "unique section IDs",
                        f"{where} repeats",
                    )
                )
            seen_ids.add(item["section_id"])
            if item["level"] != level:
                faults.append(
                    ("REGISTRY_FORM_LEVEL", f"level {level} at this depth", where)
                )
            expected_parent = parent["section_id"] if parent else None
            if item["parent_id"] != expected_parent:
                faults.append(
                    (
                        "REGISTRY_FORM_PARENT",
                        f"parent_id {expected_parent!r}",
                        f"{where}: {item['parent_id']!r}",
                    )
                )
            if item["requiredness"] == "conditional" and item["condition"] == "always":
                faults.append(
                    (
                        "REGISTRY_FORM_CONDITION",
                        "a conditional section names its own condition",
                        where,
                    )
                )
            if level == 3 and item["children"]:
                faults.append(("REGISTRY_FORM_LEVEL", "no sections below an H3", where))
            elif level == 2:
                walk(item["children"], item, 3)

    walk(form["sections"], None, 2)
    top = {item["section_id"]: item for item in form["sections"]}
    extension_ids: set[str] = set()
    local_titles: set[tuple[str, str]] = set()
    for extension in form["extensions"]:
        where = f"{form['form_id']}: {extension['id']}"
        if extension["id"] in extension_ids:
            faults.append(("REGISTRY_FORM_EXTENSION", "unique extension IDs", where))
        extension_ids.add(extension["id"])
        if extension["kind"] != "local_h3":
            continue
        parent = top.get(extension["parent_id"])
        if parent is None:
            faults.append(
                (
                    "REGISTRY_FORM_EXTENSION",
                    "a parent_id naming an H2 section of the form",
                    f"{where}: {extension['parent_id']!r}",
                )
            )
            continue
        taken = {child["title"] for child in parent["children"]}
        key = (parent["section_id"], extension["title"])
        if extension["title"] in taken or key in local_titles:
            faults.append(
                (
                    "REGISTRY_FORM_EXTENSION",
                    "a title unused under its parent",
                    f"{where}: {extension['title']!r}",
                )
            )
        local_titles.add(key)
    return faults


_TABLE_HEADING_LINE = re.compile(r"(#{2,3}) (\S(?:.*\S)?)")


def _table_diagnostics(
    tables: Sequence[Mapping[str, Any]],
    form: Mapping[str, Any] | None,
    body_contract: Mapping[str, Any] | None,
    required_h2: Sequence[str] = (),
) -> list[tuple[str, str, str]]:
    """Check each template table against its role's form and the body contract.

    A role without a form names a table's section by its template heading line;
    no template body is read here, so only the line's shape and an H2 title in
    the profile's required list are checked (BODY-TABLE-SECTION reads the body).
    """

    section_ids: set[str] = set()
    if form is not None:
        stack = list(form["sections"])
        while stack:
            item = stack.pop()
            section_ids.add(item["section_id"])
            stack.extend(item["children"])
        section_ids.update(
            item["id"] for item in form["extensions"] if item["kind"] == "local_h3"
        )
    faults: list[tuple[str, str, str]] = []
    for table in tables:
        name = table["name"]
        keys = [column["key"] for column in table["columns"]]
        if form is None:
            heading = _TABLE_HEADING_LINE.fullmatch(table["section"])
            if heading is None or (
                len(heading.group(1)) == 2 and heading.group(2) not in required_h2
            ):
                faults.append(
                    (
                        "REGISTRY_TABLE_SECTION",
                        "an H3 heading line, or an H2 heading line whose title "
                        "is in the profile's required list",
                        f"{name}: {table['section']!r}",
                    )
                )
        elif table["section"] not in section_ids:
            faults.append(
                (
                    "REGISTRY_TABLE_SECTION",
                    "a section ID or local_h3 extension ID of the role's form",
                    f"{name}: {table['section']!r}",
                )
            )
        if len(keys) != len(set(keys)) or table["row_identity"] not in keys:
            faults.append(
                (
                    "REGISTRY_TABLE_COLUMNS",
                    "unique column keys and a row_identity naming one of them",
                    f"{name}: keys {keys!r}, row_identity {table['row_identity']!r}",
                )
            )
        flags = [column["required"] for column in table["columns"]]
        if False in flags and True in flags[flags.index(False) :]:
            faults.append(
                (
                    "REGISTRY_TABLE_COLUMNS",
                    "optional columns only after every required column",
                    f"{name}: required flags {flags!r}",
                )
            )
        if (
            body_contract is not None
            and name == body_contract["table_heading"]
            and keys != body_contract["required_columns"]
        ):
            faults.append(
                (
                    "REGISTRY_TABLE_BODY_CONTRACT",
                    f"the body contract's columns {body_contract['required_columns']!r}",
                    f"{name}: {keys!r}",
                )
            )
    return faults


def _form_registry_diagnostics(
    root: Path,
    raw_registry: Mapping[str, Any],
    profiles_by_id: Mapping[str, Mapping[str, Any]],
    template_regular_paths: frozenset[PurePosixPath] | None = None,
) -> list[Diagnostic]:
    """SPEC-0168: validate forms, role bindings and TemplateDefinitions."""

    faults: list[tuple[str, str, str, str]] = []
    forms = (raw_registry.get("common_forms") or {}).get("forms", [])
    form_ids = [form["form_id"] for form in forms]
    for form_id in sorted({name for name in form_ids if form_ids.count(name) > 1}):
        faults.append(("REGISTRY_FORM_DUPLICATE", "one form per role", form_id, ""))
    for form in forms:
        faults.extend((*fault, "") for fault in _form_section_diagnostics(form))
    roles_with_form = set(form_ids)
    forms_by_role = {form["form_id"]: form for form in forms}
    for profile_id, profile in profiles_by_id.items():
        role = profile.get("document_role")
        lists = profile["sections"]
        if role in roles_with_form and (
            lists["required"] or lists["optional"] or lists["forbidden"]
        ):
            faults.append(
                (
                    "REGISTRY_FORM_LEGACY_LISTS",
                    "a profile whose role has a form carries no H2 lists",
                    f"role {role}",
                    profile_id,
                )
            )
        definition = profile.get("template_definition")
        if definition is None:
            if profile["mode"] == "template" and role in roles_with_form:
                faults.append(
                    (
                        "REGISTRY_TEMPLATE_DEFINITION",
                        "a template whose role has a form carries its definition",
                        f"role {role}",
                        profile_id,
                    )
                )
            continue
        if profile["mode"] != "template" or role is None:
            faults.append(
                (
                    "REGISTRY_TEMPLATE_DEFINITION",
                    "a definition only on a template profile with a document_role",
                    f"mode {profile['mode']}, role {role}",
                    profile_id,
                )
            )
        faults.extend(
            (*fault, profile_id)
            for fault in _table_diagnostics(
                definition["tables"],
                forms_by_role.get(role),
                profile["relationships"]["body_contract"],
                profile["sections"]["required"],
            )
        )
        for named in definition["consumer_paths"]:
            try:
                named_path = _normalize_relative_path(named)
                if named_path.as_posix() != named:
                    raise ValueError("path is not canonical")
                if not stat.S_ISREG(_lstat_named_path(root, named_path)):
                    raise ValueError("not a regular file")
            except ValueError as exc:
                faults.append(
                    (
                        "REGISTRY_TEMPLATE_DEFINITION",
                        "consumer paths naming existing regular files",
                        f"{named}: {exc}",
                        profile_id,
                    )
                )
    # A template's tables are inherited by each source it names, so a source
    # named by two tabled twins would silently keep only the later one's.
    twins_of: dict[str, list[str]] = {}
    for profile_id, profile in profiles_by_id.items():
        if profile["mode"] == "template" and (
            profile.get("template_definition") or {}
        ).get("tables"):
            for source in profile["relationships"]["source_profile_ids"]:
                twins_of.setdefault(source, []).append(profile_id)
    for source, twins in twins_of.items():
        if len(twins) > 1:
            faults.append(
                (
                    "REGISTRY_TABLE_TWIN",
                    "a source profile named by at most one template twin that carries tables",
                    f"named by {sorted(twins)!r}",
                    source,
                )
            )
    group = {
        profile_id
        for profile_id, profile in profiles_by_id.items()
        if profile_id in POLICY_ROLE_SOURCES
        or set(profile["relationships"]["source_profile_ids"])
        & set(POLICY_ROLE_SOURCES)
    }
    policy_roles = {profiles_by_id[item].get("document_role") for item in group}
    # None and "policy" are each fine alone; a mix, or any other role, is not.
    if len(policy_roles) > 1 or policy_roles - {None, "policy"}:
        faults.append(
            (
                "REGISTRY_POLICY_ROLE",
                "governance/rule, operation/policy and their template twins share the policy role",
                repr(sorted(map(str, policy_roles))),
                "",
            )
        )
    return [
        _diagnostic(rule, profile=profile_id, expected=expected, actual=actual)
        for rule, expected, actual, profile_id in faults
    ]


def _common_form_from_mapping(raw: Mapping[str, Any]) -> CommonForm:
    def section(item: Mapping[str, Any]) -> FormSection:
        return FormSection(
            section_id=item["section_id"],
            title=item["title"],
            level=item["level"],
            parent_id=item["parent_id"],
            order=item["order"],
            requiredness=item["requiredness"],
            condition=item["condition"],
            empty_policy=item["empty_policy"],
            link_only=item.get("link_only", False),
            children=tuple(section(child) for child in item["children"]),
        )

    def extension(item: Mapping[str, Any]) -> FormExtension:
        lists = item.get("retained_sections")
        return FormExtension(
            extension_id=item["id"],
            kind=item["kind"],
            condition=item["condition"],
            owner=item["owner"],
            verification=item["verification"],
            review=item["review"],
            removal=item["removal"],
            parent_id=item.get("parent_id"),
            title=item.get("title"),
            statuses=tuple(item.get("statuses", ())),
            retained=(
                None
                if lists is None
                else HeadingContract(
                    required=tuple(lists["required"]),
                    allowed=tuple(lists["required"] + lists["optional"]),
                    substantive_body=lists.get("substantive_body", False),
                    ordered=lists.get("ordered", False),
                )
            ),
        )

    return CommonForm(
        form_id=raw["form_id"],
        title=raw["title"],
        h1=raw["h1"],
        language_rule=raw["language_rule"],
        extension_policy=raw["extension_policy"],
        sections=tuple(section(item) for item in raw["sections"]),
        extensions=tuple(extension(item) for item in raw["extensions"]),
    )


def _shared_contract_from_mapping(raw: Mapping[str, Any]) -> SharedContract:
    # A comparison-base registry from before the object shape lists bare names;
    # what it never recorded reads as unverified, as for the repository record.
    return SharedContract(
        **{
            **raw,
            "extensions": tuple(
                SharedExtension(item, item, *("unverified",) * 4)
                if isinstance(item, str)
                else SharedExtension(**item)
                for item in raw["extensions"]
            ),
        }
    )


def _typed_registry_from_mapping(raw: Mapping[str, Any]) -> Registry:
    domains = tuple(
        LifecycleDomain(
            family=item["family"],
            profile_ids=tuple(item["profile_ids"]),
            states=tuple(item["states"].items()),
            transitions=frozenset(tuple(edge) for edge in item["transitions"]),
            initial_states=(
                tuple(item["initial_states"]) if "initial_states" in item else None
            ),
        )
        for item in raw["lifecycle_domains"]
    )
    domains_by_profile = {
        profile_id: domain for domain in domains for profile_id in domain.profile_ids
    }

    forms = tuple(
        _common_form_from_mapping(item)
        for item in (raw.get("common_forms") or {}).get("forms", ())
    )
    forms_by_role = {form.form_id: form for form in forms}

    def typed_profile(profile: Mapping[str, Any]) -> DocumentProfile:
        return _profile_from_mapping(
            profile,
            lifecycle_domain=domains_by_profile.get(profile["id"]),
            form=forms_by_role.get(profile.get("document_role")),
        )

    profiles = tuple(typed_profile(profile) for profile in raw["profiles"])
    profiles_by_id = {profile.profile_id: profile for profile in profiles}
    profiles = tuple(
        replace(
            profile,
            status_domain=(
                (dict(profile.constants)["status"],)
                if "status" in dict(profile.constants)
                else profiles_by_id[profile.source_profile_ids[0]].status_domain
            ),
        )
        if profile.mode == "template" and profile.source_profile_ids
        else profile
        for profile in profiles
    )
    # A template's tables are the contract of the documents it was copied from.
    inherited = {
        source: profile.tables
        for profile in profiles
        if profile.mode == "template" and profile.tables
        for source in profile.source_profile_ids
    }
    profiles = tuple(
        replace(profile, tables=inherited[profile.profile_id])
        if profile.profile_id in inherited
        else profile
        for profile in profiles
    )
    return Registry(
        schema_version=raw["schema_version"],
        shared_contract=(
            _shared_contract_from_mapping(raw["shared_contract"])
            if "shared_contract" in raw
            else None
        ),
        profiles=profiles,
        lifecycle_domains=domains,
        readme_navigation=_readme_navigation_from_mapping(raw.get("readme_navigation")),
        document_language=_document_language_from_mapping(raw.get("document_language")),
        common_forms=forms,
        frontmatter_keys=tuple(
            _frontmatter_key_from_mapping(item)
            for item in raw.get("frontmatter_keys", ())
        ),
        frontmatter_dialect=_frontmatter_dialect_from_mapping(
            raw.get("frontmatter_dialect")
        ),
    )


def _frontmatter_key_from_mapping(raw: Mapping[str, Any]) -> FrontmatterKey:
    return FrontmatterKey(
        **{
            **raw,
            "consumer_paths": tuple(raw["consumer_paths"]),
            "positive_test": KeyTestReference(**raw["positive_test"]),
            "negative_test": KeyTestReference(**raw["negative_test"]),
        }
    )


def _frontmatter_dialect_from_mapping(
    raw: Mapping[str, Any] | None,
) -> FrontmatterDialect | None:
    if raw is None:
        return None
    return FrontmatterDialect(
        current_yaml=raw["current"]["yaml"],
        current_library=raw["current"]["library"],
        loaders=tuple(FrontmatterLoader(**item) for item in raw["current"]["loaders"]),
        target_yaml=raw["target"]["yaml"],
        target_decision=raw["target"]["decision"],
        target_asserted_by_check=raw["target"]["asserted_by_check"],
        schema_dialect=raw["schema"]["dialect"],
        schema_format=raw["schema"]["format"],
        date_rule=raw["dates"]["rule"],
        date_checked_by=raw["dates"]["checked_by"],
    )


def _readme_navigation_from_mapping(
    raw: Mapping[str, Any] | None,
) -> ReadmeNavigation | None:
    if raw is None:
        return None
    return ReadmeNavigation(
        placeholders=frozenset(raw["placeholders"]),
        forbidden_index_columns=frozenset(raw["forbidden_index_columns"]),
        max_deep_links_per_child=raw["max_deep_links_per_child"],
        profiles=MappingProxyType(
            {
                profile_id: ReadmeNavigationProfile(
                    section=entry["section"], complete=entry["complete"]
                )
                for profile_id, entry in raw["profiles"].items()
            }
        ),
        pending_paths=frozenset(PurePosixPath(value) for value in raw["pending_paths"]),
        exempt_paths=frozenset(PurePosixPath(value) for value in raw["exempt_paths"]),
        index_columns=tuple(raw.get("index_columns", ())),
        optional_index_columns=tuple(raw.get("optional_index_columns", ())),
    )


def _readme_navigation_registry_diagnostics(
    raw_registry: Mapping[str, Any],
    profiles_by_id: Mapping[str, Mapping[str, Any]],
) -> list[Diagnostic]:
    """Require navigation entries to name README roles and their own sections.

    A section is a required H2 of the profile lists or, for a profile whose
    role has a form, a required H2 or H3 title unique among the form's titles.
    """

    contract = raw_registry.get("readme_navigation")
    if contract is None:
        return []
    forms = {
        form["form_id"]: form
        for form in (raw_registry.get("common_forms") or {}).get("forms", ())
    }
    faults: list[str] = []
    for profile_id, entry in contract["profiles"].items():
        profile = profiles_by_id.get(profile_id)
        if profile is None:
            faults.append(f"unknown profile {profile_id}")
            continue
        pack_anchor = (
            profile_id
            in {
                "reference/audit-pack",
                "reference/research-pack",
                "reference/data-pack",
            }
            and profile.get("mode") == "authored"
        )
        if profile.get("mode") != "router" and not pack_anchor:
            faults.append(f"{profile_id} is not a README navigation profile")
        allowed = set(profile.get("sections", {}).get("required", ()))
        form = forms.get(profile.get("document_role"))
        if form is not None:
            titles = [
                (item["title"], item["requiredness"])
                for section in form["sections"]
                for item in (section, *section["children"])
            ]
            names = [title for title, _ in titles]
            allowed.update(
                title
                for title, requiredness in titles
                if requiredness == "required" and names.count(title) == 1
            )
        if entry["section"] not in allowed:
            faults.append(f"{profile_id} section {entry['section']!r} is not required")
    if contract["max_deep_links_per_child"] < 1:
        faults.append("max_deep_links_per_child is below one")
    for key in ("pending_paths", "exempt_paths"):
        for value in contract[key]:
            if PurePosixPath(value).name != "README.md":
                faults.append(f"{key} entry {value} is not a README")
    for value in sorted(set(contract["pending_paths"]) & set(contract["exempt_paths"])):
        faults.append(f"{value} is both pending and exempt")
    return [
        _diagnostic(
            "REGISTRY_README_NAVIGATION",
            expected=(
                "README roles, their required H2 sections or their form's "
                "required, unique H2 or H3 titles, and README paths"
            ),
            actual=fault,
        )
        for fault in faults
    ]


def _document_language_from_mapping(
    raw: Mapping[str, Any] | None,
) -> DocumentLanguage | None:
    if raw is None:
        return None
    return DocumentLanguage(
        english_only_roots=tuple(raw["english_only_roots"]),
        korean_allowed_markdown_roots=tuple(
            raw.get("korean_allowed_markdown_roots", ())
        ),
        english_only_suffixes=frozenset(raw["english_only_suffixes"]),
        korean_first_profiles=frozenset(raw["korean_first_profiles"]),
        english_sections=frozenset(raw["english_sections"]),
        min_latin_words=raw["min_latin_words"],
        pending_paths=frozenset(PurePosixPath(value) for value in raw["pending_paths"]),
    )


def _document_language_registry_diagnostics(
    raw_registry: Mapping[str, Any],
    profiles_by_id: Mapping[str, Mapping[str, Any]],
) -> list[Diagnostic]:
    """Require the language contract to name real, checked profiles and paths."""

    contract = raw_registry.get("document_language")
    if contract is None:
        return []
    faults: list[str] = []
    for profile_id in contract["korean_first_profiles"]:
        profile = profiles_by_id.get(profile_id)
        if profile is None:
            faults.append(f"unknown profile {profile_id}")
        elif profile.get("mode") not in {"authored", "router"}:
            faults.append(f"{profile_id} is not an authored or router profile")
    roots = tuple(contract["english_only_roots"])
    for root in roots:
        if not root.endswith("/"):
            faults.append(f"english-only root {root} does not end in /")
    for root in contract.get("korean_allowed_markdown_roots", ()):
        if root != ".agents/" or root not in roots:
            faults.append(
                f"Korean-allowed Markdown root {root} is not an English-only .agents/ root"
            )
    for suffix in contract["english_only_suffixes"]:
        if not suffix.startswith("."):
            faults.append(f"suffix {suffix} does not start with .")
    sections = contract["english_sections"]
    if any(not name.strip() for name in sections) or len(set(sections)) != len(
        sections
    ):
        faults.append("english sections are empty or repeated")
    if contract["min_latin_words"] < 1:
        faults.append("min_latin_words is below one")
    for value in contract["pending_paths"]:
        if value.startswith(roots) and PurePosixPath(value).name != "README.md":
            faults.append(f"pending path {value} is under an English-only root")
    return [
        _diagnostic(
            "REGISTRY_DOCUMENT_LANGUAGE",
            expected="checked profiles, well-formed roots and suffixes, convertible paths",
            actual=fault,
        )
        for fault in faults
    ]


def validate_registry(
    root: Path,
    raw_registry: Mapping[str, Any],
    *,
    template_regular_paths: frozenset[PurePosixPath] | None = None,
    trusted_registry: Registry | None = None,
    raw_schema: object = _UNSET,
) -> Registry:
    """Validate a payload with filesystem or caller-proved Git template regularity.

    Supplied paths replace only template existence/type lookup, never schema,
    path normalization, profile, relationship, or lifecycle validation.
    A supplied trusted registry binds every profile's literal executable patterns
    before proposed pattern compilation, projection, or classification.
    """

    root = root.absolute()
    if raw_schema is not _UNSET and (
        not isinstance(template_regular_paths, frozenset)
        or any(not isinstance(path, PurePosixPath) for path in template_regular_paths)
    ):
        _fail(
            "REGISTRY_SCHEMA",
            expected="complete supplied schema and template regularity facts",
            actual="template facts are unavailable",
        )
    schema = (
        load_json_file(root / SCHEMA_PATH, diagnostic_path=SCHEMA_PATH)
        if raw_schema is _UNSET
        else raw_schema
    )
    if not isinstance(schema, dict):
        _fail(
            "REGISTRY_SCHEMA",
            expected="a JSON Schema object",
            actual=type(schema).__name__,
        )
    try:
        errors = schema_errors(schema, raw_registry)
    except SchemaEvaluationError:
        _fail(
            "REGISTRY_SCHEMA",
            expected="a valid local JSON Schema",
            actual="schema configuration or evaluation failed",
        )
    if errors:
        raise DocumentContractError(
            tuple(
                _diagnostic(
                    _schema_rule_id(error),
                    expected=error.message,
                    actual="schema validation failed",
                )
                for error in errors
            )
        )
    if trusted_registry is not None:
        proposed_profiles = raw_registry["profiles"]
        proposed_ids = tuple(profile["id"] for profile in proposed_profiles)
        trusted_ids = tuple(profile.profile_id for profile in trusted_registry.profiles)
        matches = len(set(proposed_ids)) == len(proposed_ids) and set(
            proposed_ids
        ) == set(trusted_ids)
        if matches:
            trusted_profiles = {
                profile.profile_id: profile for profile in trusted_registry.profiles
            }
            matches = all(
                profile["path_pattern"] == trusted_profiles[profile["id"]].path_pattern
                and profile.get("artifact_id_pattern")
                == trusted_profiles[profile["id"]].artifact_id_pattern
                for profile in proposed_profiles
            )
        if not matches:
            _fail(
                "REGISTRY_EXECUTABLE_POLICY",
                expected="the trusted profile identities and literal patterns",
                actual="proposed executable policy differs",
            )
    try:
        validate_registry_authority(raw_registry)
    except AuthorityError as exc:
        _fail(
            "REGISTRY_AUTHORITY",
            expected="the sole bounded Stage 99 document-profile authority",
            actual=str(exc),
        )
    semantic_diagnostics = _terminal_semantic_diagnostics(
        root, raw_registry, template_regular_paths=template_regular_paths
    )
    if semantic_diagnostics:
        raise DocumentContractError(semantic_diagnostics)
    return _typed_registry_from_mapping(raw_registry)


def _load_published_contract(
    root: Path,
    path: PurePosixPath,
    schema_path: PurePosixPath,
    *,
    raw_payload: object = _UNSET,
    raw_schema: object = _UNSET,
) -> dict[str, Any]:
    """Decode one published contract and validate it against its own schema.

    Identity is checked before the schema is read so that a payload from a
    retired schema generation is rejected as REGISTRY_SCHEMA rather than
    reaching a schema this repository no longer ships.
    """

    if (raw_payload is _UNSET) != (raw_schema is _UNSET):
        _fail(
            "REGISTRY_SCHEMA",
            expected="complete supplied registry and schema inputs",
            actual="a supplied input is unavailable",
        )
    payload = (
        load_json_file(root / path, diagnostic_path=path)
        if raw_payload is _UNSET
        else raw_payload
    )
    if not isinstance(payload, dict):
        _fail(
            "REGISTRY_SCHEMA",
            expected=f"a JSON object at {path.as_posix()}",
            actual=type(payload).__name__,
        )
    expected_id = f"https://hy-home.k8s/{path.as_posix()}"
    if payload.get("schema_version") != 10 or payload.get("$id") != expected_id:
        _fail(
            "REGISTRY_SCHEMA",
            expected=f"schema_version=10 $id={expected_id!r}",
            actual=(
                f"schema_version={payload.get('schema_version')!r} "
                f"$id={payload.get('$id')!r}"
            ),
        )
    schema = (
        load_json_file(root / schema_path, diagnostic_path=schema_path)
        if raw_schema is _UNSET
        else raw_schema
    )
    if not isinstance(schema, dict):
        _fail(
            "REGISTRY_SCHEMA",
            expected=f"a JSON Schema object at {schema_path.as_posix()}",
            actual=type(schema).__name__,
        )
    try:
        errors = schema_errors(schema, payload)
    except SchemaEvaluationError:
        _fail(
            "REGISTRY_SCHEMA",
            expected="a valid local JSON Schema",
            actual="schema configuration or evaluation failed",
        )
    if errors:
        raise DocumentContractError(
            tuple(
                _diagnostic(
                    _schema_rule_id(error),
                    path=path,
                    expected=error.message,
                    actual="schema validation failed",
                )
                for error in errors
            )
        )
    return dict(payload)


def _split_top_level_alternation(body: str) -> list[str]:
    """Split one alternation, ignoring bars inside groups, classes, or escapes."""

    parts: list[str] = []
    buffer: list[str] = []
    depth = 0
    in_class = False
    index = 0
    while index < len(body):
        char = body[index]
        if char == "\\":
            buffer.append(body[index : index + 2])
            index += 2
            continue
        if in_class:
            if char == "]":
                in_class = False
        elif char == "[":
            in_class = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "|" and depth == 0:
            parts.append("".join(buffer))
            buffer = []
            index += 1
            continue
        buffer.append(char)
        index += 1
    parts.append("".join(buffer))
    return parts


def _internal_routes(pattern: str) -> list[dict[str, str]]:
    """Recover the internal route list a published ``path_pattern`` encodes.

    The published form states one anchored expression per profile, with an
    alternation when the profile owns several routes. Recovering the branches
    matters beyond matching: self-tests select a route by ``kind``, so a
    projection that flattened every branch to one regex would silently retarget
    them. A branch whose escaping round-trips is an exact route; anything else
    stays a regex.
    """

    if not (pattern.startswith("^") and pattern.endswith("$")):
        _fail(
            "REGISTRY_SCHEMA",
            expected="an anchored path_pattern",
            actual=pattern,
        )
    inner = pattern[1:-1]
    branches = (
        _split_top_level_alternation(inner[3:-1])
        if inner.startswith("(?:") and inner.endswith(")")
        else [inner]
    )
    routes: list[dict[str, str]] = []
    for branch in branches:
        literal = re.sub(r"\\(.)", r"\1", branch)
        if re.escape(literal) == branch:
            routes.append({"kind": "exact", "value": literal})
        else:
            routes.append({"kind": "regex", "value": f"^{branch}$"})
    return routes


def _typed_profile_class(profile: Mapping[str, Any]) -> str:
    """Return the stable typed category for one public v9 profile."""

    family = profile["family"]
    if family != "common":
        return family
    if profile["mode"] == "router":
        return "readme"
    source_ids = profile["relationships"]["source_profile_ids"]
    if profile["mode"] == "template" and source_ids:
        source_family = source_ids[0].split("/", 1)[0]
        if source_family in {
            "governance",
            "sdlc",
            "operation",
            "reference",
            "evaluation",
        }:
            return source_family
        if source_ids[0].startswith("common/readme-"):
            return "readme"
    return "exception"


def load_internal_payload(
    root: Path,
    *,
    raw_registry: object = _UNSET,
    raw_schema: object = _UNSET,
    template_regular_paths: frozenset[PurePosixPath] | None = None,
) -> dict[str, Any]:
    """Return a defensive copy of the sole published Stage 99 registry.

    The terminal topology deliberately has no flat-registry or route-contract
    projection. Consumers mutate only this private copy in tests; production
    authority remains the root registry and its profile schema.
    """

    root = root.absolute()
    if (
        raw_registry is not _UNSET
        or raw_schema is not _UNSET
        or template_regular_paths is not None
    ) and (
        raw_registry is _UNSET
        or raw_schema is _UNSET
        or not isinstance(template_regular_paths, frozenset)
        or any(not isinstance(path, PurePosixPath) for path in template_regular_paths)
    ):
        _fail(
            "REGISTRY_SCHEMA",
            expected="complete supplied registry, schema and template regularity facts",
            actual="a supplied input is unavailable or malformed",
        )
    registry = _load_published_contract(
        root,
        REGISTRY_PATH,
        PROFILE_SCHEMA_PATH,
        raw_payload=raw_registry,
        raw_schema=raw_schema,
    )
    try:
        validate_registry_authority(registry)
    except AuthorityError as exc:
        _fail(
            "REGISTRY_AUTHORITY",
            expected="the sole bounded Stage 99 document-profile authority",
            actual=str(exc),
        )
    semantic_diagnostics = _terminal_semantic_diagnostics(
        root, registry, template_regular_paths=template_regular_paths
    )
    if semantic_diagnostics:
        raise DocumentContractError(semantic_diagnostics)
    return copy.deepcopy(registry)


def load_registry(
    root: Path,
    *,
    raw_registry: object = _UNSET,
    raw_schema: object = _UNSET,
    template_regular_paths: frozenset[PurePosixPath] | None = None,
) -> Registry:
    """Build the typed view directly from the root registry authority."""

    return _typed_registry_from_mapping(
        load_internal_payload(
            root,
            raw_registry=raw_registry,
            raw_schema=raw_schema,
            template_regular_paths=template_regular_paths,
        )
    )


def _route_matches(route: Route, path: PurePosixPath) -> bool:
    value = path.as_posix()
    if route.kind == "exact":
        return value == route.value
    return _compile_route(route.value).fullmatch(value) is not None


def classify_path(registry: Registry, path: PurePosixPath) -> DocumentProfile:
    try:
        normalized = _normalize_relative_path(path)
    except ValueError as exc:
        raise DocumentContractError(
            (
                _diagnostic(
                    "REGISTRY_ROUTE_PATH",
                    path=PurePosixPath(str(path)),
                    expected="a normalized POSIX repository-relative path",
                    actual=str(exc),
                ),
            )
        ) from exc

    matches = tuple(
        (profile, route)
        for profile in registry.profiles
        for route in profile.routes
        if _route_matches(route, normalized)
    )
    if not matches:
        raise DocumentContractError(
            (
                _diagnostic(
                    "REGISTRY_ROUTE_UNCOVERED",
                    path=normalized,
                    expected="exactly one matching profile",
                    actual="no matching profile",
                ),
            )
        )
    if len(matches) != 1:
        raise DocumentContractError(
            (
                _diagnostic(
                    "REGISTRY_ROUTE_AMBIGUOUS",
                    path=normalized,
                    expected="exactly one matching profile",
                    actual=", ".join(
                        f"{profile.profile_id}:{route.kind}:{route.value}"
                        for profile, route in matches
                    ),
                ),
            )
        )
    return matches[0][0]


def is_opaque_evaluation_output(registry: Registry, path: PurePosixPath) -> bool:
    """Select raw trial data by the current exact Stage 99 profile, not by suffix."""

    if path.suffix != ".md" or path.parts[:3] != (
        ".agents",
        "evaluations",
        "harnesses",
    ):
        return False
    profile = classify_path(registry, path)
    return profile.profile_id == "evaluation/raw-output" and profile.mode == "native"


def classify_paths(
    registry: Registry, paths: Sequence[PurePosixPath]
) -> tuple[Diagnostic, ...]:
    diagnostics: list[Diagnostic] = []
    for path in sorted(paths, key=lambda item: item.as_posix()):
        try:
            classify_path(registry, path)
        except DocumentContractError as exc:
            diagnostics.extend(exc.diagnostics)
    return tuple(diagnostics)
