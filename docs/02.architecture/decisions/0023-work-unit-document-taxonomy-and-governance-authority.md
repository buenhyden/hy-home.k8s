---
title: 'ADR-0023: Work-Unit Document Taxonomy and Governance Authority'
version: "1.0"
type: sdlc/adr
layer: "02.architecture"
status: superseded
owner: platform
updated: 2026-08-11
artifact_id: "ADR-0023"
superseded_by: ADR-0030
---

# ADR-0023: Work-Unit Document Taxonomy and Governance Authority

## Overview

This accepted decision records the human-approved work-unit-centered document
topology with a stable Stage 05 operations path and one authority plane for
document and AI-agent governance. The written design and implementation
planning were reviewed. Lifecycle acceptance and the program registry
correction from unrelated ADR-0021 occur atomically in the first implementation
work package.

## Context

The current repository separates a work unit's Spec, Plan, and Task across
Stage 03 and date-named Stage 04 collections. The resulting duplicate slug and
path conventions make lineage, migration, and validator ownership harder to
reason about. Stage 00, Stage 99, the document-profile registry, templates, and
validators also restate parts of the same contract.

External sources support lifecycle traceability and coherent change packages
but do not mandate one folder tree. ISO/IEC/IEEE 12207 and 15289 leave the
lifecycle model and information-item packaging to the adopting organization.
GitHub Spec Kit uses a Spec-to-Plan-to-Tasks flow, while OpenSpec packages a
change's proposal, spec edits, design, and tasks together. The date-free path
rule and numbered stage layout are therefore local stability decisions.

Three target directions were reviewed: retire Stage 04 while preserving Stage
05; retire Stage 04 and renumber operations to Stage 04; or keep separate Stage
03 and Stage 04 collections. The human approved the first direction and later
confirmed that a Release document family is unnecessary.

## Decision

- Co-locate `spec.md`, optional `plan.md`, and optional `tasks.md` in
  `docs/03.specs/<NNN>-<slug>/`; a Task requires both sibling documents.
- Retire `docs/03.specs/` and leave the Stage 04 numeric slot unused.
- Keep `docs/05.operations/` and its guide, incident, policy, and runbook paths
  stable. Do not create `docs/04.operations/`.
- Use stable identifiers or slugs for mutable authored documents. Keep dates in
  frontmatter except when a date is part of immutable snapshot, incident,
  postmortem, or archive identity.
- Do not add a Release profile, template, collection, lifecycle, or validator.
- Preserve all existing lifecycle identifiers. The document-profile registry
  remains the sole machine owner of routes, headings, states, forms, and
  relationships; Stage 00 owns agent-facing policy and Stage 99 owns template
  rationale and forms.
- Consolidate Stage 00 authoring policy into `document-authoring.md` and Stage
  99 support rationale into `document-contract.md` and
  `document-lifecycle.md`, deleting restated rule bodies after consumers move.
- Extend the existing harness contract and schema with agent-system risk
  policy, untrusted-input/tool-output boundaries, tool controls, human
  oversight, action-bound approval/trace record shapes, evaluation policy, and
  component provenance. Actual runtime records remain at their approved Task,
  Runbook, Incident, or provider-evidence owner and are referenced by immutable
  redacted evidence IDs; do not create a parallel agent-governance registry.
- Keep provider adapters as provider-native deltas. A tracked adapter or static
  schema PASS never proves provider discovery, enforcement, or execution.
- Introduce tested legacy/transition/terminal route states before moving
  documents. Activate terminal routes only after old consumers reach zero.
- Archive unique retired history through append-only ArchiveEnvelope records;
  preserve dated observations; delete duplicate, generated, superseded, or
  zero-consumer material only with explicit disposition evidence.
- Consolidate orchestration wrappers that share owner and behavior, but retain
  semantically distinct validators. Retire `validate-harness.sh` only after
  consumer migration and do not assume active-corpus validators are dead.

## Explicit Non-goals

- Renumbering `docs/05.operations/` or any PRD, ARD, ADR, or Spec.
- Rewriting existing Stage 98 records or historical Stage 90 observations.
- Adding Release, tutorial, or explanation document families.
- Replacing accepted ADR-0021 or ADR-0022; both retain their original decision
  scopes.
- Changing agent roles, platform desired state, provider authentication,
  hosted CI settings, remote services, credentials, or live infrastructure.
- Treating ISO, NIST, OWASP, Spec Kit, OpenSpec, or vendor guidance as local
  conformance or runtime-effectiveness evidence.

## Consequences

Work-unit discovery and execution lineage become local to one stable folder,
and future Plan/Task names no longer encode mutable dates. Stage 05 links avoid
an unrelated mass rewrite, at the cost of an intentionally unused Stage 04
number.

The migration requires a temporary dual-route contract, explicit mapping,
consumer audits, and negative fixtures. It cannot be completed through a
single unvalidated global replacement.

Human policy becomes smaller and easier to load, while the registry and harness
schemas carry more explicit machine data. Schema growth is accepted only where
it replaces ambiguity or duplicated prose; field presence remains distinct
from enforcement evidence.

Archive size may grow for unique orphan history, while reproducible or
duplicated artifacts may disappear from the tracked tree. Each disposition is
reviewable and revertible by logical commit.

## Alternatives

- **Retire Stage 04 and renumber operations to Stage 04**: rejected because
  numeric continuity does not justify rewriting every Stage 05 path and
  historical reference.
- **Keep separate Stage 03 Spec and Stage 04 Plan/Task collections**: rejected
  because it preserves duplicate work-unit identity and date-based path
  coupling.
- **Merge Spec, Plan, and Task into one Markdown body**: rejected because their
  authority, lifecycle, review, and evidence roles remain distinct even when
  physically co-located.
- **Create a new agent-system register beside the harness contract**: rejected
  because it would create another authority and synchronization surface.
- **Delete similar validators by filename or line-count reduction**: rejected
  because distinct negative fixtures and evidence semantics are contract
  boundaries.
- **Create a Release family because external research describes releases**:
  rejected because the workspace has no approved local need or public-release
  lifecycle, and the human explicitly excluded it.

## Traceability

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ARD-0011](../descriptions/0011-document-taxonomy-consolidation-architecture.md) | N/A — first decision for PRD-008 taxonomy direction; corrects only the registry's unrelated ADR-0021 association | [Spec 052](../../03.specs/0052-document-taxonomy-consolidation/spec.md) |
| [ADR-0024](./0024-terminal-artifact-identity-and-archive-layout.md) | Partially supersedes only terminal Stage 98 date/mirror-path immutability; preserves transition safety, Stage 05 stability, Release exclusion, and every unrelated decision | [Spec 052](../../03.specs/0052-document-taxonomy-consolidation/spec.md) |
