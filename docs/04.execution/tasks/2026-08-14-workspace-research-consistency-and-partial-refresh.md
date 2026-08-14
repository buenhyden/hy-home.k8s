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

## Task Table

| ID       | Upstream criterion                           | Work item                                    | Owner           | Status      | Result                                                                                                                                    | Evidence                                                                                    |
| -------- | -------------------------------------------- | -------------------------------------------- | --------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| WRCP-000 | VAL-WRCP-001–011                             | Activate the standalone execution            | primary agent   | In Progress | Activation is in progress: registry entry, ADR reciprocity, three `active` statuses, and stage indexes are being recorded in this commit. | This Task, Spec 057, reciprocal Plan, ADR-0022, `standaloneExecutions` entry, stage indexes |
| WRCP-001 | VAL-WRCP-001, VAL-WRCP-005, VAL-WRCP-011     | Topic ledger and approved cleanup            | assigned worker | Queued      | Not executed.                                                                                                                             | Not applicable                                                                              |
| WRCP-002 | VAL-WRCP-002–004, VAL-WRCP-006, VAL-WRCP-011 | Governance, agents, model, memory refresh    | assigned worker | Queued      | Not executed.                                                                                                                             | Not applicable                                                                              |
| WRCP-003 | VAL-WRCP-002–004, VAL-WRCP-006, VAL-WRCP-011 | Kubernetes, infrastructure, security refresh | assigned worker | Queued      | Not executed.                                                                                                                             | Not applicable                                                                              |
| WRCP-004 | VAL-WRCP-002–004, VAL-WRCP-006, VAL-WRCP-011 | Guide, Diátaxis, SDLC refresh                | assigned worker | Queued      | Not executed.                                                                                                                             | Not applicable                                                                              |
| WRCP-005 | VAL-WRCP-002–004, VAL-WRCP-006, VAL-WRCP-011 | CI/CD, Actions, QA, V&V refresh              | assigned worker | Queued      | Not executed.                                                                                                                             | Not applicable                                                                              |
| WRCP-006 | VAL-WRCP-007–009, VAL-WRCP-011               | Scope re-projection and reconciliation       | assigned worker | Queued      | Not executed.                                                                                                                             | Not applicable                                                                              |
| WRCP-007 | VAL-WRCP-010–012                             | Validation closure and lifecycle done        | primary agent   | Queued      | Not executed.                                                                                                                             | Not applicable                                                                              |

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
