---
title: "Work Residue Ledger Amendment"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-11-13"
artifact_id: "ADR-0060"
---

# ADR-0060: Work Residue Ledger Amendment

## Overview

The operator decided on 2026-11-13 (W03-D37 to W03-D40) that the repository
keeps one machine ledger for work residue: open handoffs, conflicts, adoption
items and survey items. This scoped amendment narrows the no-ledger clauses of
[ADR-0031](./0031-current-corpus-retention-and-validation-ownership.md),
[ADR-0036](./0036-common-knowledge-and-prompt-surfaces.md),
[ADR-0047](./0047-agent-contract-and-resource-ownership.md) and
[ADR-0048](./0048-local-qa-and-semver-release-ownership.md) from "no ledger" to
"no competing progress ledger of execution state". It narrows by dated
clarification only, replaces no paragraph, and the four ADRs stay accepted for
every other clause with their bodies as decision history. This record is
`accepted`; it changes no validator, registry, schema or ledger file.

The current user accepted this decision on 2026-11-13. The acceptance is
recorded in the SPEC-0185 Task. It accepts no SPEC-0185 criterion by itself.

## Context

The v14.7 execution package asks for one machine ledger from which unfinished,
adoption and survey state is derived, and forbids a competing progress ledger.
The accepted clauses read more broadly than that rule:

- ADR-0036 retires the memory structure because a generated progress ledger
  competed with the owning Spec Task.
- ADR-0047 Decision 4 excludes "a second state ledger" and its Non-goals
  exclude "a central progress ledger".
- ADR-0048 excludes a "permanent progress ledger".
- ADR-0031 keeps execution instances and a "roster" out of governance text.

[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
FR-0019 and FR-0022 and
[AD-0006](../descriptions/0006-workspace-agent-governance-platform.md) carry the
same reading. Stage 02 rule 3 forbids editing an accepted decision in place, and
[ADR-0055](./0055-governance-decision-current-state-amendment.md) set the
pattern of one record that narrows named clauses. The retired structure stays
retired: `scripts/validation/repository/quality.py` refuses a tracked
`progress.md`, and `tests/test_common_agents_document_routes.py` keeps the
`.agents` routes registered. These, not a governance validator, are the guards
that exist.

## Decision

The operator, as request owner, decided this on 2026-11-13. Compliance is
confirmed by the strict document checks and by comparing each amended sentence
with this text.

1. **Ledger rule.** One JSON ledger with its schema holds work residue only:
   open handoffs, conflicts, adoption items and survey items. The Task and its
   EVD rows remain the only owner of execution state, status, evidence and
   acceptance. A terminal entry carries a closure reference to an EVD row.
   Adoption entries reference `shared_contract` and `common_forms` of
   `docs/99.templates/registry.json` by key and copy none of their values.
   Views are derived on demand by a script like `scripts/document-backlinks.py`;
   no view is committed. Seeding takes current truth: stale or historical rows
   are closed by Resolves EVD rows or registered historical tables, and no
   recorded row is rewritten. Stage 90 is excluded, because audit, research and
   data stay evidence (REQ-0003-FR-0021).
2. **Entry fields and state.** An entry holds an identity, a kind (handoff,
   conflict, adoption or survey), a state, an owner, a resume condition, a
   source reference and, when terminal, a closure reference to an EVD row. The
   entry `state` is only open or terminal; it is compared with the Task and EVD
   rows (identity, state, owner and resume condition must agree) and never
   copies a Task status such as `draft` or `in-progress`. For residue the
   ledger entry is authoritative, and the Task Handoff rows point to it once
   the ledger exists.
3. **Retirement.** A terminal entry is pruned no later than the owning
   package's exit commit; its closure reference is valid only until then, and
   Git history recovers it afterwards.
4. **Location and name.** The ledger is the "work residue ledger"; the word
   "progress" is not used for it. It is not under `memory/`, no file is named
   `progress.*`, and a registered document route is required when the file lies
   under `.agents/`.
5. **Narrowed clauses.** ADR-0036's retired-memory-structure paragraph,
   ADR-0047 Decision 4's "without a second state ledger" and Non-goal
   "creates no central progress ledger", ADR-0048's Non-goal "permanent
   progress ledger", and ADR-0031's execution-instance and "roster" clauses
   each read: no competing progress ledger of execution state, and the work
   residue ledger of this decision is not one. ADR-0047 Decision 4's knowledge
   surface holds no residue state. A roster copies instance state; the residue
   ledger holds residue pointers only.

## Explicit Non-goals

- Building the ledger, its schema, the derivation script, the validator, the
  seed or tests; package 2 of W03-H30 owns them.
- Restoring the removed progress ledger, a `memory/` structure or any owner of
  execution state, status, evidence or acceptance other than the Task.
- A ledger entry for hold, disposition or retention (REQ-0003-FR-0020) or for a
  Stage 90 document (REQ-0003-FR-0021).
- A Tombstone, archive record or replacement of any amended ADR as a whole.

## Consequences

- **Positive**: the requirement for one machine residue ledger and the accepted
  no-ledger clauses read consistently, and Markdown-only or JSON-only residue
  becomes detectable once package 2 exists.
- **Negative**: a reader must combine each amended ADR with this record.
- **Operational**: none until package 2; until then no ledger file exists and
  Plan and Task review shows package-local state.

## Alternatives

- **Keep "no ledger" and carry residue in Task rows only**: rejected; the
  v14.7 package asks for one machine ledger and Task rows cannot detect residue
  that exists only in Markdown or only in JSON.
- **A ledger that also holds Task status and evidence**: rejected; it competes
  with the Task for execution state.
- **A committed generated view**: rejected; a copy drifts, so views are derived
  on demand.
- **Superseding each of the four ADRs**: rejected by the same reasoning as in
  ADR-0055; their other clauses stay current.

## Traceability

The amendment applies only to the clauses named in the Decision. The amended
ADRs keep their bodies, and their 2026-11-13 clarifications refer to this
record.

- **Requirement**: [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
  FR-0019 and FR-0022.
- **Architecture**: [AD-0006](../descriptions/0006-workspace-agent-governance-platform.md).
- **Specification**: N/A — SPEC-0185 left the tree; Git history recovers it. Its acceptance and exact source are summarized in [REQ-0003 Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage).

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0031](./0031-current-corpus-retention-and-validation-ownership.md) | Narrows the execution-instance and roster clauses by clarification; every other clause stays | N/A — SPEC-0185 left the tree; Git history recovers it |
| [ADR-0036](./0036-common-knowledge-and-prompt-surfaces.md) | Narrows the retired-memory-structure paragraph by clarification; every other clause stays | N/A — SPEC-0185 left the tree; Git history recovers it |
| [ADR-0047](./0047-agent-contract-and-resource-ownership.md) | Narrows Decision 4's second-state-ledger clause and the central-ledger Non-goal by clarification; every other clause stays | N/A — SPEC-0185 left the tree; Git history recovers it |
| [ADR-0048](./0048-local-qa-and-semver-release-ownership.md) | Narrows the permanent-progress-ledger Non-goal by clarification; every other clause stays | N/A — SPEC-0185 left the tree; Git history recovers it |
