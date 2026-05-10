# 02.architecture/decisions (Architecture Decision Records)

> 이 경로는 Azure 마이그레이션 프로젝트에서 발생한 기술적 의무 결정과 히스토리를 관리한다.

## Overview

본 디렉토리는 k3s 로컬 환경에서 Azure 클라우드로 이전하는 과정에서 직면한 기술적 선택 사항(Decision)과 그 배경(Context), 대안(Alternatives), 그리고 결과(Consequences)를 보존한다. 단순한 구현 상세보다는 아키텍처적으로 중요한 결정들을 기록하여 미래의 유지보수자와 Agent가 결정의 이유를 추적할 수 있도록 한다.

## Audience

이 README의 주요 독자:

- Cloud Architects
- Infrastructure Engineers
- AI Agents
- Future Maintainers

## Scope

### In Scope

- Azure 마이그레이션 핵심 기술 스택 선택 기록 (CNI, ALB, Identity 등)
- 결정 당시 고려된 대안(Alternatives) 분석
- 결정으로 인한 긍정적 영향과 트레이드오프(Consequences)
- 2026-05-09 공식 지원 스냅샷 기준 Azure 기술 표준 준수 여부 기록

### Out of Scope

- 세부 리소스 파라미터 및 Bicep 코드 (03.specs 참조)
- 개별 리소스의 리비전 관리 (Git History 참조)
- 제품 차원의 요구사항 (01.requirements 참조)

## Structure

```text
02.architecture/decisions/
├── 0001-cni-overlay.md           # Azure CNI Overlay 네트워킹 채택
├── 0002-agc-gateway-api.md       # AGC 및 Gateway API 주력 L7 부하분산 채택
├── 0003-workload-identity.md     # Passwordless Workload Identity 인증 채택
└── README.md                     # 본 문서
```

## How to Work in This Area

1. 기술적 대안 검토가 필요한 새로운 중대 결정이 발생하면 [adr.template.md](../../../../../docs/99.templates/adr.template.md) 템플릿을 사용하여 새 문서를 생성한다.
2. 각 문서 번호(####)는 프로젝트 전역에서 중복되지 않도록 순차적으로 부여한다.
3. 결정의 배경(Context) 섹션에는 분석 단계에서의 비교 지표를 포함한다.

## Related References

- **PARD**: [../01.requirements/2026-03-31-azure-migration.md](../../01.requirements/2026-03-31-azure-migration.md)
- **AARD**: [../02.architecture/requirements/0001-azure-migration-architecture.md](../requirements/0001-azure-migration-architecture.md)
- **Spec**: [../03.specs/azure-migration/spec.md](../../03.specs/azure-migration/spec.md)

## AI Agent Guidance

1. 새로운 인프라 도구 도입 시 반드시 ADR 작성을 제안하거나 기존 ADR과의 정합성을 체크한다.
2. 결과(Consequences) 섹션에 트레이드오프를 명확히 기술하여 에이전트가 예외 상황을 인지하도록 한다.
3. 중복된 ADR 생성을 피하고 기존 결정의 리비전이 필요한지 먼저 검토한다.
