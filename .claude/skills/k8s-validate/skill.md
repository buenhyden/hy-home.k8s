---
name: k8s-validate
description: >
  k8s 매니페스트 검증 스킬. kube-linter 실행, YAML 문법 검사, GitOps 구조 검증, 시크릿 패턴 스캔을 수행한다.
  매니페스트 수정 후 검증이 필요하거나, "kube-linter 실행해줘", "매니페스트 검증", "gitops 구조 확인",
  "시크릿 패턴 스캔"을 요청하면 반드시 이 스킬을 사용할 것.
  H100:26 drift-detector 패턴을 kube-linter 파이프라인으로 적용.
---

# k8s-validate

k8s manifest 검증 파이프라인. H100:26 infra-as-code의 drift-detector 패턴을 적용한다.

## 왜 이 스킬이 필요한가

kube-linter 없이 매니페스트를 커밋하면 보안 취약점(privilege escalation, host network 노출)이나
리소스 제한 누락이 ClusterDrift로 이어진다. 이 스킬은 편집 → 검증 → PR의 파이프라인을 표준화한다.

## 실행 순서

### Step 1: YAML 문법 검사

```bash
bash scripts/validate-k8s-manifests.sh [path]
```

- 대상 없으면 `gitops/` 전체 스캔
- YAML 파싱 오류 시 즉시 HALT — 문법 오류가 있는 매니페스트는 다음 단계로 넘어가지 않는다

### Step 2: kube-linter 실행

```bash
kube-linter lint <path> --config .kube-linter.yaml
```

- `.kube-linter.yaml`이 유일한 lint 기준이다. 직접 규칙을 추가하지 말 것
- **critical** 이슈: 즉시 수정 후 재검증
- **warning** 이슈: 수정 권고 + PR 설명에 명시
- **info** 이슈: 로그만 남기고 진행 가능

### Step 3: GitOps 구조 검증

```bash
bash scripts/validate-gitops-structure.sh
```

- `root-application.yaml` 존재 확인
- Application/ApplicationSet kind 확인
- Kustomization 파일 파싱 검증

### Step 4: 시크릿 패턴 스캔

```bash
bash scripts/check-secret-handling.sh [path]
```

- 플레인텍스트 시크릿 패턴 탐지
- `ExternalSecret`, `SealedSecret`, `$variable` 참조는 허용
- exit 1이면 PR 차단 — 시크릿 문제는 절대 통과시키지 않는다

## 출력 형식

```
=== k8s-validate 결과 ===
YAML 문법:    OK | ERR(파일명)
kube-linter:  PASS | WARN(N) | FAIL(N)
GitOps 구조:  OK | ERR(항목)
시크릿 스캔:  CLEAN | WARN(패턴)
전체 판정:    PASS | FAIL
```

## 에러 처리

- YAML 파싱 실패 → 해당 파일 경로와 오류 행 번호를 출력하고 HALT
- kube-linter 미설치 → 스킵 후 경고 메시지 출력 (비차단)
- 시크릿 패턴 탐지 → exit 1, PR 차단 (절대 비차단 처리 금지)

## 테스트 시나리오

**정상 흐름:** `gitops/workloads/adminer/` 매니페스트 수정 후 스킬 실행 → 4단계 모두 PASS → PR 준비 완료

**에러 흐름:** `stringData: password: mypassword` 포함 매니페스트 → Step 4 exit 1 → HALT, 수정 요청
