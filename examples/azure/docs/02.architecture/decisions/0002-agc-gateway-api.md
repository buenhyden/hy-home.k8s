# ADR-0002: Azure Application Gateway for Containers (AGC) with Gateway API

## Overview (KR)

이 문서는 AKS의 L7 부하 분산 및 Ingress 솔루션으로 Azure Application Gateway for Containers(AGC)와 Kubernetes Gateway API를 선택한 기록이다.

## Context

전통적인 Application Gateway Ingress Controller(AGIC)는 Azure Resource Manager(ARM) API를 통한 설정 업데이트 방식으로 인해 구성 변경 시 지연 시간이 발생한다. 2026년 기준, 보다 빠르고 선언적인 트래픽 관리가 필요하다.

## Decision

- **Azure Application Gateway for Containers (AGC)**를 주력 L7 부하 분산 장치로 사용한다.
- 구성을 위해 **Kubernetes Gateway API**를 표준으로 채택한다.
- ALB Controller를 AKS에 설치하여 AGC 리소스와 트래픽 정책을 관리한다.

## Explicit Non-goals

- 레거시 Ingress API를 통한 주된 설정 (Gateway API 우선).
- 클러스터 내부의 전용 Nginx/Traefik Ingress Controller 직접 운영 (관리형 서비스 사용).

## Consequences

- **Positive**:
  - near real-time의 설정 업데이트 (거의 즉각적인 트래픽 라우팅 변경 가능).
  - Gateway API의 강력한 표현력 (Traffic Splitting, Weighted Routing 등) 네이티브 지원.
  - 별도의 VM 스케일셋 없이 서비스 기반으로 작동하여 비용 효율성 개선.
- **Trade-offs**:
  - 기존 Ingress API와 비교하여 Gateway API에 대한 학습 곡선 필요.

## Alternatives

### Azure Application Gateway Ingress Controller (AGIC)

- Good: 기존 Ingress 리소스와 호환성 높음.
- Bad: ARM API 경유로 인한 지연 시간 발생, 현대적인 Gateway API 미지원.

### Nginx Ingress Controller (Self-managed)

- Good: 유연한 커스터마이징 가능.
- Bad: 운영 오버헤드 증가, Azure WAF 결합 시 추가 설정 필요.

## Related Documents

- **AARD**: [../02.architecture/requirements/0001-azure-migration-architecture.md](../requirements/0001-azure-migration-architecture.md)
- **ADR**: [./0001-cni-overlay.md](0001-cni-overlay.md)
- **Spec**: [../03.specs/azure-migration/spec.md](../../03.specs/azure-migration/spec.md)
