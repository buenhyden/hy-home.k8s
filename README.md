# hy-home.k8s

> WSL2 + k3d + ArgoCD GitOps 기반 로컬 플랫폼과 문서 협업 체계를 함께 관리하는 저장소다.

## Overview

`hy-home.k8s`는 단순한 로컬 Kubernetes 실험 저장소가 아니라, 사람과 AI가 같은 문서 구조를 공유하며 설계부터 운영까지 맥락을 추적하는 홈랩 프레임워크다. 모든 작업은 **Spec-Driven Development (SDD)**를 기준으로 진행되며, `docs/` 단계 체계를 통해 요구사항, 설계, 기술 결정, 실행 계획, 작업 증적, 운영 지식이 연결된다.

이 저장소는 WSL2 + Docker Desktop 환경에서 `k3d` 멀티노드 클러스터를 부트스트랩하고, ArgoCD App-of-Apps 기반 GitOps, External Secrets + Vault 연동, 외부 PostgreSQL/Valkey 인터페이스 계약을 선언형으로 관리한다. 외부 런타임 자체를 포함하지 않고, 이 저장소는 로컬 플랫폼의 **문서 SSoT + GitOps 매니페스트 + 부트스트랩 자산**에 집중한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- `docs/` 단계 문서 체계와 README 인덱스
- `gitops/` 아래의 ArgoCD, 플랫폼, 워크로드 매니페스트
- `infrastructure/` 아래의 클러스터/Helm 값/부트스트랩 및 검증 스크립트
- `examples/` 아래의 참조 구현 및 온보딩 예시
- 에이전트 게이트웨이 파일(`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`)
- 저장소 차원의 CI, pre-commit, 문서/정적 검증 설정

### Out of Scope

- 외부 Vault/PostgreSQL/Valkey 런타임 자체의 생성 및 운영
- 애플리케이션 비즈니스 로직 구현
- `docs/01-10`, `docs/90.references`, `docs/99.templates` SSoT 문서의 승인 없는 임의 재작성
- 운영 환경 SLA/DR 자체 보장

## Structure

```text
hy-home.k8s/
├── docs/                  # PRD/ARD/ADR/Spec/Plan/Task/Operations/Runbook 체계
├── gitops/                # ArgoCD가 동기화하는 선언형 GitOps 리소스
├── infrastructure/        # k3d, ArgoCD values, bootstrap 및 검증 스크립트
├── examples/              # 앱 온보딩/플랫폼 참조 예시
├── scripts/               # 저장소 유틸리티 및 자동화 스크립트
├── tests/                 # 저장소 전역 테스트 기준 문서 및 교차 테스트 영역
├── traefik/               # 로컬 ingress 노출용 Traefik 관련 매니페스트
├── secrets/               # 로컬 인증서 등 민감 파일 저장 경로
├── AGENTS.md              # 공통 에이전트 진입 게이트웨이
├── CLAUDE.md              # Claude 전용 얇은 오버레이
├── GEMINI.md              # Gemini 전용 얇은 오버레이
└── README.md              # This file
```

## How to Work in This Area

1. 저장소를 처음 읽을 때는 `README.md -> docs/README.md -> AGENTS.md -> 관련 stage 문서` 순서로 진입한다.
2. 설계/구현/운영 판단은 가능한 한 `docs/01~09` 문서 체인을 기준으로 추적한다.
3. 새 README나 가이드는 [`docs/99.templates/readme.template.md`](docs/99.templates/readme.template.md) 같은 승인된 템플릿에서 시작한다.
4. 문서 링크는 상대 경로를 사용하고, 사람 대상 README는 한국어를 유지한다.
5. `docs/00.agent-governance/*`는 영어로 유지하며, 게이트웨이 파일에는 규칙을 중복 복사하지 않는다.
6. 외부 서비스 계약이나 부트스트랩 명령을 변경했다면 관련 README, runbook, 운영 정책 링크도 함께 점검한다.

## Related References

- [docs/README.md](docs/README.md)
- [AGENTS.md](AGENTS.md)
- [docs/01.prd/2026-03-27-wsl-k3d-argocd-platform.md](docs/01.prd/2026-03-27-wsl-k3d-argocd-platform.md)
- [docs/04.specs/001-wsl-k3d-argocd-platform/spec.md](docs/04.specs/001-wsl-k3d-argocd-platform/spec.md)
- [docs/09.runbooks/0001-argocd-platform-bootstrap-runbook.md](docs/09.runbooks/0001-argocd-platform-bootstrap-runbook.md)

## Repository Map

- `docs/` - 공식 문서 체계, 요구사항부터 운영/회고까지의 단계형 SSoT
- `gitops/` - ArgoCD App-of-Apps 루트, 플랫폼 리소스, 워크로드 선언
- `infrastructure/` - k3d 클러스터 설정, ArgoCD Helm values, bootstrap 및 검증 스크립트
- `examples/` - 앱 GitOps 온보딩용 참조 구현과 템플릿
- `scripts/` - 저장소 유지보수와 자동화 보조 스크립트
- `.claude/`, `.codex/` - 에이전트 실행 규칙, 스킬, 워크플로 오버레이

## Tech Stack

| Category | Technology | Notes |
| --- | --- | --- |
| Language | Bash, Markdown, YAML | 부트스트랩/문서/매니페스트 중심 |
| Platform | WSL2 Ubuntu, Docker Desktop | 로컬 실행 환경 기준 |
| Kubernetes | k3d, k3s, kubectl, Helm | 로컬 멀티노드 클러스터와 패키징 |
| GitOps | ArgoCD, ApplicationSet | App-of-Apps 선언형 배포 |
| Secrets | External Secrets Operator, Vault | 외부 시크릿 동기화 계약 |
| Data Services | External PostgreSQL, External Valkey | 저장소 외부 런타임을 Service 계약으로 연결 |
| CI / Quality | GitHub Actions, pre-commit, markdownlint, shellcheck, kube-linter, hadolint, actionlint, zizmor | 정적 검증 및 정책 게이트 |

## Prerequisites

- `git`
- `k3d`
- `kubectl`
- `helm`
- `docker`
- `curl`
- `jq`
- `openssl`
- `rg` (`ripgrep`)
- `VAULT_TOKEN` 환경변수
- 외부 서비스 런타임 준비:
  - Vault (`https://vault.127.0.0.1.nip.io`)
  - PostgreSQL write/read 포트
  - Valkey 접근 경로

## Getting Started

### 1. Clone and Setup

```bash
git clone https://github.com/buenhyden/hy-home.k8s.git
cd hy-home.k8s
```

### 2. Repository Entry Points

리포지토리 작업 전에 다음 진입점을 우선 확인한다.

1. [README.md](./README.md) - 저장소 개요
2. [docs/README.md](./docs/README.md) - 단계형 문서 체계 개요
3. [AGENTS.md](./AGENTS.md) - 에이전트 공통 규칙
4. [docs/09.runbooks/0001-argocd-platform-bootstrap-runbook.md](./docs/09.runbooks/0001-argocd-platform-bootstrap-runbook.md) - 실제 부트스트랩 절차

### 3. External Dependencies Readiness

외부 런타임은 이 저장소가 직접 기동하지 않는다. 먼저 아래 계약이 준비되어 있어야 한다.

- Vault가 접근 가능하고 unseal 상태다.
- `secret/platform/argocd`에 `valkey_password`가 존재한다.
- PostgreSQL write/read 포트가 열려 있다.
- Valkey가 저장소 문서에 정의된 호스트/포트로 노출된다.

필요한 확인 방법은 [runbook](./docs/09.runbooks/0001-argocd-platform-bootstrap-runbook.md)에 정리되어 있다.

### 4. Bootstrap Local Platform

필수 도구와 외부 의존성이 준비되었다면 로컬 플랫폼을 부트스트랩한다.

```bash
./infrastructure/bootstrap-local.sh
```

이 스크립트는 k3d 클러스터 생성 또는 재사용, 외부 의존성 점검, ArgoCD 설치, GitOps bootstrap 적용, 기본 연결 검증까지 수행한다.

### 5. Verify and Inspect

부트스트랩 후에는 최소한 아래 경로를 확인한다.

- [gitops/README.md](./gitops/README.md) - GitOps 경계와 구조
- [infrastructure/README.md](./infrastructure/README.md) - 인프라 자산과 bootstrap note
- [examples/README.md](./examples/README.md) - 참조 워크로드 온보딩 예시
- [tests/README.md](./tests/README.md) - 저장소 전역 테스트 원칙

정적 품질 검증은 CI와 pre-commit 설정을 기준으로 한다.

- [`.pre-commit-config.yaml`](./.pre-commit-config.yaml)
- [`.github/workflows/ci.yml`](./.github/workflows/ci.yml)

repo-backed 정적 검증을 로컬에서 확인할 때는 아래 순서로 실행한다.

```bash
bash infrastructure/tests/verify-contracts-static.sh
bash scripts/validate-repo-quality-gates.sh .
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
find infrastructure scripts -type f -name '*.sh' -exec bash -n {} \;
```
