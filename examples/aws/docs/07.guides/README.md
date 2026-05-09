# 07.guides (Operational Guides)

> AWS EKS 및 관리형 서비스 설정 및 운영 지침

## Overview

이 디렉토리는 마이그레이션이 완료된 인프라 환경을 안전하고 효과적으로 사용하기 위한 실무 지침서를 보관합니다. EKS 인증 설정(aws-auth), ArgoCD 연동 가이드, 로컬 개발 환경 구성 가이드 등을 다룹니다.

## Audience

이 README의 주요 독자:

- Platform Engineers
- Operators
- AI Agents

## Scope

### In Scope

- AWS/EKS 운영 how-to 가이드
- 설정 절차, 선행 조건, 검증 방법
- Operations/Runbook으로 이어지는 링크

### Out of Scope

- 정책 통제 기준
- 장애 대응 절차
- 실행 작업 상태 추적

## Structure

```text
07.guides/
├── aws-setup-guide.md  # AWS/EKS 설정 가이드
└── README.md           # This file
```

## How to Work in This Area

1. [04.specs](../04.specs/README.md)의 기술 계약을 먼저 확인합니다.
2. 새 Guide는 `../../../../docs/99.templates/guide.template.md`를 기준으로 작성합니다.
3. 운영 정책과 복구 절차는 [08.operations](../08.operations/README.md), [09.runbooks](../09.runbooks/README.md)에 연결합니다.

## Related References

- [02.ard](../02.ard/README.md) - 아키텍처 참조 모델
- [06.tasks](../06.tasks/README.md) - 실행 작업 목록
- [08.operations](../08.operations/README.md) - 거버넌스 정책
