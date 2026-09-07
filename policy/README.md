---
title: "policy"
version: "0.2.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-08"
---
# policy

## Overview

`policy/`는 Kubernetes 매니페스트에 적용되는 **선언형 정책 규칙**의 소유
경로다. 규칙은 Rego로 작성되어 Conftest로 평가된다. Conftest는 선택 도구가
아니라 필수 도구이며, 없으면 `policy-gates`는 통과가 아니라 실패한다. 같은
규칙의 두 번째 구현은 존재하지 않는다.

이 폴더는 정책 *규칙*을 소유하고, 정책이 언제 어떤 레인에서 실행되는지는
`scripts/validation/registry.json`이 소유한다.

### Audience

- Platform maintainers
- Security reviewers
- Quality engineers

### Scope

#### In Scope

- 추적된 Kubernetes/ArgoCD 매니페스트에 대한 deny 규칙
- 평문 Secret, 와일드카드 AppProject 권한, `CreateNamespace=true`, `latest` 이미지 태그 금지

#### Out of Scope

- 매니페스트 구조·필드 계약 — `k8s-manifests`, `gitops-structure` 검증기 소유
- 비밀값 탐지와 baseline — `scripts/check-secret-handling.sh` 소유
- live 클러스터 admission 제어. 이 규칙은 저장소 정적 검사이며 런타임 admission을 대체하지 않는다

## Structure

| 경로 | 책임 |
| --- | --- |
| `conftest/kubernetes.rego` | `package main`의 deny 규칙 본문 |
| `conftest/kubernetes_test.rego` | 각 규칙이 여전히 발화하는지 증명하는 Rego 테스트 |

현재 강제되는 규칙:

| 대상 | 거부 조건 |
| --- | --- |
| `v1/Secret` | 평문 Secret 매니페스트 |
| `Application` | `syncOptions`에 `CreateNamespace=true` |
| `ApplicationSet` | 템플릿 `syncOptions`에 `CreateNamespace=true` |
| `AppProject` | `clusterResourceWhitelist`의 group 또는 kind 와일드카드 |
| `AppProject` | `namespaceResourceWhitelist`의 group 또는 kind 와일드카드 |
| 컨테이너 이미지 | `latest` 태그 사용 (init container 포함) |

## Configuration Boundary

- 규칙 본문은 이 폴더가 소유한다. 같은 판정을 다른 검증기에 중복 구현하지 않는다.
- `scripts/validate-policy-gates.sh`는 Conftest 실행만 소유하고 규칙은 소유하지
  않는다. Conftest를 찾지 못하면 fail closed 한다.
- 규칙을 추가하면 `kubernetes_test.rego`에 발화 사례와 비발화 사례를 함께
  추가한다. 규칙이 조용히 매칭을 멈추는 것은 커버리지 손실이다.
- 정책 위반 예외는 규칙을 끄는 방식이 아니라 매니페스트를 고치는 방식으로 해소한다.

## Validation

| 검증기 | 확인 대상 |
| --- | --- |
| `policy-gates` | 규칙 자체의 Rego 테스트와 추적된 YAML 전체의 Conftest 평가 |
| `repository-quality` | 저장소 전역 품질 규칙 |

실행:

```bash
bash scripts/validate-policy-gates.sh .
python3 scripts/qa.py full
```

PASS는 저장소 정적 증적이다. 클러스터에 실제로 admission 정책이 적용되어 있는지는
증명하지 않는다.

## Operations

- 규칙을 추가할 때는 위반 사례로 실패를 먼저 재현하고, 규칙 추가 후 통과를
  확인한다.
- Conftest는 시스템 경로 또는 `~/.local/bin/conftest`에서 해석된다. 검증 러너가
  경로를 확인해 전달하며, 해석에 실패하면 검사는 SKIP이 아니라 FAIL이다.
- 규칙 변경은 GitOps 매니페스트 전체에 영향을 주므로 변경 전 영향 범위를 확인한다.

## Related Documents

- [GitOps](../gitops/README.md)
- [Infrastructure](../infrastructure/README.md)
- [Scripts](../scripts/README.md)
- [Quality Policy](../.agents/governance/quality.md)
