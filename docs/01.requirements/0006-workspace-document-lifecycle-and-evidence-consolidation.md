---
title: 'Workspace Document Lifecycle and Evidence Consolidation Requirement Package'
version: "1.0"
type: sdlc/requirement-package
layer: "01.requirements"
status: superseded
owner: platform
updated: 2026-07-28
artifact_id: "REQ-0006"
superseded_by: REQ-0008
---

# Workspace Document Lifecycle and Evidence Consolidation Requirement Package

## Overview

This completed program consolidates the repository document lifecycle after
the document-assurance modernization. Specs 034 through 040 and the integrated
repository-static program contract are closed by exact terminal closure commit
`c5adc27b13893d7cbd1266c9225372cfb7df79e9`. That commit preserves the existing
profile registry, strict zero-route-debt baseline, archive preservation,
execution retention, reference currentness, and CI evidence without promoting
protected, hosted, provider, remote, or live `DEFER` evidence.

The program is evidence-first. Historical audit observations remain pinned to
their observation commit, accepted decisions remain immutable, and destructive
movement occurs only when a source blob, lineage owner, replacement relation,
and rollback path are all known.

## Vision

Contributors and AI agents can identify the current requirement, architecture,
specification, execution record, operational owner, reference snapshot, and
historical record for any governed scope without treating old evidence as
current policy or relying on Git object retention alone.

## Problem Statement

At program start, governed Markdown passed structural validation but several
semantic gaps remained: Spec 033 was modeled as an eighth original tranche,
archive bodies depended on Git history, completed execution controls remained
in the active working set, Current audit dispositions lagged implementation,
and lifecycle facts were repeated outside their machine owner.

Specs 034 through 040 close those implementation gaps with repository-static
evidence. Exact terminal closure commit
`c5adc27b13893d7cbd1266c9225372cfb7df79e9` proves the integrated strict
contract, reconciles the Current audit, preserves explicit external `DEFER`
boundaries, and transitions PRD-0006, AD-0009, ADR-0020, Spec 040, and its
reciprocal execution pair atomically. Explicit-ref lifecycle from parent
`35d8552ba423e3e2d92294ddeb81674392b8f333` to the closure commit and
clean-tree repository-static aggregate passed; this evidence-update commit is
unidentified and unclaimed.

## Personas

- **Repository contributor**: needs deterministic routing, status, and
  completion rules before authoring or moving a document.
- **Platform operator**: needs current runbooks and policies separated from
  historical execution evidence and non-authoritative research.
- **Documentation maintainer**: needs one schema owner and a bounded migration
  process that does not rewrite accepted or completed evidence.
- **AI agent and reviewer**: need affected validation, full-corpus closure
  gates, explicit DEFER semantics, and reproducible rollback evidence.
- **Audit reader**: needs observation-time facts separated from current
  remediation disposition.

## Key Use Cases

- A new program records original tranches and later follow-up Specs without
  changing the accepted historical tranche decision.
- A completed execution lineage moves its Plan and Task out of the active
  working set while preserving the exact original source payload.
- A reader resolves an archived document through one index and can verify the
  payload against its source commit, blob, and SHA-256 digest.
- A document status change is rejected when the transition or required
  evidence is not allowed for that document family.
- A reference maintainer can distinguish Current, Historical, generated,
  source-checked, and learning material without creating a second policy owner.
- An AI agent runs affected checks during work and the complete pre-commit lane
  before a logical commit, with unsupported live evidence reported as DEFER.

## Functional Requirements

| Requirement ID | Requirement | Priority | Verification intent |
| --- | --- | --- | --- |
| REQ-0006-FR-0001 | Preserve document-profiles.json as the sole machine owner of routes, frontmatter, lifecycle domains, templates, body contracts, current packs, and program lineage. | Must | Strict registry validation resolves every governed path exactly once. |
| REQ-0006-FR-0002 | Represent Spec 033 as a completed follow-up to the seven Specs fixed by ADR-0016, not as an eighth original tranche. | Must | Registry and reciprocal document checks distinguish tranches from follow-ups. |
| REQ-0006-FR-0003 | Define closed, profile-specific metadata and state-transition contracts without adding consumer-free relationship keys. | Must | Positive and negative fixtures cover allowed values, transitions, and evidence. |
| REQ-0006-FR-0004 | Replace retired metadata-only archive stubs with one non-authoritative full-body archive record per original path. | Must | Existing 31 records recover exact payloads with commit, blob, and digest evidence. |
| REQ-0006-FR-0005 | Keep current SDLC owners separate from archive records and prohibit archive reactivation. | Must | Owner and transition validators reject archive-as-current and archived-to-active cases. |
| REQ-0006-FR-0006 | Move eligible completed Plans and Tasks from closed lineages to the archive while preserving current Specs and accepted architecture decisions. | Must | A migration ledger proves eligibility, movement, links, and rollback per lineage. |
| REQ-0006-FR-0007 | Enforce lifecycle-based active-stage cardinality instead of arbitrary folder file-count limits. | Must | Current-owner, active Plan/Task, and closed-lineage residue fixtures pass. |
| REQ-0006-FR-0008 | Clarify audit, research, data, generated wiki, learning, archive, and scratch authority boundaries and consolidate only genuine duplicate current owners. | Must | Current-pack, generated-output, source-freshness, and duplicate-owner checks pass. |
| REQ-0006-FR-0009 | Keep _workspace limited to ignored, temporary, non-secret repository-support staging and reject tracked scratch children. | Must | Git-metadata checks pass without reading ignored children. |
| REQ-0006-FR-0010 | Align GitHub CI with affected fast lanes, full-document escalation, an always-running aggregate verdict, explicit artifact retention, and least privilege. | Must | Workflow fixtures and native linters pass with no remote-state claim. |
| REQ-0006-FR-0011 | Require logical commits, independent subagent review, full-corpus QA, and revertable migration boundaries. | Must | Commit, review, validation, and closure evidence are linked from each tranche. |
| REQ-0006-NFR-0001 | Preserve protected surfaces, secret boundaries, and live-system approval constraints during all migrations. | Must | Static checks pass and remote/live work is recorded as DEFER unless separately approved. |
| REQ-0006-NFR-0002 | Reconcile current Guide, Policy, Runbook, Incident, Postmortem, and helper Tests roles, frontmatter, sections, duplicate ownership, and stale semantic claims without fabricating operations evidence. | Must | Stage 05 and helper-profile audits report zero unresolved current contract conflicts or unowned exceptions. |

## Success / Acceptance Criteria

- **ACC-WDLEC-001**: Registry validation reports zero uncovered or ambiguous
  governed documents and zero duplicate current owners.
- **ACC-WDLEC-002**: The machine lineage records Specs 026-032 as the seven
  original tranches and Spec 033 as a follow-up.
- **ACC-WDLEC-003**: Every document family rejects unsupported frontmatter
  keys, values, ordering, and transitions through independent fixtures.
- **ACC-WDLEC-004**: All 31 retired metadata-only archive stubs are replaced by full-body
  archive records whose payloads match recoverable source blobs; missing and
  ambiguous recoveries are zero.
- **ACC-WDLEC-005**: All historical payload links resolve in their source-tree
  context, and all current working-tree links resolve in the current context.
- **ACC-WDLEC-006**: Every completed Plan and Task is either archived after a
  proven closed lineage or retained with a machine-readable DEFER reason and
  follow-up owner.
- **ACC-WDLEC-007**: Current audit and research pointers are unique; historical
  snapshots remain immutable; generated wiki drift is zero.
- **ACC-WDLEC-008**: Workflow security, artifact retention, affected selection,
  aggregate verdict, repository quality, and all-files pre-commit gates pass.
- **ACC-WDLEC-009**: Remote Actions, branch protection, live Kubernetes,
  Vault, ESO, Argo CD, and secret evidence are never inferred from local static
  PASS results.
- **ACC-WDLEC-010**: Current operations and helper Tests documents have one
  role-specific contract, zero duplicate current owners, zero unsupported
  metadata or sections, and explicit exceptions for absent real incidents.

## Scope and Non-goals

- **In scope**: _workspace; .github; Stages 01 through 05, 90, 98, and 99;
  document contracts, templates, validators, fixtures, indexes, migration
  ledgers, and the repository-static QA surfaces required to enforce them.
- **Protected-surface scope**: Contract and governance changes are authorized,
  including destructive consolidation, when source preservation and rollback
  evidence exist.
- **Out of scope**: Reading ignored scratch, credentials, tokens, auth files,
  kubeconfigs, shell history, personal diagnostics, or secret-bearing logs.
- **Non-goals**: Renumbering historical documents; rewriting accepted ADR
  bodies; treating references as active policy; treating Actions artifacts as
  durable records; remote publication or live-system mutation.

## Risks, Dependencies, and Assumptions

- Archive conversion must verify the exact source tree before replacing a
  retired metadata-only stub; a missing source is a blocker rather than an invitation to
  reconstruct prose.
- Moving execution records can break current traceability unless index anchors
  and closure evidence change in the same logical commit.
- Retired archive and compatibility forms may remain only as finite,
  identity-pinned, fail-closed proof fixtures; active readers stay strict-only.
- Program Specs use active to mean an approved current technical contract.
  Active status does not authorize concurrent execution; predecessor
  acceptance and the creation of the owning Plan and Task open each tranche.
- Git and GitHub object retention are not substitutes for a tracked archive
  payload; secret-removal procedures remain an explicit preservation exception.
- Current audit facts remain pinned to their observation SHA. Only remediation
  overlays may report later closure.
- The earlier FIFO self-test portability defect was remediated before terminal
  closure commit `c5adc27b13893d7cbd1266c9225372cfb7df79e9`;
  repository-static PASS still does not establish hosted, provider, remote, or
  live readiness.

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-0006-FR-0001 | ACC-WDLEC-001 | [AD-0009](../02.architecture/descriptions/0009-document-lifecycle-evidence-operating-model.md) and [Spec 034](../03.specs/0034-authority-and-lineage-foundation/spec.md) |
| REQ-0006-FR-0002 | ACC-WDLEC-002 | N/A — Spec 034 shares the downstream owner linked in REQ-0006-FR-0001 and is governed by unchanged accepted ADR-0017. |
| REQ-0006-FR-0003 | ACC-WDLEC-003 | [Spec 035](../03.specs/0035-document-schema-and-lifecycle-contract/spec.md) |
| REQ-0006-FR-0004 | ACC-WDLEC-004 | [Spec 036](../03.specs/0036-archive-record-and-workspace-boundary/spec.md), governed by ADR-0018 |
| REQ-0006-FR-0005 | ACC-WDLEC-005 | N/A — Spec 036 shares the downstream owner linked in REQ-0006-FR-0004. |
| REQ-0006-FR-0006 | ACC-WDLEC-006 | [Spec 037](../03.specs/0037-active-corpus-and-execution-retention/spec.md) |
| REQ-0006-FR-0007 | ACC-WDLEC-006 | N/A — Spec 037 shares the downstream owner linked in REQ-0006-FR-0006. |
| REQ-0006-FR-0008 | ACC-WDLEC-007 | [Spec 038](../03.specs/0038-reference-information-architecture/spec.md) |
| REQ-0006-FR-0009 | ACC-WDLEC-001 | N/A — Spec 036 shares the downstream owner linked in REQ-0006-FR-0004. |
| REQ-0006-FR-0010 | ACC-WDLEC-008 | [Spec 039](../03.specs/0039-github-ci-qa-evidence/spec.md) |
| REQ-0006-FR-0011 | ACC-WDLEC-008 | [Spec 040](../03.specs/0040-contract-cutover-and-program-closure/spec.md) |
| REQ-0006-NFR-0001 | ACC-WDLEC-009 | N/A — Spec 040 shares the downstream owner linked in REQ-0006-FR-0011 and retains external `DEFER`. |
| REQ-0006-NFR-0002 | ACC-WDLEC-010 | N/A — Specs 035 and 037 share the downstream owners linked in REQ-0006-FR-0003 and REQ-0006-FR-0006. |
