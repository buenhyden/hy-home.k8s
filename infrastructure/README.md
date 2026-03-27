# infrastructure

> WSL2 + k3d + 외부 Docker 서비스 기반 로컬 플랫폼 인프라 자산을 관리한다.

## Overview

이 디렉터리는 로컬 Kubernetes 플랫폼 부트스트랩에 필요한 인프라 설정을 담는다.
WSL2/Docker Desktop/k3d 클러스터, 외부 서비스(Vault/PostgreSQL/Valkey), ArgoCD 설치 값 파일을 포함한다.

## Structure

```text
infrastructure/
├── k3d/                     # k3d 클러스터 설정
├── docker/                  # 외부 서비스 docker compose
├── argocd/                  # ArgoCD Helm values
├── vault/                   # Vault 정책 샘플
└── README.md
```

## Related References

- [PRD](../docs/01.prd/2026-03-27-wsl-k3d-argocd-platform.md)
- [Spec](../docs/04.specs/001-wsl-k3d-argocd-platform/spec.md)
- [Runbook](../docs/09.runbooks/0001-argocd-platform-bootstrap-runbook.md)

## Bootstrap Note

- 실행 전 `VALKEY_PASSWORD`를 반드시 export 해야 한다.
- `./bootstrap-local.sh`는 동일 비밀번호를
  - Docker Valkey 기동
  - `argocd-external-valkey` Kubernetes Secret 생성
  - Vault KV(`secret/platform/argocd`) 시드
  에 동시에 사용한다.
