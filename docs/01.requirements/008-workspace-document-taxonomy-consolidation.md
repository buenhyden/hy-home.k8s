---
title: 'Workspace Document Taxonomy Consolidation Product Requirements'
type: sdlc/prd
status: draft
owner: platform
updated: 2026-08-07
---

# Workspace Document Taxonomy Consolidation Product Requirements

## Overview

This program consolidates the repository's document taxonomy, identifier
schemes, governance rule set, and validator surface into one coherent contract,
and reduces the governance corpus to a size proportional to the platform it
governs. It is grounded in dated external research into spec-driven development
folder contracts and documentation information architecture, and in measured
repository evidence observed on 2026-08-07.

The program does not redesign the platform, the GitOps model, or the agent
harness roles. It changes where authored documents live, what identifies them,
which document owns each rule, and how much machine contract the repository
carries to enforce those rules.

PRD-007 is suspended for the duration of this program. Spec 047 returns to
`draft` and Specs 048 through 051 remain planned draft successors, because
Specs 049 and 050 add validators that this program consolidates.

## Vision

A maintainer or AI agent can name one work unit, find its requirement,
architecture, specification, plan, and task evidence through one identifier and
one folder, and read exactly one document that owns each authoring rule. The
governance corpus stays small enough that a reader can hold the whole contract
in working memory, and every rule that exists is enforced by exactly one
validator.

## Problem Statement

Measured on 2026-08-07, the repository carries 154,499 lines under `docs/`,
78,352 lines under `scripts/`, and 36,154 lines of validator tests, against
4,574 lines of actual platform assets in `gitops/`, `infrastructure/`,
`traefik/`, and `policy/`. The governance machinery is roughly fifty-nine times
the size of the system it governs.

Four structural defects drive that ratio and are independently confirmed by
external evidence.

First, one unit of work is split across three trees with three unrelated
identifier schemes. 39 of 47 specifications have exactly one same-slug plan and
one same-slug task, yet the specification is addressed as
`03.specs/047-<slug>/spec.md` while its plan and task are addressed as
`04.execution/plans/2026-08-02-<slug>.md` and
`04.execution/tasks/2026-08-02-<slug>.md`. All five spec-driven development
toolchains examined co-locate a work unit's specification, plan, and task list
in one folder; none splits them by artifact type.

Second, a single lineage carries three unrelated numbers. PRD-001 maps to
ARD-0004 and Spec 004; PRD-003 maps to ARD-0006 and Specs 038 through 046;
PRD-004 maps to ARD-0007 and Spec 008. Three independent counters advance in
parallel, so `004` names one lineage in Stage 01 and a different lineage in
Stage 03. Established decision-record practice treats a record number as stable
identity that is never reused; this repository treats it as a per-stage
sequence position.

Third, ten documents totalling 1,428 lines govern how to author a document, and
each spends part of its budget declaring what it does not own. The same rule
that Stage 04 plans and tasks remain date-based appears verbatim in three
separate files, and no validator checks that those three copies agree.

Fourth, one-shot migration artifacts were never retired. Three
`active-corpus-*` census files hold 14,142 lines and are read by five
validators totalling roughly 8,000 lines, all produced for a migration that has
completed. The shared progress ledger has grown to 13,920 lines in a single
file that every agent session reads.

Leaving these unresolved keeps drift risk high, because a rule copied into
three files silently becomes false when one copy changes, and keeps agent
context cost high, because the governance corpus must be traversed before any
authored change.

## Personas

| Persona             | Goal                                                                                     | Constraint or authority boundary                                                             |
| ------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Governance steward  | Own one document per authoring rule and retire duplicated rule text.                     | May restructure governance documents; may not weaken GitOps, secret, or approval boundaries. |
| Platform maintainer | Locate a work unit's requirement, design, plan, and evidence from one identifier.        | Approves protected-surface changes; does not authorize remote or live mutation.              |
| Quality engineer    | Keep one validator per enforced rule and delete validators whose contract is retired.    | Owns validator and fixture changes; may not remove a gate without retiring its rule.         |
| Technical writer    | Author a document without reading ten overlapping rule files first.                      | Follows the selected profile; does not invent new document types.                            |
| AI agent            | Load a bounded governance context and resolve the correct target path deterministically. | Must follow bootstrap JIT loading, approval boundaries, and archive inviolability.           |

## Key Use Cases

An engineer starting a new work unit creates one numbered folder under the
specification stage and authors the specification, plan, and task evidence
inside it, without choosing between three filename conventions.

A reviewer tracing a requirement to its verification reads the lineage fields
in the specification's frontmatter and follows one link per hop, with a
validator proving that each hop is reciprocal.

A governance steward changing an authoring rule edits exactly one file and
knows that no other file restates the same rule.

An agent resuming work reads a bounded current progress ledger rather than a
14,000-line append-only history.

An auditor inspecting a retired document reads its archive record and finds the
payload byte-identical to the original Git blob, with its historical links
resolving against the commit at which it was archived.

## Functional Requirements

| Requirement ID | Requirement                                                                                                                                                                  | Priority | Verification intent                                                                                                                                                            |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| REQ-WDTC-001   | Co-locate each work unit's specification, plan, and task evidence in one numbered folder under the specification stage, and retire the separate execution stage.             | Must     | Every work unit that had a same-slug plan and task resolves to `spec.md`, `plan.md`, and `tasks.md` in one folder, and no live path under the retired execution stage remains. |
| REQ-WDTC-002   | Remove dates from authored document filenames and retain the date in frontmatter only.                                                                                       | Must     | No live authored document filename under stages 01 through 04 begins with a date, and every migrated document preserves its original `updated` value.                          |
| REQ-WDTC-003   | Renumber the operations stage so that the stage sequence is contiguous after the execution stage is retired.                                                                 | Must     | The operations stage resolves at its new number, and every tracked reference to the former number is rewritten.                                                                |
| REQ-WDTC-004   | Keep per-stage identifier sequences stable and express cross-stage lineage in machine-readable frontmatter fields.                                                           | Must     | No existing PRD, ARD, ADR, or specification number changes, and a validator rejects a specification whose declared lineage lacks a reciprocal upstream link.                   |
| REQ-WDTC-005   | Reduce the authoring rule set to one owning document per rule family and delete restated rule text.                                                                          | Must     | The document-authoring rule corpus is three documents, each rule appears once, and no document declares an authority boundary for a rule another document also states.         |
| REQ-WDTC-006   | Retire the rule that execution records remain date-based from every document that states it.                                                                                 | Must     | The retired sentence appears in no live governance document, and validators no longer encode a date-based execution path.                                                      |
| REQ-WDTC-007   | Rotate the shared progress ledger so that the live file holds only the current period and prior periods move to archive records.                                             | Must     | The live ledger is materially smaller, the archived periods are recoverable, and progress-ledger validation passes.                                                            |
| REQ-WDTC-008   | Reduce the document profile registry by removing profiles that exist only to validate template forms.                                                                        | Must     | Template forms are validated through their corresponding authored profile, the registry is materially smaller, and route coverage rejects no previously covered path.          |
| REQ-WDTC-009   | Consolidate the agent governance machine contracts and their schemas into fewer owners without losing an enforced rule.                                                      | Must     | Every rule enforced before consolidation is still enforced after it, and the contract corpus is materially smaller.                                                            |
| REQ-WDTC-010   | Delete completed one-shot migration census data and the validators that read only that data.                                                                                 | Must     | The census files and their exclusive validators are removed, and no remaining validator or document references them.                                                           |
| REQ-WDTC-011   | Consolidate duplicated research and audit packs into their surviving owners.                                                                                                 | Should   | Superseded pack members are archived with an explicit supersession link, and no two live reference documents claim the same observation ownership.                             |
| REQ-WDTC-012   | Close the ten recorded documentation gaps by either implementing the control or recording an evidence-backed decision not to.                                                | Must     | Each gap identifier has an implemented control or a dated recorded decision naming its rationale and owner.                                                                    |
| REQ-WDTC-013   | Align the script surface with the canonical validator selection contract so that no validator exists outside a declared lane and no declared lane names a missing validator. | Must     | The declared validator set and the executable validator set agree, and the repository quality gate passes.                                                                     |
| REQ-WDTC-014   | Preserve archive records as inviolable.                                                                                                                                      | Must     | No archive record payload, digest, or envelope field is modified, and archive validation passes unchanged.                                                                     |
| REQ-WDTC-015   | Suspend the in-flight delivery assurance program for the duration of this work and resume it in the consolidated structure.                                                  | Must     | The suspended program's active tranche returns to draft, its rationale is recorded, and no suspended tranche is executed during this program.                                  |
| REQ-WDTC-016   | Keep the numbered stage-prefix taxonomy unchanged apart from the retirement and renumbering this program authorizes.                                                         | Must     | No stage prefix is added or removed beyond the authorized change, and the decision to retain the scheme cites the external evidence that neither endorses nor forbids it.      |

## Success / Acceptance Criteria

| Acceptance ID | Criterion                                                                                                                                              |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ACC-WDTC-001  | One work unit resolves to one folder and one identifier, with no authored filename carrying a date under stages 01 through 04.                         |
| ACC-WDTC-002  | Cross-stage lineage is machine-readable and reciprocally validated, with no existing stage identifier renumbered.                                      |
| ACC-WDTC-003  | Each authoring rule is stated in exactly one live document, and the retired date-based execution rule appears nowhere.                                 |
| ACC-WDTC-004  | The governance corpus, machine contracts, and validator surface are measurably smaller, with a recorded before-and-after line count per reduced asset. |
| ACC-WDTC-005  | Every recorded documentation gap is closed by an implemented control or a dated recorded decision.                                                     |
| ACC-WDTC-006  | The declared and executable validator sets agree, and the repository quality gate passes at every logical commit.                                      |
| ACC-WDTC-007  | Archive validation passes with no archive payload, digest, or envelope field modified.                                                                 |
| ACC-WDTC-008  | The suspended delivery assurance program is recorded as suspended with rationale and a resumption route.                                               |

## Scope and Non-goals

In scope: the authored document taxonomy under `docs/`, authored document
filenames and identifiers, the governance rule corpus, the document profile
registry, the agent governance machine contracts, the shared progress ledger,
the reference data and research packs, the recorded documentation gaps, and the
validator and script surface that enforces those contracts.

Out of scope: the platform's desired state under `gitops/` and
`infrastructure/`; the agent role roster and its provider adapters; the subject
matter of the suspended delivery assurance program; any live cluster, hosted
CI, remote, or credential-bearing action; and the creation of new document
types for currently unoccupied documentation modes.

Explicit non-goals: this program does not remove the numbered stage-prefix
scheme, because the external research found no primary source that endorses or
forbids repository-wide numbered stage folders and the rewrite cost is
therefore unjustified. It does not create a release-notes stage, because no
reference to one exists and the repository declares no public API. It does not
renumber any existing PRD, ARD, ADR, or specification identifier.

## Risks, Dependencies, and Assumptions

| ID            | Risk, dependency, or assumption                                                                                                                    | Owner               | Mitigation or validation                                                                                                                               |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| RISK-WDTC-001 | The execution-stage retirement touches 321 tracked files and the operations renumbering touches 203, so a manual rewrite would be unreliable.      | Platform maintainer | Scripted rewrite with an explicit exclusion set, verified by the full quality gate at each logical commit.                                             |
| RISK-WDTC-002 | Archive payloads are digest-sealed and their links resolve against historical commits, so any rewrite inside them breaks validation irrecoverably. | Governance steward  | Archive paths are excluded from every rewrite; archive validation runs as a separate gate.                                                             |
| RISK-WDTC-003 | Dated reference and audit packs record point-in-time observations, so rewriting paths inside them would falsify the record.                        | Technical writer    | Reference pack path rewrites are limited to navigational links and recorded as such, or the pack is left unchanged and its historical paths annotated. |
| RISK-WDTC-004 | Consolidating the agent governance machine contracts affects the majority of declared validators and can fail closed across the whole gate.        | Quality engineer    | The contract consolidation is a single isolated logical commit that can be reverted without disturbing earlier commits.                                |
| RISK-WDTC-005 | Reducing the profile registry can silently drop route coverage and let an uncovered path pass.                                                     | Quality engineer    | Route coverage is asserted before and after with the same path inventory, and uncovered paths remain a hard failure.                                   |
| DEP-WDTC-001  | The repository quality gate is the safety net for every step and takes about two minutes on the observed baseline.                                 | Quality engineer    | The gate is run at each logical commit; a failing gate blocks the commit rather than being deferred.                                                   |
| ASM-WDTC-001  | All 24 plans and 23 tasks that have no matching specification are complete historical records.                                                     | Platform maintainer | Verified on 2026-08-07: every one of them carries `status: done`.                                                                                      |
| ASM-WDTC-002  | The suspended program's tranches have no subject overlap with this program.                                                                        | Platform maintainer | Verified by reading each tranche overview; the overlap is structural path and validator ownership only.                                                |

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner                                                                                                                                                                                                |
| -------------- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| REQ-WDTC-001   | ACC-WDTC-001         | [ARD-0011](../02.architecture/requirements/0011-document-taxonomy-consolidation-architecture.md) and [Spec 052](../03.specs/052-document-taxonomy-consolidation/spec.md) own the taxonomy and migration design. |
| REQ-WDTC-002   | ACC-WDTC-001         | N/A — Spec 052 shares the downstream owner linked in REQ-WDTC-001.                                                                                                                                              |
| REQ-WDTC-003   | ACC-WDTC-001         | N/A — Spec 052 shares the downstream owner linked in REQ-WDTC-001.                                                                                                                                              |
| REQ-WDTC-004   | ACC-WDTC-002         | N/A — ARD-0011 owns the lineage model linked in REQ-WDTC-001.                                                                                                                                                   |
| REQ-WDTC-005   | ACC-WDTC-003         | N/A — Spec 052 shares the downstream owner linked in REQ-WDTC-001.                                                                                                                                              |
| REQ-WDTC-006   | ACC-WDTC-003         | N/A — Spec 052 shares the downstream owner linked in REQ-WDTC-001.                                                                                                                                              |
| REQ-WDTC-007   | ACC-WDTC-004         | N/A — Spec 052 shares the downstream owner linked in REQ-WDTC-001.                                                                                                                                              |
| REQ-WDTC-008   | ACC-WDTC-004         | N/A — Spec 052 shares the downstream owner linked in REQ-WDTC-001.                                                                                                                                              |
| REQ-WDTC-009   | ACC-WDTC-004         | N/A — Spec 052 shares the downstream owner linked in REQ-WDTC-001.                                                                                                                                              |
| REQ-WDTC-010   | ACC-WDTC-004         | N/A — Spec 052 shares the downstream owner linked in REQ-WDTC-001.                                                                                                                                              |
| REQ-WDTC-011   | ACC-WDTC-004         | N/A — Spec 052 shares the downstream owner linked in REQ-WDTC-001.                                                                                                                                              |
| REQ-WDTC-012   | ACC-WDTC-005         | N/A — Spec 052 shares the downstream owner linked in REQ-WDTC-001.                                                                                                                                              |
| REQ-WDTC-013   | ACC-WDTC-006         | N/A — Spec 052 shares the downstream owner linked in REQ-WDTC-001.                                                                                                                                              |
| REQ-WDTC-014   | ACC-WDTC-007         | N/A — ARD-0011 owns the archive inviolability boundary linked in REQ-WDTC-001.                                                                                                                                  |
| REQ-WDTC-015 | ACC-WDTC-008 | N/A — Spec 052 owns the suspension and resumption route for the delivery assurance program named in the Overview. |
| REQ-WDTC-016   | ACC-WDTC-002         | N/A — ARD-0011 owns the retained taxonomy boundary linked in REQ-WDTC-001.                                                                                                                                      |
