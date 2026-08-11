---
title: 'Task: Example IaC and Validator QA'
type: sdlc/task
status: draft
owner: platform
updated: 2026-08-02
---

# Task: Example IaC and Validator QA

## Overview

This Task is the sole durable execution-evidence owner for Spec 050. It will
record the platform-contract extension, exact Terraform/Bicep tools, provider
lock, native non-deploy results, closed-argv and artifact regressions,
README/routing/CI ownership, placeholder cleanup, QA, reviews, commits,
closure, and Spec 051 handoff. Every row is queued; this draft claims no
implementation, cloud credential, plan, deployment, hosted-current, provider,
or live result.

## Inputs

- Parent [Spec 050](spec.md)
- Parent [Implementation Plan](plan.md)
- [PRD-007](../../01.requirements/007-repository-delivery-and-platform-assurance.md),
  [AD-0010](../../02.architecture/descriptions/ad-0010-repository-delivery-evidence-architecture.md),
  and [ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- Spec 049 platform contract, exact-tool helper behavior, validation routing,
  CI owner, aggregate, and residual DEFER records
- Current AWS Terraform source/constraints/modules, Azure Bicep module graph,
  example READMEs, `.gitignore`, inventories, and tracked placeholder

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| EIVQ-000 | VAL-EIVQ-008 | Activate reciprocal Spec/Plan/Task path and program row | platform | Queued | Not executed | Staged lifecycle, strict documents, indexes, progress, and activation commit |
| EIVQ-001 | VAL-EIVQ-001, VAL-EIVQ-005 | Define focused RED closed-argv, exact-tool, root, environment, lock, syntax, and artifact expectations | platform | Queued | Not executed | Fake-tool tests and mutation results with stable rule IDs and exact argv |
| EIVQ-002 | VAL-EIVQ-001, VAL-EIVQ-005 | Extend the platform contract, extract shared tool helper, and implement the focused validator | platform | Queued | Not executed | Contract/tool versions, helper regressions, self-test, production, and unittest results |
| EIVQ-003 | VAL-EIVQ-002, VAL-EIVQ-003, VAL-EIVQ-007 | Generate/review provider lock and run Terraform fmt/backend-disabled readonly init/validate | platform | Queued | Not executed | Selected providers/hashes, exact commands, isolated cache evidence, and tracked-artifact scan |
| EIVQ-004 | VAL-EIVQ-004, VAL-EIVQ-006, VAL-EIVQ-007 | Run standalone Bicep lint/build and align example validation guidance | platform | Queued | Not executed | Per-source result/warning matrix, README parity, and no Azure provider action |
| EIVQ-005 | VAL-EIVQ-006, VAL-EIVQ-007, VAL-EIVQ-008 | Wire affected routing, aggregate, exact-tool CI, CI contract, inventories, ignore rules, and placeholder deletion once | platform | Queued | Not executed | Affected/CI/security/aggregate results, duplicate-owner count zero, non-empty corpus, and deletion evidence |
| EIVQ-006 | VAL-EIVQ-008 | Run complete QA/reviews, close reciprocal lifecycle, and hand off to Spec 051 | platform | Queued | Not executed | Full QA, formatter/diff, review dispositions, commits, cloud DEFER, and closure evidence |

## Approval and Safety Boundaries

- **Allowed Paths**: existing platform contract/schema/fixture and validator;
  new shared tool helper/example validator/test/fixtures; Terraform lock;
  `.gitignore`; validation routing/fixture; manifest CI and CI contract;
  aggregate/inventories; example READMEs and tracked placeholder; reciprocal
  SDLC documents/indexes/progress/program relation.
- **Forbidden Paths**: ignored/private files, credentials, auth files, shell
  history, RTK logs, secret values, Terraform state/plan/cache/crash/variable
  secret files, provider response bodies, compiled deployment artifacts, and
  live cloud/cluster state.
- **Approval Required**: push, PR, hosted dispatch, Terraform plan/apply/
  destroy/import/refresh/backend mutation, Azure login/deploy/what-if/resource
  read, credential use, or live mutation. None is authorized here.
- **Static Validation**: exact tool/checksum preparation, contract/helper/
  focused self-tests, fake-tool regressions, Terraform fmt/init/validate,
  Bicep lint/build, artifact scan, affected/CI/security/aggregate/all-files/
  diff, and independent requirements/quality/security/infrastructure reviews.
- **Live Validation**: `DEFER`; cloud/provider/account/subscription/cost/quota/
  IAM/runtime evidence requires a separate approved provider context.
- **Secret Handling**: child environments are allowlisted and durable output
  contains no credential variable/value or full provider response.
- **Rollback Plan**: revert closure, CI/routing/placeholder, Bicep guidance,
  Terraform lock, and contract/helper/validator packages in reverse order.
  CI workflow/contract/test and contract/helper/consumers always revert as
  matched units.
- **Evidence Location**: this Task and
  `../../00.agent-governance/memory/progress.md`.

## Verification Summary

Not executed. Implementation will record exact CLI versions/artifacts/
checksums, contract/schema versions, selected providers and lock hashes,
Terraform/Bicep argv and results, warning codes, cache/artifact boundaries,
README/routing/CI parity, formatter effects, reviews, commits, and bounded
cloud/provider DEFER. Planned commands and official release metadata are not
current PASS evidence.

## Traceability

- **Spec**: [Example IaC and Validator QA](spec.md)
- **Plan**: [Example IaC and Validator QA Implementation Plan](plan.md)
- **Predecessor**: Spec 049 Platform Validation and Security Evidence in the
  PRD-007 program lineage
- **Successor**: Spec 051 Repository Assurance Integration and Closure in the
  PRD-007 program lineage

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [EIVQ-000](plan.md#work-breakdown) | Not executed | Queued activation evidence. |
| N/A — EIVQ-001 shares the Plan and Spec sources above | Not executed | Queued focused RED and closed-command evidence. |
| N/A — EIVQ-002 shares the Plan and Spec sources above | Not executed | Queued contract/helper/validator evidence. |
| N/A — EIVQ-003 shares the Plan and Spec sources above | Not executed | Queued Terraform lock/native/artifact evidence. |
| N/A — EIVQ-004 shares the Plan and Spec sources above | Not executed | Queued Bicep and README boundary evidence. |
| N/A — EIVQ-005 shares the Plan and Spec sources above | Not executed | Queued affected/aggregate/CI/cleanup evidence. |
| N/A — EIVQ-006 shares the Plan and Spec sources above | Not executed | Queued QA, review, closure, and successor evidence. |
