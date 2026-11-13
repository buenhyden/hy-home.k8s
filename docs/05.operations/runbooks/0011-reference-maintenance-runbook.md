---
title: "Reference Maintenance Runbook"
version: "1.4.1"
type: "operation/runbook"
status: "active"
owner: "platform"
updated: "2026-11-13"
artifact_id: "RUN-0011"
---

# Reference Maintenance Runbook

## Purpose

### Trigger and Outcome

이 Runbook은 `docs/90.references/`의 Audit, Research, Data 비권위
참고 자료를 추가·갱신·종료할 때 사용하는 실행 체크리스트다.

- 외부 조사 출처 또는 확인일을 갱신할 때
- 독립적인 Audit 또는 Data reference를 추가하거나 종료할 때
- Reference category, filename, router, consumer link를 바꿀 때
- 참고 자료가 현재 정책·요구·설계·절차를 중복하는지 재검토할 때

### Scope

Reference
내용의 사실과 출처는 각 문서가 소유하고, 이 Runbook은 절차만 소유한다.

관련 문서: Stage 90 agent instructions: `docs/90.references/AGENTS.md`, Stage 90 router: `docs/90.references/README.md`, Research collection: `docs/90.references/research/README.md`

## Preconditions

### Authority and Access

- **Type**: Repository documentation maintenance
- **Execution boundary**: tracked repository files and local static validation
- **Approval boundary**: 외부 publish, provider action, live cluster mutation,
  credential use, destructive Git operation은 포함하지 않는다.

관련 문서: Document authoring policy: `.agents/governance/document-authoring.md`

### Safety Checks

안전 점검: 해당 없음 — 이 런북은 Preconditions에 백업·가용성·동시성·비밀 보호 항목을 따로 정하지 않는다.

## Steps

### Actions

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
   전환하고, 역사·감사·복구 소비자, 보존 가치, hold, 처분 권한을 확인한다.
   [Document Lifecycle Policy](../../../.agents/governance/document-lifecycle.md)에
   따라 판단과 승인 범위를 기존 Task에 기록한다. Git-history-only 방식을
   고르면 삭제·이동 전에 현재 처분할 원형과 일치하는 정확한 원문
   `commit:path`의 도달 가능성을 확인하고 임시 위치에 복구해 현재 원형의
   bytes와 비교한다. 미커밋 차이는 오래된 Git 객체로 보호되지 않는다. 해당 Task Evidence와
   Stage 01~03은 현재 owner의 기존 Archived Lineage에, 다른 유형은 기존
   관계·처분 기록에 복구 근거를 남긴 뒤 대상만 처분한다.
   완료된 Stage 03 package에 증거 소유 Task 자체가 포함되면, 그 Task에는
   package의 소비자·hold·권한·처분 방식 판단을 최종 원문 커밋 전에 확정한다.
   Spec·Plan·Task 자신의 최종 bytes 복구 결과를 그 안에 다시 쓰면 원문이
   달라지므로, 최종 커밋 후 어느 파일도 삭제하기 전에 종료할 세 파일 각각의
   실제 `commit:path`, 도달 가능한 ref, 임시 복구 bytes 비교 결과를 살아남는
   현재 owner의 기존 Archived Lineage에 기록하고 해당 Task 판단으로 연결한다.
   이는 완료된 package의 후속 증거 위치에만 적용하며 복구·권한 조건을
   생략하지 않는다.
   하나라도 미해결이면 그 처분만 보류하고 원형은 그대로 둔다. archive 본문은
   검증 대상이 아니며, 현재 문서는 archive 파일 대신 현재 owner를 링크한다.

   다음 조회 예시는 보존 대상으로 판정된 공개 저장소 문서에만 사용한다.
   `DISPOSITION_COMMIT`은 검토한 전체 커밋 ID, `DISPOSITION_PATH`는 현재
   원형의 저장소 상대 경로, `DISPOSITION_TARGET_REF`는 원문을 보존할
   대상 ref로 같은 셸에서 설정한다. 이 값과 처분 권한·hold를 먼저 검토한다.
   명령은 원형을 바꾸지 않고 임시 디렉터리에만 복구하며 본문을 출력하지 않는다.
   이 작업의 실제 처분이나 복구 실행을 뜻하지 않는다.

   ```bash
   (
     set -eu
     : "${DISPOSITION_COMMIT:?full reviewed commit required}"
     : "${DISPOSITION_PATH:?reviewed repository-relative path required}"
     : "${DISPOSITION_TARGET_REF:?retained target ref required}"
     test -f "$DISPOSITION_PATH"
     test ! -L "$DISPOSITION_PATH"
     git ls-files --error-unmatch -- "$DISPOSITION_PATH" >/dev/null
     git cat-file -e "${DISPOSITION_COMMIT}^{commit}"
     git merge-base --is-ancestor "$DISPOSITION_COMMIT" "$DISPOSITION_TARGET_REF"
     git cat-file -e "${DISPOSITION_COMMIT}:${DISPOSITION_PATH}"
     proof_dir=$(mktemp -d)
     trap 'rm -f -- "$proof_dir/restored"; rmdir -- "$proof_dir"' EXIT
     git cat-file blob "${DISPOSITION_COMMIT}:${DISPOSITION_PATH}" > "$proof_dir/restored"
     cmp -s -- "$DISPOSITION_PATH" "$proof_dir/restored"
   )
   ```

   모든 명령이 종료 코드 0이면 대상 ref에서 커밋과 원문 객체에 도달하고,
   임시 복구 bytes가 현재 원형과 같다. 객체·ref 부재, 접근 오류, 원형과
   복구본의 차이, 미확인 hold 또는 권한은 해당 처분 `DEFER`다. 여기서 확인한
   도달성은 입력한 로컬 ref에 한정되므로 원격 보존은 별도 관측 없이 주장하지
   않는다. Git 객체와 현재 원형의 해시, 검사 대상 ref, 명령 결과를 기존
   Task Evidence에 남기되, 종료 단위에 Task 자체가 포함된 경우 위의 살아남는
   Archived Lineage에 남긴다. 문서 본문은 로그에 복사하지 않는다.

### Stop Conditions

중단 조건: 해당 없음 — 이 런북은 별도의 중단 조건 절을 두지 않으며, 보류 조건은 Actions의 6단계에 있다.

## Validation

### Service Checks

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
- [ ] 종료 대상의 현재·역사·감사·복구 소비자, 보존 가치, hold와 처분 권한을 판정하고 현재 의미를 넘겼다.
- [ ] Git-history-only 처분이면 현재 원형과 일치하는 정확한 `commit:path`의 도달성과 임시 복구 bytes 일치를 기록했다. 미충족이면 처분을 보류했다.
- [ ] 보존 자료의 출처·확인일·freshness trigger가 명시되어 있다.
- [ ] 현재 동작과 버전은 Stage 01/02 및 직접 구현 소스와 일치한다.

### Evidence

- changed-path 목록과 reviewed diff
- category 및 Stage router
- source metadata와 직접 저장소 소스
- 선택된 gate ID, 입력 snapshot, 도구·종료 코드와 요약
- 종료 전 consumer·보존·hold 판정, disposition 승인 범위, 복구 근거 또는 보류 사유

정적 PASS는 외부 출처의 현재성, hosted CI, provider runtime, live cluster
상태를 증명하지 않는다.

### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| N/A — SPEC-0054 (left the tree; Git history recovers it). It applied `.agents/governance/document-authoring.md` and selects a bounded Stage 90 reference or the canonical common-governance or Stage 01/02/03/05 owner. | A reference is added, refreshed, rerouted, or retired. | Reviewed diff and validator output; Git history recovers retired bodies. |

## Recovery

### Recovery Procedures

- validator 실패 시 실패한 owner/router/link만 수정하고 무관한 문서를
  일괄 재생성하지 않는다.

### Rollback

- 잘못된 분류는 redirect를 만들지 않고, 동일 변경을 revert하거나 canonical
  owner에 새 수정으로 바로잡는다.
- 종료된 본문은 Task에 기록한 정확한 `git show <commit>:<path>`로 복구하며,
  현재 Stage에 되살리기 전 고유 목적과 consumer를 다시 검토한다.

### Escalation

- Git 원문
  도달성이나 bytes 일치가 확인되지 않으면 처분하지 않고 문서 소유자에게 넘긴다.
