# 02.ARD (Architecture Reference Document)

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
