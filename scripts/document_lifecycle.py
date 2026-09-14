"""Pure document lifecycle comparison over registry-selected snapshots."""

from __future__ import annotations

import copy
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Literal, Mapping, Sequence

import yaml

from document_authority import AuthorityError, require_reciprocal_supersession
from document_contracts import DocumentProfile, Registry, classify_path


LifecycleSeverity = Literal["FAIL", "DEFER"]
LifecycleBaseMode = Literal["staged", "ci", "explicit-ref", "snapshot", "unknown"]


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
    original_path: PurePosixPath | None = None
    archive_reason: str | None = None
    replacement: PurePosixPath | None = None
    artifact_id: str | None = None
    original_artifact_id: str | None = None


@dataclass(frozen=True)
class LifecycleRename:
    """One exact-blob Git rename detected before document classification."""

    old_path: PurePosixPath
    new_path: PurePosixPath


@dataclass(frozen=True, order=True)
class ArtifactIdentityLineage:
    """One proof-backed same-document identity move between exact paths."""

    artifact_id: str
    source_path: PurePosixPath
    target_path: PurePosixPath


@dataclass(frozen=True)
class MigrationLifecycleEvents:
    """Proof-backed events, never permission to suppress a path's diagnostics."""

    publications: frozenset[PurePosixPath] = frozenset()
    source_removals: frozenset[PurePosixPath] = frozenset()
    current_rehomes: frozenset[tuple[PurePosixPath, PurePosixPath]] = frozenset()
    # An archive record is not a current document, so it cannot rehome through
    # `current_rehomes`. A proven archive move consumes both of its paths: the
    # record's bytes and provenance are checked by the archive owner, and the
    # move itself is admitted only from a reviewed declaration.
    archive_rehomes: frozenset[tuple[PurePosixPath, PurePosixPath]] = frozenset()
    # A form holds no lifecycle state and lives outside the governance tree, so
    # it reaches neither rehome above. Its identity is the registry route it
    # answers to, and a `moved` row is byte-identical, so a reviewed move onto
    # the same template route is the entire event.
    form_rehomes: frozenset[tuple[PurePosixPath, PurePosixPath]] = frozenset()
    identity_lineages: frozenset[ArtifactIdentityLineage] = frozenset()


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
    """A profile participates in lifecycle validation only through its domain.

    A declared domain is the claim that the profile has states, so an authored
    mode is not required: naming one profile here exempted every other one that
    declares a graph and is not authored. Two exclusions remain, each an
    ownership boundary rather than a name. A form carries an example value, not
    a document's state, so `mode: template` never transitions. A tombstone's
    creation is evidenced by the archive owner and its bytes are immutable
    afterwards, so admitting it as an ordinary creation here would answer ahead
    of the gate that owns it.
    """

    return (
        profile.lifecycle_domain is not None
        and profile.mode != "template"
        and profile.profile_id != "archive/tombstone"
    )


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
    migration_events: MigrationLifecycleEvents = MigrationLifecycleEvents(),
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
            # its appearance is not a lifecycle event. The transition, snapshot
            # and parsing paths all ask `_stateful`. Creation asked `mode`, and
            # the two answers differed: a migration record was never checked,
            # while a domainless README was reported for having no lifecycle.
            continue
        state_failure = _state_diagnostic(
            document, profile, base_mode=base_mode, side="proposed"
        )
        if state_failure is not None:
            diagnostics.append(state_failure)
            continue
        if (
            document.path in migration_events.publications
            and document.profile_id == "archive/migration"
            and document.status == "sealed"
        ) or (
            any(
                target == document.path
                for _, target in migration_events.current_rehomes
            )
            and document.status == "active"
            and profile.lifecycle_domain is not None
            and profile.lifecycle_domain.validation_class(document.status) == "current"
        ):
            continue
        domain = profile.lifecycle_domain
        assert domain is not None  # `_stateful` admits only a declared domain.
        observed = f"absent -> {document.status or 'not-applicable'}"
        inbound = {target for _, target in domain.transitions}
        initial_states = tuple(
            state for state, _ in domain.states if state not in inbound
        )
        if document.status not in initial_states:
            diagnostics.append(
                _diagnostic(
                    "LIFECYCLE-CREATE",
                    path=document.path,
                    profile=document.profile_id,
                    expected=f"create in zero-indegree lifecycle state {initial_states!r}",
                    observed=observed,
                    base_mode=base_mode,
                    evidence_gap="profile lifecycle domain owns creation states",
                )
            )
    return diagnostics


def _mirrored_archive_path(
    original_path: PurePosixPath, archive_reason: str | None = None
) -> PurePosixPath | None:
    if (
        original_path.is_absolute()
        or not original_path.parts
        or original_path.parts[0] != "docs"
        or ".." in original_path.parts
        or original_path.parts[1:2] == ("98.archive",)
    ):
        return None
    if archive_reason is not None:
        from archive_recovery import ArchiveContractError, disposition_archive_path

        try:
            return PurePosixPath(
                disposition_archive_path(original_path.as_posix(), archive_reason)
            )
        except ArchiveContractError:
            return None
    return PurePosixPath("docs/98.archive", *original_path.parts[1:])


def archive_disposition_gaps(
    registry: Registry,
    source: LifecycleDocument,
    reason: str,
    replacement: PurePosixPath | None,
    successor: LifecycleDocument | None,
) -> list[str]:
    """Share the declared terminal edge and successor checks with sealed recovery."""
    gaps: list[str] = []
    source_profile = _optional_profile_by_id(registry, source.profile_id)
    domain = source_profile.lifecycle_domain if source_profile else None
    terminal = {
        "superseded": "superseded",
        "consolidated": "superseded",
        "duplicate": "superseded",
        "retired": "retired",
        "abandoned": "withdrawn",
    }.get(reason)
    if (
        source.state_issue
        or domain is None
        or terminal is None
        or domain.validation_class(terminal) != "terminal"
        or (
            source.status != terminal
            and (source.status, terminal) not in domain.transitions
        )
    ):
        gaps.append(
            "source lacks the declared terminal state or forward lifecycle edge"
        )
    if terminal == "superseded":
        successor_profile = (
            _optional_profile_by_id(registry, successor.profile_id)
            if successor
            else None
        )
        successor_domain = (
            successor_profile.lifecycle_domain if successor_profile else None
        )
        if (
            replacement is None
            or successor is None
            or successor.state_issue
            or successor_domain is None
            or successor.status is None
            or successor_domain.validation_class(successor.status) != "current"
            or domain is None
            or successor_domain.family != domain.family
        ):
            gaps.append(
                "supersession replacement is not a current owner of the same family"
            )
    elif replacement is not None:
        gaps.append("ended-without-successor record must not claim a replacement")
    return gaps


def _archive_creation_evidence(
    registry: Registry,
    created: Sequence[LifecycleDocument],
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
    evidence_context: LifecycleEvidenceContext | None,
    *,
    base_mode: LifecycleBaseMode,
) -> tuple[list[LifecycleDiagnostic], set[PurePosixPath]]:
    diagnostics: list[LifecycleDiagnostic] = []
    admitted_source_removals: set[PurePosixPath] = set()
    for document in created:
        if document.profile_id != "archive/tombstone":
            continue
        profile = _optional_profile_by_id(registry, document.profile_id)
        gaps: list[str] = []
        original_path = document.original_path
        expected_archive_path = (
            _mirrored_archive_path(original_path, document.archive_reason)
            if original_path is not None
            else None
        )
        if profile is None or profile.lifecycle_domain is None:
            gaps.append("registry archive lifecycle domain is unavailable")
        if document.state_issue or document.status != "archived":
            gaps.append("archive envelope is not a valid archived record")
        if original_path is None:
            gaps.append("archive original_path evidence is missing")
        elif expected_archive_path != document.path:
            gaps.append("archive path does not mirror original_path")
        elif original_path not in base_documents:
            gaps.append("original source is absent from the comparison base")
        elif original_path in proposed_documents:
            gaps.append("original source remains in the proposed snapshot")
        if isinstance(document.archive_reason, str) and original_path in base_documents:
            gaps.extend(
                archive_disposition_gaps(
                    registry,
                    base_documents[original_path],
                    document.archive_reason,
                    document.replacement,
                    proposed_documents.get(document.replacement),
                )
            )
        if evidence_context is None:
            gaps.append("same-diff archive evidence context is unavailable")
        elif original_path is not None:
            if original_path not in evidence_context.changed_paths:
                gaps.append("original source removal is absent from the same diff")
            if document.path not in evidence_context.created_paths:
                gaps.append("mirrored archive creation is absent from the same diff")
        if gaps:
            diagnostics.append(
                _diagnostic(
                    "LIFECYCLE-EVIDENCE",
                    path=document.path,
                    profile=document.profile_id,
                    expected=(
                        "predicate archive-source-removal for one source removal "
                        "and mirrored content/archive creation"
                    ),
                    observed=f"absent -> {document.status or 'not-applicable'}",
                    base_mode=base_mode,
                    evidence_gap="; ".join(gaps),
                )
            )
        elif original_path is not None:
            admitted_source_removals.add(original_path)
    return diagnostics, admitted_source_removals


SPECIFICATION_PROFILES = frozenset(
    {
        "sdlc/spec",
    }
)
_RETIRED_SPECIFICATION_PROFILES = frozenset(
    {
        "sdlc/agent-design",
        "sdlc/tests",
    }
)
_RETIRED_REQUIREMENT_PROFILES = frozenset(
    {
        "sdlc/prd",
        "sdlc/srs",
        "sdlc/interface",
    }
)


def specification_relationship_profiles(registry: Registry) -> frozenset[str]:
    """Return current Spec-package profiles plus snapshot-only retired aliases."""

    registry_profile_ids = frozenset(
        profile.profile_id for profile in registry.profiles
    )
    current = SPECIFICATION_PROFILES & registry_profile_ids
    if "sdlc/spec" not in current:
        raise ValueError("registry lacks the canonical sdlc/spec relationship profile")
    return current | (_RETIRED_SPECIFICATION_PROFILES & registry_profile_ids)


def requirement_relationship_profiles(registry: Registry) -> frozenset[str]:
    """Return the terminal Requirement owner plus snapshot-only retired aliases."""

    registry_profile_ids = frozenset(
        profile.profile_id for profile in registry.profiles
    )
    current = frozenset({"sdlc/requirement"}) & registry_profile_ids
    if not current:
        raise ValueError("registry lacks the canonical Requirement Package profile")
    return current | (_RETIRED_REQUIREMENT_PROFILES & registry_profile_ids)


def _terminal_supersession_evidence(
    profile: DocumentProfile,
    target: LifecycleDocument,
    context: LifecycleEvidenceContext,
    *,
    base_mode: LifecycleBaseMode,
) -> tuple[LifecycleDiagnostic, ...]:
    """Enforce the domain-derived reciprocal rule using rendered links."""

    domain = profile.lifecycle_domain
    if domain is None or not domain.requires_reciprocal_supersession:
        return ()
    target_view = context.proposed_documents.get(target.path)
    if target_view is not None:
        for successor in target_view.relationship_links:
            successor_view = context.proposed_documents.get(successor)
            if successor_view is None:
                continue
            try:
                require_reciprocal_supersession(
                    source=target.path.as_posix(),
                    successor=successor.as_posix(),
                    source_links={"superseded_by": successor.as_posix()},
                    successor_links={
                        "supersedes": (
                            target.path.as_posix()
                            if target.path in successor_view.relationship_links
                            else ""
                        )
                    },
                )
            except AuthorityError:
                continue
            return ()
    return (
        _diagnostic(
            "LIFECYCLE-EVIDENCE",
            path=target.path,
            profile=target.profile_id,
            expected="one reciprocal supersedes/superseded_by relationship",
            observed=f"terminal supersession to {target.status}",
            base_mode=base_mode,
            evidence_gap="registry lifecycle domain requires reciprocal supersession",
        ),
    )


def artifact_identity_reuse_diagnostics(
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
    *,
    identity_lineages: frozenset[ArtifactIdentityLineage] = frozenset(),
    base_mode: LifecycleBaseMode,
) -> tuple[LifecycleDiagnostic, ...]:
    """Reject new owners of identities reserved by the base or sealed evidence."""

    reserved: dict[str, set[PurePosixPath]] = {}
    for document in base_documents.values():
        if document.artifact_id is not None:
            reserved.setdefault(document.artifact_id, set()).add(document.path)
    for lineage in identity_lineages:
        reserved.setdefault(lineage.artifact_id, set()).add(lineage.source_path)

    tombstone_lineages: set[ArtifactIdentityLineage] = set()
    for document in (*base_documents.values(), *proposed_documents.values()):
        if (
            document.profile_id != "archive/tombstone"
            or document.status != "archived"
            or document.state_issue is not None
            or document.original_artifact_id is None
            or document.original_path is None
        ):
            continue
        reserved.setdefault(document.original_artifact_id, set()).add(
            document.original_path
        )
        if document.replacement is not None:
            tombstone_lineages.add(
                ArtifactIdentityLineage(
                    document.original_artifact_id,
                    document.original_path,
                    document.replacement,
                )
            )

    allowed = identity_lineages | frozenset(tombstone_lineages)
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
        sources = reserved.get(artifact_id, set())
        if not sources or any(
            ArtifactIdentityLineage(artifact_id, source, path) in allowed
            for source in sources
        ):
            continue
        diagnostics.append(
            _diagnostic(
                "LIFECYCLE-IDENTITY-REUSE",
                path=path,
                profile=document.profile_id,
                expected=(
                    "new artifact identity absent from the comparison base and "
                    "sealed dispositions, or exact same-document lineage"
                ),
                observed=f"{artifact_id!r} reserved at another document path",
                base_mode=base_mode,
                evidence_gap="base or sealed migration/tombstone identity provenance",
            )
        )
    return tuple(diagnostics)


def compare_lifecycle(
    registry: Registry,
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
    *,
    renames: Sequence[LifecycleRename] = (),
    base_mode: Literal["staged", "ci", "explicit-ref"],
    evidence_context: LifecycleEvidenceContext | None = None,
    migration_events: MigrationLifecycleEvents = MigrationLifecycleEvents(),
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
            identity_lineages=migration_events.identity_lineages,
            base_mode=base_mode,
        )
    )
    consumed_base: set[PurePosixPath] = set()
    consumed_proposed: set[PurePosixPath] = set()

    for source, target in migration_events.archive_rehomes:
        if source in base_documents and target in proposed_documents:
            consumed_base.add(source)
            consumed_proposed.add(target)

    for rename in sorted(
        renames, key=lambda item: (item.old_path.as_posix(), item.new_path.as_posix())
    ):
        base = base_documents.get(rename.old_path)
        proposed = proposed_documents.get(rename.new_path)
        if base is None or proposed is None:
            raise ValueError(
                "exact rename must name one base and one proposed document"
            )
        if (rename.old_path, rename.new_path) in migration_events.archive_rehomes:
            # Already consumed above: a reviewed archive move, not a bare rename.
            continue
        if (rename.old_path, rename.new_path) in migration_events.current_rehomes:
            # A proven move remains a create/delete pair so state validation is
            # still performed; only its exact rename event is admitted.
            continue
        if (rename.old_path, rename.new_path) in migration_events.form_rehomes:
            # Same admission for a form: the create/delete pair still runs, and
            # a form has no state for it to evaluate.
            continue
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
                    evidence_gap="registry profile classification is immutable",
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

    created_paths = set(proposed_documents) - consumed_proposed - common_paths
    created = [
        proposed_documents[path]
        for path in sorted(created_paths, key=PurePosixPath.as_posix)
    ]
    creation_diagnostics = _create_diagnostics(
        registry, created, base_mode=base_mode, migration_events=migration_events
    )
    diagnostics.extend(creation_diagnostics)
    archive_evidence_diagnostics, _ = _archive_creation_evidence(
        registry,
        created,
        base_documents,
        proposed_documents,
        evidence_context,
        base_mode=base_mode,
    )
    diagnostics.extend(archive_evidence_diagnostics)

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


# A base or historical snapshot spells a profile identity the way the registry
# spelled it when those bytes were reviewed. Reading history through the current
# registry alone would report every renamed profile as unknown, so a snapshot
# that declares itself historical resolves a retired spelling through the route
# the path selects today. The route, not a fixed successor, decides: one retired
# identity split into six, and only the path says which kind a document became.
# The proposed snapshot passes no retired set and therefore still rejects one.
RETIRED_DOCUMENT_TYPES: frozenset[str] = frozenset(
    {
        "sdlc/ad",
        "sdlc/adr",
        "sdlc/requirement-package",
        "sdlc/guide",
        "sdlc/policy",
        "sdlc/runbook",
        "sdlc/incident",
        "sdlc/postmortem",
        "content/audit-reference",
        "content/research-reference",
        "content/data-reference",
        "content/archive",
        "content/archive-migration",
        "governance/reference",
    }
)


def document_from_text(
    registry: Registry,
    path: PurePosixPath,
    text: str,
    *,
    retired_types: frozenset[str] | None = None,
) -> LifecycleDocument:
    """Classify one document and extract only its registry-owned status."""

    selected_profile = classify_path(registry, path)
    if (
        not _stateful(selected_profile)
        and selected_profile.profile_id != "archive/tombstone"
    ):
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
    if (
        retired_types is not None
        and isinstance(claimed_profile_id, str)
        and claimed_profile_id in retired_types
    ):
        claimed_profile_id = selected_profile.profile_id
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
    if selected_profile.profile_id == "archive/migration" and status == "accepted":
        # Only byte-verified historical controls use the predecessor spelling.
        # The registry domain continues to reject accepted for future records.
        from archive_validation import (
            ArchiveContractError,
            parse_pinned_migration_control,
        )

        try:
            parse_pinned_migration_control(path.as_posix(), text.encode("utf-8"))
        except ArchiveContractError:
            profile_issue = "unverified historical Migration state"
        else:
            status = "sealed"
    original_path: PurePosixPath | None = None
    archive_reason: str | None = None
    replacement_path: PurePosixPath | None = None
    artifact_id = metadata.get("artifact_id")
    if not isinstance(artifact_id, str):
        artifact_id = None
    original_artifact_id: str | None = None
    if profile_id == "archive/tombstone":
        prior_generation: bool | None = None
        from archive_recovery import (
            ArchiveContractError,
            archive_metadata_is_prior_generation,
            validate_archive_replacement,
        )

        try:
            prior_generation = archive_metadata_is_prior_generation(metadata)
        except ArchiveContractError as error:
            profile_issue = (
                "archive replacement is missing"
                if error.code == "ARCHIVE-METADATA-REPLACEMENT"
                else "archive generation is noncanonical"
            )
        raw_original_path = metadata.get("original_path")
        if isinstance(raw_original_path, str):
            candidate = PurePosixPath(raw_original_path)
            if (
                candidate.as_posix() == raw_original_path
                and _mirrored_archive_path(candidate) is not None
            ):
                original_path = candidate
        if original_path is None:
            profile_issue = "archive original_path is missing or noncanonical"
        raw_reason = metadata.get("archive_reason")
        if isinstance(raw_reason, str):
            archive_reason = raw_reason
            if prior_generation is not None:
                try:
                    replacement = validate_archive_replacement(
                        raw_reason,
                        metadata["replacement"],
                        prior_generation=prior_generation,
                    )
                except ArchiveContractError:
                    profile_issue = (
                        "archive replacement is noncanonical for document generation"
                    )
                else:
                    if replacement is not None:
                        replacement_path = PurePosixPath(replacement.path)
        elif raw_reason is not None:
            profile_issue = "archive_reason is not a string"
        raw_original_artifact_id = metadata.get("original_artifact_id")
        if isinstance(raw_original_artifact_id, str):
            original_artifact_id = raw_original_artifact_id
    return LifecycleDocument(
        path=path,
        profile_id=profile_id,
        status=status,
        state_issue=profile_issue,
        original_path=original_path,
        archive_reason=archive_reason,
        replacement=replacement_path,
        artifact_id=artifact_id,
        original_artifact_id=original_artifact_id,
    )
