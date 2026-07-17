---
title: 'Archive Record and Workspace Boundary Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-07-18
---

# Archive Record and Workspace Boundary Technical Specification (Spec)

## Overview

This Spec implements ADR-0018 by replacing 31 metadata-only Tombstones with
one full-body content/archive record per original path. It also aligns the
archive index, template, validators, historical-link resolution, and
_workspace scratch boundary with the preservation model.

## Strategic Boundaries & Non-goals

- **In scope**: docs/98.archive, the archive form and support contracts,
  archive profiles, recovery tooling, link validation, indexes, fixtures,
  _workspace rules, and directly affected Stage 00/.github descriptions.
- **Non-goals**: Moving the remaining completed Plans and Tasks, reading
  ignored scratch, preserving secrets, restoring archive records as current,
  or rewriting historical payload links.

## Contracts

- Each original path has exactly one mirrored content/archive record.
- Archive frontmatter uses the approved closed provenance fields and order.
- The complete original source is preserved as an immutable payload.
- Payload identity is proven by source_commit, source_blob, and content_sha256.
- Payload links resolve against source_commit and original_path.
- Active documents use the archive index, not individual archive records, as
  the current navigation boundary.
- Only _workspace/README.md is tracked; ignored children are not inspected.

## Core Design

Recovery reads the exact original blob from the parent tree that still
contained original_path. The dry run records the source and digest, proves the
blob exists, parses historical links in source context, and compares the
planned archive path with the mirror rule.

The write phase replaces the Tombstone body with a canonical archive envelope
and byte-preserved payload. It updates the archive index and profile/template
contract in the same logical commit. The old Tombstone profile and form are
then removed rather than retained as a second archival role.

For the existing corpus, 26 source files resolve from commit
5e0221525450dbdacb585e6c98ade3f060ddc827 and five resolve from
82f0e1922d9748a88b1487a32a59629ba523f408. All 31 blobs and all 202 historical
local links are recoverable in those trees.

## Data Modeling & Storage Strategy

The archive envelope uses the versioned ArchiveEnvelope.v1 grammar. Canonical
UTF-8/LF archive frontmatter is followed immediately by the single line
archive marker:

    <!-- archive-envelope:v1 payload=rest-of-file encoding=git-blob-bytes -->

The next byte begins the payload and every remaining byte through EOF belongs
to it. There is no closing delimiter, so payload content cannot collide with
the envelope grammar. The payload is copied from the Git blob, not from a
line-ending-converted working-tree read; no byte or final newline is added.
The SHA-256 covers exactly those remaining bytes. The full source_blob ID
independently identifies the same payload and supplies the expected byte size.
Only UTF-8 Markdown source blobs are admitted by this profile; a non-UTF-8
source is BLOCKED for a separately designed binary archive format.

Archive reason is one of superseded, consolidated, completed-lineage, retired,
abandoned, or duplicate. Replacement is a current repository path only for
reasons that require one; otherwise it is null.

Temporary recovery inventories may exist under ignored _workspace during a
dry run. Durable recovery and migration evidence is promoted to the owning
Plan, Task, archive index, or program closure record.

## Interfaces & Data Structures

- Recovery check: original path plus source commit produces blob, byte count,
  SHA-256, link count, and proposed archive metadata.
- Archive validator: envelope schema, payload delimiter, digest, Git object,
  mirror path, reason dependency, and immutability.
- Envelope parser: exact v1 marker position, payload-to-EOF extraction, UTF-8
  admission, Git blob byte equality, final-newline preservation, and digest.
- Historical link validator: source tree plus original base path.
- Current link validator: current working tree, with active-to-individual
  archive links rejected.
- Workspace validator: Git metadata only; tracked child and force-add attempts
  fail.

## Edge Cases & Error Handling

- Missing or ambiguous source blobs block migration.
- A payload digest mismatch fails even when prose appears equivalent.
- A secret-bearing source invokes the approved secret-removal path and is not
  preserved by this workflow.
- Obsolete historical links remain valid when they resolve in the source tree;
  they are not rewritten to current locations.
- A replacement that later changes does not mutate archive-time metadata.

## Failure Modes & Fallback / Human Escalation

- If exact bytes cannot be recovered, retain the Tombstone temporarily and
  report BLOCKED with the missing provenance.
- If an archive body is modified after creation, restore it from source or
  record a separately approved provenance repair; do not recalculate the digest
  to hide the change.
- If _workspace contains ignored local state, do not list, open, hash, move, or
  delete it during repository validation.

## Verification Commands

- Run archive recovery in check mode for all 31 records.
- Verify source blobs, SHA-256 digests, mirror paths, and 202 historical links.
- Run archive schema, current link, and workspace metadata fixtures.
- Run strict registry, Markdown, owner/link, repository quality, and all-files
  pre-commit checks.

## Success Criteria & Verification Plan

- **VAL-ARWB-001**: Exact source recovery succeeds for 31 of 31 Tombstones.
- **VAL-ARWB-002**: Every migrated archive record has valid closed metadata,
  blob identity, and payload SHA-256.
- **VAL-ARWB-003**: Historical payload links resolve 202 of 202 in source
  context; current links remain unbroken.
- **VAL-ARWB-004**: Tombstone form, profile, and duplicate archival role are
  absent after cutover.
- **VAL-ARWB-005**: Archive reactivation, payload mutation, invalid reason
  dependency, and active direct-link fixtures fail.
- **VAL-ARWB-006**: _workspace has one tracked README and no validation reads
  ignored children.
- **VAL-ARWB-007**: ArchiveEnvelope.v1 round-trips payloads containing marker
  text, Markdown fences, frontmatter, empty final lines, and no final newline
  without changing any source blob byte.

## Traceability

- **Predecessor**: [Spec 035](../035-document-schema-and-lifecycle-contract/spec.md)
- **Successor**: [Spec 037](../037-active-corpus-and-execution-retention/spec.md)
- **Archive decision**: [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)
- **PRD**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **ARD**: [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- **Plan**: [Archive Record and Workspace Boundary Implementation Plan](../../04.execution/plans/2026-07-17-archive-record-and-workspace-boundary.md)
- **Task**: [Archive Record and Workspace Boundary Task](../../04.execution/tasks/2026-07-17-archive-record-and-workspace-boundary.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-WDLEC-004](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ARWB-001 | Recovery check enumerates exact source commit and blob per path. |
| [REQ-WDLEC-004](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ARWB-002 | Archive schema and digest validation inspect every record. |
| [REQ-WDLEC-005](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ARWB-003 | Dual current and historical link lanes report zero misses. |
| [REQ-WDLEC-004](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ARWB-004 | Registry-derived form inventory and stale-route scan prove removal. |
| [REQ-WDLEC-005](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ARWB-005 | Negative archive fixtures reject authority and integrity violations. |
| [REQ-WDLEC-009](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ARWB-006 | Git metadata assertions verify the scratch boundary. |
| [REQ-WDLEC-004](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ARWB-007 | Envelope parser round-trip fixtures compare extracted bytes with source blobs. |
