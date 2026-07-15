---
title: 'Document Lifecycle and Evidence Operating Model Architecture Reference Document'
type: sdlc/ard
status: active
owner: platform
updated: 2026-07-15
---

# Document Lifecycle and Evidence Operating Model Architecture Reference Document (ARD)

## Overview

This architecture extends the existing document-assurance platform without
replacing its registry, profile, template, and validation foundations. It
defines how current SDLC documents, immutable archive payloads, dated
references, temporary workspace support, validators, and GitHub CI exchange
authority and evidence.

## Boundaries & Non-goals

- **Owns**: Program and follow-up lineage, profile-specific lifecycle graphs,
  archive provenance, execution retention, reference currentness, affected
  validation, strict cutover, and rollback interfaces.
- **Consumes**: PRD-006, ADR-0015, ADR-0016, ADR-0017, ADR-0018, the Current
  2026-07-11 audit pack, Git source objects, and repository-static validators.
- **Does not own**: Product runtime state, secret values, remote rulesets,
  provider entitlements, live cluster readiness, or deployment approval.
- **Non-goals**: A parallel registry, a second archive copy, arbitrary
  file-count quotas, historical renumbering, or a new policy owner under
  references.

## Quality Attributes

- **Integrity**: Archive payload bytes are verified by source commit, Git blob,
  and SHA-256; current owners cannot resolve from archive records.
- **Traceability**: Original tranches, follow-ups, status transitions,
  execution closure, replacements, and DEFER outcomes have explicit owners.
- **Reliability**: Migration is fail-closed and lineage-scoped; missing source
  or ambiguous ownership prevents movement.
- **Security**: Ignored local state is not read, secret-bearing history follows
  removal procedures, workflows use least privilege, and no static check claims
  live assurance.
- **Operability**: Each tranche has an isolated Plan, Task, review, commit
  range, verification set, and revert boundary.
- **Scalability**: Active stages are bounded by current-owner and active-lineage
  cardinality rather than a repository-wide numeric cap.

## System Overview & Context

The operating flow is:

1. The registry selects one profile and lifecycle contract for a current path.
2. State-change validation compares the proposed change with its base and
   requires allowed transition evidence.
3. A closed execution lineage is evaluated by a migration ledger.
4. Eligible source files are wrapped as immutable archive payloads at mirrored
   paths and indexed once.
5. Historical links are resolved against the recorded source tree; current
   links are resolved against the working tree.
6. Affected checks provide fast feedback, while contract changes escalate to a
   full-document lane and the final aggregate verdict.

Responsibility remains separated:

- Stage 00 owns agent execution and approval policy.
- Stage 99 owns machine profiles, support rationale, and canonical forms.
- Stages 01-05 own current product, architecture, specification, execution, and
  operations facts.
- Stage 90 owns non-authoritative snapshots, inventories, and learning aids.
- Stage 98 owns immutable non-current archive records.
- _workspace owns only ignored, temporary, non-secret repository-support
  scratch.
- .github consumes repository contracts for remote QA but does not own SDLC
  policy or perform live deployment.

## Data Architecture

Registry v6 remains a closed JSON document. It adds explicit original-tranche
and follow-up relations, profile-specific transition definitions, conditional
archive metadata, and validator escalation facts without creating a second
hand-maintained projection.

An archive record is an envelope:

- canonical content/archive frontmatter;
- a byte-preserved source payload;
- original semantic type and path;
- archive date and finite reason;
- optional replacement;
- full source commit and blob identifiers;
- a SHA-256 payload digest.

Archive indexes expose current replacement and discovery links but do not
modify immutable archive-time metadata. Migration ledgers are temporary in
_workspace during dry-run and become durable execution or closure evidence
before task completion.

The design follows the official JSON Schema closed-object model and GitHub
Docs' schema-validated frontmatter practice:

- https://json-schema.org/understanding-json-schema/reference/object
- https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter

## Infrastructure & Deployment

The control plane is repository-static:

- Python, shell, and Node validators consume registry data.
- Pre-commit runs staged, affected, and all-files lanes.
- GitHub Actions always starts the required workflow, conditions internal jobs,
  and publishes one aggregate verdict.
- Archive payload checks read tracked Git objects only.
- No tranche deploys to Kubernetes, writes Vault, changes branch protection,
  publishes a release, or pushes remote commits.

GitHub Actions artifacts are bounded, non-canonical evidence. Long-lived
conclusions are committed as closure records. The changelog preview is
transient and receives an explicit seven-day retention period.

## Traceability

### Lifecycle Traceability

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-WDLEC-001](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | Single machine authority and zero route ambiguity | [Spec 034](../../03.specs/034-authority-and-lineage-foundation/spec.md) |
| [REQ-WDLEC-002](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | Monotonic original tranche plus follow-up lineage | [ADR-0017](../decisions/0017-program-follow-up-lineage-semantics.md) |
| [REQ-WDLEC-003](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | Closed profile metadata and transition graph | [Spec 035](../../03.specs/035-document-schema-and-lifecycle-contract/spec.md) |
| [REQ-WDLEC-004](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | Byte-preserved non-current archive envelope | [ADR-0018](../decisions/0018-full-body-archive-record-and-retention.md) and [Spec 036](../../03.specs/036-archive-record-and-workspace-boundary/spec.md) |
| [REQ-WDLEC-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | Closed-lineage execution working-set boundary | [Spec 037](../../03.specs/037-active-corpus-and-execution-retention/spec.md) |
| [REQ-WDLEC-008](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | Snapshot and currentness separation | [Spec 038](../../03.specs/038-reference-information-architecture/spec.md) |
| [REQ-WDLEC-010](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | Always-running aggregate and full-corpus escalation | [Spec 039](../../03.specs/039-github-ci-qa-evidence/spec.md) |
| [REQ-WDLEC-011](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | Independent tranche rollback and closure | [Spec 040](../../03.specs/040-contract-cutover-and-program-closure/spec.md) |
