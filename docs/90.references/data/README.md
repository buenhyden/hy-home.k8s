---
title: "90.references/data"
version: "0.2.4"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-13"
---
# 90.references/data

## Stage Responsibility

### Purpose and Readers

> 오래 유지할 data pack, 그 dataset, dataset 출처를 두는 곳이다.

`data/`는 오래 유지할 dataset 자료를 둔다. 저장소가 의존하는 데이터의 형태와
출처, 각 스냅샷을 수집한 방법, 갱신·보존 경계가 여기에 해당한다. 이후의 plan,
spec, guide, task가 인용할 수 있는 안정적인 조회 영역이다. 그렇다고 이 폴더가
활성 정책의 소유자가 되지는 않는다.

이 폴더는 활성 거버넌스 정책, runtime 권한, 배포 절차, live cluster 준비 상태,
provider 계약을 정의하지 않는다. 이것들은 계속 `.agents/`,
`docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`,
`docs/05.operations/`의 정본 소유자가 맡는다.

#### Collection Readers

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers

### Inputs and Outputs

#### In Scope

- data pack 색인 자료
- dataset의 형태, 출처, 수집 방법 기록
- 갱신·보존 경계를 명시한, 관찰 날짜가 붙은 스냅샷
- `docs/99.templates/templates/references/data-pack.template.md`로 만든 pack README
- `docs/99.templates/templates/references/data.template.md`로 만든 dataset

#### Out of Scope

- 활성 거버넌스 정책이나 provider 실행 규칙
- runtime roster 변경, hook 연결, 권한 변경
- live k3d, ArgoCD, OpenBao, ESO, Kubernetes, cloud, provider runtime, secret 검사
- secret 값, credential, 가리지 않은 민감 기록
- 운영 runbook, release gate, 배포 승인, incident 대응

## Contents

### Current Items

```text
data/
└── README.md                          # This file
```

이 collection은 현재 data pack을 보유하지 않는다. 이는 현재 처분 결과일 뿐이며,
고유한 목적과 출처 경계를 갖춘 data pack의 추가를 금지하지 않는다.

### Classification

이 README는 분류 표를 따로 두지 않는다. 분류 표를 두게 되면 여기에 둔다.

## Workflow

### Create and Review

1. data pack 자료를 추가하거나 바꾸기 전에 해당 Spec 패키지(`docs/03.specs/`)가 있으면 그 Plan과 Task를 읽는다.
2. `data/####-<slug>/README.md`는
   [data-pack.template.md](../../99.templates/templates/references/data-pack.template.md)로 만들고,
   작성하는 dataset는 `data/####-<slug>/m####-<slug>.md` 경로에
   [data.template.md](../../99.templates/templates/references/data.template.md)로 만든다.
3. pack 멤버에는 pack 내부의 `m####` 번호를 매기고, 각 dataset에는 소속 pack의
   `DATA-####-m####` artifact identity를 붙인다.
4. 모든 스냅샷에 수집 날짜, 방법, 보존 경계를 기록하고 secret 값은 절대 저장하지 않는다.
5. 활성 정책, 구현 계약, runbook, task 증거는 여기서 다시 정의하지 말고 각 정본 소유자에게 돌려보낸다.
6. data pack 구조나 검증 증거가 바뀌면 이 README와 상위 [90.references README](../README.md)를 함께 갱신한다. 검증 증거는 활성 Task가 있으면 그 Task에 기록한다.

#### Relative Link Rules

이 README의 링크 기준 위치는 `docs/90.references/data/`다.

- 번호가 붙은 pack 참조는 대상 파일이 생긴 뒤 `./####-<slug>/<filename>.md` 형식을 쓴다.
- 상위 reference로 가는 링크는 `../README.md`를 쓴다.
- 정본 소유 stage는 `../../../.agents/`, `../../01.requirements/`, `../../02.architecture/`, `../../03.specs/`, `../../05.operations/`를 쓴다.
- 작성된 data reference 파일에서 저장소 최상위 소스를 가리킬 때는 `../../../<path>`를 쓴다.
- 선택 사항이거나 계획 중인 대상 경로는 대상이 생길 때까지 code literal로 둔다.

### Transition and Exit

이 README는 상태 전환·승격·종료 규칙을 따로 정하지 않는다.

## Related Documents

### Upstream and Downstream

- [90.references README](../README.md)
- [Agent Governance Hub](../../../.agents/README.md)
- [Reference Maintenance Runbook](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)

### Policy and Templates

- [Data Pack Template](../../99.templates/templates/references/data-pack.template.md)
- [Data Reference Template](../../99.templates/templates/references/data.template.md)
- [Templates README](../../99.templates/README.md)
