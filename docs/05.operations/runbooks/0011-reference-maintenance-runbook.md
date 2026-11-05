---
title: "Reference Maintenance Runbook"
version: "1.2.1"
type: "operation/runbook"
status: "active"
owner: "platform"
updated: "2026-11-05"
layer: "operations"
artifact_id: "RUN-0011"
---

# Reference Maintenance Runbook

## Purpose

이 Runbook은 `docs/90.references/`의 Audit, Research, Data 비권위
참고 자료를 추가·갱신·종료할 때 사용하는 실행 체크리스트다. Reference
내용의 사실과 출처는 각 문서가 소유하고, 이 Runbook은 절차만 소유한다.

- **Type**: Repository documentation maintenance
- **Execution boundary**: tracked repository files and local static validation
- **Approval boundary**: 외부 publish, provider action, live cluster mutation,
  credential use, destructive Git operation은 포함하지 않는다.

## Trigger and Preconditions

- 외부 조사 출처 또는 확인일을 갱신할 때
- 독립적인 Audit 또는 Data reference를 추가하거나 종료할 때
- Reference category, filename, router, consumer link를 바꿀 때
- 참고 자료가 현재 정책·요구·설계·절차를 중복하는지 재검토할 때

## Procedure

1. 자료의 semantic owner를 분류한다.
   - Agent governance는 공통 거버넌스(`.agents/`)에 둔다.
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
   pack은 router `####-<slug>/README.md`와 member `m####-<slug>.md`로 구성한다.
3. 현재 동작 또는 버전 사실은 매니페스트, 설정, workflow, lock, 코드와
   Stage 01/02 설명을 먼저 갱신한다. Reference를 실행 입력이나 mirror로
   만들지 않는다.
4. pack 내부의 새 authored report는 category와 일치하는
   [Audit Reference](../../99.templates/templates/references/audit.template.md),
   [Data Reference](../../99.templates/templates/references/data.template.md),
   [Research Reference](../../99.templates/templates/references/research.template.md)
   template을 사용하고 provenance, observation date, authority boundary,
   freshness trigger를 작성한다. 각 주장에 출처, 관찰일, 검증 상태를 남기고
   공식·1차 출처를 우선한다. 게시된 member는 이후 이름·형식 변경에 맞춰
   고치지 않고 새 member나 날짜가 있는 addendum으로 보완한다.
5. pack router가 member를 정확히 나열하게 하고, category router와
   `docs/90.references/README.md`를 같은 변경에서 갱신한다. pack README는 member
   변경과 함께 stage한다(registry 검사가 staged와 worktree의 pack 집합을 비교한다).
   Stage 90 주장을 요구·결정·정책으로 제시하지 않고, 채택하는 Stage 01/02/05
   owner를 링크한다. 빈 category나 redirect 문서는 만들지 않는다.
6. 종료 대상의 current consumer를 canonical owner 또는 직접 저장소 소스로
   전환한 뒤
   [Document Lifecycle Policy](../../../.agents/governance/document-lifecycle.md)에
   따라 문서를 `docs/98.archive/`의 처분 디렉터리로 옮기거나 삭제한다. archive는
   검증 대상이 아니며(ADR-0053), 현재 문서는 archive 파일이 아니라 현재 owner를
   링크한다. 원문은 Git history로 복구하며, 처분 승인은 owning Task에 기록한다.

## Verification

현재 QA 실행 registry가 변경 경로에 맞춰 gate를 선택한다. 작업 트리의
`quick`은 선택된 입력의 미리보기이며, commit 직전에는 최종 Git index를
대상으로 `staged`를 한 번 수행한다.
수동으로 모든 현행 문서의 strict 검사를 상시 반복하지 않는다.

```bash
python3 scripts/qa.py quick
python3 scripts/validate-document-contract-registry.py --root . --mode strict
git diff --check
```

최종 파일을 명시적으로 stage한 뒤 그 index에 대해 별도로 실행한다.

```bash
python3 scripts/qa.py staged
```

- [ ] Reference가 공통 거버넌스나 현재 Stage 01/02/03/05 owner를 대체하지 않는다.
- [ ] 모든 pack 경로가 category별 `####-<slug>/` 규칙과 일치하는 template을 사용한다.
- [ ] 종료 대상의 current consumer가 0이고 처분 승인이 기록되어 있다.
- [ ] 보존 자료의 출처·확인일·freshness trigger가 명시되어 있다.
- [ ] 현재 동작과 버전은 Stage 01/02 및 직접 구현 소스와 일치한다.

- changed-path 목록과 reviewed diff
- category 및 Stage router
- source metadata와 직접 저장소 소스
- 선택된 gate ID, 입력 snapshot, 도구·종료 코드와 요약
- 종료 전 consumer 검색 결과와 disposition 승인 기록

정적 PASS는 외부 출처의 현재성, hosted CI, provider runtime, live cluster
상태를 증명하지 않는다.

## Recovery and Escalation

- 잘못된 분류는 redirect를 만들지 않고, 동일 변경을 revert하거나 canonical
  owner에 새 수정으로 바로잡는다.
- 종료된 본문은 `git show <commit>:<path>`로 복구하며, 현재 Stage에 되살리기
  전 고유 목적과 consumer를 다시 검토한다.
- validator 실패 시 실패한 owner/router/link만 수정하고 무관한 문서를
  일괄 재생성하지 않는다.

## Related Documents

- Stage 90 agent instructions: `docs/90.references/AGENTS.md`
- Stage 90 router: `docs/90.references/README.md`
- Research collection: `docs/90.references/research/README.md`
- [Audit Pack Template](../../99.templates/templates/references/audit-pack.template.md)
- [Data Pack Template](../../99.templates/templates/references/data-pack.template.md)
- [Research Pack Template](../../99.templates/templates/references/research-pack.template.md)
- [Audit Reference Template](../../99.templates/templates/references/audit.template.md)
- [Data Reference Template](../../99.templates/templates/references/data.template.md)
- [Research Reference Template](../../99.templates/templates/references/research.template.md)
- Document authoring policy: `.agents/governance/document-authoring.md`

### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| N/A — SPEC-0054 (left the tree; Git history recovers it). It applied `.agents/governance/document-authoring.md` and selects a bounded Stage 90 reference or the canonical common-governance or Stage 01/02/03/05 owner. | A reference is added, refreshed, rerouted, or retired. | Reviewed diff and validator output; Git history recovers retired bodies. |
