# AWS Migration Documentation

> AWS 클라우드 네이티브 환경으로의 마이그레이션을 위한 공식 문서 체계

## Overview

이 경로는 hy-home.k8s 시스템의 AWS 이관을 위한 모든 설계, 계획, 작업, 운영 문서를 관리한다. 2026년 3월 기준의 최신 AWS 기술 스택(EKS, VPC Lattice, Karpenter 등)을 반영하며, 프로젝트의 표준 문서 거버넌스를 준수한다.

## Audience

이 README의 주요 독자:

- Platform Engineers (AWS 인프라 구축 및 관리)
- Developers (AWS 환경에서의 앱 배포 및 설정)
- AI Agents (자동화된 인프라 변경 및 문서 갱신)

## Scope

### In Scope

- AWS 마이그레이션 요구사항(PRD) 및 아키텍처(ARD)
- 기술적 결정 기록(ADR) 및 세부 명세(Spec)
- 실행 계획(Plan), 상세 태스크(Task) 및 운영 가이드(Guide/Runbook)

### Out of Scope

- 타 클라우드(Azure, GCP) 마이그레이션 문서 (해당 경로에서 별도 관리)
- 프로젝트 전체 공통 거버넌스 원본 (./docs/00.agent-governance 참조)

## Structure

```text
docs/
├── 01.prd/           # 제품 요구사항 정의서 (Vision, Success Criteria)
├── 02.ard/           # 아키텍처 참조 문서 (System Overview, Logic)
├── 03.adr/           # 아키텍처 결정 기록 (Decisions, Context)
├── 04.specs/         # 기술 명세서 (Network, Storage, IAM Spec)
├── 05.plans/         # 실행 로드맵 및 마일스톤
├── 06.tasks/         # 구현 및 검증 태스크 리스트
├── 07.guides/        # 설정 및 접속 가이드
├── 08.operations/    # 운영 및 비용 관리 정책
└── 09.runbooks/      # 장애 복구 런북
```

## Documentation Standards

이 영역의 문서는 다음 기준을 따라야 한다.

- `./docs/99.templates/`의 표준 템플릿을 엄격히 준수한다.
- 모든 문서는 상호 참조(Relative Links)를 포함하여 추적성을 유지해야 한다.
- **SSoS (Single Source of Truth)**: 인프라의 모든 사양은 04.specs를 기준으로 하며, 변경 시 관련 문서를 일괄 갱신한다.

## SSoT References

- [PRD (Requirements)](./01.prd/2026-03-31-aws-migration-prd.md)
- [ARD (Architecture)](./02.ard/0001-aws-cloud-native-architecture.md)
- [ADR (Decisions)](./03.adr/0001-aws-managed-services-selection.md)
- [Spec (Detailed Specs)](./04.specs/aws-migration/spec.md)
- [Plan (Roadmap)](./05.plans/2026-03-31-aws-migration-roadmap.md)
- [Task (Execution)](./06.tasks/2026-03-31-aws-migration-tasks.md)

## AI Agent Guidance

1. 새 문서를 작성하거나 기존 문서를 수정할 때 반드시 이 인덱스 페이지의 링크를 확인하라.
2. 템플릿 사용 시 자리표시자(Placeholder)를 완전히 제거하고 실제 내용으로 교체하라.
3. `/home/hy/project-infra/hy-home.k8s/AGENTS.md`의 거버넌스 규칙을 우선 적용하라.
