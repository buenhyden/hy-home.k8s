# infrastructure

> WSL2 + k3d + 외부 서비스 연동 기반 로컬 플랫폼 인프라 자산을 관리한다.

## Overview

이 디렉터리는 로컬 Kubernetes 플랫폼 부트스트랩에 필요한 인프라 설정을 담는다.
WSL2/Docker Desktop/k3d 클러스터, 외부 서비스 연동(외부 repo 관리), ArgoCD 설치 값 파일을 포함한다.

## Structure

```text
infrastructure/
├── k3d/                     # k3d 클러스터 설정
├── argocd/                  # ArgoCD Helm values
├── vault/                   # Vault 정책 샘플
└── README.md
```

## Related References

- [PRD](../docs/01.prd/2026-03-27-wsl-k3d-argocd-platform.md)
- [Spec](../docs/04.specs/001-wsl-k3d-argocd-platform/spec.md)
- [Runbook](../docs/09.runbooks/0001-argocd-platform-bootstrap-runbook.md)

## Bootstrap Note

- 실행 전 `VAULT_TOKEN`을 반드시 export 해야 한다.
- `./bootstrap-local.sh`는 Vault KV(`secret/platform/argocd`)의 `valkey_password`를 유일한 소스로 사용한다.
- 외부 서비스(Vault/PostgreSQL/Valkey)는 별도 워크스페이스(repo)에서 관리한다.
- `./bootstrap-local.sh`의 `kubectl apply`는 ArgoCD 소유권이 생기기 전 초기 namespace, secret, MetalLB, root GitOps application 생성을 위한 bootstrap-only 예외다. 정상 운영 변경은 GitOps PR과 ArgoCD reconciliation으로 처리한다.
