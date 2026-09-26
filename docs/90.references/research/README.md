---
title: "90.references/research"
version: "0.1.1"
type: "common/readme-collection-index"
status: "active"
owner: "platform"
updated: "2026-09-26"
layer: "references"
---
# 90.references/research

> workspace harness research pack 참조, 출처 원장, 오래 유지할 연구 종합을 두는 곳이다.

> [!NOTE]
> 이 디렉터리에서 이루어지는 모든 AI 에이전트 작업은 [Agent Governance Hub](../../../.agents/README.md)를 따른다.

## Overview

`research/`는 workspace harness와 workspace engineering research pack의 오래
유지할 참조 자료를 둔다. 출처에 근거한 발견, 관찰 날짜가 붙은 출처 확인, 종합을
이후의 plan, spec, guide, task가 인용할 수 있는 안정적인 조회 영역이지만
이 폴더가 활성 정책의 소유자가 되지는 않는다.

이 폴더는 활성 거버넌스 정책, runtime 권한, 배포 절차, live cluster 준비 상태,
provider 계약을 정의하지 않는다. 이것들은 계속 `.agents/`,
`docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`,
`docs/05.operations/`의 정본 소유자가 맡는다.

### Collection Readers

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- workspace harness research pack 색인 자료
- 오래 유지할 출처 원장과 출처 우선순위 메모
- 공식 출처와 저장소 근거 증거 요약
- 분명히 표시한 경우의 비권위 market scan 요약
- `docs/99.templates/templates/references/research-pack.template.md`로 만든 pack README
- `docs/99.templates/templates/references/research.template.md`로 만든 보고서

### Out of Scope

- 활성 거버넌스 정책이나 provider 실행 규칙
- runtime roster 변경, hook 연결, 권한 변경
- live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, provider runtime, secret 검사
- 운영 runbook, release gate, 배포 승인, incident 대응
- 생성되었거나 병행 관리되는 `docs/superpowers/**` 내용

## Item Index

```text
research/
├── 0001-workspace-engineering/
├── 0002-archive-retention-and-provenance/
└── README.md
```

### Research Pack Index

| Pack | Role | Authority Boundary |
| --- | --- | --- |
| [0001-workspace-engineering/](./0001-workspace-engineering/) | 후속 workspace engineering research pack | 연구 routing과 관찰 날짜가 붙은 coverage만 담는다. 현재 권한은 정본 소유자에게 있다. |
| [0002-archive-retention-and-provenance/](./0002-archive-retention-and-provenance/) | archive 보존과 출처 research pack | 연구 routing과 관찰 날짜가 붙은 증거만 담는다. 현재 권한은 정본 소유자에게 있다. |

각 pack README는 보고서 lifecycle과 출처 coverage를 포함한 자신의
`## Report Index`를 소유한다. 이 collection은 pack만 나열하며 document-profile
registry에 Current pack을 선언하지 않는다.

현재 research pack은 `research/####-<slug>/`에만 있다. 네 자리 번호는 Research
안에서 유일하고 slug는 의미 있는 kebab-case이며 날짜가 아니다. pack 안의 보고서는
registry가 요구하는 `m####-` identity prefix 뒤에 의미 있는 주제 이름을 붙인다.
이 prefix는 identity이지 정렬 키가 아니다. 현재 보고서 파일 이름에 `part-*.md`,
날짜, 두 번째 정렬 prefix를 붙이지 않는다.

## Add and Find

1. research pack 자료를 추가하거나 바꾸기 전에 상위 spec, plan, task를 읽는다.
2. pack README는
   [research-pack.template.md](../../99.templates/templates/references/research-pack.template.md)로,
   작성하는 보고서는
   [research.template.md](../../99.templates/templates/references/research.template.md)로 만든다.
3. 출처 주장은 사실대로, 날짜와 함께 적고 `Source checked`, `Sources`, `Review and Freshness`로 범위를 명시한다.
4. market scan 자료보다 공식 문서와 저장소 근거 증거를 우선한다.
5. market 발견은 비권위 자료로 표시하고, 공식 출처나 저장소 근거를 뒤집는 데 쓰지 않는다.
6. 활성 정책, 구현 계약, runbook, task 증거는 여기서 다시 정의하지 말고 각 정본 소유자에게 돌려보낸다.
7. research pack 구조나 검증 증거가 바뀌면 이 README, 상위 [90.references README](../README.md), task 기록을 함께 갱신한다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/90.references/research/`다.

- 같은 폴더의 research 참조는 대상 파일이 생긴 뒤에만 `./`를 쓴다.
- 번호가 붙은 pack 참조는 대상 파일이 생긴 뒤 `./0001-workspace-engineering/<filename>.md`
  형식을 쓴다.
- 상위 reference로 가는 링크는 `../README.md`를 쓴다.
- 정본 소유 stage는 `../../../.agents/`, `../../01.requirements/`, `../../02.architecture/`, `../../03.specs/`, `../../05.operations/`를 쓴다.
- 작성된 research reference 파일에서 저장소 최상위 소스를 가리킬 때는 `../../../<path>`를 쓴다.
- 선택 사항이거나 계획 중인 대상 경로는 대상이 생길 때까지 code literal로 둔다.

### Source Priority

연구 출처끼리 어긋나면 다음 우선순위를 따른다.

1. 로컬 정책, 계약, task, 운영에 대해서는 저장소의 정본 소유자
2. 외부 사실에 대해서는 제품, provider, 표준, upstream 프로젝트의 공식 문서
3. 커밋된 manifest, 스크립트, 설정, template 같은 저장소 근거 증거
4. 현재 동작을 밝혀 줄 때의 공식 issue tracker, release note, 구현 저장소
5. market scan, vendor 마케팅, 블로그, 포럼, benchmark, 비교 자료

market scan 발견은 권위가 없다. 맥락, 지형, 용어를 파악하는 데 참고할 수는
있지만 market scan 자료라고 표시해야 하며 공식 문서, 저장소 근거 증거, 저장소의
정본 소유자를 뒤집을 수 없다.

## Related Documents

- [90.references README](../README.md)
- [Workspace Engineering Research Pack](./0001-workspace-engineering/README.md)
- [Archive Retention and Provenance Research Pack](./0002-archive-retention-and-provenance/README.md)
- [Archive index](../../98.archive/README.md)는 이 collection 이전에 있던 폐기된
  pack을 안내한다. 활성 문서는 그 본문에 직접 링크하지 않는다.
- [Research Reference Template](../../99.templates/templates/references/research.template.md)
- [Templates README](../../99.templates/README.md)
- [Agent Governance Hub](../../../.agents/README.md)
- [Reference Maintenance Runbook](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
