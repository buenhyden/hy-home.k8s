# Azure 비용 최적화 및 거버넌스 정책

## Overview

이 문서는 Azure 클라우드 리소스 사용에 따른 비용 효율성을 극대화하고, 프로젝트 거버넌스를 유지하기 위한 운영 지침을 상술한다.

## 1. 노드 풀 및 컴퓨팅 최적화

### 가. VM 크기 선정 (Right-sizing)

상시 모니터링을 통해 사용률이 낮은 노드 풀의 인스턴스 유형을 하향 조정한다.

### 나. Spot 인스턴스 활용

- **대상**: 개발(Dev), 테스트(QA) 환경의 `userpool`.
- **효과**: 정기적인 노드 가용성 변동을 수용하면서도 최대 90% 비용 절감 가능.

### 다. Cluster Autoscaler 활성화

- 부하가 적은 야간 시간대에 노드 수를 무중단으로 축소하여 불필요한 비용 발생 차단.

## 2. 데이터베이스 및 스토리지 최적화

### 가. PostgreSQL Burstable 티어 사용

- 서비스 초기 또는 비중요 환경은 B-시리즈 인스턴스를 사용하여 베이스라인 성능만 보장하고 비용 절감.

### 나. 삭제된 리소스 보존 기간 설정

- 백업 데이터 보존 기간을 비즈니스 요구사항에 맞춰 최적화(예: Dev 3일, Prod 30일)하여 스토리지 비용 관리.

## 3. 태깅(Tagging) 및 리소스 관리

모든 Azure 리소스에는 비용 추적을 위해 다음 태그를 필수로 부여한다.

| 태그 키 | 설명 | 예시 |
| :--- | :--- | :--- |
| **Project** | 프로젝트명 | `hy-home.k8s` |
| **Env** | 운영 환경 | `prod`, `dev`, `test` |
| **CostCenter** | 비용 정산 부서 | `platform-team` |

## 4. 관련 문서 참조

- **AARD**: [../02.architecture/requirements/0001-azure-migration-architecture.md](../../02.architecture/requirements/0001-azure-migration-architecture.md)
- **Runbook**: [../05.operations/runbooks/aks-node-replacement.md](../runbooks/aks-node-replacement.md)
- **Strategy**: [migration strategy](../../04.execution/plans/2026-03-31-migration-strategy.md)
