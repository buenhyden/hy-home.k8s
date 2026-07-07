---
title: 'Reference: Kubernetes Infrastructure Security Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-07
---

# Reference: Kubernetes Infrastructure Security Research

## Overview

이 문서는 쿠버네티스(Kubernetes) API 보안, 선언형 인프라 구조, GitOps 배포 아키텍처, 시크릿(Secrets)과 외부 Vault/ESO 연동 경계, 그리고 보안 정책 자동화(Policy-as-code) 체계를 2026-07-07 기준의 실제 리포지토리 구성 상태와 보안 가이드라인에 맞추어 정리한다.

최근 추가된 `network-reviewer` 에이전트가 Traefik Config, Ingress TLS, NetworkPolicy 포트 검증의 책임을 나누어가진 설계 구조를 본 분석에 통합하였다.

이 문서는 설명용 참고 문서로서, 실제 클러스터 매니페스트 배포, Vault 비밀정보 조작, 또는 ArgoCD의 실시간 동기화 상태를 직접 변경하지 않는다.

## Purpose

- 쿠버네티스 로컬 플랫폼의 desired state 선언 및 GitOps 운영 방식을 기술적으로 정의.
- secrets 유출 방지 및 외부 시크릿(ESO/Vault) 연동 규칙에 대한 lookup 제공.
- NetworkPolicy 및 인프라 정적 검증의 통제 범위를 명확히 규정하여 안전한 에이전트 인프라 구현 지원.

## Reference Type

- Type: durable-concept / external-standard-snapshot / dated-implementation-audit
- Source checked: 2026-07-07
- Refresh trigger: GitOps 매니페스트(Kustomize) 변경, NetworkPolicy 정의 변경, Vault auth/policy 구성 갱신.

## Authority Boundary

- **Authoritative for**:
  - 2026-07-07 기준 쿠버네티스, 인프라, GitOps, 시크릿 연동, 보안 경계에 대한 lookup 정리.
  - 리포지토리 내 실제 선언 파일 경로와 대응하는 보안 개념 간의 매핑.
- **Not authoritative for**:
  - 실 클러스터 리소스 직접 배포 및 Vault KV 쓰기 작업.
  - ArgoCD sync/rollback 수행 권한.

## Scope

- 쿠버네티스 Secret, NetworkPolicy, RBAC, Kustomize, ArgoCD App-of-Apps, Argo Rollouts, External Secrets Operator, HashiCorp Vault 연동, Conftest/Rego 정책 게이트, 정적/동적 테스트 검증 분리.
- 클라우드 provider 계정 변경 및 실 가상환경 테스팅 제외.

## Definitions / Facts

### 1. 쿠버네티스 제어 평면 및 API 보안 (Kubernetes API Security)
- **Kubernetes Secret**: base64 인코딩만으로 데이터를 보존하므로 탈취에 취약하다. 리포지토리 내 plaintext Secret 파일 커밋을 원천 차단하기 위해 `check-secret-handling.sh` 및 Conftest 정책을 local/CI 단계에 적용한다.
- **NetworkPolicy**: 워크로드 간 불필요한 트래픽 유입/유출을 통제하기 위해 `gitops/platform/network-policies/` 하위에 egress 제어 매니페스트를 선언한다.
- **AppProject allow-list & RBAC**: ArgoCD AppProject의 clusterResourceWhitelist를 공란으로 두어 일반 app이 클러스터 scoped 리소스를 조작하는 것을 방지하며, platform 프로젝트와 엄격하게 권한을 이원화한다.
- **Kustomize**: Kustomization 구조를 통해 공통 리소스 위에 패치와 overlay 설정을 덧씌우는 방식으로 선언적 desired state를 구성한다.

### 2. GitOps 및 ArgoCD 아키텍처 (GitOps & ArgoCD)
OpenGitOps의 4대 원칙(선언형, 버저닝 및 불변성, 자동 인출, 지속 조율)에 부합하도록, 로컬 k3d 환경의 모든 원하는 상태(Desired State)는 Git에 저장되며 ArgoCD가 이를 실시간으로 조율(Reconciliation)한다.
- **App-of-Apps**: `gitops/apps/root/`가 전체 platform과 workload ApplicationSet을 하위 선언 파일로 선언하는 최상위 마스터 역할을 수행한다.
- **Argo Rollouts**: progressive delivery를 지원하기 위해 Rollout 리소스와 AnalysisTemplate을 사용하여 트래픽 점진 이동 및 자동 분석 롤백 패턴을 제공한다.

### 3. 외부 시크릿 관리 (Secrets & ESO/Vault Boundaries)
- **External Secrets Operator (ESO)**: 실 Secrets의 값을 Git에 포함하지 않기 위해, 외부 Vault에서 데이터를 읽어와 쿠버네티스 Secrets 리소스를 동적으로 생성해주는 가교 역할을 한다.
- **Vault Provider**: ESO가 Vault Kubernetes auth mount를 통해 인증을 이행하며, `eso-read` Vault policy hcl 예제를 통해 ESO 토큰이 지정된 비밀 경로 외의 다른 Vault 데이터베이스 영역을 조회하지 못하도록 최소 권한을 부여한다.

### 4. 네트워크 보안 및 network-reviewer 적용
 Traefik 로컬 Ingress, TLS 인증서, Istio 서비스 메시, NetworkPolicy 설정이 복잡하게 얽혀 있는 플랫폼 구성을 보호하기 위해 전담 `network-reviewer` 에이전트가 도입되었다.
- `network-reviewer`는 Ingress 매니페스트의 host/path 포트 매핑, `verify-ingress-tls.sh` 스크립트 연결성, `apps-egress.yaml` 등의 egress NetworkPolicy CIDR/포트 유효성을 정적으로 감사하는 명시적 책임을 지닌다.

### 5. Policy-as-code 및 Conftest
정적 검증 단계에서 정책 위반을 사전에 거르는 자동화 메커니즘을 제공한다.
- `policy/conftest/kubernetes.rego` 정책 파일을 기반으로 plaintext Secret 선언 여부, 어플리케이션의 namespaces 임의 생성 여부, wildcard AppProject 권한 존재 여부, container `:latest` 이미지 태그 사용 여부를 Conftest(혹은 python fallback)로 검증한다.

## Sources

- Kubernetes API reference: Secrets, NetworkPolicies, RBAC (<https://kubernetes.io/>)
- ArgoCD Operator manual: Declarative Setup and Best Practices
- External Secrets Operator docs & HashiCorp Vault integration (<https://external-secrets.io/>)
- OPA Conftest Policy definition (<https://www.conftest.dev/>)
- [GitOps README](../../../../gitops/README.md)
- [Infrastructure README](../../../../infrastructure/README.md)
- [Vault eso-read policy sample](../../../../infrastructure/vault/policies/eso-read.hcl)
- [Observability and Network Review Agents Task Record](../../../04.execution/tasks/2026-07-06-observability-and-network-review-agents.md)

## Review and Freshness

- Review cadence: GitOps Kustomize 구조 개편 혹은 보안 정책/Vault auth 구성 변경 시
- Last reviewed: 2026-07-07
- Next review trigger: Conftest 정책 업데이트, ESO/Vault 인증 메커니즘 변경

## Related Documents

- **Parent research README**: [README.md](../README.md)
- **References README**: [../../README.md](../../README.md)
- **Workspace baseline**: [workspace-governance-baseline.md](workspace-governance-baseline.md)
- **Formatting reference**: [spec-sdlc-ci-qa-formatting.md](spec-sdlc-ci-qa-formatting.md)
- **GitOps README**: [../../../../gitops/README.md](../../../../gitops/README.md)
