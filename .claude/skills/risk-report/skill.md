---
name: risk-report
description: >
  k8s 클러스터 리스크 레지스터 생성 스킬. RBAC 과잉 권한, 네트워크 격리 취약점, 시크릿 노출,
  단일 장애점(SPoF), 모니터링 공백을 식별하고 위험도 매트릭스로 정리한다.
  "리스크 분석", "위험 등록부", "클러스터 보안 리스크", "취약점 보고서", "risk register"를
  요청하면 반드시 이 스킬을 사용할 것. H100:88 risk-register 패턴 적용.
---

# risk-report

k8s 클러스터 리스크 레지스터. H100:88 risk-register의 risk-identifier + monitoring-planner 패턴을 적용한다.

## 왜 리스크 레지스터가 필요한가

k8s 클러스터는 여러 레이어(RBAC, 네트워크, 시크릿, 워크로드)가 상호 의존한다.
개별 설정이 정상처럼 보여도 조합 취약점이 존재한다. 이 스킬은 체계적 리스크 식별과
우선순위화로 보안 공백을 줄인다.

## 리스크 식별 영역

### 1. RBAC 과잉 권한

- ClusterRole에 `*` 리소스 또는 `*` verbs 존재 여부
- ServiceAccount가 필요 이상의 권한 보유
- `cluster-admin` 바인딩 수 최소화 확인

### 2. 네트워크 격리

- NetworkPolicy 미적용 네임스페이스 (egress/ingress 무제한)
- Istio PeerAuthentication 누락 워크로드
- 외부 서비스 접근이 명시적 ExternalName / ServiceEntry로 관리되는지

### 3. 시크릿 노출

- `check-secret-handling.sh` 결과 기반
- ExternalSecret / SealedSecret 미사용 패턴
- Secret 리소스가 etcd 암호화 정책 하에 있는지 (클러스터 수준)

### 4. 단일 장애점 (SPoF)

- `replicas: 1` 인 플랫폼 컴포넌트 (ArgoCD, ESO 등)
- PodDisruptionBudget 누락
- 외부 의존성 (Vault, Grafana) 가용성 보장 여부

### 5. 모니터링 공백

- Prometheus scrape 대상 누락 네임스페이스
- ArgoCD 알림 미설정 앱
- 로그 수집(Alloy) 미연결 워크로드

## 출력 형식: 리스크 매트릭스

```markdown
## 리스크 레지스터 — hy-home.k8s — {날짜}

| ID  | 영역 | 설명 | 가능성         | 영향           | 위험도              | 권고 조치 |
| --- | ---- | ---- | -------------- | -------------- | ------------------- | --------- |
| R01 | RBAC | ...  | 높음/중간/낮음 | 높음/중간/낮음 | 심각/높음/중간/낮음 | ...       |
```

위험도 = 가능성 × 영향 (심각 > 높음 > 중간 > 낮음)

## 실행 절차

```
1. bash scripts/check-secret-handling.sh  → R0x 시크릿 항목 도출
2. kubectl get clusterrolebindings -A     → R0x RBAC 항목 도출
3. kubectl get networkpolicies -A         → R0x 네트워크 항목 도출
4. kubectl get pods -A | grep -v Running  → R0x SPoF 항목 도출
5. 매트릭스 작성 → docs/10.incidents/ 또는 별도 보고서로 저장
```

## 에러 처리

- kubectl 접근 불가 → 매니페스트 정적 분석으로 대체 (gitops/ 기준)
- 일부 네임스페이스 접근 제한 → 접근 가능 범위만 분석 후 한계 명시

## 테스트 시나리오

**정상 흐름:** "클러스터 리스크 분석해줘" → 5개 영역 스캔 → 매트릭스 출력 → `docs/10.incidents/` 저장 제안

**에러 흐름:** kubectl 미연결 → gitops/ 매니페스트 정적 분석 → 한계 명시 후 부분 리포트 출력
