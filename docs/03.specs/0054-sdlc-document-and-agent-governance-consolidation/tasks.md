---
title: 'Task: SDLC Document and AI Agent Governance Consolidation'
type: sdlc/task
status: active
owner: platform
updated: 2026-08-20
artifact_id: "TASK-0054"
---

# Task: SDLC Document and AI Agent Governance Consolidation

## Overview

This transitional Task is the execution ledger for the approved
authority-first SDLC, Spec-driven development, AI-agent governance,
operations, Stage 90, Stage 98, template, validator, fixture, SHA, and script
consolidation. WP-004 migrates this single-file ledger to append-only
`tasks/tsk-####-<slug>.md` records; until that registry cutover commits, this
file remains the current lifecycle owner.

Only one row may be `In Progress` at a time; a dependency-blocked row is
`Blocked` and is not the active execution row. A row becomes `Complete` only
after focused RED/GREEN evidence, required broad gates, independent review,
and its logical commit all exist.

## Inputs

- [Spec 0054](spec.md)
- [Plan 0054](plan.md)
- Predecessor Spec 0052 and its inherited
  WORK-109 evidence
- [ADR-0022 direct approval lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [ADR-0024 historical terminal-taxonomy decision](../../02.architecture/decisions/0024-terminal-artifact-identity-and-archive-layout.md),
  superseded where ADR-0030 defines the new terminal authority
- [ADR-0030 authority-first convergence](../../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)
- The Git parent of the WP-001 design-authority commit and the exact inherited
  WORK-109 staged/unstaged inventory recorded by WP-002
- External primary-source basis embedded in [Spec 0054](spec.md#external-basis)

## Task Table

WP-004 migrates this ledger to the terminal Task identity scheme without
renumbering Plan labels:

| Plan label | Terminal Task ID | Status before execution handoff |
| --- | --- | --- |
| WP-001 | TSK-0054-0001 | done |
| WP-002 | TSK-0054-0002 | done |
| WP-003 | TSK-0054-0003 | blocked |
| WP-004 | TSK-0054-0004 | in-progress |
| WP-005 | TSK-0054-0005 | queued |
| WP-006 | TSK-0054-0006 | queued |
| WP-007 | TSK-0054-0007 | queued |
| WP-008 | TSK-0054-0008 | queued |
| WP-009 | TSK-0054-0009 | queued |
| WP-010 | TSK-0054-0010 | queued |
| WP-011 | TSK-0054-0011 | queued |
| WP-012 | TSK-0054-0012 | queued |
| WP-013 | TSK-0054-0013 | queued |
| WP-014 | TSK-0054-0014 | queued |

Each generated Task preserves its WORK row, dependency, result, evidence,
rollback, and ordered logical commit boundaries. IDs and package-local
sequences are append-only and never reused. TSK-0054-0004 changes to
`in-progress` only when the committed Plan is selected for execution.

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-054-001 | VAL-SDLC-001, VAL-SDLC-012 | Establish and amend approved design authority. | platform | Complete | Initial scope, ADR-0030, amended Spec 0054, archive recovery controls, provider security controls, and authority-first WP order are approved. | Independent architecture, Python, and security review; strict/pre-commit GREEN; logical design-authority commits, whose identities are execution evidence rather than validator pins |
| WORK-054-002 | VAL-SDLC-001..VAL-SDLC-004, VAL-SDLC-009, VAL-SDLC-011, VAL-SDLC-012 | Complete inherited-candidate disposition, direct-approval lineage, four-digit routes, route-sensitive Stage 00/99 authority, Stage 04 retirement, Incident identity, current links, and atomic migration evidence. | platform | Complete | Four-digit PRD/Spec identity, lowercase Incident routing, Stage 04 retirement, route-sensitive Stage 00/99 owners, current links, and exact migration/recovery projection are closed atomically. | Strict-cutover 49 PASS; registry 132/69/32 and strict 501/0/0; lifecycle self-test 770 and staged PASS; archive validation/cutover 58+35 PASS and production 93/711/93; affected/staged lanes exit 0 over 315 paths; plain pre-commit exit 0; Python and architecture reviews Approve with no findings |
| WORK-054-003 | VAL-SDLC-005, VAL-SDLC-011, VAL-SDLC-012 | Create the `.agents` authority, converge Stage 00 on Codex/Claude-only support, and remove Gemini/Antigravity. | platform | Blocked | Waits only for WORK-054-004 document lifecycle and generic migration/recovery authority; resumes immediately afterward. | Agent registry/policy/projection/provider-evidence/consumer-zero gates; focused tests; two logical commits |
| WORK-054-004 | VAL-SDLC-001..VAL-SDLC-006, VAL-SDLC-009, VAL-SDLC-011, VAL-SDLC-012 | Activate flat Requirement Packages, prefix-free Architecture, Spec Task packages, profile lifecycles, Stage 99 document authority, generic recovery, and responsibility-oriented document validators. | platform | In Progress | WP-004A is activating the document registry and lifecycle foundation; WP-004B and WP-004C retain the corpus and template convergence boundaries. | Focused topology/identity/lifecycle/authority RED-GREEN; strict document and recovery gates; three logical commits |
| WORK-054-005 | VAL-SDLC-003, VAL-SDLC-007, VAL-SDLC-011, VAL-SDLC-012 | Record Stage 05 Guide/Policy/Runbook/Incident/Release responsibility dispositions without mutation. | platform | Queued | Not executed. | Complete dynamic corpus coverage, duplicate/missing disposition negatives, logical commit |
| WORK-054-006 | VAL-SDLC-003, VAL-SDLC-007, VAL-SDLC-009, VAL-SDLC-011, VAL-SDLC-012 | Apply prefix-free Stage 05 consolidation, delete the Release family, and add minimal recoverable Stage 98 evidence. | platform | Queued | Not executed. | Operations profile/role/link/lifecycle/recovery and Release consumer-zero gates, logical commit |
| WORK-054-007 | VAL-SDLC-008, VAL-SDLC-011, VAL-SDLC-012 | Record one owner/freshness/disposition for every Stage 90 path and classify the preserved main-worktree RIA candidate without mutating evidence. | platform | Queued | Not executed. | Dynamic Stage 90 coverage, candidate port/rework/discard decision, RIA disposition gates, logical commit |
| WORK-054-008 | VAL-SDLC-008, VAL-SDLC-009, VAL-SDLC-011, VAL-SDLC-012 | Converge Stage 90 on numbered Research/Audit/Data packages and atomic minimal recovery evidence. | platform | Queued | Not executed. | Freshness/generator/profile/link/recovery gates and logical commit |
| WORK-054-009 | VAL-SDLC-009, VAL-SDLC-011, VAL-SDLC-012 | Reduce Archive to Git-backed Migrations/Tombstones and close reachable recovery without count/line/current-state pins. | platform | Queued | Not executed. | Archive inventory/recovery/lifecycle/link parity and logical commit |
| WORK-054-010 | VAL-SDLC-010..VAL-SDLC-012 | Close the machine ownership graph for scripts, gates, fixtures, tests, consumers, and SHA pins; remove already-safe duplicates. | platform | Queued | Not executed. | Validation registry parity, duplicate-owner/self-test/orphan-fixture/unexplained-pin negatives, logical commit |
| WORK-054-011 | VAL-SDLC-010..VAL-SDLC-012 | Move scripts/tests into responsibility directories and retire approved compatibility wrappers at consumer-zero. | platform | Queued | Not executed. | Registry/path parity, imports/CI/pre-commit/affected-lane GREEN, logical commits per responsibility batch |
| WORK-054-012 | VAL-SDLC-009..VAL-SDLC-012 | Transfer Spec 0052 WORK-113 and global progress into Spec Tasks/Git, then remove stale generated-current graph residue. | platform | Queued | Not executed. | Task ownership, archive recovery, generated-output consumer/residue gates, logical commit |
| WORK-054-013 | VAL-SDLC-009..VAL-SDLC-012 | Transfer terminal invariants, remove taxonomy transition assets/exceptions, and activate terminal route state without a fixed file census. | platform | Queued | Not executed. | Consumer-zero/recovery, validation-registry parity, terminal registry, logical commit |
| WORK-054-014 | VAL-SDLC-001..VAL-SDLC-012 | Run final convergence, independent reviews, evidence update, and branch completion. | platform | Queued | Not executed. | Fixed-point terminal validation, final reviews, closure commit, finish-branch handoff |

## Approval and Safety Boundaries

- **Allowed Paths**: repository files explicitly named by the active work
  package in [Plan 0054](plan.md#work-breakdown).
- **Forbidden Paths**: unrelated user changes; sealed Stage 98 payloads;
  unapproved live infrastructure, credentials, provider runtime, remote CI,
  release, push, merge, and publication surfaces.
- **Approval Required**: new document families, reintroducing a Release family,
  destructive history changes, credential access, live or remote mutation,
  scope beyond the approved B boundary (which already includes Stage 90), or
  deletion lacking consumer-zero and recovery evidence.
- **Static Validation**: focused unit/contract tests, affected and staged
  lanes, registry/Markdown/link/lifecycle/archive gates, aggregate quality,
  pre-commit, all-files fixed point, and diff checks as assigned by the Plan.
- **Live Validation**: DEFER. Repository-static evidence does not establish
  provider-runtime, hosted-CI, deployment, incident-response, or platform
  behavior.
- **Secret / Vault Handling**: no secret-value read or output. Only the existing
  redacted secret-handling validator and configured detect-secrets hooks may be
  used.
- **Rollback Plan**: stop at the failing work package; preserve the worktree;
  revert only that package's logical commit if authorized. Never edit sealed
  evidence as rollback.
- **Evidence Location**: this transitional Task until WP-004, then append-only
  Spec Task records, bounded machine disposition ledgers, minimal Stage 98
  Migration/Tombstone records, and Git commits.

## Verification Summary

The design-authority package and WORK-054-002 intermediate route cutover are
complete. ADR-0030 and amended Spec 0054 supersede conflicting terminal
assumptions while retaining valid four-digit/Stage 04 evidence. WORK-054-004 is
the next eligible successor; WORK-054-003 is dependency-blocked and resumes
immediately after WORK-054-004.

Each completed row must record exact commands, exit codes, finding counts,
staged-path shape, mutation status, reviewer disposition, commit identity, and
limitations. `PASS` without those bindings is insufficient.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-054-001](plan.md#wp-001--approved-design-authority) | Complete. | Human-approved Spec 0054, ADR-0030, independent reviews, and logical design-authority commits; no commit SHA is a current validator contract. |
| [WORK-054-002](plan.md#wp-002--terminal-topology-and-four-digit-identity) | Complete. | Exact four-digit and Incident route gates, `MIG-0002` 154-row authority, focused suites, affected/staged lanes, plain pre-commit, and independent reviews are GREEN. |
| [WORK-054-003](plan.md#wp-003--codexclaude-only-ai-agent-governance) | Blocked. | Waits for WORK-054-004 authorities; predecessor candidate is input only and no completion evidence is claimed. |
| [WORK-054-004](plan.md#wp-004--document-lifecycle-task-and-registry-authority-activation) | In Progress. | WP-004A document authority and lifecycle foundation is executing; exact RED/GREEN and commit evidence is recorded in its bounded task report. |
| [WORK-054-005](plan.md#wp-005--stage-05-responsibility-ledger) | Queued. | No accepted execution evidence yet. |
| [WORK-054-006](plan.md#wp-006--stage-05-ownership-cutover) | Queued. | No accepted execution evidence yet. |
| [WORK-054-007](plan.md#wp-007--stage-90-disposition-ledger) | Queued. | No accepted execution evidence yet. |
| [WORK-054-008](plan.md#wp-008--stage-90-ownership-cutover) | Queued. | No accepted execution evidence yet. |
| [WORK-054-009](plan.md#wp-009--global-stage-98-parity-and-recovery-closure) | Queued. | No accepted execution evidence yet. |
| [WORK-054-010](plan.md#wp-010--script-gate-fixture-and-sha-ownership-fixed-point) | Queued. | No accepted execution evidence yet. |
| [WORK-054-011](plan.md#wp-011--responsibility-topology-and-compatibility-cutover) | Queued. | No accepted execution evidence yet. |
| [WORK-054-012](plan.md#wp-012--progress-and-generated-current-cleanup) | Queued. | No accepted execution evidence yet. |
| [WORK-054-013](plan.md#wp-013--transition-only-taxonomy-terminal-cutover) | Queued. | No accepted execution evidence yet. |
| [WORK-054-014](plan.md#wp-014--convergence-and-branch-completion) | Queued. | No accepted execution evidence yet. |
