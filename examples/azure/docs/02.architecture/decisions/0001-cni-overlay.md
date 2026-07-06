---
title: 'ADR-0001: Azure CNI Overlay for AKS Networking'
type: sdlc/adr
status: accepted
owner: platform
updated: 2026-07-06
---

# ADR-0001: Azure CNI Overlay for AKS Networking

## Overview

이 문서는 AKS 클러스터의 워크로드 네트워킹 플러그인으로 Azure CNI Overlay를 선택한 기록이다. 서비스 확장성과 IP 효율성을 극대화하기 위한 결정이다.

## Snapshot Boundary

This document is an example-local SDLC snapshot for cloud migration reference. It follows the repository's Cloud Example Snapshot boundary and is not live provider-latest guidance.

## Context

전통적인 Azure CNI는 모든 Pod에 VNet IP를 할당하므로 서브넷 IP가 빠르게 고갈되는 문제가 있다. 반면, Kubenet은 성능 저하가 있다. 2026년 대규모 워크로드 수용을 위해 IP 효율성과 고성능을 동시에 만족하는 대안이 필요하다.

## Decision

- **Azure CNI Overlay**를 네트워킹 플러그인으로 사용한다.
- Pod는 VNet과 별개의 오버레이 주소 공간(예: 192.168.0.0/16)에서 IP를 할당받는다.
- 노드 통신은 기본 VNet IP를 이용하며, Pod 간 통신은 캡슐화 없이 라우팅 테이블을 통해 직접 전달된다.

## Explicit Non-goals

- 온프레미스와의 직접적인 Pod-to-Pod IP 노출 (VNet 레벨 라우팅만 지원).
- 타사 CNI(Cilium, Calico 등)의 직접 설정을 통한 커스텀 구축.

## Consequences

- **Positive**:
  - VNet IP 고갈 문제 해결 (서브넷 크기에 구애받지 않고 만 단위 Pod 수용 가능).
  - 기존 Azure CNI와 유사한 전송 성능 유지.
  - Azure Network Policy와의 완벽한 통합.
- **Trade-offs**:
  - 클러스터 외부(온프레미스 등)에서 Pod IP로 직접 접근 불가 (Ingress 또는 LoadBalancer 필수).

## Alternatives

### Azure CNI (Node-assigned IP)

- Good: VNet 내부에서 Pod IP 직접 접근 가능.
- Bad: IP 주소 소모가 매우 심함 (Pod 수 + Node 수만큼 필요).

### Kubenet

- Good: IP 주소 절약 가능.
- Bad: 노드당 Pod 수 제한(110-250), 더 복잡한 라우팅 설정, 상대적으로 낮은 성능.

## Related Documents

- **AARD**: [../02.architecture/requirements/0001-azure-migration-architecture.md](../requirements/0001-azure-migration-architecture.md)
- **ADR**: [./0002-agc-gateway-api.md](0002-agc-gateway-api.md)
