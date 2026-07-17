"""Pure document lifecycle comparison over registry-selected snapshots."""

from __future__ import annotations

import copy
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Literal, Mapping, Sequence

import yaml

from document_contracts import DocumentProfile, Registry, classify_path


LifecycleSeverity = Literal["FAIL", "DEFER"]
LifecycleBaseMode = Literal["staged", "ci", "explicit-ref", "snapshot", "unknown"]
LIFECYCLE_RULE_IDS = frozenset(
    {
        "LIFECYCLE-CREATE",
        "LIFECYCLE-DELETE",
        "LIFECYCLE-RENAME",
        "LIFECYCLE-PROFILE-CHANGE",
        "LIFECYCLE-STATE",
        "LIFECYCLE-EDGE",
        "LIFECYCLE-EVIDENCE",
        "LIFECYCLE-BASE",
        "LIFECYCLE-BASE-DEFER",
    }
)


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


@dataclass(frozen=True)
class LifecycleRename:
    """One exact-blob Git rename detected before document classification."""

    old_path: PurePosixPath
    new_path: PurePosixPath


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
    return profile.admission.create.mode in {"states", "paired", "baseline-only"}


def _state_diagnostic(
    document: LifecycleDocument,
    profile: DocumentProfile,
    *,
    base_mode: LifecycleBaseMode,
    side: Literal["base", "proposed", "snapshot"],
) -> LifecycleDiagnostic | None:
    if not _stateful(profile):
        return None
    if document.state_issue is None and document.status in profile.status_domain:
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
        expected=f"{side} status in {profile.status_domain!r}",
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
    paired: dict[tuple[str, str], list[LifecycleDocument]] = {}
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
        state_failure = _state_diagnostic(
            document, profile, base_mode=base_mode, side="proposed"
        )
        if state_failure is not None:
            diagnostics.append(state_failure)
            continue
        admission = profile.admission
        observed = f"absent -> {document.status or 'not-applicable'}"
        if admission.create.mode == "states":
            if document.status not in admission.create.states:
                diagnostics.append(
                    _diagnostic(
                        "LIFECYCLE-CREATE",
                        path=document.path,
                        profile=document.profile_id,
                        expected=f"create in {admission.create.states!r}",
                        observed=observed,
                        base_mode=base_mode,
                        evidence_gap=f"admission policy {admission.policy_id}",
                    )
                )
        elif admission.create.mode == "paired":
            if document.status not in admission.create.states:
                diagnostics.append(
                    _diagnostic(
                        "LIFECYCLE-CREATE",
                        path=document.path,
                        profile=document.profile_id,
                        expected=(
                            "same-diff Plan/Task creation in one allowed state "
                            f"{admission.create.states!r}"
                        ),
                        observed=observed,
                        base_mode=base_mode,
                        evidence_gap=f"admission policy {admission.policy_id}",
                    )
                )
            else:
                paired.setdefault((admission.policy_id, document.status), []).append(
                    document
                )
        else:
            diagnostics.append(
                _diagnostic(
                    "LIFECYCLE-CREATE",
                    path=document.path,
                    profile=document.profile_id,
                    expected="no lifecycle creation",
                    observed=observed,
                    base_mode=base_mode,
                    evidence_gap=f"admission policy {admission.policy_id}",
                )
            )

    for (policy_id, status), candidates in paired.items():
        plans = [item for item in candidates if item.profile_id == "sdlc/plan"]
        tasks = [item for item in candidates if item.profile_id == "sdlc/task"]
        if len(plans) == 1 and len(tasks) == 1:
            continue
        for document in candidates:
            diagnostics.append(
                _diagnostic(
                    "LIFECYCLE-CREATE",
                    path=document.path,
                    profile=document.profile_id,
                    expected=(
                        "exactly one Plan and one Task creation in the same "
                        f"proposal state {status!r}"
                    ),
                    observed=f"Plan count {len(plans)}, Task count {len(tasks)}",
                    base_mode=base_mode,
                    evidence_gap=(
                        f"paired admission {policy_id}; reciprocal/direct-Spec "
                        "evidence is deferred to DSLC-004"
                    ),
                )
            )
    return diagnostics


def compare_lifecycle(
    registry: Registry,
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
    *,
    renames: Sequence[LifecycleRename] = (),
    base_mode: Literal["staged", "ci", "explicit-ref"],
) -> tuple[LifecycleDiagnostic, ...]:
    """Compare independently classified snapshots with fixed event precedence.

    Exact renames replace create/delete events. A same-path profile change
    replaces state/edge evaluation. Invalid state replaces edge evaluation.
    Evidence predicates are intentionally not evaluated until DSLC-004.
    """

    diagnostics: list[LifecycleDiagnostic] = []
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
        base_profile = _optional_profile_by_id(registry, base.profile_id)
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
                    evidence_gap=(
                        "profile-change admission is "
                        f"{proposed_profile.admission.profile_change}"
                    ),
                )
            )
            continue
        profile = proposed_profile
        base_state_failure = _state_diagnostic(
            base, profile, base_mode=base_mode, side="base"
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
        if base.status == proposed.status or not _stateful(profile):
            continue
        allowed_edges = {
            (edge.from_state, edge.to_state) for edge in profile.lifecycle.edges
        }
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

    deleted_paths = set(base_documents) - consumed_base - common_paths
    for path in sorted(deleted_paths, key=PurePosixPath.as_posix):
        document = base_documents[path]
        profile = _optional_profile_by_id(registry, document.profile_id)
        admission_gap = (
            f"delete admission is {profile.admission.delete}"
            if profile is not None
            else "unclassified target Markdown deletion is denied"
        )
        diagnostics.append(
            _diagnostic(
                "LIFECYCLE-DELETE",
                path=path,
                profile=document.profile_id,
                expected="document retained",
                observed=f"{document.status or 'not-applicable'} -> absent",
                base_mode=base_mode,
                evidence_gap=admission_gap,
            )
        )

    created_paths = set(proposed_documents) - consumed_proposed - common_paths
    created = [
        proposed_documents[path]
        for path in sorted(created_paths, key=PurePosixPath.as_posix)
    ]
    diagnostics.extend(_create_diagnostics(registry, created, base_mode=base_mode))
    return tuple(sorted(diagnostics, key=lifecycle_diagnostic_sort_key))


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
    claimed_profile_id = metadata.get("type")
    known_profile_ids = {profile.profile_id for profile in registry.profiles}
    profile_id = selected_profile.profile_id
    profile_issue: str | None = None
    if not isinstance(claimed_profile_id, str):
        profile_issue = "frontmatter type is missing or not a string"
    elif claimed_profile_id not in known_profile_ids:
        profile_issue = f"frontmatter type is unknown: {claimed_profile_id!r}"
    else:
        profile_id = claimed_profile_id
        if profile_id != selected_profile.profile_id:
            profile_issue = (
                f"frontmatter type {profile_id!r} differs from route profile "
                f"{selected_profile.profile_id!r}"
            )
    status = metadata.get("status")
    if not isinstance(status, str):
        return LifecycleDocument(
            path=path,
            profile_id=profile_id,
            status=None,
            state_issue="frontmatter status is missing or not a string",
        )
    return LifecycleDocument(
        path=path,
        profile_id=profile_id,
        status=status,
        state_issue=profile_issue,
    )
