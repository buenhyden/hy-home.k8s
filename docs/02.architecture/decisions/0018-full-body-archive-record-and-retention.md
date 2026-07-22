---
title: 'ADR-0018: Full-body Archive Record and Retention'
type: sdlc/adr
status: accepted
owner: platform
updated: 2026-07-19
---

# ADR-0018: Full-body Archive Record and Retention

## Overview

This decision replaces metadata-only archive Tombstones with one immutable,
non-current, full-body archive record at each mirrored original path.

## Context

The current archive keeps path, date, reason, replacement, and a prose summary
but deliberately discards the original body. Git object availability is not a
permanent records contract: unreachable objects can be pruned, reflogs expire,
and history rewriting changes commit identity. All 31 current Tombstones are
recoverable exactly from two source trees, including their 202 historical local
links, so the repository can migrate without invented reconstruction.

## Decision

- Replace content/archive-tombstone with the non-authoritative
  content/archive document type.
- Preserve the complete original source as an immutable payload inside a
  canonical archive envelope.
- Record original_type, original_path, archived_on, archive_reason,
  replacement, source_commit, source_blob, and content_sha256.
- Treat envelope replacement as immutable archive-time provenance. The archive
  index alone owns later current-replacement evolution and may select only a
  stage-zero regular index entry whose exact bounded Git-blob bytes parse as a
  registry-classified authored document in a current state; worktree bytes,
  another archive, template, missing, unselected, draft, or archived target
  are not current authority.
- Resolve payload links against source_commit and original_path, not the
  current mirrored archive location.
- Permit only the finite reasons superseded, consolidated, completed-lineage,
  retired, abandoned, and duplicate.
- Require replacement for superseded, consolidated, and duplicate; require an
  explicit null value for other reasons.
- Keep exactly one archive record per original path and prohibit a parallel
  Tombstone.
- Treat secret-bearing history as an exception governed by secret removal,
  not by ordinary preservation.

## Explicit Non-goals

- Making archive records current SDLC owners.
- Rewriting historical links to look current.
- Restoring archived documents to active status.
- Preserving secrets or credentials for completeness.
- Using Actions artifacts or ignored local files as the durable archive.

## Consequences

- Historical content, context, structure, and links remain reproducible from
  tracked repository state.
- Archive validation becomes source-tree aware and must verify both Git and
  tool-independent hashes.
- Archive files grow, but the active working set can shrink without losing
  evidence.
- Metadata corrections require an explicit provenance-repair process; ordinary
  replacement evolution belongs only in the archive index and never requires
  envelope/index replacement equality.

## Alternatives

- **Keep metadata-only Tombstones**: rejected because durable content depends
  on object retention outside the archive contract.
- **Keep original SDLC type with status archived**: rejected because it weakens
  the current-versus-historical authority boundary.
- **Store a Tombstone and a separate snapshot**: rejected because it creates
  two files with the same archival role.

Official preservation principles support keeping content, context, structure,
and record relationships together. Git documents that reflogs expire and
unreachable objects may be pruned:

- https://www.archives.gov/records-mgmt/policy/managing-web-records.html
- https://git-scm.com/docs/git-reflog
- https://git-scm.com/docs/git-gc.html

## Traceability

- **Requirement**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **Architecture**: [ARD-0009](../requirements/0009-document-lifecycle-evidence-operating-model.md)
- **Archive implementation**: [Spec 036](../../03.specs/036-archive-record-and-workspace-boundary/spec.md)
- **Execution retention**: [Spec 037](../../03.specs/037-active-corpus-and-execution-retention/spec.md)

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| Existing metadata-only archive decision | Supersedes the Tombstone-only storage model | [Spec 036](../../03.specs/036-archive-record-and-workspace-boundary/spec.md) |
