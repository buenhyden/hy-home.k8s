---
name: gitops-workflow
description: >
  ArgoCD GitOps 워크플로우 스킬. 앱 온보딩, sync 절차, PR→ArgoCD 파이프라인 실행 가이드를 제공한다.
  "ArgoCD에 앱 등록", "GitOps 절차", "sync 실패 원인", "ApplicationSet 추가",
  "새 워크로드 온보딩"을 요청하면 반드시 이 스킬을 사용할 것.
  pipeline-designer 패턴을 ArgoCD GitOps-First 제약으로 적용.
---

# gitops-workflow

ArgoCD 기반 GitOps 절차 가이드. pipeline-designer 패턴 기반으로 온보딩·변경·sync 진단 워크플로우를 표준화한다.

## 핵심 원칙: GitOps-First

모든 클러스터 변경은 반드시 **코드 → PR → ArgoCD sync** 경로를 따른다.
`kubectl apply` 직접 실행은 GitOps drift를 유발하므로 절대 금지한다.
이 원칙을 지키는 이유: ArgoCD가 선언적 상태의 유일한 진실 소스이기 때문이다.

## 워크플로우 A: 새 앱 온보딩

```
1. gitops/workloads/<app-name>/ 디렉토리 생성
2. kustomization.yaml + 리소스 파일 작성
3. gitops/clusters/local/applicationset-apps.yaml 또는
   gitops/apps/root/<app>-app.yaml 에 Application 추가
4. bash scripts/validate-k8s-manifests.sh gitops/workloads/<app-name>/
5. PR 생성 → 리뷰 → merge
6. ArgoCD auto-sync 대기 (또는 수동: kubectl -n argocd get app <name>)
```

필요 파일 목록 (최소):

- `kustomization.yaml` — 리소스 목록
- `deployment.yaml` 또는 `rollout.yaml` — 워크로드 정의
- `service.yaml` — 서비스 엔드포인트

## 워크플로우 B: 기존 앱 변경

```
1. 변경 대상 파일 편집
2. k8s-validate 스킬 실행 (kube-linter + 구조 검증)
3. git add → commit (conventional commit 형식)
4. PR 생성 → CODEOWNERS 리뷰
5. merge → ArgoCD sync 확인
```

## 워크플로우 C: Sync 실패 진단

```bash
# 1. 앱 상태 확인
kubectl get app <name> -n argocd -o wide

# 2. 상세 오류 확인
kubectl describe app <name> -n argocd

# 3. 이벤트 확인
kubectl get events -n argocd --field-selector involvedObject.name=<name>
```

진단 후 수정은 반드시 코드 변경 → PR 경로로 진행한다. 직접 patch는 사용하지 않는다.

## 플랫폼 앱 vs 워크로드 앱 구분

| 경로                               | 용도                             | 변경 권한        |
| ---------------------------------- | -------------------------------- | ---------------- |
| `gitops/apps/root/platform-*.yaml` | 플랫폼 인프라 (ArgoCD, Istio 등) | infra 스코프만   |
| `gitops/workloads/<app>/`          | 사용자 워크로드                  | infra 스코프     |
| `gitops/clusters/local/`           | 클러스터 루트 앱                 | 신중히, ADR 필요 |

## 출력 형식

온보딩 요청 시:

```
대상 앱: <name>
생성 파일: [목록]
validation: PASS/FAIL
PR 체크리스트: [ ] kube-linter [ ] 시크릿 스캔 [ ] README 업데이트
```

## 테스트 시나리오

**정상 흐름:** 새 워크로드 `my-app` 온보딩 요청 → Workflow A 실행 → 파일 생성 → k8s-validate PASS → PR 체크리스트 출력

**에러 흐름:** sync 실패 → Workflow C 진단 → 오류 원인 특정 → 코드 수정 → PR 경로 안내
