# AWS Migration Technical Specifications (Spec)

> 시스템의 구현 세부 사항과 인터페이스 계약을 정의하는 보관소

## Overview

이 경로는 AWS 이식 작업 중 각 컴포넌트(네트워크, EKS, 데이터베이스 등)의 구체적인 기술 구성 방식과 상호 작용 명세를 관리한다.

## Audience

이 README의 주요 독자:

- Developers
- Infrastructure Engineers
- AI Agents

## Structure

```text
04.specs/
├── aws-migration/
│   ├── spec.md      # Migration Core Specification
│   └── api-spec.md  # (If applicable)
└── README.md        # This file
```

## Documentation Standards

- 모든 Spec은 `spec.template.md`를 기반으로 작성한다.
- 검증 기준(Verification)이 명시적으로 포함되어야 한다.

## Related References

- **PRD**: [../01.prd/README.md](../01.prd/README.md)
- **ARD**: [../02.ard/README.md](../02.ard/README.md)
- **Plan**: [../05.plans/README.md](../05.plans/README.md)
