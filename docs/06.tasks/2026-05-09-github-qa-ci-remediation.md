---
title: 'Task: .github QA and CI Remediation'
type: task
status: done
owner: 'platform'
updated: 2026-05-09
---

# Task: .github QA and CI Remediation

## Overview (KR)

이 문서는 `.github/` QA, CI, 브랜치 정책 보정 작업의 구현·검증 작업 목록이다.
Plan에서 파생된 작업을 추적 가능하게 기록한다.

## Inputs

- **Parent Spec**: not applicable; this remediation does not introduce a new Kubernetes or runtime contract.
- **Parent Plan**: [`../05.plans/2026-05-09-github-qa-ci-remediation.md`](../05.plans/2026-05-09-github-qa-ci-remediation.md)

## Working Rules

- Documentation-only and workflow-only changes still need validation evidence.
- Keep CI role separation intact: `pre-commit`, `repo-quality-static`, `manifest-static`, and `shell-static`.
- Do not add deployment, direct cluster mutation, or publishing commands to GitHub Actions.
- Do not modify GitHub branch protection/ruleset settings in this work item.
- This document remains the execution-tracking source of truth for this remediation.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Add PR-only `branch-policy` and manual `workflow_dispatch` to CI | impl | n/a | PLN-001 | `ci.yml` contains branch policy gate and manual trigger | Platform | Done |
| T-002 | Add explicit job timeouts and maintenance workflow concurrency | impl | n/a | PLN-002 | repo quality gate validates timeout and concurrency contract | Platform | Done |
| T-003 | Update `.github` hub and PR template for branch policy and QA intake | doc | n/a | PLN-003 | PR template lists target `main` and allowed source prefixes | Platform | Done |
| T-004 | Update git workflow governance branch prefixes | doc | n/a | PLN-004 | `ci/*`, `codex/*`, and `dependabot/*` are documented | Platform | Done |
| T-005 | Extend repo quality gate for `.github` CI contract checks | test | n/a | PLN-005 | quality gate covers branch-policy, dispatch, summary linkage, timeouts, and PR wording | Platform | Done |
| T-006 | Add remediation plan/task documents and stage indexes | doc | n/a | PLN-006 | `docs/05.plans/README.md` and `docs/06.tasks/README.md` include this work | Platform | Done |
| T-007 | Run repo-backed validation bundle | test | n/a | PLN-007 | validation command output reviewed | Platform | Done |

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

## Agent-specific Types (If Applicable)

- `prompt`
- `tool`
- `memory`
- `guardrail`
- `eval`
- `observability`

## Phase View (Optional)

### Phase 1

- [x] T-001 Add branch-policy and workflow_dispatch
- [x] T-002 Add timeouts and maintenance concurrency
- [x] T-003 Update `.github` hub and PR intake
- [x] T-004 Update branch governance
- [x] T-005 Extend repo quality gate
- [x] T-006 Add tracking documents and indexes

### Phase 2

- [x] T-007 Run and record repo-backed validation bundle

## Verification Summary

- **Test Commands**:
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `git diff --check`
  - `bash infrastructure/tests/verify-contracts-static.sh`
  - `bash scripts/validate-gitops-structure.sh`
  - `bash scripts/validate-k8s-manifests.sh .`
  - `bash scripts/check-secret-handling.sh .`
  - `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +`
- **Eval Commands**: not applicable; no prompt/model behavior is changed.
- **Logs / Evidence Location**: conversation validation output for this implementation turn. Local `pre-commit`, `actionlint`, `zizmor`, and `kube-linter` are optional local tools; absence should be recorded rather than installed during this remediation.

## Related Documents

- **Plan**: [`../05.plans/2026-05-09-github-qa-ci-remediation.md`](../05.plans/2026-05-09-github-qa-ci-remediation.md)
- **GitHub Hub**: [`../../.github/ABOUT.md`](../../.github/ABOUT.md)
- **PR Template**: [`../../.github/PULL_REQUEST_TEMPLATE.md`](../../.github/PULL_REQUEST_TEMPLATE.md)
- **Git Workflow**: [`../00.agent-governance/rules/git-workflow.md`](../00.agent-governance/rules/git-workflow.md)
