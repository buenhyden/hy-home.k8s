---
title: "Archive Retention and Provenance Research Pack"
version: "0.1.1"
type: "common/readme-research-pack"
status: "active"
owner: "platform"
updated: "2026-09-15"
layer: "references"
---

# Archive Retention and Provenance Research Pack

## Overview

This pack records external evidence behind the Stage 98 retention and citation
questions that ADR-0039 decides: how Git names and keeps objects, how superseded
decisions and incident records are kept, how public URL moves are signalled,
and how schema annotations differ from validation. It is dated, descriptive
evidence, not policy.

## Research Contract

- **Observation date**: 2026-09-15.
- **Source classes**: primary documentation for Git, HTTP, JSON Schema,
  CommonMark, and GitHub; the original ADR article; the Google SRE postmortem
  chapters; the Diátaxis framework site.
- **Method**: each source was fetched on the observation date, and only claims
  with a captured quotation are recorded. A source that could not be fetched is
  recorded as `unreachable` with no claim.
- **Authority**: [common governance](../../../../.agents/README.md), the Stage 99
  registry, and the accepted architecture decisions keep current authority. A
  finding here supports or bounds a decision; it never replaces one.

## Report Index

| Reference                                                                                               | Role                                                                                                     |
| ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [Git provenance and superseded record citation](m0001-git-provenance-and-superseded-record-citation.md) | Object naming, reachability, superseded-record practice, URL moves, schema annotations, and link parsing |

## Refresh and Succession

Refresh a claim when its source changes a cited section or when a decision that
relies on it is revised. A newer finding is added as a dated entry beside the
older one; an existing claim is not rewritten.

## Evidence Boundary

These findings are external documentation. They establish no repository
behavior, hosted CI result, provider runtime, or live cluster state, and a
standard cited here is not adopted or certified by citing it.

## Related Documents

- [Research collection](../README.md)
- [ADR-0039](../../../02.architecture/decisions/0039-unit-archive-retention-and-citation-table.md)
- [Spec 0082](../../../98.archive/completed/03.specs/0082-unit-archive-retention-contract/spec.md)
