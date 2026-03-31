# AWS Migration Architecture Decision Records (ADR)

> 기술적 의사결정의 배경, 대안, 결과를 추론 가능하게 기록하는 보관소

## Overview

이 경로는 AWS 이식 과정에서 발생한 핵심 기술 선택(예: Vault vs Secrets Manager)에 대한 결정 사항을 관리한다. 과거의 결정 맥락을 이해하는 데 필수적이다.

## Audience

이 README의 주요 독자:

- Architects
- Developers
- Documentation Writers
- AI Agents

## Structure

```text
03.adr/
├── 2026-03-31-replace-vault-with-secrets-manager.md  # ADR-001
└── README.md                                          # This file
```

## Documentation Standards

- 모든 ADR은 `adr.template.md`를 기반으로 작성한다.
- 하나의 ADR은 한 번의 독립적인 결정만을 다룬다.

## Related References

- **ARD**: [../02.ard/README.md](../02.ard/README.md)
- **Spec**: [../04.specs/README.md](../04.specs/README.md)
