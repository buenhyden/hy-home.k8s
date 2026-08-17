---
title: 'Workspace Research Full-Corpus Refresh Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-08-17
---

# Workspace Research Full-Corpus Refresh Plan (Plan)

## Overview

This plan executes the fifth refresh cycle designed by
[Spec 058](../../03.specs/058-workspace-research-full-corpus-refresh/spec.md)
over the existing
[2026-08-08 WER pack](../../90.references/research/2026-08-08-wer/README.md).
It sequences thirteen work packages, `WRFC-000` through `WRFC-012`, so that
external source re-observation, workspace re-observation, blocking-class
closure, scope re-projection, and cross-link reconciliation each land as one
logical commit with its own repository-static evidence.

The five research packages `WRFC-002` through `WRFC-006` run in parallel
through read-only subagents. Every other package is sequential, and cross-link
reconciliation is deliberately placed after all content work so that link and
owner validation observes the terminal shape.

## Context

Twenty-three human request lines expand onto the thirty-six `REQ-WERPC` owner
rows the pack already registers, because two request lines each name six
document families. The request scope is byte-equivalent to
Spec 057 at
`docs/03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md`,
and Specs 055, 056, and 057 each re-tested the same twelve `Partial` rows
without promoting any of them.

This cycle therefore does not repeat a twelve-row sample. It re-observes all
thirty-six owners, which reaches the twenty-four `Verified` rows that have gone
unchecked since 2026-08-08, and it closes each retained `Partial` or `DEFER`
row against further repository-static re-testing by naming the evidence class
that blocks it.

Two inherited hazards shape the sequencing. The Markdown formatter re-pads every
cell of a table to its widest cell and previously inflated the source ledger from
797 KB to 3.0 MB, so ledger rows are written through a shell heredoc. And
`scripts/validate-active-corpus-residue-closure.py` refuses to let a Spec reach
`done` unless it is registered in `POST_CLOSURE_SPEC_AUTHORITY_PATHS`, a step the
Spec 057 plan omitted and which is scheduled explicitly here.

A third hazard was discovered during setup and is recorded for successors: the
`post-validate.sh` PostToolUse hook resolves `select-affected-surfaces.py`
against `CLAUDE_PROJECT_DIR`, so an edit made inside a linked worktree fails
`SURFACE-PATH-NORMALIZATION` and is rejected. This cycle therefore executes on a
branch in the primary checkout rather than in a worktree.

## Goals & In-Scope

- Derive the thirty-six-row topic ledger from the pack rather than restating it.
- Re-observe every owner row externally and in the workspace, as separate
  results.
- Assign exactly one blocking class to every retained `Partial` or `DEFER` row,
  and record what evidence would reopen it.
- Re-project the ten governance scopes from `docs/00.agent-governance/scopes/`.
- Reconcile the documented `graphify-out/` tracking contract with the actual
  tracked file set.
- Reconcile pack file count, owner-row count, source ID count, and claim ID
  count across the pack README, the collection README, and the ledger.
- Register Spec 058 across every lifecycle surface that a closed cycle Spec
  requires.
- Land one commit per work package and integrate the branch into `main`.

## Non-Goals & Out-of-Scope

- Creating a new research pack, a duplicate report, or a parallel scope-view
  folder.
- Creating, renumbering, or rewriting any existing requirement, source, or claim
  identifier.
- Adding any H2 heading to any touched document.
- Live k3d, ArgoCD, Vault, ESO, cluster, gateway, or registry inspection.
- Hosted CI execution, workflow dispatch, deployment, promotion, or rollback.
- Provider-runtime discovery, authentication, hook delivery, permission
  enforcement, or model resolution evidence.
- Deleting `graphify-out/GRAPH_REPORT.md`, `graph.json`, or `graph.html`, which
  are live convention referenced by `README.md`, `.codex/CODEX.md`,
  `.codex/hooks.json`, the harness catalog, and four validator or profile rules.
- Any change to `.worktrees/docs-sdlc-governance-consolidation` or its branch.
- Pushing any branch to a remote or publishing any artifact.

## Work Breakdown

| ID       | Package                    | Depends on    | Parallel |
| -------- | -------------------------- | ------------- | -------- |
| WRFC-000 | Cycle setup and baseline   | none          | no       |
| WRFC-001 | Topic ledger derivation    | WRFC-000      | no       |
| WRFC-002 | Agent-system research      | WRFC-001      | yes      |
| WRFC-003 | Governance and providers   | WRFC-001      | yes      |
| WRFC-004 | SDLC and documentation     | WRFC-001      | yes      |
| WRFC-005 | Platform and security      | WRFC-001      | yes      |
| WRFC-006 | Delivery evidence          | WRFC-001      | yes      |
| WRFC-007 | Blocking-class closure     | WRFC-002..006 | no       |
| WRFC-008 | Scope re-projection        | WRFC-007      | no       |
| WRFC-009 | Cleanup and contract fix   | WRFC-001      | no       |
| WRFC-010 | Cross-link reconciliation  | WRFC-002..009 | no       |
| WRFC-011 | Lifecycle registration     | WRFC-010      | no       |
| WRFC-012 | Validation and integration | WRFC-011      | no       |

### WRFC-000 — cycle setup and baseline

Capture the full validation lane before any content change, so that a later
failure is attributable. Record the branch, its base commit, and the observation
that `.worktrees/docs-sdlc-governance-consolidation` is left untouched.

### WRFC-001 — topic ledger derivation

Parse the pack README coverage matrix and assert thirty-six unique
`REQ-WERPC` rows with no numbering gap. Map each of the twenty-three human
request lines onto its owners and assert the union is exactly the thirty-six
rows. A mismatch fails the package rather than being reconciled silently.

### WRFC-002 through WRFC-006 — parallel research

Each package receives its owner rows, the current recorded status, the pinned
source set, and the workspace paths named by the coverage matrix. Each returns
one dated finding block per row carrying an external result, a workspace result,
a status effect, a blocking class, and a reopen condition. Subagents are
read-only by tool grant, which enforces the Spec `C-WRFC-009` write boundary
structurally rather than by instruction.

Package assignment covers the ledger exactly once: nine rows to `WRFC-002`,
four to `WRFC-003`, sixteen to `WRFC-004`, three to `WRFC-005`, and four to
`WRFC-006`.

### WRFC-007 — blocking-class closure

Assign one blocking class per retained `Partial` or `DEFER` row and mark it
reachable or structurally unreachable by repository-static work. This package
may not change a status; it records why a status persists.

### WRFC-008 — scope re-projection

Re-derive scope membership from `docs/00.agent-governance/scopes/` and re-test
the unowned canonical path set, then update the pack scope application index.

### WRFC-009 — cleanup and contract fix

Enumerate every reference to each cleanup candidate before acting. Remove only
untracked transient artifacts that no contract references. Where the documented
contract and the tracked file set disagree, correct the contract rather than
delete tracked content, and record the decision.

### WRFC-010 — cross-link reconciliation

Reconcile the four counts across the pack README, the collection README, and the
ledger, then apply cross-link and reference updates. This is the last content
commit of the cycle.

### WRFC-011 — lifecycle registration

Add the Stage 03 and Stage 04 index rows and tree entries, the
`standaloneExecutions` entry in `document-profiles.json`, the ADR 0022 lineage
row, the `POST_CLOSURE_SPEC_AUTHORITY_PATHS` allowlist entry, its mirrored test
fixture, and the durable progress ledger record.

### WRFC-012 — validation and integration

Run the full lane, compare against the `WRFC-000` baseline, integrate the branch
into `main`, and remove the cycle branch. Report any worktree that could not be
removed under the active permission boundary.

## Verification Plan

| ID           | Package       | Verification                                                              |
| ------------ | ------------- | ------------------------------------------------------------------------- |
| VAL-WRFC-001 | WRFC-001      | Thirty-six unique rows derived from the pack, no gap, request union exact |
| VAL-WRFC-002 | WRFC-002..006 | Every row records external and workspace results separately               |
| VAL-WRFC-003 | WRFC-007      | Every retained Partial or DEFER row carries one blocking-class record     |
| VAL-WRFC-004 | WRFC-002..006 | Source and claim IDs unique, sequential, none rewritten                   |
| VAL-WRFC-005 | WRFC-002..006 | Pack file count unchanged at fourteen, no H2 added                        |
| VAL-WRFC-006 | WRFC-002..006 | Every unreachable source recorded as such, never as unchanged             |
| VAL-WRFC-007 | WRFC-008      | Scope projection re-derived, unowned-path set re-tested                   |
| VAL-WRFC-008 | WRFC-010      | Pack README, collection README, and ledger agree on four counts           |
| VAL-WRFC-009 | WRFC-010      | Cross-link reconciliation is the last content commit                      |
| VAL-WRFC-010 | WRFC-009      | graphify tracking contract and tracked file set agree                     |
| VAL-WRFC-011 | WRFC-010      | Ledger byte size recorded before and after, under 1 MB                    |
| VAL-WRFC-012 | WRFC-012      | All ten verification commands pass against the recorded baseline          |
| VAL-WRFC-013 | WRFC-000..012 | One commit per package, no temporary file survives, branch merged         |

Verification commands are owned by
[Spec 058](../../03.specs/058-workspace-research-full-corpus-refresh/spec.md)
and are not restated here.

## Risks & Mitigations

| Risk                                             | Mitigation                                                                  |
| ------------------------------------------------ | --------------------------------------------------------------------------- |
| Cycle repeats Spec 057 and adds nothing          | Full-corpus scope plus terminal blocking-class closure, both new this cycle |
| Formatter inflates the source ledger             | Heredoc writes plus recorded before/after byte size                         |
| Spec cannot reach `done`                         | `POST_CLOSURE_SPEC_AUTHORITY_PATHS` registration scheduled in WRFC-011      |
| Subagent writes cause identifier collision       | Read-only tool grant; orchestrator is sole identifier allocator             |
| Unreachable source silently read as unchanged    | `C-WRFC-003` forbids it; `VAL-WRFC-006` checks it                           |
| Link validation observes an intermediate shape   | Reconciliation ordered last by `C-WRFC-008`                                 |
| Tracked content deleted without consumer proof   | `C-WRFC-010` requires enumeration and a named human decision                |
| Hook rejects edits made inside a linked worktree | Execute on a branch in the primary checkout; recorded in Context            |
| Branch integration conflicts with `main`         | Stop and report; no history rewrite                                         |

## Completion Criteria

- All thirteen packages committed, one commit each.
- All thirteen `VAL-WRFC` criteria satisfied or explicitly recorded as not met.
- Full validation lane green and compared against the `WRFC-000` baseline.
- Branch integrated into `main` and the cycle branch removed.
- Durable progress ledger records the cycle, its evidence, and its handoff.
- No live, hosted, provider-runtime, remote, secret-value, push, publish, or
  deployment evidence claimed.

## Traceability

### Lifecycle Traceability

| Spec criterion                                                                    | Work package  | Expected Task                                                                                                                                 |
| --------------------------------------------------------------------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| [VAL-WRFC-001](../../03.specs/058-workspace-research-full-corpus-refresh/spec.md) | WRFC-001      | [WRFC-001](../tasks/2026-08-17-workspace-research-full-corpus-refresh.md) will record the thirty-six-row topic ledger derived from the pack   |
| [VAL-WRFC-002](../../03.specs/058-workspace-research-full-corpus-refresh/spec.md) | WRFC-002..006 | [WRFC-002..006](../tasks/2026-08-17-workspace-research-full-corpus-refresh.md) will record separated external and workspace results per row   |
| [VAL-WRFC-003](../../03.specs/058-workspace-research-full-corpus-refresh/spec.md) | WRFC-007      | [WRFC-007](../tasks/2026-08-17-workspace-research-full-corpus-refresh.md) will record one blocking class per retained Partial or DEFER row    |
| [VAL-WRFC-004](../../03.specs/058-workspace-research-full-corpus-refresh/spec.md) | WRFC-002..006 | [WRFC-002..006](../tasks/2026-08-17-workspace-research-full-corpus-refresh.md) will record ledger comparison and identifier uniqueness        |
| [VAL-WRFC-005](../../03.specs/058-workspace-research-full-corpus-refresh/spec.md) | WRFC-002..006 | [WRFC-002..006](../tasks/2026-08-17-workspace-research-full-corpus-refresh.md) will record the unchanged pack inventory and heading-set check |
| [VAL-WRFC-006](../../03.specs/058-workspace-research-full-corpus-refresh/spec.md) | WRFC-002..006 | [WRFC-002..006](../tasks/2026-08-17-workspace-research-full-corpus-refresh.md) will record every unreachable source as unreachable            |
| [VAL-WRFC-007](../../03.specs/058-workspace-research-full-corpus-refresh/spec.md) | WRFC-008      | [WRFC-008](../tasks/2026-08-17-workspace-research-full-corpus-refresh.md) will record scope re-derivation and the unowned-path re-test        |
| [VAL-WRFC-008](../../03.specs/058-workspace-research-full-corpus-refresh/spec.md) | WRFC-010      | [WRFC-010](../tasks/2026-08-17-workspace-research-full-corpus-refresh.md) will record cross-document agreement on all four counts             |
| [VAL-WRFC-009](../../03.specs/058-workspace-research-full-corpus-refresh/spec.md) | WRFC-010      | [WRFC-010](../tasks/2026-08-17-workspace-research-full-corpus-refresh.md) will record reconciliation as the last content commit               |
| [VAL-WRFC-010](../../03.specs/058-workspace-research-full-corpus-refresh/spec.md) | WRFC-009      | [WRFC-009](../tasks/2026-08-17-workspace-research-full-corpus-refresh.md) will record the graphify consumer enumeration and contract decision |
| [VAL-WRFC-011](../../03.specs/058-workspace-research-full-corpus-refresh/spec.md) | WRFC-010      | [WRFC-010](../tasks/2026-08-17-workspace-research-full-corpus-refresh.md) will record ledger byte size before and after                       |
| [VAL-WRFC-012](../../03.specs/058-workspace-research-full-corpus-refresh/spec.md) | WRFC-012      | [WRFC-012](../tasks/2026-08-17-workspace-research-full-corpus-refresh.md) will record full lane results compared against the baseline         |
| [VAL-WRFC-013](../../03.specs/058-workspace-research-full-corpus-refresh/spec.md) | WRFC-000..012 | [WRFC-000..012](../tasks/2026-08-17-workspace-research-full-corpus-refresh.md) will record one commit per package and the terminal tree state |

### Related Documents

The owning Spec and the reciprocal Task already link reciprocally in the
`### Lifecycle Traceability` table above, so they are recorded here as code
literals rather than duplicated links.

- Owning Spec: `docs/03.specs/058-workspace-research-full-corpus-refresh/spec.md`
- Reciprocal Task:
  `docs/04.execution/tasks/2026-08-17-workspace-research-full-corpus-refresh.md`
- [ADR 0022 — direct-approval standalone execution lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [Quality standards](../../00.agent-governance/rules/quality-standards.md)
- [Source coverage and migration ledger](../../90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md)
- [Scope application index](../../90.references/research/2026-08-08-wer/scope-application-index.md)
