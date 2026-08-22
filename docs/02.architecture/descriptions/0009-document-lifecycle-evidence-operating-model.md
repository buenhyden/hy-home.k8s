---
title: 'Document Lifecycle and Evidence Operating Model Architecture Description'
type: sdlc/ad
status: accepted
owner: platform
updated: 2026-07-28
artifact_id: "AD-0009"
---

# Document Lifecycle and Evidence Operating Model Architecture Description (AD)

## Overview

This accepted architecture extends the existing document-assurance platform
without replacing its registry, profile, template, and validation foundations.
Specs 034 through 040 close its repository-static implementation, and
[ADR-0020](../decisions/0020-document-lifecycle-program-closure-evidence.md)
is the reciprocally linked same-diff accepted role-decision evidence for this
AD acceptance. Hosted, provider, remote, and live readiness remain `DEFER`;
terminal closure commit `c5adc27b13893d7cbd1266c9225372cfb7df79e9` and
parent-to-closure postflight are observed, while this evidence-update commit is
unidentified and unclaimed.

## Boundaries & Non-goals

- **Owns**: Program and follow-up lineage, profile-specific lifecycle graphs,
  archive provenance, execution retention, reference currentness, affected
  validation, strict cutover, and rollback interfaces.
- **Consumes**: PRD-0006, ADR-0015, ADR-0016, ADR-0017, ADR-0018, ADR-0020, the
  Current 2026-07-11 audit pack, Git source objects, and repository-static
  validators.
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

The exact terminal closure commit passes the repository-static traceability,
operability, and scalability frontier at active controls `0/0`, terminal
controls `6/3`, and terminal Specs `3`. Security remains split: static
boundaries pass, while its provider, remote, credential-bearing, and live
portion remains `DEFER`.

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

Registry v8 remains a closed JSON document. It adds explicit original-tranche
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
| [REQ-0006-FR-0001](../../01.requirements/0006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | Single machine authority and zero route ambiguity | [Spec 034](../../03.specs/0034-authority-and-lineage-foundation/spec.md) |
| N/A — REQ-0006-FR-0002 shares the PRD-0006 source linked in REQ-0006-FR-0001 | Monotonic original tranche plus follow-up lineage; ADR-0017 remains unchanged accepted history. | N/A — the accepted historical decision is preserved without reopening it as same-diff evidence. |
| N/A — REQ-0006-FR-0003 shares the PRD-0006 source linked in REQ-0006-FR-0001 | Closed profile metadata and transition graph | [Spec 035](../../03.specs/0035-document-schema-and-lifecycle-contract/spec.md) |
| N/A — REQ-0006-FR-0004 shares the PRD-0006 source linked in REQ-0006-FR-0001 | Byte-preserved non-current archive envelope governed by unchanged accepted ADR-0018 | [Spec 036](../../03.specs/0036-archive-record-and-workspace-boundary/spec.md) |
| N/A — REQ-0006-FR-0006 shares the PRD-0006 source linked in REQ-0006-FR-0001 | Closed-lineage execution working-set boundary | [Spec 037](../../03.specs/0037-active-corpus-and-execution-retention/spec.md) |
| N/A — REQ-0006-FR-0008 shares the PRD-0006 source linked in REQ-0006-FR-0001 | Snapshot and currentness separation | [Spec 038](../../03.specs/0038-reference-information-architecture/spec.md) |
| N/A — REQ-0006-FR-0010 shares the PRD-0006 source linked in REQ-0006-FR-0001 | Always-running aggregate and full-corpus escalation | [Spec 039](../../03.specs/0039-github-ci-qa-evidence/spec.md) |
| N/A — REQ-0006-FR-0011 shares the PRD-0006 source linked in REQ-0006-FR-0001 | Independent tranche rollback, closure, and terminal decision evidence | [ADR-0020](../decisions/0020-document-lifecycle-program-closure-evidence.md) and [Spec 040](../../03.specs/0040-contract-cutover-and-program-closure/spec.md) |
| N/A — REQ-0006-NFR-0002 shares the PRD-0006 source linked in REQ-0006-FR-0001 | Role-specific operations and helper-document integrity | N/A — Specs 035 and 037 are already linked once in their owning rows. |
