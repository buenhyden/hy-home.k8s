---
title: "Archive Ledger Beside the Navigation Index"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "platform"
updated: "2026-09-26"
layer: "architecture"
artifact_id: "ADR-0047"
---

# ADR-0047: Archive Ledger Beside the Navigation Index

## Overview

The Stage 98 README is both the archive's navigation entry and the only
machine index the archive validators read. This decision moves the machine
tables into one ledger file beside the README, so the README navigates and the
ledger records. The single-index rule of
[ADR-0040](./0040-archive-reappraisal-and-verifiable-sources.md) stands: the
index moves, and no second ledger appears.

## Context

`docs/98.archive/README.md` carries the record manifest with its
`archive-manifest:v1` marker, the Retention Catalog, and the Retention
Assessment. Validators find the first two by exact header text and the third by
the registry heading, and each script copies the README path as its own
constant. The README navigation contract of SPEC-0091 cannot check this README
while it holds these tables, so it is the one path left in `pending_paths`.

The README path has a second meaning. Sealed migration records name
`docs/98.archive/README.md#document-index` as the replacement of deleted
records, the lifecycle validator uses the README as the default replacement,
and the citation contract admits any link to it. Sealed bytes cannot change,
so that identity has to stay where it is.

ADR-0040 rejected a separate reappraisal ledger because it would be a second
management ledger beside the index that already names each unit. A relocated
index that the README no longer duplicates is not that ledger.

## Decision

- `docs/98.archive/ledger.md` is the archive ledger. It holds the record
  manifest and its marker, the Retention Catalog, and the Retention Assessment,
  moved without changing a row. It has its own Stage 99 profile,
  `archive/ledger`.
- `docs/98.archive/README.md` keeps the archive identity: the
  `## Document Index` heading, the replacement target that sealed records name,
  and the citation index. It carries no machine table and follows the README
  navigation contract.
- Validators read tables only from the ledger path the registry names. A table
  left in the README fails.
- Citing the ledger is admitted wherever citing the README is admitted.

## Explicit Non-goals

- No change to a table's columns, rows, or parsing.
- No change to a sealed record, retained body, or frozen specification.
- No JSON or per-table ledger form.
- No change to retention, reappraisal, or recovery semantics.

## Consequences

The README becomes a navigation page that the contract checks like any other,
and `pending_paths` empties. Authors who add a retention row edit the ledger
instead of the README. The ledger is a new governed form with a profile and a
template. Every table reader depends on one registry path instead of copied
constants. A frozen body that links `README.md#document-index` still resolves,
because that heading stays.

## Alternatives

**Keep the tables in the README.** Rejected: the navigation contract would keep
a permanent exemption for the one README that most needs to stay readable.

**Convert the ledger to JSON with a schema.** Rejected: every parser, the Git
reverification, and their tests would be rewritten for no change in meaning,
and review diffs would lose the table form.

**One file per table.** Rejected: three files split the one index that
ADR-0039 and ADR-0040 require.

**Supersede ADR-0040.** Rejected: its reappraisal and verifiable-source
decisions stay current; only the index location changes, and that does not
contradict its rejection of a second ledger.

## Traceability

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0040](./0040-archive-reappraisal-and-verifiable-sources.md) | N/A; ADR-0040 stays accepted | [SPEC-0092](../../03.specs/0092-archive-ledger-split/spec.md) |
