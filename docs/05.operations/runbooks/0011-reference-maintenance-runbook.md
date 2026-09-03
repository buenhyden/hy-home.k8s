---
title: 'Reference Maintenance Runbook'
version: "1.0.0"
type: operation/runbook
layer: "operations"
status: active
owner: platform
updated: 2026-09-01
artifact_id: "RUN-0011"
---

# Reference Maintenance Runbook

## Overview

이 Runbook은 `docs/90.references/`의 Audit, Research, Data 비권위
참고 자료를 추가·갱신·종료할 때 사용하는 실행 체크리스트다. Reference
내용의 사실과 출처는 각 문서가 소유하고, 이 Runbook은 절차만 소유한다.

## Runbook Type

- **Type**: Repository documentation maintenance
- **Execution boundary**: tracked repository files and local static validation
- **Approval boundary**: 외부 publish, provider action, live cluster mutation,
  credential use, destructive Git operation은 포함하지 않는다.

## When to Use

- 외부 조사 출처 또는 확인일을 갱신할 때
- 독립적인 Audit 또는 Data reference를 추가하거나 종료할 때
- Reference category, filename, router, consumer link를 바꿀 때
- 참고 자료가 현재 정책·요구·설계·절차를 중복하는지 재검토할 때

## Procedure or Checklist

1. 자료의 semantic owner를 분류한다.
   - Agent governance는 Stage 00에 둔다.
   - 현재 요구와 아키텍처는 Stage 01/02에 둔다.
   - 구현 Spec/Plan/Task는 Stage 03에 둔다.
   - 운영 Guide/Policy/Runbook/Incident/Postmortem은 Stage 05에 둔다.
   - 출처 기반 비권위 Audit/Research/Data만 Stage 90에 둔다.
2. pack 경로와 template을 함께 선택한다.
   - Audit은 `audits/####-<slug>/`와
     [Audit Pack Template](../../99.templates/templates/references/audit-pack.template.md)을 사용한다.
   - Data는 `data/####-<slug>/`와
     [Data Pack Template](../../99.templates/templates/references/data-pack.template.md)을 사용한다.
   - Research는 `research/####-<slug>/`와
     [Research Pack Template](../../99.templates/templates/references/research-pack.template.md)을 사용한다.
   - 네 자리 번호는 category 안에서 고유해야 하고 slug는 날짜가 아닌 의미
     기반 kebab-case여야 한다. 관찰일은 본문 metadata에 둔다.
3. 현재 동작 또는 버전 사실은 매니페스트, 설정, workflow, lock, 코드와
   Stage 01/02 설명을 먼저 갱신한다. Reference를 실행 입력이나 mirror로
   만들지 않는다.
4. pack 내부의 새 authored report는 category와 일치하는
   [Audit Reference](../../99.templates/templates/references/audit.template.md),
   [Data Reference](../../99.templates/templates/references/data.template.md),
   [Research Reference](../../99.templates/templates/references/research.template.md)
   template을 사용하고 provenance, observation date, authority boundary,
   freshness trigger를 작성한다.
5. category router와 `docs/90.references/README.md`를 같은 변경에서
   갱신한다. 빈 category나 redirect 문서는 만들지 않는다.
6. 종료 대상의 current consumer를 canonical owner 또는 직접 저장소 소스로
   전환한다. consumer가 0이 된 뒤 파일을 제거하며, 전체 본문 복구는 Git
   history를 사용한다.
7. Stage 00/01/02/03/05/90 문서에 Stage 98 인용 또는 cross-link가 생기지
   않았는지 확인한다.

## Verification Steps

```bash
rtk python3 scripts/validate-document-contract-registry.py --root . --mode strict
rtk python3 scripts/validate-markdown-profiles.py --root . --mode strict
rtk python3 scripts/validate-links-and-owners.py --root . --mode strict
rtk bash scripts/validate-repo-quality-gates.sh .
rtk git diff --check
```

- [ ] Reference가 현재 Stage 00/01/02/03/05 owner를 대체하지 않는다.
- [ ] 모든 pack 경로가 category별 `####-<slug>/` 규칙과 일치하는 template을 사용한다.
- [ ] 삭제 대상의 current consumer가 0이다.
- [ ] 보존 자료의 출처·확인일·freshness trigger가 명시되어 있다.
- [ ] 현재 동작과 버전은 Stage 01/02 및 직접 구현 소스와 일치한다.
- [ ] 현재 Stage 문서에 Stage 98 인용 또는 cross-link가 없다.

## Observability and Evidence Sources

- changed-path 목록과 reviewed diff
- category 및 Stage router
- source metadata와 직접 저장소 소스
- 위 validator의 종료 코드와 요약
- 삭제 전 consumer 검색 결과와 Git commit ID

정적 PASS는 외부 출처의 현재성, hosted CI, provider runtime, live cluster
상태를 증명하지 않는다.

## Safe Rollback or Recovery Procedure

- 잘못된 분류는 파일을 되살리는 redirect나 Archive 복제본 대신, 동일 변경을
  revert하거나 canonical owner에 새 수정으로 바로잡는다.
- 삭제된 본문이 필요하면 해당 경로의 Git history에서 읽고, 현재 Stage에
  복원하기 전 고유 목적과 consumer를 다시 검토한다.
- validator 실패 시 실패한 owner/router/link만 수정하고 무관한 문서를
  일괄 재생성하지 않는다.

## Traceability

- Stage 90 router: `docs/90.references/README.md`
- Research collection: `docs/90.references/research/README.md`
- [Audit Pack Template](../../99.templates/templates/references/audit-pack.template.md)
- [Data Pack Template](../../99.templates/templates/references/data-pack.template.md)
- [Research Pack Template](../../99.templates/templates/references/research-pack.template.md)
- [Audit Reference Template](../../99.templates/templates/references/audit.template.md)
- [Data Reference Template](../../99.templates/templates/references/data.template.md)
- [Research Reference Template](../../99.templates/templates/references/research.template.md)
- Document authoring policy: `docs/00.agent-governance/policies/document-authoring.md`

### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) applies `docs/00.agent-governance/policies/document-authoring.md` and selects a bounded Stage 90 reference or the canonical Stage 00/01/02/03/05 owner. | A reference is added, refreshed, rerouted, or retired. | Reviewed diff and validator output; Git history owns removed full bodies. |
