"""Pure document lifecycle comparison over registry-selected snapshots."""

from __future__ import annotations

import copy
import re
from dataclasses import dataclass, field
from pathlib import PurePosixPath
from typing import Literal, Mapping, Sequence

import yaml

from document_authority import AuthorityError, require_reciprocal_supersession
from document_contracts import (
    DocumentProfile,
    task_status,
    Registry,
    classify_path,
    task_criterion_ids,
)


LifecycleSeverity = Literal["FAIL", "DEFER"]
LifecycleBaseMode = Literal[
    "staged", "ci", "explicit-ref", "snapshot", "completion", "unknown"
]


@dataclass(frozen=True)
class LifecycleDiagnostic:
    """Stable lifecycle failure/defer envelope shared by every base mode."""

    severity: LifecycleSeverity
    rule_id: str
    path: PurePosixPath
    profile: str
    expected_transition: str
    observed_transition: str
    base_mode: LifecycleBaseMode
    evidence_gap: str


@dataclass(frozen=True)
class LifecycleDocument:
    """One independently classified document in a base or proposed snapshot."""

    path: PurePosixPath
    profile_id: str
    status: str | None
    state_issue: str | None = None
    artifact_id: str | None = None


@dataclass(frozen=True)
class LifecycleRename:
    """One exact-blob Git rename detected before document classification."""

    old_path: PurePosixPath
    new_path: PurePosixPath


@dataclass(frozen=True)
class LifecycleEvidenceDocument:
    """One proposed-snapshot document and its canonical rendered evidence."""

    document: LifecycleDocument
    all_local_links: tuple[PurePosixPath, ...]
    relationship_links: tuple[PurePosixPath, ...]
    unresolved_relationship_links: tuple[PurePosixPath, ...]
    body_table_links: tuple[PurePosixPath, ...]
    relationship_section_valid: bool
    body_contract_valid: bool
    task_terminal_evidence_valid: bool
    body_rows: tuple[tuple[tuple[str, str], ...], ...] = ()
    task_evidence_rows: tuple[tuple[tuple[str, str], ...], ...] = ()
    task_disposition_valid: bool = True


@dataclass(frozen=True)
class LifecycleEvidenceContext:
    """Immutable inputs resolved from one Git base/proposed snapshot pair."""

    base_documents: Mapping[PurePosixPath, LifecycleDocument]
    proposed_documents: Mapping[PurePosixPath, LifecycleEvidenceDocument]
    changed_paths: frozenset[PurePosixPath]
    status_changed_paths: frozenset[PurePosixPath]
    body_changed_paths: frozenset[PurePosixPath]
    created_paths: frozenset[PurePosixPath]
    base_task_rows: Mapping[PurePosixPath, tuple[tuple[tuple[str, str], ...], ...]] = (
        field(default_factory=dict)
    )
    base_task_evidence_rows: Mapping[
        PurePosixPath, tuple[tuple[tuple[str, str], ...], ...]
    ] = field(default_factory=dict)
    local_contract_issues: tuple[tuple[PurePosixPath, str, str, str, str], ...] = ()


class _UniqueKeyLoader(yaml.SafeLoader):
    """Safe frontmatter loader that rejects duplicate mapping keys."""


_UniqueKeyLoader.yaml_implicit_resolvers = copy.deepcopy(
    yaml.SafeLoader.yaml_implicit_resolvers
)


def _construct_unique_mapping(
    loader: _UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[object, object]:
    mapping: dict[object, object] = {}
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


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def lifecycle_diagnostic_sort_key(
    diagnostic: LifecycleDiagnostic,
) -> tuple[str, str, str, str, str]:
    """Return a deterministic cross-mode lifecycle diagnostic key."""

    return (
        diagnostic.path.as_posix(),
        diagnostic.rule_id,
        diagnostic.profile,
        diagnostic.expected_transition,
        diagnostic.observed_transition,
    )


def _diagnostic(
    rule_id: str,
    *,
    path: PurePosixPath,
    profile: str,
    expected: str,
    observed: str,
    base_mode: LifecycleBaseMode,
    evidence_gap: str,
    severity: LifecycleSeverity = "FAIL",
) -> LifecycleDiagnostic:
    return LifecycleDiagnostic(
        severity=severity,
        rule_id=rule_id,
        path=path,
        profile=profile,
        expected_transition=expected,
        observed_transition=observed,
        base_mode=base_mode,
        evidence_gap=evidence_gap,
    )


def _profile_by_id(registry: Registry, profile_id: str) -> DocumentProfile:
    for profile in registry.profiles:
        if profile.profile_id == profile_id:
            return profile
    raise ValueError(f"unknown lifecycle profile: {profile_id}")


def _optional_profile_by_id(
    registry: Registry, profile_id: str
) -> DocumentProfile | None:
    try:
        return _profile_by_id(registry, profile_id)
    except ValueError:
        return None


def _stateful(profile: DocumentProfile) -> bool:
    """A profile participates in lifecycle validation only through its domain.

    A declared domain is the claim that the profile has states, so an authored
    mode is not required: naming one profile here exempted every other one that
    declares a graph and is not authored. A form carries an example value, not
    a document's state, so `mode: template` never transitions.
    """

    return profile.lifecycle_domain is not None and profile.mode != "template"


def _state_diagnostic(
    document: LifecycleDocument,
    profile: DocumentProfile,
    *,
    base_mode: LifecycleBaseMode,
    side: Literal["base", "proposed", "snapshot"],
) -> LifecycleDiagnostic | None:
    if not _stateful(profile):
        return None
    lifecycle_states = (
        tuple(state for state, _ in profile.lifecycle_domain.states)
        if profile.lifecycle_domain is not None
        else ()
    )
    allowed_states = lifecycle_states
    validation_class = (
        profile.lifecycle_domain.validation_class(document.status)
        if profile.lifecycle_domain is not None and document.status is not None
        else None
    )
    if document.state_issue is None and validation_class is not None:
        return None
    observed = (
        document.state_issue
        if document.state_issue is not None
        else f"{side} status {document.status!r}"
    )
    return _diagnostic(
        "LIFECYCLE-STATE",
        path=document.path,
        profile=document.profile_id,
        expected=f"{side} status in {allowed_states!r}",
        observed=observed,
        base_mode=base_mode,
        evidence_gap="valid registry-owned lifecycle state",
    )


def _create_diagnostics(
    registry: Registry,
    documents: Sequence[LifecycleDocument],
    *,
    base_mode: LifecycleBaseMode,
) -> list[LifecycleDiagnostic]:
    diagnostics: list[LifecycleDiagnostic] = []
    for document in documents:
        profile = _optional_profile_by_id(registry, document.profile_id)
        if profile is None:
            diagnostics.append(
                _diagnostic(
                    "LIFECYCLE-CREATE",
                    path=document.path,
                    profile=document.profile_id,
                    expected="one registry-classified admitted creation",
                    observed="absent -> unclassified target Markdown",
                    base_mode=base_mode,
                    evidence_gap="current registry route and creation admission",
                )
            )
            continue
        if not _stateful(profile):
            # A profile with no lifecycle domain declares no creation state, so
            # its appearance is not a lifecycle event.
            continue
        state_failure = _state_diagnostic(
            document, profile, base_mode=base_mode, side="proposed"
        )
        if state_failure is not None:
            diagnostics.append(state_failure)
            continue
        domain = profile.lifecycle_domain
        assert domain is not None  # `_stateful` admits only a declared domain.
        observed = f"absent -> {document.status or 'not-applicable'}"
        inbound = {target for _, target in domain.transitions}
        initial_states = domain.initial_states or tuple(
            state for state, _ in domain.states if state not in inbound
        )
        if document.status not in initial_states:
            diagnostics.append(
                _diagnostic(
                    "LIFECYCLE-CREATE",
                    path=document.path,
                    profile=document.profile_id,
                    expected=f"create in lifecycle initial state {initial_states!r}",
                    observed=observed,
                    base_mode=base_mode,
                    evidence_gap="profile lifecycle domain owns creation states",
                )
            )
    return diagnostics


SPECIFICATION_PROFILES = frozenset(
    {
        "sdlc/spec",
    }
)


def specification_relationship_profiles(registry: Registry) -> frozenset[str]:
    """Return the current Spec-package profiles."""

    registry_profile_ids = frozenset(
        profile.profile_id for profile in registry.profiles
    )
    current = SPECIFICATION_PROFILES & registry_profile_ids
    if "sdlc/spec" not in current:
        raise ValueError("registry lacks the canonical sdlc/spec relationship profile")
    return current


def requirement_relationship_profiles(registry: Registry) -> frozenset[str]:
    """Return the terminal Requirement owner."""

    registry_profile_ids = frozenset(
        profile.profile_id for profile in registry.profiles
    )
    current = frozenset({"sdlc/requirement"}) & registry_profile_ids
    if not current:
        raise ValueError("registry lacks the canonical Requirement Package profile")
    return current


def _reciprocal_links(
    path: PurePosixPath, context: LifecycleEvidenceContext
) -> tuple[PurePosixPath, ...]:
    """Return the linked documents that link back to ``path``."""

    view = context.proposed_documents.get(path)
    if view is None:
        return ()
    reciprocal = []
    for successor in view.relationship_links:
        successor_view = context.proposed_documents.get(successor)
        if successor_view is None:
            continue
        try:
            require_reciprocal_supersession(
                source=path.as_posix(),
                successor=successor.as_posix(),
                source_links={"superseded_by": successor.as_posix()},
                successor_links={
                    "supersedes": (
                        path.as_posix()
                        if path in successor_view.relationship_links
                        else ""
                    )
                },
            )
        except AuthorityError:
            continue
        reciprocal.append(successor)
    return tuple(reciprocal)


def _terminal_supersession_evidence(
    profile: DocumentProfile,
    target: LifecycleDocument,
    context: LifecycleEvidenceContext,
    *,
    base_mode: LifecycleBaseMode,
) -> tuple[LifecycleDiagnostic, ...]:
    """Enforce the domain-derived reciprocal rule using rendered links.

    Some reciprocal path must reach a document whose status is not the
    target's terminal status. Predecessors share that status, so they never
    satisfy the rule on their own, and a cycle of superseded documents fails.
    """

    domain = profile.lifecycle_domain
    if domain is None or not domain.requires_reciprocal_supersession:
        return ()
    visited = {target.path}
    pending = list(_reciprocal_links(target.path, context))
    observed = f"terminal supersession to {target.status}"
    while pending:
        candidate = pending.pop()
        if candidate in visited:
            continue
        visited.add(candidate)
        if context.proposed_documents[candidate].document.status != target.status:
            return ()
        pending.extend(_reciprocal_links(candidate, context))
        observed = "supersession chain ends without a current decision"
    return (
        _diagnostic(
            "LIFECYCLE-EVIDENCE",
            path=target.path,
            profile=target.profile_id,
            expected="one reciprocal supersedes/superseded_by relationship",
            observed=observed,
            base_mode=base_mode,
            evidence_gap="registry lifecycle domain requires reciprocal supersession",
        ),
    )


def artifact_identity_reuse_diagnostics(
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
    *,
    base_mode: LifecycleBaseMode,
) -> tuple[LifecycleDiagnostic, ...]:
    """Reject new owners of identities reserved by the base."""

    reserved: dict[str, set[PurePosixPath]] = {}
    for document in base_documents.values():
        if document.artifact_id is not None:
            reserved.setdefault(document.artifact_id, set()).add(document.path)
    diagnostics: list[LifecycleDiagnostic] = []
    for path, document in sorted(
        proposed_documents.items(), key=lambda item: item[0].as_posix()
    ):
        artifact_id = document.artifact_id
        if artifact_id is None:
            continue
        base = base_documents.get(path)
        if base is not None and base.artifact_id == artifact_id:
            continue
        if not reserved.get(artifact_id):
            continue
        diagnostics.append(
            _diagnostic(
                "LIFECYCLE-IDENTITY-REUSE",
                path=path,
                profile=document.profile_id,
                expected="new artifact identity absent from the comparison base",
                observed=f"{artifact_id!r} reserved at another document path",
                base_mode=base_mode,
                evidence_gap="base identity provenance",
            )
        )
    return tuple(diagnostics)


def _task_item_edge_diagnostics(
    profile: DocumentProfile,
    path: PurePosixPath,
    context: LifecycleEvidenceContext,
    *,
    base_mode: LifecycleBaseMode,
) -> tuple[LifecycleDiagnostic, ...]:
    """Keep each Task work ID's assignment and forward state across Git blobs."""

    if profile.profile_id != "sdlc/task" or profile.body_contract is None:
        return ()
    before_rows = context.base_task_rows.get(path)
    after_view = context.proposed_documents.get(path)
    if not before_rows or after_view is None:
        return ()  # An older generation may have no recognizable Task table.
    if not after_view.body_rows:
        return (
            _diagnostic(
                "TASK-ITEM-HIDE",
                path=path,
                profile="sdlc/task",
                expected="all base work IDs remain in the bound Task table",
                observed="proposed Task table missing or malformed",
                base_mode=base_mode,
                evidence_gap="base and proposed bound Task rows",
            ),
        )
    before = {dict(row)["ID"].strip().strip("`"): dict(row) for row in before_rows}
    after = {
        dict(row)["ID"].strip().strip("`"): dict(row) for row in after_view.body_rows
    }

    def criterion_ids(cell: str) -> tuple[str, ...] | None:
        linked = task_criterion_ids(cell)
        if linked is not None:
            return linked
        plain = tuple(part.strip() for part in cell.split(","))
        return (
            plain
            if all(re.fullmatch(r"VAL-[A-Z0-9-]+-[0-9]{3}", part) for part in plain)
            else None
        )

    def effective_status(row: Mapping[str, str], header: str | None) -> str:
        value = row["Status"].strip()
        return (header or "") if value == "frontmatter" else value

    issues: list[LifecycleDiagnostic] = []
    for work_id, old in before.items():
        new = after.get(work_id)
        rule = ""
        observed = ""
        old_criteria = criterion_ids(old["Upstream criterion"])
        new_criteria = (
            criterion_ids(new["Upstream criterion"]) if new is not None else None
        )
        if new is None:
            rule, observed = "TASK-ITEM-DELETE", f"{work_id} removed"
        elif old_criteria != new_criteria:
            rule, observed = "TASK-ITEM-HIDE", f"{work_id} upstream criterion changed"
        elif effective_status(
            old, context.base_documents[path].status
        ) != effective_status(new, after_view.document.status) and (
            profile.lifecycle_domain is None
            or not profile.lifecycle_domain.allows(
                effective_status(old, context.base_documents[path].status),
                effective_status(new, after_view.document.status),
            )
        ):
            rule, observed = (
                "TASK-ITEM-EDGE",
                f"{work_id}: {old['Status']} -> {new['Status']}",
            )
        elif old["Result"] not in {"NOT-RUN", "NOT_RUN"} and new["Result"] == "NOT_RUN":
            rule, observed = "TASK-ITEM-RESET", f"{work_id} result reset to NOT_RUN"
        if rule:
            issues.append(
                _diagnostic(
                    rule,
                    path=path,
                    profile="sdlc/task",
                    expected="preserved work ID, assignment, and forward item state",
                    observed=observed,
                    base_mode=base_mode,
                    evidence_gap="base and proposed bound Task rows",
                )
            )
    issues.extend(
        _task_evidence_retention_diagnostics(path, context, base_mode=base_mode)
    )
    return tuple(issues)


def _task_evidence_retention_diagnostics(
    path: PurePosixPath,
    context: LifecycleEvidenceContext,
    *,
    base_mode: LifecycleBaseMode,
) -> tuple[LifecycleDiagnostic, ...]:
    """Keep prior factual check rows immutable while allowing new resolution rows."""

    before = {
        dict(cells)["Evidence"].strip(): dict(cells)
        for cells in context.base_task_evidence_rows.get(path, ())
    }
    view = context.proposed_documents[path]
    after = {
        dict(cells)["Evidence"].strip(): dict(cells)
        for cells in view.task_evidence_rows
    }
    issues: list[LifecycleDiagnostic] = []
    for identifier, old in before.items():
        new = after.get(identifier)
        reason = ""
        if new is None:
            reason = f"{identifier} deleted"
        elif any(
            old.get(key, "").strip() != new.get(key, "").strip()
            for key in ("Work Unit", "Check", "Input", "Result", "Location")
        ):
            reason = f"{identifier} factual check changed"
        elif "Required" in old and any(
            old.get(key, "").strip() != new.get(key, "").strip()
            for key in ("Required", "Resolves")
        ):
            reason = f"{identifier} requirement or resolution edge changed"
        elif (
            "Required" not in old
            and old["Result"].strip() in {"FAIL", "DEFER", "NOT_RUN"}
            and new.get("Required", "").strip() != "yes"
        ):
            reason = f"{identifier} prior adverse check made optional"
        elif old.get("Criteria", "").strip() != new.get("Criteria", "").strip():
            reason = f"{identifier} criterion membership changed"
        if reason:
            issues.append(
                _diagnostic(
                    "TASK-EVIDENCE-RETENTION",
                    path=path,
                    profile="sdlc/task",
                    expected="prior EVD IDs and factual fields retained; new PASS rows append resolution",
                    observed=reason,
                    base_mode=base_mode,
                    evidence_gap="base and proposed Task Evidence rows",
                )
            )
    return tuple(issues)


def compare_lifecycle(
    registry: Registry,
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
    *,
    renames: Sequence[LifecycleRename] = (),
    base_mode: Literal["staged", "ci", "explicit-ref"],
    evidence_context: LifecycleEvidenceContext | None = None,
    enforce_task_execution: bool = False,
    base_registry: Registry | None = None,
) -> tuple[LifecycleDiagnostic, ...]:
    """Compare independently classified snapshots with fixed event precedence.

    Exact renames replace create/delete events. A same-path profile change
    replaces state/edge evaluation. Invalid state replaces edge evaluation.
    Evidence predicates are evaluated only when the adapter supplies an
    immutable base/proposed evidence context from the same Git comparison.
    """

    diagnostics: list[LifecycleDiagnostic] = []
    identity_base = (
        evidence_context.base_documents
        if evidence_context is not None
        else base_documents
    )
    identity_proposed = (
        {
            path: view.document
            for path, view in evidence_context.proposed_documents.items()
        }
        if evidence_context is not None
        else proposed_documents
    )
    diagnostics.extend(
        artifact_identity_reuse_diagnostics(
            identity_base,
            identity_proposed,
            base_mode=base_mode,
        )
    )
    consumed_base: set[PurePosixPath] = set()
    consumed_proposed: set[PurePosixPath] = set()

    for rename in sorted(
        renames, key=lambda item: (item.old_path.as_posix(), item.new_path.as_posix())
    ):
        base = base_documents.get(rename.old_path)
        proposed = proposed_documents.get(rename.new_path)
        if base is None or proposed is None:
            raise ValueError(
                "exact rename must name one base and one proposed document"
            )
        consumed_base.add(rename.old_path)
        consumed_proposed.add(rename.new_path)
        diagnostics.append(
            _diagnostic(
                "LIFECYCLE-RENAME",
                path=rename.new_path,
                profile=proposed.profile_id,
                expected="path unchanged",
                observed=(
                    f"{rename.old_path.as_posix()} -> {rename.new_path.as_posix()}"
                ),
                base_mode=base_mode,
                evidence_gap=(
                    "exact-blob rename admission is denied before profile selection"
                ),
            )
        )

    common_paths = (set(base_documents) - consumed_base) & (
        set(proposed_documents) - consumed_proposed
    )
    for path in sorted(common_paths, key=PurePosixPath.as_posix):
        base = base_documents[path]
        proposed = proposed_documents[path]
        base_profile = _optional_profile_by_id(
            base_registry or registry, base.profile_id
        )
        proposed_profile = _optional_profile_by_id(registry, proposed.profile_id)
        if base_profile is None or proposed_profile is None:
            diagnostics.append(
                _diagnostic(
                    "LIFECYCLE-STATE",
                    path=path,
                    profile=proposed.profile_id,
                    expected="one classified base and proposed lifecycle profile",
                    observed=(
                        f"{base.profile_id} -> {proposed.profile_id}; "
                        "current registry classification unavailable"
                    ),
                    base_mode=base_mode,
                    evidence_gap="registry-owned profile and state contract",
                )
            )
            continue
        if base.profile_id != proposed.profile_id:
            diagnostics.append(
                _diagnostic(
                    "LIFECYCLE-PROFILE-CHANGE",
                    path=path,
                    profile=proposed.profile_id,
                    expected=f"profile remains {base.profile_id}",
                    observed=f"{base.profile_id} -> {proposed.profile_id}",
                    base_mode=base_mode,
                    evidence_gap="registry profile classification is immutable",
                )
            )
            continue
        profile = proposed_profile
        base_state_failure = _state_diagnostic(
            base, base_profile, base_mode=base_mode, side="base"
        )
        proposed_state_failure = _state_diagnostic(
            proposed, profile, base_mode=base_mode, side="proposed"
        )
        if base_state_failure is not None or proposed_state_failure is not None:
            if base_state_failure is not None:
                diagnostics.append(base_state_failure)
            if proposed_state_failure is not None:
                diagnostics.append(proposed_state_failure)
            continue
        if enforce_task_execution and evidence_context is not None:
            diagnostics.extend(
                _task_item_edge_diagnostics(
                    profile, path, evidence_context, base_mode=base_mode
                )
            )
        if base.status == proposed.status or not _stateful(profile):
            continue
        allowed_edges = (
            set(profile.lifecycle_domain.transitions)
            if profile.lifecycle_domain is not None
            else set()
        )
        if (base.status, proposed.status) not in allowed_edges:
            diagnostics.append(
                _diagnostic(
                    "LIFECYCLE-EDGE",
                    path=path,
                    profile=proposed.profile_id,
                    expected=f"one declared edge in {sorted(allowed_edges)!r}",
                    observed=f"{base.status} -> {proposed.status}",
                    base_mode=base_mode,
                    evidence_gap="declared forward lifecycle edge",
                )
            )
        elif (
            evidence_context is not None
            and proposed.status == "superseded"
            and (base.status, proposed.status) in allowed_edges
        ):
            diagnostics.extend(
                _terminal_supersession_evidence(
                    profile,
                    proposed,
                    evidence_context,
                    base_mode=base_mode,
                )
            )
        if (
            evidence_context is not None
            and proposed.profile_id == "sdlc/task"
            and proposed.status == "cancelled"
            and not evidence_context.proposed_documents[path].task_disposition_valid
        ):
            diagnostics.append(
                _diagnostic(
                    "TASK-DISPOSITION",
                    path=path,
                    profile="sdlc/task",
                    expected="current Plan successor assignment or authorized Spec scope disposition",
                    observed=f"{base.status} -> {proposed.status}",
                    base_mode=base_mode,
                    evidence_gap="terminal Task obligation has no proved successor or scope basis",
                )
            )

    created_paths = set(proposed_documents) - consumed_proposed - common_paths
    created = [
        proposed_documents[path]
        for path in sorted(created_paths, key=PurePosixPath.as_posix)
    ]
    diagnostics.extend(_create_diagnostics(registry, created, base_mode=base_mode))

    if enforce_task_execution and evidence_context is not None:
        diagnostics.extend(
            local_contract_diagnostics(evidence_context, base_mode=base_mode)
        )

    return tuple(sorted(diagnostics, key=lifecycle_diagnostic_sort_key))


LOCAL_CONTRACT_EVIDENCE_GAP = "current same-package Plan and Spec authority"


def local_contract_diagnostics(
    context: LifecycleEvidenceContext, *, base_mode: LifecycleBaseMode
) -> tuple[LifecycleDiagnostic, ...]:
    """Render actual changed local Plan and Task authority issues."""

    return tuple(
        _diagnostic(
            rule,
            path=path,
            profile=profile,
            expected=expected,
            observed=observed,
            base_mode=base_mode,
            evidence_gap=LOCAL_CONTRACT_EVIDENCE_GAP,
        )
        for path, profile, rule, expected, observed in context.local_contract_issues
    )


def validate_current_task_evidence(
    context: LifecycleEvidenceContext,
    *,
    base_mode: LifecycleBaseMode,
) -> tuple[LifecycleDiagnostic, ...]:
    """Reject invalid terminal Tasks, including unchanged current documents."""

    completed = tuple(
        _diagnostic(
            "TASK-TERMINAL-EVIDENCE",
            path=path,
            profile="sdlc/task",
            expected="every completed Task row has PASS and concrete evidence",
            observed="current completed Task table is missing or invalid",
            base_mode=base_mode,
            evidence_gap="parsed current Task Table evidence",
        )
        for path, view in sorted(context.proposed_documents.items())
        if path.parts[:2] == ("docs", "03.specs")
        and view.document.profile_id == "sdlc/task"
        and view.document.status == "completed"
        and not view.task_terminal_evidence_valid
    )
    disposition = tuple(
        _diagnostic(
            "TASK-DISPOSITION",
            path=path,
            profile="sdlc/task",
            expected="current Plan successor or authorized Spec cancellation basis",
            observed=f"unchanged/current {view.document.status} without a valid obligation handoff",
            base_mode=base_mode,
            evidence_gap="current Plan and reciprocal successor or Spec scope authorization",
        )
        for path, view in sorted(context.proposed_documents.items())
        if path.parts[:2] == ("docs", "03.specs")
        and view.document.profile_id == "sdlc/task"
        and view.document.status == "cancelled"
        and not view.task_disposition_valid
    )
    return completed + disposition


def validate_snapshot_documents(
    registry: Registry,
    documents: Sequence[LifecycleDocument],
) -> tuple[LifecycleDiagnostic, ...]:
    """Validate current profile states without claiming transition history."""

    diagnostics: list[LifecycleDiagnostic] = []
    for document in documents:
        profile = _optional_profile_by_id(registry, document.profile_id)
        if profile is None:
            diagnostics.append(
                _diagnostic(
                    "LIFECYCLE-STATE",
                    path=document.path,
                    profile=document.profile_id,
                    expected="one current registry lifecycle profile",
                    observed="unclassified snapshot document",
                    base_mode="snapshot",
                    evidence_gap="registry-owned profile and state contract",
                )
            )
            continue
        state_failure = _state_diagnostic(
            document, profile, base_mode="snapshot", side="snapshot"
        )
        if state_failure is not None:
            diagnostics.append(state_failure)
    diagnostics.append(
        _diagnostic(
            "LIFECYCLE-BASE-DEFER",
            path=PurePosixPath("."),
            profile="",
            expected="base-to-proposed transition history",
            observed="snapshot mode has no comparison base",
            base_mode="snapshot",
            evidence_gap="transition history unavailable",
            severity="DEFER",
        )
    )
    return tuple(sorted(diagnostics, key=lifecycle_diagnostic_sort_key))


def document_from_text(
    registry: Registry,
    path: PurePosixPath,
    text: str,
) -> LifecycleDocument:
    """Classify one document and extract only its registry-owned status."""

    selected_profile = classify_path(registry, path)
    if not _stateful(selected_profile):
        return LifecycleDocument(
            path=path, profile_id=selected_profile.profile_id, status=None
        )
    if not text.startswith("---\n"):
        return LifecycleDocument(
            path=path,
            profile_id=selected_profile.profile_id,
            status=None,
            state_issue="missing leading YAML frontmatter",
        )
    closing = text.find("\n---\n", 4)
    if closing < 0:
        return LifecycleDocument(
            path=path,
            profile_id=selected_profile.profile_id,
            status=None,
            state_issue="unterminated YAML frontmatter",
        )
    try:
        metadata = yaml.load(text[4:closing], Loader=_UniqueKeyLoader)
    except yaml.YAMLError:
        metadata = None
    if not isinstance(metadata, dict):
        return LifecycleDocument(
            path=path,
            profile_id=selected_profile.profile_id,
            status=None,
            state_issue="frontmatter is not a unique-key mapping",
        )
    if selected_profile.profile_id == "common/native-skill-package":
        nested = metadata.get("metadata")
        metadata = nested if isinstance(nested, dict) else {}
    claimed_profile_id = metadata.get("type")
    known_profile_ids = {profile.profile_id for profile in registry.profiles}
    expected_type = (
        "governance/skill"
        if selected_profile.profile_id == "common/native-skill-package"
        else dict(selected_profile.constants).get("type", selected_profile.profile_id)
    )
    profile_id = selected_profile.profile_id
    profile_issue: str | None = None
    if not isinstance(claimed_profile_id, str):
        profile_issue = "frontmatter type is missing or not a string"
    elif claimed_profile_id == expected_type:
        pass
    elif claimed_profile_id in known_profile_ids:
        profile_id = claimed_profile_id
        profile_issue = (
            f"frontmatter type {profile_id!r} differs from route type {expected_type!r}"
        )
    else:
        profile_issue = f"frontmatter type is unknown: {claimed_profile_id!r}"
    status = metadata.get("status")
    if status is None:
        status = task_status(metadata, text, selected_profile) or None
    if not isinstance(status, str):
        return LifecycleDocument(
            path=path,
            profile_id=profile_id,
            status=None,
            state_issue="frontmatter status is missing or not a string",
        )
    artifact_id = metadata.get("artifact_id")
    if not isinstance(artifact_id, str):
        artifact_id = None
    return LifecycleDocument(
        path=path,
        profile_id=profile_id,
        status=status,
        state_issue=profile_issue,
        artifact_id=artifact_id,
    )
