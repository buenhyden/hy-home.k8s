# WSL k3d ArgoCD Bootstrap Guide

## Overview (KR)

이 문서는 WSL2 환경에서 k3d(k3s)와 ArgoCD GitOps 플랫폼을 초기 부트스트랩하는 방법을 설명한다.

## Guide Type

`how-to`

## Target Audience

- Platform Engineer
- DevOps Engineer

## Purpose

로컬 환경에서 표준 토폴로지와 GitOps 흐름을 재현해 개발/검증 기반을 일관되게 맞춘다.

## Prerequisites

- Windows 11 + WSL2 Ubuntu
- Docker Desktop (WSL backend)
- `kubectl`, `helm`, `k3d`, `argocd` CLI

## Step-by-step Instructions

1. WSL 리소스와 Docker backend 상태를 확인한다.
2. k3d 클러스터를 `1 server + 3 agents`로 생성한다.
3. ingress-nginx를 설치하고 `argocd.local` 도메인 접근을 설정한다.
4. ArgoCD를 Helm으로 설치하고 root app(App-of-Apps)을 적용한다.
5. ESO와 Vault Kubernetes Auth를 구성한다.
6. PostgreSQL/Valkey 외부 endpoint를 Service/EndpointSlice로 래핑한다.

## Common Pitfalls

- `172.30.0.0/24` 대역 중복으로 endpoint 연결 실패
- ArgoCD 프로젝트 권한 누락으로 sync 실패
- Vault role/path 매핑 불일치로 secret sync 실패

## Related Documents

- **Spec**: [`../04.specs/001-wsl-k3d-argocd-platform/spec.md`](../04.specs/001-wsl-k3d-argocd-platform/spec.md)
- **Operation**: [`../08.operations/0001-k8s-gitops-operations-policy.md`](../08.operations/0001-k8s-gitops-operations-policy.md)
- **Runbook**: [`../09.runbooks/0001-argocd-platform-bootstrap-runbook.md`](../09.runbooks/0001-argocd-platform-bootstrap-runbook.md)
