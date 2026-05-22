# 90.references/versions

> repo-backed 버전 계약, 외부 공식 지원 범위 스냅샷, cloud example version 기준을 관리한다.

> [!NOTE]
> All AI agent interactions with this directory must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

`versions/`는 실행 절차가 아니라 버전 기준과 dated external snapshot을 보존하는 reference 영역이다. 실제 manifest/config/example code와 함께 유지되는 버전 값, cloud provider 공식 지원 범위, CI/pre-commit pin 기준처럼 여러 문서가 참조하는 기준값을 둔다.

버전 값은 실제 repo 파일과 함께 갱신될 때만 현재 계약으로 취급한다. live cluster upgrade, cloud account deployment, release approval은 이 폴더가 소유하지 않는다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- repo-backed k3s, Helm chart, GitHub Actions, pre-commit version contract
- AWS/Azure example target과 외부 공식 지원 범위 snapshot
- README/docs 설명과 정적 검증을 맞추기 위한 기준값
- `Source checked`, `Last reviewed`, refresh trigger가 있는 버전 reference

### Out of Scope

- live cluster upgrade 실행 절차
- cloud account deployment procedure
- 제품 요구사항, 아키텍처 결정, 실행 계획, 운영 런북
- 실제 repo 파일에 적용되지 않은 speculative dependency bump

## Structure

```text
versions/
├── tech-stack-version-inventory.md  # repo-backed 버전 기준과 cloud snapshot
└── README.md                        # This file
```

## How to Work in This Area

1. 버전 기준을 갱신할 때는 실제 manifest/config/example code와 해당 version reference를 같은 변경에서 맞춘다.
2. 외부 공식 기준은 확인일과 공식 링크를 남긴다.
3. 새 version reference는 [reference template](../../99.templates/reference.template.md)을 기반으로 작성한다.
4. live upgrade 순서나 장애 대응 절차가 필요하면 `docs/05.operations/runbooks/`로 라우팅한다.
5. 새 파일을 추가하거나 이동하면 이 README, 상위 [90.references README](../README.md), 관련 consumer README를 함께 갱신한다.
6. `/latest` 형식의 외부 URL은 frozen permalink가 아니라 source-checked URL로 해석한다. 고정 release URL이 있으면 `tech-stack-version-inventory.md`의 source나 note에 함께 남긴다.

## Link Basis

이 README의 링크 기준 위치는 `docs/90.references/versions/`다.

- 같은 폴더의 version reference 문서는 `./`로 시작한다.
- sibling reference folder는 `../agents/`, `../learning/`, `../llm-wiki/`로 연결한다.
- CI나 pre-commit config 같은 root-level source file은 version reference 문서 기준으로 `../../../<path>`를 사용한다.

## Related Documents

- [90.references README](../README.md)
- [Tech Stack Version Inventory](./tech-stack-version-inventory.md)
- [Docs README](../../README.md)
- [Templates README](../../99.templates/README.md)
- [Reference Maintenance Runbook](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
