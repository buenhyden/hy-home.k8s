---
title: "Repository Vocabulary in the Knowledge Surface"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-11-12"
layer: "architecture"
artifact_id: "ADR-0058"
---

# ADR-0058: Repository Vocabulary in the Knowledge Surface

## Overview

This accepted amendment narrows one clause of accepted
[ADR-0036](./0036-common-knowledge-and-prompt-surfaces.md) Decision 3, which
says `.agents/knowledge/` owns hand-maintained pointer material that states no
policy of its own. It admits exactly one non-pointer document there,
`.agents/knowledge/glossary.md`, the Repository Vocabulary, which owns the
meaning of shared governance terms. Every other clause of ADR-0036 stays.
ADR-0036 keeps its body; this decision amends it, as ADR-0057 amended
ADR-0056.

The current user accepted this decision on 2026-11-12. The acceptance is
recorded in the SPEC-0163 Task. It accepts no SPEC-0163 criterion by itself.

## Context

Requirements GOV-01, R45-08 and R147-09 of the external v14.7 execution
package place the Repository Vocabulary at `.agents/knowledge/glossary.md`. On
2026-11-12 the user ruled that current v14.7 requirements prevail over
conflicting existing rules (SPEC-0161 Task, EVD-018). The pointer-only clause of
ADR-0036 conflicts with that path, and so do the context-and-memory policy, the
wiki-curator role, the knowledge-map skill and the knowledge validator, which
follow it. [REQ-0003-FR-0032](../../01.requirements/0003-workspace-agent-governance-platform.md)
states the requirement; [AD-0006](../descriptions/0006-workspace-agent-governance-platform.md)
is the governance view.

## Decision

1. **One vocabulary document.** `.agents/knowledge/glossary.md` defines the
   meaning of shared governance terms under stable `TERM-` IDs. Each term names
   the policy role and path that own its rules. It states no rule, approval
   step, command, transition or check algorithm, and policies do not redefine
   its terms.
2. **Pointer documents unchanged.** Every other document under
   `.agents/knowledge/` stays pointer material as ADR-0036 Decision 3 says.
3. **Enforcement.** The knowledge validator routes the glossary by file name to
   a term-table check: unique well-formed IDs, existing owner paths and no
   twelve-word span copied from a named owner, counting Latin and Hangul words.
   The Stage 99 registry gives the glossary its own profile.
4. **Decision makers and confirmation.** The current user decides acceptance;
   compliance is confirmed by the knowledge validator and the SPEC-0163 Task.

## Explicit Non-goals

- Editing ADR-0036's body or any other ADR-0036 clause.
- Moving policy rules into the glossary or a second vocabulary file.
- Machine-checking that every common term is present; the SPEC-0163 Task checks
  it once against the adopted contract.

## Consequences

- **Positive:** term meanings have one owner, and the pointer surface stays a
  map for every other document.
- **Trade-off:** one document in a pointer surface follows a different form, so
  its readers must know the exception.
- **Follow-up:** adopting a later vocabulary edition is a change to the
  glossary and its Contract Version, not to this decision.

## Alternatives

- **Glossary elsewhere (for example `.agents/governance/`):** rejected; the
  package fixes the path, and the user ruled that the current requirement
  prevails.
- **Keep the SDLC terminology table as the vocabulary:** rejected; it mixes
  meanings with placement rules and has no stable IDs.

## Traceability

- **Requirements:** [REQ-0003-FR-0032](../../01.requirements/0003-workspace-agent-governance-platform.md).
- **Architecture:** [AD-0006](../descriptions/0006-workspace-agent-governance-platform.md).
- **Change:** N/A — SPEC-0163 left the tree; Git history recovers it. Its acceptance and exact source are summarized in [REQ-0003 Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage).

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0036](./0036-common-knowledge-and-prompt-surfaces.md) | Narrows only Decision 3's pointer-only knowledge clause for `.agents/knowledge/glossary.md`; every other clause stays | N/A — SPEC-0163 left the tree; Git history recovers it |
