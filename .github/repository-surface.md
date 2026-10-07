---
title: "GitHub Configuration Hub"
version: "0.4.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-07"
---
# GitHub Configuration Hub

## Overview

이 문서는 `hy-home.k8s`의 GitHub 자동화 surface를 안내하는 routing 문서다.
정책의 정본은 아니다. `.github/README.md`는 GitHub가 저장소 프로필 페이지로
해석하므로 이 이름을 사용한다.

## Scope

이 디렉터리는 PR branch metadata와 저장소 유지보수 자동화를 제공한다.
로컬 QA와 release 준비는 별도의 현재 소유자가 수행한다. GitHub Actions는
QA gate, 배포 CD, live 클러스터·외부 Vault 변경 또는 release 게시자가 아니다.

## Structure

- `workflows/` - branch metadata와 유지보수 자동화
- `ISSUE_TEMPLATE/` - 버그·기능 요청 접수 양식
- `PULL_REQUEST_TEMPLATE.md` - PR 검토와 로컬 증거 연결 안내
- `CODEOWNERS` - 경로별 리뷰 소유권
- `dependabot.yml`과 `labeler.yml` - 의존성·경로 label 설정
- `SECURITY.md` - 취약점 신고 안내

## Usage

### Policy Routing

- branch 전략은 `.agents/governance/git.md`가 소유한다.
  `workflows/ci.yml`의 유일한 `ci-summary` job은 PR의 base와 source prefix를
  검사한다. main push와 manual dispatch에는 branch 검사를
  `NOT_APPLICABLE`로 보고한다. 모든 이벤트에서 full QA는 `NOT_RUN`이다.
  job의 성공은 로컬 QA 통과를 뜻하지 않는다.
- 로컬 QA 명령과 gate 구성은 `scripts/qa.py`와 validation registry가
  소유한다. 로컬 커밋, PR, main 통합과 인계의 증거 순서는
  [Quality policy](../.agents/governance/quality.md#delivery-ownership)가
  소유한다. hosted `ci-summary` 결과는 별도의 SHA·run identity를 가진다.
- `.github/requirements/ci-validation.txt`와
  `.pre-commit-config.yaml`은 로컬 Python 의존성·hook revision 계약을
  보존한다. 현재 CI는 lock이나 Python 도구를 설치하지 않는다.
  `scripts/validate-ci-python-contract.py`가 고정 pin과 workflow 경계를
  검사하므로 lock과 소비자 단언은 함께 리뷰한다.
- Issue는 요청과 triage priority를 소유한다. 승인된 수용 계약은 Spec,
  실행 결과는 Task에 기록하고 Project는 상태를 표시한다. Issue form은
  접수 단계에 Spec이나 Requirement 링크를 요구하지 않는다.
- 현재 검증 명령과 fixture는 [`scripts/README.md`](../scripts/README.md)와
  [`tests/README.md`](../tests/README.md)를 따른다. 이 hub는 그 개수를
  복사하지 않는다.
- ARWB-003의 전체 cutover는 과거 로컬·수동 증거다. 지속적인 Archive
  무결성 검사는 현재 validation owner에서 수행한다.
- `ci.yml`은 pull request의 형태를 검증한다. 직접 push 제한은 저장소 로컬 파일 밖에서 GitHub branch protection과 ruleset이 강제한다.
- PR 작성자와 리뷰어 안내는 `PULL_REQUEST_TEMPLATE.md`에 있다.
- 전체 SHA로 Action을 고정하는 규칙은 저장소 품질 gate가 강제한다.

### Workflow Roles

- `ci.yml`은 main 대상 push·pull request·`workflow_dispatch`에서
  branch metadata만 검사하고 full QA `NOT_RUN`을 출력한다.
- `labeler.yml`과 `greetings.yml`은 저장소 유지보수 자동화다.
  QA 통과나 사람의 리뷰 승인을 대체하지 않는다.
- 과거 hosted verifier, SHA main tag publisher, 임시 changelog artifact와
  stale 자동 종료는 현재 workflow에서 은퇴했다. 당시 인증된 활성화·태그
  기록은 [Archive 탐색](../docs/98.archive/README.md)에 남아 있다.
  현재 원격 App, 환경, ruleset, 보호 설정은 여기서 재조회하지 않았다.
- release 준비 PR은 main의 `CHANGELOG.md`를 갱신하고, SemVer tag와
  GitHub Release는 승인된 정확한 main commit의 단일 producer가 맡는다.
  저장소 파일만으로 실제 게시나 원격 설정을 인증하지 않는다.

### Workflow Responsibility Matrix

| Workflow | Role | Trigger / scope | Required evidence | Boundary |
| --- | --- | --- | --- | --- |
| `ci.yml` | Branch metadata policy; full QA is `NOT_RUN`. | Runs on `push`, `pull_request`, and `workflow_dispatch` for `main`-centered integration. | `ci-summary` validates PR base and source prefix, reports branch policy `NOT_APPLICABLE` on main push/manual, and reports full QA `NOT_RUN`. | No QA execution; No deploy CD; no direct Kubernetes mutation, external Vault mutation, container publish, or commit push. |
| `greetings.yml` | Repository maintenance greeting automation. | Runs on issue or PR intake events. | Posts onboarding guidance only. | Not a QA gate, not a reviewer approval, and not deployment automation. |
| `labeler.yml` | Repository maintenance labeling automation. | Runs on every opened or synchronized pull request; the action matches paths itself. | Applies labels from `.github/labeler.yml`. | Not a QA gate and must not replace CODEOWNERS or human review. |

## Related Documents

### Source Basis

- 현재 workflow 계약은 `.github/workflows/*.yml`과 공통
  [Quality policy](../.agents/governance/quality.md)가 소유한다.
- 과거 SPEC-0103과 완료 증거는 [Archive 탐색](../docs/98.archive/README.md)을
  통해 찾는다. 완료 Spec을 현재 실행 권위로 사용하지 않는다.
- 외부 도구 계약이 바뀌면 공식 출처를 확인하고 현재 소유자와 소비자를
  함께 갱신한다.
