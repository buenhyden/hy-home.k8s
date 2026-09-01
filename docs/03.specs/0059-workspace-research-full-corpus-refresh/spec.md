---
title: 'Workspace Research Full-Corpus Refresh Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-08-17
artifact_id: "SPEC-0059"
---

# Workspace Research Full-Corpus Refresh Technical Specification (Spec)

## Overview

This specification designs the fifth refresh cycle over the existing
[`0001-workspace-engineering`](../../90.references/research/0001-workspace-engineering/README.md)
research pack. The direct human request enumerated twenty-three research
topics. Because several request lines name more than one document family — one
line names Spec, Task, Plan, PRD, AD, and ADR, another names six operations
document types — those twenty-three lines expand onto the thirty-six
`REQ-WERPC` owner rows the pack already registers. Every request line maps onto
an existing owner, so this cycle creates no new research pack, no new topic
report, and no new requirement owner.

The request scope is byte-equivalent to
[Spec 0058](../0058-workspace-research-consistency-and-partial-refresh/spec.md).
That equivalence is the central design problem, not an incidental observation.
Specs 055, 056, and 057 each re-tested the same twelve `Partial` rows and
promoted none, because the blocking evidence classes — live cluster, hosted CI
outcome, provider runtime behavior, and human judgement — are unobtainable by
repository-static work. A fourth identical re-test would predictably produce a
fourth identical result.

This cycle therefore redirects effort to the two places where new information
is actually reachable:

- **Full-corpus external re-observation.** The twenty-four rows carrying
  `Verified` were externally checked on 2026-08-08 and, apart from the four
  re-checked on 2026-08-10, have not been re-observed since. A `Verified` claim
  that upstream has since changed is a `Contradicted` finding, and it is
  invisible to any cycle that samples only `Partial` rows. Re-observing all
  thirty-six owners is also the only reading of the request line asking for
  investigation of every category and sub-area that the prior cycles did not
  already satisfy.
- **Blocking-class closure.** Each retained `Partial` or `DEFER` row is
  classified by the evidence class that blocks it, and each class is marked
  either reachable by repository-static work or structurally unreachable
  without live, hosted, provider-runtime, or human-judgement evidence. Rows in
  the second group are closed against further static re-testing. This converts
  a repeating no-op into a one-time durable decision and is the deliverable
  that prevents a sixth cycle from repeating the fifth.

The request also asked for topic-by-topic workspace investigation. This Spec
keeps workspace re-observation a first-class deliverable separate from external
source refresh, because the two produce different evidence classes and fail
independently. That separation is inherited from Spec 057 `C-WRCP-002` and is
not re-litigated here.

Direct human approval on 2026-08-17 authorizes this standalone execution relation.
That approval selected full-corpus scope over a twelve-row repeat, full
Spec/Plan/Task lifecycle documents over a research-only change, and
append-in-place over a new dated research pack.
No separate PRD or Architecture Description is required or part of this standalone lifecycle.

## Strategic Boundaries & Non-goals

### In scope

- External source re-observation for all thirty-six `REQ-WERPC` owner rows,
  recorded as `changed`, `unchanged`, `unreachable`, or `superseded`.
- Workspace re-observation for all thirty-six owner rows, recorded separately
  from the external result.
- Blocking-class classification and closure for every retained `Partial` and
  `DEFER` row.
- Re-projection of the ten governance scopes over the refreshed findings in
  the pack's scope application index.
- Reconciliation of the documented `graphify-out/` tracking contract with its
  actual tracked file set, which currently disagree by one file.
- Removal of untracked transient artifacts that no contract references.
- Cross-link and reference reconciliation across the pack README, the research
  collection README, the source and claim ledger, and the durable progress
  ledger, applied only after all content changes are final.
- Registration of new `SRC-WERPC-078` and later source rows and
  `CLM-WERPC-011-NN` claim rows.
- Lifecycle registration of Spec 058: the `standaloneExecutions` entry in
  `docs/99.templates/registry.json`, the lineage row in
  [ADR 0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md),
  the Stage 03 and Stage 04 index rows, and the
  `POST_CLOSURE_SPEC_AUTHORITY_PATHS` allowlist entry in
  `scripts/validate-active-corpus-residue-closure.py` with its mirrored
  fixture in `tests/test_active_corpus_retention.py`.
- Logical-unit commits with repository-static validation evidence, and
  integration of the cycle branch into `main`.

### Out of scope and non-goals

- Creating a new dated research pack, a duplicate report, or a parallel
  scope-view folder. The human decision on 2026-08-17 selected append-in-place.
- Creating, renumbering, or rewriting any existing `REQ-WERPC` requirement ID,
  `SRC-WERPC` source ID, or `CLM-WERPC` claim ID.
- Adding any H2 heading to any touched document. Every profile in scope
  declares `headings.allowed` equal to `headings.required`, so dated findings
  are added as H3 sections under existing H2 owners.
- Live k3d, ArgoCD, Vault, ESO, cluster, gateway, or registry inspection.
- Hosted CI execution, deployment, promotion, or rollback evidence.
- Provider-runtime discovery, authentication, delegated execution, hook
  delivery, or model resolution evidence.
- Deletion of `graphify-out/GRAPH_REPORT.md`, `graph.json`, or `graph.html`.
  These are referenced by `README.md`, `.codex/CODEX.md`, `.codex/hooks.json`,
  the harness catalog, and four validator or profile rules, so they are a live
  convention rather than one-off residue.
- Any change to `.worktrees/docs-sdlc-governance-consolidation` or its branch.
  Its thirty-six unmerged commits belong to a different session and are
  reported as an observation only, following the Spec 057 precedent.
- Any manifest, workflow, permission, hook, or policy mutation. Validator and
  fixture edits are limited to mechanical allowlist registration of this Spec.
- Pushing any branch to a remote, or publishing any artifact.
- Promotion of a `DEFER` boundary on the strength of a static or metadata
  `PASS`.

## Contracts

### C-WRFC-001 — closed topic ledger

The cycle operates on exactly thirty-six owner rows. The ledger is closed: a
finding that does not map onto an existing owner is recorded as an out-of-ledger
observation and does not create a row.

### C-WRFC-002 — dual evidence classes

Every owner row records an external result and a workspace result as separate
fields. Neither substitutes for the other, and neither is inferred from the
other. A row where one class is unreachable retains the other class rather than
degrading both.

### C-WRFC-003 — unreachable is not unchanged

An external source that cannot be retrieved is recorded as `unreachable` with
its failure mode. It is never recorded as `unchanged`. Claims resting on an
unreachable source retain their prior observation date.

### C-WRFC-004 — promotion requires a changed blocking class

A status may be promoted only when named evidence changes the class that blocked
it. A cycle that promotes nothing is a success, provided the delta and its
boundaries are recorded. This restates Spec 057 and is unchanged.

### C-WRFC-005 — blocking-class closure is terminal for static work

Each retained `Partial` or `DEFER` row is assigned exactly one blocking class.
A row whose class is `live-cluster`, `hosted-ci`, `provider-runtime`, or
`human-judgement` is closed against further repository-static re-testing, and
future cycles cite this closure instead of re-observing the row. Closure records
what evidence would reopen the row.

### C-WRFC-006 — append-only integration

Findings are added to existing pack files as dated H3 sections. No pack file is
created, renamed, or deleted, and no existing section is rewritten. The pack
file count is unchanged at fourteen.

### C-WRFC-007 — source and claim provenance

New sources continue the `SRC-WERPC` sequence from `078`. New claims use the
`CLM-WERPC-011-NN` block. A re-verification of an already registered source
creates a new source row and leaves the original `Checked on` value intact.

### C-WRFC-008 — cross-link ordering

Cross-link and count reconciliation is the last content commit of the cycle, so
that link and owner validation observes the terminal shape rather than an
intermediate one.

### C-WRFC-009 — subagent write boundary

Subagents investigate and return structured findings. They do not write, edit,
or commit any repository file. All integration writes are performed by the
orchestrating session, which is the sole allocator of source and claim
identifiers. This prevents identifier collision and concurrent-edit loss.

### C-WRFC-010 — deletion boundary

Only untracked transient artifacts that no contract references may be removed
without a further named approval. Any tracked-file deletion requires a
consumer check that enumerates every reference, and an explicit human decision
recorded in the cycle Task.

### C-WRFC-011 — formatter-safe ledger writes

Rows added to `m0012-source-coverage.md` are written through a
shell heredoc rather than the editing tools, because the Markdown formatter
re-pads every cell of a table to its widest cell and previously inflated that
file from 797 KB to 3.0 MB without changing content. Post-write byte size is
recorded as evidence.

### C-WRFC-012 — logical work units

Each work package is one commit. Temporary files created during a package are
removed before that package's commit.

## Core Design

The cycle runs as twelve work packages. Packages WRFC-002 through WRFC-006 are
mutually independent and execute in parallel through subagents; every other
package is sequential.

| ID       | Package                    | Owners touched                        |
| -------- | -------------------------- | ------------------------------------- |
| WRFC-000 | Cycle setup and baseline   | none                                  |
| WRFC-001 | Topic ledger derivation    | all 36                                |
| WRFC-002 | Agent-system research      | harness, loop, agents, model, memory  |
| WRFC-003 | Governance and providers   | workspace, common, Claude, Codex      |
| WRFC-004 | SDLC and documentation     | SDLC, 12 families, Diátaxis, LLM-WIKI |
| WRFC-005 | Platform and security      | Kubernetes, infrastructure, security  |
| WRFC-006 | Delivery evidence          | CI/CD, Actions, QA, V&V               |
| WRFC-007 | Blocking-class closure     | all retained Partial/DEFER            |
| WRFC-008 | Scope re-projection        | 10 governance scopes                  |
| WRFC-009 | Cleanup and contract fix   | graphify tracking contract            |
| WRFC-010 | Cross-link reconciliation  | pack and collection indexes           |
| WRFC-011 | Lifecycle registration     | Stage 03/04, ADR, profiles            |
| WRFC-012 | Validation and integration | none                                  |

WRFC-001 derives the thirty-six rows from the pack README coverage matrix rather
than restating them, so that a mismatch between this cycle and the pack is a
detected failure rather than a silent divergence.

WRFC-002 through WRFC-006 each receive the owner rows they cover, the current
recorded status, the current recorded source set, and the workspace paths named
in the coverage matrix. Each returns one dated finding block per owner row.

WRFC-007 consumes the five finding blocks and assigns exactly one blocking class
per retained `Partial` or `DEFER` row. It may not change a status; it records why
a status persists and what would change it.

WRFC-008 re-derives scope membership from `docs/00.agent-governance/scopes/`
rather than from the previous projection, so a scope boundary change is detected.

WRFC-010 runs after every content package and reconciles the pack file count,
the owner-row count, the source ID count, and the claim ID count across the pack
README, the research collection README, and the ledger.

## Data Modeling & Storage Strategy

Findings live with their existing owners; this cycle adds no storage location.

| Artifact               | Location                                                      |
| ---------------------- | ------------------------------------------------------------- |
| Dated finding sections | the eleven topical reports, as H3 under `Definitions / Facts` |
| Cycle reconciliation   | pack `README.md`, as H3 under `Overview`                      |
| Source and claim rows  | `m0012-source-coverage.md`                     |
| Scope projection       | `m0013-scope-application-index.md`                                  |
| Blocking-class closure | `m0013-scope-application-index.md`, as a dated H3                   |
| Durable cycle record   | `docs/00.agent-governance/memory/progress.md`                 |
| Per-package evidence   | the cycle Task                                                |

Identifier allocation is strictly sequential and single-writer. Sources begin at
`SRC-WERPC-078`; claims begin at `CLM-WERPC-011-01`. The orchestrating session
allocates every identifier before any write, so no two packages can claim the
same value.

## Interfaces & Data Structures

### Topic ledger row

| Field             | Meaning                                             |
| ----------------- | --------------------------------------------------- |
| `requestId`       | `REQ-WERPC-NNN`                                     |
| `requestLine`     | the human request line that expands onto this owner |
| `primaryOwner`    | pack report and anchor that owns the topic          |
| `priorStatus`     | status recorded before this cycle                   |
| `externalResult`  | `changed`, `unchanged`, `unreachable`, `superseded` |
| `workspaceResult` | `confirmed`, `drifted`, `absent`                    |
| `postStatus`      | status after this cycle                             |

### Refresh finding row

| Field           | Meaning                                        |
| --------------- | ---------------------------------------------- |
| `claimId`       | `CLM-WERPC-011-NN`                             |
| `requestId`     | owner row the claim binds to                   |
| `evidenceClass` | `external` or `workspace`                      |
| `sourceId`      | `SRC-WERPC-NNN` backing the claim              |
| `observedOn`    | observation date                               |
| `statusEffect`  | `no-change`, `promote`, `demote`, `contradict` |

### Blocking-class record

| Field       | Meaning                                                                           |
| ----------- | --------------------------------------------------------------------------------- |
| `requestId` | retained `Partial` or `DEFER` owner row                                           |
| `class`     | `repo-static`, `live-cluster`, `hosted-ci`, `provider-runtime`, `human-judgement` |
| `reachable` | whether repository-static work can obtain the evidence                            |
| `reopenOn`  | the named evidence that would reopen the row                                      |

### Cleanup record row

| Field       | Meaning                                     |
| ----------- | ------------------------------------------- |
| `artifact`  | path considered for removal                 |
| `tracked`   | whether Git tracks it                       |
| `consumers` | every reference found, or `none`            |
| `decision`  | `removed`, `retained`, `contract-corrected` |

## Edge Cases & Error Handling

- **A request line maps onto no owner.** Record it as an out-of-ledger
  observation in the cycle Task and leave the ledger closed. Do not create a
  requirement ID.
- **A request line maps onto more than one owner.** Expected for the two
  document-family lines. Record every owner it expands onto; the expansion is
  what produces thirty-six rows from twenty-three lines.
- **An external source is unreachable.** Record `unreachable` with the failure
  mode, retain the prior observation date, and do not degrade the workspace
  result for the same row.
- **An external source has moved or been superseded.** Register the successor as
  a new source row, record `superseded`, and leave the predecessor row intact.
- **A `Verified` row is contradicted.** Record the contradiction as a claim with
  `statusEffect` of `contradict`, demote the status, and name the source. A
  demotion is a valid outcome of this cycle.
- **A workspace path named by the coverage matrix no longer exists.** Record
  `absent`, and treat it as drift in the pack rather than a repository defect
  until the canonical owner is checked.
- **The formatter inflates the ledger.** Detected by comparing byte size before
  and after. Remediate by normalizing table-cell padding and verifying that
  `diff -w` between the pre- and post-normalization file is empty.
- **A subagent returns an unusable or empty block.** Its owner rows are recorded
  as not re-observed this cycle. A package is never reported as complete on the
  strength of a missing result.

## Failure Modes & Fallback / Human Escalation

| Failure                                    | Response                                                                 |
| ------------------------------------------ | ------------------------------------------------------------------------ |
| Every external source unreachable          | Record the cycle as workspace-only and escalate before closing the Spec  |
| Baseline validation red before work starts | Stop; do not attribute a pre-existing failure to this cycle              |
| A validator fails after integration        | Revert the offending package commit, fix, re-run the full lane           |
| Tracked-file deletion appears warranted    | Stop and request a named human decision; `C-WRFC-010` forbids proceeding |
| Owner-row count disagrees across documents | Treat as a reconciliation failure in WRFC-010, not a counting preference |
| Ledger byte size regresses past 1 MB       | Normalize padding and record the before/after evidence                   |
| Branch integration conflicts with `main`   | Stop and report; do not force any history rewrite                        |

Escalation is to the human partner in every row above. No fallback silently
lowers the evidence bar, and no static `PASS` promotes a `DEFER` boundary.

## Verification Commands

```bash
bash scripts/validate-repo-quality-gates.sh .
python3 scripts/validate-links-and-owners.py --self-test
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-reference-information-architecture.py --self-test
python3 scripts/validate-affected-surfaces.py --root .
python3 scripts/validate-active-corpus-residue-closure.py --root .
git diff --check
git diff --cached --check
```

## Success Criteria & Verification Plan

| ID           | Criterion                                                                           |
| ------------ | ----------------------------------------------------------------------------------- |
| VAL-WRFC-001 | The topic ledger records thirty-six rows with unique owners, derived from the pack  |
| VAL-WRFC-002 | Every row records an external result and a workspace result as separate fields      |
| VAL-WRFC-003 | Every retained `Partial` or `DEFER` row carries exactly one blocking-class record   |
| VAL-WRFC-004 | Source and claim IDs are unique, sequential from `078` and `011-01`, none rewritten |
| VAL-WRFC-005 | Pack file count is unchanged at fourteen and no H2 was added to any touched file    |
| VAL-WRFC-006 | Every `unreachable` source is recorded as such and never as `unchanged`             |
| VAL-WRFC-007 | Scope projection is re-derived from `scopes/`, with the unowned-path set re-tested  |
| VAL-WRFC-008 | Pack README, collection README, and ledger agree on all four counts                 |
| VAL-WRFC-009 | Cross-link reconciliation is the last content commit                                |
| VAL-WRFC-010 | The `graphify-out/` tracking contract and its tracked file set agree                |
| VAL-WRFC-011 | Ledger byte size is recorded before and after, and stays under 1 MB                 |
| VAL-WRFC-012 | All ten verification commands pass, compared against the recorded baseline          |
| VAL-WRFC-013 | One commit per work package, no temporary file survives, branch merged into `main`  |

Baseline for `VAL-WRFC-012` was captured on 2026-08-17 before any content
change: seven lanes green, contract registry at 512 paths, markdown profiles at
zero violations, affected surfaces at 22 of 22 with zero uncovered. These
results are evidence of no regression, not of a newly attained state.

## Traceability

This Spec is a research-and-refresh design requested directly by the human, who
approved full-corpus scope and the full Spec/Plan/Task lifecycle before
authoring. It creates no PRD or AD and authorizes no live, hosted, or
provider-runtime observation. It is the sixth typed standalone-execution relation
under ADR 0022, with a reciprocal
[Plan](plan.md)
and [Task](README.md#task-records)
authored under the repository's standalone execution rules. Its refresh target is
the [2026-08-08 WER pack](../../90.references/research/0001-workspace-engineering/README.md),
and its predecessor cycle is
[Spec 0058](../0058-workspace-research-consistency-and-partial-refresh/spec.md).

### Lifecycle Traceability

| PRD requirement                                                        | Spec criterion | Verification method                                |
| ---------------------------------------------------------------------- | -------------- | -------------------------------------------------- |
| N/A — direct human request for topic-complete coverage                 | VAL-WRFC-001   | Topic ledger derivation and uniqueness check       |
| N/A — direct human request for per-category workspace investigation    | VAL-WRFC-002   | Separated external and workspace evidence rows     |
| N/A — direct human request to end repeated no-op re-testing            | VAL-WRFC-003   | Blocking-class record per retained row             |
| N/A — direct human request for source-backed provenance                | VAL-WRFC-004   | Ledger comparison and ID uniqueness checks         |
| N/A — direct human decision to append to the existing pack             | VAL-WRFC-005   | Pack file inventory and heading-set check          |
| N/A — direct human request for honest source reporting                 | VAL-WRFC-006   | Unreachable-versus-unchanged content review        |
| N/A — direct human request for per-scope organization                  | VAL-WRFC-007   | Scope registry re-derivation                       |
| N/A — direct human request that cross-links reflect modifications      | VAL-WRFC-008   | Integration check across shared indexes            |
| N/A — direct human request that reconciliation observe the final state | VAL-WRFC-009   | Commit ordering of the reconciliation unit         |
| N/A — direct human request for one-off artifact cleanup                | VAL-WRFC-010   | Consumer enumeration and tracked-diff review       |
| N/A — direct human request for a maintainable reference corpus         | VAL-WRFC-011   | Ledger byte-size comparison                        |
| N/A — direct human request for validation evidence                     | VAL-WRFC-012   | Full validation lane against the recorded baseline |
| N/A — direct human request for logical-unit commits and cleanup        | VAL-WRFC-013   | Commit log, temporary-file absence, merge check    |

### Related Documents

- [ADR 0022 — direct-approval standalone execution lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [Spec 056 — Partial/DEFER incremental refresh](../0057-workspace-engineering-partial-defer-incremental-refresh/spec.md)
- [Spec 053 — research pack consolidation](../0053-workspace-engineering-research-pack-consolidation/spec.md)
- [Quality standards](../../00.agent-governance/rules/quality-standards.md)
- [Source coverage and migration ledger](../../90.references/research/0001-workspace-engineering/m0012-source-coverage.md)
