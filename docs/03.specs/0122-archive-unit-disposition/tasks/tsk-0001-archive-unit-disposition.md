---
title: "Archive Unit Disposition"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0122-TSK-0001"
parent_ids: ["SPEC-0122-PLAN-0001"]
---

# Task: Archive Unit Disposition

## Overview

Remove seven consumer-free Retention Catalog units from the current tree under
[ADR-0040](../../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md)
and record each as `git-history-only`. It executes [SPEC-0122](../spec.md)
through [WORK-001–002](../plan.md#work-breakdown). This Task is the Decision
document that the seven Retention Assessment rows name.

## Inputs

- Request: the user's 2026-10-27 execution specification ranks Archive policy
  first and asks that historical payload leave the current tree once meaning,
  consumers, recovery and approval are settled.
- Approval: on 2026-10-27 the user approved disposition of exactly these seven
  units, and no other:
  - `completed/03.specs/0006-workspace-harness-gap-analysis`
  - `completed/03.specs/0071-document-taxonomy-and-form-identity-normalization`
  - `superseded/03.specs/0068-agent-projection-rendering-and-gate-reduction`
  - `superseded/03.specs/0070-retired-provider-residue-disposition`
  - `retired/03.specs/0047-current-surface-and-stash-reconciliation`
  - `retired/03.specs/0048-github-routing-and-ci-evidence`
  - `retired/03.specs/0051-repository-assurance-integration-and-closure`
- Dry-run on main `0a9e8062a914949520dcb6f12f24cf747b3aa61f`: all 64
  catalog envelopes resolve from `origin/main` with the expected object type.
  The other 57 units keep a consumer and stay `retained`.
- Assessment stays `unreviewed`: only removal eligibility was judged.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-AD-001](../spec.md#success-criteria--verification-plan) | Consumer census and isolated recovery for the seven units | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-AD-002](../spec.md#success-criteria--verification-plan) | Remove the seven units and add their assessment rows | platform | ready | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-AD-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Named deterministic check | Exact revision | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-AD-001](../spec.md#success-criteria--verification-plan) | pending | none | Consumer census and recovery remain | platform |
| [VAL-AD-002](../spec.md#success-criteria--verification-plan) | pending | none | Removal and assessment rows remain | platform |

## Approval and Safety Boundaries


- **Allowed Paths**: the seven unit directories under `docs/98.archive/`, the
  Retention Assessment table in `docs/98.archive/README.md`, this package and
  the Stage 03 README index.
- **Forbidden Paths**: every other Stage 98 payload, the frozen generation,
  catalog rows and envelopes, and completed Task facts.
- **Approval Required**: the seven removals are approved (EVD-001). Push, PR
  and merge need their own request.
- **Static Validation**: `python3 scripts/qa.py staged` on the exact index.
- **Live Validation**: not applicable; no cluster or host state changes.
- **Secret / Vault Handling**: no secret-bearing content was read or printed.
- **Rollback Plan**: availability never returns to `retained` (ADR-0040).
  Content is recovered with `git archive <envelope commit> <original path>`;
  bringing it back is a new unit under a new decision.
- **Evidence Location**: this Task. The ignored dry-run CSV under
  `_workspace/repo-support/analysis/` is a working aid, not evidence.

## Verification Summary

No unit has been removed yet. The dry-run in Inputs is a working
observation; its census and recovery are recorded as evidence when WORK-001
runs. Removal is not purification: every clone and commit that held the
bytes keeps them. Staged QA must run without the ignored `graphify-out/`
directory, because MIG-0005 retired those paths and the migration proof reads
the working tree in staged mode (a known SPEC-0120 non-goal).
