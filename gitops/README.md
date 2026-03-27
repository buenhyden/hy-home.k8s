# gitops

> ArgoCD App-of-Apps 기반으로 로컬 클러스터 desired state를 선언형 관리한다.

## Overview

이 디렉터리는 ArgoCD가 동기화할 GitOps 리소스를 포함한다.
프로젝트 경계(AppProject), ApplicationSet, 루트 애플리케이션, 플랫폼 리소스를 분리해 관리한다.

## Structure

```text
gitops/
├── clusters/local/          # ArgoCD 부트스트랩 리소스
├── apps/root/               # App-of-Apps 루트 애플리케이션 하위 app 선언
├── platform/                # 플랫폼 공통 리소스
└── README.md
```

## Related References

- [ADR-0002](../docs/03.adr/0002-argocd-helm-and-gitops-model.md)
- [ADR-0004](../docs/03.adr/0004-external-services-endpoints-and-valkey-backend.md)
- [Spec](../docs/04.specs/001-wsl-k3d-argocd-platform/spec.md)
