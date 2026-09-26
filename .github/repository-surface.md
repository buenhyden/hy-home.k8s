---
title: "GitHub Configuration Hub"
version: "0.1.2"
type: "common/readme-runtime-governance"
status: "active"
owner: "platform"
updated: "2026-09-26"
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
- 로컬 완료 순서, lane, 결과, formatter, handoff의 유일한 정본 소유자는
  [`quality.md`](../.agents/governance/quality.md)다.
  이 hub와 PR template은 GitHub 고유 소비자를 그곳으로 안내할 뿐이다.
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
- `generate-changelog.yml`은 version tag에 대해 7일 동안 유지되는 일시적인 release 증거 artifact를 만든다. 커밋, push, publish는 하지 않는다.
- `labeler.yml`, `greetings.yml`, `stale.yml`은 저장소 유지보수 자동화이며 QA gate가 아니다.
- 관심사는 분명히 나뉜다. 로컬 pre-commit은 빠른 lint와 formatting을 맡고 로컬 저장소 정적 스크립트는 필요할 때 CI·디버그 증거를 재현하며 GitHub CI는 필수 원격 gate 판정을 내린다. Helm chart rendering은 플랫폼 AppProject 허용 목록 변경을 리뷰할 때 쓰는 수동 보조 도구로 남는다.

## Source Basis

- Parent Spec: Workspace Document Governance Hardening Spec(`docs/98.archive/completed/03.specs/0013-workspace-document-governance-hardening/spec.md`)이 GitHub Actions documentation, release 증거, 공급망 개념, Markdown·YAML formatting 주장의 공식 출처 근거를 기록한다.
- 이 hub의 workflow 역할 주장은 추적되는 `.github/workflows/*.yml` 파일과 대조해 맞춘다. 외부 도구의 최신성이 바뀌면 이 hub의 동작을 바꾸기 전에 Spec이나 Stage 90 참조 문서를 먼저 갱신한다.

## Workflow Responsibility Matrix

| Workflow | Role | Trigger / scope | Required evidence | Boundary |
| --- | --- | --- | --- | --- |
| `ci.yml` | Required QA gate for branch policy, repo-quality, agent-governance, manifest, secret, and policy checks. | Runs on `push`, `pull_request`, and `workflow_dispatch` for `main`-centered integration. | `ci-summary` aggregates `branch-policy` and the single `qa` job; QA prepares its locked dependencies once and executes the shared ci profile on an immutable checkout with full history. | No deploy CD, direct Kubernetes mutation, external Vault mutation, container publish, or commit push. |
| `generate-changelog.yml` | Release-evidence artifact generator. | Runs on pushed release tags matching `v*.*.*`. | Produces a `CHANGELOG.md` artifact retained for exactly seven days for review. | Does not commit, push, publish, or mutate repository history. |
| `greetings.yml` | Repository maintenance greeting automation. | Runs on issue or PR intake events. | Posts onboarding guidance only. | Not a QA gate, not a reviewer approval, and not deployment automation. |
| `labeler.yml` | Repository maintenance labeling automation. | Runs on every opened or synchronized pull request; the action matches paths itself. | Applies labels from `.github/labeler.yml`. | Not a QA gate and must not replace CODEOWNERS or human review. |
| `stale.yml` | Repository maintenance stale-item automation. | Runs on scheduled issue or PR maintenance. | Marks or closes stale work according to workflow configuration. | Not a QA gate, not release evidence, and not deployment automation. |

## Boundaries

- `.github` 자동화는 QA gate와 release 증거 자동화를 제공하며, 배포 CD가 아니다.
- 이 디렉터리의 workflow는 live 클러스터에 배포하거나, Kubernetes를 직접 변경하거나, 외부 Vault 리소스를 바꾸거나, container를 publish하거나, 커밋을 push하면 안 된다.
