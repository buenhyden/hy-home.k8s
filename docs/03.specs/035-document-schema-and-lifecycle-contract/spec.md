---
title: 'Document Schema and Lifecycle Contract Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-07-15
---

# Document Schema and Lifecycle Contract Technical Specification (Spec)

## Overview

This Spec advances the registry to a closed, profile-specific schema for
frontmatter values, ordering, lifecycle states, transitions, transition
evidence, template parity, and full-document validation. It preserves the
five-key baseline for ordinary Markdown and defines archive metadata as a
single justified extension.

## Strategic Boundaries & Non-goals

- **In scope**: Stage 99 registry/schema/support/forms, Stage 00 routing
  summaries, profile validators, transition comparison, fixtures, and current
  draft/active authored consumers.
- **Non-goals**: Adding universal identifiers, relationship arrays, reviewers,
  or schema-version frontmatter; rewriting immutable evidence; converting the
  archive corpus; changing native GitHub or API contracts into Markdown.

## Contracts

- Ordinary authored Markdown uses title, type, status, owner, and updated in
  repository order.
- Allowed types, states, values, sections, and conditional evidence are owned
  by the selected registry profile.
- Unknown keys and additional schema properties fail.
- Status transitions are family-specific and compared against the base change.
- Archive is one content/archive profile with a closed provenance extension.
- Forms provide copyable shape; support documents explain rationale; neither
  duplicates the complete registry inventory.

## Core Design

The state model distinguishes product, architecture, decision, specification,
execution, operations, reference, template, and archive roles. Forward
transitions require the profile's evidence owner. Reverse transitions create a
successor document rather than reopening terminal evidence. Archive has only
the archived state.

Validation uses base-to-proposed comparison for changed status. A transition
must be allowed and must change or cite the owning Plan, Task, ADR, closure
record, or archive index in the same change. The validator returns a stable
rule ID, path, profile, expected transition, observed transition, and evidence
gap.

## Data Modeling & Storage Strategy

Registry objects remain closed JSON Schema objects. Status graphs, conditional
fields, archive reason dependencies, body-contract status scope, and validator
escalation are declarative data. Exhaustive inventory checks derive from the
registry; independent mutation fixtures do not copy the production inventory.

Compatibility is explicit and temporary. The old Tombstone profile may remain
readable until Spec 036 migrates every record, but new authored Tombstones are
rejected.

## Interfaces & Data Structures

- Registry loader: one parse per validator process with schema version check.
- Profile selector: exact-one route or explicit native exception.
- Frontmatter validator: key order, type, enum, pattern, required, conditional,
  and placeholder checks.
- Transition validator: base status, proposed status, allowed edge, evidence
  paths, and immutable-body guard.
- Form validator: source-profile parity plus template-only prompt allowance.

GitHub issue forms, workflow YAML, CODEOWNERS, PR templates, OpenAPI, GraphQL,
and protobuf keep native validation and do not acquire SDLC frontmatter.

## Edge Cases & Error Handling

- A file with valid global status but invalid family status fails.
- A changed status with no accessible base is reported as a comparison DEFER,
  not silently passed.
- An archive reason requiring replacement rejects null; reasons not requiring a
  replacement reject a path value.
- Template placeholders are valid only in template profiles.
- Historical payload text is excluded from active contract-residue scans.

## Failure Modes & Fallback / Human Escalation

- If a profile cannot express a rule without executable code, add a named
  validator capability rather than arbitrary registry expressions.
- If transition evidence conflicts with immutable history, create a successor
  record and escalate the relation decision.
- If compatibility weakens production enforcement outside migration paths,
  stop and combine the affected schema and migration changes atomically.

## Verification Commands

- Run registry schema self-tests and mutation probes.
- Run strict Markdown profile and transition validation.
- Run template-to-source parity validation.
- Run link/owner and historical-body guards.
- Run repository quality and all-files pre-commit.

## Success Criteria & Verification Plan

- **VAL-DSLC-001**: Every governed document matches one closed profile.
- **VAL-DSLC-002**: Unsupported key, order, enum, pattern, conditional value,
  and placeholder fixtures fail.
- **VAL-DSLC-003**: Family-invalid status and transition fixtures fail.
- **VAL-DSLC-004**: Unexplained reverse transitions and every archive
  reactivation fail.
- **VAL-DSLC-005**: Canonical templates match their authored source profiles
  without copying governance inventories.
- **VAL-DSLC-006**: Native contract surfaces remain frontmatter-free.

## Traceability

- **Predecessor**: [Spec 034](../034-authority-and-lineage-foundation/spec.md)
- **Successors**: [Spec 036](../036-archive-record-and-workspace-boundary/spec.md), [Spec 038](../038-reference-information-architecture/spec.md), and [Spec 039](../039-github-ci-qa-evidence/spec.md)
- **PRD**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **ARD**: [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-WDLEC-001](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-DSLC-001 | Strict registry selection reports zero uncovered or ambiguous paths. |
| [REQ-WDLEC-003](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-DSLC-002 | Frontmatter mutation fixtures cover closed metadata contracts. |
| [REQ-WDLEC-003](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-DSLC-003 | Base-to-proposed lifecycle fixtures cover each family edge. |
| [REQ-WDLEC-005](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-DSLC-004 | Negative transition fixtures reject reopen and reactivation. |
| [REQ-WDLEC-003](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-DSLC-005 | Registry-derived parity checks cover Markdown forms. |
| [REQ-WDLEC-010](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-DSLC-006 | Native linters and route exceptions verify native surfaces. |
