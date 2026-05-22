# hy-home.k8s

> WSL2 + k3d + ArgoCD GitOps 기반 로컬 플랫폼과 문서 협업 체계를 함께 관리하는 저장소다.

## Overview

`hy-home.k8s`는 단순한 로컬 Kubernetes 실험 저장소가 아니라, 사람과 AI가 같은 문서 구조를 공유하며 설계부터 운영까지 맥락을 추적하는 홈랩 프레임워크다. 모든 작업은 **Spec-Driven Development (SDD)**를 기준으로 진행되며, `docs/` 단계 체계를 통해 요구사항, 설계, 기술 결정, 실행 계획, 작업 증적, 운영 지식이 연결된다.

이 저장소는 WSL2 + WSL-native Docker 환경에서 `k3d` 멀티노드 클러스터를 부트스트랩하고, ArgoCD App-of-Apps 기반 GitOps, External Secrets + Vault 연동, 외부 PostgreSQL/Valkey 인터페이스 계약을 선언형으로 관리한다. 외부 런타임 자체를 포함하지 않고, 이 저장소는 로컬 플랫폼의 **문서 SSoT + GitOps 매니페스트 + 부트스트랩 자산**에 집중한다.

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
- `traefik/` 아래의 k3d 로컬 노출 보조용 dynamic config
- `examples/` 아래의 앱 온보딩 및 AWS/Azure cloud target 참조 예시
- 에이전트 게이트웨이 파일(`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`)
- 저장소 차원의 CI, pre-commit, 문서/정적 검증 설정

### Out of Scope

- 외부 Vault/PostgreSQL/Valkey 런타임 자체의 생성 및 운영
- 애플리케이션 비즈니스 로직 구현
- AWS/Azure 실제 리소스 프로비저닝과 cloud 계정 상태 변경
- `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, `docs/99.templates` SSoT 문서의 승인 없는 임의 재작성
- 운영 환경 SLA/DR 자체 보장

## Structure

```text
hy-home.k8s/
├── docs/                  # PRD/ARD/ADR/Spec/Plan/Task/Operations/Runbook 체계
├── gitops/                # ArgoCD가 동기화하는 선언형 GitOps 리소스
├── infrastructure/        # k3d, ArgoCD values, bootstrap 및 검증 스크립트
├── examples/              # 앱 온보딩 및 AWS/Azure cloud target 참조 예시
├── scripts/               # 저장소 유틸리티 및 자동화 스크립트
├── tests/                 # 저장소 전역 테스트 기준 문서 및 교차 테스트 영역
├── traefik/               # k3d 로컬 노출 보조용 Traefik dynamic config
├── secrets/               # 로컬 인증서 등 민감 파일 저장 경로
├── .github/               # GitHub Actions, PR template, CODEOWNERS, labeler, zizmor
├── AGENTS.md              # 공통 에이전트 진입 게이트웨이
├── CLAUDE.md              # Claude 전용 얇은 오버레이
├── GEMINI.md              # Gemini 전용 얇은 오버레이
└── README.md              # This file
```

## Documentation Map

`docs/`는 stage별 책임이 분리된 문서 SSoT다. 새 문서나 변경 증적은 아래 책임에 맞는 위치와 템플릿에서 시작한다.

| Area | Responsibility | Template |
| --- | --- | --- |
| [`docs/01.requirements`](docs/01.requirements/README.md) | 제품 요구사항, 사용자 문제, 범위, 성공/수용 기준 | [`prd.template.md`](docs/99.templates/prd.template.md) |
| [`docs/02.architecture`](docs/02.architecture/README.md) | 아키텍처 요구사항, 참조 구조, 의사결정 | [`ard.template.md`](docs/99.templates/ard.template.md), [`adr.template.md`](docs/99.templates/adr.template.md) |
| [`docs/03.specs`](docs/03.specs/README.md) | 기능/워크플로우/시스템 구현 명세와 feature-local API/Agent/Data/Test 계약 | [`spec.template.md`](docs/99.templates/spec.template.md), helper templates는 [`03.specs README`](docs/03.specs/README.md) 참조 |
| [`docs/04.execution`](docs/04.execution/README.md) | 실행 계획, 작업 분해, 검증 증적 | [`plan.template.md`](docs/99.templates/plan.template.md), [`task.template.md`](docs/99.templates/task.template.md) |
| [`docs/05.operations`](docs/05.operations/README.md) | 운영 가이드, 정책, 런북, 사고 기록 | [`guide.template.md`](docs/99.templates/guide.template.md), [`operation.template.md`](docs/99.templates/operation.template.md), [`runbook.template.md`](docs/99.templates/runbook.template.md), [`incident.template.md`](docs/99.templates/incident.template.md), [`postmortem.template.md`](docs/99.templates/postmortem.template.md) |
| [`docs/90.references`](docs/90.references/README.md) | 참조 자료, 용어, 버전 인벤토리, lookup material | [`reference.template.md`](docs/99.templates/reference.template.md) |
| [`docs/99.templates`](docs/99.templates/README.md) | canonical document templates, target folder mapping, target-relative link 규칙 | [template-folder mapping](docs/99.templates/README.md#template-folder-mapping)을 기준으로 새 문서를 시작한다. |

## 현재 구현 경계

- `gitops/`는 로컬 k3d 클러스터의 desired state 정본이다. 현재 구현은 `clusters/local`의 bootstrap/AppProject/ApplicationSet, `apps/root`의 App-of-Apps 선언, `platform/*` 공통 컴포넌트, `workloads/adminer` 참조 워크로드를 포함한다.
- `infrastructure/`는 클러스터 bootstrap과 repo-backed static checks를 위한 실행 자산이다. MetalLB 계약은 별도 디렉터리가 아니라 `ipaddresspool.yaml`, `l2advertisement.yaml` 루트 파일로 관리한다.
- `traefik/`은 canonical 배포 경로가 아니라 `hy-home.docker` Traefik gateway와 맞물리는 로컬 dynamic config 참조다. Kubernetes desired state는 `gitops/`와 ArgoCD reconciliation이 기준이다.
- `examples/`는 앱 온보딩 템플릿과 AWS/Azure cloud target reference-only 자산이다. 실제 cloud 계정, live cluster, provider runtime 변경은 이 저장소의 일반 실행 경로가 아니다.

## How to Work in This Area

1. 저장소를 처음 읽을 때는 `README.md -> docs/README.md -> AGENTS.md -> 관련 stage 문서` 순서로 진입한다.
2. 설계/구현/운영 판단은 가능한 한 `docs/01.requirements`부터 `docs/05.operations/runbooks`까지의 문서 체인을 기준으로 추적한다.
3. 새 README나 authored stage 문서는 [`docs/99.templates/README.md`](docs/99.templates/README.md)의 template-folder mapping을 확인한 뒤 승인된 템플릿에서 시작한다.
4. 문서 링크는 상대 경로를 사용하고, 사람 대상 README는 한국어를 유지한다.
5. `docs/00.agent-governance/*`는 영어로 유지하며, 게이트웨이 파일에는 규칙을 중복 복사하지 않는다.
6. README 파일은 기본적으로 frontmatter를 요구하지 않는다. PRD/ARD/ADR/Spec/Plan/Task/Guide/Operations Policy/Runbook/Incident/Postmortem/Reference 같은 authored stage 문서는 `title`, `type`, `status`, `owner`, `updated` metadata를 유지한다.
7. 문서 체계나 템플릿을 바꾸면 [`docs/README.md`](docs/README.md), 해당 stage README, [`docs/99.templates/README.md`](docs/99.templates/README.md), 생성 문서 적용 범위를 같은 변경에서 점검한다.
8. 브랜치 전략은 `main` 중심 PR flow를 기본으로 하며, 상세 규칙은 [`docs/00.agent-governance/rules/git-workflow.md`](docs/00.agent-governance/rules/git-workflow.md)를 따른다.
9. 인프라 변경은 GitOps-first로 다룬다. 일반 변경에서 live cluster mutation, `kubectl apply`, 외부 Vault 조작을 도입하지 않는다.
10. `.github` 자동화나 QA gate를 바꿀 때는 [`.github/ABOUT.md`](.github/ABOUT.md)와 PR template의 검증 체크리스트를 함께 확인한다.
11. 외부 서비스 계약이나 부트스트랩 명령을 변경했다면 관련 README, runbook, 운영 정책 링크도 함께 점검한다.
12. AWS/Azure 예시는 2026-05-09 공식 지원 스냅샷을 기준으로 관리하며, 실제 cloud 배포 절차가 아니라 참조 구현으로 다룬다.

## Common Workflows

| Workflow | Start Here | Expected Follow-up |
| --- | --- | --- |
| 요구사항 변경 | [`docs/01.requirements`](docs/01.requirements/README.md) | 관련 ARD/ADR, Spec, Plan 링크를 갱신한다. |
| 아키텍처 결정 | [`docs/02.architecture`](docs/02.architecture/README.md) | 결정의 결과를 Spec, 운영 정책, runbook에 반영한다. |
| 기능 구현 | [`docs/03.specs`](docs/03.specs/README.md) | Plan/Task를 만들고 검증 증적을 남긴다. |
| 운영 절차 변경 | [`docs/05.operations`](docs/05.operations/README.md) | guide, policy, runbook 중 하나로 분류하고 GitOps-first 경계를 유지한다. |
| 참조값 갱신 | [`docs/90.references`](docs/90.references/README.md) | 스냅샷 기준일과 관련 active stage 문서 영향을 함께 확인한다. |
| 문서 체계 변경 | [`docs/99.templates`](docs/99.templates/README.md) | docs hub, 대상 stage README, 생성 문서의 안전한 구조 반영 여부를 함께 확인한다. |

## Link Basis

이 README의 링크 기준 위치는 repository root다.

- `docs/...` 링크는 canonical documentation taxonomy로 연결한다.
- `gitops/`, `infrastructure/`, `examples/`, `scripts/`, `tests/`, `traefik/` 링크는 root-level implementation/support 영역으로 연결한다.
- nested README 예시는 이 파일의 root-relative 링크를 복사하지 않고, 최종 README 위치에서 상대 경로를 다시 계산한다.

## Related Documents

- [docs/README.md](docs/README.md)
- [AGENTS.md](AGENTS.md)
- [docs/01.requirements/2026-03-27-wsl-k3d-argocd-platform.md](docs/01.requirements/2026-03-27-wsl-k3d-argocd-platform.md)
- [docs/03.specs/001-wsl-k3d-argocd-platform/spec.md](docs/03.specs/001-wsl-k3d-argocd-platform/spec.md)
- [docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md](docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md)
- [docs/90.references/README.md](docs/90.references/README.md)
- [.github/ABOUT.md](.github/ABOUT.md)
- [scripts/README.md](scripts/README.md)

## Repository Map

- `docs/` - 공식 문서 체계, 요구사항부터 운영/회고까지의 단계형 SSoT
- `gitops/` - ArgoCD App-of-Apps 루트, 플랫폼 리소스, 워크로드 선언
- `infrastructure/` - k3d 클러스터 설정, ArgoCD Helm values, bootstrap 및 검증 스크립트
- `traefik/` - k3d 로컬 ingress-nginx 뒤에서 ArgoCD/Headlamp/Kiali/Rollouts를 노출하는 보조 dynamic config
- `examples/` - 앱 GitOps 온보딩용 참조 구현과 AWS/Azure cloud target 예시
- `scripts/` - 저장소 유지보수와 자동화 보조 스크립트
- `graphify-out/` - 공유된 graphify 탐색 산출물. `GRAPH_REPORT.md`, `graph.json`, `graph.html`만 추적한다.
- `.github/` - `main` PR flow용 CI, release evidence, PR/issue intake, CODEOWNERS, labeler, zizmor 설정
- `.claude/`, `.codex/` - 에이전트 실행 규칙, 스킬, 워크플로 오버레이

## Tech Stack

| Category | Technology | Notes |
| --- | --- | --- |
| Language | Bash, Markdown, YAML | 부트스트랩/문서/매니페스트 중심 |
| Platform | WSL2 Ubuntu, WSL-native Docker | 로컬 실행 환경 기준 |
| Kubernetes | k3d, k3s, kubectl, Helm | 로컬 멀티노드 클러스터와 패키징 |
| GitOps | ArgoCD, ApplicationSet | App-of-Apps 선언형 배포 |
| Ingress | ingress-nginx, Traefik dynamic config | 로컬 k3d 유지. Ingress NGINX upstream retirement 이후 cloud target은 Gateway API/ALB/AGC로 분리 |
| Secrets | External Secrets Operator, Vault | 외부 시크릿 동기화 계약 |
| Data Services | External PostgreSQL, External Valkey | 저장소 외부 런타임을 Service 계약으로 연결 |
| Cloud Examples | AWS EKS 1.35 target, AKS 1.35 target, Terraform AWS provider 6.x | 2026-05-09 공식 지원 스냅샷 기준 참조 구현 |
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
4. [docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md](./docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md) - 실제 부트스트랩 절차

### 3. External Dependencies Readiness

외부 런타임은 이 저장소가 직접 기동하지 않는다. 먼저 아래 계약이 준비되어 있어야 한다.

- Vault가 접근 가능하고 unseal 상태다.
- `secret/platform/argocd`에 `valkey_password`가 존재한다.
- PostgreSQL write/read 포트가 열려 있다.
- Valkey가 저장소 문서에 정의된 호스트/포트로 노출된다.

필요한 확인 방법은 [runbook](./docs/05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md)에 정리되어 있다.

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
- [traefik/README.md](./traefik/README.md) - k3d 로컬 노출 보조 경로
- [examples/README.md](./examples/README.md) - 앱 온보딩 및 cloud target 참조 예시
- [tests/README.md](./tests/README.md) - 저장소 전역 테스트 원칙

정적 품질 검증은 CI와 pre-commit 설정을 기준으로 한다.

- [`./.pre-commit-config.yaml`](./.pre-commit-config.yaml)
- [`./.github/workflows/ci.yml`](./.github/workflows/ci.yml)
- [`./.github/ABOUT.md`](./.github/ABOUT.md)

repo-backed 정적 검증을 로컬에서 확인할 때는 아래 순서로 실행한다. 이 묶음은 CI의 `repo-quality-static`, `manifest-static`, `shell-static` 책임과 맞춰져 있다.

```bash
bash scripts/generate-llm-wiki-index.sh --check
bash scripts/validate-repo-quality-gates.sh .
bash infrastructure/tests/verify-contracts-static.sh
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +
```

`validate-repo-quality-gates.sh`는 authored docs에서 bare/main direct push 예시와 PR-flow 문맥 없는 push 예시 회귀를 차단하고, README/examples 등 broader Markdown roots에서는 bare/main direct push 예시를 차단한다. 또한 `generate-llm-wiki-index.sh --check`로 LLM WIKI generated index freshness를 확인한다. `pre-commit`, `kube-linter`, `zizmor`, `actionlint`, `shellcheck`는 로컬에 있으면 사용한다. 로컬 `PATH`에 없을 때는 위의 repo-backed 검증을 먼저 실행하고, 전체 hook/tool matrix는 GitHub Actions에서 확인한다.

Cloud 예시의 버전 기준은 [Tech Stack Version Inventory](./docs/90.references/versions/tech-stack-version-inventory.md)에 기록한다. 2026-03-24 이후 Ingress NGINX는 upstream retired 상태이므로 로컬 k3d 계약은 유지하되, AWS/Azure target은 ALB/Gateway API/AGC 계열로 분리한다.
