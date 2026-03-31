# AWS Infrastructure Runbooks

> 장애 복구 및 정기 운영 작업의 실행 지침을 정의하는 보관소

## Overview

이 경로는 AWS 환경에서 발생할 수 있는 장애 상황에 대한 즉각적인 대응 절차와 반복적인 운영 작업(DB 복구, 클러스터 롤백 등)의 런북을 관리한다.

## Audience

이 README의 주요 독자:

- Operators
- Backend Developers
- AI Agents

## Structure

```text
09.runbooks/
├── aws-recovery.md  # Core Infrastructure Recovery
└── README.md        # This file
```

## Documentation Standards

- 모든 런북은 `runbook.template.md`를 기반으로 작성한다.
- 운영자가 고민 없이 즉시 따라 할 수 있는 단계별 절차(Procedure)가 필수적이다.

## Related References

- **ARD**: [../02.ard/README.md](../02.ard/README.md)
- **Operation**: [../08.operations/README.md](../08.operations/README.md)
- **Guide**: [../07.guides/README.md](../07.guides/README.md)
