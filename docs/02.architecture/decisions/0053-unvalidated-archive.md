---
title: "Unvalidated Archive"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-11-05"
layer: "architecture"
artifact_id: "ADR-0053"
supersedes: "ADR-0040"
---

# ADR-0053: Unvalidated Archive

## Overview

`docs/98.archive/` stops being a validated stage. No validator reads it, no
migration is recorded or proved, and Git history alone recovers a document
that left its stage. The directory keeps its README and disposition structure.

## Context

ADR-0040 kept retained
units frozen, catalogued and re-verified: a Retention Catalog with Git
envelopes, a Retention Assessment table, an ordered citation table, sealed
migration ledgers and a dedicated integrity gate. On 2026-11-03 that model
cost three registered QA gates, about 15,700 lines of archive scripts and
tests, and archive and migration branches in the link, lifecycle,
Markdown-profile, language and agent-consumer validators. Every move into the
archive needed proof, and every later validator change had to keep the frozen
generations passing.

The operator asked on 2026-11-03 to minimize and, where possible, delete
every CI/CD check of the archive's files and entries, together with the
migration checks, and then to delete the archived files and keep only the
README and structure.

## Decision

- `docs/98.archive/**` is outside the document inventory. No profile, form,
  lifecycle, link, catalog, retention, citation, assessment, envelope or
  migration rule applies to it.
- A change under it reruns only secret scanning. Its files are excluded from
  formatters and Markdown lint, and a link into it is not checked.
- A document that is no longer current leaves its stage by deletion or by a
  move into the archive. Neither needs a record; `git show <commit>:<path>`
  recovers it.
- A move between active stages keeps no migration record. Exact-blob renames
  stay denied by the lifecycle gate as before.
- The archive keeps its README and disposition directories. Its earlier
  bodies, tombstones, migration ledgers and catalog leave the tree.

## Explicit Non-goals

- Rewriting completed Task evidence or historical ADR text that describes the
  earlier model.
- Changing lifecycle states, supersession, or secret scanning for current
  documents.

## Consequences

- QA no longer selects archive gates, and validators no longer carry frozen
  generation exemptions.
- Nothing proves where an archived document came from; Git history is the
  only record. A wrong deletion is recovered from Git, not from a catalog.
- A current document links the current owner, not an archived file. An
  existing link into the archive stays unchecked, so a completed record that
  cannot be edited keeps its bytes.

## Alternatives

- **Keep the code and disable the gates.** Rejected: the operator asked for
  deletion, and dormant validators still constrain every later change.
- **Keep the archive bodies without validation.** Rejected: the operator
  asked to keep only the README and structure.

## Traceability

Requirement: REQ-0003-FR-0020 in
[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md).

**Current-state clarification (2026-11-05).** `docs/98.archive/README.md` is
still formatted and linted as the stage index; the operator-approved
[ADR-0055](./0055-governance-decision-current-state-amendment.md) (clause 7) narrows the Decision's lint exclusion to the other files.

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| ADR-0040 | Supersedes ADR-0040, removed from the decision log and summarized in AD-0006 Archived Lineage; no retention unit, catalog or citation table carries forward | N/A — SPEC-0140 left the tree; Git history recovers it |
