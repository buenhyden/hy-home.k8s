---
title: "Inventory, Operations and QA Baseline"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0129-TSK-0001"
parent_ids: ["SPEC-0129-PLAN-0001"]
---

# Task: Inventory, Operations and QA Baseline

## Overview

Record the tracked-file inventory, the operations survey and a staged QA
timing baseline, and make the two operations edits the survey supports. It
executes [SPEC-0129](../spec.md) through
[WORK-001–004](../plan.md#work-breakdown).

## Inputs

- Request: the operator said on 2026-10-27 to continue with the remaining
  partial CRs of the SPEC-0125 status table that need no decision.
- Start: main `3e922d51`, branch `docs/operations-survey-and-qa-baseline`.

### Tracked File Inventory

Observed on main `3e922d51` with `git ls-files -s` and content checks.

| Kind | Count | Disposition |
| --- | --- | --- |
| Tracked files | 1364 | Top level: `docs` 858, `tests` 93, `.agents` 88, `gitops` 85, `scripts` 71, `.claude` 45, `examples` 36, `.codex` 25, `infrastructure` 16, `.github` 15, `_workspace` 7, `policy` 3, `secrets` 2, root files 10 |
| Executable files | 24 | Mode `100755`; scripts and hooks |
| Symlinks | 18 | All `.claude/skills/<id>` links to `.agents/skills/<id>`; none dangling |
| Submodules | 0 | No `.gitmodules` |
| Large-file pointers | 0 | No Git LFS pointer content; `.gitattributes` sets text and line endings only |
| Binary files | 0 | Every tracked regular file is text |
| `secrets/` | 2 | `secrets/README.md` and `secrets/certs/.gitkeep`; no secret material |

The largest tracked files are the offline schema
`scripts/validation/platform/schemas/deployment-apps-v1.json` (692,047
bytes) and the research register `m0012-source-coverage.md` (504,481 bytes).

### Operations Survey

A read-only reviewer surveyed `docs/05.operations` on 2026-10-28: one guide,
five policies, twelve runbooks and an incidents README with no records. All
are active and current; none names a retired component as current.

| Finding | Files | Disposition |
| --- | --- | --- |
| The root-platform `source.path` and `targetRevision` check appears verbatim twice | RUN-0001 step 6, RUN-0002 step 9 | Fixed here: RUN-0002 step 9 refers to RUN-0001 step 6 |
| `ingressClassName: nginx` reads like the retired controller | POL-0007 section 2-2 | Fixed here: the Traefik-served compatibility class is named with ADR-0050 |
| ESO readiness, OpenBao `sys/health`, OpenBao role preconditions and the mkcert ClusterIssuer check recur with different targets or flags | RUN-0001, RUN-0002, RUN-0003, RUN-0010 | Kept: each use has its own target or stage |
| Contract-check commands are named in several runbooks and policies | RUN-0001, RUN-0002, RUN-0003, RUN-0009, POL-0003, POL-0005, POL-0007 | Kept: the validation registry owns their execution |
| RUN-0012 frontmatter `updated` (2026-10-08) precedes its last commit (2026-10-09) | RUN-0012 | Kept: correct when RUN-0012 next changes |
| Incident facts and standing guidance | `incidents/README.md`, all runbooks | Separate: no incident record exists and no runbook carries an incident timeline |

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SV-001](../spec.md#success-criteria--verification-plan) | Record the tracked-file inventory | platform | in-progress | PASS | EVD-005 closes EVD-001 |
| WORK-002 | [VAL-SV-002](../spec.md#success-criteria--verification-plan) | Record the operations survey and make its two edits | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-SV-003](../spec.md#success-criteria--verification-plan) | Record the staged QA timing baseline | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-004 | [VAL-SV-004](../spec.md#success-criteria--verification-plan) | Run staged QA and observe the hosted checks | platform | ready | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-SV-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Inventory record | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-SV-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Survey record and review | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-SV-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Timing record | Exact commits | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-SV-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Staged QA and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-SV-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Inventory record | Main `3e922d51`: `git ls-files -s` modes `100755`, `120000` and `160000`, `.gitmodules` absence, LFS pointer and NUL-byte content checks, symlink target resolution | PASS | Tracked File Inventory above: 1364 files, 24 executable, 18 resolving skill links, no submodule, LFS pointer or binary, `secrets/` holds only a README and `.gitkeep` | yes | EVD-001 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-SV-001](../spec.md#success-criteria--verification-plan) | pending | none | Inventory evidence remains | platform |
| [VAL-SV-002](../spec.md#success-criteria--verification-plan) | pending | none | Edits and review remain | platform |
| [VAL-SV-003](../spec.md#success-criteria--verification-plan) | pending | none | Timing remains | platform |
| [VAL-SV-004](../spec.md#success-criteria--verification-plan) | pending | none | Staged QA and hosted checks remain | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `docs/05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md` and
  `docs/05.operations/policies/0007-app-gitops-onboarding-policy.md`.
- **Forbidden Paths**: other operations documents, file modes, the secret
  baseline, provider settings and credentials.
- **Approval Required**: the operator said on 2026-10-27 to continue. Push,
  pull request and merge follow RUN-0013.
- **Static Validation**: `qa.py staged` on each commit.
- **Live Validation**: none; no runbook step is executed.
- **Secret / Vault Handling**: no secret is read or written.
- **Rollback Plan**: revert the pull request.
- **Evidence Location**: this Task.

## Verification Summary

Not run yet.
