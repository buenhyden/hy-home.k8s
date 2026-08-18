---
title: 'Workspace Research Consistency and Partial Refresh Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-08-14
artifact_id: "SPEC-0058"
---

# Workspace Research Consistency and Partial Refresh Technical Specification (Spec)

## Overview

This specification designs a single combined cycle over the existing
[`2026-08-08-wer`](../../90.references/research/2026-08-08-wer/README.md)
research pack. It joins two requested workstreams that share one integration
surface: a constraint-consistency pass over scope projection, one-off artifact
cleanup, and cross-link integrity; and an incremental re-observation of the
twelve `Partial` requirement rows.

The direct human request enumerated twenty-three research topics. All but three
map onto an existing `REQ-WERPC` owner in the active pack, so this cycle
creates no new research pack and no new topic report. Because several request
lines name more than one document-family or document-type owner — one line
names the Spec, Task, Plan, PRD, ARD, and ADR families, another names six
operations document types — the twenty-three request lines expand onto
thirty-six owner rows in the topic ledger. It refreshes and reconciles what
the pack already owns.

The three exceptions are the Spec, Task, and Plan document families. The pack's
[document-family contract matrix](../../90.references/research/2026-08-08-wer/spec-driven-sdlc-and-document-contracts.md)
already describes all twelve families, but the coverage matrix registers owners
for only nine — `REQ-WERPC-011` through `REQ-WERPC-019`. Spec, Task, and Plan
therefore carry researched content with no traceable requirement owner. Three
prior refresh cycles did not surface this because no request named those
families explicitly. This cycle admits exactly three new owners to close the
gap; that is a traceability correction over existing research, not new
research.

The request also asked for topic-by-topic workspace investigation. This Spec
treats workspace re-observation as a first-class deliverable separate from
external source refresh, because the two produce different evidence classes and
fail independently.

Direct human approval on 2026-08-14 authorizes this standalone execution relation.
No separate PRD or Architecture Description is required or part of this standalone lifecycle.

### Prior-cycle constraint

The pack's own
[scope application index](../../90.references/research/2026-08-08-wer/scope-application-index.md)
records that all twelve `Partial` rows are blocked by evidence classes that
repository-static work cannot obtain: live cluster and effective RBAC, hosted
CI run outcomes, provider runtime behavior, and human usability or stakeholder
judgement. [Spec 0057](../0057-workspace-engineering-partial-defer-incremental-refresh/spec.md)
re-tested the same twelve rows on 2026-08-12 and promoted none.

This cycle therefore defines its expected outcome as a dated delta — external
source change plus workspace re-observation — and not as status promotion.
Promotion remains permitted, but only with named evidence that changes a
blocking class. A cycle that promotes nothing is a success, not a failure,
provided the delta and its boundaries are recorded.

## Strategic Boundaries & Non-goals

### In scope

- Re-projection of the ten governance scopes and the five unowned canonical
  paths recorded by the scope application index.
- Removal of superseded one-off artifacts approved by the human: the tracked
  `graphify-out/2026-06-04/` snapshot and untracked local `sessions/` files.
- Cross-link and reference reconciliation across the pack README, the research
  collection README, the source and claim ledger, and the durable progress
  ledger, applied after all content changes are final.
- External source re-check and workspace re-observation for the twelve
  `Partial` rows: `REQ-WERPC-006`, `008`, `009`, `014`, `020`, `022`, `023`,
  `025`, `026`, `028`, `032`, and `033`.
- Admission of `REQ-WERPC-034` (Spec), `REQ-WERPC-035` (Task), and
  `REQ-WERPC-036` (Plan) as coverage-matrix owners over the document-family
  matrix rows that already describe them.
- Registering Spec 057 in `POST_CLOSURE_SPEC_AUTHORITY_PATHS` in
  `scripts/validate-active-corpus-residue-closure.py`, required for this Spec
  to reach status `done` under `CLOSURE-AUTHORITY-SCOPE`, following the
  precedent of Specs `041`-`046` and `053`-`056`. This is mechanical
  registration of a closed Spec, not a change to validator behavior.
- Logical-unit commits with repository-static validation evidence.

### Out of scope and non-goals

- Creating a new dated research pack or a duplicate report.
- Creating any new `REQ-WERPC` requirement owner beyond the three admitted for
  the Spec, Task, and Plan document families.
- Renumbering or rewriting any existing source ID, claim ID, or requirement ID.
- Live k3d, ArgoCD, Vault, ESO, cluster, gateway, or registry inspection.
- Hosted CI execution, deployment, promotion, or rollback evidence.
- Provider-runtime discovery, authentication, delegated execution, or model
  resolution evidence.
- Any change to `.worktrees/docs-sdlc-governance-consolidation` or its branch.
  Its thirty-two unmerged commits are reported as an observation and left
  untouched.
- Any manifest, workflow, permission, hook, or policy mutation. This cycle is
  documentation and reference work only.
- Promotion of a `DEFER` boundary on the strength of a static or metadata
  `PASS`.

## Contracts

### C-WRCP-001 — closed topic ledger

Before any refresh work, the twenty-three requested topics are mapped onto
existing `REQ-WERPC` owners in one closed, thirty-six-row table: a request
line naming more than one document-family or document-type owner receives one
row per named owner. Each ledger row receives exactly one primary owner and
one disposition: `refresh-partial`, `reconfirm-verified`, or
`exclude-duplicate`. A topic absent from this ledger cannot gain new source,
claim, or report content.

### C-WRCP-002 — dual evidence classes

Workspace re-observation and external source re-check are recorded as separate
evidence with separate outcomes. A workspace observation may not be reported as
external source confirmation, and an unreachable external source may not be
reported as `unchanged`. An unreachable source is recorded as `unreachable`
with its prior observation date preserved.

### C-WRCP-003 — evidence-state closure

Every admitted candidate terminates as `Verified`, `Partial`, `DEFER`, or
`Contradicted`. A retained `Partial` or `DEFER` names the unavailable evidence,
the owning authority, the safe collection boundary, and the refresh trigger.
Promotion to `Verified` requires a named change in the blocking evidence class
recorded in the scope application index.

### C-WRCP-004 — source and claim provenance

New sources continue from `SRC-WERPC-074`; new claims continue from
`CLM-WERPC-010-01`. Every new source carries a unique ID, primary URL, checked
date, source status, adopted scope, rejected inference, and refresh trigger.
Every new claim carries a unique ID, supporting source IDs, exact workspace
paths or selectors, uncertainty, and evidence depth. No existing ID is
renumbered, reordered, or silently rewritten.

### C-WRCP-005 — existing-pack integration

Accepted findings are appended to their existing canonical report under a dated
`2026-08-14` subsection. The pack README, the source and claim ledger, and the
scope application index are updated atomically with the final owner
projections and counts. No new research folder or duplicate report is created.

### C-WRCP-006 — deletion boundary

Only the two human-approved cleanup targets may be removed. Removal of the
tracked `graphify-out/2026-06-04/` snapshot is preceded by a consumer check
proving no tracked document, script, validator, fixture, or configuration
references it. The untracked `sessions/` files are local-only and produce no
tracked diff. Any other candidate is reported, never deleted.

### C-WRCP-007 — cross-link ordering

Reference and cross-link reconciliation executes only after deletion and all
research appends are final, so that link validation observes the terminal
repository shape. Structural indexes that enumerate pack contents are corrected
in the same logical unit as the reconciliation.

### C-WRCP-008 — logical work units

Design, cleanup, each disjoint research workstream, scope re-projection,
cross-link reconciliation, and validation closure are separate non-empty
logical commits. Temporary working files live only under the session scratchpad
path, are content-bounded and non-secret, and are absent before terminal
validation.

### C-WRCP-009 — subagent write boundary

Research subagents are read-only. They return findings; they do not write to
tracked files. All tracked-file mutation is performed by the primary agent, so
that ledger ID allocation stays serialized and collision-free.

### C-WRCP-010 — admitted new owner boundary

Exactly three new requirement owners may be created: `REQ-WERPC-034` for the
Spec family, `REQ-WERPC-035` for the Task family, and `REQ-WERPC-036` for the
Plan family. Each is admitted only because the document-family contract matrix
already carries its research and the coverage matrix omits its owner row.

Each new owner must point at the existing matrix row as its primary owner
anchor, name its canonical workspace path, and take its status from the
evidence already recorded there plus this cycle's dated re-observation. A new
owner may not be used to introduce a topic the pack never researched, and no
fourth owner may be added under this contract. Creating these rows is a
traceability correction; it does not by itself raise or lower any status.

## Core Design

The cycle uses six bounded components executed in a fixed order. The order is
load-bearing: cleanup precedes research so that research never cites a path
scheduled for removal, and reconciliation follows both so that link validation
observes final state.

1. **Topic ledger.** Build the closed `C-WRCP-001` mapping from the twenty-three
   requested topics to the thirty-six existing and admitted owner rows, with
   dispositions.
2. **Cleanup.** Execute the two approved removals behind the `C-WRCP-006`
   consumer check. Record the stale-worktree observation without acting on it.
3. **Workspace re-observation.** For each of the twelve `Partial` rows,
   re-read the exact canonical owner paths and record what changed since the
   prior dated observation.
4. **External source re-check.** For the same twelve rows, re-check registered
   primary sources and record `unchanged`, `changed`, or `unreachable`.
5. **Scope re-projection.** Re-derive the ten scope rows and the five unowned
   canonical paths against the current scope registry.
6. **Reconciliation and closure.** Update pack README, ledger, collection
   README, and durable progress ledger; run the validation lanes.

Components 3 and 4 are disjoint per topic group and are the only parallel
stage. Under `C-WRCP-009` the parallel workers return findings only.

## Data Modeling & Storage Strategy

No schema, database, or persistent runtime store is introduced. All state is
Markdown and JSON already tracked by the repository.

| Store                   | Path                                                                                 | Role in this cycle                                    |
| ----------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------- |
| Pack README             | `docs/90.references/research/2026-08-08-wer/README.md`                               | Requirement coverage matrix and reconciliation counts |
| Source and claim ledger | `docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md` | Append-only `SRC`/`CLM` registration                  |
| Scope application index | `docs/90.references/research/2026-08-08-wer/scope-application-index.md`              | Scope re-projection and unowned-path list             |
| Topic reports           | eight owner files in the same pack                                                   | Dated `2026-08-14` subsections                        |
| Collection README       | `docs/90.references/research/README.md`                                              | Folder routing and item index                         |
| Durable progress ledger | `docs/00.agent-governance/memory/progress.md`                                        | Repo-changing work record                             |

Append-only is the governing rule for the ledger. Correction of an existing row
is expressed as a new dated row that supersedes it, never as an in-place
rewrite, so provenance survives.

## Interfaces & Data Structures

### Topic ledger row

| Field         | Values                                                       |
| ------------- | ------------------------------------------------------------ |
| Request line  | Verbatim requested topic                                     |
| Primary owner | Exactly one `REQ-WERPC-0NN`                                  |
| Disposition   | `refresh-partial`, `reconfirm-verified`, `exclude-duplicate` |

### Refresh finding row

| Field                  | Values                                                      |
| ---------------------- | ----------------------------------------------------------- |
| Requirement            | `REQ-WERPC-0NN`                                             |
| Workspace observation  | Exact path or selector plus observed delta                  |
| External source result | `unchanged`, `changed`, `unreachable`                       |
| Final disposition      | `Verified`, `Partial`, `DEFER`, `Contradicted`              |
| Retention detail       | Missing evidence, authority, safe boundary, refresh trigger |

### Cleanup record row

| Field          | Values                          |
| -------------- | ------------------------------- |
| Target         | Exact path                      |
| Tracking state | `tracked`, `untracked-ignored`  |
| Consumer check | `no-consumer`, `consumer-found` |
| Action         | `removed`, `reported-only`      |

## Edge Cases & Error Handling

- **Consumer found for a deletion target.** The removal is abandoned, the
  target is reported instead, and the finding is recorded. Deletion never
  proceeds against a live reference.
- **External source unreachable.** Recorded as `unreachable` under
  `C-WRCP-002`; the prior observation date is preserved and the requirement
  keeps its status.
- **Source contradicts a registered claim.** The contradiction is registered as
  a new dated source and claim, and the affected requirement moves to
  `Contradicted` rather than being edited into agreement.
- **Scope registry changed since 2026-08-10.** The scope row is re-derived from
  the current registry, and the change is recorded as the reason for the
  re-projection.
- **Unowned path adopted by a scope.** Removed from the unowned list with the
  owning scope named. Adding a path to a scope is a `meta` decision and is not
  performed by this cycle.
- **Status count mismatch between README and index.** The pack README is
  authoritative; the index is corrected to agree with it.
- **Validation regression after cleanup.** The cleanup commit is corrected
  before any research commit proceeds, so regressions cannot compound.

## Failure Modes & Fallback / Human Escalation

| Failure mode                                          | Detection                     | Fallback                                               | Escalation                                                  |
| ----------------------------------------------------- | ----------------------------- | ------------------------------------------------------ | ----------------------------------------------------------- |
| Deletion target has a tracked consumer                | Consumer check before removal | Report-only disposition                                | None; the contract handles it                               |
| A requested topic maps to no existing owner           | Topic ledger construction     | Halt; the cycle's no-new-owner premise is void         | Human decision on scope expansion                           |
| An external source moved or was withdrawn             | Source re-check               | Record `unreachable` or `changed`; preserve prior date | Human review if a claim is invalidated                      |
| Blocking evidence would require live or hosted access | Evidence-class check          | Retain `DEFER` with named boundary                     | Human authorization required; never self-granted            |
| Cross-document validation regresses                   | Strict validator run          | Revert the offending logical unit                      | Human review if the cause is a pre-existing contract defect |
| Ledger ID collision                                   | Uniqueness check before write | Serialize through the primary agent per `C-WRCP-009`   | None; the contract prevents it                              |
| Stale worktree pressure to clean up                   | Explicit non-goal             | Report only                                            | Human decision on the thirty-two unmerged commits           |

## Verification Commands

Repository-static validation for this cycle:

```bash
python3 scripts/validate-links-and-owners.py --self-test
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-reference-information-architecture.py --self-test
python3 scripts/validate-affected-surfaces.py --root .
bash scripts/validate-repo-quality-gates.sh .
git diff --check
git diff --cached --check
```

A baseline run on 2026-08-14 recorded `PASS` for the cross-document validator
and the repository quality gates on a clean working tree. Because the baseline
is green, the acceptance signal for this cycle is absence of regression, not
first attainment of `PASS`.

External source checks are read-only public documentation fetches. Their
success proves only what was observable at the recorded time. Their failure
proves only that the fetch was unavailable, never that a control is absent.

## Success Criteria & Verification Plan

| Criterion    | Success condition                                                                                                                                 | Verification evidence                                       |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| VAL-WRCP-001 | The twenty-three requested topics form one closed, thirty-six-row ledger, mapped onto existing owners plus exactly the three admitted new owners. | Topic ledger table and owner-uniqueness check               |
| VAL-WRCP-002 | Workspace observation and external source result are recorded separately for each of the twelve `Partial` rows.                                   | Per-requirement finding rows in the dated sections          |
| VAL-WRCP-003 | Every admitted candidate has one final disposition, and each retained `Partial` or `DEFER` names evidence, authority, boundary, and trigger.      | Content contract review of dated sections                   |
| VAL-WRCP-004 | New sources and claims continue the existing sequence with complete provenance and no existing ID is renumbered or rewritten.                     | Before/after ledger comparison and ID uniqueness check      |
| VAL-WRCP-005 | Only the two approved targets are removed, each preceded by a passing consumer check; the stale worktree is unchanged.                            | Consumer-check output, `git status`, `git worktree list`    |
| VAL-WRCP-006 | Findings are appended as dated `2026-08-14` subsections to existing reports; no new pack or duplicate report exists.                              | Exact path allowlist and pack file inventory                |
| VAL-WRCP-007 | The scope re-projection covers all ten scopes and re-tests the five unowned paths against the current registry.                                   | Scope index diff against `docs/00.agent-governance/scopes/` |
| VAL-WRCP-008 | Pack README, ledger, scope index, and collection README agree on counts and owner projections.                                                    | Integration check and strict links/owners validation        |
| VAL-WRCP-009 | Cross-link reconciliation is the last content change before validation closure.                                                                   | Commit order in the logical-unit sequence                   |
| VAL-WRCP-010 | Every validation lane returns no regression against the recorded 2026-08-14 baseline.                                                             | Task evidence with exact commands and results               |
| VAL-WRCP-011 | Each logical work unit is a separate non-empty commit and no temporary file survives.                                                             | Commit log and absence check                                |
| VAL-WRCP-012 | Exactly three new owners exist, each anchored to an existing document-family matrix row, and no fourth owner was created.                         | Coverage-matrix diff and owner-count check                  |

## Traceability

This Spec is a research-and-reconciliation design requested directly by the
human, who approved the combined workstream and the two deletion targets before
authoring. It creates no PRD or ARD, activates no execution Plan, and
authorizes no external research until the written Spec is separately approved.
After approval, a reciprocal Plan and Task are authored under the repository's
standalone execution rules.

### Lifecycle Traceability

| PRD requirement                                                      | Spec criterion | Verification method                            |
| -------------------------------------------------------------------- | -------------- | ---------------------------------------------- |
| N/A — direct human request for topic-complete research coverage      | VAL-WRCP-001   | Topic ledger and owner-uniqueness check        |
| N/A — direct human request for per-category workspace investigation  | VAL-WRCP-002   | Separated workspace and external evidence rows |
| N/A — direct human request for explicit status closure               | VAL-WRCP-003   | Content contract review                        |
| N/A — direct human request for source-backed provenance              | VAL-WRCP-004   | Ledger comparison and uniqueness checks        |
| N/A — direct human approval of two one-off cleanup targets           | VAL-WRCP-005   | Consumer check and tracked-diff review         |
| N/A — direct human request to integrate into the existing pack       | VAL-WRCP-006   | Exact path and duplicate-owner checks          |
| N/A — direct human request for per-scope organization                | VAL-WRCP-007   | Scope registry re-derivation                   |
| N/A — direct human request that cross-links reflect modifications    | VAL-WRCP-008   | Integration check across shared indexes        |
| N/A — direct human request that reconciliation observe final state   | VAL-WRCP-009   | Commit ordering of the reconciliation unit     |
| N/A — direct human request for logical-unit commits                  | VAL-WRCP-010   | Validation lane results against the baseline   |
| N/A — direct human request for a clean terminal tree                 | VAL-WRCP-011   | Commit log and temporary-file absence check    |
| N/A — direct human approval of three admitted document-family owners | VAL-WRCP-012   | Coverage-matrix diff and owner-count check     |

### Related Documents

- [Research pack README](../../90.references/research/2026-08-08-wer/README.md)
- [Scope application index](../../90.references/research/2026-08-08-wer/scope-application-index.md)
- [Source coverage and migration ledger](../../90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md)
- [Spec 053 — research pack consolidation](../053-workspace-engineering-research-pack-consolidation/spec.md)
- [Spec 055 — gap-only refresh](../0056-workspace-engineering-gap-only-refresh/spec.md)
- [Spec 056 — Partial/DEFER incremental refresh](../0057-workspace-engineering-partial-defer-incremental-refresh/spec.md)
- [Quality standards](../../00.agent-governance/rules/quality-standards.md)
- [ADR-0022 — direct-approval standalone execution lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [Implementation Plan](../../04.execution/plans/2026-08-14-workspace-research-consistency-and-partial-refresh.md)
- [Task](../../04.execution/tasks/2026-08-14-workspace-research-consistency-and-partial-refresh.md)
