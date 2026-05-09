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

2026-05-09 follow-up은 기존 완료 상태를 뒤집지 않고 `.github` policy SSoT와 실행 미러의 경계를 보강한다. 중복 제거 기준은 `policy SSoT + minimal executable/checklist mirrors`이며, CI job 간 방어적 중복은 의도된 QA coverage로 유지한다.

## Inputs

- **Parent Spec**: not applicable; this remediation does not introduce a new Kubernetes or runtime contract.
- **Parent Plan**: [`../05.plans/2026-05-09-github-qa-ci-remediation.md`](../05.plans/2026-05-09-github-qa-ci-remediation.md)

## Working Rules

- Documentation-only and workflow-only changes still need validation evidence.
- Keep CI role separation intact: `pre-commit`, `repo-quality-static`, `manifest-static`, and `shell-static`.
- Do not add deployment, direct cluster mutation, or publishing commands to GitHub Actions.
- Do not modify GitHub branch protection/ruleset settings in this work item.
- Treat `.github/ABOUT.md` as a routing hub, not the branch policy source of truth.
- Keep branch policy SSoT in `docs/00.agent-governance/rules/git-workflow.md`; CI and PR template are required mirrors.
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
| T-008 | Reduce `.github/ABOUT.md` to policy routing and workflow roles | doc | n/a | PLN-008 | ABOUT links to branch policy, CI enforcement, PR template, and version inventory SSoTs | Platform | Done |
| T-009 | Clarify PR branch target and `infra` change type wording | doc | n/a | PLN-009 | PR template says branch exceptions require matching CI/governance update and `infra` is not a prefix | Platform | Done |
| T-010 | Remove unnecessary greeting workflow content permission | impl | n/a | PLN-010 | `greetings.yml` no longer grants `contents: read` | Platform | Done |
| T-011 | Add branch prefix parity checks from `git-workflow.md` | test | n/a | PLN-011 | quality gate compares CI regex/message and PR template prefixes to governance SSoT | Platform | Done |
| T-012 | Add `.github/ABOUT.md` drift guard | test | n/a | PLN-011 | quality gate fails if ABOUT mirrors the full branch policy instead of routing to SSoTs | Platform | Done |
| T-013 | Record follow-up evidence by local/CI-only/skipped lanes | doc | n/a | PLN-012 | verification summary separates local PASS from optional unavailable tools | Platform | Done |

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
- [x] T-008 Reduce ABOUT to a routing hub
- [x] T-009 Clarify PR template branch policy wording
- [x] T-010 Remove unnecessary greeting permission
- [x] T-011 Add branch prefix parity checks
- [x] T-012 Add ABOUT drift guard
- [x] T-013 Record evidence lanes

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
- **Logs / Evidence Location**: repo-discoverable summary in this section. Latest follow-up validation is split by evidence lane:
  - Local PASS: `bash scripts/validate-repo-quality-gates.sh .`
  - Local PASS: `git diff --check`
  - Local PASS: `bash infrastructure/tests/verify-contracts-static.sh`
  - Local PASS: `bash scripts/validate-gitops-structure.sh`
  - Local PASS with optional-tool skip: `bash scripts/validate-k8s-manifests.sh .` passes YAML syntax; `kube-linter` is skipped when unavailable on PATH.
  - Local PASS: `bash scripts/check-secret-handling.sh .`
  - Local PASS: `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +`
  - CI-only / optional local tools: full `pre-commit`, `actionlint`, `zizmor`, and `kube-linter` coverage is expected in CI or a fully provisioned local toolchain.
  - Skipped / unavailable locally: current local PATH does not provide `pre-commit`, `actionlint`, `zizmor`, or `kube-linter`; do not report those as locally passed unless rerun in a toolchain that has them.

## Related Documents

- **Plan**: [`../05.plans/2026-05-09-github-qa-ci-remediation.md`](../05.plans/2026-05-09-github-qa-ci-remediation.md)
- **GitHub Hub**: [`../../.github/ABOUT.md`](../../.github/ABOUT.md)
- **PR Template**: [`../../.github/PULL_REQUEST_TEMPLATE.md`](../../.github/PULL_REQUEST_TEMPLATE.md)
- **Git Workflow**: [`../00.agent-governance/rules/git-workflow.md`](../00.agent-governance/rules/git-workflow.md)
