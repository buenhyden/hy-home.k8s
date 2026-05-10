# sample-app

> 새 애플리케이션을 `hy-home.k8s` GitOps 경로에 온보딩할 때 사용하는 참조 예시다.

## Overview

이 디렉터리는 `hy-home.k8s` 클러스터에 새로운 앱을 온보딩할 때 참조하는 GitOps 예시다. Rollout, Service, Ingress, AnalysisTemplate, ExternalSecret, Traefik dynamic config 예시를 함께 제공해 앱별 manifest 세트를 빠르게 만들 수 있게 한다.

예시는 feature branch + PR flow를 전제로 한다. `main`에 직접 반영하는 흐름은 저장소 운영 정책과 quality gate에서 허용하지 않는다.

## Audience

이 README의 주요 독자:

- Application Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 앱별 GitOps manifest 템플릿
- placeholder 치환 방식
- Argo Rollouts, ESO, Ingress, AnalysisTemplate 구성 예시
- `hy-home.docker` Traefik dynamic config 샘플 위치 안내

### Out of Scope

- 실제 애플리케이션 소스 코드
- live cluster에 직접 리소스를 적용하는 절차
- production secret 값 또는 credential 예시
- AWS/Azure cloud target 구현

## Structure

```text
examples/sample-app/
├── kustomization.yaml        # Kustomize 진입점
├── rollout.yaml              # Argo Rollout (canary 전략)
├── service.yaml              # Service (Istio http- 포트 명명 규칙)
├── ingress.yaml              # Ingress (nginx + cert-manager mkcert TLS)
├── analysis-template.yaml    # AnalysisTemplate (Prometheus 재시작 검사)
├── external-secret.yaml      # ExternalSecret (Vault 연동, 선택 사항)
└── traefik-k3d.yaml.example  # Traefik dynamic config (hy-home.docker 레포용)
```

## How to Work in This Area

### 1. 플레이스홀더 교체

파일 내 `<appname>`, `<owner>`, `<tag>`, `<port>`를 실제 값으로 교체한다.

| 플레이스홀더 | 설명                     | 예시        |
| ------------ | ------------------------ | ----------- |
| `<appname>`  | 앱 이름 (소문자, 하이픈) | `my-api`    |
| `<owner>`    | GitHub 사용자명/조직명   | `buenhyden` |
| `<tag>`      | 컨테이너 이미지 태그     | `v1.2.3`    |
| `<port>`     | 앱 listen 포트           | `8080`      |

### 2. workloads 디렉토리에 복사

```bash
cp -r examples/sample-app gitops/workloads/<appname>
# 플레이스홀더 일괄 교체
sed -i 's/<appname>/my-api/g; s/<owner>/buenhyden/g; s/<tag>/v1.0.0/g; s/<port>/8080/g' \
  gitops/workloads/<appname>/*.yaml
```

### 3. Traefik 설정 추가 (hy-home.docker 레포)

```bash
cp examples/sample-app/traefik-k3d.yaml.example \
  ../hy-home.docker/infra/01-gateway/traefik/dynamic/<appname>-k3d.yaml
# 플레이스홀더 교체
```

### 4. feature branch + PR flow로 반영

```bash
git checkout -b feat/<appname>-gitops
git add gitops/workloads/<appname>/
git commit -m "feat: add <appname> to GitOps"
git push origin feat/<appname>-gitops
```

PR review 후 `main`에 병합되면 ArgoCD `apps-generator` ApplicationSet이 자동으로 Application을 생성하고 배포한다.

## 현재 플랫폼 전제 조건

- `apps` namespace에 `PeerAuthentication STRICT` 적용 중 → Istio mTLS 강제
- `apps` namespace NetworkPolicy → postgres(172.18.0.15) egress 허용
- `ingress-nginx`에 Istio sidecar 주입 → mTLS 체인 완성
- AnalysisTemplate이 Prometheus(`prometheus-external.platform.svc.cluster.local:9090`) 접근 필요

## Related References

- Guide: [`docs/05.operations/guides/0008-github-app-gitops-onboarding-guide.md`](../../docs/05.operations/guides/0008-github-app-gitops-onboarding-guide.md)
- Runbook: [`docs/05.operations/runbooks/0010-github-app-gitops-onboarding-runbook.md`](../../docs/05.operations/runbooks/0010-github-app-gitops-onboarding-runbook.md)
- Operations: [`docs/05.operations/policies/0007-app-gitops-onboarding-policy.md`](../../docs/05.operations/policies/0007-app-gitops-onboarding-policy.md)
- 참조 구현: [`gitops/workloads/adminer/`](../../gitops/workloads/adminer)
