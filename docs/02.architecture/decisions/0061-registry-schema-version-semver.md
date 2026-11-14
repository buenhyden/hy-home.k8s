---
title: "Registry Schema Version SemVer Amendment"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-11-14"
artifact_id: "ADR-0061"
---

# ADR-0061: Registry Schema Version SemVer Amendment

## Overview

This amendment records that the Stage 99 registry value
`schema_version` is a SemVer string, not an integer. The declared generation 10
maps to `10.0.0` and the current value is `11.0.0`. It amends the current-state
sentences of accepted [ADR-0033](./0033-common-document-contract-v9.md) and
Decision 1 of accepted [ADR-0059](./0059-registry-common-form-model.md) that
name the integer, as ADR-0059 amended ADR-0033. Both ADRs keep their bodies and
every other clause stays.

This record is written in the ADR form of its day (W03-D69). The current user
accepted this decision on 2026-11-14. The acceptance is recorded in the
SPEC-0207 Task. It accepts no SPEC-0207 criterion by itself.

## Context

The external v14.7 execution package separates the Registry serialization
version from the profile content version, and says an integer value moves by an
explicit mapping after its consumers are analysed (REQ:862, REQ:890). On
2026-11-14 the user decided that the W03 requirement text governs a conflict
with a current rule (W03-D65, fourth resolution). The change was decided as
W03-D66 and its ADR bound as W03-D69.

The repository named a generation by its integer from generation 1 (2026-07-12)
to generation 10 (2026-10-05); the values were never SemVer. ADR-0033 says the
current Registry is `schema_version` 10, and ADR-0059 Decision 1 says the value
stays 10 when optional keys are added. An integer cannot carry the MINOR and
PATCH steps of the bump rule (REQ:877 to REQ:882). The strict loader and the
profile schema reject an unknown key, so a new top-level key is a breaking
change. Three readers pin the value by equality: the strict loader, the history
reader of the lifecycle validator and the pre-edit write guard, which fails
closed with `HOOK-DOC-REGISTRY`.

[REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md)
makes the registry the single machine owner of document form;
[AD-0006](../descriptions/0006-workspace-agent-governance-platform.md) is the
governance view.

## Decision

1. **Representation.** `schema_version` is a JSON string holding a SemVer value
   of the repository grammar with no prerelease and no build metadata, in the
   registry and as the `const` of its schema property. A reader that needs the
   MAJOR number reads it from the string.
2. **Mapping.** An integer generation `N` of 1 to 10 means `N.0.0`: the
   integer scheme recorded no compatible revision, so MINOR and PATCH are 0.
   Generation 10 is `10.0.0`. The mapping preserves order and meaning, makes no
   compatibility claim between generations and never converts a value wholesale
   to `1.0.0`. One reader function owns it, and only the history reader, which
   reads registry blobs of earlier commits, accepts an integer.
3. **Current value.** This change replaces the integer by a string and breaks
   every reader that was valid before, so it is MAJOR and the registry value is
   `11.0.0`.
4. **Readers.** The loader and the write guard accept the one MAJOR number they
   implement and refuse any other. The history reader reads every blob whose
   MAJOR number is in an explicit readable set with its own typed reading and
   falls back to the current registry only for a blob it cannot read. A MAJOR
   step appends its number to the readable set and edits the implemented number
   in the code and in the guard; a MINOR or PATCH step edits the registry value
   and the schema `const` only.
5. **Bump rule.** The public contract of a Registry Schema Version is what code
   reading the registry observes. The release unit is one change set that lands
   on `main`, and the highest level wins. MAJOR is a change that breaks a
   registry or a consumer that was valid before, including a new key where a
   strict consumer rejects an unknown key. MINOR is a compatible addition that
   earlier valid producers and consumers survive. PATCH is a compatible fix that
   enforces an already declared contract. NO_CHANGE leaves the serialization
   shape untouched. Each later registry change applies its own bump at its
   implementation commit and records the level and the reason in its Task.
6. **Amended sentences.** ADR-0033's current-state sentence that the current
   Registry is `schema_version` 10 reads: `schema_version` is a SemVer string
   whose current value is `11.0.0`, and generation 10 is `10.0.0`. ADR-0059
   Decision 1's `schema_version` stays 10 reads: the optional keys it added
   carry no separate step and belong to generation 10, `10.0.0`.
7. **Decision makers and confirmation.** The user decided the representation,
   the mapping and the current value on 2026-11-14 and decides acceptance of
   this record. Compliance is confirmed by the registry, Markdown profile,
   links and lifecycle validators, the SPEC-0207 regression tests and the
   SPEC-0207 Task.

## Explicit Non-goals

- Editing the body of ADR-0033 or ADR-0059, or any other clause of either.
- Changing any profile, form, template, lifecycle domain or section content,
  which is the profile content version.
- The integer versions of other files: the agent role registry and the two
  provider bindings, the validation registry, the work residue ledger and the
  workspace memory database.
- Contract Versions, Document Revisions, artifact identities and package
  edition labels.

## Consequences

- **Positive**: the registry can carry MINOR and PATCH steps, and each later
  change has a defined starting value and a stated level rule.
- **Negative**: a reader must combine ADR-0033 and ADR-0059 with this record
  until each is replaced.
- **Operational**: a MAJOR step edits one constant of the code, one of the
  guard, the registry value and the schema `const` together, and an old blob
  stays readable while the history window reaches it. The integer branch of the
  reader function ends when no replayed commit predates this change.

## Alternatives

- **The integer 11 (W03-D63)**: rejected; an integer cannot carry MINOR and
  PATCH steps, and the user decided the string form.
- **Convert every value to `1.0.0`**: rejected; it erases the generation order
  that code and history rely on.
- **Keep the integer and add a second version field**: rejected; two machine
  owners of one fact would drift.
- **Keep the value at 10 for additive keys**: rejected; the strict consumers
  reject an unknown key, so such a key is a breaking change.

## Traceability

- **Requirements:** [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md), [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md).
- **Architecture:** [AD-0006](../descriptions/0006-workspace-agent-governance-platform.md).
- **Change:** N/A — SPEC-0207 left the tree; Git history recovers it. Its acceptance and exact source are summarized in [REQ-0003 Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage).

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0033](./0033-common-document-contract-v9.md) | Amends only the current-state sentence that names the integer; every other clause stays | N/A — SPEC-0207 left the tree; Git history recovers it |
| [ADR-0059](./0059-registry-common-form-model.md) | Amends only Decision 1's integer sentence; every other clause stays | N/A — SPEC-0207 left the tree; Git history recovers it |
