---
title: "Hosted QA Cleanup"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0015"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Hosted QA Cleanup

## Overview

Execute the explicitly requested hosted QA removal with honest remaining CI
results and fail-closed provenance. This follows completed local integration;
it does not discard passing regressions or earlier evidence.

## Inputs

- [VAL-P02-015](../spec.md#success-criteria--verification-plan) and
  [WORK-015](../plan.md#work-breakdown).
- Latest user instruction: remove failing GitHub Actions tests/QA stages,
  integrate locally independently of remote results, and reflect origin/main.
- Accepted local main `3ff0ab627f887d7d75aa545560a051477731d285`.
- CI/quality/governance owners' read-only bounded consumer plans; source writes
  remain held until ready. No new RED/GREEN or remote outcome is observed yet.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-015 | [VAL-P02-015](../spec.md#success-criteria--verification-plan) | Retire hosted full-QA execution and update direct consumers | platform | frontmatter | NOT_RUN | pending | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-150 | [VAL-P02-015](../spec.md#success-criteria--verification-plan) | WORK-015 | Scope and registered-form creation preflight | Local accepted main 3ff0ab62; original registered Task form | NOT_RUN | Pending | pending |

## Approval and Safety Boundaries

- **Allowed Paths**: This Spec/Plan/Task; `scripts/README.md` current delivery
  guidance only; `.github/workflows/ci.yml`, `.github/workflows/qa-verifier.yml`,
  `.github/repository-surface.md`, `.github/rulesets/main-protection.md`,
  `.github/PULL_REQUEST_TEMPLATE.md`; `scripts/validate-ci-python-contract.py`,
  `scripts/validation/repository/quality.py`, `tests/test_validate_ci_python_contract.py`,
  `tests/test_ci_qa_workflow.py`; `.agents/governance/quality.md` current delivery
  guidance and `.agents/workflows/work-lifecycle.md` Completion step 2 only.
- **Forbidden Paths**: Registry/schema/Archive, production regressions and proof
  implementation, old Task evidence, native/private/global configuration,
  hooks, limits, remote protection administration and all unrelated consumers.
- **Approval Required**: Latest explicit user scope authorizes these normal
  commits, local integration and origin/main reflection without remote-QA
  dependence. Remote writes belong to the separately assigned delivery owner;
  authentication and observed remote outcomes are not inferred.
- **Static Validation**: Actual registered-form creation metadata; bounded named
  RED/GREEN, scoped final-byte tools, each actual-index staged/message and
  separate review; prospective scoped completion then fresh actual closing
  checks. Full/affected/discovery execution remains NOT_RUN.
- **Live Validation**: DEFER; no cluster, runtime or native trust operation.
- **Secret / Vault Handling**: No secret reads; private raw direct audit remains
  NOT_OBSERVED/DEFER and is not granted by this CI instruction.
- **Rollback Plan**: Reviewed normal forward correction with all history,
  branches, worktrees and original evidence preserved.
- **Evidence Location**: This Task and exact structured check receipts; ignored
  proposal/closing attachments capture actual identities without self-SHA edits.

## Verification Summary

Draft scope only. The target hosted topology is branch-policy, qa-isolated and
ci-summary; the summary reports full QA NOT_RUN and never fabricates proof.
Provenance verification is explicitly inactive while its Python refusals and
dependent publisher gating remain. Direct stale consumer changes are bounded;
passing production tests and local validation registry entries are retained.

Four normal commits will record draft, ready, implementation and completion.
Workflow, registered-validator/tests and governance writers own disjoint paths;
this document writer alone stages and commits. Initial creation metadata,
source RED/GREEN, own index/message checks and closing acceptance are pending.
No current-source or hosted PASS is inferred from the removal request. Removed
GitHub QA and excluded local full/affected execution remain NOT_RUN; remote
outcomes and integrated-main results are recorded only if observed.

