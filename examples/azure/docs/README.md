# Azure Migration Documentation

> 이 경로는 로컬 k3s/k3d 환경을 2026년 3월 기준 Azure(AKS) 환경으로 이전하기 위한 전체 문서 체계를 관리한다.

## Overview

본 디렉토리는 `hy-home.k8s` 프로젝트의 Azure 클라우드 전환을 위한 전략, 설계, 구현 명세 및 운영 지침을 포함하는 9단계 문서 체계(9-Directory Structure)를 관리한다. 모든 문서는 프로젝트 거거넌스 표준에 따라 작성되었으며, 상호 참조(Traceability)를 통해 마이그레이션의 전 과정을 추적 가능하게 한다.

## Content Structure (9 Dirs)

| Directory | Type | Description |
| :--- | :--- | :--- |
| [01.prd](./01.prd) | PRD | 마이그레이션 요구사항 및 성공 지표 정의 |
| [02.ard](./02.ard) | ARD | 참조 아키텍처 모델 및 품질 속성 정의 |
| [03.adr](./03.adr) | ADR | 기술적 의사결정 기록 (CNI, ALB, Identity 등) |
| [04.specs](./04.specs) | SPEC | 상세 기술 명세 및 인터페이스 정의 |
| [05.plans](./05.plans) | PLAN | 단계별 이행 전략 및 릴리스 계획 |
| [06.tasks](./06.tasks) | TASK | 개별 작업 진행 상황 및 검증 증적 관리 |
| [07.guides](./07.guides) | GUIDE | 개발자 및 운영자 온보딩 가이드 |
| [08.operations](./08.operations) | OPER | 운영 정책, 거버넌스 및 통제 기준 |
| [09.runbooks](./09.runbooks) | RUN | 재해 복구 및 긴급 대응 절차서 |

## Global Rules & Standards

1. **Naming Convention**: 모든 문서는 템플릿(01~09)에 정의된 접두어(`YYYY-MM-DD-` 또는 `####-`)를 준수한다.
2. **KR Overview**: 모든 기본 문서의 상단에는 한국어 요약(Overview) 섹션을 포함한다.
3. **Traceability**: 모든 산출물은 상대 경로를 통한 유기적 링크 관계를 유지한다.

## AI Agent Guidance

- 모든 인프라 변경 및 운영 작업은 위 9개 가이드라인의 범위 내에서 수행되어야 함.
- 2026년 3월 기준 Azure 기술 표준(AKS v1.30+, AGC, Workload Identity)이 문서 전반에 적용되었음을 인지할 것.
