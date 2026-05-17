# 02.architecture/requirements (ARD)

## Overview

이 경로는 PRD 요구를 시스템 경계, 품질 속성, 데이터 흐름, 보안·관측성·운영성 요구로 확장하는 ARD(Architecture Reference Document) stage다.
여기서 정의한 아키텍처 관점은 ADR과 Spec의 상위 입력으로 사용된다.

ARD는 참조 아키텍처와 품질 속성을 설명한다. 단일 기술 선택 자체는 `../decisions/`의 ADR에 남기고,
파일 단위 구현 설계나 운영 명령 절차는 각각 `../../03.specs/`, `../../05.operations/`로 넘긴다.

## Audience

이 README의 주요 독자:

- Platform Architects
- Platform Engineers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 시스템 경계와 책임
- 품질 속성, 데이터 흐름, 보안/관측성/운영성 요구
- 참조 아키텍처와 하위 ADR/Spec 링크

### Out of Scope

- 단일 기술 결정 기록
- 세부 구현 파일 설계
- 운영 명령 절차

## Structure

```text
02.architecture/requirements/
├── 0001-wsl-k3d-argocd-platform.md
├── 0002-wsl2-k3d-argocd-ha-platform.md
├── 0003-platform-expansion-mesh-dashboard.md
└── README.md
```

## How to Work in This Area

1. 관련 `01.requirements/` 문서를 먼저 읽어 요구사항 경계를 고정한다.
2. 새 ARD는 `../../99.templates/ard.template.md`에서 시작한다.
3. 주요 설계 결정은 `02.architecture/decisions/`에 별도 ADR로 연결한다.
4. 기존 ARD의 역사적 값은 현재 실행계약으로 재작성하지 않고, 현재성은 이 README의 인덱스와 각 문서의 current-contract note로 표시한다.
5. 구현 가능한 계약은 `03.specs/`로 내려보내고 양방향 링크를 유지한다.

## Document Index

| 문서 | 역할 | 문서 상태 | 현재성 | 다음 단계 |
| --- | --- | --- | --- | --- |
| [`./0001-wsl-k3d-argocd-platform.md`](./0001-wsl-k3d-argocd-platform.md) | WSL2 k3d/k3s GitOps 플랫폼의 초기 참조 아키텍처 | Draft | Historical baseline. 현재 계약 확인은 Spec 001과 GitOps desired state를 함께 본다. | [`../../03.specs/001-wsl-k3d-argocd-platform/spec.md`](../../03.specs/001-wsl-k3d-argocd-platform/spec.md) |
| [`./0002-wsl2-k3d-argocd-ha-platform.md`](./0002-wsl2-k3d-argocd-ha-platform.md) | WSL2 멀티노드 HA, Traefik↔k3d TLS 경계, CI 정적 게이트 참조 아키텍처 | Draft | Historical ARD. 현재 외부 서비스 EndpointSlice/CIDR 계약은 `172.18.x` 기준의 GitOps manifest와 static contract test가 우선한다. | [`../decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](../decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md) |
| [`./0003-platform-expansion-mesh-dashboard.md`](./0003-platform-expansion-mesh-dashboard.md) | cert-manager, Dashboard, Istio, Kiali 확장 참조 아키텍처 | Draft | Historical expansion record. Kubernetes Dashboard는 Headlamp로 대체되었고 현재 계약은 ADR-0010과 `gitops/platform/headlamp/`가 우선한다. | [`../decisions/0010-headlamp-replaces-dashboard.md`](../decisions/0010-headlamp-replaces-dashboard.md) |

## Related Documents

- [Architecture README](../README.md)
- [01.requirements](../../01.requirements/README.md)
- [02.architecture/decisions](../decisions/README.md)
- [03.specs](../../03.specs/README.md)
- [99.templates ARD Template](../../99.templates/ard.template.md)
