# tests

> k3d/GitOps 저장소의 전역 검증 기준과 cross-repo evidence를 설명하는 진입 문서다.

## Overview

`tests/`는 애플리케이션 테스트 피라미드를 강제하는 폴더가 아니다. 이 저장소의 기본 검증 모델은 k3d GitOps 구성, Kubernetes manifest, secret handling, shell script, repository governance를 정적으로 확인하는 것이다.

실제 실행 가능한 검증 스크립트는 `scripts/`와 `infrastructure/tests/`에 둔다. 이 폴더는 여러 경로를 가로지르는 장기 테스트 산출물이나 evidence가 필요할 때만 확장한다.

## Audience

이 README의 주요 독자:

- Platform maintainers
- Operators
- Documentation writers
- AI agents

## Scope

### In Scope

- 저장소 전체 검증 모델 설명
- k3d/GitOps/static validation evidence의 해석 기준
- 향후 cross-repo integration 또는 e2e evidence를 둘 때의 기준

### Out of Scope

- 애플리케이션 단위 테스트 피라미드
- 소스 코드와 co-location되는 unit test 규칙
- live k3d bootstrap, ArgoCD sync, 외부 Vault 변경 같은 승인 필요 작업
- CI 원격 실행 결과를 로컬에서 통과한 것으로 간주하는 문서화

## Structure

```text
tests/
└── README.md    # This file
```

## How to Work in This Area

1. 기본 검증 기준은 [scripts/README.md](../scripts/README.md)와 [infrastructure/README.md](../infrastructure/README.md)를 먼저 확인한다.
2. manifest나 GitOps 구조를 바꾸면 `scripts/`와 `infrastructure/tests/`의 정적 검증을 함께 실행한다.
3. 이 폴더에는 여러 하위 시스템을 동시에 검증하는 산출물이 있을 때만 새 파일을 추가한다.
4. live cluster evidence는 사람 승인 bootstrap 또는 break-glass 절차로만 기록하며, 로컬 정적 검증과 분리해서 보고한다.

## Validation Model

| Area | Command |
| --- | --- |
| Repository quality gates | `bash scripts/validate-repo-quality-gates.sh .` |
| External service contracts | `bash infrastructure/tests/verify-contracts-static.sh` |
| GitOps structure | `bash scripts/validate-gitops-structure.sh` |
| Kubernetes manifests | `bash scripts/validate-k8s-manifests.sh .` |
| Secret handling | `bash scripts/check-secret-handling.sh .` |
| Shell syntax | `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` |

## Evidence Boundaries

- Repo/static 검증 통과는 live k3d 운영 검증 완료를 의미하지 않는다.
- `pre-commit`, `kube-linter`, `actionlint`, `zizmor`, `graphify`, `rtk` 같은 optional local tools가 없으면 통과로 간주하지 않고 제한사항으로 보고한다.
- 외부 Vault, 실제 Kubernetes API, ArgoCD reconciliation 상태는 승인된 live check가 없으면 검증 범위 밖이다.

## Related References

- [Repository README](../README.md)
- [scripts README](../scripts/README.md)
- [infrastructure README](../infrastructure/README.md)
- [Agentic execution rules](../docs/00.agent-governance/rules/agentic.md)
- [Local harness catalog](../docs/00.agent-governance/harness-catalog.md)
