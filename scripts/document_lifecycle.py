"""Pure document lifecycle comparison over registry-selected snapshots."""

from __future__ import annotations

import functools
import re
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Literal, Mapping, Sequence

from document_authority import (
    AuthorityError,
    REGISTRY_PATH,
    require_reciprocal_supersession,
)
from frontmatter_yaml import FrontmatterError, load_frontmatter
from document_contracts import (
    DocumentContractError,
    DocumentProfile,
    LifecycleDomain,
    SCOPED_EXECUTION_APPROVAL_COMMAND,
    SPEC_PLAN_FIRST_APPROVED_EXTENSION,
    UNRESOLVED_EVIDENCE_RESULTS,
    task_status,
    Registry,
    classify_path,
    load_json_file,
    local_extension_names,
    registry_schema_version,
    task_criterion_ids,
    is_criterion_id,
)
from common_document_contract import (
    CommonDocumentError,
    has_common_envelope,
    payload_markdown,
)
from semver_grammar import numeric_version_order


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
    version: str | None = None


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
    # SPEC-0193: the artifact identifiers named by the `supersedes` and
    # `superseded_by` frontmatter keys, read for the whole-tree supersession walk.
    supersedes_ids: tuple[str, ...] = ()
    superseded_by_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class PolicyCodeSection:
    """The `policy_rule_ids` codes of one registry snapshot, read as plain JSON."""

    codes: Mapping[str, str]  # code -> path of its first record
    reserved: frozenset[str]
    # path -> code of every record; a code split by SDLC-R036 has two paths.
    paths: Mapping[str, str] = field(default_factory=dict)
    # SPEC-0225 (Q07-H01): the declared rule ID baseline; a section without the
    # key is baseline 1. Codes and rule IDs are kept only within one baseline.
    baseline: int = 1


@dataclass(frozen=True)
class LifecycleEvidenceContext:
    """Immutable inputs resolved from one Git base/proposed snapshot pair."""

    base_documents: Mapping[PurePosixPath, LifecycleDocument]
    proposed_documents: Mapping[PurePosixPath, LifecycleEvidenceDocument]
    changed_paths: frozenset[PurePosixPath]
    status_changed_paths: frozenset[PurePosixPath]
    body_changed_paths: frozenset[PurePosixPath]
    created_paths: frozenset[PurePosixPath]
    approved_initial_paths: frozenset[PurePosixPath] = frozenset()
    base_task_rows: Mapping[PurePosixPath, tuple[tuple[tuple[str, str], ...], ...]] = (
        field(default_factory=dict)
    )
    base_task_evidence_rows: Mapping[
        PurePosixPath, tuple[tuple[tuple[str, str], ...], ...]
    ] = field(default_factory=dict)
    local_contract_issues: tuple[tuple[PurePosixPath, str, str, str, str], ...] = ()
    retired_identities: Mapping[str, PurePosixPath] = field(default_factory=dict)
    # SPEC-0206: rule ID -> (path, Status) of every Rules table at each snapshot,
    # and the code section of each registry; `None` is a registry without one.
    base_policy_rules: Mapping[str, tuple[PurePosixPath, str]] = field(
        default_factory=dict
    )
    proposed_policy_rules: Mapping[str, tuple[PurePosixPath, str]] = field(
        default_factory=dict
    )
    base_policy_section: PolicyCodeSection | None = None
    proposed_policy_section: PolicyCodeSection | None = None


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


def creation_states(domain: LifecycleDomain) -> tuple[str, ...]:
    """Return the states a document may be created in under one lifecycle domain.

    A domain declares them in `initial_states`; otherwise they are the states with
    no inbound transition, and a domain whose every state has one yields none.
    """

    inbound = {target for _, target in domain.transitions}
    return domain.initial_states or tuple(
        state for state, _ in domain.states if state not in inbound
    )


def _create_diagnostics(
    registry: Registry,
    documents: Sequence[LifecycleDocument],
    *,
    base_mode: LifecycleBaseMode,
    approved_initial_paths: frozenset[PurePosixPath] = frozenset(),
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
        initial_states = creation_states(domain)
        if document.status not in initial_states and not (
            document.profile_id in {"sdlc/spec", "sdlc/plan"}
            and document.status == "approved"
            and document.path in approved_initial_paths
        ):
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
    if (
        domain is None
        or not domain.requires_reciprocal_supersession
        or _successor_owned_operation(profile)
    ):
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


def _successor_owned_operation(profile: DocumentProfile) -> bool:
    return (
        profile.profile_id.startswith("operation/")
        and "supersedes" in profile.frontmatter.allowed
        and "superseded_by" not in profile.frontmatter.allowed
    )


def operating_supersession_diagnostics(
    registry: Registry,
    documents: Mapping[PurePosixPath, LifecycleEvidenceDocument],
    *,
    base_mode: LifecycleBaseMode,
) -> tuple[LifecycleDiagnostic, ...]:
    """Resolve current operating successors by artifact ID, including after a move."""

    profiles = {
        p.profile_id for p in registry.profiles if _successor_owned_operation(p)
    }
    if not profiles:
        return ()
    indexed = {
        view.document.artifact_id: view.document
        for view in documents.values()
        if view.document.artifact_id is not None
    }
    incoming: dict[str, list[LifecycleDocument]] = {}
    issues: list[LifecycleDiagnostic] = []

    def fail(document: LifecycleDocument, expected: str, observed: str) -> None:
        issues.append(
            _diagnostic(
                "LIFECYCLE-EVIDENCE",
                path=document.path,
                profile=document.profile_id,
                expected=expected,
                observed=observed,
                base_mode=base_mode,
                evidence_gap="successor-authored operating supersession by artifact ID",
            )
        )

    for view in documents.values():
        document = view.document
        if document.profile_id not in profiles:
            continue
        if view.superseded_by_ids:
            fail(
                document,
                "supersedes written only by the successor",
                "predecessor carries superseded_by",
            )
        for identity in view.supersedes_ids:
            predecessor = indexed.get(identity)
            if predecessor is None:
                continue  # A retained identifier may name an archived predecessor.
            if (
                predecessor.profile_id != document.profile_id
                or predecessor.path == document.path
            ):
                fail(
                    document,
                    "a distinct predecessor of the same operating profile",
                    identity,
                )
            else:
                incoming.setdefault(identity, []).append(document)

    for document in indexed.values():
        if document.profile_id not in profiles or document.status != "superseded":
            continue
        pending = list(incoming.get(document.artifact_id or "", ()))
        visited = {document.path}
        while pending:
            successor = pending.pop()
            if successor.path in visited or successor.state_issue is not None:
                continue
            if successor.status == "active":
                break
            visited.add(successor.path)
            if successor.status == "superseded":
                pending.extend(incoming.get(successor.artifact_id or "", ()))
        else:
            fail(
                document,
                "an active successor reachable through same-profile supersedes IDs",
                "no active operating successor",
            )
    return tuple(issues)


def supersession_cycle_diagnostics(
    documents: Mapping[PurePosixPath, LifecycleEvidenceDocument],
    *,
    base_mode: LifecycleBaseMode,
) -> tuple[LifecycleDiagnostic, ...]:
    """SPEC-0193: refuse a document that is reachable from itself.

    `supersedes` and `superseded_by` form one successor graph over the whole
    proposed tree, so a lifecycle domain without a superseded state is covered
    too. An edge runs from a predecessor to its successor: a document that names
    a predecessor in `supersedes` is its successor, and one that names a
    successor in `superseded_by` is its predecessor, so a reciprocal pair is one
    edge and never a loop. The walk starts from every document and never counts
    its start as visited, so a self-reference is found.
    """

    successors: dict[str, set[str]] = {}
    for view in documents.values():
        identity = view.document.artifact_id
        if identity is None:
            continue
        for predecessor in view.supersedes_ids:
            successors.setdefault(predecessor, set()).add(identity)
        for successor in view.superseded_by_ids:
            successors.setdefault(identity, set()).add(successor)
    diagnostics: list[LifecycleDiagnostic] = []
    for path, view in sorted(documents.items()):
        identity = view.document.artifact_id
        if identity is None or identity not in successors:
            continue
        visited: set[str] = set()
        pending = list(successors[identity])
        while pending:
            node = pending.pop()
            if node == identity:
                diagnostics.append(
                    _diagnostic(
                        "LIFECYCLE-EVIDENCE",
                        path=path,
                        profile=view.document.profile_id,
                        expected="no document reachable from itself over "
                        "supersedes and superseded_by",
                        observed="supersession cycle",
                        base_mode=base_mode,
                        evidence_gap="whole-tree supersession walk",
                    )
                )
                break
            if node not in visited:
                visited.add(node)
                pending.extend(successors.get(node, ()))
    return tuple(diagnostics)


def artifact_identity_reuse_diagnostics(
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
    *,
    base_mode: LifecycleBaseMode,
    retired: Mapping[str, PurePosixPath] | None = None,
) -> tuple[LifecycleDiagnostic, ...]:
    """Reject new owners of identities reserved by the base or a lineage."""

    retired = retired or {}
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
        lineage = next(
            (
                identity
                for identity in sorted(retired)
                if artifact_id == identity or artifact_id.startswith(identity + "-")
            ),
            None,
        )
        if not reserved.get(artifact_id) and lineage is None:
            continue
        diagnostics.append(
            _diagnostic(
                "LIFECYCLE-IDENTITY-REUSE",
                path=path,
                profile=document.profile_id,
                expected="new artifact identity absent from the comparison base",
                observed=(
                    f"{artifact_id!r} reserved at another document path"
                    if lineage is None
                    else f"{artifact_id!r} reserved by retired identity "
                    f"{lineage!r} in the Archived Lineage of "
                    f"{retired[lineage].as_posix()}"
                ),
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
    before = {dict(row)["Item"].strip().strip("`"): dict(row) for row in before_rows}
    after = {
        dict(row)["Item"].strip().strip("`"): dict(row) for row in after_view.body_rows
    }

    def criterion_ids(cell: str) -> tuple[str, ...] | None:
        linked = task_criterion_ids(cell)
        if linked is not None:
            return linked
        plain = tuple(part.strip() for part in cell.split(","))
        return plain if all(is_criterion_id(part) for part in plain) else None

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


# Same pattern as the repository quality gate's local checkout path rule.
_LOCAL_CHECKOUT_PATH = re.compile(
    r"(?<![\w:/])/(?:[^\s`'\"()]+/)?hy-home\.k8s(?![\w.-])"
)


def _redacted(old: str, new: str) -> bool:
    """A recorded cell may only swap each local checkout path for `<checkout>`."""
    return bool(_LOCAL_CHECKOUT_PATH.search(old)) and (
        _LOCAL_CHECKOUT_PATH.sub("<checkout>", old) == new
    )


def _task_evidence_retention_diagnostics(
    path: PurePosixPath,
    context: LifecycleEvidenceContext,
    *,
    base_mode: LifecycleBaseMode,
) -> tuple[LifecycleDiagnostic, ...]:
    """Keep prior factual check rows immutable while allowing new resolution rows."""

    before = {
        dict(cells)["Evidence ID"].strip(): dict(cells)
        for cells in context.base_task_evidence_rows.get(path, ())
    }
    view = context.proposed_documents[path]
    after = {
        dict(cells)["Evidence ID"].strip(): dict(cells)
        for cells in view.task_evidence_rows
    }
    issues: list[LifecycleDiagnostic] = []
    prior_approvals = tuple(
        key
        for key, row in before.items()
        if row.get("Command") == SCOPED_EXECUTION_APPROVAL_COMMAND
    )
    approvals = tuple(
        key
        for key, row in after.items()
        if row.get("Command") == SCOPED_EXECUTION_APPROVAL_COMMAND
    )
    if approvals[: len(prior_approvals)] != prior_approvals:
        issues.append(
            _diagnostic(
                "TASK-EVIDENCE-RETENTION",
                path=path,
                profile="sdlc/task",
                expected="existing scoped execution approval rows followed by any new records",
                observed="scoped approval history removed, reordered or inserted before a retained record",
                base_mode=base_mode,
                evidence_gap="ordered authority and withdrawal records",
            )
        )
    for identifier, old in before.items():
        new = after.get(identifier)
        reason = ""
        missing = (
            ()
            if new is None
            else tuple(
                key
                for key in ("Criteria", "Work Unit", "Command", "Input", "Result")
                if key not in old or key not in new
            )
        )
        if new is None:
            reason = f"{identifier} deleted"
        elif missing:
            # A column a rule reads is an error when absent, never an empty value.
            reason = f"{identifier} lacks the column {missing[0]}"
        elif any(
            old.get(key, "").strip() != new.get(key, "").strip()
            and not _redacted(old.get(key, "").strip(), new.get(key, "").strip())
            for key in (
                "Work Unit",
                "Method",
                "Tool and Config",
                "Command",
                "Exit",
                "Input",
                "Result",
                "Location",
            )
        ):
            reason = f"{identifier} factual check changed"
        elif "Required" in old and any(
            old.get(key, "").strip() != new.get(key, "").strip()
            for key in ("Required", "Resolves")
        ):
            reason = f"{identifier} requirement or resolution edge changed"
        elif (
            "Required" not in old
            and old["Result"].strip() in UNRESOLVED_EVIDENCE_RESULTS
            and new.get("Required", "").strip() != "true"
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
                    evidence_gap="base and proposed Task evidence rows",
                )
            )
    return tuple(issues)


def version_change_diagnostic(
    path: PurePosixPath,
    profile: str,
    field: str,
    base: object,
    proposed: object,
    *,
    base_mode: LifecycleBaseMode,
) -> LifecycleDiagnostic | None:
    """Enforce numeric order and reset rules on structurally valid versions."""

    before, after = numeric_version_order(base), numeric_version_order(proposed)
    if before is None or after is None or after == before:
        return None
    if after < before:
        rule = "LIFECYCLE-VERSION-DOWNGRADE"
        expected = f"{field} not lower than {base}"
    # Only the staged comparison observes one proposed change. A ref-to-ref
    # comparison can span valid major, minor and patch changes.
    elif base_mode == "staged" and (
        (after[0] > before[0] and any(after[1:]))
        or (after[:2] > before[:2] and after[2] != 0)
    ):
        rule = "LIFECYCLE-VERSION-RESET"
        expected = f"{field} resets components below the highest increase to zero"
    else:
        return None
    return _diagnostic(
        rule,
        path=path,
        profile=profile,
        expected=expected,
        observed=f"{base} -> {proposed}",
        base_mode=base_mode,
        evidence_gap="compare three numeric components and reset lower components",
    )


_RELEASED_STAGES = frozenset({"approved", "adopted"})
_EDITION_FIELDS = ("content_digest", "source_revision", "source")


def _registry_schema_release(raw: Mapping[str, object]) -> str | None:
    try:
        return registry_schema_version(raw)
    except DocumentContractError:  # reported by the registry loader, not compared
        return None


def registry_version_diagnostics(
    base: Mapping[str, object],
    proposed: Mapping[str, object],
    *,
    base_mode: LifecycleBaseMode,
) -> tuple[LifecycleDiagnostic, ...]:
    """Compare the scalar version fields of two raw Stage 99 registry mappings.

    Read the relevant editions without validating historical Registry schemas.
    """

    path = REGISTRY_PATH
    base_schema = _registry_schema_release(base)
    found: list[LifecycleDiagnostic | None] = [
        version_change_diagnostic(
            path,
            "",
            "schema_version",
            base_schema,
            _registry_schema_release(proposed),
            base_mode=base_mode,
        )
    ]
    sections = {
        name: (base.get(name), proposed.get(name))
        for name in ("shared_contract", "common_forms")
    }
    for name, (before, after) in sections.items():
        if (
            not isinstance(before, Mapping)
            or not isinstance(after, Mapping)
            or before.get("contract_id") != after.get("contract_id")
        ):
            continue
        found.append(
            version_change_diagnostic(
                path,
                "",
                f"{name}.version",
                before.get("version"),
                after.get("version"),
                base_mode=base_mode,
            )
        )
        if (
            before.get("stage") in _RELEASED_STAGES
            and type(before.get("version")) is str
            and before.get("version") == after.get("version")
        ):
            fields = (
                (*_EDITION_FIELDS, "forms")
                if name == "common_forms"
                else _EDITION_FIELDS
            )
            changed = [
                field for field in fields if before.get(field) != after.get(field)
            ]
            if changed:
                found.append(
                    _diagnostic(
                        "LIFECYCLE-VERSION-EDITION-CHANGED",
                        path=path,
                        profile="",
                        expected=f"released {name} {before['version']} keeps {', '.join(fields)}",
                        observed=f"{', '.join(changed)} changed under the same version",
                        base_mode=base_mode,
                        evidence_gap="a released edition never changes; raise the version",
                    )
                )

    def definitions(snapshot: Mapping[str, object]) -> dict[str, Mapping]:
        profiles = snapshot.get("profiles")
        if not isinstance(profiles, list):
            return {}
        return {
            profile["id"]: profile["template_definition"]
            for profile in profiles
            if isinstance(profile, Mapping)
            and isinstance(profile.get("id"), str)
            and isinstance(profile.get("template_definition"), Mapping)
        }

    old_definitions = definitions(base)
    base_order = numeric_version_order(base_schema)
    for profile_id, after in definitions(proposed).items():
        before = old_definitions.get(profile_id)
        if before is None:
            continue
        contract_id, version = before.get("contract_id"), before.get("contract_version")
        # Generation 21 split the combined binding on the current wire format.
        if (
            "contract_id" not in before
            and base_order is not None
            and base_order[0] < 21
            and isinstance(version, str)
        ):
            contract_id, _, version = version.partition("/")
        if isinstance(contract_id, str) and contract_id == after.get("contract_id"):
            found.append(
                version_change_diagnostic(
                    path,
                    profile_id,
                    "TemplateDefinition.contract_version",
                    version,
                    after.get("contract_version"),
                    base_mode=base_mode,
                )
            )

    return tuple(item for item in found if item is not None)


def policy_history_diagnostics(
    context: LifecycleEvidenceContext, *, base_mode: LifecycleBaseMode
) -> tuple[LifecycleDiagnostic, ...]:
    """SPEC-0206: a rule ID never leaves its table or returns from `retired`, and
    a registered code never changes, across the base and the proposal.

    A base registry without the code section has no record to keep, so no rule.
    """

    base = context.base_policy_section
    if base is None:
        return ()
    proposed = context.proposed_policy_section or PolicyCodeSection({}, frozenset())
    if proposed.baseline != base.baseline:
        # SPEC-0225 (Q07-H01): a change that declares a new baseline is the
        # user-approved reset DOCLIFE-R022 names; it may drop reserved codes and
        # reissue rule IDs. Within one baseline every refusal below holds.
        return ()
    found: list[LifecycleDiagnostic] = []

    def refuse(rule: str, path: PurePosixPath, expected: str, observed: str) -> None:
        found.append(
            _diagnostic(
                rule,
                path=path,
                profile="",
                expected=expected,
                observed=observed,
                base_mode=base_mode,
                evidence_gap="base and proposed policy Rules tables and code section",
            )
        )

    for rule_id, (path, status) in sorted(context.base_policy_rules.items()):
        code = rule_id.rsplit("-R", 1)[0]
        kept = context.proposed_policy_rules.get(rule_id)
        if kept is None:
            if code in proposed.reserved and code not in proposed.codes:
                continue  # the policy left the tree and its code is reserved
            refuse(
                "POLICY-RULE-DELETE",
                path,
                f"{rule_id} stays in a Rules table",
                f"{rule_id} removed",
            )
        elif status.startswith("retired") and not kept[1].startswith("retired"):
            refuse(
                "POLICY-RULE-REISSUE",
                kept[0],
                f"{rule_id} stays retired",
                f"{rule_id}: {status} -> {kept[1]}",
            )
    by_path = dict(proposed.paths) or {
        path: code for code, path in proposed.codes.items()
    }
    for code, path in sorted(base.codes.items()):
        if code not in proposed.codes and code not in proposed.reserved:
            observed = f"{code} ({path}) neither registered nor reserved"
        elif by_path.get(path, code) != code:
            observed = f"{path}: {code} -> {by_path[path]}"
        else:
            continue
        refuse(
            "POLICY-CODE-CHANGE",
            REGISTRY_PATH,
            "every registered code is kept or reserved and never changes",
            observed,
        )
    for code in sorted(base.reserved - proposed.reserved):
        refuse(
            "POLICY-CODE-CHANGE",
            REGISTRY_PATH,
            "the reserved codes never shrink",
            f"{code} left reserved_codes",
        )
    return tuple(found)


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
            retired=(
                evidence_context.retired_identities
                if evidence_context is not None
                else frozenset()
            ),
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
        version_failure = version_change_diagnostic(
            path,
            proposed.profile_id,
            "document version",
            base.version,
            proposed.version,
            base_mode=base_mode,
        )
        if version_failure is not None:
            diagnostics.append(version_failure)
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
            if (
                base_mode == "staged"
                and proposed.profile_id in {"sdlc/spec", "sdlc/plan"}
                and base.status == proposed.status == "approved"
                and path in evidence_context.body_changed_paths
            ):
                diagnostics.append(
                    _diagnostic(
                        "LIFECYCLE-APPROVAL-STALE",
                        path=path,
                        profile=proposed.profile_id,
                        expected="revised approved contract returns to in-review",
                        observed="approved contract body changed under its existing approval state",
                        base_mode=base_mode,
                        evidence_gap="review of revised contract bytes",
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
    approved_initial_paths = frozenset()
    if (
        evidence_context is not None
        and SPEC_PLAN_FIRST_APPROVED_EXTENSION
        in local_extension_names(registry.shared_contract)
    ):
        approved_initial_paths = (
            evidence_context.approved_initial_paths
            & evidence_context.created_paths
            & frozenset(created_paths)
        )
    diagnostics.extend(
        _create_diagnostics(
            registry,
            created,
            base_mode=base_mode,
            approved_initial_paths=approved_initial_paths,
        )
    )

    if enforce_task_execution and evidence_context is not None:
        diagnostics.extend(
            local_contract_diagnostics(evidence_context, base_mode=base_mode)
        )
        diagnostics.extend(
            policy_history_diagnostics(evidence_context, base_mode=base_mode)
        )

    if evidence_context is not None:
        diagnostics.extend(
            operating_supersession_diagnostics(
                registry, evidence_context.proposed_documents, base_mode=base_mode
            )
        )
        diagnostics.extend(
            supersession_cycle_diagnostics(
                evidence_context.proposed_documents, base_mode=base_mode
            )
        )

    return tuple(sorted(diagnostics, key=lifecycle_diagnostic_sort_key))


LOCAL_CONTRACT_EVIDENCE_GAP = "current same-package Plan and Spec authority"


_PACKAGE_DIR = re.compile(r"[0-9]{4}-[a-z][a-z0-9]*(?:-[a-z0-9]+)*")
_TERMINAL_TASK_STATES = frozenset({"completed", "cancelled"})
# Level 5 is where the common envelope places a Requirement's lineage.
_LINEAGE_HEADING = re.compile(r"^(#{2,5}) Archived Lineage[ \t]*$", re.MULTILINE)


def _archived_lineage_text(text: str) -> str:
    """Return the body of each level-2 to level-5 `Archived Lineage` section."""

    sections = []
    for match in _LINEAGE_HEADING.finditer(text):
        level = len(match.group(1))
        end = re.compile(rf"^#{{1,{level}}} ", re.MULTILINE).search(text, match.end())
        sections.append(text[match.end() : end.start() if end else len(text)])
    return "\n".join(sections)


_HISTORICAL_IDENTITY = ("OPS-[0-9]{4}", "MIG-[0-9]{4}")
_SCHEMA_PATH = Path(__file__).resolve().parents[1] / (
    "docs/99.templates/01.contracts/frontmatter.schema.json"
)
_TABLE_SEPARATOR = re.compile(r"\s*:?-+:?\s*")


@functools.lru_cache(maxsize=1)
def _identity_branches() -> tuple[re.Pattern[str], ...]:
    """Top-level alternatives of `terminalArtifactId` plus historical prefixes."""

    pattern = load_json_file(_SCHEMA_PATH)["$defs"]["terminalArtifactId"]["pattern"]
    body = pattern.removeprefix("^(?:").removesuffix(")$")
    branches, depth, start = [], 0, 0
    for index, character in enumerate(body):
        depth += (character == "(") - (character == ")")
        if character == "|" and depth == 0:
            branches.append(body[start:index])
            start = index + 1
    branches.append(body[start:])
    return tuple(re.compile(item) for item in (*branches, *_HISTORICAL_IDENTITY))


def _table_cells(row: str) -> list[str]:
    cells = re.split(r"(?<!\\)\|", row.strip().removeprefix("|"))
    if not cells[-1].strip():
        cells.pop()
    return [cell.strip() for cell in cells]


def _identity_tokens(cell: str) -> list[str]:
    """Longest identity at each position not glued to a letter, digit or `-`."""

    tokens, position = [], 0
    while position < len(cell):
        if position and re.match(r"[A-Za-z0-9-]", cell[position - 1]):
            position += 1
            continue
        matches = [
            match.group(0)
            for branch in _identity_branches()
            if (match := branch.match(cell, position))
        ]
        longest = max(matches, key=len, default="")
        end = position + len(longest)
        if longest and not re.match(r"[A-Za-z0-9]", cell[end : end + 1]):
            tokens.append(longest)
            position = end
        else:
            position += 1
    return tokens


def lineage_retired_identities(
    texts: Mapping[PurePosixPath, str],
) -> dict[str, PurePosixPath]:
    """Identity tokens in the first cell of each `Archived Lineage` data row.

    Each token maps to the first document, in path order, whose lineage names it.
    """

    retired: dict[str, PurePosixPath] = {}
    for path, text in sorted(texts.items(), key=lambda item: item[0].as_posix()):
        if "Archived Lineage" not in text:
            continue
        rows = [
            line
            for line in _archived_lineage_text(text).splitlines()
            if line.lstrip().startswith("|")
        ]
        for index, row in enumerate(rows):
            cells = _table_cells(row)
            following = _table_cells(rows[index + 1]) if index + 1 < len(rows) else []
            if (
                not cells
                or all(_TABLE_SEPARATOR.fullmatch(cell) for cell in cells)
                or (following and all(_TABLE_SEPARATOR.fullmatch(c) for c in following))
            ):
                continue
            for token in _identity_tokens(cells[0]):
                retired.setdefault(token, path)
    return retired


def package_exit_diagnostics(
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
    base_texts: Mapping[PurePosixPath, str],
    proposed_texts: Mapping[PurePosixPath, str],
    *,
    base_mode: LifecycleBaseMode,
) -> tuple[LifecycleDiagnostic, ...]:
    """Refuse a staged Stage 03 package exit in the wrong shape.

    The inputs are full snapshots, so an unchanged Task is still judged.
    Recovery proof, holds and authority stay manual (ADR-0056 Decision 6).
    """

    packages: dict[str, list[PurePosixPath]] = {}
    for path in base_documents:
        if (
            len(path.parts) >= 4
            and path.parts[:2] == ("docs", "03.specs")
            and _PACKAGE_DIR.fullmatch(path.parts[2])
        ):
            packages.setdefault(path.parts[2], []).append(path)
    lineage = "\n".join(
        _archived_lineage_text(proposed_texts.get(path, ""))
        for path, document in proposed_documents.items()
        if document.profile_id == "sdlc/requirement"
        and proposed_texts.get(path) != base_texts.get(path)
    )
    diagnostics = []
    for name in sorted(packages):
        root = PurePosixPath("docs/03.specs", name)
        paths = packages[name]
        tasks = [path for path in paths if path.parts[3] == "01.tasks"]
        tasks_terminal = all(
            base_documents[path].status in _TERMINAL_TASK_STATES for path in tasks
        )
        spec = base_documents.get(root / "spec.md")
        finished = tasks_terminal and (
            bool(tasks) or (spec is not None and spec.status == "cancelled")
        )
        deleted = [path for path in paths if path not in proposed_documents]

        def refuse(
            path: PurePosixPath, rule: str, observed: str, expected: str
        ) -> None:
            diagnostics.append(
                _diagnostic(
                    "LIFECYCLE-PACKAGE-EXIT",
                    path=path,
                    profile=base_documents[path].profile_id
                    if path in base_documents
                    else "sdlc/spec",
                    expected=expected,
                    observed=f"{rule}: {observed}",
                    base_mode=base_mode,
                    evidence_gap=(
                        "package exit shape; recovery, hold and authority stay manual"
                    ),
                )
            )

        if deleted:
            if not finished:
                refuse(
                    root,
                    "R1",
                    "deletes a package that is not finished at the base",
                    "every Task completed or cancelled first",
                )
            elif len(deleted) != len(paths):
                refuse(
                    root,
                    "R2",
                    f"deletes {len(deleted)} of {len(paths)} package files",
                    "the whole package leaves in one change",
                )
            elif f"{root.as_posix()}/" not in lineage:
                refuse(
                    root,
                    "R3",
                    "no Requirement changed here names the package in Archived Lineage",
                    "Archived Lineage entry in the same change",
                )
            continue
        if tasks and tasks_terminal:
            for document in ("spec.md", "plan.md"):
                path = root / document
                if path in base_texts and proposed_texts.get(path) != base_texts[path]:
                    refuse(
                        path,
                        "R4",
                        "edits the Spec or Plan of a finished package",
                        "finished package Spec and Plan unchanged",
                    )
    return tuple(diagnostics)


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
            evidence_gap="parsed current Task evidence",
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


def _frontmatter_version(text: str) -> str | None:
    """The frontmatter `version` of a document, or None when it has none."""

    closing = text.find("\n---\n", 4)
    if not text.startswith("---\n") or closing < 0:
        return None
    try:
        metadata = load_frontmatter(text[4:closing])
    except FrontmatterError:
        return None
    version = metadata.get("version") if isinstance(metadata, dict) else None
    return version if isinstance(version, str) else None


def document_from_text(
    registry: Registry,
    path: PurePosixPath,
    text: str,
    *,
    base_side: bool = False,
) -> LifecycleDocument:
    """Classify one document and extract only its registry-owned status.

    A comparison base was valid when committed, so its unknown type can only
    come from a profile the change removes; it is read under the path's profile.
    """

    selected_profile = classify_path(registry, path)
    if not _stateful(selected_profile):
        return LifecycleDocument(
            path=path,
            profile_id=selected_profile.profile_id,
            status=None,
            version=_frontmatter_version(text),
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
        metadata = load_frontmatter(text[4:closing])
    except FrontmatterError:
        metadata = None
    if not isinstance(metadata, dict):
        return LifecycleDocument(
            path=path,
            profile_id=selected_profile.profile_id,
            status=None,
            state_issue="frontmatter is not a unique-key mapping",
        )
    version = metadata.get("version")
    if selected_profile.profile_id == "common/native-skill-package":
        # The envelope version is a different object (SKILL-REV), not compared.
        nested = metadata.get("metadata")
        metadata = nested if isinstance(nested, dict) else {}
        version = None
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
    elif not base_side:
        profile_issue = f"frontmatter type is unknown: {claimed_profile_id!r}"
    status = metadata.get("status")
    if status is None:
        semantic = text
        if has_common_envelope(text):
            try:
                semantic = payload_markdown(
                    text, profile_id=selected_profile.profile_id
                )
            except CommonDocumentError:
                # The Markdown profile gate reports malformed common shells.
                pass
        status = task_status(metadata, semantic, selected_profile) or None
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
        version=version if isinstance(version, str) else None,
    )
