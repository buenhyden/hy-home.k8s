---
title: "Unit Archive Retention Contract Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "done"
owner: "platform"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0082"
---

# Unit Archive Retention Contract Technical Specification (Spec)

## Overview

[ADR-0039](../../02.architecture/decisions/0039-unit-archive-retention-and-citation-table.md)
proposes retaining whole units byte for byte, deciding a class from the unit's
state, naming one Git object per unit, deciding every citation from one ordered
registry table, and tracking moves between active stages by identity. This Spec
owns applying that decision and correcting the current statements that no
longer match the accepted ADR-0038 contract.

A document takes one state edge per integration, so the work lands in three
integrations. The proposal records the survey, corrects stale statements,
records the external evidence, and proposes ADR-0039. After it is integrated
and ADR-0039 is accepted, the cutover moves the registry, validators, forms,
and governance prose together. After that is integrated, the first exact
disposition retains ADR-0038.

## Strategic Boundaries & Non-goals

Authorized scope for the proposal: the corrected current statements in
`.agents/roles/README.md`, the Stage 01 and Stage 02 indexes, AD-0006, the
current prose of `docs/98.archive/README.md` outside its manifest comment and
frozen record table, one comment in `scripts/validate-links-and-owners.py`,
ADR-0039, a proposed-successor note in ADR-0038, the Spec ownership
sentence in REQ-0003, the decision, Stage 03, Stage 90, and research collection
indexes, the new research pack
`docs/90.references/research/0002-archive-retention-and-provenance/`, this
package, and the activation of SPEC-0080 and SPEC-0081 for closure.

Authorized scope for the cutover, after acceptance: `docs/99.templates/registry.json`,
`docs/99.templates/contracts/document-profile.schema.json`,
`docs/99.templates/templates/archive/`, `docs/99.templates/README.md`,
`scripts/archive_dispositions.py`, `scripts/document_contracts.py`,
`scripts/archive_validation.py`, `scripts/archive_cutover.py`,
`scripts/validate-document-lifecycle.py`, `scripts/document_lifecycle.py`,
`scripts/validate-links-and-owners.py`, `scripts/validation/registry.json`, their
tests, `.agents/governance/document-lifecycle.md`,
`.agents/governance/document-authoring.md`, `.agents/skills/archive-cutover/`,
`docs/README.md`, the stage indexes, REQ-0003, AD-0006, and the closure of
SPEC-0080 and SPEC-0081.

Authorized scope for the retention: ADR-0038, its retained path, its Retention
Catalog row, the current documents that cite it, and the closure of this
package.

Explicit non-goals. No frozen record, ledger, retained package, manifest
comment, frozen record table row, or ADR-0038 retained body changes. No
lifecycle state or edge is added. SPEC-0079 is not retained, because current
documents still cite it. No push, pull request, merge, live cluster, provider
runtime, or secret action is authorized by this Spec.

## Contracts

- A disposition retains one unit: a Stage 03 spec package, an Incident bundle,
  or a standalone document. The unit anchor's state decides the class, and every
  other member is terminal in its own family.
- A retained unit equals its envelope object entry for entry by relative path,
  file mode, and blob, and the envelope object equals the base object at the
  original path.
- One catalog row names one unit. A document row names a blob and a package or
  bundle row names a tree.
- Full validation re-verifies every catalog row; a missing object is a failure.
- One registry citation table, ordered and default-deny, decides every citation,
  and the link and archive validators consume the same decision.
- A move between active stages that keeps identity, family, and state needs no
  Stage 98 record.
- A retention mode applies only to the profiles the registry binds to it.
- The frozen ADR-0032 generation and the sixteen link-rebased ADR-0038 bodies
  keep their bytes and are classified by exact path.

## Core Design

The registry stays the only machine owner. It gains the units, the modes, the
citation table, and the finite legacy set, and the schema and loader validate
them. `scripts/archive_dispositions.py` owns the shared reading: the unit of a
path, the mirror path and its inverse, and the citation decision. The link
validator and the archive validator consume the same decision, and the
archive validator keeps its registry-less reading of the frozen generation. The lifecycle gate replaces link-resolved comparison with an
entry comparison of Git objects for new rows, admits a class by the unit
anchor's state, checks object type and mode, and admits identity-preserving
moves. The archive cutover check re-verifies every catalog row on the full lane.

## Data Modeling & Storage Strategy

A catalog row keeps the two columns `Disposition Record` and `Retention
Envelope`. For a package or bundle the record cell names the unit directory and
the envelope names the tree at the original directory. A retained unit keeps its
source bytes, modes, and frontmatter. No digest, blob column, or path ledger is
added. The legacy set lists the sixteen ADR-0038 retained bodies by path.

## Interfaces & Data Structures

The registry gains `retention_units` (`unit`, `root_pattern`, `anchor`,
`required_members`), `retention_modes` (`mode`, `profile_ids`, `classes`),
`archive_citation` (ordered `rules` of `source`, `target`, and `decision`), and
`legacy_rebased_retained_paths`. `retention_classes` keeps `class`, `names`, and
`admitted_states`, which now name anchor states, and no state is admitted by two
classes. `scripts/archive_dispositions.py` exposes
`citation_decision(registry, source, source_profile_id, target)`,
`retention_unit_of(registry, path)`, and the existing mirror functions.
`CITABLE_NAMINGS` and `rebase_relative_links` are removed once no consumer
remains. The archive validator reports `ARCHIVE-UNIT-MEMBERSHIP`,
`ARCHIVE-UNIT-STATE`, and `ARCHIVE-ENVELOPE-OBJECT` alongside the existing
catalog codes; the link validator keeps `LINK-ARCHIVE-BYPASS`, and the
archive validator reports `ARCHIVE-DIRECT-CURRENT-LINK` from the same decision. A new validation
gate, `archive-contract-tests`, runs the fast archive regression modules in the
quick and staged profiles only.

## Edge Cases & Error Handling

A package whose `spec.md` is `done` but whose Task is still `in-progress` is not
retained. A package with a cancelled Task is completed. A withdrawn package is
retired. An Incident without a published Postmortem is not resolved. A unit
whose member was deleted in the same change fails membership. An envelope that
names a blob for a package, or a commit the base cannot reach, fails. A frozen
record placed under `completed/` is still a frozen record for citation. An
identity-preserving move whose target lies under `docs/98.archive/` is a
disposition, not a move. A body in the legacy set keeps
link-resolved verification.

## Failure Modes & Fallback / Human Escalation

If ADR-0039 is rejected, it takes the `rejected` edge, this package is withdrawn
through its `active` and `withdrawn` edges in later integrations,
and the proposal's statement corrections stay valid under ADR-0038. If the
cutover cannot keep frozen content passing unmodified, it stops and returns to
the request owner rather than weakening a gate. Before integration each step
reverts by commit; after the retention is integrated, recovery is a forward fix
and never deletes a retained unit.

## Verification Commands

```bash
python3 -m unittest tests.test_archive_dispositions tests.test_archive_disposition_lifecycle tests.test_documentation_link_boundary
python3 scripts/qa.py quick
python3 scripts/qa.py staged
python3 scripts/qa.py full
```

`full` owns unit discovery and the pre-commit manual stage. No command here
proves hosted CI, provider runtime, or live cluster behavior.

## Success Criteria & Verification Plan

| ID          | Criterion                                                                                                                                                                | Evidence                                          |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| VAL-UAR-001 | ADR-0039 records the unit, exact retention, envelope, mode, citation-table, and identity-move decisions in its proposed state, and ADR-0038 names its proposed successor | Decision review and the lifecycle gate            |
| VAL-UAR-002 | The survey judgment is recorded for every reviewed item, and current statements that contradicted ADR-0038 are corrected with frozen bytes unchanged                     | Proposal Task and staged QA                       |
| VAL-UAR-003 | A research reference records each external source with its access date, the claims used, their limits, and unreachable sources                                           | Research review and the strict document gates     |
| VAL-UAR-004 | The registry, schema, and loader declare and validate units, modes, the citation table, and the legacy set                                                               | Registry regressions                              |
| VAL-UAR-005 | The lifecycle gate admits exact unit retention by anchor state and rejects membership, byte, mode, type, and reachability faults                                         | Lifecycle regressions over temporary repositories |
| VAL-UAR-006 | One citation decision is consumed by every citation check, with the ordered rules exercised for every source class                                                       | Link and archive regressions                      |
| VAL-UAR-007 | An identity-preserving move between active stages is admitted without a Stage 98 record, and a changed identity is rejected                                              | Lifecycle regressions                             |
| VAL-UAR-008 | Full validation re-verifies every catalog row and fails on a missing object                                                                                              | Archive cutover regressions and full QA           |
| VAL-UAR-009 | Governance prose, indexes, the skill, and forms state the adopted contract, and the fast gate runs in quick and staged                                                   | Policy review and validation-registry regressions |
| VAL-UAR-010 | ADR-0038 is retained as the first exact disposition, its current consumers cite ADR-0039, and this package closes                                                        | Retention Task, staged and full QA                |
| VAL-UAR-011 | SPEC-0080 and SPEC-0081 reach `done` one lifecycle edge per integration: activated in the proposal and closed in the cutover | Lifecycle gate against the merge base |

## Traceability

The [Implementation Plan](plan.md) owns order and risk. The
[proposal Task](tasks/tsk-0001-propose-the-unit-retention-contract.md), the
[cutover Task](tasks/tsk-0002-cut-over-registry-and-validators.md), and the
[retention Task](tasks/tsk-0003-retain-adr-0038-and-close.md) own the evidence.

### Lifecycle Traceability

| Requirement ID                                                                        | Spec criterion | Verification method                                 |
| ------------------------------------------------------------------------------------- | -------------- | --------------------------------------------------- |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-UAR-001    | Decision review against the disposition requirement |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-UAR-002    | Owner-by-owner statement review                     |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-UAR-003    | Research source and limit review                    |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-UAR-004    | Registry, schema, and loader agreement              |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-UAR-005    | Lifecycle gate regressions                          |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-UAR-006    | Citation decision regressions                       |
| [REQ-0003-FR-0023](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-UAR-007    | Identity lineage regressions                        |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-UAR-008    | Full-lane catalog re-verification                   |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-UAR-009    | Policy and index review                             |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-UAR-010    | Disposition admitted by the lifecycle gate          |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-UAR-011 | Lifecycle edges admitted per integration |
