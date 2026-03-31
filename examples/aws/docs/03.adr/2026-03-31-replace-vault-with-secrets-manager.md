# ADR-001: Replace Local Vault with AWS Secrets Manager for AWS Environment

## Overview (KR)

이 문서는 AWS 환경 이식 시 로컬에서 사용하던 HashiCorp Vault를 AWS Secrets Manager로 교체하기 위한 아키텍처 결정 기록이다. 관리 오버헤드 감소와 AWS 네이티브 통합을 주 목적으로 한다.

## Context

현재 로컬 K3s 환경에서는 HashiCorp Vault를 별도 컨테이너로 실행하여 시크릿을 관리하고 있다. 하지만 AWS로 이식할 경우 다음 문제들이 발생한다:

1. **운영 복잡성**: EKS 내부에 Vault를 안정적으로 운영(HA 구성, Unseal 자동화 등)하기 위한 리소스와 노력이 크다.
2. **연동 편의성**: AWS의 다른 서비스(RDS, ElastiCache)와의 자격 증명 자동 로테이션 기능을 활용하기 어렵다.
3. **IAM 통합**: AWS Secrets Manager는 IAM Policy를 통한 세밀한 접근 제어가 기본적으로 지원된다.

## Decision

- AWS 환경에서는 **AWS Secrets Manager**를 기본 시크릿 저장소로 사용한다.
- Kubernetes와의 연동은 **External Secrets Operator (ESO)**를 사용하여 Secrets Manager의 시크릿을 K8s Secret으로 동기화한다.
- 기존 Vault의 시크릿 데이터를 마이그레이션 도구를 통해 AWS Secrets Manager로 이전한다.

## Explicit Non-goals

- 타 클라우드(GCP, Azure)의 Secret Manager 지원.
- Vault의 Transit Engine 등 특수 기능의 대체 (현재 필요하지 않음).

## Consequences

- **Positive**:
  - 서버리스 관리형 서비스로 운영 부담 제로.
  - RDS 자격 증명 자동 로테이션 기능 활용 가능.
  - IAM IRSA를 통한 안전한 시크릿 접근 제어.
- **Trade-offs**:
  - AWS 서비스 비용 발생 (Secrets 당 비용).
  - 로컬 환경(Vault)과 클라우드 환경(Secrets Manager) 간의 관리 도구 이원화.

## Alternatives

### Keep HashiCorp Vault on EKS

- Good: 로컬과 동일한 도구 사용, 추가 비용 억제 가능.
- Bad: 유지보수(업데이트, 백업, HA) 오버헤드가 매우 높음.

### AWS Parameter Store (SSM)

- Good: 비용이 저렴하거나 무료(Standard).
- Bad:Secrets Manager에 비해 시크릿 관리 기능(로테이션 등)이 제한적임.

## Related Documents

- **PRD**: [../01.prd/2026-03-31-aws-migration-prd.md](../01.prd/2026-03-31-aws-migration-prd.md)
- **ARD**: [../02.ard/2026-03-31-aws-migration-ard.md](../02.ard/2026-03-31-aws-migration-ard.md)
- **Spec**: [../04.specs/aws-migration/spec.md](../04.specs/aws-migration/spec.md)
