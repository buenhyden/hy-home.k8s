---
title: "hy-home.k8s"
version: "0.2.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-05"
---
# hy-home.k8s

> Linux server + k3d + ArgoCD GitOps 기반 로컬 플랫폼과 문서 협업 체계를 함께 관리하는 저장소다.

## Overview

`hy-home.k8s`는 단순한 로컬 Kubernetes 실험 저장소가 아니라, 사람과 AI가 같은 문서 구조를 공유하며 설계부터 운영까지 맥락을 추적하는 홈랩 프레임워크다. 모든 작업은 **Spec-Driven Development (SDD)**를 기준으로 진행되며, `docs/` 단계 체계를 통해 요구사항, 설계, 기술 결정, 실행 계획, 작업 증적, 운영 지식이 연결된다.

이 저장소는 Linux server + native Docker Engine 환경에서 `k3d` 멀티노드 클러스터를 부트스트랩하고, ArgoCD App-of-Apps 기반 GitOps, External Secrets + OpenBao(Vault API 호환) 연동, 외부 PostgreSQL/Valkey 인터페이스 계약을 선언형으로 관리한다. 외부 런타임 자체를 포함하지 않고, 이 저장소는 로컬 플랫폼의 **문서 SSoT + GitOps 매니페스트 + 부트스트랩 자산**에 집중한다.

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
- `examples/` 아래의 앱 온보딩 및 AWS/Azure cloud target 참조 예시
- 에이전트 게이트웨이 파일(`AGENTS.md`, `CLAUDE.md`)
- 저장소 차원의 CI, pre-commit, 문서/정적 검증 설정

### Out of Scope

- 외부 Vault/PostgreSQL/Valkey 런타임 자체의 생성 및 운영
- 애플리케이션 비즈니스 로직 구현
- AWS/Azure 실제 리소스 프로비저닝과 cloud 계정 상태 변경
- `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/05.operations`, `docs/90.references`, `docs/99.templates` SSoT 문서의 승인 없는 임의 재작성
- 운영 환경 SLA/DR 자체 보장

## Structure

```text
hy-home.k8s/
├── docs/                  # Requirement Package/AD/ADR/Spec/Plan/Task/Operations/Runbook 체계
├── gitops/                # ArgoCD가 동기화하는 선언형 GitOps 리소스
├── infrastructure/        # k3d, ArgoCD values, bootstrap 및 검증 스크립트
├── examples/              # 앱 온보딩 및 AWS/Azure cloud target 참조 예시
├── scripts/               # 저장소 유틸리티 및 자동화 스크립트
├── tests/                 # 저장소 전역 테스트 기준 문서 및 교차 테스트 영역
├── _workspace/            # Temporary non-secret analysis scratch boundary; README tracked only
├── policy/                # Kubernetes 매니페스트에 적용하는 Conftest/Rego 정책 규칙
├── secrets/               # 로컬 인증서 등 민감 파일 저장 경로
├── .github/               # GitHub Actions, PR template, CODEOWNERS, labeler, zizmor
├── .agents/               # 공급자 중립 역할·스킬 registry와 공유 자산
├── .claude/               # Claude native 투영과 권한·훅 선언
├── .codex/                # Codex native 투영과 로컬 베이스라인
├── AGENTS.md              # Codex/GPT 전용 얇은 게이트웨이
├── CLAUDE.md              # Claude 전용 얇은 오버레이
└── README.md              # This file
```

### Documentation Map

`docs/`는 stage별 책임이 분리된 문서 SSoT다. 새 문서나 변경 증적은 stage 책임에 맞는
위치와 템플릿에서 시작하며, stage별 책임과 template 선택 안내는 문서 허브
(`docs/README.md`)가 소유한다.

### 현재 구현 경계

- `gitops/`는 로컬 k3d 클러스터의 desired state 정본이다. 현재 구현은 `clusters/local`의 bootstrap/AppProject/ApplicationSet, `apps/root`의 App-of-Apps 선언, `platform/*` 공통 컴포넌트, `workloads/adminer` 참조 워크로드를 포함한다.
- `infrastructure/`는 클러스터 bootstrap과 repo-backed static checks를 위한 실행 자산이다. MetalLB 계약은 별도 디렉터리가 아니라 `ipaddresspool.yaml`, `l2advertisement.yaml` 루트 파일로 관리한다.
- k8s UI와 앱은 k8s 전용 router(k3d serverlb, `192.168.0.14:443`)가 받는 `<name>.hy-k8s.home.arpa`로 노출한다. ArgoCD는 `argo.hy-k8s.home.arpa`이고 `hy-k8s.home.arpa/<name>`은 subdomain으로 redirect된다. `hy-home.docker` Traefik은 외부 서비스(`hy.home.arpa`)만 싣는다.
- `examples/`는 앱 온보딩 템플릿과 AWS/Azure cloud target reference-only 자산이다. 실제 cloud 계정, live cluster, provider runtime 변경은 이 저장소의 일반 실행 경로가 아니다.

### Canonical Owners

- [docs/README.md](docs/README.md)
- [AGENTS.md](AGENTS.md)
- [.agents/README.md](.agents/README.md)
- `.github/repository-surface.md`
- [scripts/README.md](scripts/README.md)

### Top-level Areas

- `docs/` - 공식 문서 체계, 요구사항부터 운영/회고까지의 단계형 SSoT
- `gitops/` - ArgoCD App-of-Apps 루트, 플랫폼 리소스, 워크로드 선언
- `infrastructure/` - k3d 클러스터 설정, ArgoCD Helm values, bootstrap 및 검증 스크립트
- `examples/` - 앱 GitOps 온보딩용 참조 구현과 AWS/Azure cloud target 예시
- `scripts/` - 저장소 유지보수와 자동화 보조 스크립트
- `tests/` - 저장소 validator의 독립 behavior coverage와 synthetic fixtures
- `policy/` - 추적된 Kubernetes 매니페스트에 적용하는 Conftest/Rego deny 규칙
- `secrets/` - 로컬 인증서 배치 경로. 키 자료는 추적하지 않는다
- `_workspace/` - 비밀값을 담지 않는 임시 분석 경계. README만 추적한다
- `.github/` - `main` PR flow용 CI, release evidence, PR/issue intake, CODEOWNERS, labeler, zizmor 설정
- `.agents/` - 공급자 중립 역할·스킬·평가 하니스와 registry. Codex/Claude projection의 공통 의미를 소유하며 native 실행을 증명하지 않는다.
- `.claude/` - 추적되는 Claude project adapter. 실제 native discovery와 적용은 별도 runtime 증거가 필요하다.
- `.codex/` - 추적되는 Codex project adapter. 실제 native discovery와 적용은 별도 runtime 증거가 필요하다.

### Tech Stack

| Category       | Technology                                                                                      | Notes                                                                                           |
| -------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Language       | Bash, Markdown, YAML                                                                            | 부트스트랩/문서/매니페스트 중심                                                                 |
| Platform       | Linux server (Ubuntu 24.04 LTS), native Docker Engine                                           | 로컬 실행 환경 기준                                                                             |
| Kubernetes     | k3d, k3s, kubectl, Helm                                                                         | 로컬 멀티노드 클러스터와 패키징                                                                 |
| GitOps         | ArgoCD, ApplicationSet                                                                          | App-of-Apps 선언형 배포                                                                         |
| Ingress        | ingress-nginx, k8s 전용 router(k3d serverlb)                                                    | 로컬 k3d 유지. Ingress NGINX upstream retirement 이후 cloud target은 Gateway API/ALB/AGC로 분리 |
| Secrets        | External Secrets Operator, OpenBao(Vault API)                                                   | 외부 시크릿 동기화 계약                                                                         |
| Data Services  | External PostgreSQL, External Valkey                                                            | 저장소 외부 런타임을 Service 계약으로 연결                                                      |
| Cloud Examples | AWS EKS 1.35 target, AKS 1.35 target, Terraform AWS provider 6.x                                | provider README와 인접 실행 자산이 함께 소유하는 bounded 참조 구현                              |
| CI / Quality   | GitHub Actions, pre-commit, markdownlint, shellcheck, kube-linter, actionlint, zizmor | 정적 검증 및 정책 게이트                                                                        |

## Getting Started

### Prerequisites

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
  - OpenBao, Vault API 호환 (`https://openbao.hy.home.arpa`)
  - PostgreSQL write/read 포트
  - Valkey 접근 경로

### 1. Clone and Setup

```bash
git clone https://github.com/buenhyden/hy-home.k8s.git
cd hy-home.k8s
```

### 2. Repository Entry Points

리포지토리 작업 전에 다음 진입점을 우선 확인한다.

1. [README.md](./README.md) - 저장소 개요
2. [docs/README.md](./docs/README.md) - 단계형 문서 체계 개요
3. [AGENTS.md](./AGENTS.md), [CLAUDE.md](./CLAUDE.md) - provider별 얇은 에이전트 게이트웨이
4. `docs/05.operations/runbooks/README.md` - 실제 부트스트랩 절차

### 3. External Dependencies Readiness

외부 런타임은 이 저장소가 직접 기동하지 않는다. 먼저 아래 계약이 준비되어 있어야 한다.

- Vault가 접근 가능하고 unseal 상태다.
- `secret/platform/argocd`에 `valkey_password`가 존재한다.
- PostgreSQL write/read 포트가 열려 있다.
- Valkey가 저장소 문서에 정의된 호스트/포트로 노출된다.

필요한 확인 방법은 runbook (`docs/05.operations/runbooks/README.md`)에 정리되어 있다.

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
- [examples/README.md](./examples/README.md) - 앱 온보딩 및 cloud target 참조 예시
- [tests/README.md](./tests/README.md) - 저장소 전역 테스트 원칙

## Usage

### Repository Workflow

처음에는 [문서 허브](docs/README.md)에서 목적에 맞는 stage를 찾고,
에이전트 작업은 [공통 거버넌스](.agents/README.md)에서 역할과 절차를 찾는다.
문서 작성·링크·언어 기준과 에이전트 실행·승인·Git 절차는
[공통 거버넌스](.agents/README.md)에서 각 정책 소유자를 찾는다.

### Language Policy

이 README는 사람이 읽는 진입점이다. 문서별 언어 경계는
문서 저술 정책이 소유한다.

### Common Workflows

| Workflow       | Start Here                                               | Expected Follow-up                                                              |
| -------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------- |
| 요구사항 변경  | Stage 01 requirements | 관련 AD/ADR, Spec, Plan 링크를 갱신한다.                                       |
| 아키텍처 결정  | Stage 02 architecture | 결정의 결과를 Spec, 운영 정책, runbook에 반영한다.                              |
| 기능 구현      | Stage 03 specs | Plan/Task를 만들고 검증 증적을 남긴다.                                          |
| 운영 절차 변경 | Stage 05 operations | guide, policy, runbook 중 하나로 분류하고 GitOps-first 경계를 유지한다.         |
| 참조값 갱신    | Stage 90 references | 스냅샷 기준일과 관련 active stage 문서 영향을 함께 확인한다.                    |
| 문서 체계 변경 | Stage 99 templates | docs hub, 대상 stage README, 생성 문서의 안전한 구조 반영 여부를 함께 확인한다. |

### Relative Link Rules

링크는 이 파일의 위치를 기준으로 계산한다. stage 문서로 가는 링크와
outside-doc 참조 경계는 문서 저술 정책이
소유한다.

## Verification

정적 품질 검증은 CI와 pre-commit 설정을 기준으로 한다.

- [`./.pre-commit-config.yaml`](./.pre-commit-config.yaml)
- [`./.github/repository-surface.md`](./.github/repository-surface.md)

로컬 검증은 공통 QA 진입점을 사용한다. `quick`은 변경 범위, `full`은 인계 전 전체 저장소의 정적 검증을 수행한다. CI는 같은 차단 게이트를 `ci` 프로필로 실행한다.

```bash
python3 scripts/qa.py --list
python3 scripts/qa.py quick
python3 scripts/qa.py full
```

`full`은 독립 스냅샷에서 pre-commit과 전체 테스트를 포함한다. 동일 바이트에 대해 하위 검사 전체를 다시 실행하지 않는다. 필수 도구가 없으면 실패로 기록하며, 설치 절차와 준비 조건은 QA 운영 안내 (`docs/05.operations/guides/README.md`)를 따른다. 검증기의 bounded timeout·출력·프로세스 정리 보장은 유지된다.

표면별 승인 경계와 역할·스킬 정본은 [에이전트 거버넌스](.agents/README.md)가 라우팅한다. 정적 PASS는 네이티브 발견·권한 강제·훅 수신이나 hosted CI·클러스터 동작의 증거가 아니다. 실제 k3d/Argo CD/Vault 작업은 별도 승인된 운영 범위에 속한다.

Cloud 예시의 정확한 버전 기준은 [`examples/`](./examples/) 아래 각 cloud 예시의 실행 소스가 소유한다. 2026-03-24 이후 Ingress NGINX는 upstream retired 상태이므로 로컬 k3d 계약은 유지하되, AWS/Azure target은 ALB/Gateway API/AGC 계열로 분리한다.

## Related Documents

- [문서 허브](./docs/README.md)
- [문서 작성 양식과 가이드](./docs/99.templates/README.md)
- [에이전트 실행 거버넌스](.agents/README.md)
- [문서 저술 정책](.agents/governance/document-authoring.md)
- 현재 로컬 GitOps 플랫폼 요구사항 (`docs/01.requirements/README.md`)
- 현재 로컬 GitOps 플랫폼 Spec (`docs/03.specs/README.md`)
- ArgoCD 플랫폼 부트스트랩 Runbook (`docs/05.operations/runbooks/README.md`)
- [저장소 스크립트 인덱스](./scripts/README.md)
