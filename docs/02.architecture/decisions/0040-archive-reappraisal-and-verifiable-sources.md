---
title: "Archive Reappraisal and Verifiable Sources"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-17"
layer: "architecture"
artifact_id: "ADR-0040"
supersedes: "ADR-0039"
---

# ADR-0040: Archive Reappraisal and Verifiable Sources

## Overview

This decision revises the Stage 98 contract that ADR-0039 accepted. It
keeps ADR-0039's units, exact retention, anchor-state classes, single catalog
row, ordered citation table, and identity-tracked moves. It changes three
things: a retained unit is frozen against unapproved change rather than kept
forever, a unit's current evidential value is judged in a management table
beside the catalog rather than never, and an envelope's reachability is checked
against the default branch the decision names rather than against whatever
`HEAD` is.

It supersedes ADR-0039 as a whole. SPEC-0085 cut the registry, Archive index,
validators, and tests over to it.

## Context

A read-only survey at `980c5458` compared ADR-0039 with the registry, catalog,
and validators that implement it. The proposal Task of SPEC-0085 records each
finding with its file and line.

- Retention has no end state. ADR-0039 forbids editing, deleting, renaming, or
  recreating a retained unit, and the lifecycle gate fails any base catalog row
  or retained body that changes or leaves. A unit whose retention need has
  ended can only leave through an unreviewed commit that the gate rejects.
- Nothing records what a retained unit is worth now. A completed package whose
  result a later change replaced, or whose evidence proved wrong, still reads as
  citable `completed/` evidence. The citation table decides by class alone.
- ADR-0039 says an envelope stays reachable from the default branch. The full
  lane checks reachability from `HEAD`, and the lifecycle gate checks it from
  the comparison base. On a branch that is later squashed, both pass for a
  source commit that the default branch never receives.
- The catalog accepts a 40-character object ID only, while the lifecycle gate
  and recovery module accept the repository's object format. The catalog check
  does not detect a shallow clone; a missing object surfaces as a generic gap.
- REQ-0003-FR-0020 requires the whole body to be retained and says nothing about
  when retention may end.

## Decision

### What ADR-0039 keeps

Stage 98 keeps two kinds and six dispositions. A Stage 03 spec package, an
Incident bundle, and any other governed document are the three retention units.
The anchor's state decides the class, every other member is terminal in its own
family, and a finished unit waits in its stage until its disposition is
approved. A retained unit equals its source Git object entry for entry, links
included, and one catalog row names that object as `<commit>:<original path>`.
The sixteen link-rebased bodies and the frozen ADR-0032 generation keep their
generation. A move between active stages keeps its identity and needs no record.
Secret-bearing content follows the secret-handling process first.

### Frozen means no unapproved change

A retained unit's bytes are never edited, renamed, recreated, or partly deleted.
Exactly one change is admitted: an approved removal of the whole unit from the
current tree, after which the unit's availability is `git-history-only`. Its
catalog row stays unchanged, and its envelope stays verifiable, so Git still
recovers it. Removal is not purification: every clone and every commit that
holds the bytes keeps them.

### Current judgment sits beside the catalog

The Archive index carries a `Retention Assessment` table under the Retention
Catalog. It holds one row for a catalog unit only when that unit's judgment has
changed; a unit without a row is `unreviewed` and `retained`. A row never
repeats the envelope, the class, or a digest, and it never makes a unit
`usable` by default.

| Column             | Meaning                                                                  |
| ------------------ | ------------------------------------------------------------------------ |
| Disposition Record | The catalog row's record path, as a code span                            |
| Assessment         | `unreviewed`, `usable`, `superseded`, `withdrawn`, or `invalidated`      |
| Availability       | `retained`, `git-history-only`, or `purged`                              |
| Current Owner      | The current document that owns what the unit once owned, or `none`       |
| Decision           | The current governed document that records the judgment and its approval |
| Assessed           | The date of that judgment                                                |
| Hold               | `none`, or the current document whose obligation blocks removal          |

- `usable` means the unit's historical claims may be cited as evidence. It never
  means current authority.
- `superseded` means a later owner replaced the unit's applicability. The unit's
  completed facts stay true, and the row names that owner.
- `withdrawn` means the unit's scope was abandoned with no successor.
- `invalidated` means the unit's evidence proved wrong. It is a new judgment of
  old evidence, not a rewrite of the old state.
- Every value other than `unreviewed` and `retained` needs a Decision.
- `git-history-only` needs Hold `none`, the whole unit absent from the tree, and a
  catalog envelope that still verifies. Availability never returns to
  `retained`; bringing the content back is a new unit under a new decision.
- `purged` is reserved. It needs a security-approved history purification
  contract that this repository does not have, so a row cannot carry it.

The table's allowed values and conditions come from the Stage 99 registry, and
every validator reads them there.

### Citation checks availability first

The ordered citation table gains one rule after the index rule: a source outside
Stage 98 may not link a retained body whose assessment is `withdrawn` or
`invalidated`, or whose availability is not `retained`. It names the unit by
identifier and reaches its judgment through the index. The rule precedes the
Incident exemption. `superseded` stays citable as historical evidence, because
its facts remain true. A source under Stage 98 keeps linking anywhere, so frozen
outgoing links are never re-judged.

### An envelope is verifiable from the default branch

The registry names the default branch. Validators resolve it as the remote
tracking reference when one exists and as the local branch otherwise; when
neither exists, the check fails rather than falls back to `HEAD`. A new catalog
row's commit must already be reachable from that branch, so a unit's prepared
source is integrated before the change that retains it. Every existing row,
including a `git-history-only` row, is re-verified the same way. An object ID
has the length of the repository's object format. A shallow or partial clone,
a missing object, or an unexpected object type is a failure, never a skip.

## Explicit Non-goals

- It removes no real retained unit and records no real reappraisal. Each needs
  its own approval.
- It does not reappraise the frozen ADR-0032 generation or any record without a
  catalog row. Those have no envelope to keep recoverable, and none is invented.
- It does not change lifecycle state names or edges; a separate decision owns
  that.
- It does not define a history purification procedure.
- It does not retain ADR-0039. That disposition needs its own authorization
  after the supersession is accepted.
- It authorizes no live cluster, provider runtime, network, push, or merge
  action.

## Consequences

A unit whose retention need ended has a reviewed exit, and a unit whose evidence
proved wrong stops being cited as valid evidence without any frozen byte
changing. The catalog, its parser, and every existing row stay as they are.

The Archive index gains a table and the registry gains one contract. The
lifecycle gate gains one narrow admitted transition, so its unapproved-change
regressions must keep failing. Preparing a source on a feature branch that is
squashed is now refused at retention time instead of discovered at recovery
time, at the cost of one more integration before a retention. Mechanical checks
prove that a Decision document exists and is current; they cannot prove that
its approval is real, which stays a review obligation.

## Alternatives

**Add assessment columns to the catalog.** Rejected: every existing row would be
rewritten, which the immutability check exists to forbid.

**Record the judgment in the retained body's frontmatter.** Rejected: it
rewrites frozen bytes and mixes the historical state with the current one.

**A separate reappraisal ledger file.** Rejected: it is a second management
ledger beside the index that already names each unit.

**Exempt listed paths from the immutability check.** Rejected: an allowlist
switches the check off for its entries instead of admitting one transition.

**Keep retention permanent.** Rejected: a unit would stay in the tree after
every consumer and obligation is gone, or leave through an unreviewed commit.

**Keep reachability from `HEAD`.** Rejected: it passes for source commits that a
squash later makes unreachable, which the envelope exists to prevent.

## Traceability

### Lifecycle Traceability

| Decision lineage | Replacement relation                                                       | Affected Spec                                                                       |
| ---------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| [ADR-0039](./0039-unit-archive-retention-and-citation-table.md) | Supersedes ADR-0039; the frozen generations keep theirs | [SPEC-0085](../../03.specs/0085-archive-reappraisal-and-document-standards/spec.md) |
