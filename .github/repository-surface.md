---
title: "GitHub Configuration Hub"
version: "0.2.0"
type: "common/readme-runtime-governance"
status: "active"
owner: "platform"
updated: "2026-10-02"
---
# GitHub Configuration Hub

이 문서는 `hy-home.k8s`의 main branch PR 흐름에 쓰이는 저장소 고유 GitHub
자동화 surface를 안내한다. 정책의 정본이 아니라 routing surface다. 이름이
`README.md`가 아니라 `repository-surface.md`인 이유는 두 가지다. `.github`
디렉터리 자체의 내용이 아니라 저장소의 자동화 surface를 설명하기 때문이고
GitHub가 `.github/README.md`를 저장소 프로필 페이지로 해석하기 때문이다.

## Content Mapping

- `workflows/` - CI, release 증거, 저장소 유지보수 자동화
- `ISSUE_TEMPLATE/` - 구조화된 버그·기능 접수 양식
- `PULL_REQUEST_TEMPLATE.md` - `docs/01.requirements/`, `docs/`, `docs/03.specs/`, GitOps QA에 맞춘 PR 검증 체크리스트
- `CODEOWNERS` - 저장소 경로와 GitHub 설정의 리뷰 소유권
- `dependabot.yml`과 `labeler.yml` - GitHub 기본 기능을 쓰는 의존성·label 설정
- `SECURITY.md` - 취약점 신고 안내

## Policy Routing

- branch 전략 정책은 `.agents/governance/git.md`에 있다.
- CI 강제는 `workflows/ci.yml`과 `scripts/qa.py`가 맡고 로컬 QA와 공유하는
  논리 gate는 validation registry가 소유한다.
- QA job 하나가 Python 3.12를 고르고
  `requirements/ci-validation.txt`의 완전 해시·binary 전용 lock을 설치한다.
  기록된 Gitleaks와 Conftest asset은 고정된 checksum과 대조하고 전체 이력을
  가진 immutable event checkout을 검증한다. pre-commit과 unit discovery는
  full/ci profile 안에서 한 번씩 실행된다. 이들의 설정은 계속 lock,
  pre-commit 설정, execution registry가 소유한다.
- Dependabot은 고정된 Actions만 다룬다. 해시된 Python lock은 사람이 직접
  갱신한다. `scripts/validate-ci-python-contract.py`가 해석된 pin을 정확히
  단언하므로, lock 변경과 그 단언은 리뷰를 거친 한 변경에서 함께 바뀌어야 한다.
  자동 bump는 자기 gate를 통과할 수 없는 pull request를 열게 된다.
- 로컬 커밋, PR, main, 로컬 전용 인계의 delivery owner와 증거 순서는
  [`quality.md`](../.agents/governance/quality.md#delivery-ownership)가 소유한다.
  PR의 최종 full QA는 hosted CI가 담당한다. 이 hub와 PR template은
  GitHub 고유 소비자를 그곳으로 안내한다.
- 현재 검증기 명령과 fixture inventory는
  [`scripts/README.md`](../scripts/README.md)와
  [`tests/README.md`](../tests/README.md)에 있다. 이 hub는 그 개수를 옮겨
  적지 않는다.
- ARWB-003은 31개 record·202개 link 전체 cutover 증명을 명시적인 로컬·수동 증거로 기록한다. 그래서 공통 QA profile은 그 별도 증명을 호출하지 않는다. 차단형 ACER migration 검증기는 닫힌 lane에 공급된, 보안 검증을 거친 정확한 Gitleaks 실행 파일로 추가된 archive payload를 분류한다.
- `ci.yml`은 pull request의 형태를 검증한다. 직접 push 제한은 저장소 로컬 파일 밖에서 GitHub branch protection과 ruleset이 강제한다.
- PR 작성자와 리뷰어 안내는 `PULL_REQUEST_TEMPLATE.md`에 있다.
- CI Python 의존성 identity는 `.github/requirements/ci-validation.txt`에 있고
  pre-commit 저장소 revision과 source tag 출처는 `.pre-commit-config.yaml`에
  있다.
- 전체 SHA로 Action을 고정하는 규칙은 저장소 품질 gate가 강제한다. zizmor 억제 파일은 필요 없다.

## Workflow Roles

- `ci.yml`은 저장소의 정본 통합 branch를 대상으로 하는 push와 pull request에 필요한 QA gate이며 `workflow_dispatch`로 수동 재실행할 수 있다. 단일 QA job이 선택된 현재 정적 계약을 강제하지만 추적되는 workflow 파일을 hosted run 증거로 취급하지는 않는다.
- `qa-verifier.yml`은 별도 verifier App의 `qa-provenance`와
  `qa-main-verdict`를 발행한다. 성공한 main push에는 격리된 publisher job이
  연결된다. App·환경·required-check·ruleset 관측 전에는 비활성 상태다.
- `generate-changelog.yml`은 version tag에 대해 7일 동안 유지되는 일시적인 release 증거 artifact를 만든다. 커밋, push, publish는 하지 않는다.
- `labeler.yml`, `greetings.yml`, `stale.yml`은 저장소 유지보수 자동화이며 QA gate가 아니다.
- 관심사는 분명히 나뉜다. 로컬 pre-commit은 빠른 lint와 formatting을 맡고 로컬 저장소 정적 스크립트는 필요할 때 CI·디버그 증거를 재현하며 GitHub CI는 필수 원격 gate 판정을 내린다. Helm chart rendering은 플랫폼 AppProject 허용 목록 변경을 리뷰할 때 쓰는 수동 보조 도구로 남는다.

## Source Basis

- 현재 workflow 계약은 `.github/workflows/*.yml`과 공통 [Quality policy](../.agents/governance/quality.md)가 소유한다.
- 과거 조사 기록은 [archive 탐색](../docs/98.archive/README.md)을 통해 찾는다. 완료 Spec을 실행 권위나 선행 읽기 조건으로 사용하지 않는다.
- 외부 도구 계약이 바뀌면 공식 출처를 확인하고 해당 현재 workflow·정책·참조 소유자를 함께 갱신한다.

## Workflow Responsibility Matrix

| Workflow | Role | Trigger / scope | Required evidence | Boundary |
| --- | --- | --- | --- | --- |
| `ci.yml` | Required QA gate for branch policy, repo-quality, agent-governance, manifest, secret, and policy checks. | Runs on `push`, `pull_request`, and `workflow_dispatch` for `main`-centered integration. | `ci-summary` aggregates `branch-policy` and the single `qa` job; QA prepares its locked dependencies once and executes the shared ci profile on an immutable checkout with full history. | No deploy CD, direct Kubernetes mutation, external Vault mutation, container publish, or commit push. |
| `generate-changelog.yml` | Release-evidence artifact generator. | Runs on pushed release tags matching `v*.*.*`. | Produces a `CHANGELOG.md` artifact retained for exactly seven days for review. | Does not commit, push, publish, or mutate repository history. |
| `greetings.yml` | Repository maintenance greeting automation. | Runs on issue or PR intake events. | Posts onboarding guidance only. | Not a QA gate, not a reviewer approval, and not deployment automation. |
| `labeler.yml` | Repository maintenance labeling automation. | Runs on every opened or synchronized pull request; the action matches paths itself. | Applies labels from `.github/labeler.yml`. | Not a QA gate and must not replace CODEOWNERS or human review. |
| `qa-verifier.yml` | Protected PR/main verdict and separately gated immutable main-tag publisher. | Default-branch `workflow_run` after completed CI; publisher requires authenticated successful `push` on `main` and successful verifier job. | Expected-verifier-App `qa-main-verdict` v2 full or v4 full-or-reused, exact source run/attempt/checkout, current main tip, publisher App/environment and ruleset observations. Hosted activation remains DEFER. | Main-only `qa-control` and `qa-tag-publish` keep App keys separate; no PR code/cache/artifact execution. `QA_TAG_ENABLED` defaults off; only exact tag creation is permitted by the publisher. |
| `stale.yml` | Repository maintenance stale-item automation. | Runs on scheduled issue or PR maintenance. | Marks or closes stale work according to workflow configuration. | Not a QA gate, not release evidence, and not deployment automation. |

## Protected Main Tags

- `publish-main-tag` job은 `verify-qa` 성공 뒤에만 실행되며 main push의
  source event·branch·repository·conclusion을 환경 접근 전에 제한한다.
  `workflow_run`의 `GITHUB_SHA`와 `GITHUB_REF`는 기본 branch의 제어 코드
  checkout용이다. 원본 push의 `after` 필드로 취급하지 않는다. 게시 SHA는
  인증된 source run의 `head_sha`, 실제 테스트 checkout, App verdict,
  현재 main tip이 모두 일치할 때만 선택한다. 여러 commit을 포함한 push도
  그 tip 하나만 대상이며, main이 이미 전진했다면 게시를 거부한다.
- 기존 bounded verifier/parser로 source repository·CI workflow·run·attempt와
  전체 gate를 재검증하고, 기대한 verifier App ID의 정확한
  `qa-main-verdict`를 대조한다. 첫 단계에는 publisher key가 없다.
  두 번째 단계도 독립적으로 재인증한 뒤 key를 읽고 token을 발급한다.
  `ci-summary`의 이름이나 성공 상태만으로 태그를 만들지 않는다.
- Operator는 verifier와 다른 publisher App에 `metadata: read`와
  `contents: write`만 부여하고 `QA_PUBLISHER_PRIVATE_KEY`를
  main만 허용하는 `qa-tag-publish` 환경에만 보관한다. App ID는
  `QA_PUBLISHER_APP_ID`이며 verifier의 key나 ID를 재사용하지 않는다.
  생성하는 installation token은 현재 repository ID와 위 권한으로 좁히며
  사용 후 폐기한다. workflow의 `GITHUB_TOKEN` 권한은 read-only다.
- `contents: write` 자체는 태그 불변성을 보장하지 않는다. Operator가
  `refs/tags/main-*`에 별도 ruleset 두 개를 적용해야 한다. 생성 제한에는
  publisher App만 creation bypass를 주고, update/delete 제한에는 publisher
  bypass를 주지 않는다. 명시적으로 승인된 operator bypass는 따로 기록한다.
  활성 규칙·대상·상속·전체 bypass actor를 설정 쓰기 권한이 있는 주체로
  read-back하고, 일반 publisher token의 update/delete 거부를 관측한다.
  bypass 목록이 응답에서 생략되면 빈 목록이나 강제 증거로 해석하지 않는다.
- 위 관측과 protected main check가 확인된 뒤에만 환경 소유
  `QA_TAG_ENABLED`를 `true`로 둔다. 같은 이름의 repository/organization
  변수는 두지 않는다. 환경 변수는 job 시작 뒤 제공되므로 step 조건과
  Python 진입점에서 검사한다. 비활성일 때 key 단계와 게시를 건너뛴다.
  App 설치·환경 제한·ruleset·거부 시험·hosted 성공/재시도 관측은 현재
  **DEFER**이며, 추적된 YAML이나 fixture 통과가 이를 대신하지 않는다.
- 생성은 `refs/tags/main-<40-hex SHA>`의 lightweight commit ref에 대한
  `POST` 한 번이다. 이미 같은 commit object면 `noop`, 다른 target이나
  annotated tag면 실패한다. 동시 생성 충돌도 같은 ref/type/SHA를
  read-back한 경우만 `noop`이며 다른 API 실패는 실패로 남는다.
  ref update/delete와 force는 제공하지 않는다. 롤백은 publication을 끄며
  기존 태그를 이동하거나 삭제하지 않는다.
- App token으로 생긴 태그도 workflow event를 만들 수 있다. QA의 push
  filter는 `branches: [main]`만 허용하므로 태그를 제외하고, changelog의
  `v*.*.*` filter는 `main-*`와 일치하지 않는다. 이 경계는
  `GITHUB_TOKEN`의 재귀 억제 동작에 의존하지 않는다.

공식 계약: [workflow_run identity](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_run),
[Git ref creation](https://docs.github.com/en/rest/git/refs#create-a-reference),
[App token restriction](https://docs.github.com/en/rest/apps/apps#create-an-installation-access-token-for-an-app),
[tag rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets),
[ruleset bypass read-back](https://docs.github.com/en/rest/repos/rules#get-a-repository-ruleset),
[environment variable timing](https://docs.github.com/en/actions/reference/workflows-and-actions/variables#configuration-variable-precedence),
[App-triggered events](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).

## Boundaries

- `.github` 자동화는 QA gate와 release 증거 자동화를 제공하며, 배포 CD가 아니다.
- 이 디렉터리의 workflow는 live 클러스터에 배포하거나, Kubernetes를 직접 변경하거나, 외부 Vault 리소스를 바꾸거나, container를 publish하거나, 커밋을 push하면 안 된다.
