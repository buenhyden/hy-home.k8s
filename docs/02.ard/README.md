# 02.ARD (Architecture Reference Document)

## Overview

이 경로는 PRD 요구를 시스템 경계, 품질 속성, 참조 구조로 확장하는 ARD stage다.
여기서 정의한 아키텍처 관점은 ADR과 Spec의 상위 입력으로 사용된다.

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
02.ard/
├── 0001-wsl-k3d-argocd-platform.md
├── 0002-wsl2-k3d-argocd-ha-platform.md
├── 0003-platform-expansion-mesh-dashboard.md
└── README.md
```

## How to Work in This Area

1. 관련 `01.prd/` 문서를 먼저 읽어 요구사항 경계를 고정한다.
2. 새 ARD는 `../99.templates/ard.template.md`에서 시작한다.
3. 주요 설계 결정은 `03.adr/`에 별도 ADR로 연결한다.
4. 구현 가능한 계약은 `04.specs/`로 내려보내고 양방향 링크를 유지한다.

## Related References

- [Docs README](../README.md)
- [01.prd](../01.prd/README.md)
- [03.adr](../03.adr/README.md)
- [04.specs](../04.specs/README.md)

## 목적

이 폴더는 아키텍처 참조 문서(Architecture Reference Document, ARD)를 저장한다. ARD는 시스템 수준의 경계, 품질 속성, 참조 구조, 데이터 흐름, 보안·관측성·운영성 요구를 정의한다.

## 포함할 내용

- 시스템 경계와 책임
- 품질 속성(성능, 보안, 신뢰성, 확장성, 운영성)
- 참조 아키텍처
- 데이터 흐름
- 배포 및 인프라 관점
- 소유권과 근거 문서 링크

## 포함하지 말아야 할 내용

- 한 번의 구체 결정 자체
- 세부 구현 파일 설계
- 운영 명령 절차

## 연결 규칙

- PRD를 입력으로 받고, ADR·Spec의 상위 참조가 된다.
- Agent 시스템인 경우 모델/도구/메모리/컨텍스트/가드레일에 대한 아키텍처 수준 요구를 포함한다.

## Templates

- `../99.templates/ard.template.md`

## 문서 인덱스

| 문서                                                                                       | 설명                                                                                 | 상태  | 최종 수정  |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ----- | ---------- |
| [`0001-wsl-k3d-argocd-platform.md`](./0001-wsl-k3d-argocd-platform.md)                     | WSL2 k3d/k3s GitOps 플랫폼 참조 아키텍처                                             | Draft | 2026-03-27 |
| [`0002-wsl2-k3d-argocd-ha-platform.md`](./0002-wsl2-k3d-argocd-ha-platform.md)             | WSL2 멀티노드 HA + Traefik↔k3d TLS 경계 + CI 정적 게이트 계층을 포함한 참조 아키텍처 | Draft | 2026-05-09 |
| [`0003-platform-expansion-mesh-dashboard.md`](./0003-platform-expansion-mesh-dashboard.md) | 2026-03-29 cert-manager/Dashboard/Istio/Kiali 확장 ARD, 현재 실행계약은 Headlamp/172.18.x 기준 | Draft | 2026-05-09 |

## 관련 폴더

- `01.prd/`: ARD의 입력이 되는 요구사항
- `03.adr/`: ARD에서 파생되는 결정 기록
- `04.specs/`: ARD를 구현 계약으로 구체화하는 명세

## 예시

- WSL2/k3d 플랫폼의 경계와 품질 속성은 `0002-wsl2-k3d-argocd-ha-platform.md`에 기록한다.
