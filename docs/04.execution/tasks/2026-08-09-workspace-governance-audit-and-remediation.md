---
title: 'Task: Workspace Governance Audit and Remediation'
type: sdlc/task
status: active
owner: platform
updated: 2026-08-09
---

# Task: Workspace Governance Audit and Remediation

## Overview

This Task is the durable execution and evidence ledger for the approved
[Workspace Governance Audit and Remediation Plan](../plans/2026-08-09-workspace-governance-audit-and-remediation.md)
and [Spec 054](../../03.specs/054-workspace-governance-audit-and-remediation/spec.md).
It tracks the exact ten-file Current audit pack, canonical-owner audit and
remediation, machine-contract cutover, evidence-gated cleanup, independent
reviews, terminal verification, and lifecycle closure.

Detailed worker and review reports live under the ignored SDD directory
`.superpowers/sdd/2026-08-09-workspace-governance-audit-and-remediation/` while
the branch is active. This Task records only durable results, exact evidence,
limitations, logical commits, and unresolved blockers.

## Inputs

- [Spec 054](../../03.specs/054-workspace-governance-audit-and-remediation/spec.md)
- [Implementation Plan](../plans/2026-08-09-workspace-governance-audit-and-remediation.md)
- [ADR-0022](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [Audit collection](../../90.references/audits/README.md)
- [Document profile registry](../../99.templates/support/document-profiles.json)
- [RIA data owner](../../90.references/data/reference-information-architecture.json)
- Direct human design approval and Spec approval on 2026-08-09

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WGIA-000 | VAL-WGA-001, VAL-WGA-012 | Activate Spec/Plan/Task and standalone execution relation | primary agent | Done | Active reciprocal execution is registered. Approval-date regression reproduced RED and is GREEN after exact ISO calendar-date parsing; focused checks and the complete repository quality gate pass. | Spec 054, ADR-0022, reciprocal Plan/Task, indexes, `standaloneExecutions` row, links/owners fixture/self-test; strict registry 492 paths; Markdown profiles 0; strict links PASS; Ruff/compile/diff PASS; Python review Approved; Spec review finding fixed. |
| WGIA-001 | VAL-WGA-001, VAL-WGA-002 | Freeze observation identity and establish exact pack/finding contracts | assigned worker | Queued | Not executed. | Exact 10-file/30-row checks, source inventory, negative fixtures, review reports. |
| WGIA-002 | VAL-WGA-002, VAL-WGA-003 | Audit purpose, roles, governance, operating contracts, and provider shims | assigned worker | Queued | Not executed. | Governance report, owner matrix, finding register, focused gates and reviews. |
| WGIA-003 | VAL-WGA-002, VAL-WGA-004 | Audit SDD, SDLC, documentation, templates, README rules, and guides | assigned worker | Queued | Not executed. | Documentation report, registry/template evidence, focused gates and reviews. |
| WGIA-004 | VAL-WGA-002, VAL-WGA-005 | Audit CI/CD, GitHub Actions, QA, formatting, lint, syntax, tests, fixtures, Validation and Verification | assigned worker | Queued | Not executed. | Delivery/QA report, lane matrix, dormant-control disposition, gates and reviews. |
| WGIA-005 | VAL-WGA-002, VAL-WGA-006 | Audit harness, loop, scripts, fixtures, checkpoints, blockers, recovery, and handoff | assigned worker | Queued | Not executed. | Harness/loop report, state/owner matrices, focused gates and reviews. |
| WGIA-006 | VAL-WGA-002, VAL-WGA-007 | Audit LLM-WIKI, knowledge routing, and memory classes | assigned worker | Queued | Not executed. | Knowledge/memory report, generator and lifecycle evidence, reviews. |
| WGIA-007 | VAL-WGA-002, VAL-WGA-008 | Audit integrated orchestration and every current AI-agent role | assigned worker | Queued | Not executed. | Exact role/adaptor/model/evaluation matrix, focused gates and reviews. |
| WGIA-008 | VAL-WGA-002, VAL-WGA-009 | Audit security and approval boundaries | assigned worker | Queued | Not executed. | Security report, trust/control matrix, static gate evidence and review. |
| WGIA-009 | VAL-WGA-010, VAL-WGA-012 | Build disposition ledger and integrated remediation roadmap | assigned worker | Queued | Not executed. | Candidate/consumer ledger, roadmap, review dispositions, focused gates. |
| WGIA-010 | VAL-WGA-003, VAL-WGA-004, VAL-WGA-007, VAL-WGA-012 | Correct accepted governance, documentation, and knowledge owner conflicts | assigned worker | Queued | Not executed. | RED/GREEN tests, canonical-owner diffs or reviewed no-delta evidence. |
| WGIA-011 | VAL-WGA-005, VAL-WGA-006, VAL-WGA-008, VAL-WGA-009, VAL-WGA-012 | Correct accepted delivery, harness, agent, and security owner conflicts | assigned worker | Queued | Not executed. | RED/GREEN tests, owner-family commits or reviewed no-delta evidence. |
| WGIA-012 | VAL-WGA-011 | Cut over the sole Current audit and mutable consumers atomically | assigned worker | Queued | Not executed. | RIA/profile/index/link RED/GREEN, protected historical baseline, atomic commit. |
| WGIA-013 | VAL-WGA-010 | Delete only proof-complete candidate artifacts | assigned worker | Queued | Not executed. | Zero-consumer proof, isolated/staged post-delete validation, exact deletions or reviewed no-deletion result. |
| WGIA-014 | VAL-WGA-001–012 | Re-audit, close criteria, run terminal QA/reviews, clean residue, and hand off branch finishing | primary agent | Queued | Not executed. | Criterion walk, complete gates, whole-branch review, logical commit ledger, done lifecycle. |

## Approval and Safety Boundaries

- **Allowed Paths**: repository-static owners under root governance adapters,
  `docs/00.agent-governance/**`, `docs/01.requirements/**` through
  `docs/05.operations/**`, `docs/90.references/**` except protected historical
  bodies unless navigation metadata is explicitly mutable, `docs/99.templates/**`,
  `.github/**`, `scripts/**`, `tests/**`, and exact proven deletion candidates.
- **Forbidden Paths**: every existing `docs/98.archive/**` payload, digest,
  envelope, and record; unrelated user changes; user/global provider config;
  secret values; remote or live resources.
- **Approval Required**: any change to approved PRD/ARD/accepted ADR/operations
  policy, ambiguous architecture or authority, live/provider/hosted/remote
  action, credential handling, destructive external action, push, PR, or merge.
- **Static Validation**: exact work-package checks plus strict registry,
  Markdown profiles, links/owners, RIA, generated-index checks, affected
  validators, archive validation, full quality gate, harness, diff checks, and
  pre-commit when available.
- **Live Validation**: `DEFER`; this execution has no live, hosted, provider-
  runtime, authenticated, credential-bearing, or remote authorization.
- **Secret / Vault Handling**: do not read, print, copy, rotate, or write secret
  values. Static secret-reference and policy structure may be inspected.
- **Rollback Plan**: keep every non-empty work package in a logical commit;
  revert the affected unit. Current-pointer and deletion changes are separate
  commits validated in staged or isolated trees before commit.
- **Evidence Location**: this Task, the ten-file audit pack, canonical owner
  diffs and tests, durable progress, Git commits, and ignored task/review
  reports while execution is active.

## Verification Summary

WGIA-000 activation is complete. No topic audit, canonical remediation,
Current pointer cutover, or deletion is complete. The
2026-07-11 audit remains Current until WGIA-012 passes atomically. Repository-
static evidence will be recorded per work package; hosted, provider-runtime,
remote, credential-bearing, and live evidence remains `DEFER`.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WGIA-000](../plans/2026-08-09-workspace-governance-audit-and-remediation.md#work-breakdown) | Done. | RED: the different valid approval date was rejected with `STANDALONE-EXECUTION-APPROVAL`. GREEN: links/owners self-test accepts both valid dates and rejects the invalid calendar date. Strict registry reports 492 paths with 0 uncovered/ambiguous; Markdown profiles report 0 violations; strict links, Ruff, Python compile, cached diff, and complete repository quality gate pass. Python review is Approved; the Spec review's sole index-drift finding was fixed and no other Critical/Important finding remained. |
| N/A — WGIA-001 shares the Plan and Spec sources above | Queued. | Exact pack/finding contract evidence will be recorded here. |
| N/A — WGIA-002 shares the Plan and Spec sources above | Queued. | Governance audit and review evidence will be recorded here. |
| N/A — WGIA-003 shares the Plan and Spec sources above | Queued. | SDLC/document/template audit evidence will be recorded here. |
| N/A — WGIA-004 shares the Plan and Spec sources above | Queued. | CI/QA/Validation/Verification audit evidence will be recorded here. |
| N/A — WGIA-005 shares the Plan and Spec sources above | Queued. | Harness/loop/script/blocker audit evidence will be recorded here. |
| N/A — WGIA-006 shares the Plan and Spec sources above | Queued. | LLM-WIKI and memory audit evidence will be recorded here. |
| N/A — WGIA-007 shares the Plan and Spec sources above | Queued. | Integrated and role-specific agent audit evidence will be recorded here. |
| N/A — WGIA-008 shares the Plan and Spec sources above | Queued. | Security/approval audit evidence will be recorded here. |
| N/A — WGIA-009 shares the Plan and Spec sources above | Queued. | Candidate disposition and integrated roadmap evidence will be recorded here. |
| N/A — WGIA-010 shares the Plan and Spec sources above | Queued. | Governance/documentation/knowledge remediation evidence will be recorded here. |
| N/A — WGIA-011 shares the Plan and Spec sources above | Queued. | Delivery/harness/agent/security remediation evidence will be recorded here. |
| N/A — WGIA-012 shares the Plan and Spec sources above | Queued. | Atomic Current transition evidence will be recorded here. |
| N/A — WGIA-013 shares the Plan and Spec sources above | Queued. | Exact deletion or reviewed no-deletion evidence will be recorded here. |
| N/A — WGIA-014 shares the Plan and Spec sources above | Queued. | Terminal criterion, QA, review, residue, and closure evidence will be recorded here. |
