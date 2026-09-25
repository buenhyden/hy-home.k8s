---
title: "Archive Ledger Split Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-09-26"
layer: "specs"
artifact_id: "SPEC-0092"
---

# Archive Ledger Split Technical Specification (Spec)

## Overview

`docs/98.archive/README.md` is the archive's navigation entry and also the
machine index that the archive validators read: the record manifest with its
`archive-manifest:v1` marker, the Retention Catalog, and the Retention
Assessment. The README navigation contract of SPEC-0091 therefore leaves it in
`pending_paths`. [ADR-0047](../../02.architecture/decisions/0047-archive-ledger-beside-the-navigation-index.md)
moves the tables into `docs/98.archive/ledger.md` and keeps the README as the
archive identity. This Spec implements that decision. It is the second part of
the three-part program the request owner approved on 2026-09-25.

## Strategic Boundaries & Non-goals

In scope: the `archive/ledger` profile, template, and registry paths; the
ledger file; the table readers in `scripts/archive_validation.py`,
`scripts/archive_dispositions.py`, `scripts/archive_cutover.py`, and
`scripts/validate-links-and-owners.py`; the tests that read the tables; the
README rewrite; the instructions that tell authors where to add a row; and
ADR-0047.

Out of scope: a table's columns, rows, or parsing rules; any sealed record,
retained body, or frozen specification; retention, reappraisal, or recovery
semantics; the document language contract; any live cluster or provider
action.

## Contracts

- The archive has one index, stored in `docs/98.archive/ledger.md`. The ledger
  holds the manifest marker and table, the Retention Catalog, and the Retention
  Assessment, byte-identical to their README rows.
- `docs/98.archive/README.md` keeps the archive identity. Its path and its
  `## Document Index` heading stay the replacement target that sealed records
  name and the default replacement of a deleted record. It holds no machine
  table and follows the README navigation contract.
- A reader locates the ledger only through the registry. `archive_assessment.index`
  names the ledger; `archive_citation.index` keeps naming the README and a new
  `archive_citation.ledger` names the ledger. No script keeps its own copy of
  either path.
- `archive_target_kind` classifies the ledger as the `index` kind, so a link to
  the ledger is admitted wherever a link to the README is.
- A machine table or manifest marker left in the README fails, and an
  untracked ledger fails.
- The README's `## Document Index` links each direct child once:
  `completed/`, `migrations/`, `retired/`, `superseded/`, and `ledger.md`.
  The prose that points at individual migration records and the Spec 0052
  package moves to the ledger's `## Record Manifest`, rewritten in English.
- After the move `readme_navigation.pending_paths` is empty.

## Core Design

The move keeps two concepts apart. The index identity (`ARCHIVE_INDEX`, the
README) is used for replacement edges, lifecycle defaults, and citation. The
ledger storage (`ARCHIVE_LEDGER`) is used by every code path that reads a
table: the manifest reader and parser, the catalog and assessment spans, the
cutover corpus and manifest checks, and the link validator's assessment read.
Each script derives both from the registry through one helper in
`scripts/archive_dispositions.py`.

The ledger is a governed Markdown document. Its profile requires
`## Overview`, `## Record Manifest`, `## Retention Ledger`, and
`## Related Documents`. The catalog and assessment keep their `###` headings
under `## Retention Ledger`, so the heading-based span finder is unchanged.

## Data Modeling & Storage Strategy

```json
"archive_citation": {"index": "docs/98.archive/README.md", "ledger": "docs/98.archive/ledger.md"},
"archive_assessment": {"index": "docs/98.archive/ledger.md", "heading": "Retention Assessment"}
```

Only the named fields change; every other field keeps its value. The schema
requires `archive_citation.ledger` whenever `archive_citation` is present, and
the registry self-check requires it to equal `archive_assessment.index`.

## Interfaces & Data Structures

| Code | Failure |
| --- | --- |
| `ARCHIVE-LEDGER-MISSING` | The registry ledger path is not a tracked regular file |
| `ARCHIVE-LEDGER-RESIDUE` | The README still holds a manifest marker, manifest header, catalog header, or assessment heading |
| `REGISTRY_ARCHIVE_LEDGER` | `archive_citation.ledger` is absent or differs from `archive_assessment.index` |

Existing `ARCHIVE-INDEX-*`, `ARCHIVE-CATALOG-*`, and `ARCHIVE-ASSESSMENT-*`
codes keep their meaning and report the ledger path.

## Edge Cases & Error Handling

A frozen body that links `../../98.archive/README.md#document-index` keeps
resolving, because the heading stays. A sealed record whose replacement is the
README keeps its meaning, because the identity stays. A synthetic test root
that writes tables into its README fails `ARCHIVE-LEDGER-RESIDUE`, which the
test fixtures fix by writing the ledger instead. The copied totals sentence in
the README (`25/25`, `198/198`) is deleted rather than moved, because only the
marker is machine-checked.

## Failure Modes & Fallback / Human Escalation

A failing gate stops the commit, and no assertion is weakened. The move is one
commit so that no tree has the tables in both files or in neither. If the
parsed manifest, catalog, or assessment differs before and after the move, the
commit is not made and the difference is reported.

## Verification Commands

```bash
python3 -m unittest tests.test_archive_dispositions tests.test_archive_reappraisal tests.test_archive_catalog_reverification tests.test_archive_registry_contract tests.test_archive_citation_decision
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/archive_cutover.py --root .
python3 scripts/qa.py staged
python3 scripts/qa.py full
git diff --check
```

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-ALS-001 | The ledger profile, template, and registry fields exist and the registry rejects a ledger that differs from the assessment index | Registry gate and focused tests |
| VAL-ALS-002 | The parsed manifest, catalog, and assessment are identical before and after the move | Comparison recorded in the Task |
| VAL-ALS-003 | Every table reader uses the registry ledger path, and no script keeps its own path copy | Focused tests and review |
| VAL-ALS-004 | A table left in the README and an untracked ledger each fail with their own code | Focused tests |
| VAL-ALS-005 | The README passes the navigation contract and `pending_paths` is empty | Link gate |
| VAL-ALS-006 | No sealed record, retained body, or frozen specification changes | `git diff --stat` over those paths |
| VAL-ALS-007 | Each commit passes staged QA and the final tree runs full QA | Staged and full QA |

## Traceability

The [Implementation Plan](plan.md) owns order and risk. The
[ledger Task](tasks/tsk-0001-split-archive-ledger.md) owns the evidence.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ALS-001 | Registry gate and focused tests |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ALS-002 | Recorded comparison |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ALS-003 | Focused tests and review |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ALS-004 | Focused tests |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ALS-005 | Link gate |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ALS-006 | Diff over frozen paths |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ALS-007 | Staged and full QA |
