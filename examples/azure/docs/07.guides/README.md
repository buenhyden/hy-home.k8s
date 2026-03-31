# 07.guides (User Guides & How-to)

> 이 경로는 Azure 마이그레이션 프로젝트의 사용자 가이드, 온보딩 절차 및 시스템 이해를 돕는 문서를 관리한다.

## Overview

본 디렉토리는 개발자와 운영자가 새롭게 구축된 Azure 인프라 환경에 적응하고, 필요한 작업을 스스로 수행할 수 있도록 돕는 "학습 및 참조 가이드"를 관리한다. 도구 설치, 클러스터 접속, 애플리케이션 배포 및 트러블슈팅 절차를 포함한다.

## Audience

이 README의 주요 독자:

- New Developers
- External Contributors
- Junior Operators
- AI Agents

## Scope

### In Scope

- Azure 환경 온보딩 가이드 (Onboarding)
- 특정 작업 수행 방법 (How-to)
- 시스템 구조 및 개념 설명 (System Guide)
- 일반적인 장애 유형 해결 가이드 (Troubleshooting)

### Out of Scope

- 운영 정책 및 거버넌스 (08.operations 참조)
- 긴급 복구 및 실행 절차 (09.runbooks 참조)
- 아키텍처 상세 설계 (02.ard 참조)

## Structure

```text
07.guides/
├── 0001-azure-onboarding-guide.md    # Azure AKS 온보딩 가이드
└── README.md                          # 본 문서
```

## How to Work in This Area

1. [0001-azure-onboarding-guide.md](./0001-azure-onboarding-guide.md)를 통해 기본 환경 설정을 완료한다.
2. 가이드 작성 시 [guide.template.md](../../../docs/99.templates/guide.template.md) 템플릿을 준수한다.
3. 복잡한 명령어나 절차는 가독성을 위해 코드 블록을 적극 활용한다.

## Related References

- **Spec**: [../04.specs/azure-migration/spec.md](../04.specs/azure-migration/spec.md)
- **Runbook**: [../09.runbooks/README.md](../09.runbooks/README.md)
- **Tasks**: [../06.tasks/2026-03-31-migration-tasks.md](../06.tasks/2026-03-31-migration-tasks.md)

## AI Agent Guidance

1. 사용자 가이드는 친절하고 명확한 어조로 작성한다.
2. 실제 환경과 다른 정보가 발견되면 즉시 수정을 제안한다.
3. 가이드 내의 모든 명령어는 실제 실행 가능한 최신 버전 기준인지 확인한다.
