---
title: "Archive Registry and Test Consumers"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0132"
---

# Archive Registry and Test Consumers Technical Specification (Spec)

## Overview

After [SPEC-0131](../0131-archive-evidence-owner-migration/spec.md), 35
Archive units stay `retained`. The census named the registry, validators or
tests as consumers of most of them. A trial on 2026-10-28 removed all 34 units
other than SPEC-0104 in a scratch worktree and ran the archive, lifecycle,
registry and link validators, plus the test modules that name the units.

The trial showed that most of those consumers do not read the bodies:
- the registry's rebased-path list is classified by path alone;
- removed records are skipped by the catalog check;
- most test paths are synthetic.

The real dependents were current documents that link to a unit, plus three
units whose bodies something still reads:
- frozen migration ledgers resolve a link through ADR-0032;
- one test seeds from the SPEC-0080 package;
- one test reads the SPEC-0103 Spec.

This Spec moves the document consumers of 26 units and removes those units
under
[ADR-0040](../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md)
as `git-history-only`. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-archive-registry-and-test-consumers.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - the links and owner sentences in REQ-0003, ADR-0039, ADR-0040,
    ADR-0047, the archive research README and m0001, m0012 and
    `.claude/provider.md` that name the 26 units;
  - removing the 26 whole units and adding one Retention Assessment row each.
- Non-goals:
  - ADR-0032, SPEC-0080 and SPEC-0103, which frozen ledgers or tests read;
  - SPEC-0004, SPEC-0005, SPEC-0008 and SPEC-0104, which current Requirements
    and ADRs cite as delivery evidence, and SPEC-0072, which REQ-0003 names as
    the trace owner of FR-0011 and acceptance criterion 09;
  - SPEC-0054, which 78 current links cite as the governance convergence
    record;
  - changing a validator, the registry, a test or a frozen Archive record.

## Contracts

- A history link becomes the package or decision identifier as plain text,
  and each edited document names the Retention Catalog as the recovery route.
- A sentence that names a removed Task or Spec as a current owner keeps its
  fact and says the package recorded it.
- A unit is removed only whole, only with Hold `none`, only when no tracked
  file outside Stage 98 links to it or reads it, and only when its catalog
  envelope still resolves from `main`.
- Each removed unit gets assessment `unreviewed` and availability
  `git-history-only`; catalog rows, envelopes and the registry's rebased-path
  list stay unchanged.

## Core Design

The disposition reuses the ADR-0040 table and validators. The consumer test is
the trial itself: units are removed, then the validators and the test
modules that name them run on the result.

## Data Modeling & Storage Strategy

Twenty-six rows in the Retention Assessment table of
`docs/98.archive/README.md`.

## Interfaces & Data Structures

Row columns follow the registry `archive_assessment` contract, as in
SPEC-0122.

## Edge Cases & Error Handling

- The registry's rebased-path list keeps names of removed decisions; the
  path-only check still classifies them, and the catalog check skips removed
  records.
- A unit with a consumer outside this repository cannot be observed; removal
  is still recoverable from Git history.

## Failure Modes & Fallback / Human Escalation

If a removed unit is needed again, it returns as a new unit under a new
decision, recovered with `git archive <envelope commit> <original path>`.

## Verification Commands

- `python3 scripts/validate-archive-integrity.py --root .`
- `python3 scripts/validate-document-lifecycle.py --root . --mode strict`
- `python3 scripts/validate-links-and-owners.py --root . --mode strict`
- `python3 -m unittest` on the test modules that name a unit.
- `git rev-parse` envelope equality and `git archive` restore per unit.
- `python3 scripts/qa.py staged` on each exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-RT-001 | No tracked file outside Stage 98 links to or reads the 26 units, every stated fact is kept, and the archive, lifecycle and link validators and the named test modules pass with the units removed. |
| VAL-RT-002 | Each unit's envelope object equals its current object, or for the fifteen decisions whose links ADR-0038 rebased differs only in link targets, and restores into a scratch directory with the expected file count. |
| VAL-RT-003 | The 26 units are absent, each has a valid `git-history-only` row, and staged QA passes on every commit. |
| VAL-RT-004 | An independent reviewer confirms the consumer edits and removals, and the pull request's hosted checks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RT-001 | Trial validation and review |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RT-002 | Isolated recovery |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RT-003 | Assessment validation and staged QA |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RT-004 | Independent review and hosted checks |
