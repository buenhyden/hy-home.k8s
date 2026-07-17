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


@dataclass(frozen=True)
class LifecycleEvidenceContext:
    """Immutable inputs resolved from one Git base/proposed snapshot pair."""

    base_documents: Mapping[PurePosixPath, LifecycleDocument]
    proposed_documents: Mapping[PurePosixPath, LifecycleEvidenceDocument]
    changed_paths: frozenset[PurePosixPath]
    status_changed_paths: frozenset[PurePosixPath]
    body_changed_paths: frozenset[PurePosixPath]
    created_paths: frozenset[PurePosixPath]


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


SPECIFICATION_PROFILES = frozenset(
    {
        "sdlc/spec",
        "sdlc/api-spec",
        "sdlc/agent-design",
        "sdlc/data-model",
        "sdlc/tests",
    }
)


def _predicate_for_edge(
    registry: Registry,
    profile_id: str,
    from_state: str,
    to_state: str,
):
    profile = _profile_by_id(registry, profile_id)
    predicate_ids = {
        edge.predicate_id
        for edge in profile.lifecycle.edges
        if edge.from_state == from_state and edge.to_state == to_state
    }
    if len(predicate_ids) != 1:
        raise ValueError(
            f"lifecycle edge does not resolve one predicate: "
            f"{profile_id} {from_state} -> {to_state}"
        )
    predicate_id = next(iter(predicate_ids))
    predicates = [
        predicate
        for predicate in registry.evidence_predicates
        if predicate.predicate_id == predicate_id
    ]
    if len(predicates) != 1:
        raise ValueError(f"unknown or duplicate evidence predicate: {predicate_id}")
    return predicates[0]


def _candidate_pair(
    target: LifecycleDocument,
    context: LifecycleEvidenceContext,
    *,
    registry: Registry | None = None,
    require_dependency_ready: bool = False,
) -> tuple[tuple[tuple[PurePosixPath, PurePosixPath, PurePosixPath], ...], str | None]:
    """Resolve one reciprocal Plan/Task pair with one direct Spec identity."""

    views = context.proposed_documents
    target_view = views.get(target.path)
    if target_view is None:
        return (), "target is absent from the proposed snapshot"
    task_paths = sorted(
        (
            path
            for path, view in views.items()
            if view.document.profile_id == "sdlc/task"
            and (
                path == target.path
                or target.path in view.relationship_links
                or path in target_view.relationship_links
            )
        ),
        key=PurePosixPath.as_posix,
    )
    plan_paths = sorted(
        (
            path
            for path, view in views.items()
            if view.document.profile_id == "sdlc/plan"
            and (
                path == target.path
                or target.path in view.relationship_links
                or path in target_view.relationship_links
                or any(task in view.relationship_links for task in task_paths)
            )
        ),
        key=PurePosixPath.as_posix,
    )
    pairs: list[tuple[PurePosixPath, PurePosixPath, PurePosixPath]] = []
    split_identity = False
    for plan in plan_paths:
        plan_view = views[plan]
        for task in task_paths:
            task_view = views[task]
            if (
                task not in plan_view.relationship_links
                or plan not in task_view.relationship_links
            ):
                continue
            plan_specs = {
                linked
                for linked in plan_view.relationship_links
                if linked in views
                and views[linked].document.profile_id in SPECIFICATION_PROFILES
            }
            task_specs = {
                linked
                for linked in task_view.relationship_links
                if linked in views
                and views[linked].document.profile_id in SPECIFICATION_PROFILES
            }
            if len(plan_specs) != 1 or len(task_specs) != 1 or plan_specs != task_specs:
                split_identity = True
                continue
            spec = next(iter(plan_specs))
            if target.profile_id in SPECIFICATION_PROFILES and spec != target.path:
                split_identity = True
                continue
            if (
                target.profile_id not in SPECIFICATION_PROFILES
                and views[spec].document.profile_id != "sdlc/spec"
            ):
                split_identity = True
                continue
            if target.profile_id not in {
                "sdlc/plan",
                "sdlc/task",
                *SPECIFICATION_PROFILES,
            } and (
                task not in target_view.relationship_links
                or target.path not in task_view.body_table_links
            ):
                continue
            pairs.append((plan, task, spec))
    pairs = sorted(
        set(pairs),
        key=lambda item: (
            item[0].as_posix(),
            item[1].as_posix(),
            item[2].as_posix(),
        ),
    )
    if require_dependency_ready:
        if registry is None:
            raise ValueError("dependency-ready pair resolution requires the registry")
        ready_paths: set[PurePosixPath] = set()
        wrong_ready_state_paths: set[PurePosixPath] = set()
        for program in registry.program_lineage:
            ready = next(
                (
                    relation
                    for relation in program.tranches
                    if relation.state not in {"done", "archived"}
                ),
                None,
            )
            if ready is None:
                continue
            candidates = [
                path
                for path, view in views.items()
                if view.document.profile_id == "sdlc/spec"
                and path.name == "spec.md"
                and path.parent.name.startswith(f"{ready.spec_id}-")
            ]
            if len(candidates) == 1:
                candidate = candidates[0]
                if views[candidate].document.status == ready.state:
                    ready_paths.add(candidate)
                else:
                    wrong_ready_state_paths.add(candidate)
        blocked = [pair for pair in pairs if pair[2] not in ready_paths]
        pairs = [pair for pair in pairs if pair[2] in ready_paths]
        if blocked and not pairs:
            if any(pair[2] in wrong_ready_state_paths for pair in blocked):
                return (), "pair Spec status does not match registry ready state"
            return (), "pair targets a blocked successor or unknown Spec"
    if len(pairs) == 1:
        return tuple(pairs), None
    if split_identity:
        return tuple(pairs), "Plan/Task reciprocal links do not share one direct Spec"
    return tuple(
        pairs
    ), f"expected one reciprocal Plan/Task pair, observed {len(pairs)}"


def _program_evidence(
    registry: Registry,
    target: LifecycleDocument,
    context: LifecycleEvidenceContext,
) -> tuple[tuple[PurePosixPath, ...], tuple[str, ...]]:
    views = context.proposed_documents
    programs = [
        program
        for program in registry.program_lineage
        if target.path.name.startswith(f"{program.prd_id}-")
    ]
    if len(programs) != 1:
        return (), ("target does not resolve one registry program lineage",)
    program = programs[0]
    relation_paths: list[PurePosixPath] = []
    gaps: list[str] = []
    for relation in (*program.tranches, *program.follow_ups):
        candidates = [
            path
            for path, view in views.items()
            if view.document.profile_id == "sdlc/spec"
            and len(path.parts) >= 2
            and path.name == "spec.md"
            and path.parent.name.startswith(f"{relation.spec_id}-")
        ]
        if len(candidates) != 1:
            gaps.append(
                f"program Spec {relation.spec_id} resolved {len(candidates)} documents"
            )
            continue
        relation_path = candidates[0]
        relation_paths.append(relation_path)
        if views[relation_path].document.status != "done":
            gaps.append(f"program Spec {relation.spec_id} is not done")
    target_view = views.get(target.path)
    linked_specs = (
        {
            path
            for path in target_view.relationship_links
            if path in views and views[path].document.profile_id == "sdlc/spec"
        }
        if target_view is not None
        else set()
    )
    if linked_specs != set(relation_paths):
        gaps.append("PRD relationship does not resolve the exact declared Spec set")
    base_unfinished = [
        path
        for path in relation_paths
        if path not in context.base_documents
        or context.base_documents[path].status != "done"
    ]
    if not base_unfinished or base_unfinished[-1] not in context.status_changed_paths:
        gaps.append("last unfinished program relation did not change in the same diff")
    current_components = [
        path
        for path, view in views.items()
        if view.document.profile_id in {"sdlc/plan", "sdlc/task"}
        and view.document.status in {"draft", "active"}
        and any(relation in view.relationship_links for relation in relation_paths)
    ]
    if current_components:
        gaps.append("program retains an extra current execution component")
    return tuple(relation_paths), tuple(gaps)


def validate_transition_evidence(
    registry: Registry,
    target: LifecycleDocument,
    from_state: str,
    to_state: str,
    context: LifecycleEvidenceContext,
    *,
    base_mode: Literal["staged", "ci", "explicit-ref"],
    allow_created_target: bool = False,
) -> tuple[LifecycleDiagnostic, ...]:
    """Validate one allowed edge against registry-closed proposed evidence."""

    predicate = _predicate_for_edge(registry, target.profile_id, from_state, to_state)
    views = context.proposed_documents
    target_view = views.get(target.path)
    gaps: list[str] = []
    evidence_paths: tuple[PurePosixPath, ...] = ()
    base_paths = set(context.base_documents)
    proposed_paths = set(views)
    actual_created = frozenset(proposed_paths - base_paths)
    actual_status_changed = frozenset(
        path
        for path in base_paths & proposed_paths
        if context.base_documents[path].profile_id != views[path].document.profile_id
        or context.base_documents[path].status != views[path].document.status
    )
    context_universe = base_paths | proposed_paths

    if any(path != document.path for path, document in context.base_documents.items()):
        gaps.append("base snapshot key differs from embedded document path")
    if any(path != view.document.path for path, view in views.items()):
        gaps.append("proposed snapshot key differs from embedded document path")
    if context.created_paths != actual_created:
        gaps.append("created-path projection differs from canonical snapshots")
    if context.status_changed_paths != actual_status_changed:
        gaps.append("status-change projection differs from canonical snapshots")
    if not context.body_changed_paths.issubset(context.changed_paths):
        gaps.append("body-change projection is outside changed paths")
    if not actual_created.issubset(context.body_changed_paths):
        gaps.append("created documents are absent from body-change projection")
    if not (
        actual_created | actual_status_changed | context.body_changed_paths
    ).issubset(context.changed_paths):
        gaps.append("canonical changes are absent from changed-path projection")
    if not context.changed_paths.issubset(context_universe):
        gaps.append("changed-path projection is outside snapshot paths")

    if target_view is None:
        gaps.append("target is absent from the proposed evidence snapshot")
    elif target_view.document != target:
        gaps.append("proposed evidence projection differs from transition target")
    elif len(target_view.relationship_links) != len(
        set(target_view.relationship_links)
    ):
        gaps.append("relationship contains duplicate evidence targets")
    if target_view is not None and target_view.unresolved_relationship_links:
        gaps.append(
            "orphan relationship targets "
            f"{[path.as_posix() for path in target_view.unresolved_relationship_links]!r}"
        )
    if (
        target_view is not None
        and "rendered-link" in predicate.capabilities
        and not target_view.relationship_links
    ):
        gaps.append("required rendered relationship link is missing")
    related_orphans = sorted(
        (
            path
            for path, view in views.items()
            if view.unresolved_relationship_links
            and (
                path == target.path
                or target.path in view.relationship_links
                or target.path in view.body_table_links
            )
        ),
        key=PurePosixPath.as_posix,
    )
    if related_orphans:
        gaps.append(
            f"orphan evidence owners {[path.as_posix() for path in related_orphans]!r}"
        )
    base_target = context.base_documents.get(target.path)
    if allow_created_target:
        if target.path not in actual_created:
            gaps.append("created transition target exists in the base snapshot")
    elif (
        target.path in actual_created
        or base_target is None
        or base_target.profile_id != target.profile_id
        or base_target.status != from_state
    ):
        gaps.append("base evidence projection differs from transition source")

    if target_view is not None:
        owner_profile = _optional_profile_by_id(registry, target.profile_id)
        owner_contract = (
            owner_profile.body_contract if owner_profile is not None else None
        )
        if owner_contract is not None and owner_contract.reciprocal_evidence:
            for linked_path in target_view.relationship_links:
                linked_view = views.get(linked_path)
                if linked_view is None:
                    continue
                linked_profile = _optional_profile_by_id(
                    registry, linked_view.document.profile_id
                )
                linked_contract = (
                    linked_profile.body_contract if linked_profile is not None else None
                )
                reciprocal_in_scope = (
                    linked_profile is not None
                    and linked_profile.mode == "authored"
                    and linked_contract is not None
                    and linked_view.document.status in linked_contract.enforced_statuses
                )
                if (
                    reciprocal_in_scope
                    and target.path not in linked_view.all_local_links
                ):
                    gaps.append(
                        "reciprocal body evidence is missing from "
                        f"{linked_path.as_posix()}"
                    )

    if target_view is None:
        pass
    elif predicate.relationship == "self":
        evidence_paths = (target.path,)
        if (
            "rendered-link" in predicate.capabilities
            and not target_view.relationship_links
        ):
            gaps.append("required rendered relationship link is missing")
    elif predicate.relationship == "program-lineage":
        evidence_paths, program_gaps = _program_evidence(registry, target, context)
        gaps.extend(program_gaps)
    elif predicate.relationship == "pair":
        pairs, pair_gap = _candidate_pair(
            target,
            context,
            registry=registry,
            require_dependency_ready=(
                predicate.predicate_id == "activate-execution-pair"
            ),
        )
        if pair_gap is not None:
            gaps.append(pair_gap)
        evidence_paths = tuple(path for plan, task, _ in pairs for path in (plan, task))
    elif predicate.predicate_id == "activate-heading-profile":
        evidence_paths = (target.path,)
        if not target_view.relationship_links:
            gaps.append("required rendered relationship link is missing")
    elif predicate.predicate_id == "accept-architecture":
        raw_links = target_view.relationship_links
        if len(raw_links) != len(set(raw_links)):
            gaps.append("relationship contains duplicate evidence targets")
        evidence_paths = tuple(
            path
            for path in raw_links
            if path in views and views[path].document.profile_id == "sdlc/adr"
        )
        if any(
            target.path not in views[path].relationship_links for path in evidence_paths
        ):
            gaps.append(
                "architecture evidence does not link back through its relationship"
            )
    elif predicate.predicate_id == "terminate-reviewed-reference":
        pairs, pair_gap = _candidate_pair(target, context)
        if pair_gap is not None:
            gaps.append(pair_gap)
        evidence_paths = tuple(path for plan, task, _ in pairs for path in (plan, task))
    else:
        evidence_paths = tuple(target_view.relationship_links)

    unique_evidence = tuple(dict.fromkeys(evidence_paths))
    if len(unique_evidence) != len(evidence_paths):
        gaps.append("multiply matching evidence is ambiguous")
    evidence_paths = unique_evidence

    for requirement in predicate.evidence:
        allowed_profiles = {
            target.profile_id if profile_id == "$self" else profile_id
            for profile_id in requirement.profile_ids
        }
        matches = [
            path
            for path in evidence_paths
            if path in views
            and views[path].document.profile_id in allowed_profiles
            and views[path].document.status in requirement.states
        ]
        observed_profiles = sorted(
            {
                views[path].document.profile_id
                for path in evidence_paths
                if path in views
            }
        )
        if len(matches) < requirement.minimum or (
            requirement.maximum is not None and len(matches) > requirement.maximum
        ):
            gaps.append(
                "evidence requirement "
                f"profiles={sorted(allowed_profiles)!r} states={requirement.states!r} "
                f"expected={requirement.minimum}..{requirement.maximum!r} "
                f"observed={len(matches)} profiles={observed_profiles!r}"
            )

    if len(evidence_paths) < predicate.minimum or (
        predicate.maximum is not None and len(evidence_paths) > predicate.maximum
    ):
        gaps.append(
            f"relationship cardinality expected {predicate.minimum}.."
            f"{predicate.maximum!r}, observed {len(evidence_paths)}"
        )

    if target_view is not None and not target_view.relationship_section_valid:
        gaps.append("registry relationship section is missing or ambiguous")

    required_body_paths = tuple(dict.fromkeys((target.path, *evidence_paths)))
    for path in required_body_paths:
        view = views.get(path)
        if view is None or not view.body_contract_valid:
            gaps.append(f"body contract mismatch at {path.as_posix()}")
    if "task-terminal-evidence" in predicate.capabilities:
        for path in evidence_paths:
            view = views.get(path)
            if (
                view is not None
                and view.document.profile_id == "sdlc/task"
                and not view.task_terminal_evidence_valid
            ):
                gaps.append(
                    f"Task terminal evidence is incomplete at {path.as_posix()}"
                )

    if predicate.same_diff == "self-status-and-body":
        if target.path not in context.status_changed_paths:
            gaps.append("target status did not change in the same diff")
        if target.path not in context.body_changed_paths:
            gaps.append("target body did not change in the same diff")
    elif predicate.same_diff == "pair-created-or-status-changed":
        for path in evidence_paths:
            if path not in actual_created and path not in context.status_changed_paths:
                gaps.append(f"pair member did not change state at {path.as_posix()}")
    elif predicate.same_diff == "target-and-last-relation-changed":
        if target.path not in context.status_changed_paths:
            gaps.append("program target status did not change in the same diff")
        if target.path not in context.body_changed_paths:
            gaps.append("program target body did not change in the same diff")
    elif predicate.same_diff == "target-and-evidence-status-body-changed":
        if target.path not in context.status_changed_paths:
            gaps.append("architecture target status did not change in the same diff")
        if not any(
            path in context.status_changed_paths and path in context.body_changed_paths
            for path in evidence_paths
        ):
            gaps.append(
                "no architecture evidence changed status and body in the same diff"
            )
    elif predicate.same_diff == "target-plan-task-status-changed":
        for path in (target.path, *evidence_paths):
            if path not in context.status_changed_paths:
                gaps.append(f"required status did not change at {path.as_posix()}")
    elif predicate.same_diff == "pair-status-changed":
        for path in evidence_paths:
            if path not in context.status_changed_paths:
                gaps.append(f"pair status did not change at {path.as_posix()}")

    if not gaps:
        return ()
    return (
        _diagnostic(
            "LIFECYCLE-EVIDENCE",
            path=target.path,
            profile=target.profile_id,
            expected=(
                f"predicate {predicate.predicate_id} for {from_state} -> {to_state}"
            ),
            observed=f"evidence paths {[path.as_posix() for path in evidence_paths]!r}",
            base_mode=base_mode,
            evidence_gap="; ".join(dict.fromkeys(gaps)),
        ),
    )


def compare_lifecycle(
    registry: Registry,
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
    *,
    renames: Sequence[LifecycleRename] = (),
    base_mode: Literal["staged", "ci", "explicit-ref"],
    evidence_context: LifecycleEvidenceContext | None = None,
) -> tuple[LifecycleDiagnostic, ...]:
    """Compare independently classified snapshots with fixed event precedence.

    Exact renames replace create/delete events. A same-path profile change
    replaces state/edge evaluation. Invalid state replaces edge evaluation.
    Evidence predicates are evaluated only when the adapter supplies an
    immutable base/proposed evidence context from the same Git comparison.
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
        elif evidence_context is not None:
            assert base.status is not None and proposed.status is not None
            diagnostics.extend(
                validate_transition_evidence(
                    registry,
                    proposed,
                    base.status,
                    proposed.status,
                    evidence_context,
                    base_mode=base_mode,
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
    creation_diagnostics = _create_diagnostics(registry, created, base_mode=base_mode)
    diagnostics.extend(creation_diagnostics)
    if evidence_context is not None:
        failed_creation_paths = {item.path for item in creation_diagnostics}
        for document in created:
            if (
                document.path in failed_creation_paths
                or document.profile_id not in {"sdlc/plan", "sdlc/task"}
                or document.status not in {"draft", "active"}
            ):
                continue
            pairs, pair_gap = _candidate_pair(
                document,
                evidence_context,
                registry=registry,
                require_dependency_ready=True,
            )
            if pair_gap is not None:
                diagnostics.append(
                    _diagnostic(
                        "LIFECYCLE-EVIDENCE",
                        path=document.path,
                        profile=document.profile_id,
                        expected=(
                            "one reciprocal Plan/Task creation pair with one "
                            "shared direct Spec identity"
                        ),
                        observed=f"paired admission evidence {pairs!r}",
                        base_mode=base_mode,
                        evidence_gap=pair_gap,
                    )
                )
            elif document.status == "active":
                diagnostics.extend(
                    validate_transition_evidence(
                        registry,
                        document,
                        "draft",
                        "active",
                        evidence_context,
                        base_mode=base_mode,
                        allow_created_target=True,
                    )
                )
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
