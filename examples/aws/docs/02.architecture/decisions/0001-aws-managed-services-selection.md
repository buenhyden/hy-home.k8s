# ADR-0001: AWS Managed Services and Compute Strategy Selection

## Overview (KR)

이 문서는 hy-home.k8s 시스템의 AWS 마이그레이션 과정에서 EKS 클러스터 구성 및 주요 관리형 서비스(RDS, ElastiCache)를 선택한 배경과 기술적 결정을 기록한다.

## Context

로컬 K3s/k3d 환경은 단일 노드 장애에 취약하며, 데이터베이스 및 캐시 시스템의 직접 관리에 따른 운영 부담이 크다. 클라우드로의 마이그레이션 시, 2026년 기준의 기술 성숙도와 비용 효율성을 고려하여 최적의 오퍼링을 선택할 필요가 있다.

## Decision

- **Compute**: **Amazon EKS 1.35 target**을 표준 런타임으로 선택하며, 노드 관리는 **Karpenter**로 자동화한다.
- **Relational Database**: **Amazon RDS Aurora Serverless v2 (PostgreSQL)**를 선택하여 부하에 따른 유연한 스케일링과 고가용성을 확보한다.
- **In-memory Cache**: **Amazon ElastiCache Serverless (Redis compatible)**를 사용하여 운영 오버헤드 없이 캐시 용량을 자동 조정한다.
- **Secret Management**: **AWS Secrets Manager**와 **External Secrets Operator (ESO)**를 통합하여 K8s 매니페스트 내 시크릿 관리를 자동화한다.

## Explicit Non-goals

- 멀티 클라우드(Azure, GCP) 환경과의 연동 전략 수립 (AWS 단일 리전에 집중).
- 마이크로서비스 코드의 서버리스(Lambda) 전환 (컨테이너 기반 유지).

## Consequences

- **Positive**:
  - 인프라 운영 부담(Patch, Backup, Scaling) 80% 이상 감소.
  - 가용 영역(AZ) 장애 시에도 자동 장애 조치(Failover) 가능.
  - Karpenter를 통한 리소스 사용 최적화로 클라우드 비용 효율화.
- **Trade-offs**:
  - AWS 특정 서비스에 대한 벤더 종속성(Vendor Lock-in) 증가 (관리 효율성을 위해 수용).
  - 로컬 환경 대비 초기 설정 복잡도 및 학습 곡선 존재.

## Alternatives

### Alternative 1: Self-managed Kubernetes on EC2

- Good: 초기 비용 절감 가능, 전체 인프라에 대한 완전한 제어.
- Bad: 업그레이드, 보안 패치, 노드 관리 등 운영 부담(Undifferentiated Heavy Lifting) 매우 높음.

### Alternative 2: Managed Node Groups (EKS)

- Good: AWS 기본 기능으로 안정적, 노드 그룹별 관리 가능.
- Bad: Karpenter 대비 확장 속도가 느리고 인스턴스 타입 선택의 유연성이 부족함.

## Related Documents

- **PARD**: [../01.requirements/2026-03-31-aws-migration-prd.md](../../01.requirements/2026-03-31-aws-migration-prd.md)
- **AARD**: [../02.architecture/requirements/0001-aws-cloud-native-architecture.md](../requirements/0001-aws-cloud-native-architecture.md)
- **Spec**: [../03.specs/aws-migration/spec.md](../../03.specs/aws-migration/spec.md)
