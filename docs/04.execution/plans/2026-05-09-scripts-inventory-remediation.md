---
title: 'scripts Inventory Remediation Implementation Plan'
type: plan
status: done
owner: 'platform'
updated: 2026-05-21
---

# scripts Inventory Remediation Plan

## Overview (KR)

이 문서는 `scripts/` 폴더의 스크립트 사용 여부 조사 결과를 바탕으로, 불필요한 삭제 없이 현재 실행 계약을 명확히 하기 위한 실행 계획서다.
작업 분해, 검증, 위험 관리, 완료 기준을 정의한다.

## Context

2026-05-09 초기 조사 시점의 `scripts/`에는 `*.sh` 스크립트 4개와 `README.md`만 있었다.
`validate-repo-quality-gates.sh`, `validate-gitops-structure.sh`, `validate-k8s-manifests.sh`, `check-secret-handling.sh`는 CI, PR 템플릿, root README, `.claude/settings.json`, `scripts/README.md` 중 하나 이상에서 호출되거나 허용된다.

따라서 이번 보정의 핵심은 삭제가 아니라 `scripts/README.md`를 README 템플릿과 한국어 사용자 문서 규칙에 맞추고, 조사 결과를 plan/task 문서로 추적 가능하게 남기는 것이다.

2026-05-09 follow-up은 스크립트 존폐가 아니라 선택 인자 계약 보정이다.
`validate-k8s-manifests.sh`와 `check-secret-handling.sh`의 선택 인자는 임의 subpath가 아니라 repo root로 고정한다.
잘못된 root 또는 검사 대상 0건은 false-negative를 막기 위해 실패해야 한다.

## 2026-05-17 Evidence Refresh

2026-05-17 현재 인벤토리는 `scripts/README.md`가 소유하며, `scripts/`에는 `*.sh` 스크립트 5개가 있다.
2026-05-09 문맥의 "네 스크립트" 표현은 당시 snapshot을 뜻하며 현재 인벤토리 주장이 아니다.

현재 보존 기준은 Tier A/B/C로 분리한다.
Tier A는 CI job 또는 post-edit hook이 직접 실행하는 자동 실행 게이트이며 보존 근거다.
Tier B는 필수 품질 게이트가 간접 실행하고 generated artifact 또는 check contract를 소유하는 필수 간접 품질 게이트이며 보존 근거지만 indirect로 표시한다.
Tier C는 README, PR template, docs, allowlist, manual command reference 같은 문서·수동·허용 목록 표면이며 그 자체로는 보존 근거가 아니다.

`generate-llm-wiki-index.sh`는 `validate-repo-quality-gates.sh`가 `--check`로 간접 실행하고 `docs/90.references/llm-wiki/wiki-index.md`의 generated artifact contract를 소유하므로 Tier B indirect 품질 게이트 dependency다.
2026-05-17 기준 Tier C-only, unused, one-off 삭제 후보는 없다.

## Goals & In-Scope

- **Goals**:
  - `scripts/`의 현재 인벤토리와 유지 결정을 명확히 기록한다.
  - `scripts/README.md`를 `docs/99.templates/readme.template.md` 구조에 맞춘다.
  - CI, PR 템플릿, `.claude/settings.json`, root README와의 실행 계약을 문서화한다.
  - 이번 조사와 보정 작업을 plan/task 문서로 추적 가능하게 남긴다.
- **In Scope**:
  - `docs/04.execution/plans`, `docs/04.execution/tasks`에 보정 작업 추적 문서 추가
  - `docs/04.execution/plans/README.md`, `docs/04.execution/tasks/README.md` 인덱스 갱신
  - `scripts/README.md` 재작성
  - 필요 시 historical memory note 보강
  - `validate-k8s-manifests.sh`, `check-secret-handling.sh`의 repo-root 인자 계약 명확화

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - 스크립트 삭제, 통합, 리네임
  - 새 스크립트 또는 새 CLI 옵션 추가
  - 임의 subpath scan 모드 추가
  - 새 CI job 또는 pre-commit hook 추가
  - live cluster 확인 또는 직접 cluster mutation 수행
- **Out of Scope**:
  - Kubernetes manifest 변경
  - 외부 Vault, ArgoCD, k3d 런타임 변경
  - README 템플릿 자체 변경

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | scripts 조사 결과를 plan/task 문서로 기록 | `docs/04.execution/plans/`, `docs/04.execution/tasks/` | REQ-DOC-001 | stage README index updated |
| PLN-002 | `scripts/README.md`를 템플릿 구조와 한국어 사용자 문서 규칙에 맞게 재작성 | `scripts/README.md` | REQ-DOC-002 | README contains required template sections |
| PLN-003 | 2026-05-09 당시 네 스크립트의 `Keep` 결정을 명시하고, 2026-05-17 refresh에서 현재 5개 스크립트를 Tier A/B 기준으로 재분류 | `scripts/README.md` | REQ-SCRIPT-001 | all current scripts are listed with `Keep` status |
| PLN-004 | historical memory note의 과거 인벤토리 표현을 현재 README 기준으로 보강 | `docs/00.agent-governance/memory/progress.md` | REQ-GOV-001 | repo quality gate PASS |
| PLN-005 | repo-backed validation bundle 실행 | `scripts/`, `infrastructure/tests/` | REQ-VAL-001 | verification commands PASS or limitation documented |
| PLN-006 | manifest/secret 검증 스크립트의 선택 인자를 repo root로 명확화하고 잘못된 root를 실패 처리 | `scripts/validate-k8s-manifests.sh`, `scripts/check-secret-handling.sh`, `scripts/README.md` | REQ-SCRIPT-002 | subpath false-negative check fails clearly |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | repo governance quality gate | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Static | whitespace and patch hygiene | `git diff --check` | no output |
| VAL-PLN-003 | Static | shell syntax | `find infrastructure scripts docs/00.agent-governance/hooks -type f -name '*.sh' -exec bash -n {} +` | no syntax errors |
| VAL-PLN-004 | Static | k3d/GitOps static contracts | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-005 | Static | GitOps structure | `bash scripts/validate-gitops-structure.sh` | PASS |
| VAL-PLN-006 | Static | YAML syntax and optional kube-linter | `bash scripts/validate-k8s-manifests.sh .` | PASS or tool limitation stated |
| VAL-PLN-007 | Security | plaintext secret scan | `bash scripts/check-secret-handling.sh .` | PASS |
| VAL-PLN-008 | Negative | manifest validator rejects non-root subpath | `bash scripts/validate-k8s-manifests.sh gitops` | fails with repo-root error |
| VAL-PLN-009 | Negative | secret scanner rejects non-root subpath | `bash scripts/check-secret-handling.sh gitops` | fails with repo-root error |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Useful validation scripts are deleted as "unused" | High | Treat CI, PR template, README, and runtime permission references as usage evidence |
| `scripts/README.md` drifts from actual script inventory | Medium | List every current `*.sh` script, mark each as `Keep`, and separate Tier A/B retention evidence from Tier C command/documentation surfaces |
| Historical memory note is mistaken for current inventory | Low | Add a note that the current inventory source is `scripts/README.md` |
| Documentation-only change skips validation | Medium | Run the repo-backed validation bundle and record limitations |
| Subpath-like argument produces an empty successful scan | Medium | Treat the optional argument as repo root, validate required directories, and fail on zero matched YAML files |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: not applicable; no prompt/model behavior is changed.
- **Sandbox / Canary Rollout**: not applicable; no runtime rollout or manifest change is planned.
- **Human Approval Gate**: live cluster checks, direct mutation, and external runtime changes remain out of scope.
- **Rollback Trigger**: revert only this documentation/governance change set if validation fails.
- **Prompt / Model Promotion Criteria**: not applicable.

## Completion Criteria

- [x] Scoped work completed
- [x] Verification passed or limitations documented
- [x] Required docs updated
- [x] `scripts/README.md` states the current script inventory and `Keep` decisions
- [x] Manifest and secret scan scripts reject non-root subpath input clearly

## Related Documents

- **Task**: [`../tasks/2026-05-09-scripts-inventory-remediation.md`](../tasks/2026-05-09-scripts-inventory-remediation.md)
- **Scripts README**: [`../../../scripts/README.md`](../../../scripts/README.md)
- **Root README**: [`../../../README.md`](../../../README.md)
- **Agent Governance Memory**: [`../../00.agent-governance/memory/progress.md`](../../00.agent-governance/memory/progress.md)
