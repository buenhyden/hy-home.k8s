---
title: "Purpose-Based QA and CI Follow-up"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0107-TSK-0003"
parent_ids: ["SPEC-0107-PLAN-0001"]
---

# Task: Purpose-Based QA and CI Follow-up

## Overview

This Task owns P05 execution for [WORK-003](../plan.md#work-breakdown) and
[VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan). It records
the current leaf/caller/input audit, implementation and selected local
validation before the single criterion acceptance decision. Completed
[Task 0001](tsk-0001-local-qa-and-release.md) and
[Task 0002](tsk-0002-archive-and-qa-retirement.md) retain their original
results. Their earlier local and hosted observations are inputs for comparison,
not P05 execution evidence.

## Inputs

- The current [Spec](../spec.md), [Plan](../plan.md),
  [REQ-0003](../../../01.requirements/0003-workspace-agent-governance-platform.md),
  [AD-0006](../../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md),
  [ADR-0048](../../../02.architecture/decisions/0048-local-qa-and-semver-release-ownership.md),
  [quality policy](../../../../.agents/governance/quality.md),
  [validation registry](../../../../scripts/validation/registry.json), and
  [GitHub surface](../../../../.github/repository-surface.md).
- The user's current P05 request: purpose- and input-based redesign of QA,
  CI/CD gates, lint and format, with local purpose QA for this public K8s
  repository and narrow trusted-base server PR style. Investigate actual
  leaves and consumers, retain distinct continuing protection, select affected
  checks, measure duplicate execution, and report results by actual input.
  Local investigation, plan, source/consumer repair, selected checks, normal
  commits, local main integration and cleanup of owned development refs are
  authorized. Remote writes or dispatch, server settings, deployment, tag,
  secrets and live operation have their separate target and authority.
- Intake source: clean `codex/p05-purpose-qa` worktree at
  `11a1c26210c26962b9899df0f046513b7e57056f` on 2026-10-09, based on
  local `main`. Stage 99 `sdlc/spec`, `sdlc/plan` and `sdlc/task` profiles
  select the three existing forms. Before this edit, this Spec package had
  completed WORK-001/002 and Tasks 0001/0002, with no
  `VAL-LOCAL-QA-006`, `WORK-003` or `SPEC-0107-TSK-0003` in the package.
- The one common review candidate remains `WGOV-CORE / 3.0.0-draft.3`,
  proposed owner `buenhyden`, proposed source
  `Project-Template/.agents/governance/shared-standard.md`, and reviewed
  content digest
  `sha256:3f46c63daae094649edccec33682ecba99844b184c4b78b558281c7c05ff3271`.
  Stage 99 registry source revision and approval reference are null. C01,
  C06, C07 and C12 are comparison input, not a final approved edition,
  local adoption or four-repository adoption. Existing local contracts own
  this implementation while the common decision remains pending.
- Initial P05 investigation has not measured the current leaf/caller map or
  completed implementation. The coordinator's remote read of branch metadata
  and prior PR 136 CI is a dated historical input; the P05 Task must bind any
  hosted claim to its own observed SHA, run, App and protection input.
  `SEC-P01-001` HIGH remains open with the security/CI operator.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-003 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | Map purpose QA and hosted consumers; repair proven duplicate selection and evidence boundaries; measure and validate the actual P05 input | platform | frontmatter | NOT_RUN | EVD-P05-001 records only intake ownership and source; implementation and acceptance await actual evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P05-001 | [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | WORK-003 | Canonical owner, Stage 99 route and unused in-package ID audit | Local `main` source `11a1c26210c26962b9899df0f046513b7e57056f`; `git status --short --branch`, `git rev-parse HEAD`, `rg --files` and `rg -n` over this Spec package and Stage 99 registry; source files read on 2026-10-09 | PASS | This Task Inputs; Spec criterion and Plan WORK-003 link; current forms `docs/99.templates/templates/specs/{spec,plan,task}.template.md` | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-LOCAL-QA-006](../spec.md#success-criteria--verification-plan) | pending | EVD-P05-001 | Complete current consumer map, changed-rule regression, selected final-index checks, actual message, measurement and independent review; decide local acceptance from the resulting evidence | platform for local QA and documents; CI/security operator for hosted protection and `SEC-P01-001` |

## Approval and Safety Boundaries

- **Allowed Paths**: this Spec package, current local QA/validation scripts,
  tests, hooks, quality and formatting guidance, relevant Operations guidance,
  and bounded `.github/` workflow and repository-surface consumers assigned
  to a single writer. File ownership is coordinated before each edit.
- **Forbidden Paths**: frozen Archive payloads, unrelated provider or personal
  configuration, actual secrets, live Kubernetes/Vault resources and another
  writer's in-progress files.
- **Approval Required**: the current P05 request authorizes local audit,
  implementation, checks, normal logical commits, local main integration and
  owned worktree/ref cleanup. It does not authorize remote push/PR write,
  workflow dispatch, protection/ruleset mutation, Release/tag publication,
  deployment, credential use or live operation. Any such action needs its
  actual operation, target, reviewed revision and operator approval record.
- **Static Validation**: derive named regressions and selected affected/staged
  gates from the current registry and changed input. Before each normal commit,
  inspect the final index, run its read-only lint/format and applicable
  document/purpose checks, and validate the actual message. Record commands,
  tool/config/input identity, failures and explicit resolutions here.
- **Live Validation**: DEFER to the operating owner until an authorized live
  target and execution evidence exist. Prior PR checks cannot become P05
  hosted or live PASS.
- **Secret / Vault Handling**: inspect only non-secret source and metadata;
  do not read, print or transmit credentials or Vault data.
- **Rollback Plan**: use a forward correction on the isolated branch for
  source and consumer changes; preserve failed-check and completed-Task facts.
  A protected remote or live action requires its own operator rollback plan.
- **Evidence Location**: this Task, actual reviewed commits and narrowly
  scoped ignored command receipts where an exact post-commit OID cannot be
  written into its own commit. No parallel progress ledger.

## Verification Summary

Only the owner/profile/ID intake EVD-P05-001 has been observed. The current
leaf/caller/fixture census, before/after measurements, implementation,
negative regressions, exact-index QA, actual message, independent review and
local integration are pending on their future inputs. The coordinator has a
historical remote branch/PR observation, but this Task has no P05 hosted run,
settings write, dispatch, deployment, native enforcement or live PASS.
The common candidate is unapproved, and `SEC-P01-001` HIGH remains open.
