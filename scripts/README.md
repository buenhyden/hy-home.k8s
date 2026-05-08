# scripts

> 저장소 유지보수, 정적 검증, 자동화 보조 스크립트의 현재 실행 계약을 정리하는 진입 문서다.

## Overview

`scripts/`는 k3d/GitOps 저장소를 live cluster mutation 없이 검증하기 위한 repo-backed 유틸리티를 보관한다.
현재 스크립트는 모두 유지 대상이며, 삭제·통합·리네임 대상은 없다.

이 영역은 GitOps manifest 자체(`gitops/`)나 live runtime 점검(`infrastructure/tests/`)을 대체하지 않는다.
대신 CI, PR 템플릿, root README, `.claude/settings.json`에서 호출하거나 허용하는 반복 가능한 정적 검증 명령을 제공한다.

## Audience

이 README의 주요 독자:

- Platform maintainers
- Operators
- Documentation writers
- AI Agents

## Scope

### In Scope

- 저장소 문서, GitOps 구조, manifest syntax, secret handling을 검증하는 작은 스크립트
- CI와 로컬 수동 검증에서 반복 실행할 수 있는 deterministic check
- 선택 도구가 없을 때의 local fallback 안내
- 현재 스크립트 유지 여부와 사용 근거

### Out of Scope

- live cluster mutation을 수행하는 `kubectl apply`, `kubectl patch`, 배포 스크립트
- 외부 Vault, PostgreSQL, Valkey, Observability runtime을 직접 변경하는 스크립트
- GitOps manifest의 원천 파일
- `infrastructure/tests/`가 담당하는 runtime 또는 contract-level 검증 절차

## Structure

```text
scripts/
├── check-secret-handling.sh          # GitOps/infrastructure manifest plaintext secret pattern scan
├── validate-gitops-structure.sh      # ArgoCD root app and kustomization structure validation
├── validate-k8s-manifests.sh         # YAML syntax and optional kube-linter validation
├── validate-repo-quality-gates.sh    # Repository governance, workflow, docs, and inventory gates
└── README.md                         # This file
```

## How to Work in This Area

1. 새 스크립트를 만들기 전에 `.github/workflows/ci.yml`, `.pre-commit-config.yaml`, root `README.md`, `.claude/settings.json`의 기존 명령 계약을 확인한다.
2. 스크립트는 한 가지 검증 책임만 가져야 하며, 반복 실행해도 결과가 달라지지 않아야 한다.
3. secret, credential, live cluster mutation, publish/deploy 동작은 이 폴더의 기본 경로에 추가하지 않는다.
4. 스크립트를 추가·삭제·리네임하면 이 README, root `README.md`, PR 템플릿, CI path filter, `.claude/settings.json` 허용 목록을 함께 검토한다.
5. 변경 후 최소한 `bash scripts/validate-repo-quality-gates.sh .`와 `git diff --check`를 실행한다.

## Script Inventory

| Script | Status | Usage Evidence | Purpose |
| --- | --- | --- | --- |
| `validate-repo-quality-gates.sh` | Keep | root README, CI `repo-quality-static`, PR template, `.claude/settings.json` | Docs structure, README sections, template placement, workflow duplication, script references, obsolete files, version inventory drift, and agent mirror validation. |
| `validate-gitops-structure.sh` | Keep | root README, CI `manifest-static`, PR template, `.claude/settings.json` | ArgoCD root app, root app kind, and GitOps kustomization structure validation. |
| `validate-k8s-manifests.sh` | Keep | root README, CI `manifest-static`, PR template, `.claude/settings.json` | YAML syntax validation and optional `kube-linter` coverage for manifests. |
| `check-secret-handling.sh` | Keep | root README, CI `manifest-static`, PR template, `.claude/settings.json` | Plaintext secret pattern scan for GitOps and infrastructure manifests. |

## Local Tool Availability

필수 도구:

- `python3`
- Python `PyYAML`

선택 도구:

- `pre-commit`: 전체 hook matrix를 로컬에서 실행할 때 사용한다. 없으면 repo-backed 스크립트 묶음을 먼저 실행하고 CI 결과를 확인한다.
- `kube-linter`: `validate-k8s-manifests.sh`가 PATH에서 발견하면 실행한다. 없으면 해당 스크립트가 kube-linter 단계만 skip하고 YAML syntax는 계속 검증한다.
- `graphify`: 선택적 지식 그래프 갱신 도구다. 없으면 직접 source inspection 결과를 기록한다.

## Related References

- [Root README](../README.md)
- [GitHub CI Workflow](../.github/workflows/ci.yml)
- [Pull Request Template](../.github/PULL_REQUEST_TEMPLATE.md)
- [Pre-commit Config](../.pre-commit-config.yaml)
- [Claude Settings](../.claude/settings.json)
- [Infrastructure Tests](../infrastructure/tests/)
- [Agent Governance Bootstrap](../docs/00.agent-governance/rules/bootstrap.md)
- [scripts Inventory Remediation Plan](../docs/05.plans/2026-05-09-scripts-inventory-remediation.md)
