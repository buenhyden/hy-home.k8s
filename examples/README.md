# Examples

이 디렉토리는 `hy-home.k8s` 플랫폼의 참조 구현 예시와 템플릿을 관리한다.

## 구조

```
examples/
└── sample-app/      ← GitOps 앱 온보딩 완전 예시 (템플릿)
```

## 예시 목록

| 디렉토리                       | 설명                                                      | 관련 문서                                                                                                                                                                                                                  |
| ------------------------------ | --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`sample-app/`](./sample-app/) | Rollout + AnalysisTemplate + Ingress + ESO 패턴 완전 예시 | [Guide](../docs/07.guides/0008-github-app-gitops-onboarding-guide.md) · [Runbook](../docs/09.runbooks/0010-github-app-gitops-onboarding-runbook.md) · [Policy](../docs/08.operations/0007-app-gitops-onboarding-policy.md) |

## 사용 방법

각 예시 디렉토리의 `README.md`를 참조한다.
새 앱 온보딩 시 `sample-app/`을 복사하여 플레이스홀더를 교체하는 것이 시작점이다.

```bash
cp -r examples/sample-app gitops/workloads/<appname>
```

## 참조 구현

실제 운영 중인 참조 구현:

- [`gitops/workloads/adminer/`](../gitops/workloads/adminer/) — DB 관리 UI (Rollout + AnalysisTemplate + PeerAuthentication)
