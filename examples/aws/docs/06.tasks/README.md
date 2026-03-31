# AWS Migration Tasks

> 실제 구현 및 검증 작업 단위의 실행 내역을 기록하는 보관소

## Overview

이 경로는 ‘AWS 이식’이라는 대주제 아래에서 실행되는 모든 커밋 수준의 단위 작업들에 대한 추적 기록을 관리한다. 수행된 일, 수행한 사람, 수행 결과(증거)를 포함한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- AI Agents

## Structure

```text
06.tasks/
├── 2026-03-31-bootstrap-aws.md  # Core Cluster Setup Tasks
└── README.md                    # This file
```

## Documentation Standards

- 모든 작업 단위 기록은 `task.template.md`를 기반으로 작성한다.
- 추적 가능하며, 검증 결과(Evidence)를 반드시 포함한다.

## Related References

- **Plan**: [../05.plans/README.md](../05.plans/README.md)
- **Spec**: [../04.specs/README.md](../04.specs/README.md)
- **Walkthrough**: `walkthrough.md` (If applicable)
