---
title: "Propose Archive Reappraisal and Document Standards"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-17"
layer: "specs"
artifact_id: "SPEC-0085-TSK-0001"
---

# Task: Propose Archive Reappraisal and Document Standards

## Overview

This Task records the read-only survey behind
[ADR-0040](../../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md)
and [SPEC-0085](../spec.md), the proposal integration, and the navigation
corrections of WP-002. It closes when both are committed with staged evidence.

## Inputs

- Request of 2026-09-17 and the request owner's selection on the same day:
  WP-001 through WP-004 in this round, local logical commits without push, a
  sparse assessment table, and per-document vocabulary mapping.
- [ADR-0039](../../../02.architecture/decisions/0039-unit-archive-retention-and-citation-table.md),
  the Stage 99 registry, the Archive index, and the lifecycle, quality,
  authoring, and SDLC policies under `.agents/governance/`.
- [REQ-0003](../../../01.requirements/0003-workspace-agent-governance-platform.md).

## Task Table

| ID       | Upstream criterion | Work item                                           | Owner    | Status | Result                  | Evidence                         |
| -------- | ------------------ | --------------------------------------------------- | -------- | ------ | ----------------------- | -------------------------------- |
| WORK-001 | VAL-ARS-001        | Survey the contract, implementation, and navigation | platform | Done   | Findings recorded below | Survey                           |
| WORK-002 | VAL-ARS-002 | Propose ADR-0040 and create this package | platform | Done | ADR-0040 `proposed`, SPEC-0085 package created, indexes and REQ-0003 name them | Commit `aa64090f`; staged QA 6 PASS |
| WORK-003 | VAL-ARS-003 | Correct navigation drift in the indexes | platform | In progress | Six indexes and one policy corrected in the working tree | Quick and staged QA on the navigation commit |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/02.architecture/`, `docs/03.specs/`, the stage and
  collection indexes under `docs/`, `docs/98.archive/README.md` outside the
  Retention Catalog rows, and `.agents/governance/document-lifecycle.md`.
- **Forbidden Paths**: every retained body, sealed record, ledger, and catalog
  row under `docs/98.archive/`; `gitops/`; secrets and private configuration.
- **Approval Required**: accepting ADR-0040 needs the request owner's review of
  the written decision. Push, pull request, and merge are not approved.
- **Static Validation**: focused gates while editing, `python3 scripts/qa.py
staged` per logical commit, and the final full profile under TSK-0002.
- **Live Validation**: not run. No live cluster, provider runtime, or network
  action is authorized.
- **Secret / Vault Handling**: no secret, credential, or private configuration
  is read or printed.
- **Rollback Plan**: revert the proposal and navigation commits; neither changes
  a validator or a frozen byte.
- **Evidence Location**: this Task record.

### Survey

Read on 2026-09-17 at `980c5458` on `main`, equal to `origin/main`, with a clean
tree and the `sha1` object format. Evidence level is source reading and static
code comparison unless a row says the command was run.

#### Contract and implementation findings

| Finding                                                                                                                    | Kind                               | Evidence                                                                                                                                                                               | Disposition                         |
| -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| A retained unit has no approved exit                                                                                       | Rule conflict with the request     | `scripts/validate-document-lifecycle.py` base-row and body comparison around lines 2589 to 2616 fails any change or departure                                                          | ADR-0040, WP-003                    |
| No current judgment of retained evidence exists                                                                            | Missing capability                 | No assessment or availability value in the registry, schema, or `scripts/`; `git-history-only` is only a mode bound to `^common/template-`                                             | ADR-0040, WP-003                    |
| Citation is decided by class alone                                                                                         | Missing capability                 | `archive_dispositions.citation_decision` and the six registry rules                                                                                                                    | ADR-0040, WP-003                    |
| Reachability is checked from `HEAD`, not the default branch                                                                | Policy and implementation mismatch | ADR-0039 "An envelope stays verifiable"; `scripts/archive_cutover.py` `is_ancestor(commit, "HEAD")` near line 1108; the lifecycle gate checks the comparison base                      | ADR-0040, WP-004                    |
| The catalog commit grammar is 40 hexadecimal characters only                                                               | Policy and implementation mismatch | `scripts/archive_dispositions.py` `_COMMIT`; the lifecycle gate and `archive_recovery` accept the repository object format                                                             | WP-004                              |
| The catalog check does not detect a shallow clone                                                                          | Missing negative case              | Only first-parent history checks `--is-shallow-repository`                                                                                                                             | WP-004                              |
| All thirty-four catalog envelopes are reachable from `main` and `origin/main`                                              | Current fact, command run          | `git merge-base --is-ancestor` per distinct commit, exit 0 for all eight                                                                                                               | No existing row breaks under WP-004 |
| Lifecycle state names collide with retention class and other family names                                                  | Rule conflict                      | `lifecycle_domains` in the registry: incident `resolved` is current and `closed` terminal; requirement-architecture holds both `retired` and `withdrawn`; audit `completed` is current | WP-005 gated on its own decision    |
| Pinned historical checks compare old spellings                                                                             | Constraint                         | `scripts/validate-document-lifecycle.py` WORK054 task statuses; `scripts/validate-links-and-owners.py` pinned `done` and `accepted` comparisons                                        | WP-005 historical alias             |
| `current_executable_references` terminal set omits `withdrawn`, `retired`, `closed`, `invalidated` and includes `accepted` | Stale implementation fact          | `scripts/validation/current_executable_references.py` line 21                                                                                                                          | WP-005                              |
| No wiki-link syntax exists in the corpus or the parser                                                                     | Not applicable                     | The canonical parser handles inline and reference links, code spans, fences, and HTML comments                                                                                         | Recorded; no change                 |
| A completed unit waiting in its stage has no validator, only notes                                                         | Accepted local practice            | ADR-0039 "Completion does not authorize disposition"; SPEC-0072 and SPEC-0084 notes                                                                                                    | Kept; no new status                 |
| The quality policy uses `DEFER` for missing authority and not-yet-run alike                                                | Rule ambiguity                     | `.agents/governance/quality.md` Result vocabulary                                                                                                                                      | WP-006                              |

#### Navigation findings

| Index                                                   | Finding                                                                               | Kind                                                      | Action                                                        |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------- |
| `docs/README.md`                                        | Accurate: every superseded ADR, ADR-0038 included, is under `superseded/`             | Matches                                                   | Reviewed; no change                                           |
| `docs/01.requirements/README.md` line 109               | Names ADR-0038 as the retention authority                                             | Stale                                                     | Name ADR-0039 as current                                      |
| `docs/02.architecture/README.md` line 27                | Says ADR-0038 stays in the decision log                                               | Stale                                                     | State that it is retained under `superseded/`                 |
| `docs/02.architecture/decisions/README.md` line 65      | Tree lists `0038-six-disposition-archive-stage.md`, which is not in the directory     | Stale inventory                                           | Match the directory                                           |
| `docs/02.architecture/decisions/README.md` ADR-0039 row | Says it proposes and that validators admit only ADR-0038 routes until SPEC-0082       | Stale                                                     | State the accepted cutover                                    |
| `docs/02.architecture/descriptions/README.md`           | No finding in the ADR, archive, or inventory checks                                   | Matches                                                   | Reviewed; no change                                           |
| `docs/03.specs/README.md` line 24                       | Explains completion by ADR-0038 and says an active Spec must match the implementation | Stale; mixes target contract with observed implementation | Name ADR-0039 and separate the target from the observed state |
| `docs/03.specs/README.md` lines 72 to 73                | Present SPEC-0054 as owning integrated acceptance and WP-013 as owning the cutover    | Stale; SPEC-0054 is `done`                                | Present them as historical                                    |
| `docs/03.specs/README.md` SPEC-0062 row | Opens with the 2026-09-05 observation of seven done and three blocked Tasks | Matches: the same row records the 2026-09-16 closure as dated history | No change |
| `docs/98.archive/README.md` Retention Class             | Says any non-current document leaves Stages 01 to 99 alike                            | Too broad for Stage 99                                    | State the mode per profile                                    |
| `.agents/governance/document-lifecycle.md` line 48      | The same broad Stage 99 wording                                                       | Too broad                                                 | State the mode per profile                                    |
| `docs/99.templates/README.md` line 188                  | ADR-0038 retained sixteen rebased bodies                                              | Matches the registry                                      | No change                                                     |
| `docs/05.operations/`, `docs/90.references/` indexes    | No ADR-0038 or archive-authority residue found by search                              | Search only, not a full read                              | Recorded as searched, not as verified                         |

#### Document conformance inventory

Documents outside Stage 98, grouped by collection. A group is judged only on the
checks named in its row; a document not read in full is not reported as
conforming.

| Collection                           | Profile                         | Status counts                                                                                   | Kind                   | Checks applied                                          | Finding                                                                      | Action                                    |
| ------------------------------------ | ------------------------------- | ----------------------------------------------------------------------------------------------- | ---------------------- | ------------------------------------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------- |
| `docs/01.requirements/`              | `sdlc/requirement`              | active 4                                                                                        | Current norm           | Frontmatter and status aggregate; REQ-0003 FR-0020 read | FR-0020 has no exit from retention                                           | Amend in WP-003                           |
| `docs/02.architecture/descriptions/` | `sdlc/architecture-description` | active 4                                                                                        | Current structure      | Aggregate                                               | None found                                                                   | Review AD-0006 in WP-003                  |
| `docs/02.architecture/decisions/`    | `sdlc/architecture-decision`    | accepted 16, proposed 1 before this Task                                                        | Decisions              | Aggregate; ADR-0039 read in full                        | ADR-0039 carries a pre-cutover sentence                                      | Superseded by ADR-0040 rather than edited |
| `docs/03.specs/`                     | spec, plan, task                | spec: active 3, done 3, draft 2, withdrawn 2; task: done 27, queued 19, cancelled 16, blocked 1 | Execution records      | Aggregate; package members listed                       | SPEC-0054, SPEC-0062, and SPEC-0084 are finished and waiting for disposition | No disposition in this round              |
| `docs/05.operations/`                | guide, policy, runbook          | active 1, 5, 9                                                                                  | Current operations     | Aggregate and search                                    | No archive-contract finding; no Incident exists                              | No change                                 |
| `docs/90.references/research/`       | `reference/research`            | published 12, draft 2                                                                           | Historical observation | Aggregate                                               | None found                                                                   | No change                                 |
| `docs/99.templates/templates/`       | template profiles               | seeds only                                                                                      | Forms                  | Status seeds listed                                     | Seeds follow today's families                                                | Revisit in WP-005                         |
| `docs/98.archive/`                   | frozen and retained             | 498 files                                                                                       | Historical             | Catalog reachability run; bodies not read               | Not judged                                                                   | Frozen; no change                         |

#### Rule ownership

| Rule                            | Owner                                 | Consumers                                                  | Matches                                           |
| ------------------------------- | ------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------- |
| Lifecycle states and edges      | Stage 99 registry `lifecycle_domains` | `document_contracts`, `document_authority`, lifecycle gate | Yes, with hardcoded literals in pinned checks     |
| Retention units, classes, modes | Stage 99 registry                     | `archive_dispositions`, lifecycle and cutover gates        | Yes                                               |
| Citation into Stage 98          | Registry `archive_citation`           | `citation_decision` for the link and archive gates         | Yes, one evaluator                                |
| Envelope reachability           | ADR-0039                              | `archive_cutover`, lifecycle gate                          | No: `HEAD` and base instead of the default branch |
| Result vocabulary               | `.agents/governance/quality.md`       | `qa.py`, runner, Task evidence                             | Yes, but `DEFER` is ambiguous                     |

## Verification Summary

WORK-001 and WORK-002 are complete. Commands run: `git status`, `git log`, `git rev-parse
--show-object-format`, `git merge-base --is-ancestor` over every distinct
catalog commit against `main` and `origin/main`, and frontmatter aggregation
over tracked `docs/` files. For WORK-002, `python3 scripts/qa.py quick` first
failed `links-and-owners` on unlinked traceability cells and a missing REQ-0003
back-reference, both repaired; it then returned 6 PASS on the working tree, and
`python3 scripts/qa.py staged` returned 6 PASS on the exact index committed as
`aa64090f`, whose commit hooks and message check also passed. Hosted CI and live lanes are not
run.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result          | Evidence          |
| --------------------- | --------------- | ----------------- |
| [WORK-001](../plan.md#work-breakdown) | Survey recorded | This record |
| [WORK-002](../plan.md#work-breakdown) | Done | Commit `aa64090f`; staged QA 6 PASS |
| [WORK-003](../plan.md#work-breakdown) | Not executed | Navigation commit |
