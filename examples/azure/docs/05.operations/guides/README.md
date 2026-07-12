# 05.operations/guides (User Guides & How-to)

> 이 경로는 Azure 마이그레이션 프로젝트의 사용자 가이드, 온보딩 절차 및 시스템 이해를 돕는 문서를 관리한다.

## Overview

본 디렉토리는 개발자와 운영자가 새롭게 구축된 Azure 인프라 환경에 적응하고, 필요한 작업을 스스로 수행할 수 있도록 돕는 "학습 및 참조 가이드"를 관리한다. 도구 설치, 클러스터 접속, 애플리케이션 배포 및 트러블슈팅 절차를 포함한다.

### Audience

이 README의 주요 독자:

- New Developers
- External Contributors
- Junior Operators
- AI Agents

### Scope

#### In Scope

- Azure 환경 온보딩 가이드 (Onboarding)
- 특정 작업 수행 방법 (How-to)
- 시스템 구조 및 개념 설명 (System Guide)
- 일반적인 장애 유형 해결 가이드 (Troubleshooting)

#### Out of Scope

- 운영 정책 및 거버넌스 (05.operations/policies 참조)
- 긴급 복구 및 실행 절차 (05.operations/runbooks 참조)
- 아키텍처 상세 설계 (02.architecture/requirements 참조)

## Snapshot Contract

이 인덱스는 2026-07-12에 저장소 정적 상태로 관찰한 Azure 마이그레이션 예시다. 기반 마이그레이션 기록은 2026-03-31 기준이고, 2026-05-09 지원 상태 언급은 해당 날짜의 주석으로만 유지하며, 이 경로는 active main-stage 소유권이나 provider-latest 가이드를 대체하지 않는다.

## Report Index

```text
05.operations/guides/
├── 0001-azure-onboarding-guide.md    # Azure AKS 온보딩 가이드
└── README.md                          # 본 문서
```

## Refresh and Succession

Spec 030이 `docs/90.references/cloud-examples/azure`로의 후속 통합을 소유한다. Azure 공식 서비스·API·지원 계약 또는 하위 인벤토리가 바뀔 때 이 예시를 다시 검토하며, 실행 자산은 계속 `examples/azure/`에 둔다.

1. [0001-azure-onboarding-guide.md](0001-azure-onboarding-guide.md)를 통해 기본 환경 설정을 완료한다.
2. 가이드 작성 시 [guide.template.md](../../../../../docs/99.templates/templates/sdlc/operations/guide.template.md) 템플릿을 준수한다.
3. 복잡한 명령어나 절차는 가독성을 위해 코드 블록을 적극 활용한다.

## Evidence Boundary

이 README는 저장소 정적 문서 증거만 제공한다. live Azure 구독, AKS, 자격 증명, 비용, 네트워크, secret 또는 provider-latest 준비 상태를 증명하지 않는다.

이 README의 링크 기준 위치는 `examples/azure/docs/05.operations/guides/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- **Spec**: [../03.specs/azure-migration/spec.md](../../03.specs/azure-migration/spec.md)
- **Runbook**: [../05.operations/runbooks/README.md](../runbooks/README.md)
- **Tasks**: [../04.execution/tasks/2026-03-31-migration-tasks.md](../../04.execution/tasks/2026-03-31-migration-tasks.md)

### AI Agent Guidance

1. 사용자 가이드는 친절하고 명확한 어조로 작성한다.
2. 실제 환경과 다른 정보가 발견되면 즉시 수정을 제안한다.
3. 가이드 내의 모든 명령어는 실제 실행 가능한 최신 버전 기준인지 확인한다.
