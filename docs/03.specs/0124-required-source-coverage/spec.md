---
title: "Required Source Coverage"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0124"
---

# Required Source Coverage Technical Specification (Spec)

## Overview

The operator's repository survey names ten required sources (SRC-MEM,
SRC-AGENT, SRC-DOC, SRC-SDD-A to SRC-SDD-D, SRC-C4, SRC-ADR and SRC-ARC42) and
asks that each be read directly and recorded against six perspectives:
structure, governance, rules, system, policy and templates. The research
register
[m0012](../../90.references/research/0001-workspace-engineering/m0012-source-coverage.md)
last observed six of them on 2026-09-27. It has never observed
`akitaonrails/ai-memory`, `specdriven.ai`, the Microsoft spec-driven
development article or the dev.to practical introduction, and it records no
per-perspective support for any of the ten. This Spec adds one dated
observation block to that register. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-required-source-coverage.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - one dated observation block in m0012 with source rows for the ten
    sources and a ten-by-six support matrix;
  - this package and the Stage 03 README index.
- Non-goals:
  - adopting, installing or copying any source content, template or script;
  - changing governance, templates, validators or other research members;
  - rewriting earlier m0012 rows or identifiers.

## Contracts

- Each perspective records one `source_support` value: `EXPLICIT` (the
  source states it, with the section or file), `DERIVED_PROPOSAL` (the source
  does not state it; a project could derive a proposal from what it does
  state), `NOT_SPECIFIED` (the relevant content was read and does not address
  it) or `NOT_RETRIEVED` (the read failed; the failure is named).
- `NOT_RETRIEVED` is never recorded as `NOT_SPECIFIED` or as applied.
- A source value states the source's support only. It is not an execution
  state, and repository permissions, numbering, lifecycle or schema are never
  recorded as a source's own rule.
- Each source row records the final URL, source type, commit SHA or page
  revision where exposed, the date read and the sections actually read.
  Sources already in m0012 keep their IDs; new sources get the next free
  `SRC-WERPC` numbers.
- Workspace application stays "not observed in this cycle", as the
  register's evidence axes already state.

## Core Design

A delegated read-only researcher reads each exact URL and its named
sub-pages, resolving the current commit for the two GitHub repositories, and
returns the metadata and the six values. The block is appended after the
2026-09-27 current rows, so earlier rows stay unchanged.

## Data Modeling & Storage Strategy

No stored data. The register is a Markdown reference document.

## Interfaces & Data Structures

The block has two tables: source rows in the register's existing column
order, and a matrix with one row per source and one column per perspective.

## Edge Cases & Error Handling

- A page that cannot be read is `NOT_RETRIEVED` with its failure, never
  replaced by an earlier observation or a similar site.
- Example values in community articles (timeouts, lockouts, durations) are
  recorded as illustrations, not policy.

## Failure Modes & Fallback / Human Escalation

If a source cannot be read in this cycle, the block records it as
`NOT_RETRIEVED` and the Task names it as a residual gap. Reverting the pull
request removes the block.

## Verification Commands

- `python3 scripts/validate-markdown-profiles.py`.
- `python3 scripts/validate-links-and-owners.py`.
- `python3 scripts/validate-document-lifecycle.py --mode strict`.
- `python3 scripts/qa.py staged` on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-RS-001 | m0012 has a 2026-10-27 block with a row for each of the ten sources and a ten-by-six matrix in which every cell holds one of the four values with its section or failure, and an independent reader confirms the values against the sources. |
| VAL-RS-002 | Staged QA passes on the exact index and the pull request's hosted checks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RS-001 | Independent source re-read |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RS-002 | Staged QA and hosted checks |
