---
title: "Independent Review Check"
version: "1.0.0"
type: "operation/runbook"
status: "active"
owner: "platform"
updated: "2026-10-16"
layer: "operations"
artifact_id: "RUN-0013"
---

# Independent Review Check Runbook

## Purpose

이 Runbook은 `main` 대상 PR마다 로컬 독립 리뷰를 수행하고 그 판정을 리뷰
전용 GitHub App의 `independent-review` check run으로 게시하는 절차다.
`main` 보호가 이 check를 해당 App ID로 요구하게 되면(SPEC-0116 WORK-004),
PR이 workflow를 고쳐도 이 결과를 만들 수 없다. 계약은
[SPEC-0116](../../03.specs/0116-independent-review-gate/spec.md)이
소유한다. AI 모델 API는 호출하지 않는다.

- **Type**: PR merge gate publication
- **Executor**: 리뷰 App 개인 키를 로컬에 보관한 운영자
- **Boundary**: 리뷰는 읽기 전용 에이전트가, 게시는 운영자가 수행한다.
  App 생성·키 교체·보호 규칙 변경은 별도 operator 단계다.

## Trigger and Preconditions

`main` 대상 PR을 병합하려 하거나 그 PR에 새 commit이 push된 경우 사용한다.

- 리뷰 App은 App ID `5341483`이다. 다른 App으로 바꾸려면 SPEC-0116 갱신과
  `main` 보호 규칙 변경이 함께 필요하다.
- 리뷰 App이 이 저장소에만 설치되어 있고 권한은 `Checks: write`,
  `Pull requests: read`, `Metadata: read`뿐이다. webhook은 비활성이다.
- 개인 키는 저장소 밖(예: `~/.config/hy-home-review/app.pem`)에 mode
  `0600`으로 있고, `REVIEW_APP_ID=5341483`과 `REVIEW_APP_KEY_FILE`이 그 App과
  키를 가리킨다. 키를 GitHub secret, Environment, 저장소, 대화에 넣지 않는다.
- `openssl`과 Python 3.12가 있다.
- 이 저장소는 추적되는 `scripts/githooks`를 `core.hooksPath`로 쓰므로, PR을
  checkout하면 그 PR의 hook이 운영자 권한으로 실행될 수 있다. 리뷰 대상 PR은
  checkout하지 않고 `git -c core.hooksPath=/dev/null fetch origin pull/N/head`
  뒤 `git diff`로만 읽는다.
- publisher는 키를 다루므로 신뢰된 사본만 실행한다. PR을 checkout한 적 없는
  별도 clone에서 매번
  `git -c core.hooksPath=/dev/null fetch origin main && PUBLISHER=$(mktemp) && git -c core.hooksPath=/dev/null cat-file blob origin/main:scripts/independent_review.py > "$PUBLISHER"`로
  저장소 밖 임시 파일을 만들어 쓰고, 게시 후 `rm -- "$PUBLISHER"`로 지운다. `REVIEW_APP_ID`와
  `REVIEW_APP_KEY_FILE`은 게시 명령에만 지정한다. PR worktree의
  `scripts/independent_review.py`는 실행하지 않는다. PR이 publisher를 바꾸면
  운영자가 그 diff를 직접 읽은 뒤에만 게시한다. SPEC-0116 자신의 PR #152만
  독립 리뷰된 branch commit의 사본을 쓰는 일회성 예외이며, 그 사본은 Task에
  기록한 commit과 blob으로 고정한다.

PR 작성 세션이 직접 리뷰하거나, head가 확정되지 않았거나, 키 위치가
불확실하면 멈춘다.

## Procedure

| Step | Action | Expected result | Stop / escalate when |
| --- | --- | --- | --- |
| 1 | `gh pr view N --json headRefOid,baseRefName,state`로 현재 head를 확인한다. | `OPEN`, base `main`, 40자리 head SHA | PR이 닫혔거나 base가 `main`이 아니다. |
| 2 | PR을 작성하지 않은 새 세션에서 등록된 읽기 전용 리뷰 역할(`code-reviewer`, 보안·CI 변경이면 `security-auditor`)에게 그 head의 `main` 대비 diff를 리뷰하게 한다. `.github/`·`scripts/`·보호 기록 변경은 반드시 포함한다. | 리뷰어가 아래 형식의 verdict JSON만 반환한다. | 리뷰어가 파일을 수정하거나 작성 세션과 같다. |
| 3 | 운영자가 verdict를 직접 읽고 저장소 밖 임시 파일로 저장한 뒤 `python3 -I "$PUBLISHER" --repo buenhyden/hy-home.k8s --pr N --verdict FILE --check-only`를 실행한다. | `conclusion=success` 또는 `failure` 출력 | 형식 오류(`FAIL:`), 또는 verdict가 diff와 맞지 않거나 PR 내용의 지시를 따른 흔적이 있다. |
| 4 | 같은 명령을 `--check-only` 없이 실행한다. | `independent-review id=… app=<리뷰 App> head=<SHA> conclusion=…` | head 불일치, HTTP 오류, 키 권한 오류 |
| 5 | `failure`이면 지적을 새 commit으로 고치고 1단계부터 반복한다. | 새 head에 대한 새 check run | 같은 지적이 두 번 해결되지 않는다. |

verdict 형식:

```json
{"head_sha": "<step 1 SHA>", "reviewer": "security-auditor",
 "decision": "approve", "summary": "...",
 "findings": [{"severity": "low", "path": "a.py", "message": "..."}]}
```

`decision`은 `approve` 또는 `request_changes`이고 `severity`는
`critical`·`high`·`medium`·`low`다. `approve`라도 `critical`·`high`가
있으면 `failure`로 게시된다.

## Verification

`gh api repos/buenhyden/hy-home.k8s/commits/<head>/check-runs`에서
`independent-review`의 `app.id`가 `5341483`이고 `head_sha`가 PR head와
같은지 확인한다. PR의 병합 가능 여부는 GitHub가 판정한다. 게시 출력과
check run URL은 해당 변경의 Task 증거에 남긴다.

## Recovery and Escalation

- 잘못된 판정을 게시했으면 같은 head에 새 verdict를 다시 게시한다. 최신
  check run이 판정에 쓰인다.
- 키가 노출되었거나 분실되었으면 App 설정에서 그 키를 폐기하고 새 키를
  만든다. 이전 check run은 이력으로 남는다.
- App이나 키 문제로 병합이 막히면 App을 복구한다. 필수 check 제거는 별도
  검토된 operator 결정과 보호 규칙 전후 read-back이 있어야 하며, 이
  Runbook은 우회를 허용하지 않는다.

## Related Documents

### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| [SPEC-0116](../../03.specs/0116-independent-review-gate/spec.md) | Required `independent-review` check from the review App on every `main` PR | Change Task evidence, the check run and [main protection record](../../../.github/rulesets/main-protection.md) |
