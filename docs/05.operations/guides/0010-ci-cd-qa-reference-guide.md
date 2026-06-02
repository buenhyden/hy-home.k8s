---
title: 'CI/CD & QA 로컬-vs-GitHub 참조 가이드'
type: guide
status: active
owner: platform
updated: 2026-06-02
---

# CI/CD & QA 로컬-vs-GitHub 참조 가이드

---

## Overview (KR)

이 가이드는 `hy-home.k8s` 워크스페이스의 QA/CI 검증 체계를 설명한다.
로컬 개발 환경에서 실행 가능한 검증 명령과 GitHub Actions에서만 실행되는 작업을
명확히 구분하여, 커밋 전 로컬 검증 패턴과 원격 CI 게이트 구조를 이해하도록 돕는다.

## Guide Type

- how-to

## Target Audience

- 플랫폼 팀 개발자
- AI 에이전트 (문서 및 GitOps 변경 작업 시)
- 새로운 기여자

## Purpose

커밋 전 로컬에서 실행 가능한 검증 명령을 정의하고, GitHub Actions에서만 수행되는
CI 게이트와의 경계를 명확히 한다. 이 가이드를 따르면 PR 제출 전 로컬에서
CI 실패를 사전에 예방할 수 있다.

## Prerequisites

- WSL2 + k3d 환경 구성 완료 (`docs/05.operations/guides/0002-wsl2-k3d-argocd-ha-setup-guide.md`)
- `pre-commit` 설치: `pip install pre-commit && pre-commit install`
- Python 3.x 설치 및 `pyyaml` 패키지: `pip install pyyaml`
- Bash 4.x 이상 (WSL2 기본 제공)

## Step-by-step Instructions

### 1. 로컬 실행 — 커밋 전 필수 검증

로컬 개발 환경에서는 **빠른 피드백**을 위해 `pre-commit` 기반의 린트와 문법 검사만을 필수로 수행한다.
구조 검증, 의존성 점검 등의 무거운 검사는 GitHub Actions CI가 전담하여 중복 실행을 방지한다.

#### 1-1. pre-commit 전체 실행

```bash
pre-commit run --all-files
```

포함 훅: commitizen, gitleaks, detect-secrets, markdownlint-cli2,
check-dependabot, shellcheck, shfmt, actionlint, kube-linter, hadolint, check-jsonschema

단일 파일 격리 실행 (오류 발생 시):

```bash
pre-commit run --files <path/to/file>
```

#### 1-2. 디버깅 및 CI 스크립트 (선택 사항)

무거운 구조/매니페스트 검사는 GitHub Actions CI에서 수행된다. 로컬에서 CI 실패를 디버깅하거나 명시적으로 검증이 필요할 때만 아래의 스크립트들을 활용한다.

```bash
bash scripts/validate-repo-quality-gates.sh .
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
bash scripts/validate-policy-gates.sh .
```

`validate-repo-quality-gates.sh`는 문서 변경 시 다음 archive/currentness 계약도 함께 검증한다.

- `docs/98.archive`는 허용된 canonical docs stage이며 모든 Tombstone은 `archive-tombstone.template.md` 구조를 따른다.
- active `docs/01-05` 문서는 오래된 UI/endpoint runtime contract를 historical 또는 superseded 메모만으로 보존할 수 없다.
- archive Tombstone은 old full body를 보존하지 않고 metadata-only 본문을 유지한다.
- `docs/99.templates/reference.template.md`는 archive 정책이나 archive wording을 포함하지 않는다.

#### 1-8. Shell 문법 검사 (단일 파일)

```bash
bash -n scripts/<script-name>.sh
bash -n docs/00.agent-governance/hooks/<hook-name>.sh
```

### 2. GitHub Actions 전용 — 로컬 재현 불가

다음 작업들은 GitHub 이벤트 컨텍스트 또는 저장소 권한이 필요하여
로컬에서 실행되지 않는다.

#### 2-1. branch-policy (`.github/workflows/ci.yml`)

- **트리거**: PR 오픈/동기화 시에만 실행
- **역할**: PR base branch = `main` 강제, source branch 접두사 검증
- **허용 접두사**: `feat/`, `fix/`, `docs/`, `refactor/`, `test/`, `chore/`, `ci/`, `release/`, `hotfix/`, `codex/`, `dependabot/`
- **로컬 대안**: 없음 (branch policy는 PR 컨텍스트 필요)

#### 2-2. generate-changelog (`.github/workflows/generate-changelog.yml`)

- **트리거**: `v*.*.*` 태그 푸시 시
- **역할**: git-cliff로 CHANGELOG 자동 생성 및 아티팩트 업로드
- **로컬 대안**: `git cliff --output CHANGELOG.md` (git-cliff 설치 시 로컬 미리보기 가능)

#### 2-3. labeler (`.github/workflows/labeler.yml`)

- **트리거**: PR 오픈/동기화 시
- **역할**: 변경 경로 기반 자동 PR 라벨 부여
- **로컬 대안**: 없음 (GitHub API 필요)

#### 2-4. stale (`.github/workflows/stale.yml`)

- **트리거**: 매일 01:30 UTC (cron)
- **역할**: 30일(이슈)/45일(PR) 비활성 시 `stale` 라벨 부착, 이후 5일(이슈)/10일(PR) 경과 시 자동 닫기
- **로컬 대안**: 없음 (GitHub API 필요)

#### 2-5. greetings (`.github/workflows/greetings.yml`)

- **트리거**: 최초 PR/이슈 오픈 시
- **역할**: 첫 기여자 자동 환영 메시지
- **로컬 대안**: 없음 (GitHub API 필요)

### 3. CI Job 구조 (`.github/workflows/ci.yml`)

CI 파이프라인은 5개 검사 job과 1개 집계 job(`ci-summary`)으로 구성된다:

| Job                   | 트리거 조건                             | 로컬 재현 명령                                  |
| --------------------- | --------------------------------------- | ----------------------------------------------- |
| `branch-policy`       | PR 이벤트 전용                          | 없음                                            |
| `changes`             | 항상 실행 (path filter)                 | 없음                                            |
| `pre-commit`          | 모든 파일 변경                          | `pre-commit run --all-files`                    |
| `repo-quality-static` | docs, .github, .claude, scripts 등 변경 | `bash scripts/validate-repo-quality-gates.sh .` |
| `manifest-static`     | gitops, infrastructure YAML 변경        | 아래 참조                                       |
| `ci-summary`          | 항상 실행 (집계)                        | 없음                                            |

`manifest-static` 로컬 재현:

```bash
bash infrastructure/tests/verify-contracts-static.sh
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
bash scripts/validate-policy-gates.sh .
```

### 4. 커밋 전 로컬 체크리스트

모든 변경 사항 발생 시:

```bash
pre-commit run --all-files
```

로컬에서는 `pre-commit`만 통과하면 PR을 생성할 수 있으며, 통합 및 정책 게이트 검증은 GitHub CI에 위임한다.
또한 신규 애플리케이션 코드는 90% coverage 유지를, 인프라 변경 시에는 validation-matrix 커버리지를 준수해야 한다.

## Common Pitfalls

- **markdownlint auto-fix**: `pre-commit run --all-files` 첫 실행 시 파일이 자동 수정됨 → 수정된 파일을 스테이징 후 재실행
- **validate-repo-quality-gates.sh 실패**: LLM Wiki 인덱스 미동기화가 원인인 경우가 많음 → `bash scripts/generate-llm-wiki-index.sh` 실행 후 재시도
- **archive Tombstone 실패**: old 문서 본문을 보존했거나 `docs/98.archive/README.md` 외부에서 Tombstone을 직접 링크한 경우 발생 → Tombstone metadata와 활성 문서 링크를 정리
- **active docs stale contract 실패**: `docs/01-05` 활성 문서에 old UI/endpoint runtime claim이 남은 경우 발생 → current replacement 문서로 갱신하거나 archive로 이동
- **branch-policy 실패**: PR source branch 접두사 오류 → branch를 재생성하거나 GitHub에서 PR base를 확인
- **validate-policy-gates.sh conftest 미설치**: conftest 바이너리 없을 경우 스크립트가 graceful exit 0으로 종료함 (정책 게이트 미적용 상태) → conftest 설치 권장

## Related Documents

- **CI 워크플로우**: [`.github/workflows/ci.yml`](../../../.github/workflows/ci.yml)
- **Scripts 인벤토리**: [`../../../scripts/README.md`](../../../scripts/README.md)
- **K8s GitOps 정책**: [`../policies/0001-k8s-gitops-operations-policy.md`](../policies/0001-k8s-gitops-operations-policy.md)
- **HA 플랫폼 가이드**: [`0002-wsl2-k3d-argocd-ha-setup-guide.md`](0002-wsl2-k3d-argocd-ha-setup-guide.md)
- **Archive Index**: [`../../98.archive/README.md`](../../98.archive/README.md)
