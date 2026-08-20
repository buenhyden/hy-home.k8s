---
title: 'Workspace Research Full-Corpus Reverification Task'
type: sdlc/task
status: draft
owner: platform
updated: 2026-08-20
artifact_id: "TASK-0062"
---

# Workspace Research Full-Corpus Reverification Task (Task)

## Overview

This Task is the execution ledger for `WRFR-000` through `WRFR-009` in the
reciprocal [Plan](plan.md), implementing [Spec 0062](spec.md). It begins in
`draft`: the design Spec is approved, but the Plan, execution mode, remote query
allowlist, and repository mutations remain unapproved until the human reviews
this Plan.

The target is a 2026-08-20 external-source and workspace reverification of all
thirty-six existing `REQ-WERPC-*` owners, integrated into the existing
`2026-08-08-wer` pack. No research, remote GitHub query, tracked implementation,
staging, or execution commit has occurred under this Task.

## Inputs

- [Spec 0062](spec.md)
- [Plan](plan.md)
- [Current WER research pack](../../90.references/research/2026-08-08-wer/README.md)
- [Source coverage and migration ledger](../../90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md)
- [Scope application index](../../90.references/research/2026-08-08-wer/scope-application-index.md)
- [Research collection contract](../../90.references/research/README.md)
- [Quality standards](../../00.agent-governance/rules/quality-standards.md)
- [ADR 0022 — direct-approval standalone execution lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)

### Approved design baseline

| Field | Baseline |
| --- | --- |
| Canonical research pack | `docs/90.references/research/2026-08-08-wer/` |
| Pack Markdown files | 14 |
| Request owners | 36, exact IDs `001..036` |
| Source IDs | 90, terminal `SRC-WERPC-090` |
| Claim IDs | 135, terminal `CLM-WERPC-012-04` |
| New source start | `SRC-WERPC-091` |
| New claim block | `CLM-WERPC-013-NN`, starting `01` |
| Matrix states | 23 `Verified`, 1 `Verified gap`, 12 `Partial` |
| Evidence date | 2026-08-20 |
| Execution branch | `codex/2026-08-20-full-corpus-reverification` |
| Design commit | `60b1c89e38ae6a72d6cbde7e74bd580604e3a80c` |

### Closed workstream assignment

| Workstream | Exact request IDs | Topical owners |
| --- | --- | --- |
| Agent engineering | 001, 002, 026–032 | harness/loop, agents, model, memory |
| Provider/common | 003–006 | workspace governance, provider status |
| SDLC/documentation | 007, 010–021, 034–036 | SDLC/contracts, Diataxis, LLM-WIKI |
| Platform/security | 008, 009, 025 | Kubernetes/infrastructure/security |
| Delivery/quality | 022–024, 033 | CI/CD, Actions, QA, V&V |

The union is exact and disjoint. Research agents may write only their ignored
structured report. They may not edit repository files, allocate final IDs,
stage, or commit.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WRFR-000 | VAL-WRFR-012, 013 | Activate standalone lifecycle and SDD workspace | platform | Queued | Not executed | Written Spec approved; Plan review pending |
| WRFR-001 | VAL-WRFR-001..007, 009 | Freeze baseline, collect five read-only reports, allocate IDs | platform + research agents | Queued | Not executed | Exact 36-row input defined in Plan |
| WRFR-002 | VAL-WRFR-002..005, 008, 013 | Integrate agent engineering findings | agent integrator | Queued | Not executed | Awaiting reviewed agent report/allocation |
| WRFR-003 | VAL-WRFR-002..005, 008, 013 | Integrate provider/common findings | provider integrator | Queued | Not executed | Awaiting reviewed provider report/allocation |
| WRFR-004 | VAL-WRFR-002..005, 008, 013 | Integrate SDLC/documentation findings | documentation integrator | Queued | Not executed | Awaiting reviewed SDLC report/allocation |
| WRFR-005 | VAL-WRFR-002..005, 008, 013 | Integrate platform/security findings | platform/security integrator | Queued | Not executed | Awaiting reviewed platform report/allocation |
| WRFR-006 | VAL-WRFR-002..005, 008, 011, 013 | Integrate delivery/quality and read-only GitHub evidence | delivery/security integrator | Queued | Not executed | Pre-remote security review required |
| WRFR-007 | VAL-WRFR-006..010, 013 | Integrate source, claim, scope, and pack projections | sole ledger integrator | Queued | Not executed | Awaiting all five topical commits |
| WRFR-008 | VAL-WRFR-008, 010, 013 | Reconcile indexes, links, lifecycle, and progress | documentation integrator | Queued | Not executed | Awaiting terminal parsed counts |
| WRFR-009 | VAL-WRFR-010, 012..015 | Run terminal lanes, whole-branch review, closure, cleanup | platform + QA | Queued | Not executed | Awaiting WRFR-008 |

## Approval and Safety Boundaries

- **Allowed Paths**: the exact files listed under each Plan work package, this
  Plan's unique ignored SDD workspace returned from the guarded helper-Plan
  alias, and exact temporary alias
  `/tmp/0062-workspace-research-full-corpus-reverification-plan.md`.
- **Forbidden Paths**: any new research directory or topic report; policy,
  manifest, workflow, application, runtime, credential, secret, primary-checkout
  staged RIA, sibling worktree, sibling SDD workspace, and unlisted `/tmp` path.
- **Shared helper marker**: `.superpowers/sdd/.gitignore` is validated as exact
  helper state and restored to its recorded initial state. An initially absent
  marker is removed only when no foreign sibling exists; otherwise cleanup stops
  fail-closed without deleting foreign state or claiming completion.
- **Approval Required**: written Plan approval before WRFR-000; pre-remote
  security approval before any GitHub query; human finishing choice before push,
  merge, publication, branch deletion, or worktree cleanup.
- **External Research**: read-only official/primary-source retrieval; search is a
  locator and never substitutes for reading the source.
- **Remote GitHub**: exactly the nine Plan allowlisted metadata classes, at most
  once each, through the guarded checker; no dispatch, rerun, approval, merge,
  settings mutation, raw logs, tokens, or secret-bearing data.
- **Static Validation**: task-local closed-corpus checker, domain validators,
  document registry, Markdown profiles, links/owners, RIA, affected/staged lanes,
  aggregate quality, pre-commit, all-files, formatter review, and diff checks.
- **Live Validation**: `DEFER`; no live cluster, infrastructure, provider runtime,
  deployment, user, operator, or stakeholder activity is authorized.
- **Secret / Vault Handling**: no secret value, token, credential, raw workflow
  log, Vault payload, or recovery material may be read, printed, or stored.
- **Rollback Plan**: revert the exact logical commit for a tracked work package;
  no remote or live state exists to roll back. Guarded ignored artifacts remain
  available until their final consumer and are then removed with exact-path
  absence proof.
- **Evidence Location**: durable results in this Task, pack owners, source/claim
  ledger, scope index, Stage 03 index, ADR 0022, and durable progress; transient
  reports/review packages in this Plan's ignored SDD workspace only.

### Stop conditions

Execution stops only for a destructive or irreversible action, a
security-sensitive action not already approved, an external side effect such as
push/merge/publication, or a Plan defect that leaves every path forward a guess.
All other conflicts receive a recorded SDD ruling and continue under the Spec.

## Verification Summary

Execution has not started. Design-stage evidence only:

- isolated worktree created from clean tracked `HEAD`;
- primary checkout's unrelated staged RIA files excluded from the branch;
- pre-authoring `bash scripts/validate-repo-quality-gates.sh .` passed;
- strict document registry passed with 538 paths after Spec indexing;
- strict Markdown profiles reported zero violations;
- strict cross-document links and owners passed;
- design commit `60b1c89e38ae6a72d6cbde7e74bd580604e3a80c` contains only Spec 0062 and the Stage 03 index entry.

These results prove only the draft design surface. They do not prove research
currency, workspace findings, remote GitHub state, provider runtime, hosted CI,
live infrastructure, or user validation.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [VAL-WRFR-001](spec.md) | Not executed | WRFR-001 owns the exact `001..036` checker contract |
| [VAL-WRFR-002](spec.md) | Not executed | WRFR-001..007 own the dual-evidence schema defined in Plan |
| [VAL-WRFR-003](spec.md) | Not executed | WRFR-001 owns the closed workstream assignment above |
| [VAL-WRFR-004](spec.md) | Not executed | WRFR-001..007 own the source-fidelity review gate |
| [VAL-WRFR-005](spec.md) | Not executed | WRFR-001..006 own the selector/evidence-depth contract |
| [VAL-WRFR-006](spec.md) | Not executed | WRFR-001 and WRFR-007 own the closed outcome vocabulary and self-tests |
| [VAL-WRFR-007](spec.md) | Not executed | WRFR-001 and WRFR-007 own the blocking-class completeness contract |
| [VAL-WRFR-008](spec.md) | Not executed | WRFR-002..008 own the existing-owner append-only contract |
| [VAL-WRFR-009](spec.md) | Not executed | WRFR-001 and WRFR-007 own source 091 and claim block 013 continuity |
| [VAL-WRFR-010](spec.md) | Not executed | WRFR-007..009 own the shared projection sequence |
| [VAL-WRFR-011](spec.md) | Not executed | WRFR-006 and WRFR-009 own the nine-class remote/security contract |
| [VAL-WRFR-012](spec.md) | Not executed | WRFR-000 and WRFR-009 own the isolated workspace and exact cleanup contract |
| [VAL-WRFR-013](spec.md) | Not executed | WRFR-000..009 own the per-task commit/review gate |
| [VAL-WRFR-014](spec.md) | Not executed | WRFR-009 owns the whole-branch review gate |
| [VAL-WRFR-015](spec.md) | Not executed | WRFR-009 owns the terminal lane sequence |

### Related Documents

- [Spec 0062](spec.md)
- [Plan](plan.md)
- [Current WER research pack](../../90.references/research/2026-08-08-wer/README.md)
- [ADR 0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [Durable progress ledger](../../00.agent-governance/memory/progress.md)
