---
title: 'ADR-0001: Selection of Azure Application Gateway for Containers (AGC)'
type: sdlc/adr
status: accepted
owner: platform
updated: 2026-07-06
---

# ADR-0001: Selection of Azure Application Gateway for Containers (AGC)

## Overview

이 문서는 `hy-home.k8s` 인프라의 Azure 마이그레이션 시, L7 부하 분산 장치 및 인프라 게이트웨이로 Application Gateway for Containers (AGC)를 선택한 아키텍처 결정을 기록한다.

## Snapshot Boundary

This document is an example-local SDLC snapshot for cloud migration reference. It follows the repository's Cloud Example Snapshot boundary and is not live provider-latest guidance.

## Context

현재 로컬 환경에서는 Traefik 또는 Nginx Ingress Controller를 사용하고 있으나, Azure 환경으로 이전하면서 다음과 같은 요구사항이 발생했다:

- **Kubernetes Native Management**: 인프라 영역과 애플리케이션 영역의 관심사 분리(Gateway API).
- **Auto-scaling & Performance**: 트래픽 부하에 따른 즉각적인 프로비저닝 없이 자동 성능 확장 필요.
- **ALB Controller/Add-on**: 클러스터 외부의 관리형 서비스와 밀접하게 연동되는 공식 지원 솔루션 필요.

## Decision

- **Gateway API 채택**: 표준 Gateway API 형식을 사용하여 L7 라우팅 및 게이트웨이 리소스를 정의한다.
- **AGC 활용**: Azure의 차세대 L7 솔루션인 AGC를 통해 Ingress 로직을 클러스터 밖에서 처리한다.
- **ALB Controller 설치**: AKS 내부에 ALB Controller를 배포하여 Azure AGC 리소스를 쿠버네티스 객체와 동기화한다.

## Explicit Non-goals

- 기존 Application Gateway (v2)의 WAF 기능 상세 설정 (AGC 기능 내에서만 다룸).
- Multi-cluster 게이트웨이 통합 설정.

## Consequences

- **Positive**:
  - 인바운드 트래픽 처리 성능 극대화 (최대 30,000 requests/sec).
  - Gateway API를 통한 역할 기반(Role-based) 네트워크 관리 가능.
  - AKS 업그레이드나 노드 재시작에 관계없는 독립적인 엔드포인트 유지.
- **Trade-offs**:
  - 기존 Ingress 리소스 대비 Gateway API 학습 곡선 필요.
  - 리소스 사용에 따른 Azure 추가 비용 발생.

## Alternatives

### Standard Application Gateway (v2)

- Good: WAF 정책 통합이 수월하고 익숙한 모델.
- Bad: Pod IP 변경 시 업데이트 지연(Backend Pool 업데이트 방식)이 발생하며, IngressController의 성능 오버헤드 존재.

### Nginx Ingress Controller (In-cluster)

- Good: 기존 설정 유지 가능, 커스텀 유연성 높음.
- Bad: L4 LoadBalancer 비용 발생 + Nginx 파드 자원 소모 + 관리 포인트 증가.

## Related Documents

- **PARD**: [../01.requirements/2026-03-31-azure-migration-prd.md](../../01.requirements/2026-03-31-azure-migration-prd.md)
- **AARD**: [../02.architecture/requirements/2026-03-31-azure-migration-ard.md](../requirements/2026-03-31-azure-migration-ard.md)
- **Spec**: [../03.specs/2026-03-31-resource-specs.md](../../03.specs/2026-03-31-resource-specs.md)
