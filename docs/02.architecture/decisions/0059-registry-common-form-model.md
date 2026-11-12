---
title: "Registry Common Form Model"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-11-12"
layer: "architecture"
artifact_id: "ADR-0059"
---

# ADR-0059: Registry Common Form Model

## Overview

This accepted amendment adds optional keys to the generation-10 Stage 99
registry so it can carry one common document form per role. It amends the
current-state clarification of accepted
[ADR-0033](./0033-common-document-contract-v9.md), which lists the generation-10
top-level keys. ADR-0033 keeps its body; this decision amends it, as ADR-0058
amended ADR-0036. Every other ADR-0033 clause stays.

The current user accepted this decision on 2026-11-12. The acceptance is
recorded in the SPEC-0168 Task. It accepts no SPEC-0168 criterion by itself.

## Context

The external v14.7 execution package's W03 stage requires the approved registry
itself to carry the COMMON-DOC-FORM-1 section contract (H2 and H3 with section
IDs, parents, order, conditions, required and prohibited content and empty
policy), a TemplateDefinition for every template, a document-role binding (one
Policy role for `governance/rule` and `operation/policy`), and shared-contract
approval fields with an `approved` stage. On 2026-11-12 the user ruled that
current v14.7 requirements prevail over conflicting existing rules (SPEC-0161
Task, EVD-018) and decided W03-D01 to W03-D05 (EVD-025, EVD-026). The
generation-10 registry models required and optional H2 lists only, and the
non-delegable authority guard admits an exact profile key set.
[REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md)
makes the registry the single machine owner of document form;
[AD-0006](../descriptions/0006-workspace-agent-governance-platform.md) is the
governance view.

## Decision

1. **Top-level keys.** `schema_version` stays 10, as it did when
   `readme_navigation`, `document_language` and `shared_contract` were added
   as optional keys. The top-level keys are
   `$schema`, `$id`, `schema_version`, `profiles`, `lifecycle_domains`,
   `readme_navigation`, `document_language`, `shared_contract` and
   `common_forms`. Families and modes are unchanged.
2. **Common forms.** `common_forms` holds one form per common document role,
   each a section tree as in COMMON-DOC-FORM-1, plus named extensions with
   condition, owner, verification, review and removal. A role receives its form
   only in the change that moves its documents.
3. **Profile keys.** A profile may carry `document_role` and, for a template
   profile, `template_definition`. The authority guard admits them as optional
   keys and keeps its ban on agent fields.
4. **Shared contract.** The record carries `approved_by`, `approved_at`,
   `scope`, `effective_from`, `migration`, `rollback` and `consumer_version`,
   and its stage is `candidate`, `approved` or `adopted`. An approval fact that
   is not on record is `unverified`, never inferred.
5. **Bounded coexistence.** The H2 lists stay only for profiles
   whose role has no form yet; the change that moves the last role removes
   them and their checks.
6. **Decision makers and confirmation.** The current user decides acceptance;
   compliance is confirmed by the registry, Markdown profile and lifecycle
   validators and the SPEC-0168 Task.

## Explicit Non-goals

- Editing ADR-0033's body or any other ADR-0033 clause.
- Changing any current document's headings in the change that adopts this
  decision.
- A document generator; templates stay hand-copied and checked.
- Moving `docs/99.templates/` (Q-08 keeps the path).

## Consequences

- **Positive:** one registry carries the same form for every document of a
  role, and the Policy role, template definitions and contract approval facts
  become machine-readable.
- **Trade-off:** two heading models coexist until the last role moves, so
  readers must check whether a profile has a form.
- **Follow-up:** each role's form arrives with the change that moves its
  documents; the ADR family keeps its current form for accepted ADRs until each
  is replaced (W03-D02).

## Alternatives

- **Bump to generation 11:** rejected; the fail-closed pre-edit guard and the
  history reader pin generation 10, and earlier optional keys were added
  without a bump.
- **Add keys without amending ADR-0033:** rejected; its current key list would
  become false.
- **A separate form file beside the registry:** rejected; two machine owners of
  document form would contradict REQ-0003-FR-0012.
- **A bare `role` key:** rejected; the authority guard reserves agent field
  names.

## Traceability

- **Requirements:** [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md), [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md).
- **Architecture:** [AD-0006](../descriptions/0006-workspace-agent-governance-platform.md).
- **Change:** N/A — SPEC-0168 left the tree; Git history recovers it. Its acceptance and exact source are summarized in [REQ-0003 Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage).

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0033](./0033-common-document-contract-v9.md) | Amends only the current-state key list; every other clause stays | N/A — SPEC-0168 left the tree; Git history recovers it |
