---
title: '.github QA and CI Remediation Implementation Plan'
type: plan
status: done
owner: 'platform'
updated: 2026-05-09
---

<!-- Target: docs/05.plans/YYYY-MM-DD-<feature>.md -->

# .github QA and CI Remediation Implementation Plan

> Use this template for `docs/05.plans/YYYY-MM-DD-<feature>.md`.
>
> Rules:
>
> - Every active plan must include explicit verification criteria.
> - Plan explains execution order, risk control, and rollout strategy.

---

# .github QA and CI Remediation Plan

## Overview (KR)

이 문서는 `.github/` 폴더의 QA, CI, 브랜치 정책, PR intake 계약을 현재 `hy-home.k8s` 워크스페이스에 맞게 보정하기 위한 실행 계획서다.
중복 제거보다 현재 CI 구조를 유지하면서 branch-policy 차단 게이트와 작은 운영 품질 보강을 추가하는 데 초점을 둔다.

## Context

현재 `.github/`의 repo-tracked 파일에는 중복 workflow 이름, 중복 step label, action version drift, 금지된 live mutation 명령이 발견되지 않았다.
CI는 `pre-commit`, `repo-quality-static`, `manifest-static`, `shell-static`으로 역할이 나뉘어 있고, `main` 대상 push/PR 중심 전략과 맞는다.

이번 보정은 새 배포/CD를 추가하지 않는다. GitHub Actions workflow는 `.github/workflows`에 두고, event/job/step 구조, explicit timeout, concurrency, `GITHUB_TOKEN` 권한을 repository QA 계약으로 관리한다.

## Goals & In-Scope

- **Goals**:
  - PR base와 source branch prefix를 CI에서 차단 가능한 정책으로 만든다.
  - CI를 수동으로 재실행할 수 있도록 `workflow_dispatch`를 추가한다.
  - CI 및 maintenance workflow job에 explicit timeout을 둔다.
  - overlapping 가능성이 있는 maintenance workflow에 concurrency를 둔다.
  - `.github` 문서, PR 템플릿, git workflow governance, repo quality gate를 새 CI 계약과 일치시킨다.
- **In Scope**:
  - `.github/workflows/*.yml` 보정
  - `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md` 보정
  - `docs/00.agent-governance/rules/git-workflow.md` branch prefix 목록 보정
  - `scripts/validate-repo-quality-gates.sh` 품질 게이트 확장
  - `docs/05.plans`, `docs/06.tasks` 보정 작업 추적 문서 추가
  - `docs/05.plans/README.md`, `docs/06.tasks/README.md` 인덱스 갱신

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - 새 CD/deploy workflow 추가
  - GitHub branch protection 또는 ruleset API 변경
  - GitHub-native instruction 계층 추가
  - `.github/gates/` 추적 파일 추가
  - Kubernetes manifest 변경
- **Out of Scope**:
  - `kubectl apply`, `kubectl patch`, `argocd app sync`, `vault kv`, `docker push`, `git push`를 workflow에 추가하는 변경
  - live cluster 검증 또는 직접 cluster mutation
  - 외부 GitHub repository setting 변경

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | `ci.yml`에 PR-only `branch-policy` job과 `workflow_dispatch` 추가 | `.github/workflows/ci.yml` | REQ-CI-001 | repo quality gate validates branch-policy and manual dispatch |
| PLN-002 | CI 및 maintenance workflow job timeout, maintenance concurrency 보강 | `.github/workflows/*.yml` | REQ-CI-002 | repo quality gate validates job timeouts and required concurrency |
| PLN-003 | `.github` 문서와 PR 템플릿을 새 branch/QA 계약과 정렬 | `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md` | REQ-DOC-001 | repo quality gate validates PR branch wording |
| PLN-004 | governance branch rules에 `ci/*`, `codex/*`, `dependabot/*` 추가 | `docs/00.agent-governance/rules/git-workflow.md` | REQ-GOV-001 | manual review plus repo quality gate |
| PLN-005 | repo quality gate가 새 CI 계약을 강제하도록 확장 | `scripts/validate-repo-quality-gates.sh` | REQ-VAL-001 | quality gate fails on missing branch-policy, summary linkage, timeout, or workflow_dispatch |
| PLN-006 | 보정 작업 plan/task 문서 추가 및 stage README 인덱스 갱신 | `docs/05.plans/`, `docs/06.tasks/` | REQ-DOC-002 | stage README indexes include new docs |
| PLN-007 | repo-backed validation bundle 실행 | `scripts/`, `infrastructure/tests/` | REQ-VAL-002 | validation commands PASS or limitation documented |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | repo governance and CI quality gate | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Static | whitespace and patch hygiene | `git diff --check` | no output |
| VAL-PLN-003 | Static | k3d/GitOps static contracts | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-004 | Static | GitOps structure | `bash scripts/validate-gitops-structure.sh` | PASS |
| VAL-PLN-005 | Static | YAML syntax and optional kube-linter | `bash scripts/validate-k8s-manifests.sh .` | PASS or tool limitation stated |
| VAL-PLN-006 | Security | plaintext secret scan | `bash scripts/check-secret-handling.sh .` | PASS |
| VAL-PLN-007 | Static | shell syntax | `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` | no syntax errors |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Branch policy becomes stricter than documented workflow | Medium | Align `ci.yml`, `.github/ABOUT.md`, PR template, and git workflow governance in one change set |
| Optional local tools are mistaken for required local dependencies | Low | Do not install `pre-commit`, `actionlint`, `zizmor`, or `kube-linter`; record local availability limits |
| Maintenance automations overlap and create noisy runs | Low | Add workflow-level concurrency to labeler, stale, and changelog workflows |
| CI summary misses a failed required gate | High | Add `branch-policy` to `ci-summary.needs` and validate summary linkage in repo quality gate |
| Workflow accidentally introduces deployment mutation | High | Preserve forbidden command scan for live mutation and publish commands |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: not applicable; no prompt/model behavior is changed.
- **Sandbox / Canary Rollout**: GitHub Actions changes are validated by static repo-backed checks before PR.
- **Human Approval Gate**: GitHub branch protection/ruleset changes, live cluster mutation, publishing, or deployment commands require separate human approval.
- **Rollback Trigger**: revert only this `.github`/docs/scripts change set if CI semantics fail or branch policy blocks intended repository flow.
- **Prompt / Model Promotion Criteria**: not applicable.

## Completion Criteria

- [x] Scoped workflow, docs, and governance changes completed
- [x] `branch-policy` is included in CI and `ci-summary`
- [x] CI manual dispatch, job timeouts, and maintenance concurrency are present
- [x] Repo quality gate enforces the new CI contract
- [x] Required docs updated
- [x] Verification passed or limitations documented

## Related Documents

- **Task**: [`../06.tasks/2026-05-09-github-qa-ci-remediation.md`](../06.tasks/2026-05-09-github-qa-ci-remediation.md)
- **Git Workflow**: [`../00.agent-governance/rules/git-workflow.md`](../00.agent-governance/rules/git-workflow.md)
- **GitHub Hub**: [`../../.github/ABOUT.md`](../../.github/ABOUT.md)
- **PR Template**: [`../../.github/PULL_REQUEST_TEMPLATE.md`](../../.github/PULL_REQUEST_TEMPLATE.md)
- **GitHub Workflow Syntax**: [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- **GitHub Concurrency**: [Control workflow concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency)
