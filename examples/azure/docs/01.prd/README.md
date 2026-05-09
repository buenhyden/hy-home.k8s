# 01.prd (Product Requirements Document)

> 이 경로는 Azure 마이그레이션 프로젝트의 비전과 요구사항을 정의하는 PRD 산출물을 관리한다.

## Overview

본 디렉토리는 로컬 k3s/k3d 인프라의 Azure 마이그레이션 프로젝트(hy-home.k8s)에서 비즈니스 목표와 제품 요구사항을 수립하고 문서화하는 공간이다. 시스템의 성공 지표, 워크로드 이전 범위, 2026-05-09 공식 지원 스냅샷 기준의 비기능적 품질 요구를 핵심 산출물로 관리한다.

## Audience

이 README의 주요 독자:

- Project Stakeholders
- Infrastructure Leads
- AI Agents

## Scope

### In Scope

- Azure 마이그레이션 제품 비전 및 비즈니스 가치 산출
- 기능적 요구사항(FR) 및 비기능적 요구사항(NFR)
- 서비스 성공 기준 및 2026년 기준 Azure SLA 정의

### Out of Scope

- 상세 기술 설계 및 데이터 모델링 (02.ard, 04.specs 참조)
- 개별 기술 의사결정의 아키텍처 배경 (03.adr 참조)

## Structure

```text
01.prd/
├── 2026-03-31-azure-migration-prd.md    # Azure 마이그레이션 핵심 PRD
└── README.md                            # 본 문서
```

## How to Work in This Area

1. 신규 요구사항 발생 시 [prd.template.md](../../../docs/99.templates/prd.template.md) 템플릿을 사용하여 새 문서를 생성한다.
2. 모든 요구사항은 고유 아이디(REQ-PRD-*)를 부여하며 상호 추적성을 보장한다.

## Related References

- **ARD**: [../02.ard/2026-03-31-azure-migration-ard.md](../02.ard/2026-03-31-azure-migration-ard.md)
- **Spec**: [../04.specs/2026-03-31-resource-specs.md](../04.specs/2026-03-31-resource-specs.md)
- **Plan**: [../05.plans/2026-03-31-migration-strategy.md](../05.plans/2026-03-31-migration-strategy.md)
