---
title: 'Workspace Document Lifecycle and Evidence Consolidation Product Requirements'
type: sdlc/prd
status: active
owner: platform
updated: 2026-07-15
---

# Workspace Document Lifecycle and Evidence Consolidation Product Requirements

## Overview

This program consolidates the repository document lifecycle after the completed
document-assurance modernization. It preserves the existing profile registry
and strict zero-route-debt baseline while closing the remaining gaps in
program lineage, state-transition evidence, archive preservation, execution
retention, reference currentness, and CI evidence.

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

The repository now routes all governed Markdown through a machine-readable
profile and passes strict structural validation, but several semantic gaps
remain. The program registry incorrectly counts completed Spec 033 as an
eighth original tranche despite ADR-0016 fixing seven tranches. Archive files
are metadata-only Tombstones, so their bodies depend on Git history. Completed
Plans and Tasks remain in the active execution stage after their lineages
close. Current audit dispositions lag implementation evidence. The lifecycle
state table is repeated outside its machine owner, and the repository quality
self-test assumes FIFO support that is absent in the current filesystem.

Leaving these gaps unresolved makes historical preservation, active-owner
selection, and QA outcomes dependent on conventions that are not consistently
machine-verifiable.

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
| REQ-WDLEC-001 | Preserve document-profiles.json as the sole machine owner of routes, frontmatter, lifecycle domains, templates, body contracts, current packs, and program lineage. | Must | Strict registry validation resolves every governed path exactly once. |
| REQ-WDLEC-002 | Represent Spec 033 as a completed follow-up to the seven Specs fixed by ADR-0016, not as an eighth original tranche. | Must | Registry and reciprocal document checks distinguish tranches from follow-ups. |
| REQ-WDLEC-003 | Define closed, profile-specific metadata and state-transition contracts without adding consumer-free relationship keys. | Must | Positive and negative fixtures cover allowed values, transitions, and evidence. |
| REQ-WDLEC-004 | Replace metadata-only Tombstones with one non-authoritative full-body archive record per original path. | Must | Existing 31 records recover exact payloads with commit, blob, and digest evidence. |
| REQ-WDLEC-005 | Keep current SDLC owners separate from archive records and prohibit archive reactivation. | Must | Owner and transition validators reject archive-as-current and archived-to-active cases. |
| REQ-WDLEC-006 | Move eligible completed Plans and Tasks from closed lineages to the archive while preserving current Specs and accepted architecture decisions. | Must | A migration ledger proves eligibility, movement, links, and rollback per lineage. |
| REQ-WDLEC-007 | Enforce lifecycle-based active-stage cardinality instead of arbitrary folder file-count limits. | Must | Current-owner, active Plan/Task, and closed-lineage residue fixtures pass. |
| REQ-WDLEC-008 | Clarify audit, research, data, generated wiki, learning, archive, and scratch authority boundaries and consolidate only genuine duplicate current owners. | Must | Current-pack, generated-output, source-freshness, and duplicate-owner checks pass. |
| REQ-WDLEC-009 | Keep _workspace limited to ignored, temporary, non-secret repository-support staging and reject tracked scratch children. | Must | Git-metadata checks pass without reading ignored children. |
| REQ-WDLEC-010 | Align GitHub CI with affected fast lanes, full-document escalation, an always-running aggregate verdict, explicit artifact retention, and least privilege. | Must | Workflow fixtures and native linters pass with no remote-state claim. |
| REQ-WDLEC-011 | Require logical commits, independent subagent review, full-corpus QA, and revertable migration boundaries. | Must | Commit, review, validation, and closure evidence are linked from each tranche. |
| REQ-WDLEC-012 | Preserve protected surfaces, secret boundaries, and live-system approval constraints during all migrations. | Must | Static checks pass and remote/live work is recorded as DEFER unless separately approved. |

## Success / Acceptance Criteria

- **ACC-WDLEC-001**: Registry validation reports zero uncovered or ambiguous
  governed documents and zero duplicate current owners.
- **ACC-WDLEC-002**: The machine lineage records Specs 026-032 as the seven
  original tranches and Spec 033 as a follow-up.
- **ACC-WDLEC-003**: Every document family rejects unsupported frontmatter
  keys, values, ordering, and transitions through independent fixtures.
- **ACC-WDLEC-004**: All 31 existing Tombstones are replaced by full-body
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
  Tombstone; a missing source is a blocker rather than an invitation to
  reconstruct prose.
- Moving execution records can break current traceability unless index anchors
  and closure evidence change in the same logical commit.
- A compatibility window is required while the old Tombstone profile and the
  full-body archive profile coexist on the implementation branch.
- Git and GitHub object retention are not substitutes for a tracked archive
  payload; secret-removal procedures remain an explicit preservation exception.
- Current audit facts remain pinned to their observation SHA. Only remediation
  overlays may report later closure.
- The existing FIFO self-test failure is an environment-portability defect and
  must not be relabeled as a passing baseline.

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-WDLEC-001 | ACC-WDLEC-001 | [ARD-0009](../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md) and [Spec 034](../03.specs/034-authority-and-lineage-foundation/spec.md) |
| REQ-WDLEC-002 | ACC-WDLEC-002 | [Spec 034](../03.specs/034-authority-and-lineage-foundation/spec.md), governed by ADR-0017 |
| REQ-WDLEC-003 | ACC-WDLEC-003 | [Spec 035](../03.specs/035-document-schema-and-lifecycle-contract/spec.md) |
| REQ-WDLEC-004 | ACC-WDLEC-004 | [Spec 036](../03.specs/036-archive-record-and-workspace-boundary/spec.md), governed by ADR-0018 |
| REQ-WDLEC-005 | ACC-WDLEC-005 | [Spec 036](../03.specs/036-archive-record-and-workspace-boundary/spec.md) |
| REQ-WDLEC-006 | ACC-WDLEC-006 | [Spec 037](../03.specs/037-active-corpus-and-execution-retention/spec.md) |
| REQ-WDLEC-007 | ACC-WDLEC-006 | [Spec 037](../03.specs/037-active-corpus-and-execution-retention/spec.md) |
| REQ-WDLEC-008 | ACC-WDLEC-007 | [Spec 038](../03.specs/038-reference-information-architecture/spec.md) |
| REQ-WDLEC-009 | ACC-WDLEC-001 | [Spec 036](../03.specs/036-archive-record-and-workspace-boundary/spec.md) |
| REQ-WDLEC-010 | ACC-WDLEC-008 | [Spec 039](../03.specs/039-github-ci-qa-evidence/spec.md) |
| REQ-WDLEC-011 | ACC-WDLEC-008 | [Spec 040](../03.specs/040-contract-cutover-and-program-closure/spec.md) |
| REQ-WDLEC-012 | ACC-WDLEC-009 | [Spec 040](../03.specs/040-contract-cutover-and-program-closure/spec.md) |
