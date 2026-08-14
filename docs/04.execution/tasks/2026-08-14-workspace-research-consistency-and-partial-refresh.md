---
title: 'Task: Workspace Research Consistency and Partial Refresh'
type: sdlc/task
status: active
owner: platform
updated: 2026-08-14
---

# Task: Workspace Research Consistency and Partial Refresh

## Overview

This Task is the durable execution and evidence ledger for the direct
human-approved [Spec 057](../../03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md)
and its reciprocal
[Implementation Plan](../plans/2026-08-14-workspace-research-consistency-and-partial-refresh.md).
Direct human approval on 2026-08-14 authorizes this standalone execution relation.
No separate PRD or ARD is required or part of this standalone lifecycle.
The typed relation is governed by
[ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md).

This Task tracks the eight-work-package cycle over the existing
`2026-08-08-wer` research pack: a constraint-consistency pass over scope
projection, approved one-off artifact cleanup, and a dated re-observation of
the twelve `Partial` requirement rows. WRCP-000 activates the standalone
execution relation itself; WRCP-001 through WRCP-007 execute and close the
remaining work packages defined by the Plan.

## Inputs

- [Spec 057](../../03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md)
- [Implementation Plan](../plans/2026-08-14-workspace-research-consistency-and-partial-refresh.md)
- [ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [Document profile registry](../../99.templates/support/document-profiles.json)
- Direct human approval of the written Spec and Plan on 2026-08-14

### Topic ledger

The following thirty-six-row ledger is closed for this cycle: twenty-one
`reconfirm-verified` rows, twelve `refresh-partial` rows (`REQ-WERPC-006`,
`008`, `009`, `014`, `020`, `022`, `023`, `025`, `026`, `028`, `032`, `033`),
and three `admit-new-owner` rows (`REQ-WERPC-034`, `035`, `036`) admitted by
Spec 057 amendment `C-WRCP-010` for the Spec, Task, and Plan document
families, which previously had no requirement owner in the coverage matrix.
Task 7 creates the three new owner rows; this ledger only records them.

| Request line                                     | Primary owner   | Disposition        |
| ------------------------------------------------ | --------------- | ------------------ |
| Harness engineering                              | `REQ-WERPC-001` | reconfirm-verified |
| Loop engineering                                 | `REQ-WERPC-002` | reconfirm-verified |
| Workspace application system, environment, rules | `REQ-WERPC-003` | reconfirm-verified |
| Claude implementation status                     | `REQ-WERPC-004` | reconfirm-verified |
| Codex implementation status                      | `REQ-WERPC-005` | reconfirm-verified |
| Claude/Codex common environment and rules        | `REQ-WERPC-006` | refresh-partial    |
| Spec-driven development                          | `REQ-WERPC-007` | reconfirm-verified |
| Kubernetes                                       | `REQ-WERPC-008` | refresh-partial    |
| Infrastructure                                   | `REQ-WERPC-009` | refresh-partial    |
| SDLC                                             | `REQ-WERPC-010` | reconfirm-verified |
| PRD                                              | `REQ-WERPC-011` | reconfirm-verified |
| ARD                                              | `REQ-WERPC-012` | reconfirm-verified |
| ADR                                              | `REQ-WERPC-013` | reconfirm-verified |
| Guide                                            | `REQ-WERPC-014` | refresh-partial    |
| Incident                                         | `REQ-WERPC-015` | reconfirm-verified |
| Postmortem                                       | `REQ-WERPC-016` | reconfirm-verified |
| Policy                                           | `REQ-WERPC-017` | reconfirm-verified |
| Release                                          | `REQ-WERPC-018` | reconfirm-verified |
| Runbook                                          | `REQ-WERPC-019` | reconfirm-verified |
| Documentation and Diátaxis                       | `REQ-WERPC-020` | refresh-partial    |
| LLM-WIKI                                         | `REQ-WERPC-021` | reconfirm-verified |
| CI/CD                                            | `REQ-WERPC-022` | refresh-partial    |
| GitHub Actions                                   | `REQ-WERPC-023` | refresh-partial    |
| QA                                               | `REQ-WERPC-024` | reconfirm-verified |
| Security                                         | `REQ-WERPC-025` | refresh-partial    |
| AI agent systems                                 | `REQ-WERPC-026` | refresh-partial    |
| agency-agents                                    | `REQ-WERPC-027` | reconfirm-verified |
| Task-fit model and configuration                 | `REQ-WERPC-028` | refresh-partial    |
| Short-term memory                                | `REQ-WERPC-029` | reconfirm-verified |
| Long-term memory                                 | `REQ-WERPC-030` | reconfirm-verified |
| Domain-scoped memory                             | `REQ-WERPC-031` | reconfirm-verified |
| Memory management                                | `REQ-WERPC-032` | refresh-partial    |
| Verification and Validation                      | `REQ-WERPC-033` | refresh-partial    |
| Spec document family                             | `REQ-WERPC-034` | admit-new-owner    |
| Task document family                             | `REQ-WERPC-035` | admit-new-owner    |
| Plan document family                             | `REQ-WERPC-036` | admit-new-owner    |

Assertion: 36 total rows, 21 `reconfirm-verified`, 12 `refresh-partial`, 3
`admit-new-owner`. This matches the closed count; no row was added or
widened beyond what this table lists.

### Cleanup record

The Step 3 consumer check was first run unscoped and returned six matches,
all of them self-referential mentions of the target path inside Spec 057
and the reciprocal Plan — the two governance documents that describe this
very cleanup step, not a functional or informational dependency on the
snapshot's content. That unscoped check could never pass, since it grepped
the documents authorizing the deletion. The Plan was corrected in commit
`c90dba04` to exclude both self-referencing documents from the match set.
The corrected check
(`rtk proxy grep -rn "graphify-out/2026-06-04" --include="*.md"
--include="*.json" --include="*.py" --include="*.sh" --include="*.yaml"
--include="*.yml" docs/ scripts/ tests/ .github/ .claude/ .codex/ .agents/
.gemini/ .pre-commit-config.yaml .gitignore | rtk proxy grep -v
"057-workspace-research-consistency-and-partial-refresh" | rtk proxy grep
-v "2026-08-14-workspace-research-consistency-and-partial-refresh"`)
returned zero matches: no script, validator, fixture, config, or workflow
depends on the snapshot. Both approved targets were removed this cycle.

| Target                                          | Tracking state    | Consumer check | Action        |
| ----------------------------------------------- | ----------------- | -------------- | ------------- |
| `graphify-out/2026-06-04/`                      | tracked           | no-consumer    | removed       |
| `sessions/2026-08-11-session.md` and two others | untracked-ignored | no-consumer    | removed       |
| `.worktrees/docs-sdlc-governance-consolidation` | untracked-ignored | not-applicable | reported-only |

The `.worktrees/docs-sdlc-governance-consolidation` worktree's branch is 32
commits ahead of and 58 behind `main`, so it holds unmerged work and is an
explicit non-goal of this cycle.

## Task Table

| ID       | Upstream criterion                           | Work item                                    | Owner           | Status      | Result                                                                                                                                                                                                                    | Evidence                                                                                    |
| -------- | -------------------------------------------- | -------------------------------------------- | --------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| WRCP-000 | VAL-WRCP-001–011                             | Activate the standalone execution            | primary agent   | In Progress | Activation is in progress: registry entry, ADR reciprocity, three `active` statuses, and stage indexes are being recorded in this commit.                                                                                 | This Task, Spec 057, reciprocal Plan, ADR-0022, `standaloneExecutions` entry, stage indexes |
| WRCP-001 | VAL-WRCP-001, VAL-WRCP-005, VAL-WRCP-011     | Topic ledger and approved cleanup            | assigned worker | Done        | Topic ledger frozen (36 rows: 21 reconfirm-verified, 12 refresh-partial, 3 admit-new-owner). Consumer check found no real consumer, so both approved cleanup targets were removed; the worktree observation was recorded. | This Task's Topic ledger and Cleanup record subsections                                     |
| WRCP-002 | VAL-WRCP-002–004, VAL-WRCP-006, VAL-WRCP-011 | Governance, agents, model, memory refresh    | assigned worker | Queued      | Not executed.                                                                                                                                                                                                             | Not applicable                                                                              |
| WRCP-003 | VAL-WRCP-002–004, VAL-WRCP-006, VAL-WRCP-011 | Kubernetes, infrastructure, security refresh | assigned worker | Queued      | Not executed.                                                                                                                                                                                                             | Not applicable                                                                              |
| WRCP-004 | VAL-WRCP-002–004, VAL-WRCP-006, VAL-WRCP-011 | Guide, Diátaxis, SDLC refresh                | assigned worker | Queued      | Not executed.                                                                                                                                                                                                             | Not applicable                                                                              |
| WRCP-005 | VAL-WRCP-002–004, VAL-WRCP-006, VAL-WRCP-011 | CI/CD, Actions, QA, V&V refresh              | assigned worker | Queued      | Not executed.                                                                                                                                                                                                             | Not applicable                                                                              |
| WRCP-006 | VAL-WRCP-007–009, VAL-WRCP-011               | Scope re-projection and reconciliation       | assigned worker | Queued      | Not executed.                                                                                                                                                                                                             | Not applicable                                                                              |
| WRCP-007 | VAL-WRCP-010–012                             | Validation closure and lifecycle done        | primary agent   | Queued      | Not executed.                                                                                                                                                                                                             | Not applicable                                                                              |

## Approval and Safety Boundaries

- **Allowed Paths**: this Task; Spec 057 and its index; the reciprocal Plan and
  its index; ADR-0022; `docs/99.templates/support/document-profiles.json`;
  `docs/04.execution/plans/README.md`; `docs/04.execution/tasks/README.md`;
  and only this ignored report:
  `.superpowers/sdd/2026-08-14-workspace-research-consistency-and-partial-refresh/task-1-report.md`.
- **Forbidden Paths**: `docs/98.archive/**`; protected Current or retired audit
  bodies; research-pack content before WRCP-001 admission; GitHub, workflow,
  GitOps, infrastructure, provider, model, memory-contract, secret, credential,
  user/global configuration, remote, and live-system surfaces; and unrelated
  user changes.
- **Approval Required**: any research beyond approved WRCP work packages,
  remote mutation, secret or variable access, provider or cluster access,
  implementation/configuration change, destructive action, push, pull request,
  merge, or authority/scope expansion.
- **Static Validation**: strict registry, Markdown-profile, and links/owners
  checks; `git diff --check` and `git diff --cached --check`.
- **Live Validation**: `DEFER`; WRCP-000 performs no remote, provider-runtime,
  hosted, credential-bearing, cluster, infrastructure, or live validation.
- **Secret / Vault Handling**: no secret or credential is read, written, or
  printed; none is in scope for this activation.
- **Rollback Plan**: revert the single activation commit; no other lifecycle
  state depends on it yet.
- **Evidence Location**: this Task's Verification Summary and Traceability
  sections, and the activation commit recorded in Step 10.

## Verification Summary

The pre-activation baseline run of
`python3 scripts/validate-links-and-owners.py --root . --mode strict` on a
clean working tree returned:

```text
PASS CROSS-DOCUMENT . cross-document expected="valid" actual="valid" owner="cross-document-validator"
```

This is a valid draft-state baseline, not a fabricated failure.

After the activation edits (Task creation; ADR reciprocal row and prose;
Spec `### Related Documents` and Overview approval statements; Plan
Lifecycle Traceability link conversion; registry `standaloneExecutions`
entry; frontmatter `status: active` on Spec, Plan, and Task; and stage index
updates), the following strict validators were run on the staged tree:

- `python3 scripts/validate-links-and-owners.py --root . --mode strict`
- `python3 scripts/validate-markdown-profiles.py --root . --mode strict`
- `python3 scripts/validate-document-contract-registry.py --root . --mode strict`
- `git diff --check && git diff --cached --check`

Their exact final output lines:

```text
PASS CROSS-DOCUMENT . cross-document expected="valid" actual="valid" owner="cross-document-validator"
PASS SUMMARY . - expected="no violations" actual="0" owner="markdown-profile-validator"
PASS document contract registry: 512 paths (strict, tracked-only plus explicit includes)
```

Both `git diff --check` and `git diff --cached --check` exited 0 with no
whitespace errors. Full command transcripts are recorded in the ignored
task-1 report at
`.superpowers/sdd/2026-08-14-workspace-research-consistency-and-partial-refresh/task-1-report.md`.

Two intermediate transient diagnostics were observed and resolved before this
final run, not fabricated failures: `PROGRAM-LINEAGE-EXECUTION-GATE` between
Step 1 (Task frontmatter set `active`) and Step 6 (registry entry added), and
`REGISTRY_STANDALONE_STATE` between Step 6 (registry `state: active`) and
Step 7 (Spec/Plan frontmatter set `active`). Both are expected artifacts of
the documented step ordering and cleared once the later step ran.

Remote, hosted-runtime, provider-runtime, credential-bearing, cluster,
infrastructure, and live evidence remain `DEFER` for WRCP-000; this activation
performs repository-static edits only.

## Traceability

### Lifecycle Traceability

| Criterion / work item                                                                                                                                  | Result                                                                                                                                                                                                                 | Evidence                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| [WRCP-000](../plans/2026-08-14-workspace-research-consistency-and-partial-refresh.md#task-1-wrcp-000--activate-the-standalone-execution)               | In progress. The direct-approval standalone execution relation is being activated in this commit: registry entry, ADR reciprocity, three `active` statuses, stage indexes, and converted Lifecycle Traceability links. | This Task, Spec 057, reciprocal Plan, ADR-0022, `standaloneExecutions` entry, activation commit |
| [WRCP-001](../plans/2026-08-14-workspace-research-consistency-and-partial-refresh.md#task-2-wrcp-001--topic-ledger-and-approved-cleanup)               | Not yet executed.                                                                                                                                                                                                      | Not applicable                                                                                  |
| [WRCP-002](../plans/2026-08-14-workspace-research-consistency-and-partial-refresh.md#task-3-wrcp-002--governance-agents-model-memory-refresh)          | Not yet executed.                                                                                                                                                                                                      | Not applicable                                                                                  |
| [WRCP-003](../plans/2026-08-14-workspace-research-consistency-and-partial-refresh.md#task-4-wrcp-003--kubernetes-infrastructure-security-refresh)      | Not yet executed.                                                                                                                                                                                                      | Not applicable                                                                                  |
| [WRCP-004](../plans/2026-08-14-workspace-research-consistency-and-partial-refresh.md#task-5-wrcp-004--guide-diátaxis-sdlc-and-document-family-refresh) | Not yet executed.                                                                                                                                                                                                      | Not applicable                                                                                  |
| [WRCP-005](../plans/2026-08-14-workspace-research-consistency-and-partial-refresh.md#task-6-wrcp-005--cicd-actions-qa-vv-refresh)                      | Not yet executed.                                                                                                                                                                                                      | Not applicable                                                                                  |
| [WRCP-006](../plans/2026-08-14-workspace-research-consistency-and-partial-refresh.md#task-7-wrcp-006--scope-re-projection-and-reconciliation)          | Not yet executed.                                                                                                                                                                                                      | Not applicable                                                                                  |
| [WRCP-007](../plans/2026-08-14-workspace-research-consistency-and-partial-refresh.md#task-8-wrcp-007--validation-closure-and-lifecycle-done)           | Not yet executed.                                                                                                                                                                                                      | Not applicable                                                                                  |
