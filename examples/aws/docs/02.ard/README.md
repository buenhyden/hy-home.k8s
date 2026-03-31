# AWS Migration Architecture Reference Document (ARD)

> 시스템 전체의 참조 아키텍처와 품질 속성을 정의하는 보관소

## Overview

이 경로는 AWS 클라우드 환경으로의 이식을 위한 시스템 아키텍처 원칙, 경계, 레이어별 책임을 정의하는 ARD 문서들을 관리한다.

## Audience

이 README의 주요 독자:

- Architects
- Infrastructure Engineers
- AI Agents

## Structure

```text
02.ard/
├── 2026-03-31-aws-migration-ard.md  # AWS Migration Core ARD
└── README.md                        # This file
```

## Documentation Standards

- 모든 ARD는 `ard.template.md`를 기반으로 작성한다.
- 품질 속성(성능, 보안, 가용성 등)이 기술 명세의 기준이 되어야 한다.

## Related References

- **PRD**: [../01.prd/README.md](../01.prd/README.md)
- **ADR**: [../03.adr/README.md](../03.adr/README.md)
- **Spec**: [../04.specs/README.md](../04.specs/README.md)
